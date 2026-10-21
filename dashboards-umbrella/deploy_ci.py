#!/usr/bin/env python3
"""deploy_ci.py — build + deploy + smoke + rollback do guarda-chuva das dashboards CM.

Irmao de landing-pages/build/deploy_ci.py, de onde vem a espinha (api/fetch/vercel, descoberta
do alvo de rollback pelo ALIAS, smoke com retry, promote). Tres coisas sao diferentes aqui:

  1. Builder: dashboards-umbrella/build_umbrella.py <dist> (1 argumento, saida em texto).
     REUSADO e "nao consegui ler gerado_em" saem com exit 0 e so aparecem como texto — aqui
     viram falha. A dist e sempre efemera, entao um exportador que nao rodou nao acha JSON
     nem na fonte nem na dist e o build morre sozinho; o grep e o cinto e suspensorio.
  2. Smoke com Basic Auth. Sem o header, tudo responde 401 e o rollback dispararia sempre.
  3. Criterio de smoke de dashboard, nao de LP: 401 sem auth, X-Robots-Tag noindex, e por
     rota 308 sem barra + 200 com barra + o index.html E o JSON de dados servidos byte a byte
     iguais aos da dist. O hash do JSON prova que o que esta no ar e exatamente o que o
     validar_contrato.py aprovou minutos antes.

Uso:
    py dashboards-umbrella/deploy_ci.py                    # build + deploy + smoke (+ rollback)
    py dashboards-umbrella/deploy_ci.py --dry-run          # so o build (nada vai pro ar)
    py dashboards-umbrella/deploy_ci.py --force-fail       # deploya e simula falha p/ ensaiar o rollback
    py dashboards-umbrella/deploy_ci.py --checar-producao  # smoke estrutural do que esta no ar, sem hash
Env: VERCEL_TOKEN (deploy), DASHBOARD_BASIC_AUTH_USER/_PASS (build e smoke; fallback .env.local).
Os dados-*.json precisam ter sido exportados e validados antes. Sai 1 em qualquer falha.

Nunca roda da pasta-fonte nem de dentro do repo: a dist vai para um diretorio temporario
(o build_umbrella.py recusa caminho dentro do repo de qualquer jeito).
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
UMB = REPO / "dashboards-umbrella"
MANIFEST = UMB / "manifest.json"
SMOKE_BACKOFF = (0, 3, 8, 15)  # espera (s) antes de cada tentativa: o alias leva segundos pra virar


def log(msg: str) -> None:
    print(f"[deploy_ci] {msg}", flush=True)


# ---------------------------------------------------------------- vercel / http

def api(path: str, token: str, team: str) -> dict:
    sep = "&" if "?" in path else "?"
    req = urllib.request.Request(f"https://api.vercel.com{path}{sep}teamId={team}",
                                 headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def vercel(args: list[str], cwd: str, token: str, team: str) -> subprocess.CompletedProcess:
    cmd = ["npx", "--yes", "vercel@latest", *args, "--token", token, "--scope", team]
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=600,
                          shell=(os.name == "nt"))


def fetch(url: str, basic: str | None = None) -> tuple[int, dict, bytes]:
    """GET sem seguir redirect. (status, headers, corpo). Nunca levanta."""
    class SemRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    headers = {"User-Agent": "dashboards-deploy-ci", "Cache-Control": "no-cache"}
    if basic:
        headers["Authorization"] = f"Basic {basic}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.build_opener(SemRedirect).open(req, timeout=30) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), b""
    except Exception as e:
        return 0, {"erro": str(e)}, b""


def credencial_basic() -> str:
    user = os.environ.get("DASHBOARD_BASIC_AUTH_USER")
    pw = os.environ.get("DASHBOARD_BASIC_AUTH_PASS")
    env_local = REPO / ".env.local"
    if (not user or not pw) and env_local.exists():
        for linha in env_local.read_text(encoding="utf-8").splitlines():
            if not user and linha.startswith("DASHBOARD_BASIC_AUTH_USER="):
                user = linha.split("=", 1)[1].strip()
            if not pw and linha.startswith("DASHBOARD_BASIC_AUTH_PASS="):
                pw = linha.split("=", 1)[1].strip()
    if not user or not pw:
        log("ERRO: DASHBOARD_BASIC_AUTH_USER/_PASS ausentes (env ou .env.local)")
        sys.exit(1)
    return base64.b64encode(f"{user}:{pw}".encode()).decode()


def norm(b: bytes) -> bytes:
    return b.replace(b"\r\n", b"\n")


def md5(b: bytes) -> str:
    return hashlib.md5(norm(b)).hexdigest()


def cabecalho(headers: dict, nome: str) -> str:
    return next((v for k, v in headers.items() if k.lower() == nome.lower()), "")


# ---------------------------------------------------------------- build

def build(dist: str) -> None:
    log(f"build -> {dist}")
    proc = subprocess.run([sys.executable, str(UMB / "build_umbrella.py"), dist],
                          capture_output=True, text=True, encoding="utf-8")
    saida = (proc.stdout or "") + (proc.stderr or "")
    for linha in saida.splitlines():
        log(f"  {linha}")
    if proc.returncode != 0:
        log("BUILD FALHOU (nada publicado, live intacto)")
        sys.exit(1)
    # REUSADO / gerado_em ilegivel saem com exit 0: num pipeline desassistido, isso e dado
    # velho indo pro ar como se fosse de hoje.
    if "AVISO build_umbrella:" in saida:
        log("BUILD COM AVISO — tratado como falha no CI (REUSADO = um exportador nao produziu o JSON)")
        sys.exit(1)


# ---------------------------------------------------------------- smoke

def alvos_smoke(man: dict, dist: str | None) -> list[tuple]:
    """(nome, caminho, com_auth, checagem). dist=None => smoke estrutural, sem hash."""
    alvos = [
        ("raiz sem auth = 401", "/", False, ("status", 401)),
        ("raiz com auth = 200 + noindex", "/", True, ("raiz", None)),
        ("nav.js", "/nav.js", True, ("arquivo", "nav.js")),
    ]
    for d in man["dashboards"]:
        s = d["slug"]
        alvos += [
            (f"/{s} sem barra = 308", f"/{s}", True, ("redirect", f"/{s}/")),
            (f"/{s}/ = index da dist", f"/{s}/", True, ("arquivo", f"{s}/index.html")),
            (f"/{s}/{d['dados']} = JSON validado", f"/{s}/{d['dados']}", True,
             ("arquivo", f"{s}/{d['dados']}")),
        ]
    return alvos


def checar(base: str, alvo: tuple, basic: str, dist: str | None) -> str | None:
    nome, caminho, com_auth, (tipo, arg) = alvo
    status, headers, corpo = fetch(base + caminho, basic if com_auth else None)
    if tipo == "status":
        return None if status == arg else f"{nome}: veio {status}"
    if tipo == "redirect":
        loc = cabecalho(headers, "Location")
        if status == 308 and loc.rstrip().endswith(arg):
            return None
        return f"{nome}: veio {status} {loc!r} (trailingSlash fora do lugar quebra os caminhos relativos)"
    if status != 200:
        return f"{nome}: HTTP {status}"
    if tipo == "raiz":
        if "noindex" not in cabecalho(headers, "X-Robots-Tag").lower():
            return f"{nome}: sem X-Robots-Tag noindex"
        arg = "index.html"
    if dist is not None:
        local = Path(dist, arg).read_bytes()
        if md5(corpo) != md5(local):
            return f"{nome}: servido != dist (alias ainda no deploy anterior?)"
    elif tipo == "arquivo" and arg.endswith("index.html") and b"/nav.js" not in corpo:
        return f"{nome}: index sem /nav.js injetado"
    return None


def smoke(base: str, man: dict, basic: str, dist: str | None, backoff=SMOKE_BACKOFF) -> list[str]:
    """Tenta em rodadas com espera crescente; cada rodada re-checa SO o que ainda falha.

    Sem retry, o deploy derruba a si mesmo: o alias leva alguns segundos para servir a versao
    nova, o hash do JSON bate com a VELHA, o smoke falha e o rollback descarta um deploy bom
    (foi o incidente do lp-deploy corrigido em 2026-09-14).
    """
    alvos = alvos_smoke(man, dist)
    falhas: list[str] = []
    for i, espera in enumerate(backoff):
        if espera:
            # Na 1a rodada nada foi checado ainda: dizer "ainda falhando" ali mentiria no log
            # (o ensaio de rollback de 2026-10-21 imprimiu "24 ainda falhando" antes de tentar).
            log(f"smoke: aguardando {espera}s antes da primeira checagem" if i == 0 else
                f"smoke: {len(alvos)} alvo(s) ainda falhando — nova tentativa em {espera}s")
            time.sleep(espera)
        falhas, restantes = [], []
        for alvo in alvos:
            erro = checar(base, alvo, basic, dist)
            if erro:
                falhas.append(erro)
                restantes.append(alvo)
        if not restantes:
            return []
        alvos = restantes
    return falhas


# ---------------------------------------------------------------- main

def main() -> int:
    dry = "--dry-run" in sys.argv
    force_fail = "--force-fail" in sys.argv
    so_checar = "--checar-producao" in sys.argv
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    dominio, team, projeto = man["dominio"], man["vercel_org_id"], man["projeto_vercel_id"]
    base = f"https://{dominio}"
    basic = credencial_basic()

    if so_checar:
        log(f"smoke estrutural de {base} (sem comparar hash — o que esta no ar agora)")
        falhas = smoke(base, man, basic, None, backoff=(0,))
        for f in falhas:
            log(f"FALHA: {f}")
        n = len(alvos_smoke(man, None))
        log(f"{n - len(falhas)}/{n} checagens ok")
        return 1 if falhas else 0

    dist = os.path.join(tempfile.mkdtemp(prefix="dashboards-dist-"), "dist")
    build(dist)
    if dry:
        log("dry-run: build ok, nada publicado")
        return 0

    token = os.environ.get("VERCEL_TOKEN")
    if not token:
        log("ERRO: VERCEL_TOKEN ausente")
        return 1

    # Alvo de rollback = o deploy que o ALIAS serve agora. Nao usar "ultimo deploy READY":
    # depois de um rollback anterior, o ultimo criado nao e o que esta no ar.
    prev = None
    try:
        dep = api(f"/v4/aliases/{dominio}", token, team).get("deployment") or {}
        if dep.get("id"):
            prev = {"uid": dep["id"], "url": dep.get("url", "")}
    except Exception as e:
        log(f"aviso: leitura do alias falhou ({e}); caindo pro ultimo deploy READY")
    if prev is None:
        deps = api(f"/v6/deployments?projectId={projeto}&target=production&state=READY&limit=1",
                   token, team).get("deployments", [])
        prev = {"uid": deps[0]["uid"], "url": deps[0]["url"]} if deps else None
    log(f"servindo {dominio} agora (alvo de rollback): "
        + (f"{prev['uid']} ({prev['url']})" if prev else "nenhum — primeiro deploy"))

    os.makedirs(os.path.join(dist, ".vercel"), exist_ok=True)
    with open(os.path.join(dist, ".vercel", "project.json"), "w", encoding="utf-8") as f:
        json.dump({"projectId": projeto, "orgId": team}, f)
    log("vercel deploy --prod ...")
    proc = vercel(["deploy", "--prod", "--yes"], dist, token, team)
    deploy_url = (proc.stdout.strip().splitlines() or [""])[-1]
    if proc.returncode != 0 or not deploy_url.startswith("https://"):
        log(f"DEPLOY FALHOU (nada publicado, live intacto):\n{proc.stderr[-2000:]}")
        return 1
    log(f"deploy ok: {deploy_url}")

    falhas = smoke(base, man, basic, dist)
    if force_fail:
        log("--force-fail: simulando falha de smoke para ensaiar o rollback")
        falhas = falhas or ["falha simulada (--force-fail)"]
    if not falhas:
        log(f"SMOKE OK — {len(man['dashboards'])} dashboards no ar, JSONs servidos = JSONs validados")
        return 0

    for f in falhas:
        log(f"FALHA SMOKE: {f}")
    if prev is None:
        log("sem deploy anterior — nao ha rollback; o deploy novo fica no ar. Corrija e re-deploye.")
        return 1
    log(f"ROLLBACK: promote {prev['uid']} ...")
    proc = vercel(["promote", f"https://{prev['url']}", "--yes"], dist, token, team)
    if proc.returncode != 0:
        log(f"ROLLBACK FALHOU — INTERVENCAO MANUAL URGENTE (promote {prev['uid']} na UI da "
            f"Vercel):\n{proc.stderr[-2000:]}")
        return 1
    # Checagem estrutural do estado RESTAURADO (a versao anterior), nao do deploy que falhou.
    restante = smoke(base, man, basic, None, backoff=(3, 8))
    n = len(alvos_smoke(man, None))
    log(f"rollback concluido — versao ANTERIOR no ar: {n - len(restante)}/{n} checagens ok"
        + ("" if not restante else f" (ainda falhando: {'; '.join(restante)})"))
    return 1


if __name__ == "__main__":
    sys.exit(main())
