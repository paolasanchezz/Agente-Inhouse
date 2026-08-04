# LP Buzzmonitor — buzz-academy-experience

**Gerado em:** 2026-08-03
**Copy-fonte:** `copy.txt` (output de /lp-preparar; fonte bruta: doc interno "Buzz Academy Experience — Universidade do Buzz")
**Briefing especial:** ID visual escura (dark roxo Buzzmonitor) a pedido do cliente — override do padrão hero-branco das GUIDELINES §3. Trilhas com codificação de cor própria: Intelligence=lilás, Growth=teal, Branding=laranja.

## Estrutura

- HERO (dark, H1 "Buzz Academy Experience", 3 pills de trilha, CTA)
- CADASTRO (2ª seção, ToFu §10 — form MOCK, aguarda /lp-integrar-form)
- PROBLEMA (4 dores, lista vertical com X)
- PONTE (seção de pausa aérea — §2)
- TRILHAS overview (grid 3 cards)
- TRILHAS detalhe (3 `<details>` expansíveis, 5 cursos cada, CTA por trilha)
- COMO-FUNCIONA (4 passos, teal)
- PARA-QUEM (3 perfis, check teal)
- CTA-FINAL (gradiente roxo→laranja + scrim, tag amarela rotacionada)
- FOOTER

## Estado

- [x] HTML gerado
- [ ] Revisão (frontend-design review + web-design-guidelines) — rodar `/lp-revisar buzzmonitor/buzz-academy-experience`
- [ ] OG image 1200×630 — gerar antes de publicar (template `.claude/skills/lp-gerar/og-template.html` + Chrome headless; salvar em `assets/og-image.png`; no Windows renderizar em $TEMP e copiar)
- [ ] Formulário integrado — rodar `/lp-integrar-form buzzmonitor/buzz-academy-experience [snippet]`
- [ ] Publicado — rodar `/lp-publicar buzzmonitor buzz-academy-experience content.buzzmonitor.com`

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (nav + footer, raster base64 web-safe §19)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon §12)

## GTM

- Região: brasil (slug sem sufixo → fallback §5.1) → container `GTM-WFJVK858` injetado (head + noscript). Gate `check_gtm_region.py`: OK.

## Pendências de conteúdo (ver toggle no Notion da copy)

- [FACT-CHECK] "certificado" (COMO-FUNCIONA) — confirmar com o time da Buzz Academy.
- [OBSERVACAO] Nomes quase iguais de curso de IA nas trilhas Intelligence e Branding (literal do catálogo-fonte).
- [OBSERVACAO] "Universidade do Buzz" (doc-fonte) vs "Buzz Academy" (briefing) — copy segue o briefing.
