# Revisao LP — buzzmonitor/case-youse

**Data:** 2026-07-09
**Auditores:** frontend-design (review mode) + web-design-guidelines + verificação visual (Chrome headless desktop 1440 / mobile 500)

## Aplicado automaticamente (2 criticos)

- [x] OG-IMAGE-MISSING — `og:image` referenciava arquivo inexistente — gerada `assets/og-image.png` (1200×630, 119 KB) via template brand + Chrome headless. No deploy guarda-chuva vira `/assets/buzzmonitor/og-case-youse.png` (lp-publicar renomeia).
- [x] CTA-FINAL-LAYOUT — `.cta-final-meta` era `inline-flex` e a linha "Online · Gratuito · Case real" caía na MESMA linha do botão (container 680px comportava os dois) — trocado por `flex`; meta agora empilha acima do botão. Obs.: a referência `mcp-na-pratica-p` tem o mesmo padrão latente (container 640px), vale conferir lá também.

## Verificado sem achados

- GTM: GTM-WFJVK858 (brasil) presente nos 2 blocos (`<head>` + noscript)
- Fidelidade da copy: textos literais de `copy.txt`; em-dash = 0; sem pull-quote/kicker/punchline inventado
- SEO §15: description 1, og 10, twitter 4, canonical 1, JSON-LD parseia (Organization + WebPage)
- hreflang: LP única (sem irmãs) — pt-BR + x-default próprios, ok
- Logos: SVGs Buzzmonitor raster (sem `<text>` vivo), href pra home regional com target=_blank
- A11y: skip-link, focus-visible, labels, alt/aria-hidden, prefers-reduced-motion, noscript fallback pros reveals/staggers

## Melhorias opcionais (4)

Para o usuario decidir. Aplicar via Edit manual ou pedir `/lp-revisar` novamente.

- [ ] Form mock sem `<p class="cm-feedback" role="status" aria-live="polite">` — adicionar já deixa a integração ClickMeeting drop-in (a referência mcp-na-pratica-p tem)
- [ ] Input de e-mail sem `spellcheck="false"` (Web Interface Guidelines)
- [ ] CSS sem `touch-action: manipulation` global em botões/links (remove delay de tap em alguns mobiles)
- [ ] `.header-cta` some em ≤520px (herdado da referência) — no mobile o caminho pro form é o scroll natural + CTA final

## Nice-to-haves (3)

Estilistico. Ignorar e aceitavel.

- [ ] `<meta name="theme-color" content="#390155">` pra combinar a UI do browser mobile com a marca
- [ ] `text-wrap: balance` nos headings longos (H1/section-h2)
- [ ] Footer dark logo após CTA final dark forma bloco escuro longo — hairline já separa; clarear footer é opcional

## Proximos passos

- Design aprovado? -> /lp-integrar-form buzzmonitor/case-youse "{snippet}" (aqui: fluxo ClickMeeting — criar série + mapear chave `case-youse` nas serverless functions + JS da referência)
- Publicar: /lp-publicar buzzmonitor case-youse webinar.buzzmonitor.com
