"""paridade_gerar_esperado.py — roda a dash LOCAL (fonte da verdade) e salva
paridade_esperado.json pro paridade_check.mjs comparar o motor.js.

ENXUTO: a query de atribuicao 90d custa ~8s. Pra nao levar 30min, validamos o
KPI de cada intervalo (7 counts) numa lista variada de intervalos — que cobre
atual/ant/mtd/ytd implicitamente (cada um e so "o atual" de outro intervalo) —
mais listas+ranking so no YtD (cobre dedup e group by). Usa as MESMAS SQLs da
dash local, entao os numeros sao identicos.

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard-buzz-br-vercel/paridade_gerar_esperado.py
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOCAL = ROOT.parent / "dashboard-pessoal"
sys.path.insert(0, str(LOCAL))

for _line in (LOCAL / ".env").read_text(encoding="utf-8").splitlines():
    _l = _line.strip()
    if _l.startswith("SUPABASE_PG_URL=") and "SUPABASE_PG_URL" not in os.environ:
        os.environ["SUPABASE_PG_URL"] = _l.split("=", 1)[1].strip().strip('"').strip("'")

import psycopg  # noqa: E402
from lib.queries import (  # noqa: E402
    q_count_leads, q_count_evento, q_count_fechamentos, q_count_perdidos,
    q_lista_leads, q_lista_evento, q_lista_propostas, q_lista_fechamentos, q_lista_perdidos,
    q_ranking, q_source_por_content,
)
from lib.render import enriquecer_content  # noqa: E402

# Intervalos variados. "atual" de cada um cobre os 4 periodos que o motor deriva.
# Pequenos primeiro (aquecem cache). "*"=tem validacao extra (listas+ranking).
RANGES = [
    ("um_dia",       "2026-05-20", "2026-05-20", False),
    ("cross_month",  "2026-04-15", "2026-05-15", False),
    ("maio_inteiro", "2026-05-01", "2026-05-31", False),
    ("ytd",          "2026-01-01", "2026-07-01", True),
]


def _fd(cur, sql):
    cur.execute(sql)
    cols = [d.name for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def _fs(cur, sql):
    cur.execute(sql)
    row = cur.fetchone()
    return row[0] if row else 0


def _kpis(cur, ini, fim):
    return {
        'leads': _fs(cur, q_count_leads(ini, fim)),
        'ce':    _fs(cur, q_count_evento('ce', ini, fim)),
        'ra':    _fs(cur, q_count_evento('ra', ini, fim)),
        'rr':    _fs(cur, q_count_evento('rr', ini, fim)),
        'prop':  _fs(cur, q_count_evento('prop', ini, fim)),
        'fech':  _fs(cur, q_count_fechamentos(ini, fim)),
        'perd':  _fs(cur, q_count_perdidos(ini, fim)),
    }


def _rank(rows):
    return [{"dim": r.get("dim"), "leads": r.get("leads", 0), "ce": r.get("ce", 0),
             "ra": r.get("ra", 0), "rr": r.get("rr", 0), "prop": r.get("prop", 0),
             "fech": r.get("fech", 0)} for r in rows]


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    out = {}
    url = os.environ["SUPABASE_PG_URL"]
    with psycopg.connect(url, autocommit=True, connect_timeout=20) as conn, conn.cursor() as cur:
        cur.execute("SET statement_timeout = '120s'")
        for nome, ini_s, fim_s, extras in RANGES:
            t0 = time.time()
            ini, fim = date.fromisoformat(ini_s), date.fromisoformat(fim_s)
            rec = {"ini": ini_s, "fim": fim_s, "kpis_atual": _kpis(cur, ini, fim)}
            if extras:
                mtd_ini = date(fim.year, fim.month, 1)  # perdidos_mtd e sempre do mes corrente (como no render)
                rec["listas_len"] = {
                    'leads': len(_fd(cur, q_lista_leads(ini, fim))),
                    'ra':    len(_fd(cur, q_lista_evento('ra', ini, fim))),
                    'rr':    len(_fd(cur, q_lista_evento('rr', ini, fim))),
                    'prop':  len(_fd(cur, q_lista_propostas(ini, fim))),
                    'fech':  len(_fd(cur, q_lista_fechamentos(ini, fim))),
                    'perdidos_mtd': len(_fd(cur, q_lista_perdidos(mtd_ini, fim))),
                }
                src_map = {r['utm_content']: r['utm_source'] for r in _fd(cur, q_source_por_content(ini, fim))}
                rec["rank_source"] = _rank(_fd(cur, q_ranking('utm_source', ini, fim)))
                rec["rank_content"] = _rank(enriquecer_content(_fd(cur, q_ranking('utm_content', ini, fim)), src_map))
            out[nome] = rec
            print(f"  fonte -> {nome:13s} ({ini_s}..{fim_s}) {'+extras' if extras else '       '} {time.time()-t0:5.1f}s", flush=True)

    (ROOT / "paridade_esperado.json").write_text(
        json.dumps(out, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"\nOK -> paridade_esperado.json ({len(RANGES)} intervalos)", flush=True)


if __name__ == "__main__":
    main()
