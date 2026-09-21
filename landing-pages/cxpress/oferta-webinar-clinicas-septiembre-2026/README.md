# LP `oferta-webinar-clinicas-septiembre-2026` (Cxpress · ES-LATAM)

**Rediseño** de la página que hoy vive en GreatPages:
https://www.cxpress.ai/oferta-webinar-clinicas-septiembre-2026

| Campo | Valor |
|---|---|
| Marca | Cxpress |
| Región / idioma | LATAM, ES-LATAM (`es-419`) |
| Funil | BoFu / remarketing (asistentes al webinar de clínicas) |
| Fuente de copy | Copy literal visible en la página original (`copy.txt`) |
| GTM | `GTM-WRQ47B9R` (contenedor LATAM, `brand/cxpress/tracking.json`) |
| Dominio asumido | `content.cxpress.io` (paraguas Cxpress, convención del repo) |
| Estado | Generada, revisada y con formulario integrado. **No publicada.** |

**Form provider:** Jotform, `jsform/261525344798871` ("Ofertas Cxpress LATAM", integrado 2026-09-21)

> **El form es compartido.** Tambien lo usa `landing-pages/cxpress/webinar-tecnologia-maio2026-oferta-latam`. Cambiar campos, estilo o Thank You Page afecta a las dos LPs.

### Estilo del formulario

El embed es un iframe cross-origin: el CSS de la LP no entra. Para que el form tome el estilo de la pagina hay que pegar [`assets/jotform-custom-css.css`](assets/jotform-custom-css.css) en el editor de Jotform, en **Form Designer (pincel) > Styles > Inject Custom CSS**. Probado inyectado sobre el form real. Lo unico que no alcanza es el widget de telefono internacional, que corre en un iframe anidado propio.

---

## Qué cambió respecto de la original

La **copy no se tocó**: ni una frase fue reescrita. Lo que cambió es el diseño.

| | Original (GreatPages) | Rediseño |
|---|---|---|
| Color dominante | Blanco con azul royal de acento | **Azul marino `#232960`** como espina dorsal (hero, urgencia, CTA final, footer) |
| Paleta | Royal + naranja + amarillo repartidos | 3 colores: navy (base), royal (apoyo), naranja (única acción) |
| Hero | Formulario a la derecha sobre fondo blanco | Hero navy full-bleed, tarjeta blanca elevada, corte diagonal hacia la sección siguiente |
| Jerarquía de oferta | 4 bullets sueltos | Bloque "Tu oferta incluye" con regla divisoria y cifras destacadas en amarillo |
| Urgencia | Banda con sello centrado | Banda navy con sello rotado (`-3deg`) + mascota Samir |
| Dashboards | 6 preguntas en texto plano | 6 tarjetas con borde lateral de color rotativo e icono de pregunta |
| Plataforma | Lista numerada 01-06 | Misma lista, numerales en Bitter (fuente de acento de marca) |
| Cierre | Botón suelto | Sección CTA navy con recap de la oferta + botón |
| Decoración | Líneas sueltas de GreatPages | Vocabulario de marca: píldoras y arcos (brandbook p. 5-6), solo en márgenes |

## Estructura (6 secciones + footer)

1. **Hero** (navy): overline, H1 con la palabra "caos" en amarillo, sub, bloque de oferta, tarjeta de formulario
2. **Problema + capacidades** (blanco): dolor a la izquierda, 6 capacidades con check a la derecha
3. **Urgencia** (navy): sello rotado + mascota. Aparece **una sola vez** en la página
4. **Dashboards** (off-white): 6 preguntas en grid 3×2
5. **Plataforma** (blanco): lista numerada 01-06, sección de respiro sin cards
6. **CTA final** (navy): recap de la oferta + botón

## Decisiones que conviene saber

- **Formulario en el hero (§1), no en la 4ª sección.** `GUIDELINES.md` §10 manda form al medio/fin para BoFu. Se mantiene arriba porque (a) el tráfico son inscritos al webinar, o sea lead caliente que ya conoce la marca, y (b) es donde estaba en la página original, que ya está corriendo. Override documentado, como pide la §10. Todos los CTA de la página hacen scroll a `#oferta`.
- **Tres secciones oscuras en vez de una.** `GUIDELINES.md` §1 sugiere una sola sección oscura. El pedido explícito fue "azul oscuro como color principal", así que el navy ancla hero, urgencia y cierre, con secciones claras intercaladas. No es colcha de retazos: es un único tono repetido.
- **Formulario Jotform** (`jsform/261525344798871`), integrado con `/lp-integrar-form` sobre el mock. Los campos son los del form (Nombre, Apellidos, E-mail Comercial, Empresa, País, Teléfono, opt-out de newsletter), no los 4 de la página de GreatPages. El wrapper `.jotform-embed` no lleva la clase de card para evitar card dentro de card; el título, el subtítulo y la nota legal quedan en la tarjeta de la LP.
- **Sin countdown.** La página original no tiene fecha de inicio publicada, y `GUIDELINES.md` §7 prohíbe `aria-live` en contadores.

## Assets

| Archivo | Origen |
|---|---|
| `assets/og-oferta-webinar-clinicas-septiembre-2026.png` | Generado desde `assets/og-template.html` (1200×630) |
| Mascota Samir | `brand/cxpress/assets/mascot/samir-laptop-cutout.png` |
| Logos | `brand/cxpress/assets/logos/logo-reversed.svg` y `logo-icon.png` (favicon) |

## Cómo publicar

`content.cxpress.io` está en `landing-pages/dominios/MIGRADOS.json`: publicar = entrar en el manifiesto del dominio + PR, el CI deploya. **Nunca** `vercel deploy` a mano. Ver `landing-pages/CONTEXT.md` (Regla Nº 1).

Si la idea es reemplazar la página de GreatPages en `cxpress.ai`, eso es otra decisión (dominio distinto, fuera del paraguas) y hay que definirla antes de publicar.
