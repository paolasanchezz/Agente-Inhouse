---
name: anuncios
description: Guia interativo de análise de Meta Ads. Faz perguntas com chips clicáveis e dispara /bunzzai (1 conta) ou /bunzzai-geral (consolidado das 6 contas). Usar quando o usuário digitar /anuncios sem saber qual comando rodar.
argument-hint: "(opcional) Ex: /anuncios | /anuncios buzzmonitor_brl | /anuncios geral"
allowed-tools: AskUserQuestion, Read, Glob
---

# /anuncios — Router determinístico (Bunzzai)

Script fixo. Uma pergunta por vez. Pule se `$ARGUMENTS` já responde. Dispare direto após última pergunta — sem pedir confirmação. Meta Ads é **SOMENTE LEITURA**.

> Desde 2026-06-22, todas análises de Meta Ads passam pelo **Bunzzai** (MCP do CRM próprio). O pipeline antigo `meta-ads-*` foi desativado — ver `.claude/skills-desativadas/`.

## Normalização de inputs

Antes de validar, **converta `conta` para lowercase**. Ex: `Buzzmonitor_BRL` → `buzzmonitor_brl`. Se o valor não estiver na lista permitida após normalizar, trate como ausente e pergunte via AskUserQuestion.

## Fast-path

Se `$ARGUMENTS` já indica claramente a intenção, pule todas as perguntas e dispare direto.

| Atalho | Disparo |
|---|---|
| `geral` ou `consolidado` ou `todas` | `/bunzzai-geral` |
| `{conta}` (uma das 6 válidas) | `/bunzzai {conta}` |

Contas válidas: `buzzmonitor_brl` `buzzmonitor_usd` `buzzmonitor_eur` `cxpress_brl` `cxpress_usd` `cxpress_eur`

Se parcial (ex: só "buzzmonitor" sem moeda), use o que tem e pergunte só o que falta.

---

## Q1 — Escopo

Pular se `$ARGUMENTS` já indica `geral` ou conta específica.

AskUserQuestion — question: "O que quer analisar?" header: "Escopo" multiSelect: false

1. "Uma conta específica (Recomendado)" → fluxo Q2/Q3 abaixo
2. "Consolidado das 6 contas" → dispara `/bunzzai-geral` direto (publica no Notion)

## Q2 — Marca

Pular se conta já conhecida via `$ARGUMENTS`.

AskUserQuestion — question: "Qual marca da conta?" header: "Marca" multiSelect: false

1. "Buzzmonitor"
2. "Cxpress"

## Q3 — Moeda

Pular se conta já conhecida via `$ARGUMENTS`.

AskUserQuestion — question: "Qual moeda?" header: "Moeda" multiSelect: false

1. "BRL (R$)"
2. "USD ($)"
3. "EUR (€)"

→ conta = `{marca}_{moeda}` (tudo lowercase)

## Disparo

- Se escopo = "consolidado das 6 contas": `Invoke Skill(bunzzai-geral)`.
- Senão: `Invoke Skill(bunzzai, args: "{conta}")`.
