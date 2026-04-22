---
name: anuncios
description: Guia interativo de análise de Meta Ads. Faz perguntas com chips clicáveis e dispara a skill correta do pipeline meta-ads-*. Usar quando o usuário digitar /anuncios sem saber qual comando rodar.
argument-hint: "(opcional) Ex: /anuncios | /anuncios performance buzzmonitor_brl mes_atual | /anuncios tendencias cxpress_usd"
allowed-tools: AskUserQuestion, Read, Glob
---

# /anuncios — Router determinístico

Script fixo. Uma pergunta por vez. Pule se `$ARGUMENTS` já responde. Dispare direto após última pergunta — sem pedir confirmação. Meta Ads é **SOMENTE LEITURA**.

## Normalização de inputs

Antes de validar, **converta `conta` e `periodo` para lowercase**. Ex: `Buzzmonitor_BRL` → `buzzmonitor_brl`, `Mes_Atual` → `mes_atual`. Se o valor não estiver na lista permitida após normalizar, trate como ausente e pergunte via AskUserQuestion.

## Fast-path

Se `$ARGUMENTS` contém tarefa + conta (+ período quando aplicável, já normalizados), pule todas as perguntas e vá direto ao Disparo.

| Atalho | Disparo |
|---|---|
| `performance {conta} {periodo}` | `/meta-ads {conta} {periodo}` |
| `tendencias {conta}` | `/meta-ads-trends {conta}` |
| `fetch {conta} {periodo}` | `/meta-ads-fetch {conta} {periodo}` |
| `report {conta} {periodo}` | `/meta-ads-report {conta} {periodo}` |

Contas válidas: `buzzmonitor_brl` `buzzmonitor_usd` `buzzmonitor_eur` `cxpress_brl` `cxpress_usd` `cxpress_eur`
Períodos válidos: `mes_atual` `mes_anterior` `ultimos_30`

Se parcial, use o que tem e pergunte só o que falta.

---

## Q1 — Tarefa

AskUserQuestion — question: "O que quer saber dos anúncios?" header: "Tarefa" multiSelect: false

1. "Performance geral (Recomendado)" → skill=meta-ads, precisa_periodo=sim
2. "Tendências (CpL/CTR caindo?)" → skill=meta-ads-trends, precisa_periodo=não
3. "Só atualizar dados locais" → skill=meta-ads-fetch, precisa_periodo=sim
4. "Re-gerar relatório" → skill=meta-ads-report, precisa_periodo=sim

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

## Q4 — Período

Pular se precisa_periodo=não OU período já conhecido.

AskUserQuestion — question: "Qual período?" header: "Período" multiSelect: false

1. "Mês atual (Recomendado)" → mes_atual
2. "Mês anterior" → mes_anterior
3. "Últimos 30 dias" → ultimos_30

## Disparo

Invoke Skill({skill}, args: "{conta} {periodo}")
