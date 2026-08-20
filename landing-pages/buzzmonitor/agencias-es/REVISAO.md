# Revisao LP — buzzmonitor/agencias-es

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

- [x] **"Monitorización" → "Monitoreo de Redes Sociales"** — aprovado pelo Victor em 2026-08-12, aplicado no HTML e no copy.txt.
- [ ] **Contraste do gradiente orange→pink** (btn-primary, cta-box, gradient-text): texto branco/14-16px fica ~2.6-4.4:1 na ponta laranja, abaixo de AA. **Identico a LP design base aprovada e no ar** (plataforma-integral-social-media) — corrigir aqui divergiria a familia visual. Se quiser resolver, o certo e escurecer o gradiente nas DUAS LPs (ex.: partir de #d95400) ou usar navy nos cta-boxes.
- [x] **Container GTM**: Victor confirmou em 2026-08-12 — manter o container padrao de Buzz LATAM (GTM-MKQBX2MG, tracking.json).
- [ ] **Exclamacoes**: 8+ "¡...!" replicadas da LP original (teto anti-IA = 2). Sugestao em copy.txt: manter so nos 3 CTAs de botao.
- [x] **"Informes" -> "Reportes"** — decisao revertida pelo Victor em 2026-08-20. O padrao ES-LATAM e explicito ("relatorio -> reporte, NAO informe" — Regra de Ouro n3 + tabela "General y Negocios"), e a propria LP ja usava "reportes" na meta description e no hero, entao a fidelidade ao design base estava gerando incoerencia interna. Aplicado no HTML e no copy.txt nas 3 ocorrencias de copy nossa (1084, 1118, 1347). O depoimento da Cecilia Esquivel (1230) ficou intacto: e fala de terceiro. A LP design base (plataforma-integral-social-media) foi corrigida no mesmo PR.

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

- Design aprovado? → `/lp-integrar-form buzzmonitor/agencias-es "<snippet>"` (campos do form real documentados no copy.txt)
- Publicar: `/lp-publicar buzzmonitor agencias-es content.buzzmonitor.com` (guarda-chuva CI: manifesto + PR)

---

## Enxugamento estrutural (2026-08-12, tarde)

Victor: *"ficou linda, porem ficou extremamente grande, com excesso de coisas"*. Publico-alvo
definido: **analista de agencia que nunca ouviu falar da Buzzmonitor** e quer automatizar
relatorios, unificar atendimento e automatizar social listening.

**19 blocos -> 8 secoes. ~12.700px -> ~7.840px (-38%).** Nenhum texto novo inventado: todo
H2/H3/bullet que ficou e literal da copy original. O corte foi por redundancia.

### Cortado

| Secao | Por que |
|---|---|
| GESTIONA-CON-IA (8 cards) | duplicava IA-LO-CAMBIA-TODO; fundidas em 1 secao de IA (o card Visual Listening foi preservado) |
| CHATGPT (secao pausa) | ja era card na secao de IA e bullet em Programacion |
| TODO-EN-UNA-PLATAFORMA (6 bullets) | repetia os modulos; so o H2 sobreviveu como titulo da grade |
| SIN-TAREAS-MANUALES | repetia modulos + IA sem argumento novo |
| SUPERA-EXPECTATIVAS (3 colunas) | 2 das 3 colunas repetiam listening/atencion |
| TRIAL duplicado | a oferta de 14 dias aparecia 2x identica; agora 1x no CTA final |
| 21 bullets de modulo | 45 -> 24 (4 por bloco) |
| INTRO-PLATAFORMA como secao | H2 virou titulo da secao Soluciones |

### Reorganizado

- **Logos de agencias subiram** pra logo depois do hero (publico nao conhece a marca: prova social antes do pitch).
- **Os 3 jobs do publico** (listening, atendimento unificado, dashboards/relatorios) viraram os 3 splits COM PRINT da secao Soluciones, 4 bullets cada. Quem nunca viu o produto precisa ver, nao ler bullet.
- **Form foi pro fim**, dentro do bloco de oferta: volta ao default da GUIDELINES §10 (MoFu/BoFu = ultima secao). O override "form na 3a secao" existia so por fidelidade a LP original, que deixou de ser o objetivo. Hero, meio de pagina e nav ancoram em `#demo`.
- Assets sem secao dona removidos: `tela-computador-bm2.png`, `monitoreo-de-videos.png`.

### Critico de contraste resolvido no cta-box

O gradiente da familia (`#ff6b16` -> `#ec174c`) dava 2.6:1 com o checklist branco de 14px. O
cta-box (unico bloco com texto branco pequeno sobre fill) passou a usar tons profundos
**`#c04a00` -> `#c2103c`** (4.98:1 e 6.1:1, ambos acima de AA). Botoes e `.gradient-text`
seguem com o gradiente claro da familia, identicos a LP irma, entao a identidade nao muda.

### Segue aberto

- `.gradient-text` em headings: `#ff6b16` sobre branco = 2.85:1, abaixo de 3:1 pra texto grande. Identico a LP `plataforma-integral-social-media` no ar; corrigir exigiria mexer nas duas.
- `.btn-primary`: branco sobre o gradiente claro = 2.85:1 na ponta laranja. Mesma situacao acima.
