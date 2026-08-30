# LP Cxpress — banimento-de-whatsapp

**Gerado em:** 2026-08-30
**Copy-fonte:** `copy.txt` (doc "Nova Banimento Whats (Google Ads)", Victor)
**Domínio de destino:** `content.cxpress.io/banimento-de-whatsapp` (guarda-chuva, deploy via CI)
**Idioma / região:** PT-BR / brasil
**Form provider:** Jotform `261034073026647` (o mesmo da LP irmã `/evite-banimento-whatsapp`, integrado em 2026-08-30)
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
- [x] Formulário integrado — Jotform `261034073026647`
- [ ] Entrar no `landing-pages/dominios/content-cxpress-io/manifest.json` e publicar — rodar `/lp-publicar cxpress banimento-de-whatsapp content.cxpress.io`

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
