# LP Buzzmonitor — todo-en-uno

**Gerado em:** 2026-10-08
**Copy-fonte:** `copy.txt` (reescrita a partir de contenido.getbuzzmonitor.com/buzzmonitor-todo-en-uno-para-tu-estrategia, tom mais persuasivo + estetica premium)
**Regiao:** LATAM (ES) — `es-419`, GTM `GTM-MKQBX2MG`

## Estrutura (v2, 2026-10-08)

1. HERO — H1 de dor curto + animacao "5 abas soltas viram 1 janela Buzzmonitor"
2. LOGOS — agencias (McCann, IPG Mediabrands, TBWA, Havas, Eureka&Co, Kaleidoscopio, Sube)
3. PROBLEMA — "¿Te suena familiar?" + 4 dores (lista com X)
4. FUNCIONALIDADES — componente de abas acessivel (ARIA tabs, setas do teclado), 1 painel por funcionalidade
5. CIFRAS + TESTIMONIOS — 4 cifras + 3 citas reais (fundo dark)
6. CTA FINAL — form mock (#demo)
7. FOOTER

v1 (secoes alternadas + RESULTADOS + 6 testimonios) foi descartada por feedback: "muito generica, titulo com muito texto".

## Estado

- [x] HTML gerado
- [ ] OG image 1200×630 → `assets/og-todo-en-uno.png`
- [ ] Revisao — `/lp-revisar buzzmonitor/todo-en-uno`
- [x] Formulario integrado — Jotform LATAM 241825239057661 (2026-10-15), no bloco do hero
- [ ] Publicado — `/lp-publicar buzzmonitor todo-en-uno content.buzzmonitor.com`
- [ ] Copy nao publicada no Notion (MCP Notion desconectado na sessao de 2026-10-08)

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `./assets/logos-agencias/*` (7 logos, copiados de `plataforma-completa-social-media-latam`)

## Interacoes (v4, 2026-10-08)

Pedido explicito do usuario: "muitas animacoes responsivas durante todo o journey". Override consciente de GUIDELINES §4 (2-3 momentos).
Barra de progresso de scroll · H1 palavra a palavra + sublinhado desenhado · spotlight + parallax 3D das cartas no hero (so ponteiro fino) ·
marquee de logos (pausa no hover) · franja de modulos clicavel (abre a aba correspondente) · sublinhado laranja desenhado nos H2 ·
dores com "carimbo" do X · abas com autoplay e barra de progresso (para ao interagir, pausa no hover/foco) · coreografia da arte de cada painel
(linhas, bolhas com "digitando", barras crescendo, grafico desenhado, calendario) · contadores das cifras · hover nos depoimentos/cifras ·
CTA fixo no mobile (some ao chegar no form). Tudo desligado com prefers-reduced-motion; sem JS o conteudo fica visivel.

## v6 (2026-10-08) — estilo guillaumezhu.com

Reescrita completa (v5 brutalista/clean + blur alejandroha ficou no historico da sessao). Hero e CTA final em moldura arredondada com
gradiente fluido animado (blobs roxo/laranja/rosa + grao), cubo 3D com os 5 modulos girando com o scroll (+ parallax do ponteiro), nav em pilula
de vidro que troca para clara apos o hero, H1/H2 com letras "em escada" assentando com o scroll, secao de modulos fixa (sticky) com 5 cartas
distribuidas em leque conforme o scroll (clicaveis, abrem a aba), abas com autoplay, contadores, marquee, CTA fixo no mobile.
Sem libs externas. prefers-reduced-motion: tudo estatico (cartas em grade, letras no lugar).

## v7 (2026-10-08) — minimal premium + graficas reais

Fonte gerada por script (`build_v7.py` + `v7.css` + `v7.js`, fora do repo, na scratchpad da sessao) — o `index.html` e o artefato final.
Tema escuro premium (#0B0710, hairlines, League Spartan 300/400), laranja so como acento. Graficas inline SVG/HTML com dados ficticios
verossimeis: volume de mencoes 30 dias (tooltip interativo com variacao vs. periodo anterior, linha desenhada), donut de sentimento (hover),
alerta de crise, contador ao vivo, termos em alta, bandeja com SLA em contagem regressiva + resposta de IA digitando, KPIs + barras,
share of voice, calendario com status. Revelacao de titulos por palavra (mascara), sempre completa. Cartas do deck com miniaturas de dashboard,
brilho que segue o cursor e parallax interno. Bug corrigido: autoplay das abas fazia scrollIntoView e puxava a pagina no mobile.

## v8 (2026-10-08) — replica da UI Buzzmonitor

Fonte: `build_v8.py` + `screens_v8.py` + `v7.css` + `v8.css` + `v8.js` (scratchpad da sessao). Telas renderizadas em largura fixa (860/640px) e escaladas
via `--k` (JS `fit()`), para ficar identicas em qualquer viewport. Icones de redes reais copiados para `assets/redes/` (de outras LPs Buzzmonitor).
Bugs corrigidos: classe `.live` colidia com o deck (agora `.is-pinned`); `.st` (status) colidia com stair (agora `.stair`); grid min-content com telas escaladas (`minmax(0,…)`);
`.panel p` vazava cor clara para os titulos dos widgets.

## (substituido) Hero com laptop fotografica (2026-10-08)

`assets/laptop-mockup.png` = `plataforma-completa-para-dados/assets/dashboard-laptop.png` com a tela original apagada (PIL). O dashboard HTML (860x545) e
projetado sobre a tela da foto via homografia -> `matrix3d` (JS `mapLaptop()`, cantos da tela medidos em pixels: TL 339.9,38.5 · TR 888,32.2 · BL 306.8,403.9 · BR 858.8,438.2).
Reflexo de vidrio via `.lap__glare` com clip-path no mesmo quadrilatero.

## Hero com MacBook 3D (2026-10-08)

Substitui a foto: MacBook modelada em CSS 3D (base com espessura, teclado com teclas, trackpad, alto-falantes, dobradica, tampa com face de tela e face de
aluminio). Comeca fechada; ao entrar na viewport a tampa gira de -90deg a 10deg (2s), a tela "liga" (flash + fade) e entao os graficos animam.
Parallax do ponteiro e leve giro com o scroll no rig. `assets/laptop-mockup.png` removido (nao usado).

## Revertido (2026-10-08)

A pedido do usuario, o hero voltou ao estado anterior aos mockups de laptop (CSS, foto e 3D): dashboard direto no hero com inclinacao 3D no scroll. Versao 3D guardada na scratchpad (`*.mac.bak`).

## Clic em "Modulos" (2026-10-09)

Link do header `#modulos`: rola ate o topo da secao e distribui as 5 cartas automaticamente (2,4 s), independente do scroll. Navegacao normal continua com as cartas acompanhando o scroll. O estado automatico vale enquanto o usuario fica na secao; ao sair, volta o modo scroll.

**Form provider:** Jotform (2026-10-15) — form LATAM `241825239057661` (mesmo de `plataforma-completa-social-media-latam` e `plataforma-integral-social-media`).

## Form no hero + logos de clientes (2026-10-15)

- Hero agora: copy | formulario (card branco, `#demo`); dashboard animado em linha propria a largura total abaixo, ainda dentro do bloco escuro do hero.
- CTA do hero removido (o form esta ao lado). Secao final (`#cierre`) virou CTA centralizado que sobe para `#demo`. CTA fixo mobile some ao chegar no `#cierre`.
- Pontos coloridos da prova social -> logos de clientes (Coca-Cola, Nubank, Uber) em circulos brancos sobrepostos com anel na cor do fundo. Assets em `assets/logos-clientes/`.

- 2026-10-15: removidos do hero o dashboard animado e os cards AI Insights / Alerta de crise (pedido do usuario). Hero = copy | formulario.

- 2026-10-15: slug renomeado `todo-en-uno-premium-latam` -> `todo-en-uno` (pedido do usuario). Destino: content.buzzmonitor.com/todo-en-uno

## 7 modulos + navegacao das abas (2026-10-15)

- Deck e abas com 7 modulos: novos 06 MCP (tela estilo Claude consultando Buzzmonitor) e 07 Trends (tela Trends: temas em alta com sparklines, sentimento, quem esta falando).
- "Como funciona": dica "Elige un modulo..." (mobile: "Toca... o desliza"), botoes anterior/seguinte com contador 01/07, ponto pulsante na proxima aba ate o usuario interagir, swipe no mobile, abas com scroll horizontal.
- Deck: espacamento e tempos de distribuicao genericos por N cartas. OG regenerada com os 7 modulos.

- 2026-10-15: deck no mobile virou pilha (cada carta entra sozinha e fica inteira na frente, anteriores atras como baralho) + pontos de progresso; CTA fixo some dentro do deck. Desktop segue em leque.
- 2026-10-15: cartas do deck reordenadas (numero + titulo em cima, tela no meio, descricao embaixo). Desktop: leque escala pela altura disponivel, sem corte embaixo em notebooks baixos. Mobile: titulo das cartas de tras some na pilha.
- 2026-10-15: mobile ganha respiro abaixo da descricao das cartas; desktop com entrelinha menor na descricao (1.3).
- 2026-10-15: desktop, entrada das cartas mais espacada (intervalo maior entre cartas, track 350vh, auto-deal 2,9s) pra dar tempo de ler cada uma.
- 2026-10-15: desktop, entrada das cartas ainda mais lenta (track 430vh, auto-deal 3,6s) e leque ancorado logo abaixo do titulo do bloco (sem margem entre titulo e cartas).
- 2026-10-15: descricao das cartas maior (desktop 14px, mobile 15px); carta 07 agora diz "Temas en tendencia".
- 2026-10-15: "Temas en alza" -> "Temas en tendencia" tambem na tela e no texto do painel Trends; entrelinha da descricao das cartas no desktop 1.2.
