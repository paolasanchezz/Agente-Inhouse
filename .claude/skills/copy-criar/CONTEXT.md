# Contexto Compartilhado — Copy

> Este arquivo e lido por todas as skills do grupo copy-* antes de qualquer acao.

---

## Marcas Validas

| Marca | Arquivo de produto |
|---|---|
| `buzzmonitor` | `conhecimento/produto/buzzmonitor/buzzmonitor.md` |
| `buzzcreators` | `conhecimento/produto/buzzcreators/buzzcreators.md` |
| `cxpress` | `conhecimento/produto/cxpress/cxpress.md` |
| `elife` | `conhecimento/produto/elife/elife.md` |

## Regioes e Mapeamento de Idioma

| Regiao | Idioma | Pasta linguistico | Pasta produto lang |
|---|---|---|---|
| `brasil` | PT-BR | nenhuma | nenhuma |
| `portugal` | PT-PT | `pt-portugal` | `pt-pt` |
| `latam` | ES-LATAM | `es-latam` | `es` |

Se `regiao` != `brasil`: carregar tambem `conhecimento/produto/{marca}/{pasta-lang}/{marca}.md` e `conhecimento/linguistico/{pasta-linguistico}/padrao-linguistico.md`.

## Base de Conhecimento de Copy

| Arquivo | Quando carregar |
|---|---|
| `conhecimento/copywriting/fundamentos-copy.md` | SEMPRE |
| `conhecimento/copywriting/funil-copy.md` | SEMPRE |
| `conhecimento/copywriting/video-curto-ads.md` + `video-curto-organico.md` | tipo = video-curto |
| `conhecimento/copywriting/estatico-ads.md` + `estatico-organico.md` | tipo = estatico |
| `conhecimento/copywriting/email-copy.md` | tipo = email |
| `conhecimento/editorial/regras-anti-ia.md` | Em revisoes |
| `conhecimento/editorial/estilo-newsletter.md` | Em revisoes |

## Convencoes de Output

- Copys criadas: `conhecimento/copywriting/criacao/{marca}/YYYY-MM-DD/`
- Copys revisadas: `conhecimento/copywriting/revisoes/`
- Swipe file: `conhecimento/copywriting/swipe-file/`

## Notion

- Pasta Entregas (publicacao): `33b3934026fd80ceb414dd22cb7dbe1f`
