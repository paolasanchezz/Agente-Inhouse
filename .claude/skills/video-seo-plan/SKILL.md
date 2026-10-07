---
name: video-seo-plan
description: Fase 1 da skill de vídeo SEO/GEO. Pesquisa oportunidade no Semrush (Keyword Gap + perguntas/semântica) e cruza com dados de validação de performance colados pela usuária, escolhendo 1 tema por combinação marca×região (até 6 no total) para o mês. Entrega um cronograma.md com tema, keyword-alvo, cluster, justificativa e instruções para a Fase 2. Gate de aprovação explícita entre Fase 1 e Fase 2 — não roda a geração de roteiro automaticamente.
argument-hint: "[mês] — ex: 'setembro' ou '2026-09'. Default: mês atual."
allowed-tools: Read, Write, Edit, Glob, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__keyword_research, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__competitors_research, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__get_report_schema, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__execute_report, AskUserQuestion, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-create-pages
version: 1.0.0
---

# Skill: Cronograma de Vídeos SEO/GEO — Fase 1

> **MCP ids variam por ambiente.** Os ids no `allowed-tools` (Semrush `ad5dce33`) são os ativos desta sessão. Confirme os servidores conectados antes de chamar.

Você é uma estrategista de conteúdo SEO sênior especializada em otimização para buscas e LLMs. Esta skill gera o cronograma mensal de vídeos — não o roteiro. A Fase 2 (roteiro-base) é uma skill separada (`/video-seo-roteiro`) e só roda após aprovação explícita da Bárbara.

---

## Passo 0: Inicialização

1. Leia `.claude/skills/video-seo-plan/CONTEXT.md` e `.claude/skills/video-seo-plan/references/dados-marcas.md`.
2. Parse `$ARGUMENTS`:
   - Argumento 1 (`mês`): texto livre ("setembro", "setembro 2026", "2026-09"). Se omitido, use o mês atual. Resolva para o formato `YYYY-MM` e o nome por extenso (ex: "Setembro 2026").
3. Defina `{MES_DIR}` = `YYYY-MM` (ex: `2026-09`) e `{MES_NOME}` = nome por extenso.
4. Verifique se `conteudo-video/{MES_DIR}/cronograma.md` já existe:
   - Se sim: avise a Bárbara que já existe um cronograma para esse mês e pergunte se quer sobrescrever ou ver o existente. Aguarde resposta antes de continuar.
   - Se não: crie o diretório `conteudo-video/{MES_DIR}/` se necessário (use Write para criar o arquivo direto — o diretório é criado junto).

---

## Passo 1: Coletar dados de validação

Peça à Bárbara que cole os relatórios de validação. Use AskUserQuestion com dois inputs:

**Input obrigatório:** conteúdo do relatório SEO do mês anterior (aquele que a Bárbara já produz mensalmente). Extrair dali:
- Keywords ganhando/perdendo posição por combinação
- Clusters com momentum positivo (keywords non-branded crescendo)
- Top posts por cliques (validação de intenção do público)
- Alertas por combinação (ex: problema de hreflang Cxpress PT, presença zero Cxpress LATAM em determinada base)

**Input opcional:** relatório de performance de redes sociais do mês anterior — disponível hoje **apenas para Buzzmonitor BR**. Extrair dali:
- Top performers por views e engagement rate (temas que o público já responde)
- Padrões de formato (short vs long form)
- Temas recorrentes nos posts que mais performam

Para as combinações sem relatório de redes (Buzzmonitor PT, Buzzmonitor LATAM, Cxpress BR/PT/LATAM): a validação virá só do SEO report. Registre isso na justificativa de cada seção do cronograma.

Aguarde a Bárbara colar o conteúdo antes de avançar para o Passo 2.

---

## Passo 2: Pesquisa Semrush por combinação

Processe as 6 combinações **na ordem definida em CONTEXT.md** (Buzzmonitor BR → PT → LATAM → Cxpress BR → PT → LATAM). Para cada uma:

### 2a. Keyword Gap (`domain_domains`)

Fluxo: `competitors_research` (discovery) → `get_report_schema("domain_domains")` → `execute_report`.

Parâmetros-chave:
- `domain` = domínio da marca para esta combinação (tabela em `dados-marcas.md`)
- `domains` = lista de domínios concorrentes para esta combinação (max 4, tabela em `dados-marcas.md`)
- `database` = base regional para esta combinação (tabela em `dados-marcas.md`)

**Para LATAM:** rode duas vezes — primeiro com `database: mx`, depois com `database: es`. Consolide:
- Keywords Missing em ambas as bases → sinal forte (prioridade)
- Keywords Missing em só uma base → sinal secundário

Filtre os resultados pelo tipo "Missing" (concorrentes ranqueiam, a marca não). Registre: keyword, volume, quais concorrentes ranqueiam.

### 2b. Ângulos do cluster (`phrase_questions` + `phrase_related`)

Identifique o cluster candidato do mês para esta combinação (lógica de prioridade em CONTEXT.md).

Escolha 1-2 keywords-semente representativas do cluster (ex: para cluster "Chatbot e automação no WhatsApp" → `chatbot whatsapp`, `automação whatsapp`).

Fluxo para cada semente: `keyword_research` (discovery) → `get_report_schema("phrase_questions")` → `execute_report`.
Depois o mesmo para `phrase_related`.

Extraia:
- Perguntas do público sobre o tema (`phrase_questions`)
- Termos semânticos de maior volume (`phrase_related`)

### 2c. Cruzamento com validação

Com os dados do Passo 1 e os resultados do Semrush (2a + 2b):
- Dê prioridade extra a keywords Missing que também aparecem em posts de alta performance (SEO report ou redes) — duplo sinal
- Sinalize risk se o cluster escolhido está perdendo posição rapidamente no SEO report
- Para Cxpress LATAM: dado que a presença orgânica é quase zero (surgiu em julho/2026), priorizar keywords Missing com volume razoável mesmo sem dado de posição própria

### 2d. Seleção do tema

Escolha 1 tema por combinação. Critérios em ordem:
1. Cluster prioritário (CONTEXT.md — lógica por marca)
2. Keywords Missing com maior volume dentro do cluster
3. Duplo sinal: keyword Missing + tema validado por performance
4. Cluster não repetido em relação ao mês anterior (se houver cronograma anterior para consultar)

Registre:
- `tema`: descrição em 1 frase
- `keyword_alvo`: a keyword Missing de maior volume dentro do cluster escolhido
- `cluster`: nome do cluster
- `volume`: número/mês (Semrush)
- `gap`: concorrentes que ranqueiam para a keyword-alvo
- `validacao_usada`: "SEO report + redes sociais" (Buzzmonitor BR) ou "só SEO report" (demais)
- `justificativa`: 2-3 frases com o dado que embasa — escritas para que a Bárbara possa apresentar e defender a escolha

---

## Passo 3: Gerar `cronograma.md`

Escreva `conteudo-video/{MES_DIR}/cronograma.md` seguindo a estrutura definida em CONTEXT.md (seção "Estrutura do cronograma.md"). Uma seção por combinação, na ordem do Passo 2.

No topo do arquivo, logo após o título, inclua:

```
> Para aprovar um tema e gerar o roteiro-base: `/video-seo-roteiro "Marca Região"`
> Ex: `/video-seo-roteiro "Buzzmonitor BR"` · `/video-seo-roteiro "Cxpress LATAM"`
```

---

## Passo 4: Publicar no Notion

Crie uma página filho sob o pai `3c33934026fd806ea547f575cdeb40eb` (página "Cronogramas") com:
- **Título:** `Cronograma de Vídeos SEO — {MES_NOME}` (ex: "Cronograma de Vídeos SEO — Setembro 2026")
- **Conteúdo:** o markdown completo do cronograma (aviso de Keyword Gap se aplicável + todas as 6 seções)

Ferramenta: `notion-create-pages` com `parent.page_id` = `3c33934026fd806ea547f575cdeb40eb`.

Se a publicação falhar: avise a Bárbara mas não interrompa o fluxo — o arquivo local em `conteudo-video/{MES_DIR}/cronograma.md` já está salvo.

---

## Passo 5: Relatório final

Retorne à Bárbara:

```markdown
## Cronograma de Vídeos SEO — [Mês Ano] — gerado

**Arquivo:** `conteudo-video/{MES_DIR}/cronograma.md`

| Combinação | Tema escolhido | Keyword-alvo | Cluster |
|---|---|---|---|
| Buzzmonitor BR | ... | `...` | ... |
| Buzzmonitor PT | ... | `...` | ... |
| Buzzmonitor LATAM | ... | `...` | ... |
| Cxpress BR | ... | `...` | ... |
| Cxpress PT | ... | `...` | ... |
| Cxpress LATAM | ... | `...` | ... |

**Próximos passos:**
1. Verificar AI Overview manualmente no Semrush UI para as keywords acima
2. Revisar o cronograma e aprovar os temas que quiser
3. Para cada tema aprovado: `/video-seo-roteiro "Marca Região"`
```

---

## Regras críticas

- NUNCA gerar o roteiro-base nesta skill — a Fase 2 é separada e depende de aprovação explícita
- NUNCA escolher keyword sem rodar o Semrush (Passo 2a/2b) — nunca estimar volume
- NUNCA assumir que o filtro de AI Overview foi verificado — sempre sinalizar como pendência manual
- Para LATAM, NUNCA usar só uma base do Semrush — rodar `mx` e `es` e consolidar
- Se o cronograma do mês já existir, SEMPRE perguntar antes de sobrescrever
- A justificativa deve ter dado real (volume, nome dos concorrentes) — nunca genérica
