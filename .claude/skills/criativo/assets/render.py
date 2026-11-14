"""Renderiza criativos (card-*.html) em PNG nas dimensoes Meta.

Uso:
    python render.py [formatos] [uso]
        formatos : csv de 1x1,4x5,9x16   (default: 4x5)
        uso      : organico | anuncio    (default: organico)

Em uso=anuncio, gera tambem um <card>-<dim>-guia.png com overlay das zonas
reservadas (faixas vermelhas) + limite da area segura (tracejado verde),
pra QA visual de que nada critico invade a margem de seguranca.

Dois motores, escolhidos automaticamente:

  1. Playwright (preferido). Injeta data-uso/data-fmt no .canvas antes do
     screenshot, entao um mesmo HTML serve a todos os formatos, e desenha o
     overlay-guia lendo o padding COMPUTADO do .canvas — sempre fiel ao css.
  2. Chrome headless (fallback). Entra em cena quando o Playwright nao esta
     instalado ou nao carrega (no Windows o greenlet costuma falhar com
     "ImportError: DLL load failed while importing _greenlet"). Injeta os
     atributos no HTML antes de abrir e desenha o guia com Pillow.

Pre-requisito do caminho 1 (uma vez por maquina):
    python -m pip install playwright && python -m playwright install chromium
O caminho 2 so precisa do Chrome (ou Edge) instalado e, em anuncio, do Pillow.
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIMS = {"1x1": (1080, 1080), "4x5": (1080, 1350), "9x16": (1080, 1920)}

# Overlay-guia (caminho Playwright): le o padding computado do .canvas (== safe
# zone) e desenha faixas reservadas + limite da area segura. Sem numeros fixos.
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

CHROME_CANDIDATOS = [
    r"C:/Program Files/Google/Chrome/Application/chrome.exe",
    r"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%/Google/Chrome/Application/chrome.exe"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "chromium-browser",
    # Edge e Chromium e vem em todo Windows: ultima opcao, mesmas flags
    r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
    r"C:/Program Files/Microsoft/Edge/Application/msedge.exe",
]
CHROME_TIMEOUT = 60  # s por card; Chrome travado nao pode prender o render

# Tag de abertura do .canvas, com "canvas" como palavra inteira no class:
# pega class="canvas", class="canvas c1" e class="canvas" data-uso="...".
CANVAS_RE = re.compile(r'<(\w+)(?=[^>]*\sclass="(?:[^"]*\s)?canvas[\s"])')


# ------------------------------------------------------------------ comuns
def safe_zone(w, uso, fmt):
    """(esq, topo, dir, base) em px, espelhando o base.css.

    Atencao: padding em porcentagem no CSS resolve SEMPRE contra a largura do
    bloco, inclusive padding-top e padding-bottom. Por isso os 7%/10%/11% do
    base.css sao fracoes de `w`, nunca da altura — calcular contra a altura
    desenharia uma margem mais severa do que a que o navegador aplicou.
    """
    if uso == "anuncio":
        if fmt == "9x16":
            return 64, 250, 64, 340
        return round(w * .10), round(w * .10), round(w * .10), round(w * .11)
    if fmt == "9x16":
        return 64, 120, 64, 160
    return round(w * .07), round(w * .07), round(w * .07), round(w * .07)


def acha_chrome():
    for c in CHROME_CANDIDATOS:
        if "/" in c or os.sep in c:
            if Path(c).exists():
                return c
        elif shutil.which(c):
            return shutil.which(c)
    return None


# ------------------------------------------------------- motor 1: Playwright
def roda_playwright(cards, fmts, uso):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for fmt in fmts:
            w, h = DIMS[fmt]
            for card in cards:
                ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
                pg = ctx.new_page()
                out = ROOT / f"{card.stem}-{w}x{h}.png"
                pg.goto(card.as_uri(), wait_until="networkidle", timeout=30000)
                pg.evaluate("() => document.fonts.ready")
                pg.evaluate(
                    "([u,f]) => { const c=document.querySelector('.canvas');"
                    " if(c){ c.setAttribute('data-uso',u); c.setAttribute('data-fmt',f);} }",
                    [uso, fmt],
                )
                pg.wait_for_timeout(350)
                pg.screenshot(path=str(out), full_page=False)
                print(f"  {card.name} [{fmt}] -> {out.name} ({out.stat().st_size} bytes)")
                if uso == "anuncio":
                    pg.evaluate(GUIDE_JS)
                    pg.wait_for_timeout(120)
                    gout = ROOT / f"{card.stem}-{w}x{h}-guia.png"
                    pg.screenshot(path=str(gout), full_page=False)
                    print(f"      guia -> {gout.name}")
                ctx.close()
        browser.close()


# --------------------------------------------------- motor 2: Chrome headless
def desenha_guia(png, w, h, uso, fmt, out):
    from PIL import Image, ImageDraw

    base = Image.open(png).convert("RGBA")
    capa = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    e, t, dr, b = safe_zone(w, uso, fmt)
    vermelho = (222, 36, 81, 56)
    d.rectangle([0, 0, w, t], fill=vermelho)
    d.rectangle([0, h - b, w, h], fill=vermelho)
    d.rectangle([0, 0, e, h], fill=vermelho)
    d.rectangle([w - dr, 0, w, h], fill=vermelho)
    verde, passo, traco = (0, 190, 110, 242), 26, 15
    for x in range(e, w - dr, passo):
        d.line([x, t, min(x + traco, w - dr), t], fill=verde, width=3)
        d.line([x, h - b, min(x + traco, w - dr), h - b], fill=verde, width=3)
    for y in range(t, h - b, passo):
        d.line([e, y, e, min(y + traco, h - b)], fill=verde, width=3)
        d.line([w - dr, y, w - dr, min(y + traco, h - b)], fill=verde, width=3)
    Image.alpha_composite(base, capa).convert("RGB").save(out)


def marca_canvas(html, uso, fmt):
    """Poe data-uso/data-fmt na tag do .canvas, no comeco da tag.

    O caminho Playwright injeta os atributos via JS; aqui eles entram no HTML
    antes de abrir, com o mesmo efeito sobre o base.css. Entram ANTES dos
    atributos existentes: com atributo repetido o navegador fica com o
    primeiro, entao o valor injetado vence um data-uso fixado no card (mesmo
    comportamento do setAttribute do caminho Playwright).
    """
    return CANVAS_RE.subn(
        lambda m: f'<{m.group(1)} data-uso="{uso}" data-fmt="{fmt}"', html, count=1)


def roda_chrome(cards, fmts, uso, chrome):
    falhas = 0
    for fmt in fmts:
        w, h = DIMS[fmt]
        for card in cards:
            marcado, achou = marca_canvas(card.read_text(encoding="utf-8"), uso, fmt)
            if not achou:
                print(f"  AVISO: {card.name} sem .canvas — safe-zone e formato"
                      " NAO aplicados nesta peca", file=sys.stderr)
            out = ROOT / f"{card.stem}-{w}x{h}.png"
            gout = ROOT / f"{card.stem}-{w}x{h}-guia.png"
            # PNG de rodada anterior nao pode passar por resultado desta
            out.unlink(missing_ok=True)
            gout.unlink(missing_ok=True)
            tmp = ROOT / f".tmp-{card.stem}-{fmt}.html"
            tmp.write_text(marcado, encoding="utf-8")
            # Chrome headless escreve o PNG numa pasta temporaria propria (no
            # Windows ele pode nao ter permissao de escrever direto na pasta do
            # repo) e com perfil descartavel (nao briga com o Chrome aberto)
            td = Path(tempfile.mkdtemp(prefix="criativo-render-"))
            shot = td / "shot.png"
            motivo = ""
            try:
                r = subprocess.run([
                    chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--user-data-dir={td / 'perfil'}",
                    f"--window-size={w},{h}", "--force-device-scale-factor=1",
                    "--virtual-time-budget=8000", f"--screenshot={shot}", tmp.as_uri(),
                # sem PIPE: processo filho do Chrome herdando o pipe faria
                # o run() esperar EOF pra sempre depois do timeout
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                   timeout=CHROME_TIMEOUT)
                if r.returncode != 0:
                    motivo = f"Chrome saiu com codigo {r.returncode}"
                elif not shot.exists():
                    motivo = "Chrome nao gerou o PNG"
                else:
                    shutil.move(str(shot), str(out))
            except subprocess.TimeoutExpired:
                motivo = f"Chrome nao respondeu em {CHROME_TIMEOUT}s"
            finally:
                tmp.unlink(missing_ok=True)
                # ignore_errors: apos timeout, filho do Chrome ainda pode
                # segurar o perfil; lixo em %TEMP% nao derruba o render
                shutil.rmtree(td, ignore_errors=True)
            if motivo:
                falhas += 1
                print(f"  ERRO ao renderizar {card.name} [{fmt}]: {motivo}", file=sys.stderr)
                continue
            print(f"  {card.name} [{fmt}] -> {out.name} ({out.stat().st_size} bytes)")
            if uso == "anuncio":
                desenha_guia(out, w, h, uso, fmt, gout)
                print(f"      guia -> {gout.name}")
    return falhas


# ------------------------------------------------------------------- main
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

    try:
        import playwright.sync_api  # noqa: F401
    except Exception as erro:
        chrome = acha_chrome()
        if not chrome:
            print(f"ERRO: Playwright indisponivel ({erro.__class__.__name__}: {erro})"
                  " e nenhum Chrome/Edge encontrado.\n"
                  "  Instale o Playwright:  python -m pip install playwright"
                  " && python -m playwright install chromium\n"
                  "  ou instale o Google Chrome.", file=sys.stderr)
            sys.exit(1)
        if uso == "anuncio":
            try:
                import PIL  # noqa: F401  (o guia do caminho Chrome e desenhado com Pillow)
            except ImportError:
                print("ERRO: o overlay-guia de anuncio no caminho Chrome precisa do Pillow:\n"
                      "  python -m pip install pillow", file=sys.stderr)
                sys.exit(1)
        print(f"  Playwright indisponivel ({erro.__class__.__name__})"
              f" -> Chrome headless ({Path(chrome).name})")
        if roda_chrome(cards, fmts, uso, chrome):
            sys.exit(1)
    else:
        roda_playwright(cards, fmts, uso)

    print("  OK.")


if __name__ == "__main__":
    main()
