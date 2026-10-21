"""exportar_dados.py — Cxpress: gera dados-cxpress.json para a dashboard dinamica-estatica no Vercel.

Espelha dashboard-buzz-br-vercel/exportar_dados.py, adaptado ao modelo de dados Cxpress:
- Fonte UNICA (cxpress_deals_funil_principal_prod), SEM email/dedup, SEM regra 90d.
- Cada deal traz TODAS as datas do funil na propria linha => exportamos UMA linha por deal
  (no escopo CM) com as 7 datas de etapa ja normalizadas (YYYY-MM-DD ou null). O navegador
  (motor.js) conta cada KPI filtrando pela data da etapa no intervalo escolhido.

A logica CM (filtro_cm calibrado, escopo) continua sendo fonte unica em dashboard/queries_cxpress.py
— aqui so mudamos a PROJECAO: em vez de contar por periodo, listamos as linhas cruas.
A serie de 12m e FIXA (nao depende do range) => pre-computada aqui.

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard-cxpress-vercel/exportar_dados.py
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

# Reusa a lib da dash Cxpress (fonte unica da logica CM).
ROOT = Path(__file__).resolve().parent
DASH = ROOT.parent / "dashboard"
sys.path.insert(0, str(DASH))

import psycopg  # noqa: E402

import queries_cxpress as Q  # noqa: E402
from gerar_relatorio_cxpress import load_url, colher_serie, fetch_all  # noqa: E402

HOJE = date.today()
# Versao do formato deste JSON. Bumpar JUNTO com dashboards-umbrella/contratos/cxpress.json
# quando um campo lido pelo painel for removido, renomeado, mudar de tipo ou de literal.
# Adicionar campo NAO bumpa. validar_contrato.py falha se os dois divergirem.
SCHEMA_VERSION = 1
OUT_PATH = ROOT / "dados-cxpress.json"


def q_deals_raw() -> str:
    """Uma linha por deal no escopo CM, com as 7 datas de etapa normalizadas.

    Reusa o MESMO escopo (_escopo = filtro_inbound AND filtro_cm) das queries da dash local.
    Sem filtro de data na base: o motor.js filtra por data de etapa no intervalo (identico ao
    count(*) FILTER (WHERE data BETWEEN ...) das q_count_kpis/q_ranking, que tambem partem da
    base inteira do escopo). utm_content sai cru (URL-encoded) — o render decodifica (igual a dash).
    """
    esc = Q._escopo("d")
    return f"""
SELECT d.id, d.title AS deal, d.utm_source, {Q._content('d')} AS utm_content,
       {Q.COL_RESP} AS responsavel,
       {Q.COL_VALOR} AS valor_text, d.currency,
       d.status, d.motivo_de_perda_closer_sdr AS motivo, d.etapa_do_lost AS etapa,
       d.{Q.COL_LEAD}::date AS d_lead,
       {Q._d('d.' + Q.COL_TRIAGEM)} AS d_triagem,
       {Q._d('d.' + Q.COL_AGENDAMENTO)} AS d_agendamento,
       {Q._d('d.' + Q.COL_DEMO)} AS d_demo,
       {Q._d('d.' + Q.COL_PROPOSTA)} AS d_proposta,
       {Q._d('d.' + Q.COL_FECHAMENTO)} AS d_fechamento,
       {Q._d('d.' + Q.COL_LOST)} AS d_lost
FROM {Q.TABELA} d
WHERE {esc}
"""


def _jsonify(r: dict) -> dict:
    """dates -> ISO 'YYYY-MM-DD'; o resto passa (o json.dumps default=str cobre Decimal)."""
    return {k: (v.isoformat() if isinstance(v, date) else v) for k, v in r.items()}


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print(f"Exportando dados CM Cxpress {date(2026, 1, 1)} -> {HOJE} ...", flush=True)
    url = load_url()

    with psycopg.connect(url, autocommit=True) as conn, conn.cursor() as cur:
        cur.execute("SET statement_timeout = '300s'")
        print("  [1/2] deals (escopo CM, todas as datas)...", flush=True)
        deals = fetch_all(cur, q_deals_raw())
        print("  [2/2] serie 12m...", flush=True)
        serie = colher_serie(cur, HOJE)

    out = {
        "schema_version": SCHEMA_VERSION,
        "gerado_em": HOJE.isoformat(),
        "escopo": {"ini": date(2026, 1, 1).isoformat(), "fim": HOJE.isoformat()},
        "deals": [_jsonify(r) for r in deals],
        "serie": serie,
    }

    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, default=str), encoding="utf-8")

    size = OUT_PATH.stat().st_size
    print("\n" + "=" * 56)
    print("EXPORT OK ->", OUT_PATH.name)
    print("=" * 56)
    print(f"  deals   : {len(deals):>6d} linhas")
    print(f"  serie   : {len(serie.get('labels', []))} semanas")
    print(f"  tamanho : {size / 1024:.1f} KB  ({size / 1024 / 1024:.2f} MB)")
    print("=" * 56)


if __name__ == "__main__":
    main()
