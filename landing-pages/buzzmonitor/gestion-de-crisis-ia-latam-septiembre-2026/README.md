# Buzzmonitor — LP webinar "Gestión de Crisis con IA" (LATAM)

Webinar · 24 de septiembre 2026 · 10:00 MX · 11:00 COL/PER · 12:00 CL · 13:00 ARG · online y en vivo.
Anticipación, monitoreo y respuesta estratégica de crisis en redes sociales + demostración en vivo de la plataforma.

Se publicará en `webinar.buzzmonitor.com/gestion-de-crisis-ia-latam-septiembre-2026` (guarda-chuva).

> Adaptación ES-LATAM de la LP `gestao-de-crises-ia-agosto-2026` (PT-BR, 25 de agosto 2026). Mismo tema, mismo diseño y estructura, sin modificar la LP original. Traducida al español y re-fechada para el evento de LATAM.

## Status

- [x] Copy traducida a ES-LATAM (pilar lingüístico + anti-IA aplicados)
- [x] Fecha/horarios actualizados (24 sept · 10:00 MX/11:00 COL-PER/12:00 CL/13:00 ARG)
- [x] Speakers: Raquel Oliveira (Business Developer) y Amanda Bozza (Head of Operations Latam and Iberia) — fotos en `assets/speakers/`
- [x] OG image 1200×630 → `assets/og-gestion-de-crisis-ia-latam-septiembre-2026.png`
- [x] Formulario integrado — Jotform (2026-08-26), mismo form compartido de `webinar-atencion-multicanal-latam` (`jsform/261188302248052`)
- [x] Revisión formal (`/lp-revisar`) — 6 críticos corregidos (GTM erróneo, contraste AA en badge de speaker, piso tipográfico mobile, form mock sin atributos, JSON-LD y logos apuntando al home de Brasil en vez del home LATAM). Detalle en `REVISAO.md`.
- [x] Reorganización a pedido del usuario (2026-08-26): formulario movido a la 2ª sección (justo después del hero, patrón ToFu de `webinar-atencion-multicanal-latam`); hero visual y área de speakers agrandados
- [x] Registrado en `landing-pages/dominios/webinar-buzzmonitor-com/manifest.json` + publicado vía CI (`webinar.buzzmonitor.com/gestion-de-crisis-ia-latam-septiembre-2026`)

**Form provider:** Jotform (`jsform/261188302248052`, 2026-08-26)

## Diferencias vs. la LP original (PT-BR)

- Idioma: `es-419` (en vez de `pt-BR`), `og:locale` `es_LA`
- Fecha: 24 de septiembre 2026 (jueves) en vez de 25 de agosto (evento multi-huso LATAM en vez de horario único Brasília)
- Speakers: Raquel Oliveira + Amanda Bozza (en vez de Nathalia Crivellaro, Potyra Santos y Bruna Barreto) — grid ajustado a 2 columnas
- Formulario: Jotform compartido de LATAM (`jsform/261188302248052`, mismo de `webinar-atencion-multicanal-latam`) en vez del JotForm en portugués de la original
- Orden de secciones: formulario en la 2ª sección (la original lo tiene al final) — a pedido del usuario, siguiendo el patrón de `webinar-atencion-multicanal-latam`
- Instagram del footer: `@getbuzzmonitor.es` (cuenta LATAM, en vez de `@buzzmonitorbr`)
- Slug/URL nuevos, sin tocar la LP original ni su registro en el manifiesto

## Cómo actualizar

Editar `index.html` y correr `/lp-publicar buzzmonitor gestion-de-crisis-ia-latam-septiembre-2026 webinar.buzzmonitor.com`.
