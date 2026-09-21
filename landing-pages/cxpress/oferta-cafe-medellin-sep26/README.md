# LP `oferta-cafe-medellin-sep26` (Cxpress · ES-LATAM)

Oferta post-evento para asistentes al **Café con Cxpress** de Medellín (Hotel Dann Carlton, 24/09/2026).
LP de registro del evento: [`cafe-medellin-sep26`](../cafe-medellin-sep26/).

| Campo | Valor |
|---|---|
| Marca | Cxpress |
| Región / idioma | LATAM, ES-LATAM (`es-419`), tuteo (Colombia) |
| Funil | BoFu, público caliente (ya asistió al workshop) |
| Dominio | `content.cxpress.io` |
| GTM | `GTM-WRQ47B9R` (contenedor LATAM) |
| Form | Jotform `261525344798871` ("Ofertas Cxpress LATAM"), el mismo de `oferta-webinar-clinicas-septiembre-2026` |

## Nota sobre la marca

El pedido original decía "Café con Buzzmonitor" y "presenta a Buzzmonitor como solución de
atención al cliente". Se construyó como **Cxpress**, por tres razones verificadas:

1. El evento se llama **Café con Cxpress** (así se titula la LP de registro, que vive en
   `landing-pages/cxpress/`). No existe ningún "Café con Buzzmonitor" en el repositorio.
2. Atención al cliente, WhatsApp e IA de primer nivel son el territorio de Cxpress según
   `brand/cxpress/brand-manifest.json`. Buzzmonitor es social listening
   (`brand/buzzmonitor/brand-manifest.json`), no atiende clientes por WhatsApp.
3. El propio pedido decía, en la misma frase, "que se enfoque un poco más en lo que hace Cxpress".

Confirmado con el usuario antes de escribir.

## Estructura (plataforma primero, oferta al cierre)

Decisión del usuario: más peso al producto que en la LP de clínicas.

| § | Sección | Fondo |
|---|---|---|
| 1 | Hero: dolor + qué es Cxpress + tarjeta con la oferta resumida | navy |
| 2 | Diagnóstico: 5 dolores con marca de error | blanco |
| 3 | La plataforma: 6 módulos en grid | off-white |
| 4 | WhatsApp + IA: 3 pasos + diferencial de API oficial | navy |
| 5 | Oferta + formulario | navy |

El formulario queda en la **última sección**, que es el default de `GUIDELINES.md` §10 para
BoFu: el scroll filtra intención. A diferencia de la LP de clínicas, acá no hizo falta
override. El CTA del hero baja hasta `#oferta`.

## Precisión de producto

Los 6 módulos y el flujo de IA salen de `brand/cxpress/BRANDBOOK.md` §2 (módulos principales
y features de IA confirmadas). **No hay ninguna métrica ni case en la copy**: el brandbook
marca los cases como pendientes de validación interna y prohíbe inventarlos.

El diferencial de la API oficial de WhatsApp (frente a WhatsApp Web) sale de
BRANDBOOK §2 "Diferenciais-Chave", punto 1.

## Pilares de copy aplicados

Copy nueva, escrita nativamente en ES-LATAM (no traducida). Se cargaron los 3 pilares
obligatorios del `CLAUDE.md`:

1. `conhecimento/linguistico/es-latam/padrao-linguistico.md`: tuteo, "correo electrónico",
   "celular", "monitoreo", CTA en 1.ª persona ("Quiero mi oferta").
2. `conhecimento/copywriting/fundamentos-copy.md` §0: el H1 carga el dolor
   ("Tu chatbot responde. Tus clientes siguen esperando a un humano"), no la solución.
3. `conhecimento/editorial/regras-anti-ia.md` + anexo ES-LATAM: 0 em-dash, 0 exclamaciones,
   1 antítesis por negación (máximo 2), sin filler ni frases de apertura típicas de IA.

## Assets

| Archivo | Origen |
|---|---|
| `assets/og-oferta-cafe-medellin-sep26.png` | Generado desde `assets/og-template.html` (1200×630) |
| Logos y favicon | `brand/cxpress/assets/logos/` |

## Estilo del formulario

El embed es un iframe cross-origin, así que el CSS de la LP no lo alcanza. El CSS que le da
la cara de la marca está en
[`../oferta-webinar-clinicas-septiembre-2026/assets/jotform-custom-css.css`](../oferta-webinar-clinicas-septiembre-2026/assets/jotform-custom-css.css)
y se pega en el editor de Jotform. Como las dos LPs comparten el mismo formulario, pegarlo
una vez sirve para ambas.

## Cómo actualizar

`content.cxpress.io` está en `landing-pages/dominios/MIGRADOS.json`: editar el source, entrar
en el manifiesto y abrir PR. El CI deploya. Nunca `vercel deploy` a mano.
