# REVISION: `oferta-cafe-medellin-sep26` (Cxpress ES-LATAM)

Fecha: 2026-09-21

## Verificaciones

| Chequeo | Resultado |
|---|---|
| Em-dash (guion largo) en HTML y copy | 0 |
| Exclamaciones | 0 (el `¡ENVIAR!` es del Jotform, no de la copy) |
| Antítesis por negación | 1 (límite: 2 en piezas de hasta 500 palabras) |
| Frases y filler típicos de IA | ninguno detectado |
| Español de España | ninguno ("correo electrónico", "celular", "panel", tuteo) |
| Voseo | ninguno (Colombia, tuteo) |
| "Cxpress" con artículo en español | no aparece (regla del BRANDBOOK §2) |
| H1 lidera con el dolor | sí (fundamentos-copy §0) |
| Overflow horizontal a 375px | `scrollWidth == 375`, sin desborde |
| Formulario | Jotform `261525344798871` cargando dentro de la tarjeta |
| Posición del formulario | última sección (default §10 para BoFu, sin override) |
| Paleta | 3 colores: navy, royal, naranja (§1) |
| Skip-link, `:focus-visible`, `prefers-reduced-motion` | presentes |
| Fallback de animación | `setTimeout` de 4 s + `@supports not` |
| Favicon | `logo-icon.png` del brand, un solo `<link rel="icon">` |
| SEO (§15) | description, robots, 8 OG, Twitter card, JSON-LD (Organization + WebPage + Offer) |
| GTM | `GTM-WRQ47B9R` en `<head>` y `<noscript>` |
| Iconos de redes | paths oficiales de Simple Icons (los mismos ya corregidos en la LP de clínicas) |

## Contraste (AA)

Mismos pares que la LP hermana, todos por encima de 4.5:1. Texto sobre fondo teñido siempre
en navy `#232960`, nunca en royal (la advertencia de `GUIDELINES.md` §7).

## Ajustes durante la revisión visual

1. Anchos de bloque pasados de `ch` a px en H1 del hero, subtítulo, H2 de la sección de IA y
   H2 de la oferta. La unidad `ch` mide la fuente del contenedor, no la del título, y dejaba
   los titulares en columnas de 4 y 5 líneas. Es la misma trampa que apareció en la LP de
   clínicas.

## Pendiente

- [ ] Pegar el CSS del Jotform en el editor (sirve para esta LP y para la de clínicas, que
      comparten formulario).
- [ ] Confirmar que la oferta (15 días + 50% + 20 h) sigue vigente para este evento en la
      fecha de publicación. Fue confirmada por el usuario el 2026-09-21.
