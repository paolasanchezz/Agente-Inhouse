# LP Buzzmonitor — plataforma-completa-atendimento

**Gerado em:** 2026-08-06
**Copy-fonte:** `copy.txt` (transcrito da página Notion "Copy LP da dor 3 - Atendimento descentralizado", editada pelo usuário a partir do rascunho de `/lp-preparar` — ver `copy.txt.2026-08-05.bak` para a versão anterior)
**Domínio-alvo:** `content.buzzmonitor.com/plataforma-completa-atendimento` (guarda-chuva migrado ao CI, ver `landing-pages/dominios/MIGRADOS.json`)
**LPs irmãs de referência de estrutura:** `landing-pages/buzzmonitor/plataforma-completa-monitoramento/` (Dor 1) e `landing-pages/buzzmonitor/plataforma-completa-para-dados/` (Dor 2), mesmo guarda-chuva
**Inspiração de cores/clima explícita do usuário:** `landing-pages/buzzmonitor/plataforma-integral-social-media/` — paleta navy `#081b3a` + laranja `#ff6b16` + rosa `#ec174c`, cards com hover-lift e reveal em cascata (deliberadamente diferente da paleta roxo/laranja das LPs irmãs deste guarda-chuva, a pedido do usuário)

## Estrutura

- HEADER (logo + CTA "Demonstração gratuita")
- HERO — H1/SUB/CTA + imagem real (`assets/hero.jpg`, enviada pelo usuário via Google Drive)
- PROBLEMA — H2 + lede + lista de 7 itens (X vermelho) + fechamento; vídeo em loop ao lado (`assets/problema.mp4` — arquivo era MP4, não GIF; embutido como `<video loop muted playsinline>`, autoplay controlado via JS respeitando `prefers-reduced-motion`, ver REVISAO.md 2ª rodada)
- SOLUCAO — H2 (título em degradê laranja/rosa) + fila de 15 ícones de canais (SVG inline, sobre caixa laranja bem claro `#fff1e6`; 5 ícones redesenhados em 2026-08-11 por estarem distorcidos: Threads, Bluesky, TikTok, WordPress, Pinterest) + grid de 6 feature cards + fechamento em gradiente + CTA
- IA COMO DIFERENCIAL — recriação em HTML do infográfico fornecido pelo usuário: título em maior destaque; layout de 2 colunas — **galeria de 5 imagens reais à esquerda** (soltas, não vinculadas a uma etapa específica, rola de forma independente) e **timeline vertical de 8 etapas à direita** (ícone + texto, compacta, como no design original); 2 etapas em destaque visual (5 e 8, ambas "Seu time...") com uma tag "Seu time só entra aqui" ancorada acima do ícone + seta orgânica (curva bezier) saindo do ícone em direção à tag; 3 callouts conectados visualmente à etapa 5 (branch com conector dashed); banner de fechamento só com a frase (sem logo) + CTA
- CASES — 4 cards horizontais alternando o lado do bloco colorido, todos os degradês em laranja/rosa; logomarcas reais dos 4 clientes (Youse, 14bits, Herval, E-CLIK) em branco 100% via `filter:brightness(0) invert(1)`, sem fundo/badge atrás
- LOGO-WALL — **pendente** (ver Pendências), reservado como comentário HTML sem conteúdo inventado
- CTA-FINAL — fundo gradiente navy→rosa, form real Jotform (embed `jsform/252995108251662`)
- FOOTER (logo invertido + copyright)

## Estado

- [x] HTML gerado (`index.html`, ~660 linhas)
- [x] Fidelidade de copy conferida: contagem de itens por seção bate com `copy.txt` (7 problema, 15 ícones de canal, 6 features, 8 etapas da timeline, 3 callouts, 4 cases) — nenhum texto inventado fora da whitelist (labels de formulário, aria-labels, skip-link, copyright)
- [x] Checklist técnico/SEO: em-dash literal 0, `meta description` 1, `og:` 10 tags, `twitter:` 4 tags, JSON-LD parseia como JSON válido, GTM `GTM-WFJVK858` injetado 2x (head + noscript pós-body)
- [x] Logos validados web-safe (`grep -c '<text'` = 0 em `logo-primary.svg` e `logo-reversed.svg`)
- [x] Header/footer: logo linka para `https://buzzmonitor.com/` (não `/`), `target="_blank" rel="noopener"`, aria-label localizado
- [x] Reveal-on-scroll com fallback `<noscript>` (`.reveal{opacity:1!important}`) e `prefers-reduced-motion` global
- [x] Formulário integrado — **Form provider:** Jotform (`jsform/252995108251662`, integrado em 2026-08-06 a pedido direto do usuário, antes da revisão formal — wrapper CSS canônico `.jotform-embed iframe` aplicado, sem card duplicado)
- [x] OG image 1200×630 → `assets/og-plataforma-completa-atendimento.png` (~93 KB, gerada em 2026-08-07 via Chrome headless a partir de `assets/og-source.html`, ver `render_og.py`)
- [x] Revisão (`frontend-design` review + `web-design-guidelines` + GTM + fidelidade de copy + SEO) — rodada em 2026-08-07, ver `REVISAO.md` (7 críticos aplicados, 1 crítico sinalizado pendente de decisão sua sobre contraste dos botões, 3 melhorias + 1 nice-to-have opcionais)
- [x] Mídia real integrada (2026-08-11) — hero, vídeo da seção problema e 5 imagens da timeline, todas enviadas pelo usuário via Google Drive, redimensionadas/otimizadas antes de entrar no repo (ver Assets referenciados)
- [x] Logomarcas reais dos 4 clientes nos cases (2026-08-11) — Youse Seguros, 14bits, Grupo Herval, E-CLIK (marca da crm bonus, confirmado pelo usuário), todas em branco 100% sem fundo
- [x] 2ª revisão (2026-08-11) — ver `REVISAO.md`: 1 crítico novo aplicado (vídeo da seção problema não respeitava `prefers-reduced-motion` + faltava dimensão intrínseca), críticos da 1ª rodada reconfirmados sem regressão, 5 melhorias + 1 nice-to-have opcionais, 1 crítico ainda pendente de decisão sua (contraste dos botões)
- [ ] Publicado — rodar `/lp-publicar buzzmonitor plataforma-completa-atendimento content.buzzmonitor.com`

## Pendências

- **Contraste dos botões (crítico sinalizado na revisão, não aplicado):** texto branco sobre o degradê laranja→rosa dos `.btn-primary` fica abaixo do AA em parte do gradiente (~2.85:1 na ponta laranja). Ver `REVISAO.md` para os números completos e as 2 opções de correção — decisão sua, mesmo padrão já aceito conscientemente na LP irmã `plataforma-completa-monitoramento`.
- **Logomarcas dos cases:** as 4 aplicadas em 2026-08-11 (Youse Seguros, 14bits, Grupo Herval e E-CLIK, arquivos enviados pelo usuário via Google Drive, ver Assets). Youse e 14bits já vinham com fundo transparente; Herval veio em JPEG com fundo branco, convertido para PNG com transparência (heurística de distância da cor branca, sem numpy disponível no ambiente). O arquivo do case E-CLIK mostra a marca "crm bonus" — confirmado pelo usuário que é intencional (E-CLIK é uma marca da crm bonus, e eles querem usar essa logo).
- **LOGO-WALL:** copy.txt reserva a seção mas não define conteúdo (nota: "reaproveitar asset das LPs irmãs"). Como o asset `logo-wall.png` das irmãs é específico da Dor 1/2 (clientes daquele contexto), decidi **não** reaproveitar automaticamente sem confirmação — a seção está como comentário HTML vazio (`<!-- LOGO-WALL: aguardando asset final -->`) entre CASES e CTA-FINAL, sem quebrar o layout. Confirmar com o usuário se é para reaproveitar o mesmo `logo-wall.png` ou gerar um novo.
- **Galeria de imagens da timeline:** por pedido do usuário (2026-08-11), as 5 imagens não estão mais vinculadas a etapas específicas — viraram uma galeria solta na coluna esquerda da seção, independente da timeline (que voltou a ocupar a coluna direita, compacta, como no design original).
- **Ícones de "gif" nas 8 etapas da timeline e nos 3 callouts:** continuam sendo ícones SVG com animação CSS leve (não há imagem/gif real fornecida associada a cada etapa individualmente, já que as 5 imagens agora vivem na galeria solta).
- **Ícones de canal (fila de 15):** construídos como SVG inline simplificado (glifo + cor de marca), não são os logotipos oficiais pixel-perfect de cada rede. 5 deles (Threads, Bluesky, TikTok, WordPress, Pinterest) foram redesenhados em 2026-08-11 por estarem distorcidos/pouco reconhecíveis — os outros 10 (Facebook, Instagram, YouTube, WhatsApp, LinkedIn, E-mail, Reclame Aqui, Reddit, Google Play, Google Meu Negócio) não foram alterados. Se algum ainda não estiver bom, avisar qual.
- **Números em destaque nos blocos coloridos dos cases** ("36h → 3h", "+220%", "100% · 142 lojas", "1 hora"): são restatements visuais dos mesmos números já literais no `<h3>` de cada case (ex: "SLA reduzido de 36 horas para 3"), não texto/claim novo.
- **Filler word "realmente"** (seção SOLUCAO, fechamento): foi sinalizada como sugestão anti-IA numa rodada anterior do `/lp-preparar` e o usuário manteve o texto ao editar no Notion — mantido literal, não é mais uma pendência de revisão.
- **Botão do header:** texto pedido pelo usuário veio como "Demonstração gratutia" — corrigido silenciosamente o typo para "Demonstração gratuita" (mesma grafia usada no resto da página).

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `./assets/og-plataforma-completa-atendimento.png` (OG image 1200×630, gerada via `./assets/og-source.html` + `./assets/render_og.py`, Chrome headless)
- `./assets/hero.jpg` (imagem da seção HERO, enviada pelo usuário via Google Drive; original 1672×941 PNG 1,4 MB, redimensionada para 900px de largura + convertida para JPEG q90 → 105 KB)
- `./assets/problema.mp4` (vídeo em loop da seção PROBLEMA, enviado pelo usuário como "GIF" mas era um MP4; usado como `<video autoplay loop muted>` para o mesmo efeito visual sem gerar um GIF real gigante; 2,4 MB, mantido no tamanho original)
- Galeria solta da seção IA COMO DIFERENCIAL (coluna direita, não vinculada a etapas específicas — ver Pendências): `./assets/etapa-2.webp` (387×320, 8 KB), `./assets/etapa-3.gif` (original 960×540 250 frames 6,7 MB, redimensionado para 480×270 → 1,65 MB), `./assets/etapa-4.png` (original 2160×2160 439 KB, redimensionado para 720×720 → 104 KB), `./assets/etapa-5.png` (original 1920×1080 473 KB, redimensionado para 720×405 → 126 KB). O `etapa-1.gif` foi removido a pedido do usuário em 2026-08-11.
- Logos de clientes na seção CASES: `./assets/logo-youse.png` (897×500, fundo transparente original), `./assets/logo-14bits.png` (210×93, fundo transparente original), `./assets/logo-herval.png` (230×110, convertido de JPEG com fundo branco para PNG com transparência), `./assets/logo-eclik.png` (430×340, fundo branco opaco original — funciona bem porque o badge branco atrás de cada logo já cobre esse caso)
- Ícones de canal, timeline (8 etapas) e callouts continuam 100% SVG/CSS inline
