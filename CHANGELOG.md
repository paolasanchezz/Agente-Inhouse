# Changelog

Mudanças relevantes nas skills do Agente Inhouse.

Cada skill é versionada de forma independente, no campo `version` do frontmatter de seu `SKILL.md`. O esquema é semver simplificado:

- **MAJOR** — muda interface (parâmetros, comandos) ou comportamento de forma incompatível.
- **MINOR** — adiciona capacidade preservando compatibilidade.
- **PATCH** — correção, ajuste de tom, refinamento de prompt sem mudar comportamento esperado.

**Como atualizar:** ao alterar uma skill, bumpe a `version` no frontmatter e adicione uma entrada nova na seção da skill correspondente abaixo, no mesmo PR. Datas em ISO (`YYYY-MM-DD`).

---

## lp-preparar (CONTEXT.md), landing-pages/CONTEXT.md
### 2026-04-28 — Documentação dos guarda-chuvas Buzzmonitor (3 subdomínios) + Cxpress
- Tabela de marcas em `lp-preparar/CONTEXT.md` ampliada: Buzzmonitor agora tem 3 subdomínios guarda-chuva (`evento.*`, `material.*`, `webinar.*`) com convenção de uso por tipo de LP. Cxpress documentado com `content.cxpress.io` (subdomínio único, qualquer tipo de LP).
- `landing-pages/CONTEXT.md` §4.2 ganhou tabela "Guarda-chuvas ativos hoje" com mapping subdomínio→projeto Vercel→LPs ativas, mais regra editorial: LPs novas devem priorizar subdomínio mais específico.
- Argument-hint de `lp-pipeline` e `lp-publicar` atualizado: exemplo agora usa `evento.buzzmonitor.com` (mais alinhado com convenção atual). PageSpeed example em `lp-publicar` Passo 5.1 também atualizado.
- **Comportamento das skills inalterado** — `lp-publicar` Passo 0.5 já era genérico, detecta qualquer guarda-chuva via API Vercel. Mudança é puramente documentacional.
- **Migração concomitante:** LP `vendendo-com-creators` (Buzzcreators, evento presencial) movida de `webinar.buzzmonitor.com` → `evento.buzzmonitor.com`. Redirect 301 ativo no antigo para preservar URLs já compartilhadas. Detalhes em `landing-pages/buzzcreators/vendendo-com-creators/REVISAO.md` Iteração 2.5.

---

## pauta-quente
### 1.0.0 — 2026-04-24
- Skill nova `/pauta-quente` para transformar noticia recente em conteudo multi-formato x multi-idioma por marca. Orientada a evento externo (URL obrigatoria), complementar a `/copy-criar` (standalone).
- Inputs: `[url] [marca] [tipos-csv] [idiomas-csv]`. Tipos: `carrossel`, `video-curto`, `blog`, `linkedin`, `email`. Idiomas: `br` (PT-BR), `pt` (PT-PT), `es` (ES-LATAM). Combinacoes cartesianas tipos x idiomas numa unica execucao.
- Pipeline de 10 passos: parsing -> fingerprint URL (primaria/imprensa-com-fonte/agregador) -> pesquisa expandida ate fonte primaria (ate 3 queries WebSearch quando necessario + 1 query de contexto) -> carregar base de conhecimento (brand + copy + anti-ia + linguistico por idioma) -> definir angulo edutainment + conector com produto -> **gerar pecas** (em memoria) -> **revisao anti-IA pos-geracao dedicada** (varre frases tipicas, filler words, anti-patterns estruturais; corrige em lugar; log em REVISAO-LOG.md) -> salvar local -> publicar Notion (gate: so publica pecas sem `requer-atencao-humana`) -> resumo final.
- Diretrizes editoriais obrigatorias: edutainment (educacao + entretenimento), fontes primarias rastreadas (nunca "noticia da noticia"), conector com produto ao final com feature especifica + beneficio concreto, CTA focado em beneficio por canal.
- Output local em `pauta-quente/{marca}/YYYY-MM-DD-{slug-noticia}/` (pasta raiz nova, versionada, espelhando `newsletter/` e `traducao/`).
- Output Notion em `Entregas > Pauta Quente {Marca} > YYYY-MM-DD — {tema}` com toggles organizados por tipo primeiro, idioma dentro (corte natural para distribuidor por canal). Icon 🔥.
- **Docs novos criados junto:** `conhecimento/copywriting/blog-copy.md` (9 secoes — titulo, estrutura, lead, corpo, fontes, conector, CTA, extensao, checklist) e `conhecimento/copywriting/linkedin-copy.md` (10 secoes — hook, estruturas por tamanho, ritmo visual, storytelling, tom, conector, CTA, hashtags, anti-padroes, checklist). Ambos espelham o padrao de `email-copy.md`.
- Gate automatico: pecas marcadas `revisao: requer-atencao-humana` apos 2 rodadas de revisao ficam so em disco local, nao sao publicadas no Notion — evita vazamento de IA em entrega oficial.

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
### 1.7.0 — 2026-04-28 (consolidacao pos-revisao critica)

Round de fixes a partir de revisao critica das skills LP + CONTEXT/GUIDELINES (3 alta + 5 media + 4 baixa severidade). Foco: eliminar contradicoes, deduplicar regras espalhadas, fonte unica para regras canonicas (cascata GTM, snippet GTM, anti-padroes, wrapper CSS form).

#### Alta severidade (bugs reais)
- **`landing-pages/CONTEXT.md` §5.1:** documentar explicitamente que `lp-gerar` pula o passo 2 da cascata (HTML ainda nao existe) — antes essa diferenca nao estava em lugar nenhum, gerava confusao entre lp-gerar (2 passos) vs lp-revisar (3 passos).
- **`landing-pages/CONTEXT.md` §3.7 (validacao favicon):** `curl` de exemplo trocou `{path}` (variavel inexistente — favicon resolve em `/` absoluto) por paths corretos solo (`/assets/logos/...`) e guarda-chuva (`/assets/{marca}/logos/...`).
- **`landing-page` (advisor) v1.1.0 → v1.2.0:** Q1 reduzida de 7 → 3 opcoes (LP nova / Alterar / Etapa especifica) — AskUserQuestion suporta no maximo 4. Q1b expande "Etapa especifica" se necessario. Fluxo: Alterar agora delega decisao fina a `landing-pages/CONTEXT.md` §2.2 em vez de duplicar a tabela.

#### Media severidade (deduplicacao)
- **Cascata de regiao centralizada em `landing-pages/CONTEXT.md` §5.1.** Removida de `lp-gerar` e `lp-revisar` (substituida por ref) e do brand CONTEXT (`.claude/skills/lp-preparar/CONTEXT.md`). Antes vivia em 4 lugares — qualquer mudanca exigia atualizar 4 arquivos com risco de divergir.
- **Snippet GTM canonico em `landing-pages/CONTEXT.md` §5.3.** Removido de `lp-gerar` Passo 3 (briefing) e `lp-revisar` Passo 3.5. Skills agora apontam pro snippet em §5.3. Se Google atualizar o snippet, 1 lugar pra atualizar.
- **Wrapper CSS `.form.jotform-embed` so em `lp-integrar-form` Passo 3.** Removido de GUIDELINES §10 e do brand CONTEXT — esses agora referenciam.
- **Anti-padroes consolidados em `landing-pages/CONTEXT.md` §7** (categoria + historico). `lp-publicar` substituiu sua lista propria por referencia a §7.1. CONTEXT §2.3 (anti-padroes de fluxo) tambem virou ref para §7.1.
- **Fluxo de alteracao alinhado:** `landing-page` advisor agora delega 100% a `landing-pages/CONTEXT.md` §2.2 (matriz canonica de 11 linhas) em vez de manter tabela propria com 6 categorias incompletas.

#### Baixa severidade (polish)
- **Adicionada `landing-pages/CONTEXT.md` §5.2 — ownership chain:** `lp-gerar` injeta inicial, `lp-revisar` audita+corrige, `lp-publicar` valida no live. Antes essa cadeia ficava implicita em 3 SKILL.md sem visao consolidada.
- **PageSpeed endpoint movido** do brand CONTEXT (.claude/skills/lp-preparar/CONTEXT.md) — so `lp-publicar` Passo 5.1 usa, ja tinha duplicado la. Brand CONTEXT e shared entre todas skills lp-* — endpoint de validacao pos-deploy nao pertencia ali.
- **Brand CONTEXT "Pasta sibling" atualizada** pra refletir solo + guarda-chuva (antes so descrevia formato solo `{marca}-lp-{slug}/` — desatualizado desde lp-publicar v1.5.0). Detalhes operacionais redirecionam pra `landing-pages/CONTEXT.md` §4.
- **Refs "CONTEXT.md" agora sempre com path completo** nas skills lp-* (`landing-pages/CONTEXT.md` ou `.claude/skills/lp-preparar/CONTEXT.md`). Tira ambiguidade entre os dois CONTEXT.

#### Skills bumpadas
- `lp-gerar` 1.3.0 → 1.4.0 (cascata removida, snippet GTM removido, ref pro CONTEXT §5.1/§5.3)
- `lp-revisar` 1.2.0 → 1.3.0 (idem)
- `lp-publicar` 1.6.0 → 1.7.0 (anti-padroes removidos, ref pro CONTEXT §7)
- `landing-page` (advisor) 1.1.0 → 1.2.0 (Q1 enxuta, Fluxo Alterar delegado)
- Brand CONTEXT (`.claude/skills/lp-preparar/CONTEXT.md`) — sem campo version, mas reescrita

#### Skills nao tocadas neste round
- `lp-preparar` (carga ja correta em 1.1.0)
- `lp-integrar-form` (carga ja correta em 1.2.0; agora e fonte canonica do wrapper CSS)
- `lp-pipeline` (carga ja correta em 1.1.0)

### 1.6.0 — 2026-04-28
- **Novo `landing-pages/CONTEXT.md`** — runbook operacional unificado para todas as skills lp-*. Cobre: mapa mental (fonte-verdade vs sibling), fluxo padrao de LP nova, **matriz de alteracao pós-deploy** (§2.2 — "o que mudou → o que rodar", endereça problema recorrente do Victor de não saber qual skill rodar quando pede ajuste numa LP já viva), convenção unificada de assets/imagens (brand vs LP-local, paths source vs deploy, namespace solo vs guarda-chuva, formatos por tipo, regra do favicon, mascotes por marca), modos de deploy, cascata de detecção de região (deduplicada — antes em 3 skills), **troubleshooting** (sintoma → causa → solução cobrindo favicon 404, mascote 404, colisão de assets, CSP bloqueando form, GTM ausente/errado, FetchError CLI, smoke test divergente, sibling apagada/divergente, vazamento de path interno, conflito de domínio), anti-padrões documentados (linkados aos incidentes que motivaram cada versão), checklist pré-deploy, quando-não-usar-este-pipeline, e referências cruzadas. Complementar a `landing-pages/GUIDELINES.md` (que segue como regras de **design** — paleta, hero, motion, copy, seções-tipo, favicon §11). CONTEXT cobre o "como operar"; GUIDELINES cobre o "como deve ser".
- **Skills bumpadas** (todas adicionam `landing-pages/CONTEXT.md` ao Passo 0/1 de carga de insumos):
  - `lp-preparar` 1.0.0 → 1.1.0
  - `lp-gerar` 1.2.0 → 1.3.0
  - `lp-revisar` 1.1.0 → 1.2.0
  - `lp-integrar-form` 1.1.0 → 1.2.0
  - `lp-publicar` 1.5.0 → 1.6.0
  - `lp-pipeline` 1.0.0 → 1.1.0 (novo bloco "Contexto comum" que carrega GUIDELINES + CONTEXT antes da validação de argumentos; e detecção de pedido de alteração vs LP nova com redirect para CONTEXT.md §2.2)
  - `landing-page` (advisor) — adicionado `version: 1.1.0` ao frontmatter (não tinha versionamento antes); nova opção "Alterar LP existente" no Q1 + novo Fluxo: Alterar com sub-pergunta sobre o que mudou (copy/visual/asset/form/tracking/dominio) que dispara a skill correta conforme a matriz §2.2 do CONTEXT
- **Motivo (do Victor):** "toda vez que peço alterações numa LP, o agente tem dificuldade em deploy correto, em qual passo seguir quando é alteração, e em tratar imagens (logos, ilustrações, onde guardar, como evitar 404)". A exploração confirmou que a base é sólida mas o conhecimento operacional estava disperso em 6 SKILL.md + CHANGELOG + READMEs por LP. Agora 1 doc canonico e carregado pelas 6 skills cobre fluxo de alteração, assets e troubleshooting num lugar só.
- **Não-mudancas (intencionais):** `landing-pages/GUIDELINES.md` segue identico (regras de design não mudaram). `.claude/skills/lp-preparar/CONTEXT.md` segue como compartilhado para convenções de marca/IDs Notion (papel diferente do CONTEXT operacional recém-criado). LPs existentes em `landing-pages/{marca}/{slug}/` não foram tocadas. `brand/` não tocado.

### 1.5.0 — 2026-04-27
- `lp-publicar` (v1.5.0): novo **modo guarda-chuva** para LPs que compartilham domínio. Quando `[dominio]` é fornecido, o **Passo 0.5** consulta a API da Vercel (`GET /v9/projects?teamId=...`) checando se algum projeto já tem esse domínio nos aliases. Se sim, a skill anexa a LP nova como subpasta do sibling existente em vez de criar projeto novo. Comportamento default (modo solo) inalterado.
- **Namespace de assets por marca em multi-LP:** no modo guarda-chuva, paths são reescritos para `/assets/{marca}/X` em vez de `/assets/X`, evitando colisão de filename entre marcas (ex: Buzzmonitor e Buzzcreators têm ambos `logo-icon.png`). Source pode usar `../../brand/{marca}/...` ou `./assets/...` que a skill faz a conversão correta.
- **Validação de regressão zero (§2.4 + §3.4.b):** antes do deploy guarda-chuva, capture-se hash MD5 do `index.html` de cada LP vizinha (baseline). Pós-deploy, smoke test refaz o hash via URL pública — qualquer divergência aborta o relatório (algo da entrega quebrou vizinhas, investigar antes de publicar).
- **Não-sobrescrever `vercel.json` e `README.md` em modo guarda-chuva (§1.6 + §1.8):** o sibling já está configurado para multi-LP; sobrescrever pode mudar CSP/headers e quebrar form/script de vizinhas. Skill compara com template e avisa em vez de aplicar silenciosamente.
- **Anti-padrões documentados:** nova seção no fim do SKILL.md tabula 5 anti-padrões com motivo e quando aconteceram (criar projeto duplicado em vez de guarda-chuva, sobrescrever vercel.json, copiar asset com filename igual sem namespace, path relativo sobrando, misturar entregas no mesmo deploy).
- **Incidente que motivou:** 2026-04-27, LP Buzzcreators `vendendo-com-creators` foi inicialmente publicada em projeto Vercel separado (`buzzcreators-lp-vendendo-com-creators`) em vez de usar o guarda-chuva já existente para `webinar.buzzmonitor.com` (`buzzmonitor-lp-monitoramento-concorrentes`). Consolidação manual + 2 deploys + projeto órfão. v1.5.0 evita o cenário desde a primeira execução.

### 1.4.0 — 2026-04-27
- `lp-publicar` (v1.4.0): §1.3-1.5 reescritos para suportar **assets LP-locais** além de assets do `brand/`. Antes, §1.4 só sabia copiar de `brand/{marca}/assets/` — assets em `landing-pages/{marca}/{slug}/assets/` (ex: mascot específico de uma LP) não eram copiados ao sibling, e o redeploy quebrava. Agora classifica cada referência por padrão (`../../brand/...` → brand, `./assets/...` → LP-local, `/assets/...` → checa brand primeiro, senão LP-local) e copia da origem certa. §1.5 ganhou verificação obrigatória pós-rewrite (grep por `../assets/`, `./assets/`, `../../brand/` remanescente — se sobrar, aborta).
- **Fix:** LP `buzzmonitor/monitoramento-concorrentes-maio-2026` (BR + PT) com mascot.png 404 no live — caminho relativo `./assets/mascot.png` resolvendo para `/assets/mascot.png` (raiz vazia) por causa de `cleanUrls: true` + `trailingSlash: false` no Vercel. Path corrigido para absoluto, mascot levado pro sibling root e redeployado.

### 1.3.0 — 2026-04-23
- `lp-revisar` (v1.1.0): novo **Passo 3.5 — Auditoria de GTM (CRITICO)**. Resolve regiao via cascata (sufixo slug `-pt`/`-latam`/`-br` → `<html lang>` → fallback `brasil`), resolve GTM esperado em `tracking.json` e audita os 2 snippets no HTML. GTM ausente ou com ID errado vira CRITICO e eh corrigido automaticamente no Passo 4; caso "tracking.json null mas LP tem GTM" vira MELHORIA em `REVISAO.md`.
- `lp-gerar` (v1.2.0): Passo 1 agora detecta regiao explicitamente por cascata (sufixo slug → fallback `brasil`). Antes dependia de "briefing ou CTX regional", sem mecanismo deterministico — motivo pelo qual LPs PT recebiam GTM BR.
- `lp-integrar-form`: nota em `## Notas` delega auditoria de GTM para `lp-revisar` (Passo 3.5). Skill continua focada so em trocar form mock por embed real, sem auditoria duplicada.
- **Tracking.json atualizado com IDs reais por regiao:**
  - Buzzmonitor: BR `GTM-WFJVK858` (ja existia), LATAM `GTM-MKQBX2MG` (novo), PT `GTM-NCFT22CW` (novo).
  - Cxpress: BR `GTM-T4XDWHL3`, LATAM `GTM-WRQ47B9R`, PT `GTM-NW6V5KBM` (antes tudo `null`).
- **Cascata de deteccao de regiao documentada em CONTEXT.md:** sufixo do slug → `<html lang>` → fallback `brasil`. Fonte unica usada por `lp-gerar` e `lp-revisar`.
- **Fix:** LP `buzzmonitor/monitoramento-concorrentes-maio-2026-pt` estava com GTM BR (`GTM-WFJVK858`) em vez de PT (`GTM-NCFT22CW`) — bug causado pela regiao implicita antes desta versao. Trocado nos 2 lugares (script e noscript).

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
### 1.1.0 — 2026-04-27
- **Novo Passo 4.5 obrigatório — re-revisão sobre as próprias correções.** Disparado por feedback do Victor após revisão da Copy LP do evento Vendendo com Creators (Buzzcreators), onde a v2 publicada no Notion vazou 3 padrões de IA introduzidos *durante* a correção: (a) antítese-por-negação ("X, não Y") repetida 6× em ~400 palavras, (b) 6 em-dashes de ênfase em texto que tinha zero, (c) substitutos decorativos no lugar dos fillers removidos ("planilha mágica", "com achismo" para "de forma clara").
- O Passo 4.5 roda 4 contagens no texto **corrigido**: antítese-por-negação (max 2 / peça), **em-dash (tolerância zero — qualquer `—` no output vaza IA)**, substitutos decorativos (filler 2.0 — palavras que dão ritmo sem trazer info), ritmo sintático repetitivo (2+ frases consecutivas com mesma forma).
- Causa-raiz documentada: a skill antes terminava em "aplicar correções → apresentar resultado", sem loop sobre o output. Os erros de IA mais previsíveis são introduzidos *durante* o conserto (especialmente quando o revisor tenta dar "punch" no lugar de filler removido).
- Atualização paralela em `conhecimento/editorial/regras-anti-ia.md`: nova seção "Estruturas Viciadas" com 3 sub-regras (antítese-por-negação, **em-dash com tolerância zero**, filler 2.0); regra "de forma X" adicionada à lista de filler words; "Teste Final de Naturalidade" agora inclui re-checagem pós-correção como obrigatória; "Não é X, é Y" tirado da lista de frases (era específico demais) e absorvido pela nova regra estrutural mais ampla.
- **Em-dash com tolerância zero (decisão do Victor 2026-04-27):** "nenhum ser humano usa isso". Regra ficou absoluta — Ctrl+F por `—` no texto final, esperado 0 ocorrências. Substitutos: vírgula (pausa curta), ponto (pausa forte), parênteses (aparte), nova linha (atribuição de citação). Única exceção é separador de seção markdown `---` (três hifens, vira `<hr>`, não é em-dash).

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
