# LP Buzzmonitor — webinar-atencion-multicanal-latam

**Gerado em:** 2026-07-29
**Copy-fonte:** `copy.txt` (output de /lp-preparar)
**Design espelhado:** `landing-pages/buzzmonitor/monitoreo-competidores-ia-latam/index.html` (mesma paleta, tipografia, ticket de data, countdown, grids de programa/problema, urgencia dark)
**Regiao:** latam (es-419) · GTM-MKQBX2MG
**Form provider:** Jotform (integrado em 2026-07-29)

## Estrutura

- HERO (eyebrow + h1 + sub + CTA + ticket "Save the date")
- Countdown (contagem regressiva ate 2026-08-27T16:00:00-06:00)
- CUPO GRATUITO — form Jotform, id="inscripcion" (2a secao, ToFu)
- PROGRAMA — grid 3 itens
- PREGUNTA — lista 4 itens (X vermelho) + CTA
- CASO REAL — card de estatistica (Youse Seguros, 36h -> 3h)
- WEBINAR BANNER — banner gradiente + CTA
- PARA QUIÉN ES — checklist 3 itens + CTA + visual "IA en este webinar" (nucleo IA + 4 tags orbitando: Atencion al Cliente Multicanal, Smart Replies, Sentiment Classification, AI Insights). Secao "IA EN ESTE WEBINAR" removida como bloco standalone em 2026-07-29 (a pedido do usuario — o visual foi reaproveitado aqui, o titulo "IA en este webinar" nao aparece mais na pagina).
- QUIEN PRESENTA — 2 speakers (Luis Perez, Lorena Rodriguez)
- AVISO + CTA FINAL — secao urgencia (dark) unificada, CTA final
- Footer

## Estado

- [x] HTML gerado
- [x] Revisao (frontend-design review + web-design-guidelines) — ver `REVISAO.md`
- [x] Formulario integrado — Jotform (`jsform/261188302248052`)
- [x] Publicado — https://webinar.buzzmonitor.com/webinar-atencion-multicanal-latam (2026-07-29, guarda-chuva, deploy `dpl_8cAu76vySXf62o8f2F6LGKon37S4`)

## Pendencias antes de publicar

1. ~~Fotos dos speakers~~ — resolvido em 2026-07-29: reaproveitadas as fotos reais de `landing-pages/buzzmonitor/social-listening-mayo-2026-latam/assets/` (mesmos speakers, Luis Perez e Lorena Rodriguez), copiadas para `assets/luis-perez.jpg` e `assets/lorena-rodriguez.jpg` desta LP.
2. ~~OG image custom (1200x630)~~ — decisao do usuario em 2026-07-29: nao gerar. `og:image`/`twitter:image` apontam para `{{BRAND_LOGO_PNG_PATH}}` (o logo da marca, 250x250), nao para uma imagem 1200x630 dedicada. Preview em WhatsApp/LinkedIn vai mostrar so o logo, nao um card ilustrado.
3. `{{DOMAIN}}` e `{{BRAND_LOGO_PNG_PATH}}` no `<head>` (SEO) sao placeholders — `lp-publicar` resolve com o dominio real e o path do logo na hora do deploy.

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `./assets/luis-perez.jpg`, `./assets/lorena-rodriguez.jpg` (fotos dos speakers)
- `./assets/` (LP-local, pendente: og-image.png)
