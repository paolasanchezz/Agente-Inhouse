# Revisao LP — cxpress/gestao-canais-ia-2026

**Data:** 2026-07-10
**Auditores:** frontend-design (review mode) + web-design-guidelines
**Contexto:** re-revisao de LP em producao (content.cxpress.io). Backport de 2 fixes de acessibilidade
validados no clone `cafe-bogota-jul26` + auditoria completa. As duas LPs compartilham o mesmo bloco
`<style>` — os itens deferidos abaixo valem para AS DUAS (o clone nao esta neste branch).
(Revisao anterior de build em 2026-06-12 preservada no historico git.)

## Aplicado automaticamente (3 criticos)

- [x] **Contraste do hero eyebrow** — `.hero .eyebrow` (linha 156) — adicionado `color:var(--navy)` sobre
  `background:var(--lilac-soft)`. Era royal `#4A69BD` herdado do `.eyebrow` base sobre lilas `#D7E2FF` ≈ 4.0:1
  (reprova AA). Agora navy `#232960` sobre lilas ≈ **10.4:1** ✓. (fix pedido)
- [x] **Countdown inundava screen readers** — `#countdown` (linha 429) — `aria-live="polite"` trocado por
  `aria-hidden="true"`. O contador muda a cada segundo (violava WCAG 2.2.2 no eixo SR); a data ja esta no hero
  e no JSON-LD. ✓ (fix pedido)
- [x] **Contraste do `.signup-sub`** — `.signup-sub` (linha 288) — `color:rgba(255,255,255,.86)` trocado por
  `#fff`. Sobre o inicio (royal) do gradiente do signup era ≈ 4.3:1 (reprova AA para 19px normal); solido
  branco ≈ **5.2:1** ✓. Mesma classe do fix do eyebrow + do guardrail novo em GUIDELINES §7. (aprovado neste ciclo)

## Melhorias opcionais (deferidas — valem para as DUAS LPs)

Para o usuario decidir. Aplicar via Edit manual ou pedir `/lp-revisar` novamente.

- [ ] **Countdown vs WCAG 2.2.2 (eixo visual)** — o `setInterval(tick,1000)` (linhas 604–632) atualiza os numeros
  a cada segundo indefinidamente sem pausa/stop, e o bloco `prefers-reduced-motion` (328–332) NAO desliga o
  countdown — usuario com reduced-motion ainda ve os numeros piscando. `aria-hidden` ja cobre o eixo SR. Fix:
  gatear o interval em `matchMedia('(prefers-reduced-motion: reduce)')` e renderizar estatico ("faltam X dias").
  Nota: os dois auditores discordaram se isto e violacao real de 2.2.2 (o design-review considerou compliant
  por causa do aria-hidden; o a11y-review sustentou que o eixo visual permanece). Decisao do usuario: manter por ora.
- [ ] **`.reach-addr .a2` (linha 196 / markup 426)** — `rgba(255,255,255,.82)` 16px ≈ 4.1:1 no extremo royal do
  gradiente 135° (passa ≈ 6.9:1 na regiao mid/navy onde provavelmente fica). Mesmo fix de 1 valor: solido branco.
- [ ] **Form gateado atras do reveal** — `.jotform-embed.reveal` (linha 395) comeca `opacity:0`. Elemento de
  conversao principal nao deveria depender de scroll-reveal. Fix: tirar `reveal` do wrapper do form (animar so
  ribbon/subtitulo acima). Ha fallbacks (`<noscript>`, reduced-motion, no-IntersectionObserver), entao nao e break.
- [ ] **Sem CTA final antes do footer** (§6) — ultima secao de conteudo e "Sobre a Cxpress" (576–590). Quem le
  ate o fim nao tem botao pra inscrever sem rolar de volta. Fix: banda de CTA de fechamento (botao → `#inscricao`)
  depois do About. Idealmente pareada com o bloco de logistica (abaixo).
- [ ] **Logistica cedo demais na narrativa** (§6/§8) — "Como chegar" (mapa+endereco+countdown, secao 412) esta no
  §4, antes de beneficios/agenda/palestrantes. Considerar mover pra perto do footer, junto do CTA final (leva a
  urgencia/countdown pro lugar certo).
- [ ] **Nome acessivel redundante nos logos** — nav (350–352) e footer (596–598): `<a aria-label="Cxpress: pagina
  inicial">` + `<img alt="Cxpress">` → SR anuncia "Cxpress" duas vezes. §17 usa `alt=""` no img quando o link ja
  tem aria-label. Fix: `alt=""` nos dois imgs de logo.
- [ ] **Embed Jotform via `jsform` (document.write)** — linha 396. Chrome pode intervir em scripts document.write
  cross-origin em conexao lenta. O wrapper canonico `.jotform-embed iframe` (336–337) ja antecipa iframe. Preferir
  o metodo iframe.
- [ ] **`scroll-margin-top` nos ancoras sob a nav sticky** — nav e `position:sticky;height:72px`; alvos `#main`
  (360), `#inscricao` (391), `#como-chegar` (412) sem `scroll-margin-top` → heading fica sob o header ao rolar.
  Fix: `scroll-margin-top:88px` nesses alvos.
- [ ] **Alvo do skip-link nao focavel** — `<main id="main">` (360) sem `tabindex="-1"` → movimento de foco pos
  skip-link (346) e inconsistente em alguns browsers. Add `tabindex="-1"`.
- [ ] **Imagens sem `width`/`height` explicitos (CLS)** — logo nav (351), logos de empresa dos palestrantes
  (537/545/553/561/569), logo footer (597). Fotos dos palestrantes e faixa de clientes ja tem.
- [ ] **`theme-color` divergente** — `<meta name="theme-color" content="#232960">` (19) e navy, mas o fundo da
  pagina e branco.
- [ ] **JSON-LD `Organization` sem `sameAs`** (linha 43) — §15 recomenda LinkedIn/Instagram em `sameAs` pra rich
  results. `Organization.url` (home.cxpress.io) confere com o manifest.
- [ ] **CSS morto** — `.btn-orange` (126–127), `.spk-badge` (260–264), `.spk-photo.placeholder` (258–259),
  `.spk-logo .tbd` (270) e todo o CSS do form hand-built (`.form`/`.field`, 300–316, o form real e embed Jotform)
  nao sao referenciados no markup. Remover pra manter o stylesheet honesto.

## Nice-to-haves

Estilistico. Ignorar e aceitavel.

- [ ] `loading="lazy"` nas imagens abaixo da dobra (fotos/logos dos palestrantes, faixa de clientes 586).
- [ ] `text-wrap:balance` no h1 (157) e h2s de secao (107) pra evitar viuvas.
- [ ] `.nav-dot` anima `box-shadow` (144–145) — nao compositor-friendly; preferir `transform`/`opacity`. Ja
  desligado sob reduced-motion.
- [ ] `preconnect` pra `https://form.jotform.com` e `https://www.googletagmanager.com` (so Google Fonts tem, 50–51).
- [ ] Ribbon heading (294–299 / markup 393) depende de `background-clip:text` + `-webkit-text-fill-color:transparent`;
  add `color` solido de fallback pro titulo nao sumir onde clip-text nao e suportado.
- [ ] Hero repete a propria info (§3) — eyebrow (365), hero-pill (368–383) e nav-meta (354) restatem formato/data/local.
- [ ] H1 (366) lidera com o titulo do evento, nao com a dor (sugestao de copy pro dono da copy, nao reescrever).
- [ ] Benefits: 5 cards em grid `auto-fit` 3-col (210) → linha de baixo com 2 cards estica mais largo. Centralizar
  a linha orfa ou fixar 3-col com resto centralizado.
- [ ] `.cb-lab` (204) `rgba(255,255,255,.72)` 11.5px cai a ~2.6:1 sobre a regiao royal da barra (a barra e
  `aria-hidden`, entao so afeta baixa-visao sighted). Subir pra ~0.85.
- [ ] Typography: `&nbsp;` em "Av. Paulista, 807" / "9h as 12h" / "Sao Paulo - SP"; considerar en dash (–) no lugar
  de hifen em "807 - 17o andar" / "Sao Paulo - SP".
- [ ] Safe-area insets (`env(safe-area-inset-*)`) na nav sticky full-bleed e secoes full-width pra devices com notch.

## Checks que passaram (sem acao)

- GTM: regiao=brasil, `GTM-T4XDWHL3` no `<head>` + `<noscript>`, confere com `tracking.json` regions.brasil.
- Copy fidelity: 0 em-dashes; HTML bate com `copy.txt` secao a secao; sem pull-quote/kicker/punchline inventado.
- SEO: description(1), robots(1), og:(10 ≥8), twitter:(4), JSON-LD(1, parseia: Organization+WebPage+Event), canonical(1).
- Logo SVGs (`logo-primary.svg`, `logo-reversed.svg`) sem `<text>` vivo (sem risco de serifa no browser).
- hreflang: LP unica (sem irmas `-es`/`-pt`) → nao exige hreflang de irma.
- Positivos: 1 unico `<h1>`, hierarquia h1→h2→h3 limpa, header/main/footer/section semanticos, skip-link,
  `:focus-visible` global, todo `<img>` com `alt`, SVGs decorativos `aria-hidden`, iframe do mapa com `title`,
  viewport sem travar zoom, `<noscript>` fallback do reveal.

## Notas de verificacao pos-deploy

- OG image `content.cxpress.io/assets/cxpress/og-gestao-canais-ia-2026.png` vive no namespace guarda-chuva (fora do
  repo) — confirmar HTTP 200 pos-deploy. Mesmo pro PNG do `logo` no JSON-LD (linha 43). URL/dimensoes (1200×630) OK.
- CSP do mapa: garantir `frame-src https://www.google.com` no `vercel.json` do guarda-chuva (o `lp-publicar` detecta
  drift de CSP; se faltar, patch cirurgico). Herdado da revisao de build 2026-06-12.

## Proximos passos

- Publicar (escopo aprovado: 3 criticos aplicados) → `/lp-publicar cxpress gestao-canais-ia-2026 content.cxpress.io`
- Aplicar os deferidos nas DUAS LPs (esta + cafe-bogota-jul26) num ciclo dedicado → editar e rodar `/lp-revisar` de novo
