---
name: escrever
description: Guia interativo de copywriting. Faz perguntas com chips clicáveis e dispara a skill correta do pipeline copy-*. Usar quando o usuário digitar /escrever sem saber qual comando rodar.
argument-hint: "(opcional) Ex: /escrever | /escrever criar buzzmonitor brasil video-curto tofu 'briefing aqui' | /escrever revisar copy.md buzzmonitor"
allowed-tools: AskUserQuestion, Read, Glob
---

# /escrever — Router determinístico

Script fixo. Uma pergunta por vez. Pule se `$ARGUMENTS` já responde. Dispare direto após última pergunta — sem pedir confirmação.

## Normalização de inputs

Antes de validar qualquer argumento, **converta para lowercase** os identificadores (`marca`, `regiao`, `pais`, `tipo`, `estagio`). Ex: `Buzzmonitor` → `buzzmonitor`; `Vídeo-Curto` → `video-curto`. Se após a normalização o valor ainda não estiver na lista permitida, trate como ausente e faça a pergunta via AskUserQuestion.

## Fast-path

Se `$ARGUMENTS` contém tarefa + parâmetros válidos (já normalizados), pule para Disparo.

| Atalho | Disparo |
|---|---|
| `criar {marca} {regiao} {tipo} {estagio} "{briefing}"` | `/copy-criar {marca} {regiao} {tipo} {estagio} "{briefing}"` |
| `revisar {arquivo-ou-texto} {marca}` | `/copy-revisar {arquivo-ou-texto} {marca}` |
| `pesquisar {marca} {pais} {tipo}` | `/copy-pesquisar {marca} {pais} {tipo}` |
| `swipefile add {conteudo}` | `/copy-swipefile add {conteudo}` |
| `swipefile buscar {tema}` | `/copy-swipefile buscar {tema}` |

Marcas: `buzzmonitor` `buzzcreators` `cxpress` `elife`
Regiões/Países: `brasil` `portugal` `latam`
Tipos: `video-curto` `estatico` `email` `geral`
Estágios: `tofu` `mofu` `bofu`

---

## Q1 — Tarefa

AskUserQuestion — question: "O que quer fazer com copy?" header: "Tarefa" multiSelect: false

1. "Criar copy nova (Recomendado)" → fluxo=criar
2. "Revisar copy existente" → fluxo=revisar
3. "Pesquisar referências" → fluxo=pesquisar
4. "Swipe file (banco de referências)" → fluxo=swipefile

---

## Fluxo: Criar copy nova

Q: Marca — AskUserQuestion: "Qual marca?" header: "Marca" → Buzzmonitor | Buzzcreators | Cxpress | Elife → `marca` (lowercase)
Q: Região — AskUserQuestion: "Qual região?" header: "Região" → Brasil (Recomendado) | Portugal | LATAM → `regiao` (lowercase)
Q: Tipo — AskUserQuestion: "Qual tipo de copy?" header: "Tipo" → Vídeo curto | Estático | Email | Geral → `tipo` (kebab-case)
Q: Funil — AskUserQuestion: "Qual estágio do funil?" header: "Funil" → ToFu (Recomendado) | MoFu | BoFu → `estagio` (lowercase)
Q: Briefing — texto livre: "Descreva o briefing em uma frase." → `briefing`

→ Invoke Skill(copy-criar, args: "{marca} {regiao} {tipo} {estagio} \"{briefing}\"")

## Fluxo: Revisar copy

Q: Copy — texto livre: "Cole a copy ou informe o caminho do arquivo." → `arquivo_ou_texto`
Q: Marca — AskUserQuestion (igual acima) → `marca`

→ Invoke Skill(copy-revisar, args: "{arquivo_ou_texto} {marca}")

## Fluxo: Pesquisar referências

Q: Marca — AskUserQuestion (igual acima) → `marca`
Q: País — AskUserQuestion: "Qual país de referência?" header: "País" → Brasil | Portugal | LATAM → `pais` (lowercase)
Q: Tipo — AskUserQuestion (igual acima) → `tipo`

→ Invoke Skill(copy-pesquisar, args: "{marca} {pais} {tipo}")

## Fluxo: Swipe file

Q: Ação — AskUserQuestion: "O que fazer no swipe file?" header: "Ação" → Adicionar exemplo | Buscar exemplo → `acao`
Q: Conteúdo — texto livre conforme ação:
  - Adicionar: "Cole a URL ou texto da copy a salvar."
  - Buscar: "Qual tema buscar? (ex: 'remarketing', 'video curto BoFu')"

→ Se adicionar: Invoke Skill(copy-swipefile, args: "add {conteudo}")
→ Se buscar: Invoke Skill(copy-swipefile, args: "buscar {conteudo}")
