---
name: criativo
description: Guia interativo de criativos. Faz perguntas com chips clicaveis e dispara a skill criativo-gerar com o enquadramento certo (tipo, uso organico/anuncio, formato). Usar quando o usuario digitar /criativo sem saber os parametros.
argument-hint: "(opcional) Ex: /criativo | /criativo cxpress brasil carrossel anuncio 4x5 case-10-para-4"
allowed-tools: AskUserQuestion, Read, Glob, Skill
---

# /criativo — Router deterministico

Script fixo. Uma pergunta por vez. Pule a pergunta se `$ARGUMENTS` ja responde. Dispare direto
apos a ultima pergunta — sem pedir confirmacao.

## Normalizacao de inputs

Antes de validar, **converta para lowercase** os identificadores (`marca`, `regiao`, `tipo`,
`uso`, `formato`). Ex: `Cxpress`->`cxpress`, `4:5`/`4X5`->`4x5`, `Anuncio`/`Anúncio`->`anuncio`.
Se apos normalizar o valor nao estiver na lista permitida, trate como ausente e pergunte.

## Fast-path

Se `$ARGUMENTS` ja tem marca + slug (e idealmente tipo/uso/formato validos), pule pro Disparo,
assumindo defaults pros que faltarem (`regiao=brasil`, `tipo=carrossel`, `uso=organico`, `formato=4x5`).

Marcas: `buzzmonitor` `buzzcreators` `cxpress` `elife`
Regioes: `brasil` `portugal` `latam`
Tipos: `carrossel` `estatico`
Uso: `organico` `anuncio`
Formatos: `1x1` `4x5` `9x16`

---

## Q1 — Marca
AskUserQuestion: "Qual marca?" header: "Marca" → Buzzmonitor | Buzzcreators | Cxpress | Elife → `marca`

## Q2 — Regiao
AskUserQuestion: "Qual regiao?" header: "Regiao" → Brasil (Recomendado) | Portugal | LATAM → `regiao`

## Q3 — Tipo de peca
AskUserQuestion: "Carrossel ou estatico?" header: "Tipo"
1. "Carrossel (5 cards)" → `tipo=carrossel`
2. "Estatico (1 imagem)" → `tipo=estatico`

## Q4 — Uso (define a margem de seguranca)
AskUserQuestion: "Vai ser organico ou anuncio?" header: "Uso"
1. "Organico (Recomendado)" — pode usar a borda inteira, mascote sangrando → `uso=organico`
2. "Anuncio (margem de seguranca Meta)" — puxa conteudo critico pra dentro + gera overlay-guia de QA → `uso=anuncio`

## Q5 — Formato
AskUserQuestion: "Qual formato?" header: "Formato" (multiSelect: true — pode pedir mais de um)
1. "Feed 4:5 (Recomendado)" → `4x5`
2. "Quadrado 1:1" → `1x1`
3. "Stories/Reels 9:16" → `9x16`
→ junte os escolhidos em CSV → `formato`

## Q6 — Slug
Texto livre: "Nome curto da peca em kebab-case (ex: case-10-para-4)." → `slug`

## Q7 — Copy
Texto livre: "Cole a copy (por card, se carrossel) ou o caminho/URL do arquivo. Se ja existe
copy.txt na pasta da peca, pode dizer 'usar existente'." → `copy`

Se o usuario nao tiver copy ainda, sugira gerar antes:
`/copy-criar {marca} {regiao} estatico {estagio} "{tema}"` e retomar depois.

---

## Disparo

Invoke Skill(criativo-gerar, args: "{marca} {regiao} {tipo} {uso} {formato} {slug}\n\nCOPY:\n{copy}")

(Os parametros vao na 1a linha; a copy vai apos o marcador `COPY:`. Se `copy` = "usar existente",
omita o bloco COPY — o worker le o copy.txt da pasta.)
