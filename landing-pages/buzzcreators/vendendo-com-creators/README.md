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

- **Live:** https://webinar.buzzmonitor.com/vendendo-com-creators
- **Inspect (Vercel):** https://vercel.com/elife-group/buzzmonitor-lp-monitoramento-concorrentes/AEmQ3GZdS1bf2ZYqnvh4FVkJzfuU
- **Deployment ID:** `dpl_AEmQ3GZdS1bf2ZYqnvh4FVkJzfuU`
- **Project:** `buzzmonitor-lp-monitoramento-concorrentes` (`prj_bqOBy4RXCnPFu8Fn7csQ6wzyjwb6`) — guarda-chuva Buzzmonitor que serve `webinar.buzzmonitor.com`

## Convivência no projeto guarda-chuva

`webinar.buzzmonitor.com` é multi-LP. Esta LP coexiste com:
- `webinar.buzzmonitor.com/monitoramento-concorrentes-maio-2026` (Buzzmonitor BR)
- `webinar.buzzmonitor.com/monitoramento-concorrentes-maio-2026-pt` (Buzzmonitor PT)

Para evitar colisão de assets (Buzzmonitor e Buzzcreators têm `logo-icon.png` com nomes iguais), os assets desta LP ficam em `/assets/buzzcreators/...` (namespace por marca) — não em `/assets/logos/...` (que é da Buzzmonitor).

**Source uses LP-local paths** (`./assets/buzzcreators/X`) em vez do padrão brand (`../../brand/{marca}/assets/X`). Os arquivos físicos estão em `landing-pages/buzzcreators/vendendo-com-creators/assets/buzzcreators/`.

> **Projeto Vercel separado** `buzzcreators-lp-vendendo-com-creators` (`prj_qwXzsA7qo0QPhsVyNyGDEOkAqBx6`) foi criado em deploy anterior e ficou **órfão** (sem domínio, conteúdo idêntico ao do guarda-chuva). Pode ser removido manualmente via Vercel Dashboard sem impacto. SSO Protection foi desabilitada lá (irrelevante depois da remoção).

## Assets referenciados

- `../../brand/buzzcreators/assets/logos/logo-full-color.svg` (header)
- `../../brand/buzzcreators/assets/logos/logo-icon.png` (favicon)

## Pendências de copy (placeholders)

Renderizados literalmente como aparecem:
- `[X] vagas presenciais` (HERO label)
- `[NOME DO MENTOR] — [cargo / posição atual]` (SPEAKER name)
- `[1-2 frases sobre autoridade...]` (SPEAKER bio)
- `[Foto opcional...]` (SPEAKER photo note)

Substituir antes do deploy ou marcar como pendência em `REVISAO.md`.
