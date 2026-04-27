# Agente Inhouse — Grupo Elife

Este agente automatiza a criacao de newsletters, traducoes de copy, criacao de copy, landing pages e analise de campanhas Meta Ads para as marcas do Grupo Elife: Buzzmonitor, Buzzcreators, Cxpress e Elife.

---

## Arquitetura

### Fluxo das Skills

```
Newsletters:  /news-pipeline → /news-pesquisar → /news-gerar → /news-revisar
Traducao:     /trad-pipeline → /trad-traduzir → /trad-revisar
Copywriting:  /copy-criar (standalone) | /copy-pesquisar → /copy-swipefile | /copy-revisar (standalone)
Pauta Quente: /pauta-quente (standalone — noticia → multi-formato × multi-idioma)
Landing Page: /lp-pipeline → /lp-preparar → /lp-gerar → /lp-revisar → (/lp-integrar-form) → /lp-publicar
Meta Ads:     /meta-ads → fetch + report | /meta-ads-trends (standalone)
Calibracao:   /trad-calibrar (atualiza padroes linguisticos)
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
| `meta-ads/` | Modulo Python de analise de campanhas (read-only) |
| `.claude/skills/` | Definicoes das skills e CONTEXT.md compartilhados |

### Contextos Compartilhados

Cada familia de skills tem um `CONTEXT.md` com marcas, regioes, caminhos e IDs do Notion:
- `.claude/skills/copy-criar/CONTEXT.md` — para skills copy-*
- `.claude/skills/news-pesquisar/CONTEXT.md` — para skills news-*
- `.claude/skills/trad-traduzir/CONTEXT.md` — para skills trad-*
- `.claude/skills/lp-preparar/CONTEXT.md` — para skills lp-*
- `.claude/skills/meta-ads/CONTEXT.md` — para skills meta-ads-*

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
Aceita `[brand]` e `[region]`. Default: `buzzmonitor brasil`.

| Comando | O que faz |
|---|---|
| `/news-pipeline [brand] [region]` | Pesquisa, gera 5 newsletters e revisa |
| `/news-pesquisar [brand] [region]` | So a pesquisa |
| `/news-gerar [brand] [region]` | So gera os rascunhos |
| `/news-revisar [brand] [region]` | So revisa os rascunhos |

- `[brand]`: `buzzmonitor` | `buzzcreators` | `cxpress` | `elife`
- `[region]`: `brasil` (PT-BR) | `latam` (ES-LATAM) | `portugal` (PT-PT)

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

### Landing Pages

Aceita `[marca]` e `[slug]`. Guidelines universais em `landing-pages/GUIDELINES.md`. Fonte em `landing-pages/{marca}/{slug}/`, deploy em pasta sibling isolada.

| Comando | O que faz |
|---|---|
| `/lp-pipeline [marca] [slug] [fonte] [dominio]` | Fluxo completo: preparar → gerar → revisar → (pausa) → publicar |
| `/lp-preparar [marca] [slug] [fonte]` | Estrutura copy crua em blocos rotulados + anti-IA |
| `/lp-gerar [marca] [slug]` | Gera HTML estatico invocando `frontend-design` |
| `/lp-revisar [marca]/[slug]` | Audita (design + a11y) e aplica criticos |
| `/lp-integrar-form [marca]/[slug] "snippet"` | Troca form mock por embed real (manual-trigger) |
| `/lp-publicar [marca] [slug] [dominio]` | Sync sibling + deploy Vercel + PageSpeed + relatorio Notion |

- `[marca]`: `buzzmonitor` | `buzzcreators` | `cxpress` | `elife`
- `[slug]`: kebab-case curto (ex: `monitoramento-maio`)
- `[fonte]`: URL Notion, caminho de arquivo ou texto colado

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
