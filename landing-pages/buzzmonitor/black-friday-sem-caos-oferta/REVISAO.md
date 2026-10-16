# Revisão LP — buzzmonitor/black-friday-sem-caos-oferta

**Data:** 2026-10-16
**Auditores:** design review + web interface guidelines + checks determinísticos (GTM, SEO, fidelidade de copy, em-dash, logo, OG)

## Aplicado automaticamente (0 críticos)

Nenhum crítico. A LP herda o HTML/CSS do template `reports-monitoramento-ia-agencias-oferta`, que já tinha os 4 fixes de contraste AA aplicados na revisão de `gestao-de-crises-ia-agosto-2026-oferta`.

Ajuste menor aplicado: H1 do hero quebrava deixando "meses." sozinho na 3ª linha (desktop). `2 primeiros meses.` agora fica junto (`white-space:nowrap`). Copy inalterada.

## Checks determinísticos — todos OK

- GTM: `GTM-WFJVK858` bate com a região brasil (status `ok`, `.tracking.lock` gravado).
- Em-dash: 0.
- Fidelidade de copy: 100% literal ao `copy.txt`. Fora da copy só whitelist (skip-link, aria-labels, form Jotform).
- SEO: description (1), robots (1), og: (10), twitter: (4), JSON-LD (1, parseia: Organization/WebPage/Service; `Organization.url` = manifest), canonical (1).
- Logo: href `https://buzzmonitor.com/` com `target="_blank" rel="noopener"`; SVGs sem `<text>` vivo.
- Sem LPs irmãs `-es`/`-pt`: hreflang omitido corretamente.
- OG: `assets/og-black-friday-sem-caos-oferta.png` 1200×630, sem `og-image.png` órfão. Fonte em `assets/og-source.html`.
- Ícones Tabler novos (`ti-discount`, `ti-bell-ringing`, `ti-filter`, `ti-layout-dashboard`) resolvem para glifo.
- Mobile 375px: sem scroll horizontal.
- Form: Jotform `253573505200650` (o mesmo das outras ofertas).

## Melhorias opcionais (1)

- [ ] O form é compartilhado com as outras ofertas: se o comercial precisar saber que o lead veio com a condição de 50% off, vale um campo oculto/etiqueta no Jotform.

## Nice-to-haves (0)
