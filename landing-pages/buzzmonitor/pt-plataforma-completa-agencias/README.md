# LP Buzzmonitor — pt-plataforma-completa-agencias (PT-PT)

**Gerado em:** 2026-10-07 (pedido da Thamires)
**Copy-fonte:** `copy.txt` (tradução PT-PT da LP BR https://conteudo.buzzmonitor.com.br/plataforma-completa-agencias, estrutura da v3 da `agencias-es`). Notion: Entregas > "Copy LP · Buzzmonitor · pt-plataforma-completa-agencias · 2026-10-07" (aprovada)
**Design base:** `landing-pages/buzzmonitor/agencias-es/index.html` — mesmo HTML/CSS, só mudam texto, idioma, tracking e os blocos listados em "Diferenças". Mesmo padrão das LPs `monitoramento-manual-pt` e `mcp-buzzmonitor-pt`.
**Destino:** `content.buzzmonitor.com/pt-plataforma-completa-agencias`

## ⚠️ Região forçada (slug com PREFIXO `pt-`)

O slug foi pedido com `pt-` no início, não no fim. A cascata de região (`landing-pages/CONTEXT.md` §5.1)
lê **sufixo** do slug, então não resolve por ele; resolve pelo passo 2 (`<html lang="pt-PT">`).
Qualquer skill que regenere o HTML do zero (`lp-gerar` pula o passo 2) cairia no fallback **brasil**
e trocaria o GTM. Ao mexer nesta LP: editar o `index.html` existente, nunca regenerar.

- `<html lang="pt-PT">`, `og:locale=pt_PT`, JSON-LD `inLanguage: pt-PT`
- GTM Portugal `GTM-NCFT22CW` (head + noscript)
- Home regional `https://getbuzzmonitor.com/pt/` (logo header/footer + `Organization.url`)

## Estrutura

1. HERO (H1 dor + H2 + H3 + CTA + vídeo `hero-plataforma.mp4`)
2. Prova social: números + parede de logos de clientes
3. Soluções (3 splits com print: Monitorização · Atendimento · Dashboards) + caixa "Redes e canais integrados" (14 canais, 5 visíveis + "Ver mais")
4. Módulos (Métricas · Agendamento e Publicação · Gestão de Crises)
5. IA (print + 6 cards)
6. Depoimentos (vídeo YouTube da LP BR)
7. CTA final: oferta de 14 dias + formulário
8. Faixa de logos de agências
9. Footer

## Diferenças em relação à `agencias-es`

- **Formulário:** a ES envia para o endpoint GreatPages da LATAM (`contenido.getbuzzmonitor.com/conversion`). Esse envio foi **removido** (leads PT cairiam na base LATAM). Ficou mock (`action="#"`) até `/lp-integrar-form` com o Jotform PT `261405305585859` (o mesmo de `mcp-buzzmonitor-pt` e `monitoramento-manual-pt`).
- **Meta Pixel hardcoded** da LATAM (`935436740448328`) removido: nas LPs PT o pixel vem pelo GTM de Portugal.
- **Depoimentos:** grade de 6 citações ES trocada pelo vídeo de depoimentos da LP BR (`youtube.com/embed/nBMZZZKrMpI`). Traduzir citações de pessoas reais para PT-PT seria pôr-lhes palavras na boca. CSP do domínio já libera `www.youtube.com` em `frame-src`.
- **Preço** (`$390 USD/Mes`) removido: não há preço EUR documentado.
- **Canal Reclame Aqui** (só Brasil) removido: 14 canais.
- **Footer:** X, Facebook e YouTube da conta ES removidos (sem equivalente PT no `brand-manifest.json`); ficam Instagram `buzzmonitor.pt` + LinkedIn.
- **Vídeo hero:** `social-listening-es.mp4` (UI em espanhol) trocado por `hero-plataforma.mp4` + `hero-poster.jpg` (origem: `monitoramento-com-ia`). Texto do vídeo em português neutro.
- **Prints:** os 4 da ES têm a UI em espanhol ("Distribución de reacciones", "Prioridad de Tickets", "¿Qué necesito saber?"). Trocados pelas versões em português já usadas noutras LPs:
  - Monitorização: `crise-1.png` (Distribuição de reações) — origem `monitoramento-manual-pt`
  - Atendimento: `crise-2.png` (Top 5 tags mais frequentes) — origem `monitoramento-manual-pt`
  - Dashboards: `dashboard-analytics.png` — origem `plataforma-completa-para-dados`
  - IA: `insights.png` (AI Insights) — origem `monitoramento-manual-pt`
  Todos com nome idêntico e conteúdo byte a byte igual ao das LPs de origem (md5 conferido), então não colidem no `/assets/buzzmonitor/` do guarda-chuva.
- **Header mobile (≤640px):** "Pedir demonstração" é mais longo que "Agenda una demo" e empurrava o botão de menu 46px para fora do ecrã em 375px. Corrigido sem baixar a fonte do piso §20 (14px): gap do `.nav` 24→10px, padding do CTA 15→12px e seta "→" escondida no CTA da navbar. Medido: `scrollWidth` = 375 em 375px e 414 em 414px. Em 320-360px ainda transborda (a ES também), ver REVISAO.md.

**Form provider:** Jotform PT `261405305585859` (integrado em 2026-10-09)

## Estado

- [x] Copy PT-PT aprovada
- [x] HTML gerado
- [x] OG image 1200×630 → `assets/og-pt-plataforma-completa-agencias.png` (mesmo layout da OG da `agencias-es`)
- [x] Revisão (ver `REVISAO.md`)
- [x] Formulário integrado (Jotform PT `261405305585859`)
- [ ] Publicado (`/lp-publicar buzzmonitor pt-plataforma-completa-agencias content.buzzmonitor.com`)

## Pendências que precisam de decisão humana

1. **Preço em EUR** para a linha "Planos a partir de…" (omitida).
2. **Contacto WhatsApp PT** (bloco da LP BR omitido, número brasileiro).
3. **Vídeo de depoimentos** com áudio PT-BR; trocar se houver versão PT-PT.
4. **Prints da plataforma** (crise-1, crise-2, dashboard, insights) mostram a UI em PT-BR (ex.: "Curtiram", "Amaram"). É a UI real do produto; trocar se houver capturas em PT-PT.
5. ~~Política de privacidade PT~~ resolvido: rodapé aponta para `https://buzzmonitor.com/pt-pt/privacidade/` (página PT-PT oficial, 200).

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg`, `logo-icon.png`
- `./assets/hero-plataforma.mp4`, `hero-poster.jpg`
- `./assets/crise-1.png`, `crise-2.png`, `dashboard-analytics.png`, `insights.png`
- `./assets/plataformas/*.webp` (14)
- `./assets/logos-clientes/*` (30), `./assets/logos-agencias/*` (8)
