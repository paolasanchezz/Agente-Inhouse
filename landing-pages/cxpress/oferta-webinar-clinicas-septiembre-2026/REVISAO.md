# REVISION: `oferta-webinar-clinicas-septiembre-2026` (Cxpress ES-LATAM)

Fecha: 2026-09-21

## Verificaciones hechas

| Chequeo | Resultado |
|---|---|
| Em-dash (`—`) en el HTML | 0 ocurrencias |
| `&mdash;` en el HTML | 0 ocurrencias |
| Copy alterada respecto de la original | Ninguna frase reescrita (ver `copy.txt`) |
| Overflow horizontal a 375px | `document.scrollWidth == 375`, sin desborde |
| Formulario | Embed Jotform `261525344798871`. Los campos y sus labels los controla Jotform dentro del iframe |
| Skip-link + `:focus-visible` | Presentes |
| `prefers-reduced-motion` | Reveals y transiciones desactivados |
| Fallback de animación | Si `IntersectionObserver` falla, `setTimeout` de 4 s muestra todo; además `@supports not` |
| `alt` / `aria-hidden` | Decorativos con `alt=""` o `aria-hidden="true"`; SVG de iconos ocultos a lectores |
| Favicon | `logo-icon.png` del brand, un solo `<link rel="icon">` |
| Paquete SEO (§15) | description, robots, 8 tags OG, Twitter card, JSON-LD con Organization + WebPage + Offer |
| GTM | `GTM-WRQ47B9R` (LATAM) en `<head>` y `<noscript>` |
| `<img>` en grid (§14) | `.urgency__mascot img` con `min-height:0` |

## Contraste (AA, ≥4.5:1)

| Combinación | Ratio aprox. |
|---|---|
| Blanco sobre navy `#232960` | 13:1 |
| `#D7E2FF` (sub del hero) sobre navy | 10:1 |
| Navy sobre `#D7E2FF` (eyebrow) | 10:1 |
| Navy sobre `#FFDCC3` (overline del hero) | 9:1 |
| Navy sobre naranja `#EF863C` (botones) | 5.3:1 |
| Navy sobre amarillo `#F1A908` (sello) | 7:1 |
| `#4a4a4a` sobre blanco (body secundario) | 8.9:1 |

La advertencia de `GUIDELINES.md` §7 (royal sobre lila reprueba con ≈4.0:1) no aplica: todo el texto sobre fondo teñido usa navy, nunca royal.

## Ajustes aplicados durante la revisión visual

1. Decoración del hero rehecha: las formas quedaron solo en los márgenes, fuera de la columna de texto.
2. Iconos de las tarjetas de preguntas: se reemplazó el glifo `¿?` por SVG con `display:block` (el texto se envolvía alrededor del icono inline).
3. Anchos de bloque en px en vez de `ch` (la unidad `ch` medía la fuente del contenedor, no la del título, y dejaba los H2 en columnas demasiado angostas).
4. Píldora naranja del CTA final movida fuera del área de la tarjeta, donde se veía como una mancha marrón sobre el navy.
5. Lista numerada: columna del numeral de 96px a 76px, para acercar número y texto.
6. Móvil: se ocultan las formas decorativas que quedaban pegadas al contenido, y el sello de urgencia baja a 12px para entrar en una línea.
7. Placeholder de los inputs de `#9aa0b5` a `#6f7688` (más legible, aunque las labels visibles ya cubren el requisito).

## Pendiente antes de publicar

- [x] Formulario real integrado (Jotform `261525344798871`).
- [ ] Pegar `assets/jotform-custom-css.css` en Jotform (Form Designer > Styles > Inject Custom CSS) para que el form tome el estilo de la LP. Hasta que se pegue, el form se ve con el tema por defecto de Jotform (botón naranja `#FF6100`, inputs blancos). **Afecta también a `webinar-tecnologia-maio2026-oferta-latam`, que comparte el mismo form.**
- [ ] Confirmar a dónde redirige el Jotform al enviar (Thank You Page): es configuración del formulario, no de la LP.
- [ ] Confirmar dominio destino: `content.cxpress.io` (paraguas, deploy por CI) o reemplazo de la página en `cxpress.ai` (GreatPages, decisión aparte).
- [ ] Validar el placeholder de teléfono (`+57 300 000 0000`, Colombia) contra el público real de la campaña.

## Móvil: formas decorativas por debajo del texto (corregido 2026-09-22)

El usuario reportó elementos superpuestos en móvil. Medido con un script que compara cajas
(recortando por cada ancestro con `overflow:hidden`), a 375 px había 8 casos de forma
decorativa por debajo de texto. Los peores:

| Forma | Encima de | Cobertura |
|---|---|---|
| arco del hero | H1 | 78% |
| arco del hero | eyebrow "Oferta exclusiva" | 64% |
| arco de urgencia | sello de 7 días | 90% |
| arco del cierre | H2 final | 63% |

**Causa raíz: un problema de especificidad CSS, no de posición.** Existía la regla
`.d3,.d4,.d5,.u3,.f1,.f2{ display:none }` dentro del `@media (max-width:640px)`, pero nunca
se aplicó: `.hero__deco span` tiene especificidad (0,1,1) y le gana a `.d3` (0,1,0). O sea que
el `display:block` del contenedor ganaba siempre y las formas seguían visibles en móvil.

**Arreglo:** ocultar los **contenedores** (`.hero__deco, .urgency__deco, .final__deco`) en vez
de los spans. Ocultar el padre no compite en especificidad con la regla de los hijos. Se movió
además al breakpoint de 980 px, que es donde el layout colapsa a una sola columna: las formas
se compusieron apoyadas en los márgenes de la grilla de 2 columnas, y sin esos márgenes no
tienen dónde vivir sin pisar el contenido.

**Verificado después del arreglo** a 320, 375 y 768 px: 0 formas sobre texto, 0 solapes de
texto contra texto, 0 desborde horizontal.
