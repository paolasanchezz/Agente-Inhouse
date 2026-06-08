"""
Exporta deals FECHADOS com pelo menos 1 campo de dor OU funcionalidade preenchido,
separados por unidade de negocio, em 3 CSVs com colunas semanticamente rotuladas
(dor_*, feature_*, contexto basico).

Estrutura comum:
  Identificacao: id, title, data_fechamento, valor, currency, bd, sdr, link_ac
  Atribuicao:    utm_source, utm_content + (email | contact | pais)
  DOR (cada fonte = coluna separada):
    dor_* (campos rotulados como dor + SPIN problema/implicacao)
  FEATURE (cada fonte = coluna separada):
    feature_* (campos rotulados como features + objetivo + SPIN necessidade)
  CONTEXTO:
    plataforma_atual, concorrentes, canais, etc

Saída: conhecimento/clientes-fechados/
  - dor-features-buzzmonitor-brasil.csv
  - dor-features-buzzmonitor-latam.csv
  - dor-features-cxpress-brasil.csv

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard/exportar_dor_features.py

Apos rodar, atualizar a data em conhecimento/clientes-fechados/README.md (campo
'Ultima atualizacao'). Recomendado a cada 2 meses para manter relevancia das
dores e features capturadas em vendas recentes.
"""
import csv
from pathlib import Path

import psycopg


def load_env() -> str:
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


QUERY_BUZZ_BR = """
SELECT
    id,
    title,
    data_fechamento_auto::date AS data_fechamento,
    value AS valor,
    currency,
    email_contato_principal_bd_sdr AS email,
    utm_source,
    utm_content,
    bd_auto AS bd,
    sdr_responsavel AS sdr,
    -- DOR
    NULLIF(dores_atuais_bd, '')      AS dor_dores_atuais,
    NULLIF(spin_problema_bd, '')     AS dor_spin_problema,
    NULLIF(spin_implicacao_bd, '')   AS dor_spin_implicacao,
    NULLIF(bant_need_bd, '')         AS dor_bant_need,
    -- FEATURE
    NULLIF(principais_features_modulos_bd, '') AS feature_principais_modulos,
    NULLIF(objetivo_buzzmonitor_bd, '')        AS feature_objetivo,
    NULLIF(spin_necessidade_bd, '')            AS feature_spin_necessidade,
    -- CONTEXTO
    NULLIF(plataforma_atual_bd, '')         AS plataforma_atual,
    NULLIF(plataformas_concorrentes_bd, '') AS concorrentes_avaliados,
    NULLIF(canais_bd, '')                   AS canais,
    NULLIF(particularidades_cliente_bd, '') AS particularidades,
    'https://elifebrasil.activehosted.com/app/deals/' || id AS link_ac
FROM deals_contratos_prod
WHERE data_fechamento_auto IS NOT NULL
  AND (
       NULLIF(dores_atuais_bd, '')               IS NOT NULL
    OR NULLIF(spin_problema_bd, '')              IS NOT NULL
    OR NULLIF(spin_implicacao_bd, '')            IS NOT NULL
    OR NULLIF(bant_need_bd, '')                  IS NOT NULL
    OR NULLIF(principais_features_modulos_bd, '') IS NOT NULL
    OR NULLIF(objetivo_buzzmonitor_bd, '')       IS NOT NULL
    OR NULLIF(spin_necessidade_bd, '')           IS NOT NULL
  )
ORDER BY data_fechamento DESC, id DESC
"""

QUERY_BUZZ_LATAM = """
SELECT
    id,
    title,
    COALESCE(
        fecha_de_cierre_de_negocio::date,
        fecha_de_inicio_de_contrato::date,
        fecha_de_primer_pago_automatico::date
    ) AS data_fechamento,
    value AS valor,
    currency,
    pais,
    status,
    utm_source,
    utm_content,
    closer AS bd,
    sdr,
    -- DOR
    NULLIF(areas_de_oportunidad, '')  AS dor_areas_oportunidade,
    NULLIF(el_problema_del_lead, '')  AS dor_problema_lead,
    NULLIF(spin_problema, '')         AS dor_spin_problema,
    NULLIF(spin_implicacion, '')      AS dor_spin_implicacao,
    -- FEATURE
    NULLIF(principales_modulos_features, '') AS feature_principais_modulos,
    NULLIF(objetivo_del_proyecto, '')        AS feature_objetivo,
    NULLIF(oportunidades_futuras, '')        AS feature_oportunidades_futuras,
    NULLIF(spin_necesidad, '')               AS feature_spin_necessidade,
    -- CONTEXTO
    NULLIF(plataforma_actual, '')      AS plataforma_atual,
    NULLIF(competidores, '')           AS concorrentes_avaliados,
    NULLIF(canales, '')                AS canais,
    NULLIF(quien_es_este_cliente, '')  AS quem_e_o_cliente,
    NULLIF(description, '')            AS description,
    NULLIF(observaciones, '')          AS observacoes,
    'https://elifeeurope.activehosted.com/app/deals/' || id AS link_ac
FROM deals_latam_contratos_staging
WHERE (
       status = 'Ganho'
    OR primer_pago_realizado_automatico IS NOT NULL
    OR fecha_de_inicio_de_contrato      IS NOT NULL
    OR fecha_de_cierre_de_negocio       IS NOT NULL
  )
  AND (
       NULLIF(areas_de_oportunidad, '')          IS NOT NULL
    OR NULLIF(el_problema_del_lead, '')          IS NOT NULL
    OR NULLIF(spin_problema, '')                 IS NOT NULL
    OR NULLIF(spin_implicacion, '')              IS NOT NULL
    OR NULLIF(principales_modulos_features, '')  IS NOT NULL
    OR NULLIF(objetivo_del_proyecto, '')         IS NOT NULL
    OR NULLIF(oportunidades_futuras, '')         IS NOT NULL
    OR NULLIF(spin_necesidad, '')                IS NOT NULL
  )
ORDER BY data_fechamento DESC NULLS LAST, id DESC
"""

QUERY_CXPRESS_BR = """
SELECT
    id,
    title,
    LEFT(data_do_fechamento_auto, 10) AS data_fechamento,
    COALESCE(NULLIF(valor_atualizado_do_fee, ''), NULLIF(cxpress_fee_mensal, '')) AS valor_fee,
    currency,
    contact,
    utm_source,
    utm_content,
    closer_bd_auto AS bd,
    sdr_bdr_auto   AS sdr,
    -- DOR
    NULLIF(o_que_te_trouxe_ate_aqui_qual_sua_principal_queixa_sdr_bdr, '') AS dor_principal_queixa,
    NULLIF(bant_needs_off, '')        AS dor_bant_needs,
    NULLIF(spin_problema, '')         AS dor_spin_problema,
    NULLIF(spin_implicacao, '')       AS dor_spin_implicacao,
    -- FEATURE
    NULLIF(canais_a_integrar_no_sistema, '') AS feature_canais_a_integrar,
    NULLIF(necessidade_do_lead, '')          AS feature_necessidade_lead,
    NULLIF(prioridade_de_implementacao, '')  AS feature_prioridade_implementacao,
    NULLIF(spin_necessidade, '')             AS feature_spin_necessidade,
    -- CONTEXTO
    NULLIF(area_que_sera_atendida, '')               AS area_atendida,
    NULLIF(volume_medio_diario_de_atendimentos, '')  AS volume_atendimentos,
    NULLIF(qualificacoes_adicionais, '')             AS qualificacoes_adicionais,
    NULLIF(automacao_no_atendimento, '')             AS automacao_atendimento_atual,
    NULLIF(plataforma_concorrente, '')               AS concorrente_avaliado,
    'https://cxpress.activehosted.com/app/deals/' || id AS link_ac
FROM cxpress_deals_funil_principal_prod
WHERE data_do_fechamento_auto IS NOT NULL
  AND data_do_fechamento_auto <> ''
  AND (
       NULLIF(o_que_te_trouxe_ate_aqui_qual_sua_principal_queixa_sdr_bdr, '') IS NOT NULL
    OR NULLIF(bant_needs_off, '')               IS NOT NULL
    OR NULLIF(spin_problema, '')                IS NOT NULL
    OR NULLIF(spin_implicacao, '')              IS NOT NULL
    OR NULLIF(canais_a_integrar_no_sistema, '') IS NOT NULL
    OR NULLIF(necessidade_do_lead, '')          IS NOT NULL
    OR NULLIF(prioridade_de_implementacao, '')  IS NOT NULL
    OR NULLIF(spin_necessidade, '')             IS NOT NULL
  )
ORDER BY data_fechamento DESC NULLS LAST, id DESC
"""


def exportar(conn: psycopg.Connection, query: str, out_path: Path, label: str) -> int:
    with conn.cursor() as cur:
        cur.execute(query)
        cols = [d.name for d in cur.description]
        rows = cur.fetchall()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        writer.writerow(cols)
        for row in rows:
            writer.writerow(["" if v is None else str(v) for v in row])

    print(f"  {label}: {len(rows)} linhas -> {out_path.relative_to(Path(__file__).parent.parent)}")
    return len(rows)


def main() -> None:
    url = load_env()
    out_dir = Path(__file__).parent.parent / "conhecimento" / "clientes-fechados"

    print("Conectando ao Supabase (looker_readonly)...")
    with psycopg.connect(url, autocommit=True) as conn:
        print("Exportando deals fechados com dor OU feature preenchidos:")
        total = 0
        total += exportar(conn, QUERY_BUZZ_BR,    out_dir / "dor-features-buzzmonitor-brasil.csv", "Buzz BR    ")
        total += exportar(conn, QUERY_BUZZ_LATAM, out_dir / "dor-features-buzzmonitor-latam.csv",  "Buzz LATAM ")
        total += exportar(conn, QUERY_CXPRESS_BR, out_dir / "dor-features-cxpress-brasil.csv",     "Cxpress BR ")
        print(f"\nTotal geral: {total} deals fechados com dor ou feature preenchidos.")


if __name__ == "__main__":
    main()
