# LP Cxpress — chatbot-whatsapp

**Importada em:** 2026-09-04
**Origem:** projeto Vercel solo [`cxpress-chatbot-whatsapp.vercel.app`](https://cxpress-chatbot-whatsapp.vercel.app/) — a LP já estava no ar fora do guarda-chuva. Pedido do Bruno: colocá-la num domínio da Cxpress.
**Região:** brasil (pt-BR) · **Domínio alvo:** `content.cxpress.io` (guarda-chuva migrado pro CI)
**URL de produção:** `https://content.cxpress.io/chatbot-whatsapp`
**Form provider:** Jotform `261034073026647` — o mesmo das LPs irmãs `whatsapp-business` e `banimento-de-whatsapp`. Dois pontos de captura: a seção "Solicite uma apresentação gratuita" (jsform) e o modal do botão flutuante (iframe com `data-src`, carregado só ao abrir)
**Tracking:** GTM-T4XDWHL3 (padrão Cxpress BR, `brand/cxpress/tracking.json`) — **adicionado na importação**; a versão solo não tinha container nenhum

## O que mudou da versão solo para esta

Nenhuma palavra de copy foi reescrita — a copy publicada está transcrita em `copy.txt`. As mudanças são de infraestrutura, para a página se comportar como as vizinhas do guarda-chuva:

| # | Mudança | Por quê |
|---|---|---|
| 1 | GTM-T4XDWHL3 no `<head>` + `noscript` no topo do `<body>` | A versão solo não tinha tracking: a página não gerava dado nenhum. Container de BR, como manda `brand/cxpress/tracking.json` |
| 2 | Logos via `../../brand/cxpress/assets/logos/` | Antes eram URLs absolutas para `https://content.cxpress.io/assets/cxpress/logos/...` — funcionavam, mas por acidente. O `build_umbrella.py` reescreve a referência de brand para `/assets/cxpress/` no deploy |
| 3 | 7 imagens baixadas do espelho WordPress para `./assets/` | Vinham de `home.cxpress.io/wp-content/plugins/cxpress-campaign-pages/mirrors/assets/{hash}.webp`. Dependência externa com nome de hash: se o plugin do WP mudar, a LP perde as imagens. Agora são locais e com nome legível |
| 4 | `<link rel="canonical">`, `robots`, `author`, favicon, Open Graph e Twitter Card | A versão solo não tinha nenhum deles. O canonical aponta para `content.cxpress.io/chatbot-whatsapp`, que passa a ser a URL oficial |
| 5 | `assets/og-chatbot-whatsapp.png` (1200×630) | Gerado por `assets/render_og.py` a partir de `assets/og-template.html`, no mesmo padrão da LP irmã `whatsapp-business` (GUIDELINES §18) |

## 2ª rodada (2026-09-04, olhando a página no ar)

Pedidos do Bruno com base no print da página de origem (`home.cxpress.io/app-whatsapp`). Nenhuma palavra de copy reescrita.

| # | Pedido | O que foi feito |
|---|---|---|
| 1 | Centralizar o H1 e jogar os assets para as laterais, como no print | Hero deixou de ser grid de 2 colunas e virou coluna única centrada (overline, H1, apoio, CTA e print da plataforma empilhados). H1 com `max-width:26ch` + `text-wrap:balance`; o print da plataforma cresceu de 480 para 860 px, já que agora ocupa a largura toda |
| 2 | Assets nas laterais | Dois clusters de 4 pílulas (amarelo, laranja, azul, navy) em SVG inline, um em cima à esquerda e outro espelhado mais abaixo à direita, no arranjo do print. Cores por token (`--warning`, `--accent`, `--primary`, `--primary-dark`), aplicadas por CSS e não por atributo `fill` |
| 3 | Excluir os big numbers | Seção `+220% / Até 15x / 98%` removida inteira — markup, CSS e o JS do contador animado, que só ela usava |
| 4 | Excluir "Fale com um de nossos especialistas no WhatsApp agora mesmo!" | Faixa verde removida (markup + CSS) |

**A nota de fonte não foi embora com os big numbers.** Ela explicava o `*` que também marca três números da faixa de resultados do topo (14%, 9%, 45%); deixar os asteriscos sem nota nenhuma transformaria aqueles números em afirmação sem fonte. A nota passou para o rodapé da própria faixa de resultados.

**Onde os clusters somem.** Abaixo de 1100 px eles ficam `display:none`: nesse ponto a coluna de texto centrada ocupa a largura toda e as pílulas passariam por cima do H1. Verificado a 1440, 1200, 1024 e 375 px — sem colisão com o H1 e sem scroll horizontal em nenhum deles.

## 3ª rodada (2026-09-04, faixa de resultados)

Pedido do Bruno: transformar a faixa de resultados do topo (14%, 9%, 25%, 45%) em big numbers de verdade — números grandes, cor moderna, entrada em cascata, contagem animada e hover de card.

| Item | Antes | Agora |
|---|---|---|
| Tamanho do número | `clamp(32px, 3vw, 42px)` | `clamp(46px, 5.6vw, 76px)`, peso 800, `letter-spacing` -.035em |
| Cor | sólida, `--primary-dark` | gradiente no próprio glifo (`background-clip:text`), um por número |
| Bloco | texto solto sobre faixa branca | card branco com borda, raio e `--shadow-card`, sobre faixa `--tint` |
| Entrada | `.reveal` com `data-step` genérico | cascata por posição no grid (0 / .12 / .24 / .36s) |
| Contagem | não tinha | sobe de 0 até o valor em 2s, uma vez, ao entrar na tela |
| Hover | não tinha | `translateY(-8px)` + `--shadow-card-hover` |
| Grid | 4 colunas, 2 abaixo de 760px | 4 / 2 (≤900px) / 1 (≤560px) |
| Apoio | 15px | 16px, `text-wrap:balance` |

### Três decisões que fogem do pedido literal

**Gradiente não é "azul para roxo".** Roxo não existe na paleta da Cxpress. Cada número usa um gradiente **dentro da própria família de cor** da marca: 14% e 9% em azul (`--primary` → `#1F3E8F`, `--primary-deep` → `--primary-dark`), 25% em verde WhatsApp (`--wa-ink` → `#0E5C34`) e 45% em laranja escuro (`--accent-ink` → `#7A3806`).

**Gradiente monocromático, não entre matizes.** A primeira versão ia de laranja/verde até o navy; no meio do glifo isso vira um marrom sujo. Ficando dentro da família, a cor sai limpa.

**Nenhum stop usa o laranja e o amarelo de preenchimento.** `--accent` (#EF863C) dá 2,58:1 em branco e `--warning` (#F1A908) dá 2,02:1 — abaixo do 3:1 mínimo até para texto grande. Por isso entrou o token `--accent-ink` (#A94D07, 5,60:1), irmão do `--wa-ink` que já existia. Todos os oito stops usados ficam acima de 4,5:1 em branco e no `--tint`.

### Detalhes de implementação

- O gradiente só é aplicado dentro de um `@supports (background-clip:text)`. Sem essa guarda, um navegador que ignore a propriedade renderizaria o número transparente — ou seja, invisível. O fallback é `--primary-dark` sólido.
- A cascata vem de `nth-child` na seção, não do `data-step` global. Dentro de um grid, o `data-step` calculado sobre a ordem global dos `.reveal` entrega o atraso embaralhado (mesmo bug documentado na LP irmã `whatsapp-business`).
- O contador respeita `prefers-reduced-motion`: com movimento reduzido o número fica direto no valor final.
- `font-weight: 900` não foi usado — a Open Sans carregada na página traz só 700 e 800; pedir 900 faria o navegador engordar a fonte por síntese.

### Verificado

1400 px (4 colunas), 768 px (2 colunas), 390 px (1 coluna) — sem scroll horizontal em nenhum, contagem partindo de 0 e cascata visualmente correta.

## 4ª rodada (2026-09-05, seção de clientes)

Pedido do Bruno: trocar a seção de clientes pela da LP `quiz-atendimento-latam` (`Más de 800 clientes confían en nosotros`), traduzida, e tirar qualquer opacidade dos logos.

| Antes | Agora |
|---|---|
| Título centrado + 5 nomes de clientes em texto (Real, Riosal, Trendtec, Boa Vontade, Netsul) | Esteira infinita com 14 logos reais + rótulo `Mais de 800 clientes confiam em nós` |
| Sem imagem nenhuma | `assets/clientes/` com os 14 PNGs |
| Nomes com `opacity:.75` | Logos com `opacity:1`, sem filtro |

**Tradução.** `Más de 800 clientes confían en nosotros` → `Mais de 800 clientes confiam em nós`. Região brasil, então não entra padrão linguístico de PT-PT/ES-LATAM; a frase é literal e já nativa em PT-BR.

**Tirei também o `grayscale`, não só a opacidade.** A LP de origem usa `filter:grayscale(1); opacity:.72` e a irmã `whatsapp-business` usa `opacity:.72; filter:saturate(.9)` — as duas metades do mesmo efeito de apagar a esteira. O pedido foi "deixe 100%", então os logos ficaram em cor cheia. **Se a intenção era manter o cinza e mexer só na opacidade, é uma linha:** devolver `filter:grayscale(1)` em `.ticker__logo`.

**Os PNGs vieram da `whatsapp-business`, não baixados da LP de origem.** Conferi por hash: os arquivos que a `quiz-atendimento-latam` serve são byte-a-byte iguais aos que já estão no repositório. Isso importa porque o guarda-chuva tem **namespace de assets compartilhado** (`/assets/cxpress/clientes/`): como `chatbot-whatsapp` vem antes de `whatsapp-business` na ordem alfabética do manifesto, as cópias desta LP é que vão pro dist. Sendo idênticas, a vizinha não muda — validado comparando os 42 logos do dist com a fonte da `whatsapp-business`.

**Animação.** Marquee de 46s, pausa no hover, `mask-image` com fade nas bordas. O bloco global de `prefers-reduced-motion` da página já congela a esteira (`animation:none!important`), deixando a primeira fila legível e parada.

### Verificado

1400 px (rótulo à esquerda + esteira à direita), 390 px (empilhado) — 14 logos carregando, nenhum quebrado, `opacity:1`, `filter:none`, sem scroll horizontal.

## 5ª rodada (2026-09-05, seção "Descubra tudo o que é possível fazer")

Pedido do Bruno: comparar as proporções das imagens da seção e corrigir. A comparação achou desproporcão **e** dois assets quebrados.

### O diagnóstico

| # | Bloco | Arquivo antigo | Dimensões | Razão | Problema |
|---|---|---|---|---|---|
| 1 | Atendimento integrado | `atendimento-integrado.png` | 880×700 | 1,26 | ilustração, razão fora da série |
| 2 | Inteligência artificial | `atendimento-ia.webp` | 219×241 | 0,91 | **badge de 219 px** esticado 2,5× numa coluna de 540 — borrado, e ainda era o bloco mais alto |
| 3 | Cadastros | `cadastros-clientes.webp` | 1779×1033 | 1,72 | ok |
| 4 | Tickets | `gestao-tickets.webp` | 566×318 | 1,78 | **frame 0 do `plataforma-canais.gif`** — tela praticamente vazia, 843 KB de nada |
| 5 | Dashboards | `dashboards.webp` | 816×458 | 1,78 | **frame escuro do `plataforma-dashboard.gif`** — borrado e ilegível |

Com `width:100%;height:auto`, essas razões davam blocos de **303 a 594 px** de altura na mesma coluna de 540 px.

Os arquivos 4 e 5 batem **pixel a pixel** com as dimensões dos GIFs de plataforma que o repositório já tem: alguém congelou um frame de cada animação na versão solo, e calhou de pegar o frame vazio num e o frame escuro no outro.

### As correções

| # | Agora |
|---|---|
| 2 | `plataforma/plataforma-chatbot-ia.gif` (786×442) — mostra a configuração do chatbot e o bot respondendo no WhatsApp, que é exatamente o que o bloco promete |
| 4 | `plataforma/plataforma-canais.gif` (566×318) — fila de tickets, canais e distribuição entre agentes |
| 5 | `plataforma/plataforma-dashboard.gif` (816×458) — painéis de métrica legíveis |

Os três GIFs vieram da LP irmã `atendimento-clinicas`, byte a byte (o namespace `/assets/cxpress/plataforma/` é compartilhado no guarda-chuva, então precisam ser idênticos — validado no dist). Os três `.webp` mortos saíram do repositório (1,4 MB).

**Moldura única.** `.feature__media` virou um painel com borda, raio e sombra, e a imagem ganhou `aspect-ratio:16/9` + `object-fit:contain`. Os cinco blocos passam a medir igual — 540×305 no desktop, 326×184 a 390 px — e nenhuma imagem distorce: a ilustração de 1,26, que é a única fora da série, encaixa centralizada.

**A proporção ficou na imagem, não no container.** A primeira tentativa pôs `aspect-ratio:16/9` no `.feature__media` e `height:100%` na imagem. Altura em porcentagem não resolve dentro de um container dimensionado por `aspect-ratio`: a imagem voltava à razão intrínseca e renderizava 538×428 dentro de um painel de 540×304, estourando o quadro (o `overflow:hidden` cortava o pé da ilustração). Com a proporção na própria `img`, não há porcentagem para resolver.

### Peso

Os GIFs somam 5,0 MB, e os assets da LP vão a 6,7 MB. Todos os cinco estão abaixo da dobra e receberam `loading="lazy"` mais `width`/`height` (que também reserva o espaço e evita salto de layout). Se o peso incomodar, o caminho é reencodar os GIFs para vídeo (`.webm`/`.mp4` em loop mudo), que cortaria isso em mais de 90% — vale como pauta separada, porque as LPs irmãs carregam os mesmos arquivos.

### Verificado

1400 px e 390 px: os cinco painéis com medida idêntica, nenhuma imagem estourando o quadro, todos os arquivos servindo 200 e sem scroll horizontal.

## 6ª rodada (2026-09-05, moldura das imagens)

Pedido do Bruno: tirar o retângulo atrás das imagens da seção de plataforma — a moldura que a rodada anterior tinha criado.

Saíram a borda, a sombra e o fundo branco do `.feature__media`. Ficou só o `border-radius` com `overflow:hidden`, e a proporção 16:9 continua na imagem. Os painéis passaram de 538×303 para 540×304 (os 2 px eram a borda).

**A remoção é total em 2 dos 5 blocos e parcial nos outros 3.** Conferido no arquivo:

| Bloco | Arquivo | Fundo do arquivo | Resultado |
|---|---|---|---|
| 1 Atendimento integrado | `atendimento-integrado.png` | RGBA transparente | retângulo sumiu de vez, a ilustração senta no tint |
| 3 Cadastros | `cadastros-clientes.webp` | RGBA transparente | idem, só o mockup de laptop |
| 2 IA | `plataforma-chatbot-ia.gif` | opaco `#f2f2f2` | segue um bloco cinza claro |
| 4 Tickets | `plataforma-canais.gif` | opaco `#fcfcfc` | segue um bloco quase branco |
| 5 Dashboards | `plataforma-dashboard.gif` | opaco `#2e2e2e` | segue um bloco cinza escuro, o mais visível dos três |

Nos três GIFs o retângulo está **dentro do arquivo**, não no CSS — nenhuma regra de estilo tira aquilo. Para sumir de verdade seria preciso reexportar os GIFs com fundo transparente, e no caso do dashboard isso quebraria a legibilidade: os cards dele são claros e existem justamente por contraste com o fundo escuro. Por isso o raio de canto ficou: é o que o CSS ainda pode fazer para o bloco de cor não parecer um retângulo duro.

## Assets

| Arquivo | Onde aparece |
|---|---|
| `painel-atendimento.webp` | hero |
| `atendimento-integrado.png` | plataforma, bloco 1 |
| `plataforma/plataforma-chatbot-ia.gif` | plataforma, bloco 2 |
| `cadastros-clientes.webp` | plataforma, bloco 3 |
| `plataforma/plataforma-canais.gif` | plataforma, bloco 4 |
| `plataforma/plataforma-dashboard.gif` | plataforma, bloco 5 |
| `especialista-atendimento.webp` | faixa "Fale com um especialista no WhatsApp" |
| `clientes/cliente-*.png` (14) | esteira de clientes |
| `og-chatbot-whatsapp.png` | Open Graph / Twitter Card |
| `og-template.html` + `render_og.py` | fonte da imagem de OG (não vão pro deploy) |

## Pendências

- **Projeto solo `cxpress-chatbot-whatsapp` continua no ar.** Com a LP publicada no guarda-chuva, o ideal é apontar o solo para a URL nova (ou pausar o projeto) para não competir no índice. Precisa de decisão do Bruno/Victor — não foi mexido.
- **Sem JSON-LD.** As LPs irmãs (`whatsapp-business`) têm `Organization` + `FAQPage`. Esta tem FAQ na página mas não tem o schema. Nice-to-have para SEO, não bloqueia.
- **O `**` da faixa de resultados continua sem definição.** Depois da rodada 2 a nota de fonte (`*`) está na própria faixa, mas "Aumento da produtividade com IA generativa.**" usa um segundo nível de asterisco que nenhuma nota explica. Herdado da versão solo — precisa da fonte para fechar.
