# LP Cxpress — webinar-clinicas-latam

**Gerado em:** 2026-08-11
**Copy-fonte:** `copy.txt` (duplicada, com aprovação do usuário, a partir do texto literal visível em https://www.cxpress.ai/webinar-clinicas — mesmo copy, mesmo idioma ES-LATAM, mesma marca Cxpress)
**Design-fonte:** visual/estrutural espelhado em `landing-pages/cxpress/latam-webinar-atencionalcliente/index.html` (mesma família visual Cxpress LATAM — tokens, hero-grid, speaker-card — que também compartilha os mesmos 2 speakers)

## Estrutura

- HERO (overline + h1 + sub + CTA)
- PROBLEMA-Y-FORM (h2 + form mock + 3 paragrafos de contexto) — form na 2ª seção (padrão ToFu/webinar, GUIDELINES §10)
- APRENDIZAJES (lista de 6 itens)
- PARA-QUIEN (lista de 4 itens, fundo escuro primary-dark) + CTA
- PROVA-ESPECIALISTAS (2 speaker cards: Milagro Pantoja, Laura Rodríguez — fotos reaproveitadas de `latam-webinar-atencionalcliente`) + CTA
- PROVA-SOCIAL (+800 clientes)
- FOOTER

## Estado

- [x] HTML gerado
- [x] OG image 1200×630 → `assets/og-webinar-clinicas-latam.png` (gerada via Chrome headless + template do brandbook)
- [x] Revisão (`/lp-revisar cxpress/webinar-clinicas-latam`) — 4 críticos de contraste corrigidos, ver `REVISAO.md`
- [x] Formulário integrado — mock substituído por embed real (ver Form provider abaixo)
- [ ] Publicado — `/lp-publicar cxpress webinar-clinicas-latam content.cxpress.io`

**Form provider:** Jotform (2026-08-13)

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `./assets/doctora-equipo-clinica.jpg` (foto de fundo do hero, enviada pelo usuario via Downloads — `landing clinicas.png`, convertida pra JPEG. Padrao foto-de-fundo + scrim, igual `banimento-whatsapp-clinicas`)
- `./assets/speakers/milagros-pantoja.jpg`
- `./assets/speakers/laura-rodriguez.jpg`
- `../../brand/cxpress/assets/plataforma/clientes-cxpress.png` (banner de logos de clientes, reusado — mesmo asset usado em ~15 outras LPs Cxpress)

## Notas

- Página original (`cxpress.ai/webinar-clinicas`, construída em GreatPages) tinha resíduos ocultos em PT-BR no DOM (heading duplicado, CTA "QUERO ASSISTIR", link de demo) que não aparecem ao visitante ES — excluídos por não serem copy visível real.
- Nomes/cargos dos 2 speakers não estavam em texto/DOM na página original (seção renderizada como imagem composta) — confirmados pelo usuário via screenshot e cruzados com a LP irmã `latam-webinar-atencionalcliente`, que já usa as mesmas 2 pessoas.
- GTM: `GTM-WRQ47B9R` (região LATAM, `brand/cxpress/tracking.json`).
- `brand/cxpress/brand-manifest.json` ainda está no formato antigo (`websites`, sem bloco `regions`) — JSON-LD `Organization` ficou sem `sameAs` (Instagram/LinkedIn) por causa disso. Considerar migrar o manifest.
