# LP Buzzcreators — Vendendo com Creators

**Gerado em:** 2026-04-27
**Copy-fonte:** `copy.txt` (output de `/lp-preparar`)
**Notion:** https://www.notion.so/34f3934026fd8117845eecefb914ca38

## Estrutura

- HOOK (intro pré-hero)
- HERO (com ticket "save the date" rotacionado, gradiente assinatura no H1)
- PROBLEMA (lista vertical, 4 itens, X vermelhos)
- BENEFICIOS (grid 3 colunas, 6 itens, ✓ verdes)
- SPEAKER (card horizontal — placeholders)
- PROVA (3 stats em destaque + nota com ROI 3x / 60%)
- CTA INTERMEDIARIO (banner gradiente assinatura)
- PARA QUEM (grid 2 colunas, 5 itens)
- URGENCIA (fundo dark roxo + tag laranja rotacionada -3deg)
- CTA FINAL (form mock)
- FOOTER

## Configuração especial desta LP

- **GTM:** `GTM-WFJVK858` — container da **Buzzmonitor Brasil** (não Buzzcreators), por pedido explícito do briefing. `brand/buzzcreators/tracking.json` está null em todas regiões; a injeção é manual nesta LP.
- **Form:** mock (action="#"). Integração real via `/lp-integrar-form buzzcreators/vendendo-com-creators "<snippet>"` com Jotform `260213440661648`.

## Estado

- [x] HTML gerado
- [x] GTM Buzzmonitor BR injetado (script + noscript)
- [x] Revisão concluída (REVISAO.md) — 3 críticos aplicados, 5 melhorias opcionais documentadas
- [x] Form integrado — Jotform `260213440661648` (2026-04-27)
- [x] Publicado em produção (2026-04-27)

**Form provider:** Jotform — script `https://form.jotform.com/jsform/260213440661648` (integrado em 2026-04-27)

## URL pública

- **Live:** https://evento.buzzmonitor.com/vendendo-com-creators (migrada de `webinar.*` em 2026-04-28)
- **Project Vercel:** `buzzmonitor-evento` — guarda-chuva Buzzmonitor de eventos presenciais que serve `evento.buzzmonitor.com`
- **Redirect 301 ativo** em `webinar.buzzmonitor.com/vendendo-com-creators` → `evento.buzzmonitor.com/vendendo-com-creators` (preserva URLs já compartilhadas).

## Convivência no projeto guarda-chuva

`evento.buzzmonitor.com` é guarda-chuva de **eventos presenciais** (Buzzmonitor + Buzzcreators). Esta é a primeira LP do projeto; futuras LPs presenciais cairão aqui.

Para evitar colisão de assets entre marcas (Buzzmonitor e Buzzcreators têm `logo-icon.png` com nomes iguais), os assets desta LP ficam em `/assets/buzzcreators/...` (namespace por marca).

**Source uses LP-local paths** (`./assets/buzzcreators/X`). Os arquivos físicos estão em `landing-pages/buzzcreators/vendendo-com-creators/assets/buzzcreators/`.

## Assets referenciados

- `./assets/buzzcreators/logo-full-color.svg` (header)
- `./assets/buzzcreators/logo-icon.png` (favicon)
- `./assets/buzzcreators/bruno-filho.png` (foto do speaker)

## Estrutura visual atual (pós Iteração 2)

- HERO (com ticket "save the date" rotacionado, gradiente assinatura no H1, label "Apenas 80 vagas presenciais")
- HOOK (callout com dado YOUPIX/Nielsen 2025: 53% / 48%)
- BENEFICIOS (lista vertical, 6 itens com checks roxos sólidos, CTA "Quero estar lá dia 20/05", fundo branco)
- SPEAKER (Bruno Filho — Coordenador de Novos Negócios Buzzcreators, foto circular)
- CTA INTERMEDIARIO (banner gradiente assinatura)
- PARA QUEM (lista com setas →, 5 itens)
- CTA FINAL (card branco completo: H2 + chips de evento + form Jotform `260213440661648` + endereço Espaço Paulista + botão Google Maps)
- URGENCIA (fundo dark roxo + tag laranja rotacionada)
- VIDEO BUZZCREATORS (H2 "Conheça o Buzzcreators" + lead institucional + iframe YouTube `nBK4ehM0YLo`)
- FOOTER (Buzzcreators · Buzzmonitor · eventos@buzzmonitor.com.br)
