# LP Buzzmonitor — plataforma-completa-para-dados

**Gerado em:** 2026-07-29
**Copy-fonte:** `copy.txt` (transcrito da página Notion "Copy LP da dor 2 - Dados fragmentados", editada pelo usuário)
**Domínio-alvo:** `content.buzzmonitor.com/plataforma-completa-para-dados` (guarda-chuva migrado ao CI — ver `landing-pages/dominios/MIGRADOS.json`)
**LP irmã de referência visual:** `landing-pages/buzzmonitor/plataforma-completa-monitoramento/` (mesmo CSS system, mesmo guarda-chuva)

## Estrutura

- HEADER (logo + CTA)
- HERO — H1/SUB/CTA + ilustração SVG customizada (cenário confuso: pilha de relatórios/planilha + 12 selos de rede social: Facebook, Instagram, YouTube, LinkedIn, X, Pinterest, Reclame Aqui, Google Meu Negócio, App Store, Google Play, Bluesky, Threads)
- PROBLEMA — dados fragmentados (3 parágrafos, com termos-chave em negrito)
- DIFERENCIAIS (SOLUCAO) — 1 bloco split único (texto completo+pills à esquerda / screenshot à direita), grid de 6 benefícios, fechamento em `.text-gradient` (laranja/amarelo animado) + CTA
- IA COMO DIFERENCIAL — fundo `.bg-gradient` (laranja/amarelo/azul, fornecido pelo usuário), grid de 6 cards (Dashboards ilimitados, Buzz Pills, AI Insights, Classificação automática, Relatórios de produtividade, Buzzmonitor Trends). Sem overline (removido a pedido do usuário)
- CASES — Oi / Betnacional / Prime Energy / Camil (réplica da LP irmã, case 3 trocado de Grupo Casas Bahia para Prime Energy)
- CTA-FINAL — pill + H2 + embed real Jotform
- LOGO-WALL — imagem única reaproveitada da LP irmã (`logo-wall.png`), não recriada em HTML
- FOOTER

**Removido (round 2, 2026-07-29):** seção PROVA standalone (caixa lilás com o texto Prime Energy) — conteúdo reaproveitado no case Prime Energy da seção CASES.

## Estado

- [x] HTML gerado
- [x] Checklist técnico/SEO/GTM validado (em-dash: 0, og: 10 tags, twitter: 4 tags, JSON-LD parseia, GTM-WFJVK858 injetado 2x)
- [x] Fidelidade de copy conferida via extração de texto (sem pull-quotes/kickers inventados)
- [x] Revisão visual completa (design + a11y) — `/lp-revisar` rodado em 2026-07-30, 5 críticos + 6 melhorias/nice-to-haves aplicados a pedido do usuário, ver `REVISAO.md` (resta 1 nice-to-have de baixo impacto)
- [x] Formulário integrado — Jotform (2026-07-29), mesmo form da LP irmã (`jsform/252995108251662`)
- [x] OG image (1200×630) — gerada via Chrome headless em 2026-07-29, `assets/og-image.png` (logo renderizou corretamente, ao contrário do bug conhecido na LP irmã — path corrigido para 4 níveis acima)
- [x] Imagem da seção DIFERENCIAIS trocada — `assets/dashboard-mockup.png` (1536×1024), recebida via Google Drive em 2026-07-29
- [ ] Publicado — rodar `/lp-publicar buzzmonitor plataforma-completa-para-dados content.buzzmonitor.com`

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `./assets/dashboard-mockup.png` (1536×1024 — ilustração de laptop com dashboard, fornecida pelo usuário via Google Drive) — usada na seção Diferenciais
- `./assets/dashboard-analytics.png` e `./assets/dashboard-laptop.png` — não mais referenciadas no HTML (substituídas), mantidas no repo caso voltem a ser úteis
- `./assets/logo-wall.png` (1912×690 — reaproveitado de `plataforma-completa-monitoramento/assets/logo-wall.png`, mesma imagem)
- `./assets/og-image.png` (1200×630 — OG image gerada via `assets/og-source.html` + Chrome headless)

## Notas

- Preview local via `file://` não resolve os paths `../../brand/...` (convenção de source pré-deploy — só resolve corretamente após `lp-publicar` reescrever para `/assets/...`), mesmo comportamento já esperado na LP irmã. Sem erros de console.
- Animações aplicadas com moderação, do catálogo `content.cxpress.io/livraria`: shine-sweep no `.btn-primary`, card-lift nos cards de diferenciais/IA/cases, gradiente animado (`.bg-gradient`) na seção IA, live-indicator na pill do CTA-final, scroll-reveal (IntersectionObserver) em toda a página.
