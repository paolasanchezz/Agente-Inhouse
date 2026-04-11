# Contexto Compartilhado — Newsletters

> Este arquivo e lido por todas as skills do grupo news-* antes de qualquer acao.

---

## Marcas Validas

| Marca | Arquivo de produto | Concorrentes |
|---|---|---|
| `buzzmonitor` | `conhecimento/produto/buzzmonitor/buzzmonitor.md` | `conhecimento/produto/buzzmonitor/concorrentes.md` |
| `buzzcreators` | `conhecimento/produto/buzzcreators/buzzcreators.md` | `conhecimento/produto/buzzcreators/concorrentes.md` |
| `cxpress` | `conhecimento/produto/cxpress/cxpress.md` | `conhecimento/produto/cxpress/concorrentes.md` |
| `elife` | `conhecimento/produto/elife/elife.md` | `conhecimento/produto/elife/concorrentes.md` |

## Regioes e Mapeamento de Idioma

| Regiao | Idioma | Nome idioma | Pasta linguistico | Pasta produto lang |
|---|---|---|---|---|
| `brasil` | PT-BR | Portugues Brasileiro | nenhuma | nenhuma |
| `latam` | ES-LATAM | Espanol Latinoamericano | `es-latam` | `es` |
| `portugal` | PT-PT | Portugues Europeu | `pt-portugal` | `pt-pt` |

Se `region` != `brasil`: carregar tambem `conhecimento/produto/{brand}/{pasta-lang}/{brand}.md` e `conhecimento/linguistico/{pasta-linguistico}/padrao-linguistico.md`.

## Caminhos

| O que | Onde |
|---|---|
| Pesquisa (material coletado) | `conhecimento/produto/{brand}/pesquisa/` |
| Arquivo de pesquisas anteriores | `conhecimento/produto/{brand}/pesquisa/arquivo/YYYY-MM/` |
| Entregas de newsletters | `newsletter/{brand}/entregas/YYYY-MM/` |
| Estilo editorial | `conhecimento/editorial/estilo-newsletter.md` |
| Regras anti-IA | `conhecimento/editorial/regras-anti-ia.md` |
| Template de newsletter | `.claude/skills/news-gerar/template-newsletter.md` |

## Notion

- Pagina raiz Newsletter: `33c3934026fd80778073f1868c5bf11c`
- Estrutura: Newsletter > {NomeDaMarca} > [Mes] de [Ano] — [IDIOMA-SIGLA]
