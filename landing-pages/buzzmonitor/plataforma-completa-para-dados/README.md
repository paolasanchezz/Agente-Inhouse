# LP Buzzmonitor — plataforma-completa-para-dados

**Gerado em:** 2026-07-29
**Copy-fonte:** `copy.txt` (transcrito da página Notion "Copy LP da dor 2 - Dados fragmentados", editada pelo usuário)
**Domínio-alvo:** `content.buzzmonitor.com/plataforma-completa-para-dados` (guarda-chuva migrado ao CI — ver `landing-pages/dominios/MIGRADOS.json`)
**LP irmã de referência visual:** `landing-pages/buzzmonitor/plataforma-completa-monitoramento/` (mesmo CSS system, mesmo guarda-chuva)

## Estrutura

- HEADER (logo + CTA)
- HERO — H1/SUB/CTA + ilustração SVG customizada (cenário confuso: pilha de relatórios/planilha + 12 selos de rede social: Facebook, Instagram, YouTube, LinkedIn, X, Pinterest, Reclame Aqui, Google Meu Negócio, App Store, Google Play, Bluesky, Threads)
- PROBLEMA — dados fragmentados (3 parágrafos, com termos-chave em negrito)
- DIFERENCIAIS (SOLUCAO) — bloco 1 `.dif-hero`: H2+H3+intro centralizados + `.dif-hero-visual` (imagem grande centralizada, `dashboard-categorias.png`); bloco 2 `.dif-top`: parágrafos sobre IA ao lado de `dashboard-mockup.png` (pill-row removida — round 7); grid de 6 benefícios (ícones circulares), fechamento em `.text-gradient` (laranja/amarelo animado) + CTA
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
- [x] OG image (1200×630) — gerada via Chrome headless em 2026-07-29, `assets/og-plataforma-completa-para-dados.png` (logo renderizou corretamente, ao contrário do bug conhecido na LP irmã — path corrigido para 4 níveis acima)
- [x] Imagem da seção DIFERENCIAIS trocada — `assets/dashboard-mockup.png` (1536×1024), recebida via Google Drive em 2026-07-29
- [x] Publicado — live em https://content.buzzmonitor.com/plataforma-completa-para-dados desde 2026-07-30 (PR #123, deploy CI [run 30556599509](https://github.com/victorfmlopes/Agente-Inhouse/actions/runs/30556599509)). Relatório: ver Notion "Entrega LP · Buzzmonitor · plataforma-completa-para-dados · 2026-07-30"
- [x] Round 6 (2026-07-31): seção Diferenciais reestruturada em 2 blocos + nova imagem `dashboard-categorias.png` (mulher com celular cercada pelas categorias reais) + ícones do benefit-grid trocados para circulares.
- [x] Round 7 (2026-07-31): pill-row (8 categorias em lilás) removida.
- [x] Round 8 (2026-07-31): benefit-grid em 6 colunas numa linha só (desktop); fonte do fechamento `.text-gradient` aumentada.
- [x] Republicado em 2026-07-31 (PR [#141](https://github.com/victorfmlopes/Agente-Inhouse/pull/141), merge direto via API — o merge-bot/CI de PR não disparou o check-suite do GitHub Actions em nenhuma tentativa nesta rodada, causa não diagnosticada, provavelmente pontual; deploy disparou normalmente pelo push na main, [run 30651822820](https://github.com/victorfmlopes/Agente-Inhouse/actions/runs/30651822820)). Vizinhas do guarda-chuva conferidas intactas (200 nas 4).
- [x] Round 9 (2026-07-31): pill-row reinserida dentro do `.dif-hero` (7 termos, sem "Campanhas"); `.dif-top` de volta a `align-items:center`; fonte do fechamento `.text-gradient` reduzida para `clamp(24px,3.4vw,31px)` — testado empiricamente no browser (31px é o maior valor que cabe em 2 linhas no container de 720px; 38px quebrava em 3).
- [x] Round 10 (2026-07-31): pill "Campanhas" adicionada de volta (8 termos no total); "Crises" renomeada para "Gestão de crises".
- [x] Round 11 (2026-07-31): botões trocados de laranja/roxo para azul (`--blue:#3E5CC7`, validado ≥AA com texto branco); botão do cabeçalho com texto "Demonstração gratuita"; degradê da seção IA trocado de laranja/amarelo/azul para roxo/azul/rosa. **Pendente novo `/lp-publicar` pra levar essas mudanças ao ar.**

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `./assets/dashboard-categorias.png` (1672×941 — mulher com celular cercada pelas categorias/gráficos reais, fornecida via Google Drive) — usada no bloco `.dif-hero-visual` (topo da seção Diferenciais)
- `./assets/dashboard-mockup.png` (1536×1024 — ilustração de laptop com dashboard, fornecida pelo usuário via Google Drive) — usada no bloco `.dif-top` (2º bloco da seção Diferenciais)
- `./assets/dashboard-analytics.png` e `./assets/dashboard-laptop.png` — não mais referenciadas no HTML (substituídas), mantidas no repo caso voltem a ser úteis
- `./assets/logo-wall.png` (1912×690 — reaproveitado de `plataforma-completa-monitoramento/assets/logo-wall.png`, mesma imagem)
- `./assets/og-plataforma-completa-para-dados.png` (1200×630 — OG image gerada via `assets/og-source.html` + Chrome headless)

## Notas

- Preview local via `file://` não resolve os paths `../../brand/...` (convenção de source pré-deploy — só resolve corretamente após `lp-publicar` reescrever para `/assets/...`), mesmo comportamento já esperado na LP irmã. Sem erros de console.
- Animações aplicadas com moderação, do catálogo `content.cxpress.io/livraria`: shine-sweep no `.btn-primary`, card-lift nos cards de diferenciais/IA/cases, gradiente animado (`.bg-gradient`) na seção IA, live-indicator na pill do CTA-final, scroll-reveal (IntersectionObserver) em toda a página.
