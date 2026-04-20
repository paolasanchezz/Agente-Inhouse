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

## Identidade de Marca

| Marca | Manifest | Tokens | Regras de Geracao |
|---|---|---|---|
| `buzzmonitor` | `brand/buzzmonitor/brand-manifest.json` | `brand/buzzmonitor/tokens.json` | `brand/buzzmonitor/generation-rules.json` |
| `buzzcreators` | `brand/buzzcreators/brand-manifest.json` | `brand/buzzcreators/tokens.json` | `brand/buzzcreators/generation-rules.json` |
| `cxpress` | `brand/cxpress/brand-manifest.json` | `brand/cxpress/tokens.json` | `brand/cxpress/generation-rules.json` |
| `elife` | `brand/elife/brand-manifest.json` | `brand/elife/tokens.json` | `brand/elife/generation-rules.json` |

Ao gerar newsletters, carregar `brand/{marca}/brand-manifest.json` para personalidade e voz. Para newsletters em HTML, carregar tambem `brand/{marca}/tokens.json` para cores e tipografia.

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
