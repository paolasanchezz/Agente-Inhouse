# LP Cxpress — whatsapp-business

**Gerado em:** 2026-08-28 · **Refeito em:** 2026-09-04 (troca integral de copy + 2ª rodada de ajustes do Bruno)
**Copy-fonte:** `copy.txt` — transcrição da página viva [`home.cxpress.io/app-whatsapp`](https://home.cxpress.io/app-whatsapp) (print enviado pelo Bruno + espelho local `D:\Elife\174 - LP ClaudeCode\mirrors\mirrors\pages\app-whatsapp.html`, capturado em 2026-07-23)
**Região:** brasil (pt-BR) · **Domínio alvo:** `content.cxpress.io` (guarda-chuva migrado pro CI)
**Form provider:** Jotform `261034073026647` (o mesmo da LP irmã `banimento-de-whatsapp`), nos dois pontos de captura: a seção "Entre em contato conosco!" e o modal do botão flutuante. Trocado em 2026-09-04, na 2ª rodada, a pedido do Bruno — antes era o `261027639617663` ("LPs - Proposta")
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
| Seções | Hero · Clientes+métricas · **Dores** · Plataforma · **Integrações** · Quem somos · Form · FAQ | Hero · Clientes · **Porquê (3 cards)** · **Vídeo** · **Prova (4 números)** · Plataforma · Quem somos · Form · FAQ |
| FAQ | 4 perguntas | 5 perguntas (entrou "A inteligência artificial (IA) faz o atendimento sozinha?") |

## 2ª rodada (2026-09-04, depois do primeiro deploy)

Correções pedidas pelo Bruno olhando a página no ar. Nenhuma palavra de copy foi reescrita: as mudanças são de estrutura, peso tipográfico, movimento e formulário.

| # | Pedido | O que foi feito |
|---|---|---|
| 1 | Tirar a faixa do consultor | Seção removida (markup + CSS). Saiu junto o `.btn--accent`, que só ela usava |
| 2 | H1 maior e com mais destaque | Teto de 40 → **48 px**, `letter-spacing` -.015 → -.025em, `line-height` 1.08. Para caber em 3 linhas nesse corpo, a coluna de texto do hero foi de 1.32fr → 1.9fr e o gap 48 → 40 px |
| 3 | Título do vídeo em no máximo 2 linhas | Medida de 24ch → **38ch**. Dá 2 linhas a 1440 (36 px) e a 1280 (33 px) |
| 4 | Big numbers com destaque e contador | Número de `clamp(38-50px)` → **`clamp(52-76px)`**, cor para navy (o `%` segue laranja escuro) e contagem animada ao entrar na tela |
| 5 | Faltavam animações nos cards do "Porquê" | Corrigido um bug de stagger (ver abaixo) + entrada com `translateY(30px) scale(.985)`, marcador verde entrando depois com escala, e hover em sombra/borda |
| 6 | Espaço vazio grande no topo da seção | `padding-top` da seção de 128 → **72 px** |
| 7 | Trocar o formulário | Jotform `261034073026647` nos dois pontos de captura |
| 8 | Centralizar a seção do formulário como na `banimento-de-whatsapp` | Grid de 2 colunas trocado por coluna única centrada: pílula verde 76×9 em `--wa`, H2 e apoio em 820px, Jotform num card branco de 600px com radius 24px. Valores idênticos aos da LP irmã |

**O bug do stagger.** Os cards já tinham `.reveal`, mas o atraso vinha do JS como `idx % 5 * 60ms` calculado sobre a ordem **global** dos `.reveal` da página. Dentro de um grid de 3, a ordem saía embaralhada (240 ms, 0 ms, 60 ms) e a entrada parecia quebrada; o delay inline também vencia qualquer regra de CSS. Agora o JS não escreve delay nenhum e o stagger vem do CSS por seção (0 / .10s / .20s) — o que arruma a entrada em toda a página, não só nesses cards.

O hover dos cards mexe só em sombra e borda, de propósito: `transform` fica reservado à entrada. Se o hover também usasse `transform`, herdaria o `transition-delay` do stagger e sairia lento.

## Estrutura (9 seções, ordem da página de origem)

| # | Seção | Layout | Fundo |
|---|---|---|---|
| 1 | HERO | Texto à esquerda (H1 com "WhatsApp" em verde escuro), tela do chatbot animada à direita, selos de canal flutuantes | gradiente claro |
| 2 | CLIENTES | Rótulo + esteira infinita com 42 logos (padrão `banimento-de-whatsapp`) | branco |
| 3 | PORQUÊ | H2 + subtítulo + grid de 3 cards com ✓ verde (GUIDELINES §8) | tint |
| 4 | VÍDEO | H2 + fachada de vídeo (YouTube `36sbDc02_DU` sob demanda) + CTA | branco |
| 5 | PROVA | 4 números grandes (14% · 9% · 25% · 45%) com contagem animada + notas NBER e McKinsey | tint |
| 6 | PLATAFORMA | 5 features alternando lado, cada uma com a tela real. A 01 tem selos de canal pulsando, a 03 tem holofote sequencial | branco |
| 7 | QUEM SOMOS | Faixa escura (única da LP), 2 parágrafos + 3 badges | navy |
| 8 | FORM | Composição centralizada no desenho da `banimento-de-whatsapp`: pílula verde, H2 e apoio centrados em 820px, e-mail, e o Jotform num card branco de 600px no meio | royal |
| 9 | FAQ | Acordeão `<details>` com 5 perguntas | tint |

Ritmo tonal: gradiente → branco → tint → branco → tint → branco → navy → royal → tint → rodapé navy. Alternância perfeita, sem duas seções da mesma cor encostadas.

A faixa "Fale com um de nossos consultores no WhatsApp agora mesmo!" existia entre a PROVA e a PLATAFORMA e **saiu em 2026-09-04** a pedido do Bruno. A LP passa a divergir da página de origem nesse ponto por decisão, não por omissão. A rota de conversa por WhatsApp na página fica sendo o botão flutuante pulsante.

## Cena animada do hero

Mesma gramática da LP `telefonia-ia-latam`: a interface real é a base e a animação **revela regiões dela em sequência**, em loop de 14 s, só com `transform`/`opacity`.

- **Holofote sequencial** (`.hero__spot`): três paradas medidas no próprio SVG — linha de abas de canal → par de selos de API oficial → conversa. Escurecimento de 20 % em volta (em 30 % a tela do produto ficava suja no primeiro quadro, que é o que o visitante vê antes do ciclo começar).
- **Indicador de digitação** (`.hero__typing`): entra junto com a parada da conversa e sai com ela. Sem rótulo, só os três pontos, para **não inventar texto** que não está na copy.
- **Selos de canal flutuantes** (`.hero__chip`): WhatsApp, Instagram e e-mail, decorativos, sem texto.
- Pausa fora de vista via `.fx-idle` (IntersectionObserver). Sob `prefers-reduced-motion` e abaixo de 720 px a cena não existe: fica só a tela, limpa.

Os conectores tracejados que existiam na versão anterior **saíram**: com holofote, digitação, selos, malha de pontos, halo verde e anel inclinado, o hero passava do "um elemento forte" da GUIDELINES §3.

## Estado

- [x] HTML gerado (`index.html`, 1570 linhas, 91 KB)
- [x] Copy trocada pela da página de origem e conferida string por string (auditoria de fidelidade no `REVISAO.md`)
- [x] Seções padrão portadas da `banimento-de-whatsapp` (navbar, rodapé, FAB pulsante + modal, slider de clientes)
- [x] Cena animada do hero
- [x] Formulário integrado — Jotform `261034073026647` na seção e no modal, com o listener que impede os dois embeds do mesmo form de se redimensionarem entre si
- [x] Validações determinísticas (SEO, anti-IA, diagramação, contraste, pisos mobile, overflow) — ver `REVISAO.md`
- [x] OG image conferida — `assets/og-whatsapp-business.png` diz "Atendimento no WhatsApp inteligente e organizado" + "Centralize e automatize o seu atendimento, simples e eficaz.", ambas alinhadas com a copy da origem. Não precisou regerar
- [x] Publicado em `content.cxpress.io/whatsapp-business` (fluxo CI, PRs #504, #506 e o desta rodada)

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
| `./assets/og-whatsapp-business.png` | OG image |

`assets/telas/tela-agentes.svg`, `tela-disparo-ativo.svg` e `tela-tickets.svg` ficaram sem uso nesta versão. Mantidos na pasta: são telas do produto já otimizadas, úteis se uma feature voltar.
