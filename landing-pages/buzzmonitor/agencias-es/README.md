# LP Buzzmonitor — agencias-es (ex-plataforma-integral-agencias, renomeada 2026-08-12 a pedido do Victor)

**Gerado em:** 2026-08-12
**Copy-fonte:** `copy.txt` (réplica literal de https://contenido.getbuzzmonitor.com/agencias, estruturada via /lp-preparar)
**Design base:** `landing-pages/buzzmonitor/plataforma-integral-social-media` (mesmo design system: paleta orange/pink/ink, Inter, gradient-text, reveal, quote-cards, logo marquee)
**Região/idioma:** LATAM · es-419 (slug com sufixo `-es` resolve latam na cascata; confirmado pelo gate de CI)
**GTM:** GTM-MKQBX2MG (latam, tracking.json) + Meta Pixel 935436740448328 (mesmo par da LP design base, mesmo domínio)

## Estrutura (v2 enxuta, 2026-08-12)

8 secoes. Racional do corte em `REVISAO.md` e no cabecalho do `copy.txt`.

1. HERO (overline dor + H1 + CTA + **video** `social-listening-es.mp4`)
2. Prova social imediata (logos de agencias)
3. Diferencial ("Lo que las mejores agencias hacen diferente.")
4. Soluciones (3 splits com print: Monitoreo · Atencion Centralizada · Dashboards, 4 bullets cada) + CTA
5. Modulos restantes (grade de 3: Metricas · Programacion · Gestion de Crisis)
6. IA (print ai-insights + 6 cards com nomes oficiais)
7. Depoimentos (6 agencias) + Numeros e parede de logos
8. CTA final: oferta de 14 dias + **form Jotform**
9. Footer

## Estado

- [x] HTML gerado
- [x] OG image 1200×630 → `assets/og-agencias-es.png`
- [x] Validações: em-dash 0 · SEO completo (1 desc, 10 og, 4 twitter, JSON-LD parseia) · GTM gate OK (latam/MKQBX2MG)
- [x] Revisão (frontend-design review + web-design-guidelines) — 8 críticos aplicados, ver `REVISAO.md`
- [x] Formulário integrado — Jotform `241825239057661` (mesmo form da LP plataforma-integral-social-media; 2026-08-12)
- [x] Publicado em https://content.buzzmonitor.com/agencias-es (guarda-chuva CI)

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header/footer; raster base64, web-safe §19)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `./assets/social-listening-es.mp4` + `social-listening-es-poster.jpg` (hero — origem: ia-para-social-listening-es)
- `./assets/ai-insights.png`, `crises-1.png`, `crises-2.jpg`, `img-relatorios-dashboard.png` (prints — origem: ia-para-social-listening-es)
- `./assets/logos-agencias/*` e `./assets/logos-clientes/*` (origem: plataforma-integral-social-media)
- `./assets/og-agencias-es.png`

## Notas

- Sugestões de idioma/anti-IA pendentes de decisão do Victor no fim do `copy.txt` (destaque: "Monitorización" é grafia de Espanha; LATAM seria "Monitoreo" — mantido literal da LP original).
- hreflang: LP única (sem irmãs BR/PT no repo) — só canonical + x-default.
