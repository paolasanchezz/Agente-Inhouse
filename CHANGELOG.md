# Changelog

Mudanças relevantes nas skills do Agente Inhouse.

Cada skill é versionada de forma independente, no campo `version` do frontmatter de seu `SKILL.md`. O esquema é semver simplificado:

- **MAJOR** — muda interface (parâmetros, comandos) ou comportamento de forma incompatível.
- **MINOR** — adiciona capacidade preservando compatibilidade.
- **PATCH** — correção, ajuste de tom, refinamento de prompt sem mudar comportamento esperado.

**Como atualizar:** ao alterar uma skill, bumpe a `version` no frontmatter e adicione uma entrada nova na seção da skill correspondente abaixo, no mesmo PR. Datas em ISO (`YYYY-MM-DD`).

---

## lp-publicar, setup-agencia (+ docs LP)
### 2026-05-07 — Sync sibling via Vercel API + LP `webinar-tecnologia-maio2026` recuperada (lp-publicar v3.1.0, setup-agencia v0.5.0)

Hardening de modo guarda-chuva apos **incidente real** que apagou `/livraria` da production por ~2h. Causa-raiz: deploy feito de maquina sem `livraria/` na sibling local, `BASELINES_OTHERS` (Passo 2.4) vazio, smoke test 3.4.b iterou sobre lista vazia e nao detectou regressao. Production foi substituida por snapshot que tinha apenas `playbook-whatsapp2026` + LP nova.

**O fluxo da correcao em 1 sessao:**
1. Investigacao do 404 reportado pelo Victor leva ao deploy `dpl_3rKKvvAfdinBXbQB1MeFFdJP51Au` (criado ~11h, 1.35h antes do diagnostico).
2. Plano: hardenizar `lp-publicar` com sync via Vercel API antes de modificar sibling.
3. Implementacao do Passo 0.5.d.
4. Primeiro teste em producao (`/lp-publicar cxpress livraria content.cxpress.io`): sync baixa playbook + webinar do live, sibling local mantem livraria, deploy preserva as 3 LPs. **livraria restaurada com sucesso**.
5. 4 bugs descobertos durante o teste foram corrigidos no mesmo PR.
6. LP `webinar-tecnologia-maio2026` recuperada do live pro repo (estava no Vercel mas sem source — foi publicada de outra maquina sem commit).

- **lp-publicar 3.0.0 → 3.1.0 (MINOR — capacidade nova retro-compat)**:
  - **Novo Passo 0.5.d "Sync sibling com ultimo deploy production"** entre 0.5.c e Passo 1, executado SO em modo guarda-chuva.
  - **0.5.d.i**: resolve `VERCEL_TOKEN` em 4 camadas — env var > `.env.local` no CWD > `.env.local` no repo principal (suporta worktrees via `git rev-parse --git-common-dir`) > parse de `auth.json` do CLI Vercel (sempre em `com.vercel.cli/Data/auth.json`, com `/Data/` no meio do path; cross-platform Linux/macOS/Windows). Token resolvido **sempre validado** via `curl /v2/user` antes de usar — descarta tokens expirados que o CLI renova internamente mas a API REST direta nao tem fallback.
  - **0.5.d.iii**: logica de download recursivo extraida pra arquivo helper `.claude/skills/lp-publicar/sync_sibling.py` (em vez de heredoc Python inline na skill). Heredoc combinado com escape de backslash em paths Windows + redirecionamento de stdin gerava bugs sutis. Script externo isola tudo, le env vars com `os.environ`, da pra testar isolado.
  - **0.5.d.iv**: validacao pos-sync cruza slugs vivos no dominio (curl 200) com `landing-pages/{*}/{*}/` no repo. Se algum slug vivo NAO esta na sibling pos-sync, aborta com mensagem clara — sem isso, deploy apagaria a vizinha.
  - **Edge case re-publicacao**: se o slug atual ja existe na sibling pos-sync, deixa — Passo 1.2 sobrescreve com a versao do source.
  - **Passo 0.1**: tambem ganhou fallback worktree pro `.env.local` (mesma logica do 0.5.d.i).
  - **Comentarios em 2.4 e 3.4.b**: explicitando 3 camadas de defesa (sync, baseline, smoke test).
  - Sem mudanca em interface, args ou comandos invocaveis.

- **setup-agencia 0.4.0 → 0.5.0**:
  - **Novo Passo 4.5 "Vercel API token (opcional)"** depois de 4.4. Recomendado pra colaboradores que vao publicar em guarda-chuva. Pulavel — fallback continua sendo `auth.json` do CLI.
  - Novo fallback `vercel-token-falhou` (mensagem hardcoded com instrucao manual).

- **`.claude/skills/lp-publicar/sync_sibling.py` (NOVO)**: script helper invocado pelo Passo 0.5.d.iii. Le env vars (`DEPLOY_ID`, `ORG_ID`, `VERCEL_TOKEN`, `SIBLING`), faz GET na arvore de arquivos do deploy, baixa cada folha via V7 e grava em `$SIBLING/`. Descarta o wrapper top-level `src/` que o Vercel envelopa.

- **landing-pages/CONTEXT.md** (sem bump — so doc):
  - §4.3 reescrita pra explicitar 3 camadas de defesa (sync, baseline, smoke test) e referenciar §7.2.
  - §6 (Troubleshooting): 2 linhas novas — "vizinhas viraram 404" e "Sync incompleto".
  - §7.2 (Historico): linha 2026-05-07 documentando o **incidente real** (livraria apagada e restaurada na mesma sessao via v3.1.0) + recuperacao da LP webinar.

- **`landing-pages/cxpress/webinar-tecnologia-maio2026/` (NOVA)**: source recuperado do live (deploy production atual). Contem `index.html` (~42KB) + `README.md` documentando origem + debito tecnico (sem `copy.txt`, sem `REVISAO.md`). Paths revertidos de absolutos (`/assets/...`) pra padrao source (`../../brand/cxpress/assets/...`).

- **`.env.local.example`**: nova secao "Vercel API (opcional)" documentando `VERCEL_TOKEN` e como gerar.

### 2026-05-04 — `.env.local` central + auto-invoke setup-agencia em fallback (v3.0.0)

Iteração de DX em cima da v2.0.0. Reduz precedência de `SIBLING_BASE` de 4 caminhos para 2, elimina branching do sanity check OneDrive/iCloud (vira responsabilidade do setup-agencia) e fecha o loop entre as skills: se config falta, lp-publicar invoca setup-agencia automaticamente.

- **`.env.local.example` (novo, raiz, versionado)**: template KEY=VALUE com `LP_SIBLING_BASE`. Documento auto-explicativo do formato pra colaboradores. Por enquanto só essa chave; preparado pra crescer com outras configs cross-skill per-máquina.

- **`.env.local` (gitignored)**: arquivo real escrito pelo setup-agencia. Substitui o `landing-pages/.lp-config.local.json` da v2.0.0 (removido do `.gitignore`).

- **lp-publicar 2.0.0 → 3.0.0 (MAJOR — comportamento muda)**:
  - Passo 0.1 simplificado de 4 caminhos → 2: env var `LP_SIBLING_BASE` no shell > linha em `.env.local`. Fim do fallback "parent-do-repo + sanity check OneDrive/iCloud/Dropbox" (v2.0.0). Config é responsabilidade do setup-agencia.
  - **Auto-invoke setup-agencia em fallback**: se nem env var nem `.env.local` resolverem, lp-publicar usa o tool `Skill` para invocar `setup-agencia` com argumento `"so lp"`, espera ele escrever `.env.local`, e re-resolve. Loop fechado, zero "rode X primeiro depois volte".
  - `allowed-tools` ganhou `Skill` para o auto-invoke acima.
  - **Migração necessária**: colaboradores existentes (Victor) precisam rodar `/setup-agencia` uma vez em modo `"so lp"` pra criar `.env.local`. Sem isso, primeira chamada de `/lp-publicar` automaticamente dispara o setup. Sem quebra silenciosa — só uma pergunta extra na primeira vez.

- **setup-agencia 0.3.0 → 0.4.0**:
  - Passo 4.4 reescrito: ao invés de instruir o user a rodar `setx`/`export` no shell (com fricção cross-platform: reabrir terminal, escolher entre bashrc/zshrc/etc), agora pergunta o path com `AskUserQuestion` (sugerindo parent-do-repo se não for sync-watched) e escreve `.env.local` direto via `Write`/`Edit`.
  - Validação de path: rejeita pasta dentro do repo, dentro de OneDrive/iCloud/Dropbox; pede outra.
  - Novo fallback `lp-sibling-falhou`.

- **landing-pages/CONTEXT.md §1**: precedência atualizada para 2 caminhos. Menciona auto-invoke do setup-agencia.

- **lp-preparar/CONTEXT.md** (sem bump — só doc): atualizada referência de precedência.

- **landing-pages/cxpress/livraria/README.md**: instrução manual de cópia atualizada para ler `.env.local` em vez do fallback `${LP_SIBLING_BASE:-../}` da v2.0.0. Mensagem clara "rode /setup-agencia primeiro" se faltar.

- **`.gitignore`**: substituído `landing-pages/.lp-config.local.json` por `.env.local`.

- **Motivação de DX**: o ponto crítico do Victor depois da v2.0.0 era que cada execução de `/lp-publicar` recomputava o ambiente (`git rev-parse` + `dirname` + sanity check). Custo em tokens marginal mas a complexidade era real — 4 caminhos pra entender e debugar. v3.0.0 troca essa complexidade por um arquivo de config persistente, mais alinhado com `meta-ads/.env` que já existe há tempo.

---

## news-gerar, news-revisar, template-newsletter.md, estilo-newsletter.md
### 2026-05-04 — Enxugamento + pergunta-eixo INTERNA (v2.1.0)

Feedback do Victor pos primeiro teste end-to-end com Cxpress BR: NL "muito grande, estrutura feia". Pediu reducao pela metade dos caracteres + remocao da pergunta-eixo do output visivel ("deixe como algo interno, que so nos vemos na hora de construir, mas que nao aparece de forma explicita para o cliente").

- **news-gerar 2.0.0 → 2.1.0**:
  - Limite do corpo: ≤600 → **≤300 palavras**
  - Bloco "## A pergunta da semana" no template **REMOVIDO** — pergunta-eixo agora vive como comentario HTML interno no topo do arquivo local (`<!-- Pergunta-eixo (planejamento interno, NAO publicar): "..." -->`) e em `dor-semana.md`. NUNCA aparece como bloco visivel ao leitor.
  - Mini-blocos da resposta encurtados: 95-115 → 35-55 palavras cada (total 110-170 vs 280-340 antes)
  - Abertura encurtada: 40-60 → 30-50 palavras
  - "Mais pra explorar": 1-2 bullets → 1 bullet (15-25 palavras)
  - Estrutura visivel: 2 blocos obrigatorios (Abertura + Resposta em capitulos) + 3 opcionais (era 3 obrigatorios + 3 opcionais)

- **news-revisar 2.0.0 → 2.1.0**:
  - Validar limite ≤300 palavras no corpo
  - Adicionar checagem: pergunta-eixo **NAO** aparece como bloco visivel (sem `> ## A pergunta da semana`, sem callout/blockquote com a pergunta literal). Se aparecer, REMOVER e absorver no assunto/abertura
  - Atualizar criterios de aprovacao

- **template-newsletter.md** (em news-gerar):
  - Reescrito conforme nova anatomia
  - Bloco "Pergunta da semana" removido como elemento visivel — vira nota explicativa de que a pergunta-eixo e elemento INTERNO de planejamento

- **conhecimento/editorial/estilo-newsletter.md**:
  - Anatomia atualizada: 2 blocos obrigatorios + 3 opcionais (em vez de 3 + 3)
  - Limite ≤300 palavras no corpo
  - Checklist atualizada: "Pergunta-eixo NAO aparece como bloco visivel"

- **Cxpress 2026-W19** (newsletter ja gerada): reescrita do corpo aplicando v2.1.0 (~376 → ~185 palavras), bloco da pergunta-eixo removido, Notion atualizado via `notion-update-page` (`replace_content`).

- **Sem mudanca em**: news-pesquisar (continua gerando `dor-semana.md` com a pergunta-eixo), news-pipeline, news-criar-post.

---

## news-* (familia) + estilo-newsletter.md + CLAUDE.md
### 2026-05-04 — Newsletter semanal noticiosa com eixo no blog proprio (v2.0.0)

- **Migracao da familia news-* de 5 NLs/mes formato campanha → 1 NL/semana formato curadoria editorial.**
- **Feedback de origem:** Alessandro (socio) leu as 4 NLs do mes e disse "esta com muita cara de campanha de email marketing", pediu formato mais noticioso, 90% conteudo do blog proprio (oportunidade de revisar centenas de posts antes de divulgar), 10-20% clipping de imprensa, foco em dores, linguagem jornalistica e direta, sugestao de "uma pergunta por edicao", edutainment (educacao + entretenimento). Benchmark: a propria newsletter Buzzmonitor.

- **news-pesquisar 1.0.0 → 2.0.0 (MAJOR):**
  - Foco totalmente reorientado: mapear dores (BRANDBOOK §Publico-Alvo) + indexar blog proprio em profundidade + clipping PR (mencoes da marca em imprensa, data ≤ 7 dias).
  - Removidos da news: noticias gerais de mercado e analise de concorrentes (concorrentes.md preservado para outras skills).
  - Cache cumulativo `conhecimento/produto/{brand}/blog-cache.md` indexa posts ja conhecidos (nao deleta entre semanas).
  - Versionamento de pasta: `pesquisa/atual/` (semana corrente) + `pesquisa/arquivo/YYYY-WW/` (historico).
  - Novos outputs: `dores-candidatas.md`, `indice-blog.md`, `dor-semana.md`, `pauta-sugerida.md` (condicional), `clipping-pr.md`, `RESUMO.md`.
  - Detecta lacuna: dor com cobertura <3 posts gera pauta sugerida.
  - Argumento `foco` removido (era engessante).

- **news-criar-post 1.0.0 (NOVO):**
  - Skill manual-trigger invocada pelo `news-pipeline` apos aprovacao explicita da pauta.
  - Le `pesquisa/atual/pauta-sugerida.md`, escreve post completo (1500-2500 palavras) seguindo `conhecimento/copywriting/blog-copy.md` com edutainment + tom jornalistico.
  - Salva local em `newsletter/{brand}/posts-sugeridos/post-{slug}-{semana}.md` e publica draft no Notion sob `Entregas > Drafts de Blog > {Marca} > [{semana}] {H1}`.
  - Atualiza `dor-semana.md` adicionando o novo post como ancora 1, e `_state.json` registrando a pauta consumida.
  - Time editorial revisa, publica no blog real e atualiza dor-semana.md com URL final antes do disparo da news.

- **news-gerar 1.0.0 → 2.0.0 (MAJOR):**
  - Output: 1 NL em `newsletter/{brand}/entregas/newsletter-{semana}.md` (sem subpasta YYYY-WW — direto na pasta `entregas/`).
  - Le `dor-semana.md`, `clipping-pr.md`, `_state.json` e (se existir) swipe-file Buzzmonitor.
  - Estrutura nova: 3 blocos obrigatorios (Abertura jornalistica + Pergunta da semana + Resposta em capitulos) + 3 opcionais (Mais pra explorar + Na imprensa + Bloco extra).
  - Limites: ≤600 palavras no corpo, 3-6 links contextuais (≥3 blog proprio, ≤1 clipping, ≤1 extra).
  - Notion: 1 pagina por edicao (nao toggle), titulo `[{semana}] {Assunto}`.
  - Atualiza `_state.json` com pergunta-dor e links da edicao para dedupe (6 semanas pergunta, 4 semanas links).

- **news-revisar 1.0.0 → 2.0.0 (MAJOR):**
  - Argumento `[todas|N]` removido (sempre 1 NL).
  - Novas validacoes: ≥3 links blog proprio, 3-6 links totais, ≤1 clipping PR, ≤1 extra, 0 noticias gerais de mercado, dedupe vs `_state.json`.
  - Linguagem jornalistica: rejeita aberturas "imagine que...", "no mundo atual...", frases medias ≤22 palavras.
  - Tom nao-vendedor: max 1 mencao a marca fora dos links de blog; alerta se >40% links forem para dominio proprio fora do blog.
  - Edutainment: cada mini-bloco da resposta valida ter analogia, dado, exemplo ou definicao.
  - Limite mantido em 600 palavras (corpo).

- **news-pipeline 1.0.0 → 2.0.0 (MAJOR):**
  - Novo fluxo: pesquisa → (pausa explicita: aprovar pauta sugerida?) → news-criar-post (se aprovada) → news-gerar → news-revisar.
  - Argumento `foco` removido.
  - Adicionada nota de cadencia semanal (loop ou schedule).
  - Relatorio final consolida estado da edicao + draft de blog (se houver) + pendencias do time editorial.

- **template-newsletter.md (em news-gerar):** reescrito completo. Estrutura espelha a anatomia: Abertura jornalistica (40-60 palavras) + Pergunta da semana (15-20 palavras em destaque) + Resposta em tres tempos (3 mini-blocos, 280-340 palavras, 3 links) + opcionais.

- **conhecimento/editorial/estilo-newsletter.md (in-place):**
  - Referencia de estilo: YouScan → newsletter oficial Buzzmonitor (com pointer para swipe-file a popular com amostras reais).
  - Adicionadas secoes: Anatomia da newsletter semanal, Linguagem jornalistica e direta, Edutainment, Criterios de selecao de post proprio, Criterios de clipping PR, Bloco extra (sem cadencia fixa).
  - Demovidos: "Tipos de Gancho (10 tipos)" → "Aberturas jornalisticas (referencia opcional)" — tipos viram inspiracao para abertura curta, nao eixo da NL. "Tipos de CTA" → removido (sem cadencia fixa).
  - Checklist pre-publicacao reescrita.

- **CLAUDE.md:** fluxo `Newsletters` atualizado (inclui pausa de aprovacao + news-criar-post). Tabela de comandos news-* expandida (5 comandos). Nota de cadencia semanal via `/loop` ou `/schedule`.

- **Conhecimento sustentado:** `conhecimento/copywriting/swipe-file/buzzmonitor-newsletter.md` sera populado com 3-5 edicoes reais da newsletter Buzzmonitor (Victor envia). Sem o swipe, news-gerar usa fallback editorial baseado em estilo-newsletter.md.

- **Migracao:** sem modo legacy. Pesquisas e entregas mensais antigas ficam em `entregas/YYYY-MM/` e `pesquisa/arquivo/` como historico. Primeira execucao da v2.0 cria `entregas/newsletter-{semana}.md`, `_state.json` zerado e `blog-cache.md` zerado.

- **BREAKING:** argumento `foco` removido de news-pipeline e news-pesquisar; argumento `[todas|N]` removido de news-revisar; pesquisa nao gera mais `noticias-mercado.md` nem `analise-concorrentes.md` para a news.

- Plano de implementacao em `~/.claude/plans/n-s-rodamos-a-skill-eventual-token.md`.

---

## lp-publicar, lp-preparar, setup-agencia, landing-pages/CONTEXT.md
### 2026-05-04 — Cross-platform: paths sibling e auth Vercel parametrizados

- **lp-publicar 1.7.0 → 2.0.0 (MAJOR — comportamento muda por máquina):**
  - Novo Passo 0.1: `SIBLING_BASE` resolvido em runtime em ordem de precedência: env var `LP_SIBLING_BASE` > `landing-pages/.lp-config.local.json` (campo `siblingBase`, gitignored) > pasta-mãe do repo (`dirname(git rev-parse --show-toplevel)`). Sanity check aborta se default cair em pasta sync-watched (OneDrive/iCloud/Dropbox/node_modules/.git/worktrees) — exige `LP_SIBLING_BASE` explícita.
  - Passo 0.5 reescrito em 3 sub-passos: pre-flight do CLI Vercel (`vercel --version` + `vercel whoami --scope $TEAM`, abortando com erro claro se faltar instalação ou auth), detecção de guarda-chuva via `vercel alias ls` + awk (CLI cuida de auth internamente — zero dependência de filesystem cross-platform), garantia de `.vercel/project.json` no sibling de guarda-chuva (auto-link via `vercel link` se ausente — destrava primeira execução em outra máquina).
  - **Por que `alias ls` em vez de `curl + Python lendo auth.json` (escolha original do plano):** verificação descobriu que Python da Microsoft Store (caso comum no Windows) roda em sandbox AppContainer e não consegue acessar paths absolutos em `AppData/Roaming/`, mesmo com paths corretos. Validado: `Path('auth.json').exists()` no CWD = True; `Path(os.environ['APPDATA']) / '...'` = False. Pivot para CLI nativo elimina toda essa categoria de bug. Bônus: `alias ls` cobre o caso "domínio atribuído mas projeto sem deploy custom-domain" (cenário "guarda-chuva em popularização" — `material.buzzmonitor.com` hoje), que `vercel projects ls` não pega.
  - Removidas todas as menções a `C:/Users/titof/Downloads/Claude/{nome}/` no SKILL.md (substituídas por `${SIBLING_BASE}/{nome}/`).
  - Removida a leitura direta de `$APPDATA/com.vercel.cli/Data/auth.json` (Windows-only e quebrava com Python sandboxed).
  - **Migração para Victor:** comportamento default (parent-do-repo) já bate com o setup atual (`Downloads/Claude` é o parent de `Agente Inhouse/`). Verificação end-to-end confirmou que SIBLING_BASE resolve igual ao path antes hardcoded. Nenhuma ação necessária.

- **lp-preparar 1.1.0 → 1.2.0:**
  - Tabela "Projetos Vercel correspondentes" no `CONTEXT.md` perdeu coluna "Sibling local" (derivada em runtime, era redundante). Restaram subdomínio + projeto Vercel.
  - Seção "Pasta sibling (deploy artifact)" agora documenta `${SIBLING_BASE}/{nome}/` em vez de path absoluto.

- **landing-pages/CONTEXT.md:**
  - §1 (Mapa mental): adicionada linha sobre resolução de `SIBLING_BASE` em runtime.
  - §4.1, §4.2, §6 (troubleshooting): paths absolutos `C:/Users/titof/...` substituídos por `${SIBLING_BASE}/...`.

- **setup-agencia 0.2.0 → 0.3.0:**
  - Passo 1.2 ganhou opção 5 — "Landing Pages (/landing-page)" — que dispara o novo Passo 4.
  - Novo **Passo 4** (Vercel CLI) com sub-passos: validar CLI via `npx vercel --version`, login via `npx vercel login`, validar org com `vercel whoami --scope team_nC991VqUuSU2jXZN152xqqEg`, e configuração opcional de `LP_SIBLING_BASE`. Explicita que **MCP Vercel ≠ CLI Vercel**.
  - Passo 4 antigo (Test drive) renumerado para 5; Passo 5 (Resumo) para 6 — agora inclui `/landing-page` e o checkmark de Vercel.
  - Novos fallbacks: `vercel-cli-falhou`, `vercel-login-falhou`, `vercel-org-falhou`.

- **landing-pages/cxpress/livraria/README.md:** instrução manual de cópia atualizada para usar `LP_SIBLING_BASE` com fallback a parent-do-repo + auto-link via `vercel link` se `.vercel/project.json` ausente. Funciona cross-máquina.

- **`.gitignore`:** adicionado `landing-pages/.lp-config.local.json` (config pessoal por colaborador).

- **Motivação:** colega tentou rodar `/lp-pipeline` em máquina nova e falhou em 2 frentes — sibling apontando pra `C:/Users/titof/...` inexistente, e leitura de auth Vercel via `$APPDATA` falhando porque ela autenticou só o MCP Vercel (não o CLI). Pós-mortem em `~/.claude/plans/uma-colega-rodou-lp-pipeline-staged-biscuit.md`.

---

## landing-pages/GUIDELINES.md
### 2026-04-30 — §10 Posicionamento do formulário (sugestão)
- Nova seção §10 com defaults de posicionamento por tipo de LP, válidos para todas as marcas:
  - **Webinar / material rico** → form na 2ª dobra (lead frio, otimizar volume).
  - **BoFu (demo, falar com vendas)** → form no meio da página (scroll filtra intenção, otimiza qualificação).
  - Sempre manter CTA visível na 1ª dobra que rola suave até o form.
- Sugestão, não obrigação. Override permitido com justificativa no PR/REVISAO.md.
- §6 (Estrutura mínima) ajustada: "CTA final com formulário" → "CTA final", desacoplando posição do form da estrutura narrativa (a §10 decide onde o form aparece).
- §§ 11-13 renumeradas (antigas §§ 10-12: integração tardia, favicon, performance).
- Base de pesquisa: CXL (long vs short form), MarketingExperiments (Sierra Tucson +220% com form abaixo da dobra), Unbounce Conversion Benchmark Report, Clearbit (lead form quality).

---

## meta-ads (benchmarks)
### 1.1.0 — 2026-04-30 — Threshold único nos benchmarks
- `meta-ads/data/benchmarks.json` simplificado: removida a tier "bom"/"aceitável", agora é **um threshold só = mínimo aceitável**. Status binário `[OK]` / `[RUIM]` (antes 3-tier).
- Valores atualizados conforme padrão atual da agência:
  - **CTR link** (cliques/impressões): Topo ≥ 1,0% / Remarketing ≥ 0,6%.
  - **Taxa de conversão LP** (leads/cliques): Topo ≥ 15% / Remarketing ≥ 5%.
  - **CpL** (gasto/leads):
    - BRL: Webinar ≤ R$ 18 / Material rico ≤ R$ 12 / Remarketing ≤ R$ 220.
    - USD (Latam): Webinar ≤ US$ 5 / Material rico ≤ US$ 3 / Remarketing ≤ US$ 60.
    - EUR (Portugal): Webinar ≤ € 6 / Material rico ≤ € 6 / Remarketing ≤ € 60.
  - **Frequência** (global): ≤ 7,0.
- `benchmark_checker.py` adaptado: `get_metric_status()` retorna `[OK]` ou `[RUIM]` (sem `[OK] Aceitável`).
- `full_trends_report.py` `_benchmarks_for()` adaptado para nova estrutura: `_bom` e `_ruim` apontam ao mesmo threshold (matriz de cenários CpL × CTR × Conv.LP segue funcionando como classificação binária).
- Skill `meta-ads/SKILL.md` (1.0.0 → 1.1.0): seção "Status dos Benchmarks" reescrita com tabela explícita por etapa de funil e moeda. `meta-ads/CONTEXT.md` ganha tabela de referência idêntica para colaboradores consultarem.

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
### 1.9.0 — 2026-04-30 (lp-integrar-form: card-dentro-de-card)

Round de fix a partir de incidente visual durante integracao do form Jotform na LP `buzzmonitor/social-listening-mayo-2026-latam`. Foco: garantir que o wrapper do embed nao herde o card visual do form mock.

#### Sintoma observado
Apos `/lp-integrar-form` substituir o `<form>` mock pelo embed Jotform, o live mostrou **dois cards aninhados**: o card branco com `padding: 40px`, `border` e `box-shadow` do `.form` (estilo do mock no `lp-gerar`) envolvendo outro card branco que o Jotform renderiza por padrao em volta dos campos.

#### Causa-raiz
- `lp-integrar-form` Passo 2 instruia: `<div class="form jotform-embed">{snippet}</div>`. A classe `form` foi mantida com a intencao de "preservar tamanho/contexto" do mock.
- Mas `.form` no `lp-gerar` e um **card visual completo** (`background: #fff; padding: 40px; border: 1px solid; box-shadow`) — nao so estilos de campo. Provedores externos (Jotform, RD Station, HubSpot) ja vem com card proprio. Resultado: dois cards.
- O CSS canonico `.form.jotform-embed { padding: 16px; overflow: hidden }` (Passo 3 da v1.2.0) so sobrescrevia o padding — nao desligava background/border/shadow herdados.

#### Mudancas
- **`lp-integrar-form` 1.2.0 → 1.3.0** — Passo 2 atualizado: wrapper agora usa apenas `<div class="jotform-embed">` (sem `form`). Passo 2 explicita "NAO herdar a classe `form` do mock" com referencia ao incidente. Passo 3 reduzido: `.jotform-embed iframe { width: 100% !important; ... }` (sem padding/background/overflow no wrapper — o provedor cuida do card). Passo 3 inclui regra de migracao: se LP antiga tem `.form.jotform-embed` (v<=1.2.0), substituir pelo novo seletor.
- **CHANGELOG entry** (este) — registra incidente para referencia futura, conforme `feedback_skill_improvement.md` (bug em skill durante uso → atualizar a skill antes de fechar caso pontual).

#### Skills bumpadas
- `lp-integrar-form` 1.2.0 → 1.3.0 (wrapper limpo, sem heranca de card mock)

#### Skills nao tocadas
- `lp-gerar`, `lp-revisar`, `lp-preparar`, `lp-publicar`, `lp-pipeline`, `landing-page` (advisor) — nao envolvidas. O `.form` no `lp-gerar` continua sendo card visual valido para o mock; mudanca foi apenas no que `lp-integrar-form` faz na transicao mock → embed.

#### Como impacta a LP afetada
A LP `buzzmonitor/social-listening-mayo-2026-latam` foi consertada in-place no mesmo round: `index.html` ajustado (classe `form` removida do wrapper, CSS reduzido) e re-deploy via `/lp-publicar`. Skill atualizada previne o cenario na proxima integracao.

### 1.8.0 — 2026-04-29 (guard anti-vazamento de copy)

Round de fixes a partir de incidente de geracao da LP `buzzmonitor/social-listening-mayo-2026-latam`. Foco: prevenir o gerador de inventar texto novo durante `lp-gerar` quando o briefing pede componentes visuais ricos (pull-quotes, kickers, tags rotacionadas, art cards).

#### Sintoma observado
Auditoria pos-`lp-gerar` (modo review) detectou **5 vazamentos CRITICOS** no HTML gerado:
- Frase-ancora do CIERRE truncada: `"...sino las que mejor entienden lo que se dice de ellas"` virou `"...sino las que mejor escuchan"`.
- Pull-quote inventado em `<aside class="for-quote">` na secao Para Quien (frase nao existia em `copy.txt`).
- Question inventada na secao Cierre (`"Sobran datos. Falta lectura. Vamos a leer juntos el 28 de Mayo."` — nao em `copy.txt`).
- Punchline de marketing inventada: `"Sin spam, sin enredos."` no CTA final.
- 5 em-dashes adicionados ao body durante expansao de bullets em `<h3>+<p>` (regras-anti-ia.md tem tolerancia zero para em-dash).

Plus: sinonimos cosmeticos (hero h1 `"utilizar"` -> `"usar"`), virgula+conjuncao reescrita como ponto+frase no hero sub.

#### Causa-raiz
- `lp-gerar` Passo 3 (briefing) instruia "estrutura solicitada" descrevendo elementos visuais (`card visual`, `tag rotacionada`, `pull-quote`) sem amarrar o texto desses elementos a uma linha especifica de `copy.txt`. O gerador interpretou "tem espaco visual aqui" como permissao para inventar.
- `lp-gerar` Passo 4 (validacao) so checava contagem de itens e emoji — nao fazia diff textual entre `copy.txt` e strings do HTML.
- `lp-revisar` tinha auditoria de GTM (Passo 3.5) mas nao tinha equivalente para fidelidade da copy.
- Incentivo composicional perverso: `frontend-design` e otimizada para gerar UIs "memoraveis" — quando ve um art card com slot vazio, preenche com texto criativo, nao com decoracao geometrica.

#### Mudancas
- **`lp-gerar` 1.4.0 -> 1.5.0** — Passo 3 (briefing pra `frontend-design`) ganhou bloco **REGRA DE FIDELIDADE DA COPY** explicitando: (a) todo texto visivel vem literal de `copy.txt`, (b) lista do que NAO inventar (pull-quotes, kickers, taglines, disclaimers punchy), (c) regra de nao truncar nem reescrever cosmeticamente, (d) whitelist exata do que pode aparecer fora da copy (5 categorias), (e) instrucao explicita "se componente visual pede texto e copy nao tem, fazer sem texto OU repetir literal frase relevante da copy". Passo 4 dividido em 4.1 (checklist tecnico — adicionado item de fallback robusto de reveal-on-scroll via `<noscript>`) e 4.2 (auditoria de fidelidade — diff textual em 4 buckets, busca dos 4 padroes mais comuns de vazamento, contagem de em-dash, validacao da frase-ancora, deteccao de sinonimos).
- **`lp-revisar` 1.3.0 -> 1.4.0** — novo **Passo 3.6: Auditoria de Fidelidade da Copy (CRITICO)**. Defesa em camadas: roda independente da auditoria que a `lp-gerar` ja faz. Procedimento de 7 etapas: carregar `copy.txt`, extrair textos do HTML, classificar em 4 buckets (literal/whitelist/cosmetica/vazamento), procurar 4 padroes (pull-quote, kicker, tag rotacionada, punchline), auditar em-dash com grep, validar frase-ancora, detectar sinonimos. Tabela de severidade-acao mapeia cada tipo de achado. Vazamentos sao tratados com mesma prioridade do GTM — CRITICOS, nao opcionais.
- **CHANGELOG entry** (este) — registra incidente para referencia futura, conforme `feedback_skill_improvement.md` (bug em skill durante uso -> atualizar a skill antes de fechar caso pontual).

#### Skills bumpadas
- `lp-gerar` 1.4.0 -> 1.5.0 (regra de fidelidade no briefing + checklist auditoria de fidelidade no Passo 4.2 + fallback robusto de reveal Passo 4.1)
- `lp-revisar` 1.3.0 -> 1.4.0 (novo Passo 3.6 — auditoria de fidelidade da copy)

#### Skills nao tocadas
- `lp-preparar`, `lp-publicar`, `lp-integrar-form`, `lp-pipeline`, `landing-page` (advisor) — nao envolvidas no path de geracao do HTML.

#### Como impacta a LP afetada
A LP `buzzmonitor/social-listening-mayo-2026-latam` foi consertada in-place no mesmo round (5 criticos + 4 melhorias aplicados via `Edit` em `index.html`, documentados em `REVISAO.md`). Nao precisa re-rodar `lp-gerar` — fix cirurgico foi suficiente. Skills atualizadas previnem o cenario na proxima LP.

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
