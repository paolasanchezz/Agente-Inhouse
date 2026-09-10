# LP — Café con Cxpress (Medellín, Sep) · ES-LATAM

Landing page de evento presencial da Cxpress em **Medellín, Colombia**, 24/09/2026, 4:00 p.m. (COT, UTC-5).
Copy em **Español Latinoamericano** (tuteo), herdada da edição de Bogotá (`../cafe-bogota-jul26/copy-fonte.md`).

## Origem do design

| Fonte | O que veio dela |
|---|---|
| [`buzzmonitor/perpetuo-monitoramento-concorrentes`](../../buzzmonitor/perpetuo-monitoramento-concorrentes/index.html) | Esqueleto, grid e animações: header sticky com CTA, hero 2 colunas (copy à esquerda + form-card flutuante à direita), seção clara com cantos superiores arredondados sobrepondo o hero, bloco de palestrante com anéis pulsantes, seção escura com marquee, CTA final centralizado com glow, footer. Reveal-on-scroll com `--d`, glows em `breathe`, seta em `nudge`, hover-lift nos cards, borda superior em `scaleX`. |
| [`cxpress/cafe-bogota-jul26`](../cafe-bogota-jul26/index.html) | Toda a copy, tom de voz e ordem de argumentação (contexto → aprendizados → caso en vivo → sobre Cxpress → fecho), mais os blocos próprios de evento presencial (mapa + endereço + countdown). |
| `brand/cxpress/` | Cores, tipografia, raios e formas. Navy `#232960` + royal `#4A69BD` + laranja `#EF863C` de acento (3 cores, GUIDELINES §1). Open Sans (títulos), Source Sans 3 (corpo), Bitter (eyebrows). |

## Arquivos

```
index.html                            HTML5 semântico
assets/cafe-medellin-sep26.css        CSS3 puro, mobile first
assets/cafe-medellin-sep26.js         JS vanilla (reveal on scroll + countdown)
assets/laura-rodriguez.jpg            foto da ponente (400×400)
assets/og-cafe-medellin-sep26.png     OG image (1200×630)
assets/og-template.html               template que gera a OG (Chrome headless)
```

**Regerar a OG** depois de mudar data, local ou ponente:

```bash
cd landing-pages/cxpress/cafe-medellin-sep26/assets
"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu \
  --hide-scrollbars --force-device-scale-factor=1 --window-size=1200,630 \
  --virtual-time-budget=6000 --screenshot="$(pwd -W)/og-cafe-medellin-sep26.png" \
  "file:///$(pwd -W)/og-template.html"
```

O `--force-device-scale-factor=1` não é opcional: sem ele a tela em HiDPI rende 2400×1260 e o arquivo estoura o limite de peso.

- [x] Formulário integrado

**Form provider:** Jotform (jsform `261303944881662`) — integrado em 09/09/2026 via `/lp-integrar-form`.

**Por que o CSS/JS vivem em `assets/` e com o slug no nome:** o `landing-pages/build/build_umbrella.py` só copia pro deploy o que é referenciado sob `/assets/{marca}/`. Um `style.css` na raiz da pasta da LP não é copiado (404 em produção) e, sem o sufixo de slug, colidiria com o `style.css` de outra LP no namespace compartilhado `assets/cxpress/` do guarda-chuva. Mesma lógica do `og-{slug}.png` (GUIDELINES §18).

## Atualizações de conteúdo vs. a edição de Bogotá

| Campo | Bogotá (jul) | Medellín (set) |
|---|---|---|
| Data | 28/07/2026 | **24/09/2026** |
| Hora | 10:00 a.m. | **4:00 p.m.** (COT) |
| Local | Edificio Ecotek, Bogotá | **Hotel Dann Carlton Medellín**, Cra. 43A #7-50, El Poblado |
| Countdown | `2026-07-28T10:00:00-05:00` | `2026-09-24T16:00:00-05:00` |
| JSON-LD `Event` | Bogotá | Medellín (`startDate`, `location`, `streetAddress`) |
| Mapa | Calle 99 #10-57 | Cra. 43A #7-50, El Poblado |

## Imagens e placeholders a substituir

| # | Item | Arquivo | Tamanho recomendado | Estado |
|---|---|---|---|---|
| 1 | **OG image** | `assets/og-cafe-medellin-sep26.png` | 1200×630, 343 KB | ✅ **gerada.** Template versionado em `assets/og-template.html`, renderizado com Chrome headless (GUIDELINES §18). Traz badge, headline, dados do evento e a foto da Laura |
| 2 | **Foto da ponente** | `assets/laura-rodriguez.jpg` | 400×400, 21 KB | ✅ **Laura Rodríguez.** O Victor enviou a foto como SVG de 158 KB com JPEG 800×800 embutido em base64; extraí o raster e regravei em JPG 400×400 (quality 86, progressivo). O crop circular é do CSS (`border-radius:50%` + `object-fit:cover`), o `clipPath` do SVG era redundante |
| 3 | **Nome + cargo da ponente** | `.spk-name` / `.spk-role` | — | ✅ Laura Rodríguez · B2B Sales & Customer Success · Cxpress |
| 4 | **Formulário** | Jotform `261303944881662` no hero | — | ✅ **integrado.** Mesmo form da edição de Bogotá. Wrapper `.jotform-embed` sem padding/fundo próprio (o card branco é a `.form-card` da LP, igual à LP de referência). O handler JS do mock foi removido (Passo 2.5) e o CSS morto do mock (`.field*`, `.form-row`, `.btn-royal`, `.btn-block`) saiu junto |
| 5 | Logo header/footer | `brand/cxpress/assets/logos/logo-reversed.svg` | — | ✅ do brand |
| 6 | Favicon | `brand/cxpress/assets/logos/logo-icon.png` | 13 KB | ✅ do brand |
| 7 | Mapa | iframe Google Maps | — | ✅ endereço real já apontado |

**Sem bloco de prova social de clientes.** Passou por duas versões (marquee de nomes, depois marquee de 22 logos da `whatsapp-business`) e o Victor pediu para tirar em 09/09/2026. A seção `.clients`, os 22 PNGs, o `@keyframes marquee` e as regras de animação foram removidos junto: nada de CSS ou asset órfão. Se um dia voltar, o histórico do git tem as duas versões prontas, e a nota que importa é que aqueles logos são PNG opacos com fundo claro (0% de transparência), então precisam de seção clara, não da navy.

## Decisões de estrutura

- **Bloco de números (`.stats`) da LP de referência foi removido.** A referência abre a seção escura com 4 métricas em count-up ("1.000+ marcas", etc.). Não há métrica Cxpress verificada em `brand/cxpress/BRANDBOOK.md`, e inventar número em LP pública não é opção. A LP fecha sem bloco de prova social numérica nem de clientes. Se o Victor passar os números, o slot entra na seção `.about` e o count-up volta.
- **Formulário no hero (§1), não na 2ª seção.** É o que a LP de referência faz e o tráfego é ToFu (evento gratuito, lead frio), onde GUIDELINES §10 pede form alto. O CTA do header e o do fecho rolam pro mesmo `#signup`.
- **Três seções escuras** (hero, "¿Cómo llegar?", "Sobre Cxpress" + CTA final) em vez de uma só, como sugere GUIDELINES §1. Override consciente: a LP de referência é dark-dominante e foi ela que o briefing mandou replicar. Não é colcha de retalhos, é o mesmo navy nas três, com o miolo claro (evento, caso, ponente) no meio.
- **Card da ponente no padrão da [`buzzmonitor/black-friday-alta-performance-outubro-2026`](../../buzzmonitor/black-friday-alta-performance-outubro-2026/index.html)** (pedido do Victor, 09/09/2026): caixa branca com borda e sombra, blob em gradiente royal→laranja atrás da foto de 130px, dois anéis que pulsam no hover do card, e o logo da Cxpress fechando o card (`logo-primary.svg`, vetor com paths, valida a GUIDELINES §19). Card único centralizado (`max-width:380px`), porque há uma ponente só. Os anéis antigos, que pulsavam em loop permanente, saíram: na referência eles só aparecem no hover, o que é menos ruidoso.
- **Título e subtítulo do card do formulário centralizados**, e o card ganhou entrada própria (`translateY(30px) scale(.975)` → nada) mais a borda em gradiente respirando (`cardEdge`, 4,5s). Nada anima no hover de propósito: dentro vive o iframe do Jotform, e mexer o card enquanto alguém digita seria hostil.
- **Costura `.about` / `.cta` colapsada.** As duas são navy e não há troca de fundo marcando o limite, então o `padding-bottom` de uma somado ao `padding-top` da outra abria 209px de vazio (ficou visível quando o bloco de clientes saiu da `.about` e ela virou uma seção curta). `.section.about{padding-bottom:28px}` derruba pra 133px no desktop e 103px no mobile. Seletor duplo de propósito: `.about` sozinho perde pro `.section` dos `@media` mais abaixo no arquivo, que tem a mesma especificidade e vem depois.
- **Countdown com `aria-hidden="true"`** e sem `aria-live` (GUIDELINES §7): a data já está na copy do hero, no bloco de endereço e no JSON-LD.

## Config técnica

- `<html lang="es-419">` · `og:locale=es_CO` · `inLanguage=es-CO`
- **GTM:** `GTM-WRQ47B9R` (container LATAM, de `brand/cxpress/tracking.json`) no head + noscript
- SEO completo (GUIDELINES §15): description, robots, 10 tags OG, 4 Twitter, JSON-LD `Organization` + `WebPage` + `Event`, canonical + `x-default`
- Sem framework, sem build: HTML5 + CSS3 + JS vanilla. Mobile first com media queries em `min-width` (640 / 900 / 1080)
- Zero em-dash no HTML, CSS e JS (validado com `grep -c`)

## QA já rodado (viewport medido ao vivo)

| Checagem | Resultado |
|---|---|
| Overflow horizontal em 375px | `scrollWidth` = 375, nenhum elemento visível vazando (só glows decorativos dentro de `overflow:hidden`, marquee por design e skip-link fora da tela) |
| Overflow horizontal em 1280px | `scrollWidth` = 1265 |
| Grids | 375px: 1 coluna em tudo · 1280px: hero 2col, aprendizados 3col, perguntas 2col, mapa 2col |
| Pisos de tipografia mobile (§20) | H1 34px, H2 seção 28px, corpo/itens/botão 17px, labels 14px |
| Quebra equilibrada (§21) | H1 "Cómo automatizar WhatsApp Business con IA": `white-space:nowrap` no `.hl` a partir de 380px pra não partir o nome da marca, e `con&nbsp;IA` pra não deixar "IA" órfã — 3 linhas limpas de 380px a 1920px; abaixo de 380px o nome parte de propósito (não cabe inteiro com o piso de 34px do §20) · H2 "Las empresas que liderarán…" 36% → **13%** (`.section-head` de 720 pra 860px) · "Convertimos el criterio…" 30% → **0%** (1 linha) · "Reserva tu lugar en Medellín" 29% → **0%** (teto do `.cta h2` de 48 pra 42px) |
| Contraste | Laranja só como preenchimento; botão laranja com texto navy (5,2:1); eyebrow em fundo claro usa `#a94d07` (5,6:1); botão royal com texto branco (5,1:1) |
| Countdown | 15 dias / 02h para 24/09 às 16:00 COT, conferido em 09/09/2026 |
| JSON-LD | parseia, 3 nós |

## Duas coisas no Jotform que a LP não controla

O form `261303944881662` é compartilhado com a edição de Bogotá, e o que ele renderiza vive num iframe cross-origin: nenhum CSS da LP alcança o interior dele. Os dois pontos abaixo só se resolvem no designer do Jotform.

1. **Coleta 3 campos, não 6.** O form pede Nombre, E-mail Comercial e Nombre de tu empresa, mais um checkbox "No deseo recibir Newsletter". A `copy-fonte.md` da edição de Bogotá especifica 6 campos (Nombre, Apellido, Correo corporativo, Teléfono, Empresa, País). Se os 6 forem requisito, precisa de um form novo ou de editar esse (que afeta Bogotá também).
2. **O botão de envio é verde (`¡ENVIAR!`).** Verde está fora da paleta Cxpress (navy / royal / laranja) e destoa dentro do card branco da LP. Trocar no tema do form.

Nenhum dos dois quebra a captura de lead. O `parentURL` é transmitido pelo embed (conferido no `src` do iframe), que é o que alimenta o `url_conversao` no CRM.

## Pendência de copy (não corrigida de propósito)

A copy herdada de Bogotá tinha **4 antíteses-por-negação**; com o hero novo (10/09/2026) restam **3** ("no se diseña escribiendo respuestas: se diseña definiendo…", "No será una demostración: será una construcción en vivo", "Un cliente no piensa en canales. Piensa en soluciones") — a quarta ("responden pero no saben decidir") saiu junto com o lead antigo. `conhecimento/editorial/regras-anti-ia.md` limita a 2 por peça de até 500 palavras. Como é copy aprovada pelo cliente e GUIDELINES §5 manda não reescrever o tom em silêncio, fica **sinalizado como sugestão** para quem aprova a copy decidir.

## Publicação

✅ **No ar** em https://content.cxpress.io/cafe-medellin-sep26 (slug registrado no `landing-pages/dominios/content-cxpress-io/manifest.json`). Guarda-chuva migrado pro CI: toda alteração vai por `/lp-publicar cxpress cafe-medellin-sep26 content.cxpress.io`, que commita a fonte e deixa o GitHub Actions deployar. **Nunca** `vercel deploy` na mão.

**Todos os itens de conteúdo estão fechados.** O `build_umbrella.py` roda com `avisos: []` (dry-run em 09/09/2026), com os 8 arquivos resolvendo no `dist`. Falta só a decisão de negócio: publicar, e antes disso resolver (ou aceitar) os 2 pontos do Jotform acima.

**Reverter o form pro mock**, se precisar: trocar o `<div class="jotform-embed">` por um `<form action="#" onsubmit="event.preventDefault()">`. O CSS dos campos (`.field`, `.form-row`) foi removido junto com o mock, então precisa voltar também. Está no histórico do git.

## Alterações depois de publicada

| Data | O que mudou | Por quê |
|---|---|---|
| 10/09/2026 | **Hero.** H1 "Atención digital desorganizada" → "Cómo automatizar **WhatsApp Business** con IA". Lead longo (custo + antítese) → "Descubre cómo diseñar agentes de IA que entienden el contexto, toman decisiones y resuelven conversaciones." | Pedido do time: headline direta no que o workshop entrega (automação de WhatsApp Business com IA) em vez de nomear a dor. Sem tocar em `<title>`, OG ou JSON-LD — continuam no eixo "diseña agentes de IA que resuelven", que o lead novo mantém. Quebra de linha medida ao vivo de 320 a 1920px (§21) |
