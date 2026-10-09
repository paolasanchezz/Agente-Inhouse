"""queries_cxpress.py — queries SQL para a dashboard de **Content Marketing Cxpress Brasil**.

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

ESCOPO calibrado 2026-06-09 (auditoria utm_source/medium/url_conversao + validacao manual Victor):
- filtro_inbound: NO-OP (TRUE) — a dashboard conta deal CM independente de funil_auto, entao
  fechamento de OUTBOUND entra normalmente (reconfirmado por Victor em 2026-08-07). Em 2026 o
  escopo CM tem 557 deals Outbound contra 196 Inbound: o gate de canal e o filtro_cm(), nao o
  funil, porque funil_auto reflete o PROCESSO de vendas e nao a origem do lead. Ver filtro_inbound().
- filtro_cm: exclui Google Ads (google+cpc); inclui whitelist social/owned + URL clinicas/content.
- 2026-08-07: 'webinar' entrou na whitelist de utm_source (ver CM_UTM_SOURCES).
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


def _content(alias: str = 'd') -> str:
    """utm_content EFETIVO — coluna primeiro, fallback pro utm_content do querystring de url_conversao.

    A coluna utm_content chega NULL para a maior parte do trafego CM (Meta/IG): auditoria 2026-06-23
    achou 284 de 640 deals CM de 2026 com content SO na URL (renderizavam '—' na lista e caiam em
    '(vazio)' no ranking). Quando a coluna ESTA preenchida ela traz o rotulo curto do CRM (ex 'ad_03'),
    entao tem precedencia; so cai pro valor da URL (verboso, ex 'ad_01_estatico - Use o mesmo WhatsApp')
    quando a coluna esta vazia. O valor sai URL-encoded ('+' e %XX, inclusive em alguns valores da
    propria coluna) — a decodificacao acontece no render (render_helpers_cxpress._decode_content)."""
    a = (alias + '.') if alias else ''
    return (
        f"COALESCE("
        f"NULLIF(TRIM({a}utm_content), ''), "
        f"NULLIF(substring({a}url_conversao FROM 'utm_content=([^&]*)'), ''))"
    )


# ============ ESCOPO ============

def filtro_inbound(alias: str = '') -> str:
    """No-op — NAO filtra por funil_auto (espelha decisao Buzz BR 2026-05-19, aplicada a
    Cxpress em 2026-06-09 ao auditar o gap dashboard 5 vs Meta Ads 9 leads em 15d).

    O AC classifica sistematicamente leads de midia paga/conteudo como 'Outbound' — 393 deals
    com UTM CM em 2026, incluindo [RMKT] meta da LP clinicas — porque funil_auto reflete o
    PROCESSO de vendas (SDR move lead pra cadencia outbound), nao o canal de origem. O gate
    de canal da dashboard e o filtro_cm(). Para restringir por funil de novo, trocar o corpo
    por: a = (alias + '.') if alias else ''; return f"{a}funil_auto = 'Inbound'".
    """
    return "TRUE"


# Whitelist de utm_source CM (calibrada 2026-06-09 contra dados reais + validacao Victor).
# Inclui sources exatos. Prefixos compostos (instagram_feed, facebook_mobile_feed, newsletter+cxpress,
# linktree+cxpress, etc.) sao cobertos via LIKE no filtro_cm() abaixo.
# Excluidos explicitamente (decisao Victor): whatsapp, youtube — comportamento misto outbound/CM,
# tracking ruidoso. google+cpc tambem fora (Google Ads, nao CM).
#
# 'webinar' e 'qrcode-webinar-bloqueio-whatsapp' incluidos 2026-08-07 (decisao Victor) apos o deal
# 81535 'Grupo Calusa' (Ganho, fechamento 19/05/2026) nao aparecer como fechamento CM. A coluna
# utm_source chegou 'webinar' enquanto a url_conversao trazia a UTM real do anuncio:
# home.cxpress.io/bloqueio-whatsapp-comercial-como-evitar?utm_source=ig&utm_medium=cpc
# &utm_campaign=[meta][conversao][webinar][janeiro]&utm_creative=ad_04 — ou seja, trafego de
# Instagram Ads pra LP de conteudo. Que era defeito de preenchimento da COLUNA (e nao LP fora de
# escopo) ficou claro nos vizinhos: dos 44 deals de 2026 na mesma LP, 40 ja contavam como CM
# porque a coluna deles veio 'ig'/'meta'.
#
# Ambos valem INDEPENDENTE da URL de conversao (decisao Victor): UTM de webinar e 100% nossa —
# so o proprio time tagueia assim, nao ha origem externa que produza esse valor. Logo nao ha
# risco de falso positivo que justifique amarrar a source a uma LP de conteudo. Mesmo criterio ja
# vigente no Buzzmonitor BR desde 2026-06-22, que tem 'webinar', 'pos-webinar', 'webinar-ao-vivo'
# e 'apresentacao-webinar' na whitelist (queries.py:28-45).
#
# A exclusao de content.cxpress.io/webinar-tecnologia-maio2026 (CM_URLS_EXCLUIDAS_SEMPRE) segue valendo e
# nao conflita: ela barra a INSCRICAO como topo de funil, por URL, antes da whitelist de source —
# criterio de etapa do funil, nao de canal.
CM_UTM_SOURCES: list[str] = [
    'meta', 'ig', 'instagram', 'fb', 'facebook',
    'linkedin', 'email', 'blog', 'tiktok',
    'chatgpt.com', 'gemini', 'lp-agradecimento',
    'webinar', 'qrcode-webinar-bloqueio-whatsapp',
]

# utm_source de midia paga que NUNCA conta como CM — nem convertendo em URL de conteudo
# (CM_URL_PATTERNS deixaria passar: caso deal 89850, utm_source='chatgptads' em
# content.cxpress.io, out/2026). 'chatgpt.com' (referral organico/GEO) segue na whitelist.
# Decisao Victor 2026-10-08, vale pra todas as dashboards CM.
CM_UTM_SOURCES_EXCLUIR: list[str] = ['chatgptads']

# URLs de conteudo CM que entram independente de utm_source (caso o tracking nao tenha sido preservado).
# Atualizar conforme novas LPs/dominios de CM forem lancados.
CM_URL_PATTERNS: list[str] = [
    'https://home.cxpress.io/atendimento-para-clinicas%',  # LP CM (sem UTM) — confirmada Victor 2026-06-09
    'https://content.cxpress.io/%',                         # dominio de conteudo
    'https://conteudo.elife.com.br/%',                       # conteudo Elife historico (compartilhado)
]

# Sources de e-mail/newsletter PROPRIOS — canais 100% nossos (o disparo sai do nosso ESP, nenhuma
# origem externa produz esses valores). Por isso tem PRECEDENCIA sobre a exclusao de paginas internas
# (CM_URLS_EXCLUIDAS_SALVO_EMAIL): se o lead chegou por e-mail nosso, e CM mesmo que tenha convertido
# numa pagina de cadastro interno. Decisao Victor 2026-08-07 (ver Revisao na doc de mapeamento).
# NAO tem precedencia sobre CM_URLS_EXCLUIDAS_SEMPRE — topo de funil e criterio de ETAPA, nao de canal.
# 'newsletter' entra por prefixo no filtro (cobre Newsletter, newsletter+cxpress, newsletter_startups,
# newsletter+elife — 24 deals na base em 6 grafias).
CM_SOURCES_EMAIL_PROPRIO: list[str] = ['email']

# URLs excluidas SEMPRE — nunca contam, qualquer que seja o utm_source. Match ILIKE com %.
# Inscricao de webinar = topo de funil (precedente Buzz BR 2026-05-26: so a OFERTA conta). Sem isto,
# o lote de 123 inscricoes do webinar-tecnologia (01/jun, todas Outbound) inunda o funil. Como o
# critério aqui e ETAPA do funil (e nao canal), nem e-mail proprio fura esta lista.
CM_URLS_EXCLUIDAS_SEMPRE: list[str] = [
    'https://content.cxpress.io/webinar-tecnologia-maio2026%',
]

# URLs excluidas SALVO se a source for e-mail/newsletter proprio (CM_SOURCES_EMAIL_PROPRIO).
# Cadastro interno (home.cxpress.io/cadastro-interno[-bdr]) e funil de registro MANUAL/indicacao —
# a pagina tem 51 deals / 10 fechamentos, 43 deles via whatsapp, nenhum CM. Excluida desde
# 2026-06-15 por causa do deal 81723 'Destinando Viagens' (utm_source='email' sem nenhum outro
# parametro), que na epoca foi lido como e-mail comercial 1:1.
#
# 2026-08-07: Victor auditou o 81723 e confirmou que a origem E Content Marketing. Em vez de
# override nominal por deal_id, a regra virou estrutural a pedido dele — e-mail e newsletter
# proprios passam a valer nesta pagina tambem, hoje e no futuro. Efeito imediato: volta so o 81723
# (1 fechamento, R$ 129.000 no campo de fee, 03/02/2026); os 43 de whatsapp seguem fora, porque
# whatsapp nao esta na whitelist de sources. Nenhum deal 'newsletter*' converteu nessa pagina ainda.
CM_URLS_EXCLUIDAS_SALVO_EMAIL: list[str] = [
    'https://home.cxpress.io/cadastro-interno%',  # cobre /cadastro-interno e /cadastro-interno-bdr
]


def filtro_cm(alias: str = '') -> str:
    """Filtro Content Marketing — calibrado contra dados reais + validacao manual Victor 2026-06-09.

    Regras:
    1. Exclui Google Ads (google + cpc) e as sources pagas de CM_UTM_SOURCES_EXCLUIR
       (chatgptads) — esta segunda vale ate sobre CM_URL_PATTERNS.
    2. Exclui sources nao-CM (whatsapp, youtube, vtexday2026, Indicação, Ramal, ActiveCampaign, etc.)
       — implicitamente, por nao casar a whitelist nem os padroes LIKE.
    3. Inclui sources sociais/owned (CM_UTM_SOURCES) + variacoes case-insensitive com prefixos
       (instagram_feed, facebook_mobile_feed, newsletter+cxpress, linktree+cxpress, ...).
    4. Inclui URLs de conteudo CM (CM_URL_PATTERNS) mesmo sem utm_source.

    5. Exclui URLs de topo de funil (CM_URLS_EXCLUIDAS_SEMPRE): inscricao de webinar nunca e lead
       CM, qualquer que seja o utm_source — criterio de ETAPA do funil.
    6. Exclui URLs de pagina interna (CM_URLS_EXCLUIDAS_SALVO_EMAIL): cadastro interno / indicacao
       (registro manual) nao e conteudo — SALVO quando a source e e-mail/newsletter proprio
       (CM_SOURCES_EMAIL_PROPRIO), canal 100% nosso. Decisao Victor 2026-08-07 apos auditar o deal
       81723 'Destinando Viagens'. Aqui o criterio e CANAL, e o canal proprio ganha da pagina.

    COALESCE na exclusao de URL: sem ele, `NOT (NULL ILIKE x)` = NULL derruba do filtro
    qualquer lead com url_conversao vazia mesmo com utm_source valido (mesma classe do bug
    google/cpc do Buzz BR corrigido em 2026-05-26). Mesmo motivo pro COALESCE em utm_source na
    clausula de e-mail proprio: sem ele um deal de URL interna com source NULL viraria NULL em vez
    de FALSE e escaparia da exclusao.
    """
    a = (alias + '.') if alias else ''
    sources = ", ".join(f"'{s}'" for s in CM_UTM_SOURCES)
    email_sources = ", ".join(f"'{s}'" for s in CM_SOURCES_EMAIL_PROPRIO)
    excluir = ", ".join(f"'{s}'" for s in CM_UTM_SOURCES_EXCLUIR)
    url_clauses = "\n        OR ".join(f"{a}url_conversao ILIKE '{p}'" for p in CM_URL_PATTERNS)
    excl_sempre = "\n        OR ".join(
        f"COALESCE({a}url_conversao, '') ILIKE '{p}'" for p in CM_URLS_EXCLUIDAS_SEMPRE
    )
    excl_salvo_email = "\n          OR ".join(
        f"COALESCE({a}url_conversao, '') ILIKE '{p}'" for p in CM_URLS_EXCLUIDAS_SALVO_EMAIL
    )
    # TRUE quando o lead veio de e-mail/newsletter proprio — usado pra furar a exclusao de pagina interna.
    email_proprio = (
        f"(LOWER(COALESCE({a}utm_source, '')) IN ({email_sources})"
        f" OR LOWER(COALESCE({a}utm_source, '')) LIKE 'newsletter%')"
    )
    return f"""(
      NOT (LOWER(COALESCE({a}utm_source, '')) = 'google' AND LOWER(COALESCE({a}utm_medium, '')) = 'cpc')
      AND LOWER(TRIM(COALESCE({a}utm_source, ''))) NOT IN ({excluir})
      AND NOT (
        {excl_sempre}
      )
      AND NOT (
        (
          {excl_salvo_email}
        )
        AND NOT {email_proprio}
      )
      AND (
        LOWER({a}utm_source) IN ({sources})
        OR LOWER({a}utm_source) LIKE 'instagram%'
        OR LOWER({a}utm_source) LIKE 'facebook%'
        OR LOWER({a}utm_source) LIKE 'newsletter%'
        OR LOWER({a}utm_source) LIKE 'linktree%'
        OR {url_clauses}
      )
    )"""


def _escopo(alias: str = 'd') -> str:
    """Combina inbound + CM (ambos no-op por padrao). Use no WHERE das queries."""
    return f"({filtro_inbound(alias)}) AND ({filtro_cm(alias)})"


# ============ KPIs (7 do funil, contados pela data do evento) ============

def q_count_kpis(ini: date, fim: date) -> str:
    """Counts das 7 etapas no periodo. Cada metrica conta pela data do SEU evento.

    EXCECAO — Perdidos (definicao COORTE, igual Buzzmonitor BR q_count_perdidos):
    leads CRIADOS no periodo que terminaram como Perdido (lost + motivo preenchido
    + status = 'Perdido'). Datar pelo lost misturava coortes (deal de 2024 perdido hoje
    contava) e gerava % Perdidos > 100% no painel da secao 2. Coorte garante perd <= leads.

    status = 'Perdido' (estado FINAL) filtra deals reativados: o AC mantem data_do_lost_auto
    e motivo na linha quando um deal perdido e reaberto (caso Medprime 2026-06-09: lost 01/06,
    reativado 03/06 com demo marcada, status 'Aberta' — contava perdido e ativo ao mesmo tempo).
    Na base ha 25 'Aberta' + 4 'Ganho' com lost+motivo orfaos.
    """
    i, f = ini.isoformat(), fim.isoformat()
    return f"""
SELECT
  count(*) FILTER (WHERE d.{COL_LEAD}::date BETWEEN '{i}' AND '{f}') AS leads,
  count(*) FILTER (WHERE {_d('d.' + COL_TRIAGEM)} BETWEEN '{i}' AND '{f}') AS triagem,
  count(*) FILTER (WHERE {_d('d.' + COL_AGENDAMENTO)} BETWEEN '{i}' AND '{f}') AS agendamento,
  count(*) FILTER (WHERE {_d('d.' + COL_DEMO)} BETWEEN '{i}' AND '{f}') AS demo,
  count(*) FILTER (WHERE {_d('d.' + COL_PROPOSTA)} BETWEEN '{i}' AND '{f}') AS proposta,
  count(*) FILTER (WHERE {_d('d.' + COL_FECHAMENTO)} BETWEEN '{i}' AND '{f}') AS fechamento,
  count(*) FILTER (WHERE d.{COL_LEAD}::date BETWEEN '{i}' AND '{f}'
                     AND {_d('d.' + COL_LOST)} IS NOT NULL
                     AND NULLIF(TRIM(d.motivo_de_perda_closer_sdr), '') IS NOT NULL
                     AND d.status = 'Perdido') AS perd
FROM {TABELA} d
WHERE {_escopo('d')}
"""


# ============ LISTAS DE DEALS ============

def q_lista_leads(ini: date, fim: date) -> str:
    return f"""
SELECT d.id, d.title AS deal, d.utm_source, {_content('d')} AS utm_content,
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
SELECT d.id, d.title AS deal, d.utm_source, {_content('d')} AS utm_content,
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
SELECT d.id, d.title AS deal, d.utm_source, {_content('d')} AS utm_content,
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
SELECT d.id, d.title AS deal, d.utm_source, {_content('d')} AS utm_content,
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
SELECT d.id, d.title AS deal, d.utm_source, {_content('d')} AS utm_content,
       {COL_RESP} AS responsavel,
       {_d('d.' + COL_FECHAMENTO)} AS data_evento,
       {COL_VALOR} AS valor_text, d.currency
FROM {TABELA} d
WHERE {_d('d.' + COL_FECHAMENTO)} BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {_escopo('d')}
ORDER BY {_d('d.' + COL_FECHAMENTO)}
"""


def q_lista_perdidos(ini: date, fim: date) -> str:
    """Perdidos (definicao COORTE, igual Buzzmonitor BR q_lista_perdidos):
    leads CRIADOS no periodo que terminaram como Perdido, com motivo preenchido e
    status = 'Perdido' (estado final — deals reativados/ganhos com lost orfao ficam fora).
    Ordenado pela data da perda (mais recente primeiro)."""
    return f"""
SELECT d.id, d.title AS deal, d.utm_source, {_content('d')} AS utm_content,
       d.motivo_de_perda_closer_sdr AS motivo,
       d.etapa_do_lost AS etapa,
       {_d('d.' + COL_LOST)} AS data_evento,
       COALESCE({_d('d.' + COL_DEMO)}, {_d('d.' + COL_AGENDAMENTO)},
                {_d('d.' + COL_TRIAGEM)}, d.{COL_LEAD}::date) AS ultima_conversao
FROM {TABELA} d
WHERE d.{COL_LEAD}::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {_d('d.' + COL_LOST)} IS NOT NULL
  AND NULLIF(TRIM(d.motivo_de_perda_closer_sdr), '') IS NOT NULL
  AND d.status = 'Perdido'
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
    # utm_content usa o valor EFETIVO (coluna + fallback URL); utm_source agrupa direto.
    dim_expr = _content('') if dim == 'utm_content' else dim
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
  COALESCE({dim_expr}, '(vazio)') AS dim,
  {fl[0]} AS leads,
  {fl[1]} AS triagem,
  {fl[2]} AS agendamento,
  {fl[3]} AS demo,
  {fl[4]} AS proposta,
  {fl[5]} AS fechamento
FROM base
GROUP BY {dim_expr}
HAVING {fl[0]} > 0 OR {fl[1]} > 0 OR {fl[2]} > 0 OR {fl[3]} > 0 OR {fl[4]} > 0 OR {fl[5]} > 0
ORDER BY leads DESC, fechamento DESC, demo DESC
"""


def q_source_por_content(ini: date, fim: date) -> str:
    """Mapa utm_content -> utm_source dominante no periodo (colorir o badge no ranking de content)."""
    esc = _escopo('d')
    return f"""
SELECT COALESCE({_content('')}, '(vazio)') AS utm_content,
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
