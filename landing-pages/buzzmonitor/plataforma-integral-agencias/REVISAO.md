# Revisao LP — buzzmonitor/plataforma-integral-agencias

**Data:** 2026-08-12
**Auditores:** frontend-design (review mode, com auditoria de fidelidade da copy) + web-design-guidelines (a11y/semantica)

## Passou sem achados

- **Fidelidade da copy: 100%.** Todos os textos visiveis batem literalmente com `copy.txt` (20 secoes conferidas). Zero em-dash. Nenhum texto inventado fora da whitelist.
- GTM gate deterministico: `ok` (latam → GTM-MKQBX2MG), selo `.tracking.lock` gravado.
- SEO completo (1 description, 10 og:, 4 twitter:, JSON-LD parseia, canonical), OG image 1200×630 no padrao §18, favicon PNG, logo raster web-safe (§19), `min-height:0` em imgs de grid (§14), reveals com fallback triplo (noscript + reduced-motion + setTimeout), skip-link, labels em todos os inputs, hierarquia de headings correta, sem overflow horizontal mobile (validado em viewport real 375px).

## Aplicado automaticamente (8 criticos/melhorias)

- [x] Video hero: botao pausar/reproduzir (WCAG 2.2.2) + `prefers-reduced-motion` desliga autoplay (mostra poster)
- [x] Contadores `.js-counter`: valores finais renderizados no HTML (copy visivel sem JS) + respeitam `prefers-reduced-motion`
- [x] Selects do form mock: removido `required` (com 1 option placeholder o submit travava — o form real repõe via /lp-integrar-form)
- [x] `focus-visible` global em links e botoes (navy; branco sobre gradiente)
- [x] `scroll-margin-top: 92px` em todos os alvos de ancora (header sticky de 78px)
- [x] Menu mobile fecha ao clicar em link interno
- [x] Ano do footer hardcoded "2026" (nao depende de JS)
- [x] `loading="lazy"` nas 60 imgs do marquee + `aria-hidden` na aspa decorativa dos quote-cards

## Decisoes pendentes do Victor (nao aplicadas de proposito)

- [ ] **"Monitorización de Redes Sociales"** (card Modulos): grafia de Espanha; padrao ES-LATAM pede "Monitoreo". Mantido literal da LP original (que atende tambem Espanha). Trocar?
- [ ] **Contraste do gradiente orange→pink** (btn-primary, cta-box, gradient-text): texto branco/14-16px fica ~2.6-4.4:1 na ponta laranja, abaixo de AA. **Identico a LP design base aprovada e no ar** (plataforma-integral-social-media) — corrigir aqui divergiria a familia visual. Se quiser resolver, o certo e escurecer o gradiente nas DUAS LPs (ex.: partir de #d95400) ou usar navy nos cta-boxes.
- [ ] **Container GTM**: usei GTM-MKQBX2MG (tracking.json latam, mesmo da LP design base no mesmo dominio — e o que o gate de CI valida). Registro: o ecossistema GreatPages LATAM ES usa GTM-5PNK2VZ. Confirmar qual deve medir esta LP antes de rodar midia.
- [ ] **Exclamacoes**: 8+ "¡...!" replicadas da LP original (teto anti-IA = 2). Sugestao em copy.txt: manter so nos 3 CTAs de botao.
- [ ] "Informes" (~9x) vs "reportes" (padrao LATAM): mantido "informes" por fidelidade (original + design base usam).

## Melhorias opcionais

- [ ] Marquee de logos: pausa so em hover/reduced-motion — sem mecanismo pra teclado/touch (herdado da design base)
- [ ] `width`/`height` intrinsecos nas imgs de conteudo (prints, logos) pra reduzir CLS
- [ ] Secao Modulos (#soluciones) sem H2 proprio — a copy original nao tem; adicionar exigiria texto novo (violaria fidelidade). Se quiser, definir um H2 com o Victor
- [ ] `.footer-social` como `<nav aria-label>` em vez de `<div>`
- [ ] Menu mobile: fechar com Escape + devolver foco ao botao
- [ ] `.btn-on-gradient` (texto rosa sobre branco ≈4.4:1): trocar texto pra navy se quiser AA estrito

## Nice-to-haves

- [ ] `.btn-light` e CSS morto (nunca usado) — remover
- [ ] Setas "→" e icones emoji decorativos em `<span aria-hidden>`
- [ ] `text-wrap: balance` nos titulos
- [ ] Wrapper `aria-hidden="true"` no segundo conjunto (duplicado) do marquee

## Proximos passos

- Design aprovado? → `/lp-integrar-form buzzmonitor/plataforma-integral-agencias "<snippet>"` (campos do form real documentados no copy.txt)
- Publicar: `/lp-publicar buzzmonitor plataforma-integral-agencias content.buzzmonitor.com` (guarda-chuva CI: manifesto + PR)
