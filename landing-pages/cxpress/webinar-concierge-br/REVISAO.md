# Revisao LP — cxpress/webinar-concierge-br

**Data:** 2026-10-07
**Auditoria:** checagens deterministicas (GTM, SEO, em-dash, JSON-LD, overflow mobile) + revisao visual desktop 1280px e mobile 375px. A LP reaproveita o CSS da `webinar-whatsapp-ia-pt`, ja revisada e no ar.

## Aplicado automaticamente (3 criticos)

- [x] Header CTA estourava 375px (viewport de layout virava 474px) — `.hd__cta` quebra em 2 linhas e o logo reduz ≤480px. Overflow agora 0.
- [x] Stat "8h → 26min" vazava o card a 1280px (`white-space:nowrap` + 42px) — fonte `clamp(28px,2.6vw,34px)` sem nowrap.
- [x] "26 minutos" quebrava no meio do destaque (hero e OG) — `&nbsp;`.

## Checagens OK

- GTM `GTM-T4XDWHL3` (brasil) no head + noscript — `check_gtm_region.py` status `ok`, selo gravado.
- SEO: description 1 · robots 1 · og: 10 · twitter: 4 · canonical 1 · JSON-LD parseia (Organization, WebPage, VideoObject).
- Em-dash: 0 no HTML e 0 no copy.txt.
- Fidelidade da copy: todo texto visivel vem do copy.txt; fora dele so whitelist (labels/placeholders do form, skip-link, aria-labels, footer).
- Logo `logo-reversed.svg` sem `<text>` vivo (§19). Href da logo → `https://home.cxpress.io`, `target=_blank rel=noopener`.
- LP unica (sem irmas -pt/-es) → sem hreflang.

## Melhorias opcionais (3)

- [ ] Foto do Luiz Fantini no byline do hero (o deck tem a foto no slide 2) — reforca autoridade do apresentador.
- [ ] Brand manifest da Cxpress ainda no formato `websites` (sem bloco `regions`) — JSON-LD usa home.cxpress.io + Instagram cxpress.io por analogia com a LP de referencia.
- [ ] Pagina de obrigado `webinar-concierge-br-obrigado` (a referencia tem uma) para o redirect do formulario.

## Nice-to-haves (1)

- [ ] Grafico de barras da evolucao Pascoa 2024/2025/2026 (slide 9) na secao Resultado — exigiria copy nova (Pascoa 2025: 59%).

## Proximos passos

- Design aprovado? -> /lp-integrar-form cxpress/webinar-concierge-br "{snippet}"
- Publicar: /lp-publicar cxpress webinar-concierge-br content.cxpress.io
