# Revisao LP — cxpress/coex-whatsapp

**Data:** 2026-06-10 (geracao) · **Reconciliado:** 2026-06-25 (pos-redesign, PR #28)
**Auditores:** frontend-design (review mode) + checklist tecnico lp-gerar (na geracao original)

> Esta LP passou por um redesign manual depois da revisao original (CLIENTES na 2a dobra, FORM em
> card com preco + requisito, secao QUEM SOMOS, troca das stats para o relatorio Sentinela, remocao
> do bloco COEX, novo Jotform). As secoes novas **ainda nao passaram por um `/lp-revisar` completo** —
> recomendado rodar `/lp-revisar cxpress/coex-whatsapp` (e nas outras 3 LPs da campanha) antes de publicar.

## Aplicado na revisao original (2 criticos)

- [x] Contraste WCAG AA do numero das stats — `.stat__num` laranja #EF863C sobre branco dava ~2.6:1 (minimo 3:1 para texto grande). Trocado para `--primary-dark`; destaque laranja permanece no `border-top` do card e nos asteriscos.
- [x] Contraste WCAG AA do overline do hero — `.hero__overline` #4A69BD 14px sobre #D7E2FF dava ~4.0:1 (minimo 4.5:1). Trocado para `--primary-dark` (~10:1).

## Pendentes de decisao (Victor — ver review PR #28)

- [ ] **Stats do relatorio Sentinela (2025)** — `+220%`, `15x`, `-60%`, `98%` sao claims fortes em LP publica de anuncio, atribuidas a relatorio interno. Validar se os numeros estao aprovados e sao citaveis. As mesmas 4 stats se repetem nas 4 LPs da campanha.
- [ ] **Selo "Api Oficial do ChatGPT"** (secao QUEM SOMOS) — consumir a API da OpenAI nao confere status "oficial" como o BSP do WhatsApp. Validar a redacao/claim e corrigir capitalizacao `Api` -> `API`.

## Melhorias opcionais (do audit original, ainda abertas)

- [ ] Padding vertical duplicado no hero — `section{padding:130px 0}` soma com o padding do `.hero__inner`. Fix: `.hero{padding:0}`.
- [ ] Regra morta `noscript ~ * .hero__content > *{opacity:1}` — remover.
- [ ] `<ul class="prova__grid">` com `style="list-style:none"` inline — mover para o CSS e adicionar `role="list"`.
- [ ] GIFs sem alternativa para `prefers-reduced-motion` (WCAG 2.2.2) — envolver em `<picture>` com frame estatico. (3 GIFs de plataforma, ~5,2 MB no total.)
- [ ] `backdrop-filter` sem `-webkit-` no `.navbar` (Safari).
- [ ] Links institucionais do footer como texto puro — converter em `<a>` quando o time passar as URLs.

## Nice-to-haves

- [ ] Peso 600 da Source Sans 3 carregado e nao usado — remover do link do Google Fonts.
- [ ] `<title>` com 69 chars pode truncar na SERP.
- [ ] `<link rel="preload">` para a imagem above-the-fold do hero — ganho marginal de LCP.

## Validado (estado atual)

- Estrutura MOFU conforme GUIDELINES; FECHO unica dark.
- GTM GTM-T4XDWHL3 nos 2 blocos (regiao brasil).
- SEO: description 1, og 10, twitter 4, JSON-LD parseia, canonical 1. URLs SEO usam placeholder `{{DOMAIN}}` (resolvido pelo lp-publicar). `og:image` aponta para `assets/cxpress/og-coex-whatsapp.png` (caminho ja no formato guarda-chuva — bate com o que o lp-publicar gera a partir de `assets/og-image.png`).
- OG image: **gerada** (`assets/og-image.png`, ~53 KB) — corrige o "PENDENTE" da revisao original.
- Favicon unico PNG do brand; SVGs de logo sem `<text>` vivo.
- Mobile: headline antes do visual, 1 coluna.

## Proximos passos

- Rodar `/lp-revisar` nas 4 LPs (secoes novas sem audit completo).
- Publicar via `/lp-publicar cxpress {slug} content.cxpress.io` (uma LP por deploy — nunca deploy manual).
