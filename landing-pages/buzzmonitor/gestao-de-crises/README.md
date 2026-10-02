# LP Buzzmonitor — gestao-de-crises

**Gerado em:** 2026-10-02
**Copy-fonte:** `copy.txt` (output de /copy-criar + /lp-preparar; Notion "Copy LP da dor 4 - Antecipação de crises" em Campanha MOFU: 4 dores dos clientes)
**Uso:** Campanha Meta Ads MoFu, Dor 4 (antecipação de crises / crises e avaliações negativas chegando tarde)
**Domínio-alvo sugerido:** `content.buzzmonitor.com/gestao-de-crises` (guarda-chuva migrado ao CI)

## Formato e base visual

Pedido explícito: formato e visual da LP `promo.buzzmonitor.com/monitoramento-com-ia`, e não o das LPs das dores 1 a 3.
A fonte dessa LP no repo é `landing-pages/buzzmonitor/social-listening-ia/` (classes `hero`, `benefits`, `sp`, `ais`, `vid`, `av`, `cr`, `wa`, `oferta`, `dep`).
O HTML foi montado sobre o CSS e os componentes dessa fonte (em vez de gerado do zero via `frontend-design`), para manter a paridade visual pedida.

## Estrutura (round 3, 2026-10-02)

1. HEADER (logo + redes + CTA)
2. HERO: overline com ponto pulsante, H1 com "crise" em laranja, mock de alerta no centro das órbitas
3. FAIXA DE LOGOS full-bleed (ponta a ponta, logos de 90px, tiras `clientes-1..4.webp` recortadas sem respiro lateral, espaçamento uniforme)
4. BENEFÍCIOS: degradê laranja→rosa, 6 cards + 1 card largo roxo (MCP)
5. PROVA SOCIAL + FORMULÁRIO: 4 números + Jotform `252995108251662` (o mesmo das LPs das dores 1 a 3) em card branco com contorno preto, com 2 badges flutuantes
6. SINAIS DE CRISE: gráfico com pico + chips (Procon, boicote, atraso, estragado) + "Alerta via e-mail ou WhatsApp"
7. SAIBA DA CRISE ANTES DA DIRETORIA: 4 passos numerados
8. AUDIOVISUAL: 2 imagens com tags REELS / ÁUDIO
9. MCP PARA CRISES: 1 balão + card "Report de Crise" + tablet horizontal com o report real da Skill de Crise rolando (26 s em loop) e 3 destaques que saltam para frente; prova social do MCP com logos e big numbers em degradê (Tech & Soul, Design bridge and partners, autorizados em 2026-10-02)
10. CASE E-CLIK
11. OFERTA 14 dias
12. DEPOIMENTOS
13. FOOTER

Seção de WhatsApp removida no round 3.

## Estado

- [x] HTML gerado (715 linhas, ~60 KB, CSS inline)
- [x] Checklist técnico/SEO: em-dash 0, `og:` 10, `twitter:` 4, JSON-LD válido, GTM `GTM-WFJVK858` 2x, canonical com `{{DOMAIN}}`
- [x] Overflow horizontal 0 em 1440 px e 390 px (Playwright); imagens quebradas 0 (exceto os 2 logos do brand, ver Pendências)
- [x] OG image 1200×630 → `assets/og-gestao-de-crises.png` (fonte: `assets/og-source.html`, render via Playwright)
- [ ] Revisão (frontend-design review + web-design-guidelines): rodar `/lp-revisar buzzmonitor/gestao-de-crises`
- [x] Formulário integrado: Jotform `252995108251662` (round 3)
- [x] Report no tablet (seção MCP): `assets/mcp-report.webp` + destaques `hl-kpis.webp`, `hl-descricao.webp`, `hl-plano.webp`, gerados do PDF da Skill de Crise (rodapé Elife Portugal cortado)
- [ ] Publicado: rodar `/lp-publicar buzzmonitor gestao-de-crises content.buzzmonitor.com`

## Pendências

- **Logos do brand no preview local:** `../../brand/...` é a convenção de source (GUIDELINES/CONTEXT §3) e é resolvida no build do guarda-chuva. No preview local direto da pasta eles aparecem quebrados, igual às LPs irmãs.
- **Posição do formulário:** 3ª seção, como na referência (override consciente de GUIDELINES §10 para MoFu, registrado no `copy.txt`).
- **Contraste do laranja:** botões `#EB7C2E` com texto branco ficam abaixo de AA (mesmo caso já aceito na referência e nas LPs irmãs). Textos laranja pequenos usam `#b85613` (AA).
- Mídia opcional: se houver vídeo/gif da tela de triggers, ele pode substituir o mock do hero ou os 4 passos da seção 6.

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header), `logo-reversed.svg` (footer), `logo-icon.png` (favicon). `grep -c '<text'` = 0 nos dois SVGs
- `assets/clientes-1..4.webp` (tiras de logos rasterizadas e recortadas a partir de `social-listening-ia/assets/slideclientes1..4.svg`)
- `assets/logo-tech-and-soul.png`, `assets/logo-design-bridge-and-partners.png` (enviados pela usuária, recortados)
- `assets/mcp-report.webp`, `assets/hl-*.webp` (report da Skill de Crise)
- `assets/og-gestao-de-crises.png` + `assets/og-source.html`
- `assets/audiovisual-reels.jpg`, `assets/audiovisual-audio.jpg` (de `social-listening-ia`, renomeados)
- `assets/megafone.png` (de `social-listening-ia`)
- `assets/logo-eclik.png` (de `plataforma-completa-atendimento`, marca crm bonus, renderizado em branco via `filter`)
- `assets/mccan.svg`, `assets/totalpass.svg`, `assets/mcdonalds.svg` (de `monitoramento-com-ia`)
