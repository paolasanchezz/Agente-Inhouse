# Prova de paridade — build_umbrella × produção (Fase 1)

> Gate da migração LP→CI (PLANO-MIGRACAO-CI.md §2.1, item 1.3). Executada em
> **2026-07-15** contra os deploys production READY mais recentes de cada guarda-chuva.

## Resultado: PARIDADE FECHADA nos 4 guarda-chuvas

| Domínio | Deploy auditado | LPs | Idênticos | Só-newline | Diferentes | Faltando | Sobrando |
|---|---|---|---|---|---|---|---|
| content.cxpress.io | `dpl_FGfe8npfySCTZxPxB74KyQ7qpckd` | 30 | 79 | 19 | **0** | **0** | **0** |
| webinar.buzzmonitor.com | `dpl_5rV1eTcM1sCunQ6QTMZVcwtdfPos` | 27 | 78 | 15 | **0** | **0** | **0** |
| evento.buzzmonitor.com | `dpl_C8s6CQXBPjVqbyAeK2KTMYUZiQin` | 4 | 16 | 3 | **0** | **0** | **0** |
| material.buzzmonitor.com | `dpl_Dm8tjME8BEd8b7WmWAvSfmYHw8HZ` | 5 | 33 | 5 | **0** | **0** | **0** |

Método: download de todos os arquivos de cada deploy via API Vercel → build local
via `build_umbrella.py` a partir dos manifestos → comparação md5 arquivo a arquivo.

## Classes de diff aceitas (explicadas)

1. **Só-newline (42 arquivos):** CRLF×LF entre source e live — resíduo de deploys
   históricos feitos de siblings Windows + normalização do git (`autocrlf`).
   Invisível pro browser. No primeiro deploy via CI esses arquivos normalizam
   pra LF — mudança de hash sem mudança de conteúdo. O smoke test do workflow
   deve comparar com newline normalizado.
2. **`og:image` referenciado mas inexistente (8 refs):** já é 404 no live hoje
   (pré-existente, documentado no INVENTARIO-2026-07-15.md §3.1). O build emite
   aviso e segue — mesmo comportamento do live. Corrigir gerando as imagens (follow-up).
   Idem `case-ia-de-voz/beatriz.jpg`.

## Drift encontrado e resolvido (source ≠ live)

Em 14 LPs o source do repo divergia do que está no ar. **O live foi adotado como
verdade** e os sources foram re-importados (versões antigas recuperáveis no git):

- **content.cxpress.io (9):** atendimento-digital, case-ia-de-voz, conheca-a-cxpress,
  ebook-marketing-conversacion-latam, gestao-canais-ia-2026, latam-webinar-atencionalcliente,
  playbook-whatsapp2026, webinar-tecnologia-maio2026(-oferta) — mistura de hotfix
  não commitado e convenção de path da era solo.
- **webinar.buzzmonitor.com (5):** buzzcreators-webinar-junho e mcp-para-social-listening
  (live virou versão "webinar gravado"), ia-no-sac-agosto-2026 (copy editada e deployada
  em 15/07 sem commit), social-listening-julho-2026-brasil (countdown só no live),
  webinar-diversidade-2026 (data remarcada 23/07→04/08 só no live).

Isso é o retrato do problema que a migração mata: 14 LPs onde "o que o repo diz"
e "o que está no ar" já tinham divergido silenciosamente.

## Decisões de desenho tomadas na Fase 1

- **`vercel.json` versionado verbatim por domínio** (`dominios/{dom}/vercel.json`,
  cópia fiel do live) em vez de composição template+extras prevista no plano §1.1.
  Mais simples, paridade perfeita, e editar CSP vira um PR normal. A composição
  com template pode voltar depois se houver drift sistemático de CSP.
- **`extra_files` no manifesto** cobre: `_placeholder` estrutural (material),
  assets legados da era solo na raiz de content.cxpress.io (`/assets/logos`,
  `/assets/mascot`, `/assets/speakers`), e assets vivos no live sem referência
  em HTML nenhum (mantidos por segurança; limpeza é follow-up).
- **Assets referenciados por LPs que só existiam no live** (26 arquivos — ex.
  fotos de palestrantes, murais de logos) foram realocados pros
  `landing-pages/{marca}/{slug}/assets/` — sources agora são autocontidos.
- **Item 1.4 (testes):** a prova de paridade contra 66 LPs reais cobre todos os
  casos do plano (asset LP-local, asset brand, redirect-source, multi-marca,
  og-image, BOM, CRLF, namespace por slug, refs bare). Testes unitários formais
  ficam como melhoria futura; o gate de regressão do build é re-rodar esta prova.

## Bugs de transform encontrados e corrigidos no build durante a prova

1. Validação de doctype rejeitava HTML com BOM UTF-8 (LPs importadas do live).
2. Refs bare já namespaceadas (`src="assets/{marca}/…"`) ganhavam namespace duplo.
3. Refs `./assets/{marca}/…` idem (ordem dos replaces).

## Como re-rodar a prova

Harness versionado em `landing-pages/build/paridade_check.py` — baixa o live,
regenera manifestos, builda e compara:

```bash
set -a; source .env.local; set +a   # VERCEL_TOKEN
REPO_ROOT="$(cygpath -m "$(git rev-parse --show-toplevel)")" \
  CACHE_DIR="<pasta-de-cache-fora-do-repo>" \
  py landing-pages/build/paridade_check.py
```

Antes do cutover da Fase 2 a prova DEVE ser re-executada fresh (o live muda todo
dia; o harness detecta deploy novo e re-baixa sozinho). Atenção: o harness
REGENERA os manifestos a partir do live — depois do cutover (manifesto passa a
ser a fonte de verdade) ele só serve como auditoria, não deve sobrescrever manifesto.
