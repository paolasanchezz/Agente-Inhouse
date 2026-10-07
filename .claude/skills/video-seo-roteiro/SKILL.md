---
name: video-seo-roteiro
description: Fase 2 da skill de vídeo SEO/GEO. Só roda após aprovação explícita da Bárbara sobre o tema gerado pela Fase 1 (/video-seo-plan). Para a combinação marca×região especificada, gera o roteiro-base do vídeo: 3 opções de título, abertura com keyword nos primeiros segundos, estrutura de tópicos com keywords secundárias, definição citável, sugestão de descrição YouTube e indicação de corte para Shorts/Reel. Aplica diretrizes GEO/LLM ao longo de todo o roteiro. Não é a copy final de rede social nem o roteiro de produção — é a fundação de SEO/GEO para o time de conteúdo adaptar.
argument-hint: '"Marca Região" — ex: "Buzzmonitor BR" | "Cxpress LATAM" | "Buzzmonitor PT"'
allowed-tools: Read, Write, Edit, Glob, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__keyword_research, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__get_report_schema, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__execute_report, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-create-pages
version: 1.0.0
---

# Skill: Roteiro-base de Vídeo SEO/GEO — Fase 2

> **MCP ids variam por ambiente.** O id do Semrush no `allowed-tools` (`ad5dce33`) é o ativo desta sessão. Confirme antes de chamar.

Esta skill executa a Fase 2 do fluxo de vídeo SEO/GEO. Só deve rodar após a Bárbara ter aprovado o tema gerado pela `/video-seo-plan`. O argumento é a combinação aprovada: `"Buzzmonitor BR"`, `"Cxpress LATAM"`, etc.

O roteiro-base é uma fundação de SEO/GEO — não é a copy final de rede social, não é o roteiro de produção com indicação de câmera ou edição. Essa adaptação é responsabilidade do time de conteúdo.

---

## Passo 0: Inicialização

1. Leia `.claude/skills/video-seo-plan/CONTEXT.md` e `.claude/skills/video-seo-plan/references/dados-marcas.md`.
2. Parse `$ARGUMENTS`:
   - Argumento 1 (`combinacao`): string no formato `"Marca Região"` (ex: `"Buzzmonitor BR"`). Obrigatório — se omitido, liste as combinações disponíveis e peça que a Bárbara informe.
   - Resolva `{SLUG}` = versão kebab-case lowercase: `"Buzzmonitor BR"` → `buzzmonitor-br`, `"Cxpress LATAM"` → `cxpress-latam`.
3. Determine o mês corrente (`{MES_DIR}` = `YYYY-MM`).
4. Verifique se `conteudo-video/{MES_DIR}/cronograma.md` existe. Se não existir: pare e avise que o cronograma do mês não foi gerado ainda — rodar `/video-seo-plan` primeiro.

---

## Passo 1: Ler o cronograma aprovado

1. Leia `conteudo-video/{MES_DIR}/cronograma.md`.
2. Encontre a seção correspondente à combinação especificada (ex: `## Buzzmonitor BR`).
3. Extraia:
   - `{TEMA}`: descrição do tema
   - `{KEYWORD_ALVO}`: keyword-alvo principal
   - `{CLUSTER}`: nome do cluster
   - `{VOLUME}`: volume mensal (Semrush)
   - `{JUSTIFICATIVA}`: texto da justificativa (contexto para montar o roteiro)
   - `{REGIAO_IDIOMA}`: BR (PT-BR) / PT (PT-PT) / LATAM (ES-LATAM)
   - `{RESPONSAVEL}`: nome da responsável (tabela em `dados-marcas.md`)

4. Se a seção não existir no cronograma: pare e avise que esta combinação não está no cronograma do mês — verificar com a Bárbara.

> **Atenção para PT e LATAM:** se `{REGIAO_IDIOMA}` for PT ou LATAM, o roteiro-base será escrito no idioma da região (PT-PT ou ES-LATAM). Nunca escrever PT-PT ou ES-LATAM "de cabeça" — carregar o pilar linguístico antes do Passo 3:
> - PT-PT: `conhecimento/linguistico/pt-portugal/padrao-linguistico.md`
> - ES-LATAM: `conhecimento/linguistico/es-latam/padrao-linguistico.md`
> Se o arquivo não existir: PARE. Não escreva nenhuma palavra do roteiro antes de carregar o pilar.

---

## Passo 2: Pesquisa de keywords secundárias

Com a `{KEYWORD_ALVO}` do Passo 1, rode dois relatórios do Semrush para mapear o vocabulário do roteiro:

### 2a. Perguntas do público

Fluxo: `keyword_research` (discovery) → `get_report_schema("phrase_questions")` → `execute_report`.
- `phrase` = `{KEYWORD_ALVO}`
- `database` = base regional para esta combinação (tabela em `dados-marcas.md`)
- Para LATAM: use `mx` como primário.

Extraia as 6-10 perguntas mais relevantes (volume + relevância ao tema). Essas perguntas vão guiar a estrutura de tópicos e a abertura do roteiro.

### 2b. Termos semânticos relacionados

Fluxo: `keyword_research` (discovery) → `get_report_schema("phrase_related")` → `execute_report`.
- Mesmos parâmetros.

Extraia os 12-15 termos de maior volume semântico relacionado. Esses termos serão distribuídos como "keywords secundárias" ao longo dos tópicos do roteiro — aumentam a cobertura semântica e melhoram a indexação por fala.

### 2c. Organizar

Agrupe os termos por tópico natural (termos que respondem à mesma pergunta ou cobrem o mesmo ângulo ficam juntos). Este agrupamento vai orientar a estrutura de tópicos no Passo 3.

---

## Passo 3: Gerar o roteiro-base

Escreva o roteiro completo aplicando **em todo o texto** as diretrizes GEO/LLM e de YouTube de `dados-marcas.md`. Referência de formato: seção "Estrutura do roteiro-base" em CONTEXT.md.

Abra o bloco principal com o header `## Vídeo YouTube (horizontal)` antes das seções de título, abertura, tópicos, definição citável e descrição YouTube — deixa claro para as responsáveis de conteúdo que esse bloco é específico do vídeo longo.

### 3a. Opções de título (3 variações)

Critérios inegociáveis para qualquer variação:
- Espelhar como o público de fato pesquisa — não título "criativo" desconectado
- A `{KEYWORD_ALVO}` ou variação próxima deve aparecer no título
- Sem emoji
- Sem travessão (em dash)
- As 3 variações devem ser claramente distintas entre si (ângulo, formulação, extensão) — não são a mesma frase levemente reformatada

Tipos de variação a cobrir: (1) formulação como pergunta direta, (2) formulação imperativa/how-to, (3) formulação descritiva com número ou dado.

### 3b. Abertura (primeiros 10-15 segundos)

É o trecho mais importante do roteiro — tanto para retenção quanto para indexação de fala pelo YouTube.

Regras:
- A `{KEYWORD_ALVO}` deve ser mencionada **verbalmente nos primeiros 5 segundos**
- Responder diretamente à pergunta central antes de qualquer contextualização — nunca abrir com "Olá, tudo bem?" ou "No vídeo de hoje vou falar sobre..."
- Definição citável ou dado concreto na abertura, se o tema comportar (aumenta chance de citação por LLMs no trecho mais assistido)
- Extensão: 3-5 frases curtas, ritmo de fala natural

### 3c. Estrutura de tópicos

Liste os tópicos do vídeo em ordem lógica. Para cada tópico:
- Nome do tópico (equivale a um H2 na versão de texto)
- Keyword secundária principal que deve ser mencionada em voz alta nesse trecho (dos dados do Passo 2)
- 1-2 frases descrevendo o que cobrir — orientação para o time de conteúdo, não o script completo

Mínimo 4 tópicos, máximo 7 (mantém o vídeo focado e o Shorts/Reel aproveitável).

O último tópico ou penúltimo deve incluir a menção ao produto/solução (a marca) de forma integrada ao conteúdo — não como bloco de "publicidade" separado.

### 3d. Definição citável

Redigir pelo menos uma frase de definição isolada sobre o tema central. Critérios:
- Autocontida — faz sentido sem o contexto do parágrafo anterior
- Linguagem clara e direta, sem jargão desnecessário
- Pode começar com "[Termo] é..." ou "[Processo] funciona [assim]..." — formatos que LLMs usam como resposta direta
- Sem travessão (em dash)

Formatar como blockquote no arquivo de saída.

### 3e. Sugestão de descrição YouTube

Parágrafo de 4-6 frases. Critérios:
- Aprofunda o tema com keywords relacionadas do Passo 2 — não só repete o título
- Menciona a keyword-alvo na primeira frase
- Inclui ao menos 3-4 das keywords secundárias mapeadas no Passo 2 de forma natural
- Pode terminar com um CTA suave (link para a plataforma, LP ou artigo do blog relacionado — não inventar URLs, usar só o que a Bárbara tiver fornecido ou que constar em `landing-pages/catalogo/` se existir)

### 3f. Corte para Shorts/Reel (vertical)

Identificar 1-2 trechos do roteiro com maior potencial de funcionar sozinhos como peça de 15-30 segundos. Para cada opção, preencher três campos:

Para cada opção de corte, preencher todos os campos abaixo:

1. **Frase inicial (Reel/Shorts):** a frase de abertura já escrita no estilo Reel — gancho direto de dor ou afirmação forte, sem "Olá" ou "Bem-vindos". Escrever no idioma da região com o pilar linguístico aplicado. É o que o talento fala nos primeiros 2-3 segundos — não é descrição do gancho, é o gancho em si.
2. **Desenvolvimento (corte do vídeo longo):** quais tópicos/momentos do vídeo longo compõem o meio do Reel/Short (15-30 seg). Referenciar os tópicos pelo nome e indicar o tempo aproximado de cada trecho. Priorizar o tópico com maior diferencial ou sinal mais forte.
3. **CTA final:** frase de encerramento (3-5 seg). Acionável, menciona a marca/produto ou direciona para o link.
4. **Legenda:** sugestão de legenda para publicação — inclui a keyword-alvo de forma natural + 2-3 hashtags relevantes. Não muito longa.
5. **Thumb:** frase curta para thumbnail (máx. 5-6 palavras). Deve conter a keyword ou variação próxima. Foco na dor do público. Caixa alta é padrão para thumb.
6. **Gancho:** explicação de por que a seleção funciona como peça autônoma — para orientar a responsável de conteúdo.

Usar o header `## Corte para Shorts/Reel (vertical)` para esta seção. Separar cada opção com `---`.

---

## Passo 4: Salvar o roteiro

Escreva `conteudo-video/{MES_DIR}/roteiros/{SLUG}.md` com o conteúdo completo do roteiro.

Se `conteudo-video/{MES_DIR}/roteiros/` não existir: o Write cria o diretório junto com o arquivo.

Se o arquivo já existir: avise a Bárbara que existe uma versão anterior e pergunte se quer sobrescrever.

---

## Passo 5: Publicar no Notion

Crie uma página filho sob o pai `3c33934026fd80138da3ce090c91b46e` (página "Roteiros") com:
- **Título:** `{MARCA} {REGIAO} — {TEMA_CURTO} — {MES_NOME}` (ex: "Cxpress LATAM — Chatbot no WhatsApp — Setembro 2026")
- **Conteúdo:** o markdown completo do roteiro-base

Ferramenta: `notion-create-pages` com `parent.page_id` = `3c33934026fd80138da3ce090c91b46e`.

Se a publicação falhar: avise a Bárbara mas não interrompa o fluxo — o arquivo local em `conteudo-video/{MES_DIR}/roteiros/{SLUG}.md` já está salvo.

---

## Passo 6: Relatório final

Retorne à Bárbara:

```markdown
## Roteiro-base gerado

- **Combinação:** [Marca] [Região]
- **Tema:** {TEMA}
- **Keyword-alvo:** `{KEYWORD_ALVO}` ([volume]/mês, Semrush base [db])
- **Keywords secundárias mapeadas:** [lista curta — 5-6 termos mais relevantes]
- **Arquivo:** `conteudo-video/{MES_DIR}/roteiros/{SLUG}.md`
- **Responsável de conteúdo:** {RESPONSAVEL}

**Próximos passos:**
- Verificar AI Overview no Semrush UI para `{KEYWORD_ALVO}` (sinal de prioridade)
- Entregar o arquivo para {RESPONSAVEL} adaptar para linguagem e produção
- Para gerar o próximo roteiro: `/video-seo-roteiro "Outra Combinação"`
```

---

## O que esta skill NÃO deve gerar

- Legenda final de rede social
- Hashtags
- Indicação de take ou corte de câmera
- Trilha sonora ou decisões de produção
- Copy pronta para publicar — o roteiro-base é material bruto para o time de conteúdo

## Regras críticas

- NUNCA rodar sem um cronograma aprovado (Passo 0) — se não existir, pare e indique `/video-seo-plan`
- NUNCA escrever PT-PT ou ES-LATAM sem carregar o pilar linguístico (Passo 1 — regra inegociável)
- NUNCA inventar keywords secundárias — todas vêm do Semrush (Passo 2)
- NUNCA usar travessão (em dash) em nenhum trecho do roteiro
- NUNCA abrir o vídeo sem mencionar a keyword-alvo nos primeiros 5 segundos (Passo 3b)
- NUNCA gerar mais de um roteiro por execução — uma combinação por chamada
