# LP Buzzmonitor — black-friday-sem-caos

**Gerado em:** 2026-10-08
**Copy-fonte:** `copy.txt` (briefing passado pela Catharina em chat, sem roteiro formal)

## Estrutura

- HERO (título "Black Friday sem caos." + tagline + dor + ticket com countdown real)
- PROBLEMA (stat em destaque: case Caffeine Army + 4 itens de dor)
- DIFERENCIAL (vídeo-mockup do webinar + conceito)
- PROGRAMA (6 cards "o que você vai levar", último destacado)
- PARA QUEM É (5 perfis, lista numerada)
- URGÊNCIA (fundo escuro, vagas limitadas)
- CTA FINAL / INSCRIÇÃO (form Jotform real, já integrado)
- FOOTER

Visual segue o mesmo sistema de design das últimas LPs de webinar Buzzmonitor (`da-collab-a-receita-setembro-2026`, `gestao-de-crises-ia-agosto-2026`) — mesma paleta, tipografia, classes CSS e componentes (ticket card, countdown, learn-grid, for-visual SVG reaproveitado).

## Estado

- [x] HTML gerado
- [x] Formulário integrado (Jotform 252154974852667, embed real — decisão da Catharina, sem mock)
- [ ] OG image 1200×630 → `assets/og-black-friday-sem-caos.png` (arquivo **único** — nunca também `og-image.png`)
- [ ] Revisão (`frontend-design` review + `web-design-guidelines`) — rodar `/lp-revisar buzzmonitor/black-friday-sem-caos`
- [ ] Publicado — rodar `/lp-publicar buzzmonitor black-friday-sem-caos webinar.buzzmonitor.com`

## Pendências conhecidas

- Duração do evento assumida em 60 min (não confirmada pela Catharina)
- Sem palestrante definido — seção "quem conduz" omitida de propósito
- Confirmar se o formulário Jotform 252154974852667 está de fato configurado pra enviar as respostas pra planilha certa (mesmo form reaproveitado de outros webinars)

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon + avatar do mockup de vídeo)

## Redesign 2026-10-19

Visual refeito com a estética dos criativos do webinar (Barlow Condensed + Hanken Grotesk, cores chapadas da marca, adesivo "sem caos.", celular com comentários subindo, atendente com balões de notificação). Copy, formulário Jotform, SEO e GTM inalterados. Assets novos com prefixo `bfsc-` (namespace no `/assets/buzzmonitor/` do guarda-chuva).
