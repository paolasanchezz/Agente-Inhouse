"""sincronizar.py — copia o componente campo-telefone (CSS + JS) pra dentro das LPs.

Uso (na raiz do repo):
    py landing-pages/_componentes/campo-telefone/sincronizar.py            # grava
    py landing-pages/_componentes/campo-telefone/sincronizar.py --check    # so confere (exit 1 se defasado)

As LPs sao HTML autocontido (sem build step), entao o componente vive embutido em cada uma,
entre marcadores. Este script troca so o que esta entre os marcadores; o markup do campo e a
leitura no submit sao de cada LP e nao passam por aqui (ver README).
"""
import pathlib
import re
import sys

AQUI = pathlib.Path(__file__).resolve().parent
LPS_DIR = AQUI.parent.parent  # landing-pages/

# LPs com o campo. Ao ligar o telefone numa LP nova, acrescente aqui.
LPS = [
    "buzzcreators/conheca-o-buzzcreators",
    "buzzmonitor/atencion-al-cliente-es",
    "buzzmonitor/caso-smartfit",
    "buzzmonitor/gestion-crisis",
    "buzzmonitor/perpetuo-monitoramento-concorrentes",
    "buzzmonitor/perpetuo-monitoramento-concorrentes-pt",
    "buzzmonitor/primer-listening-5-pasos",
    "buzzmonitor/que-es-mcp",
    "cxpress/webinar-bloqueo-whatsapp",
]

CSS_INI, CSS_FIM = "/* campo-telefone:inicio */", "/* campo-telefone:fim */"
JS_INI, JS_FIM = "<!-- campo-telefone:inicio -->", "<!-- campo-telefone:fim -->"


def bloco_css():
    css = (AQUI / "campo-telefone.css").read_text(encoding="utf-8").strip()
    return f"{CSS_INI}\n{css}\n{CSS_FIM}\n"


def bloco_js():
    js = (AQUI / "campo-telefone.js").read_text(encoding="utf-8").strip()
    return f"{JS_INI}\n<script>\n{js}\n</script>\n{JS_FIM}\n"


def aplicar(html, ini, fim, bloco, posicao):
    """Tira o bloco de onde estiver e reinsere em posicao(html) — sempre no mesmo lugar."""
    rx = re.compile(re.escape(ini) + r".*?" + re.escape(fim) + r"\n?", re.S)
    html = rx.sub("", html)
    pos = posicao(html)
    return html[:pos] + bloco + html[pos:]


def pos_css(html):
    # Ultimo </style> do <head>. O primeiro costuma ser o <noscript><style> do .reveal, que so
    # vale com JS desligado — CSS la dentro nao chega no navegador (bug do v1 deste script).
    fim_head = html.find("</head>")
    pos = html.rfind("</style>", 0, fim_head if fim_head >= 0 else len(html))
    if pos < 0:
        raise SystemExit("nenhum </style> no <head>")
    return pos


def pos_js(html):
    pos = html.rfind("</body>")
    if pos < 0:
        raise SystemExit("</body> nao encontrado")
    return pos


def main():
    check = "--check" in sys.argv
    css, js = bloco_css(), bloco_js()
    defasadas = []
    for lp in LPS:
        path = LPS_DIR / lp / "index.html"
        eol = "\r\n" if b"\r\n" in path.read_bytes() else "\n"  # preserva o fim de linha do checkout
        html = path.read_text(encoding="utf-8")
        novo = aplicar(html, CSS_INI, CSS_FIM, css, pos_css)
        novo = aplicar(novo, JS_INI, JS_FIM, js, pos_js)
        if novo != html:
            defasadas.append(lp)
            if not check:
                path.write_text(novo, encoding="utf-8", newline=eol)
    verbo = "defasadas" if check else "atualizadas"
    print(f"{len(defasadas)}/{len(LPS)} LPs {verbo}" + ("".join(f"\n  - {lp}" for lp in defasadas)))
    if check and defasadas:
        sys.exit(1)


if __name__ == "__main__":
    main()
