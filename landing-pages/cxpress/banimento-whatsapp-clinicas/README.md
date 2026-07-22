# LP Cxpress — banimento-whatsapp-clinicas

**Gerado em:** 2026-07-22
**Copy-fonte:** `copy.txt` (output de `/lp-preparar`, réplica literal da LP `banimento-whatsapp`)

## Origem

Design idêntico à referência [`content.cxpress.io/banimento-whatsapp`](https://content.cxpress.io/banimento-whatsapp) (source local em `landing-pages/cxpress/banimento-whatsapp/`), variante para o segmento **clínicas e serviços de saúde** (já listado em `brand/cxpress/brand-manifest.json > audience.segments`).

Único texto novo pedido pelo usuário (H1 + SUB do hero) já era, coincidentemente, idêntico ao hero já publicado na referência — então a copy ficou 100% igual à original em todas as seções.

## Diferenças vs. a referência

1. **Metadados** (title, canonical, OG, Twitter Card, JSON-LD) apontam para o slug `banimento-whatsapp-clinicas` em vez de `banimento-whatsapp`, com title/description mencionando "clínicas" para evitar conteúdo duplicado indexável.
2. **Visual do hero**: troca do GIF genérico `plataforma-canais.gif` pelo mockup estático `mockup-plataforma-laptop.png` — mesmo asset já usado na LP `atendimento-clinicas` (outra LP Cxpress para o mesmo segmento). **Decisão tomada sem imagem gerada por IA**: o Bloom (gerador de imagem da sessão) está sem créditos (`INSUFFICIENT_CREDITS`), então não foi possível gerar uma ilustração/foto nova remetendo a ambiente de clínica. Perguntei ao usuário como prosseguir e segui com a opção mais conservadora (reaproveitar asset existente do brand) na ausência de resposta. **Ponto de revisão em aberto** — se o time preferir uma imagem de clínica de verdade (foto ou ilustração gerada), trocar depois: `bloom_generate_image` (quando houver créditos) ou upload manual de uma foto via `/lp-integrar-form`-like fluxo de asset.
3. **Formulário**: trocado do Jotform herdado da referência (`261045149477663`) para o Jotform próprio desta LP, `261027639617663`, informado pelo usuário em 2026-07-22.
4. Todo o restante (copy, CSS, estrutura de seções, ordem, cores, animações) é idêntico à referência.

## Estrutura

- HERO (com CTA)
- CLIENTES (prova social)
- FORM / agendar (Jotform embutido — já é integração real, herdada da referência)
- BENEFICIOS
- PROVA (stats)
- PLATAFORMA (features)
- FAQ
- QUEM SOMOS
- FECHO
- FOOTER

## Estado

- [x] HTML gerado (clonado da referência + metadados/hero ajustados)
- [x] Revisão (frontend-design review + web-design-guidelines + checks determinísticos) — 0 críticos, ver `REVISAO.md`
- [x] Formulário integrado — Jotform `261027639617663` (2026-07-22, fornecido pelo usuário, substituiu o `261045149477663` herdado da referência)
- [x] OG image dedicada — `assets/og-image.png` (1200×630) gerada via Chrome headless a partir de `.claude/skills/lp-gerar/og-template.html` (overline + H1 do próprio hero, logo Cxpress). `lp-publicar` renomeia para `og-{slug}.png` no deploy (guarda-chuva).
- [ ] Publicado — rodar `/lp-publicar cxpress banimento-whatsapp-clinicas [dominio]`

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `../../brand/cxpress/assets/plataforma/mockup-plataforma-laptop.png` (hero — **novo nesta LP**, trocado do GIF genérico)
- `../../brand/cxpress/assets/plataforma/clientes-cxpress.png` (prova social)
- `../../brand/cxpress/assets/plataforma/plataforma-canais.gif`, `plataforma-chatbot-ia.gif`, `plataforma-dashboard.gif` (seção Plataforma)
- `../../brand/cxpress/assets/plataforma/quem-somos-foto.jpg`
- `../../brand/cxpress/assets/plataforma/elife-logo.png`
