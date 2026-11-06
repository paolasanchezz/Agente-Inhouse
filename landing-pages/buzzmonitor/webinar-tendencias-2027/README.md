# LP Buzzmonitor — webinar-tendencias-2027 (LATAM)

**Generado en:** 2026-11-06
**Copy-fuente:** `copy.txt` (output de /lp-preparar, ES-LATAM)
**Evento:** Webinar "Marketing Trends 2027" · jueves 10 de diciembre 2026 · 10:00 MX · 11:00 COL/PER · 13:00 CL/ARG (Chile en horario de verano, UTC-3) · online y en vivo · gratuito
**Speakers:** Lorena Rodríguez y Luis Pérez (Business Developer · Buzzmonitor)
**Destino:** `webinar.buzzmonitor.com/webinar-tendencias-2027` (guarda-chuva migrado al CI)

Estética tomada del report "Marketing Trends 2027" (artefacto preliminar del estudio): fondo crema `#f6f4f0`, violeta `#3a12a3`, naranja `#eb7c2e`, franja oscura `#0c0915` con brillos, Inter Tight + logo "Marketing Trends 2027" en Poppins, tarjetas de tendencia con degradado.

> **Desvío consciente de GUIDELINES §3:** el hero va centrado (no texto a la izquierda + visual a la derecha) para replicar el layout del estudio, a pedido del usuario ("basada en la estética del artefacto").

## Estructura

1. Hero: eyebrow + logo Marketing Trends 2027 + H1 (dolor) + sub + CTA + píldoras de fecha/horario + abanico animado de las 9 tendencias (decorativo, aria-hidden)
2. Inscripción (form en la 2ª sección, patrón ToFu §10) + ticket de fecha
3. Contexto: 4 datos (Gartner, SparkToro/Similarweb, Forrester ×2)
4. Programa: franja oscura con las 9 tendencias + CTA
5. Para quién es: 4 ítems con check
6. Speakers: Lorena Rodríguez y Luis Pérez
7. Cierre oscuro: "¿Sabes qué está diciendo tu cliente hoy?" + CTA
8. Footer

## Estado

- [x] Copy ES-LATAM (3 pilares: lingüístico, fundamentos, anti-IA). Em-dash: 0
- [x] HTML generado
- [x] OG image 1200×630 → `assets/og-webinar-tendencias-2027.png` (fuente: `assets/og-source.html`)
- [x] QA visual en navegador: desktop 1440 y mobile 375 (sin overflow horizontal, H1 34px en mobile)
- [x] SEO: description, 10 og, 4 twitter, JSON-LD (Organization + WebPage + Event) válido, canonical
- [x] GTM LATAM `GTM-MKQBX2MG` (head + noscript)
- [x] Formulario integrado: Jotform compartido LATAM `jsform/261188302248052` (2026-11-06), mismo de los demás webinars LATAM
- [ ] Copy sin publicar en Notion (MCP de Notion no estaba conectado en la sesión)
- [x] Publicación: entrada en `landing-pages/dominios/webinar-buzzmonitor-com/manifest.json` + PR (CI deploya). `/lp-publicar buzzmonitor webinar-tendencias-2027 webinar.buzzmonitor.com`

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header y footer; raster base64, sin `<text>`)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `assets/speakers/tendencias-2027-lorena-rodriguez.jpg` (de `workshop-reportes-ia-cdmx-octubre-2026`, 400×400)
- `assets/speakers/tendencias-2027-luis-perez.jpg` (de `gestion-de-crisis-ia-latam-septiembre-2026`, 400×400)
- `assets/og-webinar-tendencias-2027.png`

## Pendientes a confirmar

- Duración del webinar (no informada; no aparece en la LP ni en el JSON-LD `endDate`)
- Cargo de Lorena: "Business Developer" vs "Business Development Representative" (workshop CDMX)

**Form provider:** Jotform (`jsform/261188302248052`, 2026-11-06)

## Cómo actualizar

Editar `index.html` y correr `/lp-publicar buzzmonitor webinar-tendencias-2027 webinar.buzzmonitor.com` (flujo CI: PR → merge-bot → deploy).
