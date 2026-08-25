# LP Buzzmonitor — social-listening-guia-es

**Gerado em:** 2026-08-24
**Copy-fonte:** `copy.txt` (output de `/lp-preparar`, revisado 2x por Paola)
**Região/idioma:** LATAM · ES-419 · destino previsto `material.buzzmonitor.com/social-listening-guia-es`

> **Nota de nomenclatura:** a pasta foi renomeada de `social-listening-guia` para `social-listening-guia-es` durante o `/lp-gerar`. Sem o sufixo `-es`, a cascata de detecção de região (`landing-pages/CONTEXT.md` §5.1) cai no fallback `brasil` — o que geraria `<html lang="pt-BR">`, GTM do Brasil e OG locale errados numa LP inteiramente em espanhol. Convenção: BR sem sufixo, LATAM/ES = `-es`, PT = `-pt`.

## Estrutura (atualizada apos varias iteracoes de design, 2026-08-25)

- HERO (overline "PLAYBOOK GRATUITO" + H1 com dor/gradiente + sub + CTA; visual: mascote grande centralizada + radar/sonar + 4 cards flutuantes com beneficios reais + dot-field + orbit path)
- FORM (2ª seção, regra ToFu/material rico do GUIDELINES §10 — fundo gradiente laranja→rosa, card do form em branco, form real via Jotform embed, bloco de texto ao lado em branco/grande)
- DESTAQUE (seção de pausa, H2 + 2 BODY, sem lista)
- QUE VAS A APRENDER (grid de 5 beneficios, TODAS as cards em degrade roxo→laranja com texto branco)
- PARA QUIEN (grid de 4 cards com icone em circulo pastel, nao mais lista vertical)
- CLIENTES (prova social: 10 logos em marquee animado/loop infinito + 4 stats com contador animado, fundo branco)
- CTA FINAL (fundo gradiente roxo→laranja)
- FOOTER (5 redes sociais reais: Instagram, X, Facebook, LinkedIn, YouTube)

## Paleta usada (§1 GUIDELINES — 3 cores)

Primary `#390155` (roxo) + Secondary `#EB7C2E` (laranja, CTA) + Teal `#0E9D9B` (check icons). Primary Light `#F2D8FF` como fundo da seção CLIENTES (conforme `generation-rules.json`).

## Estado

- [x] HTML gerado
- [x] OG image 1200×630 → `assets/og-social-listening-guia-es.png`
- [x] Revisão (frontend-design review + web-design-guidelines) rodada
- [x] Formulário integrado — Jotform (2026-08-25), form id `262355185955871`
- [x] Publicado — live em `material.buzzmonitor.com/social-listening-guia-es` (varias entregas incrementais via PR, ultima #358)

**Form provider:** Jotform (2026-08-25) — `https://form.jotform.com/jsform/262355185955871`, embed via `<script>` dentro de `.jotform-embed`.

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
