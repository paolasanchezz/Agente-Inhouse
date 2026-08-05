# Revisao LP — cxpress/video-atendimento-obrigado

**Data:** 2026-07-29
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel WIG)

## Checks que passaram limpos

- Em-dash: 0 no HTML e na copy
- Fidelidade da copy: eyebrow, H1, H2, body e CTA literais do `copy.txt`
- GTM: `GTM-T4XDWHL3` (brasil) presente nos 2 blocos
- Vídeo: embed `youtube-nocookie` 16:9 com `title`, `allowfullscreen` e `referrerpolicy`; carrega no load (sem gate extra)
- A11y: skip-link, `:focus-visible`, `prefers-reduced-motion`, reveal com fallback `<noscript>`
- Logos web-safe (§19) e href regional (§17) ok
- Exceções deliberadas documentadas no README (precedente `conheca-a-cxpress-confirmado`): `noindex, follow`, sem OG/JSON-LD/canonical, sem form (§6/§15)

## Aplicado automaticamente (1 critico)

- [x] Indicador do header duplicava o eyebrow "Vídeo liberado" (§3 "nunca duplicar") — removido; header ficou só com o logo

## Aplicado no deploy (1 crítico adicional)

- [x] **Reveal sem failsafe** (§4) — mesma correção da LP mãe: adicionado `setTimeout(revealAll, 1500)` como 3ª camada, garantindo que o texto apareça mesmo se o IntersectionObserver não disparar.

## PENDÊNCIA ABERTA (LP já está no ar)

- [x] **Resolvida (2026-08-03):** o CTA chegou a ir ao ar com `href="#"` porque o link `wa.me` não existia no repositório; a seção foi removida e, no mesmo dia, reposta com o link real que a Marielle informou (`wa.me/551150395028` + mensagem pré-preenchida) e o CTA "Agende uma demonstração gratuita". Sem pendência.

## Melhorias opcionais (3)

- [ ] `touch-action: manipulation` no `body`/CTA (WIG mobile)
- [ ] CSS morto: regras `.header__meta`/`.dot` ficaram órfãs após remover o indicador — limpar
- [ ] **Privacidade do embed (opcional):** o vídeo usa `www.youtube.com`, que o CSP já libera. Migrar para `youtube-nocookie.com` (sem cookie até o play) exige 1 linha no `frame-src` do `dominios/content-cxpress-io/vercel.json` + 1 no embed, no mesmo PR. É path protegido, então passa por revisão do Victor e não auto-mergeia.

## Nice-to-haves (1)

- [ ] Loading do iframe: trocar por facade (thumbnail + play que injeta o iframe) se o PageSpeed reclamar de third-party blocking — só se necessário

## Próximos passos

- Se o número do WhatsApp mudar, editar o `href` do `.cta-whatsapp` no `index.html` e a nota no `copy.txt`
- Publicar em batch com a mãe: `/lp-publicar cxpress "video-atendimento,video-atendimento-obrigado" content.cxpress.io`
