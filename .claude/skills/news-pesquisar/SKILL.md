---
name: news-pesquisar
description: Mapeia dores da marca, indexa o blog proprio em profundidade e busca clipping de imprensa para alimentar a newsletter semanal. Output: dor da semana + posts-ancora + pauta sugerida (se houver lacuna) + clipping PR.
argument-hint: "[brand] [region]  — ex: buzzmonitor brasil | cxpress latam | buzzcreators portugal"
allowed-tools: WebFetch, WebSearch, Read, Write, Edit, Agent, Bash
version: 2.0.0
---

# Skill: Pesquisar Material para Newsletter Semanal

Voce e um pesquisador editorial especializado em curadoria de blog proprio + clipping de imprensa. Sua missao e (1) escolher a pergunta-dor da semana, (2) mapear quais posts do blog respondem a ela, (3) detectar lacunas que merecam virar post novo, e (4) coletar mencoes da marca em midia externa.

**ESTA SKILL NAO COLETA MAIS** noticias gerais de mercado nem analise de concorrentes para a news (esse material existia na v1 mas a v2 foca no blog proprio com clipping pontual).

## Passo 0: Parsing de Argumentos

Leia `.claude/skills/news-pesquisar/CONTEXT.md` para marcas, regioes, caminhos e Notion IDs.

Faca o parsing de `$ARGUMENTS`:
- **Argumento 1** (`brand`): `buzzmonitor` | `buzzcreators` | `cxpress` | `elife` — default: `buzzmonitor`
- **Argumento 2** (`region`): `brasil` | `latam` | `portugal` — default: `brasil`

Use o mapeamento do CONTEXT.md para idioma e pastas.

Calcule a semana ISO atual: formato `YYYY-WW` (ex: `2026-W18`). Salve como `{SEMANA_ISO}` para usar nos paths.

## Passo 1: Carregar Contexto

Leia os seguintes arquivos:

1. `brand/{brand}/BRANDBOOK.md` — produto, blog URL, nome de exibicao, **publico-alvo e dores**
2. Se existir, `newsletter/{brand}/entregas/_state.json` — historico de perguntas-dor, posts e links das ultimas 6 semanas (para dedupe)
3. Se existir, `conhecimento/produto/{brand}/blog-cache.md` — indice cumulativo de posts ja conhecidos
4. Se `region` != `brasil`: leia tambem `conhecimento/produto/{brand}/{lang-pasta}/{brand}.md` e `conhecimento/linguistico/{lang-linguistico}/padrao-linguistico.md`

Extraia do BRANDBOOK:
- **NomeDaMarca**: campo "Nome de exibicao" do bloco `### Configuracao` (dentro de `## 2. Produto`)
- **BlogURL**: coluna "Blog" da tabela em `## 3. URLs e Contatos Oficiais` para a regiao indicada (use a linha "Brasil" se a regiao nao tiver URL especifica)
- **SiteURL**: coluna "Site" da mesma tabela
- **Dores e publico-alvo**: bloco `### Publico-Alvo` em `## 1. Identidade` — extraia lista de dores nomeadas, perfis, contextos. Se a granularidade for baixa, complete com inferencias claras a partir do posicionamento e features.

## Fase 0: Arquivar Pesquisa Anterior

Se existir `conhecimento/produto/{brand}/pesquisa/atual/` com arquivos:
1. Leia o cabecalho de qualquer arquivo em `atual/` para identificar a semana anterior (formato `YYYY-WW`)
2. Use Bash para mover:
   ```bash
   mkdir -p "conhecimento/produto/{brand}/pesquisa/arquivo/{SEMANA_ANTERIOR}"
   mv conhecimento/produto/{brand}/pesquisa/atual/* "conhecimento/produto/{brand}/pesquisa/arquivo/{SEMANA_ANTERIOR}/" 2>/dev/null || true
   ```

A pasta `atual/` agora deve estar vazia. Ela sera repopulada com a pesquisa desta semana.

## Fase 1: Mapear Dores Candidatas
**Output**: `conhecimento/produto/{brand}/pesquisa/atual/dores-candidatas.md`

A partir das dores extraidas do BRANDBOOK no Passo 1, monte uma lista de dores candidatas para virarem pergunta da semana. Para cada dor:

- **Nome da dor** (curta, frase nominal — ex: "atendimento que nao escala", "monitoramento de marca em multiplos canais")
- **Descricao** (1-2 frases sobre o que esse leitor sente no dia a dia)
- **Perfil afetado** (qual perfil do publico-alvo sente essa dor — ex: "gestor de SAC em rede varejista", "head de marketing digital")
- **Sinais de quentitude** (heuristica: a dor aparece em queries do nicho? em discussoes recentes? em pesquisas do setor?)
- **Ultima vez usada na newsletter** (consultar `_state.json`; se ausente, "nunca")

**Filtragem por dedupe**: descarte dores usadas como pergunta da semana nas ultimas 6 semanas (campo `pergunta_dor.dor` em `_state.json`).

Saida (no idioma da regiao):
```
# Dores Candidatas — {NomeDaMarca}, semana {SEMANA_ISO}
**Marca**: {NomeDaMarca} | **Regiao**: {region} | **Idioma**: {idioma}

## Dor 1: [Nome curto]
- **Descricao**: ...
- **Perfil afetado**: ...
- **Sinais de quentitude**: ...
- **Ultima vez usada**: nunca | YYYY-WW

[repetir para 4-6 dores]
```

## Fase 2: Indexar o Blog em Profundidade
**Output**: `conhecimento/produto/{brand}/pesquisa/atual/indice-blog.md`
**Cache cumulativo**: `conhecimento/produto/{brand}/blog-cache.md`

A meta NAO e coletar 3-4 posts recentes — e mapear posts do blog que respondam as dores candidatas, mesmo que sejam antigos.

### Fase 2.1: WebFetch da listagem do blog

Use WebFetch em `{BlogURL}` para obter a lista de posts visiveis. Anote URL, titulo e data quando disponiveis.

### Fase 2.2: WebSearch por dor

Para cada dor candidata da Fase 1, faca uma busca dirigida no dominio do blog:
```
site:{dominio_do_blog} [palavras-chave da dor]
```

Exemplos:
- Buzzmonitor (CX/social listening): `site:buzzmonitor.com.br atendimento omnichannel`
- Cxpress (CX/atendimento): `site:cxpress.com.br SLA chatbot`
- Buzzcreators (creator economy): `site:buzzcreators.com.br influenciadores B2B`
- Elife (estrategia digital): `site:elife.com.br estrategia conteudo`

Colete 3-6 URLs por dor. Para cada URL nova (que nao esteja no `blog-cache.md`), use WebFetch para extrair: titulo, data publicacao (se disponivel), descricao/snippet, dores cobertas (heuristica por palavras-chave do conteudo), tags/categorias.

### Fase 2.3: Atualizar cache cumulativo

Para cada post novo encontrado, adicione entrada em `conhecimento/produto/{brand}/blog-cache.md`:

```markdown
## [Titulo do post]
- **URL**: ...
- **Data publicacao**: YYYY-MM-DD (ou "desconhecida")
- **Snippet**: ...
- **Dores cobertas**: dor-1, dor-3
- **Tags**: cx, atendimento, ia
- **Ultima verificacao**: {data atual}
```

Posts ja existentes no cache: atualize apenas o campo "Ultima verificacao". NAO delete posts antigos do cache.

Se o cache nao existir, crie com cabecalho:
```markdown
# Cache de Blog — {NomeDaMarca}
> Indice cumulativo de posts ja indexados. Nao deletar entradas antigas — o blog e cumulativo.
```

### Fase 2.4: Gerar indice da semana

Saida em `pesquisa/atual/indice-blog.md`:
```markdown
# Indice de Blog — {NomeDaMarca}, semana {SEMANA_ISO}
**Marca**: {NomeDaMarca} | **Posts encontrados nesta busca**: N

## Por Dor

### Dor: [Nome da dor]
- [Titulo do post] — [data] — [URL]
- [Titulo do post] — [data] — [URL]

[repetir para cada dor candidata]

## Posts novos adicionados ao cache nesta semana
- [Titulo] — [URL]
```

## Fase 3: Match Dor ↔ Posts (escolher pergunta-eixo)
**Output**: `conhecimento/produto/{brand}/pesquisa/atual/dor-semana.md`

Para cada dor candidata, conte quantos posts do `indice-blog.md` cobrem **angulos diferentes** da resposta.

**Criterio de cobertura suficiente**: ≥3 posts cobrindo angulos distintos da mesma dor (ex: para "atendimento omnichannel" — 1 post sobre integracao de canais, 1 sobre roteamento por IA, 1 sobre metricas de SLA = 3 angulos distintos).

**Selecao**:
1. Filtre dores com cobertura ≥3
2. Entre essas, escolha a com sinais de quentitude mais fortes E menor uso recente
3. Se houver empate, priorize a que tenha posts publicados nos ultimos 18 meses

**Se nenhuma dor candidata atingir cobertura ≥3**: escolha a dor mais quente com cobertura 1-2 e marque para a Fase 3.5 (lacuna).

Output (no idioma da regiao):
```markdown
# Dor da Semana — {NomeDaMarca}, semana {SEMANA_ISO}
**Marca**: {NomeDaMarca} | **Regiao**: {region}

## Dor escolhida
**[Nome da dor]**

[Descricao 2-3 frases]

## Pergunta-eixo formulada
**[Pergunta direta que essa dor se torna — 15-20 palavras, formato jornalistico]**

## Posts-ancora (3 obrigatorios)

### 1. [Titulo do post]
- **URL**: ...
- **Angulo desta dor**: [como esse post responde a pergunta]
- **Frase-chave para usar na news**: [tese curta]

### 2. [Titulo do post]
- **URL**: ...
- **Angulo desta dor**: ...
- **Frase-chave para usar na news**: ...

### 3. [Titulo do post]
- **URL**: ...
- **Angulo desta dor**: ...
- **Frase-chave para usar na news**: ...

## Posts secundarios (1-2 — opcional, para "Mais pra explorar")

- [Titulo] — [URL] — [angulo correlato]

## Cobertura
- Posts-ancora encontrados: N
- Status: SUFICIENTE (≥3) | INSUFICIENTE (1-2 — gera pauta sugerida)
```

## Fase 3.5: Detectar Lacuna e Sugerir Pauta (CONDICIONAL)
**Output**: `conhecimento/produto/{brand}/pesquisa/atual/pauta-sugerida.md`

Execute esta fase APENAS se a dor escolhida na Fase 3 tiver cobertura insuficiente (1-2 posts).

A pauta sugerida vai ser apresentada ao usuario pelo `news-pipeline`. Se aprovada, a skill `news-criar-post` escreve o post completo.

Output (no idioma da regiao):
```markdown
# Pauta Sugerida — {NomeDaMarca}, semana {SEMANA_ISO}
**Marca**: {NomeDaMarca} | **Regiao**: {region}

## Dor sem cobertura suficiente
**[Nome da dor]**

[Descricao 2-3 frases sobre por que essa dor merece um post novo]

## Por que vale virar post
- Sinais de demanda: [pesquisas do nicho, queries no Google, discussao em comunidade — citar evidencia]
- Posts existentes que cobrem parcialmente: [titulos + gap especifico de cada um]
- Diferencial proposto: [o que o post novo cobre que os existentes nao cobrem]

## Pergunta-eixo proposta para o post
**[Pergunta direta — 15-20 palavras]**

## Outline sugerido

### H1
[Titulo jornalistico — sem clickbait]

### H2 1: [Subtitulo]
[Pontos a cobrir, 3-4 bullets]

### H2 2: [Subtitulo]
[Pontos a cobrir]

### H2 3: [Subtitulo]
[Pontos a cobrir]

### H2 4: Acao pratica / proximos passos
[Como o leitor aplica isso]

## Tom
- Edutainment: definicao clara + analogia util + exemplo concreto + acao pratica
- Linguagem jornalistica e direta
- Termina com 1-2 perguntas para reflexao (sem CTA vendedor)

## Tamanho alvo
1500-2500 palavras
```

## Fase 4: Clipping PR (mencoes da marca em midia externa)
**Output**: `conhecimento/produto/{brand}/pesquisa/atual/clipping-pr.md`

Use WebSearch ativo para encontrar mencoes da marca em veiculos terceiros nos ultimos 7 dias.

### Fase 4.1: Montar queries de clipping

A partir do `{NomeDaMarca}` e do setor da marca, monte queries em veiculos relevantes para a regiao:

- Brasil: `"{NomeDaMarca}" site:meioemensagem.com.br OR site:proxxima.com.br OR site:portaldemarketing.com.br OR site:ecommercebrasil.com.br`
- Portugal: `"{NomeDaMarca}" site:marketeer.sapo.pt OR site:dinheirovivo.pt OR site:exame.pt`
- LATAM: `"{NomeDaMarca}" site:puromarketing.com OR site:marketingdirecto.com OR site:reasonwhy.es`

Adicione filtro de data quando suportado pelo provedor de busca: ultimos 7 dias.

### Fase 4.2: Filtrar mencoes relevantes

Para cada resultado, faca WebFetch e classifique:
- **Relevante**: entrevista com porta-voz, citacao em reportagem, premio, ranking, parceria, lancamento mencionado
- **Nao relevante**: mencao casual sem contexto, listagem em diretorio, post pago

Mantenha apenas as relevantes (maximo 2 — a melhor entra na news).

### Fase 4.3: Output

```markdown
# Clipping PR — {NomeDaMarca}, semana {SEMANA_ISO}
**Marca**: {NomeDaMarca} | **Regiao**: {region}

## Mencao 1
- **Veiculo**: [nome]
- **URL**: ...
- **Data**: YYYY-MM-DD (≤7 dias)
- **Contexto**: [tipo: entrevista | citacao em reportagem | premio | ranking | parceria | lancamento]
- **Resumo**: [2-3 frases sobre o que foi dito]
- **Frase-chave**: [trecho curto que pode ser usado na news]

[repetir se houver mencao 2]

## Sem mencoes
[Se nada relevante for encontrado, escrever: "Nenhuma mencao relevante de {NomeDaMarca} em midia externa nos ultimos 7 dias."]
```

## Fase 5: RESUMO

Crie `conhecimento/produto/{brand}/pesquisa/atual/RESUMO.md` (no idioma da regiao):

```markdown
# Resumo da Pesquisa — Semana {SEMANA_ISO}
**Marca**: {NomeDaMarca} | **Regiao**: {region} | **Idioma**: {idioma}
**Data**: {data atual}

## Dor da semana
[Nome da dor]

## Pergunta-eixo
[Pergunta]

## Cobertura
- Posts-ancora encontrados: N (status: SUFICIENTE | INSUFICIENTE — pauta sugerida em pauta-sugerida.md)
- Posts secundarios: N
- Posts novos adicionados ao cache nesta semana: N

## Clipping PR
- Mencoes encontradas: N
- Veiculos: [listar]

## Proximas etapas
[Se cobertura SUFICIENTE]: pipeline segue direto para news-gerar.
[Se cobertura INSUFICIENTE]: pipeline apresenta pauta-sugerida.md para aprovacao manual antes de news-criar-post.
```

## Regras Criticas

- NAO coletar noticias gerais de mercado — esta v2 foca em blog proprio e clipping de marca
- NAO copiar conteudo de concorrentes (analise de concorrentes preservada em `conhecimento/produto/{brand}/concorrentes.md` para outras skills, mas NAO entra no fluxo desta news)
- NAO inventar URLs ou postss — se WebSearch nao encontrar, marque "Nenhum post encontrado" honestamente
- Escrever os outputs no idioma da regiao (PT-BR | ES-LATAM | PT-PT)
- Cache cumulativo (`blog-cache.md`) NUNCA e deletado — apenas adicionar/atualizar entradas
- Pasta `atual/` e sempre limpa pela Fase 0 antes de gravar nova pesquisa
