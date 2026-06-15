# Contexto Compartilhado — Traducao

> Este arquivo e lido por todas as skills do grupo trad-* antes de qualquer acao.

---

## Protocolo (os 3 pilares)

Toda skill trad-* carrega antes de traduzir/revisar:
1. **Linguistico** — o `padrao-linguistico.md` do target (tabela abaixo). Se nao carregar, PARAR e rodar `/trad-calibrar [target]`.
2. **Anti-IA** — `conhecimento/editorial/regras-anti-ia.md` **+ o anexo do idioma** (PT-PT / ES-LATAM). Aplicar inclusive DEPOIS de corrigir (re-contagem pos-correcao).
3. **Boas praticas** — `conhecimento/copywriting/fundamentos-copy.md` quando a peca for criada/reescrita, nao so transposta.

Referencia global: `CLAUDE.md` (secao "Protocolo de Copy").

---

## Targets Validos

| Target | Idioma alvo | Padrao linguistico |
|---|---|---|
| `pt-pt` | Portugues Europeu | `conhecimento/linguistico/pt-portugal/padrao-linguistico.md` |
| `es-latam` | Espanol Latinoamericano | `conhecimento/linguistico/es-latam/padrao-linguistico.md` |

## Identidade de Marca

Ao traduzir, consultar `brand/{marca}/brand-manifest.json` secao `voice.samplePhrases` para manter consistencia de marca no idioma-alvo. Consultar tambem `brand/{marca}/BRANDBOOK.md` secao "Adaptacao por Regiao".

| Marca | Manifest | Brandbook |
|---|---|---|
| `buzzmonitor` | `brand/buzzmonitor/brand-manifest.json` | `brand/buzzmonitor/BRANDBOOK.md` |
| `buzzcreators` | `brand/buzzcreators/brand-manifest.json` | `brand/buzzcreators/BRANDBOOK.md` |
| `cxpress` | `brand/cxpress/brand-manifest.json` | `brand/cxpress/BRANDBOOK.md` |
| `elife` | `brand/elife/brand-manifest.json` | `brand/elife/BRANDBOOK.md` |

## Caminhos

| O que | Onde |
|---|---|
| Entregas de traducao | `traducao/entregas/YYYY-MM/` |
| Regras anti-IA | `conhecimento/editorial/regras-anti-ia.md` |
| Padrao linguistico (nucleo) | `conhecimento/linguistico/{target}/padrao-linguistico.md` — lido por todas as skills; so regra acionavel |
| Pesquisa do padrao (proveniencia) | `conhecimento/linguistico/{target}/padrao-pesquisa.md` — log escrito SO pelo `/trad-calibrar`; consumidoras nao leem |

## Convencoes de Nomes

- Original: `[nome]-original.md`
- Traducao: `[nome]-[target].md`
- Log de revisao: `[nome]-revisao-log.md`

## Notion

IDs sao lidos de `conhecimento/config/notion-ids.md` (fonte unica). Para publicacao, use a chave `entregas`.
