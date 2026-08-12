# LP Buzzmonitor — plataforma-integral-agencias

**Gerado em:** 2026-08-12
**Copy-fonte:** `copy.txt` (réplica literal de https://contenido.getbuzzmonitor.com/agencias, estruturada via /lp-preparar)
**Design base:** `landing-pages/buzzmonitor/plataforma-integral-social-media` (mesmo design system: paleta orange/pink/ink, Inter, gradient-text, reveal, quote-cards, logo marquee)
**Região/idioma:** LATAM · es-419 (resolvida manualmente — slug sem sufixo, mas LP é ES pra `content.buzzmonitor.com`; o gate de CI resolve latam pelo `<html lang="es-419">`)
**GTM:** GTM-MKQBX2MG (latam, tracking.json) + Meta Pixel 935436740448328 (mesmo par da LP design base, mesmo domínio)

## Estrutura

- NAV (Plataforma · IA · Soluciones · Clientes + CTA Agenda una demo → #demo)
- HERO (overline dor + H1 + body + CTA; **vídeo** `social-listening-es.mp4` reaproveitado da LP ia-para-social-listening-es no lugar do banner original)
- INTRO-PLATAFORMA + FORM (3ª seção, espelhando a LP original — override consciente da GUIDELINES §10; form MOCK, §11)
- AGENCIAS-DIFERENTE (3 parágrafos + logos de agências)
- IA-LO-CAMBIA-TODO (print ai-insights.png + 5 cards)
- MODULOS (6 cards com bullets ✓)
- TRIAL (cta-box gradiente, preço $390 USD/mês)
- SIN-TAREAS-MANUALES (bullets + print tela-computador-bm2.png)
- SUPERA-EXPECTATIVAS (3 colunas + CTA)
- GESTIONA-CON-IA (8 cards; print monitoreo-de-videos.png no card Visual Listening)
- TODO-EN-UNA-PLATAFORMA (6 bullets)
- CHATGPT (seção pausa)
- MONITOREA-TUS-REDES / ATENCION-CENTRALIZADA / DASHBOARDS-TIEMPO-REAL (zigzag com prints crises-1.png, crises-2.jpg, img-relatorios-dashboard.png)
- TESTIMONIOS (6 quotes de agências + CTA)
- CLIENTS-PROOF (4 stats animados + logo marquee)
- CTA-FINAL (trial repetido — fidelidade à LP original)
- FOOTER

## Estado

- [x] HTML gerado
- [x] OG image 1200×630 → `assets/og-plataforma-integral-agencias.png`
- [x] Validações: em-dash 0 · SEO completo (1 desc, 10 og, 4 twitter, JSON-LD parseia) · GTM gate OK (latam/MKQBX2MG)
- [ ] Revisão (frontend-design review + web-design-guidelines) — rodar `/lp-revisar buzzmonitor/plataforma-integral-agencias`
- [ ] Formulário integrado — rodar `/lp-integrar-form buzzmonitor/plataforma-integral-agencias [snippet]` (campos do form real documentados em copy.txt)
- [ ] Publicado — rodar `/lp-publicar buzzmonitor plataforma-integral-agencias content.buzzmonitor.com`

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header/footer; raster base64, web-safe §19)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `./assets/social-listening-es.mp4` + `social-listening-es-poster.jpg` (hero — origem: ia-para-social-listening-es)
- `./assets/ai-insights.png`, `tela-computador-bm2.png`, `monitoreo-de-videos.png`, `crises-1.png`, `crises-2.jpg`, `img-relatorios-dashboard.png` (prints — origem: ia-para-social-listening-es)
- `./assets/logos-agencias/*` e `./assets/logos-clientes/*` (origem: plataforma-integral-social-media)
- `./assets/og-plataforma-integral-agencias.png`

## Notas

- Sugestões de idioma/anti-IA pendentes de decisão do Victor no fim do `copy.txt` (destaque: "Monitorización" é grafia de Espanha; LATAM seria "Monitoreo" — mantido literal da LP original).
- hreflang: LP única (sem irmãs BR/PT no repo) — só canonical + x-default.
