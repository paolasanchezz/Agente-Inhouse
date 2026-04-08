---
name: pesquisar
description: Pesquisa blog da Buzzmonitor, noticias do mercado e concorrentes para coletar material para newsletters.
argument-hint: "[foco-opcional: ex. 'atendimento ao cliente', 'IA em social listening']"
allowed-tools: WebFetch, WebSearch, Read, Write, Agent, Bash
---

# Skill: Pesquisar Material para Newsletters

Voce e um pesquisador especializado em social listening e marketing digital. Sua tarefa e coletar material de alta qualidade para a geracao de newsletters da Buzzmonitor.

## Antes de Comecar
Leia `conhecimento/buzzmonitor.md` para entender o produto e `conhecimento/concorrentes.md` para entender o mercado.

## Fase 0: Arquivar Pesquisa Anterior
Antes de gravar qualquer arquivo novo, verifique se ja existem arquivos em `pesquisa/` (exceto a pasta `pesquisa/arquivo/`).

Se existirem arquivos anteriores (`blog-buzzmonitor.md`, `noticias-mercado.md`, `analise-concorrentes.md`, `RESUMO.md`):
1. Leia a data no cabecalho de qualquer um desses arquivos para identificar o mes da pesquisa anterior (formato `YYYY-MM`)
2. Use Bash para criar a pasta de arquivo e mover os arquivos:
   ```bash
   mkdir -p pesquisa/arquivo/YYYY-MM
   mv pesquisa/blog-buzzmonitor.md pesquisa/arquivo/YYYY-MM/
   mv pesquisa/noticias-mercado.md pesquisa/arquivo/YYYY-MM/
   mv pesquisa/analise-concorrentes.md pesquisa/arquivo/YYYY-MM/
   mv pesquisa/RESUMO.md pesquisa/arquivo/YYYY-MM/
   ```
   (substitua YYYY-MM pela data identificada no cabecalho dos arquivos)

Se nao existirem arquivos anteriores, pule esta fase e continue.

## Fase 1: Blog da Buzzmonitor
**Output**: `pesquisa/blog-buzzmonitor.md`

1. Use WebFetch em `https://buzzmonitor.com/blog/` para obter a listagem de posts
2. Identifique os 5-8 posts mais recentes
3. Para cada post, use WebFetch na URL do post e extraia:
   - Titulo
   - Resumo (2-3 frases)
   - Caso de uso ou case de sucesso mencionado
   - Metricas ou resultados citados
   - Diferencial do produto destacado
   - Potencial angulo para newsletter
4. Se `$ARGUMENTS` foi fornecido, priorize posts relacionados a esse tema

Formato do arquivo de saida:
```
# Pesquisa Blog Buzzmonitor — [DATA]

## Post 1: [Titulo]
- **URL**: [link]
- **Resumo**: [2-3 frases]
- **Case/Exemplo**: [empresa e resultado]
- **Metricas**: [numeros citados]
- **Angulo para Newsletter**: [como usar este material]

[repetir para cada post]
```

## Fase 2: Noticias do Mercado
**Output**: `pesquisa/noticias-mercado.md`

1. Use WebSearch com estas queries (adapte conforme o foco):
   - "social listening tendencias 2026"
   - "social media monitoring news"
   - "atendimento ao cliente IA novidades 2026"
   - "customer experience social media trends"
   - "monitoramento de redes sociais Brasil"
2. Para os 5-6 resultados mais relevantes, use WebFetch para extrair pontos-chave
3. Foque em:
   - Tendencias que conectam com capacidades da Buzzmonitor
   - Dados surpreendentes que funcionam como ganchos de newsletter
   - Mudancas de comportamento do consumidor
   - Pesquisas e relatorios recentes do setor

Formato do arquivo de saida:
```
# Noticias do Mercado — [DATA]

## Noticia 1: [Titulo]
- **Fonte**: [nome da fonte e URL]
- **Resumo**: [2-3 frases]
- **Dado-chave**: [estatistica ou insight principal]
- **Conexao com Buzzmonitor**: [como isso se relaciona com nosso produto]
- **Potencial como Gancho**: [como usar como abertura de newsletter]

[repetir para cada noticia]
```

## Fase 3: Analise de Concorrentes
**Output**: `pesquisa/analise-concorrentes.md`

1. Selecione 4-5 concorrentes da lista (rotacione a cada execucao, nao repita os mesmos sempre):
   - Stilingue, Sprout Social, Sprinklr, Brandwatch, Mlabs, Etus, V-tracker, Zeeng, HootSuite, Emplifi, Blip, Hi Platform, Plusoft, iCustomer, Keepcon, Knewin, Torabit
2. Para cada concorrente selecionado, use WebSearch para buscar:
   - Novidades e lancamentos recentes
   - Posts de blog ou conteudo recente
   - Posicionamento e messaging atual
3. Extraia:
   - O que estao comunicando/lancando
   - Gaps que a Buzzmonitor preenche
   - Temas em comum que podemos abordar de forma diferenciada

**IMPORTANTE**: NAO copie conteudo de concorrentes. Apenas resuma posicionamento estrategico.

Formato do arquivo de saida:
```
# Analise de Concorrentes — [DATA]

## [Nome do Concorrente]
- **Novidades**: [lancamentos ou anuncios recentes]
- **Posicionamento**: [como se apresentam]
- **Gap vs Buzzmonitor**: [o que nao oferecem que nos oferecemos]
- **Tema Aproveitavel**: [tema que podemos abordar melhor]

[repetir para cada concorrente]
```

## Ao Finalizar
Crie um resumo executivo em `pesquisa/RESUMO.md` com:
- Data da pesquisa
- Quantidade de posts analisados, noticias encontradas, concorrentes pesquisados
- Top 5 angulos mais promissores para newsletters
- Dados/estatisticas mais impactantes encontrados
- Recomendacao de temas prioritarios
