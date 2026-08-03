# LP Buzzmonitor — Webinar Diversidade 2026

**Gerado em:** 2026-07-01 (reconstruído 2026-07-02 no padrão real de webinar)
**Copy-fonte:** `copy.txt`
**Região:** brasil (pt-BR) · **GTM:** GTM-WFJVK858
**Evento:** Webinar do 8º Estudo de Diversidade · 04/08/2026 (terça) · 11h BRT · online e ao vivo

## Direção

LP construída **no padrão real das LPs de webinar Buzzmonitor** (base: `analise-preditiva-maio-2026`): hero com ticket card de data (sem foto), fontes League Spartan + Manrope + Lato, ticker roxo, form na 2ª dobra, seções problema (X vermelhos) / oferta / programa / para quem / palestrantes / urgência dark, paleta 3 cores + acentos em gradiente.

**Referências ao estudo (leves, decisão da cliente):** as fotos do estudo entram **só depois da 1ª dobra** — mosaico 2×2 (mix cor + P&B) na seção "O estudo" e collage de 3 fotos na seção "Para quem". Copy original, sem repetir os textos da LP do estudo.

## Estrutura

Hero (ticket 04/08) → ticker → Inscrição (form mock, 2ª dobra) → Problema (3 X-cards + punchline) → O estudo (mosaico de fotos + copy) → Programa (3 cards) → Para quem (lista ✅ + fotos) → Palestrantes (genérico, Time Buzzmonitor) → Urgência (dark) → Footer.

## Decisões (confirmadas pela cliente)

- Data/hora: 04/08 (terça), 11h BRT.
- Palestrantes: genérico "Especialistas da Buzzmonitor" (sem nomes).
- Inscrição: form mock. Integrar embed real via `/lp-integrar-form` depois.
- Fotos: 7 reaproveitadas do estudo, todas abaixo da 1ª dobra.

## Estado

- [x] HTML no padrão webinar + validado (0 em-dash, SEO completo c/ JSON-LD Event, GTM 2 blocos, fotos abaixo da dobra)
- [x] Formulário real integrado — Jotform `252154974852667` (`/jsform/` embed), 2026-07-02
- [ ] Revisão — `/lp-revisar buzzmonitor/webinar-diversidade-2026`
- [ ] OG image 1200×630 → `assets/og-image.png`
- [ ] Publicar — `/lp-publicar buzzmonitor webinar-diversidade-2026 webinar.buzzmonitor.com`

**Form provider:** Jotform (jsform 252154974852667) · integrado 2026-07-02

## Assets

`assets/` — 7 retratos do estudo. Logos vêm de `../../brand/buzzmonitor/assets/logos/` (reescritos no deploy).

## Cadência de e-mail pós-inscrição

Criada em 2026-07-20: `conhecimento/copywriting/criacao/buzzmonitor/2026-07-20/cadencia-webinar-diversidade-2026/` — confirmação, aquecimento, faltam 3 dias, é amanhã, estamos ao vivo, e-mail com o estudo em si. Sem oferta/demo depois; a automação termina entregando o PDF do estudo (`../estudo-diversidade-2026`). Cada e-mail tem um header próprio (`assets/0N-*-header.png`, 1200×400) gerado no mesmo padrão visual desta LP (cores, fontes, fotos reais do estudo). Banner de newsletter também disponível (`assets/07-newsletter-banner.jpg`) e capa de YouTube/vídeo em `assets/08-youtube-cover.jpg` (1280×720, grid de 8 fotos do estudo, sem CTA escrito).

## Descrição do evento (Título + Descrição)

Texto de divulgação do webinar (plataforma de transmissão / listagem de evento), no formato Título + Descrição usado nos webinars anteriores da Buzzmonitor: `descricao-evento.md`. Publicado também no hub Notion do webinar (topo da página).
