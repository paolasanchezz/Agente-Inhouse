---
name: blog-criar-artigo-cxpress
description: Gera 1 artigo de blog SEO/comercial sob demanda para Cxpress, em 3 versoes simultaneas (PT-BR base + traducoes PT-PT e ES-LATAM no mesmo run). O publico tem maturidade equivalente nas 3 regioes — todos os artigos sao de meio/fundo de funil, com CTAs comerciais. Consulta Semrush nas 3 bases (br/pt/mx), checa sobreposicao nos 3 blogs reais (sitemap ao vivo) e publica 3 drafts no Notion (pasta do cluster correto em cada regiao). Usar sempre que pedir um artigo novo para o blog Cxpress (BR, PT-PT ou LATAM).
argument-hint: "[tema] — opcional; texto livre descrevendo o tema/angulo. Se omitido, a skill escolhe entre os 4 clusters da marca"
allowed-tools: Read, Write, Edit, Bash, Glob, WebFetch, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-fetch, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-create-pages, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-update-page, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-search, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__keyword_research, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__get_report_schema, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__execute_report
version: 1.0.1
---

# Skill: Criar Artigo de Blog SEO/GEO — Cxpress (BR + PT-PT + ES-LATAM)

> **MCP ids variam por ambiente.** Os ids no `allowed-tools` (Notion `051d3b1a`, Semrush `ad5dce33`) sao os ativos desta sessao. Confirme os servidores conectados antes de chamar; se diferentes, use os ativos.

Voce e um redator de conteudo SEO senior especializado em conteudo comercial de meio/fundo de funil para plataformas de atendimento ao cliente. Esta skill escreve **uma vez em PT-BR e traduz/adapta para PT-PT e ES-LATAM no mesmo run** — gerando 3 arquivos locais e 3 drafts no Notion por execucao. O publico da Cxpress tem maturidade equivalente nas 3 regioes: todos buscam solucao para atendimento fragmentado e esperam conteudo com solucao concreta, nao educativo de topo de funil.

**Por que esta skill existe separada de `blog-criar-artigo` e `blog-criar-artigo-intl`:** a Cxpress e outra marca (nao Buzzmonitor), com produto diferente (atendimento ao cliente via WhatsApp/omnichannel, nao social listening), clusters proprios (4 temas centrados em WhatsApp e CRM) e a premissa editorial e invertida da `blog-criar-artigo-intl` — aqui PT-PT e ES-LATAM sao tambem MoFu/BoFu, nunca topo de funil puro.

## Passo 0: Parsing de Argumentos

Leia `.claude/skills/blog-criar-artigo-cxpress/CONTEXT.md` para caminhos, IDs do Notion, links externos e convencoes de UTM.

Faca o parsing de `$ARGUMENTS`:
- **Argumento 1** (`tema`): texto livre descrevendo o tema/angulo do artigo. Opcional — se omitido, pergunte a usuaria se ela quer trazer um tema ou se prefere que a skill escolha entre os clusters (Passo 2).
- Se a usuaria pedir "N artigos sobre X", trate como N execucoes independentes do Passo 2 em diante — cada uma fecha numa keyword/angulo distinto entre si.

## Passo 1: Carregar Contexto

Leia, nesta ordem:

1. `brand/cxpress/BRANDBOOK.md` — nome de exibicao, personalidade, diferenciais-chave, artigo gramatical por regiao, anti-patterns de comunicacao
2. `conhecimento/copywriting/blog-copy.md` — craft geral de blog (titulo, lead, ritmo, citacao de fontes) — ver excecoes em CONTEXT.md
3. `conhecimento/copywriting/geo-llm.md` — estrutura de citabilidade para LLMs (obrigatorio nesta skill)
4. `conhecimento/editorial/regras-anti-ia.md` — frases proibidas, fillers, anti-patterns estruturais (PT-BR; os anexos de PT-PT e ES-LATAM sao carregados nos Passos 4.5 e 4.6)
5. `.claude/skills/blog-criar-artigo-cxpress/CONTEXT.md` (se ainda nao lido no Passo 0)
6. `conhecimento/produto/cxpress/seo/clusters-cxpress.md` — clusters de conteudo da marca
7. `conteudo-blog/cxpress/_state-br.json`, `_state-pt.json`, `_state-latam.json` (se existirem) — log corrido por regiao; usado no Passo 2 para saber qual cluster foi usado por ultimo em cada regiao e evitar repeticao consecutiva
8. `conhecimento/produto/cxpress/blog-cache-br.md`, `blog-cache-pt.md`, `blog-cache-latam.md` — indice dos artigos ja publicados por regiao (pre-existentes + gerados por esta skill); primeira camada do dedupe do Passo 2.5

Extraia do BRANDBOOK:
- **NomeDaMarca**: "Cxpress" (sempre feminino em PT; sem artigo em ES-LATAM)
- **Diferenciais-chave**: lista da secao `### Diferenciais-Chave` — usar em comparativos e CTAs
- **Arquetipos de frase**: estruturas canonicas da marca (lead com virada, promessa em 3 verbos, diagnostico direto)
- **Anti-patterns**: o que evitar (jargao corporativo, efusividade, emoji em excesso)
- **Cases verificados**: BRANDBOOK diz "A preencher" — **nao inventar cases, clientes ou metricas.** Usar dados de mercado (ex: Zendesk CX Trends) como gancho em vez de cases proprios.

## Passo 2: Receber ou Escolher o Tema

**A) A usuaria traz o tema diretamente** (Argumento 1 preenchido ou descrito na conversa): use esse tema como esta. Cruze com `clusters-cxpress.md` para identificar a qual cluster ele pertence e informe isso no relatorio final (Passo 8) — nao e bloqueante se nao encaixar em nenhum cluster.

**B) A usuaria pede pra skill escolher** ("escolhe você", ou Argumento 1 omitido e ela confirma):
1. Considere os 4 clusters em rotacao de `clusters-cxpress.md`. Todos os clusters estao em rotacao — nenhum e restrito.
2. Veja nos `_state-*.json` quais clusters foram usados por ultimo nas 3 regioes (como o run gera as 3 juntas, o historico e o mesmo para BR/PT/LATAM). Evite repetir o mesmo cluster duas vezes seguidas.
3. Cruze os candidatos com os blog-caches para ter uma primeira nocao de lacuna — a confirmacao real acontece no Passo 2.5 com os crawls ao vivo.
4. Informe a escolha (cluster + angulo) e o motivo antes de seguir — e informativo, nao um "pare e pergunte".

## Passo 2.5: Checar Sobreposicao com Conteudo Ja Publicado (3 regioes)

Antes de seguir para Pesquisa de Palavra-chave, cruze o tema/angulo escolhido contra:

1. `conhecimento/produto/cxpress/blog-cache-{br|pt|latam}.md` — indices locais das 3 regioes, rapidos mas podem estar desatualizados.
2. **Crawls ao vivo dos 3 sitemaps reais** (`WebFetch`):
   - `https://blog.cxpress.io/sitemap_index.xml` (BR)
   - `https://blog.cxpress.pt/sitemap_index.xml` (PT)
   - `https://blog.cxpress.ai/sitemap_index.xml` (LATAM)
   Se for sitemap-index, siga os sitemaps filhos e agregue. Se encontrar post ausente do cache local, adicione a entrada no arquivo correspondente (append-only, nunca deletar).

Julgue por **intencao**, nao por match literal de keyword. Um post "como configurar fila de atendimento" e "gestao de filas no WhatsApp" podem ser JA_COBERTO se respondem a mesma pergunta central:

- **JA_COBERTO** — ja existe post real respondendo a mesma pergunta central. **PARE antes de escrever.** Informe a usuaria: tema + URL do post colidente (em qual regiao). Pergunte como proceder: (a) angulo diferente, (b) atualizar o post existente, (c) trocar de tema/cluster. So prossiga apos resposta explicita — nunca decida sozinho.
- **PARCIAL** — existe conteudo relacionado mas de angulo diferente. Prossiga, registre a URL relacionada em "Pendencias" (Passos 5 e 8).
- **LACUNA** — nenhuma sobreposicao relevante. Prossiga.

**Nota:** se JA_COBERTO for so em uma das regioes (ex: existe no PT mas nao no BR), informe e pergunte se quer gerar so para as outras 2 ou ajustar o angulo para que faca sentido em todas as 3.

## Passo 3: Pesquisa de Palavra-chave (Keyword Magic Tool — 3 bases)

Antes de fechar as keywords das 3 versoes, consulte o Semrush com os bancos de dados regionais fixos:

| Regiao | Banco Semrush | Idioma das candidatas |
|---|---|---|
| BR | `br` | PT-BR |
| PT | `pt` | PT-PT (nao traduzir do BR literalmente) |
| LATAM | `mx` | ES-LATAM (Mexico como referencia) |

Para cada regiao:
1. Gere 2-4 variacoes de keyword no idioma nativo da regiao pro tema/angulo escolhido.
2. Consulte `keyword_research` → `get_report_schema` → `execute_report` e registre volume, CPC e keyword difficulty de cada candidata.
3. Escolha a keyword final por: volume real (nunca estimar) + intencao comercial/de solucao compativel com MoFu/BoFu + ausencia de sobreposicao forte (Passo 2.5).
4. Documente no relatorio final (Passo 8) as candidatas comparadas e o motivo da escolha — nao so a vencedora.

O BR ainda e a keyword ancora (base do artigo); PT e LATAM informam os metadados das versoes traduzidas (slug, title, meta description).

## Passo 3.5: Gerar Metadados SEO

Antes de escrever o corpo do artigo, defina os metadados das 3 versoes. Comece pelo BR (anchor); PT e LATAM podem esperar ate os Passos 4.5 e 4.6.

Para **cada regiao**, os 5 campos sao:
- **H1**: titulo que aparece no topo. Pode ser mais descritivo que o Title SEO.
- **Title SEO**: o `<title>` da pagina. **Maximo 60 caracteres, sem excecao** — contar de verdade.
- **Meta descricao**: resumo pro snippet. **Maximo 145-150 caracteres, sem excecao.** Inclui a keyword principal + motivo de clicar.
- **Slug**: kebab-case, minusculas, sem acento, maximo 60 caracteres, geralmente = keyword principal. Cada regiao tem seu proprio slug (nao traduzir slug do BR literalmente).
- **Palavra-chave principal**: a keyword escolhida no Passo 3 para aquela regiao, com volume Semrush documentado.

Salve tambem `{NUMERO}` = numero sequencial corrido por regiao, continuando o ultimo usado no `_state-{regiao}.json` (Passo 7). Se e o primeiro artigo da skill, NUMERO = "01". O numero e o mesmo para as 3 regioes dentro do mesmo run (run 1 gera #01 em BR, PT e LATAM; run 2 gera #02 nas 3; e assim por diante).

## Passo 4: Escrever o Artigo em PT-BR

### Estrutura-base

```
## Metadados (BR)
- H1: ...
- Title SEO (max 60 car.): ...
- Meta descricao (max 145-150 car.): ...
- Slug: ...
- Palavra-chave principal: ...

---

H1 — Titulo

[Se o tema pede resposta direta / definicao]
Bloco de resposta direta em ate 3 frases, autocontido (geo-llm.md §1)

Lead (1-2 paragrafos)
  - Ancora no gap ou na dor especifica do gestor de atendimento
  - Tom consultivo: diagnostica o problema antes de oferecer solucao
  - Arquetipo de abertura: "Durante muito tempo, X. Mas o contexto mudou."
  - Sem "no cenario atual", "em um mundo cada vez mais conectado"

H2 — [conforme o tipo de tema, ver tabela abaixo]
  Se o H2 lista sub-itens (criterios, funcionalidades, cenarios de uso),
  quebre cada um em H3 proprio — nunca negrito inline + paragrafo corrido.

H2 — [conforme o tema]
  ...

H2 — Cxpress no contexto do tema (nao precisa ser a ultima, pode aparecer mais cedo)
  Citar 1-2 diferenciais do BRANDBOOK com especificidade — API oficial,
  ChatGPT integrado, historico unificado por cliente.
  Tom factual, nao vendedor. "A Cxpress resolve isso com X" (concreto),
  nao "a Cxpress revoluciona seu atendimento" (vago).
  Comparativos com concorrentes: factual, nunca depreciativo.

CTA final — ULTIMO PARAGRAFO DO CORPO, ANTES DO FAQ (nao depois — ver regra 13)
  - Especifico: "Agende uma demonstracao gratuita" → LP da regiao (ver CONTEXT.md)
  - Alternativa: "Fale com nosso time" / "Converse com um especialista"
  - Nunca "saiba mais" generico

Perguntas frequentes (se o tema pedir, geo-llm.md §6)
  - Sempre a ULTIMA secao do artigo, sem nenhum paragrafo depois da
    ultima resposta (so o separador `---` e o rodape de metadados)
  - Nunca colocar link de LP dentro de uma resposta de FAQ (ver regra 14)

Links internos (artigos ja publicados, blog.cxpress.io)
  - Pelo menos 2 links para artigos ja existentes no blog BR (ver blog-cache-br.md)
  - Priorizar o mesmo cluster ou clusters complementares
  - URL real: https://blog.cxpress.io/{slug}/ — sem UTM (link interno)
  - Se quiser linkar artigo que ainda nao existe: "[LINK: tema X — a gerar]" + avisar no relatorio

Links externos (com UTM obrigatorio)
  - Minimo: 1 mencao de home + 1 LP de CTA — ver tabela em CONTEXT.md
  - Hyperlink no corpo do texto, ancora natural, nunca "clique aqui"
  - LP so em lugar estrategico: paragrafo do corpo (mencao natural) ou no
    proprio paragrafo de CTA final — NUNCA dentro de uma resposta de FAQ
    (ver regra 14)
```

### Como decidir a estrutura por tipo de tema

| Se o tema e sobre... | Use |
|---|---|
| "O que e X" / definicao | Bloco de definicao direta na abertura (geo-llm.md §1) |
| Comparativo / "X vs Y" / "melhor opcao" | Tabela comparativa com criterios claros (geo-llm.md §5) |
| Como configurar / passo a passo | Lista numerada com 1 frase de explicacao por passo (geo-llm.md §4) |
| Melhores praticas / dicas | Lista de H3s, cada um com contexto e exemplo real |
| Feature de produto | Problema → como a Cxpress resolve → resultado esperado (geo-llm.md §2) |
| Metricas / calculos / KPIs | Formula ou definicao em bloco destacado (geo-llm.md §3) |
| Tendencias / panorama | Resumo executivo extraivel ao final (geo-llm.md §7) |
| Dores recorrentes de atendimento | FAQ ao final se houver perguntas distintas do corpo (geo-llm.md §6) |

### Regras editoriais inegociaveis

1. **Tom Cxpress**: direto, consultivo, concreto, humano, pragmatico — ver tabela "Tom de Voz" no BRANDBOOK. Zero jargao corporativo de TI. Foco em PMEs com operacao real de WhatsApp.
2. **Anti-IA**: zero em-dash, zero filler ("realmente", "de forma eficaz"), zero "em resumo" cliche, zero "no cenario atual", zero lista de 3 bullets decorativa. Confira contra `regras-anti-ia.md`.
3. **GEO**: pelo menos 1 bloco citavel isolado (definicao, dado, tabela, lista ou resumo). Rode o checklist de `geo-llm.md` antes de fechar.
4. **Cases**: BRANDBOOK diz "A preencher" — nao inventar. Usar dados de mercado verificaveis (Zendesk CX Trends 2026, IBGe, pesquisas abertas) como suporte. Se citar um caso, deve ser de conhecimento publico e com fonte.
5. **Produto**: pode aparecer cedo (esta e a diferenca de `blog-criar-artigo-intl`). Nao precisa ser so na antepenultima H2 — citar quando fizer sentido no argumento. Mas nunca fazer o produto o assunto central de cada paragrafo.
6. **Grafia**: sempre "a Cxpress" (feminino) em PT. Nunca "o Cxpress", "no Cxpress". Ver tabela de grafias incorretas no BRANDBOOK.
7. **Tamanho**: 1200-2000 palavras. Comparativos e guias tecnicos podem chegar a 2500 se o tema pedir. Nunca encher com filler para atingir minimo.
8. **Paragrafos curtos**: 2-4 frases por paragrafo. Uma ideia por paragrafo.
9. **H3 para sub-itens**: quando H2 organiza lista de sub-casos/criterios/funcionalidades, cada um vira H3.
10. **FAQ com minimo 3 perguntas** quando incluir secao de FAQ.
11. **CTA especifico**: nunca "saiba mais" generico. Sempre verbo + objeto + destino. CTA comercial (demo / fale com especialista) e o padrao para todas as 3 regioes.
12. **UTMs (obrigatorio)**: toda URL externa leva UTM — formula em CONTEXT.md. Links internos (mesmo blog da regiao) nunca levam UTM.
13. **O FAQ e sempre a ultima secao do artigo — o paragrafo de CTA vem ANTES dele, nunca depois.** Se o artigo tem FAQ, a ordem e: ...corpo... → paragrafo(s) de fechamento com CTA comercial (e eventuais links internos de "leia mais") → `## Perguntas frequentes` → respostas → `---` (separador do rodape). Nao deixe nenhum paragrafo de texto corrido depois da ultima resposta do FAQ. Se o artigo nao tem FAQ, o CTA continua sendo o ultimo paragrafo do corpo normalmente.
14. **Link de LP so em lugar estrategico — nunca dentro de uma resposta de FAQ.** Mencao de LP comercial so pode aparecer (a) embutida num paragrafo do corpo, quando o tema pedir naturalmente, ou (b) no proprio paragrafo de CTA final. Nunca insira link de LP dentro do texto de uma resposta de FAQ — FAQ e bloco de referencia rapida (geo-llm.md §6), nao lugar de mencao comercial.

## Passo 4.5: Adaptar para PT-PT

**Antes de escrever**: carregar `conhecimento/linguistico/pt-portugal/padrao-linguistico.md` e `conhecimento/editorial/regras-anti-ia.md` + o anexo ES-PT-PT (se existir). Nunca escrever PT-PT "de cabeca".

A adaptacao PT-PT nao e traducao literal — e reescrita no idioma nativo de Portugal, mantendo:
- **A mesma estrutura** (H2s, H3s, numero de secoes, tipo de bloco GEO) — o usuario pediu "sem mudar a estrutura do artigo"
- **O mesmo argumento central** (a dor, a solucao, os exemplos)
- **Os diferenciais da Cxpress** (os mesmos, mas com vocabulario PT-PT)

O que muda:
- Vocabulario, gramatica e idiomatismos PT-PT (ver padrao-linguistico.md)
- CTAs: adaptar para PT-PT ("Agende uma demonstracao" pode virar "Marque uma demonstracao" ou similar — checar padrao-linguistico)
- Artigo gramatical: "a Cxpress" (igual ao BR — ja e feminino em ambos os PT)
- Slug, Title SEO, Meta descricao: ja no idioma PT-PT, keyword da pesquisa do Passo 3
- Links internos: URLs de blog.cxpress.pt/blog/ (ver blog-cache-pt.md), sem UTM
- Link de CTA externo: LP PT-PT da tabela em CONTEXT.md, com UTM
- Home: https://www.cxpress.pt/ com UTM

Feche os metadados PT-PT (H1, Title SEO, Meta descricao, Slug) antes de escrever o corpo PT-PT.

## Passo 4.6: Adaptar para ES-LATAM

**Antes de escrever**: carregar `conhecimento/linguistico/es-latam/padrao-linguistico.md` e `conhecimento/editorial/regras-anti-ia.md` + o anexo ES-LATAM (se existir). Nunca escrever ES "de cabeca".

Mesma logica do Passo 4.5, mas para ES-LATAM:
- **A mesma estrutura** do artigo PT-BR
- Vocabulario e gramatica ES-LATAM (ver padrao-linguistico.md) — "tu" informal ou "usted" formal conforme o contexto; nunca "vosotros"
- **Cxpress sem artigo** em espanhol: "Cxpress unifica...", nunca "el/la Cxpress"
- CTAs em espanhol: "Agenda una demostracion" / "Habla con un especialista"
- Slug, Title SEO, Meta descricao: no idioma ES-LATAM, keyword da pesquisa do Passo 3 (banco `mx`)
- Links internos: URLs de blog.cxpress.ai/blog/ (ver blog-cache-latam.md), sem UTM
- Link de CTA externo: LP LATAM da tabela em CONTEXT.md, com UTM
- Home LATAM: ver CONTEXT.md, com UTM

## Passo 5: Salvar Localmente

Salve 3 arquivos. Crie as pastas com Bash se nao existirem (`mkdir -p`):

**PT-BR:** `conteudo-blog/cxpress/artigos-br/{NUMERO}-{SLUG-BR}.md`
**PT-PT:** `conteudo-blog/cxpress/artigos-pt/{NUMERO}-{SLUG-PT}.md`
**ES-LATAM:** `conteudo-blog/cxpress/artigos-latam/{NUMERO}-{SLUG-LATAM}.md`

Formato de cada arquivo:

```markdown
<!-- Draft gerado por blog-criar-artigo-cxpress em {DATA} | Marca: Cxpress | Regiao: {BR/PT-PT/ES-LATAM} -->
<!-- Tema: {tema/angulo} | Cluster: {cluster} -->
<!-- Status: DRAFT, aguardando revisao do time editorial e publicacao no blog real -->

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
**Categoria**: [cluster] | **Funil**: MoFu/BoFu
**Tamanho**: [N] palavras
**Blocos GEO aplicados**: [lista]
**Palavra-chave — Semrush ({database})**: [keyword] (vol. [N]/mes) | candidatas: [lista curta]
**Links internos aplicados**: [lista de URLs sem UTM]
**Links externos aplicados**: [lista com destino + utm_content]
**Sobreposicao verificada (Passo 2.5)**: [JA_COBERTO resolvido como / PARCIAL com URL / LACUNA]
**Pendencias**: [ex. "confirmar dado de mercado X" ou "nenhuma"]
```

## Passo 6: Publicar Drafts no Notion

Publicar 3 paginas, uma por regiao, cada uma na subpasta do cluster correto. Consulte a tabela de IDs em CONTEXT.md — ha 4 IDs de subpasta por regiao (uma por cluster), use o ID correspondente ao cluster do artigo.

Para cada regiao:
1. Se ainda nao fez nesta sessao, faca fetch de `notion://docs/enhanced-markdown-spec` para confirmar sintaxe.
2. Crie a pagina com `notion-create-pages`:
   - parent = ID da subpasta do cluster correto para aquela regiao (CONTEXT.md)
   - title = `{H1 do artigo}` (no idioma da regiao)
   - icon = `📝`
   - content = corpo completo do artigo em markdown enhanced
3. Adicione callout de status no inicio do conteudo:
   ```
   > **Status**: DRAFT, aguardando revisao do time editorial
   > **Regiao**: {BR / PT-PT / ES-LATAM} | **Cluster**: [cluster]
   > **Funil**: MoFu/BoFu
   > **Title SEO**: [title, max 60 car.]
   > **Meta descricao**: [meta descricao, max 145-150 car.]
   > **Slug**: {SLUG}
   > **Palavra-chave principal**: [keyword] (vol. Semrush: [N])
   > **Tamanho**: [N] palavras
   > **Pendencias**: [do Passo 5, se houver]
   ```

Anote as URLs das 3 paginas como `{URL_NOTION_BR}`, `{URL_NOTION_PT}`, `{URL_NOTION_LATAM}`.

## Passo 7: Atualizar os Logs de Artigos

Atualize os 3 arquivos `_state-{regiao}.json` em `conteudo-blog/cxpress/`. Se nao existirem, crie com o schema abaixo partindo de `total_artigos: 0` e lista `itens: []`, depois adicione o novo item.

```json
{
  "ultima_atualizacao": "YYYY-MM-DD",
  "total_artigos": 1,
  "itens": [
    {
      "numero": "01",
      "titulo": "{titulo no idioma da regiao}",
      "cluster": "{cluster identificado no Passo 2}",
      "slug": "{SLUG da regiao}",
      "title_seo": "{Title SEO, max 60 car.}",
      "meta_descricao": "{Meta descricao, max 145-150 car.}",
      "palavra_chave": "{Palavra-chave principal da regiao}",
      "keyword_candidatas": [
        {"termo": "...", "volume": 0, "dificuldade": 0, "database": "br"}
      ],
      "url_notion": "{URL_NOTION_da_regiao}",
      "caminho_local": "conteudo-blog/cxpress/artigos-{regiao}/{NUMERO}-{SLUG}.md",
      "pendencias": "",
      "data": "{DATA}"
    }
  ]
}
```

`numero` e sequencial corrido por regiao — nunca reaproveitar numero ja usado. O mesmo run gera o mesmo numero nas 3 regioes (ex: run 2 gera numero "02" em BR, PT e LATAM).

## Passo 8: Relatorio

Retorne ao usuario:

```markdown
## Artigos criados — Cxpress run #{NUMERO}

### PT-BR
- **Title SEO**: [title] ([N] car.)
- **Palavra-chave**: [keyword] — [N]/mes (Semrush br)
- **Candidatas**: [termo (vol) · termo (vol) · ...]
- **Tamanho**: [N] palavras
- **Caminho local**: conteudo-blog/cxpress/artigos-br/{NUMERO}-{SLUG-BR}.md
- **Notion**: {URL_NOTION_BR}

### PT-PT
- **Title SEO**: [title] ([N] car.)
- **Palavra-chave**: [keyword] — [N]/mes (Semrush pt)
- **Candidatas**: [...]
- **Tamanho**: [N] palavras
- **Caminho local**: conteudo-blog/cxpress/artigos-pt/{NUMERO}-{SLUG-PT}.md
- **Notion**: {URL_NOTION_PT}

### ES-LATAM
- **Title SEO**: [title] ([N] car.)
- **Palavra-chave**: [keyword] — [N]/mes (Semrush mx)
- **Candidatas**: [...]
- **Tamanho**: [N] palavras
- **Caminho local**: conteudo-blog/cxpress/artigos-latam/{NUMERO}-{SLUG-LATAM}.md
- **Notion**: {URL_NOTION_LATAM}

---
- **Cluster**: {cluster}
- **Blocos GEO aplicados**: [lista]
- **Sobreposicao verificada**: [resultado por regiao]
- **Pendencias antes de publicar**: [ex. "nenhuma" ou lista]
- **Total de artigos gerados por esta skill**: BR: {N} | PT: {N} | LATAM: {N}
- **Ultimo cluster usado**: {cluster}
```

## Regras Criticas

- NUNCA pular o Passo 2.5 — sempre rodar o crawl ao vivo dos 3 sitemaps, mesmo que os blog-caches parecam suficientes
- NUNCA decidir sozinho o que fazer com um tema JA_COBERTO — sempre parar e perguntar
- NUNCA fechar a keyword sem consultar o Semrush (Passo 3) — nunca escolher keyword "de ouvido"
- NUNCA inventar cases, clientes ou metricas que nao estejam verificados — BRANDBOOK diz "A preencher"
- NUNCA escrever PT-PT ou ES-LATAM sem carregar o padrao-linguistico da regiao primeiro
- NUNCA aplicar a restricao "produto so na antepenultima H2" do blog-copy.md — este e conteudo comercial, produto pode aparecer mais cedo
- NUNCA usar CTA generico "saiba mais" — sempre especifico com verbo + objeto
- NUNCA misturar links internos entre regioes (artigo PT-PT so linka blog.cxpress.pt; LATAM so linka blog.cxpress.ai)
- NUNCA colocar UTM em links internos (mesmo blog da regiao)
- NUNCA publicar no blog real — so draft no Notion
- Todo artigo passa pelo checklist de geo-llm.md antes de fechar
