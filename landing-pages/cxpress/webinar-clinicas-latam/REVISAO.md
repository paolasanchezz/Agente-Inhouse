# Revisão LP — cxpress/webinar-clinicas-latam

**Data:** 2026-08-11
**Auditores:** frontend-design (review mode) + web-design-guidelines + check_gtm_region.py

## Aplicado automaticamente (4 críticos)

Todos os 4 críticos eram do mesmo padrão: texto branco sobre fundo `accent` (laranja `#EF863C`) — contraste real ≈2.6:1, abaixo do mínimo AA de 4.5:1 para texto normal (exatamente o padrão de risco descrito em GUIDELINES §7 — "atenção especial ao eyebrow/badge que herda a cor de destaque e só troca o fundo"). Causa raiz: usei `accent` como cor do CTA primário, mas `brand/cxpress/generation-rules.json` define o **primaryDark** como cor do CTA padrão e o `accent` como CTA **secundário** — inverti isso na geração.

- [x] `.btn-primary` (CTA principal, aparece 5x na LP) — linha 278 — trocado `background: var(--accent)` → `background: var(--primary-dark)`. Contraste 2.6:1 → 13.5:1. Também alinha com `generation-rules.json` (ctaButton: primaryDark).
- [x] `.btn-primary:hover` — linha 283 — trocado `background: var(--accent-hover)` → `background: var(--primary-darker)` (evita reintroduzir o mesmo problema no hover, mantém a família de cor coesa).
- [x] `.header-cta:hover` — linha 230 — mesmo fix, `var(--accent)` → `var(--primary-darker)`.
- [x] `.speaker-badge` (badge "Speaker" nos 2 speaker cards) — linha 515 — trocado `color: var(--neutral-0)` → `color: var(--primary-dark)`. Contraste 2.6:1 → 5.2:1.
- [x] `.audience-header .section-label` (chip "Para quién es" na seção escura) — linha 453 — trocado `color: var(--neutral-0)` → `color: var(--primary-dark)`. Contraste 2.6:1 → 5.2:1.

## GTM (determinístico)

- [x] `check_gtm_region.py` — status `ok`, container `GTM-WRQ47B9R` bate com a região LATAM. Stamp gravado (`--write-stamp`).

## Fidelidade de copy

- [x] Sem vazamentos — todo texto visível bate com `copy.txt` ou está na whitelist (form labels, footer, skip-link, alt de imagem factual). Zero em-dash.

## SEO

- [x] `meta description` (1), `og:` (10), `twitter:` (4), JSON-LD (1, parseia), `canonical` (1) — todos presentes.
- [x] Logos SVG do header/footer sem `<text>` vivo (não serifam).

## Melhorias opcionais (3)

Para o usuário decidir — não bloqueiam publicação.

- [ ] `Organization.sameAs` ausente no JSON-LD (sem Instagram/LinkedIn) — causa: `brand/cxpress/brand-manifest.json` ainda está no formato antigo (`websites`, sem bloco `regions`). Ficaria resolvido migrando o manifest da marca (fora do escopo desta LP).
- [ ] `.social-proof-stat` (texto "+800 clientes...") usa `accent-hover` sobre fundo branco — contraste ≈3.1:1, no limite do AA para texto grande em negrito (passa por pouco nos tamanhos maiores do `clamp`, arrisca no menor). Se quiser 100% de margem, trocar a cor para `var(--primary-dark)`.
- [ ] Não há uma seção de "CTA final" full-width antes do footer (GUIDELINES §6) — a última seção (prova social) termina só com o stat, sem botão. A copy original também não tinha CTA ali, então não inventei um — mas repetir o CTA "¡Quiero inscribirme!" mais uma vez ali é uma opção de conversão, se quiser.

## Nice-to-haves (2)

Estilístico. Ignorar é aceitável.

- [ ] `.hero-content { order: -0; }` (linha 349) — `-0` é equivalente a `0`, sobra de código sem efeito. Pode remover a linha sem mudar nada visualmente.
- [ ] Speaker cards são verticais/centralizados (foto no topo, nome e cargo abaixo, centralizado) em vez do padrão "horizontal" descrito em GUIDELINES §8 ("foto circular à esquerda, nome+cargo à direita"). Optei por manter vertical porque é exatamente o padrão já usado em `latam-webinar-atencionalcliente` (LP irmã, mesmos 2 speakers) — consistência com a família > aderência literal ao §8. Vale considerar atualizar o §8 do GUIDELINES para refletir esse padrão real, já usado em várias LPs Cxpress.

## Próximos passos

- Design aprovado? → gerar OG image (`assets/og-webinar-clinicas-latam.png`, 1200×630) — ainda pendente, bloqueia publicação.
- Formulário real → `/lp-integrar-form cxpress/webinar-clinicas-latam "snippet"` quando houver provedor definido.
- Publicar → `/lp-publicar cxpress webinar-clinicas-latam content.cxpress.io`
