# Revisao LP — buzzmonitor/plataforma-completa-atendimento

**Data:** 2026-08-11 (2ª rodada — a 1ª foi em 2026-08-07, ver histórico git para o registro anterior; entre as duas rodadas houve trabalho extenso direto no chat: imagens/vídeo reais na hero e problema, galeria solta na timeline, logomarcas reais nos cases, redesenho de ícones)
**Auditores:** frontend-design (review manual, guidelines aplicadas item a item) + web-design-guidelines (checklist Vercel Labs, fetch ao vivo) + `check_gtm_region.py` (determinístico) + auditoria de fidelidade de copy + auditoria SEO/hreflang/logo/OG

## Aplicado automaticamente nesta rodada (1 crítico)

- [x] **A11y — vídeo da seção PROBLEMA com autoplay sem respeitar `prefers-reduced-motion`** (`.problema-visual video`) — o `<video autoplay loop muted>` ignorava a preferência de movimento reduzido do usuário; a regra CSS global (`@media (prefers-reduced-motion: reduce)`) só cobre `animation`/`transition`, não playback de `<video>`. Corrigido: removido `autoplay` do HTML, adicionado `id="problema-video"` + script que só chama `.play()` quando `!matchMedia('(prefers-reduced-motion: reduce)').matches`, com fallback pro evento `loadeddata` se o vídeo ainda não estiver pronto. Também adicionado `width="1280" height="720"` (dimensão real, lida via `videoWidth`/`videoHeight` no navegador) — antes o `<video>` não tinha dimensões intrínsecas no HTML, risco de layout shift (CLS) antes do metadata carregar.
  - Nota de verificação: confirmei via `matchMedia` que a detecção de `prefers-reduced-motion` funciona, e que `.play()` funciona no vídeo (testado manualmente). O preview sandbox usado nesta sessão parece bloquear autoplay disparado por script na carga inicial da página (comportamento do próprio sandbox de automação, não reproduz o comportamento padrão de autoplay mudo em navegadores reais) — o padrão de código aplicado é o padrão-textbook para esse cenário (idêntico ao usado por sites com hero em vídeo respeitando reduced-motion).

## Críticos de rodadas anteriores — confirmados ainda corrigidos (sem regressão)

- [x] Contraste AA do rótulo "Etapa N" na timeline — ainda `rgba(255,255,255,.62)`.
- [x] Contraste AA do título "Solução" e fechamento em gradiente — ainda usando `--grad-warm-text` (não o `--grad-warm` claro).
- [x] Ícones decorativos com `aria-hidden="true"` — reconferido, todos os SVGs novos desta rodada (ícones de canal redesenhados, timeline) também têm o atributo.
- [x] OG image 1200×630 presente e válida, sem `og-image.png` órfão.
- [x] `scroll-margin-top` no `#cta-final`.
- [x] GTM `GTM-WFJVK858` bate com a região `brasil`, stamp `.tracking.lock` ainda válido (fingerprint não mudou).
- [x] Em-dash literal renderizado: **0** (reconferido após todas as mudanças desta sessão).

## Críticos sinalizados, NÃO aplicados automaticamente (decisão sua)

- [ ] **Contraste AA nos botões (`.btn-primary`)** — texto branco sobre o degradê laranja→rosa (`--grad-warm`) continua em **~2.85:1** na ponta laranja e **~4.38:1** na ponta rosa, abaixo do mínimo 4.5:1. Mesmo trade-off já aceito conscientemente por você nesta e na LP irmã `plataforma-completa-monitoramento`. Não alterado sem confirmação — ver opções na rodada anterior (README/histórico).

## Melhorias opcionais (5)

- [ ] **Números em destaque nos cases** ("36h → 3h", "+220%", "100% · 142 lojas", "1 hora") — restatement visual dos números já no `<h3>`, não é texto novo. Documentado, sem ação necessária.
- [ ] `.case-block .brand` e `.eyebrow` — 2 classes CSS definidas mas não usadas em nenhum elemento do HTML atual (`.brand` ficou órfã depois que os cases passaram a usar `.case-logo` com imagem real). Sem impacto visual, só limpeza de código.
- [ ] Ícones de canal (15) são glifos SVG simplificados, não logomarcas oficiais pixel-perfect — 5 já foram redesenhados por estarem distorcidos (Threads, Bluesky, TikTok, WordPress, Pinterest); os outros 10 seguem como glifos aproximados.
- [ ] `./assets/hero.jpg` não tem `fetchpriority="high"` — é provavelmente o maior candidato a LCP (Largest Contentful Paint) da página, being a imagem grande logo no topo. Adicionar o atributo ajudaria o navegador a priorizar o download.
- [ ] As 4 imagens de `.case-logo` (logos de clientes) não têm `loading="lazy"` — impacto mínimo dado o tamanho pequeno dos arquivos (6-34 KB cada), mas seria consistente com o resto da página.

## Nice-to-haves (1)

- [ ] Os 4 cases usam só laranja/rosa nos degradês do bloco colorido (pedido explícito seu) — visualmente um pouco repetitivo entre os 4 cards, mas é a paleta pedida.

## Auditoria de fidelidade de copy

Nenhum vazamento de copy nova (pull-quote, kicker, tag rotacionada, punchline) encontrado. Textos fora de `copy.txt` continuam restritos à whitelist (aria-labels funcionais, skip-link, footer, form via embed externo) ou são edições diretas já aprovadas por você no chat ao longo da sessão (texto do botão "Demonstração gratuita", frase "Seu time só entra aqui", textos das imagens/galeria que são puramente visuais). Em-dash literal renderizado: **0**.

## Auditoria SEO / multi-idioma / logo / OG

- Pacote SEO: `meta description` 1, `og:` 10, `twitter:` 4, JSON-LD válido, `canonical` 1 — todos OK.
- `Organization.url` = `https://buzzmonitor.com/` (bate com `brand-manifest.json#regions.brasil.home`); `sameAs` inclui LinkedIn + Instagram BR — OK.
- Multi-idioma: LP única, hreflang omitido corretamente (só `x-default` + `canonical`) — OK.
- Logo header/footer: `href="https://buzzmonitor.com/"`, `target="_blank" rel="noopener"`, aria-label localizado — OK. Logos SVG confirmados sem `<text>` vivo (web-safe) — OK.
- OG image: 1200×630 confirmada via Pillow, sem duplicata `og-image.png`.

## Próximos passos

- Design aprovado? Formulário já integrado (Jotform, `jsform/252995108251662`).
- Decidir sobre o contraste dos botões (ver crítico pendente acima) — única decisão de design ainda aberta.
- Quando aprovada: `/lp-publicar buzzmonitor plataforma-completa-atendimento content.buzzmonitor.com`
