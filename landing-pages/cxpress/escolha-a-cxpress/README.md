# LP Cxpress — escolha-a-cxpress

Reprodução otimizada da página `https://home.cxpress.io/escolha-a-cxpress` (WordPress, plugin
`cxpress-campaign-pages`) como LP estática no pipeline do repo.

- **Marca / região:** Cxpress · Brasil (PT-BR)
- **Domínio de destino:** `content.cxpress.io/escolha-a-cxpress` (guarda-chuva, deploy via CI)
- **Estágio de funil:** BoFu, tráfego de campanha Google Search (intenção de compra)
- **Formulário:** Jotform `261034073026647` (o mesmo da LP `planos`), embed `jsform` oficial
- **Status:** pronta para revisão. **Não está no `manifest.json`** — não vai pro ar até rodar
  `/lp-publicar cxpress escolha-a-cxpress content.cxpress.io`.

---

## 1. O que mudou em relação à página original

### Velocidade

| | Original (WordPress) | Esta LP |
|---|---|---|
| HTML | 257 KB (33 KB gz) | 52 KB (12 KB gz) |
| Fontes | 4 famílias do Google Fonts (Open Sans, Roboto, Source Sans Pro, Nunito Sans) com **todos** os pesos e itálicos, mais Material Icons, servidas de `fonts.googleapis.com` + `fonts.gstatic.com` | 2 arquivos `woff2` variáveis **self-hosted** (75 KB), com `preload`. Zero conexão a terceiros no caminho crítico |
| Tabela comparativa | 3 imagens (WebP de 163 KB + 38 KB + 32 KB, uma por breakpoint) | `<table>` em HTML, 0 KB de imagem |
| Ilustrações | PNG e GIF (um GIF de 100 KB na seção de canais) | WebP redimensionado; os dois blocos animados viraram composição em CSS (0 KB) |
| DOM | Blocos de texto duplicados desktop/mobile | Um DOM só, responsivo por CSS |
| CSS/JS | 1 CSS + 2 JS externos + CSS inline gigante | Todo o CSS inline no `<head>`; 1 script próprio de ~30 linhas |
| Peso da página | mais pesada e com `load` medido em **~6 s** | **98 KB acima da dobra**, 280 KB a página inteira (fora o iframe do Jotform) |

Outras decisões de performance:

- `loading="lazy"` + `decoding="async"` em tudo abaixo da dobra; `fetchpriority="high"` só no logo do hero.
- `width`/`height` explícitos em toda imagem (CLS zero).
- `preconnect` para `form.jotform.com`, que é o único terceiro do caminho de conversão.
- LCP é texto (o H1), não imagem.

### Conversão (campanha Google Search)

1. **Formulário centralizado na primeira seção** (pedido do briefing). Override consciente da
   GUIDELINES §10, que manda form na 4ª seção ou na última em BoFu. Justificativa: tráfego de
   Search já chega com intenção declarada, e a página original também abria com o formulário.
   O argumento completo (comparativo, prova, FAQ) continua abaixo, e o CTA final devolve para
   o mesmo formulário.
2. **Barra fixa de CTA no mobile** ("Contratar a Cxpress" + WhatsApp). Tráfego pago entra e sai
   rápido no celular; a barra mantém a conversão a um toque em qualquer ponto da rolagem.
3. **Saídas de alta intenção**: WhatsApp no topo, no fim do comparativo, no CTA final e no rodapé,
   mais telefone clicável. Quem veio de Search comparando fornecedor costuma querer falar agora.
4. **FAQ com `FAQPage` no JSON-LD**, respondendo as objeções que aparecem na busca (preço, canais,
   IA, implementação, suporte, atuação fora do Brasil). Também abre caminho para rich result.
5. **Pacote SEO completo** que a página original não tinha: `og:title` e `og:description` estavam
   **vazios** no WordPress, e não havia JSON-LD.
6. **`user-scalable=no` removido** do viewport. A original bloqueia o pinch-zoom, o que reprova
   em acessibilidade e é penalizado no relatório de experiência da página.
7. **Correções de texto** herdadas da original: "Agendar demontração" → demonstração,
   "custo beneficio" → custo-benefício, "Tempo de respostaro" → Tempo de resposta.

### Fidelidade ao hero original (ajuste pedido pelo Victor)

- Linha acima do H1 voltou a ser **"O melhor custo-benefício do mercado"**, em laranja (a original
  escreve "custo beneficio", sem hífen e sem acento).
- **"atendimento"** no H1 em `#4a69bd`, como na original.
- Selo **"Conecte-se à Cxpress"** abaixo do formulário, em laranja com o check. O check era um GIF
  na original; aqui é um SVG desenhado por `stroke-dashoffset`, sem bytes de imagem, com
  `prefers-reduced-motion` respeitado. O selo também virou âncora para o comparativo.
- **Grafismos laterais**: composição de 4 pílulas da marca (laranja, royal, âmbar, laranja)
  sangrando pelas bordas do hero, em cor cheia, feitas em CSS. Escalam em telas médias e somem
  abaixo de 860px, onde invadiriam o texto.

**Sobre o laranja e o contraste.** O laranja da marca (`#ef863c`) em texto sobre fundo claro dá
2,6:1 e reprova AA (GUIDELINES §7 exige 4,5:1). Então ele foi separado em dois usos:

| Token | Onde entra | Contraste |
|---|---|---|
| `--orange` `#ef863c` | preenchimentos: botão primário, selo do check, pílulas decorativas | botão usa texto navy, 5,2:1 |
| `--orange-ink` `#a94d07` | laranja como **texto**: overline do hero, "Conecte-se à Cxpress" | 5,6:1 no branco, 5,2:1 no lilás do hero |

Assim a página ganhou presença de laranja sem nenhum bloco reprovando acessibilidade. O CTA
primário laranja usa texto navy pelo mesmo motivo (laranja com texto branco dá 2,6:1).

### Tabela comparativa

- Virou `<table>` semântica com `caption`, `scope="col"`/`scope="row"` e legenda visível.
  Google lê, leitor de tela lê, e dá para copiar o conteúdo.
- Coluna da Cxpress destacada com tint da marca e o logo no cabeçalho.
- Marcadores **na paleta da marca** (royal / âmbar / cinza), não verde e vermelho: o brand da
  Cxpress proíbe verde (`generation-rules.json → neverDo`), e o par âmbar/cinza lê como avaliação
  em vez de acusação, que é o tom certo para um comparativo assinado pela própria marca.
- Cada marcador vem acompanhado do rótulo em texto ("Sim", "Limitado", "Alto custo"), então a
  informação não depende de cor.
- No mobile a tabela vira um card por critério, com o nome da coluna no `::before`. A original
  simplesmente trocava por uma imagem menor, ilegível no celular.
- Fecha em CTA: **"Contratar a Cxpress"** + "Falar no WhatsApp".
- Nota de rodapé ("Comparativo qualitativo elaborado pela Cxpress. Concorrentes identificados por
  siglas.") para deixar explícito que a avaliação é da marca.

**Marcadores normalizados (aprovado pelo Victor).** A imagem original usava marcadores diferentes
para o mesmo rótulo, o que num comparativo assinado pela marca o leitor detecta em segundos e lê
como viés. Agora **cada rótulo tem um marcador só**:

| Rótulo | Antes | Agora | Onde mudou |
|---|---|---|---|
| Básico | ✓ em 4 células, ! em 1 | **! parcial** nas 5 | OCD em *Suporte local*, *Onboarding* e *Clareza*; CHG em *Onboarding* |
| Técnico | ✗ em 3 células, ! em 1 | **! parcial** nas 4 | ZDK em *Onboarding*, *Clareza* e *Facilidade de uso* |
| Lento | ✗ em 1 célula, ! em 1 | **! parcial** nas 2 | ZDK em *Tempo de resposta* |

O critério da normalização é a própria legenda: "Não atende" (✗) é para ausência. "Básico",
"Técnico" e "Lento" descrevem um critério **atendido com limitação**, então são "Parcial ou
limitado". Ficaram em ✗ apenas "Não" (canal ausente) e "Alto custo" (que nega o próprio critério
de custo-benefício).

O argumento não enfraquece: a coluna da Cxpress continua sendo a única com ✓ em todas as linhas, e
uma tabela em que os concorrentes aparecem honestamente como "parcial" sustenta melhor a comparação
diante de um comprador que está justamente pesquisando fornecedor.

Para reverter qualquer célula, é trocar `mk--part` por `mk--yes` / `mk--no` na célula.

---

## 2. Estrutura

0. **Menu** — só a logo, centralizada, ancorando `#topo`.
1. **Hero** (`#topo-hero`) — overline, H1 com a dor, subtítulo, **formulário
   centralizado** (`#form`), faixa de 3 provas.
2. **Comparativo** (`#comparativo`) — selo "Conecte-se à Cxpress", legenda, tabela,
   fecho e CTA duplo.
3. **Por que escolhem** — 4 números de prova (em CSS) + os 5 bullets da original.
4. **Módulos** — os 5 blocos da original, alternando texto e visual.
5. **Clientes** — esteira infinita com 42 logos.
6. **FAQ** — 6 perguntas em `<details>`.
7. **CTA final** — volta para o formulário, WhatsApp e telefone.
8. **Rodapé** — logo, linha legal e redes sociais.
9. **Botão flutuante** — abre o formulário da campanha num modal.

---

## 3. Assets

| Arquivo | Origem | Observação |
|---|---|---|
| `logo-cxpress.png`, `icon-whatsapp.png` | LP `planos` | |
| `clientes/cliente-01..42.png` | LP `banimento-de-whatsapp` | 42 logos da esteira, 308 KB no total; o build deduplica no destino |
| logo do rodapé | `brand/cxpress/assets/logos/logo-reversed.svg` | referenciado por `../../brand/...`, o build reescreve para `/assets/cxpress/logos/` |
| `mockup-tickets.webp`, `mockup-dashboard.webp`, `card-api-chatgpt.webp` | mirrors da página original | redimensionados e reconvertidos |
| `fonts/*.woff2` | Google Fonts, subset latin | Open Sans e Source Sans 3, variáveis |
| `og-escolha-a-cxpress.png` | `assets/og-template.html` via `render_og.py` | 1200×630 |

Os dois blocos que eram GIF/imagem na original ("canais no mesmo painel" e "fila de tickets")
são markup + CSS, sem imagem. O mesmo vale para o selo "Conecte-se à Cxpress": o GIF
do anel laranja virou SVG desenhado por `stroke-dashoffset`.

Saíram com a troca do rodapé e da seção de clientes (não são mais referenciados):
`logo-cxpress-branco.png`, `canais-integrados.webp`, `clientes-cxpress.webp`,
`icon-footer-1.png`.

---

## 4. Checks rodados

```
grep -c "—" index.html                     # 0
grep -c 'meta property="og:' index.html    # 10
grep -c 'meta name="twitter:' index.html   # 4
JSON-LD                                    # parseia (Organization + WebPage + SoftwareApplication + FAQPage)
py landing-pages/build/check_mobile_type.py --port 8123 landing-pages/cxpress/escolha-a-cxpress
                                           # h1=34 corpo=17 min=14, único overflow é o skip-link (fora da tela por design)
py landing-pages/build/build_umbrella.py   # 0 avisos, todos os assets resolvidos
```

Contraste conferido nos pares críticos: o CTA laranja usa **texto navy** (5,2:1), não branco
(2,6:1, reprova AA). O gradiente do CTA final foi escurecido para o texto claro passar em 4,5:1.

---

## 5. Jotform "cortado no celular": era artefato da emulação, não bug da página

Durante a construção, o Jotform embedado aparecia **cortado à direita** na emulação de celular
(375px), aqui e também na LP `content.cxpress.io/planos` em produção. O teste decisivo fechou o
caso: um `<iframe>` do formulário com **largura lógica de 700px**, reduzido por `transform` para
não alargar a viewport, continuou cortado **e com os dois botões lado a lado** (o layout de
desktop). Ou seja, o formulário não estava respondendo à largura do iframe em nenhum valor: estava
simplesmente renderizando a versão desktop.

Isso é o comportamento conhecido do Chrome: a **emulação de dispositivo do DevTools não se propaga
para iframes cross-origin** (out-of-process). `form.jotform.com` é outro domínio, então recebe as
métricas reais de desktop, monta o layout de desktop e vaza para fora do iframe estreito. Num
celular de verdade o iframe recebe métricas de celular e o formulário monta a versão mobile, que é
a mesma que aparece perfeita ao abrir `form.jotform.com/261034073026647` direto no navegador.

Duas evidências de apoio: o formulário fora de iframe na mesma largura mede `.form-all` = 359px e
não vaza nada, e a LP `/planos` está no ar com esse embed captando leads.

**Resultado:** o workaround que eu tinha montado (wrapper `.jotform-fit` + JS de escala) foi
**removido**, porque corrigia um problema que não existe fora da emulação e ainda podia encolher o
formulário sem motivo num aparelho real. Ficou só o embed canônico do `lp-integrar-form`.

**O que permaneceu, por ser ganho independente:** no celular o card do formulário ocupa a largura
cheia da tela. O Jotform já tem margem interna própria, então somar o padding do card por cima só
espremia os campos.

Ainda assim, é um teste de 30 segundos: ao abrir a LP publicada, dar uma olhada no formulário pelo
celular. Se algum dia aparecer cortado num aparelho real, o conserto é a largura do formulário no
painel do Jotform, que resolve todas as LPs de uma vez, e não CSS LP a LP.

## 6. Pendências antes de publicar

- [ ] Decidir o destino da URL antiga: `home.cxpress.io/escolha-a-cxpress` deve receber um 301
      para a nova, senão as duas competem no índice e o anúncio precisa apontar para a nova.
- [ ] Atualizar a URL final do anúncio no Google Ads para `content.cxpress.io/escolha-a-cxpress`.
- [ ] Rodar `/lp-publicar cxpress escolha-a-cxpress content.cxpress.io` (entra no manifesto e o
      CI deploya). **Nunca deployar à mão.**
- [ ] Depois de publicar, adicionar a linha em `landing-pages/catalogo/lps-cxpress.md`.

---

## 7. Alinhamento com a `banimento-de-whatsapp` e a `telefonia-ia-latam`

Rodada de ajustes pedida pelo Victor, tomando a `banimento-de-whatsapp` como
página-padrão e a `telefonia-ia-latam` como origem do desenho.

| # | Ajuste | Referência |
|---|---|---|
| 2 | Rodapé enxuto (logo + linha legal + 4 redes, alvos de 44 px) no lugar do rodapé k2x | `banimento-de-whatsapp` |
| 3 | H1 quebra depois de "atendimento", como na original. Exigiu abrir o `.hero__head` de 820 px para 980 px: a 2ª linha pede 949 px no topo do `clamp` | mirror WordPress |
| 3 | Selo "Conecte-se à Cxpress" foi do fim do hero para o **topo do comparativo**, com o check **acima** do texto e o anel laranja **vazado** (era círculo cheio com traço branco) | mirror WordPress |
| 4 | Seção de clientes virou esteira infinita de 42 logos, com pausa no hover | `banimento-de-whatsapp` |
| 4 | Checagem dos títulos: 9 títulos, nenhum duplicado (o do modal foi renomeado para "Fale com um especialista pelo WhatsApp") | — |
| 5 | Menu: link "Falar no WhatsApp" removido, logo centralizada ancorando `#topo` | — |
| 6 | Botão flutuante do WhatsApp abrindo o formulário num modal | `banimento-de-whatsapp` |

### Cuidados que isso trouxe

- **Dois embeds do mesmo Jotform** (261034073026647: o do hero e o do modal). O resizer
  do `jsform` acha o iframe pelo id do FORMULÁRIO, então um redimensionaria o outro.
  Um listener registrado **antes** do embed do hero aplica a altura no iframe certo e
  barra a mensagem ali (mesma solução da `banimento-de-whatsapp`).
- **`.jotform-embed` com margem negativa no mobile** foi escopado para
  `.form-card .jotform-embed`, senão vazava para dentro do modal.
- **Botão flutuante x barra fixa do mobile**: abaixo de 860 px o botão sobe para
  `bottom: calc(94px + safe-area)` para não cair sobre a `.sticky-cta`.
- **Selo abaixo da dobra**: o traço do check só anima em `.is-visible`, senão a
  animação terminaria antes de alguém ver. Com `.no-reveal` e no `<noscript>` o selo
  aparece desenhado (GUIDELINES §4).
- **Esteira e `prefers-reduced-motion`**: a regra global zera `animation-duration` e a
  esteira saltaria para -50%; aí ela recebe `animation: none`.

### Deliberadamente diferente da `banimento-de-whatsapp`

- A seção de clientes ficou com fundo off-white (lá é branco) e manteve o H2 no
  tamanho display desta LP: lá a faixa é uma tira fina colada no hero, aqui é uma
  seção de prova com headline própria entre duas seções brancas (GUIDELINES §1).
- O rodapé novo **não traz** o CNPJ/endereço da Elife nem os links de
  "Condições gerais de uso" e "Políticas de privacidade", que existiam no rodapé k2x.
  A `banimento-de-whatsapp` também não traz. **Decidido pelo Victor em 2026-09-04:
  segue sem os links legais no rodapé.**

---

## 8. Segunda rodada (2026-09-04, pós-publicação)

Ajustes pedidos pelo Victor depois de ver a página no ar, com o full-page capture da
página original (`01 - Escolha a Cxpress/FireShot Capture 009`) como referência.

| Ajuste | Detalhe |
|---|---|
| Trust item removido | Saiu "Suporte em português, com time no Brasil"; a faixa ficou com 2 itens |
| Overline do comparativo removido | Saiu "Compare antes de contratar"; o `.cmp__head` ficou com H2 + lead |
| Selo menor e em loop | 58px → 40px. O loop agora copia o GIF original (`4d9d0c6bf57aff01cc6e.gif`, 2020ms): o **anel fica inteiro o tempo todo** e só o **check** apaga e redesenha (2,02s, infinito) |
| Menos respiro entre seções | Ver tabela abaixo. O vão da faixa de provas até o selo caiu de 206px para 146px, e a página encurtou ~430px no total |

### Paddings de seção

| Seção | Antes | Depois |
|---|---|---|
| `.hero` (base) | 96px | 64px |
| `.cmp` | 110 / 96 | 64 / 72 |
| `.why` | 96 | 72 |
| `.mods` | 110 / 96 | 76 / 72 |
| `.clientes` | 88 | 66 |
| `.faq` | 96 | 72 |
| `.cta-final` | 96 | 76 |
| mobile (`≤860px`) | 70-74 | 48-56 |

> **Desvio consciente do GUIDELINES §2.** A regra pede mínimo de 120px no desktop e 80px
> no mobile. Estes valores ficam abaixo dos dois por **pedido explícito do Victor**
> (2026-09-04), depois de ver o vão entre a faixa de provas e o selo na página no ar.
> Não "corrigir de volta" sem falar com ele. Vale notar que os valores anteriores
> (96-110px) já estavam abaixo do mínimo do §2.

### Sobre o estado-base do selo

Com o loop, o estado-base de anel e check passou a ser **desenhado** (`dashoffset: 0`) e a
animação virou um extra que roda em `.is-visible`. Antes o base era "apagado" e só a
animação revelava o selo: se o IntersectionObserver não disparasse, o selo ficava
invisível. Agora sem JS, sem observer ou com `prefers-reduced-motion` ele aparece
inteiro (GUIDELINES §4). O `<noscript>` deixou de precisar forçar `dashoffset`.

### Pendente desta rodada

**Imagem do módulo "Gerencie com eficiência por meio de dashboards".** Na página original
esse módulo usa um **painel escuro com cards de KPI flutuando** ("Tempo médio de espera",
"Total de consumidores", "Taxa de desistência" etc.), e o monitor claro que a nossa LP usa
(`mockup-dashboard.webp`) aparece lá na seção "Por que as empresas escolhem". Esse painel
escuro **não foi encontrado** na pasta de assets do mirror: não há vídeo (`.mp4`/`.webm`) e
nenhum dos 9 GIFs nem o asset escuro mais próximo em proporção (`89865d70476a5e6f931f.webp`,
que é line-art decorativo) correspondem. Provavelmente é composto pelo builder do
WordPress (div escura + cards soltos) ou não entrou no dump do mirror. **Aguardando o
arquivo do Victor.**

---

## 9. Terceira rodada (2026-09-04)

| Ajuste | Detalhe |
|---|---|
| Só o botão pulsante para WhatsApp | Saíram os 3 CTA "Falar no WhatsApp" (comparativo, CTA final e barra fixa do mobile). O único caminho de WhatsApp agora é o botão flutuante. As classes `.btn--ghost` e `.btn--ghost-light` ficaram sem uso e saíram do CSS |
| H1 | "cresce" subiu para a 1ª linha: **"Seu atendimento cresce."** / **"Sua operação acompanha?"**. O royal, que era só em "atendimento", passou a cobrir "atendimento cresce" e "operação acompanha" |
| Caixa do formulário centralizada | `text-align:center` no `.form-card`; o `.jotform-embed` recebe `text-align:left` para o formulário não herdar o centro |
| Menu com efeito vidro | O menu saiu do hero e virou `<header class="topbar">` **antes do `<main>`**, `position:sticky` com `backdrop-filter: saturate(180%) blur(14px)` sobre `rgba(255,255,255,.72)`. A logo agora aponta para `#form` |

### Por que a barra ficou fora do `.hero`

O `.hero` tem `overflow:hidden` (por causa das pílulas decorativas), e `position:sticky`
dentro de um ancestral com `overflow:hidden` **para de colar** assim que a seção sai de
cena. Como `<header>` irmão do `<main>`, a barra cola em qualquer posição de scroll
(medido: `top: 0` no topo, no meio e no fim da página).

Camadas: barra `z-index: 75`, acima do botão flutuante (70) e abaixo do modal (90).
Há um `@supports not (backdrop-filter)` que sobe a opacidade do fundo para `.94`, senão
em navegador sem suporte a logo ficaria sobre o texto que passa atrás.

### Efeitos colaterais tratados

- **Pílulas decorativas subiram 80px** (`top` de 108/132/232/250 para 28/52/152/170).
  Sem a barra dentro do hero o conteúdo subiu ~102px, e sem isso elas ficariam baixas
  em relação à headline. `.hero` padding-top foi de 26px para 40px.
- **`scroll-margin-top` do `.form-card`** foi de 20px para 96px (76px no mobile), senão
  a âncora `#form` (que a logo usa) paravam com o título do card atrás da barra.
  Medido: card para em 96px, título em 131px, base da barra em 77px.
- **`.hero :focus-visible` saiu da regra de outline branco.** O hero tem fundo claro, e
  o outline branco ali era invisível. Bug pré-existente, corrigido de passagem porque a
  regra estava sendo editada de todo jeito.
- **Barra fixa do mobile ficou com 1 botão** ("Contratar a Cxpress"). O botão flutuante
  segue em `bottom: calc(94px + safe-area)` para não cair sobre ela (medido: não se
  sobrepõem a 375px).

### A conferir com o Victor

A copy do CTA final ainda termina com **"Se preferir, fale agora pelo WhatsApp."**, mas o
botão de WhatsApp que ficava ao lado dela saiu. A frase não virou mentira (o botão
flutuante está na tela, pulsando), mas ficou sem um alvo adjacente. Não mexi porque
é decisão de copy (GUIDELINES §5).
