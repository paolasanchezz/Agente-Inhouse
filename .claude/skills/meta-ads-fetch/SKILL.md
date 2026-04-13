---
name: meta-ads-fetch
description: Atualiza dados locais de campanhas e insights sem gerar relatório. Usar antes de análise manual ou quando o usuário quer só sincronizar o banco local.
argument-hint: "[conta] [periodo] — ex: buzzmonitor_brl mes_atual | cxpress_eur ultimos_30"
allowed-tools: Bash, Read
version: 1.0.0
---

# Skill: /meta-ads-fetch — Atualização de Dados

> Leia `.claude/skills/meta-ads/CONTEXT.md` antes de prosseguir.

## Quando usar
Quando o usuário quer só atualizar os dados locais sem gerar relatório,
ou antes de uma análise manual dos dados brutos no banco.

---

## Fluxo

### Atualizar estrutura (campanhas → adsets → ads)
```bash
cd meta-ads
python scripts/fetch_campaigns.py --account [conta]
```

### Atualizar insights para um período
```bash
cd meta-ads
python scripts/fetch_insights.py --account [conta] --period [mes_atual|mes_anterior|ultimos_30]
```

### Ambos em sequência
```bash
cd meta-ads
python scripts/fetch_campaigns.py --account [conta] && \
python scripts/fetch_insights.py --account [conta] --period [periodo]
```

---

## Comportamento incremental (by design)
- Campanhas coletadas = ACTIVE atualmente ∪ spend > 0 nos últimos 30 dias (3 chamadas)
- Adsets incluem `daily_budget` e `lifetime_budget` (orçamento ABO coletado corretamente)
- Datas de insights já presentes no banco não geram nova chamada à API
- Dados de hoje nunca são coletados (dia incompleto)
- Se a saída indicar "0 novas linhas inseridas", é correto — dados já estavam no cache
