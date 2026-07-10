"""queries_latam.py — queries SQL para a dashboard de Content Marketing **LATAM**.

Espelha a especificacao em dashboard/MAPEAMENTO-CAMPOS-latam.md.

Diferencas vs Brasil (queries.py):
- Fonte: deals_latam_inbound_staging UNION deals_latam_outbound_staging (dedup por id),
  + deals_latam_contratos_staging (fechamentos = FECHADO_LATAM; valor em `value` USD).
- Sem account_id e sem dim de contato (dim_contacts vazia) => SEM regra de 90 dias e
  sem dedup por pessoa. Cada registro e classificado pelo proprio utm_source/url_conversao.
- Dominio de conteudo LATAM = getbuzzmonitor.com (nao .com.br).
- Funil mais curto: Lead -> Primer contacto -> Reunion -> Cierre. Sem etapa de proposta.
- Moeda USD; valor do contrato na coluna `value` (USD). fee_mensual e inconsistente — nao usar.
- Fechado (cierre) = FECHADO_LATAM: status='Ganho' raramente e marcado no AC LATAM => conta
  tb pagamento/contrato/cierre reais. Ver constante.

NOTA: tabelas _staging (decisao Victor 2026-05-29). utm_source vazio no inbound (gap de
ETL) => leads sem atribuicao nao contam (mesma logica do Brasil). Ver §6 do mapeamento.
"""
from __future__ import annotations

from datetime import date


# ============ CONSTANTES ============

# Whitelist de utm_source CM (match exato, lowercased). Variantes de placement
# (Instagram_Feed, Facebook_Mobile_Feed...) sao pegas pelos LIKE em filtro_cm_latam().
CM_UTM_SOURCES_LATAM: list[str] = [
    'meta', 'ig', 'instagram', 'facebook', 'fb', 'fb-ig', 'linkedin',
    'email', 'emailmkt', 'emblue', 'chatgpt.com', 'notion', 'blog',
    'tiktok', 'youtube', 'reddit', 'paid social', 'an',
]

# Dominio proprio de conteudo da LATAM (contenido.getbuzzmonitor.com, getbuzzmonitor.com/es/...)
CONTENT_DOMAIN_LIKE = '%getbuzzmonitor.com%'

# Sinais FORTES de URL: contam como CM **independente da UTM** (paginas de produto/oferta).
# Sobrepoem ate a exclusao de Google Ads. Decisao Victor 2026-05-29.
URL_FORTE_CM: list[str] = [
    '%contenido.getbuzzmonitor.com/plataforma-completa%',
    '%oferta%',
    # LP MCP-ES vive em material.buzzmonitor.com (NAO cai no dominio de conteudo
    # getbuzzmonitor.com) => incluida por URL exata p/ contar tb leads sem UTM ou
    # com UTM custom. So a mcp-es (nao o dominio inteiro). Decisao Victor 2026-07-06.
    '%material.buzzmonitor.com/mcp-es%',
]

# URLs comerciais (pricing/trial) que NAO contam como CM quando vem SEM UTM (null/vazia/
# string literal 'null'). Sem atribuicao = nao da pra reivindicar como Content Marketing.
# Decisao Victor 2026-06-08. Match exato — variantes com query string (que carregam UTM
# real, ex.: google_es, Instagram_Reels) seguem a regra normal do filtro CM.
URLS_COMERCIAIS_SEM_UTM_EXCLUIR: list[str] = [
    'https://getbuzzmonitor.com/es/planes/',
    'https://getbuzzmonitor.com/es/freetrial/',
    'https://getbuzzmonitor.com/es/personalizar-el-plan/',
]

# URLs que NUNCA sao CM (independente da UTM). Decisao Victor 2026-06-08.
# Match ILIKE (padrao %...%) p/ cobrir variantes com query string.
# IMPORTANTE: comparar com COALESCE(url, '') no SQL — sem isso, NULL ILIKE retorna NULL
# e o NOT propaga NULL, derrubando QUALQUER deal com url_conversao IS NULL do filtro CM
# (mesma armadilha documentada em queries.py _sql_exclusao_deals).
URLS_FORA_CM: list[str] = [
    '%contenido.getbuzzmonitor.com/buzzmonitor-institucional%',
]

# Deals de TESTE excluidos por ID (match exato). Decisao Victor 2026-07-10.
# Lote de QA de LP->deal criado em 08/07/2026 (todos utm_source='organic' + status
# 'Aberta', sem pais/closer/reunion, com URL de conteudo getbuzzmonitor.com — e por
# isso passavam no filtro CM). Exclusao POR ID (nao por UTM nem por titulo) pra nao
# derrubar organic-CM legitimo (ex.: deal 43572, [Lead Evento] Cafe con Buzzmonitor,
# organic + contenido.getbuzzmonitor.com). Aplicada no _leads_subquery() => remove
# esses ids de leads/primer contacto/reunion/perdidos/rankings/serie. Nao afeta
# fechamentos (nenhum e 'Ganho'/cierre). Se aparecer novo lote de teste, somar aqui.
DEALS_TESTE_EXCLUIR_LATAM: set[int] = {
    43661, 46385, 46427, 46700, 47739, 48641, 49473, 49540, 51056, 51129,
    51261, 53571, 53760, 54152, 54998, 55017, 55193, 55977, 56696, 56768,
    57195, 58247, 58824,
}

# Colunas necessarias para o funil (identicas em inbound e outbound)
_LEAD_COLS = (
    "id, title, cdate, mdate, status, pais, utm_source, utm_medium, utm_content, url_conversao, "
    "sdr, closer, fecha_de_primer_contacto, fecha_y_hora_de_primer_contacto, fecha_de_reunion"
)

# Normalizacao de pais (para agrupamentos; pais e recorte, nao filtro)
PAIS_NORM = """CASE
  WHEN lower(trim(pais)) IN ('mexico','méxico') THEN 'México'
  WHEN lower(trim(pais)) IN ('peru','perú') THEN 'Perú'
  WHEN lower(trim(pais)) IN ('panama','panamá') THEN 'Panamá'
  WHEN lower(trim(pais)) = 'chile' THEN 'Chile'
  WHEN pais IS NULL OR trim(pais)='' THEN NULL
  ELSE initcap(trim(pais))
END"""


# ============ FECHAMENTO (CIERRE) — definicao ampliada (Victor 2026-06-06) ============
# status='Ganho' quase nao e mantido no AC LATAM (ex.: stage 176 do pipeline Contratos =
# 84/96 'Aberta' apesar de fee+cierre+contrato). Conta como fechado quem tem QUALQUER sinal
# forte de fechamento real. Impacto CM: cierres all-time 2 -> 34, 2026 1 -> 7.
FECHADO_LATAM = (
    "(status = 'Ganho' OR primer_pago_realizado_automatico = TRUE "
    "OR fecha_de_inicio_de_contrato IS NOT NULL OR fecha_de_cierre_de_negocio IS NOT NULL)"
)

# Data do fechamento: cierre > inicio de contrato > primer pago (datas reais; SEM mdate). Deals
# sem nenhuma das tres ficam fora de janelas temporais (backlog a preencher no AC).
DATA_FECHO = "COALESCE(fecha_de_cierre_de_negocio, fecha_de_inicio_de_contrato, fecha_de_primer_pago_automatico)"

# Valor do contrato (USD): coluna `value`. fee_mensual e inconsistente (as vezes value*100, as
# vezes nao — ex.: value=1615/fee=90000). Cast defensivo texto->numeric.
VALOR_USD = "NULLIF(regexp_replace(coalesce(value,''), '[^0-9.]', '', 'g'), '')::numeric"


# ============ FILTRO CM LATAM ============

def filtro_cm_latam(alias: str = '') -> str:
    """SQL do filtro Content Marketing LATAM. `alias` prefixa as colunas (ex: 'd').

    Estrutura:
      (1) URL FORTE (plataforma-completa / oferta) => CM **independente da UTM**
          (sobrepoe ate google+cpc). Ver URL_FORTE_CM.
      (2) Regra geral: exclui Google Ads (google/google_es + cpc) E exige
          dominio de conteudo OU fonte social/owned da whitelist; E exclui URLs
          comerciais (planes / freetrial / personalizar-el-plan) que vem SEM UTM
          (null/vazia/'null' literal) — sem atribuicao = sem CM.
      (3) Wrapper externo (sempre exclui): URLs fora de CM (URLS_FORA_CM, ex.:
          /buzzmonitor-institucional) — independente de UTM. Usa COALESCE pra
          nao derrubar deals com url_conversao IS NULL (NULL ILIKE = NULL = falsy
          no NOT).
    """
    a = (alias + '.') if alias else ''
    sources = ", ".join(f"'{s}'" for s in CM_UTM_SOURCES_LATAM)
    url_forte = "\n      OR ".join(f"{a}url_conversao ILIKE '{p}'" for p in URL_FORTE_CM)
    urls_excluir = ", ".join(f"'{u}'" for u in URLS_COMERCIAIS_SEM_UTM_EXCLUIR)
    url_fora = "\n        OR ".join(f"COALESCE({a}url_conversao, '') ILIKE '{p}'" for p in URLS_FORA_CM)
    return f"""(
      (
        -- (1) sinal forte de URL — CM independente da UTM
        {url_forte}
        -- (2) regra geral (exclui Google Ads + URLs comerciais sem atribuicao)
        OR (
          NOT (lower(coalesce({a}utm_source,'')) LIKE 'google%' AND lower(coalesce({a}utm_medium,'')) = 'cpc')
          AND NOT (
            {a}url_conversao IN ({urls_excluir})
            AND (NULLIF(TRIM({a}utm_source), '') IS NULL OR LOWER(TRIM({a}utm_source)) = 'null')
          )
          AND (
            {a}url_conversao ILIKE '{CONTENT_DOMAIN_LIKE}'
            OR lower({a}utm_source) IN ({sources})
            OR lower({a}utm_source) LIKE 'instagram%'
            OR lower({a}utm_source) LIKE 'facebook%'
          )
        )
      )
      -- (3) wrapper externo: URLs fora de CM sempre (independente de UTM)
      AND NOT (
        {url_fora}
      )
    )"""


def _leads_subquery() -> str:
    """Subquery dos leads: inbound UNION outbound, **dedup SEMPRE por id** (nunca por UTM).

    Desempate quando o mesmo id aparece nas 2 tabelas (73 casos): fica com o registro
    mais COMPLETO (url/utm preenchidos) e, em empate, o mais recente. A chave de dedup
    e o id; completude e so criterio de desempate.
    """
    _excl = ", ".join(str(i) for i in sorted(DEALS_TESTE_EXCLUIR_LATAM))
    where_excl = f"WHERE id NOT IN ({_excl})" if _excl else ""
    return f"""(
      SELECT DISTINCT ON (id) {_LEAD_COLS}
      FROM (
        SELECT {_LEAD_COLS} FROM deals_latam_inbound_staging
        UNION ALL
        SELECT {_LEAD_COLS} FROM deals_latam_outbound_staging
      ) u
      {where_excl}
      ORDER BY id,
        (url_conversao IS NOT NULL AND url_conversao <> '') DESC,
        (utm_source IS NOT NULL) DESC,
        mdate DESC NULLS LAST
    )"""


# ============ CONTAGENS POR KPI ============

def q_count_kpis(ini: date, fim: date) -> str:
    """Counts de Leads / Primer contacto / Reunion no periodo, com filtro CM.

    Cada metrica conta pela data do SEU evento (lead=cdate, CE=primer contacto,
    reunion=fecha_de_reunion). Sem regra de 90d (LATAM nao tem account_id).
    """
    f = filtro_cm_latam('d')
    return f"""
SELECT
  count(*) FILTER (WHERE d.cdate::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}') AS leads,
  count(*) FILTER (WHERE COALESCE(d.fecha_de_primer_contacto, d.fecha_y_hora_de_primer_contacto::date)
                         BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}') AS ce,
  count(*) FILTER (WHERE d.fecha_de_reunion BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}') AS reunion
FROM {_leads_subquery()} d
WHERE {f}
"""


def q_count_perdidos(ini: date, fim: date) -> str:
    """Perdidos no periodo (status='Perdido'), com filtro CM. Datado por mdate (sem data dedicada)."""
    f = filtro_cm_latam('d')
    return f"""
SELECT count(*) AS perd
FROM {_leads_subquery()} d
WHERE d.status = 'Perdido'
  AND d.mdate::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {f}
"""


def q_count_fechamentos(ini: date, fim: date) -> str:
    """Fechamentos (cierres) no periodo, com filtro CM. Valor pela coluna `value` (USD).

    Fechado = FECHADO_LATAM (status='Ganho' OU pagamento/contrato/cierre reais).
    Data: DATA_FECHO (cierre > inicio > primer pago; sem mdate, 2026-06-06).
    """
    f = filtro_cm_latam('')
    return f"""
SELECT count(*) AS fech, COALESCE(SUM({VALOR_USD}), 0) AS valor
FROM deals_latam_contratos_staging
WHERE {FECHADO_LATAM}
  AND {DATA_FECHO}
      BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {f}
"""


# ============ LISTAS ============

def q_lista_leads(ini: date, fim: date) -> str:
    f = filtro_cm_latam('d')
    return f"""
SELECT d.id, d.title AS deal, d.utm_source, d.utm_content, d.url_conversao,
       {PAIS_NORM.replace('pais', 'd.pais')} AS pais,
       COALESCE(NULLIF(TRIM(d.sdr),''), NULLIF(TRIM(d.closer),'')) AS responsable,
       d.cdate::date AS data_conversao
FROM {_leads_subquery()} d
WHERE d.cdate::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {f}
ORDER BY d.cdate
"""


def q_lista_reuniones(ini: date, fim: date) -> str:
    f = filtro_cm_latam('d')
    return f"""
SELECT d.id, d.title AS deal, d.utm_source, d.utm_content,
       {PAIS_NORM.replace('pais', 'd.pais')} AS pais,
       COALESCE(NULLIF(TRIM(d.sdr),''), NULLIF(TRIM(d.closer),'')) AS responsable,
       d.fecha_de_reunion AS data_evento
FROM {_leads_subquery()} d
WHERE d.fecha_de_reunion BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {f}
ORDER BY d.fecha_de_reunion
"""


def q_lista_perdidos(ini: date, fim: date) -> str:
    f = filtro_cm_latam('d')
    return f"""
SELECT d.id, d.title AS deal, d.utm_source, d.utm_content,
       {PAIS_NORM.replace('pais', 'd.pais')} AS pais,
       d.mdate::date AS data_evento
FROM {_leads_subquery()} d
WHERE d.status = 'Perdido'
  AND d.mdate::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {f}
ORDER BY d.mdate
"""


def q_lista_fechamentos(ini: date, fim: date) -> str:
    f = filtro_cm_latam('')
    return f"""
SELECT id, title AS deal, utm_source, utm_content,
       {PAIS_NORM} AS pais,
       COALESCE(NULLIF(TRIM(closer),''), NULLIF(TRIM(sdr),'')) AS responsable,
       {VALOR_USD} AS valor, currency,
       {DATA_FECHO} AS data_fech
FROM deals_latam_contratos_staging
WHERE {FECHADO_LATAM}
  AND {DATA_FECHO}
      BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {f}
ORDER BY {DATA_FECHO}
"""


def q_ranking_pais(ini: date, fim: date) -> str:
    """Ranking de leads CM por pais no periodo."""
    f = filtro_cm_latam('d')
    return f"""
SELECT {PAIS_NORM.replace('pais', 'd.pais')} AS pais, count(*) AS leads
FROM {_leads_subquery()} d
WHERE d.cdate::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {f}
GROUP BY 1
ORDER BY 2 DESC
"""


# ============ RANKINGS / SÉRIES (Bloco 4 e 5) ============

def q_ranking(dim: str, ini: date, fim: date) -> str:
    """Ranking por 'utm_source' ou 'utm_content' no período (filtro CM).

    Retorna: dim, leads, pc (primer contacto), reunion, cierre. Cada métrica conta pela
    data do seu evento. Cierre vem de contratos (FECHADO_LATAM), agrupado pelo mesmo dim.
    """
    assert dim in ('utm_source', 'utm_content'), dim
    i, fm = ini.isoformat(), fim.isoformat()
    fb = filtro_cm_latam('b')
    fc = filtro_cm_latam('')
    g = f"lower(coalesce({dim}, '(vacío)'))"
    return f"""
WITH base AS (SELECT * FROM {_leads_subquery()} b WHERE {fb}),
leads_p AS (SELECT {g} dim, count(*) leads FROM base
            WHERE cdate::date BETWEEN '{i}' AND '{fm}' GROUP BY 1),
pc_p AS (SELECT {g} dim, count(*) pc FROM base
         WHERE COALESCE(fecha_de_primer_contacto, fecha_y_hora_de_primer_contacto::date) BETWEEN '{i}' AND '{fm}' GROUP BY 1),
reu_p AS (SELECT {g} dim, count(*) reunion FROM base
          WHERE fecha_de_reunion BETWEEN '{i}' AND '{fm}' GROUP BY 1),
cie_p AS (SELECT {g} dim, count(*) cierre FROM deals_latam_contratos_staging
          WHERE {FECHADO_LATAM} AND {fc}
            AND {DATA_FECHO} BETWEEN '{i}' AND '{fm}'
          GROUP BY 1),
dims AS (SELECT dim FROM leads_p UNION SELECT dim FROM pc_p UNION SELECT dim FROM reu_p UNION SELECT dim FROM cie_p)
SELECT d.dim,
       COALESCE(l.leads,0) leads, COALESCE(p.pc,0) pc,
       COALESCE(r.reunion,0) reunion, COALESCE(c.cierre,0) cierre
FROM dims d
LEFT JOIN leads_p l USING(dim)
LEFT JOIN pc_p p USING(dim)
LEFT JOIN reu_p r USING(dim)
LEFT JOIN cie_p c USING(dim)
ORDER BY leads DESC, cierre DESC, reunion DESC
"""


def q_source_por_content(ini: date, fim: date) -> str:
    """Mapa utm_content -> utm_source dominante no período (para colorir o badge no ranking de content)."""
    fb = filtro_cm_latam('b')
    return f"""
SELECT lower(coalesce(utm_content,'(vacío)')) utm_content,
       (array_agg(utm_source ORDER BY cdate DESC))[1] utm_source
FROM {_leads_subquery()} b
WHERE {fb} AND cdate::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
GROUP BY 1
"""


def q_serie_12m(hoje: date) -> str:
    """Série semanal das últimas 52 semanas: leads, pc, reunion, cierres (por data do evento)."""
    fb = filtro_cm_latam('b')
    fc = filtro_cm_latam('')
    h = hoje.isoformat()
    return f"""
WITH base AS (SELECT * FROM {_leads_subquery()} b WHERE {fb})
SELECT date_trunc('week', cdate)::date semana, 'leads' metrica, count(*) n FROM base
  WHERE cdate >= '{h}'::date - INTERVAL '52 weeks' GROUP BY 1
UNION ALL
SELECT date_trunc('week', COALESCE(fecha_de_primer_contacto, fecha_y_hora_de_primer_contacto::date))::date, 'pc', count(*) FROM base
  WHERE COALESCE(fecha_de_primer_contacto, fecha_y_hora_de_primer_contacto::date) >= '{h}'::date - INTERVAL '52 weeks' GROUP BY 1
UNION ALL
SELECT date_trunc('week', fecha_de_reunion)::date, 'reunion', count(*) FROM base
  WHERE fecha_de_reunion >= '{h}'::date - INTERVAL '52 weeks' GROUP BY 1
UNION ALL
SELECT date_trunc('week', {DATA_FECHO})::date, 'cierres', count(*)
  FROM deals_latam_contratos_staging
  WHERE {FECHADO_LATAM} AND {fc}
    AND {DATA_FECHO} >= '{h}'::date - INTERVAL '52 weeks'
  GROUP BY 1
"""


def q_proporcao_12m(hoje: date) -> str:
    """Primer contacto + Reunión por source nos últimos 12 meses (para o gráfico 5.2)."""
    fb = filtro_cm_latam('b')
    h = hoje.isoformat()
    return f"""
SELECT lower(coalesce(utm_source,'(vacío)')) source,
  count(*) FILTER (WHERE COALESCE(fecha_de_primer_contacto, fecha_y_hora_de_primer_contacto::date) >= '{h}'::date - INTERVAL '12 months') pc_12m,
  count(*) FILTER (WHERE fecha_de_reunion >= '{h}'::date - INTERVAL '12 months') reunion_12m
FROM {_leads_subquery()} b
WHERE {fb}
GROUP BY 1
ORDER BY reunion_12m DESC, pc_12m DESC
"""


# ============ SELF-TEST (ancoras da auditoria) ============

if __name__ == '__main__':
    import sys
    from pathlib import Path
    import psycopg

    env = Path(__file__).parent / ".env"
    url = next((l.split("=", 1)[1].strip().strip('"').strip("'")
                for l in env.read_text(encoding="utf-8").splitlines()
                if l.strip().startswith("SUPABASE_PG_URL=")), None)
    if not url:
        raise SystemExit("SUPABASE_PG_URL nao encontrado em dashboard/.env")

    hoje = date.today()
    y_ini, y_fim = date(2026, 1, 1), hoje
    all_ini, all_fim = date(2019, 1, 1), hoje

    with psycopg.connect(url, autocommit=True) as conn, conn.cursor() as cur:
        cur.execute("SET statement_timeout = '120s'")
        def scalar(sql, idx=0):
            cur.execute(sql); r = cur.fetchone(); return r[idx] if r else None
        print("== Self-test LATAM (apos exclusao buzzmonitor-institucional 2026-06-08: ~6074 all-time, ~525 em 2026) ==")
        cur.execute(q_count_kpis(all_ini, all_fim)); a = cur.fetchone()
        print(f"  CM all-time: leads={a[0]} ce={a[1]} reunion={a[2]}")
        cur.execute(q_count_kpis(y_ini, y_fim)); y = cur.fetchone()
        print(f"  CM 2026:     leads={y[0]} ce={y[1]} reunion={y[2]}")
        # Definicao ampliada de fechado (2026-06-06): status='Ganho' OU pagamento/contrato/cierre
        # reais; valor pela coluna `value` (USD). Espera ~34 all-time CM, ~7 em 2026 (com data real).
        cur.execute(q_count_fechamentos(all_ini, all_fim)); fa = cur.fetchone()
        print(f"  Fechamentos CM all-time: {fa[0]} · USD {fa[1]}")
        cur.execute(q_count_fechamentos(y_ini, y_fim)); fy = cur.fetchone()
        print(f"  Fechamentos CM 2026:     {fy[0]} · USD {fy[1]}")
