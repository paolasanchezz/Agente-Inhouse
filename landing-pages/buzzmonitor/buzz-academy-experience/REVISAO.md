# Revisao LP — buzzmonitor/buzz-academy-experience

**Data:** 2026-08-03
**Auditores:** frontend-design (review mode, agente independente) + web-design-guidelines (agente independente) + auditorias determinísticas (GTM, fidelidade de copy, SEO §15-§19, screenshots desktop/mobile via Playwright)

## Contexto de briefing

ID visual **escura** foi pedido explícito do cliente — override sancionado do padrão hero-branco (GUIDELINES §3). Dark derivado do roxo da marca (#140222), nunca preto neutro.

## Aplicado automaticamente (6 críticos)

- [x] Focus ring invisível no form card — `:focus-visible` global amarelo dava 1.28:1 sobre o card lilás (WCAG 1.4.11) — adicionada regra escopada `.form-card :focus-visible` com outline roxo #390155 (12.25:1) + ring dos inputs reforçado (alpha 0.15 → 0.35)
- [x] Placeholder abaixo de AA — rgba(36,6,58,0.45) sobre branco = 3.05:1 — subido para 0.62 (≈5:1)
- [x] CTA da nav quebrava em 2 linhas no mobile (54px de altura) — `white-space: nowrap` no `.btn` + logo 24px e padding compacto ≤560px
- [x] Tap target dos `.btn--sm` ~39px — padding 12px → 15px (~45px)
- [x] Semântica de lista perdida (`list-style:none` + VoiceOver/Safari) e ordem dos cursos invisível pra leitor de tela (números 01-05 são aria-hidden) — `role="list"` nas 4 listas (problema, cursos ×3, passos, perfis)
- [x] Tab podia pousar em elemento `.reveal` ainda invisível — listener `focusin` adiciona `.visible` na hora
- [x] `.cadastro` padding-top 110px < mínimo §2 (120px) — subido pra 130px

## Verificações que passaram (sem achado)

- Contraste AA de todos os pares texto/fundo do tema dark (pior caso 6.2:1 no botão laranja/texto roxo; hero__meta 7.1:1; branco sobre scrim do CTA final 8.1:1)
- Em-dash: 0 no HTML e na copy (tolerância zero ok) · fidelidade de copy 100% literal (7 CTAs, frases-âncora intactas, zero punchline inventada)
- GTM `GTM-WFJVK858` (brasil) head+noscript · gate `check_gtm_region.py` OK · selo `.tracking.lock` gravado
- SEO §15 completo (description, 10 og:, 4 twitter:, JSON-LD válido, canonical) · §16 n/a (LP única) · §17 logos → home regional com target=_blank · §18 og-image.png 1200×630 gerada (dark, tricolor) · §19 logo raster sem `<text>`
- Form mock §11 (`action="#"`), labels for/id, autocomplete, form na 2ª seção (ToFu §10)
- Seções-tipo §8 (problema = lista vertical com X; CTA final full-width com gradiente oficial) · pausa aérea §2 (ponte) · reveals com noscript + prefers-reduced-motion + fallback sem IntersectionObserver
- Mobile 390px real (Playwright): sem overflow horizontal, headline antes do visual, grids colapsam

## Melhorias opcionais (7)

Para o usuário decidir. Aplicar via Edit manual ou pedir `/lp-revisar` novamente.

- [ ] H1 abre pelo nome do programa, não pela dor (§3/§5 + fundamentos §0) — foi pedido explícito do briefing ("Hero com 'Buzz Academy Experience'"); a dor vive no SUB. Alternativa pra teste A/B: H1 "O mercado cobra experiência de quem ainda está estudando" + overline "Buzz Academy Experience"
- [ ] "três trilhas" (ponte) e "três momentos" (para-quem) por extenso — §5 pede algarismos; manter exige mexer na copy aprovada (copy.txt + Notion juntos)
- [ ] Overview de trilhas (cards) + acordeões logo abaixo = 3ª repetição dos nomes das trilhas (pills contam) — avaliar fundir card no summary do acordeão numa v2
- [ ] Paleta com 5 matizes (lilás/laranja/teal funcionais + amarelo focus/tag + rosa X) — §1 pede 2-3; poda mais barata: tag "Comece hoje" do CTA final em laranja em vez de amarelo
- [ ] `summary > h3` — alguns leitores de tela achatam heading dentro de role=button; mover heading pra fora se navegação por headings for prioridade
- [ ] `prefers-reduced-motion` não zera transitions de hover (translateY dos cards/botões, rotação do chevron) — cobrir com `transition-duration: 0.01ms` global na media query
- [ ] Feedback de submit no form real — quando integrar embed (`/lp-integrar-form`), garantir sucesso/erro com `aria-live="polite"`

## Nice-to-haves (8)

Estilístico. Ignorar é aceitável.

- [ ] `meta theme-color #140222` + `color-scheme: dark` no html
- [ ] `tabindex="-1"` no `<main id="conteudo">` (skip-link em browsers antigos)
- [ ] `touch-action: manipulation` nos interativos
- [ ] `env(safe-area-inset-*)` na nav fixa (notch/landscape)
- [ ] `spellcheck="false"` no campo de e-mail
- [ ] `translate="no"` nos nomes de marca/trilha
- [ ] JSON-LD `Course` sem `hasCourseInstance`/`offers` (Google exige ambos pra rich result de Course; como está é markup inerte, sem erro)
- [ ] Lato 700 baixado sem uso no CSS — remover da URL do Google Fonts
- [ ] `aria-label` dos logos sem "(abre em nova aba)"

## Notas de conformidade registradas

- X das dores em #FF7396 (derivado do token pink #DE2451) — token puro reprovaria contraste no chip dark; derivação legítima §8
- Glows radiais do hero (atmosfera, 3 matizes em fade) + 1 gradiente linear no CTA final — aderência estrita à §1 pediria 1 tipo; tratado como exceção documentada do briefing dark
- Paths `../../brand/...` no source são a convenção §3.2 — o build do CI reescreve pra `/assets/buzzmonitor/...` no deploy

## Próximos passos

- Design aprovado? → `/lp-integrar-form buzzmonitor/buzz-academy-experience "<snippet>"` (form real, manual-trigger)
- Publicar (com mock, decisão do briefing) → `/lp-publicar buzzmonitor buzz-academy-experience content.buzzmonitor.com`
