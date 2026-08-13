# LP Buzzmonitor — monitoramento-com-ia

**Gerado em:** 2026-08-13
**Origem:** recriação de `material.buzzmonitor.com/monitoramento-redes-sociais` (export Webflow em `landing-pages/buzzmonitor/monitoramento-redes-sociais/`)
**Destino:** `https://content.buzzmonitor.com/monitoramento-com-ia` (guarda-chuva `content-buzzmonitor-com`, deploy via CI)
**Uso:** aquisição paga / orgânico BR, MoFu (agendar demonstração)

## Por que recriada

A versão em Webflow depende de `webflow.css` + `webflow.js` + jQuery + GSAP + Lenis + `tabler-icons.min.css`
(**1,39 MB só de CSS**, dos quais 1,24 MB são os ícones Tabler usados em 5 glifos do footer) e as classes `bz-*`
não têm **nenhum** override nos `@media` de 991/767/479 px: `bz-grid-2col` fica `1fr 1fr` até no celular,
`bz-h1` fica travado em 56 px, `bz-testi-grid` mantém 3 colunas. É a "estrutura técnica pouco responsiva"
que motivou a recriação.

Esta versão é **1 arquivo** (`index.html`, ~46 KB, CSS inline, zero framework), com grid que colapsa em
980 px / 760 px / 480 px, tipografia em `clamp()` e os 5 ícones sociais do footer como SVG inline.

## Estrutura

Mesma ordem narrativa do original, com **1 seção removida** (pedido do usuário):

1. HEADER (logo do brand, linka pra home Buzzmonitor em nova aba)
2. HERO (fundo branco com pattern de bolinhas radiais, H1 com "Redes Sociais" em laranja, CTA pill,
   card com os 15 chips de canal + popover no hover/foco, e o vídeo da plataforma)
3. TRUSTED-BY (marquee CSS infinito com os 11 logos de cliente + máscara de fade nas laterais)
4. FORMULÁRIO `#formulario` (grafismo decorativo à esquerda, 6 checks + card laranja com o Jotform,
   selo de preço e os 2 badges flutuantes)
5. EXPERIMENTE GRÁTIS 14 DIAS (5 checks + bloco de preço + CTA)
6. IA PARA GERAÇÃO DE INSIGHTS (colunas invertidas, botão outline laranja com seta animada)
7. MONITORAMENTO DE VÍDEOS, ÁUDIOS E IMAGENS
8. GESTÃO DE CRISES EM TEMPO REAL (colunas invertidas)
9. WHATSAPP (card + ícone)
10. DEPOIMENTOS (3 cards com glow colorido por marca: McCann / TotalPass / McDonald's)
11. FOOTER escuro (logo invertido, descrição, 5 sociais, política de privacidade)

**Removida:** a seção "● AI Insights" com o iframe do YouTube (`Z1FddOh05O4`) e o CTA "Comece Grátis!".
O tema de IA já é coberto pela seção 6.

## Trocas em relação ao original

| Item | Original (`monitoramento-redes-sociais`) | Aqui |
|---|---|---|
| **Formulário** | Jotform `250074757320049` | Jotform **`252995108251662`** (o mesmo de `plataforma-completa-monitoramento`) |
| **GTM** | `GTM-WFJVK858` | `GTM-WFJVK858` (idêntico; é o container BR de `tracking.json`) |
| Hero animado | GIF de 5,5 MB no CDN da Cloudinary | MP4 local `hero-plataforma.mp4` (818 KB, 6,7× menor) + poster JPG, `autoplay muted loop playsinline` |
| Ícones do footer | `tabler-icons.min.css` (1,24 MB) | 5 SVGs inline |
| Links sociais do footer | `href="#"` | URLs reais (Facebook/Instagram/YouTube/LinkedIn BR + LinkedIn global) |
| CTAs das seções 7 e 8 | `href="#"` (mortos) | `#formulario` |
| Atribuição do 3º depoimento | "na McDonals." (typo) | "na McDonald's" |
| Logo header/footer | assets do export Webflow | `brand/buzzmonitor/assets/logos/logo-primary.svg` e `logo-reversed.svg` (GUIDELINES §17) |
| Favicon | 6 `<link>` (favicon.png, dark, 48, webclip 180/192/512) | 1 `<link>` pro `logo-icon.png` do brand (GUIDELINES §12) |
| SEO | sem canonical, sem JSON-LD `WebPage`, `lang="en"` | pacote completo da GUIDELINES §15, `lang="pt-BR"` |

## Estado

- [x] HTML gerado (responsivo, 1 arquivo)
- [x] Assets copiados do export Webflow + MP4/poster baixados do CDN da Cloudinary
- [x] Formulário real integrado (Jotform `252995108251662`)
- [x] GTM `GTM-WFJVK858` (`check_gtm_region.py`: 1 OK, 0 bloqueios)
- [x] Registrada no `dominios/content-buzzmonitor-com/manifest.json`
- [x] `build_umbrella.py` roda limpo (11 LPs, 0 avisos)
- [ ] Deploy (CI, ao mergear o PR)

## Pendências

- **Botão do WhatsApp** (`Fale agora!`) aponta pra `#formulario`. No original o `href` é `#` (morto) e não
  existe número de WhatsApp verificado da Buzzmonitor no repo (o `wa.me/551150395028` que aparece em
  `landing-pages/cxpress/video-atendimento-obrigado` é da **Cxpress**, não assumido aqui). Com o número
  certo, é trocar 1 atributo.
- **Contraste do laranja (herdado do original, deliberado):** branco sobre `#ff6900` dá **2,89:1** e laranja
  `#ff6900` sobre branco (botão outline) dá **2,89:1**, abaixo do 4,5:1 da AA. É o mesmo caso já decidido pelo
  Victor em `plataforma-completa-monitoramento` (2026-07-29), então foi mantido por fidelidade. Se quiser
  resolver sem mudar a identidade: `#c75300` fecha 4,5:1 nos dois sentidos (texto no branco e branco no fundo).
  Afeta `.btn-primary`, `.formcard__title`, `.net__cta` e `.btn-outline`.
- Dois cinzas do original **foram** corrigidos porque a mudança é imperceptível: `#718096` → `#5f6b7a` no
  label do trusted-by (4,0 → 5,4:1) e `#888` → `#6f6f6f` na atribuição dos depoimentos (3,5 → 5,0:1).

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header), `logo-reversed.svg` (footer),
  `logo-icon.png` (favicon) — os 3 SVGs do brand são raster/base64, sem `<text>` vivo (GUIDELINES §19)
- `./assets/hero-plataforma.mp4` (900×506, 17,5 s, 818 KB) + `./assets/hero-poster.jpg` (10 KB) — baixados de
  `res.cloudinary.com/eqe5rlby/video/upload/.../gif-plataforma-hero_x5uc5x` (o mesmo asset que o original usava
  como GIF de 5,5 MB via `background-image`)
- 15 ícones de canal `.webp` + 11 logos de cliente (`img-cliente-01..11`, 10 SVG + 1 AVIF)
- `img-grafismos-buzzmonitor.svg`, `preco.svg`, `img-experimente-14-dias.svg`, `img-gestao-crises.svg`,
  `whatsapp.svg`
- `img-ai-insights.webp` (+ `-p-500`), `img-monitoramento-audiovisual.webp` (+ `-p-500`) — servidos com `srcset`
- `aspasamarelas.svg`, `aspasroxa-2.svg`, `aspasLaranja.svg`, `mccan.svg`, `totalpass.svg`, `mcdonalds.svg`
- `og-monitoramento-com-ia.png` (1200×630) — cópia da `og-monitoramento.png` do original, renomeada pra
  convenção `og-{slug}.png` (GUIDELINES §18)

`mccan.svg` tem viewBox quadrada (652×652) com muito respiro em volta: precisa de `object-fit: cover`
(igual ao original) senão a wordmark encolhe e quase desaparece no card de depoimento.

## Validações rodadas

- em-dash: 0 (`—` e `&mdash;`)
- `meta description`: 1 · `og:`: 10 · `twitter:`: 4 · JSON-LD: 1, parseia
- OG image: 1200×630 ✓
- `check_gtm_region.py`: 1 OK, 0 aviso, 0 bloqueio
- `build_umbrella.py`: 11 LPs, 0 avisos, 0 placeholder/path relativo vazando
- **Overflow horizontal: 0 elementos** em 390 / 768 / 1440 px (auditado via Playwright, varrendo
  `body *` e comparando `getBoundingClientRect().right` com `innerWidth`)
- **Imagens quebradas: 0** nos 3 breakpoints (com `loading=lazy` forçado a `eager`)
- Grid: 2 colunas em 1440, 1 coluna em ≤980; depoimentos 3 → 2 (≤980) → 1 (≤760) colunas
- Ordem no mobile: texto antes do visual nas seções invertidas (`.grid2--flip`), conforme GUIDELINES §3
- Vídeo do hero: `readyState 4`, `paused: false` nos 3 breakpoints (o `play()` no script cobre o caso do
  wrapper `.reveal` começar em `opacity: 0`)
- Popover dos chips: reposicionado por JS (load + resize + hover/foco/touch) pra nunca sair da viewport,
  medido em 390/768 px
- Header `position: sticky` preservado usando `overflow-x: clip` (não `hidden`) no `body`
