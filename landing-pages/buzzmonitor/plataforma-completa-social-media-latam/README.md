# LP Buzzmonitor — plataforma-completa-social-media-latam

**Origem:** HTML trazido pelo usuario (`~/Downloads/buzzmonitor-latam-lp.html`), fora do pipeline padrao `/lp-preparar` → `/lp-gerar`. Nao existe `copy.txt` fonte.
**Regiao:** LATAM (ES) — `es-419`, GTM `GTM-MKQBX2MG`, Meta Pixel `935436740448328`.

## Estado

- [x] Logo real da marca aplicado (header + marca decorativa do hero + favicon)
- [x] Revisao (frontend-design review + web-design-guidelines + auditoria SEO/GTM/logo) — 12 criticos aplicados. Ver `REVISAO.md`.
- [x] OG image gerada (`assets/og-plataforma-completa-social-media-latam.png`, 1200×630)
- [x] Formulario integrado — Jotform, form id `241825239057661` (mesmo form usado em `mcp-es` e `plataforma-integral-social-media`), 2026-07-31
- [x] Ajustes visuais 2026-07-31: fundo branco no form do CTA final, cards do hero reposicionados (bug de `nth-child` contando `.connector`/`.center-mark` como irmaos), logos reais na secao "marcas y agencias" (removido "de Latinoamérica" do texto), secao nova "Empresas que ya confían en Buzzmonitor" com stats + logo wall, footer redesenhado (logo + redes sociais + política de privacidad)
- [x] Copy ajustada 2026-07-31: tabela comparativa (removido "Aspecto" do cabecalho, "Reportes automaticos" -> "Dashboards en tiempo real"), testimonios trocados pelos 6 reais de contenido.getbuzzmonitor.com/agencias (McCann, Kaleidoscopio, Publicis, Eureka&Co, SA365, Sube Agencia), CTA unificado em "Agenda una demo" em todos os botoes primarios, botao do header reduzido
- [x] Filtro dos logos (marcas/agencias + empresas) trocado de `grayscale(1)` para `brightness(0) invert(0.55)` — a versao anterior deixava logos de cor clara (IKEA, McDonald's) quase invisiveis; a nova achata qualquer cor pra uma silhueta cinza uniforme
- [x] Meta Pixel adicionado 2026-07-31 — `935436740448328`, snippet hardcoded no `<head>` (mesmo padrao usado em `cxpress/whatsapp-business-smb-latam`, commit `baff500`), logo apos o GTM
- [ ] Publicacao — `{{DOMAIN}}` / `{{OG_IMAGE_PATH}}` / `{{BRAND_LOGO_PNG_PATH}}` ficam como placeholder ate `/lp-publicar` decidir dominio/modo

**Form provider:** Jotform (2026-07-31)

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header + footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon + marca decorativa do hero)
- `./assets/og-plataforma-completa-social-media-latam.png` (OG image, LP-local)
- `./assets/logos-agencias/*` (7 logos — Kaleidoscopio Agency, McCann, IPG Mediabrands, Sube, Eureka&Co, Havas, TBWA) e `./assets/logos-clientes/*` (29 logos — Coca-Cola, Sephora, Samsung, IKEA, Amazon, Uber etc.) — baixados da própria LP oficial da Buzzmonitor (`contenido.getbuzzmonitor.com/agencias`), a pedido do usuário, pra reaproveitar a prova social real da marca nesta LP
