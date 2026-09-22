# Revisao LP · buzzmonitor/mcp-claude-latam (v3)

**Data:** 2026-09-10 (v3 + update do mesmo dia)
**Checks deterministicos:** `check_gtm_region.py` (ok, GTM-MKQBX2MG, latam) · `bump_mobile_type.py` (sem mudancas pendentes) · `check_mobile_type.py` (sem overflow real)
**Revisoes anteriores:** `versions/v2/REVISAO.md` (v2) · `versions/v1/REVISAO.md` (v1)

## Desvios deliberados das GUIDELINES (aprovados por Ulises)

- **§1 e §3 pedem fundo claro.** A LP e escura ponta a ponta por pedido explicito. O espirito da §1 fica: 3 cores fortes
  (ambar, laranja, vermelho) sobre preto quente, alternancia unica de fundo e **uma so** familia de degradado.
- **§5 e fundamentos-copy §0: o H1 abre pela solucao,** nao pela dor. Sinalizado na v1; Ulises optou pelo copy do brief.
  A alternativa que abria pela dor esta em `versions/v1/copy.txt`.
- **§11 manda integrar formulario so depois do design aprovado.** Ulises pediu a integracao junto com estes ajustes.
  Rodou pela skill `/lp-integrar-form` (wrapper canonico), entao a unica coisa que se perde e a folga de iterar
  layout sem o iframe no meio.

## Aplicado nesta rodada (pedidos de Ulises)

- [x] **Menos aire no topo do hero** (`padding-top` de `clamp(130,15vw,190)` para `clamp(96,9vw,124)`).
- [x] **Menos aire entre blocos:** `--pad` de `clamp(96,12vw,200)` para `clamp(64,7vw,118)`, mais `margin-top` menor em passos, filas e prompts. A pagina caiu de 8.437 px para ~7.500 px.
- [x] **MacBook menor** (`min(1020px,100%)` para `min(760px,92%)`) e abertura da tampa terminando com o equipo ja bem dentro da tela (`(vh*0.82 - top)/(vh*0.50)`, antes `(vh*0.92 - top)/(vh*0.72)`).
- [x] **Hover dos botoes da esquerda pra direita** (`translateX(-101%)` para `translateX(0)`, antes era `translateY`).
- [x] **Paso 0 em destaque:** card com borda em degradado, etiqueta "PASO 0", glow proprio e o CTA "Crear cuenta gratis" dentro. Saiu o CTA "Conectar ahora", que apontava pro mesmo bloco onde ja estava. A coluna direita (URL + Paso 0) agora equilibra a esquerda (3 passos).
- [x] **Ticker com capacidades do MCP** em vez da URL repetida (8 itens).
- [x] **Textos:** "Prueba su potencial ahora", "Reportes más rápidos y análisis más precisos. Menos trabajo manual.", "Social Listening + Claude." em uma linha com "Ahora sí se puso interesante." sublinhado em laranja, e "Buzzmonitor extrae los datos." + "Claude te da los insights" (degradado).
- [x] **Prompts reagindo ao scroll:** cada card recebe um `--near` continuo (distancia ao centro da tela) que controla desfoque, opacidade, escala e deslocamento. O mais central ganha borda laranja, glow e cursor piscando. Trilho lateral preenche conforme o bloco passa.
- [x] **Bloco de equipos como painel principal:** borda em degradado de 1,4 px, glow de secao, eyebrow proprio e sombra funda.
- [x] **Redes de LATAM no footer:** Instagram, X, Facebook, LinkedIn e YouTube, com as URLs tiradas do source de `plataforma-integral-social-media` (nao inventadas).
- [x] **Maquina de escrever nos 9 titulos principais** com cursor piscando, mais desfoque de entrada estendido ao resto dos blocos.
- [x] **Movimento permanente:** drift lento nos resplandores de hero, spotlight, prueba, conversacion, cierre e equipos; ticker; video; cursores piscando; pip do eyebrow.
- [x] **Halo do mouse em todos os blocos, sem corte:** o halo estava em `z-index:0`, entao o fundo opaco das secoes `--void-2` o cobria e ele "sumia" na fronteira. Passou para `z-index:290` com `mix-blend-mode:screen`, e ganhou suavizacao por lerp (persegue o cursor em vez de saltar).
- [x] **Formulario Jotform real** (`241825239057661`) via `/lp-integrar-form`.

## Bugs encontrados e corrigidos durante a rodada

- **Zig-zag dos prompts invertido.** O `<span>` do trilho virou o primeiro filho e quebrou `:nth-child(even)`. Trocado por `:nth-of-type`.
- **`.uline` nao existia.** A v2 tinha trocado o sublinhado por `.grad`, entao `<em class="uline">` saiu em italico e sem sublinhado. Regra recriada na versao escura.
- **Ticker com dois pontos por item e fonte monoespacada.** Sobrou a regra `.ticker span` da versao anterior (URL). Removida.
- **Opacidade dos prompts travada em 1.** `.js .reveal.in{opacity:1}` (0,3,0) vencia o `calc()` de `.prompt` (0,1,0). Os prompts sairam de `.reveal` e passaram a depender so do `--near`.
- **Contraste dos prompts.** A primeira versao do `--near` apagava os cards ate 34% de opacidade, o que reprova AA para texto branco no escuro. Piso subido para 66% e o desfoque virou o diferenciador (max 2 px).
- **Ancora `#f-nombre` morta** depois que o form mock saiu. Reapontada para `#form` no card.
- **`.valor h2` competindo com o hero.** Com a copy nova (mais longa), 104 px virava o maior texto da pagina. Reduzido para 80 px.

## Verificado

- **Sem JS:** tudo visivel, sem maquina de escrever, o video ate toca. **`prefers-reduced-motion`:** 0 elementos com opacidade < 0.85, video pausado, nenhum `.tw` construido, 0 cursores.
- **Sem scroll horizontal** em 1440 px nem em 390 px. Os unicos "overflow" que o `check_mobile_type` aponta sao o skip-link (fora da tela por design), os dois resplandores decorativos (recortados por `overflow:hidden`) e os itens do marquee (mais largos que a tela por design, §20).
- **Jotform carrega de verdade:** 7 campos, checkbox de newsletter e botao ENVIAR, dentro do wrapper, sem overflow.
- **SEO:** 1 description, 1 robots, 10 og, 4 twitter, 1 JSON-LD (parseia), 1 canonical. **GTM:** container LATAM correto. **Em-dash:** 0 no HTML e 0 na copy. **Zero erro de JS.**

## Pendentes (nao dependem de mim)

1. URL canonica de signup para "Probar gratis" e "Crear cuenta gratis".
2. OG image 1200x630 (`assets/og-mcp-claude-latam.png`).
3. Dominio: `content.buzzmonitor.com` ou `material.buzzmonitor.com`.
4. Confirmar se o MCP gera dashboards, para decidir se entra a linha "crea dashboards a medida" no ticker.

## Melhorias opcionais

- [ ] **O interior do formulario nao se estiliza daqui** (iframe cross-origin). Para um formulario escuro de verdade, o caminho e mudar o tema no proprio Jotform ou trocar o embed pelo codigo-fonte completo em vez do `jsform`.
- [ ] Sem bloco de prova social; a copy nao tem. Uma faixa de logos fecharia a estrutura da §6.
- [ ] Legibilidade do MacBook no mobile (ja tem zoom de 1,22 abaixo de 640 px).
- [ ] "performance" no bloco VALOR e anglicismo; o padrao ES-LATAM prefere "desempeño". Mantido literal por pedido.

---

## Update da v3 (2026-09-10, segunda tanda)

- [x] **Footer em 4 colunas** (logo, Política de Privacidad, copyright, redes), `space-between`, redes a direita. O agrupamento antigo (`.foot__col` com redes + privacidade empilhadas) foi desfeito.
- [x] **Tampa do MacBook abrindo com o scroll.** A rotacao saiu de `.mac` e foi pra um `.mac__hinge` com `transform-origin:50% 100%` (dobradica na base). Vai de `rotateX(78deg)` (praticamente fechada) a `0`, ao longo de `(vh*0.95 - top)/(vh*0.85)`, com easing `easeInOut`. Antes eram 15 graus num trecho de meia tela, que terminava antes de dar pra ver.
- [x] **Halo do mouse atras do MacBook.** `z-index` do halo de 290 para 150 e do `.stage` para 160. **Causa real:** `.hero__in` tinha `z-index:1`, o que criava um contexto de empilhamento e prendia o `.stage` inteiro abaixo do halo, por mais alto que fosse o z-index interno. Removido o `z-index` do `.hero__in` (a ordem visual continua certa porque `.hero__aura` vem antes no DOM). O halo continua por cima do fundo de todas as secoes, que era o que impedia o corte na fronteira, e agora fica abaixo da nav tambem.
- [x] **Marco laranja do bloco do formulario removido.** `.panel::before` (borda de 1,4 px em degradado) trocado por `border:1px solid rgba(255,255,255,.09)`. Glow e sombra ficam.
- [x] **Destinos dos CTAs unificados:** "Agendar una reunión" e "Hablar con ventas" vao pra `#form`; "Conectar MCP" vai pra `#instrucciones` (ancora nova no bloco dos 3 passos, com `scroll-margin-top` pra nao ficar embaixo da nav); "Crear cuenta gratis" e "Probar gratis" vao pra `https://app.buzzmonitor.com.br/user/signup/start` com `utm_source=lp&utm_content=lp-mcp-claude-latam` (convencao de §5.5 do CONTEXT).

**Revalidado:** sem em-dash, SEO completo, JSON-LD parseia, GTM LATAM ok, zero ancora quebrada, zero erro de JS, sem scroll horizontal em 1440 nem em 390, tampa aberta sem JS e sob `prefers-reduced-motion` (video pausado, 0 elementos invisiveis). Ancoras medidas pos-clique: `#form` em 110 px com a nav terminando em 90 px; `#instrucciones` em 104 px.

**Pendente do pedido:** o ultimo item da mensagem de Ulises ficou cortado em "los que dicen " e nao foi aplicado.

---

## Segundo update da v3 (2026-09-10)

- [x] **Typewriter disparando por bloco.** **Causa:** o `setTimeout(4000)` que eu tinha posto como rede de seguranca escrevia todos os titulos de uma vez e anulava o gatilho do IntersectionObserver. Removido. A rede de seguranca passou pro loop de scroll, que so escreve o que esta em tela (ou o que ja ficou acima, pra cobrir salto por ancora). Medido: no load so os 2 titulos do hero; apos rolar ate o fim, os 9 completos e nenhum vazio.
- [x] **Tampa do MacBook fechada -> aberta.** **Causa:** com a dobradica embaixo, `rotateX` positivo joga o topo pra tras, o que le como tela deitada pra tras; voltar a 0 parecia fechar. Invertido pra negativo, `perspective-origin:50% 130%` (camera um pouco de baixo) e um `.mac__scrim` cuja opacidade e `1 - var(--open)`, entao a tela some quando a tampa esta baixada.
- [x] **Ticker dentro do bloco no desktop**, correndo abaixo do passo 3 e por tras do card do Paso 0 (`position:absolute` no `.pasos`, `z-index` menor que `.steps`/`.urlwrap`, e base opaca no card e na caixa da URL pra nao vazar). Abaixo de 1001 px continua banda cheia embaixo do bloco.
- [x] **Mobile-first:** todos os alvos de toque em 44 px (logo agora dentro de um `.logo-link` de 44 px; o botao de pausa saiu de dentro de `.mac`, que aplicava `scale(.93)` e o encolhia pra 41 px), nav de 83 px pra 74 px, `.stage` a 100% da largura, e abaixo de 640 px os desfoques grandes caem pra 14 px com o drift desligado (custo de GPU).
- [x] **Botao do header:** texto "Agendar reunión", 13 px, padding menor.

### Incidente durante a edicao

Um `str.replace` meu casou um fecho de `div` ambiguo e **duplicou o hero inteiro dentro do `<header>`**, deixando dois `</header>`, dois `<main>` e 13 ids repetidos. Detectado pela checagem de estrutura (contagem de tags + ids duplicados) antes de qualquer screenshot. Reparado removendo o bloco duplicado; a arvore voltou a 1 header, 1 main, 6 sections, 0 ids repetidos. Licao: ancorar replaces em texto unico (ex.: o href do CTA), nunca em sequencias de `</div>`.

**Revalidado:** em-dash 0, SEO completo, JSON-LD parseia, GTM LATAM ok, 0 ancoras quebradas, 0 ids duplicados, 0 img sem alt, 0 erro de JS, sem scroll horizontal em 1440 nem em 390, 0 alvos de toque abaixo de 44 px, tampa aberta sem JS e sob reduced-motion (video pausado, 0 elementos invisiveis, 0 typewriters construidos).

---

## Terceiro update da v3 (2026-09-10)

- [x] **Ticker limitado a faixa livre (desktop).** Antes atravessava a tela inteira e passava por baixo do card do Paso 0, o que dava a impressao de o card estar sobreposto ao carrossel. Agora vai da borda esquerda da janela ate `calc(var(--rightcol-w) - 44px)`, ou seja, entra 44 px por baixo do card (efeito "sai de tras dele") e some. Mascara passou a fazer fade so na ponta esquerda (`linear-gradient(90deg,transparent 0,#000 24%,#000 100%)`).
  A largura da coluna direita virou variavel CSS no `.pasos` (`--rightcol-w`, derivada de `--wrap-w`, `--gut` e `--pasos-gap`, com o fator .475 do `.95fr`). Medido: o corte cai exatamente no `left` do card em 1024, 1200 e 1440 px.
- [x] **Botao do header menor que o logo:** 171x26 px contra 132x27 px. Fonte 12 px, padding 6/13. Continua acima do minimo de 24x24 do WCAG 2.5.8 (AA). No mobile volta a `min-height:44px`.

**Revalidado:** em-dash 0, JSON-LD parseia, GTM ok, 0 ancoras quebradas, 0 ids duplicados, arvore intacta (1 header, 1 main, 6 sections, 1 footer), 0 erro de JS, sem scroll horizontal em 1440 nem em 390, nenhum alvo de toque abaixo de 24 px, e sem JS / com reduced-motion tudo visivel.

---

## Quarto update da v3 (2026-09-10)

- [x] **Ticker parando antes do card.** `right` foi de `calc(var(--rightcol-w) - 44px)` (entrava 44 px por baixo) para `calc(var(--rightcol-w) + 26px)`, e a mascara ganhou fade na ponta direita tambem: `linear-gradient(90deg,transparent 0,#000 17%,#000 85%,transparent 100%)`. Folga medida ate o card: 26 px em 1024, 1200 e 1440.
- [x] **Botao do header dimensionado por breakpoint:** 136x21 no mobile (logo 114x23) e 171x26 no desktop, ~25% maior.
  **Pegadinha de cascata:** as duas primeiras tentativas nao pegaram porque `.nav .btn` (0,2,0) e o bloco de pisos de tipografia gerado pelo `bump_mobile_type.py` ficam **depois** na folha e sobrescreviam `.nav__cta` (0,1,0). A regra foi movida pro fim do `<style>` com seletor `.nav .nav__cta`.
  **Acessibilidade:** 21 px de altura fica abaixo do minimo de 24x24 do WCAG 2.5.8 (AA), entao o alvo de toque real e mantido em 156x45 por um `::after` transparente (`inset:-12px -10px`). Isso exige `overflow:visible`, o que desliga a varredura do hover nesse botao no mobile, onde nao ha hover mesmo.

**Revalidado:** em-dash 0, JSON-LD parseia, GTM ok, 0 ancoras quebradas, 0 ids duplicados, arvore intacta, 0 erro de JS, sem scroll horizontal em 1440 nem em 390, e tudo visivel sem JS e com reduced-motion.

---

## Correcao pos-publicacao (2026-09-11)

- [x] **Letra branca no hover do CTA da nav.** Ao reestruturar o botao (link = alvo de toque, `<span>` = pilula visual),
  copiei junto um `color:#fff` no hover. A varredura do `.btn` e **branca**, entao era branco no branco: o texto sumia.
  Agora a pilula mantem `#0A0507` no hover.
  **Varredura em todos os botoes:** so este estava errado. Medido o contraste texto x varredura em cada variante
  usada na LP (`.btn` 4x, `.btn--ghost` 3x, pilula da nav): **20,24:1** em todas apos o fix. O `.copy-btn` nao tem
  varredura (fundo em degradado fixo, texto quase preto, ~7:1). `.btn--solid` e `.btn--light` continuam definidos
  no CSS mas nao sao usados por nenhum elemento.

---

## Quinto update da v3 (2026-09-21)

- [x] **CTAs de reuniao -> "Quiero saber más"** nos dois botoes que levam ao form (header e bloco EQUIPOS). CTA em 1.a pessoa e o padrao do `padrao-linguistico.md` ES-LATAM (Regra de Ouro 5).
- [x] **Menu de secoes no header** com 4 ancoras (`#instrucciones`, `#valor`, `#conversacion`, `#equipos`). Medido pos-clique: as 4 caem abaixo do header, nenhuma fica tapada.
- [x] **Botao do header +20% de caixa** (texto igual): 26 -> 31 px no desktop.
- [x] **Navegacao mobile refeita.** A 1a versao (hamburguer + painel) foi descartada apos medir num iPhone 14: hamburguer e CTA centrados em y=37 de uma tela de 844 px (pior zona pro polegar), painel ocupando 250 px (30% da tela) e **cobrindo o H1 inteiro** (borda inferior em 332, H1 comecando em 175), com o header apertado (114+44+150 = 308 dos 390 px).
  Trocado por: **chips de secao com rolagem horizontal** no header (sempre visiveis, zero tap, chip ativo acompanhando o scroll e auto-scroll da faixa) e **CTA como barra fixa no rodape**, que se esconde sozinha quando o bloco do form entra na tela (o CTA aponta pra la, entao so atrapalharia).

### Armadilhas de cascata desta rodada (3)

1. `.nav .nav__cta-pill` do fim da folha (≤640) ainda dimensionava o botao como pilula inline e anulava o tamanho de barra. Reescrito pro novo papel.
2. `.nav.stuck .nav__in` do bloco ≤640 mantinha `margin:8px auto`, entao o header descolava do topo ao rolar e o conteudo aparecia na fresta. Zerado no mobile.
3. `.nav.stuck .nav__in` da folha base (0,3,0) reimpunha `background:rgba(16,9,11,.72)` por cima do `.nav__in` (0,1,0) do bloco mobile. Com header de 2 linhas o texto de tras vazava. **Medido por pixel** antes de concluir: (22,17,19) onde deveria ser (12,7,9), ou seja 4% de vazamento. Fundo passou a opaco (`#0C0709`) nos dois estados.

**Revalidado:** em-dash 0, SEO completo, JSON-LD parseia, GTM LATAM ok, 0 ancoras quebradas, 0 ids duplicados, arvore intacta, build do guarda-chuva OK (31 LPs, 0 aviso da nossa), 0 erro de JS, sem scroll horizontal em 390/768/1440, nenhum alvo de toque abaixo de 24 px, rodape nao coberto pela barra, e tudo visivel sem JS e com reduced-motion. Desktop intacto (CTA segue estatico no header).

- [x] **Video do hero cortado no mobile.** Medido em 390/768/1440 com a tampa forcada aberta: a proporcao da tela do MacBook bate com a do video (1.600 vs 1.602), entao o container nunca cortou nada. O corte vinha de um `transform:scale(1.22)` que eu mesmo tinha posto no bloco ≤640 pra dar legibilidade ao texto do Claude, e que deixava de fora 18% de cada eixo. Zoom removido e `object-fit` de `cover` pra `contain` com fundo preto, como o Ulises sugeriu: agora o quadro nunca e recortado, e a tarja so apareceria se a caixa mudasse de proporcao. Medido depois: **100% x 100% visivel** nos tres breakpoints.
  **Contrapartida assumida:** sem o zoom, a UI do Claude no celular fica menor. Os 3 passos em texto logo abaixo continuam sendo a fonte legivel; o video e demonstracao.
  **Nota de metodo:** a primeira medicao saiu errada (AR 6.5) porque o `getBoundingClientRect` de um elemento com `rotateX` devolve a caixa projetada, nao a de layout. Foi preciso forcar a tampa aberta antes de medir.
