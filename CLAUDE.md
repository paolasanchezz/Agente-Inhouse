# Agente Inhouse — Grupo Elife

Este agente automatiza a criacao de newsletters, traducoes de copy, criacao de copy, landing pages e analise de campanhas Meta Ads para as marcas do Grupo Elife: Buzzmonitor, Buzzcreators, Cxpress e Elife.

---

## Protocolo de Copy (OBRIGATORIO em qualquer idioma e formato)

Toda tarefa que **cria ou altera texto que vai pro publico** (anuncio, e-mail, legenda, roteiro, landing page, newsletter, criativo, traducao) carrega os **3 pilares ANTES de escrever a primeira palavra**:

1. **Linguistico** - se a regiao/idioma nao for `brasil`/PT-BR, leia `conhecimento/linguistico/{pt-portugal|es-latam}/padrao-linguistico.md`. Se nao carregar, **PARE**. Nunca escreva PT-PT ou ES "de cabeca" (e assim que brasileirismo vaza: "esta crescendo" no lugar de "esta a crescer", "usuario", "aplicativo", "faturamento", "fale conosco").
2. **Boas praticas** - `conhecimento/copywriting/fundamentos-copy.md` (+ o doc do tipo: video-curto, estatico ou email).
3. **Anti-IA** - `conhecimento/editorial/regras-anti-ia.md` **+ o anexo do idioma** (PT-PT / ES-LATAM). Fonte unica de anti-IA. O `estilo-newsletter.md` e so estrutura de newsletter, nao e a lista anti-IA.

**Sem skill = sem rede de protecao.** Se o pedido vier solto no chat ("escreve uma copy em PT-PT pra..."), **PARE e use a skill certa** (`/escrever`, `/traduzir`, `/landing-page`, `/criativo`, `/pauta-quente`) ou, se for inevitavel escrever a mao, carregue os 3 arquivos acima primeiro. Contrato operacional detalhado em cada `CONTEXT.md`.

---

## Arquitetura

### Fluxo das Skills

```
Newsletters:  /news-pipeline → /news-pesquisar → (pausa: aprovar pauta?) → /news-criar-post → /news-gerar → /news-revisar
Traducao:     /trad-pipeline → /trad-traduzir → /trad-revisar
Copywriting:  /copy-criar (standalone) | /copy-pesquisar → /copy-swipefile | /copy-revisar (standalone)
Pauta Quente: /pauta-quente (standalone — noticia → multi-formato × multi-idioma)
Blog SEO/GEO: /blog-diario [marca] [regiao] [tema?] (standalone autonomo — cluster → bake-off de volume multi-fonte → post SEO/GEO + METADADOS + CTA→LP → rascunho Notion; diario via /schedule)
Landing Page: /lp-pipeline → /lp-preparar → /lp-gerar → /lp-revisar → (/lp-integrar-form) → /lp-publicar | /lp-sync (standalone — snapshot sibling) | /lp-health-check (standalone — monitora prod)
Criativos:    /criativo (ponta-a-ponta — adapta copy → brand+GUIDELINES → gera [HTML|Bloom] → revisa → entrega; organico|anuncio · 1x1/4x5/9x16)
Webinar:      /roteiro-webinar-perpetuo (standalone — roteiro com timestamps + falas + demo da plataforma + slides de abertura)
Meta Ads:     /bunzzai [conta] (1 conta · drill-down) | /bunzzai-geral (consolidado 6 contas · publica Notion) — ANALISE/leitura
Meta criar:   /meta-campanha [acao] [marca] (cria·edita campanha/adset/ad via MCP oficial Meta — ESCRITA; tudo PAUSADO; ativar/orcamento via hook)
Calibracao:   /trad-calibrar (atualiza padroes linguisticos)
Redes Sociais: /social-pipeline → /social-analytics → /social-plan → copies em lote → (pausa) → /social-canva
```

### Diretorios

| Diretorio | O que contem |
|---|---|
| `brand/` | Identidade visual, tokens de design e regras de geracao por marca (ver `brand/DESIGN.md`) |
| `conhecimento/` | Base de conhecimento — fonte de verdade sobre produtos, copy, linguistica e editorial |
| `newsletter/` | Entregas de newsletters geradas (publicadas no Notion) |
| `traducao/` | Traducoes geradas (publicadas no Notion) |
| `pauta-quente/` | Conteudos gerados a partir de noticia recente por marca (`pauta-quente/{marca}/YYYY-MM-DD-{slug}/`) |
| `landing-pages/` | LPs geradas por marca (`landing-pages/{marca}/{slug}/`) + `GUIDELINES.md` universal |
| `social-media/` | Planejamentos editoriais de redes sociais por marca (`social-media/{marca}/YYYY-MM/`) |
| `criativos/` | Criativos gerados por marca/regiao (`criativos/{marca}/{regiao}/{slug}/`) + `GUIDELINES.md` universal. Outputs **gitignored** (PNGs pesados, upload manual); só o GUIDELINES versiona |
| `meta-ads/` | Enxuto — so `benchmarks.json` (usado pelo /bunzzai). Pipeline antigo arquivado em `meta-ads-legacy/` |
| `.claude/skills/` | Definicoes das skills e CONTEXT.md compartilhados |
| `.claude/skills-desativadas/` | Skills tiradas de circulacao (ex: pipeline `meta-ads-*` substituido por /bunzzai em 2026-06-22) |

### Contextos Compartilhados

Cada familia de skills tem um `CONTEXT.md` com marcas, regioes, caminhos e IDs do Notion:
- `.claude/skills/copy-criar/CONTEXT.md` — para skills copy-*
- `.claude/skills/news-pesquisar/CONTEXT.md` — para skills news-*
- `.claude/skills/trad-traduzir/CONTEXT.md` — para skills trad-*
- `.claude/skills/lp-preparar/CONTEXT.md` — para skills lp-*
- `.claude/skills/bunzzai/CONTEXT.md` — para `/bunzzai` e `/bunzzai-geral` (analise de Meta Ads via MCP Bunzzai)

A skill `/criativo` nao usa CONTEXT.md — suas regras universais ficam em `criativos/GUIDELINES.md`.

### Brand / Design System

Ao criar landing pages, criativos ou componentes para uma marca especifica, carregar:
1. `brand/DESIGN.md` (visao geral e hierarquia)
2. `brand/{marca}/tokens.json` (cores, tipografia, espacamento — formato W3C DTCG)
3. `brand/{marca}/generation-rules.json` (regras de composicao para AI)
4. `brand/{marca}/brand-manifest.json` (identidade, tom de voz, messaging)

Conhecimento de produto fica em `conhecimento/produto/` — nao duplicar em `brand/`.

### Versionamento

Cada skill tem `version` no frontmatter (semver simplificado). Mudanças vão em `CHANGELOG.md` no mesmo PR. Bump MAJOR ao quebrar interface da skill.

---

## Setup

**Primeira vez? Rode `/setup-agencia`** — guia interativo que conduz instalacao de Python e MCP do Notion. Recomendado para todos os colaboradores no primeiro uso.

### Meta Ads — sem setup local
Desde 2026-06-22, todas analises rodam via MCP Bunzzai (`/bunzzai` ou `/bunzzai-geral`). Nao precisa de token Meta nem instalacao Python — basta o MCP Bunzzai conectado.

O pipeline antigo (`/meta-ads-*` + scripts Python locais) foi desativado mas mantido em `meta-ads-legacy/` pra auditoria pontual e em `.claude/skills-desativadas/` pra eventual reativacao.

### Notion
Requer MCP Notion conectado. IDs das pastas ja estao hardcoded nas skills e nos CONTEXT.md.

### Demais skills
Funcionam sem setup adicional.

---

## Comandos Disponiveis

### Primeira vez? Comece aqui:

| Comando | Quando usar |
|---|---|
| `/setup-agencia` | Setup interativo do zero — Python, Notion MCP, Bunzzai MCP. Use na primeira vez ou ao trocar de maquina. |

### Nao sabe qual comando rodar? Use um destes (advisors):

| Comando | Quando usar |
|---|---|
| `/traduzir` | Traduzir copy para PT-PT ou ES-LATAM |
| `/escrever` | Criar, revisar ou pesquisar copy |
| `/newsletter` | Gerar newsletters semanais |
| `/landing-page` | Criar, revisar, integrar form ou publicar LP |
| `/criativo` | Criar imagem de criativo (estatico/carrossel), organico ou anuncio |
| `/anuncios` | Analisar performance (Bunzzai) ou criar/editar campanha (`/meta-campanha`) de Meta Ads |

Cada um faz perguntas com opcoes clicaveis. Os comandos diretos abaixo continuam funcionando para quem ja tem pratica.

### Entrega e revisao (commit + PR)

Ao final das alteracoes, rode `/commit` para entregar ao Victor revisar. A skill cria branch nova, commita, faz push e abre pull request automaticamente. **Nunca commita em main**, com uma excecao: quando o proprio Victor (admin do repo) pedir explicitamente sem usar a skill (ex: "commit direto em main", "sem branch", "sem PR", "faz direto"). Nesse caso, commitar + push em main mantendo as demais regras: nunca `--force`, nunca `--no-verify`, nunca pular hooks, mensagem PT-BR sem assinatura de IA, nunca incluir `.env` ou credentials no stage. O override so vale para o Victor. Outros colaboradores sempre via `/commit`.

Para revisar um PR, o Victor roda `/pull-request-review` com o link ou numero — gera relatorio local com achados em 3 niveis de severidade. Nao posta comentario no GitHub.

| Comando | O que faz |
|---|---|
| `/commit` | Cria branch `claude/{slug}`, commita, push e abre PR pra main. Sem args — totalmente automatico. Primeira vez requer `gh auth login` (skill guia). |
| `/pull-request-review [url-ou-num]` | Revisa PR localmente — diff + dominio-especifico do repo (skills/brand/LP/meta-ads). Relatorio em `reviews/pr-{N}-YYYY-MM-DD.md` com criticos, importantes e nice-to-haves. |

### Newsletters
Aceita `[brand]` e `[region]`. Default: `buzzmonitor brasil`. **Newsletter semanal noticiosa, eixo no blog proprio** (90% links blog, 10-20% clipping da marca em imprensa). 1 NL por execucao.

| Comando | O que faz |
|---|---|
| `/news-pipeline [brand] [region]` | Pesquisa + (pausa para aprovar pauta sugerida, se houver lacuna) + criacao de post + geracao + revisao. 1 NL/execucao |
| `/news-pesquisar [brand] [region]` | Mapeia dores + indexa blog + busca clipping PR; gera dor da semana, posts-ancora e (se houver lacuna) pauta sugerida |
| `/news-criar-post [brand] [region]` | Cria post de blog (1500-2500 palavras) para preencher lacuna identificada; publica draft no Notion. Manual-trigger (so apos aprovar pauta) |
| `/news-gerar [brand] [region]` | Gera 1 newsletter da semana a partir de dor-semana.md |
| `/news-revisar [brand] [region]` | Revisa 1 newsletter (fact-check, linguagem jornalistica, anti-IA, dedupe) |

- `[brand]`: `buzzmonitor` | `buzzcreators` | `cxpress` | `elife`
- `[region]`: `brasil` (PT-BR) | `latam` (ES-LATAM) | `portugal` (PT-PT)
- Para automatizar cadencia semanal: `/loop 7d /news-pipeline {brand} {region}` ou `/schedule` (decisao por marca/regiao do usuario)

### Traducao de Copy

| Comando | O que faz |
|---|---|
| `/trad-pipeline [arquivo] [pt-pt\|es-latam]` | Traduz e revisa |
| `/trad-traduzir [arquivo] [pt-pt\|es-latam]` | So traduz |
| `/trad-revisar [arquivo] [pt-pt\|es-latam]` | So revisa |
| `/trad-calibrar [pt-pt\|es-latam]` | Atualiza padrao linguistico |

### Copywriting

| Comando | O que faz |
|---|---|
| `/copy-criar [marca] [regiao] [tipo] [estagio] ["briefing"]` | Cria 3 variacoes de copy com hooks e angulos diferentes |
| `/copy-pesquisar [marca] [pais] [tipo]` | Pesquisa referencias frescas de copy |
| `/copy-revisar [arquivo-ou-texto] [marca]` | Revisa copy (tecnica + produto + IA) e corrige |
| `/copy-swipefile add [url-ou-texto]` | Adiciona exemplo ao swipe file |
| `/copy-swipefile buscar [tema]` | Busca exemplos no swipe file |

- `[marca]`: `buzzmonitor` | `buzzcreators` | `cxpress` | `elife`
- `[regiao]`/`[pais]`: `brasil` | `portugal` | `latam`
- `[tipo]`: `video-curto` | `estatico` | `email` | `geral`
- `[estagio]`: `tofu` | `mofu` | `bofu` (default: `tofu`)

Base de conhecimento: `conhecimento/copywriting/` (fundamentos, video-curto, estatico, blog, linkedin, email, funil)

### Pauta Quente

Transforma uma noticia recente em conteudo multi-formato e multi-idioma. Rastreia fonte primaria, aplica edutainment + conector com produto e publica no Notion em `Entregas > Pauta Quente {Marca}`.

| Comando | O que faz |
|---|---|
| `/pauta-quente [url] [marca] [tipos-csv] [idiomas-csv]` | Gera N pecas (tipos x idiomas) a partir da noticia. Ex: `/pauta-quente https://... buzzmonitor "carrossel,blog,email" "br,pt,es"` |

- `[url]`: link completo da noticia (http:// ou https://)
- `[marca]`: `buzzmonitor` | `buzzcreators` | `cxpress` | `elife`
- `[tipos-csv]`: combinacao de `carrossel` | `video-curto` | `blog` | `linkedin` | `email`
- `[idiomas-csv]`: combinacao de `br` (PT-BR) | `pt` (PT-PT) | `es` (ES-LATAM)

### Blog SEO/GEO (Diario)

Skill standalone **autonoma** que gera 1 blogpost otimizado para SEO + GEO por execucao, a partir dos **clusters de tema** da marca (fonte local em `conhecimento/produto/{marca}/seo/clusters-{regiao}.md` — Victor envia, o agente transcreve). Escolhe o tema por **bake-off de volume multi-fonte** (Semrush + autocomplete/Trends/GSC, que corroboram ou refutam o Semrush), evita duplicar posts existentes (inventario = blog-cache + sitemap vivo + rascunhos Notion), escreve no idioma nativo, monta bloco **METADADOS** completo (slug, title, meta description, keywords, cluster) e CTA pra 1 modulo + LP (catalogo `landing-pages/catalogo/lps-{marca}.md`) em MoFu/BoFu. **Anti-IA minimo** (so precisao factual + grafia + idioma — nao roda regras-anti-ia.md). Publica rascunho no Notion (`SEO > {Marca} > Conteúdos complementares`); artefato local Astro-ready pra posting via API futuro. **v1: Cxpress BR.** Regras em `.claude/skills/blog-diario/CONTEXT.md`.

| Comando | O que faz |
|---|---|
| `/blog-diario [marca] [regiao] [tema?]` | Gera 1 post SEO/GEO autonomo e publica rascunho no Notion. Sem `tema`, escolhe a melhor lacuna do cluster pelo score. Diario via `/schedule` ou `/loop 1d`. |

- `[marca]`: `buzzmonitor` | `buzzcreators` | `cxpress` | `elife` (default: `cxpress`)
- `[regiao]`: `brasil` (default) | `latam` | `portugal`
- `[tema]`: opcional, entre aspas — forca um tema/keyword e pula a selecao
- Requer MCP Notion + Semrush conectados. Clusters da marca/regiao precisam existir (senao a skill para e pede ao Victor).

### Criativos (imagens estaticas / carrossel)

Skill unica **ponta a ponta**: adapta a copy → carrega brandbook + GUIDELINES → gera → revisa as imagens → entrega numa pasta local. Duas engines independentes: **HTML/CSS + Playwright** (padrao, texto pixel-perfect) e **Bloom** (IA, opt-in e desligavel — sem assinatura, a opcao some). Regras universais co-desenhadas em `criativos/GUIDELINES.md`. Saida em `criativos/{marca}/{regiao}/{slug}/` (outputs gitignored — upload manual). Engine HTML requer Playwright+Chromium (`/setup-agencia`).

| Comando | O que faz |
|---|---|
| `/criativo [marca] [regiao] [tipo] [uso] [formato] [slug]` | Gera o criativo ponta a ponta. Sem args, pergunta com chips. `uso=anuncio` aplica a margem de seguranca do Meta + gera overlay-guia de QA |

- `[tipo]`: `carrossel` (estrutura ditada pela copy; arco-ref cover→contexto→insight→conector→CTA) | `estatico` (1 imagem)
- `[uso]`: `organico` (borda livre, mascote sangra) | `anuncio` (safe-zone Meta; 9:16 reserva topo 250 / base 340)
- `[formato]`: `1x1` (1080²) | `4x5` (1080×1350, default feed) | `9x16` (1080×1920) — aceita CSV
- Copy vem de `/copy-criar` ou `/pauta-quente` ou colada (a skill adapta se vier crua, ou diagrama literal se ja vier boa).

### Webinar Perpetuo

Skill standalone que gera roteiro completo de webinar perpetuo (talking head + demo da plataforma) com timestamps, falas sugeridas, indicacoes do que mostrar na tela, mais deck PPT de abertura. So o tema e obrigatorio: **infere a marca** a partir do tema (se nao informada) e escreve **todas as entregas nativamente no idioma resolvido** (PT-BR/PT-PT/ES-LATAM), aplicando o banco de conhecimento linguistico. Carrega o BRANDBOOK completo da marca. Estrutura padrao: Hook → Contexto + Dor → Promessa → Demo da plataforma (40-50% do tempo, 3 momentos) → CTA. Demo usa grafias exatas de features do `BRANDBOOK.md` da marca.

| Comando | O que faz |
|---|---|
| `/roteiro-webinar-perpetuo [marca] [regiao\|idioma] [duracao] ["tema/dor"]` | Gera roteiro + slides de abertura. So o tema e obrigatorio — marca inferida do tema, idioma do idioma/regiao. Ex: `/roteiro-webinar-perpetuo es-latam "Primer monitoreo de marca en 5 pasos"` |

- `[marca]`: `buzzmonitor` | `buzzcreators` | `cxpress` | `elife` (opcional — inferida do tema se omitida)
- `[regiao]`: `brasil` (default) | `portugal` | `latam`
- `[idioma]`: `pt-br` (default) | `pt-pt` | `es-latam` (aceita `br`/`pt`/`es`; define o pilar linguistico de TODAS as entregas)
- `[duracao]`: `5min` | `10min` (default) | `15min` | `20min` | `30min`
- `[tema]`: texto livre entre aspas — tema + dor central + (se houver) objetivo

Saida em `conhecimento/copywriting/criacao/{marca}/YYYY-MM-DD/webinar-{slug}/` (`roteiro.md`, `slides-abertura.md`, `INDICE.md`, `REVISAO-LOG.md`) e Notion em `Entregas > Webinars — {NomeDaMarca}`.

### Landing Pages

Aceita `[marca]` e `[slug]`. Regras de design em `landing-pages/GUIDELINES.md`; runbook operacional (fluxos, assets, troubleshooting, fluxo de alteracao pos-deploy) em `landing-pages/CONTEXT.md` — carregado por todas as skills lp-*. Fonte em `landing-pages/{marca}/{slug}/`, deploy em pasta sibling isolada.

**Regra inegociavel:** toda alteracao ou deploy de LP roda pela skill `lp-publicar`. Fluxo manual (`cd sibling && vercel deploy ...`) e anti-padrao — mata as 4 camadas de defesa da skill (sync via Vercel API, drift-check, baseline, smoke test) e historicamente causa regressao silenciosa em vizinhas (incidentes 2026-05-11, 2026-05-13 e 2026-06-16). Essa regra tem **trava tecnica**: um hook `PreToolUse` em `.claude/settings.json` (commitado — vale pra todos os colaboradores) pede **confirmacao** antes de qualquer deploy Vercel — `vercel deploy|promote|rollback|redeploy` via Bash/PowerShell e o tool MCP `deploy_to_vercel`. Se o prompt de confirmacao aparecer e voce **nao** estiver dentro de `/lp-publicar` (ou `/dashboard-atualizar` para dashboards), **recuse** e rode a skill. Se voce precisa apenas de snapshot fresh da sibling para inspecao/debug (sem deploy), use `/lp-sync [dominio]`. Detalhes em `landing-pages/CONTEXT.md` §7.1 (anti-padroes) e §7.2 (incidentes); logica da trava em `.claude/hooks/guard_vercel_deploy.py`.

**Excecao — Webflow (publicacao direta via MCP):** a regra acima e especifica do pipeline **Vercel** (sibling + guarda-chuva — foi nesse modelo que os 3 incidentes aconteceram). Quando **qualquer colaborador** pedir **explicitamente** para subir/publicar uma LP no **Webflow** (nomeando Webflow + acao de publicar), publique direto via o MCP do Webflow, **sem** `lp-publicar` — as 4 camadas de defesa sao Vercel-especificas e nao protegem nada no Webflow. Destino ambiguo ("poe no ar" sem dizer onde) → pergunte Vercel ou Webflow, nunca assuma. A autorizacao e **por pedido** (nao e passe livre permanente nem entre sessoes); gate = so o pedido explicito, sem checkpoint extra (decisao do Victor, 2026-06-25). LP e conteudo publico: se a copy nao passou pelo pipeline, rode linguistico + anti-IA antes (3 pilares, topo deste doc). Requer um MCP do Webflow conectado (se nao houver, avise e pare — nao caia no Vercel por conta propria). Regras completas em `landing-pages/CONTEXT.md` §2.4.

| Comando | O que faz |
|---|---|
| `/lp-pipeline [marca] [slug] [fonte] [dominio]` | Fluxo completo: preparar → gerar → revisar → (pausa) → publicar |
| `/lp-preparar [marca] [slug] [fonte]` | Estrutura copy crua em blocos rotulados + anti-IA |
| `/lp-gerar [marca] [slug]` | Gera HTML estatico invocando `frontend-design` |
| `/lp-revisar [marca]/[slug]` | Audita (design + a11y) e aplica criticos |
| `/lp-integrar-form [marca]/[slug] "snippet"` | Troca form mock por embed real (manual-trigger) |
| `/lp-publicar [marca] [slug] [dominio]` | Sync sibling + deploy Vercel + PageSpeed + relatorio Notion |
| `/lp-sync [dominio]` | Read-only — popula sibling local com snapshot do ultimo deploy READY (antes de inspecao/debug manual). Nao deploya. |
| `/lp-health-check [--dry-run] [--no-drift]` | Descobre todas LPs em producao via Vercel API + HTTP check + email pra Victor se houver falha. Silenciosa quando OK. Pra rodar diariamente via `/schedule`. |

- `[marca]`: `buzzmonitor` | `buzzcreators` | `cxpress` | `elife`
- `[slug]`: kebab-case curto (ex: `monitoramento-maio`)
- `[fonte]`: URL Notion, caminho de arquivo ou texto colado
- `[dominio]`: FQDN do guarda-chuva (ex: `content.cxpress.io`, `webinar.buzzmonitor.com`)

### ClickMeeting — Convites de Moderador

Rotina diaria que envia convite (role=presenter — a API nao aceita `moderator` em invitation/email) para a proxima sessao agendada de cada serie recorrente. Config em `.claude/skills/convites-moderador/config.json` (mapping `recurring_config_id` -> email do moderador). Roda 07:00 BRT via workflow no n8n (`Convites Moderador ClickMeeting - diario 07h BRT`, id `1TFA4xHvFEZQ5lns`; fonte versionada em `integracoes/n8n/convites-moderador-clickmeeting.json`). Migrado do GitHub Actions em 2026-07-07 — o `.github/workflows/convites-moderador.yml` fica como fallback manual desabilitado.

| Comando | O que faz |
|---|---|
| `/convites-moderador [--dry-run] [--series RID]` | Manual on-demand. Dry-run lista o plano sem enviar; `--series` filtra 1 recurring_config_id. |

### Redes Sociais — multi-marca

Fluxo mensal ponta-a-ponta: analytics do mes anterior alimenta planejamento do mes novo, que alimenta copies, que alimentam designs no Canva. Cada etapa publica no Notion em "Redes Sociais" (hub por mes e por marca). Aceita as 4 marcas (Instagram + LinkedIn); as decisoes especificas de cada marca (handles, modelo de rede, pilares, cadencia, referencias, nicho) vivem em `brand/{marca}/social-media.json` — nada de decisao de marca hardcoded nas skills.

| Comando | O que faz |
|---|---|
| `/social-pipeline [marca] [mes]` | Orquestrador completo. Costura todas as etapas com pausas pra aprovacao. Default: buzzmonitor + mes atual |
| `/social-analytics [marca] [YYYY-MM]` | Standalone — gera relatorio de performance. CSVs do Meta sao enviados via chat (regra); separa conta propria × secundarias × UGC pela config da marca |
| `/social-plan [marca] [mes]` | Standalone — gera planejamento editorial mensal. Exige relatorio.md do mes anterior (excecao: primeiro ciclo da marca) |
| `/social-canva [copies-file] [post-num]` | Standalone — gera designs no Canva pra um post (ou todos). Deriva a marca do caminho; requer brand templates em `brand/{marca}/canva-template-ids.json` |

- `[marca]`: `buzzmonitor` | `cxpress` | `buzzcreators` | `elife` (default: buzzmonitor)
- `[mes]`: `julho`, `julho 2026`, `2026-07` (default: mes atual)
- Estrutura local: `social-media/{marca}/{YYYY-MM}/` com subpastas `analytics/`, `copies/`, `designs/`
- Config social por marca: `brand/{marca}/social-media.json` (Buzzmonitor = modelo de referencia; Cxpress/Buzzcreators = rascunho; Elife = esqueleto — campos null a skill pergunta e preenche no uso)
- Brand templates do Canva: especificacao em `brand/buzzmonitor/canva-brand-templates.md` (vale como modelo pra todas as marcas); IDs por marca em `brand/{marca}/canva-template-ids.json`

### Dashboard CM (Buzzmonitor Brasil)

Dashboard interna semanal de Content Marketing — KPIs do funil de leads + fechamentos. Atualizada toda semana pelo Victor (admin). Single-purpose: nao cobre outras marcas/dashboards.

| Comando | O que faz |
|---|---|
| `/dashboard-atualizar` | Roda gerador Python, lida com gate de regressao (fechamentos novos via chips), copia HTML pra sibling fora do repo, deploya na Vercel, valida via HTTP + Basic Auth. Manual-trigger. |
| `/auditar-deals-cm [--desde] [--ate]` | Read-only. Acha deals CM que somem da dashboard por UTM vazia (falha de automacao AC->Supabase): recupera UTM localmente (contato/empresa + titulo/inbound), re-roda o filtro CM reaproveitado e lista os "CM nao mapeados" em 3 niveis de confianca. So propoe remediacao; nunca grava no Supabase. |

Fonte: `dashboard/` (gerador Python + queries Supabase). Deploy: pasta sibling `{DASHBOARD_SIBLING_BASE}/dashboard-buzzmonitor-brasil/` (fora do repo — evita PII no git). Runbook manual: `dashboard/DEPLOY.md`. Auditoria de UTM: `dashboard/AUDITORIA-DEALS-CM.md`.

### Dashboard SEO (Buzzmonitor Brasil)

Dashboard de SEO on-demand — KPIs de GSC + GA4 + Semrush num HTML visual. Single-purpose (Buzzmonitor BR). **Sem chave de API no repo:** Semrush via MCP; Google via OAuth com credenciais locais por usuario (`~/.seo-report-buzzmonitor/`, gitignored).

| Comando | O que faz |
|---|---|
| `/seo-report [data?]` | Coleta GSC+GA4 (script Python OAuth) + Semrush (MCP), gera dashboard HTML e abre no navegador. Sem args, coleta na hora; aceita caminho de um `seo_data.json` ja gerado. Manual-trigger. |

Fonte: `.claude/skills/seo-report/` (SKILL.md + `seo_report_buzzmonitor.py`). Requer Python + libs Google (`/setup-agencia` cobre Python) e o MCP Semrush conectado.

### Meta Ads — via Bunzzai (SOMENTE LEITURA)

Desde 2026-06-22, todas analises de Meta Ads rodam pelo **MCP Bunzzai** (CRM proprio com snapshots cumulativos). Sem dependencia de token Meta — basta o MCP conectado. Cobre Buzzmonitor + Cxpress (todas as moedas).

O pipeline antigo (`meta-ads-*` + scripts Python locais) foi desativado: skills em `.claude/skills-desativadas/`, scripts em `meta-ads-legacy/`. Reaproveita-se apenas `meta-ads/data/benchmarks.json` (thresholds de CpL/CTR/Conv.LP) e a matriz de cenarios (consolidada em `.claude/skills/bunzzai/CONTEXT.md`).

| Comando | O que faz |
|---|---|
| `/bunzzai [conta]` | Uma conta — drill-down Conta -> Campanha -> Adset -> Ad com diff de janelas 7d/15d/30d, diagnostico cruzado (CpL × CTR × Conv. LP) e detecao de cron travado |
| `/bunzzai-geral` | Consolidado das 6 contas — drill-down Conta -> Funil -> Adset -> Ad, publica no Notion |

- `[conta]`: `buzzmonitor_brl` | `buzzmonitor_usd` | `buzzmonitor_eur` | `cxpress_brl` | `cxpress_usd` | `cxpress_eur`

**Diferencas metricas vs Meta API direta** (cliques totais vs `link_clicks`, conversoes amplas vs `leads custom`): documentadas em `.claude/skills/bunzzai/CONTEXT.md`. Quando a decisao envolver budget grande (>R$ 1.000) ou CpL pertinho do threshold, rodar manualmente `meta-ads-legacy/scripts/audit_vs_bunzzai.py` pra cross-check (requer token Meta fresh — `meta-ads-legacy/SETUP.md`).

### Meta Ads — criacao/gestao via MCP oficial (ESCRITA)

Para **criar ou mexer** em campanha (nao analisar), use `/meta-campanha` — primeira skill de escrita no Meta, via o **MCP oficial da Meta** (OAuth, tools `ads_*`). Atua como gestor de trafego: forca briefing completo, classifica funil, questiona publico incoerente, mostra o plano e cria **tudo PAUSADO**. Regras, contas e convencoes em `.claude/skills/meta-campanha/CONTEXT.md`.

| Comando | O que faz |
|---|---|
| `/meta-campanha [acao] [marca] [briefing]` | Cria campanha/adset/ad, edita (publico/orcamento/posicionamento/link), pausa/religa, renomeia. Tudo pausado; **ativar e orcamento alto exigem aprovacao**. |

**Trava tecnica (hook commitado, vale pra todos):** `guard_meta_activate.py` pede confirmacao antes de **ativar/religar** ou de criar/editar com **orcamento acima do teto** (`meta-ads/data/budget-guardrails.json` — conservador R$50/$12/EUR12 por adset/dia). Mesma filosofia do guard do Vercel; cobre o MCP oficial da Meta e, por defesa, as tools de escrita do BunzzAI. Logica em `.claude/hooks/guard_meta_activate.py`.
