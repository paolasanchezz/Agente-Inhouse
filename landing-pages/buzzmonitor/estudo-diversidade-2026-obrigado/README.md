# LP Buzzmonitor — estudo-diversidade-2026-obrigado

Thanks page da LP `estudo-diversidade-2026`: entrega o PDF do estudo imediatamente após o envio do form (sem e-mail, sem etapas extras). Página de entrega pura, sem CTA de venda.

**Gerado em:** 2026-08-03
**Página mãe:** `landing-pages/buzzmonitor/estudo-diversidade-2026/` (publicar sempre em batch)

## Estrutura

- HERO (eyebrow "Estudo liberado" + H1 + card de download do PDF)
- FOOTER

## Material

- `assets/estudo-diversidade-2026.pdf` (cópia do PDF já usado na LP-mãe) — botão "Baixar o estudo" com `download`.

## Configuração pendente (fora do repo)

- **Thank You URL do Jotform:** configurar no builder do form (jotform.com, form `262024846121045`) para redirecionar para esta página após o envio: `https://material.buzzmonitor.com/estudo-diversidade-2026-obrigado`. Isso é feito na plataforma do Jotform, não no código — não dá pra automatizar por aqui.

## Estado

- [x] HTML gerado
- [ ] Revisão
- [ ] Publicado — adicionar ao manifesto `landing-pages/dominios/material-buzzmonitor-com/manifest.json` junto com a LP-mãe

## Exceções deliberadas às GUIDELINES (precedente: cxpress/video-atendimento-obrigado)

- **`noindex, follow`** (exceção ao §15): página pós-ação; validação de crawlability do lp-publicar vai apontar isso como esperado, não como erro.
- **Sem OG image, sem og/twitter completos, sem JSON-LD**: ninguém compartilha esta URL.
- **Sem estrutura mínima de LP** (§6): não há form nem captação aqui, é só entrega.

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `assets/estudo-diversidade-2026.pdf` (material entregue)

## Notas

- GTM injetado: `GTM-WFJVK858` (região brasil), mesmo container da LP-mãe.
