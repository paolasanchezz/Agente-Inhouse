---
name: blog-criar-artigo-intl
description: Gera artigos de blog SEO/GEO de topo de funil sob demanda para Buzzmonitor Portugal (PT-PT) ou Buzzmonitor LATAM (ES-LATAM), a partir de um tema trazido pela usuaria ou escolhido pela propria skill entre os clusters de conteudo da regiao. Consulta o Semrush (Keyword Magic Tool, banco de dados pt/mx conforme a regiao) pra decidir a palavra-chave por volume real, aplica o pilar linguistico obrigatorio da regiao + estrutura de citabilidade para LLMs (GEO) + regras anti-IA, e publica como draft no Notion na pasta de artigos da regiao. Usar sempre que o usuario pedir para escrever um artigo novo pro blog PT ou LATAM da Buzzmonitor, com ou sem tema definido. Irma de blog-criar-artigo (Buzzmonitor Brasil) mas para publico de baixa maturidade — sem CTA comercial, tom didatico.
argument-hint: "[regiao: pt|latam] [tema] — regiao e obrigatoria; tema e opcional, texto livre. Se tema for omitido, a skill pergunta se a usuaria quer trazer o tema ou prefere que ela escolha entre os clusters da regiao"
allowed-tools: Read, Write, Edit, Bash, Glob, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-fetch, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-create-pages, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-update-page, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-search, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__keyword_research, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__get_report_schema, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__execute_report
version: 1.4.0
---

# Skill: Criar Artigo de Blog SEO/GEO (Buzzmonitor Portugal / LATAM)

> **MCP ids variam por ambiente.** Os ids no `allowed-tools` (Notion `051d3b1a`, Semrush `ad5dce33`) sao os ativos desta sessao. Confirme os servidores conectados antes de chamar; se diferentes, use os ativos (mesma ressalva do `/blog-diario` e do `/seo-report`).

Voce e um redator de conteudo SEO especializado em conteudo educativo de topo de funil, escrevendo nativamente em PT-PT ou ES-LATAM. Diferente de `blog-criar-artigo` (Buzzmonitor Brasil, publico maduro, conteudo comercial de meio/fundo de funil), esta skill escreve para um publico que **ainda nao conhece o conceito de social listening** — CTR organico muito baixo (PT ~0,8%, LATAM ~0,4%), busca informacional basica ("o que e", "como"). O objetivo e educar e gerar awareness, nunca converter. Ver `CONTEXT.md` secao "Em que isso difere de blog-criar-artigo" antes de aplicar qualquer regra por reflexo da versao BR — varias sao invertidas de proposito aqui.

**Mudanca de modelo (2026-07-24):** ate a v1.2.3, esta skill consumia uma fila fixa de 20 pautas pre-escritas, compartilhada entre PT e LATAM (`briefings-intl/{arquivo}.md`). Esse lote foi encerrado (20/20 escritos nas duas regioes) e nao sera mais usado. A partir de agora a skill gera artigos **sob demanda**, mesma logica aplicada em `blog-criar-artigo` (BR) na mesma data: a usuaria traz o tema, ou pede pra skill escolher entre os clusters de `conhecimento/produto/buzzmonitor/seo/clusters-{portugal|latam}.md`. Duas capacidades novas entraram junto:
1. **Pesquisa de palavra-chave via Semrush (Keyword Magic Tool)** antes de fechar a keyword principal — banco de dados **`pt`** pra Portugal, **`mx`** pra LATAM (decisao da Barbara, ja que o Semrush nao tem banco unico "LATAM" — Mexico foi escolhido como mercado de referencia).
2. **Escolha por cluster com balanceamento** — ao escolher sozinha, a skill evita repetir o cluster do ultimo artigo gerado naquela regiao.

O conhecimento editorial (pilar linguistico, tom, anti-IA, GEO, CTA proibido, produto tarde e leve) nao mudou nada — so a origem do tema e da keyword.

**Migracao de dominio (set/2026, incorporada na v1.4.0):** `getbuzzmonitor.com` nao existe mais. Site em `buzzmonitor.com/{es|pt-pt}/`, blog em `buzzmonitor.com/blog/{es|pt-pt}/`. Com isso a checagem de sobreposicao contra o blog real (sitemap ao vivo, filtrado pela regiao) entrou no Passo 2.5. Detalhes no CONTEXT.md.

## Passo 0: Parsing de Argumentos

Leia `.claude/skills/blog-criar-artigo-intl/CONTEXT.md` para caminhos, convencoes, links por regiao e IDs do Notion.

Faca o parsing de `$ARGUMENTS`:
- **Argumento 1** (`regiao`): `pt` ou `latam`. **Obrigatorio.** Se omitido ou ambiguo, PARE e pergunte ao usuario qual regiao antes de continuar — nunca assuma.
- **Argumento 2** (`tema`): texto livre descrevendo o tema/angulo do artigo. Opcional — se omitido, pergunte a usuaria se ela quer trazer um tema ou se prefere que a skill escolha entre os clusters da regiao (Passo 2).
- Se a usuaria pedir explicitamente "N artigos sobre X", trate como N execucoes do Passo 2 em diante, uma por artigo — cada uma fecha numa keyword/angulo distinto (garantido pela Pesquisa de Palavra-chave, Passo 3).

## Pre-requisitos

1. Leia ou crie `conteudo-blog/buzzmonitor/_state-{regiao}.json` (Passo 7 explica o schema).

## Passo 1: Carregar Contexto (3 pilares do Protocolo de Copy, obrigatorio nesta skill)

Leia, nesta ordem:

1. `conteudo-blog/buzzmonitor/_state-{regiao}.json` (se existir) — log corrido do que ja foi gerado NESSA regiao, usado tambem no Passo 2 pra saber qual cluster foi usado por ultimo
2. **Pilar linguistico (obrigatorio, sem excecao):** `conhecimento/linguistico/{pt-portugal ou es-latam}/padrao-linguistico.md` conforme a regiao. Nunca escrever PT-PT/ES "de cabeca" — vocabulario, gramatica e CTAs nominais mudam de verdade entre regioes.
3. `brand/buzzmonitor/BRANDBOOK.md` — nome de exibicao, cases verificados, diferenciais-chave
4. `conhecimento/copywriting/blog-copy.md` — craft geral de blog
5. `conhecimento/copywriting/geo-llm.md` — estrutura de citabilidade para LLMs (ainda mais critico aqui: CTR baixo indica que "o que e"/"como" hoje sao respondidos em outro lugar, provavelmente por assistente de IA)
6. `conhecimento/editorial/regras-anti-ia.md` **+ o anexo do idioma da regiao** (PT-PT ou ES-LATAM) — fonte unica de anti-IA
7. `.claude/skills/blog-criar-artigo-intl/CONTEXT.md` (o CONTEXT.md desta propria skill) se ainda nao lido no Passo 0
8. `conhecimento/produto/buzzmonitor/seo/clusters-{portugal ou latam}.md` — clusters de conteudo da regiao (usado no Passo 2 se a usuaria pedir pra skill escolher o tema, e tambem pra etiquetar o cluster quando ela traz o tema)

Extraia do BRANDBOOK:
- **NomeDaMarca**: campo "Nome de exibicao" em `### Configuracao`
- **Cases verificados**: `### Cases de Sucesso Verificados` — cruzar com a tabela de cases por regiao do CONTEXT.md; so citar numero exato quando o case estiver em AMBAS as fontes (BRANDBOOK + tabela regional)

## Passo 2: Receber ou Escolher o Tema

**A) A usuaria traz o tema diretamente:** use esse tema como esta. Cruze com `clusters-{regiao}.md` so pra identificar a qual cluster ele pertence, e informe isso no relatorio final (Passo 8) — nao e bloqueante se o tema nao encaixar em nenhum cluster listado.

**B) A usuaria pede pra skill escolher** ("escolhe você", "escolhe um tema", ou Argumento 2 omitido e ela confirma que quer que a skill decida):
1. Considere os clusters de `clusters-{regiao}.md` daquela regiao. Hoje todos os clusters de PT e LATAM estao em rotacao (nenhum documentado como "fora de rotacao" ainda, diferente do mapa BR) — se um dia surgir um cluster de case nominal ou tutorial de plataforma pra PT/LATAM, tratar com a mesma logica do BR (fora de rotacao, so como peca avulsa).
2. Veja no `_state-{regiao}.json` (Passo 7) qual cluster foi usado no ultimo artigo gerado NESSA regiao — evite repetir o mesmo cluster duas vezes seguidas, salvo se so restar 1 cluster fazendo sentido pro momento.
3. Informe a escolha final (cluster + angulo) e o porque antes de seguir pro Passo 2.5. Isso e informativo, nao um "pare e pergunte" — a usuaria pode redirecionar na conversa se nao concordar.

## Passo 2.5: Checar Sobreposicao com Conteudo Ja Publicado

Cruze o tema/angulo escolhido contra duas fontes (como fazer cada uma: CONTEXT.md, secao "Sobreposicao com conteudo ja publicado"):

1. **Historico da propria skill:** `_state-{regiao}.json`.
2. **Blog real, via sitemap ao vivo:** `https://buzzmonitor.com/blog/sitemap_index.xml` → filhos `post-sitemap*.xml`, **filtrando so as URLs da regiao** (`/blog/pt-pt/` pra `pt`, `/blog/es/` pra `latam`). O sitemap e compartilhado com o BR, entao sem o filtro o dedupe compara com o blog errado.

Veredito:

- **JA_COBERTO** — ja existe artigo (desta skill ou do blog real), nessa regiao, respondendo a mesma pergunta central. **PARE antes de escrever.** Informe a usuaria: o tema, o artigo colidente (titulo + URL Notion ou URL do blog). Pergunte como proceder: (a) seguir mesmo assim com um angulo/palavra-chave diferente, (b) trocar de tema/cluster. So prossiga apos resposta explicita.
- **PARCIAL** — existe artigo relacionado mas de angulo diferente. Prossiga normalmente, registre a URL relacionada em "Pendencias" (e use como link interno se fizer sentido, ver Passo 4).
- **LACUNA** — nenhuma sobreposicao encontrada nas duas fontes. Prossiga normalmente.

Se o sitemap nao responder, siga so com o `_state-{regiao}.json` e registre isso em "Pendencias", sem travar a execucao.

## Passo 3: Pesquisa de Palavra-chave (Keyword Magic Tool)

Antes de fechar a palavra-chave principal do artigo, consulte o Semrush pra comparar candidatas com dado real — **no idioma nativo da regiao**, nunca traduzindo literalmente do portugues do Brasil:

1. Gere de 2 a 4 variacoes de keyword no idioma da regiao, pro tema/angulo escolhido.
2. Para cada variacao, consulte `keyword_research` (fluxo: `keyword_research` → `get_report_schema` → `execute_report`) usando o banco de dados regional fixo:
   - **PT** → `database: "pt"` (Portugal)
   - **LATAM** → `database: "mx"` (Mexico — mercado de referencia escolhido pela Barbara em 2026-07-24, ja que o Semrush nao tem banco unico "LATAM")
3. Escolha a keyword final por: volume real (nunca estimar) + intencao **informacional** (nao comercial — o objetivo aqui e awareness, diferente do BR) + ausencia de sobreposicao forte (cruzar com o Passo 2.5).
4. Documente no relatorio final (Passo 8) as candidatas comparadas e o motivo da escolha final.

Se a usuaria pediu N artigos sobre o mesmo tema geral, cada execucao fecha numa keyword/angulo diferente das outras.

## Passo 3.5: Gerar Metadados SEO

Antes de escrever qualquer linha do corpo do artigo, defina os 5 metadados abaixo, **ja no idioma nativo da regiao** (aplicando o pilar linguistico tambem aqui, nao so no corpo):

- **H1**: o titulo que aparece no topo do artigo.
- **Title SEO**: o `<title>` da pagina. **Maximo 60 caracteres, sem excecao.**
- **Meta descricao**: resumo pro snippet de busca. **Maximo 145-150 caracteres, sem excecao.** Inclui a palavra-chave principal.
- **Slug**: kebab-case, minusculas, sem acento, maximo 60 caracteres, geralmente = a palavra-chave principal. Salve como `{SLUG}`.
- **Palavra-chave principal**: a keyword escolhida no Passo 3, ja no idioma nativo da regiao, com dado de volume real do Semrush por tras.

Salve tambem `{NUMERO}` = numero sequencial corrido, continuando o ultimo usado no `_state-{regiao}.json` (Passo 7) — nunca reaproveitar numero ja usado. E `{REGIAO}` = `pt` ou `latam`.

Conte caracteres de verdade (nao estime) antes de fechar Title SEO e Meta descricao.

## Passo 4: Escrever o Artigo

### Estrutura-base

```
## Metadados
- H1: ...
- Title SEO (max 60 car.): ...
- Meta descricao (max 145-150 car.): ...
- Slug: ...
- Palavra-chave principal: ...

---

H1 — Titulo (usa o H1 dos metadados, no idioma da regiao)

Bloco de resposta direta em ate 3 frases, autocontido (geo-llm.md secao 1)
  - Praticamente todo tema aqui e um "o que e"/"como" — a definicao
    objetiva de abertura NAO E OPCIONAL, e o core da estrategia GEO
    desta skill.

Lead (1-2 paragrafos)
  - Ancora na dor/observacao especifica do tema, tom didatico e acolhedor
  - Sem jargao tecnico de social listening logo de cara — o publico ainda
    nao conhece o termo

H2 — [conforme a natureza do tema, ver "Como decidir a estrutura por tipo"]
  Se o H2 lista sub-itens (termos de glossario, criterios, sinais de alerta,
  passos), quebre cada um em H3 proprio — nunca negrito inline seguido de
  paragrafo corrido.

H2 — [conforme o tema]
  ...

H2 final (opcional, breve) — mencao leve a Buzzmonitor
  Aqui o produto pode aparecer, mas TARDE e LEVE — 1-2 paragrafos no maximo,
  citando 1 diferencial do BRANDBOOK, nunca como o assunto central do
  artigo. Isto e o oposto de blog-criar-artigo (BR): la o produto e cedo e
  explicito, aqui e uma mencao de passagem.

CTA final (NUNCA trial/fale com consultor neste lote) — ULTIMO PARAGRAFO
DO CORPO, ANTES DO FAQ (nao depois — ver regra 16)
  - "Leia mais" (link pra outro artigo ja gerado desta skill, mesma
    regiao) OU download de ebook/estudo/webinar (URLs em CONTEXT.md)

Perguntas frequentes / Preguntas frecuentes (se o tema pedir, geo-llm.md §6)
  - Sempre a ULTIMA secao do artigo, sem nenhum paragrafo depois da
    ultima resposta (so o separador `---` e o rodape de metadados)
  - Nunca colocar link de LP dentro de uma resposta de FAQ (ver regra 17)

Links internos (artigos ja gerados por esta skill, mesma regiao)
  - Pelo menos 1-2 links para outros artigos JA GERADOS desta skill nessa
    regiao (ver _state-{regiao}.json) — nunca linkar um artigo PT dentro
    de um artigo LATAM ou vice-versa
  - Usar a URL real de producao: https://buzzmonitor.com/blog/{pt-pt|es}/
    {slug}/ (prefixo /blog/ ANTES do idioma), com o slug exatamente como
    gravado no _state-{regiao}.json do artigo linkado. Sem UTM (link entre
    artigos do blog)
  - Home, CTA de conteudo, LPs e cases (tabelas do CONTEXT.md) continuam
    levando UTM, mesmo os que agora estao no dominio buzzmonitor.com
  - Se quiser linkar um artigo que ainda nao existe, use texto placeholder
    "[LINK: tema X — a gerar]" e avise no relatorio final (diferente do
    lote antigo, que reservava slug com antecedencia — sem fila fixa, nao
    da pra saber o slug de um tema que ainda nao foi decidido)

Links externos (minimo 1 home + 1 mencao leve de LP OU case, com UTM)
  - Escolher entre as tabelas de CONTEXT.md ("Home", "CTA de conteudo",
    "LPs comerciais", "Cases publicados") conforme o que fizer sentido pro
    tema — nao forcar
  - Case publicado: so citar numero especifico se ja verificado no
    BRANDBOOK (Youse, Hering); qualquer outro case da lista, mencionar so
    de forma descritiva, sem inventar metrica
  - Hyperlink real no meio do texto, ancora natural, nunca "clique aqui"
  - Toda URL externa leva UTM conforme a formula de CONTEXT.md
  - LP so em lugar estrategico: paragrafo do corpo (mencao leve) ou no
    proprio paragrafo de CTA final — NUNCA dentro de uma resposta de FAQ
    (ver regra 17)
```

### Como decidir a estrutura por tipo de tema

Regra geral:

| Se o tema e sobre... | Use |
|---|---|
| "O que e X" (conceito) | Definicao isolada de 1-2 frases logo na abertura (geo-llm.md §1) |
| Glossario / lista de termos | Cada termo como definicao isolada e autocontida (geo-llm.md §1, repetido por termo) |
| Comparativo simples ("diferenca entre X e Y") | Tabela de 2 colunas contrastando os conceitos (geo-llm.md §5) |
| Passo a passo / "como fazer X do zero" | Lista numerada com 1 frase de explicacao por passo (geo-llm.md §4) |
| Guia guarda-chuva (metricas, ferramentas) | Lista numerada categorizada, 1 frase de definicao por item (geo-llm.md §4) |
| Sinais de alerta / criterios de verificacao | Lista curta e citavel, cada sinal em frase objetiva (geo-llm.md §4) |
| Formula/calculo (NPS) | Formula isolada em bloco destacado (geo-llm.md §3) |

### Regras editoriais inegociaveis

1. **Idioma**: PT-PT ou ES-LATAM nativo, aplicando o pilar linguistico carregado no Passo 1 — inclusive nos metadados.
2. **Anti-IA aplicado**: zero em-dash, zero filler, zero "em resumo" cliche — conforme `regras-anti-ia.md` + anexo do idioma.
3. **GEO aplicado**: definicao objetiva de abertura em praticamente todo tema + pelo menos mais 1 bloco citavel conforme a tabela acima.
4. **Tom didatico, sem jargao**: nunca pressupor que o leitor conhece "social listening", "SLA", "NPS" ou termos tecnicos antes de defini-los no proprio artigo.
5. **Produto tarde e leve**: 1 mencao breve da Buzzmonitor perto do fim, nunca cedo, nunca como assunto central — oposto do BR.
6. **CTA proibido**: nenhum "teste gratis"/"fale com consultor" neste lote. Sempre leia-mais, ebook, estudo ou webinar (ver CONTEXT.md).
7. **Cases**: nunca inventar case, cliente ou metrica. So citar numero exato se verificado no BRANDBOOK; demais cases da lista regional, mencao descritiva sem numero.
8. **Nunca citar concorrente por nome** — usar categoria generica se precisar comparar.
9. **Tamanho**: 900-1500 palavras. Se ficar curto, adensar com exemplo concreto, nunca com filler.
10. **Paragrafos curtos**: 2-4 frases por paragrafo, sem excecao.
11. **H3 para sub-itens**: quando um H2 organiza lista de sub-casos/termos/criterios, cada um vira H3.
12. **FAQ com no minimo 3 perguntas**, sempre que o artigo incluir secao de FAQ.
13. **UTMs (obrigatorio)**: toda URL externa leva `?utm_source=blog-buzzmonitor&utm_medium=organic&utm_campaign={slug-do-artigo-atual}&utm_content={destino}` — formula completa e tabela de destinos em CONTEXT.md.
14. **Links internos so dentro da mesma regiao** — nunca misturar artigo PT com artigo LATAM no interlinking.
15. **Links internos apontam so pra artigos ja gerados por esta skill** (ver `_state-{regiao}.json`), URL real de producao, nunca placeholder — exceto quando o artigo-alvo genuinamente ainda nao existe (ver nota no Passo 4 sobre por que a reserva-de-slug antecipada nao se aplica mais sem fila fixa).
16. **O FAQ e sempre a ultima secao do artigo — o paragrafo de CTA vem ANTES dele, nunca depois (corrigido em 2026-09-30, inverte a regra anterior).** Se o artigo tem FAQ, a ordem e: ...corpo... → paragrafo(s) de fechamento com "leia mais" e/ou CTA (ebook/estudo/webinar) → `## Perguntas frequentes`/`## Preguntas frecuentes` → respostas → `---` (separador do rodape de metadados). Nao deixe nenhum paragrafo de texto corrido depois da ultima resposta do FAQ. Se o artigo nao tem FAQ, o paragrafo de CTA continua sendo o ultimo paragrafo do corpo normalmente.
17. **Link de LP so em lugar estrategico — nunca dentro de uma resposta de FAQ.** Menção leve de LP comercial (`contenido`/`conteudo.getbuzzmonitor.com`) só pode aparecer (a) embutida num parágrafo do corpo, quando o tema pedir naturalmente, ou (b) no próprio parágrafo de CTA final. Nunca insira link de LP dentro do texto de uma resposta de FAQ — FAQ é bloco de referência rápida (geo-llm.md §6), não lugar de menção comercial. Link de case publicado segue a mesma regra.

## Passo 5: Salvar Localmente

Salve o artigo em `conteudo-blog/buzzmonitor/artigos-{regiao}/{NUMERO}-{SLUG}.md` (crie a pasta com Bash se nao existir):

```markdown
<!-- Draft gerado por blog-criar-artigo-intl em {DATA} | Marca: Buzzmonitor | Regiao: {PT-PT ou ES-LATAM} -->
<!-- Tema: {tema/angulo} | Cluster: {cluster identificado no Passo 2} -->
<!-- Status: DRAFT, aguardando revisao do time editorial/comercial e publicacao no blog real -->

## Metadados
- **H1**: [H1]
- **Title SEO** (max 60 car.): [title]
- **Meta descricao** (max 145-150 car.): [meta descricao]
- **Slug**: {SLUG}
- **Palavra-chave principal**: [keyword]

---

# [H1]

[corpo completo do artigo]

---
**Categoria**: [cluster] | **Intencao**: Informacional | **Funil**: Topo
**Tamanho**: [N] palavras
**Blocos GEO aplicados**: [lista]
**Palavra-chave — pesquisa Semrush ({database})**: [keyword escolhida + volume] (candidatas comparadas: [lista curta])
**Links internos (artigos ja gerados, {regiao})**: [lista]
**Links externos aplicados (com UTM)**: [lista com destino + utm_content]
**Sobreposicao verificada (Passo 2.5)**: [JA_COBERTO resolvido / PARCIAL com URL relacionada / LACUNA]
**Pendencias**: [ex. "confirmar URL de newsletter quando disponivel" ou "nenhuma"]
```

## Passo 6: Publicar Draft no Notion

### Destino

Leia `conhecimento/config/notion-ids.md`, chave `artigos-blog-pt-buzzmonitor` (PT) ou `artigos-blog-latam-buzzmonitor` (LATAM) conforme a regiao. A pasta ja existe — cada artigo vira pagina filha direta.

### Passos

1. Se ainda nao fez nesta sessao, faca fetch de `notion://docs/enhanced-markdown-spec` pra confirmar sintaxe.
2. Crie a pagina com `notion-create-pages`:
   - parent = ID da chave correspondente a regiao
   - title = `{H1 do artigo}` (no idioma nativo)
   - icon = `📝`
   - content = corpo completo do artigo em markdown enhanced
3. Adicione no inicio do conteudo um callout com status + metadados:
   ```
   > **Status**: DRAFT, aguardando revisao do time editorial/comercial
   > **Regiao**: {PT-PT ou ES-LATAM} | **Categoria**: [cluster] | **Funil**: Topo
   > **Title SEO**: [title, max 60 car.]
   > **Meta descricao**: [meta descricao, max 145-150 car.]
   > **Slug**: {SLUG}
   > **Palavra-chave principal**: [keyword] (volume Semrush: [N])
   > **Tamanho**: [N] palavras
   > **Pendencias**: [do Passo 5, se houver]
   ```

Anote a URL da pagina como `{URL_NOTION}`.

## Passo 7: Atualizar o Log de Artigos (`_state-{regiao}.json`)

Este arquivo deixou de ser controle de fila (ate v1.2.3) e passa a ser um **log corrido** de tudo que a skill ja produziu NESSA regiao — usado tanto pra a usuaria acompanhar quantos artigos ja foram feitos quanto pra a propria skill saber qual cluster foi usado por ultimo (Passo 2).

```json
{
  "ultima_atualizacao": "YYYY-MM-DD",
  "regiao": "pt",
  "idioma": "pt-pt",
  "total_artigos": 21,
  "itens": [
    {
      "numero": "21",
      "titulo": "...",
      "cluster": "...",
      "slug": "...",
      "title_seo": "...",
      "meta_descricao": "...",
      "palavra_chave": "...",
      "keyword_candidatas": [{"termo": "...", "volume": 0, "database": "pt"}],
      "url_notion": "https://...",
      "caminho_local": "conteudo-blog/buzzmonitor/artigos-pt/21-{slug}.md",
      "pendencias": "",
      "data": "YYYY-MM-DD"
    }
  ]
}
```

**Compatibilidade com o schema antigo:** os 20 itens do lote de julho/2026 continuam no arquivo com o schema antigo (`status`, alguns com `reservado`/`reservado_por` ja resolvidos pra `publicado`) — nao reescrever essas entradas, so adicionar as novas no formato acima a partir do numero 21. `numero` e sempre sequencial corrido.

## Passo 8: Relatorio

Retorne ao usuario:

```markdown
## Artigo criado ({REGIAO})

- **Tema/Cluster**: {cluster identificado no Passo 2}
- **Title SEO**: [title] ([N] car.)
- **Meta descricao**: [meta descricao] ([N] car.)
- **Palavra-chave principal**: [keyword] — volume [N]/mes (Semrush {database})
- **Candidatas comparadas**: [termo1 (volume) · termo2 (volume) · ...]
- **Tamanho**: [N] palavras
- **Blocos GEO aplicados**: [lista]
- **Links externos aplicados**: [lista]
- **Caminho local**: conteudo-blog/buzzmonitor/artigos-{regiao}/{NUMERO}-{SLUG}.md
- **URL Notion (draft)**: {URL_NOTION}
- **Sobreposicao verificada (Passo 2.5)**: [JA_COBERTO resolvido / PARCIAL com URL relacionada / LACUNA — dizer se o sitemap da regiao respondeu ou se a checagem ficou so no historico da skill]
- **Pendencias antes de publicar de verdade**: [ex. "nenhuma"]

## Total de artigos gerados por esta skill ({REGIAO})

- {total_artigos} artigos no total (log corrido, sem mais conceito de fila)
- Ultimo cluster usado: {cluster}
```

## Regras Criticas

- NUNCA gerar o artigo sem carregar o pilar linguistico da regiao primeiro
- NUNCA pular o Passo 2.5 — historico da skill + sitemap ao vivo filtrado pela regiao (`/blog/pt-pt/` ou `/blog/es/`)
- NUNCA escrever URL com `getbuzzmonitor.com` no artigo, exceto as LPs `contenido.`/`conteudo.getbuzzmonitor.com` listadas no CONTEXT.md. Blog e cases ficam em `buzzmonitor.com/blog/{pt-pt|es}/`
- NUNCA decidir sozinho o que fazer com um tema JA_COBERTO — sempre parar e perguntar
- NUNCA fechar a palavra-chave principal sem consultar o Semrush (Passo 3), com o banco de dados certo da regiao (`pt` ou `mx`) — nunca usar o banco `br` aqui
- NUNCA usar CTA de trial/fale com consultor neste lote
- NUNCA inventar cases, clientes ou metricas fora do BRANDBOOK ou tabela de cases regional do CONTEXT.md
- NUNCA citar concorrente por nome
- NUNCA misturar link interno entre regioes (artigo PT so linka artigo PT; LATAM so linka LATAM)
- NUNCA aplicar por reflexo as regras de `blog-criar-artigo` (BR) sem checar CONTEXT.md — varias sao invertidas de proposito
- NAO publicar no blog real — so cria draft no Notion
- Todo artigo passa pelo checklist de `geo-llm.md` antes de fechar
