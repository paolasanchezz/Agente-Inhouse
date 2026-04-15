# Changelog

Mudanças relevantes nas skills do Agente Inhouse.

Cada skill é versionada de forma independente, no campo `version` do frontmatter de seu `SKILL.md`. O esquema é semver simplificado:

- **MAJOR** — muda interface (parâmetros, comandos) ou comportamento de forma incompatível.
- **MINOR** — adiciona capacidade preservando compatibilidade.
- **PATCH** — correção, ajuste de tom, refinamento de prompt sem mudar comportamento esperado.

**Como atualizar:** ao alterar uma skill, bumpe a `version` no frontmatter e adicione uma entrada nova na seção da skill correspondente abaixo, no mesmo PR. Datas em ISO (`YYYY-MM-DD`).

---

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
