# Contexto Compartilhado — meta-campanha

> Este arquivo e lido pela skill `/meta-campanha` antes de qualquer acao. Cria e edita campanhas de Meta Ads via o **MCP oficial da Meta** (escrita real, gasta verba).

---

## MCP oficial da Meta — como referenciar

As tools aparecem como `mcp__<id>__ads_*` (ex.: `mcp__85846e09-94b2-4c6d-8ee5-fdc4c56dfbf1__ads_create_campaign`). **O `<id>` varia por conexao/maquina** — nunca dependa dele hardcoded. Use os tools `ads_*` que estiverem conectados na sessao. A trava (hook) ja casa por sufixo, independente do id.

Se nenhum tool `ads_*` da Meta estiver disponivel, **pare** e peca pro usuario conectar o MCP oficial (Connectors do app -> `https://mcp.facebook.com/ads`).

---

## Restricao de seguranca (LER PRIMEIRO)

1. **Tudo nasce PAUSADO.** `ads_create_campaign`/`_ad_set`/`_ad` criam em PAUSED por design. Nada vai ao ar na criacao.
2. **Ativar e religar SEMPRE pedem aprovacao do Victor.** `ads_activate_entity` e `ads_update_entity` com `status=ACTIVE` passam pelo hook `guard_meta_activate.py` (camada tecnica) — e a skill tambem confirma antes (camada humana). Nunca ative no automatico.
3. **Orcamento acima do teto pede confirmacao.** Tetos conservadores em `meta-ads/data/budget-guardrails.json` (R$50 / US$12 / EUR12 por adset/dia). O hook intercepta criacao/edicao acima disso.
4. **Pausar, renomear e editar nao-orcamentario** sao livres (sem gasto novo) — mas a skill ainda mostra o plano e confirma.
5. Fonte de escrita = **so o MCP oficial da Meta**. Vercel entra apenas para hospedar a imagem do criativo (nao adiciona requisicao ao Meta).

---

## Contas validas (verificado 2026-06-24, `ads_get_ad_accounts`)

Use o `ad_account_id` **sem** o prefixo `act_`. So opere em contas com `is_ads_mcp_enabled=true` E `is_queryable=true`.

| Marca / chave | ad_account_id | Moeda | Status |
|---|---|---|---|
| Buzzmonitor (BR) | `733381876770151` | BRL | OK |
| Buzzmonitor Latam | `300991508612624` | USD | OK |
| Buzzmonitor Portugal | `1510240806113985` | EUR | OK |
| Cxpress Brasil | `1266529690796936` | BRL | OK |
| Cxpress Latam | `1999993677432010` | USD | OK |
| **Cxpress Portugal** | `1246835670520012` | EUR | ⛔ **INDISPONIVEL** (conta UNSETTLED — pendencia de cobranca). Recusar ate resolver. |
| Elife Brasil | `666041480822419` | BRL | OK |
| Elife Portugal | `625334181331558` | EUR | OK |
| Elife Espana | `519673258626470` | EUR | OK |
| Buzzcreators 01 | `499341683195343` | BRL | ⚠️ sem metodo de pagamento — criar OK, mas avisar que nao roda ate ter pagamento |
| VozXpress | `2608073376104001` | BRL | OK |

Orcamento minimo diario da Meta: BRL/`act` 514c (R$5,14) · USD 100c ($1,00) · EUR 87c (EUR0,87). Sempre confirmar `is_ads_mcp_enabled`/`is_queryable` no momento (a leitura de contas e cacheada 1x por sessao).

---

## Classificacao de funil -> defaults de campanha (aja como gestor de trafego senior)

Classifique pela mesma tabela de palavras-chave do `.claude/skills/bunzzai/CONTEXT.md`. O funil define o objetivo — topo capta lead/atencao, fundo converte quem ja conhece.

> **Auditoria da conta (Buzzmonitor BR, 2026-06-24):** a casa roda **CONVERSAO** em quase tudo — campanhas nomeadas `[BR][CONVERSAO][Tema]`, otimizacao `OFFSITE_CONVERSIONS` (com pixel), **inclusive em MoFu e remarketing**. Orcamento por **ABO** (adset ~R$20-70/dia), bid "Highest volume" (LOWEST_COST_WITHOUT_CAP), CTAs de fundo (SEE_DETAILS, "Agende demonstracao", "Solicite proposta"). **Espelhe esse padrao por default** — nao caia em campanha de trafego achando que e "mais simples".

| Tipo (palavras-chave no nome/briefing) | Funil | Objetivo (ODAX) | optimization_goal | billing | Notas |
|---|---|---|---|---|---|
| webinar, live, aula, workshop, masterclass | Topo | `OUTCOME_LEADS`/`OUTCOME_SALES` | `OFFSITE_CONVERSIONS` (pixel) ou `LEAD_GENERATION` (form nativo) | IMPRESSIONS | precisa `promoted_object` com pixel+evento; CpL benchmark **webinar** |
| ebook, guia, kit, template, checklist, playbook, material, whitepaper, planilha | Topo | `OUTCOME_LEADS`/`OUTCOME_SALES` | `OFFSITE_CONVERSIONS` / `LEAD_GENERATION` | IMPRESSIONS | CpL benchmark **material rico** |
| buzztalk, evento presencial | Topo | `OUTCOME_LEADS` | `OFFSITE_CONVERSIONS` / `LEAD_GENERATION` | IMPRESSIONS | |
| **MoFu / consideracao / nutricao** | Meio | `OUTCOME_LEADS` (default da casa) | `OFFSITE_CONVERSIONS` (pixel) | IMPRESSIONS | a casa NAO usa so trafego em MoFu — usa conversao. So caia em `OUTCOME_TRAFFIC`/`LANDING_PAGE_VIEWS` se NAO houver pixel/evento |
| remarketing, retargeting, rmkt, rtg | Fundo | `OUTCOME_LEADS` (padrao observado) ou `OUTCOME_SALES` | `OFFSITE_CONVERSIONS` (pixel) | IMPRESSIONS | custom audience de remarketing+engajamento (+LaL); CpL benchmark **remarketing** |
| blog, conteudo, awareness, alcance | Topo | `OUTCOME_TRAFFIC` / `OUTCOME_AWARENESS` | `LANDING_PAGE_VIEWS` / `REACH` | IMPRESSIONS | so quando NAO ha captura/conversao |

**Conversao e pixel (quase sempre):** para `OFFSITE_CONVERSIONS` o `promoted_object` com pixel e **obrigatorio** — e e **setavel na criacao E na edicao** (write), nao e manual. Buscar o pixel via `ads_get_datasets` (1x, cache) e montar `promoted_object={"pixel_id":"<id>","custom_event_type":"<EVENTO>"}` (ex.: LEAD, COMPLETE_REGISTRATION, PURCHASE). Sem pixel/evento, NAO use OFFSITE_CONVERSIONS — caia em LANDING_PAGE_VIEWS e avise que a otimizacao fica mais fraca.
- Pixels da **Buzzmonitor BR** (ref. 2026-06-24 — confirmar qual + evento com o Victor, nao chutar): `705678789565591` (BM BR - Remarketing, disparando hoje) · `1280081394149462` (Conversoes - CRM). Outras contas: rodar `ads_get_datasets` na conta.

**UTM (obrigatorio) — template PADRAO de TODAS as marcas e regioes:** `ads_create_creative` nao tem campo `url_tags` -> **embutir no `link_url`** (query string). Usar SEMPRE este template (os `{{...}}` sao macros dinamicos que a **Meta** preenche na entrega — nao substituir a mao):

```
utm_source=meta&utm_medium={{placement}}&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&adset={{adset.name}}&campaignid={{campaign.id}}&adsetid={{adset.id}}&adid={{ad.id}}
```

Anexar ao `link_url` com `?` (ou `&` se a LP ja tiver query string). Ex.: `https://lp.exemplo.com/oferta?utm_source=meta&utm_medium={{placement}}&utm_campaign={{campaign.name}}&...`. A casa cruza UTM/`url_conversao` com os deals (dashboards) — anuncio sem UTM **cega a atribuicao**. Em criativo de post existente (`object_story_id`) o UTM vive no post; avisar se nao der pra setar.

Defaults de estrutura (recomendar, confirmar no plano):
- **Orcamento: a casa usa ABO** (orcamento por adset, ~R$20-70/dia). Perguntar CBO vs ABO; **default ABO** pra espelhar a conta (CBO segue valido se o Victor preferir).
- **Idade: default 28-50** (`age_min:28, age_max:50`) em todo adset, salvo pedido diferente. Cap rigido (nao so sugestao do Advantage+) -> `targeting_automation.advantage_audience=0`.
- **Nao excluir idade desconhecida** por padrao (especialmente WhatsApp/mensagens, onde o sinal de idade e esparso — excluir corta alcance com pouco ganho). So excluir se pedido.
- **CTA por funil:** fundo/MoFu de conversao -> `SEE_DETAILS`, `SIGN_UP`, `BOOK_NOW` ("Agende uma demonstracao") ou `GET_QUOTE` ("Solicite uma proposta"). Topo/awareness -> `LEARN_MORE`. Nao usar `LEARN_MORE` como default cego.
- **LP de destino especifica** — nunca a home generica; pedir a URL certa da oferta.
- **Targeting**: o MCP nao expoe busca de interesse por ID -> usar **custom audiences** (ja na conta) + **geo** + Advantage+. Nunca inventar ID de interesse.
- **UE (Portugal/Espanha)**: `dsa_beneficiary`/`dsa_payor` obrigatorios (auto-preenchidos se omitidos).
- Benchmarks CpL/CTR/Conv.LP: `meta-ads/data/benchmarks.json` — mostrar o esperado no plano.

> **Limitacao de leitura do MCP (2026-06-24):** as tools de leitura NAO expoem `promoted_object` (pixel), `destination_type`, `targeting` nem `url_tags` (UTM). Da pra ler so `optimization_goal`/`daily_budget`/`bid_strategy` (adset) e `link_url`/`call_to_action_type`/`body`/`title` (criativo — e `link_url` vem vazio em criativo de post). Ou seja: **nao da pra clonar pixel/UTM/segmentacao de uma campanha existente** — perguntar ao Victor (pixel, evento, LP, UTM, idade) em vez de assumir.
>
> **Isto e so LEITURA.** Na **ESCRITA** (criar/alterar) pixel (`promoted_object`) e targeting (geo, idade, custom audiences, exclusoes, placements) sao **100% setaveis** via `ads_create_ad_set`/`ads_update_entity`. O unico furo de targeting e **interesse-por-ID** (nao ha tool de busca de interesse) -> usar custom audiences + geo + idade + Advantage+.
>
> **Nao da pra DELETAR/ARQUIVAR pelo MCP** (visto 2026-06-24): `ads_update_entity` com `status=DELETED`/`ARCHIVED` e **forcado a PAUSED** (`status_forced_to_paused:true`). Excluir campanha/adset/ad e **manual no Ads Manager**. Quando o Victor pedir pra apagar: renomear com prefixo `[APAGAR-TESTE]`/`[APAGAR]`, pausar (ja fica pausado), e entregar o link do Ads Manager pra ele apagar em 1 clique.

---

## Sanity-check de publico (OBRIGATORIO)

Antes de montar o adset, compare o publico pedido com o ICP da marca:
- ICP por marca em `brand/{marca}/brand-manifest.json` (campos de publico/messaging) + `brand/{marca}/BRANDBOOK.md`.
- Resumo: **Buzzmonitor** = times de marketing/CX, social listening, agencias. **Cxpress** = PMEs com atendimento multicanal (clinicas, escolas, imobiliarias...). **Buzzcreators** = times/agencias de influencer marketing.
- Se o publico pedido nao bate com o ICP (ex.: marca de saude/atendimento + publico de "empreendedorismo"), **questione explicitamente** antes de seguir: "Esse publico costuma se importar com [dor que a marca resolve]? Quer mesmo manter?" — nao corrija sozinho, pergunte.

---

## Protocolo de copy (se a skill escrever texto de anuncio)

Texto de anuncio e publico -> carregue os 3 pilares ANTES de escrever (mesma regra da CLAUDE.md):
1. **Linguistico** (se regiao != brasil): `conhecimento/linguistico/{pt-portugal|es-latam}/padrao-linguistico.md`. Se nao carregar, PARE.
2. **Copywriting**: `conhecimento/copywriting/fundamentos-copy.md` + `estatico-ads.md` (ou `video-curto-ads.md`).
3. **Anti-IA**: `conhecimento/editorial/regras-anti-ia.md` + anexo do idioma (PT-PT / ES-LATAM).

Se a copy ja vier pronta (de `/copy-criar` ou colada), so diagramar nos campos do criativo — nao reescrever.

---

## Convencao de nomes de criativo

**Marca e regiao NAO entram na sigla** (ja vem da conta de anuncio). 

- Tipo: `WBN` (webinar) · `MR` (material rico) · `EVT` (evento) · `RMK` (remarketing) · `TRF` (trafego).
- **Prefixo da campanha** = `{TIPO}-{MMYY}` (ex.: `WBN-0625`). Pode usar um codigo curto da campanha no lugar.
- **Nome do criativo e do ad** = `{prefixo}_{sigla-publico}_{variante}` -> ex.: `WBN-0625_LKL_v1`, `WBN-0625_INT-MKT_v2`. A sigla de publico diferencia o mesmo criativo entre 2 adsets da mesma campanha (LKL=lookalike, RMK=remarketing, INT-XX=interesse, BROAD=aberto).
- **Nome da campanha segue a convencao da casa:** `[BR][CONVERSAO][Tema]` (ex.: `[BR][CONVERSAO][Remarketing-IA]`, `[BR][CONVERSAO][MOFU-Buzzmonitor]`). Use o token de objetivo real (`[CONVERSAO]`/`[TRAFEGO]`/`[ENGAJAMENTO]`/`[RECONHECIMENTO]`) e a regiao (`[BR]`). Mantem a classificacao do Bunzzai funcionando.
- **Nome do adset: descritivo, com o publico** (ex.: `[Remarketing - Visitas ao site + Engajamento + LaL 1% Clientes]`).
- **Atencao:** a Meta acrescenta automaticamente ` YYYY-MM-DD-<hash>` ao nome do **criativo** (visto no acervo) — e esperado, nao lutar contra.

---

## Criativo — 3 fontes -> `image_url` publica (auto-hospedar via Vercel)

O MCP da Meta nao sobe arquivo local: `ads_create_creative` aceita `image_hash` (acervo da conta) ou `image_url` (URL publica que o Meta busca). Ordem de preferencia:

1. **Post existente** -> `ads_create_ad` com `creative.object_story_id` ("pageID_postID") ou `ads_boost_ig_post`. Zero upload.
2. **Imagem ja no acervo** -> `ads_get_ad_images` (1 call, cache) -> usar `image_hash`.
3. **Arquivo novo (PC / Google Drive / repo `/criativo`)** -> **stage no Vercel** -> `image_url`:
   - Google Drive: baixar pra local primeiro (download via MCP trunca >3KB — nao serve direto).
   - repo `/criativo`: PNG em `criativos/{marca}/{regiao}/{slug}/criativo-N/*.png` (gitignored).
   - Copiar o PNG pro projeto Vercel de assets (reusa o mecanismo sibling do `/lp-publicar`) sob `/criativos-staging/{prefixo}/{arquivo}.png`, deployar, pegar `https://{dominio}/criativos-staging/{prefixo}/{arquivo}.png`, passar como `image_url`. O Meta ingere a imagem (gera `image_hash`) — a URL pode ser limpa depois.
   - **Esse deploy aciona o `guard_vercel_deploy.py`** (esperado): aprovar dentro do fluxo do `/meta-campanha`.
   - **Item de setup unico:** definir o dominio/projeto do bucket de staging (decisao do Victor). Ate definir, pedir a imagem ja como `image_url` publica ou ja no acervo.

Sempre confirmar pelo `ads_get_ad_preview` que o Meta conseguiu buscar a imagem antes de seguir.

---

## Frugalidade de requisicoes (anti-ban)

A API da Meta tem rate limit. Minimize chamadas:
- **1** `ads_get_ad_accounts` por sessao -> cachear (account_id, moeda, flags).
- `ads_get_ad_account_pages`, `ads_get_ad_account_custom_audiences`, `ads_get_datasets`, `ads_get_ad_images`: no maximo 1x cada, sob demanda, e cachear.
- **Nunca** re-listar pra "conferir" depois de criar — confie no ID retornado e grave no log local.
- Fluxos de edicao/pausa: ler primeiro o **log local** (`meta-ads/campanhas/{marca}/{YYYY-MM-DD}-{slug}.md`); so chamar `ads_get_ad_entities` (1x, filtrado) se o ID nao estiver no log.
- Nunca fazer polling/retry em loop.

---

## Log local de auditoria

Cada criacao/edicao grava em `meta-ads/campanhas/{marca}/{YYYY-MM-DD}-{slug}.md`: data, conta, IDs criados (campanha/adset/ad/criativo), estrutura, orcamento, status. Serve de fonte para edicoes futuras (frugalidade) e de historico. Nao contem PII.

---

## Notion

v1 nao publica no Notion (mantem frugal e local). Se o Victor pedir, publicar resumo em `Entregas` (ID em `conhecimento/config/notion-ids.md`).
