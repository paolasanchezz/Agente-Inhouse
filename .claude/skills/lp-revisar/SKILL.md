---
name: lp-revisar
description: Auditoria dupla de landing page (frontend-design em review mode + web-design-guidelines). Aplica achados criticos automaticamente, marca melhorias e nice-to-haves como opcionais em REVISAO.md.
argument-hint: "[marca]/[slug] — ex: buzzmonitor/monitoramento-maio"
allowed-tools: Read, Write, Edit, Glob, Grep, Skill, WebFetch
version: 1.0.0
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

Invoque `frontend-design` em **review mode**:

```
review mode: audite a landing page em `landing-pages/{marca}/{slug}/index.html`.
NAO implemente mudancas — apenas liste achados.

Contexto: LP da marca {marca}, brand em brand/{marca}/, guidelines vivas em landing-pages/GUIDELINES.md (10 secoes).

Reporte em bullets agrupados por severidade:
- CRITICO — quebra visivel, copy invisivel, hierarquia colapsada, contraste < AA, motion sem fallback, secao-tipo errada (ex: problema em grid, beneficios em lista)
- MELHORIA — ajuste que melhora mas nao quebra (espacamento, micro-ajuste tipografico, refinement de cor)
- NICE-TO-HAVE — estilistico, opiniao

Para cada achado: citar linha ou seletor CSS, dizer o que esta errado, sugerir a correcao.
```

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
