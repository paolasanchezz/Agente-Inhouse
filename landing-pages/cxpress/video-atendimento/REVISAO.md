# Revisao LP — cxpress/video-atendimento

**Data:** 2026-07-29
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel WIG)

## Checks que passaram limpos

- Em-dash: 0 no HTML e na copy (tolerância zero ok)
- Fidelidade da copy: todos os textos visíveis são literais do `copy.txt` (H1, SUB, labels, CTA, footer); nenhum pull-quote/kicker/punchline inventado
- GTM: `GTM-T4XDWHL3` (brasil) presente no `<head>` + `<noscript>` — bate com `tracking.json`
- SEO §15: description 1, robots 1, canonical 1, og ≥8 (10), twitter 4, JSON-LD parseia
- Logos: SVGs Cxpress são outline (sem `<text>` vivo, §19); header/footer apontam pra `home.cxpress.io` com `target=_blank rel=noopener` (§17)
- A11y: skip-link, `:focus-visible`, labels em todos os inputs, `autocomplete`/`inputmode`, `prefers-reduced-motion`, reveal com fallback `<noscript>` + IO-check
- hreflang: LP única (sem irmãs -es/-pt) — omissão correta (§16)

## Aplicado automaticamente (2 criticos)

- [x] OG image ausente (§18) — gerada `assets/og-video-atendimento.png` 1200×630 (56 KB) via template `assets/og-template.html` + Chrome headless; `og:image`/`twitter:image` já apontavam pro placeholder correto
- [x] Indicador do header duplicava o eyebrow do hero ("Vídeo exclusivo", §3 "nunca duplicar") — trocado por "Acesso imediato" (nav meta minimal, whitelist)

## Aplicado no deploy (1 crítico adicional)

- [x] **Reveal sem failsafe** (§4: "nunca deixar texto essencial invisível esperando animação") — o reveal dependia só do IntersectionObserver. Em aba aberta em background (Cmd+click de anúncio/e-mail), o IO não dispara enquanto a aba não é composta e a classe `is-visible` nunca era aplicada (confirmado no ar: 0 de 5 elementos). Adicionado `setTimeout(revealAll, 1500)` como 3ª camada de fallback, junto do `<noscript>` e do check de suporte a IO. Validado no ar: 5 de 5 aplicados.

## Integração do form (2026-07-29)

Jotform `262104279010647` (`jsform`, renderiza iframe de `form.jotform.com`). Achados tratados na integração:

- [x] **Cabeçalho duplicado** — o Jotform imprime `<h2>ASSISTA AGORA</h2>` dentro do iframe, que repetia o rótulo "Assista agora" do card. Removido o rótulo da LP (e o CSS dele).
- [x] **Card dentro de card** — o embed traz card próprio; o padding do `.form-card` foi reduzido via `:has(.jotform-embed)` para não empilhar dois cards (incidente 2026-04-30).
- [x] **CSS morto** — removidas as regras `.form input/label/.field/.cta` do mock (não havia mais `<form>` na página).
- [x] **Handler JS do mock removido** — sem ele, `querySelector('.form')` retornaria `null` e quebraria o console.
- [x] **CSP já cobria** — o `jsform` monta iframe de `form.jotform.com`, coberto por `*.jotform.com` em `script-src` + `frame-src`. Estilos ficam dentro do iframe (origem própria), então `style-src` não precisou de ajuste.
- [x] **Campos conferem** com a copy aprovada: Nome, Empresa, E-mail corporativo, Cargo, WhatsApp (+ campos ocultos de URL/UTM do Jotform).
- [x] **Mobile sem overflow horizontal** — validado a 375px (`scrollWidth` = viewport); H1 antes do card no mobile (§3).

## Melhorias opcionais (4)

- [ ] `touch-action: manipulation` no `body`/botões — evita delay de double-tap no mobile (WIG)
- [ ] `text-wrap: balance` no H1 — quebras de linha mais equilibradas
- [ ] CSS morto: regra `.form input::placeholder` sem nenhum `placeholder` no HTML — remover ou adicionar placeholders com exemplo (`placeholder="nome@empresa.com.br…"`)
- [ ] `brand/cxpress/brand-manifest.json` está no formato antigo (`websites`, sem bloco `regions`) — JSON-LD saiu sem `sameAs` (Instagram/LinkedIn), igual à LP de referência. Migrar o manifest resolve pra todas as LPs futuras

## Nice-to-haves (2)

- [ ] `<strong>` em "imediatamente" no SUB é ênfase editorial adicionada pela diagramação — remover se preferirem o texto plano
- [ ] Decisão de copy já sinalizada no copy.txt/Notion: H1 abre pela solução, não pela dor (§3/§5). As 3 opções do briefing são deliberadamente amplas; manter é válido

## Próximos passos

- Design aprovado? → `/lp-integrar-form cxpress/video-atendimento "snippet"` (configurar redirect do provedor para `/video-atendimento-obrigado`)
- Publicar sempre em batch com a irmã: `/lp-publicar cxpress "video-atendimento,video-atendimento-obrigado" content.cxpress.io`
