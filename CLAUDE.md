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
Landing Page: /lp-pipeline → /lp-preparar → /lp-gerar → /lp-revisar → (/lp-integrar-form) → /lp-publicar | /lp-sync (standalone — snapshot sibling) | /lp-health-check (standalone — monitora prod)
Criativos:    /criativo (ponta-a-ponta — adapta copy → brand+GUIDELINES → gera [HTML|Bloom] → revisa → entrega; organico|anuncio · 1x1/4x5/9x16)
Meta Ads:     /meta-ads → fetch + report | /meta-ads-trends (standalone)
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
| `meta-ads/` | Modulo Python de analise de campanhas (read-only) |
| `.claude/skills/` | Definicoes das skills e CONTEXT.md compartilhados |

### Contextos Compartilhados

Cada familia de skills tem um `CONTEXT.md` com marcas, regioes, caminhos e IDs do Notion:
- `.claude/skills/copy-criar/CONTEXT.md` — para skills copy-*
- `.claude/skills/news-pesquisar/CONTEXT.md` — para skills news-*
- `.claude/skills/trad-traduzir/CONTEXT.md` — para skills trad-*
- `.claude/skills/lp-preparar/CONTEXT.md` — para skills lp-*
- `.claude/skills/meta-ads/CONTEXT.md` — para skills meta-ads-*

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

**Primeira vez? Rode `/setup-agencia`** — guia interativo que conduz instalacao de Python, MCP do Notion e token Meta. Recomendado para todos os colaboradores no primeiro uso.

### Meta Ads (unico que requer instalacao)
Use `/setup-agencia` ou veja `meta-ads/SETUP.md` para passo-a-passo escrito.
Resumo: `python -m pip install -r meta-ads/requirements.txt`, copiar `.env.example` para `.env`, preencher token + data, validar com `python meta-ads/scripts/check_setup.py`. IDs das contas ja vem hardcoded.

### Notion
Requer MCP Notion conectado. IDs das pastas ja estao hardcoded nas skills e nos CONTEXT.md.

### Demais skills
Funcionam sem setup adicional.

---

## Comandos Disponiveis

### Primeira vez? Comece aqui:

| Comando | Quando usar |
|---|---|
| `/setup-agencia` | Setup interativo do zero — token Meta, Notion MCP, Python. Use na primeira vez ou ao trocar de maquina. |

### Nao sabe qual comando rodar? Use um destes (advisors):

| Comando | Quando usar |
|---|---|
| `/traduzir` | Traduzir copy para PT-PT ou ES-LATAM |
| `/escrever` | Criar, revisar ou pesquisar copy |
| `/newsletter` | Gerar newsletters semanais |
| `/landing-page` | Criar, revisar, integrar form ou publicar LP |
| `/criativo` | Criar imagem de criativo (estatico/carrossel), organico ou anuncio |
| `/anuncios` | Analisar performance de Meta Ads |

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

### Criativos (imagens estaticas / carrossel)

Skill unica **ponta a ponta**: adapta a copy → carrega brandbook + GUIDELINES → gera → revisa as imagens → entrega numa pasta local. Duas engines independentes: **HTML/CSS + Playwright** (padrao, texto pixel-perfect) e **Bloom** (IA, opt-in e desligavel — sem assinatura, a opcao some). Regras universais co-desenhadas em `criativos/GUIDELINES.md`. Saida em `criativos/{marca}/{regiao}/{slug}/` (outputs gitignored — upload manual). Engine HTML requer Playwright+Chromium (`/setup-agencia`).

| Comando | O que faz |
|---|---|
| `/criativo [marca] [regiao] [tipo] [uso] [formato] [slug]` | Gera o criativo ponta a ponta. Sem args, pergunta com chips. `uso=anuncio` aplica a margem de seguranca do Meta + gera overlay-guia de QA |

- `[tipo]`: `carrossel` (estrutura ditada pela copy; arco-ref cover→contexto→insight→conector→CTA) | `estatico` (1 imagem)
- `[uso]`: `organico` (borda livre, mascote sangra) | `anuncio` (safe-zone Meta; 9:16 reserva topo 250 / base 340)
- `[formato]`: `1x1` (1080²) | `4x5` (1080×1350, default feed) | `9x16` (1080×1920) — aceita CSV
- Copy vem de `/copy-criar` ou `/pauta-quente` ou colada (a skill adapta se vier crua, ou diagrama literal se ja vier boa).

### Landing Pages

Aceita `[marca]` e `[slug]`. Regras de design em `landing-pages/GUIDELINES.md`; runbook operacional (fluxos, assets, troubleshooting, fluxo de alteracao pos-deploy) em `landing-pages/CONTEXT.md` — carregado por todas as skills lp-*. Fonte em `landing-pages/{marca}/{slug}/`, deploy em pasta sibling isolada.

**Regra inegociavel:** toda alteracao ou deploy de LP roda pela skill `lp-publicar`. Fluxo manual (`cd sibling && vercel deploy ...`) e anti-padrao — mata as 4 camadas de defesa da skill (sync via Vercel API, drift-check, baseline, smoke test) e historicamente causa regressao silenciosa em vizinhas (incidentes 2026-05-11, 2026-05-13 e 2026-06-16). Essa regra tem **trava tecnica**: um hook `PreToolUse` em `.claude/settings.json` (commitado — vale pra todos os colaboradores) pede **confirmacao** antes de qualquer deploy Vercel — `vercel deploy|promote|rollback|redeploy` via Bash/PowerShell e o tool MCP `deploy_to_vercel`. Se o prompt de confirmacao aparecer e voce **nao** estiver dentro de `/lp-publicar` (ou `/dashboard-atualizar` para dashboards), **recuse** e rode a skill. Se voce precisa apenas de snapshot fresh da sibling para inspecao/debug (sem deploy), use `/lp-sync [dominio]`. Detalhes em `landing-pages/CONTEXT.md` §7.1 (anti-padroes) e §7.2 (incidentes); logica da trava em `.claude/hooks/guard_vercel_deploy.py`.

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

### Redes Sociais — Buzzmonitor

Fluxo mensal ponta-a-ponta: analytics do mes anterior alimenta planejamento do mes novo, que alimenta copies, que alimentam designs no Canva. Cada etapa publica no Notion em "Redes Sociais". Aceita so Instagram Buzzmonitor por enquanto.

| Comando | O que faz |
|---|---|
| `/social-pipeline [marca] [mes]` | Orquestrador completo. Costura todas as etapas com pausas pra aprovacao. Default: buzzmonitor + mes atual |
| `/social-analytics [YYYY-MM]` | Standalone — gera relatorio de performance. CSVs do Meta sao enviados via chat pela Catharina (regra) |
| `/social-plan [mes]` | Standalone — gera planejamento editorial mensal. Le relatorio.md do mes anterior se existir |
| `/social-canva [copies-file] [post-num]` | Standalone — gera designs no Canva pra um post (ou todos). Requer brand templates configurados em `brand/buzzmonitor/canva-template-ids.json` |

- `[mes]`: `julho`, `julho 2026`, `2026-07` (default: mes atual)
- Estrutura local: `social-media/buzzmonitor/{YYYY-MM}/` com subpastas `analytics/`, `copies/`, `designs/`
- Brand templates do Canva: ver `brand/buzzmonitor/canva-brand-templates.md` (especificacao) e `canva-template-ids.json` (config)

### Dashboard CM (Buzzmonitor Brasil)

Dashboard interna semanal de Content Marketing — KPIs do funil de leads + fechamentos. Atualizada toda semana pelo Victor (admin). Single-purpose: nao cobre outras marcas/dashboards.

| Comando | O que faz |
|---|---|
| `/dashboard-atualizar` | Roda gerador Python, lida com gate de regressao (fechamentos novos via chips), copia HTML pra sibling fora do repo, deploya na Vercel, valida via HTTP + Basic Auth. Manual-trigger. |
| `/auditar-deals-cm [--desde] [--ate]` | Read-only. Acha deals CM que somem da dashboard por UTM vazia (falha de automacao AC->Supabase): recupera UTM localmente (contato/empresa + titulo/inbound), re-roda o filtro CM reaproveitado e lista os "CM nao mapeados" em 3 niveis de confianca. So propoe remediacao; nunca grava no Supabase. |

Fonte: `dashboard/` (gerador Python + queries Supabase). Deploy: pasta sibling `{DASHBOARD_SIBLING_BASE}/dashboard-buzzmonitor-brasil/` (fora do repo — evita PII no git). Runbook manual: `dashboard/DEPLOY.md`. Auditoria de UTM: `dashboard/AUDITORIA-DEALS-CM.md`.

### Meta Ads (SOMENTE LEITURA)

Requer Python 3.10+ e `meta-ads/.env` configurado. **Primeira vez?** Rode `/setup-agencia` ou veja `meta-ads/SETUP.md`.

| Comando | O que faz |
|---|---|
| `/meta-ads [conta] [periodo]` | Pipeline completo: coleta + relatorio |
| `/meta-ads-fetch [conta] [periodo]` | So atualiza dados locais |
| `/meta-ads-report [conta] [periodo]` | So gera relatorio (sem nova coleta) |
| `/meta-ads-trends [conta]` | Tendencias temporais (3d/7d/15d/30d) |
| `/meta-ads-geral` | Relatorio consolidado das 6 contas — drill-down Conta->Funil->Adset->Ad, publica no Notion |

- `[conta]`: `buzzmonitor_brl` | `buzzmonitor_usd` | `buzzmonitor_eur` | `cxpress_brl` | `cxpress_usd` | `cxpress_eur`
- `[periodo]`: `mes_atual` | `mes_anterior` | `ultimos_30`

### Bunzzai (fonte alternativa via MCP — SOMENTE LEITURA)

Mesma cobertura do `/meta-ads-trends` (Buzzmonitor + Cxpress, todas as moedas), mas via MCP do Bunzzai (snapshots cumulativos no CRM proprio) em vez da Meta API direta. Zero setup local — tudo via MCP em tempo real. Util para cross-check, quando o token Meta expirou ou para auditar `cron travado` (snapshots congelados do Bunzzai). Diferencas importantes — cliques **totais** vs `link_clicks`, conversoes **amplas** vs `leads custom` — estao detalhadas em `.claude/skills/bunzzai/CONTEXT.md` §Diferencas metricas. Sugere cross-check com `/meta-ads-trends` antes de decisao de budget grande.

| Comando | O que faz |
|---|---|
| `/bunzzai [conta]` | Drill-down Conta -> Campanha -> Adset -> Ad com diff de janelas 7d/15d/30d, diagnostico cruzado (CpL × CTR × Conv. LP) e detecao de cron travado. Reaproveita benchmarks do meta-ads. |

- `[conta]`: `buzzmonitor_brl` | `buzzmonitor_usd` | `buzzmonitor_eur` | `cxpress_brl` | `cxpress_usd` | `cxpress_eur` (mesma lista do `/meta-ads`)
