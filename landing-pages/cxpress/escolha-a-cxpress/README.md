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

1. **Hero** (`#topo-hero`) — logo, WhatsApp, overline, H1 com a dor, subtítulo, **formulário
   centralizado** (`#form`), faixa de 3 provas.
2. **Comparativo** (`#comparativo`) — legenda, tabela, fecho e CTA duplo.
3. **Por que escolhem** — 4 números de prova (em CSS) + os 5 bullets da original.
4. **Módulos** — os 5 blocos da original, alternando texto e visual.
5. **Clientes** — parede de logos ("mais de 800 empresas").
6. **FAQ** — 6 perguntas em `<details>`.
7. **CTA final** — volta para o formulário, WhatsApp e telefone.
8. **Rodapé** — institucional, canais, contatos, dados legais.

---

## 3. Assets

| Arquivo | Origem | Observação |
|---|---|---|
| `logo-cxpress.png`, `logo-cxpress-branco.png`, `icon-whatsapp.png`, `canais-integrados.webp` | LP `planos` | `canais-integrados` recomprimido de PNG 127 KB para WebP 23 KB |
| `clientes-cxpress.webp` | `brand/cxpress/assets/plataforma/clientes-cxpress.png` | 368 KB PNG → 68 KB WebP a 1600 px |
| `mockup-tickets.webp`, `mockup-dashboard.webp`, `card-api-chatgpt.webp` | mirrors da página original | redimensionados e reconvertidos |
| `fonts/*.woff2` | Google Fonts, subset latin | Open Sans e Source Sans 3, variáveis |
| `og-escolha-a-cxpress.png` | `assets/og-template.html` via `render_og.py` | 1200×630 |

Os dois blocos que eram GIF/imagem na original ("canais no mesmo painel" e "fila de tickets")
são markup + CSS, sem imagem.

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
