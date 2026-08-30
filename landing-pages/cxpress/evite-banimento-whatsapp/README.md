# LP Cxpress — evite-banimento-whatsapp

**Gerado em:** 2026-08-24
**Copy-fonte:** `copy.txt`
**Origem:** variante da LP `banimento-whatsapp` (content.cxpress.io). Estrutura, layout e
textos replicados da pagina de referencia a pedido do briefing. Diff de texto visivel
contra a referencia = **1 linha** (a chamada de preco). As demais 62 linhas de texto
visivel sao identicas, verificado por diff automatizado.

- **lang:** `pt-BR`
- **dominio alvo:** `content.cxpress.io` (guarda-chuva migrado pro CI)

## Estrutura

1. HERO (overline + H1 + 2 paragrafos + CTA + celular com a tela de banimento sobre circulos/glow)
2. CLIENTES (prova social, esteira infinita com 42 logos)
3. BENEFICIOS (3 cards + CTA da secao)
4. PROVA (4 stats + nota de fonte + CTA)
5. PLATAFORMA (titulo + subtitulo + 4 features, 1 delas text-only)
6. FAQ (8 perguntas)
7. QUEM SOMOS (foto + texto + 3 badges)
8. FECHO (secao dark, titulo + subtitulo + CTA)
9. FORM (ultima secao, centralizada, embed Jotform) — alvo dos 9 CTAs (`#agendar`)
10. FOOTER

> A ordem acima e a de 2026-08-30. Ate essa data o FORM era a 2a dobra (item 3) e o
> FECHO fechava a pagina.

## Deltas em relacao a `banimento-whatsapp`

| # | O que | De | Para |
|---|---|---|---|
| 1 | Chamada de preco | `Planos a partir de R$ 1.290` | `Planos a partir de R$ 990 com 3 acessos` |
| 2 | Form Jotform | `261045149477663` | `261034073026647` (ver historico do form abaixo) |
| 3 | GTM | `GTM-T4XDWHL3` | `GTM-KN8BPFG` |
| 4 | GA4 | (nao tinha) | `gtag.js` com ID `339689858` |
| 5 | Visual do hero | `plataforma-canais.gif` | `./assets/hero-conta-banida-whatsapp.png` + blobs/glow/pilulas |
| 6 | Secao do form | card 2 colunas com divisor vertical | 1 coluna centralizada + apoio de fundo (malha de pontos, glows, pilulas, icones flutuantes) |
| 7 | Contraste/separacao | `neutral-100` (#f5f5f5) alternando | tint unico da marca `#EEF3FF` + bordas de secao + sombras mais presentes nos cards + corpo de texto em `#3d4250` |

### Rodada 2 de ajustes (2026-08-24, feedback do Victor sobre o live)

| # | O que | De | Para |
|---|---|---|---|
| 8 | Espaco morto entre HERO e CLIENTES | aparelho 320px (671px de altura) vs coluna de texto ~460px + padding 140/96px | aparelho 272px (578px), `hero__inner` padding-bottom 56px, `clientes` padding-top 40px |
| 9 | Pilula do topo direito do hero | lilas `--primary-lighter` | azul escuro `--primary-dark` (#232960) |
| 10 | Marcador dos cards de BENEFICIOS | pilula decorativa (`.card__pill`) | badge 58px com icone (escudo-check / equipe / bolha-relogio), stroke navy, fundo no tint da cor de cada card |
| 11 | CTA nos itens da PLATAFORMA | nao tinha | 1 CTA por feature (4 no total), estilo link com regua verde e seta |

Sobre o **delta 8**: o vazio nao era padding, era a diferenca de altura entre as duas
colunas do grid do hero (`align-items:center` com visual muito mais alto que o texto cria
faixa morta em cima e embaixo do texto). Reduzir o aparelho atacou a causa; o corte de
padding foi complemento. A sombra do aparelho pode transbordar pro CLIENTES sem problema,
porque o `.hero` nao tem mais `overflow:hidden` (ver nota tecnica abaixo).

Sobre o **delta 11**: o rotulo reusa o literal da copy (`Agendar demonstracao gratuita`),
porque a regra de fidelidade de copy proibe inventar texto novo por feature. Se o time
quiser CTA especifico por item (`Ver os canais`, `Conhecer a IA`), isso e copy nova e
precisa vir do pipeline. Estilo de link (nao botao cheio) de proposito: 4 botoes solidos
nessa secao competiriam com o CTA principal.

### Rodada 3 de ajustes (2026-08-27, feedback do Victor sobre o live)

| # | O que | De | Para |
|---|---|---|---|
| 12 | Fundo atras do aparelho no hero | blob azul (`.blob-a`, gradiente `--primary-lighter`) + glow royal + anel solto | circulos concentricos (`./assets/hero-circulos-concentricos.svg`) centrados no aparelho; glow ambar e as duas pilulas continuam |
| 13 | Icone do card `Historico que nao se perde` | bolha de conversa + ponteiro de relogio | relogio com seta anti-horaria (icone de historico), mesmo peso de stroke (1.7) dos outros dois |
| 14 | CTA nos itens da PLATAFORMA | link com regua verde e seta | botao outline (contorno `--wa` 2px, raio `--radius-btn`, hover preenche de verde) |

Sobre o **delta 13**: o icone antigo estava deformado por geometria invalida, nao por CSS.
O arco `a8.4 8.4 0 1116.3-5.9` fechava uma corda de 17,3 unidades com raio 8,4 (diametro
16,8) — quando a corda e maior que o diametro, o SVG escala o raio pra caber e o desenho
sai achatado. O icone novo tem arcos com corda menor que o diametro, entao renderiza igual
em qualquer engine.

Sobre o **delta 12**: os circulos sao SVG (~420 bytes) e nao PNG, pra ficarem nitidos em
qualquer densidade de tela e nao pesarem no LCP do hero. No mobile o diametro cai pra
`min(98%,360px)` de proposito: acima disso o anel externo estoura a coluna e o
`overflow-x:hidden` do body corta o circulo numa linha reta.

Sobre o **delta 14**: o contorno mantem a hierarquia que o delta 11 protegia (o CTA
principal segue sendo o unico botao solido) e ainda entrega area de clique de botao, que
o link com regua nao tinha.

### Rodada 4 de ajustes (2026-08-27, `/lp-revisar` com foco em mobile)

Auditoria completa em `REVISAO.md`. Resumo do que mudou no HTML:

| # | O que | De | Para |
|---|---|---|---|
| 15 | CTA outline da PLATAFORMA no mobile | rotulo em 2 linhas com a seta solta na borda de um botao quase full-width | `≤640px`: padding 14/18, conteudo centrado (1 linha em 390px); `≤360px` esconde a seta |
| 16 | CTA principal dentro do card do fecho em 320px | 3 linhas (`padding:16px 34px`) | `≤520px`: `.btn` full-width, padding 16/18, `text-wrap:balance` → 2 linhas centradas |
| 17 | Alvo de toque do CTA do header no mobile | 40px de altura | 46px (`padding:12px 16px` em `≤640px`) |
| 18 | Aparelho do hero no mobile | `max-width:230px` fixo | `min(62vw,260px)` — 198px em 320, 260px em 430 |
| 19 | Pilulas decorativas em tela estreita | `.f2` colava no CTA do fecho; `.pill-2` flutuava sobre os circulos | escondidas em `≤520px` |
| 20 | Logo Elife em QUEM SOMOS | `<img>` sem width/height (CLS) | `width="250" height="140"` + `loading="lazy"` |
| 21 | Toque no Android | atraso de 300ms do double-tap + flash cinza padrao | `touch-action:manipulation` + `-webkit-tap-highlight-color` |
| 22 | Rodape em iPhone com home indicator | `padding-bottom:56px` | `calc(56px + env(safe-area-inset-bottom))` |

Sobre o **delta 16**: com o piso de 17px em botao (GUIDELINES §20) o rotulo `Agendar demonstracao gratuita` nao cabe numa linha em 320px — nao ha ajuste de padding que resolva sem furar o piso. Full-width com 2 linhas centradas e a forma de fazer isso parecer intencional em vez de quebrado.

Sobre o **delta 19**: e decisao de composicao, nao correcao de bug — as pilulas nao causavam overflow. Reverter e so apagar as duas linhas do bloco `@media (max-width:520px)`.

Medicao: `scrollWidth == clientWidth` em 320/360/390/430/640/768px; pisos de tipografia intactos (h1 36px, corpo 18px); `check_mobile_type.py` sem overflow novo.

### Historico do formulario

| Quando | PR | Form | Escopo |
|---|---|---|---|
| 2026-08-24 | #345 | `261034073026647` | so esta LP (briefing original) |
| 2026-08-26 | #374 | `261027639617663` | lote de 6 LPs de proposta Cxpress ("Jotform do contato") |
| 2026-08-26 | #384 | `261045149477663` | lote de 7 LPs de proposta Cxpress ("Jotform de remarketing") |
| 2026-08-27 | (este) | `261034073026647` | so esta LP, a pedido do briefing |

> ⚠️ **Esta LP esta fora da unificacao das 7 LPs de proposta.** O PR #384 apontou
> `atendimento-digital`, `banimento-whatsapp`, `banimento-whatsapp-comercial`, `coex-whatsapp`,
> `evite-banimento-whatsapp`, `whatsapp-business-smb` e `whatsapp-smb` para o mesmo Jotform de
> remarketing. Esta LP foi revertida para o form proprio (`261034073026647`) a pedido, o que
> faz sentido com o fato de ela ter GTM (`GTM-KN8BPFG`) e GA4 (`339689858`) proprios: a
> atribuicao dela e separada do resto do lote. **Se um proximo lote unificar form nas LPs de
> proposta, esta precisa ser excluida do lote de proposito, nao por esquecimento.**
>
> Nota de manutencao: os PRs #374 e #384 alteraram apenas o `index.html`, deixando `copy.txt` e
> este README apontando IDs antigos. Reconciliado agora: os tres arquivos dizem
> `261034073026647`.

### Pontos de atencao (decisoes que precisam de OK do time)

- **GTM sobrepoe o `brand/cxpress/tracking.json`.** O tracking.json aponta `GTM-T4XDWHL3`
  para a regiao `brasil`; esta LP usa `GTM-KN8BPFG` por pedido explicito no briefing.
  Isso faz o gate `check_gtm_region.py` **bloquear** o deploy, entao a LP tem selo
  `.tracking.lock` grandfathered (`status: wrong`, fingerprint `1b72ebbdd5041c63`) pra
  liberar o CI sem mexer no container das outras LPs Cxpress BR. Consequencia: se alguem
  trocar o GTM desta LP, o fingerprint muda e o gate volta a bloquear (comportamento
  desejado). Se `GTM-KN8BPFG` virar o padrao de Cxpress BR, atualizar o `tracking.json` e
  regravar o selo com `--write-stamp`.
- **ID do GA4.** O briefing passou `339689858`. IDs de medicao GA4 normalmente tem o
  formato `G-XXXXXXXXXX`; `339689858` tem cara de **ID de propriedade / de fluxo de dados**.
  A tag foi montada literalmente com o valor recebido. Se o hit nao aparecer no GA4,
  trocar pelo `G-...` do fluxo Web.
- **Nota do site ativo aparece 2x.** `Ter um site ativo e um dos requisitos...` esta na
  copy da LP (herdada da referencia) e tambem como texto de ajuda do campo "Site da
  empresa" dentro do Jotform novo. Mantido por fidelidade a referencia; remover a linha
  da LP e uma edicao de 1 linha se o time preferir.
- **Form real, nao mock.** GUIDELINES §11 pede mock no `lp-gerar` e embed via
  `/lp-integrar-form`. Aqui o snippet do Jotform veio pronto no briefing e foi embutido
  direto, no mesmo padrao da LP de referencia.

## Validacoes rodadas

- `grep -c "—"` = 0 e `grep -c "&mdash;"` = 0 (anti-IA, tolerancia zero)
- Diff de texto visivel contra a referencia: so a linha de preco
- 10 tags `og:` / 4 tags `twitter:` / canonical / JSON-LD valido
- Placeholders `{{DOMAIN}}`, `{{OG_IMAGE_PATH}}`, `{{BRAND_LOGO_PNG_PATH}}` presentes e
  resolvidos pelo `build_umbrella.py`; nenhum path relativo vaza pos-rewrite
- Todos os assets referenciados resolvem (brand ou LP-local)
- Logos do header/footer sem `<text>` vivo (§19)
- Sem scroll horizontal em 375 / 753 / 1265 / 1521 px
- Mobile: headline antes do visual (§3)
- Embed do Jotform renderiza (iframe "CXPRESS BR")

### Nota tecnica: glow sem `filter: blur()`

Os glows do hero e da secao do form usam **falloff do proprio `radial-gradient`**, sem
`filter: blur()`. Motivo: `blur()` espalha cerca de 3x o raio para fora da caixa do
elemento e era cortado pelo `overflow:hidden` da secao, gerando uma **linha reta visivel**
no rodape do hero. Pelo mesmo motivo o `.hero` perdeu o `overflow:hidden` (a sombra do
aparelho precisa escapar) e o corte horizontal ficou por conta do `overflow-x:hidden`
do `body`. Se alguem reintroduzir `blur()` nesses elementos, o artefato volta.

## Estado

- [x] HTML gerado
- [x] OG image 1200×630 → `assets/og-evite-banimento-whatsapp.png` (regerada em 2026-08-30 a partir de `assets/og-template.html`)
- [x] Formulario integrado (Jotform `261034073026647`)

**Form provider:** Jotform (`261034073026647`, reintegrado em 2026-08-27)
- [ ] Revisao — rodar `/lp-revisar cxpress/evite-banimento-whatsapp`
- [x] Publicado em https://content.cxpress.io/evite-banimento-whatsapp (PR #345, deploy CI)

## Assets referenciados

- `./assets/hero-conta-banida-whatsapp.png` (LP-local, 430×901, PNG com alpha, 429 KB)
- `./assets/og-evite-banimento-whatsapp.png` (LP-local, OG 1200×630)
- `./assets/hero-circulos-concentricos.svg` (LP-local, fundo decorativo do hero, ~420 B)
- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `../../brand/cxpress/assets/logos/logo-primary.png` (JSON-LD, via placeholder)
- `./assets/clientes/cliente-01..42.png` (LP-local, 42 logos da esteira, 308 KB no total — copiados da LP `whatsapp-business`)
- `./assets/og-template.html` (LP-local, fonte da OG image; renderizar em 1200x630)
- `../../brand/cxpress/assets/plataforma/plataforma-canais.gif`
- `../../brand/cxpress/assets/plataforma/plataforma-chatbot-ia.gif`
- `../../brand/cxpress/assets/plataforma/plataforma-dashboard.gif`
- `../../brand/cxpress/assets/plataforma/quem-somos-foto.jpg`
- `../../brand/cxpress/assets/plataforma/elife-logo.png`

### Sobre o asset do hero

O briefing entregou um SVG de 596 KB que era so um wrapper: 2 PNGs em base64 (a arte e
uma mascara de luminancia) dentro de um `viewBox` com muito espaco vazio a esquerda. Foi
convertido para **um PNG unico com canal alpha real**, recortado no bounding box do
aparelho (medido na mascara) e re-encodado com filtro PNG adaptativo: 430×901, 429 KB.
Contra o GIF que era o visual do hero na referencia (`plataforma-canais.gif`, 2,4 MB),
o hero ficou cerca de 5x mais leve.

### Rodada 5 (2026-08-30, otimizacao de copy para Google Ads)

Copy nova do doc **"Otimizacao Banimento Whats (Google Ads)"**, aplicada via `/lp-revisar`.
Substituida em HERO, CLIENTES, BENEFICIOS, PLATAFORMA, FAQ e FECHO; PROVA e QUEM SOMOS
seguem como estavam (o doc pediu "deixar assim").

| # | O que | De | Para |
|---|---|---|---|
| 23 | Posicao do formulario | 2a dobra (logo depois de CLIENTES) | **ultima secao da pagina**, depois do FECHO. Os 9 CTAs continuam em `#agendar` |
| 24 | Chamada de preco | `Planos a partir de R$ 1.750 com 5 acessos` | `Planos a partir de R$ 1.750` (o doc pedia `R$ 990`; o Victor confirmou que o piso publico continua o do Basic — o que muda e so a linha, mais curta) |
| 25 | Secao CLIENTES | grade estatica (`clientes-cxpress.png`) alinhada a esquerda, titulo com peso de H2 | esteira infinita com os **42 logos da LP `whatsapp-business`**; titulo centralizado com peso de **subtitulo** (`.clientes__title`: fonte de corpo, 400, `clamp(18px,1.55vw,20px)`, sem a regua laranja) e secao curta (`44px 0 52px`) |
| 26 | FAQ | 5 perguntas | 8 perguntas (todas do doc) + `FAQPage` no JSON-LD |
| 27 | Rotulo de CTA | 1 rotulo unico | 2 rotulos, como o doc pede: `Agende uma demonstracao gratuita da plataforma` (hero, beneficios, fecho) e `Agendar demonstracao gratuita` (header, prova, 4 itens da plataforma) |
| 28 | CTA na secao BENEFICIOS | nao tinha | 1 botao solido no fim da grade de cards |
| 29 | Subtitulo em PLATAFORMA e FECHO | nao tinha | `.plataforma__sub` e `.fecho__sub` |
| 30 | Quebra de linha (GUIDELINES §21) | so `.btn` em `≤520px` | bloco unico de `text-wrap` com 20 seletores em `balance` e 3 em `pretty` |
| 31 | OG image | headline antiga ("Atendimento no WhatsApp sem risco de banimento") | regerada com o novo angulo, a partir de `assets/og-template.html` |
| 32 | `<title>` / meta description / OG / JSON-LD | angulo "evite banimento" | angulo "WhatsApp bloqueado ou banido" (preco segue `R$ 1.750`) |

Sobre o **delta 25**: a faixa de clientes e prova social de apoio, nao secao de conteudo — por isso o titulo perdeu o peso de H2 e a regua laranja, e a largura (`max-width:42ch`) esta calibrada pra fechar em **2 linhas** em 1440 / 1200 / 768 / 390px. Continua sendo um `<h2>` no HTML (a hierarquia semantica nao muda, so a visual).

Sobre a origem do delta 25: a esteira veio inteira da `whatsapp-business` (markup, CSS, mascara
de fade e os 42 PNGs), com as classes renomeadas pro padrao BEM desta LP
(`clients-track` → `clientes__track`). O que **nao** veio junto foram as **2 metricas**
(`85% de reducao de SLA`, `+220% de interacoes nas redes sociais`) que naquela LP ficam
entre o titulo e a esteira: o `+220%` ja e um dos 4 stats da secao PROVA desta pagina, e
repetir o numero duas vezes enfraquece os dois blocos. Se o Victor quiser as metricas
tambem, e copiar o bloco `.stats` da `whatsapp-business` (e ai vale tirar o `+220%` da PROVA).

Sobre o **delta 26**: o doc traz, na secao 7 (FAQ), um subtitulo **identico** ao da secao 6
(PLATAFORMA) — "Com a Cxpress, sua empresa nao apenas estrutura o uso do WhatsApp...".
Tem cara de copiar-e-colar do doc, e a frase nao fala de duvidas sobre banimento. Foi
aplicada so na PLATAFORMA. **Confirmar com o Victor** se ele quer mesmo repetir.

Sobre o **delta 30**: com o titulo novo (mais longo), o `balance` sozinho nao resolveu tudo.
Dois tetos de tipografia tiveram que mudar junto — `.fecho h2` de 48 para 44px (em 48 caia
em 3 linhas com 35% de desequilibrio; em 44 fecha em 2 com 14%) e `.agendar .section-title`
de 42 para 38px (cabe numa linha so dentro do card de 780px). O piso do `.hero h1` foi de
32 para 30px porque em 390px o `balance` deixava "WhatsApp" sozinho na primeira linha.
Duas armadilhas confirmadas na medicao, alem das ja documentadas na GUIDELINES §21:
`text-wrap` **nao age em `<span>` inline** (`.stat__label` precisou de `display:block`) e o
`<br class="brk">` do H2 do form brigava com o `balance` (removido).

**Medicao pos-mudanca** (desequilibrio = `1 − linha_menor / linha_maior`, via Range +
`getClientRects()`): em 1440px e 768px nenhum bloco de texto passa de 36% e nao ha orfa de
uma palavra; em 390px o unico resto e o rotulo do CTA outline do card sem imagem
("Agendar / demonstracao gratuita"), que nao cabe numa linha nos 286px disponiveis sem
furar o piso de 17px da GUIDELINES §20. `scrollWidth == clientWidth` em 390px.
