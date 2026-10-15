"""queries_portugal.py — fonte unica da logica das dashboards CM de Portugal.

As 3 marcas PT (Buzzmonitor, Cxpress, Elife) vivem no MESMO ActiveCampaign, com o
MESMO schema de 84 colunas e o MESMO dicionario de etapas. Por isso, ao contrario
de BR/LATAM/Cxpress — que divergiram em modulos separados e hoje precisam de
sincronia manual — aqui existe UM modulo so, parametrizado por marca.

Decisoes que vem da auditoria de 2026-09-09 (`dashboard/AUDITORIA-PORTUGAL.md`):

1. **Coorte por `cdate`.** Nenhum marco de funil tem data em PT: nao ha campo de
   data de reuniao nem de proposta, `data_de_fecho_do_negocio` esta preenchido em
   4 dos 669 deals de 2026, e nao existe historico de mudanca de etapa. A unica
   data 100% preenchida e `cdate`. Entao o periodo filtra os deals CRIADOS nele, e
   o painel mostra ate onde essa coorte chegou hoje.

2. **Etapa e ESTADO ATUAL, nao progressao.** Sem historico de etapa, nao da pra
   dizer que um deal hoje em "Perdidos" passou por "Reuniao". Logo o painel mostra
   a DISTRIBUICAO da coorte por etapa — nunca um funil de conversao entre etapas,
   que seria mentira. As secoes Reunioes e Fechamento (2026-10-15) seguem a mesma
   regra: fechamento = etapa atual Fecho de Negocio ou Cliente (o `status` nao
   entra); reuniao = etapa atual na Reuniao ou depois dela no pipeline, que e um
   piso (ver `chegou_reuniao`).

3. **CM e classificacao, nao filtro.** 21% a 50% dos deals de 2026 nao tem nenhum
   rastreio. Filtrar por CM esconderia metade da base sem avisar. Cada deal e
   classificado em `cm` / `nao_cm` / `sem_rastreio` e o painel mostra os tres.
"""
from __future__ import annotations

# ---------------------------------------------------------------- marcas

MARCAS = {
    "bm": {
        "nome": "Buzzmonitor Portugal",
        "tabelas": {
            "inbound": "deals_bm_inbound_portugal",
            "outbound": "deals_bm_outbound_portugal",
            "contratos": "deals_bm_contratos_portugal",  # vazia em 09/09/2026
        },
    },
    "cxpress": {
        "nome": "Cxpress Portugal",
        "tabelas": {
            "inbound": "deals_cxpress_inbound_portugal",
            "outbound": "deals_cxpress_outbound_portugal",
        },
    },
    "elife": {
        "nome": "Elife Portugal",
        "tabelas": {
            "inbound": "deals_elife_inbound_portugal",
            "outbound": "deals_elife_outbound_portugal",
        },
    },
}

ANO_INI = 2023  # a base comeca em 2023-01-10; exportamos tudo e o motor recorta

# ---------------------------------------------------------------- etapas

# `dim_stages_portugal` tem 66 etapas espalhadas por 9 pipelines, com o mesmo nome
# repetido em ids diferentes ("Iniciar Contato" e 1, 4, 29, 43, 52 e 55). Por isso
# o mapa e por TITULO normalizado, nunca por id.
ETAPAS_CANONICAS = [
    ("contato", "Contato"),
    ("material_rico", "Material Rico"),
    ("reuniao", "Reunião"),
    ("follow_up", "Follow-Up"),
    ("proposta", "Proposta"),
    ("negociacao", "Negociação"),
    ("fecho", "Fecho de Negócio"),
    ("cliente", "Cliente"),
    ("reciclagem", "Reciclagem"),
    ("stand_by", "Stand-By"),
    ("desqualificado", "Desqualificado"),
    ("perdido", "Perdido"),
    ("churn", "Churn"),
    ("outro", "Outro"),
]

# titulo (minusculo, sem acento tratado no SQL) -> chave canonica
MAPA_ETAPAS = {
    "iniciar contato": "contato",
    "tentando contato": "contato",
    "em contato": "contato",
    "review": "contato",
    "material rico": "material_rico",
    "reuniao": "reuniao",
    "follow-up": "follow_up",
    "follow up": "follow_up",
    "proposta": "proposta",
    "forecast/negociacao": "negociacao",
    "fecho de negocio": "fecho",
    "contrato": "cliente",
    "a formalizar contrato": "cliente",
    "clientes": "cliente",
    "reciclagem": "reciclagem",
    "stand-by": "stand_by",
    "desqualificado": "desqualificado",
    "perdidos": "perdido",
    "churn": "churn",
    "curso": "outro",
    "trial (buzzmonitor)": "outro",
    "trial": "outro",
}

# Etapas que significam "saiu do jogo" — nao entram no "em aberto".
ETAPAS_TERMINAIS = {"perdido", "desqualificado", "churn"}
# Etapas que significam negocio fechado. So a ETAPA conta: deal com `status`
# 'Ganho' parado em Proposta nao e fechamento (decisao Victor 2026-10-15 — o KPI
# antigo somava status e etapa e dava 7 "ganhos" com 3 deals em Fecho de Negocio).
ETAPAS_GANHAS = {"fecho", "cliente"}

# Etapas fora da linha principal do funil. Ficam de fora do "chegou a reuniao"
# mesmo quando o `stage_order` delas e maior que o da Reuniao (no pipeline 1,
# Perdidos, Desqualificado, Material Rico e Curso vem DEPOIS da Reuniao na ordem).
ETAPAS_LATERAIS = {
    "perdido", "desqualificado", "churn", "reciclagem", "stand_by",
    "material_rico", "outro",
}


def chegou_reuniao(etapa, ordem_etapa, ordem_reuniao):
    """True se a etapa ATUAL do deal fica na Reuniao ou depois dela no pipeline.

    Sem historico de etapa (auditoria §3.2), a unica prova de que houve reuniao e
    a posicao no funil: quem esta em Proposta, Negociacao ou Fecho passou pela
    Reuniao. A ordem vem do `stage_order` do proprio pipeline, porque ela muda de
    um pipeline pro outro — o Follow-Up vem ANTES da Reuniao no pipeline 1 e
    DEPOIS da Proposta nos pipelines 5 a 8.

    E um piso: deal que teve reuniao e hoje esta em Perdidos/Desqualificado nao
    entra, porque nada no CRM registra que ele passou por la.
    """
    if etapa in ETAPAS_GANHAS:
        return True  # inclui o pipeline 9 (pos-venda), que nao tem etapa Reuniao
    if etapa in ETAPAS_LATERAIS or ordem_etapa is None or ordem_reuniao is None:
        return False
    return ordem_etapa >= ordem_reuniao

# ---------------------------------------------------------------- rastreio CM

# Dominios que sao propriedade de conteudo (LP, blog, material). Vieram da
# auditoria — sao os que de facto aparecem em `url_conversao` nos deals PT.
# Repare que marca NAO se separa por dominio: deal da Cxpress converte em LP do
# Buzzmonitor e vice-versa. Isto aqui responde "e conteudo?", nao "de quem e?".
DOMINIOS_CONTEUDO = (
    "conteudo.getbuzzmonitor.com",
    "getbuzzmonitor.com",
    "buzzmonitor.pt",
    "material.buzzmonitor.com",
    "content.buzzmonitor.com",
    "conteudo.buzzmonitor.com.br",
    "cx.elifeportugal.com",
    "ai.elifeportugal.com",
    "chatbots.elifeportugal.com",
    "content.cxpress.io",
    "www.cxpress.pt",
    "cxpress.pt",
    "www.elifeportugal.com",
    "elifeportugal.com",
)

# utm_source que contam como Content Marketing (apos normalizar).
CM_UTM_SOURCES = {
    "meta", "google", "linkedin", "instagram", "facebook", "email",
    "activecampaign", "newsletter", "organic", "blog", "youtube", "tiktok",
}

# utm_source que NUNCA conta como CM, nem convertendo em dominio de conteudo:
# ChatGPT Ads (midia paga). 'chatgpt.com' (referral organico/GEO) nao e afetado.
# Decisao Victor 2026-10-08, vale pra todas as dashboards CM.
CM_UTM_SOURCES_EXCLUIR = {"chatgptads"}

# Lixo conhecido em utm_source — nao e fonte, e falha de tagueamento.
UTM_LIXO = {
    "{utm_source}", "{{site_source_name}}", "{{placement}}", "{campaign.name}",
    "test_source", "teste", "full", "an", "n/a", "null", "undefined", "-",
}

# Grafias diferentes da mesma fonte (chave = valor ja em minusculo).
UTM_SINONIMOS = {
    "fb": "meta", "facebook": "meta", "ig": "meta", "instagram": "meta",
    "facebook_mobile_feed": "meta", "instagram_feed": "meta", "fb_ig": "meta",
    "adwords": "google", "google_ads": "google", "googleads": "google", "gdn": "google",
    "ac": "activecampaign", "active_campaign": "activecampaign",
    "e-mail": "email", "mail": "email", "emkt": "email",
    "linked-in": "linkedin", "lnkd": "linkedin",
    "orgânico": "organic", "organico": "organic",
}


def normalizar_utm(valor):
    """Minuscula, tira espaco, resolve sinonimo e derruba lixo de tagueamento.

    Devolve None quando o valor nao serve como fonte (vazio, placeholder do Meta
    que nao resolveu, marcador de teste). O painel conta esses deals como
    'sem rastreio', que e o que eles sao na pratica.
    """
    if valor is None:
        return None
    v = str(valor).strip().lower()
    if not v or v in UTM_LIXO:
        return None
    # timestamps que vazaram pro campo (ex: '2023-03-06T12:24:15.394Z')
    if len(v) >= 20 and v[:4].isdigit() and "t" in v and v.endswith("z"):
        return None
    return UTM_SINONIMOS.get(v, v)


def dominio_de(url):
    """Extrai o dominio de `url_conversao`. Tolera valor que nao e URL.

    Em PT o campo as vezes traz o nome do formulario ('Formulário Cxpress'), nao
    um endereco — nesse caso devolve None, e o deal fica sem dominio mas ainda
    pode contar como rastreado pela UTM.
    """
    if not url:
        return None
    u = str(url).strip()
    if not u.lower().startswith(("http://", "https://")):
        return None
    resto = u.split("://", 1)[1]
    return resto.split("/", 1)[0].split("?", 1)[0].lower() or None


def caminho_de(url):
    """Path da url de conversao (sem query), pra ranquear LP. None se nao for URL."""
    if not dominio_de(url):
        return None
    resto = str(url).strip().split("://", 1)[1]
    path = ("/" + resto.split("/", 1)[1]) if "/" in resto else "/"
    return path.split("?", 1)[0].split("#", 1)[0] or "/"


def classificar(utm_source_norm, url_conv):
    """cm | nao_cm | sem_rastreio — a classificacao que o painel mostra.

    `cm` se a conversao aconteceu num dominio de conteudo OU se a utm_source e uma
    fonte de CM. `nao_cm` se ha rastreio mas nao aponta pra conteudo. `sem_rastreio`
    se nao ha nem UTM util nem URL de conversao — o buraco medido na auditoria
    (21,5% no Buzzmonitor, 49,8% na Cxpress, 13,2% no Elife em 2026).
    """
    dom = dominio_de(url_conv)
    tem_url = bool(str(url_conv).strip()) if url_conv else False
    if utm_source_norm in CM_UTM_SOURCES_EXCLUIR:
        return "nao_cm"
    if dom in DOMINIOS_CONTEUDO:
        return "cm"
    if utm_source_norm in CM_UTM_SOURCES:
        return "cm"
    if utm_source_norm or tem_url:
        return "nao_cm"
    return "sem_rastreio"


# ---------------------------------------------------------------- SQL

def _titulo_sem_acento(alias: str) -> str:
    """Titulo da etapa em minusculo e sem acento — a chave de MAPA_ETAPAS."""
    return (f"""lower(translate(coalesce({alias}."title_normalized", {alias}."title", ''),
             'áàâãäéèêëíìîïóòôõöúùûüçÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇ',
             'aaaaaeeeeiiiiooooouuuucAAAAAEEEEIIIIOOOOOUUUUC'))""")


# Colunas iguais nas 7 tabelas — projecao unica.
def q_deals(tabela: str, origem: str) -> str:
    """Uma linha por deal, com a etapa ja resolvida pelo titulo.

    Sem filtro de data: o motor.js recorta a coorte por `cdate` no navegador,
    igual as outras dashboards dinamica-estaticas.

    `ordem_etapa` e `ordem_reuniao` alimentam `chegou_reuniao()`: a posicao da
    etapa atual e a da etapa Reuniao no MESMO pipeline (`group_id`).
    """
    return f"""
SELECT d."id",
       d."title"                                  AS deal,
       d."cdate"::date                            AS d_criacao,
       d."mdate"::date                            AS d_modificacao,
       '{origem}'                                 AS origem,
       {_titulo_sem_acento('s')}  AS etapa_titulo,
       s."stage_order"                            AS ordem_etapa,
       (SELECT min(r."stage_order") FROM public."dim_stages_portugal" r
         WHERE r."group_id" = s."group_id"
           AND {_titulo_sem_acento('r')} = 'reuniao')  AS ordem_reuniao,
       d."status"                                 AS status,
       d."value"                                  AS valor,
       d."currency"                               AS moeda,
       d."utm_source"                             AS utm_source,
       d."utm_medium"                             AS utm_medium,
       d."utm_campaign"                           AS utm_campaign,
       d."url_conversao"                          AS url_conversao,
       d."owner"                                  AS owner_id,
       d."account_id"                             AS account_id
FROM public."{tabela}" d
-- `stage` no deal e TEXT ('1', '22'); `dim_stages_portugal.id` e bigint. Cast do
-- lado da dimensao (poucas linhas) pra nao perder indice na tabela de deals.
LEFT JOIN public."dim_stages_portugal" s ON s."id"::text = d."stage"
WHERE d."cdate" >= '{ANO_INI}-01-01'
"""


def q_todas(marca: str) -> list[tuple[str, str]]:
    """(sql, origem) para cada tabela da marca. Ignora a de contratos se vazia."""
    tabs = MARCAS[marca]["tabelas"]
    out = []
    for origem in ("inbound", "outbound"):
        if origem in tabs:
            out.append((q_deals(tabs[origem], origem), origem))
    return out
