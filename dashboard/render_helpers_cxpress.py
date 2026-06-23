"""render_helpers_cxpress.py — renderers HTML (PT-BR / BRL) para a dashboard de Content Marketing Cxpress.

Reaproveita os genericos de render_helpers.py (escape, rank_cell, badges, formatadores BR,
format_delta, parse_valor_text, render_proporcao_sources) — Cxpress e PT-BR/BRL igual ao Brasil,
so muda o funil (Lead · Triagem · Agendamento · Demo · Proposta · Fechamento + Perdido).
"""
from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import unquote_plus

sys.path.insert(0, str(Path(__file__).parent))
from render_helpers import (  # genericos reaproveitados (PT-BR)
    escape, rank_cell,
    fmt_int, fmt_pct_safe, fmt_data_br, fmt_moeda_br, parse_valor_text,
    format_delta, render_proporcao_sources,
)
from render_helpers import badge_source as _badge_source_base


def badge_source(name) -> str:
    """badge_source com aliases Cxpress: trafego Meta (ig/fb/instagram*/facebook*) usa o badge b-meta."""
    n = (name or '').strip().lower()
    if n in ('ig', 'fb') or n.startswith('instagram') or n.startswith('facebook'):
        return f'<span class="b b-meta">{escape(name)}</span>'
    return _badge_source_base(name)


# Instancia ActiveCampaign da Cxpress = elife (Buzzmonitor usa buzzmonitor.activehosted.com).
AC_DEALS_BASE = 'https://elife.activehosted.com/app/deals/'


def _deal_cell(d: dict) -> str:
    """Nome do deal envolto num link pro ActiveCampaign (igual _deal_cell do Buzz BR)."""
    name = escape(d.get('deal'))
    did = d.get('id')
    if not did:
        return f'<span class="deal-name">{name}</span>'
    return (
        f'<a class="deal-name" href="{AC_DEALS_BASE}{did}" '
        f'target="_blank" rel="noopener noreferrer" title="Abrir deal no ActiveCampaign">{name}</a>'
    )


def empty_row(cols: int) -> str:
    return f'<tr><td colspan="{cols}" class="dim center">(sem dados no período)</td></tr>'


def _resp(d: dict) -> str:
    return escape(d.get('responsavel') or '—')


def _decode_content(v):
    """Decodifica o utm_content efetivo, que chega URL-encoded da query (queries_cxpress._content):
    '+' -> espaco e %XX -> caractere. Vale tanto pro valor extraido de url_conversao quanto pra
    coluna utm_content (alguns valores da coluna tambem chegam com '+', ex 'ad_04_estatico+-+...').
    Devolve None pra vazio/None (o chamador resolve o fallback '—' / '(sem conteúdo)')."""
    if not v:
        return None
    try:
        return unquote_plus(v)
    except Exception:
        return v


# ============ ROWS — LISTAS ============

def row_lead(d: dict) -> str:
    return (
        '<tr>'
        f'<td>{_deal_cell(d)}</td>'
        f'<td>{badge_source(d.get("utm_source"))}</td>'
        f'<td class="dim">{escape(_decode_content(d.get("utm_content")) or "—")}</td>'
        f'<td class="dim">{fmt_data_br(d.get("data_evento"))}</td>'
        f'<td>{_resp(d)}</td>'
        '</tr>'
    )


def row_agendamento(d: dict) -> str:
    """Coluna final: a demo ja foi realizada?"""
    demo = d.get('data_demo')
    demo_html = (f'<span class="b b-status-ok">✓ {fmt_data_br(demo)}</span>'
                 if demo else '<span class="b b-status-pending">Pendente</span>')
    return (
        '<tr>'
        f'<td>{_deal_cell(d)}</td>'
        f'<td>{_resp(d)}</td>'
        f'<td>{badge_source(d.get("utm_source"))}</td>'
        f'<td class="dim">{escape(_decode_content(d.get("utm_content")) or "—")}</td>'
        f'<td class="dim">{fmt_data_br(d.get("data_evento"))}</td>'
        f'<td>{demo_html}</td>'
        '</tr>'
    )


def row_demo(d: dict) -> str:
    """Coluna final: saiu proposta?"""
    prop = d.get('data_proposta')
    prop_html = ('<span class="b b-status-ok">✓ Sim</span>' if prop
                 else '<span class="b b-status-no">Não</span>')
    return (
        '<tr>'
        f'<td>{_deal_cell(d)}</td>'
        f'<td>{_resp(d)}</td>'
        f'<td>{badge_source(d.get("utm_source"))}</td>'
        f'<td class="dim">{escape(_decode_content(d.get("utm_content")) or "—")}</td>'
        f'<td class="dim">{fmt_data_br(d.get("data_evento"))}</td>'
        f'<td>{prop_html}</td>'
        '</tr>'
    )


def row_prop(d: dict) -> str:
    return (
        '<tr>'
        f'<td>{_deal_cell(d)}</td>'
        f'<td>{_resp(d)}</td>'
        f'<td>{badge_source(d.get("utm_source"))}</td>'
        f'<td class="dim">{escape(_decode_content(d.get("utm_content")) or "—")}</td>'
        f'<td class="dim">{fmt_data_br(d.get("data_evento"))}</td>'
        f'<td class="num">{parse_valor_text(d.get("valor_text"))}</td>'
        '</tr>'
    )


def row_fech(d: dict) -> str:
    valor_html = parse_valor_text(d.get('valor_text'))
    valor_html = f'<b>{valor_html}</b>' if valor_html != '—' else '—'
    return (
        '<tr>'
        f'<td>{_deal_cell(d)}</td>'
        f'<td>{_resp(d)}</td>'
        f'<td>{badge_source(d.get("utm_source"))}</td>'
        f'<td class="dim">{escape(_decode_content(d.get("utm_content")) or "—")}</td>'
        f'<td class="dim">{fmt_data_br(d.get("data_evento"))}</td>'
        f'<td class="num">{valor_html}</td>'
        '</tr>'
    )


def row_perda(d: dict) -> str:
    motivo = d.get('motivo') or ''
    motivos_strong = {'Sem fit', 'Sem orçamento', 'Sem budget', 'Desqualificado'}
    motivo_class = 'b-reason' if motivo in motivos_strong else 'b-reason-soft'
    motivo_html = f'<span class="b {motivo_class}">{escape(motivo)}</span>' if motivo else '<span class="dim">—</span>'
    return (
        '<tr>'
        f'<td>{_deal_cell(d)}</td>'
        f'<td>{badge_source(d.get("utm_source"))}</td>'
        f'<td class="dim">{escape(_decode_content(d.get("utm_content")) or "—")}</td>'
        f'<td class="dim">{escape(d.get("etapa") or "—")}</td>'
        f'<td class="dim">{fmt_data_br(d.get("data_evento"))}</td>'
        f'<td>{motivo_html}</td>'
        '</tr>'
    )


# ============ RANKING DE SOURCES ============
# Colunas: # | Fonte | Leads | Triagem | %Tri | Agend. | %Agd | Demo | Prop. | Fech.

_MET = ('leads', 'triagem', 'agendamento', 'demo', 'proposta', 'fechamento')


def render_ranking_source(rows: list[dict], top_n: int = 8) -> str:
    if not rows:
        return empty_row(10)
    top, outros = rows[:top_n], rows[top_n:]
    out = [_row_rk_src(i, r) for i, r in enumerate(top)]
    if outros:
        agg = {k: sum(r.get(k, 0) for r in outros) for k in _MET}
        out.append(
            '<tr><td><span class="rk rk-n">—</span></td>'
            f'<td class="dim">outros ({len(outros)})</td>'
            f'<td class="num">{fmt_int(agg["leads"])}</td>'
            f'<td class="num">{fmt_int(agg["triagem"])}</td><td class="num">—</td>'
            f'<td class="num">{fmt_int(agg["agendamento"])}</td><td class="num">—</td>'
            f'<td class="num">{fmt_int(agg["demo"])}</td>'
            f'<td class="num">{fmt_int(agg["proposta"])}</td>'
            f'<td class="num">{fmt_int(agg["fechamento"])}</td></tr>'
        )
    return '\n              '.join(out)


def _row_rk_src(idx: int, r: dict) -> str:
    leads = r.get('leads', 0)
    leads_html = f'<b>{fmt_int(leads)}</b>' if idx < 3 else fmt_int(leads)
    return (
        '<tr>'
        f'<td>{rank_cell(idx)}</td>'
        f'<td>{badge_source(r.get("dim"))}</td>'
        f'<td class="num">{leads_html}</td>'
        f'<td class="num">{fmt_int(r.get("triagem", 0))}</td>'
        f'<td class="num">{fmt_pct_safe(r.get("triagem", 0), leads)}</td>'
        f'<td class="num">{fmt_int(r.get("agendamento", 0))}</td>'
        f'<td class="num">{fmt_pct_safe(r.get("agendamento", 0), r.get("triagem", 0))}</td>'
        f'<td class="num">{fmt_int(r.get("demo", 0))}</td>'
        f'<td class="num">{fmt_int(r.get("proposta", 0))}</td>'
        f'<td class="num">{fmt_int(r.get("fechamento", 0))}</td>'
        '</tr>'
    )


# ============ RANKING DE CONTENT ============
# Colunas: # | Conteúdo | Fonte | Leads | Agend. | Demo | Prop. | Fech.

def render_ranking_content(rows: list[dict], src_map: dict, top_n: int = 12) -> str:
    if not rows:
        return empty_row(8)
    top, outros = rows[:top_n], rows[top_n:]
    out = [_row_rk_ct(i, r, src_map) for i, r in enumerate(top)]
    if outros:
        agg = {k: sum(r.get(k, 0) for r in outros) for k in ('leads', 'agendamento', 'demo', 'proposta', 'fechamento')}
        out.append(
            '<tr><td><span class="rk rk-n">—</span></td>'
            f'<td class="dim">outros ({len(outros)})</td><td class="dim">—</td>'
            f'<td class="num">{fmt_int(agg["leads"])}</td>'
            f'<td class="num">{fmt_int(agg["agendamento"])}</td>'
            f'<td class="num">{fmt_int(agg["demo"])}</td>'
            f'<td class="num">{fmt_int(agg["proposta"])}</td>'
            f'<td class="num">{fmt_int(agg["fechamento"])}</td></tr>'
        )
    return '\n              '.join(out)


def _row_rk_ct(idx: int, r: dict, src_map: dict) -> str:
    leads = r.get('leads', 0)
    fech = r.get('fechamento', 0)
    leads_html = f'<b>{fmt_int(leads)}</b>' if idx < 3 else fmt_int(leads)
    fech_html = f'<b>{fmt_int(fech)}</b>' if fech > 0 else fmt_int(fech)
    content = _decode_content(r.get('dim')) or '(sem conteúdo)'
    src = src_map.get(r.get('dim'))  # chave crua (URL-encoded) — bate com a do q_source_por_content
    return (
        '<tr>'
        f'<td>{rank_cell(idx)}</td>'
        f'<td>{escape(content)}</td>'
        f'<td>{badge_source(src)}</td>'
        f'<td class="num">{leads_html}</td>'
        f'<td class="num">{fmt_int(r.get("agendamento", 0))}</td>'
        f'<td class="num">{fmt_int(r.get("demo", 0))}</td>'
        f'<td class="num">{fmt_int(r.get("proposta", 0))}</td>'
        f'<td class="num">{fech_html}</td>'
        '</tr>'
    )
