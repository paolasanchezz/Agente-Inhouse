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

## Melhorias opcionais (2)

- [ ] **Hero mockup upscaled ~16%** (`mockup-plataforma-laptop.png`, nativo 465×270, exibido até 540px via CSS `.hero__mockup{max-width:540px}`) — leve perda de nitidez em telas grandes. Mesmo trade-off já aceito na LP irmã `atendimento-clinicas` (mesmo asset, mesmo uso). Não bloqueia; trocar por asset em resolução maior se disponível no futuro.
- [ ] **`brand/cxpress/brand-manifest.json` está no formato antigo** (`websites`, não `regions`) — JSON-LD `Organization` sai sem `sameAs` (LinkedIn/Instagram regional). Pré-existente (mesmo gap na referência original), não introduzido por esta LP. Migrar o manifest da marca beneficiaria todas as LPs Cxpress, não só esta.

## Nice-to-haves (1)

- [ ] Alt text do hero (`"Laptop exibindo a plataforma Cxpress com a fila de tickets e uma conversa de atendimento no WhatsApp aberta, cenário de recepção de clínica"`) está um pouco longo — poderia ser mais enxuto sem perder a informação essencial.

## Pendência crítica de publicação (não é achado de design, é bloqueio operacional)

- [x] **OG image dedicada** — gerada em `assets/og-image.png` (1200×630, confirmado via Pillow), Chrome headless + `.claude/skills/lp-gerar/og-template.html` customizado (overline "API oficial do WhatsApp · Cxpress" + H1 do próprio hero + logo Cxpress). `lp-publicar` faz o rename pra `og-{slug}.png` no deploy guarda-chuva.
- **Imagem de hero é reaproveitada, não uma foto/ilustração nova de clínica** — decisão tomada porque o Bloom (gerador de imagem) está sem créditos. Fica como decisão em aberto pro usuário revisitar se quiser um visual mais específico.

## Próximos passos

- Design aprovado. Form trocado para o Jotform próprio desta LP (`261027639617663`, via `/lp-integrar-form` em 2026-07-22).
- Gerar OG image (1200×630) antes de publicar.
- Publicar: `/lp-publicar cxpress banimento-whatsapp-clinicas [dominio]` (domínio sugerido: `content.cxpress.io`, mesmo guarda-chuva da referência).
