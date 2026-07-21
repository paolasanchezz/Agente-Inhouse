# LP Buzzmonitor — ia-para-social-listening-es

**Gerado em:** 2026-07-17
**Copy-fonte:** `copy.txt` (estruturada a partir da LP publicada em contenido.getbuzzmonitor.com/ia-para-social-listening + referência de design buzzmonitor---teste-claude---webflow.webflow.io)
**Região/idioma:** LATAM · ES-419 · destino `content.buzzmonitor.com/ia-para-social-listening-es` (migrada de `material.buzzmonitor.com` em 2026-07-21; path antigo faz 301)

## Estrutura

- HERO (overline + H1 + sub + CTA + 2 stats + tela da plataforma)
- LOGOS — logo wall de 10 marcas extraídas 1:1 da LP publicada (Samsung, Sony, IKEA, Sephora, Santander, Havas, TBWA, McCann, Fundación Real Madrid, Bizum). Cinza uniforme; assets em `assets/clientes/`. Havas recolorido (era branco).
- CTA-FINAL + FORM na **segunda dobra** (movido pra cá a pedido do Victor, 2026-07-20; form réplica GreatPages). Card mostra preço "Planes desde 390 USD/mes".
- BENEFICIOS (6 itens + 3 pills)
- 4 FEATURES alternadas com telas da plataforma (social listening `.webm`, AI Insights, audiovisual, gestão de crises)
- OFERTA (dark, tag "14 días gratis"; SEM preço na versão LATAM)
- TESTIMONIOS (3 citas literais)
- VIDEO como **última seção** antes do footer (movido pra cá a pedido do Victor, 2026-07-20; YouTube `nBMZZZKrMpI`, vídeo oficial ES, facade lazy) + FOOTER

## Form (réplica GreatPages — decisão desta LP)

Mesmo esquema da LP irmã: POST JSON pro endpoint `https://contenido.getbuzzmonitor.com/conversion`
com os IDs de campo da página original (page id **1657740**) + UTMs + redirect pro `/muchas-gracias`.
CORS aberto verificado 2026-07-17. `lp-integrar-form` não se aplica.

## Tracking

- **GTM `GTM-5PNK2VZ`** (mesmo container das páginas LATAM atuais, pedido do Victor). Diverge do
  `tracking.json` latam → `.tracking.lock` com `grandfathered: true` (mesma nota da LP irmã).

## Estado

- [x] HTML gerado
- [x] Revisao (responsivo 390/768/1440 sem overflow; SEO completo; JSON-LD parseia; imgs com alt; em-dash 0)
- [x] Formulario real (réplica GreatPages, ver acima)
- [ ] Publicado — manifesto + merge na main (deploy via CI `lp-deploy.yml`)

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/{logo-icon.png, logo-primary.svg, logo-reversed.svg}`
- `./assets/img-plataforma-hero.avif` + `./assets/tela-computador-bm2.png` (hero)
- `./assets/img-social-listening.webm` (+poster `tela-monitoramento-1.png`), `img-ai-insights.webp`, `img-monitoramento-audiovisual.webp`, `img-gestao-crises.svg`, `img-relatorios-dashboard.png`
- `./assets/logo-{mcdonalds,mccann,totalpass}.svg` · `./assets/og-image.png` (1200×630)

## Pendências conhecidas

- Telas da plataforma estão com UI em PT-BR (assets do Drive). Trocar quando houver capturas ES.
- Teste real de submit do form pendente (gera lead de verdade — fazer 1 envio de teste pós-deploy e apagar o lead).
- H1 abre pelo ganho (não pela dor) seguindo a referência aprovada; se conversão não melhorar, testar variante dor-first (GUIDELINES §3).
