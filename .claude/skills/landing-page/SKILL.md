---
name: landing-page
description: Guia interativo de landing pages. Faz perguntas com chips clicaveis e dispara a skill correta do pipeline lp-*. Usar quando o usuario digitar /landing-page sem saber qual comando rodar.
argument-hint: "(opcional) Ex: /landing-page | /landing-page nova buzzmonitor monitoramento-maio https://notion.so/... | /landing-page alterar buzzmonitor monitoramento-maio | /landing-page publicar buzzmonitor monitoramento-maio"
allowed-tools: AskUserQuestion, Read, Glob
version: 1.2.0
---

# /landing-page — Router deterministico

Script fixo. Uma pergunta por vez. Pule se `$ARGUMENTS` ja responde. Dispare direto apos ultima pergunta — sem pedir confirmacao.

## Normalizacao de inputs

Antes de validar, **converta `marca` e `slug` para lowercase**. O slug deve ser kebab-case minusculo (se vier `Monitoramento-Maio`, normalize para `monitoramento-maio`). Se `marca` nao estiver na lista permitida apos normalizar, trate como ausente e pergunte via AskUserQuestion.

## Fast-path

Se `$ARGUMENTS` contem tarefa + parametros validos (ja normalizados), pule para Disparo.

| Atalho | Disparo |
|---|---|
| `nova {marca} {slug} {fonte} [dominio]` | `/lp-pipeline {marca} {slug} {fonte} {dominio}` |
| `alterar {marca} {slug}` | seguir Fluxo: Alterar (sub-pergunta sobre o que mudou) |
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
2. "Alterar LP existente (ja publicada)" → fluxo=alterar
3. "Etapa especifica do pipeline" → fluxo=etapa (Q1b decide qual)

(AskUserQuestion suporta ate 4 opcoes + Other automatico — manter Q1 enxuta. Detalhamento via Q1b se a opcao 3 for escolhida, ou via fast-path direto na linha de comando.)

### Q1b — Etapa especifica (so se Q1 = etapa)

AskUserQuestion — question: "Qual etapa do pipeline?" header: "Etapa" multiSelect: false

1. "Preparar copy (estruturar em blocos rotulados)" → fluxo=preparar
2. "Gerar HTML (ja tenho copy.txt)" → fluxo=gerar
3. "Revisar LP existente (auditoria + a11y + GTM)" → fluxo=revisar
4. "Integrar formulario real ou Publicar" → AskUserQuestion: "Qual?" → form/publicar → fluxo=form OU fluxo=publicar

---

## Fluxo: Alterar

Antes de perguntar, abrir `landing-pages/CONTEXT.md` e ler **§2.2** (matriz canonica "o que mudou → o que rodar") e **§7.1** (anti-padroes — em especial nao editar a sibling).

O advisor coleta marca/slug + categoria de mudanca; **a decisao fina (qual skill, em que ordem) sai da §2.2 do CONTEXT**, nao desta skill. Se a §2.2 for atualizada, o advisor segue automaticamente — nao duplicar a tabela aqui.

Q: Marca → `marca`
Q: Slug → `slug`
Q: O que mudou? — AskUserQuestion: "O que voce esta alterando nessa LP?" header: "Mudanca" multiSelect: false

1. "Copy / texto" → mudanca=copy
2. "Visual / CSS / HTML" → mudanca=visual
3. "Imagem (logo, mascote, ilustracao) ou Form ou GTM ou Dominio" → mudanca=outros (Q sub-categoria)

Se `mudanca=outros`, perguntar sub-categoria (asset / form / tracking / dominio) com AskUserQuestion 4-options.

**Resolucao:** consultar `landing-pages/CONTEXT.md §2.2` na linha correspondente a `mudanca` e seguir o roteiro literal (qual arquivo editar, quais skills rodar, em que ordem). Se a categoria for ambigua (ex: "mudanca grande de copy" vs "typo"), perguntar ao usuario antes de disparar.

Em todos os casos, ao final lembrar: "fonte fica em `landing-pages/{marca}/{slug}/`, sibling fora do repo e descartavel — nunca editar la direto" (CONTEXT §7.1).

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
