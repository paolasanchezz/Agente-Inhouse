# Revisao LP — cxpress/assistentedeatencionalcliente

**Data:** 2026-09-02
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel Web Interface Guidelines) + auditoria propria de GTM/SEO/fidelidade de copy

## Aplicado automaticamente (5 criticos)

- [x] **Contraste AA insuficiente** — `.quiz-progress__label` (linha ~174) usava `color:var(--primary)` (#4A69BD) sobre `background:var(--primary-lighter)` (#D7E2FF), contraste ≈3.9:1 — reprova AA para texto pequeno (4.5:1). Exatamente o par de cores que GUIDELINES §7 ja documenta como falha conhecida. Corrigido para `var(--primary-dark)` (#232960), ≈10:1.
- [x] **Hierarquia de headings quebrada** — o `<h3>` do resultado do quiz vinha logo apos o `<h1>` do hero, sem nenhum `<h2>` no meio (pulo de nivel, viola a regra de estrutura hierarquica h1-h6). Promovido para `<h2>`, no mesmo nivel dos outros titulos de secao ("Clientes que confían...", "Resultados de quienes...").
- [x] **3 imagens sem `width`/`height`** — `samir-laptop.png` (hero), `clientes-cxpress.png` (prueba social) e `logo-reversed.svg` (footer) nao tinham dimensoes intrinsecas declaradas — causa CLS (Cumulative Layout Shift) e viola GUIDELINES §14 (que ja assume esses atributos existirem). Adicionadas as dimensoes reais: 1536×1024, 1886×906 e 150×34 respectivamente.
- [x] **Logo do header levemente distorcido** — `logo-primary.svg` tinha `width="160" height="40"` (proporcao 4.0:1) mas o SVG real e 1366:310.5 (proporcao 4.4:1) — como o CSS usa `height:40px;width:auto`, o `width` HTML define a caixa e o logo achatava ~9%. Brandbook proibe logo distorcido. Corrigido para `width="176" height="40"`.

## Melhorias opcionais (5)

Para o usuario decidir. Aplicar via Edit manual ou pedir `/lp-revisar` novamente.

- [ ] Secao "Clientes" (`.clientes{padding:96px 0}`) esta abaixo do respiro minimo recomendado (GUIDELINES §2: min 120px desktop) — considerar subir para 120px+.
- [ ] `aria-live="polite"` esta no `.quiz__card` inteiro — a cada troca de passo, leitor de tela re-anuncia todo o conteudo do novo passo (incluindo as 3 opcoes). Funciona, mas e verboso; poderia escopar so pro texto da legend/heading do passo ativo.
- [ ] Sem `text-wrap: balance` nos headings (`h1`/`h2`) — preveniria linhas orfas em telas estreitas, puramente tipografico.
- [ ] Imagem do Samir no hero (acima da dobra) sem `fetchpriority="high"` — ajudaria LCP marginalmente.
- [ ] `.btn-primary:hover` anima `box-shadow` junto com `transform` — `box-shadow` nao e compositor-friendly (GPU); impacto desprezivel num unico botao, mas via de regra as guidelines da Vercel recomendam so `transform`/`opacity`.

## Nice-to-haves (2)

Estilistico. Ignorar e aceitavel.

- [ ] Links de logo (header/footer) sem estado de hover proprio (ex: leve opacidade) — reforçaria affordance de clique.
- [ ] `touch-action: manipulation` nao aplicado nos botoes — reduz delay de double-tap-zoom no mobile, ganho minimo.

## Outras auditorias (sem achados)

- **GTM/regiao** (`check_gtm_region.py`): `status: ok`, container `GTM-WRQ47B9R` bate com LATAM. Stamp `.tracking.lock` gravado.
- **Fidelidade de copy vs `copy.txt`**: nenhum vazamento encontrado — todo texto visivel (h1/h2/h3, legend, opcoes de quiz, CTAs, disclaimer) e literal da copy. Zero em-dash no HTML.
- **SEO obrigatorio** (§15): 1 description, 1 robots, 10 tags `og:`, 4 tags `twitter:`, 1 JSON-LD (parseia OK), 1 canonical. Todos os thresholds batem.
- **Multi-idioma** (§16): nenhuma LP irma com esse slug — `hreflang` omitido corretamente, so `canonical`.
- **Logo regional** (§17): header e footer apontam pra `https://home.cxpress.io` (nao `/`), ambos `target="_blank" rel="noopener"`.
- **Logo web-safe** (§19): `logo-primary.svg` e `logo-reversed.svg` com `<text>` = 0 (nao serifam).
- **OG image** (§18): **pendente** — `assets/og-assistentedeatencionalcliente.png` ainda nao foi gerada (fora do escopo do `lp-gerar`/`lp-revisar`, requer Chrome headless). Ja registrado em `README.md`.

## Proximos passos

- Design aprovado? -> `/lp-integrar-form cxpress/assistentedeatencionalcliente "{snippet}"` (quando o quiz migrar pra Jotform) ou publicar direto com o quiz mock atual
- Gerar OG image 1200×630 antes de publicar (`.claude/skills/lp-gerar/og-template.html` + Chrome headless)
- Rever mais algum critico? -> editar e rodar `/lp-revisar` novamente
