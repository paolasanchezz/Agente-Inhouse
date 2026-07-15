# Projeto guarda-chuva — evento.buzzmonitor.com

Artefato **publicado** das LPs servidas em `evento.buzzmonitor.com`. Multi-LP: cada subpasta da raiz é uma página com path próprio.

## Convenção de uso

Eventos **presenciais** Buzzmonitor (workshops, meetups, palestras físicas).

## LPs ativas

| Path | Marca | Fonte no repo |
|---|---|---|
| `/influent-summit-tablet` | Buzzcreators | `Agente Inhouse/landing-pages/buzzcreators/influent-summit-tablet/` |
| `/oferta-webinar-influencia` | Buzzcreators | `Agente Inhouse/landing-pages/buzzcreators/oferta-webinar-influencia/` |
| `/vendendo-com-creators` | Buzzcreators | `Agente Inhouse/landing-pages/buzzcreators/vendendo-com-creators/` |
| `/buzzmonitor-connect-julio-2026-latam` | **Buzzmonitor (novo, 2026-07-14)** | `Agente Inhouse/landing-pages/buzzmonitor/buzzmonitor-connect-julio-2026-latam/` |

## Estrutura prevista

```
{slug-1}/index.html       — primeira LP
{slug-2}/index.html       — segunda LP
assets/
├── logos/                — assets Buzzmonitor (compartilhados)
├── {marca-secundaria}/   — assets de outra marca (ex: Buzzcreators) com namespace
vercel.json               — cleanUrls + 7 headers de segurança
```

## Deploy

`npx vercel deploy --prod --yes` desta pasta, ou via skill `lp-publicar` no repo do agente.
