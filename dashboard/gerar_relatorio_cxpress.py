"""gerar_relatorio_cxpress.py — gera o dashboard de Funil Inbound **Cxpress Brasil**.

Clone fiel do dashboard do Brasil (mesmo CSS/toggles/rankings/charts/sortable), adaptado para:
- funil de 6 fases + Perdido: Lead -> Triagem -> Agendamento -> Demo realizada -> Proposta
  -> Fechamento (+ Perdido). Mesma contagem de KPIs do Brasil (7), entao a grade fica repeat(7,1fr).
- fonte: tabela unica cxpress_deals_funil_principal_prod (sem regra de 90d, sem contratos separados).
- idioma PT-BR, moeda BRL.

O CSS e EXTRAIDO em runtime do template do Brasil (relatorio-semanal-buzzmonitor-brasil.html)
para garantir paridade visual sem duplicar ~530 linhas.

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard/gerar_relatorio_cxpress.py
    uv run --python 3.12 --with "psycopg[binary]" python dashboard/gerar_relatorio_cxpress.py --ate 2026-06-01
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

sys.path.insert(0, str(Path(__file__).parent))
from datas import calcular_periodos, fmt_data_longa, fmt_data_curta
from queries_cxpress import (
    q_count_kpis,
    q_lista_leads, q_lista_agendamento, q_lista_demo, q_lista_propostas,
    q_lista_fechamentos, q_lista_perdidos,
    q_ranking, q_source_por_content, q_serie_12m, q_proporcao_12m,
)
import render_helpers_cxpress as R

HTML_PATH = Path(__file__).parent / "relatorio-semanal-cxpress-brasil.html"
BAK_PATH = HTML_PATH.with_suffix('.html.bak')
BRASIL_HTML = Path(__file__).parent / "relatorio-semanal-buzzmonitor-brasil.html"

_MES_C = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']


# ============ I/O ============

def load_url() -> str:
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        raise SystemExit(f"ERRO: {env_path} nao existe.")
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        if raw.strip().startswith("SUPABASE_PG_URL="):
            return raw.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("ERRO: SUPABASE_PG_URL nao encontrado em dashboard/.env")


def fetch_one(cur, sql):
    cur.execute(sql)
    cols = [d.name for d in cur.description]
    row = cur.fetchone()
    return dict(zip(cols, row)) if row else {}


def fetch_all(cur, sql):
    cur.execute(sql)
    cols = [d.name for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def extrair_css() -> str:
    """Extrai o <style> do template do Brasil. Cxpress tem 7 KPIs igual ao Brasil => sem ajuste de grade."""
    if not BRASIL_HTML.exists():
        raise SystemExit(f"ERRO: {BRASIL_HTML.name} nao encontrado (preciso dele para o CSS).")
    html = BRASIL_HTML.read_text(encoding='utf-8')
    m = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
    if not m:
        raise SystemExit("ERRO: bloco <style> nao encontrado no template do Brasil.")
    return m.group(1)


def f_dec(n) -> str:
    return f"{n:.1f}".replace('.', ',')


# ============ COLETA ============

def colher_periodo(cur, ini, fim) -> dict:
    k = fetch_one(cur, q_count_kpis(ini, fim))
    return {m: (k.get(m, 0) or 0) for m in
            ('leads', 'triagem', 'agendamento', 'demo', 'proposta', 'fechamento', 'perd')}


def colher_serie(cur, hoje) -> dict:
    raw = fetch_all(cur, q_serie_12m(hoje))
    segunda = hoje - timedelta(days=hoje.weekday())
    semanas = [segunda - timedelta(weeks=51 - i) for i in range(52)]
    counts = {(r['semana'], r['metrica']): int(r['n']) for r in raw}
    labels = [f'{s.day:02d}/{s.month:02d}' for s in semanas]
    return {
        'labels': labels,
        **{m: [counts.get((s, m), 0) for s in semanas]
           for m in ('leads', 'triagem', 'agendamento', 'proposta', 'fechamento')},
    }


def colher(cur, per) -> dict:
    a, fa = per['ini_atual'], per['fim_atual']
    pa, fpa = per['ini_ant'], per['fim_ant']
    mi, mf = per['mtd_ini'], per['mtd_fim']
    yi, yf = per['ytd_ini'], per['ytd_fim']
    d = {'periodos': per}
    print("[colher] KPIs (4 periodos)...")
    d['semana'] = colher_periodo(cur, a, fa)
    d['sem_ant'] = colher_periodo(cur, pa, fpa)
    d['mtd'] = colher_periodo(cur, mi, mf)
    d['ytd'] = colher_periodo(cur, yi, yf)
    print("[colher] Listas...")
    d['leads_semana'] = fetch_all(cur, q_lista_leads(a, fa))
    d['agend_semana'] = fetch_all(cur, q_lista_agendamento(a, fa))
    d['demo_semana'] = fetch_all(cur, q_lista_demo(a, fa))
    d['prop_semana'] = fetch_all(cur, q_lista_propostas(a, fa))
    d['fech_semana'] = fetch_all(cur, q_lista_fechamentos(a, fa))
    d['perdidos_mtd'] = fetch_all(cur, q_lista_perdidos(mi, mf))
    print("[colher] Rankings source/content (4 periodos)...")
    for key, (i, fm) in {'semana': (a, fa), 'sem_ant': (pa, fpa), 'mtd': (mi, mf), 'ytd': (yi, yf)}.items():
        d[f'rk_src_{key}'] = fetch_all(cur, q_ranking('utm_source', i, fm))
        d[f'rk_ct_{key}'] = fetch_all(cur, q_ranking('utm_content', i, fm))
    d['src_map'] = {r['utm_content']: r['utm_source'] for r in fetch_all(cur, q_source_por_content(yi, yf))}
    print("[colher] Serie 12m + proporcao...")
    d['serie'] = colher_serie(cur, per['hoje'])
    d['proporcao'] = R.render_proporcao_sources(fetch_all(cur, q_proporcao_12m(per['hoje'])))
    return d


# ============ RENDER HTML ============

KPIS = [
    ('leads', None, 'Leads'),
    ('triagem', 'leads', 'Triagem'),
    ('agendamento', 'triagem', 'Agendamento'),
    ('demo', 'agendamento', 'Demo realizada'),
    ('proposta', 'demo', 'Proposta'),
    ('fechamento', 'proposta', 'Fechamento'),
    ('perd', 'leads', 'Perdidos'),
]
INVERT = {'perd'}


def _kpi_item(label, val, pct=None, delta=None, med=None):
    pct_h = f'<div class="pct">{pct}</div>' if pct is not None else ''
    delta_h = f'<div class="delta {delta[1]}">{delta[0]}</div>' if delta else ''
    med_h = f'<div class="foot">{med}</div>' if med else ''
    return (f'<div class="kpi-item"><div class="label">{label}</div>'
            f'<div class="main"><div class="val">{R.fmt_int(val)}</div>{pct_h}</div>'
            f'{delta_h}{med_h}</div>')


def _kpi_row(k, comp=None, ky=None, sem_div=None):
    items = []
    for key, denom, label in KPIS:
        val = k[key]
        pct = R.fmt_pct_safe(val, k[denom]) if denom else None
        delta = med = None
        if comp is not None:
            delta = R.format_delta(val, comp[key], invert=(key in INVERT))
        if ky is not None and sem_div:
            med = f'méd. {f_dec(ky[key] / sem_div)}'
        items.append(_kpi_item(label, val, pct, delta, med))
    return f'<div class="kpi-row">{"".join(items)}</div>'


def _toggle(titulo, count_label, thead, rows_html):
    return (
        '<details class="toggle"><summary><span class="toggle-title">'
        f'<span>{titulo}</span><span class="toggle-count">{count_label}</span>'
        '</span><span class="caret">▼</span></summary>'
        f'<div class="table-wrap"><table><thead>{thead}</thead>'
        f'<tbody>{rows_html}</tbody></table></div></details>'
    )


def _rk_table(title, period, thead, rows_html):
    return (
        f'<div><div class="col-head"><span class="title">{title}</span>'
        f'<span class="period">{period}</span></div>'
        f'<div class="table-wrap"><table><thead>{thead}</thead>'
        f'<tbody>{rows_html}</tbody></table></div></div>'
    )


_TH_SRC = ('<tr><th>#</th><th>Fonte</th><th class="num">Leads</th><th class="num">Triagem</th>'
           '<th class="num">% Tri</th><th class="num">Agend.</th><th class="num">% Agd</th>'
           '<th class="num">Demo</th><th class="num">Prop.</th><th class="num">Fech.</th></tr>')
_TH_CT = ('<tr><th>#</th><th>Conteúdo</th><th>Fonte</th><th class="num">Leads</th>'
          '<th class="num">Agend.</th><th class="num">Demo</th><th class="num">Prop.</th>'
          '<th class="num">Fech.</th></tr>')


def render_html(d):
    p = d['periodos']
    fa, hoje = p['fim_atual'], p['hoje']
    sem_div = max(1, p['semanas_decorridas_ytd'])
    pn = p.get('periodo_nome', 'Semana')
    css = extrair_css()

    # ---- header ----
    header = (
        '<div class="top"><div class="chip">Funil Inbound · Cxpress Brasil</div>'
        '<h1>Resultados — Funil Inbound</h1><div class="sub">Relatório Semanal · Cxpress Brasil</div>'
        '<div class="meta">'
        f'<div class="item"><span class="lbl">Período</span><span class="val">{fmt_data_longa(p["ini_atual"])} → {fmt_data_longa(fa)} · {fa.year}</span></div>'
        f'<div class="item"><span class="lbl">vs. Semana anterior</span><span class="val">{fmt_data_curta(p["ini_ant"])} → {fmt_data_curta(p["fim_ant"])}</span></div>'
        f'<div class="item"><span class="lbl"><span class="no-upper">MtD</span> · Mês atual</span><span class="val">{p["mtd_ini"].day:02d} → {p["mtd_fim"].day:02d} {_MES_C[p["mtd_fim"].month-1]} {fa.year}</span></div>'
        f'<div class="item"><span class="lbl"><span class="no-upper">YtD</span> · Acumulado do ano</span><span class="val">Jan → {_MES_C[fa.month-1]} {fa.year} ({sem_div} semanas)</span></div>'
        f'<div class="item"><span class="lbl">Gerado em</span><span class="val">{hoje.day:02d} {_MES_C[hoje.month-1]} {hoje.year}</span></div>'
        '</div>'
        '<div class="sources"><b>Fonte:</b> Supabase (cxpress_deals_funil_principal_prod) · funil inbound Cxpress · '
        'escopo/filtro de canal em MAPEAMENTO-CAMPOS-cxpress.md. Moeda: BRL.</div></div>'
    )

    # ---- bloco 1 ----
    tag_sem = f'{p["ini_atual"].day:02d}–{fa.day:02d} {_MES_C[fa.month-1]} {fa.year}'
    bloco1 = (
        '<section><div class="section-head"><div class="icon">1</div>'
        f'<h2>Visão Geral · {pn}</h2>'
        f'<span class="tag">{tag_sem}</span></div>'
        + _kpi_row(d['semana'], comp=d['sem_ant'], ky=d['ytd'], sem_div=sem_div)
        + '<div class="sub-head">Acumulado <span class="no-upper">MtD</span></div>'
        + _kpi_row(d['mtd'])
        + '<div class="sub-head">Acumulado <span class="no-upper">YtD</span></div>'
        + _kpi_row(d['ytd'])
        + '</section>'
    )

    # ---- bloco 2 (perdas) ----
    def loss_item(lbl, k, periodo):
        perd, leads = k['perd'], k['leads']
        pct = round(100 * perd / leads) if leads else 0
        return (f'<div class="loss-item"><div class="label">% Perdidos · {lbl}</div>'
                f'<div class="pct">{pct}%</div>'
                f'<div class="abs">{perd} perdidos · {leads} leads · {periodo}</div>'
                f'<div class="bar"><span style="width:{min(pct,100)}%"></span></div></div>')
    perd_rows = ''.join(R.row_perda(x) for x in d['perdidos_mtd']) or R.empty_row(6)
    bloco2 = (
        '<section><div class="section-head"><div class="icon">2</div>'
        '<h2>Perdas · Semana / MtD / YtD</h2><span class="tag">data do lost</span></div>'
        '<div class="loss-panel">'
        + loss_item(pn, d['semana'], f'{p["ini_atual"].day:02d}–{fa.day:02d} {_MES_C[fa.month-1]}')
        + loss_item('<span class="no-upper">MtD</span>', d['mtd'], f'{p["mtd_ini"].day:02d}–{p["mtd_fim"].day:02d} {_MES_C[p["mtd_fim"].month-1]}')
        + loss_item('<span class="no-upper">YtD</span>', d['ytd'], f'Jan–{_MES_C[fa.month-1]}')
        + '</div>'
        + _toggle('Leads perdidos no MtD · detalhe', f'{len(d["perdidos_mtd"])} deals',
                  '<tr><th>Deal</th><th>Fonte</th><th>Conteúdo</th><th>Etapa do lost</th><th>Data</th><th>Motivo</th></tr>', perd_rows)
        + '</section>'
    )

    # ---- bloco 3 (listas) ----
    def lst(rows, fn, cols):
        return ''.join(fn(x) for x in rows) or R.empty_row(cols)
    bloco3 = (
        '<section><div class="section-head"><div class="icon">3</div>'
        '<h2>Listas de Acesso Rápido · Semana</h2><span class="tag">drill-down do funil</span></div>'
        + _toggle('3.1 · Leads da semana', f'{len(d["leads_semana"])} deals',
                  '<tr><th>Deal</th><th>Fonte</th><th>Conteúdo</th><th>Data</th><th>Responsável</th></tr>',
                  lst(d['leads_semana'], R.row_lead, 5))
        + _toggle('3.2 · Agendamentos da semana', f'{len(d["agend_semana"])} deals',
                  '<tr><th>Deal</th><th>Responsável</th><th>Fonte</th><th>Conteúdo</th><th>Data</th><th>Demo?</th></tr>',
                  lst(d['agend_semana'], R.row_agendamento, 6))
        + _toggle('3.3 · Demos realizadas na semana', f'{len(d["demo_semana"])} deals',
                  '<tr><th>Deal</th><th>Responsável</th><th>Fonte</th><th>Conteúdo</th><th>Data</th><th>Proposta?</th></tr>',
                  lst(d['demo_semana'], R.row_demo, 6))
        + _toggle('3.4 · Propostas da semana', f'{len(d["prop_semana"])} deals',
                  '<tr><th>Deal</th><th>Responsável</th><th>Fonte</th><th>Conteúdo</th><th>Data</th><th class="num">Valor</th></tr>',
                  lst(d['prop_semana'], R.row_prop, 6))
        + _toggle('3.5 · Fechamentos da semana', f'{len(d["fech_semana"])} deals',
                  '<tr><th>Deal</th><th>Responsável</th><th>Fonte</th><th>Conteúdo</th><th>Data</th><th class="num">Valor</th></tr>',
                  lst(d['fech_semana'], R.row_fech, 6))
        + '</section>'
    )

    # ---- bloco 4 (rankings) ----
    per_lbls = {
        'semana': f'{fmt_data_curta(p["ini_atual"])}–{fmt_data_curta(fa)} {fa.year}',
        'sem_ant': f'{fmt_data_curta(p["ini_ant"])}–{fmt_data_curta(p["fim_ant"])} {fa.year}',
        'mtd': f'{fmt_data_curta(p["mtd_ini"])}–{fmt_data_curta(p["mtd_fim"])} {fa.year}',
        'ytd': f'Jan–{_MES_C[fa.month-1]} {fa.year}',
    }
    titles = {'semana': 'Semana', 'sem_ant': 'Semana Anterior', 'mtd': 'MtD', 'ytd': 'YtD'}

    def src_tbl(key):
        return _rk_table(titles[key], per_lbls[key], _TH_SRC, R.render_ranking_source(d[f'rk_src_{key}']))

    def ct_tbl(key):
        return _rk_table(titles[key], per_lbls[key], _TH_CT, R.render_ranking_content(d[f'rk_ct_{key}'], d['src_map']))

    bloco4 = (
        '<section><div class="section-head"><div class="icon">4</div>'
        '<h2>Detalhe · Semana / Semana Anterior / MtD / YtD</h2>'
        '<span class="tag">% Tri = Triagem/Leads · % Agd = Agend./Triagem</span></div>'
        '<div class="sub-head">4.a · Ranking de Fontes</div>'
        f'<div class="two-col">{src_tbl("semana")}{src_tbl("sem_ant")}</div>'
        f'<div class="two-col">{src_tbl("mtd")}{src_tbl("ytd")}</div>'
        '<div class="sub-head">4.b · Ranking de Conteúdo (UTM Content)</div>'
        f'<div class="two-col">{ct_tbl("semana")}{ct_tbl("sem_ant")}</div>'
        f'<div class="two-col">{ct_tbl("mtd")}{ct_tbl("ytd")}</div>'
        '</section>'
    )

    # ---- bloco 5 (charts) ----
    bloco5 = (
        '<section><div class="section-head"><div class="icon">5</div>'
        '<h2>Tendências · Últimos 12 meses</h2><span class="tag">52 semanas</span></div>'
        '<div class="chart-wrap"><div class="chart-head">'
        '<h3>Série temporal semanal · Funil + Tx Triagem</h3>'
        '<span class="ctx">52 semanas · clique na legenda para ocultar séries</span></div>'
        '<div class="chart-canvas"><canvas id="chartTimeseries"></canvas></div></div>'
        '<div class="chart-wrap"><div class="chart-head">'
        '<h3>Agendamentos e Demos por fonte · 12 meses</h3>'
        '<span class="ctx">Agend. = Agendamentos · Demo = Demos realizadas</span></div>'
        '<div class="chart-canvas chart-canvas-tall"><canvas id="chartSourceShare"></canvas></div></div>'
        '</section>'
    )

    nota = ('<div class="sources" style="margin-top:18px">⚠️ <b>Dashboard sobre dados reais da tabela '
            'cxpress_deals_funil_principal_prod.</b> Escopo atual: todo o funil da tabela (filtros de inbound '
            'e Content Marketing estão como no-op até calibração com dados — ver MAPEAMENTO-CAMPOS-cxpress.md §Escopo). '
            'As datas de etapa vêm do ActiveCampaign como texto e são lidas como ISO (YYYY-MM-DD); confirmar o formato '
            'na 1ª carga. Sem dedup por pessoa (a tabela não tem e-mail).</div>')

    footer = (
        '<footer><b>Dashboard de Funil Inbound · dados reais do Supabase</b><br>'
        f'{pn} {fmt_data_curta(p["ini_atual"])}-{fmt_data_curta(fa)} {fa.year} · '
        f'MtD {fmt_data_curta(p["mtd_ini"])}-{fmt_data_curta(p["mtd_fim"])} · YtD Jan-{_MES_C[fa.month-1]} {fa.year}<br>'
        'Cada etapa contabilizada pela data do evento · Cxpress Brasil · uso interno</footer>'
    )

    js = _build_js(d)
    return (
        '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        f'<title>Resultados — Funil Inbound · Cxpress Brasil · {tag_sem}</title>'
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
        f'<style>{css}</style></head><body><div class="container">'
        + header + bloco1 + bloco2 + bloco3 + bloco4 + bloco5 + nota + footer
        + '</div>' + js + '</body></html>'
    )


_JS = """
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script>
  const weekLabels = __LABELS__;
  const leads = __LEADS__, triagem = __TRIAGEM__, agendamento = __AGENDAMENTO__,
        proposta = __PROPOSTA__, fechamento = __FECHAMENTO__;
  const txTriagem = leads.map((l,i)=> l ? Math.round((triagem[i]/l)*100) : 0);
  const F = { family:'Inter', size:13 };
  new Chart(document.getElementById('chartTimeseries').getContext('2d'), {
    type:'line',
    data:{ labels:weekLabels, datasets:[
      { label:'Leads', data:leads, borderColor:'#1F2937', borderWidth:2.6, tension:.35, pointRadius:0, pointHoverRadius:5, yAxisID:'y' },
      { label:'Triagem', data:triagem, borderColor:'#0B63FF', borderWidth:2.2, tension:.35, pointRadius:0, pointHoverRadius:5, yAxisID:'y' },
      { label:'Tx Triagem (%)', data:txTriagem, borderColor:'#6EA7FF', borderWidth:2, borderDash:[6,3], tension:.35, pointRadius:0, yAxisID:'yPct' },
      { label:'Agendamentos', data:agendamento, borderColor:'#6B7280', borderWidth:1.8, borderDash:[3,3], tension:.35, pointRadius:0, yAxisID:'y' },
      { label:'Propostas', data:proposta, borderColor:'#F59E0B', borderWidth:1.8, tension:.35, pointRadius:0, yAxisID:'y' },
      { label:'Fechamentos', data:fechamento, borderColor:'#16A34A', backgroundColor:'rgba(22,163,74,0.1)', borderWidth:2.5, tension:.2, pointRadius:3, pointHoverRadius:5, yAxisID:'y' }
    ]},
    options:{ responsive:true, maintainAspectRatio:false, interaction:{mode:'index',intersect:false},
      plugins:{ legend:{ position:'top', align:'end', labels:{ font:F, color:'#374151', usePointStyle:true, pointStyle:'rectRounded', padding:16 } },
        tooltip:{ backgroundColor:'#1F2937', padding:12, cornerRadius:8,
          callbacks:{ label:(c)=> c.dataset.yAxisID==='yPct' ? `${c.dataset.label}: ${c.parsed.y}%` : `${c.dataset.label}: ${c.parsed.y}` } } },
      scales:{ x:{ ticks:{ font:{family:'Inter',size:11}, color:'#6B7280', maxRotation:0, autoSkip:true, maxTicksLimit:13 }, grid:{display:false} },
        y:{ type:'linear', position:'left', beginAtZero:true, title:{display:true, text:'Volumes (Leads · Triagem · Agend. · Prop. · Fech.)', font:{family:'Inter',size:12,weight:'600'}, color:'#4B5563'}, ticks:{font:{family:'Inter',size:12},color:'#6B7280'}, grid:{color:'#F1F5F9'} },
        yPct:{ type:'linear', position:'right', beginAtZero:true, max:100, title:{display:true, text:'Tx Triagem (%)', font:{family:'Inter',size:12,weight:'600'}, color:'#0B63FF'}, ticks:{ callback:v=>v+'%', font:{family:'Inter',size:12}, color:'#0B63FF' }, grid:{display:false} } } }
  });
  const sources12m = __PROP__;
  new Chart(document.getElementById('chartSourceShare').getContext('2d'), {
    type:'bar',
    data:{ labels:['Agendamentos (12m)','Demos (12m)'],
      datasets: sources12m.map(s=>({ label:s.label, data:[s.RA, s.RR], backgroundColor:s.color, borderWidth:0, borderRadius:4, barPercentage:0.7, categoryPercentage:0.7 })) },
    options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false,
      plugins:{ legend:{ position:'top', align:'start', labels:{ font:{family:'Inter',size:12}, color:'#374151', usePointStyle:true, pointStyle:'rectRounded', padding:14, boxWidth:14 } },
        tooltip:{ backgroundColor:'#1F2937', padding:12, cornerRadius:8,
          callbacks:{ label:(c)=>{ const t=c.chart.data.datasets.reduce((s,ds)=>s+ds.data[c.dataIndex],0); const v=c.parsed.x; return `${c.dataset.label}: ${v} (${t?((v/t)*100).toFixed(1):0}%)`; } } } },
      scales:{ x:{ stacked:true, beginAtZero:true, ticks:{font:{family:'Inter',size:12},color:'#6B7280'}, grid:{color:'#F1F5F9'} },
        y:{ stacked:true, ticks:{font:{family:'Inter',size:13,weight:'600'},color:'#374151'}, grid:{display:false} } } }
  });
  function makeSortable(table){
    const ths = table.querySelectorAll('thead th');
    ths.forEach((th, idx)=>{
      if (th.textContent.trim()==='#') return;
      th.classList.add('sortable');
      const ind=document.createElement('span'); ind.className='sort-ind'; ind.textContent='⇅'; th.appendChild(ind);
      th.addEventListener('click', ()=>{
        const tbody=table.querySelector('tbody'); if(!tbody) return;
        const rows=Array.from(tbody.querySelectorAll('tr'));
        const dir = th.classList.contains('sort-asc') ? 'desc' : 'asc';
        ths.forEach(t=>{ t.classList.remove('sort-asc','sort-desc'); const i=t.querySelector('.sort-ind'); if(i) i.textContent='⇅'; });
        th.classList.add(dir==='asc'?'sort-asc':'sort-desc'); ind.textContent = dir==='asc'?'▲':'▼';
        const num = s=>{ const m=(s||'').match(/-?[\\d.,]+/); return m? parseFloat(m[0].replace(/\\./g,'').replace(',','.')) : NaN; };
        rows.sort((a,b)=>{ const sa=(a.children[idx]?.innerText||'').trim(), sb=(b.children[idx]?.innerText||'').trim();
          const na=num(sa), nb=num(sb); let c; if(!isNaN(na)&&!isNaN(nb)) c=na-nb; else c=sa.localeCompare(sb,'pt-BR',{numeric:true,sensitivity:'base'});
          return dir==='asc'?c:-c; });
        rows.forEach(r=>tbody.appendChild(r));
      });
    });
  }
  document.querySelectorAll('table').forEach(makeSortable);
</script>
"""


def _build_js(d):
    s = d['serie']
    return (_JS
            .replace('__LABELS__', json.dumps(s['labels'], ensure_ascii=False))
            .replace('__LEADS__', json.dumps(s['leads']))
            .replace('__TRIAGEM__', json.dumps(s['triagem']))
            .replace('__AGENDAMENTO__', json.dumps(s['agendamento']))
            .replace('__PROPOSTA__', json.dumps(s['proposta']))
            .replace('__FECHAMENTO__', json.dumps(s['fechamento']))
            .replace('__PROP__', json.dumps(d['proporcao'], ensure_ascii=False)))


# ============ MAIN ============

def main():
    ap = argparse.ArgumentParser(description='Gera o dashboard de Funil Inbound Cxpress Brasil.')
    ap.add_argument('--ate', type=str, default=None)
    ap.add_argument('--output', type=str, default=None)
    args = ap.parse_args()

    per = calcular_periodos(date.fromisoformat(args.ate) if args.ate else None)
    print("=" * 64)
    print("Dashboard Funil Inbound — Cxpress Brasil")
    print(f"Hoje: {per['hoje']} · Semana: {per['ini_atual']} -> {per['fim_atual']} · YtD -> {per['ytd_fim']}")
    print("=" * 64)

    url = load_url()
    with psycopg.connect(url, autocommit=True) as conn, conn.cursor() as cur:
        cur.execute("SET statement_timeout = '300s'")
        d = colher(cur, per)

    y = d['ytd']
    print(f"[render] YtD: {y['leads']} leads · {y['triagem']} triagem · {y['agendamento']} agend. · "
          f"{y['demo']} demos · {y['proposta']} propostas · {y['fechamento']} fechamentos")
    html = render_html(d)
    if HTML_PATH.exists():
        shutil.copy2(HTML_PATH, BAK_PATH)
    out = Path(args.output) if args.output else HTML_PATH
    out.write_text(html, encoding='utf-8')
    print(f"[render] HTML salvo em {out.name} ({len(html):,} bytes)")
    print("Pronto.")


if __name__ == '__main__':
    main()
