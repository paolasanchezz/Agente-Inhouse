# buzz-digital-experience · Museo de las Conversaciones Perdidas

Idioma: ES-LATAM (México, tuteo). Marca: Buzzmonitor (naranja `#EB7C2E` + morado `#390155` + teal `#0E9D9B` como acento).
Tipografía: League Spartan 800 (títulos) + Lato 400 (apoyo), vía Google Fonts.

Dominio: `content.buzzmonitor.com/buzz-digital-experience` (guarda-chuva migrado al CI).
GTM: `GTM-MKQBX2MG` (contenedor LATAM).

## Preview local

```bash
python3 -m http.server 8123 --bind 127.0.0.1
```

Y abrir `http://127.0.0.1:8123/landing-pages/buzzmonitor/buzz-digital-experience/` desde la raíz del repo (los paths a `../../brand/` resuelven solos).

## Las 11 salas

| Sala | Qué pasa | Interacción |
|---|---|---|
| Portal | contadores subiendo + "¿Quieres escuchar?" | botón ENTRAR desbloquea el scroll |
| 01 La entrada | los comentarios invaden la pantalla hasta volverse ilegibles, silencio, RUIDO tachado → "Esto son oportunidades" | scroll (5 pantallas de recorrido) |
| 02 Elige qué ignorar | 5 puertas | la elección cambia la conversación de la sala 03 |
| 03 La conversación perdida | cronómetro 00:34 + comentarios entrando + sello DECISIÓN TOMADA | automática al entrar en vista |
| 04 Ahora elige tu marca | BUSCANDO / ANALIZANDO / DETECTANDO SEÑALES → "Encontramos algo" | campo de texto (el nombre se propaga a las salas 05, 06 y 07) |
| 05 El espejo | 3 insights (compra, frustración, comparación) | ninguna |
| 06 ¿Estás escuchando? | canvas con la marca al centro y 2.400 puntos agrupados por tema, zoom out | scroll |
| 07 El momento incómodo | barras tu marca vs competidor, los números se apagan, aparece la mención | campo de texto |
| 08 ¿Qué harías? | 4 opciones + respuesta, luego Detecta → Clasifica → Analiza → Prioriza → Acciona | clic |
| 09 Oportunidades perdidas | contador grande que nunca deja de subir, tickers tipo bolsa, tarjetas cayendo | scroll |
| 10 La revelación | logo + "México no necesita hablar más" + Escucha/Entiende/Decide/Actúa | scroll |
| 11 Salida | formulario con el recorrido de la persona resumido en chips | mock, no envía nada |

## Decisiones técnicas

- Una sola página con scroll narrativo (no multipágina): las animaciones encadenadas entre bloques al estilo Apple/Vercel dependen del scroll continuo. Si se quiere ruteo por sala, se puede partir después sin rehacer el diseño.
- Sonido sintetizado con WebAudio (sin archivos): notificaciones, sello, hallazgo. Apagado hasta que la persona lo activa (los navegadores bloquean el autoplay).
- `prefers-reduced-motion`: todo se muestra en estado final, sin movimiento.
- Sin JS: la página sigue siendo legible y scrolleable (nada de texto esperando animación).
- Formulario mock (`preventDefault`), pendiente de integrar con el form real cuando el diseño esté aprobado.

## Datos

Todo lo que se muestra es de muestra y está etiquetado como tal en pantalla: conversaciones reescritas a partir de patrones de monitoreo, volúmenes ilustrativos, comparación con cifras fijas. La sala 04 no consulta datos en vivo. Para conectar datos reales habría que definir el origen (preprocesado por categoría, consulta bajo demanda o corte manual antes de cada campaña).
