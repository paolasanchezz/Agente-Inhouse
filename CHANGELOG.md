# Changelog

Mudanças relevantes nas skills do Agente Inhouse.

Cada skill é versionada de forma independente, no campo `version` do frontmatter de seu `SKILL.md`. O esquema é semver simplificado:

- **MAJOR** — muda interface (parâmetros, comandos) ou comportamento de forma incompatível.
- **MINOR** — adiciona capacidade preservando compatibilidade.
- **PATCH** — correção, ajuste de tom, refinamento de prompt sem mudar comportamento esperado.

**Como atualizar:** ao alterar uma skill, bumpe a `version` no frontmatter e adicione uma entrada nova na seção da skill correspondente abaixo, no mesmo PR. Datas em ISO (`YYYY-MM-DD`).

---

## landing-page (advisor) + familia lp-*
### 1.2.0 — 2026-04-20
- `lp-gerar` (v1.1.0): injeta automaticamente **Google Tag Manager** no HTML gerado, lendo o container id de `brand/{marca}/tracking.json` (`gtm.regions[{regiao}]` > `gtm.default`; se ambos `null`, omite).
- Novo arquivo canonico **`brand/{marca}/tracking.json`** — schema `tracking/v1` com `gtm.default` + `gtm.regions.{brasil,latam,portugal}`. Buzzmonitor preenchido (`GTM-WFJVK858` cobre BR/LATAM/PT); Cxpress/Buzzcreators/Elife ficam como stubs `null` ate IDs oficiais.
- `lp-publicar` (v1.2.0): novo passo 5.3 valida via `curl` que ambos snippets GTM (`<script>` + `<noscript>`) estao servidos na URL final. Relatorio Notion passa a listar GTM container e status `2/2 | 1/2 | 0/2`.
- LP `buzzmonitor/monitoramento-concorrentes-maio-2026` recebeu GTM injetado e foi redeployada.

### 1.1.0 — 2026-04-20
- `lp-publicar`: template `vercel.template.json` agora inclui header **Content-Security-Policy (CSP)** — cobre Jotform, RD Station, HubSpot, Google Fonts, GA/GTM, YouTube e Vimeo por default.
- `lp-publicar`: passo 1.6 documenta quando ajustar o CSP (scripts externos nao-default); passo 5.2 valida a presenca do header pos-deploy; relatorio Notion passa a listar 7 headers ativos.
- `lp-integrar-form`: novo passo 2.5 remove o JS placeholder do form quando se troca mock por embed real — evita `TypeError: Cannot read properties of null (reading 'addEventListener')` no console da LP publicada.

### 1.0.0 — 2026-04-18
- Familia nova de skills para automatizar criacao de LPs ponta-a-ponta: `lp-preparar`, `lp-gerar`, `lp-revisar`, `lp-integrar-form`, `lp-publicar`, `lp-pipeline` + advisor `/landing-page`.
- Marca-agnostica: funciona para Buzzmonitor, Buzzcreators, Cxpress e Elife.
- CONTEXT.md compartilhado em `.claude/skills/lp-preparar/CONTEXT.md`.
- `landing-pages/GUIDELINES.md` enriquecido com §8 (secoes-tipo), §9 (copy dita estrutura), §10 (integracao tardia de form).
- `lp-publicar` usa pasta sibling isolada + validacao de isolamento pre-deploy, PageSpeed Insights API pos-deploy e relatorio Notion.
- LPs existentes migradas para `landing-pages/buzzmonitor/{slug}/`.

## anuncios (advisor)
### 1.0.0 — 2026-04-14
- Reescrita completa: SKILL.md cortado de 156 para ~65 linhas (~58% menor).
- Removido step de confirmação (2 turnos LLM a menos por invocação).
- Adicionado fast-path: `/anuncios performance buzzmonitor_brl mes_atual` dispara em 1 turno.
- Removidas seções Princípios, Fallback e Passo 0 (aviso inline).

## escrever (advisor)
### 1.0.0 — 2026-04-14
- Reescrita completa: SKILL.md cortado de 206 para ~75 linhas (~64% menor).
- Removido step de confirmação. Adicionado fast-path para os 4 sub-fluxos.
- Removidas seções Princípios e Fallback.

## newsletter (advisor)
### 1.0.0 — 2026-04-14
- Reescrita completa: SKILL.md cortado de 122 para ~50 linhas (~59% menor).
- Removido step de confirmação. Adicionado fast-path.
- Removidas seções Princípios e Fallback.

## traduzir (advisor)
### 1.0.0 — 2026-04-14
- Reescrita completa: SKILL.md cortado de 122 para ~50 linhas (~59% menor).
- Removido step de confirmação. Adicionado fast-path.
- Removidas seções Princípios e Fallback.

---

## copy-criar
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823` (eliminação de duplicação, criação de CONTEXT.md compartilhado).

## copy-pesquisar
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## copy-revisar
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## copy-swipefile
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## meta-ads
### 1.0.0 — 2026-04-13
- Baseline: pipeline completo (fetch + report) consolidado após refactor `f580823`.

## meta-ads-fetch
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## meta-ads-report
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## meta-ads-trends
### 1.0.0 — 2026-04-13
- Baseline após commit `8eb3ca9` (diagnóstico cruzado, criativos de referência e métricas de vídeo).

## news-pipeline
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## news-pesquisar
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## news-gerar
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## news-revisar
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## trad-pipeline
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## trad-traduzir
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## trad-revisar
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## trad-calibrar
### 1.0.0 — 2026-04-13
- Baseline após refactor `f580823`.

## setup-agencia
### 0.1.0 — 2026-04-13
- Skill nova: guia interativo de primeiro setup (Python, Notion MCP, token Meta) para newbies. Acompanha `meta-ads/SETUP.md` e `meta-ads/scripts/check_setup.py`.

## meta-ads (módulo Python)
### 2026-04-13
- IDs das 6 contas hardcoded em `cache_manager.py` (`ACCOUNTS[*]["account_id"]`); `get_account_id` simplificado. `.env.example` reduzido a token + data + API version (de 36 para ~24 linhas, sem `META_ACCOUNT_*`).
- `scripts/check_setup.py` novo: valida `.env`, expiração do token e acesso a cada uma das 6 contas via `AdAccount.api_get`. Exit 0/1.
