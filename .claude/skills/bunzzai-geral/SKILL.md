---
name: bunzzai-geral
description: Relatorio consolidado de tendencias de Meta Ads das 6 contas Elife (Buzzmonitor BRL/USD/EUR + Cxpress BRL/USD/EUR) via MCP Bunzzai — drill-down Conta -> Funil -> Adset -> Ad, publica no Notion. Substituto do antigo /meta-ads-geral.
argument-hint: "(sem argumentos — roda sempre as 6 contas com janelas 7d/15d/30d)"
allowed-tools: Bash, Read, mcp__claude_ai_Notion__notion-create-pages
version: 1.0.0
---

# Skill: /bunzzai-geral — Relatorio Consolidado das 6 Contas via Bunzzai

> Leia `.claude/skills/bunzzai/CONTEXT.md` antes de prosseguir — contas validas, classificacao de campanhas, benchmarks, matriz de cenarios e diferencas metricas Bunzzai vs Meta.

## Quando usar

Quando o usuario quer uma **visao unica das 6 contas** (Buzzmonitor BRL/USD/EUR + Cxpress BRL/USD/EUR), com tendencias separadas por etapa de funil (Topo e Fundo) e drill-down ate nivel de anuncio. Relatorio publicado no Notion.

## Nao usar quando

- O usuario quer analise de **uma conta especifica** -> use `/bunzzai [conta]`.
- O usuario quer auditar discrepancia entre Bunzzai e Meta API direta -> rodar manualmente `meta-ads-legacy/scripts/audit_vs_bunzzai.py`.

## Restricao Absoluta

**SOMENTE LEITURA.** Mesma regra do `/bunzzai` — apenas tools `tool_get_*`, `tool_find_*`, `list_*`, `get_*_insights`, `tool_get_ad_performance`, `tool_get_campaign_monitoring`, `compare_*`, `search_entity`. Nunca criar, pausar, editar, duplicar ou excluir.

---

## Fluxo de Execucao

### Passo 1 — Resolver as 2 empresas no Bunzzai

```
mcp__bunzzai__tool_find_company(query="Buzzmonitor")
mcp__bunzzai__tool_find_company(query="Cxpress")
```

Anotar os 2 `company_id`s. Se Cxpress nao for encontrada (CRM Bunzzai pode nao ter cadastro completo), avisar usuario e seguir so com Buzzmonitor — relatorio sai com "Cxpress: nao mapeada no Bunzzai".

### Passo 2 — Avisar usuario do tempo estimado

"Vou coletar dados das 6 contas via Bunzzai (leva ~2-4 min). Sem rate limit de token Meta."

### Passo 3 — Para cada uma das 6 contas-moeda

Loop fixo (ordem importa pro relatorio final):

```
contas = [
  ("buzzmonitor_brl", company_id_buzz, "BRL", "R$"),
  ("buzzmonitor_usd", company_id_buzz, "USD", "$"),
  ("buzzmonitor_eur", company_id_buzz, "EUR", "€"),
  ("cxpress_brl",     company_id_cxp,  "BRL", "R$"),
  ("cxpress_usd",     company_id_cxp,  "USD", "$"),
  ("cxpress_eur",     company_id_cxp,  "EUR", "€"),
]
```

Para cada `(conta_key, company_id, moeda, simbolo)`:

#### 3.a Listar e filtrar campanhas por moeda

```
mcp__bunzzai__list_campaigns(company_id=<id>)
```

Filtrar pelo nome conforme heuristica do `bunzzai/CONTEXT.md`:
- `_brl` -> sem token de pais OU contendo "BR"/"Brasil"/"brl"
- `_usd` -> "Latam"/"Latin"/"USD"/"ES"/"MX"/"CO"/"AR"
- `_eur` -> "EU"/"Portugal"/"PT"/"ES Europa"/"EUR"

Se zero campanhas casarem: anotar `"<conta_key>: sem campanhas Bunzzai"` e seguir pra proxima conta — nao chutar.

#### 3.b Drill-down por campanha: adsets e ads

Para cada campanha filtrada:

```
mcp__bunzzai__list_campaign_ads(campaign_id=<id>)
```

Anotar lista de adsets/ads com seus `id`s internos.

#### 3.c Historico de monitoramento por ad

Para cada ad:

```
mcp__bunzzai__tool_get_ad_performance(ad_id=<id>)
```

Capturar `monitoring_history` (lista de snapshots cumulativos).

#### 3.d Calcular janelas 7d/15d/30d via diff de snapshots

Mesmo Python embed do `/bunzzai` SKILL.md §5 — passar o `monitoring_history` via stdin e receber trends + alerta de cron travado.

### Passo 4 — Classificar campanhas e agregar diagnostico

Para cada campanha:

1. **Classificar tipo** (webinar / material_rico / remarketing / nao_classificada) conforme tabela do `bunzzai/CONTEXT.md`.
2. **Agregar metricas por janela** somando os ads da campanha:
   - `spend_30d` = soma de `spend_30d` dos ads
   - `clicks_30d`, `impressions_30d`, `conversions_30d` = idem
   - `cpl_30d` = `spend_30d / conversions_30d` (se conv ≥ 1)
   - `ctr_30d` = `clicks_30d / impressions_30d` (se imp > 0)
   - `conv_lp_30d` = `conversions_30d / clicks_30d` (se cli > 0)
3. **Calcular tendencias** comparando janelas (7d vs 15d, 15d vs 30d) — mesma regra do `/bunzzai`.
4. **Aplicar benchmarks** indexando por `benchmark_group` (`brl`/`usd`/`eur`) × `campaign_type`.
5. **Cenario** conforme matriz cruzada CpL × CTR × Conv. LP.

### Passo 5 — Montar relatorio consolidado

```markdown
# Bunzzai — Tendencias Gerais — YYYY-MM-DD

## Resumo Executivo

- Periodo de analise: ultimos 30 dias (snapshots Bunzzai)
- Contas cobertas: <N>/6  (listar contas vazias se houver)
- Total de campanhas analisadas: <N>  (Topo: <N> · Fundo: <N> · Nao classificadas: <N>)
- Ads com cron travado: <N>  (listar)
- Investido 30d por moeda × funil **(nunca soma entre moedas)**:
  - BRL Topo: R$ <X>  · BRL Fundo: R$ <X>
  - USD Topo: $ <X>   · USD Fundo: $ <X>
  - EUR Topo: € <X>   · EUR Fundo: € <X>
- Direcao recente do CpL:
  - Caindo: <N> campanhas (<%>)
  - Estavel: <N> (<%>)
  - Subindo: <N> (<%>)
- Distribuicao de cenarios:
  - 🏆 Ouro: <N> | 🔵 Filtro natural: <N> | ⚠️ Gargalo LP: <N> | 🚨 Promessa × entrega: <N> | 🔄 Potencial travado: <N> | 💀 Substituir: <N> | ❓ Sem dados: <N>

---

## Buzzmonitor Brasil (BRL)

### >> Topo de Funil

#### Campanha: <nome> [tipo: webinar]
<tabela trends: Metrica | 30d | 15d | 7d | Tend. Recente | Tend. Estrutural>

##### Adset: <nome>
<tabela trends>

###### Ad: <nome>  <[CRON TRAVADO: N dias congelados desde YYYY-MM-DD] se aplicavel>
<tabela trends>

#### Diagnostico — Campanha <nome>
| CpL | CTR | Conv. LP | Cenario | Acao |
|---|---|---|---|---|
| [OK/RUIM] valor | [OK/RUIM] valor | [OK/RUIM] valor | 🏆 Ouro | Escalar... |

### >> Fundo de Funil
...

### >> Nao Classificadas
...

(repete pras 5 contas restantes)

---

## Avisos
- <Cron travado em X ads, listar quais e desde quando>
- <Campanhas nao classificadas — nome nao bateu com heuristica>
- <Contas sem campanhas no Bunzzai>

## Cross-check sugerido
Para campanhas com CpL [OK] mas perto do threshold ou decisoes de budget >R\$ 1.000, rodar manualmente `meta-ads-legacy/scripts/audit_vs_bunzzai.py` (requer token Meta fresh).
```

### Passo 6 — Salvar e apresentar

Salvar em `meta-ads-legacy/reports/{YYYY-MM-DD}_bunzzai_geral_todas_contas.md` (ou criar pasta nova `relatorios-bunzzai/` se preferir — combinar com Victor).

Apresentar ao usuario **somente o Resumo Executivo** + caminho do arquivo completo. Nao despejar as 500+ linhas no chat.

### Passo 7 — Publicar no Notion

**Sempre** perguntar:

> "Deseja publicar este relatorio Bunzzai no Notion?"

Se sim:
1. Ler `conhecimento/config/notion-ids.md`, pegar ID da chave `entregas`.
2. Criar pagina com `mcp__claude_ai_Notion__notion-create-pages`:
   - **parent**: ID da chave `entregas` — fixo, nao buscar
   - **title**: `Bunzzai — Tendencias Gerais — <YYYY-MM-DD>`
   - **content**: relatorio completo
3. Confirmar com link da pagina criada.

---

## Filtros de relevancia

Pra manter o relatorio legivel:

- **Adsets**: omitidos se `spend_30d = 0`.
- **Ads**: omitidos se `spend_30d = 0` OU (`conversions_30d < 1` E `impressions_30d < 1000`).
- Contadores no rodape de cada secao informam quantos foram omitidos.

## Comportamento de erro

- **Empresa nao encontrada no Bunzzai** -> avisar e seguir com a outra (relatorio parcial).
- **Conta-moeda sem campanhas filtradas** -> listar contas vazias no resumo executivo, nao bloquear.
- **Snapshots todos congelados em uma campanha** -> reportar "Cron sem atualizacao ha mais de 30 dias — pedir engenharia destravar" e omitir do diagnostico cruzado.
- **MCP Bunzzai fora do ar** -> abortar com mensagem clara.

## Observacoes

- **Moedas sao segregadas**: o resumo executivo nunca soma BRL+USD+EUR. Quando agrega, usa % ou contagem.
- **Campanhas sem classificacao**: aparecem na secao "Nao Classificadas" da conta — alertar se o volume for alto (sugere atualizar a lista de keywords no `bunzzai/CONTEXT.md`).
- **So leitura**: este fluxo nunca pausa, edita ou cria campanhas.
- **Sem dependencia de token Meta**: Bunzzai e MCP em tempo real. Nao precisa setup local.
