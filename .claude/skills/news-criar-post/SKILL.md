---
name: news-criar-post
description: Cria post de blog completo (1500-2500 palavras) para preencher lacuna identificada pela pesquisa, em tom jornalistico + edutainment, e publica como draft no Notion. Manual-trigger — invocada pelo news-pipeline apos aprovacao da pauta.
argument-hint: "[brand] [region]  — ex: cxpress brasil | buzzmonitor latam"
allowed-tools: Read, Write, Edit, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-fetch, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-pages, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-update-page, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-search
version: 1.0.0
---

# Skill: Criar Post de Blog (Draft) para Preencher Lacuna

Voce e um redator editorial senior. A skill `news-pesquisar` detectou uma dor com cobertura insuficiente (1-2 posts) no blog da marca e gerou uma pauta sugerida em `pesquisa/atual/pauta-sugerida.md`. Sua missao e transformar essa pauta em um post completo, jornalistico, com edutainment, e publica-lo como draft no Notion para o time editorial revisar e publicar no blog real.

**Esta skill e manual-trigger** — chamada pelo `news-pipeline` somente apos aprovacao explicita da pauta pelo usuario. Nao deve ser disparada automaticamente.

## Passo 0: Parsing de Argumentos

Leia `.claude/skills/news-pesquisar/CONTEXT.md` para marcas, regioes, caminhos e Notion IDs.

Faca o parsing de `$ARGUMENTS`:
- **Argumento 1** (`brand`): `buzzmonitor` | `buzzcreators` | `cxpress` | `elife` — default: `buzzmonitor`
- **Argumento 2** (`region`): `brasil` | `latam` | `portugal` — default: `brasil`

Calcule a semana ISO atual: `YYYY-WW` (ex: `2026-W18`). Salve como `{SEMANA_ISO}`.

## Pre-requisitos

1. Verifique que existe `conhecimento/produto/{brand}/pesquisa/atual/pauta-sugerida.md`. Se nao existir, INFORME o usuario e PARE: "Nenhuma pauta sugerida nesta semana — rode /news-pesquisar primeiro."
2. Confirme com o usuario que a pauta foi aprovada (essa skill nao deve ser chamada sem aprovacao explicita; o `news-pipeline` ja faz a pausa).

## Passo 1: Carregar Contexto

Leia os seguintes arquivos:

1. `conhecimento/produto/{brand}/pesquisa/atual/pauta-sugerida.md` — a pauta a transformar em post
2. `brand/{brand}/BRANDBOOK.md` — produto, nome de exibicao, cases verificados, anti-patterns
3. `conhecimento/copywriting/blog-copy.md` — guia de copywriting de blog (titulo, lead, estrutura, edutainment)
4. `conhecimento/copywriting/fundamentos-copy.md` — principios gerais
5. `conhecimento/editorial/regras-anti-ia.md` — frases proibidas, fillers, anti-patterns estruturais
6. `conhecimento/editorial/estilo-newsletter.md` — secao "Linguagem jornalistica e direta" e "Edutainment"
7. Se `region` != `brasil`: `conhecimento/produto/{brand}/{lang-pasta}/{brand}.md` e `conhecimento/linguistico/{lang-linguistico}/padrao-linguistico.md`
8. Se existir, `newsletter/{brand}/entregas/_state.json` — para registro do consumo da pauta

Extraia do BRANDBOOK:
- **NomeDaMarca**: campo "Nome de exibicao" em `### Configuracao` (dentro de `## 2. Produto`)
- **Cases verificados**: `### Cases de Sucesso Verificados` em `## 2. Produto` (so usar esses se citar case nominal)
- **Diferenciais**: `### Diferenciais-Chave` em `## 2. Produto`

Da pauta-sugerida.md, extraia:
- **Pergunta-eixo**, **outline H1/H2**, **tom alvo**, **tamanho alvo**

## Passo 2: Gerar slug do post

A partir do H1 da pauta-sugerida.md, gere um slug em kebab-case:
- Minusculas, sem acentos, sem caracteres especiais
- Espacos viram hifens
- Maximo 60 caracteres
- Ex: "Como dimensionar atendimento omnichannel sem aumentar headcount" → `dimensionar-atendimento-omnichannel-sem-aumentar-headcount`

Salve como `{SLUG}`.

## Passo 3: Escrever o Post

Siga RIGOROSAMENTE a estrutura definida em `conhecimento/copywriting/blog-copy.md` secao "Template para pauta quente / artigo editorial":

```
H1 — Titulo editorial (jornalistico, 55-70 chars, sem clickbait)

Lead (1-2 paragrafos)
  - Cena, dado ou conflito que ancora o tema
  - Justifica a leitura (por que importa agora)
  - Sem aberturas tipo "imagine que...", "no cenario atual...", "vivemos uma era..."

H2 — [Subtitulo 1] (do outline da pauta)
  - 3-5 paragrafos
  - Tese clara + evidencia + exemplo

H2 — [Subtitulo 2] (do outline)
  - 3-5 paragrafos
  - Edutainment: definicao + analogia util + exemplo concreto

H2 — [Subtitulo 3] (do outline)
  - 3-5 paragrafos

H2 — Acao pratica (ou "Como aplicar isso")
  - 2-3 paragrafos com proximos passos concretos
  - Pode incluir 1 link interno para feature/produto da {NomeDaMarca}, mas SEM virar pitch de venda

H2 — Para refletir / Perguntas que ficam (opcional, recomendado)
  - 1-2 perguntas que estimulam o leitor a aplicar
  - NAO usar como CTA vendedor
```

### Regras editoriais inegociaveis

1. **Idioma da regiao**: PT-BR (brasil) | ES-LATAM (latam) | PT-PT (portugal). Texto deve parecer escrito nativo.
2. **Anti-IA aplicado**: zero em-dashes, zero filler words ("realmente", "de forma X", "no mundo atual"), zero antitese-por-negacao em excesso (max 2 ocorrencias), zero "em resumo" como conclusao, zero listas de 3 itens decorativas.
3. **Lead jornalistico**: comeca com fato, dado ou cena — nunca com "imagine que..." ou "vivemos uma era...".
4. **Edutainment**: cada H2 deve conter ao menos UM destes — analogia util, dado verificavel, exemplo concreto, definicao clara.
5. **Cases**: se citar case nominal de cliente, USAR APENAS os listados em `### Cases de Sucesso Verificados` do BRANDBOOK. Caso contrario, usar exemplos genericos ("uma operadora de seguros...", "uma rede de varejo de moda...") sem inventar nomes reais.
6. **Conceitos nomeados**: se usar nome de vies cognitivo, efeito psicologico ou conceito academico, verificar a definicao real. Em duvida, descrever o fenomeno sem o nome tecnico.
7. **Tamanho**: 1500-2500 palavras. Se ficar abaixo de 1500, adensar com mais evidencia/exemplo, nao com filler.
8. **Conclusao**: terminar com 1-2 perguntas para reflexao OU com sintese curta + acao pratica. NUNCA terminar com CTA de demo/teste/webinar — esse post e editorial, nao funil.
9. **Tom**: especialista compartilhando, nao vendedor. {NomeDaMarca} pode ser citada como facilitadora em 1-2 momentos no maximo, sempre como ferramenta — nunca como heroina da historia.

## Passo 4: Salvar Localmente

Salve o post em `newsletter/{brand}/posts-sugeridos/post-{SLUG}-{SEMANA_ISO}.md`:

```markdown
# [H1 jornalistico]

<!-- Draft gerado por news-criar-post em {DATA} | Marca: {NomeDaMarca} | Regiao: {region} | Idioma: {idioma} | Semana: {SEMANA_ISO} -->
<!-- Pauta original: pesquisa/atual/pauta-sugerida.md -->
<!-- Status: DRAFT — aguardando revisao do time editorial e publicacao no blog real -->

[Lead 1-2 paragrafos]

## [Subtitulo 1]

[corpo]

## [Subtitulo 2]

[corpo]

## [Subtitulo 3]

[corpo]

## [Acao pratica]

[corpo]

## [Para refletir] (opcional)

[1-2 perguntas]

---
**Tamanho**: [N] palavras
**Posts existentes que cobriam parcialmente**: [lista da pauta-sugerida.md]
**Diferencial deste post**: [da pauta-sugerida.md]
```

Se a pasta `newsletter/{brand}/posts-sugeridos/` nao existir, criar com Bash: `mkdir -p newsletter/{brand}/posts-sugeridos`.

## Passo 5: Publicar Draft no Notion

### Estrutura alvo no Notion

```
Entregas (ID lido de conhecimento/config/notion-ids.md, chave `entregas`)
└── Drafts de Blog                               ← criar se nao existir (icon: 📁)
    └── {NomeDaMarca}                            ← subpasta da marca (icon: 📁)
        └── [{SEMANA_ISO}] {H1 do post}          ← pagina do post (icon: 📝)
```

### Passo 5.1: Localizar ou criar "Drafts de Blog"

1. Leia `conhecimento/config/notion-ids.md` e pegue o ID da chave `entregas` ({ENTREGAS_ID})
2. Use `notion-search` com query `Drafts de Blog` para localizar a subpasta dentro de Entregas
3. Se encontrar: anote o ID
4. Se nao encontrar: crie com `notion-create-pages`, parent = `{ENTREGAS_ID}`, title = `Drafts de Blog`, icon = `📁`

### Passo 5.2: Localizar ou criar subpasta da marca

1. Faca fetch de "Drafts de Blog" para ver se existe subpagina `{NomeDaMarca}`
2. Se existir: anote o ID
3. Se nao existir: crie com `notion-create-pages`, parent = ID de Drafts de Blog, title = `{NomeDaMarca}`, icon = `📁`

### Passo 5.3: Criar a pagina do post

1. Faca fetch de `notion://docs/enhanced-markdown-spec` para confirmar sintaxe Notion (markdown enhanced)
2. Crie a pagina com `notion-create-pages`:
   - parent = ID da subpasta da marca
   - title = `[{SEMANA_ISO}] {H1 do post}`
   - icon = `📝`
   - content = corpo completo do post em markdown enhanced (H1, H2, paragrafos, formatacoes)
3. Adicione no inicio do conteudo um callout/quote com metadados:
   ```
   > **Status**: DRAFT — aguardando revisao do time editorial
   > **Marca**: {NomeDaMarca}
   > **Regiao/Idioma**: {region} / {idioma}
   > **Semana**: {SEMANA_ISO}
   > **Pauta original**: dor "[Nome da dor]" sem cobertura suficiente
   > **Tamanho**: [N] palavras
   ```

Anote a URL da pagina recem criada como `{URL_NOTION}`.

## Passo 6: Atualizar _state.json

Edite (ou crie, se nao existir) `newsletter/{brand}/entregas/_state.json`:

```json
{
  "ultima_atualizacao": "{DATA}",
  "perguntas_dor": [...],
  "links_usados": [...],
  "pautas_sugeridas_consumidas": [
    {
      "semana": "{SEMANA_ISO}",
      "slug": "{SLUG}",
      "h1": "{H1 do post}",
      "url_notion": "{URL_NOTION}",
      "caminho_local": "newsletter/{brand}/posts-sugeridos/post-{SLUG}-{SEMANA_ISO}.md",
      "dor": "{Nome da dor da pauta}"
    }
  ]
}
```

Adicione tambem em `links_usados` uma entrada para o proprio post (a news-gerar vai citar este post como ancora):
```json
{
  "semana": "{SEMANA_ISO}",
  "url": "{URL_NOTION}",
  "titulo": "{H1 do post}",
  "tipo": "post-proprio-novo"
}
```

Se o arquivo nao existir, criar com a estrutura completa (campos vazios `[]` para os outros).

## Passo 7: Atualizar dor-semana.md

Edite `conhecimento/produto/{brand}/pesquisa/atual/dor-semana.md` para incluir o novo post como **post-ancora 1**:

- Adicionar bloco `### 1. {H1 do post}` no topo dos posts-ancora
- URL = `{URL_NOTION}` (Notion draft) — NOTA: para a news real, o time editorial deve substituir essa URL pela URL do blog publicado quando o post for ao ar. A skill `news-gerar` vai ler do dor-semana.md e citar essa URL — alertar o usuario sobre isso no relatorio final
- Atualizar campo `Status: SUFICIENTE (≥3)` com nota: "Suficiente apos criacao do post novo via news-criar-post"

## Passo 8: Relatorio para o orquestrador

Retorne ao chamador (geralmente `news-pipeline`) um sumario:

```markdown
## Post criado com sucesso

- **H1**: [titulo]
- **Tamanho**: [N] palavras
- **Slug**: {SLUG}
- **Caminho local**: newsletter/{brand}/posts-sugeridos/post-{SLUG}-{SEMANA_ISO}.md
- **URL Notion**: {URL_NOTION}
- **Dor que respondeu**: [nome]

## Acoes do time editorial necessarias antes da news ir ao ar

1. Revisar o draft no Notion ({URL_NOTION})
2. Publicar o post no blog real ({BlogURL})
3. Substituir a URL Notion pela URL final do blog em `dor-semana.md` (post-ancora 1)
4. Confirmar que a news pode ser disparada (apos confirmacao, o pipeline segue para news-gerar)
```

## Regras Criticas

- NUNCA inventar cases reais (usar so os do BRANDBOOK ou exemplos genericos)
- NUNCA inventar metricas, datas ou nomes de empresas
- NUNCA usar conceito tecnico/academico sem verificar definicao
- NUNCA terminar com CTA vendedor — este e post editorial
- ESCREVER no idioma da regiao
- NAO publicar no blog real — so cria draft no Notion
- A news-gerar so deve usar a URL Notion como temporaria; a URL final do blog precisa ser preenchida pelo time editorial antes do disparo
