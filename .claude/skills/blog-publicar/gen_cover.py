# -*- coding: utf-8 -*-
"""Capas OG automáticas do blog (1200x630) — 100% material da marca (zero copyright).

Varre os posts do blog e, para cada um SEM `cover:` no frontmatter, renderiza
`public/assets/covers/{slug}.png` (a partir do `title` + `category` do post) e
preenche `cover`/`coverAlt`. IDEMPOTENTE: post que já tem capa é pulado.

Estilo: off-white + gradiente assinatura + mascote (papagaio) marca-d'água + logo
raster + DM Sans. Mesmo template que gerou as 20 primeiras capas.

Uso:  py .claude/skills/blog-publicar/gen_cover.py [marca]   (default: buzzcreators)
Pré-requisito: Playwright + um browser. Tenta channel chrome -> msedge -> chromium
do Playwright (instalar via /setup-agencia ou `py -m playwright install chromium`).
"""
import base64
import re
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

MARCA = sys.argv[1] if len(sys.argv) > 1 else "buzzcreators"
REPO = Path(__file__).resolve().parents[3]
BLOG = REPO / "blog" / MARCA
PUB = BLOG / "public" / "assets"
OUT = PUB / "covers"
POSTS = BLOG / "src" / "content" / "blog"

if not POSTS.is_dir():
    print("ERRO: nao achei posts em " + str(POSTS), file=sys.stderr)
    sys.exit(1)
for logo in ("logo-color.png", "logo-icon.png"):
    if not (PUB / logo).exists():
        print("ERRO: falta " + logo + " em " + str(PUB), file=sys.stderr)
        sys.exit(1)
OUT.mkdir(parents=True, exist_ok=True)


def datauri(p):
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()


LOGO = datauri(PUB / "logo-color.png")
PARROT = datauri(PUB / "logo-icon.png")

TEMPLATE = r'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700&display=swap');
:root{--roxo-escuro:#3a1652;--roxo-medio:#6a3895;--laranja:#ff8119;--laranja-esc:#ff7300;--offwhite:#f7f9fb;--accent:#6a3895}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:630px;overflow:hidden;position:relative;background:var(--offwhite);font-family:'DM Sans',sans-serif;padding:74px 88px;display:flex;flex-direction:column;justify-content:center}
.grad{position:absolute;top:-150px;right:-150px;width:560px;height:560px;border-radius:50%;background:linear-gradient(135deg,var(--roxo-escuro),var(--roxo-medio),var(--laranja),var(--laranja-esc));opacity:.14}
.bar{position:absolute;left:0;top:0;bottom:0;width:16px;background:linear-gradient(180deg,var(--roxo-escuro),var(--laranja))}
.parrot{position:absolute;right:44px;top:50%;transform:translateY(-50%);height:430px;opacity:.06;z-index:0}
.overline{position:relative;z-index:1;display:inline-flex;align-items:center;gap:14px;font-size:24px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:var(--accent);margin-bottom:32px}
.dot{width:12px;height:12px;border-radius:50%;background:var(--laranja)}
h1{position:relative;z-index:1;font-size:__SIZE__px;font-weight:700;line-height:1.1;color:var(--roxo-escuro);max-width:900px;letter-spacing:-1.5px}
.foot{position:absolute;bottom:54px;left:88px;right:88px;display:flex;align-items:center;justify-content:space-between;z-index:1}
.foot img.logo{height:42px;width:auto}
.foot .tag{font-size:20px;font-weight:500;color:#8a8f97}
</style></head>
<body>
<div class="grad"></div><div class="bar"></div>
<img class="parrot" src="__PARROT__" alt="">
<div class="overline"><span class="dot"></span>__CAT__</div>
<h1>__TITLE__</h1>
<div class="foot"><img class="logo" src="__LOGO__" alt="Buzzcreators"><span class="tag">blog.buzzcreators.com.br</span></div>
</body></html>'''


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fm_value(txt, key):
    m = re.search(r'^' + key + r':\s*(.+)$', txt, re.M)
    if not m:
        return None
    v = m.group(1).strip()
    if len(v) >= 2 and v[0] in "'\"" and v[-1] in "'\"":
        v = v[1:-1]
    return v.strip()


def first_tag(txt):
    m = re.search(r'^tags:\s*\[(.+?)\]', txt, re.M)
    if not m:
        return None
    return m.group(1).split(",")[0].strip().strip("'\" ")


def build_html(cat, title):
    size = 64
    if len(title) > 52:
        size = 56
    if len(title) > 66:
        size = 50
    return (TEMPLATE.replace("__PARROT__", PARROT).replace("__LOGO__", LOGO)
            .replace("__SIZE__", str(size))
            .replace("__CAT__", esc(cat.upper())).replace("__TITLE__", esc(title)))


def patch_frontmatter(f, slug, title):
    txt = f.read_text(encoding="utf-8")
    alt = (title + " — Blog Buzzcreators").replace('"', "'")
    out, done = [], False
    for ln in txt.split("\n"):
        out.append(ln)
        if not done and ln.startswith("description:"):
            out.append("cover: '/assets/covers/" + slug + ".png'")
            out.append('coverAlt: "' + alt + '"')
            done = True
    if done:
        f.write_text("\n".join(out), encoding="utf-8")
    return done


def main():
    posts = [p for p in sorted(POSTS.glob("*.md")) if not p.name.startswith("_")]
    todo = []
    for p in posts:
        txt = p.read_text(encoding="utf-8")
        if re.search(r'^cover:', txt, re.M):
            continue  # ja tem capa -> idempotente
        title = fm_value(txt, "title") or p.stem
        cat = fm_value(txt, "category") or first_tag(txt) or "Blog"
        todo.append((p, p.stem, cat, title))

    if not todo:
        print("Nenhuma capa faltando — todos os " + str(len(posts)) + " posts ja tem cover. (idempotente)")
        return

    print("Gerando " + str(len(todo)) + " capa(s) faltante(s) de " + str(len(posts)) + " posts...")
    with sync_playwright() as pw:
        def launch():
            last = None
            for kw in ({"channel": "chrome"}, {"channel": "msedge"}, {}):
                try:
                    return pw.chromium.launch(**kw)
                except Exception as e:
                    last = e
            raise last

        b = launch()
        for f, slug, cat, title in todo:
            ctx = b.new_context(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
            pg = ctx.new_page()
            pg.set_content(build_html(cat, title), wait_until="networkidle", timeout=30000)
            pg.evaluate("() => document.fonts.ready")
            pg.wait_for_timeout(400)
            (OUT / (slug + ".png")).write_bytes(pg.screenshot(full_page=False))
            ok = patch_frontmatter(f, slug, title)
            print("  " + slug + ".png" + (" + frontmatter" if ok else "  (WARN: sem 'description:' p/ inserir cover)"))
            ctx.close()
        b.close()
    print("OK — capas geradas. Commitar os PNGs + posts via /commit.")


if __name__ == "__main__":
    main()
