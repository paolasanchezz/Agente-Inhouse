# Revisao LP — cxpress/evite-banimento-whatsapp

**Data:** 2026-08-30
**Escopo pedido:** aplicar a copy otimizada do doc "Otimizacao Banimento Whats (Google Ads)", trazer a secao de clientes exatamente como esta em `content.cxpress.io/whatsapp-business` e eliminar orfa de linha / desequilibrio de peso entre linhas.
**Auditores:** medicao instrumentada de quebra de linha (Range + `getClientRects()` agrupado por `top`) em 1440 / 768 / 390px + render headless (Chromium) da pagina inteira + GUIDELINES §20 e §21.

> A revisao de 2026-08-27 (mobile/responsividade) esta preservada no fim deste arquivo.

## Aplicado

### Copy (doc do Google Ads)

- [x] **HERO** — H1, os 2 paragrafos de subtitulo e o CTA trocados pelo texto do doc. Nenhuma frase nova escrita.
- [x] **CLIENTES** — titulo do doc ("...para otimizar suas operacoes de atendimento").
- [x] **BENEFICIOS** — titulo (`...da Meta`), os 3 pares H3/BODY e o CTA da secao (novo).
- [x] **PROVA** — mantida ("deixar assim" no doc). CTA segue `Agendar demonstracao gratuita`.
- [x] **PLATAFORMA** — titulo novo + subtitulo novo + os 4 pares H3/BODY.
- [x] **FAQ** — titulo novo e as 8 perguntas do doc (eram 5). Corrigido o espaco que faltava no doc em "contas banidas.A plataforma".
- [x] **FECHO** — titulo + subtitulo + CTA do doc. O `<span class="linha2">` da versao antiga saiu junto.
- [x] **Preco** — `Planos a partir de R$ 1.750 com 5 acessos` → `Planos a partir de R$ 1.750`. O doc pedia `R$ 990`; levantei a divergencia com a `/planos` e o Victor confirmou que o piso publico continua o do Basic. O que sobrou do pedido do doc e a linha mais curta, sem "com N acessos".

### Estrutura

- [x] **Formulario movido para a ultima secao da pagina** (depois do FECHO), como o doc pede. Os **9** CTAs da pagina apontam para `#agendar` (header, hero, beneficios, prova, 4 itens da plataforma, fecho) — conferido por `grep`.
- [x] **Titulo da secao CLIENTES com peso de subtitulo** — a pedido do Victor, virou `.clientes__title`: fonte de corpo, `font-weight:400`, `clamp(18px,1.55vw,20px)`, sem a regua laranja, `max-width:42ch` calibrado pra fechar em **2 linhas** (conferido em 1440 / 1200 / 768 / 390px). Secao encurtada de `56px 0 72px` para `44px 0 52px` e a esteira subiu de 36 para 26px de `margin-top`. Segue `<h2>` no HTML — muda o peso visual, nao a hierarquia semantica.
- [x] **Secao CLIENTES trocada pela esteira da `/whatsapp-business`** — markup, CSS, mascara de fade nas pontas, pausa no hover e os 42 PNGs (`assets/clientes/`, 308 KB). Classes renomeadas pro BEM desta LP. Geometria conferida no navegador: 2 grupos identicos de 6353px, track de 12706px, animacao `-50%` → loop sem emenda; nenhuma imagem quebrada.
- [x] **`FAQPage` no JSON-LD** com as 8 perguntas (a LP `/whatsapp-business` ja segue esse padrao). O `@graph` ja tinha Organization + WebPage + SoftwareApplication.
- [x] **Metadados** — `<title>`, meta description, 10 tags `og:`, 4 `twitter:` e as descricoes do JSON-LD passaram pro angulo novo e pro preco novo.
- [x] **OG image regerada** — a antiga dizia "Atendimento no WhatsApp **sem risco** de banimento", que agora contradiz a propria FAQ da pagina ("Nao existe garantia de risco zero"). Nova arte em `assets/og-evite-banimento-whatsapp.png`, com fonte versionada em `assets/og-template.html` (renderizar em 1200×630).

### Quebra de linha (GUIDELINES §21)

- [x] **Bloco unico de `text-wrap`** no `<style>` do head: 20 seletores em `balance` (H1, H2, H3, subtitulos, item de card, pergunta de FAQ, resposta de FAQ, labels de stat, nota, CTAs) e 3 em `pretty` (`.hero__sub`, `.quem-somos p`, `.footer p` — corpo longo).
- [x] **`.stat__label{display:block}`** — era `<span>` inline e o `balance` era simplesmente ignorado (a caixa que forma as linhas e o bloco pai). Com o `display:block` o rotulo "mais produtividade da IA..." saiu de 69% para 36% de desequilibrio.
- [x] **`<br class="brk">` removido do H2 do form** — brigava com o `balance` e produzia 158px + 317px (§21, ressalva 2).
- [x] **`.fecho h2` de 48 → 44px** — em 48px o titulo novo caia em 3 linhas com 35% de desequilibrio; em 44px o `balance` fecha em 2 linhas com 14%.
- [x] **`.agendar .section-title` de 42 → 38px** — cabe numa linha so dentro do card de 780px (654px de 668 uteis). Em 42px quebrava em 2 linhas com 50%.
- [x] **Piso do `.hero h1` de 32 → 30px** — em 390px o `balance` deixava "WhatsApp" sozinho na primeira linha. Em 30px fecha em 4 linhas, o mesmo corte do desktop.
- [x] **`.hero__sub--2`** — o segundo paragrafo do hero e curto (2 linhas) e recebe `balance`; o primeiro, longo, fica em `pretty`. Como os dois seletores tem a mesma especificidade, o bloco de `pretty` vem **antes** do de `balance` de proposito.

## Medicao pos-mudanca

Desequilibrio = `1 − linha_menor / linha_maior`. Blocos de 1 linha ignorados.

| Viewport | Blocos acima de 30% | Orfa de 1 palavra |
|---|---|---|
| 1440px | 3 (36% / 30% / 36%) | nenhuma |
| 768px | 1 (36%) | nenhuma |
| 390px | 10 | nenhuma |

Os 3 restantes em 1440px sao copy **pre-existente**, nao tocada nesta rodada:
`.stat__label` "mais produtividade da IA..." (36%), `.feature h3` "Dashboards para acompanhar
a operacao" (30%, 2 linhas sem orfa) e `.quem-somos p` (36%, 7 linhas, ultima com 64% da
maior — `pretty`, comportamento esperado para corpo longo).

Ganho medido nos blocos que mudaram (desktop 1440):

| Bloco | Antes | Depois |
|---|---|---|
| `.card p` (Integracao oficial) | 65% | < 30% |
| `.feature p` (Atendimento 24/7) | 64% | < 30% |
| `.feature p` (Gestao de tickets) | 74% | < 30% |
| `.faq details p` (CoEx) | 82% | < 30% |
| `.faq details p` (API Oficial) | 70% | < 30% |
| `.stat__label` (produtividade da IA) | 69% | 36% |
| `.fecho h2` | 35% (3 linhas) | 14% (2 linhas) |
| `.agendar .section-title` | 50% (2 linhas) | 1 linha |

`scrollWidth == clientWidth` em 390px. Render headless da pagina inteira conferido secao a secao.

## Pendente de decisao do Victor (1)

- [ ] **Subtitulo da FAQ.** O doc traz, na secao 7, um subtitulo **identico** ao da secao 6 (PLATAFORMA): "Com a Cxpress, sua empresa nao apenas estrutura o uso do WhatsApp. Toda a operacao de atendimento pode ser centralizada em uma unica plataforma." Tem cara de copiar-e-colar, e a frase nao fala de duvidas sobre banimento. Foi aplicada **so** na PLATAFORMA. Se voce quiser mesmo a repeticao, e 1 linha de HTML.
- [x] ~~**Preco `R$ 990` diverge da `content.cxpress.io/planos`.**~~ Resolvido em 2026-08-30: o Victor confirmou `R$ 1.750`. As duas LPs voltaram a dizer o mesmo piso.

## Melhorias opcionais (3)

- [ ] **Peso da esteira de clientes** — sao 84 `<img>` (42 × 2 grupos), track de 12706px. Os 8 primeiros carregam eager e o resto e `lazy`, igual a `/whatsapp-business` que ja esta em producao. Se o LCP piorar, o caminho e um sprite ou WebP.
- [ ] **3 GIFs da plataforma** (`plataforma-canais.gif`, `plataforma-chatbot-ia.gif`, `plataforma-dashboard.gif`) — Web Interface Guidelines pedem `<video autoplay muted loop playsinline>`. Exige converter os assets em `brand/cxpress/` (vale pra todas as LPs que os usam).
- [ ] **`<meta name="theme-color">`** ausente — a barra do navegador no Android/iOS nao acompanha o fundo da pagina.

## Nice-to-haves (2)

- [ ] CTA outline do card sem imagem (`Gestao de tickets e filas`) quebra em 2 linhas em 390px — "Agendar / demonstracao gratuita". O rotulo nao cabe nos 286px disponiveis sem furar o piso de 17px da §20. O `balance` ja escolheu o melhor dos dois cortes possiveis.
- [ ] Glows `.a-glow`/`.a-glow2` da secao do form sangram e sao cortados pelo `overflow-x` do body; podiam ser contidos na largura do card.

## Nao verificavel localmente

- **Embed do Jotform:** no render local o iframe carrega, mas a altura final so estabiliza em producao. Vale conferir a altura da ultima secao no celular depois do deploy — agora ela e a ultima coisa antes do rodape.

## Proximos passos

- Deploy: dominio migrado (`content.cxpress.io`) → PR de conteudo, o CI publica (`/lp-publicar`).
- Conferir no celular real: hero (4 linhas), a esteira de logos e a altura do form no fim da pagina.

---

# Revisao anterior — 2026-08-27

**Escopo pedido:** ajustar a versao mobile para responsividade
**Auditores:** frontend-design (review mode) + web-design-guidelines + medicao instrumentada (Playwright em 320 / 360 / 390 / 430 / 640 / 768px) + `check_mobile_type.py` + `check_gtm_region.py`

## Aplicado automaticamente (6 criticos e ajustes de mobile)

- [x] **CTA outline da PLATAFORMA quebrado no mobile** — `.feature__cta` — o rotulo quebrava em 2 linhas e a seta ficava solta na borda direita de um botao quase full-width. Agora, em `≤640px`: `padding:14px 18px`, `gap:8px`, conteudo centrado. Em 390px cabe numa linha (medido: 61px de altura = 1 linha); em 320/360px sao 2 linhas centradas.
- [x] **Seta solta em tela muito estreita** — `.feature__cta::after` — escondida em `≤360px`, onde o rotulo em 2 linhas ao lado da seta lia mal.
- [x] **CTA principal em 3 linhas dentro do card do fecho a 320px** — `.btn` — com o piso de 17px (GUIDELINES §20) o rotulo nao cabe numa linha, e o `padding:16px 34px` empurrava pra 3. Em `≤520px`: `display:block`, `width:100%`, `padding:16px 18px`, `text-align:center`, `text-wrap:balance` → 2 linhas centradas, botao full-width (padrao de mobile e alvo de toque maior).
- [x] **Alvo de toque do CTA do header abaixo de 44px** — `.navbar__cta` media 40px de altura no mobile. `padding:12px 16px` em `≤640px` → 46px medidos. O rotulo curto (`Agendar demo`) segue evitando overflow.
- [x] **`<img>` sem dimensoes (CLS)** — logo Elife em QUEM SOMOS — adicionado `width="250" height="140"` + `loading="lazy"`. Era a unica das 9 imagens sem dimensao explicita.
- [x] **Atraso de toque e flash cinza no Android** — `a,button,summary,input,label` ganharam `touch-action:manipulation` e `-webkit-tap-highlight-color` intencional (Web Interface Guidelines, secao Touch & Interaction).

### Ajustes de composicao mobile aplicados no mesmo escopo

- [x] **Aparelho do hero fixo em 230px** — `.hero__phone` em `≤980px` virou `max-width:min(62vw,260px)`: 198px em 320, 242px em 390, 260px em 430. Antes ficava pequeno num iPhone Pro Max e grande num 320px.
- [x] **Pilulas decorativas colidindo em tela estreita** — em `≤520px` saem `.fecho__pills .f2` (colava no CTA do fecho) e `.hero__decor .pill-2` (flutuava sobre os circulos sem ancorar a composicao; a `pill-1` ja saia em 980px). Reversivel: e uma decisao de composicao, nao um bug de layout.
- [x] **Rodape full-bleed em iPhone com home indicator** — `.footer{padding-bottom:calc(56px + env(safe-area-inset-bottom))}` em `≤640px`.

## Verificado sem achado

- **Overflow horizontal:** `scrollWidth == clientWidth` em 320, 360, 390, 430, 640 e 768px. Os 3 itens que o `check_mobile_type.py` acusa sao pre-existentes e por design: `.skip-link` (fora da tela em `left:-9999px`) e os glows `.a-glow`/`.a-glow2` da secao do form (decorativos, cortados pelo `overflow-x:hidden` do body).
- **Pisos de tipografia (GUIDELINES §20):** h1=36px, corpo=18px no mobile. `bump_mobile_type.py --dry-run` → 0 clamps a ajustar. O `min=13px` medido e o CTA do header, coberto pela excecao de `white-space:nowrap`.
- **Pacote SEO (§15):** description 1, robots 1, og 10, twitter 4, JSON-LD 1, canonical 1.
- **hreflang (§16):** LP sem irmas `-es`/`-pt` (as LPs `banimento-whatsapp-latam` e `-pt` tem outro slug-base) → hreflang dispensavel.
- **Logo regional (§17) e logo web-safe (§19):** header e footer apontam pra `https://home.cxpress.io` com `target="_blank" rel="noopener"`; nenhum SVG de logo com `<text>` vivo.
- **OG image (§18):** `og-evite-banimento-whatsapp.png` presente, 1200×630, sem `og-image.png` orfao.
- **Anti-IA:** 0 em-dash (`—`/`&mdash;`) no HTML.
- **Motion:** bloco `prefers-reduced-motion` presente e cobrindo animacao, transicao e `.reveal`; nenhum `transition:all`.
- **GTM:** `check_gtm_region.py` retorna `wrong` porque a regiao brasil espera `GTM-T4XDWHL3`, mas o container `GTM-KN8BPFG` e uma escolha documentada desta LP (delta #3 do README) e esta selada em `.tracking.lock` (`stamp_match=true`, `grandfathered=true`). Nada a corrigir.
