# LP Cxpress — agente-concierge-pt

**Gerado em:** 2026-07-29
**Copy-fonte:** `copy.txt` (escrita a partir de um briefing estratégico, ver nota no próprio arquivo)
**Idioma/região:** PT-PT (Portugal) — GTM `GTM-NW6V5KBM`
**Domínio:** `content.cxpress.io` (guarda-chuva migrado pro CI, `landing-pages/dominios/content-cxpress-io/manifest.json`)

## Estrutura

- HERO — eyebrow "Agente para Engagement" + H1 (dor) + sub (Agente Concierge/IA) + CTA, com a foto (equipa de marketing, fornecida pelo usuário) como background full-bleed da seção + scrim gradiente (mesmo padrão da LP `banimento-whatsapp-clinicas`)
- PROBLEMA — 5 dores em lista vertical, ícone X vermelho
- CONCEITO — seção de pausa (sem CTA/card), 3 parágrafos sobre o Agente para Engagement
- BENEFICIOS — grid 3x2 (6 itens), ícone check verde
- PARA-QUEM — grid 2 colunas (6 segmentos de público), sem X/check (bullet neutro)
- CTA-FINAL — fundo primaryDark, form real embutido (Jotform) num card branco
- FOOTER — copyright + logo linkando para home PT

Sem seção de Prova/Depoimentos nem Urgência — o briefing original não trouxe social proof nem prazo real (GUIDELINES §9: vazio é válido).

## Nota sobre manifest da marca

`brand/cxpress/brand-manifest.json` ainda está no formato antigo (`websites` em vez de `regions.{regiao}.{htmlLang,hreflang,ogLocale,home,instagram}`). JSON-LD `Organization` foi gerado **sem** `sameAs` (Instagram/LinkedIn) por degradação documentada em `lp-gerar` — migrar o manifest pro formato `regions` quando possível.

## Estado

- [x] HTML gerado
- [ ] Revisão (frontend-design review + web-design-guidelines) — rodar `/lp-revisar cxpress/agente-concierge-pt`
- [x] Formulário integrado — Jotform `261904529617867` (mesmo form usado em `banimento-whatsapp-pt`/`whatsapp-business-smb-pt`), embutido no CTA-FINAL num card branco (fundo da seção é escuro; texto padrão do Jotform, ex. checkbox de consentimento, não teria contraste direto sobre navy)
- [x] OG image (1200x630) — gerada via `.claude/skills/lp-gerar/og-template.html` + Chrome headless, salva em `assets/og-agente-concierge-pt.png` (nome já no formato `og-{slug}.png` esperado por `landing-pages/build/build_umbrella.py`)
- [x] Publicado — via fluxo CI (`content.cxpress.io`), entrada adicionada em `landing-pages/dominios/content-cxpress-io/manifest.json`

**Ajustes a pedido do usuário (2026-07-29):** eyebrow sem o prefixo "Novo:"; foto do hero virou background full-bleed (`.hero__bg` + `.hero__scrim`, mesma receita de `banimento-whatsapp-clinicas`) em vez de card à parte; CTAs (nav + hero) recoloridos para o verde institucional do WhatsApp `#21CC78` (mesmo tom já usado em `banimento-whatsapp-clinicas`), hover `#1AAE63`.

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-primary.svg` (header + footer)
- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `./assets/hero-bg.png` (foto do hero, fornecida pelo usuário via Google Drive)
- `./assets/og-agente-concierge-pt.png` (OG image, LP-local)
