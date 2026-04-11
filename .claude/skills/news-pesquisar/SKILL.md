---
name: news-pesquisar
description: Pesquisa blog da marca, noticias do mercado e concorrentes para coletar material para newsletters — adaptado ao idioma da regiao.
argument-hint: "[brand] [region] [foco-opcional]  — ex: buzzmonitor brasil 'atendimento ao cliente'"
allowed-tools: WebFetch, WebSearch, Read, Write, Agent, Bash
---

# Skill: Pesquisar Material para Newsletters

Voce e um pesquisador especializado em marketing digital e tecnologia. Sua tarefa e coletar material de alta qualidade para a geracao de newsletters, adaptado a marca e regiao indicadas.

## Passo 0: Parsing de Argumentos

Leia `.claude/skills/news-pesquisar/CONTEXT.md` para marcas, regioes, caminhos e Notion IDs.

Faca o parsing de `$ARGUMENTS`:
- **Argumento 1** (`brand`): `buzzmonitor` | `buzzcreators` | `cxpress` | `elife` — default: `buzzmonitor`
- **Argumento 2** (`region`): `brasil` | `latam` | `portugal` — default: `brasil`
- **Argumento 3** (foco opcional): tema para direcionar a pesquisa (ex: "atendimento ao cliente")

Use o mapeamento de regiao do CONTEXT.md para idioma e pastas.

## Passo 1: Carregar Contexto

Leia os seguintes arquivos na ordem:
1. `conhecimento/produto/{brand}/{brand}.md` — produto, blog URL, nome de exibicao
2. `conhecimento/produto/{brand}/concorrentes.md` — mapa competitivo da marca
3. Se `region` != `brasil`: leia tambem `conhecimento/produto/{brand}/{lang-pasta}/{brand}.md` (terminologia nativa) e `conhecimento/linguistico/{lang-linguistico}/padrao-linguistico.md` (padrao de escrita)

Extraia do arquivo de conhecimento do produto:
- **NomeDaMarca**: campo "Nome de exibicao" do bloco `## Configuracao`
- **BlogURL**: campo "Blog {Regiao}" do bloco `## Configuracao` (use "Blog Brasil" se a regiao nao tiver URL especifica)
- **SiteURL**: campo "Site {Regiao}" do bloco `## Configuracao`

## Fase 0: Arquivar Pesquisa Anterior

Antes de gravar qualquer arquivo novo, verifique se ja existem arquivos em `conhecimento/produto/{brand}/pesquisa/` (exceto a pasta `conhecimento/produto/{brand}/pesquisa/arquivo/`).

Se existirem arquivos anteriores (`blog-{brand}.md`, `noticias-mercado.md`, `analise-concorrentes.md`, `RESUMO.md`):
1. Leia a data no cabecalho de qualquer um desses arquivos para identificar o mes da pesquisa anterior (formato `YYYY-MM`)
2. Use Bash para criar a pasta de arquivo e mover os arquivos:
   ```bash
   mkdir -p conhecimento/produto/{brand}/pesquisa/arquivo/YYYY-MM
   mv conhecimento/produto/{brand}/pesquisa/blog-{brand}.md conhecimento/produto/{brand}/pesquisa/arquivo/YYYY-MM/
   mv conhecimento/produto/{brand}/pesquisa/noticias-mercado.md conhecimento/produto/{brand}/pesquisa/arquivo/YYYY-MM/
   mv conhecimento/produto/{brand}/pesquisa/analise-concorrentes.md conhecimento/produto/{brand}/pesquisa/arquivo/YYYY-MM/
   mv conhecimento/produto/{brand}/pesquisa/RESUMO.md conhecimento/produto/{brand}/pesquisa/arquivo/YYYY-MM/
   ```

## Fase 1: Blog da Marca
**Output**: `conhecimento/produto/{brand}/pesquisa/blog-{brand}.md`

1. Use WebFetch em `{BlogURL}` (extraido do arquivo de conhecimento) para obter a listagem de posts
2. Identifique os 5-8 posts mais recentes
3. Para cada post, use WebFetch na URL do post e extraia:
   - Titulo
   - Resumo (2-3 frases)
   - Caso de uso ou case de sucesso mencionado
   - Metricas ou resultados citados
   - Diferencial do produto destacado
   - Potencial angulo para newsletter
4. Se `$ARGUMENTS` incluiu foco tematico, priorize posts relacionados a esse tema

Formato do arquivo de saida (escreva no idioma da regiao):
```
# Pesquisa Blog {NomeDaMarca} — [DATA]
**Marca**: {NomeDaMarca} | **Regiao**: {region} | **Idioma**: {idioma}

## Post 1: [Titulo]
- **URL**: [link]
- **Resumo**: [2-3 frases]
- **Case/Exemplo**: [empresa e resultado]
- **Metricas**: [numeros citados]
- **Angulo para Newsletter**: [como usar este material]

[repetir para cada post]
```

## Fase 2: Noticias do Mercado
**Output**: `conhecimento/produto/{brand}/pesquisa/noticias-mercado.md`

**PASSO 1 — Extrair o setor da marca**: Leia o campo `## Visao Geral` de `conhecimento/produto/{brand}/{brand}.md` para identificar o setor e posicionamento da marca. Use essas informacoes para construir os termos de busca desta fase.

**PASSO 2 — Montar as queries adaptadas ao setor e regiao**:

A partir do setor identificado, construa 5 queries combinando:
- Tema principal do produto (ex: "social listening", "atendimento omnichannel", "influencer marketing")
- Termos de mercado relevantes (tendencias, IA, dados de comportamento do consumidor)
- Regiao no idioma correto: "brasil" / "latinoamerica" / "portugal"
- Ano atual (2026)

**Exemplos de adaptacao por setor** (ajuste conforme o produto real):
- Social listening/monitoramento → "social listening tendencias 2026 [regiao]", "monitoramento de redes sociais IA 2026"
- Atendimento ao cliente/CX → "atendimento omnichannel tendencias 2026 [regiao]", "customer experience IA [regiao] 2026"
- Marketing de influenciadores → "influencer marketing tendencias 2026 [regiao]", "creator economy brasil 2026"
- Servicos de CX/outsourcing → "customer experience outsourcing tendencias 2026", "CX como servico brasil 2026"

Se `$ARGUMENTS` incluiu foco tematico, adicione esse tema as queries e priorize resultados relacionados.

Para os 5-6 resultados mais relevantes, use WebFetch para extrair pontos-chave. Foque em:
- Tendencias conectadas ao produto e ao mercado da regiao
- Dados surpreendentes que funcionam como ganchos
- Mudancas de comportamento do consumidor
- Pesquisas e relatorios recentes do setor

Formato do arquivo de saida (no idioma da regiao):
```
# Noticias do Mercado — [DATA]
**Marca**: {NomeDaMarca} | **Regiao**: {region} | **Idioma**: {idioma}

## Noticia 1: [Titulo]
- **Fonte**: [nome da fonte e URL]
- **Resumo**: [2-3 frases]
- **Dado-chave**: [estatistica ou insight principal]
- **Conexao com {NomeDaMarca}**: [como isso se relaciona com o produto]
- **Potencial como Gancho**: [como usar como abertura de newsletter]

[repetir para cada noticia]
```

## Fase 3: Analise de Concorrentes
**Output**: `conhecimento/produto/{brand}/pesquisa/analise-concorrentes.md`

1. Leia `conhecimento/produto/{brand}/concorrentes.md` e selecione 4-5 concorrentes (rotacione a cada execucao)
2. Priorize concorrentes relevantes para a `{region}`: se `region` = `latam`, foque em players LATAM; se `region` = `portugal`, inclua players europeus se existirem no arquivo
3. Para cada concorrente selecionado, use WebSearch para buscar novidades recentes
4. Extraia:
   - O que estao comunicando/lancando
   - Gaps que {NomeDaMarca} preenche
   - Temas em comum que podemos abordar de forma diferenciada

**IMPORTANTE**: NAO copie conteudo de concorrentes. Apenas resuma posicionamento estrategico.

Formato do arquivo de saida (no idioma da regiao):
```
# Analise de Concorrentes — [DATA]
**Marca**: {NomeDaMarca} | **Regiao**: {region}

## [Nome do Concorrente]
- **Novidades**: [lancamentos ou anuncios recentes]
- **Posicionamento**: [como se apresentam]
- **Gap vs {NomeDaMarca}**: [o que nao oferecem que nos oferecemos]
- **Tema Aproveitavel**: [tema que podemos abordar melhor]

[repetir para cada concorrente]
```

## Ao Finalizar — Parte A: Resumo de Pesquisa
Crie um resumo executivo em `conhecimento/produto/{brand}/pesquisa/RESUMO.md` (no idioma da regiao) com:
- Data da pesquisa
- Marca, regiao e idioma
- Quantidade de posts analisados, noticias encontradas, concorrentes pesquisados
- Top 5 angulos mais promissores para newsletters
- Dados/estatisticas mais impactantes encontrados
- Recomendacao de temas prioritarios

## Ao Finalizar — Parte B: Atualizar Base de Conhecimento do Produto

Apos gravar o RESUMO.md, releia `conhecimento/produto/{brand}/{brand}.md` e `conhecimento/produto/{brand}/concorrentes.md` e aplique as atualizacoes abaixo. Use Edit para alterar apenas o que mudou — nao reescreva o arquivo inteiro.

### Atualizacoes em `conhecimento/produto/{brand}/{brand}.md`

**Se o arquivo estiver vazio ou com secoes marcadas como "a preencher":**
Preencha com o que foi descoberto na pesquisa (site, blog, posts). Apenas informacoes verificadas — nao invente features, modulos ou cases.

**Se o arquivo ja tiver conteudo:**
Verifique se a pesquisa revelou algo novo nao presente no arquivo:
1. **Novos cases ou resultados**: Se o blog citou um case com empresa e metricas verificaveis, adicione em `## Cases de Sucesso Verificados`
2. **Novas features ou modulos**: Se o blog ou site menciona uma feature ou modulo nao listado, adicione em `## Modulos Principais` ou `## Features de IA` com nota de fonte
3. **Correcoes de URL**: Se o Blog URL ou Site URL retornou redirect ou erro, corrija em `## Configuracao`
4. **Posicionamento atualizado**: Se o site usa um novo tagline ou posicionamento diferente do registrado, atualize `## Visao Geral`

**Nao altere:**
- Nomes oficiais de features ja verificados (a menos que o proprio site os corrija)
- Cases ja verificados (a menos que o blog traga dados atualizados do mesmo case)
- Grafias corretas ja registradas

### Atualizacoes em `conhecimento/produto/{brand}/concorrentes.md`

**Se o arquivo estiver vazio:**
Preencha com os concorrentes pesquisados na Fase 3, incluindo posicionamento e diferenciais identificados.

**Se o arquivo ja tiver conteudo:**
1. **Novos movimentos**: Se a Fase 3 revelou lancamento, aquisicao ou mudanca de posicionamento de um concorrente, adicione em `## Movimentos Recentes do Mercado`
2. **Novos concorrentes**: Se encontrou um player relevante nao listado, adicione na tabela do segmento correto
3. **Tendencias de mercado**: Se a Fase 2 trouxe dados novos de mercado relevantes para o contexto competitivo, adicione ou atualize `## Tendencias do Mercado`

**Nao invente** diferenciais ou posicionamentos — use apenas o que foi observado na pesquisa.
