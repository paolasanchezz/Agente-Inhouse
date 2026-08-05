# Revisão LP — buzzmonitor/plataforma-completa-para-dados

**Data:** 2026-07-30
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel Web Interface Guidelines)

## Aplicado automaticamente (5 críticos)

- [x] `transition: all` no `.btn-glow` (linha ~152) — trocado por `transition: box-shadow .3s ease, transform .3s ease` (anti-padrão explícito das Web Interface Guidelines)
- [x] Animação `.bg-gradient` (`@keyframes shift`) sem fallback de `prefers-reduced-motion` — adicionado `@media (prefers-reduced-motion: reduce){ .bg-gradient{ animation:none; } }`, consistente com as demais animações da página
- [x] Contraste do texto branco sobre `.bg-gradient` (seção IA COMO DIFERENCIAL) — durante o ciclo da animação o fundo passa por um trecho amarelo (#F1A908), onde texto branco falha AA. Adicionado `text-shadow` escuro em `.ia-head h2`/`.ia-head p` pra garantir legibilidade em qualquer ponto do gradiente, sem alterar o fundo pedido pelo usuário
- [x] Paleta ampla nos ícones dos cards — `benefit-icon`/`ia-icon` usavam as 5 cores da marca (purple/teal/pink/orange/amarelo) nos 6 itens de cada grid, violando GUIDELINES §1 ("escolher 2-3 cores fortes, fugir da tentação de usar todas"). Reduzido para rotação de 3 cores (purple/orange/teal) nos dois grids
- [x] `stamp` de verificação GTM gravado (`.tracking.lock`) — container `GTM-WFJVK858` confirmado correto pra região Brasil

## Melhorias opcionais — resolvidas em 2026-07-30 a pedido do usuário (4)

- [x] **Múltiplos gradientes (3 no total):** mantidos por decisão explícita do usuário — `.bg-gradient` e `.text-gradient` foram pedido literal dele, `.grad-hero` fica como está. Desvio de GUIDELINES §1 aceito conscientemente, não é mais pendência.
- [x] Layout do bloco `.dif-top`: `grid-template-columns` mudou de `1.05fr 1fr` para `1fr 1.25fr` (mais espaço pra imagem) e `align-items` de `center` para `start` (imagem não fica mais "flutuando" solta ao lado de um bloco de texto bem mais alto)
- [x] `.text-gradient` ganhou `color: var(--orange)` como fallback — se `background-clip:text` não for suportado, o texto aparece em laranja sólido em vez de invisível
- [x] `<link rel="preconnect" href="https://form.jotform.com">` adicionado no `<head>`

## Melhorias opcionais restantes (1)

- [ ] Nenhuma seção de "pausa" pura na página (só título grande, sem cards nem CTA) — GUIDELINES §2 recomenda pelo menos 1 momento assim pro olho descansar

## Nice-to-haves — resolvidos em 2026-07-30 (2)

- [x] `touch-action: manipulation` adicionado em `.btn` (cobre todos os botões da página)
- [x] `translate="no"` aplicado às 7 ocorrências visíveis de "Buzzmonitor" no corpo da página (Diferenciais, IA como diferencial, Cases, CTA-final, Footer)

## Nice-to-haves restantes (2)

Estilístico. Ignorar é aceitável.

- [ ] `.benefit-card:hover`/`.case-card:hover`/`.ia-card:hover` animam `box-shadow` junto com `transform` (não é 100% compositor-friendly, mas é padrão comum e de baixo impacto)
- [ ] Header não usa `<nav>` semântico ao redor do link/CTA (baixo impacto, só 1 link)

## Auditorias determinísticas

- **GTM:** `status: ok` — container `GTM-WFJVK858` bate com a região Brasil (`brand/buzzmonitor/tracking.json`). Stamp gravado.
- **Fidelidade de copy:** sem vazamentos — nenhum pull-quote, kicker ou tag rotacionada com texto inventado; frase-âncora do CTA-final bate literal com `copy.txt`; em-dash: 0 ocorrências.
- **SEO:** description (1), robots (1), og: (10), twitter: (4), JSON-LD (1, parseia, `Organization.url`/`sameAs` batem com `brand-manifest.json`), canonical (1) — pacote completo.
- **Multi-idioma:** LP não tem irmãs de outro idioma neste slug — hreflang omitido corretamente (0 ocorrências, conforme esperado).
- **Logo regional:** header/footer apontam para `https://buzzmonitor.com/` (não `"/"`), com `target="_blank" rel="noopener"` — correto.
- **Logo web-safe:** `logo-primary.svg` e `logo-reversed.svg` sem `<text>` vivo (raster/base64) — seguros pro browser.
- **OG image:** `assets/og-plataforma-completa-para-dados.png` existe, 1200×630, URL absoluta com placeholder `{{DOMAIN}}` (resolvido no `lp-publicar`).

## Próximos passos

- Decidir sobre a melhoria opcional dos gradientes (ver acima)
- Design aprovado? → `/lp-publicar buzzmonitor plataforma-completa-para-dados content.buzzmonitor.com`
- Rever mais algum crítico? → editar e rodar `/lp-revisar` novamente
