# Mapeamento de campos — Dashboard **Content Marketing Cxpress Brasil** → Supabase

> **Propósito:** define o funil e mapeia os campos da dashboard `relatorio-semanal-cxpress-brasil.html`
> contra a tabela do Supabase. É o equivalente Cxpress do `dashboard/MAPEAMENTO-CAMPOS.md` (Buzzmonitor BR).
>
> **Status (2026-06-09):** tabela `cxpress_deals_funil_principal_prod` populada (~7.326 linhas, jan/2021→jun/2026).
> Filtros **calibrados** contra dados reais + validação manual do Victor: funil_auto NÃO filtra (no-op,
> §2.1 — o AC marca leads de mídia como Outbound), corte é só por canal (whitelist CM, §2.2), inscrição
> de webinar fora, whatsapp/youtube/sem-tracking fora. Funil CM 2026: 490 leads · 35 triagem · 21 agend ·
> 18 demo · 12 propostas · 5 fechamentos · 419 perdidos-coorte. Ver §2 e §7.
>
> **Conexão:** mesmo banco do Brasil (`looker_readonly`), `SUPABASE_PG_URL` em `dashboard/.env`.

---

## 0. Resumo (por que difere do Buzzmonitor)

| Dimensão | Buzzmonitor BR | Cxpress BR |
|---|---|---|
| Tabelas | 2 (`deals_comercial_prod` + `deals_contratos_prod`) | **1** (`cxpress_deals_funil_principal_prod`) |
| Atribuição | `account_id` + janela 90d cross-table | **por linha** (todas as datas do funil estão na própria linha) |
| Dedup | por e-mail | **por deal** (a tabela não tem coluna de e-mail; há `contact` bigint) |
| Funil | Lead → CE → Reun. Agendada → Reun. Realizada → Proposta → Fechamento | Lead → **Triagem → Agendamento → Demo realizada** → Proposta → Fechamento |
| Idioma / moeda | PT-BR / BRL | PT-BR / BRL (igual) |

Como cada deal carrega todas as datas de etapa na própria linha, **não há CTE de conversões, nem
regra de 90 dias, nem UNION** — as queries (`queries_cxpress.py`) são mais simples que as do Brasil.

---

## 1. Tabela-fonte

`cxpress_deals_funil_principal_prod` — colunas relevantes:

**Básicas:** `id` (bigint, PK) · `title` · `cdate` (timestamptz — criação) · `mdate` · `status` (text) ·
`stage` (bigint) · `currency` · `contact` (bigint) · `owner` · `group` · `funil_auto` · `origem_do_lead`

**Datas das etapas (TEXTO — ver §5):** `data_de_criacao_auto` · `data_triagem_realizada_auto` ·
`data_do_agendamento_auto` · `data_de_demo_realizada_auto` · `data_do_envio_da_proposta_auto` ·
`data_do_fechamento_auto` · `data_do_lost_auto` · (apoio: `data_e_hora_da_demo`, `data_noshow_1..3`)

**Atribuição de canal:** `utm_source` · `utm_medium` · `utm_campaign` · `utm_content` · `utm_term` ·
`utm_creative` · `url_conversao` · `gclid`

**Valor (TEXTO):** `cxpress_fee_mensal` · `valor_atualizado_do_fee` · `valor_do_upsell`

**Responsáveis:** `closer_bd_auto` · `sdr_bdr_auto`

**Perda:** `data_do_lost_auto` · `motivo_de_perda_closer_sdr` · `contexto_do_lost_closer_sdr` · `etapa_do_lost`

---

## 2. Escopo: Inbound + Content Marketing (calibrado 2026-06-09)

Dashboard é **Content Marketing Cxpress Brasil**. Dois filtros aplicados em `queries_cxpress.py`,
ambos no WHERE de toda query (via helper `_escopo()`):

### 2.1. `filtro_inbound()` — **NO-OP** (não filtra por funil)

Originalmente `funil_auto = 'Inbound'`; virou no-op em 2026-06-09 ao auditar o gap "dashboard
mostra 5, Meta Ads mostra 9 leads em 15d": o AC classifica sistematicamente leads de mídia
paga/conteúdo como `Outbound` — **393 deals com UTM CM em 2026**, incluindo os [RMKT] meta da
LP clínicas — porque `funil_auto` reflete o processo de vendas (SDR move lead pra cadência
outbound), não o canal de origem. Mesma decisão já tomada no Buzz BR (2026-05-19). O gate de
canal da dashboard é exclusivamente o `filtro_cm()`.

### 2.2. `filtro_cm()` — Content Marketing (tudo − Google Ads − ruído − inscrição de webinar)

**Decisões Victor (2026-06-09)** após auditoria de utm_source/medium/url_conversao + checagem
manual de amostras no ActiveCampaign (1ª rodada sobre o recorte Inbound; estendido à tabela toda
quando `filtro_inbound` virou no-op — §2.1):

| Bucket | Decisão | Razão |
|---|---|---|
| `google + cpc` (Google Ads) | **fora** | tráfego pago Google, não-CM por definição |
| `chatgptads` (ChatGPT Ads) | **fora sempre** | mídia paga; barrado mesmo em URL de conteúdo (`CM_UTM_SOURCES_EXCLUIR`). `chatgpt.com` orgânico segue dentro. Victor 2026-10-08 (caso deal 89850) |
| `whatsapp` (qualquer medium) | **fora** | misto outbound/CM, vendedor abre conversa em muitos casos |
| `youtube` | **fora** | volume baixo + tracking ruidoso (Victor pediu corte) |
| `google` sem `cpc` | fora | orgânico/direto, ambíguo |
| sem utm e sem URL | **fora** | Victor validou amostra de 4 fechamentos: todos eram venda direta mal-classificada (Cacau Show, Claro Brasil, Lojas Marisa, Duben Seguros) |
| Inscrição de webinar (`content.cxpress.io/webinar-tecnologia-maio2026`) | **fora** | precedente Buzz BR 2026-05-26: inscrição é topo de funil, não vira lead CM; só a OFERTA conta. 124 inscrições (lote 01/jun) ficariam de fora |
| Cadastro interno (`home.cxpress.io/cadastro-interno[-bdr]`) | **fora, salvo e-mail próprio** | registro manual/indicação, não é conteúdo (43 dos 51 deals são whatsapp). Excluída em 2026-06-15; desde **2026-08-07** a exclusão **não vale** para `utm_source` de e-mail/newsletter próprio — ver Revisão 2026-08-07 abaixo |
| Whitelist social/owned | **dentro** | Meta/IG/FB/LinkedIn/Email/Blog/TikTok/Newsletter/Linktree — qualquer funil_auto |
| `webinar` e `qrcode-webinar-bloqueio-whatsapp` | **dentro** | UTM de webinar é 100% nossa; vale independente da URL. Decisão Victor 2026-08-07 — ver Revisão abaixo |
| LP `atendimento-para-clinicas` | **dentro** | CM mesmo sem UTM — exceção explícita do Victor |
| Demais URLs `content.cxpress.io` + `conteudo.elife.com.br` | dentro | domínios de conteúdo (ofertas futuras) |

**Implementação:** `CM_UTM_SOURCES` (whitelist exata) + 4 padrões LIKE (`instagram%`, `facebook%`,
`newsletter%`, `linktree%`) cobrindo variações como `Instagram_Feed`, `Facebook_Mobile_Reels`,
`newsletter+cxpress`, `Linktree Cxpress`. Mais `CM_URL_PATTERNS` (includes por URL) e **duas** listas de
exclusão por URL — `CM_URLS_EXCLUIDAS_SEMPRE` (inscrição de webinar) e `CM_URLS_EXCLUIDAS_SALVO_EMAIL`
(cadastro interno, furada por `CM_SOURCES_EMAIL_PROPRIO`) — detalhadas em §2.2.2. Toda exclusão usa
`COALESCE(url,'')` pra não derrubar leads com URL NULL.

**Funil CM 2026 final (YtD até 09/jun):** 490 leads · 35 triagem · 21 agend · 18 demo ·
12 propostas · 5 fechamentos · 419 perdidos (coorte). Janela 15d (26/05–09/06): 9 leads — **bate
com o Meta Ads** (era exatamente o gap que motivou o no-op do funil).

**Revisão 2026-06-15:** adicionado `home.cxpress.io/cadastro-interno%` à lista de exclusão por URL
(linha "Cadastro interno" na tabela acima; a constante se chamava `CM_URLS_EXCLUIDAS` — foi dividida em
duas em 2026-08-07, §2.2.2). Removeu o deal 81723 ('Destinando Viagens', fechamento 03/02 via `email`
genérico numa página de registro interno). **YtD 2026 passa a 493 leads · 4 fechamentos** (era 494 · 5).
↳ **Revertido em 2026-08-07** após auditoria do Victor: o 81723 é CM. Ver §2.2.2.

**Revisão 2026-08-07:** `webinar` entrou em `CM_UTM_SOURCES` (decisão Victor).

Motivo: o deal **81535 'Grupo Calusa'** (Ganho, fechamento 19/05/2026) não aparecia como fechamento CM.
A coluna `utm_source` chegou `webinar` — nome do evento, não canal — enquanto a `url_conversao` trazia
a UTM real do anúncio: `home.cxpress.io/bloqueio-whatsapp-comercial-como-evitar?utm_source=ig&utm_medium=cpc`
`&utm_campaign=[meta][conversão][webinar][janeiro]&utm_creative=ad_04&utm_tracking=Instagram_Feed`.
Ou seja, tráfego de Instagram Ads (Lookalike de clientes, Ad_04) para LP de conteúdo.

Que era **defeito de preenchimento da coluna** — e não LP fora de escopo — ficou claro nos vizinhos:
dos 44 deals de 2026 na mesma LP, **40 já contavam como CM** porque a coluna deles veio `ig`/`meta`.
Só 4 deals na base inteira têm `utm_source = 'webinar'`, todos dessa LP: 81535 (Ganho, fech. 19/05/2026),
80903 'Catavento Cross-sell' (Ganho, fech. 13/03/2026), 75078 'Catavento Cultural' (Ganho, fech. 27/08/2025,
fora do escopo 2026) e 81871 'Cartão de Todos' (Aberta). Efeito na dashboard 2026: **+2 fechamentos**
(81535 e 80903) e +2 leads.

A variante `qrcode-webinar-bloqueio-whatsapp` (1 deal, mesma LP e mesma campanha) **também entrou**, pelo
mesmo critério — o match da whitelist é exato, então variantes precisam ser listadas uma a uma (só os 4
padrões `LIKE` — `instagram%`, `facebook%`, `newsletter%`, `linktree%` — fazem prefixo). Se aparecerem
novas variantes `*-webinar-*`, ou se listar valor a valor virar manutenção repetitiva, vale trocar por
um padrão `LIKE '%webinar%'`.

**Validade independente da URL (decisão Victor 2026-08-07):** as duas sources valem **venha o deal de
onde vier**, sem amarração a LP de conteúdo. Razão: UTM de webinar é **100% nossa** — só o próprio time
tagueia assim, não existe origem externa que produza esse valor —, então não há classe de falso positivo
a proteger. Isso alinha a Cxpress ao **Buzzmonitor BR, que já trata `webinar` como CM desde 2026-06-22**
(junto de `pos-webinar`, `webinar-ao-vivo` e `apresentacao-webinar` — `queries.py:28-45`); a Cxpress é
que estava atrás.

Não confundir com a exclusão de `content.cxpress.io/webinar-tecnologia-maio2026`: aquela barra a
**inscrição** como topo de funil, por URL, antes da whitelist de source. É critério de **etapa do funil**,
não de canal — os dois convivem sem conflito.

### 2.2.2. Exclusão de URL em dois níveis (2026-08-07)

A lista única `CM_URLS_EXCLUIDAS` foi dividida em duas, porque as exclusões que existiam tinham
**motivos diferentes** e por isso merecem forças diferentes:

| Constante | O que exclui | Fura com e-mail próprio? |
|---|---|---|
| `CM_URLS_EXCLUIDAS_SEMPRE` | `content.cxpress.io/webinar-tecnologia-maio2026` — inscrição de webinar | **Não.** Critério é **etapa do funil**: inscrição é topo, não vira lead CM por canal nenhum |
| `CM_URLS_EXCLUIDAS_SALVO_EMAIL` | `home.cxpress.io/cadastro-interno[-bdr]` — registro manual/indicação | **Sim.** Critério é **canal**, e canal próprio ganha da página |

`CM_SOURCES_EMAIL_PROPRIO` = `['email']` + prefixo `newsletter%` (cobre `Newsletter`,
`newsletter+cxpress`, `newsletter_startups`, `newsletter+elife` — 24 deals na base em 6 grafias).

**Motivo (decisão Victor 2026-08-07):** e-mail e newsletter são canais **100% nossos** — o disparo sai
do nosso ESP e nenhuma origem externa produz esses valores de UTM. Então um lead que chegou por e-mail
nosso é CM mesmo que tenha convertido numa página de cadastro interno. O gatilho foi a auditoria do
deal **81723 'Destinando Viagens'** (Ganho, fechamento 03/02/2026, R$ 129.000 no campo de fee,
responsável Luiz Fantini, `funil_auto=Inbound`): em junho o `utm_source=email` sem nenhum outro
parâmetro foi lido como e-mail comercial 1:1 e motivou a exclusão da página; em agosto o Victor
confirmou que a origem é Content Marketing.

**Por que estrutural e não override nominal por `deal_id`:** a pedido do Victor, para que **e-mails e
newsletters futuros nessa página também contem**, sem depender de alguém notar o deal e adicioná-lo
à mão. O custo é aceitável porque o que barra os 43 deals de whatsapp da página não é a exclusão de
URL — é o próprio `whatsapp` não estar na whitelist de sources (fora do CM por decisão de jun/2026).

**Por que duas listas e não precedência global do e-mail:** verificado nos dados que a página do
`webinar-tecnologia-maio2026` tem **1 deal `email` e 1 `newsletter`**. Com precedência global, esses
dois entrariam como lead CM — exatamente o que a regra de topo de funil existe para impedir. Com a
divisão, seguem fora (validado: `passam_cm = 0` em todas as sources daquela página).

**Efeito imediato:** +1 deal no escopo (1152 → 1153) e **+1 fechamento no YtD 2026** (4 → 5). Os cinco
fechamentos CM de 2026 passam a ser: 81723 Destinando Viagens (03/02), 80903 Catavento Cross-sell
(13/03), 83610 Led Tools (24/03), 82083 Synergy Studios (01/04) e 81535 Grupo Calusa (19/05).

**Guard de NULL:** a cláusula de e-mail próprio usa `COALESCE(utm_source,'')`. Sem isso, deal de URL
interna com `utm_source` NULL viraria `NULL` em vez de `FALSE` na negação e escaparia da exclusão —
mesma classe do bug google/cpc do Buzz BR (2026-05-26). Validado: os 4 deals `cadastro-interno` com
source NULL continuam fora.

⚠️ A exclusão de `content.cxpress.io/webinar-tecnologia-maio2026` (inscrição = topo de funil) **não muda**:
ela é hard-exclude por URL e roda antes da whitelist de source. Os 124 deals daquele lote continuam fora.

**Nota sobre outbound (reconfirmado 2026-08-07):** a dashboard já aceita fechamento de deal `Outbound` —
`filtro_inbound()` é no-op desde 2026-06-09 e o gate é só o canal. Em 2026 o escopo CM tem **557 deals
Outbound contra 196 Inbound**, e um dos fechamentos que já apareciam era Outbound. O 81535 (também
`funil_auto='Outbound'`) estava barrado apenas pelo `utm_source`, não pelo funil.

### 2.2.1. Perdidos = definição COORTE (igual Buzzmonitor BR)

Perdidos conta **leads criados no período** que terminaram como Perdido (`data_do_lost_auto` válida +
`motivo_de_perda_closer_sdr` preenchido + **`status = 'Perdido'`**) — **não** "perdidos datados no
período". Datar pelo lost misturava coortes (deal de 2024 perdido hoje contava no período atual) e
gerava % Perdidos > 100% no painel da seção 2 (98 perdidos vs 97 leads). Corrigido em 2026-06-09
espelhando `q_count_perdidos`/`q_lista_perdidos` do Buzz BR. A lista de detalhe acompanha o **período
selecionado** (não MtD fixo — decisão Victor 2026-06-09: no server dinâmico a lista deve mostrar
os mesmos perdidos que o KPI do período conta) e ordena pela data da perda.

**Por que exigir `status = 'Perdido'` (estado final):** o AC mantém `data_do_lost_auto` e motivo na
linha quando um deal perdido é **reaberto** — caso Medprime (83763): lost 01/06 "Fora do timing",
reativado 03/06 com triagem + agendamento + demo marcada, status `Aberta` — contava como perdido E
ativo ao mesmo tempo. Na base há 25 `Aberta` + 4 `Ganho` com lost+motivo órfãos. Sem o status, um
deal recuperado/ganho ainda apareceria nos perdidos da coorte.

### 2.2.3. Deals de teste ficam fora (2026-10-22)

O time valida LP, form, UTM e automação criando deal de verdade no funil principal, e esses deals
caíam no escopo CM (a URL de conversão é `content.cxpress.io`). `filtro_nao_teste()` entra no
`_escopo()` e tira o deal quando: `utm_source` é `teste`/`test` (com ou sem sufixo, ex. `teste-interno`);
o título tem a **palavra** teste/test; ou o e-mail do contato (`contact` → `dim_contacts_elife_cxpress.id`,
porque a tabela de deals não tem e-mail) é de domínio interno do grupo/de exemplo
(`TESTE_DOMINIOS_EMAIL`) ou tem "teste" como pedaço separado (`testecrm@`, `gestaoteste@`). Teste que
escapa das regras vai por ID em `DEALS_TESTE_IDS`.

Na entrada saíram **25 deals** do escopo (5 só em 20/10/2026), todos Perdido/Aberta, nenhum com
triagem, agendamento, demo, proposta ou fechamento: só Leads e Perdidos caíram. As regras foram medidas
na tabela inteira (11.240 deals) antes de entrar — tudo o que casa é teste ou funcionário. Ao ampliar
domínio ou padrão, medir de novo na tabela inteira: falso positivo aqui some com lead real em silêncio.

### 2.3. Diferenças vs Buzzmonitor BR

| Aspecto | Buzzmonitor BR | Cxpress BR |
|---|---|---|
| Dedup | por e-mail (`email_contato_principal_bd_sdr`) | por deal (sem coluna de e-mail) |
| Reconversão | override manual `RECONVERSOES_MANUAIS` | n/a |
| Whitelist/blacklist nominal | `EMAIL_WHITELIST` + `EMAIL_BLACKLIST` | só deals de teste, por regra + `DEALS_TESTE_IDS` (§2.2.3) |
| `whatsapp` | dentro (decisão Victor jan/2026) | fora (decisão Victor jun/2026) |
| `youtube` | n/a (volume zero) | fora |
| Blog/conteúdo próprio | `buzzmonitor.com.br/blog/%`, `content.elife`, slugs CM | `home.cxpress.io/atendimento-para-clinicas`, `content.cxpress.io` |

**Ponto de extensão:** `CM_UTM_SOURCES` e `CM_URL_PATTERNS` no topo de `queries_cxpress.py` —
adicionar novas LPs/sources lá, sem tocar nas queries.

---

## 3. Sem regra de 90 dias

O Buzzmonitor atribui eventos pós-conversão via `account_id` + janela de 90d entre duas tabelas. A Cxpress
tem **uma tabela só**: cada deal já traz `data_triagem_realizada_auto`, `data_do_agendamento_auto`, etc. na
própria linha. Logo cada etapa é contada diretamente pela sua data, sem cross-join nem janela de atribuição.

---

## 4. Funil (contagem por data do evento)

| # | Etapa | Coluna de data | Observação |
|---|---|---|---|
| 1 | **Lead** | `cdate` | criação do deal (timestamptz) |
| 2 | **Triagem** | `data_triagem_realizada_auto` | — |
| 3 | **Agendamento** | `data_do_agendamento_auto` | demo/reunião agendada |
| 4 | **Demo realizada** | `data_de_demo_realizada_auto` | — |
| 5 | **Proposta** | `data_do_envio_da_proposta_auto` | valor em `cxpress_fee_mensal` |
| 6 | **Fechamento** | `data_do_fechamento_auto` | valor em `valor_atualizado_do_fee` (fallback `cxpress_fee_mensal`) |
| — | **Perdido** | coorte: `cdate` no período + `data_do_lost_auto` + motivo | + `motivo_de_perda_closer_sdr`, `etapa_do_lost` — ver §2.2.1 |

Cada KPI conta pela data da **sua** etapa (não pela criação) — igual à regra inegociável do Brasil.
Exceção: **Perdidos** usa coorte (§2.2.1), também igual ao Brasil.

**Links pro ActiveCampaign:** o nome do deal em toda lista é um link pra
`https://elife.activehosted.com/app/deals/{id}` (instância AC da Cxpress = `elife`;
Buzzmonitor usa `buzzmonitor.activehosted.com`). Implementado em `render_helpers_cxpress._deal_cell`.

---

## 5. ⚠️ Datas chegam como TEXTO

As colunas `data_*_auto` são `text` no Supabase (vêm assim do ActiveCampaign). O helper `_d()` em
`queries_cxpress.py` faz cast defensivo assumindo **ISO `YYYY-MM-DD`** (pega os 10 primeiros chars; devolve
NULL para qualquer outro formato, então um valor torto nunca quebra a query inteira).

**Conferir na 1ª carga:** rodar `SELECT data_triagem_realizada_auto FROM cxpress_deals_funil_principal_prod
WHERE data_triagem_realizada_auto <> '' LIMIT 20`. Se vier em `DD/MM/YYYY` ou `MM/DD/YYYY`, ajustar **só** o
`_d()` (ponto único) — senão a dashboard mostra zeros mesmo com dados.

---

## 6. Valor (texto → BRL)

`cxpress_fee_mensal` e `valor_atualizado_do_fee` são texto. O parse acontece em Python
(`render_helpers.parse_valor_text`, que trata `R$`, milhar `.` e decimal `,`). Fechamento usa
`COALESCE(valor_atualizado_do_fee, cxpress_fee_mensal)`. Moeda de reporte: **BRL**.

---

## 7. Validação / pendências

1. **Baseline 2026-06-09 (filtro final: funil no-op + CM + webinar excluído + perdido só status final):**
   Funil CM YtD = 490 leads · 35 triagem · 21 agend · 18 demo · 12 propostas · 5 fech · 415 perdidos
   (coorte, status='Perdido'). Janela 15d (26/05–09/06): 9 leads · 3 perdidos — 9 bate com o Meta Ads.
   Verificado servidor 8020 vs SQL independente — match exato. Usar como número-âncora pra detectar
   regressão.
2. **Sync AC→Supabase é diário (madrugada ~02:30 UTC):** eventos do dia (ex.: demo realizada hoje)
   só aparecem na dashboard no dia seguinte. Caso Medprime 2026-06-09: demo marcada pra 09/06 12:00,
   card movido no AC no mesmo dia — a linha local (mdate 03/06) só atualiza na carga noturna.
2. **Formato das datas** (§5) — confirmado ISO `YYYY-MM-DDT...` (jun/2026).
3. **Escopo** (§2) — calibrado e validado pelo Victor em 2026-06-09. ✅
4. **Dedup** — sem e-mail; conta por deal (igual LATAM). Se aparecerem duplicatas claras por empresa,
   avaliar dedup por `contact` (bigint).
5. **`stage`/`status`** — mapear os valores reais (ex.: `status='Ganho'` confirma fechamento? há `Perdido`?)
   e, se útil, cruzar com as datas de etapa.
6. **Deploy Vercel** — pendente (dashboard só roda LOCAL hoje, porta 8020). Mesmo motivo do BR/LATAM:
   Vercel não conecta no Supabase com `looker_readonly` (IPv4). Quando deployar, usar pasta sibling
   fora do repo (ver `reference_dashboard_sibling` e padrão `dashboard-buzzmonitor-brasil`).
