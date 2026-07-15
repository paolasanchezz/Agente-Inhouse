"""deploy_ci.py — deploya um guarda-chuva no Vercel a partir do manifesto, com
smoke test e rollback automático. É o único caminho de deploy no modelo CI
(PLANO-MIGRACAO-CI.md Fase 2).

Uso:
    py deploy_ci.py <manifest.json> [--dry-run] [--force-fail]

Fluxo: build (build_umbrella.py) -> captura o deploy production atual ->
`vercel deploy --prod` -> smoke test (toda LP do manifesto + redirects do
vercel.json) -> em falha, `vercel promote` do deploy anterior + exit 1.

--dry-run: builda e roda o smoke contra o live ATUAL sem deployar nada.
--force-fail: força falha do smoke pós-deploy pra ensaiar o rollback (usar só
em teste supervisionado; conteúdo deployado == build, rollback == estado anterior).

Env: VERCEL_TOKEN (obrigatório), REPO_ROOT (default: ../../.. deste arquivo).
Exit 0 = sucesso; 1 = falha (com rollback executado se houve deploy).
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

TEXT_EXT = (".html", ".json", ".svg", ".css", ".js", ".txt", ".xml")


def log(msg):
    print(f"[deploy_ci] {msg}", flush=True)


def api(path, token, team):
    sep = "&" if "?" in path else "?"
    req = urllib.request.Request(
        f"https://api.vercel.com{path}{sep}teamId={team}",
        headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def fetch(url):
    """GET sem seguir redirect. Retorna (status, location, body_bytes)."""
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    opener = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, headers={"User-Agent": "lp-deploy-ci"})
    try:
        with opener.open(req, timeout=30) as r:
            return r.status, r.headers.get("Location", ""), r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location", ""), b""
    except Exception as e:
        return 0, str(e), b""


def norm(b):
    return b.replace(b"\r\n", b"\n")


def smoke(manifest, dist, dominio):
    """Valida toda LP do manifesto + redirects do vercel.json no live."""
    falhas = []
    vj = json.load(open(os.path.join(dist, "vercel.json"), encoding="utf-8"))
    redirects = {r["source"].rstrip("/"): r["destination"]
                 for r in vj.get("redirects", [])}
    for lp in manifest["lps"]:
        slug = lp["slug"]
        status, loc, body = fetch(f"https://{dominio}/{slug}")
        esperado = redirects.get(f"/{slug}")
        if esperado:
            if status // 100 == 3 and loc.rstrip("/") == esperado.rstrip("/"):
                continue
            falhas.append(f"{slug}: esperava redirect p/ {esperado}, veio {status} {loc}")
            continue
        if status != 200:
            falhas.append(f"{slug}: HTTP {status}")
            continue
        local = open(os.path.join(dist, slug, "index.html"), "rb").read()
        if hashlib.md5(norm(body)).hexdigest() != hashlib.md5(norm(local)).hexdigest():
            falhas.append(f"{slug}: conteúdo live != build (hash normalizado)")
    for source, dest in redirects.items():
        status, loc, _ = fetch(f"https://{dominio}{source}")
        if not (status // 100 == 3 and loc.rstrip("/") == dest.rstrip("/")):
            falhas.append(f"redirect {source}: esperava {dest}, veio {status} {loc}")
    return falhas


def vercel(args, cwd, token, team):
    cmd = ["npx", "--yes", "vercel@latest", *args,
           "--token", token, "--scope", team]
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          timeout=600, shell=(os.name == "nt"))
    return proc


def main():
    manifest_path = sys.argv[1]
    dry = "--dry-run" in sys.argv
    force_fail = "--force-fail" in sys.argv
    token = os.environ["VERCEL_TOKEN"]
    repo = os.environ.get("REPO_ROOT") or os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", ".."))

    manifest = json.load(open(manifest_path, encoding="utf-8"))
    dominio, team = manifest["dominio"], manifest["vercel_org_id"]
    dist = os.path.join(tempfile.mkdtemp(prefix="lp-dist-"), "dist")

    log(f"build {dominio}...")
    proc = subprocess.run(
        [sys.executable, os.path.join(repo, "landing-pages", "build", "build_umbrella.py"),
         manifest_path, dist],
        capture_output=True, text=True, env={**os.environ, "REPO_ROOT": repo})
    if proc.returncode != 0:
        log(f"BUILD FALHOU:\n{proc.stderr}")
        sys.exit(1)
    for aviso in json.loads(proc.stdout).get("avisos", []):
        log(f"aviso build: {aviso}")

    if dry:
        log("dry-run: smoke contra o live atual (sem deploy)")
        falhas = smoke(manifest, dist, dominio)
        for f in falhas:
            log(f"FALHA: {f}")
        log("dry-run " + ("FALHOU" if falhas else "OK"))
        sys.exit(1 if falhas else 0)

    # estado anterior (pro rollback) — o deploy que o ALIAS do domínio serve agora.
    # Não usar "último deploy READY": após um rollback anterior, o último deploy
    # criado não é o que está no ar, e seria um alvo de rollback errado.
    prev = None
    try:
        alias = api(f"/v4/aliases/{dominio}", token, team)
        dep = alias.get("deployment") or {}
        if dep.get("id"):
            prev = {"uid": dep["id"], "url": dep.get("url", "")}
    except Exception as e:
        log(f"aviso: leitura do alias falhou ({e}); caindo pro último deploy READY")
    if prev is None:
        prev = api(f"/v6/deployments?projectId={manifest['projeto_vercel_id']}"
                   f"&target=production&state=READY&limit=1", token, team)["deployments"][0]
    log(f"servindo {dominio} agora (rollback target): {prev['uid']} ({prev['url']})")

    # link do projeto + deploy
    os.makedirs(os.path.join(dist, ".vercel"), exist_ok=True)
    with open(os.path.join(dist, ".vercel", "project.json"), "w", encoding="utf-8") as f:
        json.dump({"projectId": manifest["projeto_vercel_id"],
                   "orgId": manifest["vercel_org_id"]}, f)
    log("vercel deploy --prod ...")
    proc = vercel(["deploy", "--prod", "--yes"], dist, token, team)
    deploy_url = (proc.stdout.strip().splitlines() or [""])[-1]
    if proc.returncode != 0 or not deploy_url.startswith("https://"):
        log(f"DEPLOY FALHOU (nada publicado, live intacto):\n{proc.stderr[-2000:]}")
        sys.exit(1)
    log(f"deploy ok: {deploy_url}")

    falhas = smoke(manifest, dist, dominio)
    if force_fail:
        log("--force-fail: simulando falha de smoke pra ensaiar rollback")
        falhas = falhas or ["falha simulada (--force-fail)"]
    if not falhas:
        log(f"SMOKE OK — {len(manifest['lps'])} LPs validadas em {dominio}")
        sys.exit(0)

    for f in falhas:
        log(f"FALHA SMOKE: {f}")
    log(f"ROLLBACK: promote {prev['uid']} ...")
    proc = vercel(["promote", f"https://{prev['url']}", "--yes"], dist, token, team)
    if proc.returncode != 0:
        log(f"ROLLBACK FALHOU — INTERVENÇÃO MANUAL URGENTE (promote {prev['uid']} "
            f"na UI Vercel):\n{proc.stderr[-2000:]}")
        sys.exit(1)
    # pós-rollback: todas as URLs devem responder (200 ou redirect)
    vivos = sum(1 for lp in manifest["lps"]
                if fetch(f"https://{dominio}/{lp['slug']}")[0] in
                (200, 301, 302, 307, 308))
    log(f"rollback concluído — {vivos}/{len(manifest['lps'])} URLs respondendo")
    sys.exit(1)


if __name__ == "__main__":
    main()
