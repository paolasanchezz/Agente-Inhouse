"""Renderiza criativos (card-*.html) em PNG nas dimensoes Meta.

Uso:
    python render.py [formatos] [uso]
        formatos : csv de 1x1,4x5,9x16   (default: 4x5)
        uso      : organico | anuncio    (default: organico)

Em uso=anuncio, gera tambem um <card>-<dim>-guia.png com overlay das zonas
reservadas (faixas vermelhas) + limite da area segura (tracejado verde),
pra QA visual de que nada critico invade a margem de seguranca.

render.py injeta data-uso/data-fmt no .canvas antes do screenshot, entao um
mesmo HTML serve a todos os formatos (base.css deriva a safe zone disso).

Pre-requisito (uma vez por maquina):
    python -m pip install playwright && python -m playwright install chromium
"""
import sys
import glob
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
DIMS = {"1x1": (1080, 1080), "4x5": (1080, 1350), "9x16": (1080, 1920)}

# Overlay-guia: le o padding computado do .canvas (== safe zone) e desenha
# faixas reservadas + limite da area segura. Nao depende de numeros fixos.
GUIDE_JS = r"""() => {
  const c = document.querySelector('.canvas'); if (!c) return;
  const s = getComputedStyle(c);
  const g = document.createElement('div');
  g.setAttribute('data-guia', '1');
  g.style.cssText = 'position:absolute;inset:0;z-index:99999;pointer-events:none';
  const band = (css) => { const d=document.createElement('div');
    d.style.cssText='position:absolute;background:rgba(222,36,81,.22);'+css; g.appendChild(d); };
  band(`top:0;left:0;right:0;height:${s.paddingTop}`);
  band(`bottom:0;left:0;right:0;height:${s.paddingBottom}`);
  band(`top:0;bottom:0;left:0;width:${s.paddingLeft}`);
  band(`top:0;bottom:0;right:0;width:${s.paddingRight}`);
  const safe = document.createElement('div');
  safe.style.cssText = `position:absolute;top:${s.paddingTop};bottom:${s.paddingBottom};`
    + `left:${s.paddingLeft};right:${s.paddingRight};border:3px dashed rgba(0,190,110,.95)`;
  g.appendChild(safe);
  c.appendChild(g);
}"""


def render(page, card, w, h, uso, fmt, out):
    page.goto(card.as_uri(), wait_until="networkidle", timeout=30000)
    page.evaluate("() => document.fonts.ready")
    # injeta uso/formato no canvas -> base.css recalcula a safe zone
    page.evaluate(
        "([u,f]) => { const c=document.querySelector('.canvas');"
        " if(c){ c.setAttribute('data-uso',u); c.setAttribute('data-fmt',f);} }",
        [uso, fmt],
    )
    page.wait_for_timeout(350)
    page.screenshot(path=str(out), full_page=False)
    return out.stat().st_size


def main():
    fmts = (sys.argv[1] if len(sys.argv) > 1 else "4x5").split(",")
    uso = sys.argv[2] if len(sys.argv) > 2 else "organico"
    cards = [Path(p) for p in sorted(glob.glob(str(ROOT / "card-*.html")))]
    if not cards:
        print("ERRO: nenhum card-*.html encontrado em", ROOT, file=sys.stderr)
        sys.exit(1)
    for f in fmts:
        if f not in DIMS:
            print(f"ERRO: formato invalido '{f}'. Use: {', '.join(DIMS)}", file=sys.stderr)
            sys.exit(1)

    print(f"  uso={uso} | formatos={','.join(fmts)} | {len(cards)} card(s)")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for fmt in fmts:
            w, h = DIMS[fmt]
            for card in cards:
                ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
                pg = ctx.new_page()
                out = ROOT / f"{card.stem}-{w}x{h}.png"
                size = render(pg, card, w, h, uso, fmt, out)
                print(f"  {card.name} [{fmt}] -> {out.name} ({size} bytes)")
                if uso == "anuncio":
                    pg.evaluate(GUIDE_JS)
                    pg.wait_for_timeout(120)
                    gout = ROOT / f"{card.stem}-{w}x{h}-guia.png"
                    pg.screenshot(path=str(gout), full_page=False)
                    print(f"      guia -> {gout.name}")
                ctx.close()
        browser.close()
    print("  OK.")


if __name__ == "__main__":
    main()
