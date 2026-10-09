# Revisao LP — buzzmonitor/pt-plataforma-completa-agencias

**Data:** 2026-10-07
**Auditores:** revisao independente (design + web interface guidelines + fidelidade de copy, subagente REVIEW ONLY) + checks deterministicos (`check_gtm_region.py`, SEO/JSON-LD, build do guarda-chuva) + screenshots Playwright do dist buildado (1440px e 375px)

Base de design: `agencias-es` (v3 aprovada pelo Victor, ja revisada). Esta revisao focou no que mudou na versao PT.

## Aplicado automaticamente (5 criticos)

- [x] **Prints com UI em espanhol** ("Distribución de reacciones", "Prioridad de Tickets", "¿Qué necesito saber?") — trocados pelas versoes PT ja usadas noutras LPs: `crise-1.png`, `crise-2.png`, `dashboard-analytics.png`, `insights.png`.
- [x] **Print errado no split de Atendimento** — `etapa-5.png` era outra tela de AI Insights (repetia a da secao IA); trocado por `crise-2.png` (Top 5 tags mais frequentes).
- [x] **Print de IA esticado ~15%** — `.ia-print img` forcava `aspect-ratio: 430/284` (do `ai-insights.png` da ES); agora `16/9` (o `insights.png` e 1920x1080).
- [x] **Header mobile transbordava 46px em 375px** — CTA "Pedir demonstração" e mais longo que o ES. ≤640px: gap 24→10, padding 15→12, seta do CTA da navbar escondida. Fonte mantida em 14px (piso §20). `scrollWidth` = 375 em 375px.
- [x] **Formulario enviava para o endpoint GreatPages da LATAM** (`contenido.getbuzzmonitor.com/conversion`) — envio e lista de paises removidos; form em mock ate `/lp-integrar-form` (Jotform PT). Meta Pixel LATAM hardcoded tambem removido (PT recebe pixel pelo GTM de Portugal).

Tambem aplicado (rapido, nao-critico): `title` do iframe "Depoimentos" → "Testemunhos" (PT-PT); `hreflang="pt-PT"` proprio; comentarios CSS em espanhol traduzidos; footer da `copy.txt` alinhado com o HTML.

Checks OK: GTM `GTM-NCFT22CW` (status ok, selo gravado), `lang`/`og:locale`/`inLanguage` pt-PT, JSON-LD parseia (Organization url = `getbuzzmonitor.com/pt/`, sameAs Instagram `buzzmonitor.pt` + LinkedIn), canonical, 10 og + 4 twitter, OG 1200x630, logo sem `<text>`, 0 em-dash, todo texto visivel literal da `copy.txt`, build do guarda-chuva sem avisos e todos os assets 200.

## Melhorias opcionais (3)

- [ ] **Hero com H2/H3 em texto corrido** (`.hero-sub` h2, `.hero-lead` h3) — herdado da v3 ES, onde o Victor pediu explicitamente H1/H2/H3. Semanticamente o H3 e um paragrafo; trocar por `<p>` manteria o visual. Nao alterado por ser decisao de estrutura aprovada.
- [ ] **Header ainda transborda em 320-360px** (menu fica em 363px). A ES tem o mesmo comportamento. Opcao: esconder o CTA da navbar abaixo de 380px (o hero ja tem CTA logo abaixo).
- [ ] **`insights.png` pesa 464 KB** (1920x1080 exibido a 620px). Uma versao WebP ~1240px reduziria para ~80 KB. E o mesmo arquivo da `monitoramento-manual-pt`.

## Nice-to-haves (1)

- [ ] CSS morto herdado dos elementos removidos: `.quote-grid`/`.quote-card`, `.cta-box .price`, `.form-msg*`, `.form-card .btn[disabled]`. Nao quebra nada (nenhum JS referencia).

## Proximos passos

- Design aprovado? → `/lp-integrar-form buzzmonitor/pt-plataforma-completa-agencias` com o Jotform PT `261405305585859`
- Publicar → `/lp-publicar buzzmonitor pt-plataforma-completa-agencias content.buzzmonitor.com`
