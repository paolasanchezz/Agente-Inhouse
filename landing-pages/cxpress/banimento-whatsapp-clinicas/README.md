# LP Cxpress — banimento-whatsapp-clinicas

**Gerado em:** 2026-07-22
**Copy-fonte:** `copy.txt` (output de `/lp-preparar`, réplica literal da LP `banimento-whatsapp`)

## Origem

Design idêntico à referência [`content.cxpress.io/banimento-whatsapp`](https://content.cxpress.io/banimento-whatsapp) (source local em `landing-pages/cxpress/banimento-whatsapp/`), variante para o segmento **clínicas e serviços de saúde** (já listado em `brand/cxpress/brand-manifest.json > audience.segments`).

Único texto novo pedido pelo usuário (H1 + SUB do hero) já era, coincidentemente, idêntico ao hero já publicado na referência — então a copy ficou 100% igual à original em todas as seções.

## Diferenças vs. a referência

1. **Metadados** (title, canonical, OG, Twitter Card, JSON-LD) apontam para o slug `banimento-whatsapp-clinicas` em vez de `banimento-whatsapp`, com title/description mencionando "clínicas" para evitar conteúdo duplicado indexável.
2. **Visual do hero**: imagem própria do usuário (`assets/hero-clinica.jpg`, LP-local), enviada em 2026-07-22 via link do Google Drive. Substitui o mockup estático `mockup-plataforma-laptop.png` usado provisoriamente (decisão anterior, tomada enquanto o Bloom estava sem créditos e sem imagem de clínica disponível). Foto de médica de jaleco usando o WhatsApp no celular, com elementos ilustrativos de segurança (escudo, cadeado) sobre fundo de clínica. Redimensionada para 1080×810 e recomprimida em JPEG (~80KB, de 1.6MB original) antes de entrar no repo.
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
- `./assets/hero-clinica.jpg` (hero — foto enviada pelo usuário, LP-local)
- `../../brand/cxpress/assets/plataforma/clientes-cxpress.png` (prova social)
- `../../brand/cxpress/assets/plataforma/plataforma-canais.gif`, `plataforma-chatbot-ia.gif`, `plataforma-dashboard.gif` (seção Plataforma)
- `../../brand/cxpress/assets/plataforma/quem-somos-foto.jpg`
- `../../brand/cxpress/assets/plataforma/elife-logo.png`
