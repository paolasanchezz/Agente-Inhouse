# LP Buzzmonitor — inscripcion-confirmada

Thanks page **genérica** de confirmación de inscripción para todos los eventos de Buzzmonitor
LATAM (workshops, webinars, eventos presenciales). Texto fijo, sin nombre ni fecha del evento:
una URL sirve para todos, basta apuntar el redirect de éxito del form a ella.

**Generado en:** 2026-10-21
**Copy-fuente:** `copy.txt` (escrita por el agente a pedido del usuario; Notion no publicado: no había MCP de Notion conectado en la sesión)
**Idioma/región:** ES-LATAM (`es-419`), GTM `GTM-MKQBX2MG` (validado con `check_gtm_region.py`)
**Dominio:** `evento.buzzmonitor.com` (guarda-chuva migrado al CI, deploy solo vía `/lp-publicar`)
**URL final:** `https://evento.buzzmonitor.com/inscripcion-confirmada`

## Estructura

- CONFIRMACIÓN (sello de check con gradiente + etiqueta "Lugar reservado" + H1 "Gracias por inscribirte." + SUB (información en los próximos días) + nota de spam)
- QUIÉNES SOMOS (tarjeta tipo vidrio con panel del logo + overline + H2 "Mucho gusto, somos Buzzmonitor" + texto + botón a buzzmonitor.com/es/)
- CLIENTES (H2 "Más de 1.000 clientes..." + marquesina con 9 logos en blanco)
- FOOTER (padrón del dominio, ref. `workshop-reportes-ia-cdmx-octubre-2026`: logo + línea legal + 5 redes `buzzmonitor.es`)

Base de estructura: `cxpress/evento-confirmado`. Línea visual v2 (2026-10-21, pedido del usuario:
"más contemporáneo, tecnológico y premium"): modo oscuro (`#0E0716`) con la paleta de las LPs de
workshop LATAM (morado + gradiente rosa→naranja), grilla técnica con halos de color en el hero,
sello con anillo cónico animado, etiquetas en JetBrains Mono, tarjeta tipo vidrio en Quiénes somos
y marquesina infinita de logos en blanco (estática con `prefers-reduced-motion`).

## Excepciones deliberadas a las GUIDELINES (precedente: cxpress/evento-confirmado)

- **`noindex, follow`**: página post-acción; el Lighthouse SEO del lp-publicar va a marcar
  "is-crawlable". Esperado, no "arreglar".
- **Sin OG image, sin OG/Twitter/JSON-LD y sin placeholders `{{DOMAIN}}`**: nadie comparte esta URL.
- **Sin estructura mínima de LP** (§6) y **sin form**: no hay captación, es solo confirmación.
- **Sin canonical/hreflang**: LP única, noindex.

## Estado

- [x] HTML generado
- [x] Revisión (ver `REVISAO.md`)
- [n/a] OG image (thanks page, ver excepciones)
- [n/a] Formulario (página post-form)
- [ ] Publicado — `/lp-publicar buzzmonitor inscripcion-confirmada evento.buzzmonitor.com`

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (header, footer y tarjeta de Quiénes somos; sin `<text>`, §19 ok)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `./assets/clientes/logo-{samsung,sony,ikea,sephora,santander,havas,tbwa,mccann,realmadrid}.png`
  (copias de `la-mejor-plataforma-social-listening-es/assets/clientes`, sin Bizum por ser marca solo de España)

## Uso

En el form de inscripción de cada evento Buzzmonitor LATAM (Jotform u otro), configurar el
redirect de éxito a `https://evento.buzzmonitor.com/inscripcion-confirmada`. La página promete
que el correo con fecha, horario, lugar o enlace de acceso y agenda llega "en los próximos días":
ese correo tiene que salir.
