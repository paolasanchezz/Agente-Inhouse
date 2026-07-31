# Revisao LP — buzzmonitor/plataforma-completa-social-media-latam

**Data:** 2026-07-31
**Auditores:** frontend-design (review mode) + web-design-guidelines + auditoria SEO/GTM/logo (lp-revisar Passo 3.5-3.7)

**Origem:** HTML trazido pelo usuario via `~/Downloads/buzzmonitor-latam-lp.html` (fora do pipeline `/lp-preparar` → `/lp-gerar`). Nao existe `copy.txt` fonte — auditoria de fidelidade de copy (Passo 3.6) foi **skipped (copy-fonte ausente)**.

## Aplicado automaticamente (12 criticos)

- [x] Logo do header substituido — era `<span class="fox">` + texto desenhados em CSS/clip-path; trocado por `<img src="../../brand/buzzmonitor/assets/logos/logo-primary.svg">` (logo real da marca)
- [x] Marca decorativa no centro do visual do hero (`.center-mark`) — clip-path aproximado trocado pelo `logo-icon.png` real (mascote raposa)
- [x] Favicon ausente — adicionado `<link rel="icon" href="../../brand/buzzmonitor/assets/logos/logo-icon.png">` (GUIDELINES §12)
- [x] Logo do header linkava para `href="#"` — trocado para `https://getbuzzmonitor.com/es/` (home regional LATAM) com `target="_blank" rel="noopener"` (GUIDELINES §17)
- [x] `<html lang="es">` — trocado para `lang="es-419"` pra bater com o hreflang da regiao (GUIDELINES §16)
- [x] Pacote SEO obrigatorio ausente (GUIDELINES §15) — adicionado: `meta description` localizada, `meta robots`, `meta author`, 10 tags Open Graph, 4 tags Twitter Card, JSON-LD (Organization + WebPage + SoftwareApplication), `canonical` — todos com placeholders `{{DOMAIN}}` / `{{OG_IMAGE_PATH}}` / `{{BRAND_LOGO_PNG_PATH}}` (resolvidos pelo `lp-publicar` na publicacao, convencao de `lp-gerar`)
- [x] GTM ausente (regiao latam esperava `GTM-MKQBX2MG` e a LP nao tinha nenhum) — injetado snippet canonico (CONTEXT §5.3) no `<head>` + `<noscript>` apos `<body>`. Selo `.tracking.lock` gravado (`ok`, fingerprint `0cc09bc8991879c7`)
- [x] Skip-link ausente — adicionado `<a href="#main" class="skip-link">Ir al contenido</a>` + `id="main"` no `<main>`
- [x] Contraste AA — eyebrow (badge "SOLUCIÓN INTEGRAL..." e "MÁS VALOR, MENOS COSTO") tinha texto laranja `#ff6b16` sobre fundo quase branco (~2.8:1, reprova AA) — trocado para `var(--navy)` (~10:1)
- [x] Contraste AA — `.good` (coluna "Buzzmonitor" da comparativa) usava verde `#0aa35b` sobre branco (~3.4:1, reprova AA) — trocado para `#15803d` (~5.1:1)
- [x] Motion sem fallback — `scroll-behavior: smooth` sem respeitar `prefers-reduced-motion` — adicionado bloco `@media (prefers-reduced-motion: reduce)`
- [x] Icones decorativos (emoji dentro de `.icon`/`.circle-icon`, 20 ocorrencias) sem `aria-hidden` — leitor de tela anunciava o emoji redundante com o texto do card — adicionado `aria-hidden="true"` em todos

## OG image — gerada nesta revisao (nao pendente)

Diferente do padrao (`lp-gerar` normalmente deixa a OG image pendente), esta sessao ja gerou `assets/og-image.png` (1200×630, via template + Chrome headless) com headline + logo da marca. Confirmar que ainda serve depois de qualquer alteracao de copy.

## Melhorias opcionais (2)

- [ ] Menu mobile (`.menu-btn`) alterna `display` via JS inline em vez de classe CSS — funciona, mas fica mais robusto com toggle de classe + CSS transition. Nao bloqueante.
- [ ] `.quote-card .quote` (aspas decorativas “) poderia ser `aria-hidden="true"` — puramente decorativo, texto da citacao ja esta no `<p>` seguinte.

## Nice-to-haves (1)

- [ ] Footer nao tem logo (so texto de copyright) — GUIDELINES §17 documenta o padrao de logo no footer, mas nao e obrigatorio quando o design original nao previu. Estilistico, ignorar e aceitavel.

## Pendencias fora do escopo do /lp-revisar

- Este HTML nunca passou por `/lp-preparar` (sem `copy.txt`) — se for preciso reeditar copy no futuro, considerar rodar `/lp-preparar` retroativamente pra ter fonte estruturada + anti-IA.
- `{{DOMAIN}}`, `{{OG_IMAGE_PATH}}` e `{{BRAND_LOGO_PNG_PATH}}` ficam como placeholder ate a decisao de dominio/modo (solo vs guarda-chuva) — `lp-publicar` resolve automaticamente.

## Proximos passos

- Design aprovado? -> `/lp-integrar-form buzzmonitor/plataforma-completa-social-media-latam "{snippet}"`
- Publicar -> `/lp-publicar buzzmonitor plataforma-completa-social-media-latam [dominio]`
