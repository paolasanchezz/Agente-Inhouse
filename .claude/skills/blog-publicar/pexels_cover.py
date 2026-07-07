# -*- coding: utf-8 -*-
"""Capas fotograficas do blog via Pexels (1200x630) — padrao desde 2026-07-07.

Busca foto no Pexels (scrape keyless da pagina de busca, com User-Agent de
browser — sem API key), baixa ja recortada em 1200x630 via CDN do Pexels
(`?w=1200&h=630&fit=crop`), salva em `public/assets/covers/{slug}.jpg`,
preenche `cover`/`coverAlt` no frontmatter do post e registra a proveniencia
na tabela de `blog/{marca}/COVERS-FONTES.md`.

Licenca Pexels (https://www.pexels.com/license/): uso comercial livre, sem
atribuicao obrigatoria, modificacao permitida. Fotos ja usadas em outras
capas (lidas do COVERS-FONTES.md) sao puladas — sem capa repetida.

Uso:
  py pexels_cover.py --list [--marca M]
      Lista os posts sem `cover:` (titulo/categoria/tags), pra escolher query.
  py pexels_cover.py {slug} "query em ingles" ["alt em pt-br"] [--id N] [--marca M]
      Gera a capa de 1 post. `--id N` forca uma foto especifica do Pexels
      (pula a busca). Sem alt, cai num fallback baseado no titulo (WARN).

IDEMPOTENTE: post que ja tem `cover:` e pulado (exit 0, nada muda).
Sai com exit != 0 quando busca/download falham — o fallback documentado na
skill e o gen_cover.py (estilo HTML→PNG, so pra nao travar a publicacao).
"""
import gzip
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

REPO = Path(__file__).resolve().parents[3]
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
MIN_JPG_BYTES = 20000       # abaixo disso e placeholder/erro, nao foto
MAX_CANDIDATOS = 8          # quantos IDs da busca tentar baixar


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,image/*,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "identity",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            data = gzip.decompress(data)
        return data


def curl_candidates():
    """Caminhos de curl a tentar, em ordem.

    IMPORTANTE (Windows): `subprocess.run(["curl", ...])` resolve pelo
    CreateProcess, que olha System32 ANTES do PATH — e a curl do Windows
    (System32) leva 403/1010 do Cloudflare do pexels.com (fingerprint TLS
    banido), enquanto a curl do Git (mingw64, a que o `which` acha no PATH)
    passa. Por isso resolvemos o caminho absoluto via shutil.which e ainda
    tentamos a curl do Git explicitamente como candidato seguinte.
    """
    cands = []
    w = shutil.which("curl")
    if w:
        cands.append(w)
    git_curl = Path(r"C:\Program Files\Git\mingw64\bin\curl.exe")
    if git_curl.exists() and str(git_curl) not in cands:
        cands.append(str(git_curl))
    return cands or ["curl"]


def search_photo_ids(query):
    """Raspa a pagina de busca do Pexels e devolve IDs na ordem em que aparecem.

    A busca vai por curl: o Cloudflare do pexels.com aceita curl (do Git/unix)
    com UA de browser, mas rejeita urllib e a curl do System32 (403 por
    fingerprint TLS). O CDN de imagens nao tem esse bloqueio (urllib ok).
    """
    url = "https://www.pexels.com/search/?q=" + urllib.parse.quote(query)
    html, last = None, "?"
    for curl in curl_candidates():
        r = subprocess.run([curl, "-sL", "--max-time", "45", "-A", UA, url],
                           capture_output=True, timeout=60)
        if r.returncode == 0 and len(r.stdout) > 50000:
            html = r.stdout.decode("utf-8", errors="replace")
            break
        last = curl + " rc=" + str(r.returncode) + " " + str(len(r.stdout)) + " bytes"
    if html is None:
        raise RuntimeError("busca bloqueada/falhou em todas as curl (" + last + ")")
    ids, seen = [], set()
    for m in re.finditer(r'images\.pexels\.com/photos/(\d+)/|pexels\.com/photo/[a-z0-9-]*?(\d+)/', html):
        pid = m.group(1) or m.group(2)
        if pid not in seen:
            seen.add(pid)
            ids.append(pid)
    return ids


def download_cover(pid, dest):
    """Baixa a foto ja recortada 1200x630 pelo CDN. True se salvou valida."""
    url = ("https://images.pexels.com/photos/" + pid + "/pexels-photo-" + pid +
           ".jpeg?auto=compress&cs=tinysrgb&w=1200&h=630&fit=crop")
    try:
        data = fetch(url, timeout=60)
    except Exception as e:
        print("  foto " + pid + ": download falhou (" + str(e)[:80] + ")")
        return False
    if len(data) < MIN_JPG_BYTES or not data.startswith(b"\xff\xd8"):
        print("  foto " + pid + ": resposta nao parece JPEG valido — pulando")
        return False
    dest.write_bytes(data)
    return True


def fm_value(txt, key):
    m = re.search(r'^' + key + r':\s*(.+)$', txt, re.M)
    if not m:
        return None
    v = m.group(1).strip()
    if len(v) >= 2 and v[0] in "'\"" and v[-1] in "'\"":
        v = v[1:-1]
    return v.strip()


def patch_frontmatter(f, slug, alt):
    txt = f.read_text(encoding="utf-8")
    out, done = [], False
    for ln in txt.split("\n"):
        out.append(ln)
        if not done and ln.startswith("description:"):
            out.append("cover: '/assets/covers/" + slug + ".jpg'")
            out.append('coverAlt: "' + alt.replace('"', "'") + '"')
            done = True
    if done:
        f.write_text("\n".join(out), encoding="utf-8")
    return done


FONTES_HEADER = """# Capas do blog — fontes e licença

As capas em `public/assets/covers/*.jpg` são fotografias do **Pexels** ([licença Pexels](https://www.pexels.com/license/): uso comercial livre, sem atribuição obrigatória, modificação permitida). Baixadas já recortadas em 1200×630 via CDN do Pexels (`?w=1200&h=630&fit=crop`).

| Post (slug) | Foto Pexels |
|---|---|
"""


def used_photo_ids(fontes):
    if not fontes.exists():
        return set()
    return set(re.findall(r'pexels\.com/photo/(\d+)/', fontes.read_text(encoding="utf-8")))


def register_fonte(fontes, slug, pid):
    """Acrescenta (ou atualiza) a linha `| slug | url |` na tabela de proveniencia."""
    row = "| " + slug + " | https://www.pexels.com/photo/" + pid + "/ |"
    if not fontes.exists():
        fontes.write_text(FONTES_HEADER + row + "\n", encoding="utf-8")
        return
    lines = fontes.read_text(encoding="utf-8").split("\n")
    is_row = lambda ln: re.match(r'^\|\s*\S+\s*\|\s*https://www\.pexels\.com/photo/\d+/\s*\|\s*$', ln)
    for i, ln in enumerate(lines):
        if is_row(ln) and ln.split("|")[1].strip() == slug:
            lines[i] = row  # slug re-rodado -> atualiza em vez de duplicar
            fontes.write_text("\n".join(lines), encoding="utf-8")
            return
    last = max((i for i, ln in enumerate(lines) if is_row(ln)), default=None)
    if last is None:  # sem tabela? acrescenta no fim com header minimo
        lines += ["", "| Post (slug) | Foto Pexels |", "|---|---|", row]
    else:
        lines.insert(last + 1, row)
    fontes.write_text("\n".join(lines), encoding="utf-8")


def main():
    args = sys.argv[1:]
    marca = "buzzcreators"
    if "--marca" in args:
        i = args.index("--marca")
        marca = args[i + 1]
        del args[i:i + 2]
    force_id = None
    if "--id" in args:
        i = args.index("--id")
        force_id = args[i + 1]
        del args[i:i + 2]

    blog = REPO / "blog" / marca
    posts_dir = blog / "src" / "content" / "blog"
    out_dir = blog / "public" / "assets" / "covers"
    fontes = blog / "COVERS-FONTES.md"
    if not posts_dir.is_dir():
        print("ERRO: nao achei posts em " + str(posts_dir), file=sys.stderr)
        sys.exit(1)

    posts = [p for p in sorted(posts_dir.glob("*.md")) if not p.name.startswith("_")]

    if args and args[0] == "--list":
        missing = []
        for p in posts:
            txt = p.read_text(encoding="utf-8")
            if re.search(r'^cover:', txt, re.M):
                continue
            missing.append((p.stem, fm_value(txt, "title") or p.stem,
                            fm_value(txt, "category") or "-",
                            fm_value(txt, "tags") or "-"))
        if not missing:
            print("Nenhuma capa faltando — todos os " + str(len(posts)) + " posts ja tem cover. (idempotente)")
            return
        print(str(len(missing)) + " post(s) sem capa:")
        for slug, title, cat, tags in missing:
            print("  " + slug + "\n    title: " + title + "\n    category: " + cat + " | tags: " + tags)
        return

    if not args:
        print(__doc__)
        sys.exit(2)

    slug = args[0]
    query = args[1] if len(args) > 1 else None
    alt = args[2] if len(args) > 2 else None
    post = posts_dir / (slug + ".md")
    if not post.exists():
        print("ERRO: post nao existe: " + str(post), file=sys.stderr)
        sys.exit(1)
    txt = post.read_text(encoding="utf-8")
    if re.search(r'^cover:', txt, re.M):
        print(slug + " ja tem cover — nada a fazer. (idempotente)")
        return
    if not query and not force_id:
        print("ERRO: passe a query de busca (em ingles) ou --id N", file=sys.stderr)
        sys.exit(2)
    title = fm_value(txt, "title") or slug
    if not alt:
        alt = title + " — Blog " + marca.capitalize()
        print("WARN: sem alt descritivo — usando fallback pelo titulo. Melhor passar um alt em PT-BR que descreva a foto.")

    usados = used_photo_ids(fontes)
    if force_id:
        candidatos = [force_id]
    else:
        try:
            candidatos = [pid for pid in search_photo_ids(query) if pid not in usados]
        except Exception as e:
            print("ERRO: busca no Pexels falhou (" + str(e)[:120] + ") — use o fallback gen_cover.py", file=sys.stderr)
            sys.exit(3)
        if not candidatos:
            print("ERRO: busca por '" + query + "' nao retornou foto nova. Tente outra query ou o fallback gen_cover.py", file=sys.stderr)
            sys.exit(4)
        candidatos = candidatos[:MAX_CANDIDATOS]

    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / (slug + ".jpg")
    chosen = None
    for pid in candidatos:
        if download_cover(pid, dest):
            chosen = pid
            break
    if not chosen:
        print("ERRO: nenhum dos " + str(len(candidatos)) + " candidatos baixou valido — use o fallback gen_cover.py", file=sys.stderr)
        sys.exit(5)

    ok = patch_frontmatter(post, slug, alt)
    register_fonte(fontes, slug, chosen)
    print("OK  " + slug + ".jpg  <- https://www.pexels.com/photo/" + chosen + "/  (" +
          str(dest.stat().st_size // 1024) + " KB)" +
          ("" if ok else "  (WARN: sem 'description:' no frontmatter p/ inserir cover — inserir a mao)"))
    print("Proveniencia registrada em " + str(fontes.relative_to(REPO)))
    print("Confira a foto antes de publicar; ruim/fora do tema -> apague o .jpg + cover:/coverAlt: e re-rode com outra query ou --id.")


if __name__ == "__main__":
    main()
