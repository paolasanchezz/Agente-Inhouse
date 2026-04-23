# LP — Webinar "Conteúdo que Converte"

Landing page estática do webinar gratuito Buzzmonitor (23/Abr, 11h, YouTube + LinkedIn).

## Origem

- **Copy:** [Notion · Copy LP](https://www.notion.so/32c3934026fd808ab188cd5ef1d4e3f1)
- **Brand:** `brand/buzzmonitor/` (tokens + generation-rules + brandbook)
- **Skills:** gerada com `frontend-design`, revisada com `web-design-guidelines`

## Como abrir

HTML estático puro — basta abrir `index.html` no navegador. Sem build, sem dependências.

Logos são referenciados por caminho relativo (`../../brand/buzzmonitor/assets/logos/...`), então manter a LP dentro de `landing-pages/` preserva os caminhos.

## TODOs antes de publicar

- **Speakers:** substituir os 2 cards placeholder na seção "Com quem você vai aprender" por fotos/nomes/cargos reais.
- **Formulário:** `<form action="#">` é mock. Integrar com RD Station / HubSpot / Mautic / etc. Remover o `alert()` do `<script>` quando conectar.
- **Tracking:** adicionar GA4 / Pixel / UTM handling conforme a stack do time.
- **Fonte HK Grotesk:** fallback `Manrope` está em uso (HK Grotesk é comercial, não está no Google Fonts). Se o time tiver licença, trocar o `@font-face`/`<link>`.
- **OG image:** faltando — gerar peça social e adicionar `<meta property="og:image">`.
- **Favicon:** `favicon.svg` + `favicon.png` (mascote Buzzmonitor — `logo-icon` do brand).

## Decisões de design

- **Direção:** editorial/tech-vibrante. Evita o "purple gradient on white" genérico proibido pela skill `frontend-design` — usa gradiente roxo→laranja real da paleta Buzzmonitor no hero, com formas geométricas (círculos, semicírculos, triângulos) nas 5 cores da marca como decoração atmosférica.
- **Paleta:** roxo `#390155` (base), laranja `#EB7C2E` (CTA), teal `#0E9D9B` (metadata/accents). Rosa e amarelo só em formas decorativas — respeita a regra "2-3 cores fortes por peça".
- **Tipografia:** League Spartan (display), Manrope (subtítulos, proxy de HK Grotesk), Lato (corpo). Todas via Google Fonts, com `preconnect`.
- **Motion:** CSS-only staggered reveal no hero + IntersectionObserver para fade-up no scroll. Respeita `prefers-reduced-motion`.
- **Acessibilidade:** skip-link, focus-visible com outline amarelo (contraste alto em todos os fundos), `aria-label`/`aria-labelledby` nas seções, inputs com `<label>` e `autocomplete`.
