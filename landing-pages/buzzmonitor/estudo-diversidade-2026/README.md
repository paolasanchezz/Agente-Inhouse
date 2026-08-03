# LP Buzzmonitor — Estudo Diversidade 2026

**Gerado em:** 2026-07-01 (refeito — estética mosaico multicolor)
**Copy-fonte:** `copy.txt` (mantida da versão anterior, já revisada anti-IA)
**Região:** brasil (pt-BR) · **GTM:** GTM-WFJVK858

## Estrutura

- Hero (overline + H1 multicolor + sub + CTA "Baixe agora" → scroll para form) + mosaico
- Destaque (seção-pausa, off-white): "Você se sente representado na publicidade?" + 2 parágrafos
- Achados (mosaico de 6 cards coloridos): "O que os dados revelam"
- Prêmio (seção escura roxo): Buzz Summit 2026 + 5 categorias em chips
- Por que importa (seção-pausa) + arte mosaico 2×2
- CTA final (gradiente rosa→laranja): "Faça parte da transformação" + form mock
- Footer

## Direção de design

Estética **mosaico multicolor** (referências aprovadas pela cliente: "People first" / Instituto Transformar / cápsulas de retratos). Formas geométricas da marca (asterisco, sunburst, arco) intercaladas com fotos reais. Achados full-color (pluralidade = conceito); Prêmio escuro para drama; seções de texto arejadas.

**Revisão do hero (2026-07-01, pedido da cliente):** o hero original tinha H1 com palavras em cores diferentes (arco-íris) + mosaico de blocos. A cliente não gostou do texto multicolor e pediu um hero estilo banner (referência fintech anexada). Novo hero: foto grande `header.jpg` (grupo de 6 pessoas) + H1 **numa cor só** (roxo) sobre gradiente suave + asterisco/sunburst flutuantes. O mosaico de rostos migrou para a seção "Por que importa" (vitrine "People first" com os 8 retratos reais + 4 tiles de forma).

## Decisões registradas (validar na revisão)

1. **Fotos reais (2026-07-01):** a cliente enviou 8 retratos + `header.jpg`, todos em `./assets/`. `header.jpg` no hero; os 8 retratos no mosaico "Por que importa" (`.faces`). Placeholders SVG de silhueta removidos. Elenco cobre os grupos do estudo (negros, indígena, PCD/cadeirante, vitiligo, plus-size, idosa). Alt genérico e respeitoso em cada `<img>`.
2. **Em-dash → parênteses:** a `copy.txt` tinha 2 em-dashes no parágrafo "retrato potente — e às vezes desconfortável —"; o próprio comentário anti-IA da copy mandava trocar por parênteses (GUIDELINES §5, tolerância zero). Aplicado: "retrato potente (e às vezes desconfortável) sobre a evolução (e as lacunas)". `grep -c "—"` = 0.
3. **Posição do form (§10):** material rico / lead magnet tende a ToFu (form 2ª seção). Aqui a copy estrutura o form no **CTA final** + CTA do hero com scroll âncora até ele. Mantida a estrutura da copy; se quiser testar form mais acima, é override documentável.

## Estado

- [x] HTML gerado (estética mosaico) + validado (anti-IA 0 em-dash, SEO completo, GTM 2 blocos, JSON-LD OK, 6 achados, 5 chips)
- [x] Hero refeito (foto `header.jpg` + H1 cor única) — pedido da cliente
- [x] Fotos reais (8 retratos + header) integradas em `./assets/`
- [x] Foto do hero trocada (2026-07-30) — nova `header.jpg`; antiga preservada em `assets/header-old-backup.jpg`
- [x] Conteúdo atualizado com dados reais da 8ª edição (2026-07-30) — fonte: `Diversidade-na-Comunicação_2026 - Ano Base 2025_6.pdf` (SA365 + Elife + Buzzmonitor, 10.229 posts, 261 perfis, 20 anunciantes, jan/25-jun/26). Números antigos ("mais de 6 mil publicações", achados genéricos de "avanço") substituídos por estatísticas reais, inclusive quedas onde os dados mostram queda (idosos, negros, LGBTQIAPN+, PcDs, pessoas gordas)
- [x] Revisão (frontend-design review + web-design-guidelines) — rodada 2026-08-03, 3 críticos corrigidos (em-dash x2, contraste do overline), ver `REVISAO.md`. 1 decisão pendente (seção Quiz fora da copy.txt original — flagada, não removida)
- [x] OG image (1200×630) — já existe em `assets/og-image.png`, dimensões conferidas (1200×630)
- [x] Publicado (2026-08-03) em `material.buzzmonitor.com/estudo-diversidade-2026` (guarda-chuva CI)
- [x] Formulário integrado (2026-08-03) — Jotform (form `262024846121045`), form mock trocado por embed real. **Form provider:** Jotform (2026-08-03)
- [ ] **Thank You URL do Jotform** — configurar no builder do form (jotform.com) para redirecionar para `https://material.buzzmonitor.com/estudo-diversidade-2026-obrigado` (thanks page já publicada, ver `../estudo-diversidade-2026-obrigado/`). Configuração feita na plataforma do Jotform, não no repo.
- [x] Cadência de e-mail criada — `conhecimento/copywriting/criacao/buzzmonitor/2026-07-20/cadencia-email-estudo-diversidade-2026/cadencia.md` (6 e-mails: convite + 3 repiques + convite 2 + convite 3; sem oferta, termina no material)

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)

> Nota: no preview local (`python -m http.server` na pasta da LP) as logos aparecem quebradas porque `../../brand/` sobe acima da raiz servida. Resolve no deploy — a `lp-publicar` reescreve os paths para `/assets/...`.
