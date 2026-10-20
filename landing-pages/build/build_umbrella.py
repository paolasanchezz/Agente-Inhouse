"""build_umbrella.py — monta a pasta dist/ de um guarda-chuva a partir do manifesto.

Uso:
    py build_umbrella.py <manifest.json> <dist_dir>

Determinístico e stdlib-only. Absorve as regras de deploy da skill lp-publicar
(Passos 1.3-1.6): rewrite de paths pra namespace de marca, resolução de
placeholders SEO, remoção de sufixos de trabalho no <title>, cópia seletiva de
assets e composição do vercel.json. Nunca lê nada fora de landing-pages/,
brand/ e do próprio manifesto — validação de isolamento embutida.

Saída: dist/ pronta pra `vercel deploy --prebuilt` (ou inspeção de paridade).
Exit 0 = OK; exit 1 = erro de validação (mensagem no stderr).
"""
import json
import os
import re
import shutil
import sys

MARCAS = ("buzzmonitor", "buzzcreators", "cxpress", "elife")
TITLE_SUFFIXES = re.compile(r"\s*\[(?:REVISADO|TESTE|DRAFT)\]")
RELATIVE_LEAK = re.compile(r"\.\./assets/|\./assets/|\.\./\.\./brand/")
PLACEHOLDER_LEAK = re.compile(r"\{\{[A-Z_]+\}\}")

# Vercel Web Analytics em site estatico: o tracker NAO e injetado sozinho (isso
# so vale pra framework com build, via @vercel/analytics). HTML puro precisa da
# tag abaixo. Same-origin, entao o CSP dos guarda-chuvas ja cobre ('self' em
# script-src e connect-src). Opt-in por dominio: "web_analytics": true no manifesto.
VERCEL_ANALYTICS_TAG = '<script defer src="/_vercel/insights/script.js"></script>'
HEAD_CLOSE = re.compile(r"</head>", re.I)

# Âncora interna (href="#inscricao", #form...) rola sem deixar o #secao na URL — o hash
# vazava pro url_conversao do CRM e pro link copiado da barra. Vale pra TODA LP, sem
# opt-in: o script entra inline antes do último </body> (depois dos scripts da própria
# LP, que precisam ler o hash primeiro). Fonte e racional: _componentes/ancoras-sem-hash/.
ANCORAS_SEM_HASH_JS = os.path.join("landing-pages", "_componentes", "ancoras-sem-hash",
                                   "ancoras-sem-hash.js")
ANCORAS_MARCADOR = 'data-lp="ancoras-sem-hash"'
BODY_CLOSE = re.compile(r"</body>", re.I)


def die(msg):
    sys.stderr.write(f"ERRO build_umbrella: {msg}\n")
    sys.exit(1)


def read_text(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write_text(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)


def inject_web_analytics(html, slug):
    """Insere o tracker do Vercel Web Analytics antes de </head>. Idempotente."""
    if "/_vercel/insights/script.js" in html:
        return html
    if not HEAD_CLOSE.search(html):
        die(f"{slug}: web_analytics ligado mas index.html nao tem </head>")
    return HEAD_CLOSE.sub(f"{VERCEL_ANALYTICS_TAG}\n</head>", html, count=1)


def inject_ancoras_sem_hash(html, js):
    """Insere o script antes do último </body> (ou no fim, se não houver). Idempotente."""
    if ANCORAS_MARCADOR in html:
        return html
    tag = f"<script {ANCORAS_MARCADOR}>\n{js.strip()}\n</script>\n"
    fechamentos = list(BODY_CLOSE.finditer(html))
    if not fechamentos:
        return html + tag
    pos = fechamentos[-1].start()
    return html[:pos] + tag + html[pos:]


def transform_html(html, marca, slug, dominio, web_analytics=False, ancoras_js=None):
    """Regras do Passo 1.5 da lp-publicar (modo guarda-chuva)."""
    html = html.replace(f"../../brand/{marca}/assets/", f"/assets/{marca}/")
    # ./assets/{marca}/X já namespaceado: só absolutiza — antes do genérico, senão duplica
    html = html.replace(f"./assets/{marca}/", f"/assets/{marca}/")
    html = html.replace("./assets/", f"/assets/{marca}/")
    # ref bare já namespaceada (assets/{marca}/X) só ganha a barra — nunca duplicar namespace
    html = re.sub(rf'(src|href)="assets/{marca}/', rf'\1="/assets/{marca}/', html)
    html = re.sub(r'(src|href)="assets/', rf'\1="/assets/{marca}/', html)
    html = html.replace("{{DOMAIN}}", dominio)
    html = html.replace("{{OG_IMAGE_PATH}}", f"assets/{marca}/og-{slug}.png")
    html = html.replace("{{BRAND_LOGO_PNG_PATH}}", f"assets/{marca}/logos/logo-primary.png")
    html = re.sub(r"(<title>[^<]*?)" + TITLE_SUFFIXES.pattern + r"([^<]*</title>)",
                  r"\1\2", html)
    if web_analytics:
        html = inject_web_analytics(html, slug)
    if ancoras_js:
        html = inject_ancoras_sem_hash(html, ancoras_js)
    return html


def asset_refs(html, marca):
    """Todos os paths sob /assets/{marca}/ referenciados no HTML (relativos ou absolutos)."""
    return sorted(set(re.findall(rf"/assets/{marca}/([^\"'\\)\s>]+)", html)))


def main():
    if len(sys.argv) != 3:
        die("uso: build_umbrella.py <manifest.json> <dist_dir>")
    manifest_path, dist = sys.argv[1], sys.argv[2]
    manifest = json.load(open(manifest_path, encoding="utf-8"))
    repo = os.environ.get("REPO_ROOT") or os.path.abspath(
        os.path.join(os.path.dirname(manifest_path), "..", "..", ".."))
    dominio = manifest["dominio"]
    web_analytics = bool(manifest.get("web_analytics", False))
    ancoras_path = os.path.join(repo, ANCORAS_SEM_HASH_JS)
    if not os.path.isfile(ancoras_path):
        die(f"componente obrigatório não existe: {ANCORAS_SEM_HASH_JS}")
    ancoras_js = read_text(ancoras_path)
    avisos = []

    if os.path.isdir(dist):
        shutil.rmtree(dist)
    os.makedirs(dist)

    for lp in manifest["lps"]:
        slug, marca, source = lp["slug"], lp["marca"], lp["source"]
        if marca not in MARCAS:
            die(f"{slug}: marca desconhecida '{marca}'")
        src_dir = os.path.join(repo, source)
        index = os.path.join(src_dir, "index.html")
        if not os.path.isfile(index):
            die(f"{slug}: source sem index.html ({source})")
        html = read_text(index)
        if not html.lstrip("﻿ \t\r\n").lower().startswith(("<!doctype html", "<html")):
            die(f"{slug}: index.html não começa com doctype/html")
        html = transform_html(html, marca, slug, dominio, web_analytics, ancoras_js)
        if RELATIVE_LEAK.search(html):
            die(f"{slug}: path relativo sobrando pós-rewrite")
        if PLACEHOLDER_LEAK.search(html):
            die(f"{slug}: placeholder {{{{...}}}} não resolvido")
        write_text(os.path.join(dist, slug, "index.html"), html)

        # assets referenciados: brand primeiro, depois LP-local (Passos 1.3-1.4)
        for rest in asset_refs(html, marca):
            dest = os.path.join(dist, "assets", marca, rest)
            if os.path.exists(dest):
                continue
            brand_src = os.path.join(repo, "brand", marca, "assets", rest)
            local_src = os.path.join(src_dir, "assets", rest)
            src = brand_src if os.path.isfile(brand_src) else (
                local_src if os.path.isfile(local_src) else None)
            if src is None:
                avisos.append(f"{slug}: asset referenciado inexistente: {rest}")
                continue
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copyfile(src, dest)

    # extras verbatim (placeholder estrutural, assets legados de era solo, etc.)
    for dist_rel, repo_rel in sorted(manifest.get("extra_files", {}).items()):
        src = os.path.join(repo, repo_rel)
        if not os.path.isfile(src):
            die(f"extra_files: {repo_rel} não existe no repo")
        dest = os.path.join(dist, dist_rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(src, dest)

    # vercel.json do domínio (arquivo versionado apontado pelo manifesto)
    vj = os.path.join(repo, manifest["vercel_json"])
    if not os.path.isfile(vj):
        die(f"vercel_json não existe: {manifest['vercel_json']}")
    shutil.copyfile(vj, os.path.join(dist, "vercel.json"))

    # validação de isolamento (Passo 2 da lp-publicar): nada interno no dist
    proibidos = re.compile(r"\.env|credentials|\.claude|conhecimento/|meta-ads/|token", re.I)
    for base, _dirs, files in os.walk(dist):
        for f in files:
            rel = os.path.relpath(os.path.join(base, f), dist).replace("\\", "/")
            if proibidos.search(rel):
                die(f"isolamento: path suspeito no dist: {rel}")

    print(json.dumps({"dominio": dominio, "lps": len(manifest["lps"]),
                      "web_analytics": web_analytics, "avisos": avisos},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
