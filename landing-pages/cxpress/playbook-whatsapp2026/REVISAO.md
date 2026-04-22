# Revisao LP — cxpress/playbook-whatsapp2026

**Data:** 2026-04-21
**Auditores:** frontend-design (review mode) + web-design-guidelines

## Aplicado automaticamente (4 criticos)

- [x] `.hero h1 .mark::after` com `z-index: -1` sem stacking context garantido — adicionado `isolation: isolate` em `.hero h1` (linha 265) para prevenir que o realce amarelado desapareca em alguns browsers
- [x] `.header-cta` `transition: all` — substituido por `transition: background, color` (linha 145)
- [x] `.btn` `transition: all` — substituido por `transition: background, color, transform, box-shadow` (linha 166)
- [x] `.form-field input` `transition: all` — substituido por `transition: background, border-color, box-shadow` (linha 824)

## Melhorias opcionais (9)

Para o usuario decidir. Aplicar via Edit manual ou pedir `/lp-revisar` novamente.

- [ ] **`.audience-inner` layout 2-col vazio** — coluna esquerda so tem o section-label, gap morto em desktop. Consolidar em coluna unica: label no topo, lista abaixo full-width com max-width ~720px. (`src:664-671`)
- [ ] **3 momentos escuros na LP** — `.pbook` gradient + `.changes-closing` primaryDark + `.cta-final` primaryDark. GUIDELINES §1 prescreve UMA secao escura. Atenuar `.changes-closing`: usar fundo primary-lighter com borda primary e texto primaryDark.
- [ ] **`.cover-card` sem sombra default** — card branco em fundo primary-lighter tem pouca separacao visual. Adicionar `box-shadow: var(--shadow-sm)` no state padrao. (`src:610`)
- [ ] **`aria-label` redundante no header logo** — anchor tem `aria-label="Cxpress — topo"` + img com `alt="Cxpress"`. O aria-label sobrescreve o alt. Manter so o alt e remover o aria-label. (`src:938`)
- [ ] **Pulse animation infinita** — dot do kicker pulsa para sempre, pode cansar. Limitar a 5 ciclos via `animation-iteration-count: 5` ou reduzir intensidade (opacity .6→.9). (`src:251-256`)
- [ ] **Placeholder contraste borderline** — `rgba(255,255,255,.38)` sobre input translucido no dark bg = ~3:1, borderline AA. Subir para `.52`. (`src:826`)
- [ ] **Input `:focus` → `:focus-visible`** — trocar seletor para nao mostrar ring em cliques de mouse. (`src:831`)
- [ ] **Placeholders sem `…`** — "Seu nome" e "Nome da sua empresa" devem terminar com ellipsis (convencao Vercel). E-mail ja mostra padrao. (`src:1147, 1155`)
- [ ] **Form submit sem `aria-live`** — `onsubmit` muta texto do botao sem elemento de status para screen reader. Adicionar `<div role="status" aria-live="polite">` dedicado. (`src:1144`)

## Nice-to-haves (8)

Estilistico. Ignorar e aceitavel.

- [ ] Trocar logo-icon.png (circulo ja existe) por `samir-sticker.png` na secao "Quem Preparou" — evita circle-in-circle
- [ ] Substituir emoji `📄` do kicker por icone SVG inline (render consistente cross-platform)
- [ ] Adicionar `<meta name="theme-color">` (`#ffffff` + `#232960` dark)
- [ ] Adicionar `<meta property="og:image">` 1200x630 para preview social
- [ ] Usar `&nbsp;` em "PDF gratuito" / "6 seções" (prevenir quebras feias)
- [ ] Aumentar `.cover-card::before` barra accent de 2px para 3px ou full-width
- [ ] CTA accent em `.changes-closing` pode competir visualmente — alternativa outline com borda accent
- [ ] Adicionar indicador `↗` no link externo `home.cxpress.io` no footer

## Proximos passos

- Design aprovado? -> `/lp-integrar-form cxpress/playbook-whatsapp2026 "{snippet}"` (ou pular e publicar com mock)
- Publicar: `/lp-publicar cxpress playbook-whatsapp2026 [dominio-opcional]`
- Rever mais algum critico? -> editar e rodar `/lp-revisar cxpress/playbook-whatsapp2026` novamente
