# LP Cxpress — whatsapp-business-smb

**Gerado em:** 2026-07-24
**Copy-fonte:** transcrição literal e integral de [`home.cxpress.io/whatsapp-business-smb`](https://home.cxpress.io/whatsapp-business-smb) (site GreatPages, fora do pipeline), a pedido explícito do usuário ("mantenha o conteúdo integral e original da LP"). Ver `copy.txt` para a estrutura completa e as notas de extração.

## Origem

Duplicata da LP `whatsapp-business-smb`, hoje hospedada em `home.cxpress.io` (site institucional em GreatPages, fora do pipeline de LPs). O usuário pediu pra trazê-la pro nosso pipeline (`content.cxpress.io`) com o design aprimorado — mesmo sistema visual/CSS desenvolvido em `landing-pages/cxpress/banimento-whatsapp-clinicas/` (correção de espaçamento, tipografia e componentes consistentes), mas **mantendo o conteúdo (texto) 100% original**.

Diferença de escopo em relação à sessão de `banimento-whatsapp-clinicas`: lá a melhoria foi um tratamento de **hero como fundo de seção com gradiente** (adequado a uma foto rica enviada pelo usuário). Aqui, o "aprimorar design" foi aplicado de forma criteriosa ao conteúdo real desta LP — o visual do hero na fonte é uma animação pequena do dashboard (não uma foto), então o tratamento de fundo-com-gradiente não se aplicava bem. Optei por manter o padrão "texto à esquerda + mockup em card à direita" (já testado em 8+ LPs Cxpress), aplicando as correções de qualidade aprendidas (ver abaixo).

## O que foi extraído da fonte

Página construída em GreatPages (não WordPress) — imagens carregam via lazy-load acionado por scroll, então a extração exigiu inspeção de DOM + scroll simulado (não deu pra usar só um fetch simples). Conteúdo mapeado em 9 blocos:

1. **Hero** — badge "Condições especiais", H1 "Atendimento eficiente começa com organização", 2 parágrafos de corpo, CTA "Fale com um especialista". Visual: GIF do dashboard da Cxpress (menu de navegação + integração com IA), baixado da fonte.
2. **Clientes** — "Mais de 800 clientes no Brasil, Latam e Portugal" + "Confiam na nossa solução" + grade de logos (reaproveitada de `brand/cxpress/assets/plataforma/clientes-cxpress.png`, mesmo asset usado nas demais LPs Cxpress).
3. **Destaque WhatsApp CoEx** (seção nova, não existe nas outras LPs Cxpress do repo) — badge, H2, subtítulo, 4 benefícios em grid 2×2, frase de fechamento.
4. **Benefícios** — H2 + subtítulo + 3 cards + fechamento com CTA.
5. **Prova (stats)** — 14% / 9% / 25% / 45%, com notas de rodapé NBER/McKinsey. **Sem headline própria na fonte** — não inventei uma.
6. **Plataforma** — 5 features (uma a mais que o padrão de 4 usado nas outras LPs): 3 ilustradas com os GIFs de produto já existentes (`plataforma-canais.gif`, `plataforma-chatbot-ia.gif`, `plataforma-dashboard.gif`) e 2 em cards `feature--textonly` (a fonte não tem imagem própria pra essas duas).
7. **Quem somos** — texto institucional padrão + badges (API oficial WhatsApp, API oficial ChatGPT, Um produto Elife).
8. **Condições especiais / Formulário** — badges de preço, H2, corpo, preço (R$ 1.750), e-mail comercial, formulário Jotform.
9. **FAQ** — 6 perguntas (uma a mais que o padrão de 5: inclui "Posso usar o mesmo número no WhatsApp Business e na Cxpress?", específica desta LP).

Não existe seção "Fecho" (pausa dark) nesta LP — a fonte não tem, então não foi criada.

## Melhorias de design aplicadas (aprendidas em banimento-whatsapp-clinicas)

- `.hero{padding:0}` desde o início — evita o bug de padding empilhado (`section{padding:130px 0}` genérico + padding próprio do `.hero__inner`) que causou o espaço em branco excessivo identificado naquela outra sessão. Gap menu→H1 aqui: **146px** (mesmo valor-alvo da correção anterior).
- Logo Elife corrigida desde a criação (`assets/elife-logo-badge.png`, mesma técnica de reconstrução de canal alfa — crop 235×81, unmultiply contra fundo cinza 244/244/244).
- Componentes de card (`.card`, `.beneficios__grid`, `.destaque__grid`) compartilhados via CSS reaproveitado, sem duplicação.

## Formulário

Jotform `261027639617663` — **mesmo ID usado na página fonte** (confirmado via inspeção do iframe ao vivo) e o mesmo já usado em `banimento-whatsapp-clinicas`. É um formulário compartilhado entre múltiplas campanhas Cxpress — não pode ser alterado sem afetar outras páginas (ver conversa sobre a ideia de clonar o formulário no Jotform para um fluxo de "obrigado" dedicado, discutida mas não implementada nesta LP).

## Estrutura

- HERO (mockup do dashboard em card)
- CLIENTES (prova social)
- DESTAQUE (WhatsApp CoEx)
- BENEFICIOS
- PROVA (stats, sem headline)
- PLATAFORMA (5 features)
- QUEM SOMOS
- FORM / Condições especiais
- FAQ (6 perguntas)
- FOOTER

## Estado

- [x] HTML gerado (base: sistema visual de `banimento-whatsapp-clinicas`, adaptado pra 9 blocos de conteúdo próprios)
- [x] SEO completo (title, description, canonical, OG, Twitter Card, JSON-LD) — slug `whatsapp-business-smb`
- [x] GTM — `GTM-T4XDWHL3` (região `brasil`, mesmo container das demais LPs Cxpress BR), validado via `check_gtm_region.py`
- [x] OG image dedicada — `assets/og-whatsapp-business-smb.png` (1200×630), gerada via Chrome headless + `.claude/skills/lp-gerar/og-template.html`, com overline "Condições especiais" + H1 do hero + logo Cxpress
- [x] Testado localmente — build do guarda-chuva (`build_umbrella.py`, 0 avisos novos) + servidor estático local; validado via `getComputedStyle`/`getBoundingClientRect` (sem screenshot disponível nesta sessão): sem overflow horizontal em mobile (375px, corrigido — ver Revisão), tablet (768px) e desktop (1265px); grids renderizam 2/3/4 colunas conforme esperado por breakpoint; todos os 10 assets referenciados respondem HTTP 200
- [ ] Publicado — rodar `/lp-publicar cxpress whatsapp-business-smb content.cxpress.io`

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `./assets/hero-dashboard.gif` (hero — GIF do produto baixado da fonte, LP-local)
- `./assets/elife-logo-badge.png` (badge Quem Somos — versão corrigida/transparente, LP-local)
- `../../brand/cxpress/assets/plataforma/clientes-cxpress.png` (prova social)
- `../../brand/cxpress/assets/plataforma/plataforma-canais.gif`, `plataforma-chatbot-ia.gif`, `plataforma-dashboard.gif` (seção Plataforma, 3 das 5 features)
- `../../brand/cxpress/assets/plataforma/quem-somos-foto.jpg`

## Atualizacao de preco — 2026-08-28

Novo preco minimo de plano da Cxpress: **R$ 1.750**. A chamada de preco desta LP passou a
`Planos a partir de R$ 1.750`, **sem** mencao a quantidade de acessos — por decisao do usuario,
o detalhamento de acessos fica restrito a LP canonica de precos (`/planos`), que segue intacta
com "A partir de R$ 1.750 por mes, com 5 acessos de operador". Alteracao aplicada em bloco nas
9 LPs BR da Cxpress que citavam preco fora da `/planos`.

As LPs LATAM (`USD 260/mes`) e PT-PT (`295 EUR/mes`) **nao** foram alteradas: os valores oficiais
em USD/EUR ainda nao foram definidos e seguem defasados em relacao ao minimo BR.
