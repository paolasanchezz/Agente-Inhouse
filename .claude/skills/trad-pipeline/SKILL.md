---
name: trad-pipeline
description: Executa o pipeline completo de tradução — traduz a copy e revisa como nativo, publicando o resultado no Notion (pasta Entregas).
argument-hint: "[arquivo] [pt-pt|es-latam]  — ex: meu-texto.md pt-pt"
allowed-tools: Read, Write, Edit, WebSearch, WebFetch, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-fetch, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-pages
---

# Skill: Pipeline de Tradução

Executa em sequência: `/trad-traduzir` → `/trad-revisar`.

## Validação de Argumentos

`$ARGUMENTS` deve ter dois valores: `[arquivo] [target]`

**Se o arquivo não for fornecido**, pare e informe:
> "Nenhuma copy fornecida. Uso:\n  /trad-pipeline meu-texto.md pt-pt\n  /trad-pipeline meu-texto.md es-latam"

**Se o target não for `pt-pt` nem `es-latam`**, pare e informe o uso correto.

## Etapa 1: Tradução

Execute o fluxo completo da skill `/trad-traduzir` com os mesmos argumentos recebidos.

Consulte `.claude/skills/trad-traduzir/SKILL.md` e execute todos os passos na íntegra.

Ao final desta etapa, o arquivo de tradução estará em `traducao/entregas/YYYY-MM/[nome]-[target].md`.

## Etapa 2: Revisão e Publicação

Execute o fluxo completo da skill `/trad-revisar` passando o arquivo gerado na Etapa 1 e o mesmo target.

Consulte `.claude/skills/trad-revisar/SKILL.md` e execute todos os passos na íntegra, incluindo a publicação no Notion.

## Output para o Usuário

Ao finalizar, informe:
- Arquivo traduzido e revisado (caminho)
- Status da revisão (APROVADO / REQUER ATENÇÃO)
- URL da página criada no Notion
