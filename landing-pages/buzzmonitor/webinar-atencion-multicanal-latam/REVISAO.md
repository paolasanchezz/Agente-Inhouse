# Revisao LP — buzzmonitor/webinar-atencion-multicanal-latam

**Data:** 2026-07-29
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel) + auditoria GTM/copy/SEO (lp-revisar)

## Aplicado automaticamente (2 criticos)

- [x] **GUIDELINES §1 (gradiente como fundo de secao)** — `.banner` (WEBINAR BANNER) usava `background: var(--grad-hot)` cobrindo a secao inteira, com H2 branco por cima. Isso viola a regra explicita "aplicar [gradiente] em 1-2 momentos de alto impacto, nao em fundo de secao" e alem disso deixava o texto branco com contraste marginal (~2.8:1) na ponta laranja do degrade, abaixo de AA. Corrigido: fundo branco, eyebrow em `--c-accent-2`, H2 em `--c-n900` com a palavra "IA" com o mesmo `.grad` text-clip ja usado no hero (reaproveita o unico gradiente da LP em um 3o momento pontual, nao como fundo).
- [x] **GUIDELINES §8 (gramatica da secao "Urgencia")** — a secao `.urgency` (AVISO + CTA FINAL) tinha fundo escuro correto, mas faltava o selo/tag em cor quente rotacionada que a regra exige explicitamente ("Regra: aparece uma vez na LP"). Adicionado `<span class="tag">Aviso</span>` (fundo laranja `--c-accent`, texto escuro para contraste AA, `rotate(-3deg)`) — reaproveita literalmente o nome da propria secao da copy, sem inventar frase nova.

## Melhorias opcionais — aplicadas a pedido do usuario (5/5)

- [x] `.sp-company img` (logo Buzzmonitor nos cards de speaker) agora tem `width="120" height="24"` explicitos — elimina o risco de layout shift.
- [x] Mesmas imagens agora com `loading="lazy"` (estao abaixo do fold).
- [x] `.ai-pulse` (circulo decorativo animado) agora com `aria-hidden="true"`.
- [x] `aria-label` redundante removido do link do Instagram no footer — o texto visivel (`@buzzmonitor.es`) ja e o nome acessivel; o icone SVG ja tinha `aria-hidden="true"`.
- [x] `.ai-core` (circulo "IA") trocou o fundo de `--grad-hot` para `--c-primary` solido — contraste do texto branco sobe de ~2.8:1 para >8:1 (AA/AAA), sem alterar layout ou tamanho.

## Nice-to-haves (2)

Estilistico. Ignorar e aceitavel.

- [ ] O countdown regressivo (contagem ate 27/08 16:00 MX) e um elemento decorativo/funcional que espelha a LP de referencia — nao vem de um bloco de copy.txt, mas tambem nao inventa texto (so exibe numeros derivados da propria data ja informada). Se preferir remover, e so avisar.
- [ ] O card "CASO REAL" usa uma seta unicode (`→`) para representar "de 36h a 3h" — nao e em-dash (tolerancia zero respeitada, contagem = 0), mas e um simbolo que nao esta literal na copy. Risco baixo, mas fica registrado para transparencia.

## Auditorias que passaram sem achados

- **GTM:** `GTM-MKQBX2MG` (regiao latam) presente no `<head>` e no `<noscript>` apos `<body>` — bate com `tracking.json`.
- **Fidelidade de copy:** nenhum vazamento encontrado — todo texto visivel bate literal com `copy.txt` ou pertence a whitelist (ticket boilerplate, nav meta, form labels/disclaimer, footer). Em-dash: 0 ocorrencias.
- **SEO:** 1 description, 10 `og:`, 4 `twitter:`, JSON-LD parseia (tipo `Event`), 1 canonical. `Organization.url` bate com `brand-manifest.json#regions.latam.home`. `sameAs` inclui LinkedIn + Instagram latam.
- **Logo:** header/footer apontam para `regions.latam.home` (nao `"/"`), `target="_blank" rel="noopener"`, `aria-label` localizado em ES. Nenhum SVG de logo com `<text>` vivo (`logo-primary.svg`/`logo-reversed.svg` = raster, grep retornou 0).
- **Multi-idioma:** nenhuma LP irma detectada para este slug — `hreflang` omitido corretamente, mantendo so `canonical`.

## Pendencias ja conhecidas (herdadas do lp-gerar, nao remedidas aqui)

- Fotos reais dos 2 speakers (placeholder de iniciais no lugar).
- OG image (1200x630) ainda nao gerada — `{{OG_IMAGE_PATH}}` e placeholder.
- `{{DOMAIN}}` no bloco SEO e placeholder — `lp-publicar` resolve.

## Proximos passos

- Fotos dos speakers prontas + design aprovado? -> `/lp-integrar-form buzzmonitor/webinar-atencion-multicanal-latam "snippet"`
- Quer que eu aplique alguma das melhorias/nice-to-haves acima? Me avise quais.
