# -*- coding: utf-8 -*-
"""Relatorio publico de evolucao semanal do CM LATAM (deals / reunioes / fechamentos).

Gera a pagina estatica que fica no ar, SEM SENHA, em
https://relatorio-cm-latam-2026.vercel.app (projeto Vercel isolado `relatorio-cm-latam-2026`,
time elife-group) — feita pro Victor enviar aos diretores, que nao tem acesso a dashboard
interna. E a excecao ao padrao das dashboards CM (todas com senha forte). Conteudo e 100%
agregado: nenhum nome de deal, nenhum e-mail.

Como atualizar:
  1. `/dashboard-atualizar latam`  (reexporta dados-latam.json — senao os numeros congelam)
  2. `py dashboard-latam-vercel/gerar_relatorio_publico.py`
  3. `cd <sibling> && vercel deploy --prod --yes`  (o guard de deploy vai pedir confirmacao)
     sibling = C:/Users/titof/Downloads/Claude/relatorio-cm-latam-2026 (fora do repo)

Fonte: dashboard-latam-vercel/dados-latam.json (o mesmo JSON da dashboard, ja no escopo CM).
Contagem espelha o motor.js: leads por d_lead, reunioes por d_reunion, fechamentos por d_fech.

Graficos: SVG inline, zero JS. Paleta e tipografia: brand/buzzmonitor/tokens.json.
Janelas de 3 meses ("ultimos 3 meses" x "3 meses anteriores") sao MOVEIS, ancoradas em
gerado_em — nao hardcodar mes, senao o texto vira mentira no mes seguinte.

Saidas:
  1. dashboard/relatorio-evolucao-latam-2026.html  -> copia local (gitignored)
  2. <sibling>/index.html                          -> pasta do projeto Vercel publico
"""
from __future__ import annotations
import json, datetime as dt, collections, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIBLING = Path(r"C:/Users/titof/Downloads/Claude/relatorio-cm-latam-2026")
SRC = ROOT / "dashboard-latam-vercel" / "dados-latam.json"
OUT_FILE = ROOT / "dashboard" / "relatorio-evolucao-latam-2026.html"

MA = 6  # janela da media movel (semanas)

D = json.loads(SRC.read_text(encoding="utf-8"))
HOJE = dt.date.fromisoformat(D["gerado_em"])
INI = dt.date(2026, 1, 1)
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
MESES_EXT = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
             "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]


def wstart(iso: str) -> dt.date:
    x = dt.date.fromisoformat(iso)
    return x - dt.timedelta(days=x.weekday())


def rot(d: dt.date) -> str:
    return f"{d.day:02d}/{MESES[d.month - 1]}"


def no_periodo(iso: str | None) -> bool:
    return bool(iso) and INI.isoformat() <= iso <= HOJE.isoformat()


def eh_meta(r: dict) -> bool:
    return (r.get("utm_source") or "") == "meta"


# ---------- serie semanal (aceita filtro de leads) ----------
def serie(filtro=None) -> list[dict]:
    L, R, C = collections.Counter(), collections.Counter(), collections.Counter()
    for r in D["leads"]:
        if filtro and not filtro(r):
            continue
        for f, acc in (("d_lead", L), ("d_reunion", R)):
            if no_periodo(r.get(f)):
                acc[wstart(r[f])] += 1
    if filtro is None:
        for r in D["fech"]:
            if no_periodo(r.get("d_fech")):
                C[wstart(r["d_fech"])] += 1
    out, w = [], wstart(INI.isoformat())
    while w <= HOJE:
        out.append({
            "w": w,
            "ini": max(w, INI),
            "fim": min(w + dt.timedelta(days=6), HOJE),
            "leads": L[w], "reun": R[w], "fech": C[w],
            "parcial": (w + dt.timedelta(days=6)) > HOJE or w < INI,
        })
        w += dt.timedelta(days=7)
    return out


weeks = serie()
weeks_meta = serie(eh_meta)


# ---------- blocos (trimestres e janelas de 3 meses) ----------
def bloco(a: str, b: str, filtro=None) -> dict:
    ls = [r for r in D["leads"] if filtro is None or filtro(r)]
    la = sum(1 for r in ls if r.get("d_lead") and a <= r["d_lead"] <= b)
    re_ = sum(1 for r in ls if r.get("d_reunion") and a <= r["d_reunion"] <= b)
    fe = sum(1 for r in D["fech"] if r.get("d_fech") and a <= r["d_fech"] <= b)
    coorte = [r for r in ls if r.get("d_lead") and a <= r["d_lead"] <= b]
    cr = sum(1 for r in coorte if r.get("d_reunion"))
    sem = ((dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days + 1) / 7
    return {"leads": la, "reun": re_, "fech": fe, "sem": sem,
            "l_sem": la / sem, "r_sem": re_ / sem,
            "coorte": len(coorte), "coorte_reun": cr,
            "taxa": (100 * cr / len(coorte)) if coorte else 0.0}


TRIS = [("2026-01-01", "2026-03-31", "1º tri", "jan–mar"),
        ("2026-04-01", "2026-06-30", "2º tri", "abr–jun"),
        ("2026-07-01", HOJE.isoformat(), "3º tri", f"jul–{rot(HOJE)}")]
QS = []
for a, b, nome, sub in TRIS:
    q = bloco(a, b)
    q["nome"], q["sub"] = nome, sub
    q["meta"] = bloco(a, b, eh_meta)
    QS.append(q)
Q1, Q2, Q3 = QS


def desloca_meses(d: dt.date, k: int) -> dt.date:
    """Mesma data k meses atras (ajusta se o mes de destino for mais curto)."""
    m = d.month - 1 + k
    a, m = d.year + m // 12, m % 12 + 1
    dias = [31, 29 if (a % 4 == 0 and (a % 100 or a % 400 == 0)) else 28,
            31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]
    return dt.date(a, m, min(d.day, dias))


# janelas moveis de 3 meses, ancoradas em HOJE (mesmo comprimento nas duas)
R3_INI = desloca_meses(HOJE, -3) + dt.timedelta(days=1)
R2_FIM = desloca_meses(HOJE, -3)
R2_INI = desloca_meses(HOJE, -6) + dt.timedelta(days=1)
R2 = bloco(R2_INI.isoformat(), R2_FIM.isoformat())   # 3 meses anteriores
R3 = bloco(R3_INI.isoformat(), HOJE.isoformat())     # ultimos 3 meses
ANO = bloco("2026-01-01", HOJE.isoformat())
ANO_META = bloco("2026-01-01", HOJE.isoformat(), eh_meta)
VALOR = sum((r.get("valor") or 0) for r in D["fech"] if no_periodo(r.get("d_fech")))
# deals Meta que entraram com o nome do posicionamento (ficam fora do filtro utm_source='meta')
def eh_placement(r) -> bool:
    return (r.get("utm_source") or "").lower().startswith(("facebook", "instagram"))


# defasagem captacao -> reuniao (alimenta a nota de rodape, para nao congelar)
_LAGS = sorted((dt.date.fromisoformat(r["d_reunion"]) - dt.date.fromisoformat(r["d_lead"])).days
               for r in D["leads"]
               if no_periodo(r.get("d_lead")) and no_periodo(r.get("d_reunion"))
               and r["d_reunion"] >= r["d_lead"])
LAG_MED = statistics.median(_LAGS) if _LAGS else 0
LAG_P7 = round(100 * sum(1 for x in _LAGS if x <= 7) / len(_LAGS)) if _LAGS else 0

PLACEMENT = sum(1 for r in D["leads"] if no_periodo(r.get("d_lead")) and eh_placement(r))
PLACEMENT_JAN = sum(1 for r in D["leads"] if r.get("d_lead", "").startswith("2026-01")
                    and eh_placement(r))


# ---------- helpers ----------
def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def n(v, casas=0):
    # pt-BR: ponto separa milhar, virgula separa decimal
    return f"{v:,.{casas}f}".replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def delta(a, b):
    if not a:
        return "—"
    x = 100 * (b - a) / a
    return f"{'+' if x >= 0 else ''}{n(x, 0)}%"


def media_movel(vals, janela=MA):
    return [sum(vals[max(0, i - janela + 1):i + 1]) / len(vals[max(0, i - janela + 1):i + 1])
            for i in range(len(vals))]


# ===================== grafico semanal (reusavel) =====================
def chart_semanal(rows, tendencia="reun", com_fech=True, rotulo=None):
    """Barras = deals (eixo esq.) · linha = reunioes (eixo dir.) · tracejada = media movel."""
    W, H = 1120, (400 if com_fech else 360)
    ML, MR, MT = 58, 52, 16
    MB = 80 if com_fech else 52
    PW, PH = W - ML - MR, H - MT - MB
    topL = max(20, int((max(x["leads"] for x in rows) // 20 + 1) * 20))
    topR = max(4, int((max(x["reun"] for x in rows) // 2 + 1) * 2))
    step = PW / len(rows)
    bw = min(20, step * 0.6)

    def yl(v): return MT + PH - (v / topL) * PH
    def yr(v): return MT + PH - (v / topR) * PH
    def xc(i): return ML + step * i + step / 2

    g = []
    for k in range(0, topL + 1, max(1, topL // 4)):
        y = yl(k)
        g.append(f'<line class="grid" x1="{ML}" y1="{y:.1f}" x2="{ML + PW}" y2="{y:.1f}"/>')
        g.append(f'<text class="ax" x="{ML - 12}" y="{y + 4:.1f}" text-anchor="end">{k}</text>')
    for k in range(0, topR + 1, max(1, topR // 4)):
        g.append(f'<text class="ax ax-r" x="{ML + PW + 12}" y="{yr(k) + 4:.1f}">{k}</text>')

    for i, x in enumerate(rows):
        if x["leads"] <= 0:
            continue
        h = PH - (yl(x["leads"]) - MT)
        cls = "bar bar-p" if x["parcial"] else "bar"
        g.append(f'<rect class="{cls}" x="{xc(i) - bw / 2:.1f}" y="{yl(x["leads"]):.1f}" '
                 f'width="{bw:.1f}" height="{max(h, 1):.1f}" rx="2">'
                 f'<title>{rot(x["ini"])}–{rot(x["fim"])}: {x["leads"]} deals</title></rect>')

    # tendencia: media movel de MA semanas, tracejada cinza
    if tendencia == "reun":
        mm, esc_y = media_movel([x["reun"] for x in rows]), yr
    else:
        mm, esc_y = media_movel([x["leads"] for x in rows]), yl
    g.append('<polyline class="trend" points="'
             + " ".join(f'{xc(i):.1f},{esc_y(v):.1f}' for i, v in enumerate(mm)) + '"/>')

    # reunioes da semana: linha cheia + marcadores (tooltip por semana)
    g.append('<polyline class="line" points="'
             + " ".join(f'{xc(i):.1f},{yr(x["reun"]):.1f}' for i, x in enumerate(rows)) + '"/>')
    for i, x in enumerate(rows):
        g.append(f'<circle class="dot" cx="{xc(i):.1f}" cy="{yr(x["reun"]):.1f}" r="2.4">'
                 f'<title>{rot(x["ini"])}–{rot(x["fim"])}: {x["reun"]} reuniões</title></circle>')

    g.append(f'<line class="axis" x1="{ML}" y1="{MT + PH}" x2="{ML + PW}" y2="{MT + PH}"/>')
    for i, x in enumerate(rows):
        if i % 2 == 0:
            g.append(f'<text class="tick" x="{xc(i):.1f}" y="{MT + PH + 17}" '
                     f'text-anchor="middle">{rot(x["ini"])}</text>')

    if com_fech:
        LANE = MT + PH + 38
        g.append(f'<text class="lane-lbl" x="{ML - 12}" y="{LANE + 4}" text-anchor="end">Fech.</text>')
        g.append(f'<line class="lane" x1="{ML}" y1="{LANE}" x2="{ML + PW}" y2="{LANE}"/>')
        for i, x in enumerate(rows):
            if x["fech"]:
                cx, cy = xc(i), LANE
                g.append(f'<path class="diam" d="M {cx:.1f} {cy - 6} L {cx + 6:.1f} {cy} '
                         f'L {cx:.1f} {cy + 6} L {cx - 6:.1f} {cy} Z">'
                         f'<title>{rot(x["ini"])}–{rot(x["fim"])}: {x["fech"]} fechamento(s)</title></path>')

    return (f'<svg viewBox="0 0 {W} {H}" role="img" preserveAspectRatio="xMidYMid meet" '
            f'aria-label="{esc(rotulo or "Evolução semanal de deals e reuniões")}">{"".join(g)}</svg>')


chart_geral = chart_semanal(
    weeks, tendencia="reun", com_fech=True,
    rotulo=f"Evolução semanal de deals, reuniões e fechamentos de janeiro a {rot(HOJE)} de 2026")
chart_meta = chart_semanal(
    weeks_meta, tendencia="reun", com_fech=False,
    rotulo=f"Evolução semanal de deals e reuniões de tráfego Meta de janeiro a {rot(HOJE)} de 2026")


# ===================== paineis por trimestre =====================
def painel(titulo, vals, fmt, klass, sufixo=""):
    w, h = 340, 196
    ml, mr, mt, mb = 12, 12, 28, 42
    pw, ph = w - ml - mr, h - mt - mb
    top = (max(vals) * 1.3) or 1
    bw2, st = 60, pw / len(vals)
    out = [f'<line class="axis" x1="{ml}" y1="{mt + ph}" x2="{ml + pw}" y2="{mt + ph}"/>']
    for i, v in enumerate(vals):
        cx = ml + st * i + st / 2
        bh = (v / top) * ph
        y = mt + ph - bh
        ultimo = " q-now" if i == len(vals) - 1 else ""
        out.append(f'<rect class="qbar {klass}{ultimo}" x="{cx - bw2 / 2:.1f}" y="{y:.1f}" '
                   f'width="{bw2}" height="{max(bh, 1):.1f}" rx="3"/>')
        out.append(f'<text class="qval" x="{cx:.1f}" y="{y - 9:.1f}" '
                   f'text-anchor="middle">{fmt(v)}{sufixo}</text>')
        out.append(f'<text class="qlbl" x="{cx:.1f}" y="{mt + ph + 18:.1f}" '
                   f'text-anchor="middle">{QS[i]["nome"]}</text>')
        out.append(f'<text class="qsub" x="{cx:.1f}" y="{mt + ph + 32:.1f}" '
                   f'text-anchor="middle">{QS[i]["sub"]}</text>')
    return (f'<figure class="panel"><figcaption>{titulo}</figcaption>'
            f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(titulo)} por trimestre">'
            f'{"".join(out)}</svg></figure>')


p1 = painel("Deals por semana", [q["l_sem"] for q in QS], lambda v: n(v, 1), "c-deal")
p2 = painel("Reuniões por semana", [q["r_sem"] for q in QS], lambda v: n(v, 2), "c-reu")
p3 = painel("Deals que viraram reunião", [q["taxa"] for q in QS], lambda v: n(v, 1), "c-fech", "%")

# ===================== CSS =====================
CSS = """
  /* Tema unico e deliberado: claro em qualquer viewer (relatorio impresso/anexado).
     Nao ha bloco de dark mode de proposito — todas as cores sao pintadas explicitamente. */
  :root {
    color-scheme: light;
    --ground:#F6F2F8; --surface:#FFFFFF; --ink:#1A1420; --mut:#6B6073;
    --line:#E7DFEC; --line-soft:#F0EAF3; --soft:#FBF8FC;
    --deal:#390155; --deal-soft:#D9C2E6; --reu:#C2611B; --fech:#0E9D9B; --pos:#0E7C6F;
    --trend:#8C8395;
  }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--ground); color:var(--ink);
    font:16px/1.6 Lato,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    -webkit-font-smoothing:antialiased; }
  .wrap { max-width:1180px; margin:0 auto; padding:40px 24px 64px; }
  h1, h2, .kpi .val, .eyebrow { font-family:"League Spartan",Lato,"Segoe UI",Helvetica,Arial,sans-serif; }
  header { margin-bottom:28px; }
  .eyebrow { font-size:12px; font-weight:700; letter-spacing:.14em; text-transform:uppercase;
    color:var(--deal); margin:0 0 10px; }
  h1 { font-size:34px; font-weight:700; line-height:1.12; letter-spacing:-.015em;
    margin:0 0 8px; text-wrap:balance; max-width:22ch; }
  .sub { color:var(--mut); font-size:14.5px; margin:0; max-width:80ch; }
  .card { background:var(--surface); border:1px solid var(--line); border-radius:16px;
    padding:24px 26px; margin-bottom:18px; }
  .kpis { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:18px; }
  .kpi { background:var(--surface); border:1px solid var(--line); border-radius:16px; padding:20px 22px; }
  .kpi .lbl { font-size:11.5px; font-weight:700; letter-spacing:.1em; text-transform:uppercase;
    color:var(--mut); margin-bottom:10px; }
  .kpi .val { font-size:38px; font-weight:700; letter-spacing:-.02em; line-height:1;
    font-variant-numeric:tabular-nums; }
  .kpi .hint { font-size:13px; color:var(--mut); margin-top:9px; }
  .kpi .up { color:var(--pos); font-weight:700; }
  h2 { font-size:19px; font-weight:600; margin:0 0 4px; letter-spacing:-.01em; }
  .capt { font-size:13px; color:var(--mut); margin:0 0 18px; max-width:92ch; }
  .chart { overflow-x:auto; }
  .chart svg { min-width:660px; }
  svg { display:block; width:100%; height:auto; }
  .grid { stroke:var(--line-soft); stroke-width:1; }
  .axis, .lane { stroke:var(--line); stroke-width:1; }
  .ax { font-size:11px; fill:var(--mut); font-variant-numeric:tabular-nums; }
  .ax-r { fill:var(--reu); }
  .tick { font-size:10px; fill:var(--mut); }
  .lane-lbl { font-size:11px; fill:var(--mut); }
  .bar { fill:var(--deal); }
  .bar-p { fill:var(--deal-soft); }
  .line { fill:none; stroke:var(--reu); stroke-width:2.2; stroke-linejoin:round; stroke-linecap:round; }
  .dot { fill:var(--surface); stroke:var(--reu); stroke-width:1.5; }
  .trend { fill:none; stroke:var(--trend); stroke-width:2; stroke-dasharray:6 5;
    stroke-linecap:round; }
  .diam { fill:var(--fech); }
  .legend { display:flex; gap:14px 24px; flex-wrap:wrap; font-size:13px; color:var(--mut); margin:2px 0 16px; }
  .legend span { display:inline-flex; align-items:center; gap:8px; }
  .sw { width:12px; height:12px; border-radius:3px; display:inline-block; background:var(--deal); }
  .sw-soft { background:var(--deal-soft); }
  .sw-line { width:18px; height:3px; border-radius:2px; background:var(--reu); display:inline-block; }
  .sw-dash { width:20px; height:0; border-top:2px dashed var(--trend); display:inline-block; }
  .sw-d { width:11px; height:11px; background:var(--fech); transform:rotate(45deg);
    border-radius:2px; display:inline-block; }
  .panels { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }
  .panel { background:var(--soft); border:1px solid var(--line); border-radius:12px;
    padding:15px 10px 6px; margin:0; }
  .panel figcaption { font-size:13px; margin:0 0 4px; text-align:center; color:var(--ink);
    font-weight:700; }
  .qbar { opacity:.42; }
  .qbar.q-now { opacity:1; }
  .c-deal { fill:var(--deal); }
  .c-reu { fill:var(--reu); }
  .c-fech { fill:var(--fech); }
  .qval { font-size:15px; font-weight:700; fill:var(--ink); font-variant-numeric:tabular-nums; }
  .qlbl { font-size:12px; font-weight:700; fill:var(--ink); }
  .qsub { font-size:10.5px; fill:var(--mut); }
  ul.read { margin:10px 0 0; padding-left:0; list-style:none; display:grid; gap:15px; }
  ul.read li { position:relative; padding-left:24px; font-size:15px; max-width:92ch; }
  ul.read li::before { content:""; position:absolute; left:6px; top:10px; width:7px; height:7px;
    border-radius:99px; background:var(--deal); }
  .foot { font-size:12.5px; color:var(--mut); line-height:1.75; border-top:1px solid var(--line);
    padding-top:16px; margin:22px 0 0; max-width:104ch; }
  @media (max-width:900px) { .kpis, .panels { grid-template-columns:1fr 1fr; } h1 { font-size:27px; } }
  @media (max-width:560px) { .kpis, .panels { grid-template-columns:1fr; } .wrap { padding:28px 16px 48px; } }
  @media print { body { background:#fff; } .card, .kpi, .panel { break-inside:avoid; } }
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=League+Spartan:wght@600;700&family=Lato:wght@400;700&display=swap">')

BODY = f"""<div class="wrap">
  <header>
    <p class="eyebrow">Content Marketing · Buzzmonitor LATAM</p>
    <h1>Evolução semanal de deals, reuniões e fechamentos</h1>
    <p class="sub">1º de janeiro a {HOJE.day} de {MESES_EXT[HOJE.month - 1]} de 2026 · fonte: dashboard CM LATAM (inbound + outbound, escopo Content Marketing)</p>
  </header>

  <div class="kpis">
    <div class="kpi"><div class="lbl">Deals no ano</div><div class="val">{n(ANO['leads'])}</div>
      <div class="hint">{n(ANO['l_sem'], 1)} por semana em média</div></div>
    <div class="kpi"><div class="lbl">Reuniões</div><div class="val">{n(ANO['reun'])}</div>
      <div class="hint"><span class="up">{delta(Q1['r_sem'], Q3['r_sem'])}</span> por semana vs. 1º tri</div></div>
    <div class="kpi"><div class="lbl">Deals → reunião</div><div class="val">{n(R3['taxa'], 1)}%</div>
      <div class="hint">nos últimos 3 meses · era {n(Q1['taxa'], 1)}% no 1º tri</div></div>
    <div class="kpi"><div class="lbl">Fechamentos</div><div class="val">{ANO['fech']}</div>
      <div class="hint">US$ {n(VALOR)} em contratos</div></div>
  </div>

  <section class="card">
    <h2>Semana a semana</h2>
    <p class="capt">Deals captados (barras, eixo à esquerda) · reuniões realizadas (linha, eixo à direita) · fechamentos (losangos)</p>
    <div class="legend">
      <span><i class="sw"></i> Deals</span>
      <span><i class="sw-line"></i> Reuniões na semana</span>
      <span><i class="sw-dash"></i> Tendência das reuniões ({MA} semanas)</span>
      <span><i class="sw-d"></i> Fechamento</span>
      <span><i class="sw sw-soft"></i> Semana parcial</span>
    </div>
    <div class="chart">{chart_geral}</div>
  </section>

  <section class="card">
    <h2>Só tráfego Meta</h2>
    <p class="capt">Recorte dos deals com <code>utm_source = meta</code> — {n(ANO_META['leads'])} dos {n(ANO['leads'])} deals do ano, com as {n(ANO_META['reun'])} reuniões que vieram deles. Não inclui {PLACEMENT} deals que entraram com o nome do posicionamento em vez de <code>meta</code> (<code>Facebook_*</code>, <code>Instagram_*</code>) — {PLACEMENT_JAN} deles em janeiro.</p>
    <div class="legend">
      <span><i class="sw"></i> Deals de Meta</span>
      <span><i class="sw-line"></i> Reuniões na semana</span>
      <span><i class="sw-dash"></i> Tendência das reuniões ({MA} semanas)</span>
      <span><i class="sw sw-soft"></i> Semana parcial</span>
    </div>
    <div class="chart">{chart_meta}</div>
  </section>

  <section class="card">
    <h2>Por trimestre — o funil ficou mais eficiente</h2>
    <p class="capt">Médias semanais, que seguem comparáveis mesmo com o 3º trimestre em curso (jul a {rot(HOJE)}), e a conversão dos deals captados em cada período</p>
    <div class="panels">{p1}{p2}{p3}</div>
  </section>

  <section class="card">
    <h2>Leitura</h2>
    <ul class="read">
      <li><b>As reuniões subiram {delta(Q1['r_sem'], Q3['r_sem'])} por semana</b> em relação ao 1º trimestre ({n(Q1['r_sem'], 2)} → {n(Q3['r_sem'], 2)} por semana) e se mantêm nesse patamar desde abril.</li>
      <li><b>Cada deal passou a valer mais.</b> {n(Q1['taxa'], 1)}% dos deals captados no 1º trimestre viraram reunião, contra {n(R3['taxa'], 1)}% dos últimos três meses — {n(R3['taxa'] / Q1['taxa'], 1)}x mais eficiência. O funil entrega mais reunião com menos volume.</li>
      <li><b>O volume está em recuperação:</b> {n(R3['l_sem'], 1)} deals por semana nos últimos três meses, contra {n(R2['l_sem'], 1)} nos três anteriores ({delta(R2['l_sem'], R3['l_sem'])}). O pico de janeiro veio de um único criativo de topo de funil, que trouxe 149 deals e 1 reunião — volume que inflava o número sem gerar pipeline.</li>
      <li><b>Meta ainda gera menos deals que no 1º trimestre</b> ({n(Q3['meta']['l_sem'], 1)} por semana no 3º tri contra {n(Q1['meta']['l_sem'], 1)} no 1º), mas já são {delta(Q2['meta']['l_sem'], Q3['meta']['l_sem'])} sobre o 2º trimestre — e as reuniões vindas de Meta estão no melhor nível do ano: {n(Q3['meta']['r_sem'], 2)} por semana, contra {n(Q1['meta']['r_sem'], 2)} no 1º trimestre.</li>
      <li><b>Os fechamentos seguem raros:</b> {ANO['fech']} no ano, US$ {n(VALOR)} em contratos. Com o novo patamar de reuniões, é o indicador com mais espaço para destravar no 4º trimestre.</li>
    </ul>
  </section>

  <p class="foot">
    Escopo Content Marketing da dashboard CM Buzzmonitor LATAM — mesmo critério de UTM e mesma base de deals.
    Semanas de segunda a domingo; a primeira ({rot(weeks[0]['ini'])}–{rot(weeks[0]['fim'])}) e a última ({rot(weeks[-1]['ini'])}–{rot(weeks[-1]['fim'])}) são parciais.
    Deals e reuniões são contados pela data do evento; a taxa de conversão é por coorte — deals captados no período que marcaram reunião.
    A reunião costuma ser marcada logo após a captação (mediana de {n(LAG_MED, 0)} dia{"s" if LAG_MED != 1 else ""}, {LAG_P7}% em até 7 dias), então as coortes recentes já estão praticamente fechadas.
    Fechamentos vêm da base de contratos, pela data de fechamento. Dados de {HOJE.strftime('%d/%m/%Y')}.
  </p>
</div>"""

TITULO = "Content Marketing LATAM 2026"

OUT_FILE.write_text(
    f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{TITULO}</title>
{FONTS}
<style>{CSS}</style>
</head>
<body>
{BODY}
</body>
</html>
""", encoding="utf-8")

if SIBLING.exists():
    (SIBLING / "index.html").write_text(OUT_FILE.read_text(encoding="utf-8"), encoding="utf-8")

print("OK ->", OUT_FILE.name, f"{OUT_FILE.stat().st_size / 1024:.1f} KB"
      + (" | sibling atualizada" if SIBLING.exists() else " | SIBLING NAO ENCONTRADA"))
print(f"dados de {HOJE} | media movel = {MA} semanas")
print("GERAL  deals", ANO["leads"], "reun", ANO["reun"], "fech", ANO["fech"])
print("META   deals", ANO_META["leads"], "reun", ANO_META["reun"])
print("pico semanal meta:", max(x["leads"] for x in weeks_meta),
      "| reun max:", max(x["reun"] for x in weeks_meta))
for q in QS:
    print(f'  {q["nome"]} {q["sub"]:10s} | geral {q["l_sem"]:5.1f} deals/sem {q["r_sem"]:4.2f} reun/sem '
          f'| META {q["meta"]["l_sem"]:5.1f} deals/sem {q["meta"]["r_sem"]:4.2f} reun/sem '
          f'taxa {q["meta"]["taxa"]:4.1f}%')
