# Revisao LP — buzzmonitor/news-da-buzz

**Data:** 2026-07-21
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel), executados manualmente nesta sessão

## Aplicado automaticamente (5 críticos/ajustes)

- [x] Contraste AA: `.eyebrow-sm` ("Prévia real") usava `var(--teal)` (#0E9D9B) sobre fundo branco/neutral-100 = ~3.3:1, abaixo do AA (4.5:1). Trocado para `var(--primary)` (#390155) = alto contraste.
- [x] a11y do skip-link: `<main id="conteudo">` não tinha `tabindex="-1"`, então o foco de teclado não migrava pro conteúdo ao ativar o skip-link (só rolava a tela). Adicionado `tabindex="-1"`.
- [x] Motion: `scroll-behavior: smooth` no `<html>` não respeitava `prefers-reduced-motion`. Adicionado `@media (prefers-reduced-motion: reduce){ html{scroll-behavior:auto} }`.
- [x] Performance: imagem da seção PROVA (abaixo da dobra) sem `loading="lazy"`. Adicionado.
- [x] Formulário: campo de e-mail sem `spellcheck="false"` (guideline Vercel para campos de e-mail). Adicionado.

## Crítico sinalizado, NÃO corrigido automaticamente (decisão de marca)

- [ ] **Contraste do botão CTA laranja:** `.btn-primary` e `.navbar__cta` usam texto branco (`#ffffff`) sobre fundo `var(--secondary)` (#EB7C2E). Contraste calculado: **~2.8:1**, abaixo até do limiar de "texto grande" (3:1), falha AA (4.5:1). Essa combinação vem literalmente do brand `generation-rules.json` (`"ctaButton": "secondary (#EB7C2E laranja) com neutral.0 como texto"`) e provavelmente se repete em outras LPs Buzzmonitor já publicadas — não é um erro introduzido só nesta LP. Não alterei porque mudar a cor do CTA é uma decisão de marca/design system, não uma correção pontual desta página. Opções pro Victor/time de marca decidir: (a) escurecer o laranja do botão especificamente (ex.: usar o tom de hover `#d76d20`, ainda insuficiente sozinho — precisaria mais escuro, ~contraste 4.5 exigiria algo como `#b3550f`); (b) usar texto escuro (`--n-900`) sobre o laranja em vez de branco (dá ~6.2:1, resolve, mas muda a leitura visual do botão); (c) manter como está, assumindo o risco de acessibilidade em toda a linha de LPs que usa esse padrão. Recomendo (b) como fix de menor impacto visual.

## Melhorias opcionais (2)

- [ ] Seções (`<section>`) não têm `aria-labelledby` apontando pro `<h2>` de cada uma — melhoraria a navegação por landmarks em leitores de tela, mas não é bloqueante.
- [ ] Toque: `.navbar__cta` no mobile tem altura de alvo de toque um pouco abaixo dos 44px recomendados (padding 10px 16px + fonte 13px). Considerar aumentar padding vertical no breakpoint mobile.

## Nice-to-haves (1)

- [ ] O tilt 3D estático do `.device` (hero) é desligado em `prefers-reduced-motion: reduce` mesmo não sendo uma animação contínua — inofensivo (ainda fica legível sem o tilt), mas é uma escolha estética, não uma correção.

## Auditorias adicionais (sem achados)

- **GTM:** GTM-WFJVK858 presente no `<head>` e no `<noscript>`, correto pra região `brasil` (fallback, slug sem sufixo). Sem divergência.
- **Fidelidade de copy:** todo texto visível bate literal com `copy.txt`. Exceção documentada (whitelist explícita do pedido): remetente/assunto do mockup de e-mail no hero ("News da Buzz" / "News Buzzmonitor - Chegou a sua atualização semanal!") — texto de interface do mockup, não copy de marketing.
- **Em-dash:** 0 ocorrências de `—` e de `&mdash;` no HTML.
- **SEO:** 1 description, 10 `og:`, 4 `twitter:`, 1 JSON-LD (parseia, 2 nós: Organization + WebPage), 1 canonical. `Organization.url` bate com `brand-manifest.json#regions.brasil.home`. `sameAs` inclui LinkedIn + Instagram BR.
- **Multi-idioma:** LP única (sem irmãs ainda) — hreflang omitido corretamente, canonical presente.
- **Logo regional:** header/footer apontam pra `https://buzzmonitor.com/` (não `"/"`), `target="_blank" rel="noopener"`, `aria-label` presente. Logos `logo-primary.svg`/`logo-reversed.svg` confirmados web-safe (`grep -c '<text'` = 0 nos dois).
- **OG image:** `assets/og-news-da-buzz.png` existe, 1200×630 confirmado.

## Próximos passos

- Decisão de marca pendente: contraste do CTA laranja (ver acima) — pode ser resolvido nesta LP isoladamente ou como ajuste de design system.
- Design aprovado? → definir provedor de formulário e rodar `/lp-integrar-form buzzmonitor/news-da-buzz "<snippet>"`.
- Publicar: `/lp-publicar buzzmonitor news-da-buzz material.buzzmonitor.com` (guarda-chuva, deploy via CI).
