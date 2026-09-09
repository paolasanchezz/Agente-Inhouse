# LP Buzzmonitor — registro-eventos-latam

**Gerado em:** 2026-09-08 (v1) · **Restyle premium:** v2 · **Camada halftone:** v2.1 · **Sistema de bloco de cor do manual:** v2.2 (2026-09-08, vigente)
**Copy-fonte:** `copy.txt` (output de `/lp-preparar`, fonte = LP legada `https://contenido.getbuzzmonitor.com/registro-eventos`)
**Regiao:** LATAM (ES-419) · GTM `GTM-MKQBX2MG`
**Dominio sugerido:** `content.buzzmonitor.com` (subdominio guarda-chuva de conteudo ES-LATAM)

## O que e

Redesenho minimalista da LP de oferta pos-webinar que hoje vive no **GreatPages**
(`contenido.getbuzzmonitor.com/registro-eventos`). Mesma oferta, mesmos beneficios,
zero item cortado. O ganho e de densidade: a pagina legada empilha ~60 bullets
visiveis; aqui a lista completa de funcionalidades por modulo vive num `<details>`
fechado por padrao (progressive disclosure).

A LP legada continua no ar. Esta versao nao foi publicada.

## Estrutura (ordem e contagem ditadas pela copy, GUIDELINES §9)

| # | Secao | Blocos | Fundo |
|---|---|---|---|
| 1 | Hero + formulario | overline, H1, sub, 3 flags, CTA · card com 4 campos | branco |
| 2 | Oferta | 3 cards + linha de reforco | off-white |
| 3 | Lo que te llevas | 5 itens (grid 3+2) + CTA outline | branco |
| 4 | Costo de no actuar | tag rotacionada, H2, 3 itens, fecho, CTA | **escuro** (`#390155`) |
| 5 | Plataforma | H2, sub, 4 itens (secao de pausa) | branco |
| 6 | Soluciones | 7 itens + fecho + CTA | off-white |
| 7 | Modulos por plan | tabela 8 linhas × 2 planos + accordion de 8 grupos | branco |
| 8 | Prueba social | H2 + grade estatica de 12 logos | branco (hairline) |
| 9 | CTA final | label, H2, body, CTA | **gradiente** (unico da LP) |
| 10 | Footer | logo, contato, legal | branco (hairline) |

## Decisoes de design (sistema v2 — premium / quase monocromo)

Referencia pedida pelo Victor: Apple, Vercel, ManyChat. O que isso significou na pratica:
tirar cor e sombra da pagina e deixar tipografia, hairline e respiro fazerem o trabalho.

- **Paleta (GUIDELINES §1): 2 cores fortes, nao 3.** Roxo `#390155` virou a **tinta** da
  pagina (titulos, botao primario, marcadores de check, secao escura) e o laranja `#EB7C2E`
  ficou como **faisca**, em doses pequenas: a regua de 30px antes de cada H2, o ponto do
  eyebrow, a tag rotacionada, os rotulos de grupo do accordion e o hover. O teal saiu:
  o marcador `✓` agora e roxo, o que a §8 permite ("marcador da cor primaria da marca")
  e o que derruba a paleta para as duas cores do proprio logo.
- **Hairline em vez de sombra.** Bordas de 1px (`#ECE8F0` / `#DCD5E4`) substituiram os cards
  com sombra. A tabela de planos e o accordion perderam a caixa externa. Sobrou uma unica
  sombra de verdade, muito baixa, no card de formulario do hero.
- **Raios pequenos.** Nada de pilula de 999px: botoes e campos em 10px, cards em 14px, tag
  em 4px. A pilula lilas do eyebrow saiu e virou ponto laranja + texto em caixa alta com
  tracking, o que tambem resolveu de vez o risco de contraste em fundo tingido.
- **Botao primario roxo com texto branco (15:1).** Antes era laranja com texto roxo, para
  driblar o contraste. O roxo solido le muito mais premium, respeita a hierarquia da marca e
  liberou o laranja para ser acento. Cor centralizada em `--ink`, entao voltar ao laranja e
  trocar uma linha (a `generation-rules.json` pede `ctaButton` laranja, ver Pendencias).
- **Menos peso de display.** League Spartan 900 ficou so em H1, H2, H3 e na frase de fecho da
  secao escura. As listas de plataforma e o fecho de soluciones passaram para Lato: a pagina
  parou de gritar em todas as secoes.
- **Marquee de logos virou grade estatica** de 6x2 com hairline, estilo "trusted by" da Vercel.
  Sai o movimento, sai o botao de pausa e sai o achado de WCAG 2.2.2 junto.
- **Barra de progresso e halo radial do hero foram removidos.** Eram os dois elementos que mais
  destoavam de uma pagina premium. O unico brilho que sobrou e um radial laranja de 16% de
  opacidade no canto da secao escura.
- **Ritmo:** branco na maior parte, `#FAF9FB` (quase imperceptivel) em duas secoes, **1 secao
  escura** (§4) e **1 gradiente** (§9). Respiro de secao subiu para `clamp(104px, 12vw, 176px)`.
- **Movimento que sobrou:** reveal com stagger no scroll, header sticky que adensa, seta do
  botao que desliza 4px no hover, accordion nativo com chevron, hover em card / linha da tabela
  / logo. Tudo desligado em `prefers-reduced-motion`, com fallback `<noscript>` no reveal.
- **Ajustes de contraste (§7, AA nao negociavel):**
  - Laranja `#EB7C2E` da paleta da marca da **2,84:1** em texto sobre branco, reprova.
    Solucao: `#EB7C2E` fica so em fundo/regua/borda; **texto laranja usa `#B85210`** (4,97:1).
  - Botao primario = fundo roxo `#390155` com **texto branco** (15:1). A tag rotacionada da
    secao escura usa fundo `#EB7C2E` com texto `#390155` (5,70:1), o unico lugar onde o
    laranja carrega texto.
  - Gradiente do CTA final: `120deg, #390155 0%, #EB7C2E 165%`. O **overshoot de 165%**
    e deliberado: mantem a extremidade visivel em tom escuro o suficiente para o texto branco
    fechar ~5,7:1. Com o gradiente terminando em 100% o branco cairia a 2,84:1.
  - Primeira frase do H1 em `#7A5A8E` (5,7:1) e segunda em `#390155`: dois tons de roxo em vez
    de meia headline laranja. Setup silencioso, desfecho forte.
- **Formulario no hero (§10):** o default para BoFu e form na 4ª secao ou na ultima. Override
  justificado: o trafego e participante que acabou de sair do webinar (lead quente, ja conhece
  a marca), cenario que a propria §10 lista como excecao. A LP legada tambem abre com o form.
  Todos os outros CTAs sao ancoras que rolam ate `#form`.
- **Tabela de planos:** no desktop, comparativo de 2 colunas com destaque discreto no
  Enterprise. Em ≤640px as colunas de plano encolhem e a tabela **cabe inteira na tela**
  (sem scroll horizontal escondido, que seria armadilha de UX no celular). Entre 641px e
  780px o container `overflow-x: auto` (com `role="region"` + `tabindex="0"`) assume.

## Estado

- [x] Copy estruturada (`copy.txt`) + revisao linguistica ES-LATAM e anti-IA
- [x] HTML gerado
- [x] OG image 1200×630 → `assets/og-registro-eventos-latam.png` (321 KB, arquivo unico, na paleta v2)
- [x] Gates locais: `check_gtm_region.py` OK · `bump_mobile_type.py` 0 pendencias · em-dash 0
- [x] Auditoria de acessibilidade (Web Interface Guidelines) — ver `REVISAO.md`
- [ ] Copy publicada no Notion — **nao rodou**, MCP do Notion nao esta conectado nesta sessao
- [ ] Formulario real integrado — rodar `/lp-integrar-form buzzmonitor/registro-eventos-latam "snippet"`
- [ ] Publicado — rodar `/lp-publicar buzzmonitor registro-eventos-latam content.buzzmonitor.com`

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header e footer, raster base64, sem `<text>` vivo)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `assets/logos-clientes/*.png` (12 logos, copiados de `agencias-es`)
- `assets/og-registro-eventos-latam.png` (OG)
- `assets/og-template-registro-eventos-latam.html` (template do OG, para regerar)

## Pendencias e pontos de decisao

1. **Slug.** Ficou `registro-eventos-latam` para rastrear a origem. Se a ideia for
   substituir a pagina do GreatPages preservando links, o slug no guarda-chuva deveria
   ser o mesmo path da legada.
2. **`Universidade do Buzz`** ficou literal (esta assim na LP legada), mas e portugues
   numa pagina ES e nao consta no `BRANDBOOK.md`. Confirmar com produto se e nome proprio.
3. **H1** abre pelo ganho, nao pela dor. Mantido por ser BoFu quente; alternativa com dor
   explicita esta marcada no `copy.txt` para teste A/B.
4. **Logos de cliente** vieram do set da LP `agencias-es` (marcas ES/EU). Se a oferta for
   mirada em LATAM, vale trocar por um set regional.
6. **Cor do botao primario.** Ficou roxo `--ink`. A `brand/buzzmonitor/generation-rules.json`
   pede `ctaButton: secondary (laranja)`. Contrariei de proposito (premium + contraste), mas e
   a decisao mais facil de reverter da LP: trocar `--ink` por `--accent` em `.btn--primary` e
   o texto para `var(--ink)`. Se o Victor quiser A/B de cor de CTA, e aqui.
5. Regerar a OG image: subir um servidor local na raiz do repo e rodar Chrome headless
   `--window-size=1200,630 --screenshot` contra `assets/og-template-registro-eventos-latam.html`.

## v2.1 — camada halftone

Pedido do Victor: halftone + "maximalismo controlado, moderno, disruptivo, mas ao mesmo tempo
minimalista como esta agora", tomando referencia de um manual com secoes de SDR, Closer,
Financeiro e Customer Success. **O link enviado aponta para a LP de oferta legada, nao para esse
manual** (conferido: 0 ocorrencias de "SDR", "Financiero" e "halftone" no HTML dela; "Closer"
aparece 1 vez, num campo oculto do formulario). O manual tambem nao esta no repo. Entao esta
rodada entrega **so a parte de halftone**, que da pra fazer sem a referencia. O sistema grafico
por secao (o das secoes de cargo) segue pendente do arquivo certo.

### Como o halftone foi construido

Retícula de pontos 100% CSS, sem imagem: duas camadas de `radial-gradient` (pontos de 2,1px e
1,05px) em grade de 10px, deslocadas meio passo entre si, sempre com `mask-image` para virar
rampa em vez de textura chapada. Peso somado: ~2,7 KB de CSS, zero request.

Aplicada em **4 momentos** (maximalismo controlado = textura forte, mas nao em todo lugar):

| Onde | Cor | Opacidade | Mascara |
|---|---|---|---|
| Hero, canto superior direito | laranja | 55% | radial, entra pelo canto e dissolve |
| Cards da oferta, plaqueta de canto | laranja / teal / amarelo (1 por card) | 42% | circular, cada card recebe sua cor |
| Secao escura, canto inferior esquerdo | pessego | 20% | radial, sobe do canto |
| CTA final | branco | 20% | **vinheta invertida** |

As 3 plaquetas dos cards sao a leitura mais proxima do "estilo de secao por cargo": cada item da
oferta ganha uma cor propria em retícula, do jeito que um manual de papeis faz. E onde teal e
amarelo aparecem, sempre pequenos, com roxo e laranja seguindo dominantes (hierarquia que a
`generation-rules.json` exige).

### Contraste: por que a vinheta e invertida

Ponto claro sobre superficie escura **clareia o fundo** justo onde mora texto branco. Na primeira
versao a retícula do CTA final vinha em rampa diagonal e passava por tras do titulo: no nucleo de
cada ponto o contraste caia para ~3,7:1, abaixo do AA. Troquei por uma vinheta invertida
(`radial-gradient(... transparent 55%, #000 100%)`): os pontos emolduram a mensagem e **nao
existem atras do texto**. Mesmo raciocinio na secao escura, empurrada mais para o canto e baixada
de 30% para 20%.

Tipografia subiu um grau (H2 max 46px -> 54px, H1 do hero 52px -> 58px, tracking mais fechado)
para acompanhar o tom mais afirmativo sem mexer em estrutura nem em copy.

**Copy: intacta.** Nada mudou no `copy.txt` nesta rodada. Diff de fidelidade re-rodado: 0 textos
fora da copy.

## v2.2 — sistema de bloco de cor, traduzido do manual

Fonte: **"Manual de Active Campaign"** da Buzzmonitor (Canva, 27 paginas), enviado pelo Victor.
O que o manual faz, pagina por pagina:

- **Uma cor saturada por bloco, a sangre.** SDR = laranja `#EB7C2E` (paginas 5 a 8),
  Closers = magenta `#DE2451` (paginas 11 a 22). A capa usa faixas de amarelo, teal e roxo.
- **Titulo display grande** em League Spartan, as vezes no padrao `Bold | subtitulo leve`
  ("Closer | Campos de trato").
- **Corpo pequeno** em colunas com bullets, frases-chave em negrito.
- **Composicao em camadas de um lado:** retangulos e semicirculos planos nas cores da marca
  (teal, roxo, amarelo, magenta), uma **estrela/sunburst** recorrente como forma-assinatura,
  **reticula de pontos** em grade reta, e por cima uma **foto recortada em duotono/escala de
  cinza** (funil, sirene, mao com lapis).

### Como traduzi pra LP

Regra que me dei: **3 blocos coloridos em 10 secoes.** O maximalismo e nos blocos, o silencio
fica no resto. Assim continua "minimalista como esta agora" e ao mesmo tempo tem o DNA do manual.

| Secao | Antes (v2.1) | Agora (v2.2) |
|---|---|---|
| Oferta | off-white com 3 cards brancos | **bloco laranja a sangre**, titulo roxo, 3 colunas com fio de topo, sunburst amarelo sangrando na borda, reticula roxa e pilha geometrica (semicirculo teal + quarto de circulo amarelo + retangulo roxo) |
| Costo de no actuar | roxo com halftone no canto | mesmo roxo, **+ sunburst laranja** sangrando na direita e **+ retangulo magenta / semicirculo teal** assentados na borda de baixo |
| CTA final | gradiente roxo→laranja | **magenta chapado** (o manual nao usa gradiente, usa cor plana), com a reticula em vinheta, 2 sunbursts (amarelo e roxo) e a pilha geometrica |
| Hero | halftone laranja | mesmo halftone **+ sunburst amarelo** discreto como assinatura |
| Todas as outras 6 secoes | brancas / off-white | **inalteradas** |

O sunburst e um `<path>` SVG de 24 pontas gerado por script (alterna raio 50/39 em 48 vertices),
com rotacao lenta de 44s que para em `prefers-reduced-motion`. As formas planas sao `<i>` com
`border-radius` (semicirculo = `999px 999px 0 0`, quarto = `0 999px 0 0`), zero imagem.

### O que NAO consegui trazer, e por que

**As fotos em duotono.** Boa parte da forca do manual vem de foto recortada em escala de cinza
por cima dos blocos de cor. A LP nao tem banco de imagem e eu nao vou inventar foto. Entreguei
a camada geometrica + reticula + sunburst, que e a maior parte do DNA, mas se quiser fechar o
circulo preciso de **2 ou 3 fotos recortadas** (fundo transparente, PNG) pra tratar em duotono
via CSS (`filter: grayscale(1)` + `mix-blend-mode`). Aviso: em `landing-pages/GUIDELINES.md` §14
tem a armadilha de `<img>` em grid no Safari iOS, ja documentada.

### Contraste: onde o manual reprova e eu desviei

O manual usa **texto branco sobre o laranja** `#EB7C2E`. Isso da **2,84:1** e reprova AA (nem
passa o piso de 3:1 de texto grande). No bloco laranja da LP o texto e **roxo `#390155`**
(5,70:1) em vez de branco. Fica igualmente afirmativo e nao quebra a `GUIDELINES §7`.

Outros dois ajustes de contraste desta rodada:
- corpo dos 3 itens no laranja: era `rgba(57,1,85,.78)` = 4,20:1. Subiu pra `.88` = **4,88:1**.
- bloco magenta: o branco estava com alpha (.90 / .94), o que derrubava pra ~4,6:1. Passou a
  **branco solido**, que fecha **4,73:1** exatos sobre `#DE2451`.

**Copy: intacta.** Nada mudou no `copy.txt` desde a v2. Diff de fidelidade: 0 textos fora da copy.

## Historico de versoes

| Versao | O que era | Estado |
|---|---|---|
| v1 | Primeiro redesenho minimalista da LP legada do GreatPages. Paleta de 3 cores, botao laranja, marquee de logos, halo no hero, barra de progresso. | substituida |
| **v2** | Restyle premium quase monocromo (Apple / Vercel). Roxo como tinta, laranja como faisca, hairline em vez de sombra, raio pequeno, grade estatica de logos. | **vigente** |
| v3 | Tentativa de reforcar a marca: geometria do brandbook, painel animado de social listening (contadores, sparkline, donut, barras), numeros de cases, H2 curtos orientados a dor, CTA fixo no mobile. | **revertida** a pedido do Victor em 2026-09-08 ("nao sinto o estilo premium"). A copy voltou junto. |
| v2.1 | v2 + camada halftone em 4 momentos e plaquetas de cor por card. | substituida (as plaquetas sairam na v2.2, o halftone ficou) |
| **v2.2** | v2.1 + sistema de bloco de cor do "Manual de Active Campaign": 3 blocos saturados, sunburst, formas planas e reticula em grade. Copy da v2 intacta. | **vigente** |

O revert da v3 foi validado por comparacao pixel a pixel contra o render da v2: **0 pixels de
diferenca** em 1440x10400. A `copy.txt` voltou do backup tirado antes da reescrita.

Se um dia a ideia da v3 for retomada, o caminho que o Victor recusou foi o **excesso**: painel de
dashboard cheio de dado + faixa de numeros de case + geometria em 5 secoes ao mesmo tempo tirou o
silencio que faz a pagina parecer premium. Uma reintroducao teria que ser de um elemento por vez.
