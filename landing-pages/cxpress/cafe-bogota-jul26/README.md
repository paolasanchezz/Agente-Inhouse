# LP — Café con Cxpress (Jul) · ES-LATAM

Landing page de evento presencial (workshop) da Cxpress em **Bogotá, Colombia**, 28/07/2026, 10:00 a.m.
Copy em **Español Latinoamericano** (fonte: Notion, ver `copy-fonte.md`).

## Design
Clone 1:1 do design de [`gestao-canais-ia-2026`](../gestao-canais-ia-2026/index.html) (evento presencial Cxpress BR).
O bloco `<style>` é idêntico — mesma paleta, tipografia (Open Sans / Source Sans 3 / Bitter), hero centralizado, countdown, reveal-on-scroll. Só o conteúdo, o idioma e uma seção foram adaptados.

### Diferenças de estrutura vs. a LP de referência
- **Seção "programação/timeline"** (que na ref. tinha horários) foi substituída por **"Caso en vivo"** — a copy não traz agenda com timestamps, e sim a narrativa do workshop (Conteúdo II + IV: Liana & Cora + perguntas reflexivas). Reusa os tokens/estilo do design.
- **CTA final** ("Los cupos son limitados") adicionado antes do footer, porque a copy tem uma "Chamada final" explícita. É só um botão que rola para o formulário (não um 2º form).

## Placeholders (a resolver antes de publicar)
| Item | Estado | O que fazer |
|---|---|---|
| **Formulário** | MOCK (campos reais: Nombre, Apellido, Correo corporativo, Teléfono, Empresa, País) | Trocar pelo embed real via `/lp-integrar-form cxpress/cafe-bogota-jul26 "<snippet>"`. Comentário `FORM MOCK` marca o ponto no HTML. |
| **Fotos dos speakers** | 2 cards com ícone-placeholder | Definir os ponentes, adicionar `assets/{nome}.jpg` e trocar nome/cargo. |
| **Local (venue)** | "Lugar por confirmar" + mapa centrado em Bogotá (cidade) | Definir o endereço, atualizar `.reach-addr` + `src` do iframe do mapa + `location` no JSON-LD. |
| **OG image** | Caminho referenciado (`og-cafe-bogota-jul26.png`) ainda não gerado | Gerar 1200×630 e colocar no namespace de assets Cxpress do guarda-chuva. |

## Config técnica
- `<html lang="es-419">` · `og:locale=es_CO`
- **GTM:** `GTM-WRQ47B9R` (container LATAM, de `brand/cxpress/tracking.json`) — head + noscript
- **Countdown alvo:** `2026-07-28T10:00:00-05:00`
- **Favicon:** `brand/cxpress/assets/logos/logo-icon.png`
- Região LATAM detectada via `<html lang="es-419">` (slug `cafe-bogota-jul26` sem sufixo → cascata §5.1 passo 2: `es-*` = latam)

## Publicação
**No ar (2026-07-10):** https://content.cxpress.io/cafe-bogota-jul26 — guarda-chuva `cxpress-lp-playbook-whatsapp2026`, deploy `dpl_45u6UkYesknPq6fvAJMUqQxJ8efX`, `index,follow`. Publicado com form MOCK + ponentes/local/OG placeholder (decisão do Victor). Smoke test pós-deploy: 26/26 vizinhas intactas, 0 regressões.
Relatório Notion: https://app.notion.com/p/3993934026fd810e98d2fa9960796b13
Atualizar: editar a fonte e rodar `/lp-publicar cxpress cafe-bogota-jul26 content.cxpress.io`. Form real: `/lp-integrar-form cxpress/cafe-bogota-jul26 "<snippet>"`.

## Copy / anti-IA
Copy majoritariamente transcrita da fonte (voz do cliente preservada). Texto conectivo (nav, eyebrows, headers, form, placeholders) escrito em ES-LATAM nativo (tuteo). Zero em-dash (`—`). Marca grafada **Cxpress**.
