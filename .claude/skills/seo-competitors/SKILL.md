---
name: seo-competitors
description: Análise mensal de tráfego orgânico dos concorrentes da Buzzmonitor via Semrush. Gera HTML comparativo com ranking, tendências de keywords e insights acionáveis para o time comercial.
argument-hint: "[regiao?] — br | latam | pt | all (default: all)"
allowed-tools: Read, Write, Artifact, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__execute_report, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__get_report_schema, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__domain_overview, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__organic_research
version: 1.1.0
---

# /seo-competitors — Análise Mensal de Concorrentes

## O que esta skill faz

Para cada região selecionada, coleta via Semrush MCP o tráfego orgânico e as principais keywords de cada concorrente configurado em `config.json`, compara com o posicionamento da Buzzmonitor e gera um HTML local com:

1. **Insights comerciais** (primeiro) — síntese acionável para o time comercial
2. **Ranking de tráfego** — todos os concorrentes + Buzzmonitor, com delta mês anterior
3. **Top keywords crescendo/caindo** — por concorrente
4. **Páginas com maior ganho/perda** — por concorrente
5. **Sobreposição de keywords** — onde Buzzmonitor e concorrente competem

O HTML é salvo em `~/.seo-report-buzzmonitor/` (mesmo WORK_DIR do `/seo-report`) e aberto no navegador.

---

## Passo 0 — Setup

**0.1 — Resolver região e mês**

- `[regiao]` — `br` | `latam` | `pt` | `all` (default: `all`)
- Mês de análise = mês atual. Mês anterior = mês imediatamente anterior.
- Formato de data para Semrush: `YYYYMM15` (ex: `20260915` para setembro/2026).

**0.2 — Ler config**

```
Read: .claude/skills/seo-competitors/config.json
```

**0.3 — Verificar seo_data.json (opcional, para enriquecimento)**

Verificar se existe `~/.seo-report-buzzmonitor/seo_data.json` (saída do `/seo-report`). Se existir e tiver menos de 30 dias, ler com Read — será usado no Passo 3 para cruzar keywords da Buzzmonitor. Se não existir, continuar normalmente; a skill coleta os dados da Buzzmonitor direto do Semrush.

---

## Passo 1 — Coleta Semrush

Para cada região a processar, montar a lista de domínios: **Buzzmonitor** (conforme `config.buzzmonitor.{regiao}`) + todos os concorrentes de `config.competitors.{regiao}`.

### 1.a — Snapshot atual de keywords (`resource_organic`)

Por domínio, **2 chamadas** (mês atual + mês anterior):

```json
{
  "target": "<domain>",
  "database": "<db>",
  "display_date": "<YYYYMM15>",
  "display_limit": 500,
  "display_sort": "traffic_desc",
  "export_columns": ["keyword", "position", "volume", "traffic", "url"]
}
```

- Dedupe por keyword (manter melhor posição por string normalizada lowercase/trim).
- Guardar ambos os snapshots para calcular delta.

> Se o schema divergir, chamar `get_report_schema(report="resource_organic")` antes do `execute_report`.

### 1.b — Keywords crescendo e caindo (`resource_organic`, `display_positions`)

Por domínio, **2 chamadas** (rise + fall), **só do mês atual**:

```json
{
  "target": "<domain>",
  "database": "<db>",
  "display_positions": "rise",
  "display_limit": 10,
  "display_sort": "traffic_desc",
  "export_columns": ["keyword", "position", "volume", "traffic", "url"]
}
```

Repetir com `display_positions: "fall"`.

### 1.c — Páginas que mais ranqueiam (`resource_organic_unique`)

Por domínio, mês atual:

```json
{
  "target": "<domain>",
  "database": "<db>",
  "display_limit": 10,
  "display_sort": "traffic_desc",
  "export_columns": ["url", "keywords_count", "traffic", "traffic_share"]
}
```

### 1.d — Overview de tráfego (`domain_overview`)

Por domínio, mês atual + mês anterior — para obter o tráfego orgânico estimado mensal e número total de keywords, usados no ranking geral.

> Se `domain_overview` não suportar `display_date`, usar os totais que vêm de 1.a (contagem de keywords do snapshot + soma de `traffic` das keywords).

### Ordem de chamadas

Processar região por região. Dentro de cada região, fazer todas as chamadas de um domínio antes de ir ao próximo — facilita identificar falhas isoladas sem perder dados já coletados.

Se algum domínio falhar (limite de unidades, timeout), registrar o erro e continuar com o restante — **nunca abortar toda a região por um domínio**.

---

## Passo 2 — Processamento e delta

Para cada domínio e região:

```
traffic_atual    = soma de `traffic` das keywords do snapshot atual (deduplicado)
traffic_anterior = soma de `traffic` das keywords do snapshot do mês anterior
delta_pct        = round(((traffic_atual - traffic_anterior) / traffic_anterior) * 100, 1)
                   — None se traffic_anterior = 0
keywords_atuais  = contagem de keywords únicas no snapshot atual
```

**Ranking por região:** ordenar todos os domínios (Buzzmonitor + concorrentes) por `traffic_atual` descrescente.

**Sobreposição com Buzzmonitor:** para cada concorrente, cruzar o set de keywords do snapshot atual com o da Buzzmonitor. Calcular:
- `overlap_count` = número de keywords em comum
- `overlap_sample` = as 10 com maior volume de busca em comum, com as posições de cada um

---

## Passo 3 — Geração de insights comerciais

Com todos os dados coletados, sintetizar os insights mais relevantes para o time comercial. Esta seção é narrativa — não é tabela.

Estrutura sugerida (adaptar ao que os dados mostrarem):

**Ameaças detectadas:** concorrentes com crescimento significativo de tráfego (>20% MoM) ou que entraram em keywords estratégicas da Buzzmonitor com posição melhor.

**Oportunidades de posicionamento:** concorrentes com queda de tráfego — leads que podem estar insatisfeitos. Mencionar o concorrente e o que está caindo (categoria, keywords).

**Keywords em disputa:** as principais keywords onde a Buzzmonitor e concorrentes se sobrepõem e onde a Buzzmonitor está atrás — prioridade para argumentação comercial.

**Movimento de mercado:** concorrentes que entraram em novas categorias de keyword (ex: concorrente de social listening passando a ranquear por "atendimento ao cliente" — sinal de expansão de produto).

**Tom:** direto e prático. Quem lê é o time comercial, não técnico. Focar em implicações de negócio, não em métricas de SEO brutas. Usar nomes reais dos concorrentes.

---

## Passo 4 — Gerar o HTML

HTML único com **abas por região** (BR / LATAM / PT). Dados embutidos como variáveis JS inline — sem CDN externo. O visual segue o mesmo padrão do dashboard gerado pelo `/seo-report` para manter consistência entre os relatórios.

### Paleta e estilo — dark mode comprometido (decisão da Bárbara, 2026-09-14)

O relatório usa **dark mode fixo** (não segue preferência do sistema — design intencional para consistência com o `/seo-report`).

- Fundo: `#0d1117` · Surface: `#161b22` · Surface2: `#1c2330`
- Bordas: `#2d3748`
- Texto principal: `#e6edf3` · Secundário: `#8d9aab` · Terciário: `#5a6680`
- Acento: `#4d94f0` (azul) · Fundo acento: `#162035` · Borda acento: `#2d5a9e`
- Crescimento: `#3fb950` (fundo `#0e2513`) · Queda: `#f85149` (fundo `#380d0d`)
- Font: Inter (Google Fonts) + system-ui como fallback
- **Tabs regionais:** botões com borda (`border: 1px solid var(--border)`), sem emoji, `border-radius: 8px`. Estado ativo: cor + borda + fundo do acento. Sem underline.
- **Cards de KPI:** fundo `--surface`, borda `--border`, radius 10px. Label uppercase cinza, valor grande bold, delta abaixo.
- **Badges de posição:**
  - `position = 0` → fora do Top 100 (fundo `--surface2`, texto `--text2`) — NUNCA tratar como Top 3
  - 1–3 → fundo `#166534`, texto branco
  - 4–10 → fundo `#1e3a8a`, texto branco
  - 11–20 → fundo `#374151`, texto branco
  - > 20 → fundo `--surface2`, texto `--text2`
- **Linha da Buzzmonitor** nas tabelas: fundo `--bm-bg` (#162035) + badge "BM" em `--bm` (#4d94f0)

### Estrutura de cada aba (por região) — ordem definida pela Bárbara em 2026-09-14

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER: "Buzzmonitor · Concorrentes SEO"                   │
│  Tabs: [Brasil] [LATAM] [Portugal] — botões, sem emoji      │
│  Badges: "Semrush" · "Ref: Mês Ano" · "Gerado em {data}"   │
├─────────────────────────────────────────────────────────────┤
│  1. INSIGHTS COMERCIAIS (sempre primeiro)                    │
│     Card com fundo --accent-l + borda 2px --accent-b        │
│     4 subseções: Ameaças · Oportunidades · Keywords · Mercado│
├─────────────────────────────────────────────────────────────┤
│  2. KPI ROW (big numbers)                                    │
│     Concorrentes monitorados · Maior crescimento ·          │
│     Maior queda · Buzzmonitor {região}                      │
├─────────────────────────────────────────────────────────────┤
│  3. SOBREPOSIÇÃO COM BUZZMONITOR (antes do ranking)         │
│     Grid de cards com overlap por concorrente-chave +       │
│     card de vantagem exclusiva BM                           │
├─────────────────────────────────────────────────────────────┤
│  4. KEYWORDS EM MOVIMENTO (antes do ranking)                │
│     Gráfico de barras divergente horizontal (Chart.js CDN)  │
│     Sublabel: "Variação de tráfego orgânico MoM —           │
│       priority 1 · banco {BR|MX|PT}"                        │
│     Barras: verde (crescimento) / vermelho (queda) /        │
│       cinza (#5a6680) para contexto (ex: Harmo anomalia)    │
│     Ordenação: menor delta no topo → maior no fundo         │
│     Outlier extremo (ex: Brandwatch +360% LATAM): cap       │
│       visual no eixo X, label mostra valor real com "↑"     │
│     Cards de keywords abaixo do gráfico (só quem tem dado)  │
│     Decisão da Bárbara: 2026-09-14                          │
├─────────────────────────────────────────────────────────────┤
│  5. RANKING DE TRÁFEGO ORGÂNICO (depois das seções acima)   │
│     Tabela: # · Marca · Categoria · Tráfego Est. · Δ MoM   │
│     · Keywords · Linha BM destacada                         │
├─────────────────────────────────────────────────────────────┤
│  6. POSICIONAMENTO DA BUZZMONITOR (por último)               │
│     Top keywords orgânicas + top páginas por tráfego        │
└─────────────────────────────────────────────────────────────┘
```

### Regras de formatação de números (idêntico ao /seo-report)

- Tráfego ≥ 1.000.000 → `X.XM` · ≥ 1.000 → `X.Xk` · < 1.000 → número direto
- Delta: `▲ +X.X%` verde · `▼ -X.X%` vermelho · `—` se sem dado anterior
- URLs: truncar em 60 chars com `…`, title com URL completa no hover
- Concorrente sem dados Semrush: linha com "⚠️ Sem dados" — nunca omitir da tabela

---

## Passo 5 — Publicar como Artifact

**Não salvar como arquivo local** — publicar diretamente como Artifact para gerar um link compartilhável por e-mail ou chat.

1. Escrever o HTML gerado em arquivo temporário no scratchpad da sessão (ex: `{scratchpad}/competitors-{YYYY-MM}.html`).
2. Publicar via ferramenta `Artifact`:
   - `file_path`: o arquivo temporário do passo anterior
   - `title`: `"Concorrentes SEO — {Mês Ano}"` (ex: `"Concorrentes SEO — Setembro 2026"`)
   - `description`: `"Análise mensal de tráfego orgânico dos concorrentes da Buzzmonitor — BR, LATAM e PT"`
   - `icon`: `"chart"` (só na primeira publicação do mês; redeploys omitem para manter o ícone)
3. Retornar o link do Artifact para a Bárbara compartilhar por e-mail.

**Redeploy no mesmo mês:** se já existe um Artifact de concorrentes do mês atual (URL guardada na conversa ou via `Artifact action: "list"`), republicar no mesmo URL em vez de criar um novo — o link enviado aos destinatários continua funcionando.

---

## Integração com `/seo-report`

Se `seo_data.json` existir e for recente (< 30 dias):
- Usar `contexts.buzzmonitor-{regiao}.gsc.top_keywords` (se disponível) para enriquecer a seção de sobreposição com dados reais de clique/impressão das keywords onde a BM aparece, complementando o dado do Semrush.
- Não é obrigatório — o relatório funciona 100% só com Semrush. A integração adiciona contexto quando disponível.

---

## Exemplos de uso

```
/seo-competitors
# → processa as 3 regiões (BR + LATAM + PT), gera HTML com abas

/seo-competitors br
# → só Brasil, mais rápido para análise focada

/seo-competitors latam
# → só LATAM
```

---

## Notas técnicas

- **Semrush sem projeto:** toda a coleta usa APIs de domínio (`resource_organic`, `resource_organic_unique`, `domain_overview`) que não exigem projeto criado no Semrush — adequado ao plano atual.
- **Database por região:** BR = `br` · LATAM = `mx` · PT = `pt` (mesmo mapeamento do `/seo-report`).
- **Buzzmonitor LATAM/PT:** alvo é a subpasta (`getbuzzmonitor.com/es/` / `/pt/`), não o domínio raiz — concorrentes usam domínio raiz normalmente.
- **Dedupe obrigatório:** a mesma keyword pode aparecer várias vezes (uma por URL que ranqueia) — deduplicar por keyword mantendo a melhor posição antes de qualquer contagem ou comparação.
- **position = 0 no bucket `fall`/`lost`:** significa "fora do Top 100", nunca tratar como posição 1–3.
- **Limitar chamadas:** com até 26 domínios no BR + 23 no LATAM + 9 no PT, o volume de chamadas é alto. Se as unidades Semrush estiverem baixas, priorizar priority 1 e perguntar antes de processar priority 2.
