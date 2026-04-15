---
name: traduzir
description: Guia interativo de tradução. Faz perguntas com chips clicáveis e dispara a skill correta do pipeline trad-*. Usar quando o usuário digitar /traduzir sem saber qual comando rodar.
argument-hint: "(opcional) Ex: /traduzir | /traduzir pipeline copy.md pt-pt | /traduzir calibrar es-latam"
allowed-tools: AskUserQuestion, Read, Glob
---

# /traduzir — Router determinístico

Script fixo. Uma pergunta por vez. Pule se `$ARGUMENTS` já responde. Dispare direto após última pergunta — sem pedir confirmação.

## Fast-path

Se `$ARGUMENTS` contém tarefa + arquivo + idioma válidos, pule para Disparo.

| Atalho | Disparo |
|---|---|
| `pipeline {arquivo} {target}` | `/trad-pipeline {arquivo} {target}` |
| `traduzir {arquivo} {target}` | `/trad-traduzir {arquivo} {target}` |
| `revisar {arquivo} {target}` | `/trad-revisar {arquivo} {target}` |
| `calibrar {target}` | `/trad-calibrar {target}` |

Idiomas válidos: `pt-pt` `es-latam`

---

## Q1 — Tarefa

AskUserQuestion — question: "O que quer fazer com tradução?" header: "Tarefa" multiSelect: false

1. "Traduzir + revisar (Recomendado)" → skill=trad-pipeline, precisa_arquivo=sim
2. "Só traduzir" → skill=trad-traduzir, precisa_arquivo=sim
3. "Só revisar tradução" → skill=trad-revisar, precisa_arquivo=sim
4. "Calibrar idioma" → skill=trad-calibrar, precisa_arquivo=não

## Q2 — Arquivo

Pular se precisa_arquivo=não OU já em `$ARGUMENTS`.

Pergunte em texto livre: "Qual o caminho do arquivo? (ex: `traducao/copy-buzzmonitor.md`)"

## Q3 — Idioma

AskUserQuestion — question: "Qual idioma alvo?" header: "Idioma" multiSelect: false

1. "PT-PT" → pt-pt
2. "ES-LATAM" → es-latam

## Disparo

- Se precisa_arquivo=sim: Invoke Skill({skill}, args: "{arquivo} {target}")
- Se calibrar: Invoke Skill({skill}, args: "{target}")
