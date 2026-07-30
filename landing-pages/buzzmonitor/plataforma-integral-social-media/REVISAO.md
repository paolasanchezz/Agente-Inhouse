# Revisão LP — buzzmonitor/plataforma-integral-social-media

**Data:** 2026-07-30
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel Labs)

## Aplicado automaticamente (9 críticos)

- [x] Contraste AA: laranja (#EB7C2E) usado como cor de texto/ícone sobre fundo claro falhava (~2.6-2.8:1). Criado token `--orange-ink:#B34F15` (4.5-5:1 verificado matematicamente) e aplicado em `.kpi__delta`, `.compare-card--good svg`, `.fox-wrap svg`.
- [x] Contraste AA: texto branco sobre a ponta laranja do gradiente (`.btn-cta`, `.compare-card--good .compare-card__head`, `.race-bar--you`) falhava (~2.8:1). Criado `--gradient-safe` (rosa → laranja escurecido #B34F15) e aplicado nesses 3 componentes. Gradiente decorativo original (`--gradient`) mantido só em blobs sem texto (`.section__glow`, `.crisis-glow`) e na barra de "Principales temas" (decorativa, sem texto sobreposto).
- [x] Texto de gradiente (H1/H2 `.grad`) sem fallback se `background-clip:text` não for suportado — adicionado `@supports not (background-clip:text)` com cor sólida de fallback (pink / pink-light no CTA final escuro) nas 3 instâncias.
- [x] SVGs decorativos sem `aria-hidden="true"` explícito: ícones de check/X nos comparativos (10x), ícones dos pain-tags (3x), setas dos KPI delta (4x), ícone do race-bar (1x) — todos corrigidos.
- [x] `#cta-final` é destino de 6 links âncora mas não tinha `scroll-margin-top`; navbar sticky tapava o título ao chegar via scroll suave. Adicionado `scroll-margin-top:88px`.
- [x] `--subtitle` usava 'League Spartan' (fonte de heading, peso 300 não carregado) como fallback de HK Grotesk — trocado para 'Lato' e importado peso 300 do Lato via Google Fonts.
- [x] Padding de seção (100px/72px) abaixo do mínimo de GUIDELINES §2 (120px/80px) — aumentado para 130px/84px.
- [x] GTM auditado via `check_gtm_region.py` — status `ok` (GTM-MKQBX2MG, região latam), selo `.tracking.lock` gravado.
- [x] Auditoria de fidelidade de copy — 0 vazamentos encontrados (2 pequenas lacunas de transcrição já haviam sido corrigidas em `copy.txt` durante o `lp-gerar`).

## Melhorias opcionais (2)

- [ ] Sparkline de "Evolución de menciones" e as barras de "Principales temas" usam o laranja/gradiente original sobre fundo claro (mesma família do problema de contraste, mas em elementos de gráfico puramente decorativos/secundários dentro do mockup de dashboard) — se quiser rigor total, trocar para `--orange-ink` também.
- [ ] `.btn-cta:hover` anima `transform` + `box-shadow`; `box-shadow` é menos performático que `transform`/`opacity` puro (Web Interface Guidelines). Não bloqueante.

## Nice-to-haves (1)

- [ ] O ícone da mascote raposa é uma silhueta bem abstrata, não lê como raposa à primeira vista (já documentado como simplificação consciente no README, dado que não há asset original).

## Próximos passos

- Design aprovado? → `/lp-integrar-form buzzmonitor/plataforma-integral-social-media "{snippet}"`
- Rever mais algum crítico? → editar e rodar `/lp-revisar` novamente
