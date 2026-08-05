# Revisao LP — buzzmonitor/primeiro-listening-5-passos

**Data:** 2026-07-09
**Auditores:** frontend-design (review mode) + web-design-guidelines + verificação visual (Chrome headless 1440) — herda o template já auditado da case-youse (fixes de stagger e CTA final incorporados desde a geração)

## Aplicado automaticamente (1 critico)

- [x] OG-IMAGE-MISSING — gerada `assets/og-primeiro-listening-5-passos.png` (1200×630, 117 KB) via template brand + Chrome headless. No deploy vira `/assets/buzzmonitor/og-primeiro-listening-5-passos.png`.

## Verificado sem achados

- GTM: GTM-WFJVK858 nos 2 blocos
- Fidelidade da copy: literal de `copy.txt`; em-dash = 0 (3 da copy bruta corrigidos no lp-preparar); grafias oficiais Theme Monitoring / Sentiment Classification / Auto Tag Suggestions / Buzz Pills
- SEO §15: description 1, og 10, twitter 4, canonical 1, JSON-LD parseia
- hreflang: LP única — pt-BR + x-default, ok
- A11y: skip-link, focus-visible, labels, alt/aria-hidden, reduced-motion, noscript fallback
- CTA final: meta empilha acima do botão (fix da case-youse já incorporado)

## Melhorias opcionais (mesmas da case-youse)

- [ ] `cm-feedback` (role=status) no form pra integração drop-in
- [ ] `spellcheck="false"` no input de e-mail
- [ ] `touch-action: manipulation`
- [ ] `.header-cta` some em ≤520px (herdado da referência)

## Nice-to-haves

- [ ] `<meta name="theme-color" content="#390155">`
- [ ] `text-wrap: balance` nos headings

## Proximos passos

- Publicar: /lp-publicar buzzmonitor primeiro-listening-5-passos webinar.buzzmonitor.com
- Form real: fluxo ClickMeeting (série + mapping + JS da referência)
