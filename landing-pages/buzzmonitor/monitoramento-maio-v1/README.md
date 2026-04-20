# LP — Webinar "Monitoramento de Concorrentes"

Landing page estática do webinar gratuito Buzzmonitor (26/Mai, 11h, Online e Ao Vivo).

## Origem

- **Copy:** [Notion · Copy LP](https://www.notion.so/3443934026fd804f97d6c081c233df72)
- **Base visual:** duplicada da LP `webinar-conteudo-que-converte` (aprovada pelo usuário) — mesmo design system, copy trocada e programa reduzido para 3 eixos (Mapeamento de Lacunas / Share of Voice e Sentimento / Benchmarking com Analytics).
- **Brand:** `brand/buzzmonitor/` (tokens + generation-rules + brandbook)

## Como abrir

HTML estático puro — basta abrir `index.html` no navegador. Sem build, sem dependências.

Logos são referenciados por caminho relativo (`../../brand/buzzmonitor/assets/logos/...`), então manter a LP dentro de `landing-pages/` preserva os caminhos.

## TODOs antes de publicar

- **Speakers:** substituir os 2 cards placeholder na seção "Com quem você vai aprender" por fotos/nomes/cargos reais.
- **Formulário:** `<form action="#">` é mock. Integrar com RD Station / HubSpot / Mautic / etc.
- **Tracking:** adicionar GA4 / Pixel / UTM handling conforme a stack do time.
- **Fonte HK Grotesk:** fallback `Manrope` está em uso (HK Grotesk é comercial, não está no Google Fonts). Se o time tiver licença, trocar o `<link>`.
- **OG image:** faltando — gerar peça social e adicionar `<meta property="og:image">`.
- **Favicon:** ausente — adicionar quando tiver asset definitivo.

## Decisões de design

Segue `landing-pages/GUIDELINES.md`:
- **Paleta restrita (3 cores):** roxo `#390155` (seção dark), laranja `#EB7C2E` (CTA), rosa/vermelho `#DE2451` (gradiente + acentos). Fundos só branco ↔ off-white.
- **Hero clean:** fundo branco, texto à esquerda, ticket-card à direita.
- **Gradiente rosa→laranja** aparece em 3 momentos de alto impacto (punchline, diff-art, urgência).
- **Respiro:** 160px desktop / 100px mobile entre seções.
- **Motion:** progressive enhancement — texto sempre visível mesmo se JS/CSS falhar.
