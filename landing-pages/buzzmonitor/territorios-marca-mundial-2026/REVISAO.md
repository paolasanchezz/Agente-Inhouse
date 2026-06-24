# Revisao LP — buzzmonitor/territorios-marca-mundial-2026

**Data:** 2026-06-24
**Auditores:** frontend-design (review mode) + web-design-guidelines
**Contexto da alteracao:** pedido da diretora — acrescentar "Festivais de Verao" ao tema e colocar imagem (estilo split estadio/festival) no header e na comunicacao.

## Aplicado automaticamente (2 criticos)

- [x] **GTM no container errado** — `<head>` + `<noscript>` — a LP e PT-PT (Portugal) mas tinha `GTM-MKQBX2MG` (container LATAM). Substituido por `GTM-NCFT22CW` (portugal, por `brand/buzzmonitor/tracking.json`). Bug **pre-existente**, nao introduzido por esta alteracao. Validado: 2 ocorrencias NCFT22CW, 0 MKQBX2MG.
- [x] **2 em-dashes** (`—`) em comentarios CSS (`/* HERO — ... */`) introduzidos nesta sessao — violam regra anti-IA tolerancia zero (GUIDELINES §5). Trocados por `-`. Validado: `grep` de em-dash = 0.

## Melhorias opcionais (4) — pre-existentes, fora do escopo do pedido

Para o Victor decidir. Nenhuma bloqueia o deploy.

- [ ] **Countdown orfao (codigo morto)** — bloco JS do countdown (IIFE final) procura `#cd-d/#cd-h/#cd-m/#cd-s/#countdown` que nao existem no DOM; e o CSS `.countdown-*` (sem markup). Inofensivo (guard `if (!elD) return;`), mas e peso morto. Sugestao: remover o IIFE do countdown + regras CSS `.countdown-*`.
- [ ] **Pulse do nav sem reduced-motion** — `.nav-meta .dot::after` (animation `pulse`) nao e desligada no bloco `@media (prefers-reduced-motion: reduce)`, ao contrario das outras animacoes. Fix: `.nav-meta .dot::after { animation: none; }` no bloco reduced-motion.
- [ ] **`role="table"` redundante** na tabela da matriz — HTML nativo ja tem a semantica; remover o ARIA superfluo (manter `aria-label`).
- [ ] **Preconnect ao Jotform** — ha `preconnect` para Google Fonts mas nao para `form.jotform.com` (form above-the-fold). Adicionar `<link rel="preconnect" href="https://form.jotform.com">`.

## Melhorias no hero novo (sugestoes dos auditores) (2)

- [ ] **Selos sobre a foto** — `.hf-tag` (fundo branco .92, sem borda). Risco baixo (ambos os selos caem sobre a multidao escura no canto inferior esquerdo), mas para garantir legibilidade independente da foto: adicionar borda translucida 1px mais marcada ou um leve scrim escuro na base da `.hero-figure`.
- [ ] **Equilibrio das colunas** — coluna de texto (eyebrow+H1+2 subs+CTA+faixa meta) fica mais alta que a imagem landscape; com `align-items: center` pode sobrar respiro acima/abaixo da imagem em telas largas. Opcional: `align-items: start` ou coluna da imagem ligeiramente mais larga.

## Nice-to-haves (estilistico — ignorar e aceitavel)

- [ ] CSS morto volumoso (~250 linhas) de seccoes/elementos removidos em iteracoes anteriores (`.ticket*`, `.punchline*`, `.diff-*`, `.for-visual`/`.ai-*`, `.urgency*`, `.social-proof`/`.mural*`). Nao afeta render; limpar num passe futuro.
- [ ] `.hero-visual::before/::after` (anel pontilhado + blob) foram desenhados para o cartao menor; com a imagem grande, verificar se ainda compoem bem.
- [ ] Estilos inline repetidos (cor do eyebrow, italico do hero-sub) → mover para classes utilitarias.

## Proximos passos

- Design aprovado pelo Victor (escolheu "publicar agora").
- Form ja e Jotform real (embed presente) — nao precisa `/lp-integrar-form`.
- Publicar: `/lp-publicar buzzmonitor territorios-marca-mundial-2026 webinar.buzzmonitor.com`
