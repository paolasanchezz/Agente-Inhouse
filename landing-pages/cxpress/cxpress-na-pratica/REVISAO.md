# Revisão LP — cxpress/cxpress-na-pratica

**Data:** 2026-09-02
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel Web Interface Guidelines) + gates determinísticos (`check_gtm_region.py`, fidelidade de copy, contraste WCAG, medição no navegador a 1440px e 390px)

## Aplicado automaticamente (2 críticos)

- [x] **Contraste da borda dos campos reprovava WCAG AA (SC 1.4.11 Non-text Contrast).**
      `.field input, .field select` usavam `--line: #d1d1d1`, que dá **1,53:1** sobre branco.
      A borda é o único elemento que identifica o controle, então o mínimo é **3:1**.
      Corrigido com um token dedicado `--field-line: #8689a8` (navy da marca a 55% sobre branco,
      **3,41:1**). O `--line` continua nas 7 bordas decorativas (cards, divisores, pílula "Ainda
      não é a hora se"), que são estruturais e não exigem 3:1 — trocar globalmente deixaria os
      cards pesados.

- [x] **Âncora `#form` sem `scroll-margin-top` sob header sticky.**
      O header mede **73px** no desktop e **63px** no mobile. Todo clique nos CTAs (o do header e o
      do fecho) rolava até `#form` e escondia os 73px do topo do formulário, ou seja, o título
      "Fale com um especialista" e parte do lead sumiam atrás do header. É a rota principal de
      conversão da página. Corrigido com `scroll-margin-top: 92px` em `.hero__aside`
      (73px do header + 19px de respiro).

## Verificado e aprovado (sem ação)

| Item | Resultado |
|---|---|
| Fidelidade da copy × `copy.txt` | **0 vazamentos, 0 linhas ausentes** (42 strings visíveis conferidas por diff automatizado) |
| Em-dash / `&mdash;` (anti-IA, tolerância zero) | 0 / 0 |
| GTM × região | `GTM-T4XDWHL3`, 0 bloqueio, selo `.tracking.lock` gravado |
| Pacote SEO (§15) | description 1 · robots 1 · og 10 · twitter 4 · canonical 1 · JSON-LD 1 (parseia, 3 nós) |
| `Organization.url` × brand-manifest | bate (`brand.websites.brasil` = `https://home.cxpress.io`) |
| hreflang (§16) | ausente por decisão correta: LP única, sem irmãs |
| Logo header/footer (§17) | ambos para a home regional, `target="_blank" rel="noopener"` |
| Logo SVG com `<text>` vivo (§19) | 0 nos SVGs usados |
| OG image (§18) | `og-cxpress-na-pratica.png`, 1200×630, nome canônico, sem `og-image.png` órfão |
| Contraste de texto (12 pares medidos) | todos passam; o mais apertado é o botão laranja (navy sobre `#EF863C` = 5,23:1) |
| Seções-tipo (§8) | problema em lista vertical com X vermelho · benefícios em grid de 3 com check verde |
| Contagens da copy (§9) | problema 5 · benefícios 3 · para quem 3+2 · campos 4 |
| Pisos tipográficos mobile (§20) | h1 34 · h2 28 · h3 22 · corpo 17 · botão 17 · label 15 · hint 14 |
| Overflow horizontal a 390px | nenhum (`scrollWidth` = `clientWidth` = 390) |
| Ordem do hero no mobile (§3) | `.hero__content` antes de `.hero__aside`, sem `order` |
| Alvos de toque | inputs 52px · botões 54px (mínimo 44px) |
| Motion | fallback `<noscript>` + `prefers-reduced-motion`; nenhum `transition: all` |
| `<select>` com `background-color` e `color` explícitos | presente (correção de dark mode do Windows) |

### H1 com 37% de desequilíbrio de linha (§21) — medido, é o piso

Testei 4 tetos de fonte (52/48/44/40px) e 4 larguras (13/14/16/17ch) no navegador a 1440px.
O `text-wrap: balance` converge em **3 linhas com 37% em todos os tetos de fonte** (as
proporções não mudam com o tamanho). As alternativas são piores: 16ch dá 4 linhas com 41%,
e 13ch dá 5 linhas com 6% — mas 5 linhas de um H1 de 52px viram um bloco alto demais e
tiram o impacto do hero. As 3 linhas atuais não têm órfã (a linha curta é a do meio, e as
três têm 3+ palavras). **Fica como está**; só muda com mudança de copy do H1.

## Melhorias opcionais (9)

Para você decidir. Nenhuma quebra nada hoje.

- [ ] **`aria-live` para o feedback do formulário** — hoje o form é mock. Quando o embed real
      entrar via `/lp-integrar-form`, mensagens de erro e sucesso precisam de uma região
      `aria-live="polite"`, e o foco deve ir para o primeiro campo com erro no submit.
- [ ] **`spellcheck="false"` no campo de e-mail** — recomendação explícita das Web Interface
      Guidelines (evita o sublinhado vermelho em e-mail corporativo).
- [ ] **`autocomplete` no `<select>` de tamanho de equipe** — os outros 3 campos têm.
- [ ] **`<meta name="theme-color" content="#ffffff">`** — ausente; a barra do navegador mobile
      não acompanha o fundo da página.
- [ ] **`color-scheme: light` no `:root`** — sem isso, Android e Windows em modo escuro podem
      inverter os controles nativos (`<select>`, autofill) e destoar do card branco.
- [ ] **`touch-action: manipulation` nos interativos** — remove o atraso de 300ms do duplo-toque
      em botões e campos.
- [ ] **`env(safe-area-inset-*)` nas seções full-bleed** — CTA final e footer podem encostar no
      notch em iPhone deitado.
- [ ] **CTA final e footer usam o mesmo navy** — separados só por um hairline de 1px a 14% de
      branco. No mobile leem como um bloco navy único. Um tom mais fundo no footer (ou mais
      respiro) separaria melhor.
- [ ] **As listas de "Para quem" não têm nome acessível** — `.pill-label` são `<p>`. Como `<h3>`
      (ou com `aria-labelledby` no `<ul>`), um leitor de tela anunciaria "Faz sentido se" /
      "Ainda não é a hora se" ao entrar em cada lista.

## Nice-to-haves (5)

Estilístico. Ignorar é aceitável.

- [ ] `-webkit-tap-highlight-color` não definido (o padrão cinza do Android aparece no toque)
- [ ] Logos de header e footer sem estado de hover
- [ ] `translate="no"` em nomes de marca (Cxpress, WhatsApp, Instagram) para tradutor automático
- [ ] `fetchpriority="high"` no logo do header (acima da dobra)
- [ ] `.hero__pill--c` (pílula pêssego) continua visível no mobile enquanto `--a` e `--b` somem;
      aparece como uma lasca na borda direita do formulário. Clipada por `overflow:hidden`, não
      causa scroll horizontal.

## Correção de rota durante esta revisão

Registrei preliminarmente dois "vazamentos de copy" no formulário (`FORM TITLE` e `FORM LEAD`)
por leitura manual. O diff automatizado contra `copy.txt` mostrou que **as duas linhas estão na
copy aprovada** — o `copy.txt` já tinha sido atualizado para a estrutura com formulário no hero.
Nenhuma alteração de texto foi mantida. A auditoria de fidelidade fecha em 0 vazamentos.

## Próximos passos

- Integrar o formulário real: `/lp-integrar-form cxpress/cxpress-na-pratica "snippet"` — **hoje a
  LP está no ar sem capturar lead** (`action="#"`).
- Migrar `brand/cxpress/brand-manifest.json` para o formato `regions` (hoje é `brand.websites`).
  Sem isso o JSON-LD segue sem `sameAs`. As LPs irmãs usam
  `https://www.linkedin.com/company/cxpress-io/` e `https://www.instagram.com/cxpress.io/`.
- Medir PageSpeed em pagespeed.web.dev (a API pública devolveu 429 na publicação).
