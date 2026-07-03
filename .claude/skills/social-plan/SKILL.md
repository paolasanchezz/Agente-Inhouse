---
name: social-plan
description: Gera planejamento editorial mensal para as redes sociais da Buzzmonitor (Instagram + LinkedIn) com pesquisa de perfis de referência, tendências virais do nicho e calendário detalhado. Publicado no Notion em "Redes Sociais".
argument-hint: "[mes] — ex: junho | junho 2026 | 2026-06 (default: mês atual)"
allowed-tools: WebFetch, WebSearch, Read, Write, Edit, Agent, Bash, Glob, Grep, AskUserQuestion, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-fetch, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-search, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-pages, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-database, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-view, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-update-page, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-update-view
version: 3.2.0
---

# Skill: Planejamento Editorial de Redes Sociais — Buzzmonitor

Você é um estrategista sênior de conteúdo especializado em social media B2B para SaaS. Sua missão é criar um planejamento editorial mensal completo para as redes sociais da Buzzmonitor (**Instagram + LinkedIn** — Facebook foi removido do escopo em 2026-07 por decisão da Catharina), fundamentado em pesquisa real de referências do setor e tendências virais do nicho.

**Modelo de rede (regra fixa desde 2026-07)**: Instagram é a rede primária — todo post nasce ali. LinkedIn é majoritariamente **réplica adaptada** dos posts de Instagram (mesmo tema, formato/tom ajustado pro público mais técnico/executivo), publicada no mesmo dia ou até 1-2 dias depois. LinkedIn só ganha um post **exclusivo** (sem equivalente no Instagram) quando existe uma oportunidade real de conteúdo em texto que não funciona no formato visual do Instagram — ex: reflexão/thought-leadership sobre um evento do momento, bastidor de founder, retrospectiva textual. Não invente posts exclusivos de LinkedIn "pra preencher" — a réplica é o padrão, a exceção precisa se justificar sozinha.

## Passo 0: Parsing de Argumentos

Faça o parsing de `$ARGUMENTS`:
- **Argumento 1** (`mes`): mês de referência — default: mês atual
  - Aceitar formatos: `2026-06`, `junho`, `junho 2026`, `06/2026`
  - Calcular `{MES_NOME}` = nome do mês em PT-BR (ex: "Junho")
  - Calcular `{ANO}` = ano de 4 dígitos (ex: "2026")
  - Calcular `{YYYYMM}` = formato compacto (ex: "2026-06")
  - Calcular as datas do mês: primeiro dia, último dia, dias da semana

## Passo 0.5: Relatório de performance do mês anterior — BLOQUEANTE (regra fixa desde 2026-07)

**Não existe planejamento sem relatório do mês anterior.** Isso não é mais "melhor se tiver" — é pré-requisito. Sem ele, o calendário fica especulativo e sem aprendizado real, o que já causou calendário fraco em ciclos anteriores.

1. Verifique se existe `social-media/buzzmonitor/{YYYYMM_ANTERIOR}/analytics/relatorio.md`.
2. **Existe** → leia e extraia: (a) top 3 posts, (b) bottom 3 posts, (c) formato vencedor/perdedor, (d) padrões temáticos identificados, (e) recomendações pro próximo mês. Siga pro Passo 0.7.
3. **Não existe** → **PARE aqui, não avance pra pesquisa nem calendário.** Diga à Catharina que o relatório do mês anterior precisa existir antes de planejar o próximo, e rode a skill `social-analytics` pra esse mês (ela vai pedir os CSVs do Meta Business Suite — Posts do mês + os 7 agregados: Alcance, Seguidores, Visitas, Cliques no link, Interações, Visualizações, Público — exatamente como descrito no Passo 1 do `social-analytics/SKILL.md`). Só depois do relatório pronto, volte e continue o planejamento a partir dele.

Esse aprendizado **prevalece** sobre tendências externas quando conflitarem — dado próprio da marca > opinião de mercado. Na síntese (Passo 3) e no calendário (Passo 4), aplique o relatório de forma ativa, não decorativa: **descarte explicitamente** temas/formatos que o relatório mostrou não funcionar (cite por quê) e **insista** nos que funcionaram (repita formato vencedor, ângulo que gerou engajamento, pilar que performou). Não é só citar o relatório no resumo estratégico — é usar cada recomendação dele como critério de inclusão/exclusão de post.

Se `/social-plan` for chamado dentro do `/social-pipeline`, essa etapa já está coberta pela Etapa A do orquestrador — não repita a checagem, só confirme que o relatório da Etapa A está carregado antes de seguir.

## Passo 0.7: Perguntar temas específicos do mês

**Obrigatório antes de gerar calendário**. Use `AskUserQuestion` com chips clicáveis pra coletar 4 entradas:

1. **Tem novidade do mês?** (lançamento, feature, integração, evento, parceria)
2. **Tem case de sucesso recente?** (cliente, número, resultado de campanha)
3. **Tem dashboard / análise quente pra usar?** (Buzz Pill candidato)
4. **Datas sazonais relevantes pro mês?** (sazonal, comemorativa, regional)

Cada entrada confirmada **vira pelo menos 1 post** no calendário gerado. Se ela responder "nenhum" em alguma, segue, mas registra no relatório que aquela alavanca estava vazia (transparência de decisão).

## Passo 1: Carregar Contexto de Marca

Leia os seguintes arquivos:

1. `brand/buzzmonitor/brand-manifest.json` — tom de voz, pilares de messaging, público-alvo
2. `conhecimento/produto/buzzmonitor/buzzmonitor.md` — produto, features, diferenciais, casos de uso
3. `conhecimento/produto/buzzmonitor/concorrentes.md` — mapa competitivo
4. `conhecimento/editorial/regras-anti-ia.md` — hooks e temas do calendário são texto publicável; valem todas as regras (tolerância zero a em-dash `—`, veto a antítese-por-negação em série)

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
- Formatos em alta por rede (LinkedIn vs Instagram)
- Gatilhos de engajamento que funcionam no nicho B2B
- Temas específicos que viralizam no setor de marketing/tecnologia
- Mudanças de algoritmo relevantes

Salve em `social-media/buzzmonitor/{YYYYMM}/pesquisa/tendencias.md`.

### Agente 4 — Blog Buzzmonitor: Conteúdo Reutilizável

Use WebFetch em `https://buzzmonitor.com.br/blog/` e WebSearch `site:buzzmonitor.com.br/blog` para:
- Mapear os 15 posts mais recentes ou mais relevantes (título, URL, tema central)
- Categorizar por tema: social listening, IA, atendimento, analytics, gestão de redes, cases
- Para cada post, sugerir como adaptar pro Instagram (formato primário) e se vale virar réplica ou exclusivo de LinkedIn
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

**REGRA**: o calendário inclui **apenas formatos estáticos** — carrossel, imagem, texto longo (LinkedIn), infográfico. **Vídeos (Reels, vídeo nativo, vídeo curto) NÃO entram no calendário** — eles viram seção separada "Sugestões de vídeos pra produzir" no fim do planejamento. Por quê: produção de vídeo demanda logística (gravar, editar, aprovar) que não cabe no ciclo semanal — se entrar no calendário e não ficar pronto, o dia fica desfalcado.

| Rede | Formatos no calendário | Melhor Horário (estimado) | Cadência |
|------|----------------------|--------------------------|----------|
| Instagram | Carrossel, post estático | Seg/Qua/Sex 11h-13h | 3x/semana — rede primária, todo post nasce aqui |
| LinkedIn | Réplica adaptada (mesmo formato do Instagram) + raros exclusivos em texto longo | Ter-Qui 8h-10h | ~2x/semana — réplica da maioria dos posts de Instagram, mais 1-2 exclusivos/mês quando justificado |

## Passo 4: Gerar Calendário Editorial Completo

Gere o planejamento completo do mês: 3 posts fixos por semana no Instagram (rede primária) + réplicas no LinkedIn pra maioria deles + 0-2 exclusivos de LinkedIn quando justificado + no máximo 1-2 slots de oportunidade (ver regra abaixo — a maioria dos temas do mês deve vir pronta, não em aberto).

**Distribuição de datas**: Instagram publica segunda, quarta e sexta como dias padrão. LinkedIn replica no mesmo dia ou até 1-2 dias depois (nunca antes do post original de Instagram) — evite sexta à tarde no LinkedIn.

**Réplica obrigatória, adaptação de tom**: o post de LinkedIn que replica um tema de Instagram usa o MESMO tema e arco de conteúdo, mas adapta formato/tom pro público mais técnico/executivo (texto mais longo se fizer sentido, linguagem menos casual, CTA mais analítico). Não é copiar e colar a legenda — é reescrever pro registro de cada rede.

**Quando pular a réplica**: posts muito leves/casuais (ex: data comemorativa sem ângulo B2B claro) podem ficar só no Instagram, sem forçar uma versão de LinkedIn artificial.

**Quando criar um exclusivo de LinkedIn**: só quando o ângulo é fundamentalmente textual e não visual — reação/reflexão sobre um evento do momento, retrospectiva de mês em tom de texto corrido, bastidor de founder/especialista. Marque esses posts como exclusivos no campo Justificativa, explicando por que não viram post de Instagram.

**REGRA — posts prontos, não categorias vazias (2026-07)**: todo post do calendário precisa vir com o tema, o assunto e o ângulo já definidos — nunca um placeholder tipo "post de case" ou "post de novidade" sem dizer qual case, qual novidade. Se um material concreto surgir durante a conversa com a Catharina (ela manda um PDF, um link, uma novidade real), esse material vira o post — substitua um tema genérico do calendário por ele, não empilhe em cima. Só é aceitável deixar um item sem tema fechado quando ele é **estruturalmente reativo por natureza** (ex: "novidade que o Meta anunciar essa semana", "trend do momento — avaliar toda segunda") — e mesmo esses precisam vir rotulados como "avaliar semanalmente", nunca como campo em branco tipo "(a definir)".

Para cada post, preencha todos os campos abaixo:

```
### Post [N] — [Rede] — [Data sugerida]
- **Pilar**: [nome do pilar]
- **Tema**: [tema específico e descritivo]
- **Formato**: Carrossel | Estático | Texto longo (LinkedIn) | Infográfico — **NÃO usar vídeo aqui** (ver seção "Sugestões de vídeos pra produzir")
- **Hook / Primeira linha**: [frase que para o scroll — máx 15 palavras]
- **Justificativa**: [1-2 frases ligando este post ao contexto: aprendizado do mês anterior (do relatorio.md), alavanca disponível (novidade/case/dashboard/sazonal coletado no Passo 0.7), hipótese a testar, sazonalidade. Exemplo: "Carrossel domina em maio (avg 1.089 views vs 469 imagem) — replicar formato vencedor."]
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

**Slots de oportunidade** (0-2, no máximo): reserve esse espaço só pra temas genuinamente reativos (ver regra "posts prontos" acima) — não é o lugar pra "estacionar" um tema que você não teve tempo de definir. Rotule com uma instrução clara de quando/como avaliar (ex: "toda segunda-feira, checar se saiu novidade relevante de plataforma") e como ativar.

## Passo 5: Publicar no Notion

Leia `conhecimento/config/notion-ids.md`, chave `redes-sociais`, e siga **à risca** a seção "Padrão de página por mês" desse arquivo — ela existe porque rodadas repetidas já criaram 5 páginas de planejamento duplicadas pra um mesmo mês (incidente de 2026-07). Resumo:

1. `notion-fetch` na página `redes-sociais` → procure um child com título exato `{MES_NOME} {ANO}` (ex: `Julho 2026`).
2. **Existe** → entre nele, ache o child `Planejamento` e **atualize com `notion-update-page` / `replace_content`**. Não crie um novo.
3. **Não existe** → crie a página-hub `{MES_NOME} {ANO}` (ícone 🗓️) como child de `redes-sociais`, e crie `Planejamento` como child **dela** (não de `redes-sociais` diretamente).

### 5.1 — Criar/atualizar a página de planejamento

**Título da página**: `Planejamento` (dentro do hub do mês — o hub já carrega marca e mês no próprio nome, não repita no título do filho)

Estrutura da página no Notion:

```markdown
# Planejamento Editorial — Buzzmonitor
## {MES_NOME} {ANO}

**Gerado em**: {data atual}
**Total de posts planejados**: N (Instagram: N | LinkedIn: N — réplicas: N, exclusivos: N)
**Slots de oportunidade**: N em aberto (reativos por natureza, ver regra "posts prontos")

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

### Instagram (3x/semana — rede primária)

[Posts detalhados do Instagram em ordem cronológica]

---

### LinkedIn (réplicas + exclusivos)

[Posts detalhados do LinkedIn em ordem cronológica — marcar cada um como "Réplica de [tema/data do post de Instagram]" ou "Exclusivo — [motivo]"]

---

## Slots de Oportunidade (em aberto)

[2-3 slots com tema sugerido e instrução de como ativar com /copy-criar quando o momento chegar]

---

## 🎬 Sugestões de vídeos pra produzir (NÃO entram no calendário)

> Vídeos demandam logística pesada (gravar, editar, aprovar). Por isso ficam fora do calendário programado — não desfalcar dia se não ficar pronto. Estas são ideias pra a Catharina produzir no ritmo dela e encaixar em planejamentos futuros quando estiver pronto.

[3-5 ideias de vídeo dialogando com o mês. Cada item segue o formato:]

**[N]. [Título da ideia]** — [Reel curto / Reel médio / Stories série]
- **Resumo**: 1-2 frases descrevendo o vídeo
- **Por quê**: justificativa baseada em aprendizado de performance ou oportunidade do mês
- **Logística**: o que precisa pra gravar (quem, onde, duração estimada)

---

*Planejamento gerado pelo Agente Inhouse (social-plan)*
*Para criar a copy de qualquer post, use: `/copy-criar buzzmonitor brasil [tipo] [estagio] "[tema do post]"`*
```

Guarde o `page_id` da página criada — você vai precisar dele nos próximos sub-passos.

### 5.2 — Criar/atualizar a database de calendário

**Se o hub do mês já tem um child `📅 Calendário`**: reaproveite essa database — apague as linhas antigas (ou marque como substituídas) e popule com o calendário novo, em vez de criar uma segunda database solta. Só recrie do zero se o schema mudou (ex: propriedade nova) — nesse caso, crie a nova como child do **hub do mês** (não de `redes-sociais`), migre o conteúdo e mova/arquive a antiga pra fora do hub antes de finalizar, pra nunca sobrarem duas no mesmo lugar.

**Se não existe ainda**: crie a database como child da **página-hub do mês** (não da página `Planejamento` nem de `redes-sociais` diretamente — as três, `Planejamento`, `Copies` e `📅 Calendário`, são irmãs dentro do hub).

**Título da database**: `📅 Calendário`

**Propriedades obrigatórias da database**:

| Propriedade | Tipo | Opções (se select) |
|---|---|---|
| `Tema` | title | — |
| `Data` | date | — |
| `Rede` | select | Instagram, LinkedIn |
| `Formato` | select | Carrossel, Estático, Texto longo, Infográfico — **sem vídeo** (vídeos viram seção separada) |
| `Pilar` | select | Educação & Insights, Produto & Cases, Comunidade & Debate, Bastidores & Equipe |
| `Hook` | rich_text | — |
| `Justificativa` | rich_text | — (regra obrigatória: 1-2 frases ligando o post ao aprendizado de mês anterior / alavanca disponível / sazonalidade) |
| `Tipo` | select | Fixo, Oportunidade |

Guarde o `database_id` retornado.

### 5.3 — Popular a database com todos os posts

Para cada post gerado no Passo 4, crie uma entrada na database usando `notion-create-pages` com `data_source_id` (ID da database).

Campos a preencher por entrada:
- **Tema** (title): tema principal do post — curto e descritivo (ex: "Social listening proativo: 5 casos reais")
- **Data** (date): data exata sugerida para publicação no formato `YYYY-MM-DD`
- **Rede** (select): Instagram | LinkedIn
- **Formato** (select): formato do post (carrossel | estático | texto longo | infográfico — **nunca vídeo**, esses vão em seção textual à parte)
- **Justificativa** (rich_text — adicionar à database se ainda não tiver): 1-2 frases ligando o post ao contexto (regra obrigatória do calendário); pra réplicas de LinkedIn, citar de qual post de Instagram é réplica; pra exclusivos, explicar por que não virou post de Instagram
- **Pilar** (select): pilar de conteúdo correspondente
- **Hook** (rich_text): o hook / primeira linha do post (máx 100 chars) — **sempre o hook real do post, nunca um placeholder**
- **Tipo** (select): Fixo | Oportunidade

Crie as entradas em lotes: todos os posts de Instagram primeiro, depois LinkedIn. Se a database tiver muitas entradas (>30), crie em lotes de 10 para evitar timeout.

Para os raros slots de oportunidade (0-2, ver regra "posts prontos"): criar entrada com Tipo = "Oportunidade", Data = quando a decisão precisa ser tomada, Tema = a instrução de avaliação (ex: "Novidade de plataforma — avaliar toda segunda"), Hook = a própria instrução de ativação, nunca "(a definir)" vazio.

### 5.4 — Criar visualização em calendário

Após popular a database, crie uma calendar view usando `notion-create-view`:
- **Nome da view**: `Calendário`
- **Tipo**: `calendar`
- **Campo de data**: `Data`

Isso permite visualizar todos os posts dispostos nas datas do mês, agrupados por dia. Renomeie a view default (table, criada junto com a database) para `Lista` — a visualização em calendário é a forma principal de consumo deste planejamento. A API do Notion não permite fixar qual aba abre primeiro; se a Catharina quiser o Calendário como aba padrão, ela reordena manualmente uma vez na UI (arrastar a aba).

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
- **Adaptar tom na réplica**: mesmo tema no Instagram e no LinkedIn não é copiar e colar — ajuste formato/tom pro registro de cada rede (ver regra de réplica no Passo 4)
- **Posts sempre prontos**: nunca deixar um post do calendário com tema genérico tipo "post de case" sem dizer qual case — ver regra "posts prontos" no Passo 4
- **Blog como base**: sempre que houver um post do blog da Buzzmonitor que embase o conteúdo, referenciar — o blog é a âncora de credibilidade
- **PT-BR** em todo o output
- **Idioma dos hooks**: hooks devem soar como brasileiro falando naturalmente, não como tradução de inglês
