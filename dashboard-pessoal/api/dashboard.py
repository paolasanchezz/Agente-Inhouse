"""api/dashboard.py — handler HTTP usado pelo run_local.py.

(Originalmente foi escrito pra rodar como serverless function no Vercel, mas
mudamos pra local-only depois que o pooler IPv4 do Supabase nao aceitou o
user `looker_readonly`. A assinatura `class handler(BaseHTTPRequestHandler)`
ficou porque eh compativel com o servidor `run_local.py` da pasta.)

Endpoint:
    GET /api/dashboard?ini=YYYY-MM-DD&fim=YYYY-MM-DD&historico=1
    GET /api/dashboard?preset=7d|15d|30d|90d|mtd|ytd
    GET /api/dashboard?...&refresh=1   ← bypass do cache

Retorna JSON com:
- kpis (atual, anterior, mtd, ytd)
- listas (leads, ra, rr, prop, fech, perdidos_mtd)
- rankings (source × content × 4 periodos)
- serie_12m (gráfico 5.1)         — so com historico=1
- proporcao_sources (gráfico 5.2) — so com historico=1
- _meta.cached: true|false        — se a resposta veio do cache em memoria
- _meta.cached_at: ISO timestamp  — quando o cache foi populado

Cache em memoria: persiste enquanto o servidor estiver rodando.
"""
from __future__ import annotations

import copy
import json
import os
import sys
import threading
import time
import traceback
from datetime import date, datetime
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Permite import de ../lib
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import psycopg

from lib.datas import calcular_periodos, preset_periodo
from lib.queries import (
    q_count_evento, q_count_fechamentos, q_count_leads, q_count_perdidos,
    q_lista_evento, q_lista_fechamentos, q_lista_leads, q_lista_perdidos,
    q_lista_propostas, q_proporcao_sources_12m, q_ranking,
    q_serie_temporal_12m, q_source_por_content,
)
from lib.render import enriquecer_content, jsonify, proporcao_sources, serie_temporal_12m


def _get_pg_url() -> str:
    url = os.environ.get('SUPABASE_PG_URL')
    if not url:
        raise RuntimeError("SUPABASE_PG_URL nao definido no env")
    return url


def _fetch_dict(cur, sql: str) -> list[dict]:
    cur.execute(sql)
    cols = [d.name for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def _fetch_scalar(cur, sql: str):
    cur.execute(sql)
    row = cur.fetchone()
    return row[0] if row else 0


def _kpis(cur, ini: date, fim: date) -> dict:
    return {
        'leads': _fetch_scalar(cur, q_count_leads(ini, fim)),
        'ce':    _fetch_scalar(cur, q_count_evento('ce', ini, fim)),
        'ra':    _fetch_scalar(cur, q_count_evento('ra', ini, fim)),
        'rr':    _fetch_scalar(cur, q_count_evento('rr', ini, fim)),
        'prop':  _fetch_scalar(cur, q_count_evento('prop', ini, fim)),
        'fech':  _fetch_scalar(cur, q_count_fechamentos(ini, fim)),
        'perd':  _fetch_scalar(cur, q_count_perdidos(ini, fim)),
    }


def coletar(ini: date, fim: date, historico: bool = True) -> dict:
    periodos = calcular_periodos(ini, fim)
    out: dict = {'periodos': periodos}

    url = _get_pg_url()
    with psycopg.connect(url, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("SET statement_timeout = '60s'")

            ini_a, fim_a = periodos['ini_atual'], periodos['fim_atual']
            ini_p, fim_p = periodos['ini_ant'], periodos['fim_ant']
            mtd_i, mtd_f = periodos['mtd_ini'], periodos['mtd_fim']
            ytd_i, ytd_f = periodos['ytd_ini'], periodos['ytd_fim']

            out['kpis'] = {
                'atual': _kpis(cur, ini_a, fim_a),
                'ant':   _kpis(cur, ini_p, fim_p),
                'mtd':   _kpis(cur, mtd_i, mtd_f),
                'ytd':   _kpis(cur, ytd_i, ytd_f),
            }

            out['listas'] = {
                'leads':         _fetch_dict(cur, q_lista_leads(ini_a, fim_a)),
                'ra':            _fetch_dict(cur, q_lista_evento('ra', ini_a, fim_a)),
                'rr':            _fetch_dict(cur, q_lista_evento('rr', ini_a, fim_a)),
                'prop':          _fetch_dict(cur, q_lista_propostas(ini_a, fim_a)),
                'fech':          _fetch_dict(cur, q_lista_fechamentos(ini_a, fim_a)),
                'perdidos_mtd':  _fetch_dict(cur, q_lista_perdidos(mtd_i, mtd_f)),
            }

            src_map = {
                r['utm_content']: r['utm_source']
                for r in _fetch_dict(cur, q_source_por_content(ytd_i, ytd_f))
            }
            out['rankings'] = {
                'source': {
                    'atual': _fetch_dict(cur, q_ranking('utm_source', ini_a, fim_a)),
                    'ant':   _fetch_dict(cur, q_ranking('utm_source', ini_p, fim_p)),
                    'mtd':   _fetch_dict(cur, q_ranking('utm_source', mtd_i, mtd_f)),
                    'ytd':   _fetch_dict(cur, q_ranking('utm_source', ytd_i, ytd_f)),
                },
                'content': {
                    'atual': enriquecer_content(_fetch_dict(cur, q_ranking('utm_content', ini_a, fim_a)), src_map),
                    'ant':   enriquecer_content(_fetch_dict(cur, q_ranking('utm_content', ini_p, fim_p)), src_map),
                    'mtd':   enriquecer_content(_fetch_dict(cur, q_ranking('utm_content', mtd_i, mtd_f)), src_map),
                    'ytd':   enriquecer_content(_fetch_dict(cur, q_ranking('utm_content', ytd_i, ytd_f)), src_map),
                },
            }

            if historico:
                hoje = periodos['hoje']
                out['serie_12m'] = serie_temporal_12m(
                    _fetch_dict(cur, q_serie_temporal_12m(hoje)), hoje
                )
                out['proporcao_sources'] = proporcao_sources(
                    _fetch_dict(cur, q_proporcao_sources_12m(hoje))
                )

    return jsonify(out)


# ============ CACHE EM MEMORIA ============
# Persiste enquanto o servidor estiver rodando. Reinicia servidor pra limpar.
# Key: (ini_iso, fim_iso, historico) → (timestamp, data)
_CACHE: dict = {}
_CACHE_LOCK = threading.Lock()


def coletar_cached(ini: date, fim: date, historico: bool, refresh: bool = False) -> tuple[dict, bool, float]:
    """Retorna (data, was_cached, cached_at_ts). Se refresh=True, ignora cache e re-fetcha."""
    key = (ini.isoformat(), fim.isoformat(), historico)

    if not refresh:
        with _CACHE_LOCK:
            if key in _CACHE:
                ts, data = _CACHE[key]
                # Devolve copia rasa pra que o caller possa adicionar _meta sem mutar cache
                return copy.copy(data), True, ts

    data = coletar(ini, fim, historico=historico)
    now = time.time()
    with _CACHE_LOCK:
        _CACHE[key] = (now, data)
    return copy.copy(data), False, now


def cache_stats() -> dict:
    with _CACHE_LOCK:
        return {
            'entries': len(_CACHE),
            'keys': [{'ini': k[0], 'fim': k[1], 'historico': k[2], 'cached_at': v[0]} for k, v in _CACHE.items()],
        }


def _parse_query(qs: str) -> dict:
    parsed = parse_qs(qs)
    return {k: v[0] if v else '' for k, v in parsed.items()}


def _resolve_periodo(params: dict):
    """Aceita ini/fim ISO ou preset=7d/15d/30d/90d/mtd/ytd. Default: 7d."""
    if params.get('preset'):
        return preset_periodo(params['preset'])
    ini = params.get('ini')
    fim = params.get('fim')
    if ini and fim:
        return date.fromisoformat(ini), date.fromisoformat(fim)
    return preset_periodo('7d')


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            params = _parse_query(parsed.query)

            ini, fim = _resolve_periodo(params)
            historico = params.get('historico', '1') != '0'
            refresh = params.get('refresh') == '1'

            data, was_cached, cached_at_ts = coletar_cached(ini, fim, historico=historico, refresh=refresh)
            data['_meta'] = {
                'cached': was_cached,
                'cached_at': datetime.fromtimestamp(cached_at_ts).isoformat(timespec='seconds'),
            }
            body = json.dumps(data, ensure_ascii=False, default=str).encode('utf-8')

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Cache', 'HIT' if was_cached else 'MISS')
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            err = {
                'error': str(e),
                'type': type(e).__name__,
                'trace': traceback.format_exc(),
            }
            body = json.dumps(err, ensure_ascii=False).encode('utf-8')
            self.send_response(500)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
