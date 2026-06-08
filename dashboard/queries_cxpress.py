"""queries_cxpress.py — queries SQL para a dashboard de Funil Inbound **Cxpress Brasil**.

Fonte: tabela UNICA `cxpress_deals_funil_principal_prod` (Supabase, read-only).
Espelha dashboard/MAPEAMENTO-CAMPOS-cxpress.md.

Diferencas vs Buzzmonitor (queries.py):
- UMA tabela so (nao ha deals_contratos separada). Cada deal traz TODAS as datas do
  funil na propria linha => sem CTE de conversoes, sem regra de 90d, sem UNION.
- Sem coluna de email => sem dedup por pessoa (conta por deal, igual LATAM). Ha `contact` (bigint).
- Funil: Lead -> Triagem -> Agendamento -> Demo realizada -> Proposta -> Fechamento (+ Perdido).
- Datas dos eventos (data_*_auto) chegam como TEXTO do ActiveCampaign => cast defensivo
  via _d() (assume ISO 'YYYY-MM-DD...'; ver MAPEAMENTO §Datas se o AC exportar outro formato).
- Valor em texto (cxpress_fee_mensal / valor_atualizado_do_fee) => parse em Python.
- Moeda BRL, idioma PT-BR.

ESCOPO (filtro_inbound / filtro_cm): NO-OP por padrao (conta TODAS as linhas da tabela).
Ative/calibre quando houver dados — ver MAPEAMENTO §Escopo. A tabela ainda esta vazia (0 linhas);
todo filtro de canal/funil precisa ser conferido contra os valores reais antes de ligar.
"""
from __future__ import annotations

from datetime import date

TABELA = "cxpress_deals_funil_principal_prod"

# Colunas-data de cada etapa do funil. cdate e timestamptz; o resto chega como TEXTO do AC.
COL_LEAD = "cdate"                              # criacao do deal (timestamptz)
COL_TRIAGEM = "data_triagem_realizada_auto"
COL_AGENDAMENTO = "data_do_agendamento_auto"
COL_DEMO = "data_de_demo_realizada_auto"
COL_PROPOSTA = "data_do_envio_da_proposta_auto"
COL_FECHAMENTO = "data_do_fechamento_auto"
COL_LOST = "data_do_lost_auto"

# Valor do contrato (texto) — parseado em Python (render_helpers.parse_valor_text).
COL_VALOR = "COALESCE(NULLIF(TRIM(valor_atualizado_do_fee), ''), NULLIF(TRIM(cxpress_fee_mensal), ''))"
# Responsavel pelo deal (closer tem precedencia; cai pro SDR/BDR).
COL_RESP = "COALESCE(NULLIF(TRIM(closer_bd_auto), ''), NULLIF(TRIM(sdr_bdr_auto), ''))"


def _d(col: str) -> str:
    """Cast defensivo TEXTO->date para as colunas data_*_auto do ActiveCampaign.

    Aceita 'YYYY-MM-DD' com ou sem hora (pega os 10 primeiros chars); devolve NULL
    para vazio/lixo/formato diferente — assim um valor malformado nunca quebra a query
    inteira. Se o AC exportar DMY/MDY, ajustar SO AQUI (ponto unico). Ver MAPEAMENTO §Datas.
    """
    return f"(CASE WHEN {col} ~ '^[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}' THEN left({col}, 10)::date END)"


# ============ ESCOPO (no-op por padrao — calibrar com dados) ============

def filtro_inbound(alias: str = '') -> str:
    """Restringe ao funil INBOUND (funil_auto = 'Inbound').

    Calibrado 2026-06-06 contra os dados reais: funil_auto = 'Inbound' (3004),
    'Outbound' (3457), vazio (865). A dashboard e do funil de inbound, entao filtra 'Inbound'.
    Os 865 sem classificacao ficam de fora — trocar por
    `{a}funil_auto IS DISTINCT FROM 'Outbound'` se quiser incluir os vazios.
    """
    a = (alias + '.') if alias else ''
    return f"{a}funil_auto = 'Inbound'"


# Whitelist PROVISORIA de utm_source CM (NAO calibrada — tabela vazia). Ver MAPEAMENTO §Escopo.
CM_UTM_SOURCES: list[str] = [
    'meta', 'ig', 'instagram', 'facebook', 'fb', 'linkedin',
    'email', 'blog', 'tiktok', 'youtube', 'notion', 'chatgpt.com',
]


def filtro_cm(alias: str = '') -> str:
    """Filtro Content Marketing. NO-OP por padrao (mostra TODO o funil inbound).

    Para estreitar a dashboard so a leads de CM, trocar o corpo por
    `return _filtro_cm_provisorio(alias)` — DEPOIS de calibrar a whitelist/dominio
    contra os utm_source/url_conversao reais (hoje a tabela tem 0 linhas).
    """
    return "TRUE"


def _filtro_cm_provisorio(alias: str = '') -> str:
    """Rascunho do filtro CM (exclui Google Ads; aceita social/owned + dominio Cxpress).
    NAO usar sem calibrar contra dados reais. Mantido como ponto de partida.
    """
    a = (alias + '.') if alias else ''
    sources = ", ".join(f"'{s}'" for s in CM_UTM_SOURCES)
    return f"""(
      NOT (lower(coalesce({a}utm_source, '')) LIKE 'google%' AND lower(coalesce({a}utm_medium, '')) = 'cpc')
      AND (
        lower({a}utm_source) IN ({sources})
        OR {a}url_conversao ILIKE '%cxpress%'
      )
    )"""


def _escopo(alias: str = 'd') -> str:
    """Combina inbound + CM (ambos no-op por padrao). Use no WHERE das queries."""
    return f"({filtro_inbound(alias)}) AND ({filtro_cm(alias)})"


# ============ KPIs (7 do funil, contados pela data do evento) ============

def q_count_kpis(ini: date, fim: date) -> str:
    """Counts das 7 etapas no periodo. Cada metrica conta pela data do SEU evento."""
    i, f = ini.isoformat(), fim.isoformat()
    return f"""
SELECT
  count(*) FILTER (WHERE d.{COL_LEAD}::date BETWEEN '{i}' AND '{f}') AS leads,
  count(*) FILTER (WHERE {_d('d.' + COL_TRIAGEM)} BETWEEN '{i}' AND '{f}') AS triagem,
  count(*) FILTER (WHERE {_d('d.' + COL_AGENDAMENTO)} BETWEEN '{i}' AND '{f}') AS agendamento,
  count(*) FILTER (WHERE {_d('d.' + COL_DEMO)} BETWEEN '{i}' AND '{f}') AS demo,
  count(*) FILTER (WHERE {_d('d.' + COL_PROPOSTA)} BETWEEN '{i}' AND '{f}') AS proposta,
  count(*) FILTER (WHERE {_d('d.' + COL_FECHAMENTO)} BETWEEN '{i}' AND '{f}') AS fechamento,
  count(*) FILTER (WHERE {_d('d.' + COL_LOST)} BETWEEN '{i}' AND '{f}') AS perd
FROM {TABELA} d
WHERE {_escopo('d')}
"""


# ============ LISTAS DE DEALS ============

def q_lista_leads(ini: date, fim: date) -> str:
    return f"""
SELECT d.id, d.title AS deal, d.utm_source, d.utm_content,
       {COL_RESP} AS responsavel,
       d.{COL_LEAD}::date AS data_evento
FROM {TABELA} d
WHERE d.{COL_LEAD}::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {_escopo('d')}
ORDER BY d.{COL_LEAD}
"""


def q_lista_agendamento(ini: date, fim: date) -> str:
    """Agendamentos da semana (+ flag se a demo ja foi realizada)."""
    return f"""
SELECT d.id, d.title AS deal, d.utm_source, d.utm_content,
       {COL_RESP} AS responsavel,
       {_d('d.' + COL_AGENDAMENTO)} AS data_evento,
       {_d('d.' + COL_DEMO)} AS data_demo
FROM {TABELA} d
WHERE {_d('d.' + COL_AGENDAMENTO)} BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {_escopo('d')}
ORDER BY {_d('d.' + COL_AGENDAMENTO)}
"""


def q_lista_demo(ini: date, fim: date) -> str:
    """Demos realizadas na semana (+ flag se ja saiu proposta)."""
    return f"""
SELECT d.id, d.title AS deal, d.utm_source, d.utm_content,
       {COL_RESP} AS responsavel,
       {_d('d.' + COL_DEMO)} AS data_evento,
       {_d('d.' + COL_PROPOSTA)} AS data_proposta
FROM {TABELA} d
WHERE {_d('d.' + COL_DEMO)} BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {_escopo('d')}
ORDER BY {_d('d.' + COL_DEMO)}
"""


def q_lista_propostas(ini: date, fim: date) -> str:
    return f"""
SELECT d.id, d.title AS deal, d.utm_source, d.utm_content,
       {COL_RESP} AS responsavel,
       {_d('d.' + COL_PROPOSTA)} AS data_evento,
       {COL_VALOR} AS valor_text, d.currency
FROM {TABELA} d
WHERE {_d('d.' + COL_PROPOSTA)} BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {_escopo('d')}
ORDER BY {_d('d.' + COL_PROPOSTA)}
"""


def q_lista_fechamentos(ini: date, fim: date) -> str:
    return f"""
SELECT d.id, d.title AS deal, d.utm_source, d.utm_content,
       {COL_RESP} AS responsavel,
       {_d('d.' + COL_FECHAMENTO)} AS data_evento,
       {COL_VALOR} AS valor_text, d.currency
FROM {TABELA} d
WHERE {_d('d.' + COL_FECHAMENTO)} BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {_escopo('d')}
ORDER BY {_d('d.' + COL_FECHAMENTO)}
"""


def q_lista_perdidos(ini: date, fim: date) -> str:
    """Perdidos no periodo (datado por data_do_lost_auto), com motivo e ultima etapa atingida."""
    return f"""
SELECT d.id, d.title AS deal, d.utm_source, d.utm_content,
       d.motivo_de_perda_closer_sdr AS motivo,
       d.etapa_do_lost AS etapa,
       {_d('d.' + COL_LOST)} AS data_evento,
       COALESCE({_d('d.' + COL_DEMO)}, {_d('d.' + COL_AGENDAMENTO)},
                {_d('d.' + COL_TRIAGEM)}, d.{COL_LEAD}::date) AS ultima_conversao
FROM {TABELA} d
WHERE {_d('d.' + COL_LOST)} BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {_escopo('d')}
ORDER BY {_d('d.' + COL_LOST)} DESC
"""


# ============ RANKINGS (source + content) ============

def q_ranking(dim: str, ini: date, fim: date) -> str:
    """Ranking por 'utm_source' ou 'utm_content' no periodo.

    Retorna por dim: leads, triagem, agendamento, demo, proposta, fechamento.
    Cada metrica conta pela data do seu evento. HAVING corta dims sem atividade no periodo
    (a base cobre todos os deals; sem isso, toda source historica apareceria zerada).
    """
    assert dim in ('utm_source', 'utm_content'), dim
    i, f = ini.isoformat(), fim.isoformat()
    esc = _escopo('d')
    fl = [
        f"count(*) FILTER (WHERE {COL_LEAD}::date BETWEEN '{i}' AND '{f}')",
        f"count(*) FILTER (WHERE {_d(COL_TRIAGEM)} BETWEEN '{i}' AND '{f}')",
        f"count(*) FILTER (WHERE {_d(COL_AGENDAMENTO)} BETWEEN '{i}' AND '{f}')",
        f"count(*) FILTER (WHERE {_d(COL_DEMO)} BETWEEN '{i}' AND '{f}')",
        f"count(*) FILTER (WHERE {_d(COL_PROPOSTA)} BETWEEN '{i}' AND '{f}')",
        f"count(*) FILTER (WHERE {_d(COL_FECHAMENTO)} BETWEEN '{i}' AND '{f}')",
    ]
    return f"""
WITH base AS (SELECT * FROM {TABELA} d WHERE {esc})
SELECT
  COALESCE({dim}, '(vazio)') AS dim,
  {fl[0]} AS leads,
  {fl[1]} AS triagem,
  {fl[2]} AS agendamento,
  {fl[3]} AS demo,
  {fl[4]} AS proposta,
  {fl[5]} AS fechamento
FROM base
GROUP BY {dim}
HAVING {fl[0]} > 0 OR {fl[1]} > 0 OR {fl[2]} > 0 OR {fl[3]} > 0 OR {fl[4]} > 0 OR {fl[5]} > 0
ORDER BY leads DESC, fechamento DESC, demo DESC
"""


def q_source_por_content(ini: date, fim: date) -> str:
    """Mapa utm_content -> utm_source dominante no periodo (colorir o badge no ranking de content)."""
    esc = _escopo('d')
    return f"""
SELECT COALESCE(utm_content, '(vazio)') AS utm_content,
       (array_agg(utm_source ORDER BY cdate DESC))[1] AS utm_source
FROM {TABELA} d
WHERE {esc} AND {COL_LEAD}::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
GROUP BY 1
"""


# ============ SERIE TEMPORAL 52 SEMANAS + PROPORCAO ============

def q_serie_12m(hoje: date) -> str:
    """Serie semanal das ultimas 52 semanas: leads, triagem, agendamento, proposta, fechamento."""
    esc = _escopo('d')
    h = hoje.isoformat()
    return f"""
WITH base AS (SELECT * FROM {TABELA} d WHERE {esc})
SELECT date_trunc('week', {COL_LEAD})::date AS semana, 'leads' AS metrica, count(*) AS n FROM base
  WHERE {COL_LEAD}::date >= '{h}'::date - INTERVAL '52 weeks' GROUP BY 1
UNION ALL
SELECT date_trunc('week', {_d(COL_TRIAGEM)})::date, 'triagem', count(*) FROM base
  WHERE {_d(COL_TRIAGEM)} >= '{h}'::date - INTERVAL '52 weeks' GROUP BY 1
UNION ALL
SELECT date_trunc('week', {_d(COL_AGENDAMENTO)})::date, 'agendamento', count(*) FROM base
  WHERE {_d(COL_AGENDAMENTO)} >= '{h}'::date - INTERVAL '52 weeks' GROUP BY 1
UNION ALL
SELECT date_trunc('week', {_d(COL_PROPOSTA)})::date, 'proposta', count(*) FROM base
  WHERE {_d(COL_PROPOSTA)} >= '{h}'::date - INTERVAL '52 weeks' GROUP BY 1
UNION ALL
SELECT date_trunc('week', {_d(COL_FECHAMENTO)})::date, 'fechamento', count(*) FROM base
  WHERE {_d(COL_FECHAMENTO)} >= '{h}'::date - INTERVAL '52 weeks' GROUP BY 1
"""


def q_proporcao_12m(hoje: date) -> str:
    """Agendamentos + Demos por source nos ultimos 12 meses (grafico 5.2).

    Alias ra_12m/rr_12m para reaproveitar render_helpers.render_proporcao_sources
    (ra_12m = agendamentos, rr_12m = demos).
    """
    esc = _escopo('d')
    h = hoje.isoformat()
    return f"""
SELECT lower(coalesce(utm_source, '(vazio)')) AS source,
  count(*) FILTER (WHERE {_d(COL_AGENDAMENTO)} >= '{h}'::date - INTERVAL '12 months') AS ra_12m,
  count(*) FILTER (WHERE {_d(COL_DEMO)} >= '{h}'::date - INTERVAL '12 months') AS rr_12m
FROM {TABELA} d
WHERE {esc}
GROUP BY 1
HAVING count(*) FILTER (WHERE {_d(COL_AGENDAMENTO)} >= '{h}'::date - INTERVAL '12 months') > 0
ORDER BY ra_12m DESC, rr_12m DESC
"""
