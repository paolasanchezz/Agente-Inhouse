# Brand — Grupo Elife

Identidade visual, tokens de design e regras de geracao por marca.
Otimizado para criacao automatizada de landing pages, criativos e newsletters.

## Ponto de Entrada

Comece por `DESIGN.md` — ele explica a hierarquia e como carregar os arquivos.

## Estrutura

```
brand/
├── DESIGN.md                        ← ponto de entrada para AI
├── TRACKING.md                      ← containers GTM por marca/regiao + divergencias
├── _shared/                         ← templates base para novas marcas
│   ├── tokens-base.json
│   └── generation-rules-base.json
├── {marca}/
│   ├── brand-manifest.json          ← identidade, voz, messaging (JSON)
│   ├── tokens.json                  ← design tokens W3C DTCG (cores, tipo, spacing)
│   ├── generation-rules.json        ← regras de composicao para AI
│   ├── BRANDBOOK.md                 ← diretrizes qualitativas, do's & don'ts
│   ├── tracking.json                ← container GTM por regiao (ver TRACKING.md)
│   └── assets/
│       ├── logos/                    ← SVG/PNG por variante
│       ├── patterns/                ← elementos visuais repetiveis
│       └── assets-manifest.json     ← metadados dos assets
```

## Arquivos por Marca

| Arquivo | Formato | Para que serve |
|---|---|---|
| `brand-manifest.json` | JSON | Identidade: nome, missao, voz (escala 0-1), audience, positioning |
| `tokens.json` | JSON (DTCG) | Valores exatos: cores, tipografia, espacamento, shadows |
| `generation-rules.json` | JSON | Regras de composicao: landing page, ad, email, newsletter |
| `tracking.json` | JSON | Container GTM por regiao (brasil/latam/portugal). Fonte de verdade do gate de deploy das LPs. Ver [TRACKING.md](TRACKING.md) |
| `BRANDBOOK.md` | Markdown | Contexto qualitativo: exemplos de voz, do's & don'ts, uso de logo |
| `assets-manifest.json` | JSON | Catalogo dos arquivos visuais com path e uso |

## Marcas

| Marca | Diretorio |
|---|---|
| Buzzmonitor | `brand/buzzmonitor/` |
| Buzzcreators | `brand/buzzcreators/` |
| Cxpress | `brand/cxpress/` |
| Elife | `brand/elife/` |

## Relacao com `conhecimento/`

`brand/` contem identidade visual e voz. `conhecimento/` contem produto, copy e linguistica.
Nao duplicar — `brand-manifest.json` tem campo `crossReferences` que aponta para `conhecimento/`.

## Adicionar Nova Marca

1. Copiar arquivos de `brand/_shared/` para `brand/nome-da-marca/`
2. Preencher `brand-manifest.json`, `tokens.json`, `generation-rules.json`
3. Criar `BRANDBOOK.md` seguindo template das marcas existentes
4. Adicionar logos em `assets/logos/`
5. Atualizar tabela em `DESIGN.md`
