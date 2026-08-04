# LP Buzzmonitor — plataforma-integral-social-media

**Substituída em:** 2026-07-31 (a pedido explícito do usuário, via chat)
**Origem:** HTML trazido pelo usuário no chat, fora do pipeline padrão `/lp-preparar` → `/lp-gerar`. Não existe `copy.txt` fonte original — `copy.txt` deste commit é uma transcrição de auditoria feita a partir do HTML final.
**Região:** LATAM (ES) — `es-419`, GTM `GTM-MKQBX2MG` (mesmo container já validado nesta LP), Meta Pixel `935436740448328`.

Esta versão **substitui inteiramente** o design anterior ("Varias herramientas, cero eficiencia" — ver histórico git para a versão anterior). Slug e domínio (`content.buzzmonitor.com/plataforma-integral-social-media`) permanecem os mesmos; só o conteúdo/design mudou.

## Estrutura

1. HERO — "Toda tu operación de Social Media en una sola plataforma" + 6 tiles flutuantes dos módulos
2. Fila de logos de agências/marcas parceiras (Kaleidoscopio, McCann, Agencia Lead, Sube, Eureka&Co, Havas, TBWA)
3. DESAFIOS — 4 pain points
4. FEATURES — 6 módulos do produto
5. AUDIÊNCIAS — tabs interativas (Agencias / Empresas / Monitoreo y gestión de crisis), card única full-width em texto simples sobre gradiente (sem ilustração SVG) — restaurado em 2026-08-03 a pedido do usuário (ver nota abaixo)
6. BENEFÍCIOS — 4 cards
7. TESTIMONIOS — 6 quotes reais de clientes/agências
8. COMPARATIVA — Buzzmonitor vs. Sprinklr/Meltwater/Onclusive
9. CTA-FINAL — form Jotform
10. CLIENTS-PROOF — contadores animados + carrossel infinito de 30 logos de clientes
11. FOOTER

## Estado

- [x] HTML substituído (fluxo ad-hoc — ver "Notas de escopo" abaixo)
- [x] Logos reais de agências e clientes aplicados — baixados de `contenido.getbuzzmonitor.com/agencias` (autorização explícita do usuário) + brand assets locais
- [x] Interatividade: scroll-reveal, contadores animados, tiles flutuantes no hero, carrossel de logos auto-scroll (pausa no hover), tabs acessíveis (ARIA) na seção de audiências
- [x] Formulário integrado — Jotform, form id `241825239057661` (mesmo form já usado nesta LP antes da substituição)
- [x] Meta Pixel `935436740448328` adicionado (não existia na versão anterior desta LP)
- [x] OG image gerada (`assets/og-plataforma-integral-social-media.png`, 1200×630) via template + Chrome headless
- [ ] Auditoria formal `frontend-design` + `web-design-guidelines` (não rodada nesta sessão — ver nota abaixo)

## Alteração pontual em 2026-08-03

A pedido do usuário, dois ajustes sobre a versão interativa (sem reverter o resto):
- H2 da seção COMPARATIVA trocado de "¿Por qué migrar desde Sprinklr, Meltwater u Onclusive?" para "¿Por qué utilizar una plataforma que te cuesta caro y no te acompaña?"
- Seção "Diseñado para equipos que necesitan escalar": as 3 cards com tabs interativas foram substituídas pelas 3 cards estáticas com ilustração SVG do PR #152 (mesma H2, cards diferentes — a terceira mudou de "Gobierno e instituciones" para "Percepción pública y gestión de crisis", com copy também diferente). O JS de tabs (agora órfão, sem `.audience-tab` no DOM) foi removido; o CSS de tabs/animação de troca (`audience-fade`) também. Mantido o `reveal` (scroll-in) em cada card, consistente com o resto da página — o PR #152 não tinha esse efeito, mas é o padrão já usado nos outros grids desta LP.

## Bugs corrigidos em 2026-08-03 (pós-troca de cards do PR #152)

- **Ícone sobreposto ao texto nas cards de "Diseñado para equipos"**: `.audience__art` usava `position:absolute` com altura fixa (%), o que colidia com o texto quando o título/parágrafo era mais longo (a 3ª card, "Percepción pública y gestión de crisis", tem título de 3 linhas). Corrigido trocando `.audience` pra `flex-direction:column` e `.audience__art` pra item flex (`flex:1 1 auto`, sem `position:absolute`) — o espaço do ícone agora se ajusta automaticamente ao espaço que sobra acima do texto em cada card, sem número mágico por card.
- **Logos sumindo no carrossel infinito de clientes** (ex: McCann): todas as 60 imagens do `.logo-marquee__track` tinham `loading="lazy"`, mas como o track é um `flex` com `width:max-content` bem mais largo que a viewport (as imagens ficam posicionadas bem longe da área visível antes da animação as trazer), o navegador nunca disparava o carregamento de várias delas — ficavam com `naturalWidth:0` pra sempre. Removido `loading="lazy"` das 60 imagens do carrossel (mantido nas 7 da fila estática de agências, onde não há esse problema).

## Mais animações + ajuste de título (2026-08-03)

- Título da 3ª card de "Diseñado para equipos": "Percepción pública y gestión de crisis" → "Monitoreo y gestión de crisis" (mesma copy do parágrafo, só o título).
- Hover-lift (translateY + sombra) em `.pain-card`, `.feature-card`, `.benefit-card`, `.quote-card` e `.audience`.
- Reveal em cascata: cards dentro de `.pain-grid`, `.feature-grid`, `.benefit-grid`, `.quote-grid` e `.audiences-grid` agora entram com delay escalonado (0, .08s, .16s...) em vez de todos ao mesmo tempo.
- Pulso sutil de sombra (`cta-pulse`, 2.6s loop) no botão primário do hero, pausado no hover.
- Sublinhado animado nos links do menu (`.nav-links a`) ao passar o mouse.
- Ícone do `.feature-card` escala + rotaciona levemente no hover do card.
- Linha da tabela comparativa destaca o fundo no hover.
- Todas cobertas pelo kill-switch `prefers-reduced-motion` já existente no arquivo.

## Logo McCann atualizado (2026-08-03)

Trocado `assets/logos-agencias/mccann.png` e `assets/logos-clientes/mccann.png` pelo wordmark oficial enviado pelo usuário (`~/Downloads/McCANN-1.png`), recortado e com fundo transparente (446×88). Aparece 3x no HTML (fila pequena de agências + 2x no carrossel grande de clientes) — as 3 instâncias verificadas carregando com as dimensões corretas.

## Restauração das tabs em "Diseñado para equipos" (2026-08-03)

O usuário pediu de volta o padrão de tabs (botões pill + 1 card full-width que troca ao clicar), mostrando um screenshot do estado anterior à troca pelas cards do PR #152. Reimplementado: `.audience-tabs` (3 botões) + `.audiences-grid` com `display:block` (só a `.audience` ativa é visível, `[hidden]` nas demais) + JS de clique (`tabs.forEach(...)`) restaurado no `<script>`. Título do 3º tab já reflete a mudança pedida antes ("Monitoreo y gestión de crisis").

Os ícones SVG do PR #152 foram removidos nesta etapa (cover-fit `xMidYMid slice` quebrava num card full-width, ver histórico do commit). **Trazidos de volta em seguida** (mesmo dia, a pedido do usuário) como selo decorativo de tamanho fixo, sem `preserveAspectRatio="slice"` — em vez de esticar a arte pra cobrir o card inteiro (o que causava o corte), ela renderiza no tamanho natural do viewBox.

Ajuste fino (mesmo dia, feedback "muito pequeno e cravado no canto"): ícone aumentado de 190px pra 300px e reposicionado do canto superior direito (`top/right:24px`) pra centralizado verticalmente à direita (`top:50%; transform:translateY(-50%); right:60px`). Pra garantir que o texto (agora com `.audience__copy{max-width:620px}`, fica à esquerda) nunca colida com o ícone (à direita) mesmo em cards com título de 3 linhas, verificado via `getBoundingClientRect()` nas 3 tabs — zero overlap. Em telas ≤900px o ícone encolhe pra 190px; em ≤640px (mobile) é ocultado (`display:none`), já que o card fica estreito demais pra caber os dois lado a lado.

## Ícones centralizados + "Empresas" (2026-08-04)

Feedback do usuário: ícones ainda pequenos e colados no canto superior direito. Duas causas, as duas corrigidas:

1. **Posição/tamanho.** Trocado de `position:absolute` no canto pra item de flex empilhado: `.audience` virou `flex-direction:column; justify-content:flex-end` (ícone em cima, texto embaixo) e `.audience__art` ficou `height:260px; width:auto; margin:0 auto 26px` — o `margin:auto` horizontal centraliza. Card subiu de 420px pra 460px de altura pra caber com folga. Nota: a primeira tentativa usou `width:100%` + `flex:1`, o que **estourou o card pra 1336px** de altura (o SVG tem ratio intrínseco 400:420, então largura 100% força altura proporcional). A correção é fixar a **altura** e deixar `width:auto`.
2. **`viewBox` folgado (a causa real do "pequeno").** Os 3 SVGs vinham com `viewBox="0 0 400 420"`, mas o desenho ocupava só uma faixa central — o resto era vazio, então o ícone renderizava pequeno mesmo com 260px de caixa. Recalculados os `viewBox` pelas coordenadas reais de cada arte: `83 147 252 103` (avatares), `112 58 176 225` (pins + gráfico), `129 94 142 145` (triângulo de alerta). Agora a arte preenche a caixa.

Verificado nas 3 tabs via `getBoundingClientRect()`: centralizado horizontalmente, zero overlap com o texto, card 460px. Screenshots das 3 conferidas (variantes temporárias no dist com cada painel ativo, já removidas).

Também trocado o label da 2ª tab/card de "Marcas regionales" pra **"Empresas"** (`index.html` + `copy.txt`). Os ids internos (`tab-marcas`/`panel-marcas`) ficaram como estavam — são âncoras internas, não texto visível.

## Ícones maiores + logos Amazon/L'Oréal (2026-08-04)

**Ícones das cards.** Feedback: ainda pequenos, com muito espaço vazio, e o da card 3 desalinhado (mais alto). Corrigido em três frentes:
- `viewBox` apertado de padding 10px pra 4px nos 3 SVGs (`89 153 240 91`, `118 64 164 213`, `135 100 130 133`), tirando o vazio restante em volta do traço.
- Altura da arte 260px → 300px; card 460px → 480px.
- **Causa do desalinhamento da card 3:** ela era a única com o parágrafo quebrando em 2 linhas (copy de 98px vs 74px das outras), por causa do `.audience__copy{max-width:620px}` que existia antes — texto mais alto empurrava a arte pra cima. Com o `max-width` removido, as 3 têm copy de 74px. Também trocado `justify-content:flex-end` + `margin:0 auto 26px` por `margin:auto` na arte, que reparte o espaço livre igualmente acima/abaixo. Medido nas 3 tabs: `gapTop` 53px e `gapArtToText` 23px **idênticos**, zero overlap.

**Logos.** `logos-clientes/amazon.png` e `logos-clientes/loreal.png` trocados pelos arquivos oficiais enviados pelo usuário (`~/Downloads/Amazon_logo.svg.webp` e `LOreal-logo.png`), recortados no traço e normalizados pra 88px de altura (291×88 e 461×88). Diferente do caso McCann, **não** precisaram de compensação de tamanho: o ratio do conteúdo bate com o dos arquivos antigos (Amazon 3.31 vs 3.28; L'Oréal 5.24 vs 5.37), então renderizam do mesmo tamanho que antes na altura fixa do CSS. Os dois já vinham com fundo transparente (checado no canal alpha) — importante porque o muro aplica `brightness(0) invert(.55)`, e um fundo branco viraria um bloco preto. Conferidos os dois estados (cinza normal / cor real no hover) contra os logos vizinhos.

## Ícones das cards reduzidos 40% (2026-08-04)

Feedback: ficaram grandes demais. Altura da arte 300px → **180px** (exatamente 40% menos). Card baixada de 480px pra 400px junto, senão sobraria buraco vazio no meio (o `margin:auto` reparte o espaço livre, então card alta + arte pequena = muito vão). Medido nas 3 tabs: `artH` 180px, `gapTop` 73px, `gapToText` 43px, iguais nas três, sem overlap. Breakpoint mobile ajustado na mesma proporção (180px → 110px).

## Ilustrações normalizadas por área + cards mais estreitas (2026-08-04)

Diagnóstico do usuário confirmado com medição: as 3 ilustrações tinham **larguras muito diferentes**. Fixar só a `height` (180px) dava 475px, 139px e 176px de largura, porque as formas são muito distintas (avatares = faixa horizontal larga; pins = composição vertical; triângulo = quase quadrado). Área renderizada ia de 85.451 px² a 24.946 px², ou seja a arte de "Agencias" pesava 3,4x mais que a de "Empresas".

Correções:
- **Normalização por área.** Agora a largura manda (via `--art-w` por painel) e foi calculada pra que as 3 rendam com ~20.000 px² cada: 230px, 124px e 140px de largura. Áreas medidas: 20.058 / 19.970 / 20.052.
- **Slot de altura fixa.** A arte vive num slot de altura fixa igual pra todas (`--art-slot`, 170px desktop / 120px mobile) e o texto usa `margin-top:auto`. Antes a arte era centralizada no espaço livre com `margin:auto`, então quando o texto de uma card ocupava mais linhas o ícone subia — era isso que fazia a 3ª card parecer desalinhada, e o problema reaparecia em mobile (centro em 103px vs 136px). Com o slot fixo o **centro óptico é idêntico** nas 3: 115px no desktop, 90px no mobile, mesmo com a 3ª card tendo texto de 164px vs 98px.
- **Cards mais estreitas.** `.audiences-grid` e `.audience-tabs` com `max-width:900px; margin-inline:auto` (antes usavam os 1180px do container).
- **Mobile.** `min-height` da card 370px → 300px (o vão vazio no meio era grande demais nessa largura) e `margin-bottom:18px` na arte pra garantir respiro mínimo até o texto. Medido: gap 51/24/26px, nenhuma arte transborda, `scrollWidth == viewport` (sem scroll horizontal).

## Aire igual acima/abaixo da ilustração (2026-08-04)

Feedback: as imagens pareciam "cargadas hacia arriba". Causa: o texto estava ancorado no fundo com `margin-top:auto` e a arte ficava num slot de altura fixa no topo, então todo o espaço livre caía **entre** a arte e o texto (desktop: 74px acima da arte vs 107px abaixo).

Solução: a arte agora usa `flex:1 1 auto` e cresce pra ocupar todo o espaço livre acima do texto; o próprio SVG se centraliza dentro dela (`preserveAspectRatio` default). Assim o aire acima e abaixo é **matematicamente igual** em qualquer altura de card e qualquer comprimento de texto, sem número mágico. `min-height: var(--art-h)` (o alto natural naquele `--art-w`) serve de piso pra que a arte nunca encolha abaixo do tamanho normalizado por área. Removido o `margin-top:auto` do `.audience__copy` e o `--art-slot`, que ficaram sem uso.

Medido (aire acima / aire abaixo):
- Desktop: 74/74, 37/37, 46/46 — centro óptico idêntico nas 3 (148px).
- Mobile: 70/70, 43/43, 16/16.

`min-height` da card em mobile subiu 300px → 360px: com 300px a 3ª card (título em 2 linhas, texto de 164px) ficava com aire **0/0**, ou seja a arte encostava no texto. Com 360px o pior caso tem 16px de folga de cada lado.

## Logo McCann reduzido 30% (2026-08-03)

O wordmark novo (ver seção acima) ficou maior que os logos vizinhos por causa do aspect ratio mais alongado (5:1 vs ~3:1 do antigo), mesmo com a altura CSS fixa (`height:28px`/`max-height:34px`) igual pra todos. Como a altura é fixa via CSS, reduzir o arquivo de origem sozinho não mudaria o tamanho renderizado — a correção foi adicionar padding transparente vertical no próprio PNG (88px → 126px de altura, 19px de padding em cada lado), o que faz o logo visível ocupar 70% do espaço na mesma altura de render, encolhendo também a largura proporcionalmente (mesmo efeito visual de um "zoom out" de 30%).

## Notas de escopo (decisões tomadas nesta substituição)

- **Não passou pelo `/lp-revisar` formal.** O design foi construído e iterado diretamente no chat (fora do pipeline), com verificação manual de: contraste/legibilidade visual, estados de hover, acessibilidade dos tabs (roles ARIA, `aria-selected`, `hidden`), `prefers-reduced-motion` (kill-switch já presente cobre as novas animações), e paths de asset (convenção `../../brand/{marca}/assets/...` pra brand assets, `./assets/...` pra assets LP-local, per `landing-pages/CONTEXT.md` §3.2). Recomendado rodar `/lp-revisar` numa próxima iteração pra auditoria formal.
- **Paleta**: laranja `#ff6b16` + rosa `#ec174c` (gradiente), tom mais vibrante que o `--gradient-safe` usado na versão anterior desta LP — decisão do design trazido pelo usuário, não recalibrado pro token `--orange-ink` de contraste AA usado alhures no repo.
- **Duplicata conhecida**: existe uma LP quase idêntica em `landing-pages/buzzmonitor/plataforma-completa-social-media-latam/` (mergeada em main via PR #150/#151, no mesmo dia), criada por outra sessão em paralelo a partir do mesmo HTML de origem. Ela está **desatualizada** em relação a esta versão (não tem a troca de IPG Mediabrands → Agencia Lead, os fixes de hover de Havas/Eureka&Co, nem a interatividade) e **não está atribuída a nenhum domínio**. Ficou como está — o usuário decidiu não mexer nela nesta rodada; considerar remover ou consolidar numa limpeza futura.
- **Testimonios**: 6 quotes reais de clientes/agências (McCann, Kaleidoscopio, Publicis, Eureka&Co, SA365, Sube Agencia) — mesma fonte usada no README da LP duplicada acima (`contenido.getbuzzmonitor.com/agencias`).

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header + footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon + marca decorativa do hero)
- `./assets/og-plataforma-integral-social-media.png` (OG image, LP-local)
- `./assets/logos-agencias/*` (8 imagens — Kaleidoscopio, McCann, Agencia Lead em 2 partes LEAD/DIGITAL, Sube, Eureka&Co, Havas, TBWA)
- `./assets/logos-clientes/*` (30 imagens — Coca-Cola, Sephora, Samsung, IKEA, Amazon, Uber, etc.)
