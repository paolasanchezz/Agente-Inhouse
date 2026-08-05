# LP Buzzmonitor — plataforma-completa-monitoramento

**Gerado em:** 2026-07-23
**Copy-fonte:** `copy.txt` (output de /lp-preparar, revisado via /copy-revisar, renomeado de `monitoramento-manual`)
**Uso:** Campanha Meta Ads (MoFu) — Dor 1 (monitoramento manual, sem ferramenta)

## Estrutura

- HEADER (logo + CTA com `.btn-glow`)
- HERO (overline + H1 + sub + CTA + ilustração SVG nova: pessoa desesperada no computador cercada pelos logos de Instagram/Facebook/X/WhatsApp/LinkedIn/TikTok — refeita em 2026-07-24, Bloom estava sem créditos)
- PROBLEMA (lista vertical, 5 itens com ícones e cores variadas — refeita em 2026-07-24; ícone do 1º item trocado por lupa e alinhamento corrigido em 2026-07-29)
- SOLUCAO (redesenhada em 2026-07-29: fundo `.bg-gradient` animado, título/subtítulo centralizados, grid de 6 cards com ícone SVG + título curto; imagem `monitoramento-2.png` removida)
- DESTAQUE-IA (texto reescrito em 2026-07-24 replicando referência do usuário; mantém o GIF de demonstração à direita)
- INSIGHTS (seção nova em 2026-07-24, layout espelhado: imagem `insights.png` à esquerda, texto à direita)
- GESTAO-DE-CRISE (seção nova em 2026-07-29, colunas invertidas — texto à esquerda, imagem à direita —, visual em camadas `crise-1.png` + `crise-2.png`)
- PARA-QUEM (fundo `.bg-aurora` só com spots de luz, sem preto — cores laranja/roxo/rosa do brandbook, ajustado em 2026-07-29; lista simples sem cards)
- PROVA (case Caffeine Army, cards de métricas com números em gradiente; frase "a marca ouviu o cliente" em negrito desde 2026-07-29)
- CASES (seção nova em 2026-07-29, após PROVA: 4 cards com dados reais de clientes — Oi, Betnacional, Grupo Casas Bahia, Camil)
- CTA-FINAL (fundo gradiente roxo→laranja, embed real Jotform)
- LOGO-WALL (imagem completa `logo-wall.png` desde 2026-07-29 — substituiu a versão recriada em HTML com stats + wordmarks)
- DEPOIMENTOS ("Ainda não está convencido?") — **PENDENTE**, ver Pendências
- FOOTER (logo invertido + copyright)

## Estado

- [x] HTML gerado
- [x] Revisão (frontend-design review + web-design-guidelines) — ver `REVISAO.md` (6 críticos + 7 melhorias + 3 nice-to-haves, todos aplicados)
- [x] Formulário integrado — **Form provider:** Jotform (integrado em 2026-07-23)
- [x] Publicado — `https://buzzmonitor-lp-plataforma-completa.vercel.app/plataforma-completa-monitoramento` (republicado em 2026-07-29, 2 rodadas: (1) botões `.btn-glow`, SUB da hero, ícone da Problema, Solução redesenhada, Gestão de Crise nova, aurora na Para-Quem, Logo-Wall em HTML; (2) CTAs padronizados, aurora sem preto, negrito no Caffeine Army, seção Cases nova, Logo-Wall trocada por imagem completa)
- [ ] Seção de depoimentos ("Ainda não está convencido?") — aguardando o usuário reenviar o texto completo dos 3 depoimentos
- [ ] Domínio `conteudo.buzzmonitor.com` — já atribuído ao projeto Vercel, mas DNS ainda não configurado (ver Pendências). Publicado por ora no domínio de fallback.

## Pendências

- **DNS de `conteudo.buzzmonitor.com`:** domínio já vinculado ao projeto Vercel (`vercel domains add`), mas não resolve externamente. Falta criar o registro `A conteudo.buzzmonitor.com 76.76.21.21` no provedor de DNS da Buzzmonitor (fora do escopo da Vercel/desta skill). Até lá, a LP segue publicada em `https://buzzmonitor-lp-plataforma-completa.vercel.app/plataforma-completa-monitoramento`.
- **Depoimentos:** falta o texto exato das citações de José Manuel López (Publicis Groupe — só tenho o início truncado), Pablo Ferrer (McCANN) e David Díaz (VMLY&R). Não fabricado por serem falas atribuídas a pessoas reais — aguardando o usuário reenviar.
- Sugestão de copy ainda pendente (marcada no `copy.txt`): o claim "O lançamento foi um sucesso porque a marca ouviu o cliente" (seção PROVA) não está confirmado no case verificado do BRANDBOOK.
- Placeholders `{{DOMAIN}}`, `{{OG_IMAGE_PATH}}` e `{{BRAND_LOGO_PNG_PATH}}` no `index.html`-fonte são resolvidos automaticamente pelo `lp-publicar` a cada republicação (atualmente resolvidos para o domínio de fallback `.vercel.app`).

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer, `filter: brightness(0) invert(1)` não necessário pois o SVG já é a versão invertida)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `./assets/destaque-ia.webp` (LP-local, 960×540, ~1.8 MB, 93 frames — versão comprimida, servida via `<picture><source type="image/webp">`) e `./assets/destaque-ia.gif` (fallback pra navegadores sem suporte a WebP animado, 960×540, ~2.9 MB, 186 frames, original fornecido pelo usuário). Compressão: WebP quality=90 + frame-rate reduzido pela metade (duração de cada frame dobrada pra manter a mesma duração real da animação) — 38,6% menor mantendo resolução e qualidade por frame altas.
- Hero visual é 100% SVG inline (formas geométricas + gradiente da marca + glyphs dos 6 apps), pois a Buzzmonitor não tem mascote fixo. Substituiu o mockup CSS anterior em 2026-07-24.
- `./assets/og-plataforma-completa-monitoramento.png` (1200×630, ~47 KB, gerada via Chrome headless a partir de `./assets/og-source.html` durante a revisão de 2026-07-23).
- `./assets/insights.png` (1920×1080, ~0,45 MB; fornecida pelo usuário via Google Drive) na seção INSIGHTS.
- `./assets/crise-1.png` (620×380, "Distribuição de reações" — gráfico de pizza) e `./assets/crise-2.png` (551×355, "Top 5 tags mais frequentes" — gráfico de barras), ambas fornecidas via Google Drive em 2026-07-29, usadas em composição de camadas na seção GESTAO-DE-CRISE.
- `./assets/logo-wall.png` (1912×690, ~0,26 MB; fornecida pelo usuário via Google Drive em 2026-07-29) — imagem completa da seção LOGO-WALL (título + stats + grade de logos reais de clientes), substituindo a versão recriada em HTML.
- `./assets/monitoramento-2.png` **removida da seção SOLUCAO em 2026-07-29** (imagem ainda existe no disco/sibling mas não é mais referenciada pelo HTML — pode ser removida do repo se não for reaproveitada).

## Validações rodadas

- em-dash no HTML: 0 ocorrências
- Tags `og:`: 10 (>= 8 exigido)
- Tags `twitter:`: 4 (>= 4 exigido)
- `meta description`: 1
- JSON-LD: parseia como JSON válido, `Organization.url`/`sameAs` batem com `brand-manifest.json`
- Fidelidade de copy: todo texto visível confere literal com `copy.txt` (verificado via `get_page_text` e `read_page` no navegador)
- Logos SVG sem `<text>` vivo (grep confirmou 0 em todos os 3 arquivos) — seguros pra usar sem risco de fonte serifada
- GTM: `status: ok` (3/3 tokens confirmados no live: `gtm.js`, `ns.html`, `GTM-WFJVK858`), container bate com a região brasil
- Contraste WCAG AA: 6 falhas encontradas e corrigidas na revisão de 2026-07-23 (ver `REVISAO.md`). **Reintroduzida 1 falha em 2026-07-29:** botão `.btn-primary` voltou a usar texto branco sobre fundo laranja (~2.82:1, abaixo do 4.5:1 exigido para texto normal) — mudança pedida explicitamente pelo usuário, revertendo o fix de contraste da revisão anterior.
- Deploy 2026-07-29: 7/7 headers de segurança presentes; hash do live bate com o source local (drift-check + smoke test); assets `crise-1.png`/`crise-2.png` confirmados servidos (HTTP 200, PNG válido) via curl.
