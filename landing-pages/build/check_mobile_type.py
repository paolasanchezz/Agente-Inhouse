"""check_mobile_type.py — QA das LPs em viewport mobile (375x812).

Para cada LP servida em http://127.0.0.1:PORT, carrega em 375px de largura e mede:
  - overflow horizontal de elemento VISIVEL (o que estoura o viewport de verdade);
  - tamanho de fonte efetivo dos papeis de texto (h1/h2/lead/corpo/botao);
  - texto que ficou menor que o piso de legibilidade.

Serve pra provar que o bump de tipografia mobile (GUIDELINES 20, aplicado por
bump_mobile_type.py) nao quebrou layout: rode com --json antes e depois e
compare — o que importa e overflow NOVO.

Elemento de marquee/carrossel (faixa de logos) e mais largo que a tela por
design: os seletores em IGNORE_OVERFLOW ficam fora do relatorio.

Uso:
    py -m http.server 8123 --bind 127.0.0.1      # na raiz do repo
    py check_mobile_type.py --port 8123 --json out.json landing-pages
    py check_mobile_type.py --port 8123 --baseline antes.json --json depois.json landing-pages

Requer playwright + chromium (mesma dependencia da skill /criativo).
"""
import argparse
import json
import os
import sys

VIEWPORT = {"width": 375, "height": 812}

# largura maior que a tela por design (faixa de logos em animacao infinita)
IGNORE_OVERFLOW = ("trusted__track", "trusted__group", "marquee", "logos__track",
                   "ticker", "__track", "scroller")

PROBE = r"""
() => {
  // Neutraliza a animacao de entrada ANTES de medir. Cada LP usa um nome de
  // classe diferente pro estado visivel (is-visible, visible, in-view...), e
  // medir no meio da transicao da leitura errada de posicao (o hero aparece
  // deslocado -3px e vira falso overflow). Desligar via CSS cobre todos.
  const kill = document.createElement('style');
  kill.textContent = '[class*="reveal"],[class*="fade"],[class*="stagger"],' +
    '[class*="animate"]{opacity:1 !important;transform:none !important;' +
    'transition:none !important;animation:none !important}';
  document.head.appendChild(kill);
  document.querySelectorAll('[class*="reveal"], [class*="stagger"]').forEach(e => {
    e.classList.add('is-visible', 'visible', 'in-view', 'active');
  });
  const de = document.documentElement;
  const vw = de.clientWidth;
  const vis = e => {
    let n = e;
    while (n && n.nodeType === 1) {
      const s = getComputedStyle(n);
      if (s.visibility === 'hidden' || s.display === 'none' || parseFloat(s.opacity) === 0) return false;
      n = n.parentElement;
    }
    return true;
  };
  const over = [];
  for (const e of document.querySelectorAll('body *')) {
    const r = e.getBoundingClientRect();
    if (r.width <= 0 || r.height <= 0) continue;
    if (r.right <= vw + 1 && r.left >= -1) continue;
    if (!vis(e)) continue;
    over.push({ tag: e.tagName, cls: (e.className || '').toString().slice(0, 60),
                left: Math.round(r.left), right: Math.round(r.right),
                txt: (e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40) });
  }
  const size = s => { const e = document.querySelector(s);
    return e ? Math.round(parseFloat(getComputedStyle(e).fontSize) * 10) / 10 : null; };
  const roles = {};
  for (const s of ['h1', 'h2', '.lead', 'p', 'body', '.btn', 'a.btn', 'li'])
    roles[s] = size(s);
  // menor fonte de elemento visivel COM texto proprio
  let smallest = null;
  for (const e of document.querySelectorAll('body *')) {
    if (!e.textContent || !e.textContent.trim()) continue;
    if ([...e.children].some(c => (c.textContent || '').trim())) continue;
    if (!vis(e)) continue;
    const fs = parseFloat(getComputedStyle(e).fontSize);
    if (!smallest || fs < smallest.fs)
      smallest = { fs, cls: (e.className || '').toString().slice(0, 40),
                   txt: e.textContent.trim().replace(/\s+/g, ' ').slice(0, 30) };
  }
  return { vw, scrollW: de.scrollWidth, docH: de.scrollHeight,
           overflow: over.slice(0, 25), roles, smallest };
}
"""


def diga(msg, err=False):
    """print seguro: console do Windows e cp1252 e engasga em emoji/simbolo."""
    saida = sys.stderr if err else sys.stdout
    enc = getattr(saida, "encoding", None) or "ascii"
    saida.write(str(msg).encode(enc, "replace").decode(enc) + "\n")


def collect(targets):
    out = []
    for t in targets:
        if os.path.isdir(t):
            for base, _d, fs in os.walk(t):
                norm = base.replace("\\", "/")
                if "_experimentos" in norm or "/extras/" in norm + "/":
                    continue
                if "index.html" in fs:
                    out.append(os.path.join(base, "index.html").replace("\\", "/"))
        elif os.path.isfile(t):
            out.append(t.replace("\\", "/"))
    return sorted(set(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="+")
    ap.add_argument("--port", type=int, default=8123)
    ap.add_argument("--json")
    ap.add_argument("--baseline")
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    files = collect(args.targets)
    if args.limit:
        files = files[:args.limit]
    base = json.load(open(args.baseline, encoding="utf-8")) if args.baseline else {}
    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport=VIEWPORT, device_scale_factor=2)
        # corta rede externa: embed de form/analytics nao muda overflow horizontal
        ctx.route("**/*", lambda r: r.continue_()
                  if "127.0.0.1" in r.request.url or r.request.url.startswith("data:")
                  else r.abort())
        page = ctx.new_page()
        for i, f in enumerate(files, 1):
            url = "http://127.0.0.1:%d/%s" % (args.port, f)
            try:
                page.goto(url, wait_until="load", timeout=25000)
                page.wait_for_timeout(180)
                data = page.evaluate(PROBE)
            except Exception as e:
                results[f] = {"erro": "%s: %s" % (type(e).__name__, str(e)[:120])}
                diga("  [%3d/%d] ERRO %s" % (i, len(files), f), err=True)
                continue
            data["overflow"] = [o for o in data["overflow"]
                                if not any(k in o["cls"] for k in IGNORE_OVERFLOW)]
            results[f] = data
            diga("  [%3d/%d] %s  ovf=%d  h1=%s corpo=%s min=%s"
                 % (i, len(files), f.split("/", 1)[-1], len(data["overflow"]),
                    data["roles"].get("h1"), data["roles"].get("body"),
                    round(data["smallest"]["fs"], 1) if data["smallest"] else "-"), err=True)
        browser.close()

    if args.json:
        json.dump(results, open(args.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)

    # ---- relatorio ----
    erros = {k: v for k, v in results.items() if "erro" in v}
    com_ovf = {k: v for k, v in results.items() if v.get("overflow")}
    print("\n%d LPs medidas - %d com overflow visivel - %d com erro de carga"
          % (len(results), len(com_ovf), len(erros)))

    if base:
        novos = {}
        for k, v in com_ovf.items():
            antes = {(o["cls"], o["tag"]) for o in base.get(k, {}).get("overflow", [])}
            d = [o for o in v["overflow"] if (o["cls"], o["tag"]) not in antes]
            if d:
                novos[k] = d
        diga("OVERFLOW NOVO (nao existia no baseline): %d LPs" % len(novos))
        for k, v in novos.items():
            print("\n  %s" % k)
            for o in v[:6]:
                diga("    %s.%s  [%d..%d]  %r" % (o["tag"], o["cls"], o["left"],
                                                   o["right"], o["txt"]))
    else:
        for k, v in com_ovf.items():
            print("\n  %s" % k)
            for o in v["overflow"][:6]:
                diga("    %s.%s  [%d..%d]  %r" % (o["tag"], o["cls"], o["left"],
                                                   o["right"], o["txt"]))
    for k, v in erros.items():
        diga("  ERRO %s -> %s" % (k, v["erro"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
