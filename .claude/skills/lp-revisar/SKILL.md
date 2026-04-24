---
name: lp-revisar
description: Auditoria dupla de landing page (frontend-design em review mode + web-design-guidelines). Aplica achados criticos automaticamente, marca melhorias e nice-to-haves como opcionais em REVISAO.md.
argument-hint: "[marca]/[slug] — ex: buzzmonitor/monitoramento-maio"
allowed-tools: Read, Write, Edit, Glob, Grep, Skill, WebFetch
version: 1.1.0
---

# Skill: Revisar Landing Page

Voce audita uma LP em 2 passadas independentes (design + acessibilidade/HTML), aplica **apenas os achados criticos automaticamente**, e deixa tudo acima de critico marcado em `REVISAO.md` para o usuario decidir.

## Passo 0: Parsing e Contexto

Leia `.claude/skills/lp-preparar/CONTEXT.md`.

Parsing de `$ARGUMENTS`:
- Aceita `{marca}/{slug}` ou `{marca} {slug}` ou path completo `landing-pages/{marca}/{slug}/`.
- Normalize para `landing-pages/{marca}/{slug}/index.html`.

Se arquivo nao existe: PARE e avise.

## Passo 1: Passada 1 — Design Review

> **Nota sobre "review mode":** `frontend-design` e uma skill upstream da Anthropic voltada a GERAR UI. Ela nao tem modo de revisao nativo. O "review mode" aqui e uma **convencao de prompt deste projeto**: a primeira linha do argumento instrui explicitamente "NAO implemente — apenas liste achados", e a skill obedece ao texto do prompt. Se a chamada voltar com HTML gerado em vez de uma lista de achados, o prompt foi mal formatado — refaca com o bloco exato abaixo.

Invoque `frontend-design` com o prompt exato abaixo (primeira linha obrigatoria, nao remover):

```
REVIEW ONLY — NAO implemente nem reescreva codigo. Apenas liste achados em bullets.

Audite a landing page em `landing-pages/{marca}/{slug}/index.html`.

Contexto: LP da marca {marca}, brand em brand/{marca}/, guidelines vivas em landing-pages/GUIDELINES.md (10 secoes).

Reporte em bullets agrupados por severidade:
- CRITICO — quebra visivel, copy invisivel, hierarquia colapsada, contraste < AA, motion sem fallback, secao-tipo errada (ex: problema em grid, beneficios em lista)
- MELHORIA — ajuste que melhora mas nao quebra (espacamento, micro-ajuste tipografico, refinement de cor)
- NICE-TO-HAVE — estilistico, opiniao

Para cada achado: citar linha ou seletor CSS, dizer o que esta errado, sugerir a correcao (texto, nao codigo).
```

Se o output voltar contendo blocos de codigo HTML/CSS novos em vez de lista, descartar e reinvocar reforcando "REVIEW ONLY — apenas texto, zero codigo".

Salve o output inteiro em memoria (nao escrever em disco ainda).

## Passo 2: Passada 2 — Web Interface Guidelines

Invoque `web-design-guidelines`:

```
Audite landing-pages/{marca}/{slug}/index.html contra as Web Interface Guidelines da Vercel Labs.

Foco: acessibilidade, HTML semantico, estrutura, performance basica. Reporte achados em:
- CRITICO — violacoes WCAG AA, labels faltando, alt faltando, tab order quebrado, skip-link ausente, motion sem reduced-motion
- MELHORIA — melhoria de semantica ou a11y nao bloqueante
- NICE-TO-HAVE — polish
```

Salve o output em memoria.

## Passo 3: Consolidar Achados

Unifique as 2 listas. Deduplicate (se os dois auditores pegaram o mesmo problema, contar uma vez). Agrupe final em 3 buckets:

- CRITICOS (apply now)
- MELHORIAS (marcar em REVISAO.md, nao aplicar)
- NICE-TO-HAVES (marcar em REVISAO.md, nao aplicar)

## Passo 3.5: Auditoria de GTM (CRITICO)

### Resolver regiao (cascata)

Ver CONTEXT.md "Deteccao de regiao":

1. Sufixo do slug: `-pt` → portugal, `-latam`/`-es` → latam, `-br` → brasil.
2. `<html lang>` do index.html: `pt-PT` → portugal, `es-*` → latam, `pt-BR` → brasil.
3. Fallback: `brasil`.

### Resolver GTM esperado

Ler `brand/{marca}/tracking.json`:

```
expected_gtm_id = gtm.regions[{regiao}] || gtm.default || null
```

### Auditar HTML

Grep em `landing-pages/{marca}/{slug}/index.html` por `GTM-` (script no `<head>` e `<noscript>` apos `<body>`). Comparar com `expected_gtm_id`:

| Estado no HTML | expected_gtm_id | Severidade | Acao |
|---|---|---|---|
| Ausente | != null | CRITICO | Injetar script + noscript com ID correto |
| Presente, ID bate | != null | OK | Nenhuma |
| Presente, ID diferente | != null | CRITICO | Substituir ID nos 2 blocos |
| Presente (qualquer ID) | null | MELHORIA | Anotar em REVISAO.md — `tracking.json` da marca esta null mas LP tem GTM |
| Ausente | null | OK | Nenhuma |

### Snippet canonico para injetar (se ausente)

No `<head>`, apos `<meta name="viewport">` e antes de `<title>`:

```html
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->
```

Imediatamente apos `<body>`:

```html
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
```

Substituir `{GTM_ID}` pelo valor resolvido (ex: `GTM-NCFT22CW`). Para substituir ID errado, usar `Edit` com `replace_all` no ID antigo → novo (pega os 2 lugares numa operacao).

Registrar o achado com os demais criticos para aplicacao no Passo 4. Formato sugerido:

- `GTM ausente para {marca}/{regiao} (esperado {expected_gtm_id}) — injetar script em <head> e noscript apos <body>`
- `GTM com ID errado: encontrado {found_id}, esperado {expected_gtm_id} para {marca}/{regiao}`

## Passo 4: Aplicar Criticos

Para cada critico, use `Edit` em `landing-pages/{marca}/{slug}/index.html` com a correcao minima possivel. Nao refatorar — so fixar o critico.

Se um critico exige mudanca estrutural grande (ex: re-arquitetar secao-tipo), PARE antes de aplicar e pergunte ao usuario. Nao faca cirurgia grande silenciosamente.

## Passo 5: Gerar REVISAO.md

Caminho: `landing-pages/{marca}/{slug}/REVISAO.md`.

Formato:

```markdown
# Revisao LP — {marca}/{slug}

**Data:** YYYY-MM-DD
**Auditores:** frontend-design (review mode) + web-design-guidelines

## Aplicado automaticamente ({N} criticos)

- [x] {achado 1} — linha {X} — {correcao aplicada}
- [x] {achado 2} — seletor `.xyz` — {correcao}

## Melhorias opcionais ({N})

Para o usuario decidir. Aplicar via Edit manual ou pedir `/lp-revisar` novamente.

- [ ] {achado} — {onde} — {sugestao}

## Nice-to-haves ({N})

Estilistico. Ignorar e aceitavel.

- [ ] {achado}

## Proximos passos

- Design aprovado? -> /lp-integrar-form {marca}/{slug} "{snippet}"
- Rever mais algum critico? -> editar e rodar /lp-revisar novamente
```

## Passo 6: Relatorio Final

```
Revisao concluida — {marca}/{slug}

Criticos aplicados: {N}
Melhorias opcionais: {N} (em REVISAO.md)
Nice-to-haves: {N} (em REVISAO.md)

HTML atualizado: landing-pages/{marca}/{slug}/index.html
Relatorio: landing-pages/{marca}/{slug}/REVISAO.md

Proximo: aprovar design e rodar /lp-integrar-form {marca}/{slug} "snippet"
```
