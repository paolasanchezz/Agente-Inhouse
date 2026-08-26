# Revisão LP — buzzmonitor/gestion-de-crisis-ia-latam-septiembre-2026

**Data:** 2026-08-26
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel) + auditoria GTM + auditoria SEO/JSON-LD/logo/OG (GUIDELINES §3.5-3.7)

## Aplicado automaticamente (6 críticos)

- [x] **GTM errado** — container `GTM-WFJVK858` (herdado do PT-BR) não bate com o esperado para região `latam` (`GTM-MKQBX2MG`, `brand/buzzmonitor/tracking.json`) — corrigido nos 2 blocos (head + noscript), stamp gravado (`--write-stamp`).
- [x] **Contraste AA — `.speaker-badge`** — texto `var(--c-accent-2)` sobre fundo `rgba(222,36,81,.09)` dava ≈4.19:1, abaixo do 4.5:1 exigido pra texto pequeno (GUIDELINES §7) — trocado para `var(--c-primary)` (≈13.97:1).
- [x] **Piso tipográfico mobile** — `.ticket-date small` estava em 12px (abaixo do piso de 14px pra label/caption, GUIDELINES §20) — subido pra 14px, letter-spacing reduzido pra caber a linha multi-fuso.
- [x] **Form mock sem atributos canônicos** — faltava `action="#" method="post" onsubmit="event.preventDefault()"` (GUIDELINES §11 / web-interface-guidelines) — clique no submit dispararia navegação real da página. Corrigido.
- [x] **JSON-LD `Organization.url`/`@id` hardcodado com o home do Brasil** (`https://buzzmonitor.com/`) em vez do home regional LATAM (`brand/buzzmonitor/brand-manifest.json#regions.latam.home` = `https://getbuzzmonitor.com/es/`) — corrigido `Organization`, `WebPage.isPartOf` e `Event.organizer` pra apontar pro `#organization` correto.
- [x] **Logo header/footer linkando pro home do Brasil** (`href="https://buzzmonitor.com/"`) em vez do home regional LATAM — corrigido pros 2 links (`https://getbuzzmonitor.com/es/`), conforme GUIDELINES §17.

## Melhorias opcionais (4)

Herdadas do design da LP original (PT-BR, aprovada e em produção) — sinalizadas, não alteradas silenciosamente (mudança estrutural grande exige aprovação):

- [ ] **H1 do hero** ("Gestión de Crisis con IA.") abre pelo tema/solução, não pela dor — GUIDELINES §3 / `fundamentos-copy.md` §0 recomendam H1 = dor, H2 = solução. O H2 atual já carrega parte da dor ("La próxima crisis de tu marca ya se está escribiendo en las redes"). Ajuste é decisão de quem aprova a copy.
- [ ] **Ordem de seções** diverge do canônico (GUIDELINES §6: Hero → Problema → Oferta/Programa → Diferencial → Para quem → Prova → Urgência → CTA). A LP tem Diferencial antes de Programa, e Speakers antes de Para Quién. Herdado do original.
- [ ] **Posição do formulário** — está na última seção; GUIDELINES §10 recomenda 2ª seção pra webinar ToFu/lead frio. Herdado do original (decisão pode ter sido consciente — justificar se mudar).
- [ ] **Heading `#diff-title`** é `<h3>` enquanto as demais seções usam `<h2>` — inconsistência leve de hierarquia semântica. Herdado.

## Nice-to-haves (4)

- [ ] `.speaker-card` é layout vertical/centralizado; GUIDELINES §8 sugere horizontal (foto à esquerda). Funciona bem como está.
- [ ] `.final` (CTA final) usa fundo neutro-claro em vez de gradiente/cor primária (GUIDELINES §8) — a seção Urgência logo antes já cumpre o momento de destaque escuro.
- [ ] `.for-list li::before` (numeração decorativa laranja) ≈2.82:1 contra branco, levemente abaixo do 3:1 pra texto grande — área pequena/decorativa, herdada do original.
- [ ] Sem `&nbsp;` entre hora e código de fuso (ex.: `10:00 MX`) — pode quebrar linha no meio. Sem `spellcheck="false"` no campo de e-mail do form mock.

## Próximos passos

- Formulário mock aprovado? → `/lp-integrar-form buzzmonitor/gestion-de-crisis-ia-latam-septiembre-2026 "<snippet>"`
- Rever mais algum ponto (ordem de seções, posição do form, H1)? → decidir com o time e editar antes de publicar
- Publicar → `/lp-publicar buzzmonitor gestion-de-crisis-ia-latam-septiembre-2026 webinar.buzzmonitor.com`
