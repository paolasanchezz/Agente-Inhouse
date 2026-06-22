---
name: meta-ads-report
description: Gera relatório Markdown de Meta Ads a partir de dados já no banco local. Zero chamadas à API. Usar quando dados já foram coletados e o usuário quer re-gerar ou atualizar o relatório.
argument-hint: "[conta] [periodo] — ex: buzzmonitor_brl mes_atual | cxpress_usd mes_anterior"
allowed-tools: Bash, Read
version: 1.0.0
---

# Skill: /meta-ads-report — Gerar Relatório (sem nova coleta)

> Leia `.claude/skills/meta-ads/CONTEXT.md` antes de prosseguir.

## Quando usar
Quando os dados já foram coletados e o usuário quer apenas gerar ou re-gerar
o relatório Markdown sem fazer novas chamadas à API.

---

## Fluxo

```bash
cd meta-ads
python scripts/full_analysis.py --account [conta] --period [periodo] --only-report
```

O relatório é salvo em `meta-ads/data/reports/YYYY-MM-DD_{conta}_{periodo}.md`.

---

## Estrutura do relatório gerado
1. Visão Geral (totais consolidados)
2. Topo de Funil — por campanha / adset / anúncio
3. Fundo de Funil — por campanha / adset / anúncio
4. Campanhas Não Classificadas (se houver)
5. Análise de Tendências (3d / 7d / 15d / 30d)
6. Pontos Fortes (a preencher com análise)
7. Pontos de Atenção (a preencher com análise)
8. Sugestões de Ação (a preencher com análise)

## Após gerar
Ler o arquivo e apresentar a análise completa ao usuário, preenchendo as seções
de Pontos Fortes, Pontos de Atenção e Sugestões de Ação com base nos dados.
