# LP Buzzmonitor — buzzsummit-2026-indique-e-ganhe

**Gerado em:** 2026-08-14
**Copy-fonte:** `copy.txt` (colada pelo usuário no chat, estruturada manualmente seguindo o padrão `/lp-preparar`)

## Identidade visual — OVERRIDE explícito

Esta LP **não** usa `brand/buzzmonitor/tokens.json`. Por pedido explícito do usuário, a identidade visual replica a do site oficial do evento (https://www.buzzsummit.com.br/), extraída via inspeção computada do DOM/CSS ao vivo (BuzzSummit é uma sub-marca de evento com identidade própria, distinta da Buzzmonitor institucional):

| Token | Valor | Uso |
|---|---|---|
| Primária | `#EB7C2E` (laranja) | CTAs, ícones de destaque, números |
| Apoio/destaque | `#DE2450` (magenta) | Sub-headlines, links, tags rotacionadas |
| Apoio claro | `#F7AA50` | Badge/eyebrow do hero |
| Dark | `#181818` / `#242424` | Header, footer, 1 seção de contraste ("Sua indicação pode colocar uma marca no palco") |
| Neutro claro | `#F0F3F5` | Fundo alternado |
| Display font | Bebas Neue (Google Fonts) | H1/H2/H3, botões, nav, wordmark |
| Body font | Lato (Google Fonts) | Parágrafos, listas, FAQ |
| Botões | `border-radius: 100px` (pílula) | Todos os CTAs primários |

**Atualização:** o usuário forneceu a logo real do BuzzSummit (mascote raposa + wordmark + "2026"), salva em `assets/logo-buzzsummit.png` (1738×591, PNG com fundo transparente — o wordmark em branco só aparece contra fundo escuro, por isso é imperceptível em preview sobre fundo claro). Substituiu o wordmark tipográfico provisório no header e no footer. Ambos os links continuam apontando para `https://buzzmonitor.com/` (home institucional Buzzmonitor, conforme GUIDELINES §17 — BuzzSummit é organizado pela Buzzmonitor). Favicon **não** foi alterado — continua `brand/buzzmonitor/assets/logos/logo-icon.png`, conforme regra fixa do GUIDELINES §12 (sempre o ícone institucional, nunca um favicon customizado por LP).

## Imagens

- **Hero:** vídeo real embedado — YouTube `zdP9AHn1o1g` (After Movie BuzzSummit 2025), via `youtube-nocookie.com/embed/...`, responsivo 16:9. Testado servindo a LP por HTTP local (o preview via `file://` mostra "Erro 150" — é restrição do YouTube a origens `file://`/`null`, não um problema do embed; funciona normal assim que publicado em domínio https real).
- **Demais imagens** (fotos de speakers, marcas patrocinadoras etc.): nenhuma na copy atual, então nenhum placeholder foi criado. Se o usuário quiser adicionar, precisa de novo ciclo de `/lp-gerar` ou edição direta.
- **Pendência de publicação:** o CSP do domínio de destino (`vercel.json`) precisa liberar `frame-src https://www.youtube-nocookie.com` para o vídeo carregar em produção — conferir no Passo 1.6 da `lp-publicar` (csp_drift_check.py).

## Identidade visual — ajuste de gradiente e layout (pedido do usuário, 2ª rodada)

- **Gradiente principal** trocado de laranja→magenta para **âmbar `#FFB000` → laranja `#FF7300`** (tokens `--grad-start`/`--grad-end`). Usado na seção CTA final (fundo) e nos números da seção "Sua indicação pode colocar uma marca no palco" (texto em gradiente via `background-clip: text`).
- **Seção "Sua indicação pode colocar uma marca no palco"** redesenhada no estilo do print de referência enviado pelo usuário: números/palavras grandes em gradiente âmbar sobre fundo dark, com uma marca geométrica facetada (losango low-poly, decorativa, `aria-hidden`, escondida abaixo de 1100px) no canto direito — inspirada no layout, não é o logo real do BuzzSummit (não temos esse asset).
- Para caber no padrão "número grande + legenda", os 4 itens da seção foram re-quebrados visualmente (ex.: "Líderes" em destaque + "e decisores de marcas e empresas" como legenda) — nenhuma palavra da copy original foi cortada, reescrita ou adicionada, só a quebra de linha/ênfase tipográfica mudou. Sinalizando aqui para o usuário confirmar se prefere o texto corrido como antes.

## Estrutura

1. Hero — headline + 4 parágrafos + CTA primário + link "Entenda como funciona" + placeholder de vídeo
2. Por que indicar — contexto do evento + 4 mini-steps (você indica → time contata → oportunidade avança → você ganha)
3. Quem você pode indicar — grid de 6 personas
4. Por que sua indicação é valiosa — seção de pausa (GUIDELINES §2), sem CTA nem card
5. O BuzzSummit 2026 — chips de data/local/horário + card de tema
6. Sua indicação pode colocar uma marca no palco — seção dark, 4 stats
7. Como funciona o Indique e Ganhe — 4 steps numerados + CTA "Indicar agora"
8. Tem uma empresa em mente — lista de 4 itens + CTA "Quero indicar"
9. Perguntas frequentes — accordion nativo (`<details>`), 6 perguntas
10. CTA final — fundo gradiente laranja→magenta, único form real da LP (nome, e-mail, telefone, empresa indicada, site, mensagem, consentimento)

Único form mock da página vive na seção 10 (`#form-final`), conforme GUIDELINES §10 (MoFu/BoFu — público de rede/parceiros, não tráfego frio de anúncio). Todos os demais CTAs ("Quero indicar uma empresa", "Indicar agora", "Quero indicar") são âncoras que rolam até lá.

## Adições fora da copy literal do usuário (whitelist de compliance/footer)

Marcadas em `copy.txt` com `# [ADICIONADO]`:
- Disclaimer de consentimento + link de política de privacidade no formulário final (no padrão do programa irmão `indiqueeganhe`, Buzzmonitor)
- Linha de copyright no footer

Ajustar o texto do disclaimer se o regulamento oficial do BuzzSummit tiver redação própria.

## Correção anti-IA aplicada

Um único em-dash na copy original ("Centro de Convenções Rebouças — São Paulo") foi substituído por vírgula, conforme tolerância zero de `regras-anti-ia.md`. Sem outros clichês de IA ou filler words encontrados.

## Ajustes de design (3ª rodada, pedido do usuário)

- **Seção "Sua indicação pode colocar uma marca no palco":** removida a forma geométrica decorativa (losango facetado); título e linha de intro centralizados; números/labels da grade também centralizados para harmonizar.
- **Animação/dinamismo geral:** easing mais "elástico" nos reveals (`cubic-bezier(0.22,1,0.36,1)`), cascata escalonada (`transition-delay`) nos itens de cada grid/lista (steps, personas, stats, funciona, mente), entrada animada do hero ao carregar a página, hover com leve elevação + sombra em cards/chips, brilho pulsante contínuo nos botões primários (pausa no hover).
- **Seção "Tem uma empresa em mente?":** redesenhada em 2 colunas (texto + CTA à esquerda, lista de cards à direita); cada item ganhou um selo circular em gradiente com ícone de check, sombra, hover com deslocamento horizontal e entrada animada da esquerda.
- **Seção do formulário (CTA final):** texto de introdução com menos espaçamento entre linhas; `form-card` com padding, gap entre campos e altura da textarea reduzidos — visual mais compacto.

## Ajustes de design (4ª rodada, pedido do usuário)

- **Seção "Por que sua indicação é valiosa":** deixou de ser a seção de "pausa" (texto centrado, sem visual) e virou um layout de 2 colunas — texto alinhado à esquerda + imagem à direita, no mesmo padrão do hero (GUIDELINES §3). **Nota:** a LP ficou sem uma seção de "pausa" dedicada (GUIDELINES §2 recomenda pelo menos 1) — decisão explícita do usuário, mantida sem objeção.
- **Imagem real adicionada:** o usuário enviou `assets/Buzzsummit_2025-5454.jpg` (6000×4000, **18,7 MB** — pesado demais pra web). Gerei uma cópia otimizada em `assets/valiosa-buzzsummit-2025.jpg` (1200×800, ~193 KB, JPEG qualidade 80) e referenciei essa no HTML. **O arquivo original de 18,7 MB continua na pasta `assets/` — recomendo removê-lo antes de commitar** (peso desnecessário no repo); não apaguei por conta própria.

## Ajustes de design (5ª e 6ª rodadas, pedido do usuário)

- **Fundo diversificado por seção:** a LP estava "muito branca". Criadas 2 variantes novas — `.bg-tint` (gradiente estático quase-branco a pêssego, `#FFF6EB`→branco) e `.bg-animated` (gradiente âmbar em movimento lento, `background-position` animado 16s). Aplicadas em "Quem você pode indicar" (`bg-tint`), "O BuzzSummit 2026" (`bg-animated`) e "Perguntas frequentes" (`bg-tint`). O CTA final (`bg-gradient`) também ganhou o mesmo tipo de animação de gradiente (antes estático). O hero ganhou 2 "blobs" radiais âmbar/laranja, borrados e com flutuação lenta (`floatBlob`), atrás do conteúdo. Todas as animações são pausadas globalmente por `prefers-reduced-motion` (regra já existente no arquivo).
- **Hero recentralizado:** o layout deixou de ser 2 colunas (texto esquerda + vídeo direita) e virou 1 coluna centralizada (texto, eyebrow e CTAs centralizados; vídeo abaixo, maior — de ~470px para ~980px de largura no desktop). Isso diverge do padrão do GUIDELINES §3 ("texto à esquerda, visual à direita") — decisão explícita do usuário para esta LP, mantida sem objeção. Ordem no DOM continua com o texto antes do vídeo (mobile não quebra).

## Ajustes de design (7ª rodada, pedido do usuário)

- **Margens laterais reduzidas em telas largas:** usuário mandou print em monitor ultrawide mostrando muito vazio nas laterais. Aumentado `.container` de 1160px → 1320px, e os `max-width` de texto centralizado em todas as seções (hero, section-heads, FAQ, CTA final, "por que valiosa") — texto agora quebra em menos linhas e ocupa mais do espaço horizontal disponível. Vídeo do hero acompanhou (980px → 1100px).

## Retema para escuro-dominante (8ª rodada, pedido do usuário)

O usuário mandou print do site oficial buzzsummit.com.br mostrando que a identidade real é **predominantemente preta/escura com alto contraste** (header, hero, seção de marcas, edições, stats e depoimentos todos dark; só uma seção "Prêmio Diversidade" em roxo/índigo e o painel final "sobre a Buzzmonitor" em branco). A primeira leitura de identidade (baseada em amostragem de CSS computado do site) tinha subestimado essa proporção — a LP estava com fundo branco/off-white dominante e só 1 seção escura.

**Correção aplicada:** praticamente todas as seções de conteúdo passaram a usar fundo escuro (`--dark` #181818 alternando com `--dark-2` #242424 via nova classe `.shade-alt`), texto branco/cinza-claro para texto solto, e as seções que já tinham cards brancos/claros (personas, "como funciona", cards da FAQ... não, FAQ é texto solto — ver abaixo) mantiveram os cards claros com texto escuro por dentro (contraste igual ao dos cards de depoimento do site oficial). A seção "O BuzzSummit 2026" usa uma variante **escura** do gradiente animado (tons de marrom/preto com leve calor âmbar, em vez do gradiente claro anterior). O CTA final continua no gradiente laranja vívido (âmbar→laranja) — esse contraste forte com o resto da página escura é proposital, no mesmo espírito do site oficial.

**Decisão consciente, não implementada:** o site oficial tem uma seção roxa/índigo ("Prêmio Diversidade") — não replicada aqui pra não introduzir uma 4ª cor fora da família laranja/âmbar/preto já estabelecida (mesma lógica do pedido anterior de remover o rosa). Avisar se o usuário quiser esse acento roxo em alguma seção específica.

## Seção "O BuzzSummit 2026" redesenhada (9ª rodada, pedido do usuário)

- Layout deixou de ser 2 colunas (chips à esquerda, card de tema à direita) e virou **tudo centralizado** em coluna única.
- Elementos maiores: chips de data/local/horário (19px, padding maior), card de tema (padding 48px, H3 32px, texto 19-24px).
- **Fundo com foto real**, mais escura: usuário enviou `assets/Buzzsummit_2025-4527.jpg` (6000×4000, 21,5 MB — mesmo problema de peso das imagens anteriores). Gerei `assets/evento-bg-buzzsummit-2025.jpg` (1920×1280, ~270 KB) e apliquei como `background-image` da seção com um overlay escuro (`linear-gradient` preto a ~80% opacidade) por cima — técnica correta pra "escurecer" um fundo sem reduzir a opacidade do texto junto. **O arquivo original de 21,5 MB continua em `assets/`** — mesma recomendação de antes: remover antes de commitar.

## Ícones flutuantes da identidade oficial (10ª rodada, pedido do usuário)

Usuário enviou 3 ícones oficiais da identidade (PNG com fundo transparente): `Buzz Summit 2026 ID (2/3/4).png`. Renomeados para `assets/icon-buzzsummit-id-{2,3,4}.png` (nomes com espaço/parênteses quebram em paths depois — convenção kebab-case do projeto).

Distribuídos flutuando (animação `floatIcon`/`floatIconSlow`, translateY + rotate suave, ~9-12s) em 4 pontos que estavam visualmente vazios:
- **Hero:** ícone 4 (icosaedro), lateralizado à direita, ~130px.
- **Por que indicar:** ícone 3 (cubo empilhado), canto inferior esquerdo, ~110px.
- **Sua indicação pode colocar uma marca no palco:** ícone 2 (losango facetado — o mesmo motivo que eu tinha recriado à mão em SVG e depois removido a pedido do usuário; agora é o asset real), lateralizado à direita, ~150px.
- **Como funciona:** ícone 4 de novo, canto superior esquerdo, ~100px.

Escondidos abaixo de 1100px de viewport (`display:none`) — em telas estreitas não sobra espaço lateral pra flutuar sem sobrepor o conteúdo. Todos com `aria-hidden="true"` e `alt=""` (puramente decorativos), `pointer-events:none`, respeitam `prefers-reduced-motion` (regra global já existente pausa a animação).

## Gradiente da marca + logo + ícones (11ª rodada, pedido do usuário)

- **Gradiente `#FFB000 → #FF7300`** aplicado em todo elemento preenchido e texto em negrito/destaque que antes era laranja sólido: botões primários (`.btn-primary`, com hover via `filter: brightness()` em vez de trocar a cor, pra não perder o degradê), círculos numerados dos steps, sub-headlines em negrito, números grandes ("Como funciona"), o texto destacado "Ganhe 1.000 reais..." no hero, e os ícones SVG da seção "Quem você pode indicar" (via `<linearGradient>` compartilhado no SVG, referenciado com `stroke="url(#iconGrad)")`. **Bordas finas, links de texto pequenos e o "+" do FAQ ficaram na cor sólida `--accent`** (que já é a ponta escura do próprio degradê) — um degradê não fica visível em traços finos. Nenhuma imagem/PNG foi alterada (pedido explícito do usuário).
- **Logo (header e rodapé):** aumentada em 15% (nav 40px → 46px de altura; rodapé 48px → 55px). Link trocado de `buzzmonitor.com` para **`https://www.buzzsummit.com.br/`** (site oficial do evento) — desvio da regra padrão de "logo linka pra home da marca" (GUIDELINES §17), decisão explícita do usuário pra esta LP.
- **Ícones flutuantes:** os 4 (hero, "por que indicar", "palco", "como funciona") aumentados em 15% (130→150px, 110→127px, 150→173px, 100→115px).

## Estado

- [x] HTML gerado
- [x] Vídeo do hero (After Movie 2025) — embed real do YouTube
- [x] OG image 1200×630 → `assets/og-buzzsummit-2026-indique-e-ganhe.png` (gerada via Chrome headless na `/lp-revisar`; fonte fallback, ver REVISAO.md)
- [x] Revisão (`/lp-revisar`) — 8 críticos corrigidos (contraste AA + OG image + sync copy.txt), ver `REVISAO.md`
- [x] Formulário integrado — Jotform (242464989976077, "BR | Comercial | Indique e Ganhe"), 2026-08-17
- [ ] Domínio de destino a definir — provável candidato: `evento.buzzmonitor.com` (guarda-chuva de eventos presenciais Buzzmonitor + Buzzcreators), mas não decidido ainda
- [x] Publicado (modo solo) — https://buzzmonitor-lp-buzzsummit-2026-indi.vercel.app/buzzsummit-2026-indique-e-ganhe (2026-08-17). Sem domínio próprio ainda; rodar `/lp-publicar buzzmonitor buzzsummit-2026-indique-e-ganhe {dominio}` quando tiver um.

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- Google Fonts: Bebas Neue, Lato
- GTM: `GTM-WFJVK858` (container Brasil, `brand/buzzmonitor/tracking.json`)
