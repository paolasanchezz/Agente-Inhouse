# LP Ebook — O novo marketing e conversacao (PT-PT)

- **Marca:** Cxpress
- **Regiao/idioma:** Portugal (PT-PT)
- **Dominio:** content.cxpress.io (guarda-chuva migrado pro CI)
- **Slug:** `ebook-marketing-conversacao-pt`
- **Versao LATAM irma:** `landing-pages/cxpress/ebook-marketing-conversacion-latam`

## Estado

- [x] Formulario integrado

**Form provider:** Jotform — `jsform/261826255094865` (integrado em 2026-08-28)

O embed vive em `<div class="jotform-embed reveal" id="formulario">`. O `id="formulario"`
esta no wrapper porque os 3 CTAs da pagina apontam pra `#formulario` — nao remover.

## Deploy

Guarda-chuva migrado: editar o source + PR. O CI (`lp-deploy.yml`) publica com smoke
test e rollback automaticos. Nunca deployar a mao.
