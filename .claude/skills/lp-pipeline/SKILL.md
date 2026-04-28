---
name: lp-pipeline
description: Executa o pipeline de landing page — preparar copy, gerar HTML, revisar e (apos aprovacao manual) publicar. Pausa explicita antes de integrar form e antes de publicar.
argument-hint: "[marca] [slug] [fonte] [dominio-opcional] — ex: buzzcreators evento-creators https://notion.so/... evento.buzzmonitor.com"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, Skill, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-fetch, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-pages, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-update-page
version: 1.1.0
---

# Skill: Pipeline de Landing Page

Executa em sequencia: `/lp-preparar` → `/lp-gerar` → `/lp-revisar` → (pausa para form + aprovacao) → `/lp-publicar`.

## Contexto comum

Antes de validar argumentos, leia:

1. `landing-pages/GUIDELINES.md` — regras de design.
2. `landing-pages/CONTEXT.md` — runbook operacional (fluxos, assets, troubleshooting). Cada etapa abaixo recarrega esses arquivos por conta propria; voce os mantem em mente para responder perguntas do usuario nos checkpoints.

Se o usuario invocou `/lp-pipeline` para **alterar** uma LP existente (nao criar do zero), pare e oriente: este pipeline e para LP nova. Para alteracao, consultar `landing-pages/CONTEXT.md` §2.2 (matriz "o que mudou → o que rodar") — geralmente edit do source + `/lp-gerar` (se copy mudou) + `/lp-publicar`.

## Validacao de Argumentos

`$ARGUMENTS` deve ter ao menos: `[marca] [slug] [fonte]`. O quarto argumento `[dominio]` e opcional.

Se algum obrigatorio faltar, PARE:

```
Uso: /lp-pipeline [marca] [slug] [fonte] [dominio-opcional]
Exemplo: /lp-pipeline buzzmonitor monitoramento-maio https://notion.so/Copy-LP... webinar.buzzmonitor.com
```

## Etapa 1: Preparar Copy

Execute o fluxo completo da skill `/lp-preparar` com `[marca] [slug] [fonte]`.

Consulte `.claude/skills/lp-preparar/SKILL.md` e execute todos os passos na integra. Output: `landing-pages/{marca}/{slug}/copy.txt` + pagina Notion com copy estruturada.

## Checkpoint 1 — Revisao de copy

Apos a Etapa 1, informe ao usuario:

```
Copy estruturada publicada no Notion: {URL}

Revise a copy no Notion. Quando aprovada (ou com edicoes aplicadas em copy.txt), continue o pipeline.

Continuo agora? (sim/nao)
```

Se `nao`, PARE. O usuario pode retomar com `/lp-gerar {marca} {slug}` depois.
Se `sim`, seguir.

## Etapa 2: Gerar HTML

Execute `/lp-gerar [marca] [slug]`. Consulte `.claude/skills/lp-gerar/SKILL.md`.

## Etapa 3: Revisar

Execute `/lp-revisar [marca]/[slug]`. Consulte `.claude/skills/lp-revisar/SKILL.md`.

## Checkpoint 2 — Aprovacao de design e integracao de form

Apos Etapa 3, informe ao usuario:

```
Design revisado. Criticos aplicados. Melhorias opcionais em REVISAO.md.

Proximo passo e integrar formulario real. Isso NAO roda automaticamente (GUIDELINES §10).

Quando tiver o snippet do embed (Jotform/RD/HubSpot), rode:
  /lp-integrar-form {marca}/{slug} "<snippet>"

Depois retorne e me diga para publicar: /lp-publicar {marca} {slug} [dominio]

Ou, se quer publicar SEM form real ainda (com mock), responda "publicar agora".
```

PARE aqui por padrao. So siga para Etapa 4 se o usuario responder "publicar agora" ou se `--auto` foi passado.

## Etapa 4: Publicar

Execute `/lp-publicar [marca] [slug] [dominio-opcional]`. Consulte `.claude/skills/lp-publicar/SKILL.md`.

## Output Final

```
Pipeline concluido — {marca}/{slug}

- Copy: {URL Notion da copy}
- HTML: landing-pages/{marca}/{slug}/index.html
- Revisao: {N} criticos aplicados, {M} opcionais em REVISAO.md
- Publicado: {URL}
- Relatorio: {URL Notion do relatorio final}
```
