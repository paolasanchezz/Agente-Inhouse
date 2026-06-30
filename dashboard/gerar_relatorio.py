"""gerar_relatorio.py — popula dashboard/relatorio-semanal-buzzmonitor-brasil.html com dados reais do Supabase.

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard/gerar_relatorio.py
    uv run --python 3.12 --with "psycopg[binary]" python dashboard/gerar_relatorio.py --ate 2026-05-18

Le SUPABASE_PG_URL do dashboard/.env. Rodar a partir da raiz do projeto.

Fluxo:
  1. Calcula periodos (sab-sex, sem_ant, MtD, YtD).
  2. Smoke test: valida Fechamentos YtD 2026 = 6 deals · R$ 16.580 (§7 MAPEAMENTO).
  3. Coleta 4 conjuntos de KPIs, 6 listas, 8 rankings, 1 serie temporal, 1 proporcao.
  4. Aplica bindings no HTML via regex (data-bind, data-bind-rows, /*@bind:*/).
  5. Salva HTML com backup .bak do anterior.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import date, timedelta
from pathlib import Path

import psycopg

# imports locais
sys.path.insert(0, str(Path(__file__).parent))
from datas import calcular_periodos, fmt_data_longa, fmt_data_curta, fmt_periodo_curto
from queries import (
    q_count_leads, q_count_evento, q_count_fechamentos, q_count_perdidos,
    q_lista_leads, q_lista_evento, q_lista_propostas, q_lista_fechamentos, q_lista_perdidos,
    q_ranking, q_source_por_content,
    q_serie_temporal_12m, q_proporcao_sources_12m,
)
from render_helpers import (
    format_delta,
    fmt_int, fmt_decimal_br, fmt_pct_safe, fmt_data_br,
    row_lead, row_ra, row_rr, row_prop, row_fech, row_perda,
    render_ranking_source, render_ranking_content, render_proporcao_sources,
)


HTML_PATH = Path(__file__).parent / "relatorio-semanal-buzzmonitor-brasil.html"
BAK_PATH = HTML_PATH.with_suffix('.html.bak')

# §7 do MAPEAMENTO — gate de regressao.
# Decisao 2026-05-18: whitelist override o filtro Inbound (Victor confirmou que
# CROP e NEIVA, marcados como Outbound no CRM, sao fechamentos CM legitimos).
# Revisao 2026-05-25: +1 fechamento (Lide Comunicacao, meta/RMKT 13, R$ 2.690).
# Revisao 2026-06-22: alteracoes de filtro sem impacto no total de fechamentos.
# (a) +5 variantes em CM_UTM_SOURCES (apresentacao, webinar, newsletter, Instagram_Feed,
#     Instagram_Stories) — descobertas na auditoria da lista da colab. Nao trouxeram
#     fechamentos novos. 'redes-sociais' tambem foi adicionada mas REMOVIDA no mesmo
#     dia: era 100% deals de CS tagueados (utm_content=cs).
# (b) +catherine.nobrega@fabrikadecriacao.com.br em EMAIL_WHITELIST como GARANTIA
#     nominal (Victor confirmou CM). Hoje o deal 183535 ja passa pela regra 90d via
#     account_id casado, mas a whitelist evita perde-lo se o lead pai mudar.
# (c) +muniquebuzz@monitor.com em EMAIL_BLACKLIST (deal 189845 era "teste crm").
#     Saiu da contagem de leads/CE/RA/etc., mas nao afeta fechamentos (nao era fech).
# Total YtD 2026: 7 deals · R$ 19.270 (inalterado).
# Revisao 2026-06-30: +2 fechamentos won com cierre retroagido a 07/mai (DR. Consulta, webinar/athaide-martins, R$ 8.340; Echef Robot, Instagram_Feed, R$ 1.590). Total YtD 2026: 9 deals · R$ 29.200.
# Revisao 2026-06-30 (b): -1 fechamento — ECHEF ROBOT (deal 186199, R$ 1.590) p/ EMAIL_BLACKLIST: falso CM, lead de evento (bug de tracking Instagram_Feed/cpc). Total YtD 2026: 8 deals · R$ 27.610.
# Revisao 2026-06-30 (c): +1 fechamento — Solano Donato Carnot Damacena (deal 186979, blog/blog-monit-politico, R$ 8.500, cierre 23/jun, BD Leticia Mello). Total YtD 2026: 9 deals · R$ 36.110.
EXPECTED_FECH_YTD_2026 = 9
EXPECTED_FECH_VALOR_YTD_2026 = 36110.0

_MESES_CURTOS = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']


# ============ I/O ============

def load_url() -> str:
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        raise SystemExit(f"ERRO: {env_path} nao existe.")
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("SUPABASE_PG_URL="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("ERRO: SUPABASE_PG_URL nao encontrado em dashboard/.env")


def fetch_dict(cur, sql: str) -> list[dict]:
    cur.execute(sql)
    cols = [d.name for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def fetch_scalar(cur, sql: str):
    cur.execute(sql)
    row = cur.fetchone()
    return row[0] if row else 0


# ============ SMOKE TEST ============

def smoke_test_ytd(cur, ytd_ini: date, ytd_fim: date) -> None:
    """Valida §7 MAPEAMENTO (hard fail se YtD 2026 nao bater)."""
    print(f"[smoke test] Fechamentos YtD {ytd_ini} -> {ytd_fim}...")
    rows = fetch_dict(cur, q_lista_fechamentos(ytd_ini, ytd_fim))
    n = len(rows)
    soma = sum(float(r.get('valor') or 0) for r in rows)

    if ytd_ini.year == 2026:
        erros = []
        if n != EXPECTED_FECH_YTD_2026:
            erros.append(f"Fechamentos YtD: esperado {EXPECTED_FECH_YTD_2026}, obtido {n}")
        if abs(soma - EXPECTED_FECH_VALOR_YTD_2026) > 1.0:
            erros.append(f"Valor YtD: esperado R$ {EXPECTED_FECH_VALOR_YTD_2026:,.2f}, obtido R$ {soma:,.2f}")
        if erros:
            print("[smoke test] FALHA:")
            for e in erros:
                print(f"  - {e}")
            raise SystemExit(1)
    print(f"[smoke test] OK ({n} fechamentos · R$ {soma:,.2f})")


# ============ COLETA DE DADOS ============

def colher_kpis(cur, ini: date, fim: date) -> dict:
    return {
        'leads': fetch_scalar(cur, q_count_leads(ini, fim)),
        'ce':    fetch_scalar(cur, q_count_evento('ce', ini, fim)),
        'ra':    fetch_scalar(cur, q_count_evento('ra', ini, fim)),
        'rr':    fetch_scalar(cur, q_count_evento('rr', ini, fim)),
        'prop':  fetch_scalar(cur, q_count_evento('prop', ini, fim)),
        'fech':  fetch_scalar(cur, q_count_fechamentos(ini, fim)),
        'perd':  fetch_scalar(cur, q_count_perdidos(ini, fim)),
    }


def enriquecer_content(rows: list[dict], src_map: dict) -> list[dict]:
    for r in rows:
        r['source'] = src_map.get(r.get('dim'))
    return rows


def colher_serie_temporal(cur, hoje: date) -> dict:
    """Roda serie 12m e pivoteia por metrica em 52 buckets semanais (segunda-feira inicio)."""
    raw = fetch_dict(cur, q_serie_temporal_12m(hoje))

    # 52 segundas-feiras (date_trunc('week') retorna segunda)
    segunda_atual = hoje - timedelta(days=hoje.weekday())
    inicio = segunda_atual - timedelta(weeks=51)
    semanas = [inicio + timedelta(weeks=i) for i in range(52)]

    counts = {}
    for r in raw:
        s = r['semana']
        m = r['metrica']
        counts[(s, m)] = int(r['n'])

    labels = [f'{s.day:02d}/{s.month:02d}' for s in semanas]
    metricas = ['leads', 'ce', 'agendadas', 'propostas', 'fechamentos']
    return {
        'labels': labels,
        **{m: [counts.get((s, m), 0) for s in semanas] for m in metricas},
    }


def colher_dados(cur, periodos: dict) -> dict:
    ini_a, fim_a = periodos['ini_atual'], periodos['fim_atual']
    ini_p, fim_p = periodos['ini_ant'], periodos['fim_ant']
    mtd_i, mtd_f = periodos['mtd_ini'], periodos['mtd_fim']
    ytd_i, ytd_f = periodos['ytd_ini'], periodos['ytd_fim']
    hoje = periodos['hoje']

    dados = {'periodos': periodos}

    print("[colher] KPIs Semana atual...")
    dados['kpis_semana'] = colher_kpis(cur, ini_a, fim_a)
    print("[colher] KPIs Semana anterior...")
    dados['kpis_sem_ant'] = colher_kpis(cur, ini_p, fim_p)
    print("[colher] KPIs MtD...")
    dados['kpis_mtd'] = colher_kpis(cur, mtd_i, mtd_f)
    print("[colher] KPIs YtD...")
    dados['kpis_ytd'] = colher_kpis(cur, ytd_i, ytd_f)

    print("[colher] Listas semana...")
    dados['leads_semana']  = fetch_dict(cur, q_lista_leads(ini_a, fim_a))
    dados['ra_semana']     = fetch_dict(cur, q_lista_evento('ra', ini_a, fim_a))
    dados['rr_semana']     = fetch_dict(cur, q_lista_evento('rr', ini_a, fim_a))
    dados['prop_semana']   = fetch_dict(cur, q_lista_propostas(ini_a, fim_a))
    dados['fech_semana']   = fetch_dict(cur, q_lista_fechamentos(ini_a, fim_a))
    dados['perdidos_mtd']  = fetch_dict(cur, q_lista_perdidos(mtd_i, mtd_f))

    print("[colher] Rankings sources (4 periodos)...")
    dados['ranking_source_semana']  = fetch_dict(cur, q_ranking('utm_source', ini_a, fim_a))
    dados['ranking_source_sem_ant'] = fetch_dict(cur, q_ranking('utm_source', ini_p, fim_p))
    dados['ranking_source_mtd']     = fetch_dict(cur, q_ranking('utm_source', mtd_i, mtd_f))
    dados['ranking_source_ytd']     = fetch_dict(cur, q_ranking('utm_source', ytd_i, ytd_f))

    print("[colher] Rankings content (4 periodos)...")
    src_map = {r['utm_content']: r['utm_source'] for r in fetch_dict(cur, q_source_por_content(ytd_i, ytd_f))}
    dados['ranking_content_semana']  = enriquecer_content(fetch_dict(cur, q_ranking('utm_content', ini_a, fim_a)), src_map)
    dados['ranking_content_sem_ant'] = enriquecer_content(fetch_dict(cur, q_ranking('utm_content', ini_p, fim_p)), src_map)
    dados['ranking_content_mtd']     = enriquecer_content(fetch_dict(cur, q_ranking('utm_content', mtd_i, mtd_f)), src_map)
    dados['ranking_content_ytd']     = enriquecer_content(fetch_dict(cur, q_ranking('utm_content', ytd_i, ytd_f)), src_map)

    print("[colher] Serie temporal 12m...")
    dados['serie_12m'] = colher_serie_temporal(cur, hoje)

    print("[colher] Proporcao sources 12m...")
    dados['proporcao_sources'] = render_proporcao_sources(
        fetch_dict(cur, q_proporcao_sources_12m(hoje))
    )

    return dados


# ============ BINDING HELPERS ============

def _bind(html: str, key: str, value: str) -> str:
    """Substitui texto entre <... data-bind="key">OLD<..."""
    pattern = rf'(data-bind="{re.escape(key)}"[^>]*>)([^<]*)(<)'
    return re.sub(pattern, lambda m: f'{m.group(1)}{value}{m.group(3)}', html)


def _bind_delta(html: str, key: str, texto: str, classe: str) -> str:
    """Substitui texto E classe do delta. Match: <div class="delta XXX" data-bind="kpi...delta">TEXT</div>."""
    pattern = rf'<div class="delta [^"]*" data-bind="{re.escape(key)}">[^<]*</div>'
    new = f'<div class="delta {classe}" data-bind="{key}">{texto}</div>'
    return re.sub(pattern, new, html)


def _bind_width(html: str, key: str, pct: int) -> str:
    """Substitui style="width:XX%" em <span data-bind-width="key" style="...">."""
    pattern = rf'data-bind-width="{re.escape(key)}" style="[^"]*"'
    new = f'data-bind-width="{key}" style="width:{pct}%"'
    return re.sub(pattern, new, html)


def _bind_rows(html: str, key: str, rows_html: str) -> str:
    """Substitui conteudo entre <tbody data-bind-rows="key">...</tbody>."""
    pattern = rf'(<tbody[^>]*data-bind-rows="{re.escape(key)}"[^>]*>).*?(</tbody>)'
    inner = '\n              ' + rows_html + '\n            '
    return re.sub(pattern, lambda m: m.group(1) + inner + m.group(2), html, flags=re.DOTALL)


def _bind_js(html: str, key: str, value_js: str) -> str:
    """Substitui /*@bind:key*/.../*@end*/ por valor JS."""
    pattern = rf'/\*\s*@bind:{re.escape(key)}\s*\*/.*?/\*\s*@end\s*\*/'
    new = f'/*@bind:{key}*/{value_js}/*@end*/'
    return re.sub(pattern, new, html, flags=re.DOTALL)


# ============ RENDER (aplica bindings no HTML) ============

KPIS_FUNIL = [
    ('leads', None),     # nao tem denominador
    ('ce',    'leads'),
    ('ra',    'ce'),
    ('rr',    'ra'),
    ('prop',  'rr'),
    ('fech',  'prop'),
    ('perd',  'leads'),
]
INVERT_DELTA = {'perd'}  # queda em Perdidos = positivo


def aplicar_bindings(html: str, dados: dict) -> str:
    p = dados['periodos']
    ks = dados['kpis_semana']
    ksa = dados['kpis_sem_ant']
    km = dados['kpis_mtd']
    ky = dados['kpis_ytd']
    sem_div = max(1, p['semanas_decorridas_ytd'])

    # ====== HEADER ======
    html = _bind(html, 'header.periodo',
        f"{fmt_data_longa(p['ini_atual'])} → {fmt_data_longa(p['fim_atual'])} · {p['fim_atual'].year}")
    html = _bind(html, 'header.sem_anterior',
        f"{fmt_data_curta(p['ini_ant'])} → {fmt_data_curta(p['fim_ant'])}")
    html = _bind(html, 'header.mtd_periodo',
        f"{p['mtd_ini'].day:02d} → {p['mtd_fim'].day:02d} {_MESES_CURTOS[p['mtd_fim'].month-1]} {p['mtd_fim'].year}")
    html = _bind(html, 'header.ytd_periodo',
        f"Jan → {_MESES_CURTOS[p['fim_atual'].month-1]} {p['fim_atual'].year} ({sem_div} semanas)")
    html = _bind(html, 'header.gerado_em',
        f"{p['hoje'].day:02d} {_MESES_CURTOS[p['hoje'].month-1]} {p['hoje'].year}")
    html = _bind(html, 'tag.semana',
        f"{p['ini_atual'].day:02d}–{p['fim_atual'].day:02d} {_MESES_CURTOS[p['fim_atual'].month-1]} {p['fim_atual'].year}")

    # ====== BLOCO 1.a SEMANA ======
    for kpi, denom in KPIS_FUNIL:
        html = _bind(html, f'kpi.semana.{kpi}.val', fmt_int(ks[kpi]))
        if denom is not None:
            html = _bind(html, f'kpi.semana.{kpi}.pct', fmt_pct_safe(ks[kpi], ks[denom]))
        # delta vs semana anterior
        invert = kpi in INVERT_DELTA
        txt, cls = format_delta(ks[kpi], ksa[kpi], invert=invert)
        html = _bind_delta(html, f'kpi.semana.{kpi}.delta', txt, cls)
        # media semanal YtD
        med = ky[kpi] / sem_div
        html = _bind(html, f'kpi.semana.{kpi}.med', f'méd. {fmt_decimal_br(med, 1)}')

    # ====== BLOCO 1.b MtD ======
    for kpi, denom in KPIS_FUNIL:
        html = _bind(html, f'kpi.mtd.{kpi}.val', fmt_int(km[kpi]))
        if denom is not None:
            html = _bind(html, f'kpi.mtd.{kpi}.pct', fmt_pct_safe(km[kpi], km[denom]))

    # ====== BLOCO 1.c YtD ======
    for kpi, denom in KPIS_FUNIL:
        html = _bind(html, f'kpi.ytd.{kpi}.val', fmt_int(ky[kpi]))
        if denom is not None:
            html = _bind(html, f'kpi.ytd.{kpi}.pct', fmt_pct_safe(ky[kpi], ky[denom]))

    # ====== BLOCO 2 PERDAS (3 cards + tabela) ======
    for label, ksrc, periodo_label in (
        ('semana', ks, f"{p['ini_atual'].day:02d}–{p['fim_atual'].day:02d} {_MESES_CURTOS[p['fim_atual'].month-1]}"),
        ('mtd',    km, f"{p['mtd_ini'].day:02d}–{p['mtd_fim'].day:02d} {_MESES_CURTOS[p['mtd_fim'].month-1]}"),
        ('ytd',    ky, f"Jan–{_MESES_CURTOS[p['fim_atual'].month-1]}"),
    ):
        perd = ksrc['perd']
        leads = ksrc['leads']
        pct = round(100 * perd / leads) if leads else 0
        html = _bind(html, f'perd.{label}.pct', f'{pct}%')
        html = _bind(html, f'perd.{label}.abs', f"{perd} perdidos · {leads} leads · {periodo_label}")
        html = _bind_width(html, f'perd.{label}.bar', min(pct, 100))

    # ====== TOGGLES + TABELAS ======
    listas = [
        ('perdidos_mtd', row_perda, dados['perdidos_mtd']),
        ('leads_semana', row_lead,  dados['leads_semana']),
        ('ra_semana',    row_ra,    dados['ra_semana']),
        ('rr_semana',    row_rr,    dados['rr_semana']),
        ('prop_semana',  row_prop,  dados['prop_semana']),
        ('fech_semana',  row_fech,  dados['fech_semana']),
    ]
    for key, render_fn, items in listas:
        if items:
            rows_html = '\n              '.join(render_fn(d) for d in items)
        else:
            rows_html = '<tr><td colspan="10" class="dim center">(sem dados no período)</td></tr>'
        html = _bind_rows(html, key, rows_html)
        unit = 'deal' if len(items) == 1 else 'deals'
        html = _bind(html, f'count.{key}', f"{len(items)} {unit}")

    # ====== RANKINGS ======
    for key in ('semana', 'sem_ant', 'mtd', 'ytd'):
        html = _bind_rows(html, f'ranking_source_{key}',
                          render_ranking_source(dados[f'ranking_source_{key}'], top_n=8))
        html = _bind_rows(html, f'ranking_content_{key}',
                          render_ranking_content(dados[f'ranking_content_{key}'], top_n=12))

    # ====== CHART 5.1 ======
    s = dados['serie_12m']
    html = _bind_js(html, 'serie_12m.labels',      json.dumps(s['labels'], ensure_ascii=False))
    html = _bind_js(html, 'serie_12m.leads',       json.dumps(s['leads']))
    html = _bind_js(html, 'serie_12m.ce',          json.dumps(s['ce']))
    html = _bind_js(html, 'serie_12m.agendadas',   json.dumps(s['agendadas']))
    html = _bind_js(html, 'serie_12m.propostas',   json.dumps(s['propostas']))
    html = _bind_js(html, 'serie_12m.fechamentos', json.dumps(s['fechamentos']))

    # ====== CHART 5.2 ======
    html = _bind_js(html, 'proporcao_sources_12m', json.dumps(dados['proporcao_sources'], ensure_ascii=False))

    # ====== FOOTER ======
    html = _bind(
        html, 'footer.periodos',
        f"Semana {fmt_data_curta(p['ini_atual'])}-{fmt_data_curta(p['fim_atual'])} {p['fim_atual'].year} · "
        f"MtD {fmt_data_curta(p['mtd_ini'])}-{fmt_data_curta(p['mtd_fim'])} · "
        f"YtD Jan-{_MESES_CURTOS[p['fim_atual'].month-1]} {p['fim_atual'].year}"
    )

    return html


# ============ MAIN ============

def main():
    parser = argparse.ArgumentParser(description='Popula a dashboard CM Buzzmonitor com dados reais.')
    parser.add_argument('--ate', type=str, default=None, help='YYYY-MM-DD (default = hoje)')
    parser.add_argument('--no-smoke', action='store_true', help='Pula smoke test YtD')
    parser.add_argument('--output', type=str, default=None, help='Path do HTML de saida (default = sobrescreve)')
    args = parser.parse_args()

    ate = date.fromisoformat(args.ate) if args.ate else None
    periodos = calcular_periodos(ate)

    print("=" * 70)
    print("Dashboard Content Marketing — Buzzmonitor Brasil")
    print("=" * 70)
    print(f"Hoje:          {periodos['hoje']}")
    print(f"Semana atual:  {periodos['ini_atual']} -> {periodos['fim_atual']}")
    print(f"Semana ant.:   {periodos['ini_ant']} -> {periodos['fim_ant']}")
    print(f"MtD:           {periodos['mtd_ini']} -> {periodos['mtd_fim']}")
    print(f"YtD:           {periodos['ytd_ini']} -> {periodos['ytd_fim']}")
    print(f"Semanas YtD:   {periodos['semanas_decorridas_ytd']}")
    print()

    url = load_url()
    with psycopg.connect(url, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("SET statement_timeout = '300s'")

            if not args.no_smoke:
                smoke_test_ytd(cur, periodos['ytd_ini'], periodos['ytd_fim'])
                print()

            dados = colher_dados(cur, periodos)

    print()
    print("[render] Aplicando bindings no HTML...")
    html = HTML_PATH.read_text(encoding='utf-8')
    html_out = aplicar_bindings(html, dados)

    # backup
    if HTML_PATH.exists():
        shutil.copy2(HTML_PATH, BAK_PATH)
        print(f"[render] Backup salvo em {BAK_PATH.name}")

    output = Path(args.output) if args.output else HTML_PATH
    output.write_text(html_out, encoding='utf-8')
    print(f"[render] HTML salvo em {output.name}")
    print()
    print("Pronto. Abra no browser pra ver o resultado.")


if __name__ == '__main__':
    main()
