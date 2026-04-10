---
name: meta-ads
description: Pipeline completo de Meta Ads — coleta estrutura + insights + gera relatório. Usar quando o usuário pede análise de performance, CpL alto, frequência, criativos, tendências, comparação de períodos, etc.
argument-hint: "[conta] [periodo] — ex: buzzmonitor_brl mes_atual | cxpress_usd ultimos_30"
allowed-tools: Bash, Read
---

# Skill: /meta-ads — Análise Completa de Meta Ads

> Leia `.claude/skills/meta-ads/CONTEXT.md` antes de prosseguir.

## Quando usar
Sempre que o usuário pedir análise de Meta Ads: performance de campanhas,
comparação de períodos, criativos fracos, tendências, CpL alto, frequência elevada, etc.

## Restrição Absoluta
**SOMENTE LEITURA.** Nunca executar, sugerir nem insinuar qualquer operação de escrita
na Meta Marketing API. Apenas GET. Nunca criar, pausar, editar, duplicar ou excluir.

---

## Inputs — confirmar sempre com o usuário antes de iniciar

### 1. Conta (obrigatório)
```
buzzmonitor_brl | buzzmonitor_usd | buzzmonitor_eur
cxpress_brl     | cxpress_usd     | cxpress_eur
```

### 2. Período (obrigatório)
```
mes_atual | mes_anterior | ultimos_30
```

### 3. Token
Verificar se `META_ACCESS_TOKEN` está no `.env` e se `META_TOKEN_CREATED_AT` indica
que o token ainda é válido. Se expirado ou faltando, interromper e pedir novo token
ANTES de qualquer chamada à API.

---

## Fluxo de Execução

### Passo 1 — Análise completa (coleta + relatório)
```bash
cd meta-ads
python scripts/full_analysis.py --account [conta] --period [periodo]
```

Esse comando faz tudo em sequência:
1. Verifica token e banco
2. Atualiza estrutura de campanhas (incremental — sem re-fetch do que já existe)
3. Atualiza insights para o período (incremental — sem re-fetch de datas existentes)
4. Gera relatório Markdown em `meta-ads/data/reports/`

### Passo 2 — Apresentar relatório
Ler o arquivo gerado em `meta-ads/data/reports/` e apresentar ao usuário com análise.

---

## Se os dados já estiverem no banco (análise sem nova coleta)
```bash
cd meta-ads
python scripts/full_analysis.py --account [conta] --period [periodo] --only-report
```

---

## Hierarquia Obrigatória de Análise
Conta → Campanhas → Conjuntos de Anúncios → Anúncios
Nunca pular níveis. Anomalias no nível inferior têm contexto no superior.

## Classificação de Campanhas
- 🔵 **Topo de Funil**: Webinar, Material Rico
- 🔴 **Fundo de Funil**: Remarketing
- ⚪ **Não Classificadas**: listar separado, sinalizar para revisão manual

## Status dos Benchmarks
🟢 Bom / 🟡 Aceitável / 🔴 Ruim
Carregados de `meta-ads/data/benchmarks.json` conforme conta (grupo de moeda) e tipo.
Frequência: <5 = 🟢 | 5–7 = 🟡 | >7 = 🔴 (benchmark global)

## Regras de Apresentação
- Todos os valores monetários usam o símbolo da moeda da conta (R$, $ ou €)
- Se uma campanha não tiver leads: apresentar métricas de tráfego + indicar "Sem leads no período"
- Se dados insuficientes (< 3 dias): dizer explicitamente, não especular
- Nunca inventar dados — sempre citar a fonte (banco local)
