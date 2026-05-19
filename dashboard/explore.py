"""
Script de exploracao ad-hoc do Supabase Postgres.

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard/explore.py
    uv run --python 3.12 --with "psycopg[binary]" python dashboard/explore.py "SELECT ..."

Sem argumento: lista tabelas e views do schema public.
Com argumento SQL: executa a query (read-only, garantido pelo user looker_readonly no banco).

Le SUPABASE_PG_URL do dashboard/.env.
"""
import os
import sys
from pathlib import Path

import psycopg


def load_env() -> str:
    """Le SUPABASE_PG_URL do dashboard/.env (parser simples, sem dependencia externa)."""
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        raise SystemExit(f"ERRO: {env_path} nao existe.")
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("SUPABASE_PG_URL="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("ERRO: SUPABASE_PG_URL nao encontrado em dashboard/.env")


def list_public_tables(conn: psycopg.Connection) -> None:
    """Lista tabelas e views do schema public com row count estimado."""
    sql = """
        SELECT
            c.relname AS name,
            CASE c.relkind
                WHEN 'r' THEN 'table'
                WHEN 'v' THEN 'view'
                WHEN 'm' THEN 'matview'
                WHEN 'f' THEN 'foreign'
                WHEN 'p' THEN 'partition'
                ELSE c.relkind::text
            END AS kind,
            c.reltuples::bigint AS approx_rows
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = 'public'
          AND c.relkind IN ('r','v','m','f','p')
        ORDER BY kind, name;
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()

    if not rows:
        print("Nenhuma tabela/view encontrada no schema public.")
        return

    name_w = max(len(r[0]) for r in rows)
    kind_w = max(len(r[1]) for r in rows)
    print(f"{'NAME'.ljust(name_w)}  {'KIND'.ljust(kind_w)}  APPROX_ROWS")
    print(f"{'-'*name_w}  {'-'*kind_w}  -----------")
    for name, kind, approx in rows:
        approx_fmt = f"{approx:>11,}" if approx >= 0 else "          ?"
        print(f"{name.ljust(name_w)}  {kind.ljust(kind_w)}  {approx_fmt}")
    print(f"\nTotal: {len(rows)} objetos no schema public.")


def run_query(conn: psycopg.Connection, sql: str) -> None:
    """Executa SQL arbitrario e printa resultado tabular."""
    with conn.cursor() as cur:
        cur.execute(sql)
        if cur.description is None:
            print("(query sem resultado tabular)")
            return
        cols = [d.name for d in cur.description]
        rows = cur.fetchall()

    print("\t".join(cols))
    for row in rows:
        print("\t".join("" if v is None else str(v) for v in row))
    print(f"\n[{len(rows)} linhas]")


def main() -> None:
    url = load_env()
    with psycopg.connect(url, autocommit=True) as conn:
        if len(sys.argv) > 1:
            run_query(conn, sys.argv[1])
        else:
            list_public_tables(conn)


if __name__ == "__main__":
    main()
