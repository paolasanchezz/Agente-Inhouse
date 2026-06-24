---
name: meta-campanha
description: Cria e gere campanhas de Meta Ads via o MCP oficial da Meta (escrita real). Atua como gestor de trafego senior — forca o briefing completo, classifica funil, questiona publico incoerente, mostra o plano pra confirmar, cria tudo PAUSADO e nunca liga verba sem aprovacao. Cobre criar campanha/adset/ad, editar, pausar/religar e renomear. Usar quando o usuario quer SUBIR ou MEXER em campanha (nao analisar — analise e /bunzzai).
argument-hint: "[acao] [marca] [briefing] — ex: criar buzzmonitor \"webinar social listening, R$30/dia, publico marketing BR\""
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
version: 1.1.0
---

# Skill: /meta-campanha — Criar e gerir campanhas Meta Ads

> **Leia `.claude/skills/meta-campanha/CONTEXT.md` antes de qualquer acao** — contas validas, classificacao de funil -> objetivo, sanity-check de publico, convencao de nomes, fonte de criativo, frugalidade e seguranca.

Os tools sao do **MCP oficial da Meta** (`mcp__<id>__ads_*`; o `<id>` varia por conexao — use o que estiver na sessao). Se nenhum `ads_*` estiver conectado, pare e peca pra conectar (Connectors do app -> `https://mcp.facebook.com/ads`).

## Quando usar
- O usuario quer **criar** campanha/adset/ad, **editar** (publico, posicionamento, orcamento, link), **pausar/religar** ou **renomear** no Meta Ads.

## Nao usar quando
- O usuario quer **analisar** performance (CpL, CTR, tendencia) -> use `/bunzzai` (somente leitura).
- A conta nao esta habilitada/consultavel no MCP (ex.: Cxpress Portugal UNSETTLED) -> recusar e explicar.

## Restricao de seguranca (inegociavel)
1. **Tudo nasce PAUSADO.** Nunca ativar no automatico.
2. **Ativar / religar** (`ads_activate_entity`, `ads_update_entity status=ACTIVE`) e **orcamento acima do teto** passam pelo hook `guard_meta_activate.py` E pela confirmacao da skill. Sempre mostrar custo/dia antes.
3. Escrita so via MCP oficial da Meta. Minimize requisicoes (ver CONTEXT — frugalidade/anti-ban).

---

## As 6 acoes que a skill cobre

| # | Acao | Tool principal |
|---|---|---|
| 1 | Criar nova campanha (opcional: ja com adset + ad) | `ads_create_campaign` (+ `_ad_set`, `_creative`, `_ad`) |
| 2 | Criar novo adset em campanha existente | `ads_create_ad_set` |
| 3 | Incluir novo ad em adset existente | `ads_create_creative` + `ads_create_ad` |
| 4 | Editar campanha/adset/ad (publico, posicionamento, orcamento, link, etc.) | `ads_update_entity` |
| 5 | Pausar **ou** religar campanha/adset/ad | `ads_update_entity status=PAUSED` / `ads_activate_entity` |
| 6 | Renomear | `ads_update_entity` campo `name` |

---

## Fluxo de execucao

### Passo 0 — Carregar contexto (frugal)
Ler `CONTEXT.md`, `meta-ads/data/benchmarks.json`, e a tabela de classificacao do `.claude/skills/bunzzai/CONTEXT.md`. Fazer **1** `ads_get_ad_accounts` e cachear (account_id, moeda, flags). Resolver marca -> account_id. Se a conta estiver indisponivel (Cxpress PT) ou sem pagamento (Buzzcreators), avisar.

### Passo 1 — Determinar a ACAO
Identificar qual das 6 acoes. Se ambiguo, perguntar com chips (`AskUserQuestion`). Nao prosseguir sem saber a acao.

### Passo 2 — GATE DE BRIEFING COMPLETO (critico — o usuario costuma nao informar tudo)
Para a acao escolhida, montar um **checklist de campos obrigatorios** e mostrar **o que ja sei × o que falta**, pedindo o que falta antes de tocar no MCP. **Nunca assumir em silencio.** Campos por acao:

- **Criar campanha:** marca/conta · objetivo OU tipo de funil (webinar/material rico/MoFu/remarketing/...) · publico · orcamento + CBO/ABO (default ABO da casa) · **LP de destino especifica** (nao a home) · **pixel + evento de conversao** (se otimizar por conversao — quase sempre) · **UTM** (embutir no link) · idade (default 28-50) · fonte do criativo · regiao/idioma · agendamento (ou "rodar continuo").
- **Criar adset:** campanha-mae (ID ou nome) · publico · orcamento (se ABO) · optimization_goal · placements · agendamento.
- **Incluir ad:** adset-mae · criativo (fonte) · texto (primary text/headline/description) · link · CTA.
- **Editar:** entidade (qual e qual nivel) · exatamente quais campos -> quais valores novos.
- **Pausar/religar:** entidade + nivel + (pausar | religar).
- **Renomear:** entidade + nivel + nome novo.

Mostrar como lista marcada (ex.: "✅ Conta: Buzzmonitor BR · ❓ Publico: faltando · ❓ Orcamento: faltando"). So avancar quando o essencial estiver completo.

### Passo 3 — Camada de especialista (gestor de trafego senior)
- **Funil -> defaults:** classificar o tipo e propor objetivo (ODAX) + optimization_goal + billing + bid + placements pela tabela do CONTEXT. Explicar o porque em 1 linha. Mostrar CpL/CTR esperado vs `benchmarks.json`.
- **Sanity-check de publico (obrigatorio):** comparar o publico pedido com o ICP da marca (CONTEXT). Se incoerente, **questionar** ("Esse publico se importa com [dor da marca]? Quer mesmo?") antes de seguir — nao corrigir sozinho.
- **Copy (se for escrever texto):** carregar os 3 pilares (CONTEXT -> protocolo de copy). Se a copy ja veio pronta, so diagramar.
- Aplicar a **convencao de nomes** (CONTEXT) ao criativo e ao ad.

### Passo 4 — Criativo -> `image_url`/`image_hash`
Resolver a fonte (post existente -> `object_story_id`; acervo -> `image_hash` via `ads_get_ad_images`; arquivo novo -> stage no Vercel -> `image_url`). Detalhe e item de setup do bucket: ver CONTEXT. Confirmar com `ads_get_ad_preview` que o Meta buscou a imagem.

### Passo 5 — MOSTRAR O PLANO e confirmar (critico)
Antes de QUALQUER escrita, apresentar o plano em linguagem simples (formato abaixo) e pedir confirmacao. So criar apos o "ok".

### Passo 6 — Executar (frugal, pausado)
Encadear `ads_create_campaign` -> `ads_create_ad_set` -> `ads_create_creative` -> `ads_create_ad` (ou `ads_update_entity` na edicao). Sem reads intermediarios. Se o orcamento estiver acima do teto, o hook vai pedir confirmacao — explicar ao usuario e so aprovar se for proposital. Gravar os IDs retornados no **log local** (`meta-ads/campanhas/{marca}/{YYYY-MM-DD}-{slug}.md`).

### Passo 7 — Gate de ativacao (NUNCA pular)
Ao terminar, **nao ativar**. Mostrar o que iria ao ar e o custo/dia, e perguntar: "Quer que eu ative agora?" So chamar `ads_activate_entity` apos "sim" explicito — e o hook vai pedir a confirmacao final. Ativar de cima pra baixo (campanha -> adset -> ad); lembrar que ativar o pai nao ativa os filhos. Religar (pausado->ativo) segue a mesma regra.

### Passo 8 — Log + resumo
Atualizar o log local. Resumir ao usuario: IDs criados, estrutura, status (PAUSADO), e link do Ads Manager (`https://adsmanager.facebook.com/adsmanager/manage/campaigns?act=<account_id>`).

---

## Acoes 4-6 (editar / pausar-religar / renomear) — descoberta frugal de ID
1. Pegar o ID: primeiro o **log local**; se nao estiver, **1** `ads_get_ad_entities` (conta, filtrado por nome). Nunca listar tudo "pra achar".
2. Confirmar com o usuario qual entidade e quais mudancas (Passo 2 reduzido).
3. Mostrar o plano (antes × depois) e confirmar.
4. Executar `ads_update_entity` (ou `ads_activate_entity` p/ religar). Orcamento acima do teto / religacao -> hook pede confirmacao.

---

## Formato do plano de confirmacao (Passo 5)

```
PLANO — vou CRIAR (tudo PAUSADO, nada gasta ate voce ligar)

Conta:     Buzzmonitor BR (BRL) · act 733381876770151
Campanha:  WBN-0625 — Webinar Social Listening
           Objetivo: OUTCOME_LEADS · CBO · R$ 30,00/dia · bid: lowest cost
Adset:     WBN-0625_MKT-BR
           Otimizacao: OFFSITE_CONVERSIONS (pixel da LP) · Publico: marketing/CX, BR, 25-55
           Placements: Advantage+ · sem cap de idade rigido
Ad:        WBN-0625_MKT-BR_v1
           Criativo: <fonte> · Link: https://... · CTA: SAIBA_MAIS
           Texto: "<primary text>"

Esperado (benchmark webinar BRL): CpL <= R$ 18 · CTR link >= 1,0% · Conv. LP >= 15%
Sanity-check publico: OK (bate com ICP Buzzmonitor) [ou: ⚠️ ressalva ...]

Confirma criar assim? (depois eu mostro o custo e pergunto se quer ativar)
```

Para editar, mostrar **antes -> depois** de cada campo. Sempre marcar o que e PAUSADO e o que gasta.

---

## Regras de apresentacao
- Valores em centavos na API; **mostrar ao usuario na moeda** (R$/US$/EUR) com 2 casas.
- Nunca inventar IDs de interesse, pixel, pagina ou audiencia — buscar (`ads_get_ad_account_pages`, `ads_get_datasets`, `ads_get_ad_account_custom_audiences`, 1x cada) ou pedir ao usuario.
- Toda criacao = PAUSADO; deixar isso explicito no resumo.
- Custos sempre por dia (e total se lifetime). Comparar com benchmark e com o teto do guardrail.

---

## Comportamento de erro
- **Nenhum tool `ads_*` conectado** -> pedir pra conectar o MCP oficial; abortar.
- **Conta indisponivel** (UNSETTLED / sem pagamento / `is_ads_mcp_enabled=false`) -> recusar a conta, explicar o motivo retornado.
- **Meta rejeita a criacao** (VALIDATION) -> mostrar a mensagem exata da Meta e o campo provavel (ex.: objetivo legado nao suportado — usar ODAX; falta `promoted_object`/pixel; orcamento abaixo do minimo da moeda). Corrigir e reapresentar o plano. Nao tentar em loop.
- **Hook pediu confirmacao** (ativacao/orcamento) -> e o comportamento esperado; explicar ao usuario o que sera ligado/gasto e so prosseguir com "sim".
- **Imagem nao buscavel pelo Meta** (`ads_get_ad_preview` vazio/erro) -> revisar a URL publica (staging) antes de criar o ad.
