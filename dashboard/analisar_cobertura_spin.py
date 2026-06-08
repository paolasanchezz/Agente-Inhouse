"""
Mede cobertura (% preenchimento) dos campos descritivos candidatos a 'dor' e
'funcionalidade que chamou atencao' nos deals FECHADOS de cada unidade.

Roda 3 queries (Buzz BR, Buzz LATAM, Cxpress BR) e printa tabela alinhada.
Read-only.

Uso:
    uv run --python 3.12 --with "psycopg[binary]" python dashboard/analisar_cobertura_spin.py
"""
from pathlib import Path

import psycopg


def load_env() -> str:
    env_path = Path(__file__).parent / ".env"
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("SUPABASE_PG_URL="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("ERRO: SUPABASE_PG_URL nao encontrado.")


# (nome_amigavel, coluna_real, categoria)
# categoria: D=dor, F=funcionalidade/atracao, C=contexto

CAMPOS_BUZZ_BR = [
    ("SPIN Situacao",         "spin_situacao_bd",              "C"),
    ("SPIN Problema",         "spin_problema_bd",              "D"),
    ("SPIN Implicacao",       "spin_implicacao_bd",            "D"),
    ("SPIN Necessidade",      "spin_necessidade_bd",           "F"),
    ("Dores atuais",          "dores_atuais_bd",               "D"),
    ("Principais features",   "principais_features_modulos_bd","F"),
    ("Objetivo Buzzmonitor",  "objetivo_buzzmonitor_bd",       "F"),
    ("BANT Need",             "bant_need_bd",                  "D"),
    ("Canais",                "canais_bd",                     "C"),
    ("Plataforma atual",      "plataforma_atual_bd",           "C"),
    ("Concorrentes (cliente)","concorrentes_bd",               "C"),
    ("Plataformas concorrent","plataformas_concorrentes_bd",   "C"),
    ("Oportunidades futuras", "oportunidades_futuras_bd",      "F"),
    ("Particularidades",      "particularidades_cliente_bd",   "C"),
    ("Description (livre)",   "description",                   "C"),
    ("Motivo perda",          "motivo_perda_bd_sdr",           "D"),
]

CAMPOS_BUZZ_LATAM = [
    ("SPIN Situacao",         "spin_situacion",                "C"),
    ("SPIN Problema",         "spin_problema",                 "D"),
    ("SPIN Implicacao",       "spin_implicacion",              "D"),
    ("SPIN Necessidade",      "spin_necesidad",                "F"),
    ("El problema del lead",  "el_problema_del_lead",          "D"),
    ("Principais features",   "principales_modulos_features",  "F"),
    ("Objetivo del proyecto", "objetivo_del_proyecto",         "F"),
    ("Areas de oportunidad",  "areas_de_oportunidad",          "D"),
    ("Canales",               "canales",                       "C"),
    ("Plataforma actual",     "plataforma_actual",             "C"),
    ("Competidores",          "competidores",                  "C"),
    ("Oportunidades futuras", "oportunidades_futuras",         "F"),
    ("Quien es este cliente", "quien_es_este_cliente",         "C"),
    ("Quien usuario final",   "quien_es_el_usuario_final",     "C"),
    ("El equipo interno",     "existe_un_equipo_interno",      "C"),
    ("Score post-reunion",    "score_post_reunion",            "C"),
    ("Observaciones",         "observaciones",                 "C"),
    ("Description (livre)",   "description",                   "C"),
    ("Transcricao Meet URL",  "transcripcion_de_meet_url",     "C"),
]

CAMPOS_CXPRESS_BR = [
    ("SPIN Situacao",         "spin_situacao",                                                  "C"),
    ("SPIN Problema",         "spin_problema",                                                  "D"),
    ("SPIN Implicacao",       "spin_implicacao",                                                "D"),
    ("SPIN Necessidade",      "spin_necessidade",                                               "F"),
    ("Principal queixa",      "o_que_te_trouxe_ate_aqui_qual_sua_principal_queixa_sdr_bdr",     "D"),
    ("Necessidade do lead",   "necessidade_do_lead",                                            "F"),
    ("Escopo da proposta",    "escopo_da_proposta",                                             "F"),
    ("Canais a integrar",     "canais_a_integrar_no_sistema",                                   "F"),
    ("Prioridade implementac","prioridade_de_implementacao",                                    "F"),
    ("Automacao atendimento", "automacao_no_atendimento",                                       "C"),
    ("Integracao WhatsApp",   "integracao_com_whatsapp_api_off",                                "C"),
    ("Volume atendimentos",   "volume_medio_diario_de_atendimentos",                            "C"),
    ("Area atendida",         "area_que_sera_atendida",                                         "C"),
    ("Plataforma concorrente","plataforma_concorrente",                                         "C"),
    ("Plataforma atual",      "plataforma_atual",                                               "C"),
    ("BANT Needs",            "bant_needs_off",                                                 "D"),
    ("Observacoes",           "observacoes",                                                    "C"),
    ("Qualificacoes adic.",   "qualificacoes_adicionais",                                       "C"),
    ("Description (livre)",   "description",                                                    "C"),
    ("Motivo perda",          "motivo_de_perda_closer_sdr",                                     "D"),
]

WHERE_BUZZ_BR    = "data_fechamento_auto IS NOT NULL"
WHERE_BUZZ_LATAM = "(status = 'Ganho' OR primer_pago_realizado_automatico IS NOT NULL OR fecha_de_inicio_de_contrato IS NOT NULL OR fecha_de_cierre_de_negocio IS NOT NULL)"
WHERE_CXPRESS_BR = "data_do_fechamento_auto IS NOT NULL AND data_do_fechamento_auto <> ''"


def montar_query(tabela: str, where: str, campos: list[tuple[str, str, str]]) -> str:
    selects = ["COUNT(*) AS total_fechados"]
    for _, col, _ in campos:
        selects.append(f"COUNT(*) FILTER (WHERE NULLIF(\"{col}\"::text, '') IS NOT NULL) AS \"{col}\"")
    return f"SELECT {', '.join(selects)} FROM {tabela} WHERE {where}"


def analisar(conn: psycopg.Connection, label: str, tabela: str, where: str, campos: list[tuple[str, str, str]]) -> None:
    sql = montar_query(tabela, where, campos)
    with conn.cursor() as cur:
        cur.execute(sql)
        row = cur.fetchone()
        cols = [d.name for d in cur.description]
    by_col = dict(zip(cols, row))
    total = by_col["total_fechados"]

    print(f"\n=== {label} ({tabela}) — {total} deals fechados ===")
    print(f"  {'NOME':<26} {'COL_REAL':<60} {'CAT':<4} {'PREENCH':>9} {'%':>6}")
    print(f"  {'-'*26} {'-'*60} {'-'*4} {'-'*9} {'-'*6}")
    # ordenar por categoria D > F > C, e dentro por % desc
    enriched = [(nome, col, cat, by_col[col]) for (nome, col, cat) in campos]
    cat_ord = {"D": 0, "F": 1, "C": 2}
    enriched.sort(key=lambda x: (cat_ord[x[2]], -x[3]))
    for nome, col, cat, preench in enriched:
        pct = (preench / total * 100) if total else 0
        print(f"  {nome:<26} {col:<60} {cat:<4} {preench:>9} {pct:>5.1f}%")


def main() -> None:
    url = load_env()
    with psycopg.connect(url, autocommit=True) as conn:
        print("Cobertura de campos descritivos nos deals FECHADOS — categoria: D=dor, F=funcionalidade, C=contexto")
        analisar(conn, "BUZZ BRASIL",   "deals_contratos_prod",          WHERE_BUZZ_BR,    CAMPOS_BUZZ_BR)
        analisar(conn, "BUZZ LATAM",    "deals_latam_contratos_staging", WHERE_BUZZ_LATAM, CAMPOS_BUZZ_LATAM)
        analisar(conn, "CXPRESS BRASIL","cxpress_deals_funil_principal_prod", WHERE_CXPRESS_BR, CAMPOS_CXPRESS_BR)


if __name__ == "__main__":
    main()
