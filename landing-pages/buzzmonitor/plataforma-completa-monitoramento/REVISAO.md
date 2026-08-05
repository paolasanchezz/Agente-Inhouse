# Revisao LP — buzzmonitor/plataforma-completa-monitoramento

**Data:** 2026-07-23
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel Web Interface Guidelines) + auditorias deterministicas (GTM, copy, SEO)

## Aplicado automaticamente (6 criticos)

- [x] **Contraste `.btn-primary`** (linha 131) — texto branco sobre laranja `#EB7C2E` dava ≈2,82:1, abaixo do 4,5:1 exigido pelo WCAG AA. Usado no CTA do header e do hero. Corrigido: cor do texto trocada para `var(--purple)` (≈5,7:1, passa).
- [x] **Contraste `.overline`** (linha ~197) — texto teal `#0E9D9B` sobre o card `purple-light` da seção Prova dava ≈2,54:1. Corrigido: cor trocada para `var(--purple)`.
- [x] **Contraste `.sub-teal`** (seção Destaque-IA) — teal sobre fundo `paper` dava ≈3,05:1 (abaixo de 4,5:1 para texto 17px). Corrigido: cor trocada para `var(--purple)`.
- [x] **Contraste `.btn-outline-teal`** (CTA da seção Destaque-IA) — teal como texto/borda no estado padrão (≈3,05:1) e branco sobre teal no hover (≈3,33:1) falhavam AA. Corrigido: paleta do botão trocada para purple (padrão) / purple preenchido no hover (≈16:1).
- [x] **Contraste `.stat-number`** (seção Prova, 3 números) — técnica de `background-clip:text` com gradiente roxo→laranja deixava a porção laranja do texto em ≈2,15:1 sobre o card `purple-light`, abaixo até do limite de 3:1 pra texto grande. Corrigido: removida a técnica de gradiente-no-texto, cor sólida `var(--purple)`.
- [x] **`.destaque-visual img` sem `min-height:0`** (GUIDELINES §14) — `<img>` dentro de item de grid sem essa regra corre risco do bug documentado do Safari iOS (imagem renderiza em tamanho intrínseco gigante). Corrigido: adicionado `min-height:0` na imagem e `overflow:hidden` no container como defesa em profundidade.

## Melhorias opcionais (7 de 7 aplicadas em 2026-07-23, a pedido do usuário)

- [x] **Grid de benefícios com 5 itens em 3 colunas** (`.benefit-grid`) — trocado `repeat(3,1fr)` por `repeat(auto-fit, minmax(280px, 1fr))`. A última linha (2 cards) agora estica pra preencher a largura em vez de deixar espaço vazio.
- [x] **`text-wrap: balance` nos headings** — adicionado na regra global `h1,h2,h3`.
- [x] **`loading="lazy"` na imagem da seção Destaque-IA** — adicionado (imagem está abaixo da dobra).
- [x] **`<meta name="theme-color" content="#390155">`** — adicionado no `<head>`.
- [x] **Heading da seção Prova** — `<span class="overline">Quem já saiu do manual</span>` promovido pra `<h2 class="overline">`, sem alterar o texto (nenhuma copy nova inventada) nem o visual (a classe já define a aparência).
- [x] **Chips decorativos do hero** — `chip-1` (fundo laranja) tinha texto branco em baixo contraste; cor trocada pra `var(--purple)` (mesmo ajuste usado nos outros críticos de contraste).
- [x] **`scroll-margin-top: 80px`** — adicionado via `section[id]{...}`, cobre todas as seções com âncora (`#problema`, `#solucao`, `#destaque-ia`, `#para-quem`, `#prova`, `#cta-final`).

## Nice-to-haves (3 de 3 aplicados em 2026-07-23, a pedido do usuário)

- [x] Classes `.sub-teal` → `.sub-accent` e `.btn-outline-teal` → `.btn-outline` (renomeadas em todo o HTML/CSS, já que não usam mais teal).
- [x] `.btn-ghost` (CSS morto, não usado em nenhum elemento) removido.
- [x] `preconnect` adicionado para `googletagmanager.com` e `form.jotform.com`.

## Auditorias deterministicas

- **GTM:** `status: ok` — container `GTM-WFJVK858` bate com a região `brasil`. Selo `.tracking.lock` gravado.
- **Fidelidade de copy:** 0 vazamentos. Todo texto visível confere literal com `copy.txt` (incluindo a seção Destaque-IA adicionada via chat). 0 em-dash no HTML.
- **SEO:** `meta description` (1), `robots` (1), `og:` (10, >=8), `twitter:` (4, >=4), JSON-LD (1, parseia e bate com o brand-manifest: `Organization.url` = `https://buzzmonitor.com/`, `sameAs` inclui LinkedIn + Instagram BR), `canonical` (1). Todos OK.
- **Multi-idioma:** LP única (sem irmãs `-es`/`-pt`) — 0 hreflang no HTML está correto, não é erro.
- **Logo regional:** header e footer apontam pra `https://buzzmonitor.com/` (bate com o manifest), `target="_blank" rel="noopener"` presentes, `aria-label` localizado. Logos SVG confirmados sem `<text>` vivo (0 em ambos).
- **OG image:** estava ausente (pendência herdada do `/lp-gerar`). Gerada nesta revisão: `assets/og-plataforma-completa-monitoramento.png` (1200×630, ~47 KB), a partir de `assets/og-source.html` (template com cores da marca + overline e H1 literais do `og:title`/`OVERLINE` já aprovados). Renderizada via Chrome headless.

## Proximos passos

- Design aprovado? Formulário já está integrado (Jotform, ver README).
- Rever mais algum ponto? Editar e rodar `/lp-revisar` novamente.
- Publicar: `/lp-publicar buzzmonitor plataforma-completa-monitoramento [dominio]`
