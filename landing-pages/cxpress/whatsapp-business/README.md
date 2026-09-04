# LP Cxpress — whatsapp-business

**Gerado em:** 2026-08-28 · **Refeito em:** 2026-09-04 (troca integral de copy)
**Copy-fonte:** `copy.txt` — transcrição da página viva [`home.cxpress.io/app-whatsapp`](https://home.cxpress.io/app-whatsapp) (print enviado pelo Bruno + espelho local `D:\Elife\174 - LP ClaudeCode\mirrors\mirrors\pages\app-whatsapp.html`, capturado em 2026-07-23)
**Região:** brasil (pt-BR) · **Domínio alvo:** `content.cxpress.io` (guarda-chuva migrado pro CI)
**Form provider:** Jotform `261027639617663` ("LPs - Proposta"), nos dois pontos de captura: a seção "Entre em contato conosco!" e o modal do botão flutuante
**Tracking:** GTM-T4XDWHL3 (padrão Cxpress BR, `brand/cxpress/tracking.json`). GA4 dispara dentro do container

## O que mudou em 2026-09-04

Pedido do Bruno: adotar as **seções padrão da LP irmã `banimento-de-whatsapp`** (menu, rodapé, botão pulsante do WhatsApp e slider de clientes), **trocar toda a copy pela da `home.cxpress.io/app-whatsapp`** e, no hero, **ignorar o GIF** e animar o SVG `Chatbot_WhatsApp` no padrão da LP `telefonia-ia-latam`.

| Item | Antes (2026-08-28) | Agora |
|---|---|---|
| H1 | "Centralize seus canais de atendimento e automatize o primeiro contato com IA…" (variante B, ganho operacional) | "Plataforma de Automação de WhatsApp para atendimento inteligente e Organizado" (categoria, literal da origem) |
| Hero visual | `tela-tickets.svg` estática | `tela-chatbot-whatsapp.svg` com cena animada (holofote sequencial + indicador de digitação) |
| Navbar | própria | padrão `banimento-de-whatsapp` (rótulo longo/curto por breakpoint) |
| Rodapé | próprio (logo + linha legal + 2 links jurídicos) | padrão `banimento-de-whatsapp` (logo + linha legal + 4 redes sociais) |
| Botão flutuante | link `wa-float` estático | FAB **pulsante** padrão + modal com o Jotform da LP |
| Slider de clientes | esteira de 42 logos + 2 métricas próprias | esteira de 42 logos (métricas saíram, ver `REVISAO.md`) |
| Seções | Hero · Clientes+métricas · **Dores** · Plataforma · **Integrações** · Quem somos · Form · FAQ | Hero · Clientes · **Porquê (3 cards)** · **Vídeo** · **Prova (4 números)** · **Consultor** · Plataforma · Quem somos · Form · FAQ |
| FAQ | 4 perguntas | 5 perguntas (entrou "A inteligência artificial (IA) faz o atendimento sozinha?") |

## Estrutura (10 seções, ordem da página de origem)

| # | Seção | Layout | Fundo |
|---|---|---|---|
| 1 | HERO | Texto à esquerda (H1 com "WhatsApp" em verde escuro), tela do chatbot animada à direita, selos de canal flutuantes | gradiente claro |
| 2 | CLIENTES | Rótulo + esteira infinita com 42 logos (padrão `banimento-de-whatsapp`) | branco |
| 3 | PORQUÊ | H2 + subtítulo + grid de 3 cards com ✓ verde (GUIDELINES §8) | tint |
| 4 | VÍDEO | H2 + fachada de vídeo (YouTube `36sbDc02_DU` sob demanda) + CTA | branco |
| 5 | PROVA | 4 números (14% · 9% · 25% · 45%) + notas NBER e McKinsey | tint |
| 6 | CONSULTOR | Card com H2 + CTA laranja "Fale agora!" + glifo do WhatsApp | branco |
| 7 | PLATAFORMA | 5 features alternando lado, cada uma com a tela real. A 01 tem selos de canal pulsando, a 03 tem holofote sequencial | branco |
| 8 | QUEM SOMOS | Faixa escura (única da LP), 2 parágrafos + 3 badges | navy |
| 9 | FORM | H2 + apoio + e-mail comercial + embed do Jotform | royal |
| 10 | FAQ | Acordeão `<details>` com 5 perguntas | tint |

Ritmo tonal: gradiente → branco → tint → branco → tint → branco → branco → navy → royal → tint → rodapé navy.
A única adjacência de mesma cor (CONSULTOR e PLATAFORMA, ambas brancas) é separada por filete de seção mais 128 px de respiro, e o card cheio do CONSULTOR dá identidade própria à faixa. Registrado em `REVISAO.md`.

## Cena animada do hero

Mesma gramática da LP `telefonia-ia-latam`: a interface real é a base e a animação **revela regiões dela em sequência**, em loop de 14 s, só com `transform`/`opacity`.

- **Holofote sequencial** (`.hero__spot`): três paradas medidas no próprio SVG — linha de abas de canal → par de selos de API oficial → conversa. Escurecimento de 20 % em volta (em 30 % a tela do produto ficava suja no primeiro quadro, que é o que o visitante vê antes do ciclo começar).
- **Indicador de digitação** (`.hero__typing`): entra junto com a parada da conversa e sai com ela. Sem rótulo, só os três pontos, para **não inventar texto** que não está na copy.
- **Selos de canal flutuantes** (`.hero__chip`): WhatsApp, Instagram e e-mail, decorativos, sem texto.
- Pausa fora de vista via `.fx-idle` (IntersectionObserver). Sob `prefers-reduced-motion` e abaixo de 720 px a cena não existe: fica só a tela, limpa.

Os conectores tracejados que existiam na versão anterior **saíram**: com holofote, digitação, selos, malha de pontos, halo verde e anel inclinado, o hero passava do "um elemento forte" da GUIDELINES §3.

## Estado

- [x] HTML gerado (`index.html`, 1524 linhas, 90 KB)
- [x] Copy trocada pela da página de origem e conferida string por string (auditoria de fidelidade no `REVISAO.md`)
- [x] Seções padrão portadas da `banimento-de-whatsapp` (navbar, rodapé, FAB pulsante + modal, slider de clientes)
- [x] Cena animada do hero
- [x] Formulário integrado — Jotform `261027639617663` na seção e no modal, com o listener que impede os dois embeds do mesmo form de se redimensionarem entre si
- [x] Validações determinísticas (SEO, anti-IA, diagramação, contraste, pisos mobile, overflow) — ver `REVISAO.md`
- [ ] **OG image desatualizada** — `assets/og-whatsapp-business.png` ainda traz o H1 antigo. Regerar com `assets/og-template.html` + `assets/render_og.py` antes de publicar
- [ ] Publicado — rodar `/lp-publicar cxpress whatsapp-business content.cxpress.io`

## Assets referenciados

| Path | Onde aparece |
|---|---|
| `../../brand/cxpress/assets/logos/logo-primary.svg` | navbar |
| `../../brand/cxpress/assets/logos/logo-reversed.svg` | rodapé |
| `../../brand/cxpress/assets/logos/logo-icon.png` | favicon |
| `./assets/telas/tela-chatbot-whatsapp.svg` | hero (animado) e feature 02 |
| `./assets/telas/tela-canais.svg` | feature 01 |
| `./assets/telas/tela-principal.svg` | feature 03 |
| `./assets/telas/tela-distribuicao.svg` | feature 04 |
| `./assets/telas/tela-dashboard.svg` | feature 05 |
| `./assets/clientes/cliente-01..42.png` | esteira de clientes |
| `./assets/elife-logo-badge.png` | badge "Um produto" em Quem somos |
| `./assets/og-whatsapp-business.png` | OG image (a regerar) |

`assets/telas/tela-agentes.svg`, `tela-disparo-ativo.svg` e `tela-tickets.svg` ficaram sem uso nesta versão. Mantidos na pasta: são telas do produto já otimizadas, úteis se uma feature voltar.
