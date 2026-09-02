# LP Cxpress — banimento-de-whatsapp

**Gerado em:** 2026-08-30
**Copy-fonte:** `copy.txt` (doc "Nova Banimento Whats (Google Ads)", Victor)
**Domínio de destino:** `content.cxpress.io/banimento-de-whatsapp` (guarda-chuva, deploy via CI)
**Idioma / região:** PT-BR / brasil
**Form provider:** ⚠️ **mock** — o embed do Jotform `261034073026647` foi retirado em 2026-09-01 para simular em HTML o layout de formulário de referência (Octadesk). Reintegrar via `/lp-integrar-form cxpress/banimento-de-whatsapp` **antes de publicar**.
**Tracking:** GTM-KN8BPFG + GA4 339689858 (container de Google Ads, confirmado pelo Victor em 2026-08-30)

## De onde veio

| Referência | O que foi aproveitado |
|---|---|
| Doc "Nova Banimento Whats (Google Ads)" | **Toda a copy** e a ordem das 10 seções. Nenhuma frase nova foi escrita. |
| LP irmã `cxpress/evite-banimento-whatsapp` | Identidade visual: tokens de cor, tipografia (Open Sans / Source Sans 3 / Bitter), navbar, botões, faixa de clientes, FAQ, fecho dark, seção de formulário, assets do hero. |
| LP da Umbler ("Clone seu melhor atendente com IA") | **Esqueleto e distribuição de informação**: hero com 2 devices sobrepostos e tags de estado, faixa de logos logo abaixo do hero, dor em lista vertical ao lado do texto, passos numerados com trilho, comparativo em duas colunas lado a lado, diagrama de canais, FAQ em acordeão, fecho + CTA. |

A página **não** é uma cópia da `/evite-banimento-whatsapp`: as seções PROVA (métricas) e QUEM SOMOS não existem aqui, e as seções SINTOMAS, IMPACTO, COMO EVITAR, COMPARATIVO e OMNICHANNEL são novas.

## Estrutura (10 seções do doc + form)

| # | Seção | Layout | Fundo |
|---|---|---|---|
| 1 | HERO | Texto à esquerda; à direita o celular banido sobreposto ao painel da Cxpress, com tags "Operação convencional" e "Com a Cxpress" | branco |
| — | CLIENTES | Esteira infinita com 42 logos | branco |
| 2 | SINTOMAS | Texto + nota destacada à esquerda, 5 sinais em lista vertical com X vermelho à direita (GUIDELINES §8) | tint |
| 3 | IMPACTO | 4 cards 2×2, ícone vermelho | branco |
| 4 | COMO EVITAR | 4 passos numerados 01→04 com trilho contínuo e ✓ verde | tint |
| 5 | COMPARATIVO | 2 colunas lado a lado (6 linhas cada), a da Cxpress com cabeçalho navy + CTA abaixo | branco |
| 6 | API OFICIAL | Texto à esquerda, 7 recursos em pílulas com ✓ à direita | tint |
| 7 | OMNICHANNEL | Diagrama 5 canais → Cxpress → Equipe, com trilho tracejado animado | branco |
| 8 | IA | Texto + CTA à esquerda, GIF do chatbot à direita | tint |
| 9 | FAQ | 5 perguntas em `<details>` (JSON-LD FAQPage com as mesmas 5) | branco |
| 10 | FECHO | Única seção dark, H2 em Bitter itálico | navy |
| — | FORM | Card centralizado, **última seção** (o doc pede o form "lá pra baixo") | tint |

**CTAs:** 5 âncoras para `#agendar` (navbar, hero, comparativo, IA, fecho) + o botão do próprio formulário. Nenhum CTA aponta para fora.

## Estado

- [x] HTML gerado
- [x] OG image 1200×630 → `assets/og-banimento-de-whatsapp.png` (template em `assets/og-template.html`)
- [x] Revisão de design + a11y aplicada — ver `REVISAO.md`
- [ ] Formulário integrado — hoje é **mock** (GUIDELINES §11). Reintegrar o Jotform `261034073026647` via `/lp-integrar-form` antes de publicar
- [ ] Entrar no `landing-pages/dominios/content-cxpress-io/manifest.json` e publicar — rodar `/lp-publicar cxpress banimento-de-whatsapp content.cxpress.io`

## Ajustes de 2026-09-03 (Bruno)

**Seção omni ficou escura.** Fundo `--primary-dark` com efeito montado a partir do vocabulário
que a LP já tinha: mesh de pontos com máscara radial (mesmo do `.agendar`) mais dois glows
(azul `--primary` no topo-esquerda, laranja `--accent` embaixo-direita) e duas pílulas decorativas
nas bordas (mesmo do `.fecho`). A máscara abre um buraco no centro pra o mesh não competir com o diagrama.

Itens invertidos pra ganhar destaque no navy:

| Item | Antes | Agora |
|---|---|---|
| Título | `--primary-dark` | `--white` |
| Subtítulo e legenda | `--text-body` / `--text-muted` | `--primary-lighter` |
| Anéis | `#E6E8F5` | `rgba(255,255,255,.16)` |
| Linhas radiais | azul translucido | branco translucido |
| Pílulas de canal | branco com sombra navy | branco com aro claro e sombra preta |
| Agentes | aro `--border-strong` | aro `rgba(255,255,255,.7)` |
| Tela do notebook | navy chapado | gradiente aceso + halo azul |

A tela do notebook era navy chapado e sumiria no fundo navy. Virou **tela acesa** (gradiente
`#3a4a9e -> #1c2258` + borda clara + halo) em vez de mais uma superfície branca: assim o centro
segue sendo o elemento mais forte sem se confundir com as pílulas. Pelo mesmo motivo o halo do
keyframe `receber` passou de navy (invisível no navy) para verde `--wa`.

Contraste medido no fundo navy: título 13.5:1, subtítulo e legenda 10.4:1, texto das pílulas
13.5:1 no branco, barra laranja 5.2:1 (mínimo de 3:1 para elemento gráfico).

## Ajustes de 2026-09-02 (Bruno)

1. **Seção omni virou diagrama radial** (opção "Convergência", escolhida entre 3 protótipos animados).
   Saiu o fluxo linear `canais -> Cxpress -> equipe`; entrou o notebook com a marca no centro de 4 anéis
   concêntricos, os 5 canais nos anéis e 4 agentes em volta da plataforma. Cada canal dispara um ponto
   verde que percorre a linha radial até o notebook; ao chegar, a tela reage e um agente acende.
   Removidos `.fluxo`, `.canais`, `.canal`, `.trilho`, `.no-cx`, `.no-equipe` e `@keyframes fluir`/`fluirV`.
2. **Palco de tamanho fixo escalado por JS** (`--sw`/`--sh` no CSS, `transform: scale()` no script).
   Composição radial feita com `%` quebra em telas estreitas; com escala, não. Abaixo de 760px o palco
   troca pra uma composição compacta e as pílulas ficam **só com ícone** — rótulo de 16px reduzido a 0.4
   fica ilegível, e o H2 da seção já nomeia os canais.
3. **Ângulos dos agentes** ficam no meio dos 4 maiores vãos entre canais (-95°, 21°, 88°, 177°). Em ±40/±140
   o agente ficava a 6° do Facebook e colidia quando os raios comprimem no mobile.
4. **Ícone do WhatsApp → WhatsApp Business** (bolha com "B" no lugar do fone), desenhado inline. 19px em vez
   de 17px: a bolha não preenche a caixa como o retângulo do Instagram, e 2px equilibram a massa óptica.
5. **Subtítulo da seção**: as duas frases viraram um parágrafo só a 760px — cai de 4 pra 3 linhas.
   Medido: cada frase sozinha precisa de 922px pra caber em 1 linha, e a maior linha do H2 tem 717px;
   deixar o subtítulo mais largo que o título inverteria a hierarquia.

Todo o movimento vive em `prefers-reduced-motion: no-preference`. Sem ele, anéis, linhas, pílulas,
agentes, notebook e legenda seguem visíveis — só os pontos (decorativos) somem.

## Ajustes de 2026-09-01 (Bruno)

1. **Menu transparente:** navbar adotou o vidro do padrão `content.buzzmonitor.com/monitoramento-com-ia` — `rgba(255,255,255,.80)` + `backdrop-filter:blur(5px)` + borda `#e2e8f0`.
2. **CTAs azul-escuro em pílula:** todos os botões (`.btn`, `.navbar__cta`, `.btn--light`) passaram de verde WhatsApp para `--primary-dark` (#232960) com texto branco e `border-radius: var(--radius-pill)`. O verde `--wa` continua só como acento gráfico (checks, tags do hero, trilho do fluxo).
3. **Formulário simulado:** o embed do Jotform virou mock HTML reproduzindo o formulário de referência (Octadesk): nome, e-mail corporativo, site, faixa de funcionários, cargo, departamento, WhatsApp com DDI +55 fixo, nota de privacidade, opt-in marcado e botão Enviar. Bandeira do Brasil é SVG inline (o emoji 🇧🇷 renderiza como "BR" no Chrome/Windows).

## Decisões do Victor (2026-08-30)

1. **Formulário:** mesmo Jotform da LP irmã (`261034073026647`). Os leads das duas páginas caem no mesmo formulário; separar no funil depende de UTM/`url_conversao`.
2. **Tracking:** mantido o container de Google Ads (GTM-KN8BPFG + GA4 339689858), não o default de Brasil do `tracking.json`.
3. **FAQ:** mantido como o doc entrega, com 5 perguntas. A pergunta "A Cxpress consegue desbloquear minha conta?" (que existe na `/evite-banimento-whatsapp`) fica de fora por decisão do Victor.

## Assets referenciados

Locais (`./assets/`):
- `hero-conta-banida-whatsapp.png` — celular com a tela de banimento
- `hero-circulos-concentricos.svg` — círculos de fundo do hero
- `clientes/cliente-01..42.png` — esteira de logos
- `og-banimento-de-whatsapp.png` + `og-template.html`

Do brand (`../../brand/cxpress/assets/`):
- `logos/logo-primary.svg` (navbar) · `logos/logo-reversed.svg` (footer e nó do diagrama) · `logos/logo-icon.png` (favicon)
- `plataforma/plataforma-canais.gif` (painel do hero) · `plataforma/plataforma-chatbot-ia.gif` (seção IA)
