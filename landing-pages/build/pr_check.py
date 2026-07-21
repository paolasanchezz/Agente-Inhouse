"""pr_check.py — decide se um PR pode ser auto-mergeado pelo merge-bot de LPs.

Uso (na raiz do repo, com origin/main fetchado):
    py landing-pages/build/pr_check.py <base_ref>

Regras (PLANO-MIGRACAO-CI.md §1.2, decisão do Victor 2026-07-15):
- PATHS LIVRES (conteúdo — auto-merge se validações passarem):
    landing-pages/{marca}/**        (HTML, copy, assets de LP)
    landing-pages/dominios/*/manifest.json
    brand/*/assets/**               (logos, mascotes, imagens de marca)
- Todo o resto é MECÂNICA (skills, hooks, build/, .github/, vercel.json,
  MIGRADOS.json, extras/, tokens de design, conhecimento/) → revisão do Victor.
- Remoção de slug de manifesto NUNCA auto-mergeia (despublicação é decisão humana).

Saída: JSON {livre, motivos[], remocoes_slug[], dominios_afetados[]} em stdout.
Exit 0 sempre que a análise rodou (a decisão fica no JSON); exit 2 em erro interno.
"""
import json
import os
import re
import subprocess
import sys

import check_gtm_region  # gate GTM x regiao (modulo local, mesmo diretorio)

MARCAS = ("buzzmonitor", "buzzcreators", "cxpress", "elife", "_experimentos")
LIVRES = [
    re.compile(r"^landing-pages/(%s)/" % "|".join(MARCAS)),
    re.compile(r"^landing-pages/dominios/[^/]+/manifest\.json$"),
    re.compile(r"^brand/[^/]+/assets/"),
]


def git(*args):
    proc = subprocess.run(["git", *args], capture_output=True, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        sys.exit(2)
    return proc.stdout


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    repo = os.environ.get("REPO_ROOT", ".")
    changed = [l for l in git("diff", "--name-only", f"{base}...HEAD").splitlines() if l]

    motivos, remocoes = [], []
    for path in changed:
        if not any(rx.match(path) for rx in LIVRES):
            motivos.append(f"path protegido: {path}")

    # remoção de slug em manifesto = despublicação → nunca auto-merge
    for path in changed:
        if re.match(r"^landing-pages/dominios/[^/]+/manifest\.json$", path):
            try:
                antes = {lp["slug"] for lp in json.loads(
                    git("show", f"{base}:{path}"))["lps"]}
            except SystemExit:
                antes = set()  # manifesto novo
            try:
                depois = {lp["slug"] for lp in
                          json.load(open(os.path.join(repo, path), encoding="utf-8"))["lps"]}
            except FileNotFoundError:
                depois = set()
                motivos.append(f"manifesto removido: {path}")
            for slug in sorted(antes - depois):
                remocoes.append(f"{path}: slug '{slug}' removido")

    # Gate GTM x regiao: LP tocada no diff com container divergente da regiao NAO
    # auto-mergeia (o pixel iria pra unidade errada). Grandfathered nao conta.
    lp_touched = {}
    for path in changed:
        mm = re.match(r"^landing-pages/(%s)/([^/]+)/" % "|".join(check_gtm_region.MARCAS), path)
        if mm:
            lp_touched[(mm.group(1), mm.group(2))] = os.path.join(
                repo, "landing-pages", mm.group(1), mm.group(2))
    for (marca, slug), lp_dir in sorted(lp_touched.items()):
        if not os.path.isfile(os.path.join(lp_dir, "index.html")):
            continue  # LP removida — nao checa
        res = check_gtm_region.evaluate(repo, lp_dir, slug, marca)
        if check_gtm_region.is_blocking(res):
            motivos.append("GTM x regiao: " + check_gtm_region.human(res))

    # domínios migrados afetados pelo diff (pro dispatch pós-merge)
    migrados_path = os.path.join(repo, "landing-pages", "dominios", "MIGRADOS.json")
    migrados = json.load(open(migrados_path, encoding="utf-8")) if os.path.isfile(migrados_path) else []
    afetados = []
    for dominio in migrados:
        dom_key = dominio.replace(".", "-")
        man = json.load(open(os.path.join(
            repo, "landing-pages", "dominios", dom_key, "manifest.json"), encoding="utf-8"))
        fontes = [lp["source"] + "/" for lp in man["lps"]]
        fontes.append(f"landing-pages/dominios/{dom_key}/")
        marcas_dom = {lp["marca"] for lp in man["lps"]}
        fontes.extend(f"brand/{m}/assets/" for m in marcas_dom)
        if any(any(c.startswith(f) for f in fontes) for c in changed):
            afetados.append(dominio)

    print(json.dumps({
        "livre": not motivos and not remocoes,
        "motivos": motivos,
        "remocoes_slug": remocoes,
        "dominios_afetados": afetados,
        "arquivos": len(changed),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
