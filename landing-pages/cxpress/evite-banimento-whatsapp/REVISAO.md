# Revisao LP — cxpress/evite-banimento-whatsapp

**Data:** 2026-08-27
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

## Melhorias opcionais (3)

Para o usuario decidir. Aplicar via Edit manual ou pedir `/lp-revisar` de novo.

- [ ] **Faixa de logos de clientes no mobile** — `.clientes__grid img` — a imagem e uma folha de 1886×906 com 10 logos; em 342px de largura cada logo fica com ~60px. Alternativa: versao mobile da imagem em 2 linhas de 5 logos, ou marquee horizontal.
- [ ] **3 GIFs da plataforma** (`plataforma-canais.gif`, `plataforma-chatbot-ia.gif`, `plataforma-dashboard.gif`) — Web Interface Guidelines pedem `<video autoplay muted loop playsinline>` no lugar de GIF animado. Ganho real em dados moveis, mas exige converter os assets em `brand/cxpress/` (vale pra todas as LPs que os usam, nao so esta).
- [ ] **`<meta name="theme-color">`** ausente — a barra do navegador no Android/iOS nao acompanha o fundo da pagina.

## Nice-to-haves (2)

Estilistico. Ignorar e aceitavel.

- [ ] Glows `.a-glow`/`.a-glow2` da secao do form podiam ser contidos na largura do card em vez de sangrar e serem cortados pelo `overflow-x` do body.
- [ ] `text-wrap:balance` nos H2 de secao — no mobile os titulos centrados de 3 linhas quebram irregular (ex: "Resultados de quem estruturou o atendimento com a Cxpress").

## Nao verificavel localmente

- **Embed do Jotform (form principal):** no render local por `file://` o iframe nao carrega e a secao AGENDAR aparece com ~900px vazios. Em producao o provedor renderiza o card proprio. Vale conferir a altura da secao no celular depois do deploy.

## Proximos passos

- Deploy: dominio migrado (`content.cxpress.io`) → PR de conteudo, o CI publica.
- Conferir no celular real: hero, os 4 CTAs outline da PLATAFORMA e a altura do form.
