# LP Buzzmonitor — social-listening-guia-es

**Gerado em:** 2026-08-24
**Copy-fonte:** `copy.txt` (output de `/lp-preparar`, revisado 2x por Paola)
**Região/idioma:** LATAM · ES-419 · destino previsto `material.buzzmonitor.com/social-listening-guia-es`

> **Nota de nomenclatura:** a pasta foi renomeada de `social-listening-guia` para `social-listening-guia-es` durante o `/lp-gerar`. Sem o sufixo `-es`, a cascata de detecção de região (`landing-pages/CONTEXT.md` §5.1) cai no fallback `brasil` — o que geraria `<html lang="pt-BR">`, GTM do Brasil e OG locale errados numa LP inteiramente em espanhol. Convenção: BR sem sufixo, LATAM/ES = `-es`, PT = `-pt`.

## Estrutura

- HERO (overline + H1 com dor + sub + CTA, visual abstrato "signal/conversação" à direita)
- FORM (2ª seção, regra ToFu/material rico do GUIDELINES §10 — mock, 3 campos)
- DESTAQUE (seção de pausa, H2 + 2 BODY, sem lista)
- QUE VAS A APRENDER (grid de 5 benefícios, check teal)
- PARA QUIEN (lista vertical de 4 itens, tratamento visual distinto do grid acima)
- CLIENTES (prova social: 10 logos em grayscale + 4 stats, fundo primaryLight)
- CTA FINAL (fundo gradiente roxo→laranja)
- FOOTER

## Paleta usada (§1 GUIDELINES — 3 cores)

Primary `#390155` (roxo) + Secondary `#EB7C2E` (laranja, CTA) + Teal `#0E9D9B` (check icons). Primary Light `#F2D8FF` como fundo da seção CLIENTES (conforme `generation-rules.json`).

## Estado

- [x] HTML gerado
- [ ] OG image 1200×630 → `assets/og-social-listening-guia-es.png` (arquivo **único** — nunca também `og-image.png`)
- [ ] Revisão (frontend-design review + web-design-guidelines) — rodar `/lp-revisar buzzmonitor/social-listening-guia-es`
- [ ] Formulário integrado — rodar `/lp-integrar-form buzzmonitor/social-listening-guia-es [snippet]` (aguardando ferramenta de automação — ActiveCampaign, confirmado com Paola)
- [ ] Publicado — rodar `/lp-publicar buzzmonitor social-listening-guia-es material.buzzmonitor.com`

## Pendências de conteúdo (fora do código, decisão da Paola)

1. **Mural de logos (seção CLIENTES):** copiei 1:1 o set já usado em `ia-para-social-listening-es` (Samsung, Sony, IKEA, Sephora, Santander, Havas, TBWA, McCann, Real Madrid, Bizum). Confirmar se é o correto para este material ou se ela quer outro conjunto.
2. **OG image** ainda não existe — gerar antes de publicar.

## Validações rodadas (Passo 4 da skill lp-gerar)

- em-dash (`—`) no HTML: 0
- `&mdash;`: 0
- `meta name="description"`: 1
- `meta property="og:`: 10 (≥8 ok)
- `meta name="twitter:`: 4 (≥4 ok)
- JSON-LD: 1 bloco, parseia como JSON válido
- Todas as imagens com `alt` (ou `alt=""` + `aria-hidden="true"` quando decorativas)
- Form em mock (`action="#"`, `onsubmit="event.preventDefault()"`)
- Contagem de itens por seção bate com `copy.txt`: 5 benefícios, 4 "para quién", 10 logos + 4 stats
- Nenhum em-dash/pull-quote/kicker inventado fora da whitelist (labels de form, disclaimer genérico, footer, skip-link, aria-labels)
- Header/footer: logo aponta para `https://getbuzzmonitor.com/es/` (home LATAM), `target="_blank" rel="noopener"`, `aria-label="Buzzmonitor: página principal"`
- Logos de marca (Buzzmonitor) validados como raster/base64 (sem `<text>` vivo) — seguros conforme §19

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `./assets/clientes/logo-{samsung,sony,ikea,sephora,santander,havas,tbwa,mccann,realmadrid,bizum}.png` (LP-local, copiados de `ia-para-social-listening-es`)
