# Revisao LP — cxpress/banimento-whatsapp-clinicas

**Data:** 2026-07-22
**Auditores:** frontend-design (review mode) + web-design-guidelines + checks deterministicos (GTM, SEO, copy fidelity, logo regional, hreflang)

## Contexto da revisão

Esta LP é um clone quase literal de `landing-pages/cxpress/banimento-whatsapp/index.html` (mesmo CSS, mesma copy), já publicado e já revisado anteriormente. O delta desta LP é: (1) metadados de SEO apontando pro novo slug, (2) troca do asset visual do hero (GIF genérico → PNG estático de mockup, tema clínica). A revisão focou nesse delta + nos checks determinísticos completos.

## Aplicado automaticamente (0 críticos)

Nenhum crítico encontrado. Checks determinísticos, todos OK:

- [x] GTM — `GTM-T4XDWHL3` bate com a região (`brasil`), stamp gravado (`stamp_match: true`)
- [x] SEO — 1 description, 1 robots, 10 tags `og:`, 4 `twitter:`, 1 JSON-LD (parseia corretamente), 1 canonical
- [x] Em-dash — 0 ocorrências
- [x] Logo header/footer — `href="https://home.cxpress.io"` (bate com `brand-manifest.json > websites.brasil`), `target="_blank" rel="noopener"`, `aria-label` localizado
- [x] Logo SVG web-safe — Cxpress já documentado como OK (paths/outline, sem `<text>` vivo)
- [x] Fidelidade de copy — H1, frase de fechamento (FECHO) e todos os headings (h1-h3) idênticos byte-a-byte à referência (diff = vazio)
- [x] Hreflang — corretamente omitido. `banimento-whatsapp-clinicas` não é uma variante de idioma (é variante de segmento/público, PT-BR o tempo todo) — não entra na família hreflang de `banimento-whatsapp` / `banimento-whatsapp-pt`

## Melhorias opcionais (1)

- [ ] **`brand/cxpress/brand-manifest.json` está no formato antigo** (`websites`, não `regions`) — JSON-LD `Organization` sai sem `sameAs` (LinkedIn/Instagram regional). Pré-existente (mesmo gap na referência original), não introduzido por esta LP. Migrar o manifest da marca beneficiaria todas as LPs Cxpress, não só esta.

## Nice-to-haves (0)

Nenhum.

## Atualização 2026-07-22 (pós-publicação inicial) — hero substituído

- [x] **Imagem de hero definitiva**: o usuário enviou uma foto própria (via link do Google Drive) de uma médica de jaleco usando o WhatsApp no celular, com elementos ilustrativos de segurança (escudo, cadeado). Baixada, redimensionada pra 1080×810 e recomprimida em JPEG (~80KB, de 1.6MB original). Substitui o `mockup-plataforma-laptop.png` que era placeholder temporário. Arquivo: `assets/hero-clinica.jpg` (LP-local). Isso fecha as duas pendências anteriores (mockup reaproveitado + upscaling de 16%) — não se aplicam mais.
- [x] OG image dedicada — `assets/og-image.png` (1200×630), gerada via Chrome headless + `.claude/skills/lp-gerar/og-template.html`.

## Próximos passos

- Design aprovado, form Jotform próprio (`261027639617663`) e hero definitivo integrados.
- Publicar atualização: `/lp-publicar cxpress banimento-whatsapp-clinicas content.cxpress.io`.
