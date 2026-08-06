"""exportar_dados.py — Passo 1 do PLANO-VERCEL.

Gera dados-2026.json com TODOS os eventos CM do ano (sem dedup de periodo),
pra o navegador filtrar/agregar por intervalo arbitrario sem tocar no banco.

REUSA os predicados de dashboard-pessoal/lib/queries.py (filtro CM, regra 90d,
CTE de conversoes, whitelist/blacklist) — a logica CM continua sendo fonte unica
no Python. Aqui so mudamos a PROJECAO: em vez de contar/dedupar, listamos as
linhas cruas com data + dimensoes; a dedup por email passa a ser feita no
navegador DENTRO do range selecionado (senao divergiria em sub-periodos).

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard-buzz-br-vercel/exportar_dados.py
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date
from pathlib import Path

# Reusa a lib da dash local (fonte unica da logica CM).
ROOT = Path(__file__).resolve().parent
LOCAL = ROOT.parent / "dashboard-pessoal"
sys.path.insert(0, str(LOCAL))

import psycopg  # noqa: E402

from lib.queries import (  # noqa: E402
    EMAIL_BLACKLIST, EMAIL_WHITELIST, COLUNA_EVENTO,
    filtro_cm, filtro_inbound, _sem_outbound, _atrib_cm_90d, cte_conversoes_cm,
    predicado_evento, predicado_fechamento, _sql_email_list, _cdate_efetivo, fonte_deals_funil,
    q_serie_temporal_12m, q_proporcao_sources_12m,
)
from lib.render import serie_temporal_12m, proporcao_sources, jsonify  # noqa: E402

ANO_INI = date(2026, 1, 1)
HOJE = date.today()
FIM = HOJE
OUT_PATH = ROOT / "dados-2026.json"


# ---------- conexao ----------

def load_url() -> str:
    if os.environ.get("SUPABASE_PG_URL"):
        return os.environ["SUPABASE_PG_URL"]
    for env_path in (LOCAL / ".env", ROOT.parent / "Agente Inhouse" / "dashboard" / ".env",
                     Path.cwd() / "dashboard" / ".env"):
        if env_path.exists():
            for raw in env_path.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if line.startswith("SUPABASE_PG_URL="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("ERRO: SUPABASE_PG_URL nao encontrado (env, dashboard-pessoal/.env ou dashboard/.env)")


def fetch_dict(cur, sql: str) -> list[dict]:
    cur.execute(sql)
    cols = [d.name for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


# ---------- queries RAW (ano todo, sem dedup) ----------
# Espelham as q_lista_* de lib/queries.py, reusando os MESMOS predicados,
# mas sem DISTINCT ON e sem restricao a um periodo curto.

def q_leads_raw(ini: date, fim: date) -> str:
    f = filtro_cm("d")
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    cde = _cdate_efetivo("d.id", "d.cdate")
    return f"""
WITH wl AS ({wl}), bl AS ({bl})
SELECT d.id, d.title AS deal, d.email_contato_principal_bd_sdr AS email,
       d.utm_source, d.utm_content,
       d.sdr_sdr AS bd,
       {cde}::date AS data, {cde} AS ts,
       d.cdate::date AS cdate_cru
FROM {fonte_deals_funil()} d
WHERE {cde}::date BETWEEN '{ini}' AND '{fim}'
  AND d.email_contato_principal_bd_sdr IS NOT NULL
  AND lower(trim(d.email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
  AND (lower(trim(d.email_contato_principal_bd_sdr)) IN (SELECT email FROM wl) OR {f})
  AND {_sem_outbound('d')}
"""


def q_evento_raw(kpi: str, ini: date, fim: date) -> str:
    """ce / ra / rr / prop — eventos comerciais com regra 90d (sem dedup: count(*) nao dedupa)."""
    col = COLUNA_EVENTO[kpi]
    cte = cte_conversoes_cm(ini)
    extra = ""
    if kpi == "ra":
        extra = ", d.data_inicio_reuniao_realizada::date AS data_realizada"
    elif kpi == "rr":
        extra = ", d.data_envio_proposta_auto::date AS data_proposta"
    elif kpi == "prop":
        extra = ", d.value AS valor_text, d.currency"
    return f"""
{cte}
SELECT d.id, d.title AS deal,
       COALESCE(d.bd_auto, d.sdr_sdr) AS bd,
       d.utm_source, d.utm_content,
       d.{col}::date AS data{extra}
FROM {fonte_deals_funil()} d
WHERE d.{col}::date BETWEEN '{ini}' AND '{fim}'
  AND {predicado_evento(col, "d")}
"""


def q_fech_raw(ini: date, fim: date) -> str:
    cte = cte_conversoes_cm(ini)
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    return f"""
{cte},
wl AS ({wl}), bl AS ({bl})
SELECT ct.id, ct.title AS deal,
       COALESCE(ct.bd_auto, ct.sdr_sdr) AS bd,
       ct.utm_source, ct.utm_content,
       ct.data_fechamento_auto::date AS data,
       ct.value AS valor, ct.currency,
       ct.email_contato_principal_bd_sdr AS email
FROM deals_contratos_prod ct
WHERE ct.data_fechamento_auto::date BETWEEN '{ini}' AND '{fim}'
  AND {predicado_fechamento("ct")}
"""


def q_perdidos_raw(ini: date, fim: date) -> str:
    """Coorte: leads CM criados no ano E perdidos. Sem dedup (navegador dedupa por email no range)."""
    f = filtro_cm("d")
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    return f"""
WITH wl AS ({wl}), bl AS ({bl})
SELECT d.id, d.title AS deal, d.email_contato_principal_bd_sdr AS email,
       d.utm_source, d.utm_content,
       COALESCE(d.data_efetividade_contato_auto::date, d.cdate::date) AS ultima_conversao,
       d.motivo_perda_bd_sdr AS motivo,
       d.data_negocio_perdido_auto::date AS data_perda,
       d.cdate::date AS cdate
FROM deals_comercial_prod d
WHERE d.cdate::date BETWEEN '{ini}' AND '{fim}'
  AND d.email_contato_principal_bd_sdr IS NOT NULL
  AND d.data_negocio_perdido_auto IS NOT NULL
  AND d.motivo_perda_bd_sdr IS NOT NULL
  AND lower(trim(d.email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
  AND (lower(trim(d.email_contato_principal_bd_sdr)) IN (SELECT email FROM wl) OR {f})
  AND {_sem_outbound('d')}
"""


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print(f"Exportando dados CM {ANO_INI} -> {FIM} ...", flush=True)
    url = load_url()

    with psycopg.connect(url, autocommit=True) as conn, conn.cursor() as cur:
        cur.execute("SET statement_timeout = '120s'")
        print("  [1/9] leads...", flush=True)
        leads = fetch_dict(cur, q_leads_raw(ANO_INI, FIM))
        print("  [2/9] ce...", flush=True)
        ce = fetch_dict(cur, q_evento_raw("ce", ANO_INI, FIM))
        print("  [3/9] ra...", flush=True)
        ra = fetch_dict(cur, q_evento_raw("ra", ANO_INI, FIM))
        print("  [4/9] rr...", flush=True)
        rr = fetch_dict(cur, q_evento_raw("rr", ANO_INI, FIM))
        print("  [5/9] prop...", flush=True)
        prop = fetch_dict(cur, q_evento_raw("prop", ANO_INI, FIM))
        print("  [6/9] fech...", flush=True)
        fech = fetch_dict(cur, q_fech_raw(ANO_INI, FIM))
        print("  [7/9] perdidos...", flush=True)
        perdidos = fetch_dict(cur, q_perdidos_raw(ANO_INI, FIM))
        print("  [8/9] serie 12m...", flush=True)
        serie = serie_temporal_12m(fetch_dict(cur, q_serie_temporal_12m(HOJE)), HOJE)
        print("  [9/9] proporcao sources...", flush=True)
        prop_src = proporcao_sources(fetch_dict(cur, q_proporcao_sources_12m(HOJE)))

    out = {
        "gerado_em": HOJE.isoformat(),
        "escopo": {"ini": ANO_INI.isoformat(), "fim": FIM.isoformat()},
        "leads": jsonify(leads),
        "ce": jsonify(ce),
        "ra": jsonify(ra),
        "rr": jsonify(rr),
        "prop": jsonify(prop),
        "fech": jsonify(fech),
        "perdidos": jsonify(perdidos),
        "serie_12m": serie,
        "proporcao_sources": prop_src,
    }

    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, default=str), encoding="utf-8")

    size = OUT_PATH.stat().st_size
    print("\n" + "=" * 56)
    print("EXPORT OK ->", OUT_PATH.name)
    print("=" * 56)
    for k in ("leads", "ce", "ra", "rr", "prop", "fech", "perdidos"):
        print(f"  {k:10s}: {len(out[k]):>6d} linhas")
    print(f"  serie_12m : {len(serie.get('labels', []))} semanas")
    print(f"  tamanho   : {size/1024:.1f} KB  ({size/1024/1024:.2f} MB)")
    print("=" * 56)


if __name__ == "__main__":
    main()
