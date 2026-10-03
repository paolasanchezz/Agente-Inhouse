"""exportar_dados.py — LATAM: gera dados-latam.json para a dashboard dinamica-estatica no Vercel.

Espelha dashboard-buzz-br-vercel/exportar_dados.py, adaptado ao modelo LATAM:
- Leads: deals_latam_inbound_staging UNION outbound (dedup por id via _leads_subquery), filtro CM.
  Cada lead traz as datas do funil (cdate, primer contacto, reunion) + mdate + status na propria linha.
- Fechamentos: tabela SEPARADA deals_latam_contratos_staging (FECHADO_LATAM + filtro CM), com
  DATA_FECHO + valor USD. Por isso exportamos DOIS arrays: leads[] e fech[].
- Sem regra 90d, sem dedup por pessoa (LATAM nao tem account_id/contato).

A logica CM (filtro_cm_latam, FECHADO_LATAM, escopo) continua fonte unica em queries_latam.py.
A serie de 12m e FIXA => pre-computada aqui.

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard-latam-vercel/exportar_dados.py
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DASH = ROOT.parent / "dashboard"
sys.path.insert(0, str(DASH))

import psycopg  # noqa: E402

import queries_latam as Q  # noqa: E402
from gerar_relatorio_latam import load_url, colher_serie, fetch_all  # noqa: E402

HOJE = date.today()
OUT_PATH = ROOT / "dados-latam.json"


def q_leads_raw() -> str:
    """Leads CM (inbound∪outbound dedup por id) com as datas do funil na propria linha."""
    f = Q.filtro_cm_latam("d")
    pais = Q.PAIS_NORM.replace("pais", "d.pais")
    # url_conversao NAO entra no JSON: ja foi consumido pelo filtro CM (aplicado aqui) e
    # nao aparece em nenhuma lista/ranking/motor — mante-lo so incharia o arquivo (URLs longas).
    return f"""
SELECT d.id, d.title AS deal, d.utm_source, d.utm_content,
       {pais} AS pais,
       COALESCE(NULLIF(TRIM(d.sdr),''), NULLIF(TRIM(d.closer),'')) AS responsable,
       d.cdate::date AS d_lead,
       COALESCE(d.fecha_de_primer_contacto, d.fecha_y_hora_de_primer_contacto::date) AS d_ce,
       d.fecha_de_reunion AS d_reunion,
       d.mdate::date AS d_mdate,
       d.status,
       NULLIF(TRIM(d.motivos_de_perdida), '') AS motivo
FROM {Q._leads_subquery()} d
WHERE {f}
"""


def q_fech_raw() -> str:
    """Fechamentos CM (tabela contratos separada) — FECHADO_LATAM + filtro CM, valor USD."""
    f = Q.filtro_cm_latam("")
    return f"""
SELECT id, title AS deal, utm_source, utm_content,
       {Q.PAIS_NORM} AS pais,
       COALESCE(NULLIF(TRIM(closer),''), NULLIF(TRIM(sdr),'')) AS responsable,
       {Q.VALOR_USD} AS valor, currency,
       {Q.DATA_FECHO} AS d_fech
FROM deals_latam_contratos_staging
WHERE {Q.FECHADO_LATAM}
  AND {f}
"""


def _jsonify(r: dict) -> dict:
    out = {}
    for k, v in r.items():
        if isinstance(v, date):
            out[k] = v.isoformat()
        elif v is not None and not isinstance(v, (str, int, float, bool)):
            out[k] = float(v)  # numeric (valor USD) -> float
        else:
            out[k] = v
    return out


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print(f"Exportando dados CM LATAM -> {HOJE} ...", flush=True)
    url = load_url()

    with psycopg.connect(url, autocommit=True) as conn, conn.cursor() as cur:
        cur.execute("SET statement_timeout = '300s'")
        print("  [1/3] leads (inbound∪outbound, escopo CM)...", flush=True)
        leads = fetch_all(cur, q_leads_raw())
        print("  [2/3] fechamentos (contratos)...", flush=True)
        fech = fetch_all(cur, q_fech_raw())
        print("  [3/3] serie 12m...", flush=True)
        serie = colher_serie(cur, HOJE)

    out = {
        "gerado_em": HOJE.isoformat(),
        "escopo": {"ini": date(2026, 1, 1).isoformat(), "fim": HOJE.isoformat()},
        "leads": [_jsonify(r) for r in leads],
        "fech": [_jsonify(r) for r in fech],
        "serie": serie,
    }

    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, default=str), encoding="utf-8")

    size = OUT_PATH.stat().st_size
    print("\n" + "=" * 56)
    print("EXPORT OK ->", OUT_PATH.name)
    print("=" * 56)
    print(f"  leads   : {len(leads):>6d} linhas")
    print(f"  fech    : {len(fech):>6d} linhas")
    print(f"  serie   : {len(serie.get('labels', []))} semanas")
    print(f"  tamanho : {size / 1024:.1f} KB  ({size / 1024 / 1024:.2f} MB)")
    print("=" * 56)


if __name__ == "__main__":
    main()
