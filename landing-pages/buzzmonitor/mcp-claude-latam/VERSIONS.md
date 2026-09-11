# Versiones de la LP buzzmonitor/mcp-claude-latam

Cada versión se abre por separado. La **versión viva** siempre es el `index.html` de la raíz de la carpeta; las anteriores quedan congeladas en `versions/`.

| Versión | Archivo | Fecha | Qué es |
|---|---|---|---|
| **v1** | `versions/v1/index.html` | 2026-09-10 | Fondo claro, naranja como acento. Copy optimizado (H1 abre por el dolor). Hero con diagrama conector SVG. Beneficios en grid de 6 cards. |
| **v2** | `versions/v2/index.html` | 2026-09-10 | Fondo oscuro con degradados ámbar, naranja y rojo. Copy del brief, literal. Hero con MacBook + spotlight y la grabación real de la conexión del MCP. Beneficios como lista editorial 01 a 06. |
| **v3** *(viva)* | `index.html` | 2026-09-10 | Ajustes de Ulises sobre la v2: menos aire, MacBook más chico **que se abre con el scroll**, titulares con efecto máquina de escribir, prompts que reaccionan al scroll, bloque de equipos como panel destacado, footer en 4 columnas con las redes de LATAM y **formulario Jotform real**. Incluye el update del 2026-09-10 (ver abajo). |

## Cómo verlas en local

Desde la raíz del repo, con un servidor estático en el puerto 8123:

```bash
python3 -m http.server 8123
```

- v3 (viva): `http://127.0.0.1:8123/landing-pages/buzzmonitor/mcp-claude-latam/index.html`
- v2: `http://127.0.0.1:8123/landing-pages/buzzmonitor/mcp-claude-latam/versions/v2/index.html`
- v1: `http://127.0.0.1:8123/landing-pages/buzzmonitor/mcp-claude-latam/versions/v1/index.html`

Las rutas de assets de los snapshots fueron reescritas a `../../../../brand/...` para que funcionen desde su subcarpeta. No editar v1 ni v2: son congelados de consulta.

## Qué cambió de v1 a v2

**Copy.** v2 usa el copy del brief tal cual. v1 tenía una versión optimizada: H1 abriendo por el dolor ("Armar el reporte toma más tiempo que entenderlo"), orden de bloques reordenado al funnel y la oferta después del valor. Esa alternativa sigue en `versions/v1/copy.txt` por si se quiere testear A/B.

**Dirección visual.** v1 era clara y sobria. v2 es oscura y de alto contraste, inspirada en la jerarquía de nickho-motorsports y en el motion de crency.agency.

**Hero.** v1: diagrama SVG de nodos Buzzmonitor y Claude. v2: MacBook con spotlight cálido (referencia: el bloque `spotlight` de filmbot.com) reproduciendo la grabación real del flujo de conexión.

**Bloque de valor.** v1: grid de 6 cards. v2: lista editorial numerada 01 a 06.

## Qué cambió de v2 a v3

**Ritmo.** `--pad` bajó de `clamp(96,12vw,200)` a `clamp(64,7vw,118)` y el hero perdió aire arriba. La página pasó de 8.437 px a ~7.500 px de alto: menos negro entre el final de un bloque y el comienzo del siguiente.

**MacBook.** De `min(1020px,100%)` a `min(760px,92%)`, y la apertura de la tapa ahora termina con el equipo bien dentro de la pantalla (antes se completaba antes de que se viera entero).

**Copy.** "Prueba primero" → "Prueba su potencial ahora". "Menos trabajo manual. Más inteligencia." → "Reportes más rápidos y análisis más precisos. Menos trabajo manual.". "Social Listening + Claude." quedó en una línea con "Ahora sí se puso interesante." subrayado en naranja. El bloque de conversación pasó a "Buzzmonitor extrae los datos." + "Claude te da los insights" en degradado.

**Hero, CTAs.** Salió "Conectar ahora" (llevaba al mismo bloque donde ya estaba). El Paso 0 pasó a una tarjeta destacada con borde en degradado, etiqueta "PASO 0" y el CTA "Crear cuenta gratis" adentro, que equilibra la columna derecha contra los 3 pasos.

**Ticker.** Ya no repite la URL: ahora lista 8 capacidades del MCP (copy nueva, ver nota en `copy.txt`).

**Motion.** Máquina de escribir en los 9 titulares principales, prompts que se desenfocan y se aclaran según su distancia al centro de la pantalla, hover de botones de izquierda a derecha, halo del mouse por encima de todo (antes se cortaba en el borde entre bloques) y con suavizado por lerp, y movimiento ambiente permanente en los resplandores de cada sección.

**Equipos.** El bloque entero pasó a un panel con borde en degradado, glow propio y eyebrow, para que sea el más potente después del hero.

**Formulario.** El mock salió y entró el Jotform real (`241825239057661`). El card se volvió claro para que el blanco del formulario se lea intencional: el iframe es cross-origin y su interior no se puede estilizar desde acá.

**Footer.** Las 5 redes de LATAM (Instagram, X, Facebook, LinkedIn, YouTube), tomadas de `plataforma-integral-social-media`.

## Update de la v3 (misma versión, 2026-09-10)

Segunda tanda de ajustes de Ulises, aplicada sobre la propia v3 (no se abrió v4):

- **Footer en 4 columnas.** Logo, Política de Privacidad, copyright y redes, en horizontal con `space-between`, las redes a la derecha.
- **La tapa del MacBook se abre con el scroll.** Antes giraba apenas 15 grados y terminaba enseguida. Ahora arranca casi cerrada (78 grados sobre una bisagra en la base) y se abre a lo largo de ~0,85 de pantalla de scroll, con easing `easeInOut`. La rotación pasó a un `.mac__hinge` con `transform-origin:50% 100%`.
- **El halo del mouse quedó detrás del MacBook.** Bajó de `z-index:290` a `150` y el escenario subió a `160`. Hubo que sacarle el `z-index:1` a `.hero__in`, que creaba un contexto de apilamiento y dejaba al MacBook atrapado por debajo del halo. El halo sigue por encima del fondo de todas las secciones (por eso no se corta) y ahora por debajo de la nav.
- **Fuera el marco naranja del bloque del formulario.** El borde en degradado del panel se cambió por un `1px solid rgba(255,255,255,.09)`. El glow y la sombra quedan.
- **Destinos de los CTAs, unificados:**

| CTA | Destino |
|---|---|
| Agendar una reunión (nav y bloque de equipos) · Hablar con ventas (x2) | `#form` |
| Conectar MCP | `#instrucciones` (el bloque de los 3 pasos) |
| Crear cuenta gratis · Probar gratis (x2) | `https://app.buzzmonitor.com.br/user/signup/start` con `utm_source=lp&utm_content=lp-mcp-claude-latam` |

### Segundo update de la v3 (2026-09-10)

- **Los titulares se escriben al llegar a su bloque.** Antes se escribían todos al cargar: la culpa era un `setTimeout` de 4 s pensado como red de seguridad, que disparaba todo de golpe y anulaba el trigger por scroll. Ahora la red de seguridad vive en el loop de scroll y solo escribe lo que ya está en pantalla (o lo que quedó arriba, por si se llegó por un ancla).
- **La tapa del MacBook abre de verdad.** El sentido de giro se leía al revés: un `rotateX` positivo con la bisagra abajo parece una pantalla echada hacia atrás, y volver a 0 parecía cerrarla. Ahora gira en negativo (la tapa cae sobre la base), la cámara mira desde un poco más abajo (`perspective-origin:50% 130%`) y hay un velo oscuro sobre la pantalla que se disipa a medida que abre, para que "cerrada" no deje lugar a dudas.
- **Carrusel dentro del bloque, en desktop.** Corre por debajo del paso 3 y pasa por detrás de la tarjeta del Paso 0, que ahora tiene base opaca. Eso llena el hueco que quedaba a la izquierda y equilibra las dos columnas. En pantallas menores a 1001 px sigue siendo una banda debajo del bloque.
- **Pasada mobile-first.** Todos los blancos de toque llegan a 44 px (el logo va envuelto en un enlace de 44 px de alto, el control de pausa salió de `.mac` para no heredar su escala), la nav bajó de 83 px a 74 px, el MacBook usa el 100 % del ancho, y en menos de 640 px los desenfoques grandes bajan a 14 px y se apaga el drift, que es lo que más pesa en GPU de celular.
- **Botón del header:** "Agendar reunión", 13 px, más compacto.

### Tercer update de la v3 (2026-09-10)

- **El carrusel ya no cruza toda la pantalla.** En desktop ocupa solo la franja despejada: desde el borde izquierdo de la ventana hasta 44 px por debajo de la tarjeta del Paso 0, así que parece salir de detrás de ella y disolverse hacia el otro extremo. El fundido a negro quedó solo en la punta izquierda. El ancho se calcula con variables CSS (`--rightcol-w`, derivada del ancho del wrap, el gutter y el gap del grid), así que el corte cae exacto en el borde de la tarjeta a 1024, 1200 y 1440 px.
- **Botón del header más chico que el logo:** 171x26 px contra 132x27 px del logo. En móvil vuelve a 44 px de alto para no romper el blanco de toque.

### Cuarto update de la v3 (2026-09-10)

- **El carrusel ya no pasa por detrás del Paso 0.** Termina 26 px antes del borde de la tarjeta (medido igual a 1024, 1200 y 1440 px) y ahora tiene fundido en las dos puntas, no solo en la izquierda.
- **Botón del header:** 136x21 px en móvil (el logo mide 114x23) y 171x26 px en desktop, es decir ~25 % más grande. En móvil el botón se ve de 21 px pero el blanco de toque real es de 156x45 px, resuelto con un `::after` transparente para no romper la accesibilidad.
