"""paridade_gerar_esperado.py — LATAM: roda a dash LOCAL (queries_latam, fonte da verdade)
e salva paridade_esperado.json pro paridade_check.mjs comparar o motor.js numero a numero.

Usa as MESMAS SQLs da dashboard-latam. KPIs (leads/pc/reunion/cierre/perd) em varios
intervalos; listas + rankings so no YtD.

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard-latam-vercel/paridade_gerar_esperado.py
"""
from __future__ import annotations

import json
import sys
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DASH = ROOT.parent / "dashboard"
sys.path.insert(0, str(DASH))

import psycopg  # noqa: E402
from gerar_relatorio_latam import load_url, fetch_one, fetch_all  # noqa: E402
from queries_latam import (  # noqa: E402
    q_count_kpis, q_count_fechamentos, q_count_perdidos,
    q_lista_leads, q_lista_reuniones, q_lista_fechamentos,
    q_ranking,
)

RANGES = [
    ("um_dia",       "2026-06-02", "2026-06-02", False),
    ("cross_month",  "2026-04-15", "2026-05-15", False),
    ("maio_inteiro", "2026-05-01", "2026-05-31", False),
    ("ytd",          "2026-01-01", "2026-07-07", True),
]

_KPIS = ('leads', 'pc', 'reunion', 'cierre', 'perd')


def _kpis(cur, ini, fim):
    k = fetch_one(cur, q_count_kpis(ini, fim))
    f = fetch_one(cur, q_count_fechamentos(ini, fim))
    p = fetch_one(cur, q_count_perdidos(ini, fim))
    return {
        'leads': int(k.get('leads', 0) or 0),
        'pc': int(k.get('ce', 0) or 0),
        'reunion': int(k.get('reunion', 0) or 0),
        'cierre': int(f.get('fech', 0) or 0),
        'perd': int(p.get('perd', 0) or 0),
    }


def _rank(rows):
    return [{"dim": r.get("dim"), "leads": r.get("leads", 0), "pc": r.get("pc", 0),
             "reunion": r.get("reunion", 0), "cierre": r.get("cierre", 0)} for r in rows]


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    out = {}
    url = load_url()
    with psycopg.connect(url, autocommit=True, connect_timeout=20) as conn, conn.cursor() as cur:
        cur.execute("SET statement_timeout = '300s'")
        for nome, ini_s, fim_s, extras in RANGES:
            t0 = time.time()
            ini, fim = date.fromisoformat(ini_s), date.fromisoformat(fim_s)
            rec = {"ini": ini_s, "fim": fim_s, "kpis_atual": _kpis(cur, ini, fim)}
            if extras:
                rec["listas_len"] = {
                    'leads': len(fetch_all(cur, q_lista_leads(ini, fim))),
                    'reuniones': len(fetch_all(cur, q_lista_reuniones(ini, fim))),
                    'cierres': len(fetch_all(cur, q_lista_fechamentos(ini, fim))),
                }
                rec["rank_source"] = _rank(fetch_all(cur, q_ranking('utm_source', ini, fim)))
                rec["rank_content"] = _rank(fetch_all(cur, q_ranking('utm_content', ini, fim)))
            out[nome] = rec
            print(f"  fonte -> {nome:13s} ({ini_s}..{fim_s}) {'+extras' if extras else '       '} {time.time()-t0:5.1f}s", flush=True)

    (ROOT / "paridade_esperado.json").write_text(
        json.dumps(out, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"\nOK -> paridade_esperado.json ({len(RANGES)} intervalos)", flush=True)


if __name__ == "__main__":
    main()
