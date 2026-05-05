# LP Buzzmonitor — Social Listening Mayo 2026 LATAM

**Gerado em:** 2026-04-29
**Copy-fonte:** `copy.txt` (output de /lp-preparar)
**Idioma:** ES-LATAM
**Webinar:** 28 de Mayo de 2026 · 16:00 MX · 17:00 COL/PER · 18:00 CL · 19:00 ARG · Online y En Vivo

## Estrutura

1. Header — logo + indicador "En vivo · 28 May" (dot pulsante)
2. Hero — eyebrow + H1 com destaque tipográfico ("Social Listening" gradiente, "detectar oportunidades"/"anticipar crisis" itálicas) + sub + CTA + linha multi-país
3. Hero ticket card — 28/05 · Jueves · 16:00 MX + Formato/Duración/Inversión
4. Ticker roxo — "Las marcas que escuchan crecen"
5. Problema — 4 dores em lista vertical com X vermelhos + punchline "Sobran datos. Falta lectura." em gradiente rosa→laranja + CTA
6. Diferencial — split: card gradiente "Escuchar es estrategia" + copy "El Social Listening no es solo monitorear..."
7. Beneficios — grid 3+2 (5 itens, layout 3 cima + 2 centralizados embaixo) com checkmarks gradiente + meta "Todo aplicado con ejemplos reales"
8. Speakers — 2 cards placeholder com `[Speaker TBD]` (TODO: trocar antes de publicar)
9. Para Quien — lista numerada 01-05 dos 5 perfis + pull-quote editorial "Si tu marca existe en redes sociales..." + CTA
10. Cierre/Urgencia (dark roxo) — frase âncora "Las marcas que mejor crecen no son las que más hablan… sino las que mejor escuchan" + question
11. CTA final + Form mock — campos: nombre, email, empresa, cargo, país (select com 5 países LATAM)
12. Footer — logo reversed + link buzzmonitor.com + © 2026 + mailto eventos@buzzmonitor.com

## Estado

- [x] HTML gerado
- [x] Revisão (frontend-design + lp-revisar Passo 3.6 fidelidade da copy) — 5 críticos + 4 melhorias aplicados, ver `REVISAO.md`
- [ ] Speakers reais (2 placeholders [Speaker TBD] precisam ser trocados antes de publicar)
- [x] Formulário integrado
- [ ] Publicado — rodar `/lp-publicar buzzmonitor social-listening-mayo-2026-latam webinar.buzzmonitor.com`

**Form provider:** Jotform (`form.jotform.com/jsform/261188302248052`) · integrado em 2026-04-30

## Paleta usada (GUIDELINES §1 — 3 cores fortes)

- **CTA:** Laranja `#EB7C2E` (hover roxo `#390155`)
- **Acento/destaque:** Rosa/vermelho `#DE2451` (X da seção problema, gradiente, eyebrow)
- **Seção dark:** Roxo `#390155` (ticker + urgencia/cierre)
- **Gradiente único:** rosa→laranja `linear-gradient(120deg, #DE2451, #EB7C2E)`
- **Fundos:** alternam apenas entre branco `#FFFFFF` e off-white `#F6F4F2`

## Tipografia

- **Display:** League Spartan (700/900) — todos os H1/H2/H3
- **Subtítulo:** Manrope (300/400/500) — eyebrows, labels, CTAs, body do form
- **Body:** Lato (400/700) — texto corrente

## Tracking

- **GTM:** GTM-MKQBX2MG (resolvido pela cascata §5.1 — sufixo `-latam` no slug → `regions.latam` em `brand/buzzmonitor/tracking.json`)
- Snippets injetados no `<head>` (após viewport, antes de `<title>`) e imediatamente após `<body>`

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-icon.png` — favicon (PNG ~13KB, GUIDELINES §11)
- `../../brand/buzzmonitor/assets/logos/logo-primary.png` — logo header (fundo claro)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.png` — logo footer (fundo escuro)

Sem assets LP-locais. Mascote pontual não foi adicionada — seção "Para Quien" usa pull-quote editorial em vez do mascote (Buzzmonitor não tem mascote brand-fixo per CONTEXT §3.8).

## Form mock

`<form action="#" method="post" onsubmit="event.preventDefault()...">` com 5 campos labeled:
- Nombre completo (text, autocomplete=name)
- Email corporativo (email, autocomplete=email)
- Empresa (text, autocomplete=organization)
- Cargo (text, autocomplete=organization-title)
- País (select com MX, COL, PER, CL, ARG, Otro)

JS handler exibe mensagem de sucesso fake. Trocar por embed real (Jotform/RD/HubSpot) via `/lp-integrar-form` antes de publicar.

## Acessibilidade implementada

- Skip-link "Saltar al contenido" → `#main`
- `<html lang="es">` e `aria-label` em landmarks
- Labels visíveis em todos os inputs do form
- `alt` em todas as imagens não-decorativas, `aria-hidden="true"` em SVGs e decorações
- `prefers-reduced-motion: reduce` desliga reveal-on-scroll, ticker marquee e animações de hover
- `focus-visible` com outline laranja em links/inputs/buttons
- Reveal-on-scroll é progressive enhancement: estado oculto só vale dentro de `@media (prefers-reduced-motion: no-preference)`, então se JS falhar, texto continua visível

## Decisões de copy x design

- **Emoji 👉 da copy** (linha "Todo aplicado con ejemplos reales") foi convertido em meta-text simples sem emoji — o emoji virava decorativo num contexto editorial limpo. Caso queira manter, restaurar manualmente em `index.html` na linha do `learn-meta`.
- **H1 longo** quebrado visualmente com destaques tipográficos (gradiente em "Social Listening", itálicas em "detectar oportunidades" e "anticipar crisis") — a copy permanece literal, apenas com hierarquia visual sobreposta.
- **2 cards de speaker placeholder** em vez de 1 — projeção de que o webinar terá 2+ palestrantes (padrão dos webinars Buzzmonitor anteriores).

## Próximos passos

1. `/lp-revisar buzzmonitor/social-listening-mayo-2026-latam` — auditoria dupla (design + a11y)
2. Substituir [Speaker TBD] pelos speakers reais
3. `/lp-integrar-form buzzmonitor/social-listening-mayo-2026-latam "<snippet-do-provedor>"` — quando layout aprovado
4. `/lp-publicar buzzmonitor social-listening-mayo-2026-latam webinar.buzzmonitor.com` — modo guarda-chuva (anexa ao projeto Vercel `buzzmonitor-lp-monitoramento-concorrentes`)
