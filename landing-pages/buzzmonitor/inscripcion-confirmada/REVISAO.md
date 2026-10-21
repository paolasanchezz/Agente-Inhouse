# Revisão — buzzmonitor/inscripcion-confirmada (2026-10-21)

Revisión en navegador (servidor local, 383px y 1280px) + checks automáticos.

## Críticos (aplicados)

- Alt del último logo corregido a "Fundación Real Madrid" (el asset es el logo de la Fundación, no del club). `copy.txt` actualizado.
- Pequeña pieza decorativa de la tarjeta de Quiénes somos tocaba el logo en mobile: se movió (`left:5%; top:-56px`).

## Checks que pasaron

- Em-dash (`—` / `&mdash;`): 0.
- GTM `GTM-MKQBX2MG` en `<head>` y `<noscript>`; `check_gtm_region.py`: 1 OK, 0 avisos, 0 bloqueos.
- `<html lang="es-419">`, 1 solo `<h1>`, todas las imágenes con `alt` (decorativas con `alt=""` + `aria-hidden`).
- Contraste (WCAG AA): etiqueta 13.3:1 · H1 16:1 · SUB 18.1:1 · nota 7.1:1 · overline 5.2:1 · cuerpo 7.1:1 · botón 16:1 · footer 7.1:1.
- Todos los `target="_blank"` con `rel="noopener"`; el botón avisa "(se abre en una pestaña nueva)" para lectores de pantalla.
- Skip-link, `:focus-visible`, `prefers-reduced-motion`, reveal con `<noscript>` + fallback por timeout.
- Sin scroll horizontal en 383px; logos en grilla 3×3 en mobile.
- Logos de header/footer en SVG sin `<text>` (§19).
- Fidelidad de copy: todo el texto visible es literal de `copy.txt` (whitelist: skip-link, aria-labels, footer).

## Opcionales (no aplicados)

- Los logos de clientes son mayormente globales/España; si hay logos de clientes LATAM (MX/CO) con permiso de uso, convendría sumarlos.
- Si algún evento usa confirmación manual de cupo, esta página no sirve tal cual (afirma "Lugar reservado").

## v2 — rediseño premium/tech (2026-10-21)

Copy aprobada sin cambios; solo cambió el estilo (ver README). Re-verificado en navegador a 383px y 1280px:
- Em-dash: 0 · GTM `GTM-MKQBX2MG` OK en `check_gtm_region.py`.
- Todas las imágenes cargan; sin scroll horizontal en mobile.
- Contraste sobre `#0E0716`: blanco 19:1 · texto secundario (78%) ~12:1 · nota/footer (62%) ~7.5:1 · overline `#F4A26A` ~9:1 · botón (texto oscuro sobre blanco) 19:1.
- La copia duplicada de logos (para el loop) lleva `aria-hidden="true"` y `alt=""`; con `prefers-reduced-motion` la marquesina se detiene y la copia se oculta.
- H2 de Quiénes somos con `text-wrap:pretty` (con `balance` quedaba "Mucho" solo en una línea en mobile).
