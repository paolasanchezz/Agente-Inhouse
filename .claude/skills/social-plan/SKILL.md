---
name: social-plan
description: Gera planejamento editorial mensal para as redes sociais da Buzzmonitor (LinkedIn, Instagram, Facebook) com pesquisa de perfis de referência, tendências virais do nicho e calendário detalhado organizado por rede. Publicado no Notion em "Redes Sociais".
argument-hint: "[mes] — ex: junho | junho 2026 | 2026-06 (default: mês atual)"
allowed-tools: WebFetch, WebSearch, Read, Write, Edit, Agent, Bash, Glob, Grep, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-fetch, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-search, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-pages, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-database, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-view
version: 1.0.0
---

# Skill: Planejamento Editorial de Redes Sociais — Buzzmonitor

Você é um estrategista sênior de conteúdo especializado em social media B2B para SaaS. Sua missão é criar um planejamento editorial mensal completo para as redes sociais da Buzzmonitor (LinkedIn, Instagram, Facebook), fundamentado em pesquisa real de referências do setor e tendências virais do nicho.

## Passo 0: Parsing de Argumentos

Faça o parsing de `$ARGUMENTS`:
- **Argumento 1** (`mes`): mês de referência — default: mês atual
  - Aceitar formatos: `2026-06`, `junho`, `junho 2026`, `06/2026`
  - Calcular `{MES_NOME}` = nome do mês em PT-BR (ex: "Junho")
  - Calcular `{ANO}` = ano de 4 dígitos (ex: "2026")
  - Calcular `{YYYYMM}` = formato compacto (ex: "2026-06")
  - Calcular as datas do mês: primeiro dia, último dia, dias da semana

## Passo 1: Carregar Contexto de Marca

Leia os seguintes arquivos:

1. `brand/buzzmonitor/brand-manifest.json` — tom de voz, pilares de messaging, público-alvo
2. `conhecimento/produto/buzzmonitor/buzzmonitor.md` — produto, features, diferenciais, casos de uso
3. `conhecimento/produto/buzzmonitor/concorrentes.md` — mapa competitivo

Extraia e guarde:
- **PilaresDeMessaging**: lista de `voice.messagingPillars`
- **PublicoAlvo**: segmentos em `audience.segments`
- **Diferenciais**: `positioning.differentiators`
- **TomDeVoz**: `voice.toneAttributes` e `voice.personality`
- **ConcorrentesLista**: nomes dos principais concorrentes

## Passo 2: Pesquisa (4 agentes em paralelo)

Lance 4 agentes de pesquisa em paralelo. Cada agente salva seu output em arquivos temporários para consolidação no Passo 3.

### Agente 1 — Concorrentes nas Redes Sociais

Para cada concorrente em `ConcorrentesLista`, pesquise a presença deles nas redes:
- WebSearch: `"{concorrente}" site:linkedin.com conteúdo` e `"{concorrente}" Instagram social listening`
- Identifique quais formatos usam (carrossel, reels, texto longo, infográfico, vídeo)
- Quais temas abordam com mais frequência
- Que tipo de post gera mais engajamento (quando visível)

Foco especial em ferramentas como: Sprinklr, Brandwatch, Mention, Talkwalker, mLabs, Etus — que atuam no mesmo nicho de social listening / gestão de redes.

Salve em `social-media/buzzmonitor/{YYYYMM}/pesquisa/concorrentes.md`.

### Agente 2 — Perfis de Referência B2B SaaS

Pesquise perfis que fazem excelente conteúdo de social media B2B no nicho de marketing e tecnologia:

- **HubSpot** (LinkedIn, Instagram) — referência mundial em educational content B2B
- **Sprout Social** (LinkedIn) — dados sobre comportamento em redes sociais
- **Buffer** (LinkedIn, Instagram) — transparência, conteúdo educativo e bastidores
- **RD Station** (LinkedIn, Instagram) — referência brasileira em MarTech

Para cada um, via WebSearch e WebFetch quando possível:
- Top 3 formatos mais usados por rede
- Temas e ângulos com mais engajamento
- Cadência de publicação
- Tipo de hook e legenda que funcionam

Salve em `social-media/buzzmonitor/{YYYYMM}/pesquisa/referencias.md`.

### Agente 3 — Tendências Virais do Nicho

Pesquise tendências de conteúdo para B2B em social media em 2025/2026:

Queries sugeridas:
- `"LinkedIn B2B tendências 2026"` e `"formatos virais LinkedIn marketing"`
- `"social listening trends 2026"` e `"IA marketing redes sociais conteúdo"`
- `"Instagram B2B SaaS conteúdo 2026"` e `"carrossel LinkedIn viral marketing analytics"`
- Em inglês: `"B2B social media trends 2026"` e `"viral LinkedIn posts marketing technology"`

Fontes prioritárias: Social Media Today, Sprout Social Blog, LinkedIn Marketing Solutions Blog, Resultados Digitais, Rock Content, HubSpot Blog.

Identifique:
- Formatos em alta por rede (LinkedIn vs Instagram vs Facebook)
- Gatilhos de engajamento que funcionam no nicho B2B
- Temas específicos que viralizam no setor de marketing/tecnologia
- Mudanças de algoritmo relevantes

Salve em `social-media/buzzmonitor/{YYYYMM}/pesquisa/tendencias.md`.

### Agente 4 — Blog Buzzmonitor: Conteúdo Reutilizável

Use WebFetch em `https://buzzmonitor.com.br/blog/` e WebSearch `site:buzzmonitor.com.br/blog` para:
- Mapear os 15 posts mais recentes ou mais relevantes (título, URL, tema central)
- Categorizar por tema: social listening, IA, atendimento, analytics, gestão de redes, cases
- Para cada post, sugerir como adaptar para cada rede social (LinkedIn, Instagram, Facebook)
- Identificar posts evergreen que valem ser transformados em série de conteúdo

Salve em `social-media/buzzmonitor/{YYYYMM}/pesquisa/blog-reutilizavel.md`.

## Passo 3: Sintetizar Insights e Definir Estratégia

Com os 4 arquivos de pesquisa em mãos, sintetize:

### 3.1 Pilares de Conteúdo do Mês (3-4 pilares)

Combine os pilares de messaging da marca com as oportunidades identificadas na pesquisa. Cada pilar deve ter:
- **Nome**: curto e memorável
- **Descrição**: o que engloba, para quem fala
- **Distribuição**: % aproximado dos posts do mês

Pilares base da Buzzmonitor (ajustar conforme pesquisa):
- **Educação & Insights**: tendências de mercado, dados, benchmarks, dicas práticas de social listening/analytics
- **Produto & Cases**: use cases reais, demonstrações de funcionalidades, resultados de clientes
- **Comunidade & Debate**: perguntas ao público, opiniões sobre o setor, polls, temas controversos de marketing/CX
- **Bastidores & Equipe**: lado humano da empresa, processo, cultura, transparência

### 3.2 Temas de Oportunidade do Mês (4-6 temas)

Identifique temas específicos para {MES_NOME} {ANO}:
- Datas relevantes do setor (Dia do Marketing, eventos de social media, etc.)
- Tendências quentes identificadas na pesquisa que a Buzzmonitor pode comentar com autoridade
- Ganchos de notícias do mercado de IA, marketing analytics ou redes sociais
- Benchmarks ou dados recentes que a Buzzmonitor pode contextualizar

### 3.3 Formato por Rede

Com base na pesquisa, defina os formatos prioritários:

| Rede | Formatos Prioritários | Melhor Horário (estimado) | Cadência |
|------|----------------------|--------------------------|----------|
| LinkedIn | Carrossel, texto longo, infográfico, vídeo nativo | Ter-Qui 8h-10h | 3x/semana |
| Instagram | Carrossel, Reels, Stories, post estático | Ter-Sex 11h-13h | 3x/semana |
| Facebook | Post com imagem, vídeo curto, link com preview | Ter-Qui 12h-14h | 3x/semana |

## Passo 4: Gerar Calendário Editorial Completo

Gere o planejamento completo do mês: 3 posts fixos por semana por rede + 2-3 slots de oportunidade.

**Distribuição de datas**: use segunda, quarta e sexta como dias padrão. Para LinkedIn evitar sexta à tarde. Distribuir os dias de forma que as 3 redes não publiquem sempre no mesmo dia (escalonar quando possível).

**Repetição temática entre redes**: o mesmo tema pode aparecer nas 3 redes na mesma semana, mas com formato e linguagem OBRIGATORIAMENTE diferentes:
- LinkedIn: mais técnico, texto mais longo, dados e insights, tom profissional
- Instagram: visual em primeiro lugar, legenda mais curta e leve, emojis com moderação
- Facebook: equilíbrio entre os dois, foco em comunidade, estimular comentários

Para cada post, preencha todos os campos abaixo:

```
### Post [N] — [Rede] — [Data sugerida]
- **Pilar**: [nome do pilar]
- **Tema**: [tema específico e descritivo]
- **Formato**: Carrossel | Reels | Estático | Vídeo curto | Texto longo | Infográfico | Stories | Poll
- **Hook / Primeira linha**: [frase que para o scroll — máx 15 palavras]
- **Briefing**: [3-5 bullets descrevendo o conteúdo, ângulo, pontos principais e referências do blog quando aplicável]
- **Por que engaja**: [1 frase — qual gatilho: curiosidade, utilidade, dado surpreendente, polêmica, identificação, humor]
- **Tipo**: Fixo | Oportunidade
- **Referência de blog**: [URL do post da Buzzmonitor que embasa o conteúdo, se aplicável]
```

**Distribuição semanal sugerida**:
- Semana 1 (dias 1-7): abertura do mês — tema educacional forte + pilar de engajamento
- Semana 2 (dias 8-14): profundidade + produto — conteúdo mais técnico e cases
- Semana 3 (dias 15-21): comunidade + debate — perguntas, dados, temas controversos
- Semana 4 (dias 22-28): retrospectiva + próximos passos — síntese do mês e antecipação

**Slots de oportunidade** (2-3): deixar explicitamente sem conteúdo definido, apenas com o tema de oportunidade identificado e instrução de como preenchê-los quando o momento chegar.

## Passo 5: Publicar no Notion

Leia `conhecimento/config/notion-ids.md` e use a chave `redes-sociais`.

### 5.1 — Criar a página principal do planejamento

**Título da página**: `Planejamento Redes Sociais · Buzzmonitor · {MES_NOME} {ANO}`

Estrutura da página no Notion:

```markdown
# Planejamento Editorial — Buzzmonitor
## {MES_NOME} {ANO}

**Gerado em**: {data atual}
**Total de posts planejados**: N (LinkedIn: N | Instagram: N | Facebook: N)
**Slots de oportunidade**: N em aberto

---

## Resumo Estratégico

[2-3 parágrafos: contexto do mês, oportunidades identificadas na pesquisa, foco estratégico]

## Pilares de Conteúdo

### Pilar 1 — [Nome]
[Descrição + distribuição estimada]

### Pilar 2 — [Nome]
...

## Insights da Pesquisa

### O que os concorrentes estão fazendo
- [3-4 bullets com padrões observados]

### O que as referências fazem de melhor
- [3-4 bullets com o que o HubSpot, Buffer, RD Station fazem e que a Buzzmonitor pode adaptar]

### Tendências do nicho para este mês
- [3-4 bullets com as tendências mais relevantes]

## Temas de Oportunidade

[Lista dos temas quentes do mês com contexto]

---

## 📅 Calendário Visual

> O calendário interativo está logo abaixo (database com visualização em calendário).
> Cada card representa um post com data, rede, formato e tema.

---

## Calendário Editorial Detalhado

### LinkedIn (3x/semana)

[Posts detalhados do LinkedIn em ordem cronológica]

---

### Instagram (3x/semana)

[Posts detalhados do Instagram em ordem cronológica]

---

### Facebook (3x/semana)

[Posts detalhados do Facebook em ordem cronológica]

---

## Slots de Oportunidade (em aberto)

[2-3 slots com tema sugerido e instrução de como ativar com /copy-criar quando o momento chegar]

---

*Planejamento gerado pelo Agente Inhouse (social-plan v1.1.0)*
*Para criar a copy de qualquer post, use: `/copy-criar buzzmonitor brasil [tipo] [estagio] "[tema do post]"`*
```

Guarde o `page_id` da página criada — você vai precisar dele nos próximos sub-passos.

### 5.2 — Criar database de calendário dentro da página

Crie uma database como subpágina da página do planejamento (usando o `page_id` do passo anterior como parent).

**Título da database**: `📅 Calendário — {MES_NOME} {ANO}`

**Propriedades obrigatórias da database**:

| Propriedade | Tipo | Opções (se select) |
|---|---|---|
| `Tema` | title | — |
| `Data` | date | — |
| `Rede` | select | LinkedIn, Instagram, Facebook |
| `Formato` | select | Carrossel, Reels, Estático, Vídeo curto, Texto longo, Infográfico, Stories, Poll |
| `Pilar` | select | Educação & Insights, Produto & Cases, Comunidade & Debate, Bastidores & Equipe |
| `Hook` | rich_text | — |
| `Tipo` | select | Fixo, Oportunidade |

Use `notion-create-database` com o `page_id` da página principal como parent.

Guarde o `database_id` retornado.

### 5.3 — Popular a database com todos os posts

Para cada post gerado no Passo 4, crie uma entrada na database usando `notion-create-pages` com `data_source_id` (ID da database).

Campos a preencher por entrada:
- **Tema** (title): tema principal do post — curto e descritivo (ex: "Social listening proativo: 5 casos reais")
- **Data** (date): data exata sugerida para publicação no formato `YYYY-MM-DD`
- **Rede** (select): LinkedIn | Instagram | Facebook
- **Formato** (select): formato do post
- **Pilar** (select): pilar de conteúdo correspondente
- **Hook** (rich_text): o hook / primeira linha do post (máx 100 chars)
- **Tipo** (select): Fixo | Oportunidade

Crie as entradas em lotes: todos os posts de LinkedIn, depois Instagram, depois Facebook. Se a database tiver muitas entradas (>30), crie em lotes de 10 para evitar timeout.

Para slots de oportunidade: criar entrada com Tipo = "Oportunidade", Data = última semana do mês (ex: 28, 29, 30), Tema = tema sugerido, Hook = "(a definir)".

### 5.4 — Criar visualização em calendário

Após popular a database, crie uma calendar view usando `notion-create-view`:
- **Nome da view**: `Calendário`
- **Tipo**: `calendar`
- **Campo de data**: `Data`

Isso permite visualizar todos os posts dispostos nas datas do mês, agrupados por dia.

Salve também o planejamento localmente em `social-media/buzzmonitor/{YYYYMM}/planejamento.md` (mesma estrutura do Passo 5.1, sem publicar de volta).

## Passo 6: Apresentar ao Usuário

Apresente de forma concisa:

1. **Top 3 insights da pesquisa** que guiaram as decisões do planejamento
2. **Pilares definidos** com justificativa em 1 linha cada
3. **3 posts destaque** com maior potencial viral (com o hook completo)
4. **Link da página no Notion** com o planejamento completo
5. **Como usar**: lembrar que para criar a copy de qualquer post basta rodar `/copy-criar buzzmonitor brasil [tipo] [estagio] "[tema]"` e que slots de oportunidade podem ser ativados com `/pauta-quente` quando uma notícia relevante surgir

---

## Regras

- **Sem inventar dados**: se um perfil de concorrente não for encontrado na pesquisa, registrar honestamente "não encontrado" em vez de inventar
- **Buzzmonitor como autoridade**: o tom deve posicionar a Buzzmonitor como quem interpreta e lidera tendências do mercado — não como seguidora
- **Evitar linguagem de IA**: não usar "mergulhar", "desvendar", "navegar" de forma vaga — preferir assertividade e dados concretos
- **Adaptar obrigatoriamente por rede**: o mesmo tema em 3 redes = 3 formatos e linguagens diferentes, nunca copiar e colar
- **Blog como base**: sempre que houver um post do blog da Buzzmonitor que embase o conteúdo, referenciar — o blog é a âncora de credibilidade
- **PT-BR** em todo o output
- **Idioma dos hooks**: hooks devem soar como brasileiro falando naturalmente, não como tradução de inglês
