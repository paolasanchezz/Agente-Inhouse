# Contexto Compartilhado — video-seo-plan / video-seo-roteiro

> Lido por ambas as skills da família: `/video-seo-plan` (Fase 1) e `/video-seo-roteiro` (Fase 2).

---

## Escopo e origem

Skill criada em agosto/2026 para gerar cronograma mensal de vídeos SEO/GEO e roteiros-base para Buzzmonitor e Cxpress nas três regiões. Escopo definido pelo Victor: 2 vídeos/mês = 3 entregáveis por tema (YouTube longo + Shorts + Reel). Calendário da primeira leva: roteiros prontos até fim de agosto/2026, produção em setembro, publicação em outubro.

Dados de referência (clusters, concorrentes, domínios, bases Semrush, responsáveis): `references/dados-marcas.md`.

---

## Caminhos de saída

| Arquivo | Caminho |
|---|---|
| Cronograma mensal (Fase 1) | `conteudo-video/YYYY-MM/cronograma.md` |
| Roteiro-base por combinação (Fase 2) | `conteudo-video/YYYY-MM/roteiros/{marca-regiao}.md` |

**Mapeamento de argumento → slug de arquivo:**

| Argumento | Slug do arquivo |
|---|---|
| `"Buzzmonitor BR"` | `buzzmonitor-br` |
| `"Buzzmonitor PT"` | `buzzmonitor-pt` |
| `"Buzzmonitor LATAM"` | `buzzmonitor-latam` |
| `"Cxpress BR"` | `cxpress-br` |
| `"Cxpress PT"` | `cxpress-pt` |
| `"Cxpress LATAM"` | `cxpress-latam` |

---

## Dados de validação (Fase 1)

### Fonte e formato

A Bárbara cola o conteúdo dos relatórios diretamente no chat ao rodar `/video-seo-plan`. Não há fetch automático.

**Relatório SEO mensal** (obrigatório): cobre todas as 6 combinações. Formato: markdown estruturado com tabelas de keywords, posições, tendências, top posts, análise por propriedade. Exemplo: "Relatório SEO — Julho 2026" no Notion.

**Relatório de redes sociais** (opcional, só disponível para Buzzmonitor BR): gerado pelo `/social-plan`, contém top performers por views/engagement rate/saves, performance por formato, padrões temáticos. Para as outras 5 combinações, esse dado não existe — a skill usa apenas o SEO report como validação e deixa isso explícito na justificativa.

### Sinais a extrair do relatório SEO

- Keywords ganhando posição → cluster com momentum positivo
- Keywords perdendo posição → risco de canibalizaçãose escolhermos esse cluster
- Cluster com maior volume de keywords non-branded → mais potencial de audiência nova
- Top posts por cliques → temas que o público já procura (validação de intenção)
- Notas editoriais específicas por combinação (ex: problema de hreflang Cxpress PT, presença quase zero Cxpress LATAM)

### Sinais a extrair do relatório de redes sociais (Buzzmonitor BR)

- Top performers por views e engagement rate → formato/tema que o público já responde
- Performance por formato → preferência de short vs long form
- Padrões temáticos confirmados → âncora para o tema de vídeo

---

## Disponibilidade das ferramentas Semrush

| Ferramenta descrita no briefing | Status no MCP | Toolkit / Report |
|---|---|---|
| Keyword Gap | Disponível | `competitors_research` → `domain_domains` |
| Topic Research | Não exposto | Substituído por `phrase_questions` + `phrase_related` |
| Keyword Magic Tool | Disponível | `keyword_research` → `phrase_questions`, `phrase_related`, `phrase_related` |
| Filtro SERP Feature = AI Overview | Não disponível | Verificação manual pela Bárbara no Semrush UI |

---

## Coexistência com `/social-plan`

O `/social-plan` existe em produção para Buzzmonitor BR e gera planejamento editorial mensal para redes sociais (o que postar). Esta skill usa o relatório de performance de redes como **sinal de validação** para escolher o tema de vídeo — são papéis distintos (analítico vs. planejamento). A sobreposição real, se houver, ficará clara quando a responsável de conteúdo confirmar o fluxo de trabalho. Em aberto: confirmar com a responsável do `/social-plan` se esta skill complementa ou substitui alguma etapa.

---

## Ordem de processamento das combinações (Fase 1)

Processar sempre nesta ordem:
1. Buzzmonitor BR
2. Buzzmonitor PT
3. Buzzmonitor LATAM
4. Cxpress BR
5. Cxpress PT
6. Cxpress LATAM

---

## Prioridade de cluster por mês (lógica de seleção)

**Cxpress (todas as regiões):** cluster 3 (Chatbot e automação) tem prioridade máxima; depois cluster 1 (WhatsApp empresarial). Só ir para clusters 4 ou 2 se 3 e 1 já tiverem sido cobertos em meses anteriores ou se o gap for claramente mais forte em outro cluster.

**Buzzmonitor (todas as regiões):** selecionar o cluster com maior número de keywords "Missing" no Keyword Gap daquele mês — sem ordem fixa de prioridade entre os 5 clusters. Desempate: cluster não usado no mês anterior (consultar cronograma anterior se existir).

---

## Notion — IDs de publicação

| Entrega | Página pai no Notion | ID |
|---|---|---|
| Cronograma mensal (Fase 1) | Cronogramas | `3c33934026fd806ea547f575cdeb40eb` |
| Roteiro-base por combinação (Fase 2) | Roteiros | `3c33934026fd80138da3ce090c91b46e` |

- Título da página de cronograma: `Cronograma de Vídeos SEO — [Mês Ano]`
- Título da página de roteiro: `[Marca] [Região] — [Tema curto] — [Mês Ano]`

---

## Estrutura do `cronograma.md`

```markdown
# Cronograma de Vídeos SEO — [Mês Ano]

> Gerado em: [data] | Skill: /video-seo-plan v[X.X.X]
> Para aprovar um tema e gerar o roteiro-base: `/video-seo-roteiro "Marca Região"`

---

## [Marca] [Região]

**Cluster:** [nome do cluster]
**Tema:** [descrição do tema em 1 frase]
**Keyword-alvo:** `[keyword]`
**Volume:** [N]/mês (Semrush, base `[db]`)
**Gap:** Missing em [concorrentes que ranqueiam]
**Validação:** [SEO report + redes sociais Buzz BR / só SEO report]
**Justificativa:** [2-3 frases com o dado que embasa a escolha]
**AI Overview:** verificar manualmente no Semrush UI para `[keyword]`
**Entregáveis:** Vídeo longo YouTube · YouTube Shorts · Reel (IG/FB/TikTok)
**Responsável:** [nome]

---
```

---

## Estrutura do roteiro-base (`roteiros/{marca-regiao}.md`)

```markdown
# Roteiro-base — [Tema]
**Marca/Região:** [Marca] [Região] | **Cluster:** [cluster] | **Keyword-alvo:** `[keyword]`
*Gerado em: [data] | Skill: /video-seo-roteiro v[X.X.X]*

---

## Vídeo YouTube (horizontal)

## Opções de título (3 variações)

1. [Título 1]
2. [Título 2]
3. [Título 3]

## Abertura (primeiros 10-15 segundos)

[Script da abertura]

## Estrutura de tópicos

1. **[Tópico 1]** — keyword secundária: `[X]`
   [Descrição do que cobrir]

2. **[Tópico 2]** — keyword secundária: `[Y]`
   [Descrição do que cobrir]

[...]

## Definição citável

> [Frase isolada e clara, em formato que uma IA generativa citaria como resposta direta]

## Sugestão de descrição YouTube

[Parágrafo — aprofunda com keywords relacionadas, não só repete o título]

## Corte para Shorts/Reel (vertical)

**Opção A — [Trecho/tempo do vídeo longo]**
**Frase inicial (Reel/Shorts):** [Frase já escrita no estilo Reel — gancho de dor ou afirmação forte, sem intro]
**Desenvolvimento (corte do vídeo longo):** [Quais tópicos/momentos compõem o meio do Reel — nome do tópico + tempo aprox.]
**CTA final:** [Frase de encerramento acionável, 3-5 seg]
**Legenda:** [Sugestão de legenda com keyword natural + 2-3 hashtags]
**Thumb:** [Frase curta para thumbnail — máx. 5-6 palavras, keyword + dor, caixa alta]
**Gancho:** [Por que essa seleção funciona como peça autônoma]

---

**Opção B — [Trecho/tempo]** *(se houver segundo candidato forte)*
**Frase inicial (Reel/Shorts):** [Frase já escrita no estilo Reel]
**Desenvolvimento (corte do vídeo longo):** [Tópicos/momentos do meio]
**CTA final:** [Frase de encerramento]
**Legenda:** [Legenda com keyword + hashtags]
**Thumb:** [Frase curta para thumbnail]
**Gancho:** [Por que funciona como peça autônoma]

---

*Próximo passo: entregar este roteiro-base para [Responsável] adaptar para linguagem, tom e produção de cada rede.*
```
