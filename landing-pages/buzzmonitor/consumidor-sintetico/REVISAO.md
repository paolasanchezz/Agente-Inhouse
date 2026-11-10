# Revisao LP — buzzmonitor/consumidor-sintetico

**Data:** 2026-11-10
**Auditores:** design review (filtro GUIDELINES.md) + web-design-guidelines (acessibilidade e HTML), mais checagens deterministicas (GTM, SEO, fidelidade da copy, OG, logo)

## Checagens deterministicas (todas OK)

- GTM `GTM-WFJVK858` bate com a regiao brasil (selo `.tracking.lock` gravado)
- SEO: description 1, robots 1, og 10, twitter 4, JSON-LD 1 (parseia), canonical 1; LP sem irmas, so `x-default`
- Fidelidade da copy: 152 textos, todos literais da copy.txt exceto whitelist (skip-link, numeracao 04/05)
- Em-dash: 0
- OG `og-consumidor-sintetico.png` 1200x630, sem `og-image.png` duplicado
- Logo do header/footer (`logo-reversed.svg`) sem `<text>` vivo, link para `https://buzzmonitor.com/` com `target="_blank"`

## Aplicado automaticamente (5 criticos)

- [x] Regra canonica `.jotform-embed iframe` estava dentro do `<noscript>` (so valia sem JS) — movida para o `<style>` principal
- [x] Texto da faixa de itens (`.ticker li`) com contraste ~2:1 — trocado para `--muted #837B87` (texto grande, ~3,4:1)
- [x] Faixa animada sem como pausar por teclado/toque (WCAG 2.2.2) — botao pausar/retomar com `aria-pressed`; esfumado das bordas isolado em `.ticker__mask` para o botao nao sumir
- [x] Formulario apertado no celular (iframe com 271px em 375) — padding do `.final__box` reduzido no mobile; iframe agora com 311px
- [x] Nome acessivel do iframe era o nome interno da campanha no Jotform ("BR | MKT | Página Remarketing- [CTA Solicite uma demonstração]") — JS define `title="Formulário: agendar demonstração"`

## A confirmar com o time

- [ ] O form 252995108251662 se chama "Página Remarketing" no Jotform. Confirmar que reaproveitar esse form nesta LP e intencional para a atribuicao de leads.

## Melhorias opcionais (8)

- [ ] Anel de foco laranja (`:focus-visible`) tem ~2,5:1 sobre o creme — usar `--ink`/`--roxo` nas areas claras e manter laranja so nos blocos escuros
- [ ] `.who__row h3` fica com 21px no celular — subir o minimo do clamp para 22px
- [ ] Cinco secoes seguidas de cards (Modulos, Resultados, Para quem, Prova, Plataforma) — dar a uma delas um layout sem card ou devolver o respiro de topo
- [ ] Ordem narrativa (GUIDELINES §6): Plataforma ficou entre a Prova e o CTA final (pedido da Thamires) — alternativa e deixar a Prova colada no CTA
- [ ] `<blockquote>` usado em textos que nao sao citacao (frase do card escuro e case Maracugina) — trocar por `<div>`/`<figure>` ou atribuir a citacao com `<cite>`
- [ ] Efeito de levantar no hover dos cards "Para quem" sugere clique — remover ou limitar a `hover:hover` + sem reduced-motion
- [ ] H1 e mosaico comecam invisiveis ate o JS rodar (`.reveal`) — atrasa o LCP; tirar o `.reveal` do H1/mosaico ou animar so o `transform`
- [ ] "Para quem" usa `<div>` em vez de lista (`<ul>`/`<li>`) como os outros grupos

## Nice-to-haves (9)

- [ ] Mosaico com `role="img"` contendo `<figure>`/`<figcaption>` — usar `<div>`/`<span>`
- [ ] Numeros "01/02/03" dentro do `<h3>` de uma `<ol>` sao lidos duas vezes — `aria-hidden` no `.step__n`
- [ ] `role="region"` na faixa decorativa cria um landmark desnecessario
- [ ] Links do logo abrem nova aba sem avisar — "(abre em nova aba)" no `aria-label`
- [ ] Texto dos cards de dado (`.stat p`) em 14px — 15-16px leria melhor sobre a foto
- [ ] `text-wrap:balance` faltando em `.dif__lead`, `.plat__stat p`, `.sol__kicker`, `.sol__quote p`, `.plat__body`
- [ ] CSS morto do form mock (`.form`, `.field`, `.form__legal`...), `.overline--light` e `--rosa`
- [ ] Icone do `.plat__stat` (abaixo da dobra) sem `loading="lazy"`
- [ ] Prioridade das fotos do hero: `fetchpriority="high"` nas 1-2 primeiras e `decoding="async"` nas demais

## Proximos passos

- Republicar com os criticos: `/lp-publicar buzzmonitor consumidor-sintetico content.buzzmonitor.com`
- Aplicar melhorias escolhidas: editar e rodar `/lp-revisar buzzmonitor/consumidor-sintetico` de novo
