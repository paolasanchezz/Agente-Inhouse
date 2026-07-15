"""Fase 1 — gera manifestos a partir do live, roda build_umbrella e prova paridade.

Estágios:
  A. baixa todos os arquivos do último deploy READY de cada guarda-chuva (cache local)
  B. gera landing-pages/dominios/{dom}/manifest.json + vercel.json
  C. roda build_umbrella.py e compara md5 arquivo a arquivo
  D. arquivos do live que o build não produz (placeholder, assets legados,
     assets mortos) são importados como extras e o build re-roda
Saída: JSON com o resultado por domínio + diffs salvos no cache pra inspeção.
"""
import base64
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request

TOKEN = os.environ["VERCEL_TOKEN"]
TEAM = "team_nC991VqUuSU2jXZN152xqqEg"
REPO = os.environ["REPO_ROOT"]
CACHE = os.environ["CACHE_DIR"]
MARCAS = ("buzzmonitor", "buzzcreators", "cxpress", "elife")

UMBRELLAS = {
    "content.cxpress.io": "cxpress-lp-playbook-whatsapp2026",
    "webinar.buzzmonitor.com": "buzzmonitor-lp-monitoramento-concorrentes",
    "evento.buzzmonitor.com": "buzzmonitor-evento",
    "material.buzzmonitor.com": "buzzmonitor-material",
}


def api(path):
    sep = "&" if "?" in path else "?"
    req = urllib.request.Request(
        f"https://api.vercel.com{path}{sep}teamId={TEAM}",
        headers={"Authorization": f"Bearer {TOKEN}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def walk(tree, prefix=""):
    out = {}
    for n in tree:
        p = f"{prefix}{n.get('name', '')}"
        if n.get("type") == "directory":
            out.update(walk(n.get("children", []), f"{p}/"))
        else:
            out[p] = n.get("uid") or n.get("link", "")
    return out


def md5(b):
    return hashlib.md5(b).hexdigest()


def is_text(path):
    return path.endswith((".html", ".json", ".svg", ".css", ".js", ".txt", ".xml"))


result = {}
for dominio, project in UMBRELLAS.items():
    dom_key = dominio.replace(".", "-")
    live_dir = os.path.join(CACHE, "live", dom_key)

    # --- A. download do live (com cache) ---
    dep = api(f"/v6/deployments?projectId={project}&target=production&state=READY&limit=1")["deployments"][0]
    dep_id = dep["uid"]
    marker = os.path.join(live_dir, ".deploy_id")
    if not (os.path.isfile(marker) and open(marker).read() == dep_id):
        tree = api(f"/v6/deployments/{dep_id}/files")
        files = walk(tree if isinstance(tree, list) else tree.get("files", []))
        root = "src/" if any(p.startswith("src/") for p in files) else ""
        for path, uid in files.items():
            if not path.startswith(root):
                continue
            rel = path[len(root):]
            raw = api(f"/v7/deployments/{dep_id}/files/{uid}")
            data = base64.b64decode(raw["data"], validate=True)
            dest = os.path.join(live_dir, rel)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as f:
                f.write(data)
        os.makedirs(live_dir, exist_ok=True)
        with open(marker, "w") as f:
            f.write(dep_id)

    live = {}
    for base, _d, fs in os.walk(live_dir):
        for f in fs:
            if f == ".deploy_id":
                continue
            full = os.path.join(base, f)
            rel = os.path.relpath(full, live_dir).replace("\\", "/")
            live[rel] = open(full, "rb").read()

    # --- B. manifesto ---
    dom_dir = os.path.join(REPO, "landing-pages", "dominios", dom_key)
    os.makedirs(dom_dir, exist_ok=True)
    # vercel.json versionado = cópia fiel do live
    with open(os.path.join(dom_dir, "vercel.json"), "wb") as f:
        f.write(live["vercel.json"])

    lps, problemas = [], []
    slugs = sorted({p.split("/")[0] for p in live
                    if p.count("/") == 1 and p.endswith("/index.html")
                    and not p.startswith("_") and not p.startswith("assets/")})
    for slug in slugs:
        html = live[f"{slug}/index.html"].decode("utf-8", "replace")
        cands = [m for m in MARCAS
                 if os.path.isfile(os.path.join(REPO, "landing-pages", m, slug, "index.html"))]
        ns = re.findall(r"/assets/(%s)/" % "|".join(MARCAS), html)
        ns_top = max(set(ns), key=ns.count) if ns else None
        if len(cands) == 1:
            marca = cands[0]
        elif ns_top in cands:
            marca = ns_top
        elif not cands:
            problemas.append(f"{slug}: sem source no repo")
            continue
        else:
            problemas.append(f"{slug}: ambíguo entre {cands}")
            continue
        lps.append({"slug": slug, "marca": marca,
                    "source": f"landing-pages/{marca}/{slug}"})

    manifest = {
        "dominio": dominio,
        "projeto_vercel": project,
        "vercel_json": f"landing-pages/dominios/{dom_key}/vercel.json",
        "lps": lps,
        "extra_files": {},
    }

    # --- C/D. build + comparação (2 passadas: a 1ª descobre extras) ---
    dist = os.path.join(CACHE, "dist", dom_key)
    resumo = None
    for rodada in (1, 2):
        man_path = os.path.join(dom_dir, "manifest.json")
        with open(man_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
            f.write("\n")
        proc = subprocess.run(
            [sys.executable, os.path.join(REPO, "landing-pages", "build", "build_umbrella.py"),
             man_path, dist],
            capture_output=True, text=True, env={**os.environ, "REPO_ROOT": REPO})
        if proc.returncode != 0:
            resumo = {"build_erro": proc.stderr.strip()}
            break
        build_avisos = json.loads(proc.stdout).get("avisos", [])

        built = {}
        for base, _d, fs in os.walk(dist):
            for f in fs:
                rel = os.path.relpath(os.path.join(base, f), dist).replace("\\", "/")
                built[rel] = open(os.path.join(base, f), "rb").read()

        identicos, so_newline, diferentes, faltando, sobrando = [], [], [], [], []
        for path, lb in sorted(live.items()):
            if path not in built:
                faltando.append(path)
            elif built[path] == lb:
                identicos.append(path)
            elif is_text(path) and built[path].replace(b"\r\n", b"\n") == lb.replace(b"\r\n", b"\n"):
                so_newline.append(path)
            else:
                diferentes.append(path)
                if is_text(path):
                    d = difflib.unified_diff(
                        lb.decode("utf-8", "replace").splitlines(),
                        built[path].decode("utf-8", "replace").splitlines(),
                        "live", "build", lineterm="", n=1)
                    dd = os.path.join(CACHE, "diffs", dom_key, path.replace("/", "__") + ".diff")
                    os.makedirs(os.path.dirname(dd), exist_ok=True)
                    with open(dd, "w", encoding="utf-8") as f:
                        f.write("\n".join(list(d)[:400]))
        sobrando = [p for p in sorted(built) if p not in live]

        if rodada == 1 and faltando:
            # importa como extras verbatim (só o que NÃO é index de slug conhecido)
            for path in faltando:
                if any(path == f"{lp['slug']}/index.html" for lp in lps):
                    continue
                src = os.path.join(live_dir, path)
                dst_rel = f"landing-pages/dominios/{dom_key}/extras/{path}"
                dst = os.path.join(REPO, dst_rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                with open(dst, "wb") as f:
                    f.write(open(src, "rb").read())
                manifest["extra_files"][path] = dst_rel
            continue
        resumo = {
            "deploy_id": dep_id, "lps": len(lps), "problemas": problemas,
            "build_avisos": build_avisos,
            "identicos": len(identicos), "so_newline": len(so_newline),
            "diferentes": diferentes, "faltando": faltando, "sobrando": sobrando,
            "extras_importados": len(manifest["extra_files"]),
        }
        break
    result[dominio] = resumo

json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
