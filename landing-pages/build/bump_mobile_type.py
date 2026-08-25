"""bump_mobile_type.py — aplica os pisos minimos de tipografia mobile (GUIDELINES 20).

No mobile toda LP do repo caia no MINIMO do clamp (ex: h1 clamp(30px, 5.6vw, 56px)
resolve 30px num iPhone) ou num px cravado de 13-16px. Resultado: corpo de texto
16px e H1 30px numa tela de 375px — legivel, mas pequeno demais pra LP de
marketing (reportado pelo Victor em 2026-08-25 na LP monitoramento-com-ia).

O que o script faz, deterministicamente e so dentro dos blocos <style>:

  1. clamp(MIN, Vvw, MAX) em font-size -> eleva MIN ao piso da faixa do MAX
     (nunca abaixa, nunca passa do MAX). Desktop fica intacto: MAX nao muda.
  2. font-size cravado em px em regra de topo -> reescreve so no mobile, via um
     bloco `@media (max-width:640px)` anexado no fim do <style>, repetindo o
     MESMO seletor (cascata e especificidade preservadas). Desktop intacto.

Duas exclusoes, ambas pra nao estourar layout:

  - regra com `white-space:nowrap` fica INTOCADA. Pilula de kicker, badge e CTA
    de navbar nao reflui: +1px de fonte vira overflow horizontal na hora
    (comprovado em 8 LPs na primeira passada — hero-kicker, navbar__cta,
    hero-form-badge).
  - seletor que a LP ja ajusta dentro de algum `@media (max-width:...)` fica
    fora do passo 2 — ali o ajuste foi deliberado.

Uso:
    py bump_mobile_type.py --dry-run <arquivo-ou-pasta>...   # relatorio, nao grava
    py bump_mobile_type.py <arquivo-ou-pasta>...             # aplica

Valide com check_mobile_type.py (baseline antes x depois) — o que importa e
overflow NOVO. Idempotente: rodar duas vezes nao muda nada.
Exit 0 = OK; exit 1 = erro.
"""
import argparse
import os
import re
import sys

MARKER = "GUIDELINES 20 - pisos de tipografia mobile"
MOBILE_BP = 640

# --- passo 1: piso do MIN do clamp, por faixa do MAX (o "papel" do texto) ---
# (faixa_min, faixa_max, piso) -- primeira faixa que casa vence
CLAMP_FLOORS = (
    (44, 999, 34),   # display / H1 hero
    (36,  43, 28),   # H1 secundario / H2 grande
    (30,  35, 26),   # H2 de secao
    (24,  29, 22),   # H3 / titulo de card
    (20,  23, 18),   # subhead / numero destacado
    (17,  19, 18),   # lead (max costuma ser 18 -> lead fica 18 no mobile)
    (0,   16, 14),   # texto pequeno
)

# --- passo 2: piso do px cravado (so mobile) ---
# Sempre +1px, nunca mais. Tentei 14->16 pra dar mais folga no corpo de card e
# quebrou: `.btn-sm` (14px) herda `white-space:nowrap` de `.btn` — regra IRMA, que
# analise estatica por regra nao ve — e +2px estourou o header em
# plataforma-completa-atendimento e o eyebrow em la-mejor-plataforma-*-es.
# Com +1px: zero regressao em 132 LPs. Quem precisa de mais sobe o clamp.
PX_FLOOR = {10: 12, 11: 12, 12: 13, 13: 14, 14: 15, 15: 16, 16: 17}

FONT_SIZE_CLAMP = re.compile(
    r"font-size\s*:\s*clamp\(\s*([\d.]+)px\s*,([^,()]+),\s*([\d.]+)px\s*\)", re.I)
FONT_SIZE_PX = re.compile(r"font-size\s*:\s*([\d.]+)px", re.I)
STYLE_BLOCK = re.compile(r"(<style\b[^>]*>)(.*?)(</style>)", re.I | re.S)
MAXW_MEDIA = re.compile(r"max-width\s*:\s*[\d.]+\s*px", re.I)
NOWRAP = re.compile(r"white-space\s*:\s*nowrap", re.I)

# Header/navbar e linha unica de altura fixa: logo + CTA ocupam a largura toda e
# nao sobra folga. Crescer a fonte ali estoura o viewport (agencias-es empurrou o
# botao de menu 5px pra fora; plataforma-completa-atendimento, 11px). E chrome,
# nao texto de leitura — fica no tamanho que esta.
CHROME = re.compile(r"(^|[\s.#>+~\[])(site-)?(header|nav|navbar|topbar|menu|brand|logo)"
                    r"([-_A-Za-z0-9]*)?\b", re.I)
# seletor de header, pra conter o cascade quando o `body` sobe de tamanho
HEADER_SELS = ("header", ".navbar", ".site-header", ".nav", ".topbar")
BODY_SEL = re.compile(r"^\s*(html\s*,\s*)?body\s*$", re.I)


def eh_chrome(sel):
    return any(CHROME.search(p) for p in sel.split(","))


def clamp_floor(maxv):
    for lo, hi, floor in CLAMP_FLOORS:
        if lo <= maxv <= hi:
            return floor
    return 0


def num(v):
    f = float(v)
    return int(f) if f == int(f) else f


def blank_comments(css):
    """Troca cada /*...*/ por espacos do mesmo tamanho (offsets preservados)."""
    out = []
    i = 0
    while i < len(css):
        j = css.find("/*", i)
        if j < 0:
            out.append(css[i:])
            break
        out.append(css[i:j])
        k = css.find("*/", j + 2)
        k = len(css) if k < 0 else k + 2
        out.append(" " * (k - j))
        i = k
    return "".join(out)


def walk(css):
    """Todas as regras do CSS, com offsets no texto ORIGINAL.

    Devolve lista de dicts: prelude, ini/fim do corpo, depth, e se esta dentro
    de algum @media com max-width.
    """
    clean = blank_comments(css)
    found = []

    def rec(lo, hi, depth, in_maxw):
        i, start = lo, lo
        while i < hi:
            c = clean[i]
            if c == "}":            # fecha bloco do nivel de cima
                return
            if c == "{":
                prelude = clean[start:i].strip()
                depth_b, j = 1, i + 1
                while j < hi and depth_b:
                    if clean[j] == "{":
                        depth_b += 1
                    elif clean[j] == "}":
                        depth_b -= 1
                    j += 1
                body_ini, body_fim = i + 1, j - 1
                if prelude.startswith("@"):
                    if depth < 4:
                        rec(body_ini, body_fim, depth + 1,
                            in_maxw or bool(MAXW_MEDIA.search(prelude)))
                elif prelude:
                    found.append({"sel": prelude, "ini": body_ini, "fim": body_fim,
                                  "depth": depth, "in_maxw": in_maxw})
                i = start = j
                continue
            i += 1

    rec(0, len(clean), 0, False)
    return found


def norm_sel(sel):
    return re.sub(r"\s+", " ", sel.strip())


def process_style(css, headers=()):
    """Devolve (css_novo, mudancas_clamp, mudancas_px).

    `headers`: seletores de header presentes no HTML — recebem pin no tamanho
    original se o `body` subir, pra o aumento nao cascatear pro topo da pagina.
    """
    if MARKER in css:
        return css, [], []

    rules = walk(css)
    clamp_changes, edits = [], []
    tuned = set()

    for r in rules:
        body = css[r["ini"]:r["fim"]]
        if r["in_maxw"] and (FONT_SIZE_PX.search(body) or FONT_SIZE_CLAMP.search(body)):
            tuned.update(norm_sel(s) for s in r["sel"].split(","))
        if NOWRAP.search(blank_comments(body)) or eh_chrome(r["sel"]):
            continue        # nao reflui (pilula/badge) ou e chrome de header/nav
        for m in FONT_SIZE_CLAMP.finditer(body):
            mn, mid, mx = float(m.group(1)), m.group(2), float(m.group(3))
            target = min(max(mn, clamp_floor(mx)), mx)
            if target <= mn:
                continue
            # `mid` ja vem com o espaco da esquerda; o da direita entra aqui, pra
            # o diff sair no mesmo formato que o time escreve: clamp(a, b, c)
            novo = "font-size:clamp(%spx,%s, %spx)" % (num(target), mid.strip() and mid,
                                                       num(m.group(3)))
            edits.append((r["ini"] + m.start(), r["ini"] + m.end(), novo))
            clamp_changes.append((num(m.group(1)), num(target), num(m.group(3))))

    # aplica as substituicoes de clamp de tras pra frente (offsets preservados)
    for ini, fim, novo in sorted(edits, reverse=True):
        css = css[:ini] + novo + css[fim:]

    # ---- passo 2: px cravado, so no mobile ----
    rules = walk(css)
    px_changes, seen = [], set()
    for r in rules:
        if r["depth"] != 0 or r["in_maxw"]:
            continue
        body = blank_comments(css[r["ini"]:r["fim"]])
        if NOWRAP.search(body) or eh_chrome(r["sel"]):
            continue
        last = None
        for m in FONT_SIZE_PX.finditer(body):
            antes = body[max(0, m.start() - 30):m.start()]
            if "clamp(" in antes and ")" not in antes.split("clamp(")[-1]:
                continue        # px que faz parte de um clamp(): ja tratado
            last = m
        if last is None:
            continue
        val = float(last.group(1))
        # px fracionado (ex: 14.5px, comum em escala tipografica calculada) conta
        # pelo inteiro mais proximo — arredondar pra baixo deixaria 14.5 de fora.
        novo = PX_FLOOR.get(int(round(val)))
        if not novo or novo <= val:
            continue
        parts = [p for p in (norm_sel(p) for p in r["sel"].split(",")) if p]
        parts = [p for p in parts if p not in tuned]
        if not parts:
            continue
        key = (",".join(parts), novo)
        if key in seen:
            continue
        seen.add(key)
        px_changes.append((",".join(parts), num(val), novo))

    if px_changes:
        linhas = ["  %s{ font-size:%spx; }" % (sel, novo) for sel, _o, novo in px_changes]
        # `body` maior cascateia pro header, que nao tem folga -> pin no original
        antigo_body = next((o for sel, o, _n in px_changes if BODY_SEL.match(sel)), None)
        if antigo_body is not None and headers:
            linhas.append("  /* header nao acompanha: linha unica sem folga */")
            linhas.append("  %s{ font-size:%spx; }"
                          % (", ".join(headers), num(antigo_body)))
        css = css.rstrip() + (
            "\n\n  /* ===== %s ===== */\n  @media (max-width:%dpx){\n%s\n  }\n"
            % (MARKER, MOBILE_BP, "\n".join(linhas)))

    return css, clamp_changes, px_changes


def transform_html(html):
    """Ponto de entrada unico: aplica os pisos num HTML e devolve (novo, report).

    process_file e qualquer harness externo passam por aqui — chamar
    process_style direto perde a deteccao de header (o pin do cascade do body).
    """
    report = {"clamp": [], "px": [],
              "inline": len(re.findall(r'style="[^"]*font-size', html))}
    corpo_html = re.sub(r"<style\b.*?</style>", "", html, flags=re.I | re.S)
    headers = [s for s in HEADER_SELS
               if re.search(r"<%s\b" % s if not s.startswith(".")
                            else r'class="[^"]*\b%s\b' % s[1:], corpo_html, re.I)]

    def sub_style(m):
        novo, cc, pc = process_style(m.group(2), headers)
        report["clamp"] += cc
        report["px"] += pc
        return m.group(1) + novo + m.group(3)

    return STYLE_BLOCK.sub(sub_style, html), report


def process_file(path, apply):
    with open(path, "r", encoding="utf-8", newline="") as f:
        html = f.read()
    out, report = transform_html(html)
    changed = [out != html]
    if changed[0] and apply:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(out)
    return changed[0], report


def collect(targets):
    files = []
    for t in targets:
        if os.path.isdir(t):
            for base, _d, fs in os.walk(t):
                norm = base.replace("\\", "/")
                if "_experimentos" in norm or "/extras/" in norm + "/":
                    continue
                if "index.html" in fs:
                    files.append(os.path.join(base, "index.html"))
        elif os.path.isfile(t):
            files.append(t)
        else:
            sys.stderr.write("ERRO: alvo inexistente: %s\n" % t)
            sys.exit(1)
    return sorted(set(files))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    files = collect(args.targets)
    tot_c = tot_p = n_changed = 0
    inline = []
    for f in files:
        rel = os.path.relpath(f).replace("\\", "/")
        ch, rep = process_file(f, apply=not args.dry_run)
        if rep["inline"]:
            inline.append((rel, rep["inline"]))
        if not ch:
            continue
        n_changed += 1
        tot_c += len(rep["clamp"])
        tot_p += len(rep["px"])
        if not args.quiet:
            print("\n" + rel)
            for old, novo, mx in rep["clamp"]:
                print("  clamp min %spx -> %spx  (max %spx)" % (old, novo, mx))
            for sel, old, novo in rep["px"]:
                print("  mobile     %spx -> %spx  %s" % (old, novo, sel))

    print("\n%s%d/%d LPs alteradas - %d clamps - %d regras px no mobile"
          % ("[dry-run] " if args.dry_run else "", n_changed, len(files), tot_c, tot_p))
    if inline:
        print("\nATENCAO - font-size inline em style=\"\" (script nao mexe, revisar a mao):")
        for rel, k in inline:
            print("  %s (%d)" % (rel, k))
    return 0


if __name__ == "__main__":
    sys.exit(main())
