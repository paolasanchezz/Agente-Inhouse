"""exportar_dados.py — Buzzcreators: gera dados-buzzcreators.json para a dashboard no Vercel.

Espelha dashboard-cxpress-vercel/exportar_dados.py. Fonte da logica CM (whitelist de utm_source,
join de atribuicao deal->contato, datas de etapa) e UNICA: dashboard/queries_buzzcreators.py.
Aqui so muda a PROJECAO: em vez de contar por periodo, listamos as linhas cruas e o navegador
(motor.js) agrega no intervalo escolhido.

A serie de 12m e FIXA (nao depende do range) => pre-computada aqui.

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard-buzzcreators-vercel/exportar_dados.py
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

HOJE = date.today()
OUT_PATH = ROOT / "dados-buzzcreators.json"
ENV_PATH = DASH / ".env"

METRICAS_SERIE = ("leads", "agendamento", "reuniao", "fechamento")


def load_url() -> str:
    """Le SUPABASE_PG_URL de dashboard/.env (mesma convencao das outras dashboards)."""
    for linha in ENV_PATH.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if linha.startswith("SUPABASE_PG_URL="):
            return linha.split("=", 1)[1].strip()
    raise SystemExit(f"ERRO: SUPABASE_PG_URL nao encontrado em {ENV_PATH}")


def fetch_all(cur, sql: str) -> list[dict]:
    cur.execute(sql)
    cols = [c.name for c in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def colher_serie(cur, hoje: date) -> dict:
    """52 semanas fechadas na segunda-feira (identico ao colher_serie das outras dashs)."""
    raw = fetch_all(cur, Q.q_serie_12m(hoje))
    segunda = hoje - timedelta(days=hoje.weekday())
    semanas = [segunda - timedelta(weeks=51 - i) for i in range(52)]
    counts = {(r["semana"], r["metrica"]): int(r["n"]) for r in raw}
    return {
        "labels": [f"{s.day:02d}/{s.month:02d}" for s in semanas],
        **{m: [counts.get((s, m), 0) for s in semanas] for m in METRICAS_SERIE},
    }


def _jsonify(r: dict) -> dict:
    """dates -> ISO 'YYYY-MM-DD'; Decimal e coberto pelo default=str do json.dumps."""
    return {k: (v.isoformat() if isinstance(v, date) else v) for k, v in r.items()}


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print(f"Exportando dados CM Buzzcreators -> {HOJE} ...", flush=True)
    url = load_url()

    with psycopg.connect(url, autocommit=True, connect_timeout=60) as conn, conn.cursor() as cur:
        cur.execute("SET statement_timeout = '300s'")
        print("  [1/3] deals (escopo CM, atribuicao recuperada)...", flush=True)
        deals = fetch_all(cur, Q.q_deals_raw())
        print("  [2/3] serie 12m...", flush=True)
        serie = colher_serie(cur, HOJE)
        print("  [3/3] cobertura da atribuicao...", flush=True)
        cobertura = fetch_all(cur, Q.q_cobertura())[0]

    out = {
        "gerado_em": HOJE.isoformat(),
        "escopo": {"ini": date(2026, 1, 1).isoformat(), "fim": HOJE.isoformat()},
        "cobertura": {k: int(v) for k, v in cobertura.items()},
        "deals": [_jsonify(r) for r in deals],
        "serie": serie,
    }

    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, default=str), encoding="utf-8")

    size = OUT_PATH.stat().st_size
    print("\n" + "=" * 56)
    print("EXPORT OK ->", OUT_PATH.name)
    print("=" * 56)
    print(f"  deals CM  : {len(deals):>6d} linhas")
    print(f"  cobertura : {cobertura['com_source']}/{cobertura['deals_total']} deals com atribuicao "
          f"· {cobertura['no_escopo_cm']} no escopo CM")
    print(f"  serie     : {len(serie.get('labels', []))} semanas")
    print(f"  tamanho   : {size / 1024:.1f} KB  ({size / 1024 / 1024:.2f} MB)")
    print("=" * 56)


if __name__ == "__main__":
    main()
