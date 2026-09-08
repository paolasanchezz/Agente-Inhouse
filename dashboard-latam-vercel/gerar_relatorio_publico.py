# -*- coding: utf-8 -*-
"""Relatorio publico de evolucao semanal do CM — Buzzmonitor LATAM + Brasil.

Gera a pagina estatica que fica no ar, SEM SENHA, em
https://relatorio-cm-latam-2026.vercel.app (projeto Vercel isolado `relatorio-cm-latam-2026`,
time elife-group) — feita pro Victor enviar aos diretores, que nao tem acesso as dashboards
internas. E a excecao ao padrao das dashboards CM (todas com senha forte). Conteudo e 100%
agregado: nenhum nome de deal, nenhum e-mail. NUNCA emitir campo de PII aqui.

Duas abas (CSS puro, sem JS): LATAM e Brasil. Os graficos e as inferencias sao os MESMOS;
o que muda e o mapeamento de campos de cada base, resolvido em carregar_latam()/carregar_br().

Como atualizar:
  1. `/dashboard-atualizar latam` e `/dashboard-atualizar buzz-br` (reexporta os 2 JSONs —
     senao os numeros congelam na data do arquivo)
  2. `py dashboard-latam-vercel/gerar_relatorio_publico.py`
  3. `cd <sibling> && vercel deploy --prod --yes` (o guard de deploy vai pedir confirmacao)
     sibling = C:/Users/titof/Downloads/Claude/relatorio-cm-latam-2026 (fora do repo)

Fontes (os mesmos JSONs das dashboards, ja no escopo CM):
  LATAM  dashboard-latam-vercel/dados-latam.json — espelha o motor.js de la: deals por
         `d_lead` (1 linha = 1 deal), reunioes por `d_reunion`, fechamentos por `d_fech`
         (base de contratos separada, valor em USD).
  BRASIL dashboard-buzz-br-vercel/dados-2026.json — espelha o motor.js de la, que tem
         estrutura DIFERENTE: um array por etapa do funil (leads/ce/ra/rr/prop/fech) e
         deal contado por E-MAIL DISTINTO (nao por linha). Reuniao = `rr` (realizada,
         contagem de linhas, como no contarKpis). Fechamento em BRL.
         => somar as barras semanais NAO da o total do ano: e-mail que converteu em duas
         semanas conta nas duas (identico ao que a dashboard mostra ao trocar o intervalo).

Recorte "Meta": dentro do escopo CM (que inclui paid social), separa midia paga Meta do
resto do conteudo. LATAM: utm_source `meta` (posicionamentos `Facebook_*`/`Instagram_*`
contados a parte, na legenda). BR: `meta`/`fb` + posicionamentos `Instagram_*`/`Facebook_*`;
`ig` e `instagram` NAO entram — conferido criativo a criativo, sao link na bio / story
organico (utm_content 'bio', 'link-na-bio', 'story-01-06').

Composicao por pais: so LATAM (campo `pais` nos leads). Base = coorte do ano (deal captado
em 2026 que marcou reuniao), o unico jeito honesto de comparar taxa entre paises.

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
SRC_LATAM = ROOT / "dashboard-latam-vercel" / "dados-latam.json"
SRC_BR = ROOT / "dashboard-buzz-br-vercel" / "dados-2026.json"
OUT_FILE = ROOT / "dashboard" / "relatorio-evolucao-latam-2026.html"

MA = 6  # janela da media movel (semanas)
INI = dt.date(2026, 1, 1)
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
MESES_EXT = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
             "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]


# ============================== helpers ==============================
def wstart(iso: str) -> dt.date:
    x = dt.date.fromisoformat(iso)
    return x - dt.timedelta(days=x.weekday())


def rot(d: dt.date) -> str:
    return f"{d.day:02d}/{MESES[d.month - 1]}"


def esc(s) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def n(v, casas=0) -> str:
    # pt-BR: ponto separa milhar, virgula separa decimal
    return f"{v:,.{casas}f}".replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def delta(a, b) -> str:
    if not a:
        return "—"
    x = 100 * (b - a) / a
    return f"{'+' if x >= 0 else ''}{n(x, 0)}%"


def media_movel(vals, janela=MA):
    return [sum(vals[max(0, i - janela + 1):i + 1]) / len(vals[max(0, i - janela + 1):i + 1])
            for i in range(len(vals))]


def desloca_meses(d: dt.date, k: int) -> dt.date:
    """Mesma data k meses atras (ajusta se o mes de destino for mais curto)."""
    m = d.month - 1 + k
    a, m = d.year + m // 12, m % 12 + 1
    dias = [31, 29 if (a % 4 == 0 and (a % 100 or a % 400 == 0)) else 28,
            31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]
    return dt.date(a, m, min(d.day, dias))


def eh_meta(src, exatos, prefixos) -> bool:
    s = (src or "").lower()
    return s in exatos or (bool(prefixos) and s.startswith(prefixos))


# ============================== modelo normalizado ==============================
class Regiao:
    """Base de uma regiao no formato que os graficos consomem.

    deals : [{d, k, meta, content}]  d=data de captacao, k=chave de deduplicacao do deal
    reun  : [{d, meta}]              1 item = 1 reuniao contada (linha), como no motor.js
    fech  : [{d, valor}]
    conv  : {k: bool}                chave -> marcou reuniao alguma vez (base da coorte)
    """

    def __init__(self, chave, nome, moeda, hoje, deals, reun, fech, conv, lags,
                 placements=0, placements_1t=0, paises=None, fonte=""):
        self.chave, self.nome, self.moeda, self.fonte = chave, nome, moeda, fonte
        self.hoje = hoje
        self.deals, self.reun, self.fech, self.conv = deals, reun, fech, conv
        self.placements, self.placements_1t = placements, placements_1t
        self.paises = paises or {}
        lags = sorted(x for x in lags if x >= 0)
        self.lag_med = statistics.median(lags) if lags else 0
        self.lag_p7 = round(100 * sum(1 for x in lags if x <= 7) / len(lags)) if lags else 0

    def no_periodo(self, iso) -> bool:
        return bool(iso) and INI.isoformat() <= iso <= self.hoje.isoformat()

    # --- serie semanal ---
    def serie(self, so_meta=False) -> list[dict]:
        L = collections.defaultdict(set)
        R, C = collections.Counter(), collections.Counter()
        for r in self.deals:
            if (so_meta and not r["meta"]) or not self.no_periodo(r["d"]):
                continue
            L[wstart(r["d"])].add(r["k"])
        for r in self.reun:
            if (so_meta and not r["meta"]) or not self.no_periodo(r["d"]):
                continue
            R[wstart(r["d"])] += 1
        if not so_meta:
            for r in self.fech:
                if self.no_periodo(r["d"]):
                    C[wstart(r["d"])] += 1
        out, w = [], wstart(INI.isoformat())
        while w <= self.hoje:
            out.append({
                "w": w, "ini": max(w, INI),
                "fim": min(w + dt.timedelta(days=6), self.hoje),
                "leads": len(L[w]), "reun": R[w], "fech": C[w],
                "parcial": (w + dt.timedelta(days=6)) > self.hoje or w < INI,
            })
            w += dt.timedelta(days=7)
        return out

    # --- bloco (trimestre / janela movel de 3 meses) ---
    def bloco(self, a: str, b: str, so_meta=False) -> dict:
        coorte = set()
        for r in self.deals:
            if so_meta and not r["meta"]:
                continue
            if r["d"] and a <= r["d"] <= b:
                coorte.add(r["k"])
        re_ = sum(1 for r in self.reun
                  if (not so_meta or r["meta"]) and r["d"] and a <= r["d"] <= b)
        fe = sum(1 for r in self.fech if r["d"] and a <= r["d"] <= b)
        cr = sum(1 for k in coorte if self.conv.get(k))
        sem = ((dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days + 1) / 7
        return {"leads": len(coorte), "reun": re_, "fech": fe, "sem": sem,
                "l_sem": len(coorte) / sem, "r_sem": re_ / sem,
                "coorte": len(coorte), "coorte_reun": cr,
                "taxa": (100 * cr / len(coorte)) if coorte else 0.0}

    def valor_fech(self) -> float:
        return sum((r["valor"] or 0) for r in self.fech if self.no_periodo(r["d"]))

    def maior_criativo(self) -> dict:
        """Maior utm_content do ano em volume — serve pra checar outlier de topo de funil."""
        acc = collections.defaultdict(lambda: {"d": set(), "r": set(), "meses": collections.Counter()})
        for r in self.deals:
            if not self.no_periodo(r["d"]) or not r.get("content"):
                continue
            a = acc[r["content"]]
            a["d"].add(r["k"])
            a["meses"][r["d"][:7]] += 1
            if self.conv.get(r["k"]):
                a["r"].add(r["k"])
        if not acc:
            return {"deals": 0, "reun": 0, "mes": None, "taxa": 0.0}
        top = max(acc.values(), key=lambda a: len(a["d"]))
        mes = top["meses"].most_common(1)[0][0]
        return {"deals": len(top["d"]), "reun": len(top["r"]),
                "mes": MESES_EXT[int(mes[5:7]) - 1],
                "taxa": 100 * len(top["r"]) / len(top["d"])}


# ============================== carregadores ==============================
def carregar_latam() -> Regiao:
    D = json.loads(SRC_LATAM.read_text(encoding="utf-8"))
    hoje = dt.date.fromisoformat(D["gerado_em"])
    EXATOS, PREFIXOS = {"meta"}, ()
    deals, reun, conv, lags = [], [], {}, []
    paises = collections.defaultdict(lambda: {"d": 0, "r": 0})
    for r in D["leads"]:
        m = eh_meta(r.get("utm_source"), EXATOS, PREFIXOS)
        k = r["id"]
        deals.append({"d": r.get("d_lead"), "k": k, "meta": m, "content": r.get("utm_content")})
        conv[k] = conv.get(k, False) or bool(r.get("d_reunion"))
        if r.get("d_reunion"):
            reun.append({"d": r["d_reunion"], "meta": m})
        if r.get("d_lead") and INI.isoformat() <= r["d_lead"] <= hoje.isoformat():
            p = (r.get("pais") or "").strip() or "Não declarado"
            paises[p]["d"] += 1
            if r.get("d_reunion"):
                paises[p]["r"] += 1
        if r.get("d_lead") and r.get("d_reunion") and r["d_reunion"] >= r["d_lead"]:
            lags.append((dt.date.fromisoformat(r["d_reunion"])
                         - dt.date.fromisoformat(r["d_lead"])).days)
    fech = [{"d": r.get("d_fech"), "valor": (r.get("valor") or 0)} for r in D["fech"]]
    pl = [r for r in D["leads"]
          if (r.get("utm_source") or "").lower().startswith(("facebook", "instagram"))
          and r.get("d_lead") and INI.isoformat() <= r["d_lead"] <= hoje.isoformat()]
    return Regiao("latam", "Buzzmonitor LATAM", ("US$", "USD"), hoje, deals, reun, fech, conv,
                  lags, placements=len(pl),
                  placements_1t=sum(1 for r in pl if r["d_lead"][:7] <= "2026-03"),
                  paises=dict(paises),
                  fonte="dashboard CM Buzzmonitor LATAM (inbound + outbound, escopo Content Marketing)")


def carregar_br() -> Regiao:
    """BR tem um array por etapa e conta deal por E-MAIL distinto (motor.js::contarKpis)."""
    D = json.loads(SRC_BR.read_text(encoding="utf-8"))
    hoje = dt.date.fromisoformat(D["gerado_em"])
    EXATOS, PREFIXOS = {"meta", "fb"}, ("instagram_", "facebook_")

    def em(e) -> str:
        return (e or "").strip().lower()

    deals, prim_lead, conv = [], {}, {}
    for r in D["leads"]:
        k = em(r.get("email")) or f"id:{r['id']}"
        deals.append({"d": r.get("data"), "k": k,
                      "meta": eh_meta(r.get("utm_source"), EXATOS, PREFIXOS),
                      "content": r.get("utm_content")})
        conv.setdefault(k, False)
        if r.get("data") and (k not in prim_lead or r["data"] < prim_lead[k]):
            prim_lead[k] = r["data"]
    reun = [{"d": r.get("data"), "meta": eh_meta(r.get("utm_source"), EXATOS, PREFIXOS)}
            for r in D["rr"]]
    fech = [{"d": r.get("data"), "valor": float(r.get("valor") or 0)} for r in D["fech"]]
    # coorte: e-mail que teve reuniao realizada. A unica ponte de rr pro lead e o id do deal.
    mail_por_id = {r["id"]: em(r.get("email")) for r in D["leads"]}
    lags = []
    for r in D["rr"]:
        k = mail_por_id.get(r["id"])
        if not k:
            continue
        conv[k] = True
        dl = prim_lead.get(k)
        if dl and r.get("data") and r["data"] >= dl:
            lags.append((dt.date.fromisoformat(r["data"]) - dt.date.fromisoformat(dl)).days)
    return Regiao("br", "Buzzmonitor Brasil", ("R$", "BRL"), hoje, deals, reun, fech, conv, lags,
                  fonte="dashboard CM Buzzmonitor Brasil (escopo Content Marketing, deal por e-mail distinto)")


# ============================== graficos ==============================
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

    if tendencia == "reun":
        mm, esc_y = media_movel([x["reun"] for x in rows]), yr
    else:
        mm, esc_y = media_movel([x["leads"] for x in rows]), yl
    g.append('<polyline class="trend" points="'
             + " ".join(f'{xc(i):.1f},{esc_y(v):.1f}' for i, v in enumerate(mm)) + '"/>')

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


def painel(titulo, vals, fmt, klass, nomes, subs, sufixo=""):
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
                   f'text-anchor="middle">{nomes[i]}</text>')
        out.append(f'<text class="qsub" x="{cx:.1f}" y="{mt + ph + 32:.1f}" '
                   f'text-anchor="middle">{subs[i]}</text>')
    return (f'<figure class="panel"><figcaption>{titulo}</figcaption>'
            f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(titulo)} por trimestre">'
            f'{"".join(out)}</svg></figure>')


def chart_paises(paises: dict, minimo=15):
    """Composicao por pais: barras de deals e reunioes (share) + taxa de conversao.

    Coorte do ano: deal captado em 2026 que marcou reuniao. Paises abaixo do `minimo` de
    deals viram uma linha agregada — taxa com 3 deals nao e taxa, e ruido.
    """
    NAO_PAIS = {"Não declarado", "Otro"}
    grandes = {k: v for k, v in paises.items() if v["d"] >= minimo and k not in NAO_PAIS}
    peq = {k: v for k, v in paises.items() if v["d"] < minimo and k not in NAO_PAIS}
    ndec = {k: v for k, v in paises.items() if k in NAO_PAIS}

    linhas = sorted(grandes.items(), key=lambda x: -x[1]["d"])
    if peq:
        linhas.append((f"Outros ({len(peq)} países)",
                       {"d": sum(v["d"] for v in peq.values()),
                        "r": sum(v["r"] for v in peq.values()), "agg": True}))
    if ndec:
        linhas.append(("Sem país declarado",
                       {"d": sum(v["d"] for v in ndec.values()),
                        "r": sum(v["r"] for v in ndec.values()), "agg": True}))

    TD = sum(v["d"] for v in paises.values())
    TR = sum(v["r"] for v in paises.values())
    taxa_media = 100 * TR / TD if TD else 0
    maxd = max(v["d"] for _, v in linhas)

    LBL, BH, RH = 132, 11, 46
    COLD, COLW = LBL + 16, 300           # coluna das barras
    TW, TX = 150, LBL + 16 + 300 + 226   # regua da taxa: escala fixa 0-25%
    W, H = 1120, 30 + RH * len(linhas)
    g = [f'<text class="ph" x="0" y="14">País</text>',
         f'<text class="ph" x="{COLD}" y="14">Deals no ano</text>',
         f'<text class="ph" x="{COLD + 150}" y="14">Reuniões</text>',
         f'<text class="ph" x="{TX}" y="14">Deal → reunião</text>']
    for i, ln in enumerate(linhas):
        pais, v = ln
        y = 30 + RH * i
        agg = v.get("agg")
        cls = " agg" if agg else ""
        taxa = 100 * v["r"] / v["d"] if v["d"] else 0
        g.append(f'<text class="pn{cls}" x="0" y="{y + BH}">{esc(pais)}</text>')
        # barra de deals
        wd = COLW * 0.62 * v["d"] / maxd
        g.append(f'<rect class="pbar pb-d" x="{COLD}" y="{y + 2}" width="{max(wd, 1):.1f}" '
                 f'height="{BH}" rx="2"/>')
        g.append(f'<text class="pv" x="{COLD + max(wd, 1) + 7:.1f}" y="{y + BH}">'
                 f'{v["d"]} <tspan class="pp">({n(100 * v["d"] / TD, 1)}%)</tspan></text>')
        # barra de reunioes (mesma escala relativa ao maior pais em deals, ampliada 6x
        # pra ficar legivel — a leitura de volume esta no numero, nao no comprimento)
        wr = COLW * 0.62 * (v["r"] * 6) / maxd if TR else 0
        g.append(f'<rect class="pbar pb-r" x="{COLD}" y="{y + BH + 6}" width="{max(wr, 1):.1f}" '
                 f'height="{BH - 3}" rx="2"/>')
        g.append(f'<text class="pv pv-r" x="{COLD + max(wr, 1) + 7:.1f}" y="{y + 2 * BH + 3}">'
                 f'{v["r"]} <tspan class="pp">({n(100 * v["r"] / TR, 1) if TR else 0}%)</tspan></text>')
        # taxa
        bom = taxa >= taxa_media and not agg
        g.append(f'<rect class="tbar" x="{TX}" y="{y + 5}" width="{TW}" height="{BH + 2}" rx="3"/>')
        g.append(f'<rect class="tfill{" t-bom" if bom else ""}" x="{TX}" y="{y + 5}" '
                 f'width="{max(TW * min(taxa, 25) / 25, 2):.1f}" height="{BH + 2}" rx="3"/>')
        g.append(f'<text class="tval{" t-bom" if bom else ""}" x="{TX + TW + 10}" '
                 f'y="{y + BH + 5}">{n(taxa, 1)}%</text>')
    # linha da media na regua
    xm = TX + TW * min(taxa_media, 25) / 25
    g.append(f'<line class="tmed" x1="{xm:.1f}" y1="24" x2="{xm:.1f}" y2="{H - 6}"/>')
    g.append(f'<text class="tmedl" x="{xm + 5:.1f}" y="20">média {n(taxa_media, 1)}%</text>')
    return (f'<svg viewBox="0 0 {W} {H}" role="img" preserveAspectRatio="xMinYMin meet" '
            f'aria-label="Composição de deals e reuniões por país e taxa de conversão">'
            f'{"".join(g)}</svg>')


# ============================== painel de uma regiao ==============================
def montar_regiao(reg: Regiao) -> tuple:
    """Devolve (html_do_painel, resumo_pra_stdout)."""
    HOJE = reg.hoje
    weeks = reg.serie()
    weeks_meta = reg.serie(so_meta=True)

    TRIS = [("2026-01-01", "2026-03-31", "1º tri", "jan–mar"),
            ("2026-04-01", "2026-06-30", "2º tri", "abr–jun"),
            ("2026-07-01", HOJE.isoformat(), "3º tri", f"jul–{rot(HOJE)}")]
    QS = []
    for a, b, nome, sub in TRIS:
        q = reg.bloco(a, b)
        q["nome"], q["sub"] = nome, sub
        q["meta"] = reg.bloco(a, b, so_meta=True)
        QS.append(q)
    Q1, Q2, Q3 = QS

    R3_INI = desloca_meses(HOJE, -3) + dt.timedelta(days=1)
    R2_FIM = desloca_meses(HOJE, -3)
    R2_INI = desloca_meses(HOJE, -6) + dt.timedelta(days=1)
    R2 = reg.bloco(R2_INI.isoformat(), R2_FIM.isoformat())
    R3 = reg.bloco(R3_INI.isoformat(), HOJE.isoformat())
    ANO = reg.bloco(INI.isoformat(), HOJE.isoformat())
    ANO_META = reg.bloco(INI.isoformat(), HOJE.isoformat(), so_meta=True)
    VALOR = reg.valor_fech()
    SIM, _ = reg.moeda
    TOP = reg.maior_criativo()

    chart_geral = chart_semanal(
        weeks, tendencia="reun", com_fech=True,
        rotulo=f"{reg.nome}: evolução semanal de deals, reuniões e fechamentos de janeiro a {rot(HOJE)} de 2026")
    chart_meta = chart_semanal(
        weeks_meta, tendencia="reun", com_fech=False,
        rotulo=f"{reg.nome}: evolução semanal de deals e reuniões de tráfego Meta de janeiro a {rot(HOJE)} de 2026")

    nomes = [q["nome"] for q in QS]
    subs = [q["sub"] for q in QS]
    p1 = painel("Deals por semana", [q["l_sem"] for q in QS], lambda v: n(v, 1), "c-deal", nomes, subs)
    p2 = painel("Reuniões por semana", [q["r_sem"] for q in QS], lambda v: n(v, 2), "c-reu", nomes, subs)
    p3 = painel("Deals que viraram reunião", [q["taxa"] for q in QS], lambda v: n(v, 1),
                "c-fech", nomes, subs, "%")

    # ---- nota de escopo especifica de cada base ----
    if reg.chave == "br":
        nota_base = ("Deal é contado por <b>e-mail distinto</b> e reunião pela etapa "
                     "<i>reunião realizada</i> — o mesmo critério da dashboard CM do Brasil. "
                     "Por isso a soma das barras semanais é maior que o total do ano: quem "
                     "converteu em duas semanas conta nas duas.")
        nota_meta = (f"Recorte dos deals de mídia paga Meta — <code>utm_source = meta</code> e os "
                     f"posicionamentos <code>Instagram_*</code> — {n(ANO_META['leads'])} dos "
                     f"{n(ANO['leads'])} deals do ano, com as {n(ANO_META['reun'])} reuniões que "
                     f"vieram deles. <code>ig</code> e <code>instagram</code> ficam fora: são link "
                     f"na bio e story orgânico, não mídia paga.")
    else:
        nota_base = ("Deal é contado por linha de deal e reunião pela data da reunião — o mesmo "
                     "critério da dashboard CM LATAM. Fechamentos vêm da base de contratos.")
        nota_meta = (f"Recorte dos deals com <code>utm_source = meta</code> — "
                     f"{n(ANO_META['leads'])} dos {n(ANO['leads'])} deals do ano, com as "
                     f"{n(ANO_META['reun'])} reuniões que vieram deles. Não inclui "
                     f"{reg.placements} deals que entraram com o nome do posicionamento em vez de "
                     f"<code>meta</code> (<code>Facebook_*</code>, <code>Instagram_*</code>) — "
                     f"{reg.placements_1t} deles no 1º trimestre.")

    # ---- leitura (tudo calculado) ----
    itens = []
    itens.append(f"<b>As reuniões {'subiram' if Q3['r_sem'] >= Q1['r_sem'] else 'caíram'} "
                 f"{delta(Q1['r_sem'], Q3['r_sem'])} por semana</b> em relação ao 1º trimestre "
                 f"({n(Q1['r_sem'], 2)} → {n(Q3['r_sem'], 2)} por semana). No 2º trimestre foram "
                 f"{n(Q2['r_sem'], 2)}.")
    if Q1["taxa"] and R3["taxa"]:
        subiu = R3["taxa"] >= Q1["taxa"]
        fator = R3["taxa"] / Q1["taxa"] if subiu else Q1["taxa"] / R3["taxa"]
        itens.append(f"<b>Cada deal passou a valer {'mais' if subiu else 'menos'}.</b> "
                     f"{n(Q1['taxa'], 1)}% dos deals captados no 1º trimestre viraram reunião, "
                     f"contra {n(R3['taxa'], 1)}% dos últimos três meses — {n(fator, 1)}x "
                     f"{'mais' if subiu else 'menos'} eficiência.")
    itens.append(f"<b>O volume {'subiu' if R3['l_sem'] >= R2['l_sem'] else 'caiu'}:</b> "
                 f"{n(R3['l_sem'], 1)} deals por semana nos últimos três meses, contra "
                 f"{n(R2['l_sem'], 1)} nos três anteriores ({delta(R2['l_sem'], R3['l_sem'])}).")
    if TOP["deals"] >= 30:
        share = 100 * TOP["deals"] / ANO["leads"]
        ruim = TOP["taxa"] < ANO["taxa"] / 2
        cauda = (f"— converteu {n(TOP['taxa'], 1)}% em reunião, contra "
                 f"{n(ANO['taxa'], 1)}% da média do ano. "
                 + ("É volume de topo de funil que engorda o número sem gerar pipeline."
                    if ruim else "Concentração alta, mas em linha com o resto da operação."))
        itens.append(f"<b>Um único criativo concentra {n(share, 0)}% dos deals do ano:</b> "
                     f"{TOP['deals']} deals e {TOP['reun']} "
                     f"{'reunião' if TOP['reun'] == 1 else 'reuniões'}, com pico em "
                     f"{TOP['mes']} {cauda}")
    if ANO_META["leads"]:
        itens.append(f"<b>Meta responde por {n(100 * ANO_META['leads'] / ANO['leads'], 0)}% dos "
                     f"deals do ano</b> ({n(ANO_META['leads'])} de {n(ANO['leads'])}) e por "
                     f"{n(100 * ANO_META['reun'] / ANO['reun'], 0) if ANO['reun'] else 0}% das "
                     f"reuniões ({n(ANO_META['reun'])} de {n(ANO['reun'])}). No 3º trimestre são "
                     f"{n(Q3['meta']['l_sem'], 1)} deals de Meta por semana, contra "
                     f"{n(Q1['meta']['l_sem'], 1)} no 1º.")
    itens.append(f"<b>Fechamentos:</b> {ANO['fech']} no ano, {SIM} {n(VALOR)} em contratos.")
    leitura = "".join(f"<li>{x}</li>" for x in itens)

    # ---- secao de paises (so LATAM) ----
    secao_paises = ""
    if reg.paises:
        TD = sum(v["d"] for v in reg.paises.values())
        TR = sum(v["r"] for v in reg.paises.values())
        media = 100 * TR / TD if TD else 0
        reais = [(k, v) for k, v in reg.paises.items() if k not in {"Não declarado", "Otro"}]
        tx = lambda v: 100 * v["r"] / v["d"] if v["d"] else 0
        # "operacao grande" = 50+ deals no ano. Taxa sobre base pequena nao sustenta decisao
        # de verba, entao o ranking principal so olha essas.
        grandes = [(k, v) for k, v in reais if v["d"] >= 50]
        melhor = max(grandes, key=lambda x: tx(x[1]))
        pior = min(grandes, key=lambda x: tx(x[1]))
        maior = max(reais, key=lambda x: x[1]["d"])
        pequenos = [(k, v) for k, v in reais if 15 <= v["d"] < 50 and tx(v) > media]
        destaque = max(pequenos, key=lambda x: tx(x[1])) if pequenos else None

        bullets = [f"<b>{esc(melhor[0])} é a melhor das operações grandes:</b> "
                   f"{n(tx(melhor[1]), 1)}% dos {melhor[1]['d']} deals viraram reunião "
                   f"({melhor[1]['r']} no total), contra {n(media, 1)}% da média LATAM."]
        if maior[0] != melhor[0]:
            bullets.append(f"<b>{esc(maior[0])} lidera em volume</b> ({maior[1]['d']} deals, "
                           f"{n(100 * maior[1]['d'] / TD, 1)}% do total) mas converte "
                           f"{n(tx(maior[1]), 1)}% — volume alto não está virando reunião na "
                           f"mesma proporção.")
        if pior[0] not in (melhor[0], maior[0]) and tx(pior[1]):
            bullets.append(f"<b>{esc(pior[0])} é o extremo oposto:</b> {n(tx(pior[1]), 1)}% de "
                           f"{pior[1]['d']} deals — {n(tx(melhor[1]) / tx(pior[1]), 1)}x abaixo "
                           f"de {esc(melhor[0])}, com volume da mesma ordem.")
        if destaque:
            bullets.append(f"<b>{esc(destaque[0])} tem a maior taxa da tabela</b> "
                           f"({n(tx(destaque[1]), 1)}%), mas sobre {destaque[1]['d']} deals no ano "
                           f"— base pequena para decidir verba; vale como sinal, não como meta.")
        bul_paises = "".join(f"<li>{x}</li>" for x in bullets)
        secao_paises = f"""
  <section class="card">
    <h2>Composição por país — onde o deal virou reunião</h2>
    <p class="capt">Ano inteiro (1º de janeiro a {rot(HOJE)}), por coorte: dos {n(TD)} deals captados,
      quais marcaram reunião. A barra escura é o volume de deals e a laranja é o de reuniões —
      cada uma tem a sua própria escala, então compare laranja com laranja, não com a escura.
      A régua à direita é a taxa de conversão do país (escala até 25%); em verde, quem está acima
      da média LATAM. Países com menos de 15 deals no ano entram agrupados — taxa sobre 3 deals é
      ruído, não taxa.</p>
    <div class="chart chart-p">{chart_paises(reg.paises)}</div>
    <ul class="read read-tight">{bul_paises}</ul>
  </section>"""

    html = f"""
  <p class="sub">1º de janeiro a {HOJE.day} de {MESES_EXT[HOJE.month - 1]} de 2026 · fonte: {reg.fonte}</p>

  <div class="kpis">
    <div class="kpi"><div class="lbl">Deals no ano</div><div class="val">{n(ANO['leads'])}</div>
      <div class="hint">{n(ANO['l_sem'], 1)} por semana em média</div></div>
    <div class="kpi"><div class="lbl">Reuniões</div><div class="val">{n(ANO['reun'])}</div>
      <div class="hint"><span class="{'up' if Q3['r_sem'] >= Q1['r_sem'] else 'down'}">{delta(Q1['r_sem'], Q3['r_sem'])}</span> por semana vs. 1º tri</div></div>
    <div class="kpi"><div class="lbl">Deals → reunião</div><div class="val">{n(R3['taxa'], 1)}%</div>
      <div class="hint">nos últimos 3 meses · era {n(Q1['taxa'], 1)}% no 1º tri</div></div>
    <div class="kpi"><div class="lbl">Fechamentos</div><div class="val">{ANO['fech']}</div>
      <div class="hint">{SIM} {n(VALOR)} em contratos</div></div>
  </div>

  <section class="card">
    <h2>Semana a semana</h2>
    <p class="capt">Deals captados (barras, eixo à esquerda) · reuniões (linha, eixo à direita) · fechamentos (losangos)</p>
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
    <p class="capt">{nota_meta}</p>
    <div class="legend">
      <span><i class="sw"></i> Deals de Meta</span>
      <span><i class="sw-line"></i> Reuniões na semana</span>
      <span><i class="sw-dash"></i> Tendência das reuniões ({MA} semanas)</span>
      <span><i class="sw sw-soft"></i> Semana parcial</span>
    </div>
    <div class="chart">{chart_meta}</div>
  </section>

  <section class="card">
    <h2>Por trimestre</h2>
    <p class="capt">Médias semanais, que seguem comparáveis mesmo com o 3º trimestre em curso (jul a {rot(HOJE)}), e a conversão dos deals captados em cada período</p>
    <div class="panels">{p1}{p2}{p3}</div>
  </section>
{secao_paises}
  <section class="card">
    <h2>Leitura</h2>
    <ul class="read">{leitura}</ul>
  </section>

  <p class="foot">
    {nota_base}
    Semanas de segunda a domingo; a primeira ({rot(weeks[0]['ini'])}–{rot(weeks[0]['fim'])}) e a última ({rot(weeks[-1]['ini'])}–{rot(weeks[-1]['fim'])}) são parciais.
    Deals e reuniões são contados pela data do evento; a taxa de conversão é por coorte — deals captados no período que marcaram reunião.
    A reunião costuma ser marcada logo após a captação (mediana de {n(reg.lag_med, 0)} dia{"s" if reg.lag_med != 1 else ""}, {reg.lag_p7}% em até 7 dias), então as coortes recentes já estão praticamente fechadas.
    Dados de {HOJE.strftime('%d/%m/%Y')}.
  </p>"""

    resumo = (f'{reg.nome:22s} deals {ANO["leads"]:5d} | reun {ANO["reun"]:4d} | fech {ANO["fech"]:3d} '
              f'({SIM} {n(VALOR)}) | Meta {ANO_META["leads"]}/{ANO_META["reun"]} | '
              f'taxa 1t {n(Q1["taxa"], 1)}% -> 3m {n(R3["taxa"], 1)}%')
    return html, resumo


# ============================== CSS ==============================
CSS = """
  /* Tema unico e deliberado: claro em qualquer viewer (relatorio impresso/anexado).
     Nao ha bloco de dark mode de proposito — todas as cores sao pintadas explicitamente. */
  :root {
    color-scheme: light;
    --ground:#F6F2F8; --surface:#FFFFFF; --ink:#1A1420; --mut:#6B6073;
    --line:#E7DFEC; --line-soft:#F0EAF3; --soft:#FBF8FC;
    --deal:#390155; --deal-soft:#D9C2E6; --reu:#C2611B; --fech:#0E9D9B; --pos:#0E7C6F;
    --neg:#A32A1E; --trend:#8C8395;
  }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--ground); color:var(--ink);
    font:16px/1.6 Lato,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    -webkit-font-smoothing:antialiased; }
  .wrap { max-width:1180px; margin:0 auto; padding:40px 24px 64px; }
  h1, h2, .kpi .val, .eyebrow, .tabbar label { font-family:"League Spartan",Lato,"Segoe UI",Helvetica,Arial,sans-serif; }
  header { margin-bottom:22px; }
  .eyebrow { font-size:12px; font-weight:700; letter-spacing:.14em; text-transform:uppercase;
    color:var(--deal); margin:0 0 10px; }
  h1 { font-size:34px; font-weight:700; line-height:1.12; letter-spacing:-.015em;
    margin:0 0 8px; text-wrap:balance; max-width:26ch; }
  .sub { color:var(--mut); font-size:14.5px; margin:0 0 18px; max-width:80ch; }
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
  .kpi .down { color:var(--neg); font-weight:700; }
  h2 { font-size:19px; font-weight:600; margin:0 0 4px; letter-spacing:-.01em; }
  .capt { font-size:13px; color:var(--mut); margin:0 0 18px; max-width:92ch; }
  .chart { overflow-x:auto; }
  .chart svg { min-width:660px; }
  .chart-p svg { min-width:900px; }
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
  /* composicao por pais */
  .ph { font-size:10.5px; font-weight:700; fill:var(--mut); letter-spacing:.06em;
    text-transform:uppercase; }
  .pn { font-size:13px; font-weight:700; fill:var(--ink); }
  .pn.agg { font-weight:400; fill:var(--mut); }
  .pbar { }
  .pb-d { fill:var(--deal); }
  .pb-r { fill:var(--reu); }
  .pv { font-size:12px; fill:var(--ink); font-variant-numeric:tabular-nums; font-weight:700; }
  .pv-r { fill:var(--reu); }
  .pp { font-weight:400; fill:var(--mut); }
  .tbar { fill:var(--line-soft); }
  .tfill { fill:var(--deal-soft); }
  .tfill.t-bom { fill:var(--fech); }
  .tval { font-size:13px; font-weight:700; fill:var(--mut); font-variant-numeric:tabular-nums; }
  .tval.t-bom { fill:var(--pos); }
  .tmed { stroke:var(--ink); stroke-width:1; stroke-dasharray:3 3; opacity:.45; }
  .tmedl { font-size:10px; fill:var(--mut); }
  ul.read { margin:10px 0 0; padding-left:0; list-style:none; display:grid; gap:15px; }
  ul.read li { position:relative; padding-left:24px; font-size:15px; max-width:92ch; }
  ul.read li::before { content:""; position:absolute; left:6px; top:10px; width:7px; height:7px;
    border-radius:99px; background:var(--deal); }
  ul.read-tight { gap:10px; margin-top:18px; }
  ul.read-tight li { font-size:14px; }
  .foot { font-size:12.5px; color:var(--mut); line-height:1.75; border-top:1px solid var(--line);
    padding-top:16px; margin:22px 0 0; max-width:104ch; }
  /* abas — CSS puro (radio + sibling), sem JS */
  .tabin { position:absolute; opacity:0; pointer-events:none; }
  .tabbar { display:flex; gap:8px; border-bottom:1px solid var(--line); margin:0 0 22px; }
  .tabbar label { font-size:14.5px; font-weight:700; color:var(--mut); cursor:pointer;
    padding:11px 18px; border:1px solid transparent; border-bottom:none;
    border-radius:10px 10px 0 0; margin-bottom:-1px; }
  .tabbar label:hover { color:var(--ink); background:var(--soft); }
  .tabin:focus-visible + .tabin + .tabbar label[for="ab-latam"],
  .tabin:focus-visible + .tabbar label[for="ab-br"] { outline:2px solid var(--deal);
    outline-offset:2px; }
  .painel { display:none; }
  #ab-latam:checked ~ .tabbar label[for="ab-latam"],
  #ab-br:checked ~ .tabbar label[for="ab-br"] { color:var(--deal); background:var(--surface);
    border-color:var(--line); }
  #ab-latam:checked ~ #p-latam, #ab-br:checked ~ #p-br { display:block; }
  @media (max-width:900px) { .kpis, .panels { grid-template-columns:1fr 1fr; } h1 { font-size:27px; } }
  @media (max-width:560px) { .kpis, .panels { grid-template-columns:1fr; } .wrap { padding:28px 16px 48px; }
    .tabbar label { padding:10px 12px; font-size:13.5px; } }
  @media print { body { background:#fff; } .card, .kpi, .panel { break-inside:avoid; }
    .painel { display:block !important; } .tabbar { display:none; } }
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=League+Spartan:wght@600;700&family=Lato:wght@400;700&display=swap">')


# ============================== pagina ==============================
def main():
    latam = carregar_latam()
    br = carregar_br()
    html_latam, res_latam = montar_regiao(latam)
    html_br, res_br = montar_regiao(br)
    hoje = max(latam.hoje, br.hoje)

    body = f"""<div class="wrap">
  <header>
    <p class="eyebrow">Content Marketing · Grupo Elife</p>
    <h1>Evolução semanal de deals, reuniões e fechamentos</h1>
  </header>

  <input class="tabin" type="radio" name="aba" id="ab-latam" checked>
  <input class="tabin" type="radio" name="aba" id="ab-br">
  <nav class="tabbar" aria-label="Escolha a operação">
    <label for="ab-latam">Buzzmonitor LATAM</label>
    <label for="ab-br">Brasil</label>
  </nav>

  <div class="painel" id="p-latam">{html_latam}
  </div>

  <div class="painel" id="p-br">{html_br}
  </div>
</div>"""

    titulo = "Content Marketing 2026"
    OUT_FILE.write_text(
        f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{titulo}</title>
{FONTS}
<style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>
""", encoding="utf-8")

    if SIBLING.exists():
        (SIBLING / "index.html").write_text(OUT_FILE.read_text(encoding="utf-8"), encoding="utf-8")

    print("OK ->", OUT_FILE.name, f"{OUT_FILE.stat().st_size / 1024:.1f} KB"
          + (" | sibling atualizada" if SIBLING.exists() else " | SIBLING NAO ENCONTRADA"))
    print(f"dados de {hoje} | media movel = {MA} semanas")
    print(res_latam)
    print(res_br)


if __name__ == "__main__":
    main()
