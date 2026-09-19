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

### Redes sociais LATAM no rodape (2026-09-01)

Adicionados Facebook, Instagram e LinkedIn no rodape (URLs fornecidas pelo usuario), reusando
**o mesmo padrao de icones e aria-labels** da LP irma `webinar-clinicas-latam`, que ja publica
exatamente essas tres URLs. Alvo `_blank` + `rel="noopener"`, area de toque 40×40 e contraste
lilas sobre navy (hover inverte pra branco).

- Facebook: `https://www.facebook.com/profile.php?id=61584681389155`
- Instagram: `https://www.instagram.com/cxpress.es/`
- LinkedIn: `https://www.linkedin.com/company/cxpress/`

**Tambem preenchido o `sameAs` do JSON-LD** (`Organization`), que estava vazio — GUIDELINES §15 pede
LinkedIn + Instagram regional ali, e a ausencia estava documentada como pendencia desde a LP PT-PT.

**Nao incluido:** a `webinar-clinicas-latam` linka tambem um YouTube (`@Cxpress_es`). Como o pedido
listou so as tres redes acima, o YouTube ficou de fora — e um `<a>` a mais se quiserem.

**Fonte de verdade:** o `brand/cxpress/brand-manifest.json` ainda nao tem bloco de redes (so
`brand.websites`), entao as URLs seguem no HTML da LP. Migrar isso pro manifesto evitaria que a
proxima LP as hardcode de novo.


### Samir animado no hero (2026-09-15)

Pedido do usuario: por o Samir dentro da cena de mensagens do hero, digitando no laptop como se
estivesse respondendo cada mensagem que chega — animacao 3D, em loop que nao pareca loop, fluida a
ponto de parecer video.

**Como foi feito (e por que nao e video).** Nao ha nesta sessao nenhum gerador de imagem/video
disponivel (o unico conector, Arcads, exige autorizacao que so se completa em sessao interativa), e o
BRANDBOOK §mascote proibe redesenhar o Samir em outro estilo — so os renders oficiais valem. Entao a
animacao **nao desenha nada novo**: ela recorta o render oficial
`brand/cxpress/assets/mascot/samir-laptop.png` (que ja e 3D, ja tem o hoodie azul-marinho com o logo
Cxpress e ja esta digitando num laptop) em 7 camadas e anima cada uma so por `transform`. Roda na GPU,
na taxa de atualizacao do monitor — na pratica mais fluido que video, e sem nenhum `<video>`.

**Camadas** (`assets/samir/`, 7 WebP, 104 KB no total — menos que os 300 KB do PNG unico anterior):
`tail` · `body` · `head` (+ `lid-l`, `lid-r`, as palpebras) · `hand-l` · `hand-r`.

**Regra que faz as emendas sumirem:** cada camada copiada so se desloca **para baixo** a partir do
repouso, e todos os cortes caem em area escura (manga do hoodie, gola). Descer expoe o topo da
copia — que e a mesma arte que esta por baixo, entao nao se ve nada. Corpo e cabeca sao a excecao:
sao complementares com 14px de sobreposicao, para nao duplicar a silhueta da orelha contra o fundo
branco (foi exatamente esse o bug da 1a versao).

**Movimentos e duracoes** — respiracao 5,5s · rabo 7,3s · cabeca 6,7s · mao esquerda 2,9s · mao
direita 3,7s · piscada 6,1s. As duracoes sao **primas entre si de proposito**: a combinacao das 6 so
se repete depois de horas, entao o olho nao acha o ponto de emenda do loop. As duas maos batem em
fases opostas e com amplitudes diferentes a cada tecla, o que e o que faz ler como digitacao e nao
como um sobe-e-desce mecanico.

**Piscada:** uma faixa da pele acima de cada olho, esticada em `scaleY` (~4,8x) por ~230ms. As
palpebras sao filhas do mesmo wrapper que carrega o transform da cabeca (`.samir__face`), senao
descolariam do olho quando a cabeca baixa.

**Tratamento do render antes de cortar** (script de matting proprio, PIL+numpy, no scratchpad):
- Fundo marrom removido com modelo polinomial de 2 regioes (parede e o plano da mesa tem gradientes
  diferentes; um modelo so nao fecha) + flood fill + descontaminacao de cor nas bordas.
- As duas orelhas precisaram de fechamento morfologico localizado: a pele interna delas tem
  praticamente a mesma cor do fundo marrom, e o flood fill vazava para dentro.
- **Logo da Apple removida da tampa** do laptop (marca de terceiro numa pagina comercial), repintada
  com o proprio gradiente da tampa, com feather para nao deixar emenda.

**Onde entrou:** `.kvscene` (novo wrapper) segura o cartao da cena e o Samir logo abaixo, encostando
no rodape do cartao. O cartao perdeu `max-width`/`margin-inline` (foram pro `.kvscene`).

**A tarjeta destacada de beneficios** passou a usar `assets/samir/samir-laptop.webp` — o mesmo recorte
limpo, estatico, 39 KB (era `assets/samir-laptop.png`, 300 KB, ainda com a logo da Apple). O PNG foi
removido.

**Verificado:** 0 overflow horizontal em 390/414/768/1024/1280/1536 · 0 erro de console · todas as 7
camadas carregam · `prefers-reduced-motion` desliga tudo e deixa o Samir **visivel** em pose de
repouso · `check_gtm_region`: 1 OK, 0 bloqueio.

**Em aberto (decisao do usuario):**
- A tampa do laptop e marrom-bronze no render oficial (ela reflete o fundo marrom do render original).
  Da pra neutralizar pra cinza, mas e mexer no render de marca — nao foi feito sem pedir.
- O Samir aparece agora em dois lugares da pagina (hero animado + cartao de beneficios), na mesma pose.
  Se incomodar, o cartao de beneficios pode trocar pra `samir-dashboard.png` (outra pose oficial).
- `assets/hero-kv.webp` ficou sem uso desde que a cena do hero virou HTML/CSS (PR #465-467). Nao foi
  removido aqui pra nao misturar com esta entrega.

### Samir v2: recorte refeito e coreografia amarrada a mensagem (2026-09-15)

Retorno do usuario sobre a v1: (a) "sombra estranha embaixo das maos, como recorte mal feito",
(b) recorte do fone, (c) cauda e orelhas "com pedacos faltando", (d) o movimento devia ser mais
evidente quando chega mensagem — esperar a mensagem pra comecar a responder —, (e) a resposta devia
parecer que esta sendo escrita enquanto ele digita, e (f) uma pausa nas maos depois, piscando na
espera.

**Recorte — as 3 causas.** Todas eram do matting da v1, nao do HTML:
1. **Sombra sob as maos** = o filtro que apagava a mesa (`res_table<110` abaixo do horizonte) estava
   comendo tambem o **deck do teclado**, porque o chanfro claro de aluminio tem a mesma cor da mesa.
   O laptop ficava cortado numa reta e as maos pareciam flutuar. **Correcao:** a mesa agora sai por
   uma **linha tracada a mao** (`DESK`, 26 pontos) que segue a base real do laptop e das maos. Essa
   linha tambem serve de **barreira do flood fill** — sem isso ele entra pela mesa e sobe pelo
   chanfro. Regra que ficou: mesa marrom e tampa marrom do laptop nao se separam por cor; ali o corte
   e manual, ponto.
2. **Orelhas** = a v1 rescatava a orelha com fechamento morfologico limitado a uma **caixa
   retangular**; a caixa deixava degraus retos exatamente onde a orelha encostava nela. **Correcao:**
   cada orelha agora tem uma **silhueta tracada a mao** (`EAR_L` 17 pontos, `EAR_R` 11), feather 3,2px.
   A pele interna da orelha tem a mesma cor do fundo marrom — nenhum criterio automatico separa as duas.
3. **Cauda e fone "com pedacos faltando"** = um passo de *despeckle* (`MinFilter(5)+MaxFilter(5)`
   seguido de `MaxFilter(7)`) que remodelava a silhueta e deixava degraus de ~5px nos aneis claros da
   cauda e no arco do fone. **Correcao:** removido. No lugar, so descarte de **componentes conexos**
   pequenos (<4000px), que nao mexe na forma do que fica. Rampa de alpha tambem mais suave
   (40→98 virou 32→95), o que devolve pelo fino.

Tambem: banda do horizonte alargada (±10 → ±26px) pra matar um fio de mesa de 1px, e o retangulo do
render inserido em 4px pra matar a linha da borda.

**Coreografia — o ciclo passou de 12s a 28s (7s por mensagem).** Dentro de cada batida:

| t | o que acontece |
|---|---|
| 0,4s | chega o comentario (a rede ativa troca junto) |
| 1,0s | abre a linha da resposta com o "digitando" (tres pontos) |
| 1,2s | **o Samir comeca a teclar** |
| 1,75 / 2,3 / 2,9s | o texto da resposta **se escreve em 3 blocos**, no ritmo das maos |
| 3,45s | entra o selo "Respuesta automática" |
| 3,5s | **as maos param** |
| 4,1s | entra o "Mensaje directo enviado" |
| 4,1 → 7,0s | **espera**: maos paradas, mas ele continua respirando, mexendo a cabeca, a cauda e piscando |

O texto em blocos e so markup: cada resposta virou `<i>` por trecho, com 3 keyframes (`twA/twB/twC`)
num ciclo de **7s** — e 28 = 4×7, entao os blocos ficam sempre em fase com a batida da variante
visivel, sem precisar de delay por variante.

**O que sincroniza e o que nao.** So **as maos** entraram na batida de 7s — e o que o usuario pediu.
Respiracao (6,5s), cauda (9,1s), cabeca (8,3s) e piscada (5,9s) seguem livres e com duracoes primas
entre si; se tudo sincronizasse, a pagina inteira viraria um loop de 7s obvio. Amplitude das teclas
subiu ~40% (ate 8,4px na fonte) pra o movimento ficar visivel no tamanho em que a peca aparece.

**Bug pego na verificacao:** existiam **duas** `@keyframes smTapR` no arquivo (a nova e a da v1); a
antiga vencia por vir depois, e a mao direita nunca parava. So apareceu porque a checagem foi feita
lendo o `transform` computado a cada 0,2s do ciclo, nao a olho. Ficou como metodo: conferir
coreografia medindo, nao olhando.

**Verificado de novo:** 0 overflow em 390/414/768/1024/1280/1536 · 0 erro de console · em
`prefers-reduced-motion` o cartao mostra a 1a variante **completa** (comentario + resposta inteira +
selo + DM, sem os pontos de "digitando") e o Samir fica visivel parado.

### Samir v3: maos recortadas pela silhueta (2026-09-17)

Retorno do usuario: "se sigue viendo que bajan sus manos con un pedazo de la laptop".

**Causa:** as camadas `hand-l`/`hand-r` eram recortadas por **caixa retangular**
(`ramp(xx,600,614)*(1-ramp(xx,876,890))*...`). A caixa da mao esquerda incluia uns 90x60px do
**deck do teclado**, e a da direita um pedaco da tampa — entao a cada tecla o laptop descia junto.
A v2 arrumou o recorte *estatico* do laptop (a "sombra" sob as maos), mas nao o das camadas que se
movem; sao dois cortes diferentes e so o primeiro tinha sido refeito.

**Correcao:** cada mao agora tem **silhueta tracada a mao** (`HAND_L` 21 pontos, `HAND_R` 13),
feather 2,4px, com uma regra de forma:
- **topo** entra uns 30px pra dentro da manga escura do hoodie — como a camada so desce, o que fica
  exposto no topo e escuro sobre escuro, e a emenda nao aparece;
- **laterais e base** seguem o contorno real dos dedos e do polegar, encostando no deck sem invadi-lo;
- a borda direita da mao direita acompanha a **aresta da tampa** (que de fato oclui os dedos), 1-2px
  pra dentro.

Resultado: o laptop fica parado, so as maos descem, e os dedos afundam na tecla. Conferido em
repouso / +4px / +7px, e na pagina nos instantes 1,00 / 2,05 / 2,35 / 2,85 / 5,00s da batida.

**Nota de manutencao:** o scratchpad da sessao anterior tinha sido limpo, entao o pipeline de matting
foi reconstruido a partir desta documentacao (mesmo `subject frac` = 0,575, o que confirma a
reproducao). Vale manter os poligonos e parametros aqui: e o unico lugar onde eles sobrevivem.

**Verificado:** 0 overflow em 390/414/768/1024/1280/1536 · sem 404 alem dos logos de marca (que
resolvem na raiz do guarda-chuva, nao no preview local) · as 7 camadas carregam · `prefers-reduced-motion`
desliga tudo e deixa Samir visivel e o cartao com a 1a variante completa.

### Samir v4: cena refeita — os cartoes saem da laptop (2026-09-17)

Pedido do usuario: refazer a animacao do zero, mais fluida, Samir maior, e que **as mensagens e as
respostas parecam sair da laptop**.

**Antes de refazer, o diff.** O usuario relatou de novo que "baixan las manos con un pedazo de la
laptop". Rodei um diff pixel-a-pixel entre o composite em repouso e com as maos a +7px: 26.266 px
mudam, todos dentro da bbox das maos — a tampa e o deck ficam identicos. O recorte da v3 estava
certo; o que faltava era a **cena**, nao o recorte. Fica como metodo: antes de refazer, medir.

**O que saiu.** O cartao grande (`.kvframe`) com a simulacao de feed inteira — barra de redes, post,
preview do formato nativo, comentario, resposta e cartao de DM. Junto foram 121 linhas de CSS
(`.cc__*`, `.sw`, `.mk`, `.cv`) e 5 keyframes (`netOn`, `ctxOn`, `swPergunta/Resposta/Acao`).
0 seletores orfaos depois (conferido).

**O que entrou.** Uma faixa livre em cima (`.kvband`) e o Samir embaixo, **maior**: a cena passou de
452px para 520px de largura e ele ocupa 100% dela (antes 92% de 452 = 416px — +25%). Na faixa pousam
dois cartoes que **nascem na borda de cima da tampa** (`translate(var(--fx),var(--fy)) scale(.42)`)
e sobem ate o lugar, crescendo. Um brilho radial (`.kvglow`) pulsa na tampa a cada cartao que sai.

**Decisao de profundidade (errei primeiro).** Comecei com os cartoes **na frente** do Samir pra o
percurso ficar todo visivel — e eles passavam por cima da cara dele, horrivel. Voltaram pra **tras**
(`z-index:1`): nascem escondidos pela tampa, sobem por tras da cabeca e aparecem quando a limpam.
A oclusao **e** o efeito — e o que faz parecer que sai de dentro. O que estava errado nao era a
profundidade, era a curva: `cubic-bezier(.16,.84,.3,1)` chegava a 60% do caminho no primeiro quarto
do tempo, entao o percurso nao dava pra ler. Agora e `cubic-bezier(.45,.03,.28,1)` e a saida dura
1,15s em vez de 0,75s.

**Fluidez das teclas.** Os keyframes de `smTapL/R` agora sao gerados (script no scratchpad) com
**curva por keyframe**: ataque `cubic-bezier(.35,0,.75,.4)` e solta `cubic-bezier(.15,.7,.35,1)` —
o movimento tem peso, em vez do `linear` de antes. Sete teclas por mao, alternadas, entre 17,1% e
60,7% do ciclo de 7s.

**Cronometragem (batida de 7s, ciclo de 28s = 4 mensagens):**

| t | o que acontece |
|---|---|
| 0,30s | o comentario sai da tampa e comeca a subir |
| 1,20s | **o Samir comeca a teclar** |
| 1,25s | a resposta sai da tampa |
| 1,45 / 2,30s | os dois cartoes pousam (a resposta com "digitando") |
| 2,75 / 3,25 / 3,75s | o texto da resposta **se escreve em 3 blocos** |
| 4,05s | o selo "Respuesta automática" |
| 4,25s | **as maos param** |
| 4,25 → 6,05s | espera: maos paradas, mas respira, mexe cabeca/cauda e pisca |
| 6,05 → 6,80s | os dois cartoes sobem e somem |

Conferido medindo o `transform` das maos a cada 0,2s: teclam de 1,2s a 4,3s, param de 4,4s a 7,0s,
e nunca as duas ao mesmo tempo.

**So as maos sincronizam** com a batida. Respiracao (6,5s), cauda (9,1s), cabeca (8,3s) e piscada
(5,9s) seguem livres e primas entre si.

**Verificado:** 0 overflow em 390/414/768/1024/1280/1536 · 0 seletor orfao · as 7 camadas carregam ·
`prefers-reduced-motion` vira um still (1a variante, conversa completa, sem os pontos de digitando) e
o Samir fica visivel parado.

### Samir v5: laptop de frente, ele por tras (2026-09-17)

Pedido do usuario: por a laptop **de frente**, com o Samir aparecendo por tras dela — como se ve uma
pessoa sentada atras do computador, tapada do peito pra baixo. Sem dedos a vista: a digitacao passa a
ser sugerida pelo **balanco dos ombros**. As mensagens vao **ao lado** da laptop. E o balanco comeca
no mesmo instante em que a resposta aparece.

**Por que isso resolve de vez o bug das maos.** Nao ha mais camada de mao. O que o usuario via
("baja las manos con un pedazo de la computadora") so podia existir enquanto houvesse um recorte de
mao se movendo sobre o teclado. Nesta composicao as maos ficam atras da tampa e nunca sao desenhadas.

**Camadas novas** (`assets/samir/`, 4 WebP, 124 KB): `tail`, `torso` (cabeca + ombros, uma peca so),
`lid-l`, `lid-r` (palpebras). Sairam `body`, `head`, `hand-l`, `hand-r`. O recorte foi cortado em
source y=760 (nada abaixo aparece) e o **corte cauda/tronco desceu de x=425 para x=360**: em 425 um
pedaco da orelha esquerda ficava dentro da camada da cauda e girava junto com ela — era parte do que o
usuario via como "recorte em excesso nas orelhas".

**A laptop original do render foi removida** da camada `torso` (corte reto em y=618, so de x=892 pra
direita). Sem isso, o marrom dela espiava por cima da tampa nova. A tampa nova comeca exatamente em
y=618, entao a emenda nunca aparece. De quebra, some a tampa marrom-bronze que estava em aberto desde
a v1.

**A laptop e desenhada em CSS** (`.lap`): tampa com `aspect-ratio:16/8.1` e `clip-path` afunilado
(vista de um ponto um pouco acima), dobradica e base com perspectiva invertida (mais larga na frente).
A dobradica e o que faz a peca ler como laptop — sem ela parecia um monitor.

**Balanco de escritura** (`smType`, gerado por script, curva por keyframe): rotacao de +-0,95deg com
pivo em `50% 22%` (no meio da cabeca), entao a cabeca fica quase parada e sao os ombros que balancam —
o oposto de um pivo embaixo, que faria a cabeca varrer. Sete ciclos entre 1,30s e 4,05s da batida.

**Cronometragem (batida de 7s, ciclo de 28s):**

| t | o que acontece |
|---|---|
| 0,35s | a pergunta sai de tras da tampa e desliza pro lado |
| **1,30s** | a resposta aparece **e o balanco comeca no mesmo instante** (pedido do usuario) |
| 1,95s | a resposta pousa, com "digitando" |
| 2,55 / 3,05 / 3,55s | o texto se escreve em 3 blocos |
| 3,90s | o selo "Respuesta automática" |
| 4,05s | o balanco para |
| ate 6,05s | espera: parado, mas respirando, mexendo a cauda e piscando |
| 6,05 → 6,80s | os dois cartoes recolhem |

Conferido medindo a rotacao de `.samir__up` a cada 0,2s: balanca de 1,3s a 4,1s e fica exatamente em
0deg de 4,2s a 7,0s.

**Layout:** a coluna da arte cresceu (`grid-template-columns` de `1.05fr .95fr` para `1fr 1.1fr`) pra
caber laptop + mensagens lado a lado. Abaixo de 640px nao cabe: a cena **empilha** (mensagens em cima,
ele embaixo) e os cartoes passam a subir em vez de deslizar.

**Verificado:** 0 overflow em 390/414/768/1024/1280/1536 · 0 seletor orfao · as 4 camadas carregam ·
`prefers-reduced-motion` vira um still com a conversa completa e o Samir parado e visivel.

### Samir v6: volta a cena da v4, mas animando os DEDOS (2026-09-17)

A v5 (laptop de frente) foi descartada pelo usuario. Voltou a cena da v4 — Samir grande, cartoes
saindo da tampa — com uma mudanca: **em vez das maos, animam so os dedos.**

**Por que isso fecha o problema.** Nas v3/v4 a camada que se movia era a mao inteira, e junto dela
iam a manga e a faixa do teclado onde os dedos encostam. Mesmo com a silhueta tracada a mao, havia
sempre pixel de laptop dentro do retangulo que se deslocava. Agora a camada e **so pele de dedo**.

**Como a mascara e feita (nao e poligono chutado).** A pele sai da propria imagem —
`alpha>0.6 & R>140 & (R-B)>42 & R>G` — recortada na regiao das maos e cortada na **linha dos nos**
(uma reta por mao). Depois divide em 4 grupos: 2 na mao esquerda (separados por uma diagonal entre os
dedos) e 2 na direita. A mao direita ainda leva um `x<984` explicito: a tampa marrom do laptop passa
no teste de pele, e sem esse corte entrava um naco dela na camada.

**O movimento e `scaleY` a partir do no do dedo**, nao translacao da mao. Com o `transform-origin`
exatamente na borda de cima do grupo, essa borda **nao se move** — entao nao existe faixa exposta,
nao existe emenda pra aparecer. So a ponta do dedo desce. Um `translateY` de 1,5-2px entra junto pra
dar amplitude; como ele desloca so pele sobre pele identica, continua invisivel.

**Medido, nao olhado.** Diff pixel-a-pixel entre repouso e tecla pressionada, com respiracao, cabeca
e cauda congeladas pra isolar o efeito:

| versao | px que mudam | onde |
|---|---|---|
| v4 (mao inteira) | 26.266 | x 32-66%, y 78-97% — mao, manga e faixa do teclado |
| v6 (so dedos) | 4.579 | x 36-64%, y 83-97% — **so as pontas dos dedos** |

**Camadas** (9 WebP, 146 KB): `tail`, `body`, `head` + `lid-l`/`lid-r`, e `f1..f4` (os dedos, ~5 KB
cada). Sairam `hand-l`/`hand-r` e os keyframes `smTapL/R` — as maos agora vivem na camada `body` e
nunca se movem.

**Ritmo:** 4 grupos batendo em cascata (esquerda-direita-esquerda-direita, 2,2% de defasagem entre
eles), 5 teclas cada, entre 17,1% e 60,7% da batida de 7s. Curva por keyframe: ataque
`cubic-bezier(.3,0,.7,.35)`, solta `cubic-bezier(.2,.65,.35,1)`.

O resto da cena e identico a v4: cartoes nascendo na borda da tampa, texto em 3 blocos, selo, pausa.

**Verificado:** 0 overflow em 390/414/768/1024/1280/1536 · 0 seletor orfao (conferidos `smTapL/R`,
`samir__hl/hr`, `.rig`, `.lap`, `.msgs`, `smType`) · as 9 camadas carregam · `prefers-reduced-motion`
vira um still com a conversa completa.

### Samir v7: sem cauda, um ciclo so, e os cartoes em volta da laptop (2026-09-17)

Retorno do usuario: (a) cauda e cabeca pareciam **duas animacoes separadas**; tirar a cauda e fazer o
resto parecer uma coisa so; (b) o Samir maior; (c) as mensagens **em volta** da laptop, com cara de
que ele esta respondendo o que entra.

**Por que parecia solto.** Cada peca tinha seu proprio periodo — respiracao 6,5s, cauda 9,1s, cabeca
8,3s, dedos 7s, piscada 5,9s. Eram primos entre si de proposito (pra nao ler como loop), e o efeito
colateral foi justamente esse: cada parte andando por conta propria. **Agora tudo roda no mesmo ciclo
de 7s da batida da mensagem** — corpo, cabeca, dedos e piscada. A variedade nao vem mais de periodos
diferentes; vem das 4 mensagens diferentes que passam a cada 28s.

E a coreografia virou uma performance so, em vez de partes mexendo:
- **corpo** (`smBody`): inclina uns 2px pra frente quando comeca a digitar e volta quando termina;
- **cabeca** (`smLook`): baixa pro teclado (−0,8deg, +4px) enquanto digita e levanta na espera;
- **dedos**: teclam entre 17% e 61% do ciclo;
- **piscada**: duas por batida — uma logo apos parar de digitar, outra no meio da espera.

Medido a cada 0,4s: em repouso tudo em 0; de 1,2s a 4,2s corpo e cabeca descem juntos com os dedos
batendo; depois sobem juntos.

**Cauda removida do recorte.** Nao bastava parar de anima-la: ela e o corpo ficam separados por uma
folga cuja altura muda, e em y=360 a cauda termina em x=371 enquanto a **orelha esquerda comeca em
x=375** — 4px. Um corte reto ou comia a orelha ou deixava um naco de cauda. Entao medi a folga linha
a linha (blocos opacos por y) e o corte segue o meio dela (lista `CUT_Y`/`CUT_X` em `layers3.py`).

**Samir maior:** sem a cauda, o recorte fecha em x>=340 em vez de 161 — a mesma largura de cena rende
~16% mais figura. Somado a cena mais larga (520 → 620px, e a coluna da arte passou de `.95fr` para
`1.06fr`), a cabeca dele praticamente dobrou em relacao a v4.

**Tres cartoes em volta da laptop**, todos nascendo na borda da tampa:
- pergunta, em cima a esquerda (0,30s);
- resposta, na coluna livre em cima a direita (1,25s), com o texto se escrevendo em 3 blocos;
- **novo:** confirmacao "Mensaje directo enviado ✓" logo acima da tampa (4,05s) — fecha o ciclo
  comentario → resposta → DM, que tinha se perdido desde a v4.

As posicoes nao sao arbitrarias: com o Samir ocupando a largura toda, as unicas areas limpas sao a
faixa de cima e a coluna a direita da cabeca dele (x 65-100%, acima da tampa). Os cartoes ficam
**atras** dele, entao qualquer sobra encosta na silhueta e some, em vez de tapar a cara.

**Camadas** (8 WebP, 160 KB): `body`, `head` + `lid-l`/`lid-r`, `f1..f4` (dedos). Saiu `tail`.

**Verificado:** 0 overflow em 390/414/768/1024/1280/1536 · as 8 camadas carregam ·
`prefers-reduced-motion` vira um still com a conversa completa · abaixo de 700px a cena empilha
(cartoes em cima, ele embaixo).

### Samir v8: uma imagem so — a animacao sai do corpo (2026-09-17)

A v7 gerou "parece que tem 4 maos": os dedos, ao esticar, passavam das pontas originais que continuam
embaixo, e no tamanho novo (o Samir ficou bem maior) isso lia como um segundo par de maos.

**O padrao, depois de quatro tentativas.** Mao inteira (v3/v4), silhueta da mao (v3), dedo por dedo
com `scaleY` (v6) e dedo esticado maior (v7) — quatro tecnicas, o mesmo tipo de defeito. A causa nao
e a tecnica: **o render oficial e uma imagem plana**. Qualquer peca recortada dela que se desloque
sobre o laptop cria borda, sobra ou duplicata, e quanto maior a cena mais visivel fica. Continuar
refinando o recorte era continuar batendo na mesma parede.

**Arquitetura nova, onde esse defeito nao pode existir:** o Samir e **um `<img>` unico**, sem nenhum
corte interno. Nao ha peca que possa duplicar. Verificado lendo o `transform` computado: `samir__base`
fica em `none` e as palpebras em identidade — nada dentro da figura se move.

**A digitacao passa a vir de duas coisas que nao podem quebrar:**
1. **O conjunto inteiro se mexe** — `smLean` (inclina ~3px pra frente ao comecar a digitar, volta ao
   terminar, respira na espera) e `smWork` (tremor de ~3,6 Hz, 1,7px, so na janela de digitacao: le
   como esforco, nao como deslocamento).
2. **A luz da tela pulsando nele** — um `radial-gradient` em `mix-blend-mode:screen` que acende em
   rajadas junto com os blocos de texto que vao aparecendo no cartao de resposta. E o sinal de
   "a tela esta trabalhando" sem mexer em nenhuma parte do corpo.

Mais a piscada (as palpebras seguem sendo o unico recorte, e sempre foram silenciosas: faixa de pele
lisa sobre pele lisa) e os tres cartoes em volta da tampa, que continuam da v7.

**O que se perde, e explicito:** nao da mais pra ver dedo batendo tecla. Esse e o preco de garantir
que nao ha artefato com este render. Pra ter digitacao de verdade seria preciso um asset animado
(sequencia renderizada do Samir digitando), que exige um gerador de imagem/video — nao disponivel
nesta sessao — ou o time de brand.

**Camadas** (3 WebP, 132 KB, contando o estatico da secao de beneficios): `samir`, `lid-l`, `lid-r`.

**Verificado:** 0 overflow em 390/414/768/1024/1280/1536 · as 3 camadas carregam · nada se move
dentro da figura (transform identidade) · `prefers-reduced-motion` desliga tudo, apaga o brilho e
deixa a conversa completa.

### Samir v9: so as maos — e um defeito encontrado no asset de marca (2026-09-17)

Retorno do usuario: o Samir inteiro se mexia (queria so as maos), a piscada parecia **sobrancelha**, e
as maos pareciam **duplicadas e sobrepostas**.

**Achado importante: a mao duplicada e do render de marca, nao da animacao.**
`brand/cxpress/assets/mascot/samir-laptop.png` tem uma **terceira mao** colada a esquerda da mao
esquerda (fonte x 578-705, y 908-968) — massa de pele fora do lugar, defeito tipico de imagem gerada.
Estava ali desde sempre; so ficou obvio quando o Samir cresceu na v7/v8. **Coberta** aqui, repintando
a regiao com a manga escura que esta ao lado. Mesma categoria do defeito ja documentado no
`hero-bg.png` (a cara deformada) — vale avisar o time de brand: o arquivo de origem esta com isso.

**Piscada removida.** A unica forma de fingir piscada num render plano e esticar uma faixa de pele
sobre o olho, e a faixa disponivel fica no arco superciliar — por isso fechava parecendo sobrancelha
descendo. Piscada de verdade exigiria arte do olho fechado (o BRANDBOOK proibe redesenhar o Samir).

**So as maos animam.** A base agora sai do render com as **duas maos recortadas fora** e o buraco
preenchido com a manga escura propagada de cima. Como nao existe mao original embaixo, **nada pode
duplicar** — era exatamente isso que produzia o "4 maos" da v6/v7 (o dedo esticado passava da ponta
original, que continuava la).

Detalhe que importa: o preenchimento entra so no **miolo** do poligono (erodido 2px) e a camada da mao
tem feather de 1,2px. Assim, no repouso, base+mao reproduzem o original ate na borda; com o
preenchimento indo ate a borda aparecia um rebordo escuro, e com ele erodido demais sobrava um anel de
pele do original que virava halo claro quando a mao descia.

Corpo, cabeca e laptop ficam **parados**. Saiu tambem o brilho de tela da v8 (era o corpo inteiro
mudando de luz).

**Medido:** diff entre repouso e tecla, com os cartoes escondidos: **16.833 px**, bbox x 27-47%,
y 81-97% — so a mao. O laptop (x 51-92%) fica identico.

**Camadas** (3 WebP, 136 KB): `base`, `hand-l`, `hand-r`.

**Verificado:** 0 overflow em 390/414/768/1024/1280/1536 · 0 seletor orfao · as 3 camadas carregam ·
`prefers-reduced-motion` para as maos e deixa a conversa completa.

### Samir v10: a camada que se move e so pele de dedo (2026-09-17)

Retorno do usuario sobre a v9: as maos apareciam **por cima do laptop**, **desalinhadas com o resto
das teclas**, e ainda parecia que um pedaco do computador ia junto a cada mao.

**A observacao das teclas desalinhadas foi o que fechou o diagnostico.** As camadas da v9 eram
poligonos tracados a mao em volta de cada mao — e um poligono em volta da mao **contem teclas**
(a mao esta sobre o teclado). Ao deslocar a camada, aquelas teclas andavam junto e deixavam de bater
com as do resto do teclado, que fica na base. Nao era impressao: eram teclas mesmo se movendo.

**Correcao: a camada que se move deixou de ser poligono e passou a ser mascara de PELE**, tirada da
propria imagem (`alpha>0.6 & R>140 & (R−B)>42 & R>G`), cortada na linha dos nos e dividida em 4 grupos
(2 por mao). Dentro delas nao entra um unico pixel de tecla, de tampa ou de manga — da pra conferir
olhando as camadas isoladas: sao so os dedos recortados.

**E a duplicata some sozinha.** Os dedos agora **so descem** (translacao pura, sem `scaleY`). A copia
deslocada cobre o original inteiro menos ~5px no no do dedo, que e pele lisa sobre pele lisa identica.
Por isso nao e preciso preencher nada na base — e a "duplicata" das v6/v7 vinha justamente do
`scaleY`, que deixava a copia mais comprida que o original e fazia a ponta antiga aparecer por baixo.

**Medido na pagina** (cartoes escondidos, diff entre repouso e tecla):

| instante | px que mudam | bbox |
|---|---|---|
| 1,95s | 6.149 | x 30-42%, y 85-96% |
| 2,90s | 3.756 | x 38-59%, y 83-96% |
| 3,80s | 5.274 | x 30-55%, y 84-96% |

Tudo dentro da faixa dos dedos. O corpo, a cabeca, as mangas, o teclado e a tampa ficam identicos.
(Na v9, pelo mesmo metodo, mudavam 16.833px incluindo area de teclado.)

**Camadas** (5 WebP, 148 KB): `base` + `d1..d4` (os grupos de dedo, ~4 KB cada).

**Verificado:** 0 overflow em 390/414/768/1024/1280/1536 · as 5 camadas carregam ·
`prefers-reduced-motion` para os dedos e deixa a conversa completa.

### Samir v11: um dedo por camada (2026-09-18)

Retorno do usuario sobre a v10: *"cuando se animan las manos al escribir no se percibe bien porque
las manos siguen debajo, anima dedo por dedo y agrega parpadeos ocasionales"*.

**Dedo por dedo.** As 4 camadas viraram **6** — tres por mao —, cortadas nas **pregas entre os dedos**
medidas no render (`creaseA = 742 + (y−870)·0,146` e `creaseB = 804 + (y−864)·0,237` na mao esquerda;
`x<926 / 926-958 / >=958` na direita). Continuam sendo mascara de pele, nao poligono.

**Ritmo variado.** Os `@keyframes` passaram de 7s para **28s** (o ciclo inteiro dos 4 cartoes, e
28 = 4x7 mantem tudo em fase), com 3-4 toques por rajada sorteados por dedo e por beat — cada uma das
quatro mensagens e digitada num ritmo diferente, entao o loop nao denuncia o loop.

**O parpadeo nao saiu, e foi por um motivo estrutural.** Tres tentativas, todas descartadas antes de
subir: (1) esticar a faixa da sobrancelha — le-se como cenho franzido, nao como palpebra; (2) faixa
retangular incluindo a borda do globo — borra o olho; (3) arco derivado da elipse do proprio olho —
esticar 12px de pele por 11x transforma pele em listras verticais. **O render oficial e uma imagem
plana com os olhos abertos: nao existe arte de olho fechado.** Um piscar convincente exige esse
frame, e o BRANDBOOK nao permite redesenhar a mascote. Ficou registrado como pedido para o time de
marca: um render de Samir com os olhos fechados (mesma pose, mesmo enquadramento) resolve.

### Samir v12: recorte limpo e a cabeca que olha a mensagem (2026-09-18)

Retorno do usuario sobre a v11: um **quadrado sobreposto na mao**, o Samir parecendo teclar **no apoio
de pulso**, **bordas mal recortadas** — e um pedido novo: *"cuando llega el mensaje entrante... parezca
que Samir voltea a verlo y después comienza a responder"*.

**1. O quadrado era repintura.** A mao extra do asset de marca (defeito documentado na v9, em
x 578-705 / y 908-968) vinha sendo **repintada** com o tom da manga — e o retangulo repintado nunca
casava nas bordas. Agora ela sai por **corte no alpha**: a linha `DESK` passa por cima dela seguindo a
borda real da manga (`(560,951) (585,948) (612,940) (645,934) (675,934) (694,940) (700,954) (706,968)`),
que tambem devolve o canto frontal esquerdo do laptop no lugar certo. Sem repintura, sem quadrado.

**2. As bordas.** Tres causas somadas: blur de 1,5px antes do residuo, rampa de alpha larga (32→95) e
poligonos do PIL **sem antialias** numa linha rasa (dava serrilha na base do laptop). Corrigido:
blur 0,9 · rampa 30→60 com `smoothstep` · **todas as mascaras de poligono desenhadas em 4x e reduzidas**
(`ss_mask`). A silhueta agora corta em ~3px em vez de desbotar por ~15px. O `drop-shadow` do CSS caiu
para `0 18px 26px rgba(35,41,96,.15)` — com a borda dura, sombra forte virava halo.

Sairam junto dois restos que so apareciam ampliados: uma **cunha clara a direita da tampa** (poligono
`RIGHT`, tracado sobre a aresta medida da tampa: −0,36x por y) e um **filamento** pendurado na manga
esquerda (retraco local do `DESK` entre x 398 e 464).

**3. O apoio de pulso.** A pose e do render de marca: a mao **esquerda** pousa no trackpad e a
**direita** nas teclas — e a esquerda ficava num vazio claro. Nao da pra mover a mao (colide com a
outra) nem inventar teclas num deck quase de perfil. O que resolve a leitura e o **tom**: o poligono
`PAD` escurece a superficie ate a media real do campo de teclas (`[88, 56, 39]`), preservando o
brilho relativo e **poupando a pele**. As duas maos passam a ler como apoiadas no mesmo deck escuro.

**4. A cabeca virou camada.** Corte numa linha tracada a mao que passa **inteira dentro do escuro**
(moletom e pelo): `x = 300..1200`, `y = 400 430 470 520 560 585 600 606 600 588 566 530 480 430`.
A base guarda **34px acima dessa linha** — as duas camadas se sobrepoem, entao por mais que a cabeca
ande nao abre fresta transparente no pescoco, e o que desliza ali e escuro sobre escuro. Pivo no
pescoco (`transform-origin:40.91% 59.19%`).

Movimento: `translate(-1,22%, -0,38%) rotate(-2,2deg)` — translacao em **%** pra acompanhar o
redimensionamento da imagem. Coreografia dentro de cada beat de 7s: cartao pousa em 0,30s · a cabeca
vira entre **0,35s e 0,88s** · segura o olhar ate **1,20s** · volta pra tela ate **1,60s** · os dedos
comecam em **1,20s**. Ou seja: ele le e **so entao** responde.

**Verificado que a cabeca nao abre buraco:** compondo base+cabeca e comparando com a silhueta
original, no repouso e em `(-11px, -3px, -2,2deg)`, todos os pixels que ficam vazados estao **acima de
y=430** (a linha do pescoco esta em y≈468) — ou seja, so onde a cabeca de fato saiu e o fundo tem que
aparecer. Zero furo na costura.

**Curso dos dedos +35%** (3,2-4,6px → 4,3-6,2px), que o deck escuro agora comporta sem denunciar nada.

**Medido na pagina** (cartoes escondidos, repouso = 6,5s):

| instante | px que mudam | bbox |
|---|---|---|
| 2,05s | 2.637 | x 31-59%, y 83-96% |
| 2,35s | 2.350 | x 34-53%, y 85-96% |
| 2,95s | 2.367 | x 30-57%, y 87-96% |

Tudo dentro da faixa dos dedos.

**Camadas** (8 WebP, 100 KB): `base` + `head` + `d1..d6`.

**Verificado:** 0 overflow em 390/700/960/1280/1536 · as 8 camadas carregam ·
`prefers-reduced-motion` zera as 8 animacoes e deixa a conversa completa.

**Pendente com o time de marca:** o `samir-laptop.png` tem a mao extra (v9) e o `hero-bg.png` tem o
rosto deformado. Os dois sao defeitos do asset, nao do recorte.

### Samir v13: dedo inteiro, giro mais claro e o marrom ao lado do headset (2026-09-18)

Retorno do usuario sobre a v12: que o giro da cabeca de fato **olhe a mensagem** antes de responder;
que suma a **mancha marrom entre o cabo do headset e o rosto**; e que no tecleio ainda parecia que
**uma parte do dedo ficava parada**.

**1. A mancha marrom eram duas coisas, e as duas eram fundo carimbado.** Medido no render, a faixa
`x 1008-1070 / y 240-413` e fundo puro (`[196,129,84]`) — **nao havia orelha direita ali**, o
poligono `EAR_R` estava forcando fundo a opaco desde a v2. Saiu. E o vao entre o arco do headset e o
pelo (`x 1005-1057 / y 417-508`) e um **bolsao fechado**: o flood vem da borda da imagem e nunca
chega la, entao ficava opaco por construcao. Aberto com uma regra pontual.

Pontual **de proposito**: listando os bolsoes fechados de residuo baixo, o maior tem 9.497px e e a
**testa** do Samir. Regra geral ali comeria o rosto.

**2. O dedo que ficava parado era o limiar da mascara.** A v12 usava `R>140 & (R−B)>42`. Medindo
coluna a coluna na ponta do dedo: a pele sombreada da beirada cai pra **R 95-137** mantendo
**R−B 90-140**, enquanto o deck escurecido fica em **R−B 29-58**. Ou seja, quem separa dedo de deck e
o **R−B**, nao o R — e o limiar antigo deixava de fora justamente a borda escura da ponta, que ficava
parada enquanto o resto descia. Agora: semente `R>150 & (R−B)>70`, crescimento `R>88 & (R−B)>62`
limitado a 13px em volta da semente, **preenchimento de buraco** (entram as unhas e os brilhos) e
fechamento de 11px pra que as **pregas entre dedos** — escuras demais pra qualquer limiar — tambem
entrem. Cada dedo ainda invade 9px do vizinho: a prega pertence aos dois e nunca fica sem dono.

**3. E o dedo deixou de andar na vertical.** Com a mascara cheia sobrava um risco escuro: a silhueta
do dedo e **inclinada**, entao translacao vertical pura descobre o contorno original de lado.
Medindo a inclinacao das duas bordas de cada dedo (`dx/dy`) o vetor certo apareceu sozinho:

| | d1 | d2 | d3 | d4 | d5 | d6 |
|---|---|---|---|---|---|---|
| `dx/dy` | +0,45 | +0,15 | +0,30 | −0,39 | +0,11 | 0,00 |

Os `@keyframes` passaram de `translateY(N)` para `translate(dx·N, N)`. O dedo desliza **no proprio
eixo**, entao a copia cobre o original e nao sobra contorno.

Tentei antes tirar os dedos da base e preencher o buraco — tres preenchimentos, tres artefatos:
difusao deixa a borda pastosa, vizinho-mais-proximo deixa pente, interpolacao por coluna puxa o
marrom do deck pra cima. **Acertar o vetor foi mais barato e mais limpo que inventar o que esta
atras do dedo.**

**4. O giro.** Amplitude de `translate(-1,22%, -0,38%) rotate(-2,2deg)` para
`translate(-2,4%, -0,72%) rotate(-3,6deg)` (−21,6px e −5,7px no canvas), e a leitura ficou mais
longa: vira entre **0,32s e 0,80s**, segura o olhar ate **1,10s**, volta ate **1,55s**, dedos so em
**1,20s**. Ele le e depois responde. Reverificado que nao abre fresta: todos os pixels vazados ficam
**acima de y=430** e a costura esta em y≈468 — zero furo no pescoco.

**Medido na pagina** (cartoes escondidos, repouso = 6,5s):

| instante | px que mudam | bbox |
|---|---|---|
| 0,75s (giro) | 297.680 | elemento inteiro |
| 2,05s | 5.412 | x 30-60%, y 82-96% |
| 2,35s | 2.169 | x 30-53%, y 84-96% |
| 2,95s | 1.895 | x 29-58%, y 85-96% |

O giro e grande de proposito (era pedido pra ficar evidente); o tecleio segue confinado a faixa dos
dedos.

**Camadas** (8 WebP, 101 KB): `base` + `head` + `d1..d6`.

**Verificado:** 0 overflow em 390/700/960/1280/1536 · as 8 camadas carregam ·
`prefers-reduced-motion` zera as 8 animacoes.

### Samir v14: a imagem deixa de ser recortada e passa a ser DEFORMADA (2026-09-18)

Retorno do usuario sobre a v13: *"la animación parece estar montada por partes"* — e o pedido de
reconstruir imagem e animacao do zero.

**O diagnostico dele estava certo, e e o mesmo defeito desde a v1.** O render oficial e uma imagem
chapada. Qualquer pedaco recortado dela e deslocado tem uma borda, e e a borda que denuncia. Treze
versoes afinaram o recorte; nenhuma podia resolver, porque o problema nao era a qualidade do recorte,
era o **metodo**.

**Tentativa descartada: redesenhar Samir em vetor.** Autorizada pelo Victor como excecao explicita ao
BRANDBOOK linha 249. Cheguei a construir o personagem inteiro em SVG com rig de verdade (piscada,
giro, dedo a dedo) usando o vocabulario de formas do icone oficial. Foi recusado, com razao: qualquer
coisa desenhada a mao le mais **chapada** que o render 3D. Fica arquivado no scratchpad; a licao e que
"desenhar do zero" e resposta pra *estilo*, nao pra *fidelidade*.

**A solucao: malha deformavel.** A textura e o recorte oficial inteiro, num so arquivo. Por cima dela
ha uma folha continua de **82x72 vertices** que se **estica**. A imagem nunca e cortada:

- o **dedo** desce esticando a pele que o liga a mao — em vez de abrir fresta no no;
- a **cabeca** vira esticando o pescoco — em vez de deslizar uma camada sobre outra;
- a **palpebra** fecha porque a pele da testa desliza por cima do olho.

Borda de recorte deixa de ser possivel **por construcao**. E o unico jeito de "montado por partes"
sumir: nao ha partes.

**A piscada, que falhou quatro vezes, saiu de primeira** — nao preciso de arte de olho fechado, a
malha traz a pele da palpebra. Mas nao de qualquer jeito: a queda tem que ser **assimetrica**.
Comprimir o olho simetricamente pro proprio centro espreme a esclerotica e da **olho revirado**. O
modelo certo e o da palpebra real: a pele acima viaja `tgt-(cy-ry)` e decai com a distancia
(estica), o olho comprime na linha `cy+0.40*ry`, a bochecha sobe pouco.

**Tres controles, medidos no render** (coordenadas 0..1 da textura):

| peca | centro | raio | o que faz |
|---|---|---|---|
| pescoco (pivo) | 0.409, 0.592 | — | eixo do giro |
| cranio | 0.365, 0.285 | 0.37 x 0.32 | gira junto |
| rosto | 0.415, 0.330 | 0.20 x 0.22 | desliza **mais** que o cranio — e o que faz ler como VIRAR, nao inclinar |
| olhos | 0.383/0.530, 0.334/0.337 | 0.053/0.039 | palpebra |
| 6 pontas de dedo | — | 0.023 x 0.043 | tecla |

**Relogio unico:** `document.timeline` — o **mesmo** que move os cartoes em CSS. Beat de 7s, ciclo de
28s (4 mensagens); 28 = 4x7, entao nada sai de fase. 12 piscadas em tempos irregulares dentro dos 28s.

**Custo:** WebGL. Mitigado — `<img>` still do mesmo render por baixo (aparece sozinho se nao houver
WebGL ou com `prefers-reduced-motion`), `IntersectionObserver` pausa fora da tela e
`visibilitychange` pausa em aba oculta.

**Peso:** 1 textura WebP de **78 KB** no lugar das 8 camadas (101 KB) — e **7 requisicoes a menos**.

**Verificado:** 0 overflow em 390/700/960/1280/1536 · `is-live` verdadeiro nas cinco larguras ·
`prefers-reduced-motion` esconde o canvas e deixa o still · sem erro de console.

#### Correcoes reportadas na v14 (2026-09-18)

Quatro achados do Victor, dois de **textura** e dois de **deformacao**:

**1. Risco branco na bochecha.** A regra que abriu o vao entre o arco do headset e o pelo era uma
**caixa retangular** (`res<50` em x 996-1070 / y 408-518). A caixa mordia a borda do pelo, e a
descontaminacao de cor `(src-(1-a)*modelo)/a` sobre alpha parcial estoura pra branco — virava risco
claro dentro do pelo. Agora abre so a **componente conexa** do vao, semeada de dentro dele e
**erodida 2px**, entao nunca encosta na borda do pelo.

**2. Buraco mal recortado embaixo da mao.** Herdado da v12: pra tirar a "mao sobrando" eu tinha
**subido** a linha do `DESK` (y 934-968 entre x 612 e 706) — e junto levava os **dedos de fora** da
mao esquerda e a **quina frontal esquerda do laptop**, deixando uma cunha branca. Medi o contorno
real coluna a coluna (diferenca contra a cor local da mesa, limiar 90-160 — estavel) e o refiz onde
ele realmente esta: `(560,953) (590,964) (620,973) (652,976) (678,974) (700,978) (724,982)
(750,987) (800,993) (850,996) (900,999) (960,1002)`. Os dedos de fora voltam — sao do render oficial
e a essa escala leem como dedos, nao como defeito.

**3. Dedos esticados de forma irregular.** A elipse na ponta fazia a ponta andar tudo e a base nada:
o dedo **esticava** em vez de andar. Cada dedo virou **capsula no->ponta** (raio 17px): peso ~1 ao
longo do dedo inteiro, caindo so na faixa **acima do no**, e o deslocamento e na **direcao do
proprio dedo**. Ele anda inteiro; a esticada fica escondida no no.

**4. Giro e piscada esticavam demais.** Giro: de `rot -5,2 / dx -0,046 / squash -0,17` para
`-3,5 / -0,029 / -0,085`, deslize do rosto de 0,42 para 0,26 e queda do cranio mais larga
(`soft 0,45 -> 0,62`) — a mesma deformacao espalhada por mais area estica menos em cada ponto.
Piscada: o alvo subiu (`0,40 -> 0,30 ry`) e o alcance na testa encurtou.

E a piscada ganhou **queda eliptica unica**. Separar horizontal de vertical deixava uma **caixa
visivel no focinho**: a bochecha dentro da faixa do olho subia e a de fora nao, com aresta reta
entre as duas.

#### v14.2 — giro fora (2026-09-18)

**Giro removido.** Mesmo com amplitude baixa a esticada do pescoco continuava aparecendo. Numa arte
chapada o giro **so existe como deformacao** — sem arte de perfil nao ha como escondê-la. `look=0`.

**Revertido no mesmo dia:** cheguei a reduzir o curso do dedo pra 1/3 e a por um **halo** com a forma
da silhueta, pintado com o marrom de origem do render (`#C48158`) — a ideia era que a borda
compusesse sobre o mesmo fundo contra o qual foi renderizada, fazendo o resto de recorte sumir por
aritmetica. Funcionava tecnicamente, mas o Victor recusou o resultado: o halo le como aura em volta
da figura. Voltou tudo ao estado anterior, menos o giro.

**Assets:** `samir-hero.webp` (78 KB, textura unica).

### Samir v15: o recorte passa a vir pronto (2026-09-18)

O Victor mandou **`Samir recortado.png`** — o mesmo render, ja recortado com **alpha de verdade**
(1080x1080, 1,1% de pixels de borda parcial). Arquivado em
`brand/cxpress/assets/mascot/samir-laptop-cutout.png` e anotado no BRANDBOOK.

**Isso encerra a familia inteira de defeitos de recorte.** Da v1 a v14 eu gerava o alpha a partir do
render de fundo marrom solido: modelo polinomial de fundo, flood fill, poligonos tracados a mao,
descontaminacao de cor. Cada zona que eu corrigia abria outra — risco branco na bochecha, cunha
embaixo da mao, orelha direita inventada, filamento na manga, serrilha na base. **Nada disso existe
mais**: a borda vem pronta e e melhor que qualquer coisa que eu media.

Sobrou so o que e decisao editorial, nao tecnica:
- **cauda fora** (pedido na v7). Onde ela encosta no corpo (y 745-855) o alpha nao separa nada — os
  dois sao opacos — entao ali separo por **cor**: a cauda e parda (`R-B > 14`), o moletom e azul
  escuro. Nas outras alturas basta varrer o alpha;
- **logo da Apple fora da tampa** (marca de terceiro em pagina comercial), em `x 852-922 / y 730-818`.

**Anatomia remedida** — o enquadramento mudou (textura 889x835, aspect 1,065 contra 1,140):

| | olho esq | olho dir |
|---|---|---|
| centro | 0,357 / 0,334 | 0,512 / 0,337 |
| raio | 0,051 x 0,052 | 0,042 x 0,047 |

Seis capsulas de dedo (no -> ponta), tres por mao, raio 16px. A palpebra teve que descer mais
(`tgt` de `0,30` para `0,82` do raio): no olho novo o alvo antigo parava no meio e o resultado lia
como sono, nao como piscada.

**Resolucao:** o recorte novo tem o sujeito a ~876px de largura util contra ~1050px do render
original — cerca de 17% menos. Em troca, zero artefato de recorte. A LP exibe esse trecho a ~585px,
entao sobra margem em telas 1x e fica justo em 2x.

**Textura:** `samir-hero.webp`, 71 KB.

#### v15.1 — tecleio suave (2026-09-18)

O Victor pediu o tecleio mais suave. Mexer so no curso nao resolvia: **duas causas maiores estavam
fora do dedo**.

**1. A respiracao movia a laptop.** Ela era uma faixa em `y` (`0,50` a `0,88`), e nessa faixa entram
a laptop e as maos inteiras — tudo subia e descia junto. Era isso, mais que o dedo, que fazia o
conjunto parecer agitado. Agora e uma **elipse no torso** (centro `0,35 / 0,63`, raio
`0,27 x 0,135`) que morre antes das maos (`y>0,80`) e antes da laptop (`x>0,60`). Amplitude de
`0,0042` para `0,0032` e periodo de 3,5s para 3,8s.

**2. A capsula do dedo passava da yema.** A queda ao longo do eixo morria so em `sN=1,6` — 60% alem
da ponta — entao arrastava a **borda da laptop**, que ondulava debaixo do dedo. Agora morre em
`sN=1,12`, logo depois da yema, e a queda perpendicular encurtou (`0,65` para `0,42`).

**3. E so entao o curso:** de `0,016-0,024` para `0,0060-0,0090` da altura da textura (de ~13-20px
para ~5-7,5px), com envelope mais longo — ataque de 0,10s para 0,16s, solta de 0,14s para 0,22s.
O toque parecia seco tanto pelo curso quanto pela pressa.

**Medido na pagina** (faixa das maos, repouso em t=1,90s):

| instante | px que mudam | faixa em x |
|---|---|---|
| 2,05s | 4.351 | 188-437 |
| 2,20s | 5.940 | 188-401 |
| 2,34s | 4.117 | 188-436 |
| 2,50s | 6.625 | 188-437 |

Antes de confinar a respiracao eram 8.760 a 15.988px e a mudanca cobria a largura toda — incluindo a
laptop. Agora fica so na regiao das maos.

**Bug corrigido no caminho:** ao reescrever o bloco de anatomia da v15 eu apaguei a linha que declara
`TW/TH/FR`. O deformador de dedo lancava `TW is not defined` a cada frame e **os dedos nao animavam**
— o que se via era respiracao e piscada. So apareceu porque rodei o check de console; a olho a cena
parecia viva. Fica a licao: conferir o console, nao so o frame.

#### v15.2 — so a yema desce (2026-09-18)

Diagnostico do Victor: *"parecen ondas en las manos"*. Estava certo, e a causa era o **modelo**, nao
a amplitude.

Ate aqui o peso da capsula era ~1 **ao longo do dedo inteiro** e caia so acima do no: o dedo andava
como **bloco**. Seis blocos deslizando sobre uma massa continua de pele e exatamente o que produz
onda — a mao nao dobra em lugar nenhum, ela escorrega por partes.

Invertido: o peso agora e **0 no no**, sobe ao longo do dedo e chega a **1 na yema**
(`sm((sN-0,34)/0,58) * (1-sm((sN-0,96)/0,20))`). O dedo **dobra** em vez de deslizar — que e o que a
mao faz de verdade. A queda perpendicular tambem encurtou (`dperp-0,9 / 0,32`), e os toques por beat
cairam de 3-5 para 2-3 por dedo: 18-30 toques simultaneos em 3s eram agitacao por acumulo.

**Medido** (faixa das maos, repouso em t=1,90s): de **4.100-6.600px** para **1.600-3.100px**, e a
mudanca ficou confinada a regiao das pontas.

| versao | px que mudam | o que se move |
|---|---|---|
| v15 (bloco) | 8.760-15.988 | dedo + mao + laptop (respiracao em faixa) |
| v15.1 | 4.117-6.625 | dedo inteiro como bloco |
| v15.2 | 1.604-3.113 | so a yema |

#### v15.3 — pulso (2026-09-18)

A pedido do Victor, as **maos balancam de leve no proprio pulso** pra ligar a yema ao braco.

Pivo onde o punho sai da manga (`0,338/0,826` e `0,579/0,796`), elipse so em cima da mao. Duas
componentes somadas:

- **balanco continuo** de ~0,85 grau, periodos **diferentes** por mao (2,6s e 3,1s) e fase deslocada
  — se fossem iguais as duas maos andariam em espelho e leria como mecanismo;
- **mergulho** de ate 0,55 grau ligado a intensidade do toque daquela mao, entao o pulso cede junto
  com a yema em vez de viver por conta propria.

**~1 grau e teto, nao timidez:** a borda da laptop encosta na mao, e girar mais volta a arrasta-la —
foi o defeito que a v15.1 corrigiu. Medido: a mudanca sobe de 1.600-3.100px para 2.000-4.300px e
continua confinada em `x 188-437`, sem tocar a laptop.

### Samir v16: a resposta e escrita letra a letra, e um som opcional (2026-09-18)

**Texto.** Antes a resposta aparecia em **3 blocos** (`twA/twB/twC`, em 2,8s / 3,29s / 3,78s). Agora
sai **caractere a caractere** entre **2,35s e 4,15s** do beat de 7s — dentro da janela em que os
dedos do Samir digitam (1,20s a 4,25s), no mesmo relogio dos cartoes (`document.timeline`). Cursor
piscando enquanto escreve, some quando termina. Os pontinhos de "digitando" foram antecipados
(`twD` de 31-40% para 26-33%) pra sairem antes de a primeira letra cair.

Feito em JS e nao em CSS de proposito: `steps()` em `width` so funciona numa linha, e a resposta
quebra em duas ou tres. Com JS o texto vive num `textContent` que cresce — reflui sozinho e o cursor
acompanha a ultima letra sem posicionamento manual.

**Sem JS, ou com `prefers-reduced-motion`, o markup original de blocos `<i>` fica intacto** e a
animacao antiga continua valendo. O JS so reescreve o conteudo quando vai animar.

**Som: opt-in, e nao ha alternativa.** Chrome, Safari e Firefox **bloqueiam audio ate o usuario
interagir com a pagina** (politica de autoplay, desde 2018). Som que toca sozinho no load nao e
implementavel — nao e limitacao de implementacao, e o navegador. Alem disso, som automatico numa LP
de marketing e problema de UX serio: a maior parte do trafego chega de trabalho, com caixas ligadas.

Entao: botao discreto no canto da cena (`Sonido de tecleo`, `aria-pressed`), **desligado por
padrao**. O `AudioContext` so nasce no clique — antes disso nao existe. O som e **sintetizado**
(rajada de ruido em bandpass 1,7-2,6 kHz com decaimento de 35ms + seno de 190 Hz de 50ms, ganho
~0,06), entao nao carrega arquivo nenhum e cada tecla soa levemente diferente.

**Bugs encontrados na verificacao** (nenhum era visivel a olho):
- `tw.querySelectorAll('i')` pegava tambem os tres `<i>` dos pontinhos, e o texto saia com
  espacos na frente. Passou a ler so filhos diretos;
- o `continue` de "a contagem nao mudou" pulava o desligamento do cursor, que ficava piscando
  ate o fim do beat.

**Verificado:** texto correto nos 4 beats, cursor so na janela de escrita, 0 overflow em
390/700/960/1280/1536, botao sem estourar layout, `prefers-reduced-motion` mantendo os 3 blocos e
escondendo o botao, console limpo.

### Hero v2: o destaque muda de frase e ganha laco com o Samir (2026-09-18)

Pedido do Victor: destacar **"asistente personalizado"** e fazer o leitor entender na hora que o
Samir **e** esse agente.

**A copy nao mudou.** A H1 ja dizia *"Tu asistente personalizado de atención al cliente"* — o
destaque so trocou de lugar (`.mark` saiu de "atención al cliente" e foi pra "asistente
personalizado"). Nenhuma palavra nova, entao nao houve criacao de copy publica; o unico texto
acrescentado e o nome proprio **"Samir"**, que ja e do BRANDBOOK.

**O laco tem tres partes, e a terceira e a que mais trabalha:**

1. **Traco pontilhado** saindo do fim do destaque (`.mark::after`, SVG inline em `data:`), apontando
   pra direita. Ancorado no proprio `::after` do destaque, entao acompanha a quebra de linha sozinho
   — nao ha geometria entre colunas pra quebrar. So a partir de 960px: abaixo disso a coluna empilha
   e a seta apontaria pro vazio.
2. **Etiqueta com o nome** no ombro dele, com o **icone oficial da marca** (os 12 paths do
   `logo-reversed.svg`, nao um desenho meu).
3. **Rima de cor:** a etiqueta usa o **mesmo pessego** do sublinhado do destaque. E o que amarra os
   dois elementos mesmo quando a seta nao existe (mobile).

**A etiqueta mora dentro do `.samir-in`, nao da `.kvscene`.** Primeira tentativa foi na cena: no
desktop funcionava, mas no mobile a cena vira coluna flex e o Samir vai pro fim (`order:9`) — a
etiqueta, absoluta em relacao a cena, ficava boiando num vazio 200px acima dele. Dentro do
`.samir-in` ela fica colada nele em qualquer largura. O botao de som levou `order:10` pela mesma
razao.

**Verificado:** destaque correto nas 5 larguras, 0 overflow, etiqueta presente, seta so >=960px,
`prefers-reduced-motion` com etiqueta e seta visiveis e sem animacao, console limpo.

### Hero v3: fundo marinho, ponteiro laranja, som fora (2026-09-18)

Cinco pedidos do Victor de uma vez.

**1. Som fora.** O botao e o sintetizador WebAudio sairam por completo.

**2. Seta maior.** De 132x52 pra **210x96**, traco de 2,4 pra 3,4px e ancora mais baixa
(`bottom:-.06em`) — antes ela encostava no texto e lia como sobreposta.

**3. Icone do chip.** O `logo-reversed.svg` deu lugar ao PNG que o Victor mandou, guardado em
`brand/cxpress/assets/mascot/icon-samir-face.png` e servido como `samir-face.webp` (5 KB, 132px).

**4. Fundo marinho.** `--navy` como fundo do hero. Duas consequencias mandaram no resto:

- **o moletom do Samir e quase esse mesmo azul** — sem nada atras ele sumia no fundo. Entrou o
  `.hero__glow`, um foco de luz fria atras dele que devolve a silhueta;
- **pra "asistente personalizado" continuar sendo o ponto mais forte da tela**, ele ficou **branco**
  com sublinhado **laranja**, enquanto o resto da H1 foi pra lilas. E o unico contraste maximo da
  composicao.

Formas decorativas mantidas (pill, ring, dot, pill laranja) com opacidade e cor ajustadas pro escuro
— sao as duas formas canonicas do brandbook e continuam dentro do limite de 5 por composicao.

**5. Ponteiro laranja** com rastro. Cursor em **PNG** e nao SVG: cursor SVG nao funciona no Safari, e
o hero e a primeira coisa que a pessoa ve. 24x24, triangulo laranja com contorno branco pra
sobreviver ao marinho e aos cartoes brancos. O rastro e **um** elemento movido por `transform` a
partir de duas variaveis CSS escritas dentro de um `requestAnimationFrame` — nao ha layout por frame.
So em `hover:hover` + `pointer:fine`, desligado em `prefers-reduced-motion`.

#### Incidente: apaguei 6,4 KB de CSS e recuperei da aba do preview

Ao remover o som fiz `s.index('  .sndbtn{')` pra achar o inicio do bloco. Mas eu mesmo tinha criado
uma **segunda** ocorrencia no passo anterior — `    .sndbtn{order:10}}`, com 4 espacos, dentro do
media query do `.kvname`. A busca de 2 espacos casou dentro dela, **muito antes** no arquivo, e o
corte levou junto `.kvscene`, `.samir`, `.bub`, `.card`, `.act`, `.tw` — 6.374 caracteres. A pagina
virou texto solto com um SVG gigante.

O CSS da cena nasceu **nesta sessao**, entao nao estava no git: `git show HEAD` so tem a versao
anterior da LP, com mascote estatico. O que salvou foi a **aba do preview**, que ainda tinha o
documento antigo carregado — extrai o `<style>` de la, recortei o trecho e recolei.

Licoes que ficam: **`str.index` com um seletor CSS nao e ancora segura** — usar delimitadores unicos
ou marcadores de bloco; e **conferir o balanco de chaves dos DOIS `<style>`** da pagina depois de
qualquer corte (a primeira checagem que fiz olhava so o primeiro bloco, de 59 bytes, e dava tudo
"ok").

**Verificado:** 0 overflow em 390/700/960/1280/1536, destaque branco nas cinco, canvas vivo,
`.sndbtn` ausente, `prefers-reduced-motion` com cursor padrao, rastro escondido e still no lugar do
canvas, console limpo.

### Hero v4: marinho mais profundo, ponteiro por contraste, movimento de apoio (2026-09-18)

**1. Azul mais profundo.** Novo token `--navy-deep:#171B47` — o marinho da marca puxado pra baixo —
no hero **e** na secao de CTA final, que tambem era `--navy`. Deixar so o hero escurecido quebraria a
leitura de "abre escuro, fecha escuro" da pagina.

**2. Ponteiro por contraste.** Dois PNG: triangulo **branco** (contorno marinho) nos blocos azuis
(`.hero`, `.cta`) e **marinho** (contorno branco) nos claros. O contorno na cor oposta e o que faz
ele sobreviver a fronteira entre blocos e aos cartoes brancos dentro do hero azul. Links e botoes
herdam o ponteiro do bloco em que estao.

**3. Rastro fora, realce de volta.** O halo **laranja** que seguia o mouse saiu. No lugar entrou o
**realce que troca de cor** (`.ptr`): luz **branca** sobre bloco azul, **azul royal** sobre bloco
claro — era isso que o Victor queria que mudasse de cor, nao o ponteiro.

Vale na **pagina inteira**, nao so no hero: `position:fixed`, um unico elemento movido por
`transform` a partir de duas variaveis CSS escritas dentro de um `requestAnimationFrame`.

Quem decide a cor e **`elementFromPoint` + `closest('.hero,.cta')`**, ou seja o elemento que esta
debaixo do cursor — e nao a posicao de scroll. Por scroll a cor erraria justamente na fronteira
entre duas secoes, que e onde a troca precisa ser exata. A classe so e escrita quando o estado muda,
entao nao ha toque no DOM a cada frame.

**4. Movimento de apoio.** Regra que segui: **nada pode competir com o hero**. Ciclos de 11s a 26s,
amplitudes de poucos pixels, so `transform`/`opacity` — composto na GPU, zero layout por frame.

| elemento | ciclo |
|---|---|
| `.shape--dot` | 11s |
| `.hero__mesh` | 14s |
| `.shape--pill` | 17s |
| `.cta__pill--orange` | 18s |
| `.shape--orange`, `.hero__glow` | 19s |
| `.res__pill` | 21s |
| `.shape--ring` | 23s |
| `.cta__pill` | 26s |

**Os periodos sao primos entre si de proposito.** Se fossem multiplos, as formas voltariam a se
alinhar de tempos em tempos e a pagina inteira pulsaria junto — que e o oposto de discreto.

Alem das formas: **brilho que atravessa o botao principal** a cada 6,5s (era o unico ponto focal sem
movimento proprio, e para no hover pra nao atrapalhar o clique), **numero do tile** que sobe ao
entrar na tela e fica laranja no hover, e o **numero das estatisticas** que ganha o sublinhado pessego
da marca quando entra. A contagem dos numeros ja existia.

Tudo desligado em `prefers-reduced-motion`, inclusive o ponteiro custom (volta ao `auto`).

**Verificado:** 0 overflow em 390/700/960/1280/1536, `#171B47` nas cinco, canvas vivo, 47-55
animacoes ativas, console limpo; com `prefers-reduced-motion` cursor `auto`, formas e brilho do botao
com `animation-name:none` e still no lugar do canvas.

#### Hero v4.1 — o realce vira anel, a seta sai de tras do Samir (2026-09-18)

**Ponteiro custom fora.** Os dois PNG de cursor sairam; o cursor volta ao do sistema. Ficou so o
realce, que e o que o Victor queria que trocasse de cor.

**O realce deixou de ser mancha.** Era um borrao radial — e sobre bloco claro um borrao escuro le
como **sombra**, nao como luz. Virou **anel**: contorno de 2px com miolo vazado e um ponto de 5px no
centro. Contorno nao tem como ser lido como sombra.

**E o movimento passou a vir do ATRASO.** O anel persegue o ponteiro (`x += (alvo-x) * 0.22` por
frame) em vez de estar grudado nele. Um realce grudado e invisivel — o olho ja esta no ponteiro; o
que se ve e a distancia entre os dois quando a mao se move. Alem disso o anel **cresce de 38 pra
54px** sobre qualquer coisa clicavel (`a, button, .tile, .aud__item`), entao ele tambem informa.

**Seta: dois defeitos.**
1. *Passava por tras do Samir.* A cena tem `z-index:2`; a coluna de texto nao tinha nenhum. Agora
   `.hero__copy` e a `h1` tem `z-index:3`.
2. *Nao existia no mobile* — estava so em `min-width:960px`. Ganhou uma variante em
   `max-width:959px`: menor (78x74) e apontando pra **baixo**, que e onde o Samir passa a estar
   quando a coluna empilha. Apontar pra direita ali mandaria o olho pra fora da tela.

**Verificado:** 0 overflow em 390/700/960/1280/1536, seta presente nas cinco (210px no desktop, 78px
no mobile), cursor `auto`, anel ativo, canvas vivo, console limpo; `prefers-reduced-motion` esconde o
anel e mantem o still.

#### Hero v4.2 — sem realce de mouse, seta dimensionada ao vao (2026-09-18)

**Todo o movimento de mouse saiu.** Ponteiro custom, anel, rastro — nada disso existe mais. CSS,
markup e listeners removidos.

**A seta nao estava atras do Samir — estava GRANDE DEMAIS.** O `z-index` ja funcionava; o problema
era geometria. Medido: o vao entre o fim de "personalizado" e o inicio da silhueta dele e de
**~80px**, e a seta tinha **210px**. Sobrava 130px em cima da orelha.

Agora tem **60x52** e sobra folga em todos os breakpoints em que ela existe: **+20px** a 1536,
**+23px** a 1280, **+26px** a 1100, **+13px** a 960 (o mais apertado). Medido, nao estimado.

**A ponta tambem estava errada.** Ao reescalar eu mantive a rotacao antiga, e o que sobrou foi um
esquadro: duas linhas em angulo reto que nao apontavam pra lugar nenhum. Depois virou "V" — barbas
longas demais sobre uma tangente de 61 graus leem como **check**, nao como flecha.

Agora e **triangulo cheio**, e as coordenadas saem de conta, nao do olho: a ponta fica no fim da
curva, a base recua 13,5px **ao longo da tangente** (derivada do ultimo ponto de controle da Bezier)
e abre 6,4px pra cada lado na **perpendicular**. A linha pontilhada para 1,5px antes da base, senao
o triangulo parece colado nela.

**No mobile a seta saiu.** Apontando pra baixo ela dizia "continua rolando", nao "o Samir e esse
assistente" — o Samir fica ~1000px abaixo quando a coluna empilha. O laco ali fica por conta da
etiqueta com o nome e da rima de cor com o destaque.

#### Incidente 2: o mesmo erro, de novo

Pra tirar o bloco da seta mobile usei outro **corte por intervalo** entre dois comentarios. Entre
eles havia 23.406 caracteres — a etiqueta, a cena inteira, os cartoes, o texto das respostas. A
pagina quebrou igual a primeira vez.

Recuperado outra vez da aba do preview, agora com **gzip + base64** (22,6 KB de CSS viraram 9 KB de
transferencia) e ja removendo no navegador os dois blocos que nao deviam voltar.

**A licao da primeira vez eu escrevi mas nao segui.** A regra passa a ser: **nunca `s[:i]+s[j:]` em
CSS**. So `str.replace` com a string exata e completa do bloco. Se o bloco e grande demais pra citar
inteiro, ele precisa de marcadores proprios (`/* @bloco-x inicio */` ... `/* @bloco-x fim */`) antes
de qualquer corte.

**Verificado:** 0 overflow em 390/700/960/1280/1536, os dois `<style>` com chaves balanceadas,
`.kvscene`/`.card`/`.bub`/`.samir`/`.tw__s` de volta, seta so >=960px, cursor `auto`, sem `.ptr`,
canvas vivo, console limpo.

### Cursor fluido (2026-09-18)

Pedido: um cursor como o de **nexstudio.tech**. Inspecionei o DOM deles antes de escrever nada.

**O que eles fazem** (`div.fluid-cursor`, `position:fixed`, `pointer-events:none`, `z-index:2000`):

- `transform: translate3d(x,y,0) rotate(θdeg)` no container — o angulo acompanha a **direcao do
  movimento**;
- `transform: translate(-92%,-50%) scale(sx,sy)` no filho — **estica e achata** conforme a velocidade;
- `data-visible` / `data-interactive` / `data-pressed` pros estados;
- `cursor:none` no body: o cursor do sistema some.

**Como replicei.** O vetor de **atraso** (`alvo - posicao`) faz o trabalho todo: e proporcional a
velocidade, entao dele saem **de uma vez** a direcao (o angulo) e a forca da esticada. Nao precisa
derivar velocidade por tempo nem filtrar ruido do ponteiro. O angulo so atualiza acima de 1,1px de
atraso — sem esse limiar o cursor gira sozinho quando voce para.

**A esticada saiu** (pedido do Victor): a proporcao agora **nunca muda**. Sobraram as duas coisas
que dao vida sem deformar — o **atraso** (peso) e a **rotacao** (direcao). O unico `scale` que
restou e o do clique, e e **uniforme**, entao nao deforma.

| estado | efeito |
|---|---|
| parado / em movimento | mesma proporcao sempre |
| sobre clicavel | cresce de 32x23 pra 44x32 (mesma razao) |
| pressionado | `scale(.84)` uniforme |

**Tamanho 25% menor** que a primeira versao: 42x31 -> **32x23**.

**Cor por bloco:** **laranja** `#EF863C` sobre os blocos azuis (`.hero`, `.cta`), **marinho**
`#171B47` sobre os claros. O `path` usa `fill:currentColor` e o JS so troca `data-dark` — quem
decide e o `elementFromPoint`, nao o scroll, pra a troca ser exata na fronteira. O contorno branco
fica nos dois casos: no claro ele some no fundo, mas e o que separa a forma quando ela passa por
cima de um cartao ou de uma sombra.

**Forma: dardo com muesca, igual a referencia.** Busquei o SVG deles
(`/media/brand/nexstudio-cursor.svg`) pra entender a geometria: e um dardo apontando pra direita,
com uma **muesca em V no rabo** e cantos arredondados, `fill:black` com `stroke:white` — o contorno
branco que o Victor pediu **ja estava la**, e faz sentido: e o que sustenta a forma sobre fundo
escuro e sobre fundo claro sem trocar de cor.

Redesenhei com **coordenadas proprias** (poligono ponta / rabo-baixo / muesca / rabo-cima com raios
por canto) em vez de copiar o arquivo: ele mora em `/media/brand/` deles, e marca de terceiro. A
forma em si — um dardo — e generica; o arquivo nao e.

A ancora e a **ponta** (`translate(-94%,-50%)`, `transform-origin:94% 50%`), entao a esticada sai da
ponta e nao do centro. Contorno branco de 2,6 com `paint-order:stroke`, pra a borda ficar por fora e
nao comer a forma.

**Outra diferenca deliberada:**
**Sem `mix-blend-mode:difference`.** Eles usam pra o cursor se ver em qualquer fundo. Na nossa
   paleta o difference devolve cor estranha: sobre o marinho `#171B47` ele daria um amarelo palido.
   O laranja `#EF863C` ja tem contraste no marinho **e** no branco, entao nao precisa do truque.

**Campo de texto e excecao:** `input, textarea, select, [contenteditable]` mantem o cursor do
sistema e a gota some por cima deles. Sem isso voce perde o caret e nao sabe onde vai escrever —
custo de usabilidade que nenhum efeito paga.

**Verificado:** 0 overflow em 390/700/960/1280/1536, `cursor:none` no body e `auto` nos campos, gota
ativa, canvas vivo, console limpo; `prefers-reduced-motion` devolve o cursor do sistema e esconde a
gota. Em toque nem instancia (`pointerType==='touch'` sai na hora).

#### Mascote do card 01 (2026-09-18)

O card "Identifica intención de compra…" ainda usava `samir-laptop.webp` — recorte meu, da v2, **com
cauda e com o logo da Apple**. Ficava estranho ao lado do hero, onde o Samir nao tem nem uma coisa
nem outra.

Primeiro apontei pro `samir-hero.webp` (o mesmo do hero, de graca pelo cache), mas ali o Samir esta
**sem cauda** — e no card o Victor a quer inteira. Entao virou **`samir-card.webp`** (1087x832,
75 KB): o mesmo recorte limpo que ele mandou, **com a cauda**, e so com o logo da Apple removido
(marca de terceiro em pagina comercial).

Ou seja: **cauda fora no hero, cauda dentro no card** — os dois saem do mesmo recorte de origem, a
diferenca e so o corte.

`samir-laptop.webp` (49 KB, recorte meu da v2) foi apagado — nenhuma referencia sobrou no repo.

#### Glow dos cards no hover

Duas camadas, e a divisao entre elas nao e estetica, e tecnica:

- **halo de fora** em `box-shadow` (anel laranja de 1px + duas sombras difusas, laranja e royal).
  Tem que ser `box-shadow` porque o `.tile` tem `overflow:hidden`: qualquer pseudo-elemento com
  inset negativo seria **recortado**. `box-shadow` pinta fora da caixa e nao e afetado;
- **foco de dentro** num `::before` com gradiente radial em `var(--mx)/var(--my)`, que o JS atualiza
  no `pointermove` de cada card. Esse **pode** ser recortado — e ate melhor que seja, porque assim o
  foco respeita o canto arredondado.

O JS so escreve duas variaveis CSS no proprio card; o resto e composicao. `.tile>*{position:relative}`
pra o conteudo ficar acima do foco.

**Verificado:** os 4 cards acendem (opacidade 1 no `::before`, laranja no `box-shadow`, `--mx`
seguindo o cursor) em 390/960/1536; `prefers-reduced-motion` esconde o foco e mantem o card estatico.

#### Correcao: o circulo do canto tapava a frase (2026-09-18)

O que o Victor viu como "a animacao se sobrepoe ao texto" **nao era o glow novo** — era um
`.tile::after` que **ja existia**: um circulo lilas **chapado** de 120px no canto, que crescia no
hover. Pseudo-elemento se pinta **depois** dos filhos, entao ele ganhava do paragrafo e cobria o fim
da frase.

Duas correcoes:

- **Camadas explicitas:** `z-index:0` nos dois pseudos e `z-index:1` no conteudo. Sem numero, a
  ordem era a de pintura (`::before`, filhos, `::after`) e o `::after` sempre venceria.
- **Difuso em vez de solido:** o circulo chapado virou gradiente radial que morre em transparente
  aos 72%, maior (250px), deslocado mais pra fora do canto e com `blur(8px)`. Nao ha mais aresta.

**Verificado** em 390/700/960/1280/1536: texto em `z-index:1`, os dois brilhos em `0`, `::after` sem
cor solida (so gradiente) e com `blur(8px)`, foco do cursor ativo, 0 overflow, console limpo.

### Menu no header + glow dos cards so em azul (2026-09-18)

**Glow dos cards agora e monocromatico azul.** O gradiente laranja->royal saiu; ficou
royal -> lilas -> transparente, e o halo de fora tambem virou azul (anel royal + sombra royal +
sombra marinho). O numero do card, que acendia laranja no hover, passou a `--royal-deep` pela mesma
razao.

**Menu de navegacao.** Quatro secoes, com os rotulos que **cada uma ja usa** como kicker:

| link | secao | id |
|---|---|---|
| Qué hace por ti | `.benefits` | `#que-hace` |
| Para quién es | `.aud` | `#para-quien` |
| La prueba | `.res` | `#la-prueba` |
| La diferencia | `.why` | `#la-diferencia` |

**Nenhum texto novo foi escrito** — os quatro rotulos ja existiam na pagina e o CTA passou pra
"Agenda una demo", que e a mesma frase do botao do hero. Entao isso nao e criacao de copy publica.

**Detalhes que nao sao decorativos:**

- **`scroll-margin-top:86px`** nas secoes. O header e `position:sticky`; sem isso a ancora para
  **debaixo** dele e o titulo da secao fica escondido.
- **Scroll-spy** com `IntersectionObserver` e `rootMargin:'-86px 0px -55% 0px'`. O recuo de 86px no
  topo desconta o header (senao a secao "entra" atras dele e a marcacao adianta) e o de 55% embaixo
  faz a marcacao trocar quando a secao passa do meio da tela, nao quando so encosta. Marca com
  `aria-current`, entao o estado tambem chega pra leitor de tela.
- **Mobile (<1040px):** botao hamburguer que vira X, painel abaixo do header. Fecha com **Escape**
  (e devolve o foco pro botao), com **clique fora** e ao **escolher um link**. `aria-expanded` e
  `aria-controls` no botao.

**Verificado:** 0 overflow em 390/700/960/1040/1280/1536; menu inline a partir de 1040 e hamburguer
abaixo; CTA "Agenda una demo" nas seis; zero laranja no glow dos cards; scroll-spy marcando a secao
certa depois de clicar; Escape e clique-fora fechando; `prefers-reduced-motion` com
`scroll-behavior:auto` e sem transicao no sublinhado. Console limpo.

#### Glow dos cards: laranja (2026-09-18)

O Victor quis ver em laranja. Como e uma comparacao e vai e volta, a cor deixou de estar espalhada
pelas regras e passou a viver em **duas variaveis no `.tile`**:

```
.tile{--glow:239,134,60; --glow2:214,106,36}   /* laranja */
.tile{--glow: 74,105,189; --glow2: 35,41,96}   /* azul    */
```

`--glow` cobre o anel, a sombra principal, o foco que segue o cursor e o brilho difuso do canto;
`--glow2` e so a sombra de apoio, mais escura. Trocar entre as duas paletas e **uma linha**, nao sete
lugares — que era o que tornava esse vai-e-vem caro.

O brilho do canto, que era lilas fixo, tambem passou a usar `--glow`: com o resto quente ele ficava
destoando. Se preferir o canto sempre lilas, e so voltar aquele gradiente pros valores fixos.

**Verificado** em 390/960/1280/1536: `--glow` laranja, foco e brilho em opacidade 1 no hover, texto
ainda em `z-index:1`, 0 overflow, console limpo.

#### So o foco que segue o cursor (2026-09-18)

O brilho fixo do canto inferior direito saiu — era o antigo circulo lilas que eu tinha suavizado.
Duas luzes no mesmo card competiam entre si, e a parada nao informava nada: acendia sempre no mesmo
lugar, independente de onde estivesse o cursor.

Ficaram duas coisas, e as duas respondem ao ponteiro ou ao estado: o **foco que segue o cursor**
(`::before` com `--mx/--my`) e o **halo de fora** em `box-shadow`. Saiu junto a regra
`.bento__hero::after{display:none}`, que existia so pra desligar o brilho do canto no card grande e
virou codigo morto.

**Verificado** em 390/700/960/1040/1280/1536: `::after` com `content:none`, foco em opacidade 1 e
seguindo `--mx`, `--glow` laranja, 0 overflow, console limpo.

### Ritmo vertical mais apertado (2026-09-18)

"Demasiado aire entre bloques." Era o padding das secoes: **136px em cima + 136 embaixo = 272px** de
vazio entre uma secao e a seguinte. A essa distancia o olho nao le pausa, le **buraco**.

| | antes | depois |
|---|---|---|
| `section` (>=960px) | 136px | **92px** |
| `section` (mobile) | 88px | **62px** |
| `.hero` (base inferior) | 120px / 76px | **86px / 58px** |
| `.bento` margin-top | 52px | **38px** |
| `.stats` margem | 56/30px | **40/26px** |
| `.why__head` margin-bottom | 56px | **40px** |

184px entre secoes continua separando com folga — o que sumiu foi o excedente. A pagina encolheu
**~520px** no desktop (5.590 -> 5.067) sem tirar conteudo nenhum.

**Verificado:** 0 overflow em 390/700/960/1040/1280/1536, canvas vivo, console limpo.
