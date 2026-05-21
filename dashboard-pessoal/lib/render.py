"""render.py — transformacoes server-side antes de devolver JSON pro front.

Esse modulo NAO renderiza HTML (diferente do dashboard oficial). O front
faz o render. Aqui so transformamos dados crus em estruturas serializaveis.
"""
from __future__ import annotations

from datetime import date, timedelta
from typing import Any


# ============ PROPORCAO SOURCES 12M ============

# Mesma paleta do dashboard oficial.
_SOURCE_COLORS = ['#0B63FF', '#073FA3', '#3D85FF', '#6EA7FF', '#A0C8FF', '#1E3A8A', '#94A3B8']
_OUTROS_COLOR = '#CBD5E1'


def proporcao_sources(rows: list[dict], top_n: int = 6) -> list[dict]:
    """Transforma rows da q_proporcao_sources_12m em estrutura pro chart."""
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


# ============ SERIE TEMPORAL 12M (pivota 52 semanas) ============

def serie_temporal_12m(rows: list[dict], hoje: date) -> dict:
    """Pivota rows da q_serie_temporal_12m em arrays alinhados por semana.

    Retorna dict {labels, leads, ce, agendadas, propostas, fechamentos} — cada
    valor sao 52 ints (uma por semana, segunda como inicio).
    """
    segunda_atual = hoje - timedelta(days=hoje.weekday())
    inicio = segunda_atual - timedelta(weeks=51)
    semanas = [inicio + timedelta(weeks=i) for i in range(52)]

    counts: dict[tuple, int] = {}
    for r in rows:
        s = r['semana']
        m = r['metrica']
        counts[(s, m)] = int(r['n'])

    labels = [f'{s.day:02d}/{s.month:02d}' for s in semanas]
    metricas = ['leads', 'ce', 'agendadas', 'propostas', 'fechamentos']
    return {
        'labels': labels,
        **{m: [counts.get((s, m), 0) for s in semanas] for m in metricas},
    }


# ============ ENRIQUECIMENTO CONTENT COM SOURCE ============

def enriquecer_content(rows: list[dict], src_map: dict) -> list[dict]:
    """Adiciona 'source' a cada row de ranking_content baseado em src_map."""
    for r in rows:
        r['source'] = src_map.get(r.get('dim'))
    return rows


# ============ SERIALIZACAO (datas, decimal, etc) ============

def jsonify(obj: Any) -> Any:
    """Converte recursivamente dates/decimals/etc pra tipos JSON-safe."""
    if obj is None:
        return None
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, (list, tuple)):
        return [jsonify(x) for x in obj]
    if isinstance(obj, dict):
        return {k: jsonify(v) for k, v in obj.items()}
    if isinstance(obj, (int, float, bool, str)):
        return obj
    # decimal.Decimal nao tem __index__ mas tem __float__
    try:
        return float(obj)
    except (TypeError, ValueError):
        return str(obj)
