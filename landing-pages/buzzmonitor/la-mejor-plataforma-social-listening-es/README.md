# LP Buzzmonitor — la-mejor-plataforma-social-listening-es

**Gerado em:** 2026-07-17
**Copy-fonte:** `copy.txt` (estruturada a partir da LP publicada em contenido.getbuzzmonitor.com/la-mejor-plataforma-social-listening-marketing + referência de design escolha-a-buzzmonitor.webflow.io)
**Região/idioma:** LATAM · ES-419 · destino `content.buzzmonitor.com/la-mejor-plataforma-social-listening-es` (migrada de `material.buzzmonitor.com` em 2026-07-21; path antigo faz 301)

## Estrutura

- HERO (overline + H1 + sub + 2 CTAs + 3 stats + tela da plataforma)
- LOGOS — logo wall de 10 marcas extraídas 1:1 da LP publicada (Samsung, Sony, IKEA, Sephora, Santander, Havas, TBWA, McCann, Fundación Real Madrid, Bizum). Assets em `assets/clientes/`.
- COMPARATIVO na **segunda dobra** (tabela 15 features × Buzzmonitor + 10 concorrentes; dados em `comparativo.json`, transcritos 1:1 da LP publicada) — movido pra cá a pedido do Victor, 2026-07-20
- CTA-FINAL + FORM na **terceira dobra** (form réplica GreatPages; card mostra preço "Planes desde 390 USD/mes")
- POR-QUE-ELEGIR (texto + checklist de 6)
- SOLO-BUZZMONITOR (lista de 6 + grid de 12 ícones de canais)
- VISION-INTEGRAL (4 cards)
- OFERTA (dark, tag rotacionada "14 días gratis"; SEM preço na versão LATAM)
- TESTIMONIOS (6 citas literais de clientes) + FOOTER

## Form (réplica GreatPages — decisão desta LP)

O form NÃO é mock nem embed de provedor: replica o form GreatPages da página original
(page id **2705735**) postando JSON no MESMO endpoint `https://contenido.getbuzzmonitor.com/conversion`
com os MESMOS IDs de campo + UTMs da querystring + Referral/Dispositivo/URL, e redireciona
pro mesmo `/muchas-gracias`. Leads caem exatamente onde caem hoje. Endpoint tem CORS aberto
(`Access-Control-Allow-Origin: *`, verificado 2026-07-17). `lp-integrar-form` não se aplica.

## Tracking

- **GTM `GTM-5PNK2VZ`** — o mesmo container das páginas LATAM atuais (pedido explícito do Victor,
  2026-07-17). Diverge do `tracking.json` latam (`GTM-MKQBX2MG`) → selo `.tracking.lock`
  com `grandfathered: true`. Decidir depois se o tracking.json muda ou se as LPs migram de container.
- O container dispara Termly (consent), Meta Pixel, LinkedIn Insight, GA4 e Google Ads —
  CSP do domínio atualizado em `landing-pages/dominios/material-buzzmonitor-com/vercel.json`.

## Estado

- [x] HTML gerado
- [x] Revisao (responsivo 390/768/1440 sem overflow; SEO completo; JSON-LD parseia; imgs com alt; em-dash 0)
- [x] Formulario real (réplica GreatPages, ver acima)
- [ ] Publicado — manifesto + merge na main (deploy via CI `lp-deploy.yml`)

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/{logo-icon.png, logo-primary.svg, logo-reversed.svg}`
- `./assets/img-plataforma-hero.avif` + `./assets/tela-computador-bm2.png` (hero/oferta)
- `./assets/icon-*.webp` (12 canais) · `./assets/og-image.png` (1200×630)

## Pendências conhecidas

- Telas da plataforma estão com UI em PT-BR (assets enviados pelo Bruno no Drive). Trocar quando houver capturas ES.
- Teste real de submit do form pendente (gera lead de verdade — fazer 1 envio de teste pós-deploy e apagar o lead).
