# Contexto Compartilhado — Pauta Quente

> Este arquivo e lido pela skill pauta-quente antes de qualquer acao. Mesma estrutura do CONTEXT de copy-criar e news-pesquisar.

---

## Marcas Validas

| Marca | Arquivo de produto |
|---|---|
| `buzzmonitor` | `brand/buzzmonitor/BRANDBOOK.md` |
| `buzzcreators` | `brand/buzzcreators/BRANDBOOK.md` |
| `cxpress` | `brand/cxpress/BRANDBOOK.md` |
| `elife` | `brand/elife/BRANDBOOK.md` |

## Idiomas e Mapeamento de Regiao

| Idioma (CLI) | Regiao | Idioma canonico | Pasta linguistico | Pasta produto lang |
|---|---|---|---|---|
| `br` | `brasil` | PT-BR | nenhuma | nenhuma |
| `pt` | `portugal` | PT-PT | `pt-portugal` | `pt-pt` |
| `es` | `latam` | ES-LATAM | `es-latam` | `es` |

Se idioma != `br`: carregar tambem `conhecimento/produto/{marca}/{pasta-produto-lang}/{marca}.md` e `conhecimento/linguistico/{pasta-linguistico}/padrao-linguistico.md`.

## Tipos de Conteudo

| Tipo | Formato base | Doc de copy |
|---|---|---|
| `carrossel` | 5 cards (cover -> contexto -> insight -> conector -> CTA) | `estatico-ads.md` + `estatico-organico.md` |
| `video-curto` | Audio + overlay + caption (15-45s) | `video-curto-ads.md` + `video-curto-organico.md` + `video-curto-talking-head.md` |
| `blog` | H1 + lead + 4 H2s (600-1000 palavras) | `blog-copy.md` |
| `linkedin` | Post longo (1300-1800 chars) com hook 3 linhas | `linkedin-copy.md` |
| `email` | Subject + preview + corpo (hook -> problema -> valor -> CTA) | `email-copy.md` |

## Identidade de Marca

| Marca | Manifest | Tokens | Regras de Geracao |
|---|---|---|---|
| `buzzmonitor` | `brand/buzzmonitor/brand-manifest.json` | `brand/buzzmonitor/tokens.json` | `brand/buzzmonitor/generation-rules.json` |
| `buzzcreators` | `brand/buzzcreators/brand-manifest.json` | `brand/buzzcreators/tokens.json` | `brand/buzzcreators/generation-rules.json` |
| `cxpress` | `brand/cxpress/brand-manifest.json` | `brand/cxpress/tokens.json` | `brand/cxpress/generation-rules.json` |
| `elife` | `brand/elife/brand-manifest.json` | `brand/elife/tokens.json` | `brand/elife/generation-rules.json` |

Ao gerar peca, carregar `brand/{marca}/brand-manifest.json` para tom de voz (`voice.toneAttributes`, `voice.samplePhrases`) e BRANDBOOK.md para features, cases e grafias exatas.

## Base de Conhecimento

| Arquivo | Quando carregar |
|---|---|
| `conhecimento/copywriting/fundamentos-copy.md` | SEMPRE |
| `conhecimento/copywriting/funil-copy.md` | SEMPRE |
| `conhecimento/editorial/regras-anti-ia.md` | SEMPRE (carregada no Passo 3 e recarregada no Passo 6) |
| `conhecimento/copywriting/estatico-ads.md` + `estatico-organico.md` | tipo = carrossel |
| `conhecimento/copywriting/video-curto-ads.md` + `video-curto-organico.md` + `video-curto-talking-head.md` | tipo = video-curto |
| `conhecimento/copywriting/blog-copy.md` | tipo = blog |
| `conhecimento/copywriting/linkedin-copy.md` | tipo = linkedin |
| `conhecimento/copywriting/email-copy.md` | tipo = email |
| `conhecimento/produto/{marca}/concorrentes.md` | SEMPRE |
| `conhecimento/produto/{marca}/{pasta-lang}/{marca}.md` | idioma != br |
| `conhecimento/linguistico/{pasta-lang}/padrao-linguistico.md` | idioma != br |

## Convencoes de Output

### Local
```
pauta-quente/{marca}/YYYY-MM-DD-{slug-noticia}/
├── INDICE.md              (grade tipo x idioma x arquivo + metadados)
├── FONTES.md              (primaria + secundarias + queries usadas)
├── REVISAO-LOG.md         (log do Passo 6 de revisao anti-IA por peca)
├── carrossel-br.md
├── carrossel-pt.md
├── blog-br.md
└── ...
```

- `slug-noticia`: kebab-case, sem acentos, max 60 chars. Derivado do tema principal.
- Cada peca: 1 arquivo por combinacao tipo x idioma. Sufixo de idioma = sigla CLI (`br`, `pt`, `es`).

### Notion
IDs sao lidos de `conhecimento/config/notion-ids.md` (fonte unica). Para publicacao, use a chave `entregas`.

Estrutura alvo (3 niveis):
```
Entregas ({ENTREGAS_ROOT})
└── Pauta Quente — {NomeDaMarca}                       (subpasta por marca, icon: 🔥)
    └── YYYY-MM-DD — {Tema curto max 40 chars}          (pagina do evento, icon: 🔥)
        ├── Callout topo (Tema + Fonte primaria + Insight + Conector)
        ├── ▶ Blog
        │     ├── ▶ PT-BR
        │     ├── ▶ PT-PT
        │     └── ▶ ES-LATAM
        ├── ▶ LinkedIn
        ├── ▶ Email
        ├── ▶ Carrossel
        ├── ▶ Video-Curto
        ├── ## Fontes
        └── ## Queries de pesquisa
```

Subpasta por marca segue o padrao de `news-gerar`. Toggles organizados por tipo primeiro, idioma dentro: distribuidor pega "o blog" e publica em 3 idiomas — corte natural de trabalho.
