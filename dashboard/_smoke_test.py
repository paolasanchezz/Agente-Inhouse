"""Smoke test: valida que a query de Fechamentos YtD 2026 retorna 6 deals = R$ 16.580 (§7 do MAPEAMENTO).

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard/_smoke_test.py
    uv run --python 3.12 --with "psycopg[binary]" python dashboard/_smoke_test.py --ate 2026-05-18
"""
from __future__ import annotations

import sys
import argparse
from datetime import date
from pathlib import Path

import psycopg

# permitir import relativo
sys.path.insert(0, str(Path(__file__).parent))
from datas import calcular_periodos
from queries import q_lista_fechamentos, q_count_fechamentos


def load_url() -> str:
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        raise SystemExit(f"ERRO: {env_path} nao existe.")
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("SUPABASE_PG_URL="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("ERRO: SUPABASE_PG_URL nao encontrado em dashboard/.env")


def fetch_dict(cur, sql: str) -> list[dict]:
    cur.execute(sql)
    cols = [d.name for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ate", type=str, default=None, help="YYYY-MM-DD (default = hoje)")
    args = parser.parse_args()

    ate = date.fromisoformat(args.ate) if args.ate else None
    periodos = calcular_periodos(ate)

    print("=" * 70)
    print(f"SMOKE TEST — Fechamentos YtD CM")
    print("=" * 70)
    print(f"Hoje:          {periodos['hoje']}")
    print(f"YtD periodo:   {periodos['ytd_ini']} -> {periodos['ytd_fim']}")
    print()

    url = load_url()
    with psycopg.connect(url, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("SET LOCAL statement_timeout = '120s'")

            # Count
            cur.execute(q_count_fechamentos(periodos['ytd_ini'], periodos['ytd_fim']))
            n_count = cur.fetchone()[0]
            print(f"COUNT fechamentos YtD: {n_count}")
            print()

            # Lista detalhada
            rows = fetch_dict(cur, q_lista_fechamentos(periodos['ytd_ini'], periodos['ytd_fim']))
            print(f"LISTA detalhada ({len(rows)} deals):")
            soma = 0.0
            for r in rows:
                valor = float(r.get('valor') or 0)
                soma += valor
                print(
                    f"  [{r['id']}] {r['deal'][:50]:50}  "
                    f"{(r.get('utm_source') or '(vazio)'):20}  "
                    f"R$ {valor:>10,.2f}  "
                    f"{r['data_evento']}"
                )
            print()
            print(f"Total: R$ {soma:,.2f}")
            print()

            # Validacao formal (§7 do MAPEAMENTO-CAMPOS.md)
            esperado_count = 6
            esperado_total = 16580.0
            erros = []
            if n_count != esperado_count:
                erros.append(f"COUNT esperado {esperado_count}, obtido {n_count}")
            if abs(soma - esperado_total) > 1.0:
                erros.append(f"TOTAL esperado R$ {esperado_total:,.2f}, obtido R$ {soma:,.2f}")

            if erros:
                print("FALHA:")
                for e in erros:
                    print(f"  - {e}")
                sys.exit(1)
            else:
                print(f"OK — {esperado_count} fechamentos / R$ {esperado_total:,.2f} confirmados.")


if __name__ == "__main__":
    main()
