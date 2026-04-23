# Changelog

Mudanças relevantes nas skills do Agente Inhouse.

Cada skill é versionada de forma independente, no campo `version` do frontmatter de seu `SKILL.md`. O esquema é semver simplificado:

- **MAJOR** — muda interface (parâmetros, comandos) ou comportamento de forma incompatível.
- **MINOR** — adiciona capacidade preservando compatibilidade.
- **PATCH** — correção, ajuste de tom, refinamento de prompt sem mudar comportamento esperado.

**Como atualizar:** ao alterar uma skill, bumpe a `version` no frontmatter e adicione uma entrada nova na seção da skill correspondente abaixo, no mesmo PR. Datas em ISO (`YYYY-MM-DD`).

---

## pull-request-review
### 1.0.1 — 2026-04-23
- **Fix Windows:** `/tmp/` não persiste entre bash calls no Claude Code no Windows (shell state some). Passo 2 agora salva em `reviews/.tmp/` (dentro do repo, persiste).
- **Fix encoding:** Python 3 no Windows usa `cp1252` por padrão em `open()` — quebra ao ler JSON da API com unicode (→, ≤, emojis). Todas as chamadas de `open()` agora passam `encoding='utf-8'` explicitamente.
- **Fix SHA vazio:** `check-runs` chamava a API com `$SHA` vazio porque estava em bash call separado. Agora extração de SHA e call de check-runs ficam no mesmo bash da coleta de meta/files/commits, reusando `$TOKEN`.
- **Novo:** Passo 3.1 — salvar patches em arquivos individuais (`reviews/.tmp/patches/{path}.patch`) pra poder ler via `Read` tool, contornando problema de encoding no stdout do terminal Windows.
- Descoberto durante auto-review do PR #1; memory feedback `feedback_skill_improvement.md` aplicado (bug em skill durante uso → atualizar a skill antes de fechar).

### 1.0.0 — 2026-04-23
- Skill nova `/pull-request-review` para o Victor revisar PRs localmente — recebe URL ou número do PR, coleta diff + metadata + CI status via API do GitHub (reusa token do Git Credential Manager, mesmo padrão do `/commit`), analisa em 3 dimensões (genérico, domain-specific do Agente Inhouse, PR meta) e gera relatório em `reviews/pr-{N}-YYYY-MM-DD.md` com achados em 3 níveis de severidade (🔴 CRÍTICO, 🟡 IMPORTANTE, 🟢 NICE-TO-HAVE).
- Domain-specific checks: skills (frontmatter, CHANGELOG sync, version bump), brand tokens (W3C DTCG), LPs (GUIDELINES, favicon absoluto, 2-3 cores, Cxpress cases pendentes), meta-ads (read-only, sem secrets), conhecimento (duplicação), CLAUDE.md (manter enxuto), CHANGELOG (ISO dates, ordem).
- Relatório local apenas — skill NUNCA posta, aprova, fecha ou mergea o PR. Veredicto automático: Aprovar / Aprovar com ressalvas / Pedir ajustes / Rejeitar.
- Suporta PR de repo externo com degradação graciosa (só roda Dimensão A genérica, avisa que domain checks não aplicam).

## commit
### 2.0.0 — 2026-04-23
- **Reescrita completa do Passo 5 para via única: API direta do GitHub.** Remove dependência de `gh` CLI e remove o fallback via navegador.
- A skill agora extrai o token do **Git Credential Manager** (o mesmo que autentica `git push`) via `git credential fill` com `GIT_TERMINAL_PROMPT=0` e chama `POST /repos/{owner}/{repo}/pulls` via `curl`. Zero cliques, zero dependências externas (nem `gh`, nem navegador).
- Breaking change vs v1.x: Passo 0.3 (detecção de `gh auth`) removido; Passo 5 deixa de bifurcar por `GH_AUTH_OK`. Comportamento anterior via `gh pr create` ou URL compare no browser não existe mais.
- Detecção de PR duplicado mantida via `GET /pulls?head={owner}:{branch}&state=open`; 401/403 aborta com instrução pro usuário abrir PR manualmente (copiando título e body já prontos).
- Mensagem de erro de push auth atualizada pra guiar `git pull` manual (pra o credential helper salvar o token), em vez de `/setup-agencia`.

### 1.0.0 — 2026-04-23
- Skill nova `/commit` para colaboradores entregarem alterações ao Victor sem commitar direto em main.
- Fluxo autônomo: pre-flight checks (repo git, sem rebase/merge pendente, `gh` logado, há algo pra commitar) → inspeção com detecção de arquivos sensíveis (`.env`, credentials, tokens, keys) → branch `claude/{slug}` (infere do path dominante do diff, fallback random estilo `claude/vibrant-elgamal`) → commit PT-BR imperativo → push → `gh pr create` com base=main → retorna URL para revisão.
- Reusa branch atual se já estiver fora da main; aborta limpo se PR já existe (OPEN), se push falha non-fast-forward, se hook pre-commit bloqueia, ou se detecta arquivo sensível.
- Regras invioláveis hardcoded: nunca commita em main, nunca usa `--force`/`--no-verify`/`--amend`, nunca mergea, nunca adiciona `Co-Authored-By`.
- PR body em PT-BR com seções `## Resumo` + `## Arquivos alterados`, sem assinatura de IA.

## setup-agencia
### 0.2.0 — 2026-04-23
- Resumo final (Passo 5) agora menciona `/commit` como comando pós-alterações, com instrução clara de que nunca commita em main.
- Nenhum passo de setup adicional foi introduzido — `/commit` v2.0.0 funciona com a credencial do Git Credential Manager que todos já têm do clone HTTPS.

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
