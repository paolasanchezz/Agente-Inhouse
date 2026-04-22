---
name: newsletter
description: Guia interativo de geração de newsletters. Faz perguntas com chips clicáveis e dispara a skill correta do pipeline news-*. Usar quando o usuário digitar /newsletter sem saber qual comando rodar.
argument-hint: "(opcional) Ex: /newsletter | /newsletter pipeline buzzmonitor brasil | /newsletter pesquisar cxpress portugal"
allowed-tools: AskUserQuestion, Read, Glob
---

# /newsletter — Router determinístico

Script fixo. Uma pergunta por vez. Pule se `$ARGUMENTS` já responde. Dispare direto após última pergunta — sem pedir confirmação.

## Normalização de inputs

Antes de validar, **converta `marca` e `regiao` para lowercase**. Se após a normalização o valor não estiver na lista permitida, trate como ausente e pergunte via AskUserQuestion.

## Fast-path

Se `$ARGUMENTS` contém tarefa + marca + região válidos (já normalizados), pule para Disparo.

| Atalho | Disparo |
|---|---|
| `pipeline {marca} {regiao}` | `/news-pipeline {marca} {regiao}` |
| `pesquisar {marca} {regiao}` | `/news-pesquisar {marca} {regiao}` |
| `gerar {marca} {regiao}` | `/news-gerar {marca} {regiao}` |
| `revisar {marca} {regiao}` | `/news-revisar {marca} {regiao}` |

Marcas: `buzzmonitor` `buzzcreators` `cxpress` `elife`
Regiões: `brasil` `latam` `portugal`

---

## Q1 — Tarefa

AskUserQuestion — question: "O que quer fazer com newsletters?" header: "Tarefa" multiSelect: false

1. "Pipeline completo (Recomendado)" → skill=news-pipeline
2. "Só pesquisar" → skill=news-pesquisar
3. "Só gerar rascunhos" → skill=news-gerar
4. "Só revisar rascunhos" → skill=news-revisar

Se tarefa ∈ {gerar, revisar}, avise em 1 linha: "Essa etapa requer que `/news-pesquisar` já tenha sido executado."

## Q2 — Marca

AskUserQuestion — question: "Qual marca?" header: "Marca" multiSelect: false

1. "Buzzmonitor (Recomendado)"
2. "Buzzcreators"
3. "Cxpress"
4. "Elife"

→ marca (lowercase)

## Q3 — Região

AskUserQuestion — question: "Qual região?" header: "Região" multiSelect: false

1. "Brasil (PT-BR) (Recomendado)" → brasil
2. "LATAM (ES-LATAM)" → latam
3. "Portugal (PT-PT)" → portugal

## Disparo

Invoke Skill({skill}, args: "{marca} {regiao}")
