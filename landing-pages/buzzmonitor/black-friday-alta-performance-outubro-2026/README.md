# LP Buzzmonitor — black-friday-alta-performance-outubro-2026

**Gerado em:** 2026-08-27
**Copy-fonte:** `copy.txt` (output de /lp-preparar, a partir de copy colada pelo usuário no chat, revisada contra o Google Doc "Da Campanha ao Pós-Venda: Como Preparar sua Marca para uma Black Friday de Alta Performance")

## Origem

Nova edição da série de eventos presenciais exclusivos para clientes Buzzmonitor, no mesmo endereço e guarda-chuva da LP `buzztalk-gestao-multimarcas-para-agencias` (Av. Paulista, 807, Bela Vista, São Paulo). Publicada para `content.buzzmonitor.com`.

**Redesenho 2026-08-27 (pedido do usuário):** estrutura de seções reaproveitada de `buzztalk-gestao-multimarcas-para-agencias`, mas identidade visual trocada para a da série **Buzzconnect** (referência: `buzzmonitor-connect-julio-2026-latam`, mesma linhagem do `conteudo.buzzmonitor.com.br/buzzconnect-presencial-2026` original) — estética "sticker"/neobrutalista: fundo creme `#FAF6F0` + tinta `#121212`, cartões com borda grossa `#121212` e sombra sólida deslocada (`box-shadow: Npx Npx 0 cor`), blobs orgânicos animados, selo de data tracejado rotacionado, gradiente rosa→laranja usado só em destaques pontuais de texto (nunca como fundo de seção inteira), CTA com pulso, e CTA fixo mobile. Tipografia League Spartan (display) + **Manrope** (sub, no lugar do Hanken Grotesk) + Lato (corpo).

**Ajuste 2026-08-27 (mesma sessão):** a pedido do usuário, as 3 dobras escuras (Urgência, CTA final, Footer) passaram de roxo `#390155` para preto `#0a0a0a`, reforçando visualmente o tema "Black Friday". Texto branco/laranja vibrante nessas seções recontrastado contra o novo fundo (todos ≥7:1, folga confortável). O laranja escurecido `--c-orange-text` (usado só em seções claras) não é usado em nenhuma das 3 seções pretas, evitando reintroduzir o gap de contraste. Botão `.btn--ghost-onpurple` renomeado para `.btn--ghost-ondark` (mesmo comportamento, nome correto).

**Nota de acessibilidade:** o laranja `#CE5F14` e o teal `#0E9D9B` da paleta Buzzconnect falham contraste AA como texto pequeno sobre fundo claro (~2,6-3,7:1, replicando um gap já presente na LP de referência `buzzmonitor-connect-julio-2026-latam`). Foram criadas variantes seletivas `--c-orange-text:#a54c10` e `--c-teal-text:#0a7674` só para uso como texto (labels, links, títulos de destaque), mantendo o laranja/teal vibrantes originais em botões, ícones e decoração. Badges do cronograma usam teal/laranja com texto tinta (`#121212`, ambos ≥5,6:1) em vez de branco (branco sobre teal e sobre laranja falham AA, ~3,3:1 e ~2,8:1).

**Ajuste 2026-08-27 (rodada 2, feedback visual do usuário):**
- Corrigido padding duplicado no hero (a seção herdava o padding genérico de `section` *e* o próprio `.hero__layout` somava mais em cima — margem superior gigante). `.hero` agora zera o padding genérico.
- Títulos centralizados nas dobras Visão 360 e Palestrantes (kicker + H2 + lead); grid de palestrantes também centralizado no eixo horizontal.
- "Para quem é este evento" trocou a lista numerada por uma grade de 10 chips com ícone (perfil) + rótulo — mais visual, mesmo texto literal da copy.
- Identidade Buzzconnect reforçada a pedido do usuário: **teal `#0E9D9B` + preto + laranja** agora são as 3 cores dominantes da LP. Removido roxo/rosa de uso ativo (variável `--c-purple`/`--c-pink` ficam definidas mas sem uso ativo no momento) — trocados por teal/teal-text nos ícones de palestrante, blob do footer, texto de destaque (`.learn-close`, `.publico__outro`), hover do botão fantasma, anel decorativo da Urgência, e badges do cronograma.
- Todas as cores novas/realocadas foram recontrastadas (WCAG) antes de aplicar — ver `Validação local` abaixo.

**Ajuste 2026-08-27 (rodada 3, feedback: "para quem é" ainda não convenceu + laranja pouco vibrante + fundos muito sólidos/monocromáticos):**
- **"Para quem é este evento" redesenhada de novo** — de chips simples (ícone+rótulo monocromático) para **crachás de evento**: cartão levemente rotacionado (ângulo alternado por posição), com "presilha" no topo, borda grossa e sombra sólida, alternando fundo entre creme/laranja vibrante/teal/preto (5 de 10 coloridos, distribuídos), sempre com contraste verificado (tinta sobre laranja/teal ≥5,6:1, branco sobre preto ≥19:1). Ganha o clima de "crachá de credenciamento" do próprio evento presencial.
- **Laranja mais vibrante**: o destaque em texto (`.highlight-mark`, usado no H1 do hero e no H2 da seção final) e o selo de data (`.stamp`, "01/OUT") deixaram de usar um gradiente rosa/teal→laranja **escurecido** (necessário pra passar contraste como texto, mas ficava opaco/amarronzado) e passaram a usar **laranja cheio `#EB7C2E` sólido com texto tinta** — mesma cor vibrante do botão principal, sem diluição. Os números do contador regressivo também deixaram de usar texto em gradiente (também escurecido) e agora são chips sólidos laranja/teal alternados com texto tinta — mais vívido e também mais colorido. A variável `--grad-brand` (gradiente) foi removida por ficar sem uso.
- **Fundos menos sólidos/monocromáticos**: 
  - Textura de grão (film grain) sutilíssima (~3,5% opacidade, `mix-blend-mode:overlay`) aplicada em toda a página via SVG turbulence, pra tirar o aspecto "flat" das cores.
  - As 4 seções claras que ainda eram uma cor só (Aprendizados, Visão 360, Palestrantes, Público-alvo) ganharam gradientes radiais bem sutis (9-13% de opacidade) misturando teal e laranja nos cantos, em vez de creme/branco 100% liso.
  - As 4 seções escuras (Urgência, CTA final, Footer, Programação) ganharam manchas de luz radiais mais fortes (14-35% de opacidade) em teal e laranja nos cantos, quebrando o preto liso com "glow" colorido.
  - Opacidade dos blobs decorativos de laranja aumentada (de 0,1 para ~0,2) pra reforçar a presença da cor.
- Índices numerados da Visão 360 (`01`-`06`) ganharam cor alternada laranja/teal (antes eram só tinta), mais um toque de cor nessa dobra.
- Fundo da Programação reformulado: seção agora escura (`#0a0a0a`), com a foto `assets/plateia-evento-buzzmonitor.jpg` (enviada pelo usuário) como camada de fundo em efeito parallax (`background-attachment:fixed`, desliga em mobile/`prefers-reduced-motion` por suporte/acessibilidade), a ~55% de opacidade sob um scrim escuro para manter o texto legível, mais um blob teal decorativo.
- Header (`.site-header`) com efeito de vidro fosco mais forte: `backdrop-filter: blur(16px) saturate(180%)`, fundo mais translúcido, sombra sutil permanente (antes só aparecia depois de rolar).
- Blobs orgânicos animados adicionados em mais dobras (Aprendizados, Visão 360, Palestrantes, Público-alvo, Programação) para dar mais movimento de fundo em geral, além dos já existentes no Hero, CTA final e Footer — todos com opacidade baixa (0.1-0.16) para não competir com o conteúdo, e todos herdam o `prefers-reduced-motion` global já existente.
- Todas as cores novas/realocadas foram recontrastadas (WCAG) antes de aplicar — ver `Validação local` abaixo.

**Ajuste 2026-08-27 (rodada 4, feedback: caixas de texto estreitas + selo do hero):**
- Larguras de texto aumentadas (estavam limitadas a ~56-60ch, sobrando margem lateral): bloco da Urgência (`.urgencia__inner` 740px→900px, `.urgencia__body` →820px) e fechamento da seção Aprendizados (`.learn-close` →820px, `.learn-outro` →860px).
- Selo flutuante do hero trocado: em vez do círculo tracejado com "01/OUT", agora tem um **sino animado** (ícone SVG com animação de "toque" a cada ~3,4s, período de descanso entre um toque e outro — usa `bell-ring`, keyframe novo) mais um ponto de notificação pulsante (`pulse-dot`), ambos com fallback `prefers-reduced-motion`. Data do evento continua visível normalmente na linha "Data" do card ao lado, então nada de informação foi perdido.

**Ajuste 2026-08-31 (rodada 5, palestrantes confirmados + selo Buzzconnect):**
- Seção Palestrantes reconstruída no formato usado em `buzztalk-gestao-multimarcas-para-agencias` (mesmo repo): card branco, foto circular com anel gradiente (`linear-gradient(135deg, teal, laranja)`) atrás, e no hover 2 anéis de "onda sonora" se expandindo (teal + laranja, `@keyframes soundwave`, com fallback `prefers-reduced-motion`). Estrutura: rótulo (Palestrante/Speaker convidada) → nome → cargo → logo da empresa.
- Fotos e logo fornecidos pelo usuário: `assets/Thiagorodrigues.png`, `assets/Beatrizmoreira.png`, `assets/elifelogo.png` (logo Buzzmonitor já existia em `brand/`).
- Menção à "Buzzconnect" adicionada — a série nunca era citada nominalmente na página. Duas tentativas antes da versão final, ambas a pedido do usuário:
  1. Primeiro como selo separado no header (pill laranja rotacionada ao lado do logo). **Bug encontrado e corrigido durante o teste:** em telas muito estreitas (<400px) esse selo colidia visualmente com o botão "Quero participar" (sem gerar scroll horizontal, mas sobrepondo os dois elementos). Corrigido com `flex-wrap` no header, mas o usuário pediu pra mudar de lugar antes de publicar.
  2. Versão final: o selo saiu do header e o texto virou parte do chip já existente no topo do Hero — `"Buzzconnect - Evento exclusivo para clientes Buzzmonitor"` (hífen normal, não em-dash) no lugar do texto antigo do chip. Header voltou ao normal (só logo + CTA), sem risco de colisão.
- `copy.txt` atualizado com os dados confirmados dos palestrantes (substitui a marcação `[PENDENTE]` anterior).

## Estrutura

- HERO — chip de evento, H1 (com destaque em gradiente na cauda do texto), contexto (3 parágrafos), card-ticket "sticker" (data/horário/local + selo de data + contador regressivo, JS, alvo 01/10/2026 14h BRT, fallback noscript)
- APRENDIZADOS — grid de 6 cards estilo sticker (check teal/tinta) + 2 linhas de fechamento + CTA
- VISÃO 360 — 6 blocos em grid (Campanha, Monitoramento, Atendimento, Crises, IA e Automação, Pós-venda)
- URGÊNCIA — seção escura (roxo) com anéis decorativos girando, CTA
- PALESTRANTES — 2 cards com foto real (anel gradiente teal→laranja, efeito de "onda sonora" no hover, mesmo formato da LP `buzztalk-gestao-multimarcas-para-agencias`): Thiago Rodrigues (Head de Customer Success, Buzzmonitor) e Beatriz Moreira (Gerente de Operações Digitais, Elife)
- PROGRAMAÇÃO — timeline de 6 etapas com badges roxo/rosa alternados (14h00 às 17h30)
- PARA QUEM É — lista numerada de 10 públicos-alvo (seção de respiro/pausa, sem CTA)
- CTA FINAL — headline (destaque em gradiente) + form de inscrição mock estilo sticker (nome, e-mail corporativo, empresa, cargo, WhatsApp)
- CONTATO — e-mail
- FOOTER — logo, tagline, copyright, redes sociais (Instagram/LinkedIn da marca)
- CTA fixo mobile (aparece após rolar a hero)

**Ajuste 2026-09-04 (cronograma atualizado pelo usuário):** Programação trocada para 14h00 Recepção dos convidados e welcome coffee → 14h30 Início do evento com o time Buzzmonitor → 15h30 Networking + café com a Buzz → 16h00 Cases de clientes Buzzmonitor → 16h30 Sorteio de brindes e últimos detalhes → 17h00 Encerramento. `copy.txt` atualizado junto. Horário geral do evento também ajustado de 14h-18h para **14h-17h** em todos os pontos consistentes: LABEL do hero-card (`copy.txt` + `index.html`), JSON-LD `Event.endDate` (18:00 → 17:00). O `startDate`/alvo do contador regressivo (14h) não mudou.

## Estado

- [x] HTML gerado e validado (SEO, GTM, JSON-LD, zero em-dash)
- [x] Redesenho de identidade visual (Buzzconnect) aplicado 2026-08-27 — paleta/contraste revalidados do zero (ver nota de acessibilidade acima); os 6 críticos do `REVISAO.md` original (rodado sobre o design anterior, mais corporativo) já vêm incorporados nativamente neste redesenho — não reabrir, ver seção "Redesenho" do `REVISAO.md`
- [ ] OG image 1200×630 → `assets/og-black-friday-alta-performance-outubro-2026.png` (arquivo único — nunca também `og-image.png`)
- [ ] Rodar `/lp-revisar` novamente sobre o HTML redesenhado, para auditoria formal independente (a validação atual foi feita inline durante a criação, não por uma passada dedicada)
- [x] Formulário integrado — **Form provider:** Jotform (`250493444653662`), integrado em 2026-08-28. Form mock removido, embed com wrapper CSS canônico (`.jotform-embed iframe`), sem card duplicado.
- [x] Palestrantes confirmados em 2026-08-31 (fotos + logos enviadas pelo usuário) — Thiago Rodrigues (Buzzmonitor) e Beatriz Moreira (Elife). Card redesenhado no formato da LP `buzztalk-gestao-multimarcas-para-agencias` (blob gradiente + anéis de "onda sonora" no hover).
- [x] Menção "Buzzconnect" incorporada ao chip do Hero (`"Buzzconnect - Evento exclusivo para clientes Buzzmonitor"`), a pedido do usuário — a série nunca era mencionada nominalmente na página. Header permanece só com logo + CTA.
- [x] Publicado — `/lp-publicar buzzmonitor black-friday-alta-performance-outubro-2026 content.buzzmonitor.com` (2026-08-28, PR #405) + form Jotform (PR #419). **Pendente republicar** com os palestrantes/selo desta rodada.

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `./assets/plateia-evento-buzzmonitor.jpg` (fundo parallax da seção Programação, foto de plateia de evento anterior fornecida pelo usuário)
- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (logo da empresa no card do palestrante Thiago Rodrigues)
- `./assets/Thiagorodrigues.png` (foto do palestrante Thiago Rodrigues, fornecida pelo usuário)
- `./assets/Beatrizmoreira.png` (foto da palestrante Beatriz Moreira, fornecida pelo usuário)
- `./assets/elifelogo.png` (logo Elife no card da palestrante Beatriz Moreira, fornecido pelo usuário)

## Validação local (2026-08-27, pós-redesenho Buzzconnect)

- `grep -c "—" index.html` → 0
- SEO: 1 description, 10 og:*, 4 twitter:*, 1 JSON-LD (parseia OK)
- GTM `GTM-WFJVK858` presente 2x (script + noscript); `check_gtm_region.py` → `status: ok`, selo `.tracking.lock` gravado
- Servido localmente via `py -m http.server` com junção `landing-pages/brand` — logos e foto da Programação carregam 200 OK, sem overflow horizontal em 375px/desktop, sem erros de console (rodada 1 e rodada 2)
- Contraste checado (fórmula WCAG) rodada 1: botão laranja (tinta `#121212` sobre `#EB7C2E`) 6,65:1; `--c-orange-text` sobre creme/branco 5,22-5,77:1; destaque em gradiente com texto branco 4,69-5,77:1 — todos ≥ 4,5:1
- Contraste checado (rodada 2, paleta teal/preto/laranja): branco sobre preto `#0a0a0a` 19,8:1; laranja vibrante sobre preto 7,03:1; badges do cronograma (tinta sobre teal 5,63:1, tinta sobre laranja 6,65:1); `--c-teal-text` sobre creme/branco 5,06-5,45:1; gradiente teal→laranja-texto com texto branco 5,45-5,77:1 — todos ≥ 4,5:1. Confirmado que `--c-teal`/`--c-orange` "crus" NÃO são usados como texto em fundo claro (só como fundo/ícone/decoração), já que ambos falham AA nesse uso (~3,3:1 e ~2,8:1)
