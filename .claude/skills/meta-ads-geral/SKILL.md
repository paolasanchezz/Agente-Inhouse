---
name: meta-ads-geral
description: Relatório consolidado de tendências de Meta Ads das 6 contas — drill-down Conta→Funil→Adset→Ad, publica no Notion.
argument-hint: "(sem argumentos — roda sempre as 6 contas nos últimos 30 dias)"
allowed-tools: Bash, Read, mcp__claude_ai_Notion__notion-create-pages
version: 1.0.0
---

# Skill: /meta-ads-geral — Relatório Consolidado Multi-Conta

> Leia `.claude/skills/meta-ads/CONTEXT.md` antes de prosseguir.

## Quando usar

Quando o usuário quer uma **visão única das 6 contas** (Buzzmonitor BRL/USD/EUR + Cxpress BRL/USD/EUR), com tendências separadas por etapa de funil (Topo e Fundo) e drill-down até nível de anúncio. Relatório é publicado no Notion.

## Não usar quando

- O usuário quer análise de **uma conta específica** → use `/meta-ads` ou `/meta-ads-trends`.
- O usuário quer só atualizar os dados locais → use `/meta-ads-fetch`.

---

## Fluxo

### 1. Verificar token e setup

```bash
cd meta-ads
python scripts/check_setup.py
```

Se o token estiver expirado ou faltando, interromper e pedir novo token. Caso contrário, avisar o usuário: "Vou coletar dados das 6 contas (leva ~3-5 min)."

### 2. Fetch das 6 contas

**Ordem importa**: `fetch_campaigns.py` popula a estrutura (campaigns/adsets/ads) e precisa rodar antes de `fetch_insights.py`.

```bash
# Estrutura (campaigns + adsets + ads)
for acct in buzzmonitor_brl buzzmonitor_usd buzzmonitor_eur cxpress_brl cxpress_usd cxpress_eur; do
  python scripts/fetch_campaigns.py --account "$acct" --include-ads
done

# Insights diários (spend, impressões, leads etc.)
for acct in buzzmonitor_brl buzzmonitor_usd buzzmonitor_eur cxpress_brl cxpress_usd cxpress_eur; do
  python scripts/fetch_insights.py --account "$acct" --period ultimos_30 --include-ads
done
```

Se alguma conta falhar (erro de rate limit persistente, token inválido só para uma), continuar as demais e avisar ao usuário no final.

### 3. Gerar relatório consolidado

```bash
python scripts/full_trends_report.py > /tmp/meta-ads-geral.md
```

O script já salva automaticamente em `meta-ads/data/reports/{YYYY-MM-DD}_geral_todas_contas.md`.

### 4. Apresentar ao usuário

Mostrar **apenas o Resumo Executivo** ao usuário (primeiras seções do relatório — contagem por funil, gasto por moeda×funil, direção do CpL, distribuição de cenários), junto com o caminho do arquivo completo. Não despejar as 500+ linhas no chat.

### 5. Publicar no Notion

**Sempre** perguntar:

> "Deseja publicar este relatório no Notion?"

Se sim, criar página com `mcp__claude_ai_Notion__notion-create-pages`:
- **parent**: ID lido de `conhecimento/config/notion-ids.md` (chave `entregas`) — fixo, não buscar
- **title**: `Meta Ads — Tendências Gerais — {YYYY-MM-DD}`
- **content**: conteúdo completo do arquivo `.md` gerado

Confirmar ao usuário com o link da página criada.

---

## Estrutura do relatório

```
# Meta Ads — Tendências Gerais — {data}

## Resumo Executivo
- Contagem de campanhas por funil
- Investido 30d por moeda × funil (nunca soma entre moedas)
- Direção recente do CpL (% de campanhas caindo / subindo / estáveis)
- Distribuição de cenários

## Buzzmonitor Brasil (BRL)
### >> Topo de Funil
#### Campanha: {nome} [tipo: webinar]
<tabela trends>
##### Adset: {nome}
<tabela trends>
###### Ad: {nome}
<tabela trends>
#### Diagnóstico — Topo de Funil
<matriz CpL × CTR × Conv.LP × Cenário>

### >> Fundo de Funil
...

### >> Não Classificadas
...

## Buzzmonitor Latam (USD)
...

(repete para as 6 contas)
```

## Filtros de relevância

Para manter o relatório legível:

- **Adsets**: omitidos se `spend_30d = 0`.
- **Ads**: omitidos se `spend_30d = 0` OU (`leads_30d < 1` E `impressions_30d < 1000`).
- Contadores no rodapé de cada seção informam quantos foram omitidos.

## Diagnóstico cruzado

Aplica a matriz da `/meta-ads-trends` em **nível de campanha** (aplicar em cada ad gera ruído):

| Cenário | CpL | CTR | Conv.LP | Ação |
|---|---|---|---|---|
| 🏆 Ouro | Bom + ↓ | Bom | Boa | Escalar, marcar como referência |
| 🔵 Filtro natural | Bom | Ruim | Boa | Manter, testar hook mais amplo |
| ⚠️ Gargalo de LP | Bom | Bom | Ruim | Otimizar LP antes de escalar |
| 🚨 Promessa × entrega | Ruim | Bom | Ruim | Auditar LP vs criativo |
| 🔄 Potencial travado | Ruim | Bom | Boa | Checar budget/audiência |
| 💀 Substituir | Ruim | Ruim | Ruim | Pausar, criar criativo novo |
| ❓ Sem dados | — | — | — | Aguardar mais dados |

Os limiares de "bom"/"ruim" vêm de `meta-ads/data/benchmarks.json`, indexados por `benchmark_group` (brl/usd/eur) × `campaign_type` (webinar/material_rico/remarketing).

---

## Observações

- **Moedas são segregadas**: o resumo executivo nunca soma BRL+USD+EUR. Quando agrega, usa % ou contagem.
- **Campanhas sem classificação** (sem palavra-chave conhecida no nome) aparecem na seção "Não Classificadas" da conta — alertar usuário se o volume for alto.
- **Só leitura**: este fluxo nunca pausa, edita ou cria campanhas.
- Script zero-API: `full_trends_report.py` só lê o SQLite local. Se precisar de dados frescos, o passo 2 (fetch) é o único que chama a Meta API.
