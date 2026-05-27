"""Cross-check deterministico entre fontes no repo e deploys em producao.

Substitui a composicao manual de drift que antes era prosa no SKILL.md (fragil e
ruidosa). Le o output do discover.py via stdin e escaneia landing-pages/ no disco.

Entrada (stdin): JSON do discover.py — {"urls": [...], "skipped": [...], ...}
Saida (stdout): JSON — lista de itens de drift:
  [{"kind": "...", "item": "marca/slug" | "slug", "note": "..."}]

Categorias (kind):
  fonte_sem_deploy  — ACIONAVEL. index.html no repo sem deploy em producao em nenhum
                      lugar (nem custom, nem vercel.app). Provavel rascunho/despublicada.
  deploy_orfao      — ACIONAVEL. slug deployado num guarda-chuva sem source no repo.
  vercel_app_only   — INFORMATIVO. source no repo deployado APENAS em *.vercel.app
                      (projeto sem dominio custom). Nao e falha — e um estado legitimo
                      (preview/experimento). Nao dispara email.

Slugs com prefixo "_" (ex: _placeholder, raiz de guarda-chuva) sao estruturais e
ignorados dos dois lados — nao sao LPs de verdade.

A definicao de "acionavel" vive em ACTIONABLE_KINDS e e compartilhada com notify.py.
"""

import json
import os
import sys

BENIGN_PREFIX = "_"
ACTIONABLE_KINDS = ("fonte_sem_deploy", "deploy_orfao")


def local_sources(base="landing-pages"):
    """Retorna lista de (marca, slug) com index.html em landing-pages/{marca}/{slug}/."""
    out = []
    if not os.path.isdir(base):
        return out
    for marca in sorted(os.listdir(base)):
        mpath = os.path.join(base, marca)
        if not os.path.isdir(mpath):
            continue
        for slug in sorted(os.listdir(mpath)):
            if os.path.isfile(os.path.join(mpath, slug, "index.html")):
                out.append((marca, slug))
    return out


def solo_matches(slug, solo_projects):
    """Heuristica de match pra deploy modo solo (serve na raiz, slug vazio).

    Projetos costumam ter prefixo de marca (ex: cxpress-lp-playbook-whatsapp2026),
    entao casamos por igualdade ou sufixo com separador. Conservador de proposito.
    """
    for p in solo_projects:
        if p == slug or p.endswith("-" + slug) or p.endswith("_" + slug):
            return True
    return False


def main():
    try:
        disc = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(json.dumps([{"kind": "erro", "item": "stdin", "note": f"JSON invalido: {e}"}]))
        sys.exit(1)

    urls = disc.get("urls", [])
    skipped = disc.get("skipped", [])

    deployed_slugs = {u["slug"] for u in urls if u.get("slug")}
    solo_projects = {u["project"] for u in urls if u.get("slug") == ""}
    # projetos que existem no Vercel mas so em *.vercel.app (sem FQDN custom)
    vercelapp_projects = {
        s.get("project") for s in skipped if "FQDN" in (s.get("reason") or "")
    }

    sources = local_sources()
    source_slugs = {slug for (_m, slug) in sources}

    drift = []

    # --- lado fonte: fonte_sem_deploy / vercel_app_only ---
    for marca, slug in sources:
        if slug.startswith(BENIGN_PREFIX):
            continue
        if slug in deployed_slugs:
            continue  # casa com deploy guarda-chuva
        if solo_projects and solo_matches(slug, solo_projects):
            continue  # casa com deploy solo
        if slug in vercelapp_projects:
            drift.append({
                "kind": "vercel_app_only",
                "item": f"{marca}/{slug}",
                "note": "no ar so em *.vercel.app (sem dominio custom) - informativo",
            })
            continue
        drift.append({
            "kind": "fonte_sem_deploy",
            "item": f"{marca}/{slug}",
            "note": "index.html no repo sem deploy em producao",
        })

    # --- lado deploy: deploy_orfao ---
    for u in urls:
        slug = u.get("slug")
        if not slug:
            continue  # solo serve na raiz; nao ha slug pra orfanar
        if slug.startswith(BENIGN_PREFIX):
            continue  # placeholder estrutural do guarda-chuva
        if slug in source_slugs:
            continue
        drift.append({
            "kind": "deploy_orfao",
            "item": slug,
            "note": f"deploy em {u.get('domain', '?')}/{slug} sem source no repo",
        })

    print(json.dumps(drift, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
