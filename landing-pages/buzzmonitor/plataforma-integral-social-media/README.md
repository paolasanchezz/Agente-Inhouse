# LP Buzzmonitor — plataforma-integral-social-media

**Gerado em:** 2026-07-29
**Copy-fonte:** `copy.txt` (transcrição literal de 5 criativos estáticos aprovados da campanha, compartilhados pelo usuário no chat — não do arquivo `conhecimento/copywriting/revisoes/campana-bofu-painpoints-buzzmonitor-revisado-2026-07-28.md`, que ficou desatualizado em relação aos criativos finais)

## Estrutura

1. HERO — "Varias herramientas, cero eficiencia"
2. PROBLEMA-AGENCIAS — "Más clientes, no más caos"
3. PROBLEMA-ENTERPRISE — "¿Pagaste enterprise y te abandonaron?" (comparativo Sin acompañamiento vs Con Buzzmonitor)
4. PROBLEMA-CRISIS — "Tu marca está en crisis"
5. PROBLEMA-INSIGHTS — "Tu competencia te lleva ventaja" (Buzz Pills + AI Insights)
6. DIFERENCIAL — faixa de features (escucha social, publicación, reportes, atención al cliente) + mascote raposa
7. PRUEBA — mockup de dashboard do produto (recriado em CSS/SVG, não é screenshot real)
8. CTA-FINAL — form mock + prova social
9. FOOTER

## Estado

- [x] HTML gerado
- [x] Revisão (frontend-design review + web-design-guidelines) — 9 críticos aplicados (contraste AA, aria-hidden, scroll-margin-top, fonte, padding). Ver `REVISAO.md`.
- [x] Formulário integrado — Jotform (2026-07-30)
- [x] Publicado — https://buzzmonitor-lp-bofu-painpoints-lata.vercel.app/plataforma-integral-social-media (modo solo, 2026-07-30)
- [ ] OG image (1200x630) pendente de gerar — template em `.claude/skills/lp-gerar/og-template.html` + Chrome headless. Path final: `landing-pages/buzzmonitor/plataforma-integral-social-media/assets/og-image.png`.

## Notas de escopo (decisões tomadas nesta geração)

- **Paleta restrita a laranja (#EB7C2E) + rosa (#DE2451)** — só esse eixo, sem roxo/teal/amarelo do brand, pra bater com os 5 criativos aprovados (que usam só esse gradiente).
- **Ilustrações complexas dos criativos (bola de linha emaranhada, celular pegando fogo com posts, foguete decolando) foram simplificadas** para composições de cards/ícones/gráficos em CSS puro — não há os arquivos de ilustração originais, só a descrição visual. O idioma de cor/tipografia/cards é fiel; a ilustração bespoke não é pixel-a-pixel.
- **Mockup de dashboard (seção PRUEBA) é recriado em CSS/SVG**, não é o screenshot real do produto (não achamos um asset existente que batesse com o mockup mostrado nos criativos — o único screenshot real encontrado no repo, de uma LP antiga, tem um layout de produto diferente).
- **Mascote raposa**: não existe como asset do brand nem da campanha no repo — criada como SVG inline minimalista (silhueta simples), cor laranja.
- Copy 100% literal dos criativos (não do arquivo de campanha em `conhecimento/copywriting/revisoes/`). 2 pequenas lacunas de transcrição (labels do gráfico "Tú"/"Tu competencia" e as 4 mini-métricas do dashboard) foram identificadas na auditoria de fidelidade e adicionadas retroativamente ao `copy.txt`.

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header + footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
