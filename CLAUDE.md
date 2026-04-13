# Agente Inhouse — Grupo Elife

Este agente automatiza a criacao de newsletters, traducoes de copy, criacao de copy e analise de campanhas Meta Ads para as marcas do Grupo Elife: Buzzmonitor, Buzzcreators, Cxpress e Elife.

---

## Arquitetura

### Fluxo das Skills

```
Newsletters:  /news-pipeline → /news-pesquisar → /news-gerar → /news-revisar
Traducao:     /trad-pipeline → /trad-traduzir → /trad-revisar
Copywriting:  /copy-criar (standalone) | /copy-pesquisar → /copy-swipefile | /copy-revisar (standalone)
Meta Ads:     /meta-ads → fetch + report | /meta-ads-trends (standalone)
Calibracao:   /trad-calibrar (atualiza padroes linguisticos)
```

### Diretorios

| Diretorio | O que contem |
|---|---|
| `conhecimento/` | Base de conhecimento — fonte de verdade sobre produtos, copy, linguistica e editorial |
| `newsletter/` | Entregas de newsletters geradas (publicadas no Notion) |
| `traducao/` | Traducoes geradas (publicadas no Notion) |
| `meta-ads/` | Modulo Python de analise de campanhas (read-only) |
| `.claude/skills/` | Definicoes das skills e CONTEXT.md compartilhados |

### Contextos Compartilhados

Cada familia de skills tem um `CONTEXT.md` com marcas, regioes, caminhos e IDs do Notion:
- `.claude/skills/copy-criar/CONTEXT.md` — para skills copy-*
- `.claude/skills/news-pesquisar/CONTEXT.md` — para skills news-*
- `.claude/skills/trad-traduzir/CONTEXT.md` — para skills trad-*
- `.claude/skills/meta-ads/CONTEXT.md` — para skills meta-ads-*

### Versionamento

Cada skill tem `version` no frontmatter (semver simplificado). Mudanças vão em `CHANGELOG.md` no mesmo PR. Bump MAJOR ao quebrar interface da skill.

---

## Setup

### Meta Ads (unico que requer instalacao)
1. `cd meta-ads && python -m pip install -r requirements.txt`
2. Copiar `meta-ads/.env.example` para `meta-ads/.env` e preencher token + IDs de conta

### Notion
Requer MCP Notion conectado. IDs das pastas ja estao hardcoded nas skills e nos CONTEXT.md.

### Demais skills
Funcionam sem setup adicional.

---

## Comandos Disponiveis

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

Base de conhecimento: `conhecimento/copywriting/` (fundamentos, video-curto, estatico, email, funil)

### Meta Ads (SOMENTE LEITURA)

Requer Python 3.10+ e `meta-ads/.env` configurado (ver `.env.example`).

| Comando | O que faz |
|---|---|
| `/meta-ads [conta] [periodo]` | Pipeline completo: coleta + relatorio |
| `/meta-ads-fetch [conta] [periodo]` | So atualiza dados locais |
| `/meta-ads-report [conta] [periodo]` | So gera relatorio (sem nova coleta) |
| `/meta-ads-trends [conta]` | Tendencias temporais (3d/7d/15d/30d) |

- `[conta]`: `buzzmonitor_brl` | `buzzmonitor_usd` | `buzzmonitor_eur` | `cxpress_brl` | `cxpress_usd` | `cxpress_eur`
- `[periodo]`: `mes_atual` | `mes_anterior` | `ultimos_30`

**Primeira execucao:** `cd meta-ads && python -m pip install -r requirements.txt`
