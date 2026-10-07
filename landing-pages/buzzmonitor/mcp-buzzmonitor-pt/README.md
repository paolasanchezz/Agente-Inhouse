# LP Buzzmonitor · mcp-buzzmonitor-pt

**Gerado em:** 2026-10-07
**Região:** portugal (`pt-PT`) · **GTM:** GTM-NCFT22CW
**Copy-fonte:** `copy.txt` (tradução PT-PT da LP irmã `mcp-buzzmonitor` via `/trad-pipeline`, status APROVADO; Notion: Entregas > "mcp-buzzmonitor — PT-PT — 2026-10-07")

## O que é

Versão PT-PT da LP `content.buzzmonitor.com/mcp-buzzmonitor` (MCP da Buzzmonitor + Skills prontas). Mesmo HTML, mesma direção visual e mesmas animações da versão BR; só mudam texto, idioma e tracking. Distinta da `mcp-pt` antiga (`material.buzzmonitor.com/mcp-pt`, foco em "4 módulos"), que continua no ar.

## Diferenças em relação à LP BR

- `lang="pt-PT"`, `og:locale=pt_PT`, JSON-LD `inLanguage: pt-PT`
- GTM Portugal `GTM-NCFT22CW` (gate `check_gtm_region.py` OK, selo em `.tracking.lock`)
- Jotform PT `261405305585859` (o mesmo das LPs PT `mcp-pt` e `monitoramento-manual-pt`)
- hreflang `pt-PT` (esta) + `pt-BR` / `x-default` (`mcp-buzzmonitor`)
- OG image própria: `assets/og-mcp-buzzmonitor-pt.png` (fonte em `assets/og-source.html`)
- `assets/demo-analise.gif` copiado da LP BR (sem texto PT-BR relevante)

## Estado

- [x] Copy traduzida e revista (PT-PT, tratamento "você")
- [x] HTML gerado
- [x] OG image 1200×630
- [x] Formulário integrado (Jotform PT)
- [ ] Publicado em `content.buzzmonitor.com/mcp-buzzmonitor-pt` (manifesto + PR, fluxo CI via `/lp-publicar`)

## Pendências que precisam de decisão humana

1. **Vídeo:** reaproveita o mesmo YouTube da LP BR (`XVQ1Aloba2A`), com áudio PT-BR. Trocar se houver versão PT-PT.
2. **"turno inteiro"**: a fonte BR diz "toma um fuso inteiro do analista" (typo). Tratado como "turno".
3. A LP BR não aponta de volta para esta (hreflang só nesta página). Opcional: acrescentar `hreflang="pt-PT"` na `mcp-buzzmonitor`.
