---
name: news-pesquisar
description: Pesquisa blog da marca, noticias do mercado e concorrentes para coletar material para newsletters — adaptado ao idioma da regiao.
argument-hint: "[brand] [region] [foco-opcional]  — ex: buzzmonitor brasil 'atendimento ao cliente'"
allowed-tools: WebFetch, WebSearch, Read, Write, Agent, Bash
---

# Skill: Pesquisar Material para Newsletters

Voce e um pesquisador especializado em marketing digital e tecnologia. Sua tarefa e coletar material de alta qualidade para a geracao de newsletters, adaptado a marca e regiao indicadas.

## Passo 0: Parsing de Argumentos

Faca o parsing de `$ARGUMENTS`:
- **Argumento 1** (`brand`): `buzzmonitor` | `buzzcreators` | `cxpress` | `elife` — default: `buzzmonitor`
- **Argumento 2** (`region`): `brasil` | `latam` | `portugal` — default: `brasil`
- **Argumento 3** (foco opcional): tema para direcionar a pesquisa (ex: "atendimento ao cliente")

Mapeamento de `region`:
- `brasil` → idioma: PT-BR | pasta linguistico: nenhuma | pasta produto: (nenhuma adicional)
- `latam` → idioma: ES-LATAM | pasta linguistico: `es-latam` | pasta produto lang: `es`
- `portugal` → idioma: PT-PT | pasta linguistico: `pt-portugal` | pasta produto lang: `pt-pt`

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

Antes de gravar qualquer arquivo novo, verifique se ja existem arquivos em `newsletter/{brand}/pesquisa/` (exceto a pasta `newsletter/{brand}/pesquisa/arquivo/`).

Se existirem arquivos anteriores (`blog-{brand}.md`, `noticias-mercado.md`, `analise-concorrentes.md`, `RESUMO.md`):
1. Leia a data no cabecalho de qualquer um desses arquivos para identificar o mes da pesquisa anterior (formato `YYYY-MM`)
2. Use Bash para criar a pasta de arquivo e mover os arquivos:
   ```bash
   mkdir -p newsletter/{brand}/pesquisa/arquivo/YYYY-MM
   mv newsletter/{brand}/pesquisa/blog-{brand}.md newsletter/{brand}/pesquisa/arquivo/YYYY-MM/
   mv newsletter/{brand}/pesquisa/noticias-mercado.md newsletter/{brand}/pesquisa/arquivo/YYYY-MM/
   mv newsletter/{brand}/pesquisa/analise-concorrentes.md newsletter/{brand}/pesquisa/arquivo/YYYY-MM/
   mv newsletter/{brand}/pesquisa/RESUMO.md newsletter/{brand}/pesquisa/arquivo/YYYY-MM/
   ```

## Fase 1: Blog da Marca
**Output**: `newsletter/{brand}/pesquisa/blog-{brand}.md`

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
**Output**: `newsletter/{brand}/pesquisa/noticias-mercado.md`

Adapte os termos de busca ao idioma e regiao:

**Se region = brasil:**
- "social listening tendencias 2026"
- "social media monitoring news brasil"
- "atendimento ao cliente IA novidades 2026"
- "customer experience social media trends brasil"
- "monitoramento de redes sociais Brasil"

**Se region = latam:**
- "social listening tendencias 2026 latinoamerica"
- "marketing digital IA latam 2026"
- "atencion al cliente redes sociales tendencias"
- "customer experience social media latam"
- "monitoreo redes sociales america latina"

**Se region = portugal:**
- "social listening tendencias 2026 portugal"
- "marketing digital IA portugal 2026"
- "atendimento ao cliente redes sociais portugal"
- "customer experience tendencias europa"
- "monitorizacao redes sociais portugal"

Se `$ARGUMENTS` incluiu foco tematico, adicione esse tema as queries.

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
**Output**: `newsletter/{brand}/pesquisa/analise-concorrentes.md`

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

## Ao Finalizar
Crie um resumo executivo em `newsletter/{brand}/pesquisa/RESUMO.md` (no idioma da regiao) com:
- Data da pesquisa
- Marca, regiao e idioma
- Quantidade de posts analisados, noticias encontradas, concorrentes pesquisados
- Top 5 angulos mais promissores para newsletters
- Dados/estatisticas mais impactantes encontrados
- Recomendacao de temas prioritarios
