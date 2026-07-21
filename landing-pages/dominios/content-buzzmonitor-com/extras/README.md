# Projeto guarda-chuva — content.buzzmonitor.com

Artefato **publicado** das LPs servidas em `content.buzzmonitor.com`. Multi-LP: cada subpasta da raiz é uma página com path próprio.

## Convenção de uso

Conteúdo Buzzmonitor de topo/meio de funil em **espanhol (ES-LATAM)** — social listening, monitoramento com IA. É o equivalente Buzzmonitor do `content.cxpress.io`.

## LPs ativas

| Path | Marca | Fonte no repo |
|---|---|---|
| `/ia-para-social-listening-es` | Buzzmonitor (ES) | `Agente Inhouse/landing-pages/buzzmonitor/ia-para-social-listening-es/` |
| `/la-mejor-plataforma-social-listening-es` | Buzzmonitor (ES) | `Agente Inhouse/landing-pages/buzzmonitor/la-mejor-plataforma-social-listening-es/` |

Migradas de `material.buzzmonitor.com` em 2026-07-21 (mesmo slug). Os paths antigos em `material.buzzmonitor.com/{slug}` fazem 301 permanente para cá.

## Deploy

Domínio migrado (CI). Deploy **exclusivamente** via GitHub Actions (`lp-deploy.yml`) — build da main inteira + smoke + rollback automáticos. Não há deploy local/sibling. Ver `landing-pages/CONTEXT.md` §2.6 e `landing-pages/PLANO-MIGRACAO-CI.md`.
