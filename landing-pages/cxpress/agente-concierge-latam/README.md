# LP Cxpress — agente-concierge-latam

**Gerado em:** 2026-08-31
**Origem:** adaptacao ES-LATAM da LP `landing-pages/cxpress/agente-concierge-pt` (copy e HTML)
**Copy-fonte:** `copy.txt` (traduzida/adaptada a partir de `agente-concierge-pt/copy.txt`)
**Idioma/regiao:** ES-LATAM (`es-419`) — GTM `GTM-WRQ47B9R`
**Dominio previsto:** `content.cxpress.io` (guarda-chuva migrado pro CI)

## Estrutura

HERO (foto full-bleed + scrim) · BENEFICIOS (grid 2x2, 4 cards) · PARA-QUEM (grid 2 col, 6 segmentos)
· RESULTADOS (3 stats, topo laranja) · CTA-FINAL (form Jotform em card branco sobre primaryDark) · FOOTER.
Sem secao de Urgencia (sem prazo real; GUIDELINES §9).

Diverge da LP PT-PT: **nao tem a secao PROBLEMA** e o bloco de BENEFICIOS tem 4 cards (nao 6).
O CSS e o resto da estrutura continuam identicos a `agente-concierge-pt`.

## O que mudou em relacao a LP PT-PT

| Item | PT-PT | ES-LATAM |
|---|---|---|
| `html lang` / `inLanguage` | `pt-PT` | `es-419` |
| GTM | `GTM-NW6V5KBM` | `GTM-WRQ47B9R` (padrao das LPs LATAM) |
| Jotform | `261904529617867` | `252398149653872` (form de demo ES, mesmo usado em `atencion-digital-latam`, `whatsapp-business-smb-latam`, `atencion-clinicas-latam`) |
| Home da marca (logo header/footer + JSON-LD) | `https://www.cxpress.pt` | `https://home.cxpress.io` (`brand-manifest.json` → `websites.latam`) |
| `og:locale` | `pt_PT` | `es_LA` (+ `og:locale:alternate` `pt_PT`) |
| OG image | `og-agente-concierge-pt.png` | `og-agente-concierge-latam.png` (regerada via `.claude/skills/lp-gerar/og-template.html` + Chrome headless, com o H1 novo) |
| Secao PROBLEMA | tem | removida |
| Cards de BENEFICIOS | 6 | 4 |
| hreflang | nao tinha | par reciproco `pt-PT` ⇄ `es-419`, `x-default` na PT |

**Tambem foi alterada a LP PT-PT:** adicionados os `hreflang` reciprocos e `og:locale:alternate`
em `agente-concierge-pt/index.html`. Sem hreflang dos dois lados o par de idiomas nao e reconhecido
pelo Google. Nenhuma outra linha da LP PT foi tocada.

## Pilares de copy aplicados (contrato do CLAUDE.md)

1. **Linguistico** — `conhecimento/linguistico/es-latam/padrao-linguistico.md`: tuteo (nunca voseo/vosotros),
   espanhol neutro sem regionalismo, `reporte` (nao `informe`), `celular` (nao `movil`),
   `equipo` (nao `equipa`), `clientes potenciales` (nao `leads`).
2. **Boas praticas** — `conhecimento/copywriting/fundamentos-copy.md` (H1 lidera pela dor).
3. **Anti-IA** — `conhecimento/editorial/regras-anti-ia.md` + Anexo ES-LATAM.
   Contagens no arquivo final: em-dash `—` = **0**; antitese-por-negacao = **0**; frases-tipo IA = **0**.

## Estado

- [x] Copy ES-LATAM (`copy.txt`)
- [x] HTML gerado (`index.html`)
- [x] Assets de foto copiados da LP PT (`hero-bg.png`, `problema-bg.png`)
- [x] OG image (1200x630) — `assets/og-agente-concierge-latam.png`
- [x] Formulario integrado — Jotform `252398149653872`
- [ ] Revisao — rodar `/lp-revisar cxpress/agente-concierge-latam`
- [ ] Publicado — **NAO publicada**. Falta entrada no `landing-pages/dominios/content-cxpress-io/manifest.json`
      e o fluxo CI da skill `/lp-publicar cxpress agente-concierge-latam content.cxpress.io`.
      Nao editar manifesto nem deployar a mao (CLAUDE.md, Regra Nº 1).

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-primary.svg` (header + footer)
- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `./assets/hero-bg.png` · `./assets/og-agente-concierge-latam.png`
  (`problema-bg.png` foi apagado junto com a secao PROBLEMA; segue existindo na LP PT-PT)

## Alteracoes a pedido do usuario (2026-08-31)

- **HERO** — H1 trocado para "Tu asistente personalizado de atención al cliente"; subheader para
  "Conecta con tu comunidad y transforma engagement en ventas con un agente automático para Instagram,
  WhatsApp y TikTok."; CTA do botao para "Agenda una demo". O CTA do header (nav) segue
  "Agenda una demostración gratuita".
- **PROBLEMA** — secao removida por completo (markup + CSS `.problem*` + asset `problema-bg.png`).
- **BENEFICIOS** — H2 para "Transforma conversaciones en más engagement y ventas"; os 6 cards antigos
  trocados pelos 4 novos. Grid passou de 3 colunas para 2 (`max-width:900px`, centrado): com 4 cards,
  3 colunas quebravam em 3+1.
- **CTA-FINAL** — H2 para "Transforma conversaciones en oportunidades de venta".
- **Ajustes de design decorrentes:** `.hero h1{max-width}` de 15ch para 20ch (o H1 novo e mais longo e
  quebrava em 4 linhas); OG image regerada com o H1 novo (fonte 72px -> 60px pra caber em 2 linhas).
- **SEO reescrito (2026-08-31)** — `<title>`, `meta description`, `og:`/`twitter:description`,
  `og:image:alt` e as descricoes do JSON-LD foram realinhados ao posicionamento novo
  (atencion al cliente + conversacion que vira venda, com Instagram/WhatsApp/TikTok como keywords).
  Tamanhos: title 54 chars, description 159, og:description 156 (GUIDELINES §15: ~150-160).
  Pacote SEO validado: 1 description, 11 `og:`, 4 `twitter:`, 1 JSON-LD.

## Rediseño (2026-08-31) — estilo ManyChat sobre marca Cxpress

Pedido: mantener clean + tipografia Cxpress, con titulos mas bold y una LP dinamica con animaciones.
El HTML fue reescrito por completo (estilos + cuerpo); el `<head>` (GTM, SEO, hreflang, JSON-LD,
favicon) se conservo **byte a byte** y la copy quedo **identica** (verificado linea por linea contra
`copy.txt`: 0 ausencias).

**Direccion visual**
- Tipografia de marca sin cambios: Open Sans (titulos), Source Sans 3 (cuerpo), Bitter (kickers en
  italica). Los titulos suben a **800** con `letter-spacing -0.022em` y `line-height 1.04` (el "bold"
  ManyChat), escala hasta 70px en el H1 y 86px en los numeros de resultados.
- Paleta reducida a 3 (GUIDELINES §1): **navy** (texto + seccion oscura), **royal** (CTA, acentos,
  numeros) y **naranja** solo como micro-acento (punto del eyebrow, barras alternas de PARA-QUIEN,
  puntos del ticker). Un solo gradiente activo (royal→lila en el borde superior de las cards).
- Formas decorativas canonicas del brandbook (pill) en el hero; fondos alternan blanco ↔ off-white,
  con una unica seccion oscura (CTA final + footer como bloque continuo).

**Animaciones** (§4: 2-3 momentos, nunca esconden texto)
1. Entrada del hero en cascada (CSS puro, `animation-delay` .06s→.46s) + subrayado que se "pinta"
   bajo "atención al cliente" (`background-size` animado, sobrevive al salto de linea).
2. Burbujas de chat flotando sobre la foto (`floaty`) con puntos de "escribiendo".
3. Ticker infinito de canales entre hero y contenido (pausa en hover; es la transicion visual del §2).
4. Scroll-reveal escalonado de cards y stats (IntersectionObserver).
5. Contador animado de los 3 numeros de resultados (el valor final ya esta en el HTML: si el JS falla,
   se lee igual). Sin `aria-live` (§7).
6. Micro-interacciones: hover de cards (lift + barra superior), de items de publico (desplazamiento),
   de CTA (lift + flecha), sombra del header al hacer scroll.

**Accesibilidad y robustez verificadas**
- `prefers-reduced-motion`: todas las animaciones e infinitos apagados, todo el texto visible.
- Sin JS: `<noscript>` deja `.reveal`/`.anim` en opacidad 1 (render verificado con JS desactivado).
- Sin overflow horizontal a 390px (`scrollWidth == clientWidth == 390`); solo el ticker excede, dentro
  de su `overflow:hidden`.
- Contraste AA: el kicker de los stats paso de naranja (2.4:1, reprobaba) a navy. Kicker de seccion
  royal sobre off-white = 4.85:1. Eyebrow navy sobre lila = ~10:1.
- Pisos tipograficos mobile del §20 respetados (H1 38, H2 30/31, card 22, cuerpo 17, nota 14).

**Decision que conviene revisar:** los CTA dejaron de ser **verde WhatsApp `#21CC78`** (heredado de la
LP PT-PT, elegido alli por ser una LP de WhatsApp) y pasaron al **royal `#4A69BD`** de marca.
Motivo: `brand/cxpress/generation-rules.json` lista el verde como color fuera de paleta
("pertenecen a otras marcas del grupo") y esta LP ya no es solo de WhatsApp. Volver al verde es
cambiar una variable CSS.

Version anterior del HTML guardada fuera del repo durante la sesion (no versionada).

### Ajustes posteriores al rediseño (2026-08-31, a pedido del usuario)

- **CTA de vuelta al verde WhatsApp `#21CC78`** (hover `#1AAE63`), como en la LP PT-PT, con **texto
  blanco**. El resto de la paleta sigue navy + royal + naranja como micro-acento.
  ⚠️ **Excepcion consciente de contraste (decision del usuario, 2026-08-31):** blanco sobre `#21CC78`
  da **2.1:1**, por debajo del 4.5:1 que exige GUIDELINES §7. Se propuso texto navy sobre el mismo
  verde (6.4:1) y el usuario pidio explicitamente blanco por armonia visual. Queda registrado aqui
  para que una futura `/lp-revisar` no lo trate como bug nuevo. Si algun dia se quiere cumplir AA sin
  perder el verde: texto navy, u oscurecer el verde a ~`#128C4A` manteniendo el texto blanco.
- **Quitado el párrafo bajo el título del bloque del form** ("Una marca que responde es una marca que
  se acerca..."), en `index.html` y en `copy.txt`. El H2 pasa directo al formulario.

**Formulario en uso:** Jotform **`252398149653872`** = *"Conversión Cxpress LATAM"*, el mismo form de
demo que usan las otras 7 LPs LATAM de Cxpress (`atencion-digital-latam`, `atencion-clinicas-latam`,
`whatsapp-business-smb-latam`, `banimento-whatsapp-latam`, `coex-whatsapp-latam`, `sector-it-latam`,
`sector-marketing-latam`). Campos: Nombre, E-mail Comercial, Empresa, País, Teléfono y checkbox de
"No deseo recibir Newsletter". Vino heredado de la adaptación (la LP PT-PT usa el form PT
`261904529617867`).

### Carrusel de canales -> logos de clientes (2026-08-31, a pedido del usuario)

El marquee que antes listaba canales y funcionalidades ("Instagram · Comentarios · WhatsApp ·
Mensajes directos · TikTok · Preguntas frecuentes · Intención de compra") pasa a ser una **barra de
prova social con logos de clientes reales de Cxpress**, en linea con el componente
"barra de prova social (logos de clientes)" de `brand/cxpress/generation-rules.json`.

**De donde salieron los logos:** de `brand/cxpress/assets/plataforma/clientes-cxpress.png` (1886x906,
el mural oficial de 42 clientes que ya usan las LPs hermanas LATAM). Como el asset es una sola imagen
en rejilla y el marquee necesita piezas sueltas, se segmento por espacios en blanco reales (bandas de
fila + cortes por hueco horizontal >= 38px, no rejilla fija: la rejilla fija cortaba logos) y se
normalizo cada logo a 88px de alto. Resultado: `assets/clientes/cliente-01..42.png` (531 KB en total).
**Se versionan solo los 14 usados** (~100 KB). Os outros 28 do mural ja vivem em
`landing-pages/cxpress/whatsapp-business/assets/clientes/` (set completo, mesma numeracao) — pra
trocar um logo, copiar de la o `cliente-NN.png` correspondente.

**Seleccion en pantalla (2026-08-31, criterio del usuario: priorizar clientes con presencia fuera de
Brasil):** 14 logos, en este orden de aparicion. Primero los de alcance internacional o regional:
Thermo Fisher Scientific, Sephora, Smart Fit, Diversey, J&T Express, Ticket (grupo Edenred), Advanta
y Pagsmile. Despues, marcas grandes reconocibles en la region: Vivo, Cacau Show, Koin, Oi, Eletrobras
y Mondial. Se sacaron de la barra las mas locales de la seleccion anterior (Catavento, Uniclube, adib,
Galeria Pagé Brás, Polenghi, Salon Line).

⚠️ **La clasificacion "tiene presencia fuera de Brasil" es lectura del agente sobre cada marca, no un
dato del repo.** El mural de `brand/` no dice en que paises esta contratado cada cliente. Conviene que
alguien de Cxpress lo confirme antes de publicar: puede haber clientes con contrato solo BR en la
lista, o clientes LATAM que quedaron fuera. Cambiar cualquiera = cambiar el numero de archivo en el
`<img>` (los 42 siguen en `assets/clientes/`).

**Tratamiento visual:** grayscale + `opacity .85`, color completo al pasar el mouse (que ademas pausa
el scroll). Sin el grayscale, 19 logos a todo color pelean con la paleta de la LP (GUIDELINES §1).

**Copy anadida:** label de la barra. Primero se uso "Más de 800 clientes en Brasil, Latam y Portugal"
(literal de la LP hermana `whatsapp-business-smb-latam`); el usuario lo cambio el 2026-08-31 por
**"Más de 800 agencias y empresas confían en nosotros"**. El label vive en `copy.txt` bajo el bloque
`=== CLIENTES ===` (se agrego ahi para que la copy siga siendo la fuente de verdad, no el HTML).
Mantiene el mismo numero (800) del claim ya publicado; cambia el encuadre de origen geografico a
tipo de cliente.

**A11y:** la primera fila lleva `alt` con el nombre de cada cliente; la fila duplicada (la que existe
solo para que el loop sea continuo) va con `alt=""` y `aria-hidden="true"`, para no repetir 19 nombres
al lector de pantalla. Con `prefers-reduced-motion` el marquee se detiene.

### Correcao pre-publicacao: colisao de assets de clientes (2026-08-31)

Ao validar o build contra a `main` atual (nao contra a base local, que estava 27 commits atras),
apareceu uma **colisao real**: as LPs `whatsapp-business`, `banimento-de-whatsapp` e
`evite-banimento-whatsapp` **ja publicam** `assets/clientes/cliente-01..42.png` no mesmo dominio, e
o `build_umbrella.py` resolve todas para o mesmo destino (`dist/assets/cxpress/clientes/cliente-NN.png`,
primeiro que escreve ganha). Os arquivos recortados nesta sessao tinham o mesmo nome e **bytes
diferentes** (recorte/resize proprios), entao o deploy trocaria os logos de uma LP ou de outra
dependendo da ordem do build.

**Correcao:** descartar os recortes proprios e **reusar o set ja publicado** (copiado de
`landing-pages/cxpress/whatsapp-business/assets/clientes/`). Verificado: os 42 arquivos ficaram
byte-a-byte identicos aos das outras 3 LPs (colisao vira no-op) e a numeracao bate com a que a barra
referencia (conferidos um a um os 14 logos usados contra o `alt` de cada `<img>`). Peso: 300 KB.

Licao pro futuro: a numeracao `cliente-NN` do mural `brand/cxpress/assets/plataforma/clientes-cxpress.png`
ja e convencao no repo. Antes de recortar de novo, checar se outra LP ja tem o set.

## Rediseño v3 — "editorial Cxpress" (2026-09-01)

Pedido: look mas moderno y dinamico, sin salir de las directrices Cxpress, que no se sienta generico.
Copy intacta (verificada linea por linea contra `copy.txt`: 0 ausencias) y `<head>` intacto.

**Lo que lo saca de generico, usando activos de marca que estaban sin usar**
- **La mascota Samir** (`brand/cxpress/assets/mascot/samir-laptop.png`, con headset y laptop) protagoniza
  la tarjeta destacada de beneficios. Optimizada a 620px / 300 KB en `assets/samir-laptop.png` (el
  original pesa 2,1 MB).
- **Arco canonico del brandbook** (`border-radius: 9999px 9999px 0 0`) enmarcando la foto del hero,
  sobre un pedestal en pildora. Es literal la regla "emoldurar fotos de pessoas dentro de arcos" de
  `generation-rules.json`, que ninguna version anterior aplicaba.
- **Bitter en cursiva** (la fuente de personalidad de la marca) para kickers de seccion y numeracion.
  Antes solo se usaban Open Sans + Source Sans.
- **Composicion de pildora + anillo + punto** con parallax en el hero (formas canonicas, max 5).
- **Borde superior en arco** en la seccion final navy, en vez de una banda plana.

**Cambios de estructura**
- Beneficios pasan de 4 tarjetas iguales a **bento**: una destacada a todo el ancho (con la mascota) y
  tres normales, numeradas 01-04.
- Publico pasa de rejilla de pildoras a **lista editorial** con numeracion y linea que se dibuja en hover.
- Resultados pasan a numeros sobredimensionados (hasta 96px) separados por reglas verticales.
- Barra de clientes: el label pasa a la izquierda, en Bitter, con el marquee a la derecha.

**Verificado**
- Sin overflow horizontal a 390px (`scrollWidth == clientWidth == 390`); las formas que sobresalen
  viven dentro de secciones con `overflow:hidden`.
- `prefers-reduced-motion`: parallax, marquee, pulso, flotacion y reveals apagados.
- Sin JS: render completo (noscript deja `.reveal`/`.anim` visibles).
- Build del guarda-chuva: exit 0, mascota copiada al dist, 0 placeholders, 0 paths relativos.
- Gate GTM: 0 bloqueios.

**Contraste (regresion propia, detectada y corregida):** primero puse los numeros 01-04, el "Hasta" y
la numeracion de publico en naranja `#EF863C`, que sobre blanco da **2.5:1** y reprueba AA. Pasaron a
royal `#4A69BD` (4.85-5.2:1). El naranja queda solo en decoracion sin texto: la regla del kicker, el
punto del eyebrow, el anillo y el punto del hero.

**Sigue en pie la excepcion consciente:** CTA verde `#21CC78` con texto blanco (2.1:1), decision del
usuario documentada arriba.

### Correccion del hero (2026-09-01, reportada por el usuario)

El usuario vio "una sombra rara sobre la chica del sueter naranja" y la imagen "un poco extraña".
Dos causas distintas:

1. **La sombra era mia:** `.arcframe::after` pintaba un degradado navy (`rgba(35,41,96,.34)`) sobre el
   tercio inferior de la foto, para dar contraste a la burbuja de abajo. Como esa persona esta
   justo en esa banda, parecia suciedad sobre el sueter. **Eliminado** (la burbuja inferior ya tiene
   fondo navy propio, no necesitaba el degradado).
2. **El arco no se leia:** `hero-bg.png` no es foto a sangre, es una composicion sobre fondo claro
   con adornos propios. Enmarcarla hacia que la silueta del arco desapareciera contra el blanco y que
   el pill lila de atras pareciera la forma principal ("tarjeta dentro de tarjeta"). Se probo dejar la
   imagen suelta sin marco: peor, porque quedan a la vista sus bordes rectos y los adornos cortados.
   **Solucion:** arco como moldura preenchida en lila (rim de 18px) que recorta la imagen y esconde sus
   bordes, con `object-position:56% 54%` para centrar al grupo. Se quito el pill de fondo que competia.

Regla que queda: esta imagen **necesita recorte**; no funciona suelta.

### Hero: la foto sale, entra Samir (2026-09-01)

El usuario reporto "una marca extraña justo en la cara de la chica del sueter naranja". Se verifico a
resolucion completa **en el archivo original**: `hero-bg.png` tiene la cara de esa persona deformada
(la zona del ojo es un borron, artefacto tipico de imagen generada). No es CSS: se probo reencuadrar
mas ancho y correrla al borde, y el defecto sigue visible; sacarla del todo desbalancea la composicion.

**El defecto ya estaba publicado**: la version en el aire de esta LP y, sobre todo, la LP hermana
`agente-concierge-pt`, que usa la misma imagen a sangre completa (mismo md5).

**Decision del usuario:** reemplazar la foto por la mascota. El hero ahora lleva `samir-hero.png`
(recorte de `brand/cxpress/assets/mascot/samir-dashboard.png`, con headset y tablero de resultados,
760px / 449 KB) dentro del arco canonico, con un halo circular blanco detras y las burbujas de chat
encima. La tarjeta destacada de beneficios mantiene `samir-laptop.png`: son dos poses distintas en
contextos distintos, no repeticion.

`hero-bg.png` fue **eliminado de esta LP** (ya no se referencia). Sigue existiendo en
`landing-pages/cxpress/agente-concierge-pt/assets/`.

**Pendiente para el Victor:** decidir que hacer con la LP PT-PT, que sigue mostrando esa cara a tamano
completo en produccion.

### Vuelta a la foto en el hero (2026-09-01, decision del usuario)

Tras ver las dos versiones, el usuario pidio volver a la foto. El hero usa de nuevo `hero-bg.png`
dentro del arco (moldura lila de 18px, `object-position:56% 54%`), **sin** el degradado navy que
provocaba la "sombra" sobre una de las personas. `samir-hero.png` fue eliminado; la mascota sigue
solo en la tarjeta destacada de beneficios (`samir-laptop.png`).

**Queda en pie, conscientemente:** la cara deformada de una de las personas de `hero-bg.png` (ver
seccion anterior). Es la misma imagen que ya esta publicada aqui y en `agente-concierge-pt`. Si algun
dia hay una foto de reemplazo, se cambia el archivo y no hace falta tocar el CSS.

### Imagen del hero definitiva: sin caras (2026-09-01)

El usuario pidio una replica corregida de `hero-bg.png`. **No se pudo:** a resolucion nativa el ojo
no esta danado, esta **ausente** (piel lisa donde deberia ir el ojo). No hay informacion que
recuperar, asi que no seria retoque sino dibujar una cara humana que no existe, en una imagen que se
presenta como foto de una persona real. Ademas, el unico conector de imagen disponible (Arcads)
requiere autorizacion que no se puede completar en sesion no interactiva. Tampoco existe en el repo
una version mejor de esa composicion (solo 2 copias identicas de 1672x941).

**Decision del usuario:** reemplazar por una imagen del mismo estilo **sin caras humanas**.
Se reuso `agente-concierge-pt/assets/problema-bg.png` (celular sobre escritorio con burbujas de chat
y notificaciones flotando), material ya aprobado y publicado. Copiado a
`assets/hero-conversaciones.png`, redimensionado a 1100px / 594 KB.

Encuadre final: `object-position:66% 50%`, con la burbuja del agente en `bottom:11%; right:-15%` para
que quede a la altura del celular y no lo tape. Lectura resultante: entra el comentario (burbuja
blanca arriba) y el agente responde (burbuja navy junto al celular).

`hero-bg.png` fue **eliminado de esta LP**. Sigue en `agente-concierge-pt/assets/`, que continua
publicando esa cara a sangre completa: **pendiente de decidir con el Victor**.

### Hero: key visual proprio no lugar da foto (2026-09-01)

O usuario pediu um visual "mais atrativo" pro header. A foto saiu; entrou uma **peca desenhada**
(`assets/hero-kv.png`, 2000×2200), gerada em HTML/CSS + Chrome headless — a engine padrao das
`criativos/GUIDELINES.md` §3. Fonte editavel e instrucoes de re-render em
`criativos/cxpress/latam/hero-agente-concierge/` (gitignored, como todo output de criativo).

**O que a peca mostra:** comentario publico do Instagram (cartao flutuante) -> telefone com a
resposta do agente e o chip "Respuesta automática" -> quick replies. Profundidade por perspectiva
3D, glow radial e sombras em camadas; pilulas canonicas e grid de pontos como atmosfera.

**Licao de escala:** a 1a versao foi desenhada como cena completa (post + no + DM) num canvas de
1400px com texto 16px. No hero ela aparece a **~452px**: virava miniatura ilegivel. Refeita com
menos elementos e o dobro de escala. Regra: desenhar no tamanho em que a peca vai ser vista.

**Zona segura do arco:** o hero mascara a imagem num semicirculo, entao o terco superior e estreito.
Num canvas 1000×1100 (raio 500), a y=132 so aparece x de 161 a 838. O cartao de comentario estava em
`left:40px` e perdia ~120px pela esquerda (o usuario reportou o texto cortado); corrigido para
`left:192px; top:176px`. A conta e a tabela ficaram no README do criativo.

**Consequencias no HTML:** as duas burbulhas de chat em HTML sobre o arco foram **removidas** (a
imagem ja conta a conversa; as duas coisas competiam), junto com o CSS `.bubble*`/`.dots` que virou
morto. `hero-conversaciones.png` saiu (sem uso).

