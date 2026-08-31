"""render_helpers.py — funcoes puras pra renderizar HTML a partir de dados estruturados.

Cada funcao retorna string HTML que sera injetada via gerar_relatorio.py.
Sem side effects, sem I/O.
"""
from __future__ import annotations

import html as html_lib
from datetime import date


# ============ ESCAPE & BADGES ============

def escape(s) -> str:
    if s is None:
        return ''
    return html_lib.escape(str(s), quote=False)


# mapeamento source -> classe CSS do badge
_BADGE_CLASSES = {
    'meta':                              'b-meta',
    'chatgpt.com':                       'b-chatgpt',
    'email':                             'b-email',
    'blog':                              'b-blog',
    'lp-agradecimento':                  'b-lp',
    'lp-agradecimento-oferta-trends':    'b-lp',
    'lp-agradecimento-evento':           'b-lp',
    'webinar-ao-vivo':                   'b-webinar',
    'apresentacao-webinar':              'b-webinar',
    'pos-webinar':                       'b-webinar',
    'notion':                            'b-notion',
    'linkedin':                          'b-linkedin',
    'tiktok':                            'b-tiktok',
}


def badge_source(name) -> str:
    """Renderiza badge de source com classe correta. Aceita None/vazio."""
    name = (name or '').strip() if name else ''
    if not name:
        return '<span class="b">(vazio)</span>'
    cls = _BADGE_CLASSES.get(name) or _BADGE_CLASSES.get(name.lower())
    if cls:
        return f'<span class="b {cls}">{escape(name)}</span>'
    return f'<span class="b">{escape(name)}</span>'


# ============ RANKING ============

def rank_cell(idx: int) -> str:
    """idx 0-based: 0->rk-1 (top), 1->rk-2, 2->rk-3, 3+ -> rk-n."""
    if idx == 0:   cls = 'rk-1'
    elif idx == 1: cls = 'rk-2'
    elif idx == 2: cls = 'rk-3'
    else:          cls = 'rk-n'
    return f'<span class="rk {cls}">{idx + 1}</span>'


# ============ FORMATADORES BR ============

def fmt_int(n) -> str:
    """1234 -> '1.234' (separador milhar BR)."""
    if n is None:
        return '0'
    return f'{int(n):,}'.replace(',', '.')


def fmt_decimal_br(n, casas: int = 1) -> str:
    """10.5 -> '10,5'."""
    if n is None:
        return '—'
    return f'{n:.{casas}f}'.replace('.', ',')


def fmt_pct_safe(num, den) -> str:
    """Percentual seguro: num/den * 100, com '—' quando den=0."""
    if not den:
        return '—'
    return f'{round(100 * num / den)}%'


def fmt_data_br(d) -> str:
    """date -> '15/05'. Aceita None."""
    if d is None:
        return '—'
    if isinstance(d, str):
        # ISO yyyy-mm-dd
        try:
            d = date.fromisoformat(d)
        except ValueError:
            return d
    return f'{d.day:02d}/{d.month:02d}'


def fmt_moeda_br(v) -> str:
    """12000 -> 'R$ 12.000/mês'. None ou 0 -> '—'."""
    if v is None or v == 0:
        return '—'
    intpart = int(round(float(v)))
    return f'R$ {intpart:,}/mês'.replace(',', '.')


def parse_valor_text(v) -> str:
    """Parseia campo 'value' (text) de deals_comercial_prod. Retorna fmt BR ou '—'."""
    if not v:
        return '—'
    s = str(v).strip()
    if not s:
        return '—'
    # remover R$, espacos, /mes, etc
    clean = s.replace('R$', '').replace('r$', '').strip()
    if '/' in clean:
        clean = clean.split('/')[0].strip()
    # remover ponto de milhar BR
    if ',' in clean:
        # formato BR: "12.000,00"
        clean = clean.replace('.', '').replace(',', '.')
    try:
        n = float(clean)
        return fmt_moeda_br(n)
    except (ValueError, TypeError):
        return '—'


# ============ DELTA (vs semana anterior) ============

def format_delta(atual: int, anterior: int, invert: bool = False) -> tuple[str, str]:
    """
    Retorna (texto, classe_css) para o componente .delta dos KPIs semanais.
    invert=True pra metricas onde "diminuir e bom" (Perdidos).
    """
    if anterior == 0 and atual == 0:
        return '— igual ant.', 'd-flat'
    if anterior == 0 and atual > 0:
        return f'▲ novo (0 → {atual})', 'd-new'
    if atual == anterior:
        return '— igual ant.', 'd-flat'
    delta = atual - anterior
    pct = round((delta / anterior) * 100) if anterior else 0
    arrow = '▲' if delta > 0 else '▼'
    sign = '+' if delta > 0 else '−'
    texto = f'{arrow} {sign}{abs(pct)}% vs ant.'
    if invert:
        classe = 'd-up' if delta < 0 else 'd-down'
    else:
        classe = 'd-up' if delta > 0 else 'd-down'
    return texto, classe


# ============ ROWS — LISTAS DE DEALS ============

def _deal_cell(d: dict) -> str:
    """Nome do deal envolto num link pro ActiveCampaign (instancia BR = buzzmonitor)."""
    name = escape(d.get('deal'))
    did = d.get('id')
    if not did:
        return f'<span class="deal-name">{name}</span>'
    return (
        f'<a class="deal-name" href="https://buzzmonitor.activehosted.com/app/deals/{did}" '
        f'target="_blank" rel="noopener noreferrer" title="Abrir deal no ActiveCampaign">{name}</a>'
    )


def row_lead(d: dict) -> str:
    return (
        '<tr>'
        f'<td>{_deal_cell(d)}</td>'
        f'<td class="dim">{escape(d.get("email") or "—")}</td>'
        f'<td>{badge_source(d.get("utm_source"))}</td>'
        f'<td class="dim">{escape(d.get("utm_content") or "—")}</td>'
        f'<td class="dim">{fmt_data_br(d.get("data_conversao"))}</td>'
        f'<td>{escape(d.get("bd") or "—")}</td>'
        '</tr>'
    )


def row_ra(d: dict) -> str:
    realizou = d.get('data_realizada')
    if realizou:
        realizou_html = f'<span class="b b-status-ok">✓ {fmt_data_br(realizou)}</span>'
    else:
        realizou_html = '<span class="b b-status-pending">Pendente</span>'
    return (
        '<tr>'
        f'<td>{_deal_cell(d)}</td>'
        f'<td>{escape(d.get("bd") or "—")}</td>'
        f'<td>{badge_source(d.get("utm_source"))}</td>'
        f'<td class="dim">{escape(d.get("utm_content") or "—")}</td>'
        f'<td class="dim">{fmt_data_br(d.get("data_evento"))}</td>'
        f'<td>{realizou_html}</td>'
        '</tr>'
    )


def row_rr(d: dict) -> str:
    prop = d.get('data_proposta')
    prop_html = '<span class="b b-status-ok">✓ Sim</span>' if prop else '<span class="b b-status-no">Não</span>'
    return (
        '<tr>'
        f'<td>{_deal_cell(d)}</td>'
        f'<td>{escape(d.get("bd") or "—")}</td>'
        f'<td>{badge_source(d.get("utm_source"))}</td>'
        f'<td class="dim">{fmt_data_br(d.get("data_evento"))}</td>'
        f'<td>{prop_html}</td>'
        '</tr>'
    )


def row_prop(d: dict) -> str:
    valor_html = parse_valor_text(d.get('valor_text'))
    return (
        '<tr>'
        f'<td>{_deal_cell(d)}</td>'
        f'<td>{escape(d.get("bd") or "—")}</td>'
        f'<td>{badge_source(d.get("utm_source"))}</td>'
        f'<td class="dim">{escape(d.get("utm_content") or "—")}</td>'
        f'<td class="dim">{fmt_data_br(d.get("data_evento"))}</td>'
        f'<td class="num">{valor_html}</td>'
        '</tr>'
    )


def row_fech(d: dict) -> str:
    v = d.get('valor')
    if v is not None and float(v) > 0:
        valor_html = f'<b>{fmt_moeda_br(float(v))}</b>'
    else:
        valor_html = '—'
    return (
        '<tr>'
        f'<td>{_deal_cell(d)}</td>'
        f'<td>{escape(d.get("bd") or "—")}</td>'
        f'<td>{badge_source(d.get("utm_source"))}</td>'
        f'<td class="dim">{escape(d.get("utm_content") or "—")}</td>'
        f'<td class="dim">{fmt_data_br(d.get("data_evento"))}</td>'
        f'<td class="num">{valor_html}</td>'
        '</tr>'
    )


def row_perda(d: dict) -> str:
    motivo = d.get('motivo') or ''
    motivos_strong = {'Sem fit', 'Sem orçamento', 'Desqualificado'}
    motivo_class = 'b-reason' if motivo in motivos_strong else 'b-reason-soft'
    return (
        '<tr>'
        f'<td>{_deal_cell(d)}</td>'
        f'<td class="dim">{escape(d.get("email") or "—")}</td>'
        f'<td>{badge_source(d.get("utm_source"))}</td>'
        f'<td class="dim">{escape(d.get("utm_content") or "—")}</td>'
        f'<td class="dim">{fmt_data_br(d.get("ultima_conversao"))}</td>'
        f'<td><span class="b {motivo_class}">{escape(motivo)}</span></td>'
        '</tr>'
    )


# ============ RANKING ROWS ============

def render_ranking_source(rows: list[dict], top_n: int = 8) -> str:
    """Renderiza linhas de ranking de SOURCES.
    rows: cada item tem keys: dim, leads, ce, ra, rr, prop, fech
    """
    if not rows:
        return '<tr><td colspan="10" class="dim center">(sem dados no período)</td></tr>'

    top = rows[:top_n]
    outros = rows[top_n:]
    out = [_row_ranking_src(i, r) for i, r in enumerate(top)]

    if outros:
        agreg = {k: sum(r[k] for r in outros) for k in ('leads', 'ce', 'ra', 'rr', 'prop', 'fech')}
        agreg['dim'] = f'outros ({len(outros)})'
        out.append(_row_ranking_src_outros(agreg))

    return '\n              '.join(out)


def _row_ranking_src(idx: int, r: dict) -> str:
    leads = r.get('leads', 0)
    leads_html = f'<b>{fmt_int(leads)}</b>' if idx < 3 else fmt_int(leads)
    return (
        '<tr>'
        f'<td>{rank_cell(idx)}</td>'
        f'<td>{badge_source(r.get("dim"))}</td>'
        f'<td class="num">{leads_html}</td>'
        f'<td class="num">{fmt_int(r.get("ce", 0))}</td>'
        f'<td class="num">{fmt_pct_safe(r.get("ce", 0), leads)}</td>'
        f'<td class="num">{fmt_int(r.get("ra", 0))}</td>'
        f'<td class="num">{fmt_pct_safe(r.get("ra", 0), r.get("ce", 0))}</td>'
        f'<td class="num">{fmt_int(r.get("rr", 0))}</td>'
        f'<td class="num">{fmt_int(r.get("prop", 0))}</td>'
        f'<td class="num">{fmt_int(r.get("fech", 0))}</td>'
        '</tr>'
    )


def _row_ranking_src_outros(r: dict) -> str:
    return (
        '<tr>'
        '<td><span class="rk rk-n">—</span></td>'
        f'<td class="dim">{escape(r["dim"])}</td>'
        f'<td class="num">{fmt_int(r["leads"])}</td>'
        f'<td class="num">{fmt_int(r["ce"])}</td>'
        '<td class="num">—</td>'
        f'<td class="num">{fmt_int(r["ra"])}</td>'
        '<td class="num">—</td>'
        f'<td class="num">{fmt_int(r["rr"])}</td>'
        f'<td class="num">{fmt_int(r["prop"])}</td>'
        f'<td class="num">{fmt_int(r["fech"])}</td>'
        '</tr>'
    )


def render_ranking_content(rows: list[dict], top_n: int = 12) -> str:
    """Renderiza linhas de ranking de CONTENT.
    rows: cada item tem keys: dim (content), source, leads, ra, rr, prop, fech
    """
    if not rows:
        return '<tr><td colspan="8" class="dim center">(sem dados no período)</td></tr>'

    top = rows[:top_n]
    outros = rows[top_n:]
    out = [_row_ranking_ct(i, r) for i, r in enumerate(top)]

    if outros:
        agreg = {k: sum(r[k] for r in outros) for k in ('leads', 'ra', 'rr', 'prop', 'fech')}
        agreg['dim'] = f'outros ({len(outros)})'
        out.append(_row_ranking_ct_outros(agreg))

    return '\n              '.join(out)


def _row_ranking_ct(idx: int, r: dict) -> str:
    leads = r.get('leads', 0)
    fech = r.get('fech', 0)
    leads_html = f'<b>{fmt_int(leads)}</b>' if idx < 3 else fmt_int(leads)
    fech_html = f'<b>{fmt_int(fech)}</b>' if fech > 0 else fmt_int(fech)
    content_label = r.get('dim') or '(sem content)'
    return (
        '<tr>'
        f'<td>{rank_cell(idx)}</td>'
        f'<td>{escape(content_label)}</td>'
        f'<td>{badge_source(r.get("source"))}</td>'
        f'<td class="num">{leads_html}</td>'
        f'<td class="num">{fmt_int(r.get("ra", 0))}</td>'
        f'<td class="num">{fmt_int(r.get("rr", 0))}</td>'
        f'<td class="num">{fmt_int(r.get("prop", 0))}</td>'
        f'<td class="num">{fech_html}</td>'
        '</tr>'
    )


def _row_ranking_ct_outros(r: dict) -> str:
    return (
        '<tr>'
        '<td><span class="rk rk-n">—</span></td>'
        f'<td class="dim">{escape(r["dim"])}</td>'
        '<td class="dim">—</td>'
        f'<td class="num">{fmt_int(r["leads"])}</td>'
        f'<td class="num">{fmt_int(r["ra"])}</td>'
        f'<td class="num">{fmt_int(r["rr"])}</td>'
        f'<td class="num">{fmt_int(r["prop"])}</td>'
        f'<td class="num">{fmt_int(r["fech"])}</td>'
        '</tr>'
    )


# ============ PROPORCAO SOURCES 12M (chart 5.2) ============

# Paleta harmonica em torno de #0B63FF
_SOURCE_COLORS = ['#0B63FF', '#073FA3', '#3D85FF', '#6EA7FF', '#A0C8FF', '#1E3A8A', '#94A3B8']
_OUTROS_COLOR = '#CBD5E1'


def render_proporcao_sources(rows: list[dict], top_n: int = 6) -> list[dict]:
    """
    rows: [{source, ra_12m, rr_12m}, ...] ordenado por ra_12m desc
    Retorna lista pronta pra injetar como JSON no chart 5.2:
      [{label, color, RA, RR}, ...]
    Agrega rest como 'outros'.
    """
    if not rows:
        return []
    top = rows[:top_n]
    rest = rows[top_n:]

    out = []
    for i, r in enumerate(top):
        out.append({
            'label': r.get('source') or '(vazio)',
            'color': _SOURCE_COLORS[i] if i < len(_SOURCE_COLORS) else '#94A3B8',
            'RA': int(r.get('ra_12m', 0)),
            'RR': int(r.get('rr_12m', 0)),
        })
    if rest:
        out.append({
            'label': 'outros',
            'color': _OUTROS_COLOR,
            'RA': sum(int(r.get('ra_12m', 0)) for r in rest),
            'RR': sum(int(r.get('rr_12m', 0)) for r in rest),
        })
    return out
