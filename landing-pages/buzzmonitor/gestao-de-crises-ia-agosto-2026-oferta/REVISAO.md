# Revisão LP — buzzmonitor/gestao-de-crises-ia-agosto-2026-oferta

**Data:** 2026-08-05
**Auditores:** frontend-design (review mode) + checks determinísticos (GTM, SEO, fidelidade de copy, contraste AA)

## Aplicado automaticamente (4 críticos)

- [x] Contraste AA — `.section-eyebrow` (laranja `#EB7C2E` sobre branco, ~2.8:1) — trocado para `var(--primary)` (roxo escuro), ~17:1. Afeta eyebrows de Benefícios, Módulos e Clientes.
- [x] Contraste AA — override `.clientes .section-eyebrow` também usava laranja sobre branco — mesma troca para `var(--primary)`.
- [x] Contraste AA — `.hero-h1-accent` (laranja sobre branco no H1, texto grande, ~2.8:1, abaixo do mínimo 3:1 pra large text) — trocado para `var(--secondary-dk)` (~3.7:1).
- [x] Contraste AA — `.header-offer strong` (mesmo laranja sobre branco) — trocado para `var(--primary)`.

## Checks determinísticos — todos OK

- GTM: container `GTM-WFJVK858` bate com a região (brasil) — status `ok`, stamp gravado.
- Em-dash: 0 ocorrências (tolerância zero).
- Fidelidade de copy: 100% literal ao `copy.txt` — nenhum pull-quote, kicker ou disclaimer inventado. Único texto fora da copy são labels de formulário (Nome/Email/Empresa), skip-link e aria-labels funcionais (whitelist).
- SEO: description (1), robots (1), og: (10), twitter: (4), JSON-LD (1, parseia, `Organization.url` bate com o brand-manifest), canonical (1).
- Logo: href aponta pra `https://buzzmonitor.com/` (não `/`), `target="_blank" rel="noopener"` em header e footer. SVGs de logo sem `<text>` vivo (web-safe).
- Sem LPs irmãs (sem sufixo `-es`/`-pt`) — hreflang corretamente omitido.
- Acessibilidade: skip-link, focus-visible, labels em todos os inputs, alt em todas as imagens semânticas, prefers-reduced-motion com fallback noscript.

## Melhorias opcionais (1)

- [ ] `.benefit-icon`/`.modulo-icon` usam ícones temáticos (radar, filtro, sino) em vez do check verde padrão de §8 — está dentro da regra (permite "marcador da cor primária da marca" como alternativa ao ✓ verde), mas se quiser uniformizar com outras LPs de benefício, pode padronizar pra `ti-circle-check`.

## Nice-to-haves (1)

- [ ] Ícone `ti-mood-sad` no item de "virada de sentimento" é funcional mas genérico — `ti-mood-off` ou `ti-activity` comunicariam "monitoramento" com mais precisão.

## Pendências fora desta revisão

- OG image (1200×630) ainda não gerada — necessária antes de publicar.
- Formulário ainda em mock — integrar via `/lp-integrar-form` antes de publicar.

## Próximos passos

- Design aprovado? → `/lp-integrar-form buzzmonitor/gestao-de-crises-ia-agosto-2026-oferta "<snippet>"`
- Rever mais algum crítico? → editar e rodar `/lp-revisar` novamente
