"""queries_buzzcreators.py — logica de Content Marketing da dashboard Buzzcreators Brasil.

Paralelo de queries.py (Buzzmonitor BR), queries_cxpress.py e queries_latam.py, mas com uma
diferenca estrutural: **o deal do Buzzcreators nao tem UTM**. A fonte e o Pipedrive
(deals_pipedrive_vendas_buzzcreators), que nao guarda nenhum campo de utm_* nem no schema nem em
custom_fields. A atribuicao e RECUPERADA por join com o contato:

    deal.person_id -> dim_pipedrive_persons.custom_fields ('*UTM Source [AUTO]', 'URL Conversao [AUTO]', ...)
    fallback por e-mail -> dim_contacts (ActiveCampaign: utm_source_auto, url_conversao_auto, ...)

Cobertura medida em 2026-08-26: 1.685/3.047 deals via person + 469 incrementais via AC = 2.154 (71%);
no funil Inbound, 1.560/1.928 (81%). Detalhes e ressalvas no cabecalho de MAPEAMENTO-CAMPOS-buzzcreators.md.

RESSALVA CENTRAL (last touch): os campos [AUTO] do contato sao sobrescritos a cada nova conversao,
entao a UTM lida e o **ultimo toque conhecido do contato**, nao necessariamente o toque que gerou o
deal. Nao existe historico datado no lado Pipedrive. Isso e assumido e sinalizado na propria dash.

Funil (decisao Victor 2026-08-26): Lead -> Agendamento -> Reuniao realizada -> Fechamento (+ Perdidos).
A etapa Proposta foi OMITIDA de proposito: o Pipedrive nao registra data de entrada em Proposta
(so 34 deals tem 'Data do aceite [BD]*'), entao ela nao pode ser contada por data de evento como as
demais — e uma coluna sem data quebraria a comparacao entre periodos.
"""
from __future__ import annotations

from datetime import date


# ============ TABELAS ============

TABELA = 'public.deals_pipedrive_vendas_buzzcreators'
TABELA_PERSONS = 'public.dim_pipedrive_persons'
TABELA_CONTACTS = 'public.dim_contacts'


# ============ FILTRO CM ============

# Whitelist de utm_source que conta como Content Marketing.
# Calibrada com o Victor em 2026-08-26 sobre a distribuicao real dos 3.047 deals:
#   - google FICA DE FORA: 1.291 dos 1.297 deals google sao medium=cpc (Search pago). Mesma
#     decisao da dash Buzzmonitor BR, onde 'google' esta em INTERNOS_EXCLUIR.
#   - cs / comercial / bds / sdr FICAM DE FORA: toque do proprio time, nao aquisicao.
#   - inmail ENTRA (LinkedIn) e email ENTRA — decisao explicita do Victor.
#   - eventos presenciais/summit ENTRAM (eventos, buzzsummit, influent-summit, panfleto, convites).
#   - organic / organic-direct ENTRAM (SEO + direto).
#   - chatgpt.com ENTRA (GEO) — ja e whitelist na dash BR, mantem paridade.
# Valores em minusculo; a comparacao normaliza com lower(trim(...)).
CM_UTM_SOURCES: list[str] = [
    # --- Meta / social organico e pago de conteudo
    'meta', 'instagram', 'instagram_feed', 'instagram_stories', 'instagram_reels',
    'reels', 'feed', 'ig', 'fb', 'facebook', 'tiktok',
    # --- Link na bio (grafias que o Victor usa; ainda sem volume nesta base)
    'instabio', 'insta-bio', 'bio', 'link_in_bio',
    # --- LinkedIn
    'linkedin', 'inmail',
    # --- E-mail / newsletter / mensageria
    'email', 'newsletter', 'sms', 'whatsapp',
    # --- Conteudo proprio
    'blog', 'notion', 'oferta',
    # --- Webinars e LPs de conteudo
    'webinar', 'pos-webinar', 'apresentacao-webinar', 'apresentacao', 'webinar-ao-vivo',
    'inscrito em webinar', 'lp-agradecimento', 'lp-pos-evento',
    # --- Eventos presenciais
    'eventos', 'buzzsummit', 'influent-summit', 'panfleto-influent-summit', 'convites',
    # --- GEO / organico
    'chatgpt.com', 'gemini', 'perplexity.ai', 'organic', 'organic/direct',
]

# Sources vistos na base que NAO entram — documentados pra ninguem "redescobrir" e re-incluir.
#   internos.......: cs, cs_buzz, cs-buzzmonitor, comercial, bds, sdr, plataforma, app-buzzmonitor
#   midia paga.....: google (98% medium=cpc)
#   tracking quebrado: %utm_source_novo%, {{placement}}, teste_origem, null, others
#   pendente.......: 'redes-sociais' (3 deals) — na dash BR o Victor confirmou que NAO e CM
#                    (era CS tagueando expansao de cliente); mantido fora aqui pela mesma razao.
#                    'thebizness' (1 deal, newsletter parceira) — fora ate o Victor confirmar.
NAO_CM_DOCUMENTADOS: list[str] = [
    'google', 'cs', 'cs_buzz', 'cs-buzzmonitor', 'comercial', 'bds', 'sdr',
    'plataforma', 'app-buzzmonitor', 'redes-sociais', 'thebizness',
    '%utm_source_novo%', '{{placement}}', 'teste_origem', 'null', 'others',
]

# Dominios de conteudo. NAO creditam CM sozinhos (decisao Victor 2026-08-26: "exige source na
# whitelist") — ficam aqui porque a dash os EXIBE na coluna Conteudo e porque a documentacao
# precisa registrar quais dominios sao de conteudo (webinar/evento.buzzmonitor confirmados).
DOMINIOS_CONTEUDO: list[str] = [
    'conteudo.buzzmonitor.com.br', 'webinar.buzzmonitor.com', 'evento.buzzmonitor.com',
    'pages.buzzcreators.com.br',
]


# ============ CAMPOS DO FUNIL ============

# Chaves de custom_fields do Pipedrive (texto ISO 'YYYY-MM-DD' — verificado em 2026-08-26).
CF_AGENDAMENTO = 'Data do agendamento [SDR ou AUTO]'
CF_AGENDAMENTO_ALT = '[SDR|BDR] Data da Reunião Agendada'
CF_REUNIAO = 'Data da Reunião Realizada [BD ou AUTO]'
CF_ACEITE = 'Data do aceite [BD]*'

# Chaves de atribuicao no contato do Pipedrive.
CF_P_SOURCE = '*UTM Source [AUTO]'
CF_P_MEDIUM = '*UTM Medium [AUTO]'
CF_P_CAMPAIGN = '*UTM Campaing [AUTO]'   # typo do proprio campo no CRM
CF_P_CONTENT = '*UTM Content [AUTO]'
CF_P_URL = 'URL Conversão [AUTO]'
CF_P_URL_ORIGEM = 'URL de Origem [AUTO]'


def _cf(alias: str, chave: str) -> str:
    """custom_fields->>'chave' como texto nao-vazio (NULL quando vazio)."""
    return f"nullif({alias}.custom_fields->>'{chave}', '')"


def _cf_date(alias: str, chave: str) -> str:
    return f"{_cf(alias, chave)}::date"


# Data de cada etapa, com o alias 'd' (deal).
D_LEAD = 'd.add_time::date'
D_AGENDAMENTO = f"coalesce({_cf_date('d', CF_AGENDAMENTO)}, {_cf_date('d', CF_AGENDAMENTO_ALT)})"
D_REUNIAO = _cf_date('d', CF_REUNIAO)
D_FECHAMENTO = f"coalesce(d.won_time::date, d.data_aceite, {_cf_date('d', CF_ACEITE)})"
D_LOST = 'd.lost_time::date'


# ============ ATRIBUICAO (join deal -> person -> contato AC) ============

def join_atribuicao() -> str:
    """FROM + JOINs que trazem a UTM recuperada. Aliases: d (deal), p (person), c (contato AC)."""
    return f"""{TABELA} d
  LEFT JOIN {TABELA_PERSONS} p ON p.id = d.person_id
  LEFT JOIN {TABELA_CONTACTS} c
         ON lower(nullif(trim(coalesce(p.email, d.person_email)), '')) = lower(nullif(trim(c.email), ''))"""


# Hierarquia de fallback: contato Pipedrive -> contato AC (utm_source_auto -> utm_source_origem_auto).
SRC = (
    f"lower(trim(coalesce({_cf('p', CF_P_SOURCE)}, "
    f"nullif(c.utm_source_auto, ''), nullif(c.utm_source_origem_auto, ''))))"
)
MEDIUM = f"lower(trim(coalesce({_cf('p', CF_P_MEDIUM)}, nullif(c.utm_medium_auto, ''))))"
CAMPAIGN = f"coalesce({_cf('p', CF_P_CAMPAIGN)}, nullif(c.utm_campaing_auto, ''))"
CONTENT = f"coalesce({_cf('p', CF_P_CONTENT)}, nullif(c.utm_content_auto, ''))"
URL_CONV = (
    f"coalesce({_cf('p', CF_P_URL)}, nullif(c.url_conversao_auto, ''), {_cf('p', CF_P_URL_ORIGEM)})"
)


def _sql_list(vals: list[str]) -> str:
    return ', '.join("'" + v.replace("'", "''") + "'" for v in vals)


def filtro_cm() -> str:
    """Predicado de Content Marketing: utm_source recuperado na whitelist.

    Dominio NAO credita sozinho (decisao Victor 2026-08-26) — um lead que converteu numa LP de
    conteudo mas veio com utm_source=cs/quebrado fica FORA.
    """
    return f"{SRC} IN ({_sql_list(CM_UTM_SOURCES)})"


def _escopo() -> str:
    """Escopo da dashboard = filtro CM. Sem filtro de funil.

    A dash BR remove o funil 'Outbound'; aqui isso seria redundante e enganoso: 'Outbound' no
    Pipedrive (origem_lead) marca como o TIME abordou, e um lead prospectado que ja tinha
    convertido em conteudo continua sendo CM. O filtro de source ja segura o que importa —
    prospeccao pura nao tem utm de conteudo. origem_lead vai exportado pra quem quiser cortar.
    """
    return filtro_cm()


# ============ QUERIES ============

def q_deals_raw() -> str:
    """Uma linha por deal no escopo CM, com as datas de etapa normalizadas.

    Sem filtro de data na base: o motor.js filtra por data de etapa no intervalo escolhido
    (mesma convencao do clone Cxpress).
    """
    return f"""
SELECT d.id,
       d.title                                    AS deal,
       {SRC}                                      AS utm_source,
       {CONTENT}                                  AS utm_content,
       {CAMPAIGN}                                 AS utm_campaign,
       {MEDIUM}                                   AS utm_medium,
       {URL_CONV}                                 AS url_conversao,
       d.owner_name                               AS responsavel,
       d.origem_lead                              AS funil,
       d.stage_name                               AS etapa_atual,
       d.value                                    AS valor,
       d.currency,
       d.status,
       d.lost_reason                              AS motivo,
       {D_LEAD}                                   AS d_lead,
       {D_AGENDAMENTO}                            AS d_agendamento,
       {D_REUNIAO}                                AS d_reuniao,
       {D_FECHAMENTO}                             AS d_fechamento,
       {D_LOST}                                   AS d_lost
FROM {join_atribuicao()}
WHERE {_escopo()}
"""


def q_serie_12m(hoje: date) -> str:
    """Serie semanal das ultimas 52 semanas: leads, agendamento, reuniao, fechamento."""
    h = hoje.isoformat()
    base = f"WITH base AS (SELECT {D_LEAD} AS d_lead, {D_AGENDAMENTO} AS d_agendamento, " \
           f"{D_REUNIAO} AS d_reuniao, {D_FECHAMENTO} AS d_fechamento " \
           f"FROM {join_atribuicao()} WHERE {_escopo()})"
    partes = [
        ('leads', 'd_lead'),
        ('agendamento', 'd_agendamento'),
        ('reuniao', 'd_reuniao'),
        ('fechamento', 'd_fechamento'),
    ]
    sel = "\nUNION ALL\n".join(
        f"SELECT date_trunc('week', {col})::date AS semana, '{nome}' AS metrica, count(*) AS n "
        f"FROM base WHERE {col} >= '{h}'::date - INTERVAL '52 weeks' GROUP BY 1"
        for nome, col in partes
    )
    return f"{base}\n{sel}\n"


def q_proporcao_12m(hoje: date) -> str:
    """Agendamentos + Reunioes realizadas por source nos ultimos 12 meses (grafico 5.2).

    Alias ra_12m/rr_12m pra reaproveitar render_helpers.render_proporcao_sources
    (ra_12m = agendamentos, rr_12m = reunioes realizadas).
    """
    h = hoje.isoformat()
    return f"""
SELECT coalesce({SRC}, '(vazio)') AS source,
  count(*) FILTER (WHERE {D_AGENDAMENTO} >= '{h}'::date - INTERVAL '12 months') AS ra_12m,
  count(*) FILTER (WHERE {D_REUNIAO}     >= '{h}'::date - INTERVAL '12 months') AS rr_12m
FROM {join_atribuicao()}
WHERE {_escopo()}
GROUP BY 1
HAVING count(*) FILTER (WHERE {D_AGENDAMENTO} >= '{h}'::date - INTERVAL '12 months') > 0
ORDER BY ra_12m DESC, rr_12m DESC
"""


def q_cobertura() -> str:
    """Diagnostico: quanto da base o join de atribuicao alcanca (vai no rodape da dash)."""
    return f"""
SELECT count(*) AS deals_total,
       count(*) FILTER (WHERE {SRC} IS NOT NULL) AS com_source,
       count(*) FILTER (WHERE {_escopo()})       AS no_escopo_cm
FROM {join_atribuicao()}
"""


def q_kpis_periodo(ini: date, fim: date) -> str:
    """KPIs de um intervalo, direto em SQL — usado so pelo gate de paridade vs motor.js."""
    i, f = ini.isoformat(), fim.isoformat()
    per = f"BETWEEN '{i}'::date AND '{f}'::date"
    return f"""
SELECT
  count(*) FILTER (WHERE {D_LEAD} {per})                          AS leads,
  count(*) FILTER (WHERE {D_AGENDAMENTO} {per})                   AS agendamento,
  count(*) FILTER (WHERE {D_REUNIAO} {per})                       AS reuniao,
  count(*) FILTER (WHERE {D_FECHAMENTO} {per})                    AS fechamento,
  count(*) FILTER (WHERE {D_LEAD} {per}
                     AND {D_LOST} IS NOT NULL
                     AND d.status = 'lost')                       AS perd
FROM {join_atribuicao()}
WHERE {_escopo()}
"""


def q_ranking(dim: str, ini: date, fim: date) -> str:
    """Ranking por fonte ou conteudo no intervalo — usado so pelo gate de paridade."""
    col = {'utm_source': SRC, 'utm_content': CONTENT}[dim]
    i, f = ini.isoformat(), fim.isoformat()
    per = f"BETWEEN '{i}'::date AND '{f}'::date"
    return f"""
SELECT coalesce({col}, '(vazio)') AS dim,
  count(*) FILTER (WHERE {D_LEAD} {per})        AS leads,
  count(*) FILTER (WHERE {D_AGENDAMENTO} {per}) AS agendamento,
  count(*) FILTER (WHERE {D_REUNIAO} {per})     AS reuniao,
  count(*) FILTER (WHERE {D_FECHAMENTO} {per})  AS fechamento
FROM {join_atribuicao()}
WHERE {_escopo()}
GROUP BY 1
HAVING count(*) FILTER (WHERE {D_LEAD} {per}) > 0
    OR count(*) FILTER (WHERE {D_AGENDAMENTO} {per}) > 0
    OR count(*) FILTER (WHERE {D_REUNIAO} {per}) > 0
    OR count(*) FILTER (WHERE {D_FECHAMENTO} {per}) > 0
ORDER BY leads DESC, fechamento DESC, reuniao DESC
"""
