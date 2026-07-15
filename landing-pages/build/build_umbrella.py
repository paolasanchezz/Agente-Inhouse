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


def transform_html(html, marca, slug, dominio):
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
        html = transform_html(html, marca, slug, dominio)
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
                      "avisos": avisos}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
