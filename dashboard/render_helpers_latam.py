"""render_helpers_latam.py — renderers HTML (ES/USD) para a dashboard CM LATAM.

Reaproveita os genéricos de render_helpers.py (escape, rank_cell, badge_source,
format_delta, fmt_int) e adiciona o que é específico da LATAM: moeda USD, datas, e os
renderers de linha/ranking do funil de 5 fases (Leads · Primer contacto · Reunión · Cierre).
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from render_helpers import (  # genéricos reaproveitados
    escape, rank_cell, fmt_int, _SOURCE_COLORS, _OUTROS_COLOR, _BADGE_CLASSES,
)


# ============ BADGE / DELTA (variantes ES) ============

def badge_source(name) -> str:
    """Badge de fonte (reusa as classes do Brasil; vazio em ES)."""
    name = (name or '').strip() if name else ''
    if not name or name == '(vacío)':
        return '<span class="b">(vacío)</span>'
    cls = _BADGE_CLASSES.get(name)
    return f'<span class="b {cls}">{escape(name)}</span>' if cls else f'<span class="b">{escape(name)}</span>'


def format_delta(atual: int, anterior: int, invert: bool = False) -> tuple[str, str]:
    """Delta vs semana anterior, em espanhol. invert=True para métricas onde cair é bom."""
    if anterior == 0 and atual == 0:
        return '— igual', 'd-flat'
    if anterior == 0 and atual > 0:
        return f'▲ nuevo (0 → {atual})', 'd-new'
    if atual == anterior:
        return '— igual', 'd-flat'
    delta = atual - anterior
    pct = round((delta / anterior) * 100) if anterior else 0
    arrow = '▲' if delta > 0 else '▼'
    sign = '+' if delta > 0 else '−'
    texto = f'{arrow} {sign}{abs(pct)}% vs sem. ant.'
    if invert:
        classe = 'd-up' if delta < 0 else 'd-down'
    else:
        classe = 'd-up' if delta > 0 else 'd-down'
    return texto, classe


# ============ FORMATADORES ES / USD ============

def fmt_usd(v) -> str:
    if v is None or v == 0:
        return '—'
    return f'US$ {int(round(float(v))):,}/mes'.replace(',', '.')


def fmt_pct(num, den) -> str:
    """Percentual estilo Brasil: num/den (pode passar de 100%). '—' se den=0."""
    if not den:
        return '—'
    return f'{round(100 * (num or 0) / den)}%'


def fmt_fecha(d) -> str:
    if d is None:
        return '—'
    if isinstance(d, str):
        try:
            d = date.fromisoformat(d[:10])
        except ValueError:
            return d
    return f'{d.day:02d}/{d.month:02d}'


# ============ ROWS — LISTAS ============

def _resp(d):
    return escape(d.get('responsable') or '—')


def row_lead(d: dict) -> str:
    return (
        '<tr>'
        f'<td><span class="deal-name">{escape(d.get("deal"))}</span></td>'
        f'<td>{badge_source(d.get("utm_source"))}</td>'
        f'<td class="dim">{escape(d.get("utm_content") or "—")}</td>'
        f'<td class="dim">{escape(d.get("pais") or "—")}</td>'
        f'<td class="dim">{fmt_fecha(d.get("data_conversao"))}</td>'
        f'<td>{_resp(d)}</td>'
        '</tr>'
    )


def row_reunion(d: dict) -> str:
    return (
        '<tr>'
        f'<td><span class="deal-name">{escape(d.get("deal"))}</span></td>'
        f'<td>{_resp(d)}</td>'
        f'<td>{badge_source(d.get("utm_source"))}</td>'
        f'<td class="dim">{escape(d.get("utm_content") or "—")}</td>'
        f'<td class="dim">{escape(d.get("pais") or "—")}</td>'
        f'<td class="dim">{fmt_fecha(d.get("data_evento"))}</td>'
        '</tr>'
    )


def row_cierre(d: dict) -> str:
    v = d.get('valor')
    valor_html = f'<b>{fmt_usd(v)}</b>' if (v and float(v) > 0) else '—'
    return (
        '<tr>'
        f'<td><span class="deal-name">{escape(d.get("deal"))}</span></td>'
        f'<td>{_resp(d)}</td>'
        f'<td>{badge_source(d.get("utm_source"))}</td>'
        f'<td class="dim">{escape(d.get("pais") or "—")}</td>'
        f'<td class="dim">{fmt_fecha(d.get("data_fech"))}</td>'
        f'<td class="num">{valor_html}</td>'
        '</tr>'
    )


def row_perda(d: dict) -> str:
    return (
        '<tr>'
        f'<td><span class="deal-name">{escape(d.get("deal"))}</span></td>'
        f'<td>{badge_source(d.get("utm_source"))}</td>'
        f'<td class="dim">{escape(d.get("utm_content") or "—")}</td>'
        f'<td class="dim">{escape(d.get("pais") or "—")}</td>'
        f'<td class="dim">{fmt_fecha(d.get("data_evento"))}</td>'
        '</tr>'
    )


def empty_row(cols: int) -> str:
    return f'<tr><td colspan="{cols}" class="dim center">(sin datos en el período)</td></tr>'


# ============ RANKING ROWS ============

def render_ranking_source(rows: list[dict], top_n: int = 8) -> str:
    """Colunas: # | Fuente | Leads | PC | %PC | Reunión | %Reu | Cierre."""
    if not rows:
        return empty_row(8)
    top = rows[:top_n]
    outros = rows[top_n:]
    out = [_row_rk_src(i, r) for i, r in enumerate(top)]
    if outros:
        agg = {k: sum(r.get(k, 0) for r in outros) for k in ('leads', 'pc', 'reunion', 'cierre')}
        out.append(
            '<tr><td><span class="rk rk-n">—</span></td>'
            f'<td class="dim">otros ({len(outros)})</td>'
            f'<td class="num">{fmt_int(agg["leads"])}</td>'
            f'<td class="num">{fmt_int(agg["pc"])}</td><td class="num">—</td>'
            f'<td class="num">{fmt_int(agg["reunion"])}</td><td class="num">—</td>'
            f'<td class="num">{fmt_int(agg["cierre"])}</td></tr>'
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
        f'<td class="num">{fmt_int(r.get("pc", 0))}</td>'
        f'<td class="num">{fmt_pct(r.get("pc", 0), leads)}</td>'
        f'<td class="num">{fmt_int(r.get("reunion", 0))}</td>'
        f'<td class="num">{fmt_pct(r.get("reunion", 0), r.get("pc", 0))}</td>'
        f'<td class="num">{fmt_int(r.get("cierre", 0))}</td>'
        '</tr>'
    )


def render_ranking_content(rows: list[dict], src_map: dict, top_n: int = 12) -> str:
    """Colunas: # | Contenido | Fuente | Leads | PC | Reunión | Cierre."""
    if not rows:
        return empty_row(7)
    top = rows[:top_n]
    outros = rows[top_n:]
    out = [_row_rk_ct(i, r, src_map) for i, r in enumerate(top)]
    if outros:
        agg = {k: sum(r.get(k, 0) for r in outros) for k in ('leads', 'pc', 'reunion', 'cierre')}
        out.append(
            '<tr><td><span class="rk rk-n">—</span></td>'
            f'<td class="dim">otros ({len(outros)})</td><td class="dim">—</td>'
            f'<td class="num">{fmt_int(agg["leads"])}</td>'
            f'<td class="num">{fmt_int(agg["pc"])}</td>'
            f'<td class="num">{fmt_int(agg["reunion"])}</td>'
            f'<td class="num">{fmt_int(agg["cierre"])}</td></tr>'
        )
    return '\n              '.join(out)


def _row_rk_ct(idx: int, r: dict, src_map: dict) -> str:
    leads = r.get('leads', 0)
    cierre = r.get('cierre', 0)
    leads_html = f'<b>{fmt_int(leads)}</b>' if idx < 3 else fmt_int(leads)
    cierre_html = f'<b>{fmt_int(cierre)}</b>' if cierre > 0 else fmt_int(cierre)
    content = r.get('dim') or '(vacío)'
    src = src_map.get(r.get('dim'))
    return (
        '<tr>'
        f'<td>{rank_cell(idx)}</td>'
        f'<td>{escape(content)}</td>'
        f'<td>{badge_source(src)}</td>'
        f'<td class="num">{leads_html}</td>'
        f'<td class="num">{fmt_int(r.get("pc", 0))}</td>'
        f'<td class="num">{fmt_int(r.get("reunion", 0))}</td>'
        f'<td class="num">{cierre_html}</td>'
        '</tr>'
    )


# ============ PROPORÇÃO (chart 5.2) ============

def render_proporcao(rows: list[dict], top_n: int = 6) -> list[dict]:
    """rows: [{source, pc_12m, reunion_12m}] -> [{label,color,PC,RE}] (top_n + otros)."""
    if not rows:
        return []
    top = rows[:top_n]
    rest = rows[top_n:]
    out = []
    for i, r in enumerate(top):
        out.append({
            'label': r.get('source') or '(vacío)',
            'color': _SOURCE_COLORS[i] if i < len(_SOURCE_COLORS) else '#94A3B8',
            'PC': int(r.get('pc_12m', 0)),
            'RE': int(r.get('reunion_12m', 0)),
        })
    if rest:
        out.append({
            'label': 'otros',
            'color': _OUTROS_COLOR,
            'PC': sum(int(r.get('pc_12m', 0)) for r in rest),
            'RE': sum(int(r.get('reunion_12m', 0)) for r in rest),
        })
    return out
