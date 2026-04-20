---
name: landing-page
description: Guia interativo de landing pages. Faz perguntas com chips clicaveis e dispara a skill correta do pipeline lp-*. Usar quando o usuario digitar /landing-page sem saber qual comando rodar.
argument-hint: "(opcional) Ex: /landing-page | /landing-page nova buzzmonitor monitoramento-maio https://notion.so/... | /landing-page publicar buzzmonitor monitoramento-maio"
allowed-tools: AskUserQuestion, Read, Glob
---

# /landing-page — Router deterministico

Script fixo. Uma pergunta por vez. Pule se `$ARGUMENTS` ja responde. Dispare direto apos ultima pergunta — sem pedir confirmacao.

## Fast-path

Se `$ARGUMENTS` contem tarefa + parametros validos, pule para Disparo.

| Atalho | Disparo |
|---|---|
| `nova {marca} {slug} {fonte} [dominio]` | `/lp-pipeline {marca} {slug} {fonte} {dominio}` |
| `preparar {marca} {slug} {fonte}` | `/lp-preparar {marca} {slug} {fonte}` |
| `gerar {marca} {slug}` | `/lp-gerar {marca} {slug}` |
| `revisar {marca}/{slug}` | `/lp-revisar {marca}/{slug}` |
| `form {marca}/{slug} "{snippet}"` | `/lp-integrar-form {marca}/{slug} "{snippet}"` |
| `publicar {marca} {slug} [dominio]` | `/lp-publicar {marca} {slug} {dominio}` |

Marcas: `buzzmonitor` `buzzcreators` `cxpress` `elife`

---

## Q1 — Tarefa

AskUserQuestion — question: "O que quer fazer com a landing page?" header: "Tarefa" multiSelect: false

1. "LP nova do zero (pipeline completo) (Recomendado)" → fluxo=nova
2. "So estruturar copy" → fluxo=preparar
3. "So gerar HTML (ja tenho copy estruturada)" → fluxo=gerar
4. "Revisar LP existente" → fluxo=revisar
5. "Integrar formulario real (apos design aprovado)" → fluxo=form
6. "Publicar (deploy + dominio + relatorio)" → fluxo=publicar

---

## Fluxo: LP nova

Q: Marca — AskUserQuestion: "Qual marca?" header: "Marca" → Buzzmonitor | Buzzcreators | Cxpress | Elife → `marca`
Q: Slug — texto livre: "Slug da LP (kebab-case curto, ex: monitoramento-maio)." → `slug`
Q: Fonte — texto livre: "Onde esta a copy? (URL do Notion, caminho de arquivo ou cole o texto)" → `fonte`
Q: Dominio — texto livre: "Dominio personalizado (opcional — deixe vazio para usar a URL .vercel.app)." → `dominio`

→ Invoke Skill(lp-pipeline, args: "{marca} {slug} {fonte} {dominio}")

## Fluxo: Preparar

Q: Marca → `marca`
Q: Slug → `slug`
Q: Fonte → `fonte`

→ Invoke Skill(lp-preparar, args: "{marca} {slug} {fonte}")

## Fluxo: Gerar

Q: Marca → `marca`
Q: Slug → `slug`

→ Invoke Skill(lp-gerar, args: "{marca} {slug}")

## Fluxo: Revisar

Q: Marca → `marca`
Q: Slug → `slug`

→ Invoke Skill(lp-revisar, args: "{marca}/{slug}")

## Fluxo: Integrar form

Q: Marca → `marca`
Q: Slug → `slug`
Q: Snippet — texto livre: "Cole o snippet HTML do embed (Jotform, RD Station, HubSpot, etc.)" → `snippet`

→ Invoke Skill(lp-integrar-form, args: "{marca}/{slug} \"{snippet}\"")

## Fluxo: Publicar

Q: Marca → `marca`
Q: Slug → `slug`
Q: Dominio — texto livre: "Dominio personalizado (opcional)." → `dominio`

→ Invoke Skill(lp-publicar, args: "{marca} {slug} {dominio}")
