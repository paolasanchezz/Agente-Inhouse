# LP Cxpress — banimento-whatsapp-clinicas

**Gerado em:** 2026-07-22
**Copy-fonte:** `copy.txt` (output de `/lp-preparar`, réplica literal da LP `banimento-whatsapp`)

## Origem

Design idêntico à referência [`content.cxpress.io/banimento-whatsapp`](https://content.cxpress.io/banimento-whatsapp) (source local em `landing-pages/cxpress/banimento-whatsapp/`), variante para o segmento **clínicas e serviços de saúde** (já listado em `brand/cxpress/brand-manifest.json > audience.segments`).

Único texto novo pedido pelo usuário (H1 + SUB do hero) já era, coincidentemente, idêntico ao hero já publicado na referência — então a copy ficou 100% igual à original em todas as seções.

## Diferenças vs. a referência

1. **Metadados** (title, canonical, OG, Twitter Card, JSON-LD) apontam para o slug `banimento-whatsapp-clinicas` em vez de `banimento-whatsapp`, com title/description mencionando "clínicas" para evitar conteúdo duplicado indexável.
2. **Visual do hero**: imagem própria do usuário (`assets/hero-clinica.jpg`, LP-local), 2ª versão enviada em 2026-07-22 via link do Google Drive (substitui a 1ª foto, de uma médica com celular). Foto de recepcionista de clínica ao telefone usando o WhatsApp no laptop, com elementos ilustrativos de segurança (escudo, cadeado). Redimensionada para 1400×788 e recomprimida em JPEG (~87KB, de 1.6MB original). **Integração com gradiente** (pedido do usuário): a imagem sangra até a borda direita da viewport (`width: calc(100% + 110px)` dentro de `.hero__visual{overflow:visible}`, clipado pelo `.hero{overflow:hidden}`) e usa `mask-image: linear-gradient(...)` pra esmaecer a borda esquerda (que já é clara na foto original) até ficar transparente, misturando com o fundo branco da seção em vez do tratamento anterior de card retangular com drop-shadow. Breakpoint mobile (`max-width:980px`) usa um fade mais suave (`20%` em vez de `34%`) porque a imagem ocupa a largura toda da coluna, sem sangria.
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
