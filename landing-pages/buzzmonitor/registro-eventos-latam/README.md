# LP Buzzmonitor — registro-eventos-latam

**Gerado em:** 2026-09-08 (v1) · **Restyle premium:** v2 · **Camada halftone:** v2.1 · **Sistema de bloco de cor do manual:** v2.2 · **Hero como bloco de cor:** v2.4 · **Oferta em branco:** v2.5 · **Hero com metricas animadas:** v2.6 (2026-09-09, vigente)
**Copy-fonte:** `copy.txt` (output de `/lp-preparar`, fonte = LP legada `https://contenido.getbuzzmonitor.com/registro-eventos`)
**Regiao:** LATAM (ES-419) · GTM `GTM-MKQBX2MG`
**Publicada em:** https://content.buzzmonitor.com/registro-eventos-latam (2026-09-09)

## O que e

Redesenho minimalista da LP de oferta pos-webinar que hoje vive no **GreatPages**
(`contenido.getbuzzmonitor.com/registro-eventos`). Mesma oferta, mesmos beneficios,
zero item cortado. O ganho e de densidade: a pagina legada empilha ~60 bullets
visiveis; aqui a lista completa de funcionalidades por modulo vive num `<details>`
fechado por padrao (progressive disclosure).

**No ar desde 2026-09-09** em `content.buzzmonitor.com/registro-eventos-latam`.
A LP legada do GreatPages continua no ar em paralelo (nao foi desligada, nem redirecionada).

## Estrutura (ordem e contagem ditadas pela copy, GUIDELINES §9)

| # | Secao | Blocos | Fundo |
|---|---|---|---|
| 1 | Hero + formulario | overline, H1 (realce laranja), sub, 3 flags, CTA · card com 4 campos · **8 chips de metrica animados** | **roxo** (`#390155`) |
| 2 | Oferta | 3 cards + linha de reforco | **branco** (titulo `#EB7C2E`, conteudo preto) |
| 3 | Lo que te llevas | 5 itens (grid 3+2) + CTA outline | branco |
| 4 | Costo de no actuar | tag rotacionada, H2, 3 itens, fecho, CTA | **magenta** (`#DE2451`) |
| 5 | Plataforma | H2, sub, 4 itens (secao de pausa) | branco |
| 6 | Soluciones | 7 itens + fecho + CTA | off-white |
| 7 | Modulos por plan | tabela 8 linhas × 2 planos + accordion de 8 grupos | branco |
| 8 | Prueba social | H2 + grade estatica de 12 logos | branco (hairline) |
| 9 | CTA final | label, H2, body, CTA | **roxo** (`#390155`) |
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
- [x] OG image 1200×630 → `assets/og-registro-eventos-latam-v2.png` (160 KB, arquivo unico, sistema v2.2)
- [x] Gates locais: `check_gtm_region.py` OK · `bump_mobile_type.py` 0 pendencias · em-dash 0
- [x] Auditoria de acessibilidade (Web Interface Guidelines) — ver `REVISAO.md`
- [x] Formulario real integrado (replica do endpoint GreatPages, ver "Formulario" abaixo)
- [x] **Publicado** via fluxo CI: PR #540 -> merge-bot -> `lp-deploy.yml` run 34316747294
- [ ] Copy publicada no Notion — **nao rodou**, MCP do Notion nao estava conectado na sessao
- [ ] **1 submit de validacao no ActiveCampaign** — obrigatorio antes de mandar trafego (ver Pendencias 7)

## Formulario

Nao e embed. E **replica do envio do form GreatPages da propria pagina de origem**, mesmo padrao
que ja roda em producao em `landing-pages/buzzmonitor/agencias-es` (page id 293578):

| Item | Valor |
|---|---|
| Endpoint | `POST https://contenido.getbuzzmonitor.com/conversion` (cross-origin, `keepalive`) |
| `elemento` | `e_3619832_1_17848365766a6271e05fa7e373119784` |
| ids dos campos | herdados da page **3588766** (o form e reaproveitado entre paginas GreatPages) |
| Pagina de obrigado | `contenido.getbuzzmonitor.com/muchas-gracias` |
| Campos enviados | nome, e-mail, telefone, empresa + `input_referral_source`, `input_mobile`, `input_uri` |
| CSP | `connect-src` do `content-buzzmonitor-com/vercel.json` ja libera `contenido.getbuzzmonitor.com` |

O payload foi conferido interceptando o `fetch` na LP local (formato `{campos:{0:{id,titulo,valor}…}, elemento, eid, enav, eclid, euser}`), **sem enviar nada pra rede** e sem criar lead de teste.

`/lp-integrar-form` nao foi usada de proposito: ela troca o mock por **embed** (Jotform/RD/HubSpot).
Aqui o form e nativo com endpoint proprio, caso que a skill nao cobre e para o qual `agencias-es`
e o precedente do repo.

### O que esta fragil nisso (nao e opiniao, esta documentado)

`integracoes/activecampaign/ESTUDO-form-api-vs-greatpages.md` §1.1 registra os riscos deste
transporte, e eles valem igual aqui:

1. **Sem confirmacao de entrega.** O `/conversion` nao expoe `Access-Control-Allow-Origin` na
   resposta do POST, entao o browser entrega mas nao consegue LER o resultado. O codigo conclui
   no `.then` e no `.catch`. Se o GreatPages devolver 500, **o usuario ve sucesso do mesmo jeito**
   e o lead se perde em silencio.
2. **Acoplamento a pagina de terceiro.** Se alguem editar o form nas pages 3619832 / 3588766, os
   ids mudam e a LP para de gerar lead sem erro visivel.
3. **Sem UTM propria.** O form de origem nao tem campos de UTM, entao a atribuicao viaja dentro
   do `input_uri` (que leva a query string inteira). Combinado com o §4.1 do estudo (o filtro CM
   LATAM so reconhece URL com `getbuzzmonitor.com`, e esta LP esta em `content.buzzmonitor.com`),
   lead sem `utm_source` da whitelist tende a ficar **fora da dashboard CM LATAM**.

A recomendacao do estudo segue valendo: migrar pra webhook n8n -> API do AC (Opcao A, faseado).
Esta LP nao piora o quadro, mas **e a terceira** LP acoplada ao GreatPages.

## Publicacao

| Item | Valor |
|---|---|
| URL | https://content.buzzmonitor.com/registro-eventos-latam |
| Fluxo | CI (dominio em `MIGRADOS.json`): manifesto + PR -> merge-bot -> `lp-deploy.yml` |
| PR | #540 (auto-mergeado pelo bot: diff so tocava conteudo) |
| Run do deploy | 34316747294 (verde; smoke de todas as URLs + rollback automatico armado) |
| HTTP | 200, 82.322 bytes (bate byte-a-byte com o `dist` local) |
| Headers | 7/7 presentes (CSP, HSTS, nosniff, X-Frame-Options, Referrer-Policy, Permissions-Policy, COOP) |
| GTM | `GTM-MKQBX2MG` servido, 3/3 tokens (`gtm.js`, `ns.html`, container id) |
| Certificado | Let's Encrypt, valido ate 19/10/2026 |
| Vizinhas | intactas (o smoke do CI valida as 28 LPs do guarda-chuva) |

Metricas reais do live (Navigation Timing + PerformanceObserver, mobile-agnostico):

| Metrica | Valor |
|---|---|
| TTFB | 63 ms |
| FCP | 540 ms |
| **LCP** | **624 ms** (bom: < 2,5 s) |
| **CLS** | **0** (bom: < 0,1) |
| DOMContentLoaded | 485 ms |
| Load | 1,23 s |
| Requests | 8 (1 CSS, 4 scripts, 1 img, 2 fetch) |
| Transferido | 297 KB (HTML 17 KB comprimido) |

PageSpeed Insights nao rodou: a API publica devolveu **429** em 4 tentativas (precisa de API key
pra uso sustentado). Pra tentar de novo:

```
https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https%3A%2F%2Fcontent.buzzmonitor.com%2Fregistro-eventos-latam&strategy=mobile&category=performance&category=accessibility&category=seo&category=best-practices
```

## OG image (miniatura de redes sociais)

Refeita no sistema v2.2 pra bater com a pagina: magenta chapado `#DE2451`, reticula halftone em
vinheta, sunburst amarelo, sunburst roxo sangrando no canto e os blocos planos (retangulo roxo +
semicirculo teal) na faixa de baixo. Nada de gradiente, porque o manual usa cor plana.
Branco sobre magenta fecha 4,73:1.

### Por que o nome tem `-v2`

O crawler do Facebook (que e o mesmo que alimenta a previa do WhatsApp) **cacheia a imagem por
URL**. Trocar o conteudo mantendo `og-{slug}.png` deixaria a miniatura antiga aparecendo em novos
compartilhamentos ate o cache expirar, que leva dias.

Duas saidas foram consideradas:

1. **Query string** (`og-{slug}.png?v=2`) — **nao funciona aqui.** O `build_umbrella.py` (linha 80)
   coleta os assets com `re.findall(r"/assets/{marca}/([^\"'\)\s>]+)")`, e o `?` nao esta na
   classe de exclusao: o `?v=2` entra no nome do arquivo procurado, o asset nao e copiado e a
   miniatura vira 404.
2. **Nome versionado + path literal no `og:image`** — o que foi feito. E a excecao que a
   `GUIDELINES §18` ja preve ("referencie o arquivo por path literal no `og:image` em vez do
   placeholder `{{OG_IMAGE_PATH}}`"). Continua **um** arquivo fisico: o `og-{slug}.png` antigo foi
   removido no mesmo commit, sem duplicata.

**Custo dessa escolha:** o `og:image` desta LP nao usa mais o placeholder, entao o path
`assets/buzzmonitor/...` esta escrito na mao e assume modo guarda-chuva (que e o caso). Se algum
dia a LP virar solo, esse path precisa virar `assets/...`.

### Se precisar de uma v3

Bump o sufixo (`-v3`), troque nos dois metas (`og:image` e `twitter:image`), apague o `-v2` e
regenere:

```bash
# servidor na raiz do repo, depois:
chrome --headless=new --window-size=1200,630 --virtual-time-budget=7000 \
  --screenshot="landing-pages/buzzmonitor/registro-eventos-latam/assets/og-registro-eventos-latam-v3.png" \
  "http://127.0.0.1:PORT/landing-pages/buzzmonitor/registro-eventos-latam/assets/og-template-registro-eventos-latam.html"
```

### O que o versionamento NAO resolve

Mensagem de WhatsApp **ja enviada** guarda a previa dentro dela pra sempre: nao existe mudanca no
servidor que atualize um link que ja foi mandado. O `-v2` garante a miniatura certa em
compartilhamentos **novos**. Pra forcar o re-scrape da URL antiga (a da pagina, nao a da imagem),
usar o Sharing Debugger do Facebook em https://developers.facebook.com/tools/debug/ e clicar em
"Scrape Again".

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header e footer, raster base64, sem `<text>` vivo)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `assets/logos-clientes/*.png` (12 logos, copiados de `agencias-es`)
- `assets/og-registro-eventos-latam-v2.png` (OG, paleta v2.2 — nome versionado, ver "OG image" abaixo)
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
7. **Validar o formulario no ActiveCampaign antes de mandar trafego.** Fazer 1 submit real com
   e-mail identificavel e conferir na conta do AC: (a) o contato nasceu, (b) os 4 campos cairam
   nos campos certos, (c) a automacao que cria o negocio disparou, (d) o `input_uri` chegou com a
   query string. Enquanto isso nao for conferido, **nao se sabe** se o lead esta chegando: o
   transporte nao confirma entrega (ver "O que esta fragil nisso").
8. **Desligar ou redirecionar a LP legada do GreatPages** (`contenido.getbuzzmonitor.com/registro-eventos`)
   quando esta assumir. Hoje as duas estao no ar, competindo por indexacao com a mesma oferta.

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

## v2.4 — o hero passa a ser bloco de cor

Pedido do Victor: "usar um estilo como o dos blocos coloridos para o bloco do hero. Quero que
esse bloco seja o mais destacado de todos."

### Por que isso obrigou a remexer a cor dos outros blocos

Sao 4 blocos de cor e 3 cores de marca disponiveis, entao **uma cor repete, sem escapatoria**. A
escolha foi feita pra (a) o hero ser o mais dominante e (b) nenhum bloco saturado encostar em
outro do mesmo tom:

| Bloco | Antes | Agora | Por que |
|---|---|---|---|
| Hero | branco | **roxo `#390155`** | E o primario da marca e o tom mais escuro da paleta. Branco sobre ele da **15:1**, o que libera o tipo maior e mais pesado de toda a pagina (H1 subiu de 52px pra 62px). O card branco do formulario tambem flutua com mais forca sobre o fundo mais escuro |
| Oferta | laranja | laranja na v2.4, **branco na v2.5** | Ver secao v2.5 abaixo |
| Costo de no actuar | roxo | **magenta `#DE2451`** | Precisava sair do roxo pro hero ficar sendo o unico bloco roxo do topo. Magenta ainda cai bem no registro de alerta da secao de dor |
| CTA final | magenta | **roxo `#390155`** | Fecha a pagina no mesmo tom que abre. Hero e CTA final viram os dois extremos do mesmo bloco |

Resultado: roxo nas pontas, laranja e magenta no meio, nenhuma adjacencia do mesmo tom.

**Desvio consciente da `GUIDELINES §1`:** a regra pede "uma unica secao escura". Aqui sao duas
(hero e CTA final), de proposito, como abre-e-fecha. O que a §1 quer evitar e colcha de retalhos,
e continua valendo: 3 cores fortes, cada uma com papel fixo, e 6 das 10 secoes seguem brancas.

### Detalhes do hero

- **H1 branco, 62px no maximo** (era 52px e vinha em dois tons de roxo). No roxo so o branco
  fecha AA, entao a separacao entre as duas frases passou a ser **sublinhado amarelo** no `<em>`
  (`text-decoration` com `skip-ink: none`), que e decoracao e nao precisa de contraste.
- Subtitulo em **`#F2D8FF`** (o lilas da marca): 12,4:1 sobre o roxo. `--muted` nao serviria.
- Flags em branco com check **amarelo** (9,7:1). Ponto do eyebrow tambem amarelo.
- CTA primario do hero virou **branco com texto roxo** (o botao roxo desapareceria no fundo roxo).
- Sombra do card de formulario reforcada, porque agora ele flutua sobre cor e nao sobre branco.
- Halftone do hero passou de laranja/55% pra **branco/30%**.

### Dois bugs que apareceram no caminho

1. **`.block--ink h3` e `.block--ink .btn--primary` vazaram pra dentro do card de formulario.**
   O card e branco, entao o titulo "Activa tu acceso" ficou branco no branco e o botao de submit
   perdeu o preenchimento. Corrigido com override explicito, que **tem que vir depois** da regra
   do bloco: a especificidade empata (`.card-form h3` vs `.block--ink h3`) e quem ganha e a regra
   mais abaixo na folha. Na primeira tentativa coloquei antes e nao surtiu efeito.
2. **Formas que sumiram no proprio fundo.** O retangulo magenta da composicao da secao de dor
   ficou invisivel quando a secao virou magenta (passou a roxo); o sunburst e o retangulo roxos
   do CTA final sumiram quando ele virou roxo (passaram a magenta). Sempre que um bloco troca de
   cor, vale conferir as formas planas que vivem nele.

### Limpeza

- A tag da secao de dor passou de laranja pra **amarelo**: sobre o magenta o laranja separava so
  1,7:1, e a tag carrega informacao. Texto roxo sobre amarelo da 9,7:1.
- A variavel `--gradient` virou codigo morto quando o CTA final passou a cor plana na v2.2.
  Removida, junto com dois comentarios que ainda falavam de gradiente. **A LP nao tem mais nenhum
  `linear-gradient`** (os `radial-gradient` que sobraram sao o halftone e os brilhos).

## v2.5 — a Oferta volta pro branco, com titulo laranja e conteudo preto

Pedido do Victor: "que o bloco laranja seja branco, o titulo desse bloco seja laranja e os
bullet points (15 dias gratis, soporte consultivo, etc), incluindo suas descricoes, sejam pretos".

| Elemento | Antes (bloco laranja) | Agora (bloco branco) |
|---|---|---|
| Fundo da secao | `#EB7C2E` | `#ffffff` |
| H2 | roxo `#390155` | **laranja `#B85210`** |
| Titulo dos 3 cards | roxo | **preto `#1a1a1a`** |
| Descricao dos 3 cards | roxo a 88% | **preto `#1a1a1a`** |
| Linha "Y además..." | roxo | preto `#1a1a1a` |

### O laranja do titulo nao e o #EB7C2E, e proposital

`#EB7C2E` sobre branco da **2,84:1**. Isso reprova AA para texto normal (4,5:1) e reprova
tambem o piso de **3:1 de texto grande** da `GUIDELINES §7`, mesmo com o H2 em 54px. Entao o
titulo usa **`--accent-ink` `#B85210`** (4,97:1), que e o mesmo laranja acessivel que a LP ja
usava pra texto desde a v1. Visualmente le como laranja; a diferenca e de luminancia, nao de
matiz.

O `#EB7C2E` vivo continua presente no bloco, mas so como **elemento grafico**, onde nao existe
requisito de contraste de texto: a regua da secao, o fio de 2px no topo de cada card e o
sunburst.

### Preto = `neutral.900` do brandbook

`#1a1a1a`, que o `brand/buzzmonitor/tokens.json` define como "Texto principal". Da 18,3:1 sobre
branco. Nao usei `#000` puro: o brandbook ja tem um preto de texto definido, e usar o token
mantem a LP consistente com o resto do sistema.

### Ajustes que a troca de fundo obrigou

Formas e tints desenhados pra fundo laranja nao funcionam em branco:

- **Badge do check:** era branco a 55% (invisivel no branco). Virou tint laranja `#FDF0E5`, com
  o check em `#B85210` (4,6:1 sobre o tint).
- **Fio do topo do card:** era roxo a 30% (pensado pra contrastar com laranja). Virou
  `2px solid #EB7C2E`, que amarra com o titulo.
- **Sunburst:** era amarelo. Sobre branco o amarelo da 1,6:1 e praticamente desaparece. Virou
  laranja `#EB7C2E`.
- **Quarto de circulo da composicao:** mesmo problema, amarelo -> laranja. O semicirculo teal e
  o retangulo roxo ficaram (leem bem no branco).
- **Reticula halftone:** roxa a 30% ficava pesada no branco; baixou pra 18%.

### Limpeza

`--ink-on-orange` existia so pra carregar o texto roxo sobre o bloco laranja. Sem bloco laranja,
virou codigo morto: removida.

**Nota de composicao:** a Oferta em branco fica encostada em "Lo que te llevas", que tambem e
branca. Nao precisou de fio divisorio: a composicao geometrica (semicirculo teal + quarto
laranja + retangulo roxo) assentada na borda de baixo da Oferta ja faz o corte, e a secao
seguinte abre com o proprio marcador de secao.

## v2.6 — realce laranja no H1 e metricas animadas em volta do formulario

Quatro pedidos do Victor nesta rodada.

### 1. Titulo da Oferta no `#EB7C2E`

Voltou pro laranja vivo, **por decisao explicita dele**. Registro do que isso custa em
acessibilidade esta em `REVISAO.md`; resumo: `#EB7C2E` sobre branco da **2,84:1** e reprova AA
inclusive no piso de 3:1 de texto grande. Pra reverter, e trocar `var(--accent)` por
`var(--accent-ink)` em `.block--paper h2`.

### 2. Realce laranja atras da segunda frase do H1

A separacao das duas frases deixou de ser sublinhado amarelo e virou **marca-texto laranja**.
Detalhe que importa: o texto dentro do realce e **roxo**, nao branco. Branco sobre `#EB7C2E`
daria 2,84:1; roxo da **5,70:1**. E `box-decoration-break: clone` faz o realce acompanhar cada
linha em vez de virar um retangulo unico atras do bloco todo.

A marcacao do H1 mudou (a primeira frase ganhou um `<span>` pra manter a quebra de linha, ja que
o `<em>` deixou de ser `display: block`), mas **o texto e identico**.

### 3. Overline sem "Participantes del evento"

`Oferta exclusiva · Participantes del evento` -> **`Oferta exclusiva`**. Mudanca de copy,
aplicada tambem no `copy.txt`.

### 4. Menos ar no hero

`padding-block` de `clamp(64px, 7vw, 112px) var(--pad-y)` para
`clamp(44px, 4.6vw, 76px) clamp(64px, 7vw, 104px)`. No desktop caiu de 112/176px para 76/104px.

### As metricas animadas

8 chips decorativos (contadores, sparkline, donut de sentimento, barras) que sobem do fundo,
atravessam o hero e saem de quadro, em loop infinito. Passam **atras** do card de formulario
(`.metrics` em `z-index: 0`, o `.wrap` em `z-index: 2`), entao nunca cobrem conteudo.

- 3 trajetorias diferentes (`cross-a` sobe pra direita, `cross-b` entra pela direita e sai pela
  esquerda, `cross-c` sobe pra esquerda), com duracoes de 17s a 29s e atrasos de 0 a 12s. As
  duracoes sao desencontradas de proposito pra nunca reentrarem em sincronia.
- So `transform` e `opacity` sao animados (compositor-friendly), com `will-change`.
- **No mobile ficam 5** dos 8 (os outros somem via `display: none`), um pouco menores. Verificado
  num viewport real de 390x780: 4 chips simultaneos com opacidade entre 0,53 e 0,95.

#### O bug que quase passou

A primeira versao usava porcentagem no `translate` (`translate3d(0, 130%, 0)`). **Porcentagem em
`translate` e relativa ao proprio elemento**, nao ao container: um chip de ~40px de altura andava
~110px e o movimento passava despercebido. Trocado por `vh`/`vw`, que se referem ao viewport. Foi
detectado medindo o deslocamento real no navegador em dois instantes, nao olhando screenshot.

Segunda correcao: os chips estavam ancorados na base do hero e a rampa de opacidade abria em 38%
da animacao, entao ficavam visiveis pouco e longe do formulario. Passaram a ser ancorados no meio
do hero (`top: 40%..72%`) com opacidade abrindo em 10%.

#### Acessibilidade deste efeito

- Tudo dentro de `.metrics`, que e **`aria-hidden="true"`**: nao entra na arvore de acessibilidade.
- **`prefers-reduced-motion: reduce` esconde o bloco inteiro** (`display: none`). Quem pediu menos
  movimento nao ve nenhum.
- Os numeros sao **ilustrativos**, declarados no `copy.txt` no bloco
  `=== METRICAS ANIMADAS (decorativo, rotulos de UI, datos de ejemplo) ===`. Nao ha afirmacao de
  resultado de cliente.
- **Ponto aberto (WCAG 2.2.2):** movimento automatico que dura mais de 5s e roda em paralelo com
  outro conteudo pede um mecanismo de pausar/parar/ocultar. Hoje a LP atende so pela via
  automatica (`prefers-reduced-motion`); nao ha botao de pausa, porque o pedido foi movimento
  continuo. Fechar isso e um botao discreto de pausa, como o que a v1 teve no marquee. **Decisao
  do Victor.**

## Historico de versoes

| Versao | O que era | Estado |
|---|---|---|
| v1 | Primeiro redesenho minimalista da LP legada do GreatPages. Paleta de 3 cores, botao laranja, marquee de logos, halo no hero, barra de progresso. | substituida |
| **v2** | Restyle premium quase monocromo (Apple / Vercel). Roxo como tinta, laranja como faisca, hairline em vez de sombra, raio pequeno, grade estatica de logos. | **vigente** |
| v3 | Tentativa de reforcar a marca: geometria do brandbook, painel animado de social listening (contadores, sparkline, donut, barras), numeros de cases, H2 curtos orientados a dor, CTA fixo no mobile. | **revertida** a pedido do Victor em 2026-09-08 ("nao sinto o estilo premium"). A copy voltou junto. |
| v2.1 | v2 + camada halftone em 4 momentos e plaquetas de cor por card. | substituida (as plaquetas sairam na v2.2, o halftone ficou) |
| v2.2 | v2.1 + sistema de bloco de cor do "Manual de Active Campaign": 3 blocos saturados, sunburst, formas planas e reticula em grade. | substituida |
| v2.3 | Troca de "webinar" por "evento" em toda a copy publica (9 no HTML, 4 no `copy.txt`). | incorporada |
| v2.4 | Hero passa a ser bloco de cor (roxo) e vira o bloco mais destacado; costo vai pra magenta e CTA final pra roxo. | substituida |
| v2.5 | Oferta volta pro branco com titulo laranja e conteudo preto. Restam 3 blocos de cor: hero (roxo), costo (magenta) e CTA final (roxo). | substituida |
| **v2.6** | Titulo da Oferta no `#EB7C2E`; realce laranja atras da 2a frase do H1; overline encurtado; menos ar no hero; 8 chips de metrica animados em volta do formulario (5 no mobile). | **vigente** |

O revert da v3 foi validado por comparacao pixel a pixel contra o render da v2: **0 pixels de
diferenca** em 1440x10400. A `copy.txt` voltou do backup tirado antes da reescrita.

Se um dia a ideia da v3 for retomada, o caminho que o Victor recusou foi o **excesso**: painel de
dashboard cheio de dado + faixa de numeros de case + geometria em 5 secoes ao mesmo tempo tirou o
silencio que faz a pagina parecer premium. Uma reintroducao teria que ser de um elemento por vez.
