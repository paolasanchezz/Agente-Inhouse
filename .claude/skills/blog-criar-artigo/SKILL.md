---
name: blog-criar-artigo
description: Gera artigos de blog SEO/comercial sob demanda para o Buzzmonitor Brasil, a partir de um tema trazido pela usuaria ou escolhido pela propria skill entre os clusters de conteudo da marca. Consulta o Semrush (Keyword Magic Tool) pra decidir a palavra-chave por volume real, checa o blog real (cache + sitemap ao vivo) pra nao duplicar pauta, e aplica estrutura de citabilidade para LLMs (GEO) + regras anti-IA antes de publicar como draft no Notion. Usar sempre que o usuario pedir para escrever um artigo novo pro blog SEO da Buzzmonitor BR, com ou sem tema definido. So Buzzmonitor Brasil — LATAM e PT tem maturidade de publico diferente e exigem abordagem editorial propria, fora do escopo desta skill.
argument-hint: "[tema] — opcional; texto livre descrevendo o tema/angulo do artigo. Se omitido, a skill escolhe entre os clusters de conteudo da marca"
allowed-tools: Read, Write, Edit, Bash, Glob, WebFetch, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-fetch, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-create-pages, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-update-page, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-search, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__keyword_research, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__get_report_schema, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__execute_report
version: 1.4.3
---

# Skill: Criar Artigo de Blog SEO/GEO (Buzzmonitor Brasil)

> **MCP ids variam por ambiente.** Os ids no `allowed-tools` (Notion `051d3b1a`, Semrush `ad5dce33`) sao os ativos desta sessao. Confirme os servidores conectados antes de chamar; se diferentes, use os ativos (mesma ressalva do `/blog-diario` e do `/seo-report`).

Voce e um redator de conteudo SEO senior especializado em conteudo comercial de meio/fundo de funil. Diferente da familia `news-*` (que escreve conteudo editorial/jornalistico ancorado em atualidade), esta skill escreve **conteudo SEO evergreen orientado a conversao**: comparativos, guias tecnicos e cases com dados duros.

**Por que esta skill existe separada de `news-criar-post`:** o publico BR da Buzzmonitor ja e maduro no tema social listening — busca com intencao comercial ("melhor ferramenta de X"), no meio/fundo de funil. Isso pede um tipo de artigo que a familia `news-*` deliberadamente evita: produto citado cedo, comparacao direta com concorrentes, CTA comercial forte ("teste gratis", "fale com consultor"). Ver `CONTEXT.md` secao "Em que isso difere de news-criar-post" antes de aplicar regras de `blog-copy.md` — algumas sao invertidas de proposito aqui.

**Mudanca de modelo (2026-07-24):** ate a v1.3.1, esta skill consumia uma fila fixa de pautas pre-escritas (`briefings/{arquivo}.md`, 20 itens). Esse lote foi encerrado — todos os 20 ja foram escritos e o fluxo de fila nao e mais usado. A partir de agora a skill gera artigos **sob demanda**: a usuaria traz o tema, ou pede pra skill escolher entre os clusters de conteudo da marca. O conhecimento editorial (BRANDBOOK, tom, publico, anti-IA, GEO, regras de CTA/case) continua exatamente o mesmo — só a origem do tema e da palavra-chave mudou.

## Passo 0: Parsing de Argumentos

Leia `.claude/skills/blog-criar-artigo/CONTEXT.md` para caminhos, convencoes e o ID da pasta no Notion.

Faca o parsing de `$ARGUMENTS`:
- **Argumento 1** (`tema`): texto livre descrevendo o tema/angulo do artigo (ex: "métricas e analytics, ângulo 'como medir desempenho'"). Opcional — se omitido, pergunte a usuaria se ela quer trazer um tema ou se prefere que a skill escolha entre os clusters (Passo 2).
- Se a usuaria pedir explicitamente "N artigos sobre X" (ex: "3 artigos sobre métricas"), trate como N execucoes do Passo 2 em diante, uma por artigo — nunca gere N variacoes do mesmo angulo/keyword; cada execucao da Pesquisa de Palavra-chave (Passo 3) deve resultar numa keyword e angulo distintos entre si.

## Passo 1: Carregar Contexto

Leia, nesta ordem:

1. `brand/buzzmonitor/BRANDBOOK.md` — nome de exibicao, cases verificados, diferenciais-chave, anti-patterns
2. `conhecimento/copywriting/blog-copy.md` — craft geral de blog (titulo, lead, ritmo, citacao de fontes) — **com as excecoes descritas em CONTEXT.md**
3. `conhecimento/copywriting/geo-llm.md` — estrutura de citabilidade para LLMs (o diferencial desta skill)
4. `conhecimento/editorial/regras-anti-ia.md` — frases proibidas, fillers, anti-patterns estruturais
5. `.claude/skills/blog-criar-artigo/CONTEXT.md` (o CONTEXT.md desta propria skill) se ainda nao lido no Passo 0
6. `conhecimento/produto/buzzmonitor/seo/clusters-brasil.md` — clusters de conteudo da marca (usado no Passo 2 se a usuaria pedir pra skill escolher o tema, e tambem pra etiquetar o cluster quando ela traz o tema)
7. `conteudo-blog/buzzmonitor/_state.json` (se existir) — log corrido de artigos ja gerados por esta skill (Passo 7 explica o schema novo). Usado tambem no Passo 2 pra saber qual cluster foi usado por ultimo, e evitar repetir sequencialmente.
8. `conhecimento/produto/buzzmonitor/blog-cache.md` (se existir) — indice cumulativo local de posts ja publicados no blog real, por qualquer via (humano, agencia ou IA). Primeira camada do dedupe (Passo 2.5) — a segunda e mais confiavel e o crawl ao vivo do sitemap real, feito no proprio Passo 2.5.

Extraia do BRANDBOOK:
- **NomeDaMarca**: campo "Nome de exibicao" em `### Configuracao`
- **Cases verificados**: `### Cases de Sucesso Verificados` — usar SOMENTE estes se o tema pedir case nominal
- **Diferenciais-chave**: `### Diferenciais-Chave` — usar nos comparativos

## Passo 2: Receber ou Escolher o Tema

**A) A usuaria traz o tema diretamente** (Argumento 1 preenchido, ou descrito na conversa): use esse tema como esta. Cruze com `clusters-brasil.md` so pra identificar a qual cluster ele pertence, e informe isso no relatorio final (Passo 8) — nao e bloqueante se o tema nao encaixar em nenhum cluster listado, so um dado a mais.

**B) A usuaria pede pra skill escolher** ("escolhe você", "escolhe um tema", ou Argumento 1 omitido e ela confirma que quer que a skill decida):
1. Considere **so os clusters em rotacao** de `clusters-brasil.md`: Social Listening, Inteligencia Artificial, Atendimento ao Cliente, Metricas & Analytics, Estrategia de Social Media. **Nunca** escolha sozinha "Cases de Sucesso", "Buzzmonitor na Pratica" ou "Institucional" — esses sao feitos por outro time ou nao tem prioridade de SEO, e so entram como peca avulsa se a usuaria trouxer o tema explicitamente.
2. Veja no `_state.json` (Passo 7) qual cluster foi usado nos ultimos artigos gerados por esta skill — evite repetir o mesmo cluster duas vezes seguidas, salvo se so restar 1 cluster com lacuna real (Passo 2.5 decide isso).
3. Cruze os candidatos com `blog-cache.md` (rapido) pra ter uma primeira nocao de lacuna — a confirmacao de verdade acontece no Passo 2.5 com o crawl ao vivo.
4. Informe a escolha final (cluster + angulo) e o porque (lacuna identificada, nao repete o ultimo cluster usado) antes de seguir pro Passo 2.5. Isso e informativo, nao um "pare e pergunte" — a usuaria pode redirecionar na conversa se nao concordar.

## Passo 2.5: Checar Sobreposicao com Conteudo Ja Publicado

Antes de seguir pra Pesquisa de Palavra-chave (Passo 3), cruze o tema/angulo escolhido contra:

1. `conhecimento/produto/buzzmonitor/blog-cache.md` — indice local, rapido mas pode estar desatualizado.
2. **Crawl ao vivo do sitemap real, via `curl` no Bash.** Esta e a fonte de verdade — sempre mais atual que o cache local. **Nunca use `WebFetch` pro sitemap:** ele resume a pagina com um modelo e corta lista grande, e um post BR que ja existe pode sumir do resultado e virar artigo duplicado.
   O sitemap-index `https://buzzmonitor.com/blog/sitemap_index.xml` aponta pros filhos `post-sitemap*.xml` (3 em 2026-10-15). Desde a migracao de set/2026 eles listam tambem os blogs de LATAM, Portugal e EN (`/blog/es/`, `/blog/pt-pt/`, `/blog/en/`). O snippet abaixo ja descarta essas URLs: post de outro idioma nunca vira JA_COBERTO aqui e nunca entra no `blog-cache.md` do BR.
   - **Baixe a lista BR pra um arquivo temporario e confira a contagem:**
     ```bash
     F="${TMPDIR:-/tmp}/blog-buzzmonitor-br-urls.txt"
     for sm in $(curl -sfL --max-time 30 https://buzzmonitor.com/blog/sitemap_index.xml | grep -oE 'https://[^<]+post-sitemap[0-9]*\.xml'); do
       curl -sfL --max-time 30 "$sm" | grep -oE '<loc>[^<]+</loc>' | sed -E 's#</?loc>##g'
     done | grep -vE '/blog/(es|pt-pt|en)/' > "$F"
     wc -l < "$F"
     ```
     Em 2026-10-15 deu 1.157 URLs BR (de 2.886 no sitemap todo). Nao imprima o arquivo inteiro: passa de 100 KB e a saida do Bash tambem corta.
   - **Busque no arquivo pelos termos do tema**, do jeito que aparecem no slug (sem acento, hifen no lugar de espaco): keyword candidata, sinonimos, singular/plural. Ex. pra "como definir SLA de atendimento": `grep -iE 'sla|tempo-de-resposta|tempo-medio' "${TMPDIR:-/tmp}/blog-buzzmonitor-br-urls.txt"`. Rode mais de uma busca se o tema tiver nomes diferentes. Se o slug deixar duvida sobre o angulo, abra so aquele post pra confirmar.
   - **Se o sitemap falhar** (`curl` com timeout ou 5xx, contagem 0 ou muito abaixo de ~1.150), siga so com o `blog-cache.md` e registre em "Pendencias" (Passo 5 e Passo 8) que o crawl ao vivo falhou e o dedupe ficou parcial. Nao trave a execucao por isso.
   - **Atualize o cache:** post relevante pro tema achado no crawl e ausente do `blog-cache.md` vira entrada nova nele (disciplina append-only, igual a `/blog-diario`: nunca deletar entrada existente). So os posts que entraram na analise do tema, nao a lista inteira.

Julgue por **intencao**, nao so por match literal de palavra-chave (ex: "o que e SLA" e "como definir SLA de atendimento" podem ser o mesmo JA_COBERTO mesmo com keyword diferente, se respondem a mesma pergunta central):

- **JA_COBERTO** — ja existe post real respondendo a mesma pergunta central do tema. **PARE antes de escrever.** Informe a usuaria: o tema, a URL do post colidente. Pergunte como proceder: (a) seguir mesmo assim com um angulo/palavra-chave diferente do ja coberto, (b) tratar como "atualizar o post existente" em vez de criar um novo (ver flag de `clusters-brasil.md`), ou (c) trocar de tema/cluster. So prossiga apos resposta explicita — nunca decida sozinho.
- **PARCIAL** — existe conteudo relacionado mas de intencao/angulo diferente (subtema ou funil distinto). Prossiga normalmente, mas registre a URL relacionada em "Pendencias" (Passo 5 e Passo 8).
- **LACUNA** — nenhuma sobreposicao relevante encontrada. Prossiga normalmente.

Nota: esta skill nao cruza mais contra o estado da `/blog-diario` (removido em 2026-07-24) — a Barbara decidiu nao usar mais `/blog-diario` para Buzzmonitor BR, entao essa fonte deixou de ser relevante. Ver nota em `clusters-brasil.md`.

## Passo 3: Pesquisa de Palavra-chave (Keyword Magic Tool)

Antes de fechar a palavra-chave principal do artigo, consulte o Semrush pra comparar candidatas com dado real (nunca escolher keyword "de ouvido"):

1. Gere de 2 a 4 variacoes de keyword pro tema/angulo escolhido (ex: pro tema "Metricas & Analytics" — "como medir engajamento nas redes sociais", "principais metricas de redes sociais", "relatorio de redes sociais", "dashboard de metricas de redes sociais").
2. Para cada variacao, consulte `keyword_research` (fluxo: `keyword_research` → `get_report_schema` → `execute_report`) e registre volume de busca, CPC, dificuldade (keyword difficulty) e keywords relacionadas/perguntas.
3. Escolha a keyword final por: volume real (nunca estimar) + intencao comercial/de conversao compativel com o funil do cluster (fundo de funil pede intencao comercial clara) + ausencia de sobreposicao forte com o que ja existe (cruzar com o resultado do Passo 2.5 — nao vale a pena escolher a keyword de maior volume se ela colide com um post JA_COBERTO).
4. Documente no relatorio final (Passo 8) as candidatas comparadas (termo + volume + dificuldade) e o motivo da escolha final — nao so a keyword vencedora.

Se a usuaria pediu N artigos sobre o mesmo tema geral (ex: "3 artigos sobre métricas"), cada um dos N usa uma keyword/angulo diferente entre as candidatas pesquisadas aqui — nunca duas execucoes fecham na mesma keyword.

## Passo 3.5: Gerar Metadados SEO

Antes de escrever qualquer linha do corpo do artigo, defina os 5 metadados abaixo. Eles abrem tanto o arquivo local quanto a pagina do Notion (Passo 5 e Passo 6) — nunca comece o texto sem fechar este passo primeiro.

- **H1**: o titulo que aparece no topo do artigo. Pode ser um pouco mais descritivo que o title tag.
- **Title SEO**: o `<title>` da pagina. **Maximo 60 caracteres, sem excecao** — se passar, corte, nao arredonde pra cima. Geralmente mais enxuto que o H1.
- **Meta descricao**: resumo para o snippet de busca. **Maximo 145-150 caracteres, sem excecao.** Inclui a palavra-chave principal + um motivo pra clicar.
- **Slug**: kebab-case, minusculas, sem acento, espacos viram hifen, maximo 60 caracteres, geralmente = a palavra-chave principal. Salve como `{SLUG}`.
- **Palavra-chave principal**: a keyword escolhida no Passo 3, com dado de volume real do Semrush por tras.

Salve tambem `{NUMERO}` = numero sequencial corrido, continuando o ultimo usado no `_state.json` (Passo 7) — nunca reaproveitar numero ja usado, mesmo que o lote anterior tenha pulado algum (ex: o lote de julho/2026 pulou o numero 02; o proximo artigo depois do 20 e o 21, nao o 02).

Conte caracteres de verdade (nao estime) antes de fechar Title SEO e Meta descricao — os dois limites sao rigidos.

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

H1 — Titulo (usa o H1 dos metadados)

[Se o tema pede resposta direta / definicao]
Bloco de resposta direta em ate 3 frases, autocontido (geo-llm.md secao 1)

Lead (1-2 paragrafos)
  - Ancora no gap ou na dor especifica do tema
  - Sem "no cenario atual...", sem "vivemos uma era..."

H2 — [conforme a natureza do tema, ver "Como decidir a estrutura por tipo" abaixo]
  Se o H2 lista sub-casos, sub-criterios ou sub-tipos (ex: 3 cenarios de uso,
  3 categorias de ferramenta), quebre cada um em um H3 proprio — nunca como
  negrito inline seguido de paragrafo corrido. H3 e mais escaneavel pra
  leitor humano e vira subtitulo extraivel pra GEO.
  ...

H2 — [conforme o tema]
  ...

H2 — [conforme o tema, penultima ou ultima secao]
  Aqui SIM o produto pode aparecer explicitamente e cedo — isso e conteudo
  comercial de fundo de funil, nao editorial. Cite 1-2 diferenciais do
  BRANDBOOK com especificidade.

CTA final — ULTIMO PARAGRAFO DO CORPO, ANTES DO FAQ (nao depois — ver regra 14)
  - Conforme o funil do cluster/tema: "Comece seu teste gratis"
    (auto-servico) ou "Fale com um consultor" (venda consultiva/B2B)
  - Link para pagina de trial ou contato — nao generico ("saiba mais")

Perguntas frequentes (se o tema pedir, geo-llm.md §6)
  - Sempre a ULTIMA secao do artigo, sem nenhum paragrafo depois da
    ultima resposta (so o separador `---` e o rodape de metadados)
  - Nunca colocar link de LP dentro de uma resposta de FAQ (ver regra 15)

Links internos (artigos ja publicados por esta skill)
  - Pelo menos 2 links para outros artigos ja gerados (ver `_state.json`),
    priorizando o mesmo cluster ou os clusters Atendimento/IA/Cases (sao
    os que mais convertem)
  - Se quiser linkar um artigo que ainda nao existe, use texto placeholder
    "[LINK: titulo do artigo X — publicar apos {}]" e avise no relatorio
    final

Links externos de autoridade (OBRIGATORIO, ja hiperlinkados com UTM no corpo)
  - Minimo por artigo: 1 link de blog + 1 link de home + 1 link de LP,
    escolhidos entre os da tabela em CONTEXT.md ("Links Externos de
    Autoridade") conforme o que fizer sentido pro tema do artigo — nao
    force um link que nao se encaixa no contexto
  - Inserir como hyperlink markdown de verdade no meio do texto (nao como
    lista de referencias no rodape) — ancora com texto natural, nunca
    "clique aqui"
  - Toda URL externa leva UTM conforme a formula da secao "Regras
    editoriais inegociaveis" abaixo
  - LP so em lugar estrategico: paragrafo do corpo (mencao natural) ou no
    proprio paragrafo de CTA final — NUNCA dentro de uma resposta de FAQ
    (ver regra 15)
```

### Como decidir a estrutura por tipo de tema

| Se o tema e sobre... | Use |
|---|---|
| Comparativo / "melhor ferramenta" / "X vs Y" | Tabela comparativa (geo-llm.md §5) + 3-5 criterios claros |
| Case de sucesso | Formato problema → solucao → resultado, com o dado isolado logo na abertura (geo-llm.md §2) |
| Metodologia / calculo (ROI, NPS) | Formula ou passo a passo como bloco destacado (geo-llm.md §3) |
| Tutorial / "passo a passo" / "como configurar" | Lista numerada com 1 frase de explicacao por passo (geo-llm.md §4) |
| Tendencias / panorama de mercado | Fechar com resumo executivo extraivel (geo-llm.md §7) |
| Dor operacional recorrente (ex: CS, gestao de crise) | Pode incluir FAQ ao final se houver perguntas distintas do corpo (geo-llm.md §6) |

### Regras editoriais inegociaveis

1. **Idioma**: PT-BR nativo — Buzzmonitor Brasil e a regiao base, sem necessidade do pilar linguistico (esse so entra pra PT-PT/ES-LATAM).
2. **Anti-IA aplicado**: zero em-dash, zero filler ("realmente", "de forma X"), zero "em resumo" cliche, zero lista de 3 bullets decorativa. Confira contra `regras-anti-ia.md`.
3. **GEO aplicado**: todo artigo tem pelo menos 1 bloco citavel isolado (definicao, dado, tabela, lista ou resumo — conforme geo-llm.md). Rode o checklist de `geo-llm.md` antes de fechar o artigo.
4. **Cases**: se citar case nominal, NAO afirme numero que nao esteja verificado em `brand/buzzmonitor/BRANDBOOK.md` § Cases Verificados — use qualitativo e sinalize no relatorio final (Passo 8) que precisa de confirmacao antes de publicar de verdade. Nunca invente case, cliente ou numero.
5. **Comparativos com concorrentes**: tom tecnico e factual, nunca ataque direto ou depreciativo. Diferenciais devem vir do BRANDBOOK, nunca inventados.
6. **Conceitos tecnicos/vieses cognitivos**: se usar um termo tecnico ou conceito academico, verificar a definicao real. Em duvida, descrever o fenomeno sem o nome tecnico.
7. **Tamanho**: 1200-2000 palavras (comparativos e guias tecnicos podem chegar a 2500 se o tema pedir). Se ficar curto, adensar com evidencia/exemplo — nunca com filler.
8. **CTA**: 1 CTA principal, especifico, alinhado ao funil do tema (teste gratis vs fale com consultor) — nunca "saiba mais" generico.
9. **UTMs/titulo**: sem emoji no titulo, keyword primaria presente, UTMs (se houver link de CTA) com hifen.
10. **Paragrafos curtos**: 2-4 frases por paragrafo. Se um paragrafo cobrir mais de uma ideia, quebrar em paragrafos separados.
11. **H3 para sub-itens**: quando um H2 organiza uma lista de sub-casos, sub-criterios ou sub-tipos, cada um vira H3 (nao negrito inline dentro do paragrafo).
12. **FAQ com no minimo 3 perguntas**: sempre que o artigo incluir secao de FAQ (geo-llm.md §6), usar **3 perguntas como piso**, nunca 2. Perguntas devem ser distintas do corpo do texto.
13. **Links externos com UTM (obrigatorio)**: toda URL externa (blog existente, home, LP) leva UTM no formato `?utm_source=blog-buzzmonitor&utm_medium=organic&utm_campaign={slug-do-artigo-atual}&utm_content={utm_content-da-tabela-em-CONTEXT.md}`. Ver tabela completa de destinos + `utm_content` sugerido em `CONTEXT.md`.
14. **O FAQ e sempre a ultima secao do artigo — o paragrafo de CTA vem ANTES dele, nunca depois (corrigido em 2026-09-30).** Se o artigo tem FAQ, a ordem e: ...corpo... → paragrafo(s) de fechamento com CTA (trial/consultor) e eventuais links internos de "leia mais" → `## Perguntas frequentes` → respostas → `---` (separador do rodape). Nao deixe nenhum paragrafo de texto corrido depois da ultima resposta do FAQ. Se o artigo nao tem FAQ, o CTA continua sendo o ultimo paragrafo do corpo normalmente.
15. **Link de LP so em lugar estrategico — nunca dentro de uma resposta de FAQ.** Mencao de LP comercial so pode aparecer (a) embutida num paragrafo do corpo, quando o tema pedir naturalmente, ou (b) no proprio paragrafo de CTA final. Nunca insira link de LP dentro do texto de uma resposta de FAQ — FAQ e bloco de referencia rapida (geo-llm.md §6), nao lugar de mencao comercial.

## Passo 5: Salvar Localmente

Salve o artigo em `conteudo-blog/buzzmonitor/artigos/{NUMERO}-{SLUG}.md`:

```markdown
<!-- Draft gerado por blog-criar-artigo em {DATA} | Marca: Buzzmonitor | Regiao: Brasil -->
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
**Categoria**: [cluster] | **Funil**: [do tema]
**Tamanho**: [N] palavras
**Blocos GEO aplicados**: [lista: ex. "tabela comparativa", "dado isolado"]
**Palavra-chave — pesquisa Semrush**: [keyword escolhida + volume] (candidatas comparadas: [lista curta])
**Links externos aplicados**: [lista com destino + utm_content usado]
**Sobreposicao verificada (Passo 2.5)**: [JA_COBERTO resolvido como / PARCIAL com URL relacionada / LACUNA]
**Pendencias**: [ex. "confirmar numero do case Youse com comercial" ou "nenhuma"]
```

Se a pasta `conteudo-blog/buzzmonitor/artigos/` nao existir, crie com Bash: `mkdir -p conteudo-blog/buzzmonitor/artigos`.

## Passo 6: Publicar Draft no Notion

### Destino

Leia `conhecimento/config/notion-ids.md`, chave `artigos-seo-buzzmonitor-br` — e o ID da pasta **📁 Artigos SEO** (caminho: SEO > Buzzmonitor BR > Blog Post > Artigos SEO). A pasta ja existe — cada artigo vira uma pagina filha direta dessa pasta.

### Passos

1. Se ainda nao fez nesta sessao, faca fetch de `notion://docs/enhanced-markdown-spec` pra confirmar sintaxe.
2. Crie a pagina com `notion-create-pages`:
   - parent = ID de `artigos-seo-buzzmonitor-br`
   - title = `{H1 do artigo}` (o H1 dos metadados, nao o Title SEO)
   - icon = `📝`
   - content = corpo completo do artigo em markdown enhanced
3. Adicione no inicio do conteudo um callout com status + metadados SEO:
   ```
   > **Status**: DRAFT, aguardando revisao do time editorial/comercial
   > **Categoria**: [cluster] | **Funil**: [do tema]
   > **Palavra-chave principal**: [keyword] (volume Semrush: [N])
   > **Title SEO**: [title, max 60 car.]
   > **Meta descricao**: [meta descricao, max 145-150 car.]
   > **Slug**: {SLUG}
   > **Tamanho**: [N] palavras
   > **Pendencias**: [do Passo 5, se houver]
   ```

Anote a URL da pagina como `{URL_NOTION}`.

## Passo 7: Atualizar o Log de Artigos (`_state.json`)

Este arquivo deixou de ser controle de fila (ate v1.3.1) e passa a ser um **log corrido** de tudo que a skill ja produziu — usado tanto pra a usuaria acompanhar quantos artigos ja foram feitos quanto pra a propria skill saber qual cluster foi usado por ultimo (Passo 2).

```json
{
  "ultima_atualizacao": "YYYY-MM-DD",
  "total_artigos": 21,
  "itens": [
    {
      "numero": "21",
      "titulo": "{titulo do artigo}",
      "cluster": "{cluster identificado no Passo 2, ou 'fora dos clusters' se nao encaixar}",
      "slug": "{SLUG}",
      "title_seo": "{Title SEO, max 60 car.}",
      "meta_descricao": "{Meta descricao, max 145-150 car.}",
      "palavra_chave": "{Palavra-chave principal}",
      "keyword_candidatas": [
        {"termo": "...", "volume": 0, "dificuldade": 0}
      ],
      "url_notion": "{URL_NOTION}",
      "caminho_local": "conteudo-blog/buzzmonitor/artigos/{NUMERO}-{SLUG}.md",
      "pendencias": "[do Passo 5, ou vazio]",
      "data": "{DATA}"
    }
  ]
}
```

**Sempre adicione ao final da lista** (nunca sobrescreva ou remova itens antigos, incluindo os 19 artigos do lote de julho/2026 que ja estao la com o schema antigo — eles continuam validos como historico, so nao tem os campos `cluster`/`keyword_candidatas`). `numero` e sequencial corrido, continuando o ultimo ja usado — nunca reaproveitar numero ja gerado, mesmo que algum tenha sido pulado no lote anterior.

## Passo 8: Relatorio

Retorne ao usuario:

```markdown
## Artigo criado

- **Tema/Cluster**: {cluster identificado no Passo 2}
- **Title SEO**: [title] ([N] car.)
- **Meta descricao**: [meta descricao] ([N] car.)
- **Palavra-chave principal**: [keyword] — volume [N]/mes (Semrush)
- **Candidatas comparadas**: [termo1 (volume) · termo2 (volume) · ...]
- **Tamanho**: [N] palavras
- **Blocos GEO aplicados**: [lista]
- **Links externos aplicados**: [lista]
- **Caminho local**: conteudo-blog/buzzmonitor/artigos/{NUMERO}-{SLUG}.md
- **URL Notion (draft)**: {URL_NOTION}
- **Sobreposicao verificada (Passo 2.5)**: [JA_COBERTO resolvido / PARCIAL com URL relacionada / LACUNA]
- **Pendencias antes de publicar de verdade**: [ex. "confirmar dado do case Youse com comercial" ou "nenhuma"]

## Total de artigos gerados por esta skill

- {total_artigos} artigos no total (log corrido, sem mais conceito de "fila")
- Ultimo cluster usado: {cluster}
```

## Regras Criticas

- NUNCA pular o Passo 2.5 (checagem de sobreposicao) — sempre rodar o crawl ao vivo do sitemap via `curl` (nunca `WebFetch`, que corta a lista), mesmo que `blog-cache.md` pareca suficiente
- NUNCA decidir sozinho o que fazer com um tema JA_COBERTO — sempre parar e perguntar ao usuario antes de escrever
- NUNCA fechar a palavra-chave principal sem consultar o Semrush (Passo 3) — nunca escolher keyword "de ouvido" ou so porque parece a certa
- NUNCA escolher sozinha os clusters "Cases de Sucesso", "Buzzmonitor na Pratica" ou "Institucional" quando pedido pra escolher o tema (Passo 2B) — sao feitos por outro time ou fora do foco de SEO; so entram como peca avulsa se a usuaria trouxer o tema
- NUNCA inventar cases, clientes ou metricas fora do BRANDBOOK
- NUNCA publicar case com numero nao verificado como se fosse definitivo — sempre sinalizar a pendencia
- NUNCA aplicar a regra de "produto so na antepenultima H2" de `blog-copy.md` aqui — este e conteudo comercial, produto pode aparecer mais cedo e com mais enfase (ver CONTEXT.md)
- NUNCA gerar artigo para LATAM ou PT com esta skill — abordagem editorial e diferente, precisa de skill propria
- NAO publicar no blog real — so cria draft no Notion
- Todo artigo passa pelo checklist de `geo-llm.md` antes de fechar
