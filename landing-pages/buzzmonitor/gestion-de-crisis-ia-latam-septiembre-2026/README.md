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
- [ ] Formulario real (hoy es un mock estático — Nombre/Correo/Empresa/checkbox — integrar después con `/lp-integrar-form`)
- [x] Revisión formal (`/lp-revisar`) — 6 críticos corregidos (GTM erróneo, contraste AA en badge de speaker, piso tipográfico mobile, form mock sin atributos, JSON-LD y logos apuntando al home de Brasil en vez del home LATAM). Detalle en `REVISAO.md`. Quedan mejoras opcionales heredadas del diseño original (orden de secciones, posición del formulario, H1) sin aplicar — requieren decisión del equipo.
- [ ] Registrar en `landing-pages/dominios/webinar-buzzmonitor-com/manifest.json` + commit/PR vía `/lp-publicar` (dominio migrado a CI, deploy manual bloqueado)

## Diferencias vs. la LP original (PT-BR)

- Idioma: `es-419` (en vez de `pt-BR`), `og:locale` `es_LA`
- Fecha: 24 de septiembre 2026 (jueves) en vez de 25 de agosto (evento multi-huso LATAM en vez de horario único Brasília)
- Speakers: Raquel Oliveira + Amanda Bozza (en vez de Nathalia Crivellaro, Potyra Santos y Bruna Barreto) — grid ajustado a 2 columnas
- Formulario: mock estático (la original usa un JotForm en portugués que no aplica a este público)
- Instagram del footer: `@getbuzzmonitor.es` (cuenta LATAM, en vez de `@buzzmonitorbr`)
- Slug/URL nuevos, sin tocar la LP original ni su registro en el manifiesto

## Cómo actualizar

Editar `index.html` y correr `/lp-publicar buzzmonitor gestion-de-crisis-ia-latam-septiembre-2026 webinar.buzzmonitor.com`.
