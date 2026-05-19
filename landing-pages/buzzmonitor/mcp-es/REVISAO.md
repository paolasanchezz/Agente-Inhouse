# Revisao LP — buzzmonitor/mcp

**Data:** 2026-05-15
**Auditores:** design review (frontend-design em review mode) + web-design-guidelines + checks tecnicos (em-dash, GTM, copy fidelity)
**Contexto:** revisao + redesign solicitada pelo Victor — Hero claro, logos brand padrao analise-preditiva, Secao 2 com icone novo, Mural substituido pela Social proof animada da pocket-events.

---

## Aplicado automaticamente (13 criticos)

### Anti-IA / Copy
- [x] 6 em-dashes (`—` e `&mdash;`) substituidos por `:` e `,` — 4 em comentarios CSS/HTML, 2 em alt texts dos murais. Contagem final: 0 (tolerancia zero respeitada).

### Acessibilidade (WCAG AA)
- [x] **Skip-link** agora aponta para `#main-content` em vez de `#form-section` (linha 948) — usuario de teclado nao perde mais o conteudo principal. Adicionado `<main id="main-content">` envolvendo todo conteudo entre `<nav>` e `<footer>`.
- [x] **`aria-hidden="true"` removido do `.navbar__badge`** (Buzzmonitor MCP e informacao util, nao decoracao).
- [x] **`alt=""` nos `<img>` da logo** (header linha 956, footer linha ~1166) — link pai ja tem `aria-label`. Evita "Buzzmonitor Buzzmonitor link" pra screen reader.
- [x] **`aria-label="Apresentacao"`** no `<section class="hero">` (era "Hero", jargao).
- [x] **`.terminal__cursor` animation `blink`** envolvido em `@media (prefers-reduced-motion: no-preference)`.
- [x] **`.hero-chip--mentions { animation-name }`** movido para dentro de `@media (prefers-reduced-motion: no-preference)`.
- [x] **`scroll-behavior: smooth`** com fallback `auto` para reduced-motion.

### Contraste WCAG AA
- [x] **Nova var `--secondary-aa: #B5571F`** criada para textos pequenos laranja (contraste ~4.7:1 sobre branco vs. `--secondary` original em 3.07:1).
- [x] **`.overline`, `.hero__overline`, `.navbar__badge`** trocadas para `--secondary-aa`. Bordas/backgrounds do badge ajustadas pra harmonizar.
- [x] **`.prompt-card__num`** trocada para `#FFB07A` sobre fundo roxo `var(--primary)` — passa AA. `opacity: .8` removido pra manter contraste.
- [x] **`.terminal__title`** opacity `.35` -> `.65` — contraste WCAG AA sobre fundo `#0F0A1A`.

### Paleta (GUIDELINES §1: max 2-3 cores fortes)
- [x] **Decor dot amarelo do hero (`.hero__decor-dot--yellow`)** trocado para `var(--secondary)` com opacidade reduzida. Paleta ativa: roxo + laranja + teal (3 cores fortes — dentro do limite).

### Layout / KPI overlays
- [x] **KPI overlays do social-proof reposicionados** de `top: 0; left: 0` para `top: -18px; left: -18px` (e equivalentes para tr/bl/br). Agora flutuam parcialmente fora do `.mural-frame` em vez de cobrir os cantos do mural, preservando logos visiveis.

### Mobile (≤980px)
- [x] **Chip flutuante `.hero-chip--sentiment`** mobile reposicionado de `top: -16px; left: -10px` para `top: 8px; left: -8px` — evita colisao com CTA do hero.
- [x] **Chip `.hero-chip--mentions`** mobile reposicionado para `bottom: -12px; right: -8px`.

---

## Melhorias opcionais (5)

Para o Victor decidir. Aplicar via `Edit` manual ou pedir `/lp-revisar` novamente.

- [ ] **`.hero__sub max-width: 500px`** corta texto cedo no desktop. Subir para 560px para o paragrafo respirar.
- [ ] **`.modulo-card__icon` usa emoji** (`🔔 📈 🔍 💬 📊 🗂`). Brand tem `mcp-icon` PNG + logos SVG — para consistencia, considerar SVGs inline com cores da marca. Refactor de medio porte.
- [ ] **`.hero-chip` border** quase invisivel (`rgba(0,0,0,.04)`) — quando reduced-motion ativa e chips param de flutuar, eles "perdem" definicao. Subir para `rgba(57,1,85,.10)`.
- [ ] **`.modulos__grid > article`** semanticamente sao mais "list items" do que articles. Trocar `<article>` por `<li>` dentro de `<ul role="list">` melhora navegacao por leitor de tela.
- [ ] **Jotform iframe sem `title` acessivel** — leitor de tela anuncia "frame" generico. Verificar config do form na Jotform (nao controlavel pelo HTML local).

---

## Nice-to-haves (4)

Estilistico. Ignorar e aceitavel.

- [ ] **Footer logo height 22px** — pequeno demais ao lado de copyright 13px. Subir para 26-28px.
- [ ] **Header logo height 56px** com SVG 168.75x32.25 fica visualmente esticado em altura. Considerar 40-44px.
- [ ] **Padding extra** entre `.exemplos` (fundo branco) e `.form-section` (fundo `--neutral-100`) — divisor visual leve.
- [ ] **`.mural-dots` keyframe `dot-cycle`** transicao 45% -> 50% e abrupta. Suavizar.

---

## Auditorias automaticas (passaram)

- ✅ **GTM ID**: encontrado `GTM-WFJVK858` (Buzzmonitor/Brasil) — bate com expected_gtm_id.
- ✅ **Copy fidelity vs copy.txt**: H1, H2s, body sao literais. Sem pull-quotes inventados. Sem sinonimos cosmeticos.
- ✅ **Em-dash count**: 0 (anti-IA tolerancia zero).
- ✅ **Heading order**: h1 -> h2 -> h2 -> h3×6 -> h2 -> h2 -> h2 (sem pular niveis).
- ✅ **Favicon**: `../../brand/buzzmonitor/assets/logos/logo-icon.png` (PNG 13KB).
- ✅ **Mobile headline-first**: `.hero-content` precede `.hero-visual` no DOM; sem `order: -1`.

---

## Proximos passos

- Design aprovado? -> rodar `/lp-publicar buzzmonitor mcp material.buzzmonitor.com`
- Form ja esta integrado (Jotform `form/jsform/252995108251662`) — sem precisar de `/lp-integrar-form`
- Rever mais algum critico? -> editar e rodar `/lp-revisar buzzmonitor/mcp` de novo

## Notas operacionais

- **Junction Windows** `landing-pages/buzzmonitor/mcp/brand` foi criada temporariamente para resolver path `../../brand/...` no preview local (Python http.server nao segue links externos por padrao). **REMOVER antes do publish** para nao vazar copia do `brand/` no deploy guarda-chuva.
