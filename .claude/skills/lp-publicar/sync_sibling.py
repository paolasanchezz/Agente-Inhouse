"""Sync da sibling guarda-chuva com o ultimo deploy production via Vercel API.

Usado pelo Passo 0.5.d.iii do lp-publicar. Le entrada via env vars:
  DEPLOY_ID    — uid do deployment production READY (ex: dpl_abc123)
  ORG_ID       — team id (ex: team_nC991VqUuSU2jXZN152xqqEg)
  VERCEL_TOKEN — token Vercel ja validado contra /v2/user
  SIBLING      — path absoluto da sibling (ex: C:/Users/.../cxpress-lp-playbook-whatsapp2026)

Saida: arquivos do deploy production sao escritos em $SIBLING/, preservando
estrutura. Vercel envelopa tudo num diretorio top-level "src" — esse wrapper
e descartado para que os arquivos caiam direto na raiz do sibling.

Por que arquivo separado e nao heredoc inline na skill: heredoc + escape de
backslash + Python sandbox no Windows fica fragil. Script externo isola
tudo, da pra testar isolado, e o erro fica claro se algo quebrar.
"""

import base64
import json
import os
import urllib.request


def main():
    deploy_id = os.environ["DEPLOY_ID"]
    team_id = os.environ["ORG_ID"]
    # Token OAuth do CLI Vercel autentica nos endpoints REST V6/V7 de files
    # apenas com `slug=...`; `teamId=team_...` retorna 403 missingToken.
    # Access Tokens (Settings → Tokens) aceitam ambos. Preferir slug quando setado.
    team_slug = os.environ.get("ORG_SLUG", "elife-group")
    team_param = f"slug={team_slug}" if team_slug else f"teamId={team_id}"
    token = os.environ["VERCEL_TOKEN"]
    sibling = os.environ["SIBLING"].replace("\\", "/")

    def api_get(url):
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())

    written = 0

    def walk(node, base_path):
        nonlocal written
        name = node.get("name", "")
        t = node.get("type")
        # Vercel envelopa tudo num diretorio "src" no topo — descartar
        if base_path == "" and t == "directory" and name == "src":
            for c in node.get("children", []):
                walk(c, "")
            return
        if t == "file":
            target = os.path.join(sibling, base_path, name).replace("\\", "/")
            os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
            file_data = api_get(
                f"https://api.vercel.com/v7/deployments/{deploy_id}/files/{node['uid']}?{team_param}"
            )
            data = file_data.get("data", "")
            try:
                content = base64.b64decode(data, validate=True)
            except Exception:
                content = data.encode("utf-8") if isinstance(data, str) else bytes(data)
            with open(target, "wb") as f:
                f.write(content)
            rel = os.path.relpath(target, sibling).replace("\\", "/")
            print(f"  + {rel} ({len(content)} bytes)")
            written += 1
        elif t == "directory":
            new_base = os.path.join(base_path, name) if base_path else name
            for c in node.get("children", []):
                walk(c, new_base)

    tree = api_get(
        f"https://api.vercel.com/v6/deployments/{deploy_id}/files?{team_param}"
    )
    for root_node in tree if isinstance(tree, list) else [tree]:
        walk(root_node, "")

    print(f"\nSync OK: {written} files written to {sibling}")


if __name__ == "__main__":
    main()
