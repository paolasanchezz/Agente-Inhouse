# Projeto guarda-chuva — webinar.buzzmonitor.com

Artefato **publicado** das LPs servidas em `webinar.buzzmonitor.com`. Multi-LP: cada subpasta da raiz é uma página com path próprio.

## LPs ativas

| Path | Marca | Fonte no repo |
|---|---|---|
| `/monitoramento-concorrentes-maio-2026` | Buzzmonitor (BR) | `Agente Inhouse/landing-pages/buzzmonitor/monitoramento-concorrentes-maio-2026/` |
| `/monitoramento-concorrentes-maio-2026-pt` | Buzzmonitor (PT) | `Agente Inhouse/landing-pages/buzzmonitor/monitoramento-concorrentes-maio-2026-pt/` |
| `/social-listening-mayo-2026-latam` | Buzzmonitor LATAM | `Agente Inhouse/landing-pages/buzzmonitor/social-listening-mayo-2026-latam/` |
| `/agentes-automacao-junho-2026` | Buzzmonitor BR | `Agente Inhouse/landing-pages/buzzmonitor/agentes-automacao-junho-2026/` |
| `/agentes-automatizacion-junio-2026-latam` | Buzzmonitor LATAM | `Agente Inhouse/landing-pages/buzzmonitor/agentes-automatizacion-junio-2026-latam/` |
| `/ia-no-sac-agosto-2026` | **Buzzmonitor BR (novo)** | `Agente Inhouse/landing-pages/buzzmonitor/ia-no-sac-agosto-2026/` |

### Redirects 301 ativos

- `/vendendo-com-creators` → `https://evento.buzzmonitor.com/vendendo-com-creators` (LP migrada de webinar → evento em 2026-04-28; redirect preserva URLs já compartilhadas)

## Estrutura

```
monitoramento-concorrentes-maio-2026/index.html       — Buzzmonitor BR
monitoramento-concorrentes-maio-2026-pt/index.html    — Buzzmonitor PT
vendendo-com-creators/index.html                      — Buzzcreators BR
assets/
├── logos/                  — logos Buzzmonitor (primary, reversed, icon)
├── buzzcreators/           — assets Buzzcreators (logo-icon, logo-full-color)
├── mascot.png + .webp      — mascot Buzzmonitor
vercel.json                 — cleanUrls + 7 headers de segurança
```

Esta pasta é **apenas o artefato de deploy** — isolada do repo interno (que tem skills, `.env` do Meta e conhecimento privado).

## Convenção de assets — namespace por marca

Múltiplas marcas no mesmo domínio precisam evitar colisão de filename. Convenção:
- Buzzmonitor BR/PT: `/assets/logos/`, `/assets/mascot.*` (legacy, raiz)
- Buzzmonitor LATAM (e novas LPs): `/assets/buzzmonitor/...` (namespace explícito)
- Buzzcreators: `/assets/buzzcreators/...`
- Cxpress (futuro): `/assets/cxpress/...`

## Deploy

`npx vercel deploy --prod --yes` desta pasta, ou via skill `lp-publicar` no repo do agente.

## Formulários

- Buzzmonitor (BR + PT): Jotform `252154974852667`
- Buzzmonitor (LATAM): Jotform `261188302248052`
- Buzzcreators: Jotform `260213440661648`

Jotform é operador LGPD; dados não passam pela Vercel.
