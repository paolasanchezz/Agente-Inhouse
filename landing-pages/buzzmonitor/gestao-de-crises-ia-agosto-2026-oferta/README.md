# LP Buzzmonitor — gestao-de-crises-ia-agosto-2026-oferta

**Gerado em:** 2026-08-05
**Copy-fonte:** `copy.txt` (output de /lp-preparar)
**Domínio destino:** `webinar.buzzmonitor.com`
**Contexto:** LP de oferta pós-webinar "Gestão de Crises com IA" (25/ago/2026) — mesma família visual da oferta `social-listening-julho-2026-brasil-oferta`.

## Estrutura

- HERO (badge degradê roxo "Oferta exclusiva do webinar" / H1 "Do sinal fraco à resposta certa, em tempo real." / watermark "14" / subtext + CTA. Sem data no hero)
- OFERTA (fundo roxo gradiente, "14 dias" gigante laranja, 3 cards com stagger no scroll, bônus de desconto, validade 8/set, CTA)
- BENEFICIOS (grid de 5 itens com borda-topo, temas de detecção de crise)
- MODULOS (H2 + 4 itens grid flat — Listening em primeiro, por ser o módulo-chave de gestão de crise)
- PROVA SOCIAL (H2 + 4 métricas, fundo roxo, count-up)
- URGENCIA (eyebrow amarelo + H2 + body + CTA, fundo roxo-escuro, validade 8/set)
- CTA FINAL / form mock (id="form-section", fundo laranja, layout 2 colunas, campos Nome/Email/Empresa)
- CLIENTES (mural de logos em slideshow 16s — mural-1/mural-2.jpeg copiados de `social-listening-julho-2026-brasil-oferta/assets/logos/` pra manter a LP self-contained)
- FOOTER

## Design / animação

Reaproveita integralmente o sistema visual e o JS da LP de oferta anterior (mesma família, já aprovado):
- Fontes: Poppins (headings) + Lato (body), via Google Fonts
- Ícones: Tabler Icons webfont via CDN (jsdelivr)
- Paleta: roxo + laranja como primárias
- Animações: IntersectionObserver com stagger (data-delay), mask-reveal no heading de Benefícios, reveal por item na Oferta, count-up nos números da Prova Social, hover-lift nos cards. Safety-net de 3s. Respeita prefers-reduced-motion e tem fallback noscript.

## Nota sobre preço

Esta oferta usa o padrão "14 dias grátis + desconto ao final" **sem valor numérico explícito** (mesmo padrão da oferta de julho/2026) — evita risco de divergência entre R$1.590 (antigo) e R$1.790 (atual, a partir de 2026-08) enquanto o valor exato não precisa aparecer na peça.

## Estado

- [x] Copy preparada (`/lp-preparar`)
- [x] HTML gerado
- [x] Revisão (frontend-design review + checks determinísticos) — 4 críticos de contraste AA aplicados, ver `REVISAO.md`
- [x] OG image gerada (`assets/og-gestao-de-crises-ia-agosto-2026-oferta.png`, 1200×630)
- [x] Formulário integrado — Jotform `253573505200650` (2026-08-05, mesmo form da oferta anterior)
- [ ] Publicado — via fluxo CI (manifesto `landing-pages/dominios/webinar-buzzmonitor-com/manifest.json` + PR)

**Form provider:** Jotform (2026-08-05)

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `./assets/logos/mural-1.jpeg`, `./assets/logos/mural-2.jpeg` (mural de clientes)
