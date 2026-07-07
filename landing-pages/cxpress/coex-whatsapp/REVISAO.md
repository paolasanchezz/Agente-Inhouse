# Revisao LP — cxpress/coex-whatsapp

**Data:** 2026-06-10
**Auditores:** frontend-design (review mode) + checklist tecnico lp-gerar (SEO/GTM/fidelidade ja validados na geracao)

## Aplicado automaticamente (2 criticos)

- [x] Contraste WCAG AA do numero das stats — `.stat__num` laranja #EF863C sobre branco dava ~2.6:1 (minimo 3:1 para texto grande). Trocado para `--primary-dark`; o destaque laranja permanece no `border-top` do card e nos asteriscos (brandbook atendido sem violar AA).
- [x] Contraste WCAG AA do overline do hero — `.hero__overline` #4A69BD 14px sobre #D7E2FF dava ~4.0:1 (minimo 4.5:1). Trocado para `--primary-dark` (~10:1).

## Melhorias opcionais (6)

Para o usuario decidir. Aplicar via Edit manual ou pedir `/lp-revisar` novamente.

- [ ] Padding vertical duplicado no hero — a regra generica `section{padding:130px 0}` soma com o padding proprio do `.hero__inner` (110/130px), dando ~240px no topo. Fix: `.hero{padding:0}`.
- [ ] Regra morta `noscript ~ * .hero__content > *{opacity:1}` — desnecessaria (animacao do hero e CSS puro, roda sem JS) e neutraliza o fade-in por especificidade. Fix: remover a regra.
- [ ] `<ul class="prova__grid">` com `style="list-style:none"` inline — mover para o CSS e adicionar `role="list"` (VoiceOver perde semantica de lista sem isso).
- [ ] GIFs sem alternativa para `prefers-reduced-motion` (WCAG 2.2.2, movimento continuo >5s) — envolver em `<picture>` com `<source media="(prefers-reduced-motion: reduce)">` apontando para frame estatico PNG.
- [ ] `backdrop-filter` sem `-webkit-` no `.navbar` (Safari) — degradacao aceitavel (fundo 94% opaco), prefixo custa 1 linha.
- [ ] Links institucionais do footer como texto puro — converter em `<a>` quando o time passar as URLs de Condicoes de Uso e Privacidade (pendencia tambem no README).

## Nice-to-haves (4)

Estilistico. Ignorar e aceitavel.

- [ ] Peso 600 da Source Sans 3 carregado e nao usado — remover do link do Google Fonts.
- [ ] `<title>` com 69 chars pode truncar na SERP — "Atendimento no WhatsApp sem trocar de número | Cxpress" encurta sem perder a promessa.
- [ ] `<link rel="preload">` para `mockup-plataforma-laptop.png` (unica imagem above-the-fold) — ganho marginal de LCP.
- [ ] JSON-LD `logo` assume path guarda-chuva (`assets/cxpress/logos/...`) — correto para content.cxpress.io; revisitar so se publicar em modo solo.

## Validado sem achados

- Secoes-tipo conforme GUIDELINES §8 (beneficios grid 3, FECHO unica dark, form ultima secao MOFU §10)
- Fidelidade da copy: zero texto inventado, frase-ancora integra, em-dash 0 (HTML e copy.txt)
- GTM GTM-T4XDWHL3 nos 2 blocos (regiao brasil)
- SEO: description 1, og 10, twitter 4, JSON-LD parseia, canonical 1 (placeholders {{DOMAIN}}/{{OG_IMAGE_PATH}} para o lp-publicar)
- Logos sem `href="/"`, SVGs sem `<text>` vivo (§19), favicon unico PNG do brand
- Mobile: headline antes do visual, 1 coluna, zero overflow horizontal
- OG image: PENDENTE de geracao (ver README — gerar antes de publicar)

## Proximos passos

- Design aprovado? -> /lp-integrar-form cxpress/coex-whatsapp "{snippet}"
- Rever mais algum critico? -> editar e rodar /lp-revisar novamente
