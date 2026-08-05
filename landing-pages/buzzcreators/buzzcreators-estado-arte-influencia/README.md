# LP Buzzcreators: Estado da Arte do Marketing de Influência

**Gerado em:** 2026-05-26
**Copy-fonte:** `copy.txt` (output de /lp-preparar)
**Material rico fonte:** [Notion ESTADO DA ARTE](https://gamy-meerkat-e13.notion.site/ESTADO-DA-ARTE-MARKETING-DE-INFLU-NCIA-2025-1-eae3934026fd83b49d2f01e4314e7aff)

## Estrutura

- Header sticky (logo + CTA "Quero o material")
- Hero centralizado editorial: overline pill, H1 com "agora" em gradiente assinatura, sub, CTA, mascote interativo (foge do mouse no desktop) e marquee de tópicos no rodapé do hero
- Form (2ª seção, ToFu): mock com 4 campos (nome, e-mail, empresa, cargo)
- O que tem dentro: grid de 4 cards (cases globais, cases brasileiros, benchmark, playbook 30-60-90) + linha de 3 cards bônus (template de briefing, rota Buzzcreators, playbook 2026)
- Por que importa: 5 números editoriais gigantes, todos em gradiente assinatura, alinhamento zigzag esquerda/direita
- Para quem é: lista vertical com marcador `+` laranja
- Mini-game "Vendas com creators": clicar nos creators (nano/micro/mega) que aparecem na arena por 15s; placar em R$ amarra com a tese do material
- Urgência: seção dark (roxo primary) com tag "Atualizado" rotacionada
- Footer

## Estado

- [x] HTML gerado
- [x] Revisão (PR review #10 aplicada: SEO completo, logo limpo, a11y, §17)
- [ ] Formulário integrado: rodar `/lp-integrar-form buzzcreators/buzzcreators-estado-arte-influencia "<snippet>"`
- [ ] Publicado: sugestão de domínio `material.buzzmonitor.com` (guarda-chuva Buzzmonitor de material rico evergreen; assets em `/assets/buzzcreators/`). Rodar `/lp-publicar buzzcreators buzzcreators-estado-arte-influencia material.buzzmonitor.com`

## Decisões de design aplicadas

- **DM Sans em tudo** (sem serif): atende ao brandbook estrito por escolha do usuário.
- **Números editoriais como "cartazes tipográficos"** na seção Por que importa: clamp até 148px desktop, alinhamento alternando esquerda/direita para ritmo editorial.
- **Gradiente assinatura** (`background-clip: text`) aplicado no H1 ("agora"), nos 5 números da seção Por que importa, no divisor do footer e na barra base da OG image. Um único tipo de gradiente (roxo, laranja) na LP inteira.
- **Mascote interativo** (`logo-icon-color.svg`): foge do mouse no desktop via `position: fixed`; escondido em mobile, em `hover: none` e em `prefers-reduced-motion`.
- **Mini-game** "Vendas com creators": pesos por tier (micro aparece mais, mega aparece pouco), placar em R$, mensagens de fim variando pelo resultado. Cards são `<button>` com `aria-label`; placar com `aria-live`.
- **Reveals scroll-triggered** via IntersectionObserver com fallback `<noscript>` e respeito a `prefers-reduced-motion`.
- **SEO completo**: description, robots, Open Graph (8 tags), Twitter Card, JSON-LD (Organization + WebPage) e OG image 1200x630 (`assets/og-buzzcreators-estado-arte-influencia.png`).
- **Sem em-dash** (validado: 0 ocorrências no HTML e na copy).
- **Sem GTM** (tracking.json Buzzcreators está todo null).

## Assets referenciados

- `../../brand/buzzcreators/assets/logos/logo-icon.png` (favicon, path source; vira `/assets/.../logo-icon.png` no deploy)
- `./assets/logo-full-color.svg` (header, vetor limpo do brand, 18KB)
- `./assets/logo-full-white.svg` (footer, vetor branco do brand)
- `./assets/logo-icon-color.svg` (mascote do hero)
- `./assets/og-buzzcreators-estado-arte-influencia.png` (Open Graph 1200x630)

## Paleta usada

- Roxo escuro `#3a1652` (autoridade, urgência, footer)
- Roxo médio `#6a3895` (acentos, números editoriais)
- Laranja `#ff8119` / `#ff7300` (CTA, marcadores)
- Off-white `#f7f9fb` (alternância de seção)
- Branco `#ffffff` (base)
