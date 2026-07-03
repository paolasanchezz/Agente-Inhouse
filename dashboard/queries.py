"""queries.py — queries SQL parametrizadas para a dashboard de Content Marketing.

Espelha a especificacao em dashboard/MAPEAMENTO-CAMPOS.md.

Regras universais aplicadas:
- Filtro CM (utm_source + url_conversao em whitelist) — §2 do mapeamento
- Regra 90d pos-conversao — §3 do mapeamento
- Contagem por data do EVENTO, nao data de criacao do deal — §4

Whitelist/blacklist de emails sao constantes inline (3 emails no total).
Quando crescer, migrar pra tabelas cm_email_whitelist / cm_email_blacklist no banco.

NOTA SOBRE INDICES (DBA deve criar quando latencia apertar):
  CREATE INDEX idx_deals_comercial_account_cdate ON deals_comercial_prod (account_id, cdate);
  CREATE INDEX idx_deals_comercial_agendamento ON deals_comercial_prod (data_agendamento_auto);
  CREATE INDEX idx_deals_comercial_realizada ON deals_comercial_prod (data_inicio_reuniao_realizada);
  CREATE INDEX idx_deals_comercial_proposta ON deals_comercial_prod (data_envio_proposta_auto);
  CREATE INDEX idx_deals_comercial_perdido ON deals_comercial_prod (data_negocio_perdido_auto);
  CREATE INDEX idx_deals_contratos_account_fech ON deals_contratos_prod (account_id, data_fechamento_auto);
"""
from __future__ import annotations

from datetime import date, timedelta


# ============ CONSTANTES ============

CM_UTM_SOURCES: list[str] = [
    'meta', 'lp-agradecimento', 'ig', 'instagram', 'linkedin', 'notion', 'email',
    'checklist', 'whatsapp', 'pos-webinar', 'sms', 'webinar-ao-vivo',
    'apresentacao-webinar', 'lp-agradecimento-oferta-trends',
    'lp-agradecimento-evento', 'tiktok', 'chatgpt.com', 'gemini', 'blog',
    # Variantes adicionadas 2026-06-22 (auditoria lista colab 13-19/jun):
    # typos/variantes de utm que sao CM legitimos mas escapavam do filtro.
    # Origem provavel: lancamento de campanha sem padronizar o utm na origem.
    # NOTA: 'redes-sociais' foi tentado mas REMOVIDO no mesmo dia — Victor
    # confirmou que esse source NAO eh usado em CM (era CS tagueando expansoes
    # de cliente como utm_source=redes-sociais&utm_content=cs). 5 fechamentos
    # YtD apareceram falsamente como CM via essa variante; um deles (Fabrika,
    # deal 183535) eh CM legitimo confirmado e entrou na EMAIL_WHITELIST.
    'apresentacao', 'webinar', 'newsletter',
    'Instagram_Feed', 'Instagram_Stories',
    'insta-bio',  # link da bio do Instagram (Victor confirmou CM, 2026-07-01)
]

INTERNOS_EXCLUIR: list[str] = ['cs', 'comercial', 'sdr', 'crm', 'google']

# Sources que NAO bloqueiam a heranca de atribuicao 90d (touchpoint interno do
# time, nao origem de aquisicao — ex: re-conversao via link mandado pelo SDR,
# caso mariacristina/l3ft deal 181112). 'google' fica de fora DE PROPOSITO:
# deal google/cpc tem origem propria de midia alternativa e nao deve herdar
# atribuicao CM (decisao Victor 2026-07-02; casos agencialcm 176001,
# xconexoes 168636 e mind.digital 172460 na auditoria da lista de 51).
HERANCA_SOURCES_INTERNAS: list[str] = ['cs', 'comercial', 'sdr', 'crm']

# Filtro de funil (REATIVADO 2026-07-01; CAMPO corrigido 2026-07-02, Victor):
# Historico: no-op "TRUE" de 2026-05-19 ate 2026-07-01. Em 2026-07-01 passou a REMOVER
# o funil 'Outbound'. Em 2026-07-02 o CAMPO mudou de funil_inicial_lead_auto (classif.
# inicial AUTO — vazia em ~metade dos deals e fora de sincronia com o CRM) para
# funil_bd_sdr, o campo CURADO pelo time = "Funil [BD e SDR]" no ActiveCampaign
# (ex: deal 190191 auto=Outbound mas bd_sdr=Inbound; 175702 auto=NULL mas bd_sdr=Outbound).
# Mantem na dashboard:
#   - Inbound
#   - nao-classificados (funil_bd_sdr vazio/NULL)
#   - os emails da EMAIL_WHITELIST (Victor confirmou CROP e NEIVA como CM apesar de
#     Outbound no CRM; a whitelist tem PRECEDENCIA e sobrevive a este filtro).
#
# COBERTURA: esta funcao entra nas queries de EVENTO (CE/RA/RR/Proposta), Fechamentos
# (ramo nao-whitelist), rankings e serie temporal. As queries leads-style (Leads,
# Perdidos, leads_p do ranking, serie-leads, source_por_content) NAO chamam esta
# funcao — usam o helper _sem_outbound(), de mesma semantica.
# COALESCE(TRIM(...),'') trata funil NULL/vazio como != 'Outbound' (mantido).
def filtro_inbound(alias: str = '') -> str:
    """Exclui funil 'Outbound', preservando Inbound, nao-classificados e whitelist.

    `alias` prefixa as colunas pra uso em queries com JOIN (ex: filtro_inbound('d')).
    A clausula de whitelist usa VALUES inline (self-contained) porque nem toda query
    de evento define a CTE `wl` (ex: q_count_evento, q_proporcao_sources_12m).
    """
    p = f"{alias}." if alias else ""
    wl = _sql_email_list(EMAIL_WHITELIST)
    return f"""(
    COALESCE(TRIM({p}funil_bd_sdr), '') <> 'Outbound'
    OR lower(trim({p}email_contato_principal_bd_sdr)) IN ({wl})
  )"""


def _sem_outbound(alias: str = '') -> str:
    """Predicado leads-style: exclui funil 'Outbound' preservando emails whitelisted.

    Mesma semantica de filtro_inbound(), mas para as queries que NAO passam por ela
    (Leads, Perdidos, leads_p, serie-leads, source_por_content). Referencia a CTE `wl`
    ja presente nessas queries (evita reinjetar a lista inteira de emails inline).
    """
    p = f"{alias}." if alias else ""
    return (
        f"(COALESCE(TRIM({p}funil_bd_sdr), '') <> 'Outbound' "
        f"OR lower(trim({p}email_contato_principal_bd_sdr)) IN (SELECT email FROM wl))"
    )

# Override manual (overrides §2 do mapeamento)
EMAIL_WHITELIST: list[str] = [
    'jessica.rua@wealthmoney.com.br',     # Wealth — converteu via blog, tracking nao preservou
    'ronaldozottolo@gmail.com',           # Agencia CROP — Outbound no CRM, mas CM confirmado pelo Victor
    'equipelarissaneiva@gmail.com',       # NEIVA Brand — Outbound no CRM mas CM confirmado pelo Victor
    'm.lima@blankschool.com.br',          # BlankSchool — funil Inbound mas sem UTM/URL (tracking falhou)
    'para.fabianogomes@gmail.com',        # Fabiano Gomes — re-conversao apos lead CM original (meta+blog em jan/2026)
    'desenvolvimento@marvitubos.com.br',  # Marvi Tubos — converteu na oferta webinar Analise Preditiva 26/05, tracking veio NULL (sem URL/UTM)
    'catherine.nobrega@fabrikadecriacao.com.br',  # Fabrika (deal 183535) — fech 19/03 utm=google/monitoramento_social_media; CM confirmado pelo Victor (2026-06-22)
    # Adicionados 2026-07-02 (auditoria lista 51): lead comercial veio com tracking
    # vazio, mas a conversao real e CM (o registro de contratos guarda a UTM boa).
    'mariangela.vale@drconsulta.com',     # deal 186090 — comercial sem UTM (url=home); contrato = webinar conteudo-que-converte
    'aline.ranielle@gmail.com',           # deal 186979 — comercial sem UTM/URL; contrato = blog monitoramento-politico
]

EMAIL_BLACKLIST: list[str] = [
    'julianacastro@idwcompany.com.br',        # IDW — Google Ads em outra ferramenta
    # Outbound reclassificados pelo Victor (CRM marca Inbound mas operacionalmente sao Outbound).
    # Saem da dashboard principal; entrarao em futura pagina "Impacto de Conteudo".
    'valdofmendes@gmail.com',                 # Webinar Analise Preditiva
    'raissaboniolo.consultoria@gmail.com',    # Buzzcreators evento
    # Adicionados 2026-05-26 (apos fix do bug NULL no filtro CM):
    'stella.santana@parceiros-npx.com.br',    # NUPIXEL — lead original Gisele era Google CPC, contrato veio com URL CM mas origem nao-CM
    'teste@teste.com',                        # Teste obvio
    'thamires.oliveira@buzzmonitor.com.br',   # Email interno Buzzmonitor
    'albali@elife.com.br',                    # Email interno Elife
    # Adicionados 2026-06-06 (Victor): emails de teste/webhook/CRM que poluiam a dashboard.
    # Retirados nominalmente (nao por regra heuristica) pra evitar falso positivo em lead real.
    'teste@webhook123.com',
    'disparo@webhook.com',
    'teste@conteudourl.com',
    'teste@muniquecrm.com',
    'munique@activecampaignteste.com',
    'munique@testecrmlink.com',
    'victorlopes.gestao@cxpress.com',
    'teste@webhook.com',
    'teste@webhook04.com',
    'teste@utmdea.com',
    'teste@blogmkt.com',
    'teste@leadblogurldiferente.com',
    'teste@utmgenertor.com',
    'teste@webhooklsksks.com',
    # Adicionado 2026-06-22 (auditoria lista colab): deal de teste vazando.
    'muniquebuzz@monitor.com',                # deal 189845 — title "teste crm"
    # Adicionado 2026-06-30 (Victor): deal 186199 ECHEF ROBOT entrou como CM por bug de
    # tracking (URL de conversao trouxe utm Instagram_Feed/cpc), mas e lead de EVENTO
    # (origem_lead_bd e origem_negocio_inbound = "Evento"). Reclassificado: sai do CM.
    'roni@saldaodainformatica.com.br',        # deal 186199 — falso CM, lead de evento
    # Adicionado 2026-07-02 (auditoria lista 51): email interno Buzzmonitor num deal
    # de 2023 somava Reuniao Realizada via heranca de atribuicao por conta.
    'ana.costa@buzzmonitor.com.br',           # deal 73393 — interno Buzzmonitor
    'leandra.lira@buzzmonitor.com.br',        # deal 187029 (TIRIVA) — deal de cliente cadastrado com email interno como contato principal; herdava eventos de conversao da propria funcionaria
]

# Exclusao cirurgica de deals por URL + data (incidentes pontuais de tracking).
# Diferente da EMAIL_BLACKLIST (que bane o email pra sempre, em qualquer campanha),
# isto remove apenas deals que casam URL + intervalo de datas — o mesmo email volta
# a contar normalmente em conversoes futuras.
DEALS_EXCLUIDOS_URL_DATA: list[dict] = [
    {
        # Webinar Analise Preditiva: inscricao NUNCA vira lead CM (decisao Victor 2026-05-26).
        # A pagina de inscricao (webinar.buzzmonitor.com/analise-preditiva-maio-2026) e topo
        # de funil — nao deveria gerar deal. So a OFERTA
        # (conteudo.buzzmonitor.com.br/oferta-webinar-analise-preditiva-na-pratica) conta como CM.
        # Sem chave 'datas' => exclui qualquer data. (Originou de falha de lote em 25/05 e 06/03,
        # mas a decisao final foi excluir todas as inscricoes, nao so os lotes.)
        'url_like': 'https://webinar.buzzmonitor.com/analise-preditiva-maio-2026%',
    },
]

# Reconversoes manuais (deal_id -> data efetiva da nova conversao).
# Quando um lead CM reconverte de verdade mas o CRM so EDITA o deal antigo (nao gera
# deal novo), o cdate fica preso na data original. Este override recoloca o LEAD na
# data real da reconversao. Afeta SO a metrica de Leads (q_count_leads / q_lista_leads);
# os eventos de funil (CE/RA/proposta) permanecem nas datas reais, e a serie temporal
# 12m nao reflete o override (1 lead nao muda a forma do grafico — limitacao aceita).
# MANUTENCAO: REMOVER a entrada quando o pipeline AC->Supabase passar a gerar deal novo
# em reconversao, senao conta duplicado (deal novo + override).
RECONVERSOES_MANUAIS: dict[int, str] = {
    183266: '2026-05-26',  # Karol/Cely — reconverteu na oferta webinar; CRM so editou o deal de 09/mar. Mover (Victor 2026-05-27).
}

# Deals confirmados como CM pelo Victor que o criterio automatico NAO captura.
# Caso tipico: o lead converteu numa pagina de oferta CM, mas o CRM criou um DEAL
# NOVO sem UTM/URL, em account_id diferente e/ou fora da janela de 90d — entao nem
# o EXISTS por conta nem a auto-atribuicao por account NULL o pegam.
# Este override force-inclui os EVENTOS do deal (CE/RA/RR/Proposta) como CM,
# ignorando account-join e janela 90d. NAO afeta Leads (o lead original ja conta
# pela conversao CM real) NEM Fechamentos (gate §7 — override de fechamento e via
# EMAIL_WHITELIST). Override nominal, nao heuristico — mesma filosofia da
# EMAIL_WHITELIST / RECONVERSOES_MANUAIS. So aplica a deals_comercial_prod.
CM_DEALS_FORCADOS: dict[int, str] = {
    189715: 'Assembleia Legislativa do MA — contato converteu na oferta webinar relatorios-estrategicos (deal 180841); CRM criou deal novo sem UTM, conta diferente, +108d. CM confirmado (Victor 2026-06-15).',
    # 175702 (PiU Comunica) REMOVIDO de CM_DEALS_FORCADOS 2026-07-02 — Victor confirmou
    # Outbound. Com o filtro por funil_bd_sdr (=Outbound neste deal) ele ja sai sozinho;
    # manter o override forcaria os eventos indevidamente. NAO esta na EMAIL_BLACKLIST: o
    # mesmo contato (robertapuri@piucomunica.com.br) tem o deal 190191, bd_sdr=Inbound, que DEVE contar como CM.
}


def _cdate_efetivo(id_col: str = 'id', cdate_col: str = 'cdate') -> str:
    """SQL do cdate efetivo aplicando RECONVERSOES_MANUAIS.

    Retorna cdate_col puro se nao ha overrides; senao um CASE que troca a data
    dos deals listados pela data manual da reconversao.
    """
    if not RECONVERSOES_MANUAIS:
        return cdate_col
    cases = ' '.join(
        f"WHEN {id_col} = {did} THEN '{data}'::timestamptz"
        for did, data in RECONVERSOES_MANUAIS.items()
    )
    return f"(CASE {cases} ELSE {cdate_col} END)"


# Slugs CM na URL conteudo.buzzmonitor.com.br (whitelist)
CM_SLUGS_PREFIXES: list[str] = [
    'plataforma-completa',
    'monitoramento-de-redes-sociais-2',
    'oferta-',
    'conteudo-que-converte',
    'webinar-',
    'report-trends-',
    'masterclass-trends-',
    'gestao-de-crises-',
    'relatorios-estrategicos',
    'buzz-talks-',
    'buzztalk-',
    # 'buzzmonitor-connect-' REMOVIDO 2026-07-02 (Victor, auditoria lista 51):
    # paginas Connect (atendimento/relacionamento) sao produto, nao conteudo CM.
    # Derrubou grace/fatecie (deals 171932/172176) e o gatilho do contrato
    # luis.ferreira/BS2 (deal 178072).
]

# Colunas-data dos eventos no funil
COLUNA_EVENTO = {
    'leads': 'cdate',
    'ce':    'data_efetividade_contato_auto',
    'ra':    'data_agendamento_auto',
    'rr':    'data_inicio_reuniao_realizada',
    'prop':  'data_envio_proposta_auto',
    'perd':  'data_negocio_perdido_auto',
    # fech vive em deals_contratos_prod
    'fech':  'data_fechamento_auto',
}


# ============ HELPERS DE FORMATACAO SQL ============

def _sql_list(items: list[str]) -> str:
    """['a','b','c'] -> "'a', 'b', 'c'"""
    return ", ".join(f"'{s}'" for s in items)


def _sql_email_list(emails: list[str]) -> str:
    """Lista de emails em VALUES inline pra SELECT email FROM (VALUES (...))."""
    if not emails:
        # truque pra retornar zero linhas sem quebrar sintaxe
        return "SELECT ''::text WHERE FALSE"
    rows = ", ".join(f"('{e.lower().strip()}')" for e in emails)
    return f"SELECT lower(trim(email)) AS email FROM (VALUES {rows}) AS t(email)"


def _sql_exclusao_deals(alias: str = '') -> str:
    """Clausula SQL que exclui deals casando URL + data de DEALS_EXCLUIDOS_URL_DATA.

    Retorna 'TRUE' (no-op) se a lista estiver vazia. Aceita `alias` opcional para
    prefixar as colunas (url_conversao, cdate) quando aplicada em query com JOIN —
    mesmo contrato do filtro_cm(). Sem alias, gera SQL byte-identico ao anterior.

    COALESCE(url_conversao, '') protege contra url_conversao NULL: sem ele,
    `NULL ILIKE '...'` retorna NULL e o `NOT (...)` propaga NULL no WHERE,
    derrubando do filtro CM QUALQUER lead com URL vazia — mesmo com utm_source
    valido (ex: 'meta'). Mesma classe do bug google/cpc corrigido em 2026-05-26.
    """
    p = f"{alias}." if alias else ""
    if not DEALS_EXCLUIDOS_URL_DATA:
        return "TRUE"
    clauses = []
    for d in DEALS_EXCLUIDOS_URL_DATA:
        datas = d.get('datas')
        if datas:
            datas_sql = ", ".join(f"'{dt}'" for dt in datas)
            clauses.append(f"(COALESCE({p}url_conversao, '') ILIKE '{d['url_like']}' AND {p}cdate::date IN ({datas_sql}))")
        else:
            # Sem datas => exclui qualquer data que case a URL.
            clauses.append(f"(COALESCE({p}url_conversao, '') ILIKE '{d['url_like']}')")
    return "NOT (" + " OR ".join(clauses) + ")"


# ============ FILTRO CM UNIVERSAL ============

def filtro_cm(alias: str = '') -> str:
    """
    Retorna a string SQL do filtro Content Marketing universal.

    `alias` opcional prefixa as colunas (utm_source, utm_medium, url_conversao)
    para uso em queries com JOIN — ex: filtro_cm('d') gera `d.utm_source IN (...)`.
    Sem alias, aplica em WHERE onde as colunas nao sao ambiguas e gera SQL
    byte-identico ao anterior.

    Espelha §2 do MAPEAMENTO-CAMPOS.md.
    """
    p = f"{alias}." if alias else ""
    sources = _sql_list(CM_UTM_SOURCES)
    internos = _sql_list(INTERNOS_EXCLUIR)
    exclusao = _sql_exclusao_deals(alias)
    slugs_clauses = "\n          OR ".join(
        f"{p}url_conversao ILIKE 'https://conteudo.buzzmonitor.com.br/{slug}%'"
        for slug in CM_SLUGS_PREFIXES
    )
    return f"""(
    {exclusao}
    AND NOT (COALESCE({p}utm_source, '') = 'google' AND COALESCE({p}utm_medium, '') = 'cpc')
    AND (
      {p}utm_source IN ({sources})
      OR {p}url_conversao ILIKE 'https://buzzmonitor.com/blog/%'
      OR {p}url_conversao ILIKE 'https://buzzmonitor.com.br/blog/%'
      OR {p}url_conversao ILIKE 'https://material.buzzmonitor.com/%'
      OR {p}url_conversao ILIKE 'https://evento.buzzmonitor.com/%'
      OR (
        ({p}utm_source IS NULL OR {p}utm_source NOT IN ({internos}))
        AND (
          {slugs_clauses}
        )
      )
    )
  )"""


def _sql_cm_deals_forcados(alias: str = 'd') -> str:
    """Clausula SQL TRUE quando o deal esta em CM_DEALS_FORCADOS (override de
    evento, so comercial). Retorna 'FALSE' (no-op em OR) se a lista estiver vazia."""
    if not CM_DEALS_FORCADOS:
        return "FALSE"
    p = f"{alias}." if alias else ""
    ids = ", ".join(str(i) for i in CM_DEALS_FORCADOS)
    return f"{p}id IN ({ids})"


def _atrib_cm_90d(col: str, alias: str = 'd') -> str:
    """Predicado SQL de atribuicao CM com janela de 90 dias pos-conversao.

    Desde 2026-07-02 (Victor) a atribuicao e por CONTATO (email), nao mais por
    CONTA. Auditoria da lista de 51 leads mostrou que a heranca por conta so
    capturava ruido (deal de 2021 ressuscitado via conversao de colega, email
    interno, google/cpc de carona, cadastros duplicados) e NENHUM caso que o
    time reconhece como CM. Ramos, em ordem:

    1. OVERRIDE NOMINAL (CM_DEALS_FORCADOS) — mantido; so tabela comercial.

    2. HERANCA POR CONTATO — o evento conta se o MESMO email teve conversao CM
       ate 90d antes (inclui o registro-irmao do proprio deal em contratos, que
       carrega a UTM quando o tracking do comercial falha). GUARDA DE ORIGEM:
       deal com utm_source proprio de midia nao-CM (ex: google/cpc) NAO herda —
       a origem dele e conhecida e nao e CM (casos agencialcm/xconexoes/mind).
       Sources internas (HERANCA_SOURCES_INTERNAS) nao bloqueiam: re-conversao
       via link do time e touchpoint do MESMO lead CM (caso mariacristina/l3ft).
       Deals sem email nao herdam (nao ha de quem).

    3. AUTO-ATRIBUICAO — o proprio deal e CM (filtro_cm) e o evento esta a ate
       90d da propria conversao. Generaliza o antigo ramo account_id NULL
       (2026-06-15): continua cobrindo leads individuais sem empresa e passa a
       cobrir tambem deal CM sem email (que a CTE por contato nao contem).

    GRANULARIDADE ::date mantida (fix 2026-06-15): colunas de evento sao gravadas
    a meia-noite enquanto cdate tem hora real; comparar em timestamp cru derrubava
    eventos do mesmo dia da conversao (~28 RAs YtD 2026). Alinhado a §6.

    `col` = coluna-data do evento; `alias` = alias da tabela na query externa.
    Fechamentos (deals_contratos_prod) usam alias 'ct'. Requer a CTE
    `conversoes_cm` no WITH da query (cte_conversoes_cm).
    """
    a = alias
    fcm = filtro_cm(a)
    # Override nominal so p/ comercial (ct = fechamentos nao muda — gate §7 intacto).
    forcado = "FALSE" if a == "ct" else _sql_cm_deals_forcados(a)
    internas = _sql_list(HERANCA_SOURCES_INTERNAS)
    return f"""(
    {forcado}
    OR (
      (COALESCE({a}.utm_source, '') IN ('', {internas}) OR {fcm})
      AND {a}.email_contato_principal_bd_sdr IS NOT NULL
      AND EXISTS (
        SELECT 1 FROM conversoes_cm cm
        WHERE cm.email_conv = lower(trim({a}.email_contato_principal_bd_sdr))
          AND cm.data_conv::date <= {a}.{col}::date
          AND {a}.{col}::date - cm.data_conv::date <= 90
      )
    )
    OR (
      {fcm}
      AND {a}.cdate::date <= {a}.{col}::date
      AND {a}.{col}::date - {a}.cdate::date <= 90
    )
  )"""


def predicado_evento(col: str, alias: str = 'd') -> str:
    """Predicado COMPLETO de um evento de funil CM (CE/RA/RR/Proposta):
    blacklist excluida, whitelist com precedencia total (mesmo gate dos
    Fechamentos, §7), funil Inbound e atribuicao 90d por contato.

    Criado 2026-07-02: ate entao as queries de evento aplicavam apenas
    filtro_inbound + _atrib_cm_90d — sem EMAIL_BLACKLIST nem EMAIL_WHITELIST.
    Efeito real da lacuna: email banido somava eventos (raissa/Buzzcreators,
    4 eventos; contrato NUPIXEL na fonte unificada) e email whitelistado nao
    somava (CROP ficou sem a proposta de 12/01). Centralizado aqui pra nenhuma
    query de evento esquecer camada. Deals sem email nao caem na blacklist
    (IS NULL passa) — seguem para o ramo de atribuicao normal.
    """
    p = f"{alias}." if alias else ""
    bl = _sql_email_list(EMAIL_BLACKLIST)
    wl = _sql_email_list(EMAIL_WHITELIST)
    return f"""(
    ({p}email_contato_principal_bd_sdr IS NULL
      OR lower(trim({p}email_contato_principal_bd_sdr)) NOT IN ({bl}))
    AND (
      lower(trim({p}email_contato_principal_bd_sdr)) IN ({wl})
      OR ({filtro_inbound(alias)} AND {_atrib_cm_90d(col, alias)})
    )
  )"""


# ============ CTE conversoes_cm ============

def cte_conversoes_cm(janela_inicio: date) -> str:
    """
    Gera a CTE `conversoes_cm` que une conversoes CM de comercial + contratos,
    com janela alargada 90d antes de `janela_inicio`.

    Desde 2026-07-02 (Victor) a CTE expoe o EMAIL do contato convertido (nao mais
    account_id) — atribuicao por contato. Duas guardas:
    - deals sem email nao geram gatilho (nao ha a quem atribuir);
    - emails da EMAIL_BLACKLIST nao geram gatilho (caso NUPIXEL: contrato banido
      com URL report-trends abria janela de atribuicao pra conta inteira).

    Use no WITH ... pra qualquer query que aplica regra 90d pos-conversao.
    """
    janela = (janela_inicio - timedelta(days=90)).isoformat()
    f = filtro_cm()
    bl = _sql_email_list(EMAIL_BLACKLIST)
    return f"""WITH conversoes_cm AS (
  SELECT lower(trim(email_contato_principal_bd_sdr)) AS email_conv, cdate AS data_conv
  FROM deals_comercial_prod
  WHERE email_contato_principal_bd_sdr IS NOT NULL
    AND lower(trim(email_contato_principal_bd_sdr)) NOT IN ({bl})
    AND cdate >= '{janela}'
    AND {f}
  UNION ALL
  SELECT lower(trim(email_contato_principal_bd_sdr)), cdate
  FROM deals_contratos_prod
  WHERE email_contato_principal_bd_sdr IS NOT NULL
    AND lower(trim(email_contato_principal_bd_sdr)) NOT IN ({bl})
    AND cdate >= '{janela}'
    AND {f}
)"""


# ============ CONTAGENS POR KPI ============

def q_count_leads(ini: date, fim: date) -> str:
    """Count de Leads CM unicos por email no periodo.

    Dedupe por email: mesmo email criado em 2 deals no mesmo periodo conta 1 vez.
    """
    f = filtro_cm()
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    cde = _cdate_efetivo()
    return f"""
WITH wl AS ({wl}), bl AS ({bl})
SELECT COUNT(DISTINCT lower(trim(email_contato_principal_bd_sdr))) AS n
FROM deals_comercial_prod
WHERE {cde}::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND email_contato_principal_bd_sdr IS NOT NULL
  AND lower(trim(email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
  AND (
    lower(trim(email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
    OR {f}
  )
  AND {_sem_outbound()}
"""


def q_count_evento(kpi: str, ini: date, fim: date) -> str:
    """Count de evento pos-conversao Inbound (ce, ra, rr, prop) — aplica regra 90d."""
    col = COLUNA_EVENTO[kpi]
    cte = cte_conversoes_cm(ini)
    return f"""
{cte}
SELECT COUNT(*) AS n
FROM deals_comercial_prod d
WHERE d.{col}::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {predicado_evento(col, "d")}
"""


def q_count_perdidos(ini: date, fim: date) -> str:
    """
    Count de Perdidos (DEFINICAO COORTE): leads CM Inbound criados no periodo
    que terminaram como Perdido (data_negocio_perdido_auto IS NOT NULL).

    Antes a definicao era 'perdidos no periodo' (qualquer cdate), o que misturava
    coortes e gerava % > 100% — ex: leads de 2025 perdidos em 2026 contavam no
    denominador errado. Agora % = Perdidos / Leads do mesmo periodo, <= 100%.
    """
    f = filtro_cm()
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    return f"""
WITH wl AS ({wl}), bl AS ({bl})
SELECT COUNT(DISTINCT lower(trim(email_contato_principal_bd_sdr))) AS n
FROM deals_comercial_prod
WHERE cdate::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND email_contato_principal_bd_sdr IS NOT NULL
  AND data_negocio_perdido_auto IS NOT NULL
  AND motivo_perda_bd_sdr IS NOT NULL
  AND lower(trim(email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
  AND (
    lower(trim(email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
    OR {f}
  )
  AND {_sem_outbound()}
"""


def q_count_fechamentos(ini: date, fim: date) -> str:
    """Count de Fechamentos: whitelist override OU (Inbound + regra 90d); menos blacklist.

    Whitelist tem precedencia sobre o filtro Inbound — deals que o Victor confirmou
    como CM-fechamento mas estao marcados como Outbound no CRM continuam contando.
    """
    cte = cte_conversoes_cm(ini)
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    return f"""
{cte},
wl AS ({wl}),
bl AS ({bl})
SELECT COUNT(*) AS n
FROM deals_contratos_prod ct
WHERE ct.data_fechamento_auto::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND lower(trim(ct.email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
  AND (
    lower(trim(ct.email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
    OR (
      {filtro_inbound("ct")}
      AND {_atrib_cm_90d("data_fechamento_auto", "ct")}
    )
  )
"""


# ============ LISTAS DE DEALS (DETALHADO) ============

def q_lista_leads(ini: date, fim: date) -> str:
    """Lista de Leads dedupada por email (pega o deal mais recente quando ha duplicata)."""
    f = filtro_cm()
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    cde = _cdate_efetivo('d.id', 'd.cdate')
    return f"""
WITH wl AS ({wl}), bl AS ({bl}),
filtrados AS (
  SELECT DISTINCT ON (lower(trim(d.email_contato_principal_bd_sdr)))
    d.id, d.title AS deal,
    d.email_contato_principal_bd_sdr AS email,
    d.utm_source, d.utm_content,
    {cde}::date AS data_conversao,
    COALESCE(d.sdr_responsavel, d.sdr_sdr) AS bd,
    {cde} AS cdate
  FROM deals_comercial_prod d
  WHERE {cde}::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
    AND d.email_contato_principal_bd_sdr IS NOT NULL
    AND lower(trim(d.email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
    AND (
      lower(trim(d.email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
      OR {f}
    )
    AND {_sem_outbound('d')}
  ORDER BY lower(trim(d.email_contato_principal_bd_sdr)), d.cdate DESC
)
SELECT id, deal, email, utm_source, utm_content, data_conversao, bd
FROM filtrados
ORDER BY cdate
"""


def q_lista_evento(kpi: str, ini: date, fim: date) -> str:
    """Lista deals com evento de funil Inbound (ra, rr, prop) no periodo. Regra 90d."""
    col = COLUNA_EVENTO[kpi]
    cte = cte_conversoes_cm(ini)
    extras = ""
    if kpi == 'ra':
        extras = ", d.data_inicio_reuniao_realizada::date AS data_realizada"
    elif kpi == 'rr':
        extras = ", d.data_envio_proposta_auto::date AS data_proposta"
    return f"""
{cte}
SELECT
  d.id, d.title AS deal,
  COALESCE(d.bd_auto, d.sdr_responsavel, d.sdr_sdr) AS bd,
  d.utm_source, d.utm_content,
  d.{col}::date AS data_evento{extras}
FROM deals_comercial_prod d
WHERE d.{col}::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {predicado_evento(col, "d")}
ORDER BY d.{col}
"""


def q_lista_propostas(ini: date, fim: date) -> str:
    """Lista de Propostas Inbound com valor estimado (parsed do campo text)."""
    cte = cte_conversoes_cm(ini)
    return f"""
{cte}
SELECT
  d.id, d.title AS deal,
  COALESCE(d.bd_auto, d.sdr_responsavel, d.sdr_sdr) AS bd,
  d.utm_source, d.utm_content,
  d.data_envio_proposta_auto::date AS data_evento,
  d.value AS valor_text,
  d.currency
FROM deals_comercial_prod d
WHERE d.data_envio_proposta_auto::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {predicado_evento("data_envio_proposta_auto", "d")}
ORDER BY d.data_envio_proposta_auto
"""


def q_lista_fechamentos(ini: date, fim: date) -> str:
    """Lista de Fechamentos: whitelist override OU (Inbound + 90d); menos blacklist."""
    cte = cte_conversoes_cm(ini)
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    return f"""
{cte},
wl AS ({wl}),
bl AS ({bl})
SELECT
  ct.id, ct.title AS deal,
  COALESCE(ct.bd_auto, ct.sdr_responsavel, ct.sdr_sdr) AS bd,
  ct.utm_source, ct.utm_content,
  ct.data_fechamento_auto::date AS data_evento,
  ct.value AS valor,
  ct.currency,
  ct.email_contato_principal_bd_sdr AS email
FROM deals_contratos_prod ct
WHERE ct.data_fechamento_auto::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND lower(trim(ct.email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
  AND (
    lower(trim(ct.email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
    OR (
      {filtro_inbound("ct")}
      AND {_atrib_cm_90d("data_fechamento_auto", "ct")}
    )
  )
ORDER BY ct.data_fechamento_auto
"""


def q_lista_perdidos(ini: date, fim: date) -> str:
    """
    Lista detalhada de leads CM criados no periodo E perdidos (definicao coorte),
    dedupada por email (pega o deal perdido mais recente quando ha duplicata).
    Ordenada pela data de perda (mais recente primeiro).
    """
    f = filtro_cm()
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    return f"""
WITH wl AS ({wl}), bl AS ({bl}),
filtrados AS (
  SELECT DISTINCT ON (lower(trim(d.email_contato_principal_bd_sdr)))
    d.id, d.title AS deal,
    d.email_contato_principal_bd_sdr AS email,
    d.utm_source, d.utm_content,
    COALESCE(
      d.data_efetividade_contato_auto::date,
      d.cdate::date
    ) AS ultima_conversao,
    d.motivo_perda_bd_sdr AS motivo,
    d.data_negocio_perdido_auto::date AS data_perda
  FROM deals_comercial_prod d
  WHERE d.cdate::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
    AND d.email_contato_principal_bd_sdr IS NOT NULL
    AND d.data_negocio_perdido_auto IS NOT NULL
    AND d.motivo_perda_bd_sdr IS NOT NULL
    AND lower(trim(d.email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
    AND (
      lower(trim(d.email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
      OR {f}
    )
    AND {_sem_outbound('d')}
  ORDER BY lower(trim(d.email_contato_principal_bd_sdr)), d.data_negocio_perdido_auto DESC
)
SELECT id, deal, email, utm_source, utm_content, ultima_conversao, motivo, data_perda
FROM filtrados
ORDER BY data_perda DESC
"""


# ============ RANKINGS (SOURCES + CONTENT) ============

def q_ranking(dim: str, ini: date, fim: date) -> str:
    """
    Ranking por dimensao (`utm_source` ou `utm_content`) no periodo.

    Junta CTEs separadas por estagio do funil e faz LEFT JOIN no final,
    coalescendo zeros pra dimensoes que aparecem em alguns estagios mas nao outros.
    """
    if dim not in ('utm_source', 'utm_content'):
        raise ValueError(f"dim invalido: {dim}")

    cte = cte_conversoes_cm(ini)
    f = filtro_cm()
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    d1, d2 = ini.isoformat(), fim.isoformat()

    return f"""
{cte},
wl AS ({wl}),
bl AS ({bl}),
leads_p AS (
  SELECT {dim} AS dim, COUNT(*) AS leads
  FROM deals_comercial_prod
  WHERE cdate::date BETWEEN '{d1}' AND '{d2}'
    AND email_contato_principal_bd_sdr IS NOT NULL
    AND lower(trim(email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
    AND (
      lower(trim(email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
      OR {f}
    )
    AND {_sem_outbound()}
  GROUP BY {dim}
),
ce_p AS (
  SELECT d.{dim} AS dim, COUNT(*) AS ce
  FROM deals_comercial_prod d
  WHERE d.data_efetividade_contato_auto::date BETWEEN '{d1}' AND '{d2}'
    AND {predicado_evento("data_efetividade_contato_auto", "d")}
  GROUP BY d.{dim}
),
ra_p AS (
  SELECT d.{dim} AS dim, COUNT(*) AS ra
  FROM deals_comercial_prod d
  WHERE d.data_agendamento_auto::date BETWEEN '{d1}' AND '{d2}'
    AND {predicado_evento("data_agendamento_auto", "d")}
  GROUP BY d.{dim}
),
rr_p AS (
  SELECT d.{dim} AS dim, COUNT(*) AS rr
  FROM deals_comercial_prod d
  WHERE d.data_inicio_reuniao_realizada::date BETWEEN '{d1}' AND '{d2}'
    AND {predicado_evento("data_inicio_reuniao_realizada", "d")}
  GROUP BY d.{dim}
),
prop_p AS (
  SELECT d.{dim} AS dim, COUNT(*) AS prop
  FROM deals_comercial_prod d
  WHERE d.data_envio_proposta_auto::date BETWEEN '{d1}' AND '{d2}'
    AND {predicado_evento("data_envio_proposta_auto", "d")}
  GROUP BY d.{dim}
),
fech_p AS (
  SELECT ct.{dim} AS dim, COUNT(*) AS fech
  FROM deals_contratos_prod ct
  WHERE ct.data_fechamento_auto::date BETWEEN '{d1}' AND '{d2}'
    AND lower(trim(ct.email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
    AND (
      lower(trim(ct.email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
      OR (
        {filtro_inbound("ct")}
        AND {_atrib_cm_90d("data_fechamento_auto", "ct")}
      )
    )
  GROUP BY ct.{dim}
),
all_dim AS (
  SELECT dim FROM leads_p
  UNION SELECT dim FROM ce_p
  UNION SELECT dim FROM ra_p
  UNION SELECT dim FROM rr_p
  UNION SELECT dim FROM prop_p
  UNION SELECT dim FROM fech_p
)
SELECT
  COALESCE(a.dim, '(vazio)') AS dim,
  COALESCE(l.leads, 0) AS leads,
  COALESCE(c.ce, 0) AS ce,
  COALESCE(r.ra, 0) AS ra,
  COALESCE(rr.rr, 0) AS rr,
  COALESCE(p.prop, 0) AS prop,
  COALESCE(f.fech, 0) AS fech
FROM all_dim a
LEFT JOIN leads_p l USING (dim)
LEFT JOIN ce_p c USING (dim)
LEFT JOIN ra_p r USING (dim)
LEFT JOIN rr_p rr USING (dim)
LEFT JOIN prop_p p USING (dim)
LEFT JOIN fech_p f USING (dim)
ORDER BY leads DESC, ra DESC
"""


# ============ SOURCE DOMINANTE POR CONTENT (auxiliar) ============

def q_source_por_content(ini: date, fim: date) -> str:
    """
    Pra cada utm_content, retorna o utm_source mais frequente no periodo.
    Usado em render_ranking_content pra colorir o badge da source ao lado do content.
    """
    f = filtro_cm()
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    return f"""
WITH wl AS ({wl}), bl AS ({bl}),
ranked AS (
  SELECT
    utm_content,
    utm_source,
    COUNT(*) AS n,
    ROW_NUMBER() OVER (PARTITION BY utm_content ORDER BY COUNT(*) DESC) AS rn
  FROM deals_comercial_prod
  WHERE cdate::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
    AND email_contato_principal_bd_sdr IS NOT NULL
    AND lower(trim(email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
    AND (
      lower(trim(email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
      OR {f}
    )
    AND {_sem_outbound()}
    AND utm_content IS NOT NULL
  GROUP BY utm_content, utm_source
)
SELECT utm_content, utm_source
FROM ranked
WHERE rn = 1
"""


# ============ SERIE TEMPORAL 52 SEMANAS ============

def q_serie_temporal_12m(hoje: date) -> str:
    """
    Serie temporal semanal dos ultimos 12 meses (52 semanas) com 6 metricas:
    leads, ce, agendadas, propostas, fechamentos, e tx_ce (calculado em Python).

    Returna 1 linha por (semana_inicio, metrica) — Python pivota.
    Semana = date_trunc('week', evento) — Postgres conta segunda como inicio.
    O eixo X do grafico tambem usa essa convencao (mesma semana ISO).
    """
    # Janela alargada pra CTE: 12m + 90d = 15 meses antes de hoje
    janela_inicio = (hoje - timedelta(days=365 + 90))
    cte = cte_conversoes_cm(janela_inicio)
    f = filtro_cm()
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    hoje_iso = hoje.isoformat()
    janela_12m_inicio = (hoje - timedelta(weeks=52)).isoformat()

    return f"""
{cte},
wl AS ({wl}),
bl AS ({bl}),
eventos AS (
  SELECT date_trunc('week', cdate)::date AS semana, 'leads' AS metrica
  FROM deals_comercial_prod
  WHERE cdate::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
    AND email_contato_principal_bd_sdr IS NOT NULL
    AND lower(trim(email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
    AND (
      lower(trim(email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
      OR {f}
    )
    AND {_sem_outbound()}
  UNION ALL
  SELECT date_trunc('week', d.data_efetividade_contato_auto)::date, 'ce'
  FROM deals_comercial_prod d
  WHERE d.data_efetividade_contato_auto::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
    AND {predicado_evento("data_efetividade_contato_auto", "d")}
  UNION ALL
  SELECT date_trunc('week', d.data_agendamento_auto)::date, 'agendadas'
  FROM deals_comercial_prod d
  WHERE d.data_agendamento_auto::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
    AND {predicado_evento("data_agendamento_auto", "d")}
  UNION ALL
  SELECT date_trunc('week', d.data_envio_proposta_auto)::date, 'propostas'
  FROM deals_comercial_prod d
  WHERE d.data_envio_proposta_auto::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
    AND {predicado_evento("data_envio_proposta_auto", "d")}
  UNION ALL
  SELECT date_trunc('week', ct.data_fechamento_auto)::date, 'fechamentos'
  FROM deals_contratos_prod ct
  WHERE ct.data_fechamento_auto::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
    AND lower(trim(ct.email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
    AND (
      lower(trim(ct.email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
      OR (
        {filtro_inbound("ct")}
        AND {_atrib_cm_90d("data_fechamento_auto", "ct")}
      )
    )
)
SELECT semana, metrica, COUNT(*) AS n
FROM eventos
GROUP BY semana, metrica
ORDER BY semana, metrica
"""


# ============ PROPORCAO REUNIOES POR SOURCE 12M ============

def q_proporcao_sources_12m(hoje: date) -> str:
    """RA e RR por utm_source nos ultimos 12m. Regra 90d."""
    janela_inicio = hoje - timedelta(days=365 + 90)
    cte = cte_conversoes_cm(janela_inicio)
    janela_12m_inicio = (hoje - timedelta(weeks=52)).isoformat()
    hoje_iso = hoje.isoformat()

    return f"""
{cte}
SELECT
  COALESCE(d.utm_source, '(vazio)') AS source,
  COUNT(*) FILTER (
    WHERE d.data_agendamento_auto::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
      AND {predicado_evento("data_agendamento_auto", "d")}
  ) AS ra_12m,
  COUNT(*) FILTER (
    WHERE d.data_inicio_reuniao_realizada::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
      AND {predicado_evento("data_inicio_reuniao_realizada", "d")}
  ) AS rr_12m
FROM deals_comercial_prod d
WHERE (
    d.data_agendamento_auto::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
    OR d.data_inicio_reuniao_realizada::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
  )
GROUP BY d.utm_source
HAVING COUNT(*) FILTER (
  WHERE d.data_agendamento_auto::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
    AND {predicado_evento("data_agendamento_auto", "d")}
) > 0
ORDER BY ra_12m DESC
"""
