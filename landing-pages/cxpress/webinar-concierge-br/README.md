# LP Cxpress — webinar-concierge-br

**Gerado em:** 2026-10-07
**Copy-fonte:** `copy.txt` (output de /lp-preparar, a partir do deck "Webinar perpétuo · Como reduzimos o SLA de 8 horas para 26 minutos")
**Base de design:** clone visual de `landing-pages/cxpress/webinar-whatsapp-ia-pt` (VSL centrado), adaptado para PT-BR + secao Resultado nova.
**Apresentador:** Luiz Fantini, New Business da Cxpress
**Regiao:** brasil (pt-BR) · GTM `GTM-T4XDWHL3`

## Estrutura

- Header (logo + CTA)
- Hero VSL (eyebrow, H1, lead, video placeholder, byline, CTA)
- Faixa (4 itens)
- O webinar (3 cards)
- O desafio (3 cards de dor + frase de fecho)
- O que mudou (4 itens numerados + chips de canais)
- O resultado (4 stats, fundo escuro)
- Inscricao (form mock)
- Fecho (frase-ancora + CTA)
- Footer

## Estado

- [x] HTML gerado
- [x] OG image 1200×630 → `assets/og-webinar-concierge-br.png` (template `assets/og-template.html`, render `assets/render_og.py`)
- [x] Revisao — ver `REVISAO.md`
- [ ] Video do webinar — trocar o `div.vsl-video__ph` pelo embed real
- [ ] Formulario integrado — rodar `/lp-integrar-form cxpress/webinar-concierge-br [snippet]` (redirect pos-envio: pagina de obrigado a definir)
- [ ] Publicado — rodar `/lp-publicar cxpress webinar-concierge-br content.cxpress.io`

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-reversed.svg` (header + footer)
- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `assets/og-webinar-concierge-br.png` (OG)
