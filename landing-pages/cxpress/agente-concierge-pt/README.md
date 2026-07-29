# LP Cxpress — agente-concierge-pt

**Gerado em:** 2026-07-29
**Copy-fonte:** `copy.txt` (escrita a partir de um briefing estratégico, ver nota no próprio arquivo)
**Idioma/região:** PT-PT (Portugal) — GTM `GTM-NW6V5KBM`
**Domínio:** `content.cxpress.io` (guarda-chuva migrado pro CI, `landing-pages/dominios/content-cxpress-io/manifest.json`)

## Estrutura

- HERO — eyebrow "Novo: Agente para Engagement" + H1 (dor) + sub (Agente Concierge/IA) + CTA
- PROBLEMA — 5 dores em lista vertical, ícone X vermelho
- CONCEITO — seção de pausa (sem CTA/card), 3 parágrafos sobre o Agente para Engagement
- BENEFICIOS — grid 3x2 (6 itens), ícone check verde
- PARA-QUEM — grid 2 colunas (6 segmentos de público), sem X/check (bullet neutro)
- CTA-FINAL — fundo primaryDark, 2 CTAs ("Pedir Demonstração", "Saber Mais")
- FOOTER — copyright + logo linkando para home PT

Sem seção de Prova/Depoimentos nem Urgência — o briefing original não trouxe social proof nem prazo real (GUIDELINES §9: vazio é válido).

## Nota sobre manifest da marca

`brand/cxpress/brand-manifest.json` ainda está no formato antigo (`websites` em vez de `regions.{regiao}.{htmlLang,hreflang,ogLocale,home,instagram}`). JSON-LD `Organization` foi gerado **sem** `sameAs` (Instagram/LinkedIn) por degradação documentada em `lp-gerar` — migrar o manifest pro formato `regions` quando possível.

## Estado

- [x] HTML gerado
- [ ] Revisão (frontend-design review + web-design-guidelines) — rodar `/lp-revisar cxpress/agente-concierge-pt`
- [ ] Formulário integrado — não aplicável (esta LP usa CTAs de botão, sem formulário na copy)
- [x] OG image (1200x630) — gerada via `.claude/skills/lp-gerar/og-template.html` + Chrome headless, salva em `assets/og-agente-concierge-pt.png` (nome já no formato `og-{slug}.png` esperado por `landing-pages/build/build_umbrella.py`)
- [x] Publicado — via fluxo CI (`content.cxpress.io`), entrada adicionada em `landing-pages/dominios/content-cxpress-io/manifest.json`

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-primary.svg` (header + footer)
- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `../../brand/cxpress/assets/mascot/samir-laptop.png` (hero visual)
- `./assets/og-agente-concierge-pt.png` (OG image, LP-local)
