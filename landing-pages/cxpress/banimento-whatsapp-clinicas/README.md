# LP Cxpress — banimento-whatsapp-clinicas

**Gerado em:** 2026-07-22
**Copy-fonte:** `copy.txt` (output de `/lp-preparar`, réplica literal da LP `banimento-whatsapp`)

## Origem

Design idêntico à referência [`content.cxpress.io/banimento-whatsapp`](https://content.cxpress.io/banimento-whatsapp) (source local em `landing-pages/cxpress/banimento-whatsapp/`), variante para o segmento **clínicas e serviços de saúde** (já listado em `brand/cxpress/brand-manifest.json > audience.segments`).

Único texto novo pedido pelo usuário (H1 + SUB do hero) já era, coincidentemente, idêntico ao hero já publicado na referência — então a copy ficou 100% igual à original em todas as seções.

## Diferenças vs. a referência

1. **Metadados** (title, canonical, OG, Twitter Card, JSON-LD) apontam para o slug `banimento-whatsapp-clinicas` em vez de `banimento-whatsapp`, com title/description mencionando "clínicas" para evitar conteúdo duplicado indexável.
2. **Visual do hero**: imagem própria do usuário (`assets/hero-clinica.jpg`, LP-local), 2ª versão enviada em 2026-07-22 via link do Google Drive (substitui a 1ª foto, de uma médica com celular). Foto de recepcionista de clínica ao telefone usando o WhatsApp no laptop, com elementos ilustrativos de segurança (escudo, cadeado). Redimensionada para 1400×788 e recomprimida em JPEG (~87KB, de 1.6MB original).
   - **Iteração 1** (efêmera, substituída pela 2 abaixo): imagem como elemento à direita do hero (coluna própria), sangrando até a borda da viewport com `mask-image` esmaecendo a borda esquerda.
   - **Iteração 2 — imagem como fundo da seção inteira** (pedido do usuário): `.hero__bg` é agora um `<img>` `position:absolute;inset:0;object-fit:cover` cobrindo toda a seção hero (não mais coluna própria), com `.hero__scrim` (outro `absolute;inset:0`) aplicando `linear-gradient` branco esquerda→direita (desktop) por cima, esmaecendo a área onde o texto senta e deixando a foto visível/nítida à direita. Texto (`.hero__content`) limitado a `max-width:600px` pra não invadir a área nítida da foto. Breakpoint mobile usa gradiente **vertical** (topo→base) em vez de horizontal, porque a coluna de texto ocupa a largura toda e não há espaço pra um fade lateral funcionar. Contraste do texto sobre a foto+gradiente verificado via canvas (composição pixel a pixel): 12.4–13.4:1 em todos os pontos testados (WCAG AA exige ≥4.5:1 pra texto normal).
   - **Correção de espaçamento** (pedido do usuário — "espaço em branco grande demais entre menu e H1"): a causa raiz era a regra genérica `section{padding:130px 0}` (linha ~221) se aplicando também à `.hero` (que é um `<section>`), empilhada com o padding próprio do `.hero__inner`. Corrigido com `.hero{padding:0}`, deixando só `.hero__inner` controlar o espaçamento (64px topo desktop / 48px mobile). Gap medido entre menu e H1: 276px → 146px desktop, 154px mobile.
3. **Formulário**: trocado do Jotform herdado da referência (`261045149477663`) para o Jotform próprio desta LP, `261027639617663`, informado pelo usuário em 2026-07-22.
4. Todo o restante (copy, CSS, estrutura de seções, ordem, cores, animações) é idêntico à referência.

## Estrutura

- HERO (com CTA)
- CLIENTES (prova social)
- FORM / agendar (Jotform embutido — já é integração real, herdada da referência)
- BENEFICIOS
- PROVA (stats)
- PLATAFORMA (features)
- FAQ
- QUEM SOMOS
- FECHO
- FOOTER

## Estado

- [x] HTML gerado (clonado da referência + metadados/hero ajustados)
- [x] Revisão (frontend-design review + web-design-guidelines + checks determinísticos) — 0 críticos, ver `REVISAO.md`
- [x] Formulário integrado — Jotform `261027639617663` (2026-07-22, fornecido pelo usuário, substituiu o `261045149477663` herdado da referência)
- [x] OG image dedicada — `assets/og-image.png` (1200×630) gerada via Chrome headless a partir de `.claude/skills/lp-gerar/og-template.html` (overline + H1 do próprio hero, logo Cxpress). `lp-publicar` renomeia para `og-{slug}.png` no deploy (guarda-chuva).
- [ ] Publicado — rodar `/lp-publicar cxpress banimento-whatsapp-clinicas [dominio]`

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `./assets/hero-clinica.jpg` (hero — foto enviada pelo usuário, LP-local)
- `../../brand/cxpress/assets/plataforma/clientes-cxpress.png` (prova social)
- `../../brand/cxpress/assets/plataforma/plataforma-canais.gif`, `plataforma-chatbot-ia.gif`, `plataforma-dashboard.gif` (seção Plataforma)
- `../../brand/cxpress/assets/plataforma/quem-somos-foto.jpg`
- `../../brand/cxpress/assets/plataforma/elife-logo.png`
