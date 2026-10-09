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
    # --- superficies proprias de conteudo/webinar ONLINE (decisao Victor 2026-08-11) ---
    # Ultimo toque de material proprio: o deck exibido no webinar ao vivo
    # (Slides + Stream_en_vivo), a newsletter e o banner do site. Antes so passavam
    # quando a url_conversao carregava o dominio de conteudo — se a URL vinha vazia
    # (caso La Firma/43258), o lead sumia.
    # NAO inclui 'qr_code': QR e cracha de evento PRESENCIAL — ver ESCOPO abaixo.
    'slides', 'newsletter', 'sitio_web',
]

# utm_source de midia paga que NUNCA conta como CM — vale no wrapper externo do filtro,
# acima ate de URL_FORTE_CM e do sinal de origem propria (caso deal 66908, utm_source=
# 'chatgptads' em LP de conteudo, out/2026). 'chatgpt.com' (referral organico/GEO) segue
# na whitelist. Decisao Victor 2026-10-08, vale pra todas as dashboards CM.
CM_UTM_SOURCES_EXCLUIR_LATAM: list[str] = ['chatgptads']

# Campanhas proprias de conteudo/webinar: contam como CM pelo NOME da campanha,
# independente do utm_source do ultimo toque. Decisao Victor 2026-08-11 a partir do
# caso Oferta_Webinar_Social_Listening (leads que vieram do anuncio Meta -> LP do
# webinar -> deck do webinar; o utm_source gravado e o do deck, nao o do anuncio).
# Match ILIKE sobre lower(utm_campaign). Campanha de evento PRESENCIAL nao entra aqui.
CM_CAMPANHAS_LIKE: list[str] = [
    'oferta_%',          # Oferta_Webinar_Social_Listening, Oferta_Webinar_Monitoreo...
    '%webinar%',         # [LATAM][Webinar-*], invite_webinar_*, webinar_monitoreo*
    '%material+rico%',   # [LATAM]+[Material+Rico]+[IA] (URL-encoded)
    '%material rico%',
]

# Dominio proprio de conteudo da LATAM (contenido.getbuzzmonitor.com, getbuzzmonitor.com/es/...)
CONTENT_DOMAIN_LIKE = '%getbuzzmonitor.com%'

# Dominios das LPs proprias que aparecem em evento_conversao / contenido_conversao.
# Cobre conteudo.* (grafia PT) e getbuzzmonitor.com pelo mesmo padrao.
# `evento.buzzmonitor.com` NAO entra: e o dominio dos eventos PRESENCIAIS (Buzzmonitor
# Connect Bogota etc.), que sao de outra dashboard. Ver ESCOPO abaixo.
ORIGEM_DOMINIOS_PROPRIOS: list[str] = [
    '%getbuzzmonitor.com%',
    '%webinar.buzzmonitor.com%',
    '%material.buzzmonitor.com%',
    '%content.buzzmonitor.com%',
]

# ============ ESCOPO: conteudo + webinar ONLINE (nao evento presencial) ============
# Decisao Victor 2026-08-11. Esta dashboard mede Content Marketing — material rico,
# blog, estudos e **webinar online**. Evento PRESENCIAL (Cafe con Buzz, Merca2.0,
# BuzzTalks, Buzzmonitor Connect, Spark Summit) tem dashboard propria e NAO conta aqui,
# mesmo tendo LP no nosso dominio de conteudo.
#
# Auditoria que originou a regra (os 4 reprovados pelo Victor):
#   40128 New Athletic  USD 590 — cafe-con-buzz-peru-2026   (+ era Google Search)
#   39162 Smilehood     USD 605 — campanha BuzzTalks_Argentina
#   43197 TLP MX        USD 390 — merca20-mayo-2026
#   43484 News Monitor  USD 390 — cafe-con-buzz-peru-2026
#
# Marcadores casados contra a URL de origem **e** contra utm_campaign: a LP do BuzzTalks
# Argentina tem slug de conteudo (`social-listening-que-guia-decisiones-no-reportes`) e
# so se revela pelo nome da campanha. Slug sozinho nao basta.
EVENTO_PRESENCIAL_MARCADORES: list[str] = [
    '%buzztalk%',              # buzztalks-cdmx-2025, BuzzTalks_Argentina, Invite_BuzzTalks_Argentina
    '%cafe-con-buzz%',         # cafe-con-buzz, cafe-con-buzz-peru-2026
    '%cafeconbuzz%',           # CafeConBuzzmonitor_IAB_Peru (grafia da campanha)
    '%merca20%',               # merca20-mayo-2026, merca20-noviembre-2025
    '%merca-25%',              # merca-25-registro
    '%buzzmonitor-connect%',   # evento.buzzmonitor.com/buzzmonitor-connect-julio-2026-latam
    '%buzzconnect%',           # BuzzConnect_ActiveCampaign = convite do Buzzmonitor Connect Bogota
    '%spark%',                 # Spark Summit Colombia
    '%registro-evento%',       # registro-evento-colombia
    '%evento.buzzmonitor.com%',
]

# O marcador presencial desqualifica quando **e a conversao**, nao quando e so um toque
# lateral. Dois usos distintos, deliberadamente:
#   - em sinal_origem_propria(): derruba o sinal de origem (a LP presencial nao pode ser o
#     que faz o lead virar CM);
#   - no wrapper (4) do filtro: derruba pelo `utm_campaign`, porque a campanha e o que
#     gerou o lead (Invite_BuzzTalks_Argentina, CafeConBuzzmonitor_IAB_Peru, BuzzConnect_*).
# Nao aplicamos a `evento_conversao`/`url_conversao` no wrapper de proposito: o deal 43327
# (Preciso, campanha Oferta_Webinar_Social_Listening) converteu NO WEBINAR e so tem
# cafe-con-buzz como toque posterior — continua sendo CM. Mesmo caso do 42834
# ([LATAM][Remarketing] -> plataforma-completa, com buzztalk de toque lateral).

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
    # 2026-08-11: QA que so apareceu quando a regra de origem propria (1b) passou a
    # ler evento_conversao — os 4 tem LP nossa registrada e por isso entrariam no CM.
    # Contatos: teste@testando.com (42789), TestN8N_SOURCE/TestN8N_CAMPAIGN (42926),
    # test@test.com (66267), test2@test.com (66308).
    42789, 42926, 66267, 66308,
}

# Colunas necessarias para o funil (identicas em inbound, outbound e contratos).
# utm_campaign / evento_conversao / contenido_conversao entraram em 2026-08-11 — sao a
# materia-prima das regras de campanha propria e de sinal de origem (ver filtro_cm_latam).
_LEAD_COLS = (
    "id, title, cdate, mdate, status, pais, utm_source, utm_medium, utm_campaign, utm_content, "
    "url_conversao, evento_conversao, contenido_conversao, "
    "sdr, closer, fecha_de_primer_contacto, fecha_y_hora_de_primer_contacto, fecha_de_reunion, "
    "motivos_de_perdida"
)

# Colunas de atribuicao que o enriquecimento por contratos preenche quando o lead vem cego
# (ver _leads_subquery). O resto do funil (datas, status, dono) fica SEMPRE com a linha do lead.
_COLS_ATRIBUICAO = (
    "utm_source", "utm_medium", "utm_campaign", "utm_content",
    "url_conversao", "evento_conversao", "contenido_conversao",
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

def sinal_origem_propria(alias: str = '') -> str:
    """SQL: a origem do lead esta registrada numa LP propria (evento/webinar/material).

    `evento_conversao` e `contenido_conversao` guardam a URL do **primeiro toque** com a
    UTM completa (campanha, criativo e ate o adset), enquanto `url_conversao` costuma
    guardar so o ultimo toque — muitas vezes uma pagina comercial sem UTM nenhuma.
    Foi assim que o cierre da Agencia La Firma (deal 43258) ficou fora do CM ate
    2026-08-11: url_conversao = /es/freetrial/ sem UTM, com o anuncio Meta ->
    webinar.buzzmonitor.com/social-listening-mayo-2026-latam preservado no evento_conversao.

    Sinal restrito a DOMINIO proprio: essas duas colunas so aparecem preenchidas com LP
    nossa (contenido/conteudo.getbuzzmonitor.com, webinar.*), entao dominio basta e nao ha
    risco de arrastar trafego de terceiro.

    **E restrito ao escopo da dashboard: conteudo + webinar ONLINE.** LP de evento
    PRESENCIAL derruba o sinal, mesmo morando no dominio de conteudo — ver
    EVENTO_PRESENCIAL_MARCADORES. O marcador e testado tambem contra `utm_campaign`
    porque a LP do BuzzTalks Argentina tem slug de conteudo e so a campanha denuncia.
    """
    a = (alias + '.') if alias else ''
    ors = []
    for col in ('evento_conversao', 'contenido_conversao'):
        for dom in ORIGEM_DOMINIOS_PROPRIOS:
            ors.append(f"COALESCE({a}{col}, '') ILIKE '{dom}'")
    proprio = "(\n            " + "\n            OR ".join(ors) + "\n          )"

    presencial = []
    for marc in EVENTO_PRESENCIAL_MARCADORES:
        for col in ('evento_conversao', 'contenido_conversao', 'utm_campaign'):
            presencial.append(f"COALESCE({a}{col}, '') ILIKE '{marc}'")
    fora = "(\n            " + "\n            OR ".join(presencial) + "\n          )"

    return f"""(
          {proprio}
          AND NOT {fora}
        )"""


def filtro_cm_latam(alias: str = '') -> str:
    """SQL do filtro Content Marketing LATAM. `alias` prefixa as colunas (ex: 'd').

    Estrutura:
      (1) URL FORTE (plataforma-completa / oferta) => CM **independente da UTM**
          (sobrepoe ate google+cpc). Ver URL_FORTE_CM.
      (1b) SINAL DE ORIGEM PROPRIA em evento_conversao / contenido_conversao =>
          CM independente da UTM e da url_conversao. Restrito a conteudo/webinar
          ONLINE (evento presencial fica fora) e sem sobrepor Google Ads nem
          URLS_FORA_CM. Ver sinal_origem_propria().
      (2) Regra geral: exclui Google Ads (google/google_es + cpc) E exige
          dominio de conteudo OU fonte social/owned da whitelist OU campanha
          propria de evento/webinar/oferta (CM_CAMPANHAS_LIKE); E exclui URLs
          comerciais (planes / freetrial / personalizar-el-plan) que vem SEM UTM
          (null/vazia/'null' literal) — sem atribuicao = sem CM.
      (3) Wrapper externo: URLs fora de CM (URLS_FORA_CM, ex.: /buzzmonitor-institucional)
          — **salvo** quando ha sinal de origem propria (1b), porque nesse caso a
          institucional foi so o ultimo toque e a origem real esta registrada.
          Usa COALESCE pra nao derrubar deals com url_conversao IS NULL (NULL ILIKE =
          NULL = falsy no NOT).
    """
    a = (alias + '.') if alias else ''
    sources = ", ".join(f"'{s}'" for s in CM_UTM_SOURCES_LATAM)
    excluir = ", ".join(f"'{s}'" for s in CM_UTM_SOURCES_EXCLUIR_LATAM)
    url_forte = "\n      OR ".join(f"{a}url_conversao ILIKE '{p}'" for p in URL_FORTE_CM)
    urls_excluir = ", ".join(f"'{u}'" for u in URLS_COMERCIAIS_SEM_UTM_EXCLUIR)
    url_fora = "\n        OR ".join(f"COALESCE({a}url_conversao, '') ILIKE '{p}'" for p in URLS_FORA_CM)
    campanhas = "\n            OR ".join(
        f"lower(coalesce({a}utm_campaign,'')) LIKE '{p}'" for p in CM_CAMPANHAS_LIKE)
    origem = sinal_origem_propria(alias)
    campanha_presencial = "\n        OR ".join(
        f"COALESCE({a}utm_campaign, '') ILIKE '{m}'" for m in EVENTO_PRESENCIAL_MARCADORES)
    return f"""(
      (
        -- (1) sinal forte de URL — CM independente da UTM
        {url_forte}
        -- (1b) origem registrada em LP propria (evento/webinar/material).
        -- Diferente de (1), NAO sobrepoe a exclusao de Google Ads: uma campanha de Search
        -- que cai numa LP nossa continua sendo Ads, nao Content Marketing (decisao Victor
        -- 2026-08-11). Sem esta guarda, entravam ~muitas [CA]/[CH]/[CO][Search] all-time.
        OR (
          NOT (lower(coalesce({a}utm_source,'')) LIKE 'google%' AND lower(coalesce({a}utm_medium,'')) = 'cpc')
          AND {origem}
        )
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
            -- campanha propria de evento/webinar/oferta (ultimo toque pode ser o deck,
            -- o e-mail pos-webinar ou o QR do evento — a campanha e que identifica o CM)
            OR {campanhas}
          )
        )
      )
      -- (3) wrapper externo: URLs fora de CM sempre (independente de UTM ou de origem).
      -- O override por origem propria foi REVERTIDO em 2026-08-11: deixava entrar o deal
      -- 40128 (New Athletic), cuja url_conversao e a institucional com
      -- utm_source=google&utm_medium=cpc&utm_campaign=[LATAM][Search][Competencia-listening]
      -- (busca por "synthesio") — Google Ads, nao conteudo.
      AND NOT (
        {url_fora}
      )
      -- (4) escopo da dashboard: conteudo + webinar ONLINE. Campanha de evento PRESENCIAL
      -- (BuzzTalks, Cafe con Buzz, Merca2.0, Buzzmonitor Connect, Spark Summit) sai —
      -- tem dashboard propria. Decisao Victor 2026-08-11.
      AND NOT (
        {campanha_presencial}
      )
      -- (5) midia paga fora de CM sempre (ChatGPT Ads) — absoluto, acima de (1) e (1b).
      -- 'chatgpt.com' (organico/GEO) nao e afetado. Decisao Victor 2026-10-08.
      AND lower(trim(coalesce({a}utm_source,''))) NOT IN ({excluir})
    )"""


def _leads_subquery() -> str:
    """Subquery dos leads: inbound UNION outbound, **dedup SEMPRE por id** (nunca por UTM),
    depois **enriquecida** com a linha de mesmo id em `contratos`.

    Desempate quando o mesmo id aparece nas 2 tabelas (73 casos): fica com o registro
    mais COMPLETO (url/utm preenchidos) e, em empate, o mais recente. A chave de dedup
    e o id; completude e so criterio de desempate.

    **Enriquecimento por contratos (2026-08-11).** A mesma deal costuma existir nas duas
    pontas com preenchimento diferente: o deal 43258 (Agencia La Firma) esta 100% cego no
    inbound — utm_* e url_conversao todos NULL — enquanto a linha de contratos guarda
    url_conversao + evento_conversao com a UTM inteira do anuncio Meta que originou o lead.
    Como o filtro CM so lia inbound/outbound, esse rastro era jogado fora e o lead (que
    fechou USD 390) nunca contou como Content Marketing.

    O LEFT JOIN **so preenche buraco**: cada coluna de atribuicao fica com o valor do lead
    e cai pra contratos apenas quando o lead vem vazio. A populacao de leads nao muda
    (contratos nao entra como fonte de linhas novas) e nenhuma coluna de funil — data,
    status, dono — e tocada; essas seguem sendo as da linha do lead.

    Valores-lixo ('' e a string literal 'null', comuns na ponta de contratos) sao tratados
    como vazio nos DOIS lados, senao um 'null' textual venceria o COALESCE e mascararia o
    dado bom.
    """
    _excl = ", ".join(str(i) for i in sorted(DEALS_TESTE_EXCLUIR_LATAM))
    where_excl = f"WHERE id NOT IN ({_excl})" if _excl else ""

    def _limpo(expr: str) -> str:
        """'' e 'null' literal contam como ausente."""
        return f"NULLIF(NULLIF(TRIM({expr}), ''), 'null')"

    atrib = ",\n        ".join(
        f"COALESCE({_limpo('d.' + c)}, {_limpo('k.' + c)}) AS {c}" for c in _COLS_ATRIBUICAO)
    outras = [c.strip() for c in _LEAD_COLS.split(',')]
    outras = ",\n        ".join(f"d.{c}" for c in outras if c not in _COLS_ATRIBUICAO)

    return f"""(
      SELECT
        {outras},
        {atrib}
      FROM (
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
      ) d
      LEFT JOIN deals_latam_contratos_staging k ON k.id = d.id
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
        print("== Self-test LATAM (apos origem propria + enriquecimento por contratos + escopo"
              " conteudo/webinar 2026-08-11: ~5716 all-time, ~694 em 2026) ==")
        cur.execute(q_count_kpis(all_ini, all_fim)); a = cur.fetchone()
        print(f"  CM all-time: leads={a[0]} ce={a[1]} reunion={a[2]}")
        cur.execute(q_count_kpis(y_ini, y_fim)); y = cur.fetchone()
        print(f"  CM 2026:     leads={y[0]} ce={y[1]} reunion={y[2]}")
        # Definicao ampliada de fechado (2026-06-06): status='Ganho' OU pagamento/contrato/cierre
        # reais; valor pela coluna `value` (USD). Espera ~30 all-time CM (USD ~16.195) e ~4 em
        # 2026 (USD ~1.760). Em 2026-08-11 entrou 1 (La Firma, webinar) e sairam 2 de evento
        # presencial (Doblegiro/BuzzTalks_Chile, Pipe Toro/BuzzConnect).
        cur.execute(q_count_fechamentos(all_ini, all_fim)); fa = cur.fetchone()
        print(f"  Fechamentos CM all-time: {fa[0]} · USD {fa[1]}")
        cur.execute(q_count_fechamentos(y_ini, y_fim)); fy = cur.fetchone()
        print(f"  Fechamentos CM 2026:     {fy[0]} · USD {fy[1]}")
