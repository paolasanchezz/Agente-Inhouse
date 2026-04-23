# LP Cxpress — Playbook WhatsApp 2026

**Gerado em:** 2026-04-21
**Copy-fonte:** `copy.txt` (output de /lp-preparar)

## Estrutura

- HERO (H1 + SUB + BODY + LABEL + CTA + visual playbook mockup)
- O QUE MUDA (lista vertical 3 itens com X vermelhos + bloco de fechamento destaque + CTA)
- O QUE O PLAYBOOK COBRE (grid 3x2 com numeros decorativos 01-06)
- PARA QUEM E (lista 3 itens com checks em primary)
- QUEM PREPAROU (mascote Samir + texto)
- CTA FINAL (fundo primaryDark + form mock 3 campos + CTA)
- FOOTER (logo reversed + copyright + link home.cxpress.io)

## Estado

- [x] HTML gerado
- [ ] Revisao (frontend-design review + web-design-guidelines) — rodar `/lp-revisar cxpress/playbook-whatsapp2026`
- [ ] Formulario integrado — rodar `/lp-integrar-form cxpress/playbook-whatsapp2026 [snippet]`
- [ ] Publicado — rodar `/lp-publicar cxpress playbook-whatsapp2026 [dominio]`

## Paleta aplicada

- `primaryDark` #232960 — titulos, texto, CTA principal, secao destaque
- `primary` #4A69BD — acentos, links, hover
- `accent` #EF863C — highlight decorativo (numeros 01-06, underline mark, CTA secundario, details)
- Backgrounds alternados: branco <-> primaryLighter #D7E2FF <-> neutral.100 #f5f5f5

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon + secao Quem Preparou)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
- Google Fonts: Open Sans 400/600/700/800, Source Sans 3 400/500/600, Bitter 400/600

## GTM

Nao injetado (brand/cxpress/tracking.json retorna null). Quando disponivel, atualizar tracking.json e re-gerar.
