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
import time
import urllib.request

import check_gtm_region  # gate GTM x regiao (modulo local, mesmo diretorio)

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


SMOKE_BACKOFF = (0, 3, 8, 15)  # espera (s) antes de cada tentativa do smoke


def _check_lp(dominio, slug, dist, redirects):
    """Valida 1 slug no live. Devolve string de erro ou None."""
    status, loc, body = fetch(f"https://{dominio}/{slug}")
    esperado = redirects.get(f"/{slug}")
    if esperado:
        if status // 100 == 3 and loc.rstrip("/") == esperado.rstrip("/"):
            return None
        return f"{slug}: esperava redirect p/ {esperado}, veio {status} {loc}"
    if status != 200:
        return f"{slug}: HTTP {status}"
    local = open(os.path.join(dist, slug, "index.html"), "rb").read()
    if hashlib.md5(norm(body)).hexdigest() != hashlib.md5(norm(local)).hexdigest():
        return f"{slug}: conteudo live != build (hash normalizado)"
    return None


def _check_redirect(dominio, source, dest):
    status, loc, _ = fetch(f"https://{dominio}{source}")
    if status // 100 == 3 and loc.rstrip("/") == dest.rstrip("/"):
        return None
    return f"redirect {source}: esperava {dest}, veio {status} {loc}"


def smoke(manifest, dist, dominio, backoff=SMOKE_BACKOFF):
    """Valida toda LP do manifesto + redirects do vercel.json no live.

    Roda em TENTATIVAS com espera crescente. O alias do dominio leva alguns
    segundos pra passar a servir o deploy novo, e nesse intervalo um slug que
    acabou de nascer responde 404 (e um slug alterado ainda devolve o HTML
    velho, falhando o hash). Sem retry, LP nova derruba o proprio deploy: o
    smoke falha, o rollback promove o deploy anterior e a LP some — com o log
    dizendo "N/N URLs respondendo", que e do estado JA revertido.

    Cada tentativa re-checa SO o que ainda falha; o que ja passou nao repete.
    Devolve [] (tudo ok) ou a lista de falhas da ultima tentativa.
    """
    vj = json.load(open(os.path.join(dist, "vercel.json"), encoding="utf-8"))
    redirects = {r["source"].rstrip("/"): r["destination"]
                 for r in vj.get("redirects", [])}
    alvos = [("lp", lp["slug"]) for lp in manifest["lps"]]
    alvos += [("redirect", source) for source in redirects]

    falhas = []
    for espera in backoff:
        if espera:
            log(f"smoke: {len(alvos)} alvo(s) ainda falhando - nova tentativa em {espera}s")
            time.sleep(espera)
        falhas, restantes = [], []
        for tipo, chave in alvos:
            erro = (_check_redirect(dominio, chave, redirects[chave])
                    if tipo == "redirect"
                    else _check_lp(dominio, chave, dist, redirects))
            if erro:
                falhas.append(erro)
                restantes.append((tipo, chave))
        if not restantes:
            return []
        alvos = restantes
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

    # Gate GTM x regiao (CONTEXT §5.4) — antes de QUALQUER deploy. Container errado
    # (LP traduzida que herdou o pixel da origem) aborta aqui, com o live intacto.
    # Selos .tracking.lock sao read-only aqui (grandfather de estados pre-existentes).
    gres = [check_gtm_region.evaluate(repo, d, s, m)
            for (d, s, m) in check_gtm_region.lps_from_manifest(repo, manifest_path)]
    gbloq, gavisos, _gok = check_gtm_region.gate(gres)
    for a in gavisos:
        log(f"aviso GTM: {a}")
    if gbloq:
        log("GATE GTM BLOQUEOU (nada publicado, live intacto):")
        for b in gbloq:
            log(f"  {b}")
        sys.exit(1)

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
        deps = api(f"/v6/deployments?projectId={manifest['projeto_vercel_id']}"
                   f"&target=production&state=READY&limit=1", token, team)["deployments"]
        prev = deps[0] if deps else None
    if prev is None:
        # Guarda-chuva NOVO: projeto sem nenhum deploy de producao ainda (1o deploy).
        # Nao ha alvo de rollback — se o smoke falhar, o deploy novo fica no ar mesmo
        # (nada estava antes; nao ha estado bom pra restaurar). Fix = re-deploy.
        log(f"{dominio}: primeiro deploy do guarda-chuva (sem deploy de producao anterior) — "
            f"sem alvo de rollback")
    else:
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
    if prev is None:
        log("sem deploy anterior (primeiro deploy do guarda-chuva) — nao ha rollback a "
            "fazer; o deploy novo fica no ar. Corrija o source e re-deploye.")
        sys.exit(1)
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
