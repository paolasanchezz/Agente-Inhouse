# Inventário Fase 0 — reconciliação repo × live (2026-07-15)

> Artefato do PLANO-MIGRACAO-CI.md, itens 0.1–0.4. Fonte: API Vercel (read-only),
> deploys production READY mais recentes de cada guarda-chuva nesta data.

## 1. Estado do live por guarda-chuva

| Domínio | Projeto Vercel | Deploy auditado | LPs no ar |
|---|---|---|---|
| `content.cxpress.io` | `cxpress-lp-playbook-whatsapp2026` | `dpl_FGfe8npfySCTZxPxB74KyQ7qpckd` | 30 |
| `webinar.buzzmonitor.com` | `buzzmonitor-lp-monitoramento-concorrentes` | `dpl_GFakg4JY1cp8go7ZudEW6EzYJ5rk` | 27 |
| `evento.buzzmonitor.com` | `buzzmonitor-evento` | `dpl_C8s6CQXBPjVqbyAeK2KTMYUZiQin` | 4 |
| `material.buzzmonitor.com` | `buzzmonitor-material` | `dpl_Dm8tjME8BEd8b7WmWAvSfmYHw8HZ` | 6 (incl. `_placeholder` estrutural) |

Snapshots dos `vercel.json` live: `snapshots-2026-07-15/vercel-{dominio}.json`.
Redirects encontrados (entram nos manifestos da Fase 1):
- `webinar.*`: `/vendendo-com-creators` → `https://evento.buzzmonitor.com/vendendo-com-creators` (308); `/monitoramento-concorrentes-maio-2026` → `/analise-preditiva-maio-2026` (308)
- `material.*`: `/mcp-maio-2026` → `/mcp` (308)

## 2. Órfãs importadas (19 LPs no ar sem source no repo — anti-padrão §7.1)

Todas baixadas do live, paths revertidos pra convenção de source e commitadas
em `landing-pages/{marca}/{slug}/`. Marca inferida pelo namespace `/assets/{marca}/`.

| Slug | Marca | Domínio |
|---|---|---|
| atencion-digital-latam | cxpress | content.cxpress.io |
| banimento-whatsapp-latam | cxpress | content.cxpress.io |
| banimento-whatsapp-pt | cxpress | content.cxpress.io |
| coex-whatsapp-latam | cxpress | content.cxpress.io |
| ebook-marketing-conversacao-pt | cxpress | content.cxpress.io |
| oferta-whatsapp-comercial-bloqueado | cxpress | content.cxpress.io |
| pos-evento | cxpress | content.cxpress.io |
| sector-it-latam | cxpress | content.cxpress.io |
| sector-marketing-latam | cxpress | content.cxpress.io |
| whatsapp-agencias-pt | cxpress | content.cxpress.io |
| whatsapp-comercial-bloqueado | cxpress | content.cxpress.io |
| ia-no-sac-agosto-2026 | buzzmonitor | webinar.buzzmonitor.com |
| monitoreo-competidores-ia-latam | buzzmonitor | webinar.buzzmonitor.com |
| oferta-webinar-mcp | buzzmonitor | webinar.buzzmonitor.com |
| social-listening-julho-2026-brasil-oferta | buzzmonitor | webinar.buzzmonitor.com |
| buzzmonitor-connect-julio-2026-latam | buzzmonitor | evento.buzzmonitor.com |
| influent-summit-tablet | buzzcreators | evento.buzzmonitor.com |
| oferta-webinar-influencia | buzzcreators | evento.buzzmonitor.com |
| estudo-diversidade-2026 | buzzmonitor | material.buzzmonitor.com |

Convenção da reversão: ref a asset que existe em `brand/{marca}/assets/` →
`../../brand/{marca}/assets/...`; demais → download pro `{slug}/assets/` + ref `./assets/...`.
Refs absolutas (`https://{dominio}/assets/...`, ex. `og:image`) foram mantidas como estão.

## 3. Problemas pré-existentes encontrados (não introduzidos pela migração)

1. **`og:image` 404 no live hoje** — HTML referencia OG image que não existe no deploy:
   `atencion-digital-latam`, `pos-evento`, `sector-it-latam`, `sector-marketing-latam`,
   `whatsapp-agencias-pt` (content.cxpress.io), `oferta-webinar-mcp` (webinar),
   `buzzmonitor-connect-julio-2026-latam` (evento), `influent-summit-tablet` (evento).
   Corrigir gerando as OG images — pode ser feito junto da Fase 1 ou depois; não bloqueia.
2. **Assets legados na raiz de `content.cxpress.io`** (`/assets/logos/*`, `/assets/mascot/samir-*`,
   `/assets/speakers/*`) — herança da era solo do projeto. Pelo menos
   `ebook-marketing-conversacao-pt` referencia `/assets/logos/*` sem namespace.
   **Consequência pra Fase 1:** o manifesto de content.cxpress.io precisa de campo
   `legacy_root_assets` e o build precisa copiá-los na raiz do dist, senão a paridade quebra.
3. **Namespace `assets/elife/` em content.cxpress.io** — o slug `consumidores-sinteticos-evento`
   (live) usa assets elife. O repo tem source duplicado (`cxpress/` E `elife/` com o mesmo slug).
   **Resolver na Fase 1:** decidir qual é o source canônico do slug live e remover/arquivar o outro.
4. **LPs com source no repo mas fora dos guarda-chuvas** (informativo — prováveis solo ou rascunho):
   `buzzmonitor/pocket-events`, `buzzmonitor/social-listening-ia`, `_experimentos/hallmark-*`.

## 4. Decisões e execução Fase 0

- ✅ 0.1 Secret `VERCEL_TOKEN` criado no GitHub Actions (2026-07-15). Validação DENTRO de
  um workflow acontece na Fase 2 (workflows só rodam a partir da main; entram via PR).
- ✅ 0.2 Plano GitHub: **Free em conta pessoal** — branch protection indisponível em repo
  privado (HTTP 403 confirmado). Decisão: merge-bot via Actions (§1.2 do plano). Upgrade Pro opcional.
- ✅ 0.3 Reconciliação: 19 órfãs importadas (tabela acima). Live e repo agora 1:1 nos
  4 guarda-chuvas (exceto duplicidade elife/cxpress do item 3.3).
- ✅ 0.4 Snapshots de `vercel.json` capturados em `snapshots-2026-07-15/`.
- ⬜ 0.5 Victor: confirmar lista de paths livres (§1.2 do plano) e ordem de rollout.
