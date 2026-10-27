# LP Cxpress — oferta-whatsapp-equipe

**Gerado em:** 2026-10-23
**Copy-fonte:** `copy.txt`
**Clone estrutural de:** `landing-pages/cxpress/oferta-atendimento-blackfriday` (mesma familia de oferta pos-webinar em `content.cxpress.io`, mesma oferta).
**Webinar de origem:** `content.cxpress.io/webinar-whatsapp-equipe` (4 de novembro de 2026, 11h)
**Regiao:** brasil · `<html lang="pt-BR">` · GTM `GTM-T4XDWHL3`

## Estrutura

- Header (logo)
- Hero + formulario (kicker, H1, 2 paragrafos, oferta em 3 bullets, form mock, disclaimer)
- Marcas (marquee com os 42 logos de clientes, rotulo "Mais de 800 empresas atendem pela API Oficial com a Cxpress")
- Impacto (H2 + 2 paragrafos)
- Depois da virada (H2 + grid de 4 beneficios + fechamento + CTA)
- Footer

## Decisoes

- **Formulario:** publicado primeiro em mock para aprovacao (2026-10-27) e depois trocado pelo Jotform compartilhado das ofertas Cxpress BR.
- **SEO com placeholders** `{{DOMAIN}}`, `{{OG_IMAGE_PATH}}` e `{{BRAND_LOGO_PNG_PATH}}`, resolvidos na publicacao.
- **Sem "ao vivo"**: o webinar e reprise da gravacao.
- **Risco de bloqueio** citado so para app nao oficial, em tom condicional (correcao factual do PR #744 da LP do webinar).

## Estado

- [x] HTML gerado
- [x] OG image 1200×630 → `assets/og-oferta-whatsapp-equipe.png` (template em `assets/og-template.html`)
- [x] Revisao — ver `REVISAO.md` (2 criticos aplicados)
- [x] Formulario integrado — Jotform `261045149477663` ("CXPRESS BR | MKT | LPs - Proposta | META ADS"), o mesmo das outras ofertas Cxpress BR. O CRM diferencia os leads desta LP pela URL/UTM.

**Form provider:** Jotform (2026-10-27)
- [ ] Publicado — `/lp-publicar cxpress oferta-whatsapp-equipe content.cxpress.io`

## A confirmar antes de publicar

1. Oferta: o bullet de implantacao em 21 dias foi trocado por "Economize R$ 4 mil..." em 2026-10-23. Confirmar com comercial que a economia de R$ 4 mil vale para esta campanha.
2. "Mais de 800 empresas" segue atual.

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-primary.svg` (header, sem `<text>`)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer, sem `<text>`)
- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `./assets/clientes/cliente-01.png` … `cliente-42.png`
