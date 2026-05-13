"""Descoberta dinamica de URLs de LP em producao via Vercel API.

Le do ambiente:
  VERCEL_TOKEN — token Vercel ja validado (resolver via SKILL.md antes)
  ORG_ID       — team id (default: team_nC991VqUuSU2jXZN152xqqEg da elife-group)

Saida: imprime JSON em stdout com:
  {
    "urls": [
      {"project": "cxpress-lp-playbook-whatsapp2026",
       "domain": "content.cxpress.io",
       "slug": "playbook-whatsapp2026",   # vazio se modo solo
       "mode": "guarda-chuva" | "solo",
       "url": "https://content.cxpress.io/playbook-whatsapp2026"},
      ...
    ],
    "skipped": [
      {"project": "...", "reason": "sem alias FQDN" | "sem deploy READY" | "..."}
    ],
    "errors": [...]
  }

Filtro de projeto-LP: projeto da org que tem pelo menos um alias FQDN custom
(nao apenas *.vercel.app). Projetos sem FQDN custom sao skipados.
"""

import json
import os
import sys
import urllib.request
import urllib.error


TEAM_ID_DEFAULT = "team_nC991VqUuSU2jXZN152xqqEg"


def api_get(url, token):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def list_projects(token, team_id):
    """Pagina por todos os projetos da org."""
    projects = []
    cursor = None
    while True:
        url = f"https://api.vercel.com/v9/projects?teamId={team_id}&limit=100"
        if cursor:
            url += f"&until={cursor}"
        data = api_get(url, token)
        projects.extend(data.get("projects", []))
        pagination = data.get("pagination") or {}
        cursor = pagination.get("next")
        if not cursor:
            break
    return projects


def custom_domains_for_project(token, team_id, project_id):
    """Retorna lista de FQDNs custom (exclui *.vercel.app)."""
    url = f"https://api.vercel.com/v9/projects/{project_id}/domains?teamId={team_id}&limit=100"
    data = api_get(url, token)
    domains = []
    for d in data.get("domains", []):
        name = d.get("name", "")
        if not name or name.endswith(".vercel.app"):
            continue
        # priorizar dominios verificados sem redirect
        if d.get("verified") is False:
            continue
        if d.get("redirect"):
            continue
        domains.append(name)
    return domains


def latest_production_deploy(token, team_id, project_id):
    url = (
        f"https://api.vercel.com/v6/deployments"
        f"?projectId={project_id}&teamId={team_id}"
        f"&target=production&state=READY&limit=1"
    )
    data = api_get(url, token)
    deployments = data.get("deployments", [])
    return deployments[0]["uid"] if deployments else None


def list_slugs_from_deploy(token, team_id, deploy_id):
    """Walk no file tree do deploy.

    Retorna lista de slugs (subpastas com index.html dentro).
    Se houver index.html na raiz apos o envelope src/, retorna [""] (modo solo).
    """
    tree = api_get(
        f"https://api.vercel.com/v6/deployments/{deploy_id}/files?teamId={team_id}",
        token,
    )

    # Vercel envelopa tudo num diretorio "src" no topo
    root_children = []
    for root_node in tree if isinstance(tree, list) else [tree]:
        if root_node.get("type") == "directory" and root_node.get("name") == "src":
            root_children.extend(root_node.get("children") or [])
        else:
            root_children.append(root_node)

    slugs = []
    has_root_index = False

    for node in root_children:
        t = node.get("type")
        name = node.get("name", "")
        if t == "file" and name == "index.html":
            has_root_index = True
        elif t == "directory":
            # checar se a subpasta tem index.html direto
            for child in node.get("children") or []:
                if child.get("type") == "file" and child.get("name") == "index.html":
                    slugs.append(name)
                    break

    # modo solo: index.html na raiz E nenhum subpasta com index = LP unica
    # modo guarda-chuva: subpastas com index = N LPs
    # caso misto (raro): raiz tem index + subpastas tambem; reportar ambos
    if has_root_index and not slugs:
        return [""]  # solo: URL = https://{dominio}/
    return slugs


def discover(token, team_id):
    urls = []
    skipped = []
    errors = []

    try:
        projects = list_projects(token, team_id)
    except urllib.error.HTTPError as e:
        return {
            "urls": [],
            "skipped": [],
            "errors": [f"falha ao listar projetos (HTTP {e.code}): {e.reason}"],
        }
    except Exception as e:
        return {"urls": [], "skipped": [], "errors": [f"erro inesperado: {e}"]}

    for proj in projects:
        proj_id = proj.get("id")
        proj_name = proj.get("name", proj_id)

        try:
            domains = custom_domains_for_project(token, team_id, proj_id)
        except Exception as e:
            errors.append(f"{proj_name}: falha ao listar dominios — {e}")
            continue

        if not domains:
            skipped.append({"project": proj_name, "reason": "sem alias FQDN custom"})
            continue

        try:
            deploy_id = latest_production_deploy(token, team_id, proj_id)
        except Exception as e:
            errors.append(f"{proj_name}: falha ao buscar deploy — {e}")
            continue

        if not deploy_id:
            skipped.append({"project": proj_name, "reason": "sem deploy production READY"})
            continue

        try:
            slugs = list_slugs_from_deploy(token, team_id, deploy_id)
        except Exception as e:
            errors.append(f"{proj_name}: falha ao listar arquivos do deploy {deploy_id} — {e}")
            continue

        if not slugs:
            skipped.append({"project": proj_name, "reason": "deploy sem index.html"})
            continue

        # Para cada dominio custom e cada slug, gerar URL
        # Em guarda-chuva multi-dominio (raro) cada slug ganha N URLs (uma por dominio)
        # Convencao atual: 1 dominio principal por projeto. Pegamos o primeiro.
        primary_domain = domains[0]
        for slug in slugs:
            if slug == "":
                url = f"https://{primary_domain}/"
                mode = "solo"
            else:
                url = f"https://{primary_domain}/{slug}"
                mode = "guarda-chuva"
            urls.append({
                "project": proj_name,
                "domain": primary_domain,
                "slug": slug,
                "mode": mode,
                "url": url,
            })

    return {"urls": urls, "skipped": skipped, "errors": errors}


def main():
    token = os.environ.get("VERCEL_TOKEN")
    if not token:
        print(json.dumps({"urls": [], "skipped": [], "errors": ["VERCEL_TOKEN nao definido no ambiente"]}))
        sys.exit(1)
    team_id = os.environ.get("ORG_ID") or TEAM_ID_DEFAULT
    result = discover(token, team_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
