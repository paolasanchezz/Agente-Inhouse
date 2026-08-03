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

- [x] **Resolvida por remoção (2026-08-03):** o CTA "Conversar pelo WhatsApp" chegou a ir ao ar com `href="#"` porque o link `wa.me` do especialista nunca existiu no repositório. A Marielle pediu para retirar o botão, e a seção DÚVIDAS saiu inteira. Não há mais pendência de link.

## Melhorias opcionais (3)

- [ ] `touch-action: manipulation` no `body`/CTA (WIG mobile)
- [ ] CSS morto: regras `.header__meta`/`.dot` ficaram órfãs após remover o indicador — limpar
- [ ] **Deploy/CSP:** garantir `https://www.youtube-nocookie.com` em `frame-src` no `vercel.json` do guarda-chuva `content.cxpress.io` (patch cirúrgico; sem isso o iframe fica vazio no live). Verificar no `/lp-publicar`

## Nice-to-haves (1)

- [ ] Loading do iframe: trocar por facade (thumbnail + play que injeta o iframe) se o PageSpeed reclamar de third-party blocking — só se necessário

## Próximos passos

- Se um CTA voltar a fazer sentido aqui (e-mail, agendamento, WhatsApp com número real), a seção pode ser recriada a partir do histórico do git
- Publicar em batch com a mãe: `/lp-publicar cxpress "video-atendimento,video-atendimento-obrigado" content.cxpress.io`
