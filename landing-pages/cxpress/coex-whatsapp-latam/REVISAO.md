# Revisão LP — cxpress/coex-whatsapp-latam

**Data:** 2026-09-23
**Auditores:** frontend-design (review mode) + web-design-guidelines + scripts deterministas (GTM, SEO, JSON-LD)

## Decisión resuelta (2026-09-23)

Paola confirmó la recomendación: hero vuelve a llevar solo CTA + visual (mockup-plataforma-laptop.png), y el formulario pasó a una sección dedicada después del FAQ (antes del cierre), en **mock** — el embed real de Jotform se reintegra vía `/lp-integrar-form` recién cuando el diseño quede aprobado.

- [x] Hero: sacado `.hero__formcard`, restaurado `.hero__visual` (pills decorativos + mockup laptop) y CTA "Quiero agendar mi demo gratis" con scroll a `#agendar`.
- [x] Nueva sección `.agendar` (mock `<form>` con 4 campos: nombre, empresa, WhatsApp, correo) ubicada después de FAQ, antes del cierre — cumple GUIDELINES §10 (form en la última sección para LP MoFu/BoFu) y §11 (mock durante diseño).
- [x] `copy.txt` actualizado para reflejar la estructura final.
- [x] Sello de GTM regenerado tras el cambio.

## Aplicado automáticamente (2 críticos)

- [x] **Bloque de dolores usaba grid de 2 columnas + emoji de color como ícono** — `GUIDELINES.md` §8 exige que toda sección tipo "Problema/dor" sea **lista vertical** (no grid) con **ícono X rojo**, para distinguirla visualmente del patrón de "Beneficios" (grid + check verde). Además, el emoji nativo (👥💬📱📊🤖) renderiza en colores fijos fuera del CSS, rompiendo la disciplina de paleta de 2-3 colores (§1). Cambié `.dolores__grid` de grid a lista vertical (`flex-direction:column`) y los emojis por un ícono ✕ en `var(--danger)` (nuevo token, `#D64545`) sobre círculo tenue — línea 209 (CSS) y bloque de dolores en el HTML.
- [x] **Clase `.dolores__intro` reutilizada en la sección de resultados** (línea 512), un nombre de sección aplicado a otra semánticamente distinta. Renombrada a `.section-intro` en ambos usos.

## Mejoras opcionales (2)

- [ ] **`.pasos__grid` con 5 columnas en desktop** dentro de `max-width:1200px` deja cada celda angosta (~200px). Considerar 3+2 o aumentar el `gap` para que respire más (§2).
- [ ] **Logo de navbar/footer apunta a `https://cxpress.ai/`**, no a la home regional del manifest (`websites.latam` = `https://home.cxpress.io`, `GUIDELINES.md` §17). Es un patrón preexistente en **toda la flota de LPs Cxpress** (confirmado también en `telefonia-ia-latam`), no algo introducido en esta edición — recomendaría auditarlo aparte en vez de corregirlo solo acá, para no desalinear esta LP del resto.

## Nice-to-haves (1)

- [ ] El bloque "Diferenciales" no lleva ícono por card, solo texto — podría sumar un ícono sutil, aunque el patrón sin ícono ya es consistente con `telefonia-ia-latam`.

## Hallazgos informativos (no bloquean, ya conocidos)

- **hreflang ausente.** Existe una LP hermana `landing-pages/cxpress/coex-whatsapp/` (PT-BR, fuente original), y `GUIDELINES.md` §16 pide hreflang cruzado cuando hay variantes de idioma. No lo agregué porque la hermana PT-BR todavía tiene `canonical` con placeholder `{{DOMAIN}}` — no está desplegada a una URL real todavía. Agregar hreflang hacia una URL que no existe sería peor que omitirlo. Revisar cuando la versión PT-BR se publique.
- **FAQ "¿Cuánto tarda en implementarse?"** sigue con placeholder `[PENDIENTE: confirmar con el equipo de producto...]` — no inventé un plazo. **Bloqueante para publicar**, no para revisar.

## Checks limpios (sin hallazgos)

- Em-dash: 0 ocurrencias (tolerancia cero, `GUIDELINES.md` §5) ✓
- Fidelidad de copy vs `copy.txt`: sin vazamentos, sin pull-quotes inventados, sin parafraseo cosmético ✓
- GTM: contenedor correcto para región `latam` (`GTM-WRQ47B9R`), stamp actualizado ✓
- SEO: 1 description, 10 og:, 4 twitter:, 1 JSON-LD (parsea OK), 1 canonical ✓
- OG image: `og-coex-whatsapp.png` compartida a propósito con la LP hermana PT-BR (excepción legítima de §18), 1200×630 ✓
- Logo SVG: sin `<text>` vivo, no serifa (Cxpress ya está OK según §19) ✓
- Contraste: kicker, pill de objeción y tabla comparativa dentro de AA (verificado manualmente) ✓
- Accesibilidad: heading único h1, jerarquía sin saltos, todo `aria-labelledby` resuelve a un id real, todas las imágenes con `alt` apropiado, `prefers-reduced-motion` cubre reveals + pulse del kicker + form card, skip-link y `:focus-visible` intactos ✓
- Secciones balanceadas (12 `<section>`, 42 `<div>`, 7 `<details>` de FAQ) ✓

## Próximos pasos

1. Decidime los 2 puntos pendientes de arriba (posición del form + mock vs. real).
2. Confirmar con el equipo de producto el tiempo de implementación para cerrar la FAQ pendiente.
3. Diseño aprobado → `/lp-integrar-form cxpress/coex-whatsapp-latam "<snippet>"` (si volvimos a mock) o directo a publicar si dejamos el embed real donde está.
4. Publicar → `/lp-publicar cxpress coex-whatsapp-latam content.cxpress.io`
