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

## Assets

| Arquivo | Onde aparece |
|---|---|
| `painel-atendimento.webp` | hero |
| `atendimento-integrado.png` | plataforma, bloco 1 |
| `atendimento-ia.webp` | plataforma, bloco 2 |
| `cadastros-clientes.webp` | plataforma, bloco 3 |
| `gestao-tickets.webp` | plataforma, bloco 4 |
| `dashboards.webp` | plataforma, bloco 5 |
| `especialista-atendimento.webp` | faixa "Fale com um especialista no WhatsApp" |
| `og-chatbot-whatsapp.png` | Open Graph / Twitter Card |
| `og-template.html` + `render_og.py` | fonte da imagem de OG (não vão pro deploy) |

## Pendências

- **Projeto solo `cxpress-chatbot-whatsapp` continua no ar.** Com a LP publicada no guarda-chuva, o ideal é apontar o solo para a URL nova (ou pausar o projeto) para não competir no índice. Precisa de decisão do Bruno/Victor — não foi mexido.
- **Sem JSON-LD.** As LPs irmãs (`whatsapp-business`) têm `Organization` + `FAQPage`. Esta tem FAQ na página mas não tem o schema. Nice-to-have para SEO, não bloqueia.
- **O `**` da faixa de resultados continua sem definição.** Depois da rodada 2 a nota de fonte (`*`) está na própria faixa, mas "Aumento da produtividade com IA generativa.**" usa um segundo nível de asterisco que nenhuma nota explica. Herdado da versão solo — precisa da fonte para fechar.
