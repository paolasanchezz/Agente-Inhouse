# Contexto Compartilhado — blog-criar-artigo

> Skill standalone (nao faz parte da familia `news-*`). So Buzzmonitor Brasil.

---

## Origem e escopo

Nasceu de um diagnostico de maturidade de publico feito pela usuaria fora deste repo: o publico BR da Buzzmonitor ja e maduro em social listening, busca com intencao comercial/tecnica ("melhor ferramenta de X") e converte ~50% dos leads organicos em reuniao. Por isso o conteudo prioriza meio/fundo de funil: comparativos, guias tecnicos, cases com dados duros.

LATAM e PT tem mercados menos maduros — a abordagem editorial la e outra (mais educativa/topo de funil), nao so uma questao de idioma. Por isso essas regioes ficam **fora do escopo** desta skill. Desde 2026-07-22 existe a skill irma `blog-criar-artigo-intl` (argumento `[regiao]` = `pt`/`latam`) especificamente pra isso — ver `.claude/skills/blog-criar-artigo-intl/CONTEXT.md`.

**Mudanca de modelo (2026-07-24, decisao da Barbara):** ate a v1.3.1 esta skill consumia uma fila fixa de 20 pautas pre-escritas pela Barbara (`conteudo-blog/buzzmonitor/briefings/2026-07-artigos-prioritarios-br.md`). Esse lote foi encerrado (19/20 escritos — o item 02 nunca foi gerado) e nao sera mais usado. A partir de agora a skill gera artigos **sob demanda**: a Barbara traz o tema, ou pede pra skill escolher entre os clusters de `conhecimento/produto/buzzmonitor/seo/clusters-brasil.md`. Duas capacidades novas entraram junto com essa mudanca:
1. **Checagem ao vivo do blog real** (crawl de sitemap via `WebFetch`), alem do `blog-cache.md` local — antes o dedupe so olhava cache local + estado da `/blog-diario`.
2. **Pesquisa de palavra-chave via Semrush (Keyword Magic Tool)** antes de fechar a keyword principal — antes a keyword vinha pronta, escrita a mao no item do briefing.

O conhecimento editorial (tom, publico, anti-IA, GEO, regras de CTA/case) nao mudou nada — so a origem do tema e da keyword.

**Sobre a `/blog-diario` pra Buzzmonitor:** decisao da Barbara em 2026-07-23 — nao usar mais `/blog-diario` para Buzzmonitor BR (rodou 2x em 2026-06-30, ver `blog-seo/buzzmonitor/_state.json`, mas nao sera mais usada pra essa marca). A `blog-criar-artigo` cobre esse papel agora. Por isso o Passo 2.5 nao cruza mais contra o estado da `/blog-diario` — ela deixou de ser fonte relevante de sobreposicao pra essa marca.

## Em que isso difere de `news-criar-post`

| Aspecto | `news-criar-post` (familia news-*) | `blog-criar-artigo` |
|---|---|---|
| Fonte do tema | Gap analysis automatico (`news-pesquisar`) | Tema trazido pela usuaria, ou escolhido pela skill entre os clusters da marca |
| Origem da keyword | — | Pesquisa Semrush (Keyword Magic Tool), nunca "de ouvido" |
| Genero | Editorial/jornalistico, ancorado em atualidade | SEO comercial evergreen |
| Onde o produto aparece | So na antepenultima H2, nunca comparado a concorrente | Pode aparecer cedo; comparativos diretos com concorrentes sao formato esperado |
| CTA | Suave, "conheca o feature" | Comercial forte: "teste gratis" / "fale com consultor", conforme o funil do tema |
| Guia estrutural principal | `blog-copy.md` sozinho | `blog-copy.md` (craft geral) + `geo-llm.md` (estrutura de citabilidade) |
| Regioes | brasil / latam / portugal (arg da familia) | So brasil — hardcoded, sem arg de regiao |

**Nao misturar as duas.** Se o usuario pedir um artigo editorial ancorado em noticia recente, isso e `pauta-quente` ou `news-criar-post`, nao esta skill.

## Clusters de conteudo

Fonte: `conhecimento/produto/buzzmonitor/seo/clusters-brasil.md` (mesmo arquivo historicamente usado pela `/blog-diario`, agora consumido principalmente por esta skill — ver nota de uso por skill dentro do proprio arquivo).

- **Clusters em rotacao** (a skill pode escolher sozinha quando pedido): Social Listening, Inteligencia Artificial, Atendimento ao Cliente, Metricas & Analytics, Estrategia de Social Media.
- **Clusters fora de rotacao** (so como peca avulsa trazida pela usuaria, nunca escolhidos sozinhos pela skill): Cases de Sucesso e Buzzmonitor na Pratica (feitos por outro time), Institucional (sem prioridade de SEO organico).
- Ao escolher sozinha, a skill cruza: cluster nao repetido em relacao ao ultimo artigo gerado (`_state.json`) + lacuna real (`blog-cache.md` + sitemap ao vivo, Passo 2.5).

## Caminhos

- **Artigos gerados (local)**: `conteudo-blog/buzzmonitor/artigos/{NUMERO}-{SLUG}.md`
- **Log corrido de artigos**: `conteudo-blog/buzzmonitor/_state.json`
- **Clusters da marca**: `conhecimento/produto/buzzmonitor/seo/clusters-brasil.md`
- **Cache do blog real**: `conhecimento/produto/buzzmonitor/blog-cache.md`
- **Fila antiga (historico, nao usar mais)**: `conteudo-blog/buzzmonitor/briefings/2026-07-artigos-prioritarios-br.md` — mantida so como referencia de como os 19 primeiros artigos foram decididos, nao e mais consumida pela skill.

## Notion

- Chave em `conhecimento/config/notion-ids.md`: `artigos-seo-buzzmonitor-br`
- Caminho no workspace: SEO > Buzzmonitor BR > Blog Post > 📁 Artigos SEO
- A pasta e o destino final direto — cada artigo = 1 pagina filha direta, title = H1 do artigo, icon `📝`.

## Pesquisa de palavra-chave (Semrush Keyword Magic Tool) — Passo 3

Adicionado em 2026-07-24. Fluxo: `keyword_research` → `get_report_schema` → `execute_report`, comparando 2-4 candidatas por tema antes de fechar a keyword principal. Criterios de escolha: volume real (nunca estimar) + intencao comercial compativel com o funil do cluster + ausencia de sobreposicao forte (cruzar com o Passo 2.5). Documentar as candidatas comparadas no relatorio final, nao so a vencedora — isso da rastreabilidade de por que aquela keyword foi escolhida, util se a Barbara quiser revisar a decisao depois.

Se pedido "N artigos sobre X", cada execucao fecha numa keyword diferente das outras N-1 — a pesquisa deste passo e o que garante que os angulos nao se sobreponham entre si.

## Links Externos de Autoridade (obrigatorio, minimo 1 blog + 1 home + 1 LP por artigo)

Fornecidos pela usuaria em 2026-07-20: posts do blog real que ja performam bem no organico, a home e as LPs comerciais. Objetivo duplo: reforcar autoridade topica via interlinking (cluster → pillar) e dar ao time comercial rastreabilidade de origem SEO via UTM.

**Formula de UTM (aplicar em toda URL externa, sem excecao):**
```
?utm_source=blog-buzzmonitor&utm_medium=organic&utm_campaign={slug-do-artigo-atual}&utm_content={utm_content-da-tabela}
```
`{slug-do-artigo-atual}` = o `{SLUG}` gerado no Passo 3.5 pro artigo que esta sendo escrito (nao o slug do destino). `{utm_content}` vem da coluna abaixo.

| Destino | URL base | `utm_content` | Quando usar |
|---|---|---|---|
| Blog: Melhores ferramentas de social listening | `https://buzzmonitor.com/blog/melhores-ferramentas-de-social-listening/` | `melhores-ferramentas-social-listening` | Comparativos de ferramentas |
| Blog: KPIs nas redes sociais | `https://buzzmonitor.com/blog/kpis-nas-redes-sociais-o-que-e-e-como-analisar/` | `kpis-redes-sociais` | Artigos do cluster Metricas & Analytics |
| Blog: Social listening (o que e, como fazer, importancia) | `https://buzzmonitor.com/blog/social-listening-o-que-e-como-fazer-e-qual-a-sua-importancia/` | `social-listening-conceito` | Contexto/definicao geral do conceito (cluster → pillar page) |
| Blog: Monitoramento de concorrentes | `https://buzzmonitor.com/blog/5-possibilidades-oferecidas-pelo-monitoramento-de-concorrentes/` | `monitoramento-concorrentes` | Artigos que tocam em acompanhamento de concorrencia |
| Blog: IA para redes sociais | `https://buzzmonitor.com/blog/inteligencia-artificial-para-redes-sociais/` | `ia-redes-sociais` | Artigos do cluster IA |
| Blog: Case Hering (+11 pts NPS em 12 meses) | `https://buzzmonitor.com/blog/como-a-hering-aumentou-em-11-pontos-o-nps-da-marca-em-12-meses-com-social-listening-estrategico/` | `case-hering-nps` | Artigos de Cases de Sucesso sobre NPS/percepcao de marca |
| Home | `https://buzzmonitor.com/` | `home` | 1 mencao geral da marca, cedo no texto |
| LP: Plataforma completa | `https://conteudo.buzzmonitor.com.br/plataforma-completa` | `plataforma-completa` | CTA generico ou artigo que cobre a plataforma como um todo |
| LP: Plataforma completa (listening) | `https://conteudo.buzzmonitor.com.br/plataforma-completa-listening` | `plataforma-completa-listening` | CTA de artigos dos clusters Social Listening / Metricas & Analytics |
| LP: Plataforma completa (atendimento) | `https://conteudo.buzzmonitor.com.br/plataforma-completa-atendimento` | `plataforma-completa-atendimento` | CTA de artigos do cluster Atendimento ao Cliente |

**Como aplicar:**
- Nao forcar as 3 categorias se nao fizer sentido, mas o piso e 1 blog + 1 home + 1 LP por artigo.
- Escolher qual LP usar pelo cluster do tema (ver coluna "Quando usar"), nao por padrao fixo.
- Hyperlink de verdade no corpo do texto, com anchor text natural — nunca em lista de referencias separada nem "clique aqui".
- Se surgir um destino novo (post do blog, LP nova) fora desta tabela, perguntar a usuaria antes de usar — nao inventar URL nem `utm_content`.

## Checagem de sobreposicao com conteudo ja publicado (Passo 2.5)

Adicionado em 2026-07-23, atualizado em 2026-07-24. Fontes cruzadas antes de escrever:
- `conhecimento/produto/buzzmonitor/blog-cache.md` — indice cumulativo local do blog real. Append-only, nunca deletar entrada.
- **Crawl ao vivo do sitemap real** (`https://buzzmonitor.com/blog/sitemap.xml`, via `WebFetch`) — adicionado em 2026-07-24. Fonte de verdade, sempre mais atual que o cache local. Post encontrado no crawl mas ausente do cache vira entrada nova no `blog-cache.md`.
- **Filtro de idioma (2026-10-15):** com a migracao de LATAM/PT pra `buzzmonitor.com` (set/2026), o mesmo sitemap passou a listar `/blog/es/`, `/blog/pt-pt/` e `/blog/en/`. Pro BR, descartar essas URLs: elas nao contam como sobreposicao e nao entram no `blog-cache.md`.

Removido em 2026-07-24: a checagem contra `blog-seo/buzzmonitor/_state.json` (estado da `/blog-diario`) — a Barbara decidiu nao usar mais `/blog-diario` para Buzzmonitor BR, entao essa fonte deixou de ser relevante pra esta skill.

Veredito por intencao (JA_COBERTO / PARCIAL / LACUNA), nao por match literal de keyword. Em JA_COBERTO, a skill **para e pergunta** — nunca decide sozinha se segue, pula ou ajusta o angulo.

**Nota:** a `blog-criar-artigo-intl` (PT/LATAM) usa o mesmo sitemap desde a v1.4.0, so que filtrando pelo prefixo da regiao em vez de descartar. Ver `.claude/skills/blog-criar-artigo-intl/CONTEXT.md`.

## Schema de `_state.json` (log corrido, desde 2026-07-24)

```json
{
  "ultima_atualizacao": "YYYY-MM-DD",
  "total_artigos": 21,
  "itens": [
    {
      "numero": "01",
      "titulo": "Social listening para e-commerce",
      "slug": "social-listening-para-e-commerce",
      "title_seo": "Social listening para e-commerce: guia",
      "meta_descricao": "O que e social listening para e-commerce, por que importa e como comecar a monitorar sua marca.",
      "palavra_chave": "social listening para e-commerce",
      "status": "publicado",
      "url_notion": "https://...",
      "caminho_local": "conteudo-blog/buzzmonitor/artigos/21-{slug}.md",
      "pendencias": "",
      "data": "YYYY-MM-DD"
    }
  ]
}
```

**Compatibilidade com o schema antigo:** os 19 itens do lote de julho/2026 (numeros 01-20, faltando o 02) continuam no arquivo com o schema antigo (sem `cluster`/`keyword_candidatas`, com `status`/`pendencias` no formato anterior) — nao reescrever/migrar essas entradas, so adicionar as novas no formato acima a partir do numero 21. `numero` e sempre sequencial corrido; nunca reaproveitar um numero ja usado, mesmo que tenha sido pulado (ex: o 02 nunca existiu, mas o proximo apos o 20 e o 21, nao o 02).

## Quando NAO usar esta skill

- Artigo editorial ancorado em noticia recente → `pauta-quente` ou `news-criar-post`
- Artigo para LATAM ou PT → `blog-criar-artigo-intl`
- Newsletter semanal → familia `news-*`
- Conteudo para redes sociais → familia `social-*`
