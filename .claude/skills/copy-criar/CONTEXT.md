# Contexto Compartilhado — Copy

> Este arquivo e lido por todas as skills do grupo copy-* antes de qualquer acao.

---

## Protocolo de Copy (os 3 pilares — OBRIGATORIO)

Toda skill copy-* carrega, antes de criar ou revisar:
1. **Linguistico** — se `regiao` != `brasil`: `conhecimento/linguistico/{pt-portugal|es-latam}/padrao-linguistico.md`. Se nao carregar, PARAR (rodar `/trad-calibrar [target]`).
2. **Boas praticas** — `conhecimento/copywriting/fundamentos-copy.md` (+ doc do tipo) + `funil-copy.md`.
3. **Anti-IA** — `conhecimento/editorial/regras-anti-ia.md` **+ o anexo do idioma** (PT-PT / ES-LATAM). Fonte unica.

Referencia global em `CLAUDE.md` (secao "Protocolo de Copy").

---

## Marcas Validas

| Marca | Arquivo de produto |
|---|---|
| `buzzmonitor` | `brand/buzzmonitor/BRANDBOOK.md` |
| `buzzcreators` | `brand/buzzcreators/BRANDBOOK.md` |
| `cxpress` | `brand/cxpress/BRANDBOOK.md` |
| `elife` | `brand/elife/BRANDBOOK.md` |

## Regioes e Mapeamento de Idioma

| Regiao | Idioma | Pasta linguistico | Pasta produto lang |
|---|---|---|---|
| `brasil` | PT-BR | nenhuma | nenhuma |
| `portugal` | PT-PT | `pt-portugal` | `pt-pt` |
| `latam` | ES-LATAM | `es-latam` | `es` |

Se `regiao` != `brasil`: carregar tambem `conhecimento/produto/{marca}/{pasta-lang}/{marca}.md` e `conhecimento/linguistico/{pasta-linguistico}/padrao-linguistico.md`.

## Identidade de Marca

| Marca | Manifest | Tokens | Regras de Geracao |
|---|---|---|---|
| `buzzmonitor` | `brand/buzzmonitor/brand-manifest.json` | `brand/buzzmonitor/tokens.json` | `brand/buzzmonitor/generation-rules.json` |
| `buzzcreators` | `brand/buzzcreators/brand-manifest.json` | `brand/buzzcreators/tokens.json` | `brand/buzzcreators/generation-rules.json` |
| `cxpress` | `brand/cxpress/brand-manifest.json` | `brand/cxpress/tokens.json` | `brand/cxpress/generation-rules.json` |
| `elife` | `brand/elife/brand-manifest.json` | `brand/elife/tokens.json` | `brand/elife/generation-rules.json` |

Ao criar copy, carregar `brand/{marca}/brand-manifest.json` para tom de voz e mensagens-chave. Usar `voice.toneAttributes` para calibrar formalidade e entusiasmo. Para copy visual (estatico, video), consultar tambem `tokens.json` e `generation-rules.json`.

## Base de Conhecimento de Copy

| Arquivo | Quando carregar |
|---|---|
| `conhecimento/copywriting/fundamentos-copy.md` | SEMPRE |
| `conhecimento/copywriting/funil-copy.md` | SEMPRE |
| `conhecimento/copywriting/video-curto-ads.md` + `video-curto-organico.md` + `video-curto-talking-head.md` | tipo = video-curto |
| `conhecimento/copywriting/estatico-ads.md` + `estatico-organico.md` | tipo = estatico |
| `conhecimento/copywriting/email-copy.md` | tipo = email |
| `conhecimento/editorial/regras-anti-ia.md` | **SEMPRE** (criacao e revisao) — fonte unica anti-IA. Se `regiao` != `brasil`, ler tambem o anexo do idioma. |
| `conhecimento/editorial/estilo-newsletter.md` | Apenas newsletters (estrutura/anatomia). NAO e a lista anti-IA: ele delega pra `regras-anti-ia.md`. |

## Convencoes de Output

- Copys criadas: `conhecimento/copywriting/criacao/{marca}/YYYY-MM-DD/`
- Copys revisadas: `conhecimento/copywriting/revisoes/`
- Swipe file: `conhecimento/copywriting/swipe-file/`

## Notion

IDs sao lidos de `conhecimento/config/notion-ids.md` (fonte unica). Para publicacao, use a chave `entregas`.
