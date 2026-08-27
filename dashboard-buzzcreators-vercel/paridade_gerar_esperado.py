"""paridade_gerar_esperado.py — Buzzcreators: gera paridade_esperado.json a partir do SQL.

Diferenca vs Cxpress/Buzz BR: aqui NAO existe dashboard local pra servir de referencia — a
Buzzcreators nasceu direto no modelo dinamico-estatico. Entao o gate compara duas implementacoes
independentes da MESMA regra:

    SQL  (queries_buzzcreators.q_kpis_periodo / q_ranking, agregando no Postgres)
      vs
    JS   (motor.js, agregando no navegador sobre o JSON exportado)

Se as duas baterem, o export + a agregacao no browser estao corretos. Se divergirem, ou o JSON
perdeu linha/coluna no caminho, ou a regra foi implementada diferente nos dois lados.

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard-buzzcreators-vercel/paridade_gerar_esperado.py
    node dashboard-buzzcreators-vercel/paridade_check.mjs
"""
from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DASH = ROOT.parent / "dashboard"
sys.path.insert(0, str(DASH))

import psycopg  # noqa: E402

import queries_buzzcreators as Q  # noqa: E402
from exportar_dados import fetch_all, load_url  # noqa: E402

HOJE = date.today()
OUT_PATH = ROOT / "paridade_esperado.json"


def intervalos() -> dict[str, tuple[date, date]]:
    """Mesmos presets do date-picker + um intervalo livre atravessando meses."""
    return {
        "7d": (HOJE - timedelta(days=6), HOJE),
        "30d": (HOJE - timedelta(days=29), HOJE),
        "90d": (HOJE - timedelta(days=89), HOJE),
        "mtd": (HOJE.replace(day=1), HOJE),
        "ytd": (date(HOJE.year, 1, 1), HOJE),
        "livre_mar_mai": (date(2026, 3, 15), date(2026, 5, 20)),
    }


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    url = load_url()
    out: dict[str, dict] = {}

    with psycopg.connect(url, autocommit=True, connect_timeout=60) as conn, conn.cursor() as cur:
        cur.execute("SET statement_timeout = '300s'")
        for nome, (ini, fim) in intervalos().items():
            print(f"  {nome}: {ini} -> {fim}", flush=True)
            kpis = fetch_all(cur, Q.q_kpis_periodo(ini, fim))[0]
            out[nome] = {
                "ini": ini.isoformat(),
                "fim": fim.isoformat(),
                "kpis_atual": {k: int(v) for k, v in kpis.items()},
                "rank_source": [
                    {k: (v if k == "dim" else int(v)) for k, v in r.items()}
                    for r in fetch_all(cur, Q.q_ranking("utm_source", ini, fim))
                ],
                "rank_content": [
                    {k: (v if k == "dim" else int(v)) for k, v in r.items()}
                    for r in fetch_all(cur, Q.q_ranking("utm_content", ini, fim))
                ],
            }

    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nOK -> {OUT_PATH.name} ({len(out)} intervalos)")
    print("Proximo: node dashboard-buzzcreators-vercel/paridade_check.mjs")


if __name__ == "__main__":
    main()
