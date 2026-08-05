# Revisão LP — buzzmonitor/indiqueeganhe

**Última revisão:** 2026-08-05
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel Labs)

## Revisão 2026-08-05 — pós-alterações (título hero, subtítulo, linha do stepper, imagem "quem vale a pena", fonte do H2, cor das caixinhas)

**0 críticos novos.** As alterações desta rodada (remoção de "por isso" no H1, troca da 1ª frase do subtítulo, linha única conectando os 4 passos do stepper, imagem `assets/quem-vale-a-pena.png` no lugar das caixinhas antigas, aumento da fonte do H2 "Quem vale a pena indicar?" e caixinhas de segmento em lilás/roxo) não introduziram nenhuma quebra visível, problema de contraste ou vazamento de copy.

Checagens re-executadas após as mudanças:
- **GTM:** `status: ok`, `stamp_match: true` (fingerprint não mudou — mudança de copy/CSS não afeta região/GTM).
- **Fidelidade de copy:** H1 e subtítulo do hero no HTML batem literal com `copy.txt` atualizado. 0 em-dash.
- **SEO:** description=1, robots=1, og=10, twitter=4, JSON-LD=1 (parseia, tipos `Organization`/`WebPage`/`SoftwareApplication` corretos), canonical=1 — inalterados.
- **Logo regional:** sem regressão, hrefs corretos, sem `<text>` vivo nos SVGs.
- **Imagem nova:** `<img>` com `alt` descritivo, `width`/`height` explícitos (1672×941) e `loading="lazy"` (correto — está abaixo da dobra). `alt` não é literal de `copy.txt` (a copy não tinha texto para essa imagem no momento em que foi escrita) — tratado como descrição de acessibilidade necessária, mesmo critério já aplicado ao `title` do vídeo do hero.
- **Contraste das caixinhas de segmento:** fundo `primary-light` `#F2D8FF` + texto `primary` `#390155` ≈ 12:1 — muito acima do mínimo.

## Aplicado em revisões anteriores (2026-07-02, 2 críticos)

- [x] Contraste de ícone falha WCAG 1.4.11 em 2 dos 4 persona-cards — corrigido unificando o `fill` para `var(--primary)`.
- [x] Vídeo do hero com `loading="lazy"` indevido (acima da dobra) — removido.
- [x] OG image ausente — gerada (`assets/og-image.png`, 1200×630).

## Melhorias opcionais (7 — ainda abertas, nenhuma delas foi afetada pelas mudanças desta rodada)

Para o usuário decidir. Aplicar via Edit manual ou pedir `/lp-revisar` novamente.

- [ ] **Paleta com 4 cores fortes em uso** (roxo + laranja + teal + amarelo) — GUIDELINES §1 recomenda 2-3.
- [ ] **Nenhuma seção de "pausa"** (GUIDELINES §2) — as 7 seções são todas densas (cards, listas, form).
- [ ] **Sem `@media` reduzindo padding no mobile** — `.section{padding:120px 0}` e `.hero{padding:96px 0 100px}` não caem para o piso de 80px em telas pequenas.
- [ ] **`scroll-margin-top` ausente nos ids de âncora** (`#como-funciona`, `#form`, `#quem-pode-indicar`) — funciona hoje por causa do padding generoso, mas é frágil.
- [ ] **"R$ 500" / "R$ 1.000" sem non-breaking space** — pode quebrar linha entre "R$" e o número.
- [ ] **Sem `preconnect` para os embeds** (`youtube.com`, `form.jotform.com`).
- [ ] **`text-wrap: balance` ausente em h1/h2** — headlines longas podem quebrar com palavra órfã.

## Nice-to-haves (4 — ainda abertos)

Estilístico. Ignorar é aceitável.

- [ ] `.step:nth-child(4) .step__num` muda de roxo para laranja sem explicação visual clara.
- [ ] `touch-action: manipulation` e `-webkit-tap-highlight-color` não definidos nos botões/links.
- [ ] `.footer__links a` não tem `:hover` além do sublinhado estático.
- [ ] `.persona-card:hover` anima `box-shadow` junto com `transform` — impacto desprezível.

## Próximos passos

- Design aprovado, vídeo, form e imagem já integrados.
- Rever mais algum crítico? → editar e rodar `/lp-revisar` novamente.
- Publicar → `/lp-publicar buzzmonitor indiqueeganhe [dominio]`
