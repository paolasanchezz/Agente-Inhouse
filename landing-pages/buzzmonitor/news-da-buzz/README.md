# LP Buzzmonitor — news-da-buzz

**Gerado em:** 2026-07-21
**Copy-fonte:** `copy.txt` (escrita diretamente para este pedido, a partir do briefing da Catharina + banner real da newsletter + memória do conteúdo das edições recentes; não veio de Notion)
**Região/idioma:** brasil / pt-BR · **GTM:** GTM-WFJVK858 · **Domínio previsto:** material.buzzmonitor.com (guarda-chuva, migrado pro deploy via CI)

## Estrutura

- HERO — masthead com a imagem real da newsletter (recortada, `assets/newsletter-preview-cropped.png`) + overline com ícone + H1 (agora o antigo texto de valor, sem abertura pela dor, decisão explícita da Catharina em 2026-07-21) + CTA, com ilustração animada de um laptop recebendo um e-mail ao lado (CSS/JS puro, sem imagem/vídeo externo)
- ASSINATURA (2ª seção, form ToFu conforme GUIDELINES §10) — form mock (Nome, E-mail) + CTA + disclaimer
- PROBLEMA — lista vertical de 4 dores com ícone X
- O QUE VOCE RECEBE — fundo roxo (primary), grid de 4 cards brancos flutuando com ícone check
- DIFERENCIAL — fundo laranja (secondary), seção de pausa (só título + parágrafo, texto escuro pro contraste)
- PARA QUEM — grid 2x2, fundo branco
- CTA FINAL — fundo escuro (primary), CTA claro
- FOOTER

**Revisão de design 2026-07-21 (pedido da Catharina):** a seção PROVA (mockup "prévia real" mais abaixo na página) foi removida — a imagem real da newsletter subiu pro topo do hero, recortada pra tirar o espaço em branco que sobrava embaixo (bbox original: conteúdo até y=1386 de 1890px; recorte final 3780×1426). O H1 antigo ("Toda semana sai uma ferramenta de IA nova...") foi removido; o texto que era SUB virou o novo H1. O overline trocou de "Newsletter gratuita da Buzzmonitor · toda semana" pra "Toda semana, na sua caixa de entrada", com um ícone de envelope e um pill com gradiente suave (mais "bonito" conforme pedido).

**Ajuste 2026-07-21 (2ª rodada):** masthead aumentado (640px → 860px de largura máxima), com glow degradê suave atrás pra reforçar o centro visual, e animação de entrada (fade + leve escala ao carregar) seguida de flutuação contínua sutil (desliga em `prefers-reduced-motion`).

**Ajuste 2026-07-21 (3ª rodada):** a pedido da Catharina, adicionadas 2 seções coloridas pra tirar o "tudo branco" — O QUE VOCE RECEBE virou fundo roxo (primary, cards brancos flutuando) e DIFERENCIAL virou fundo laranja (secondary, texto escuro pra manter contraste AA). Evitei colocar o roxo em PARA QUEM (ficaria colado no CTA FINAL, que já é roxo escuro, e os dois se fundiriam num bloco só) — por isso o roxo foi pro bloco de benefícios, que fica isolado entre a seção cinza de problema e a laranja de diferencial.

**Ajuste 2026-07-21 (4ª rodada):** nova seção COMPARATIVO (tabela "sem x com a News da Buzz", pedido da Catharina) inserida entre PROBLEMA e O QUE VOCE RECEBE — 4 pares de linha, coluna "sem" à esquerda e "com" à direita, seta central, com stagger de entrada (cada linha revela com delay crescente) e fallback completo pra no-JS/reduced-motion. Copy nova (não existia em `copy.txt` antes desta rodada).

**Ajuste 2026-07-21 (5ª rodada, feedback sobre a tabela e a seção laranja):**
- Tabela COMPARATIVO: rótulos das colunas perderam o fundo em pill (viraram só ícone + texto); coluna "sem" mudou de rosa pra cinza apagado (`--n-100`/`--n-700`, sem destaque); coluna "com" ganhou fundo em degradê (teal escuro → roxo primary) com texto branco, "mais chamativo"; bordas removidas dos dois lados; overline "Duas rotinas, dois resultados" removido.
- Seção DIFERENCIAL: o fundo laranja com glow (rodada 3) foi considerado feio pela Catharina. Trocado por fundo branco, título com texto em degradê (gradiente roxo→laranja via `background-clip:text`, com fallback sólido roxo pra navegadores sem suporte) e corpo em preto (`--n-900`). Alinhamento mudou de centralizado pra à esquerda, e o container voltou a usar a largura cheia (1180px) em vez do recorte de 820px — isso alinha o título/parágrafo com a mesma margem esquerda de BENEFICIOS e PARA QUEM, corrigindo o desalinhamento que a Catharina notou.

**Ajuste 2026-07-21 (6ª rodada):** a pedido da Catharina, toda vez que "News da Buzz" aparece em um título (H1/H2), o texto vira o lettering real da imagem enviada por ela, inline com o resto da frase. Gerado `assets/news-da-buzz-wordmark.png`: recorte automático (Python/Pillow, análise de bounding-box por densidade de pixel) do banner original, isolando só "News da Buzz" + os 3 tracinhos laranja (sem a raposa, sem a frase "O seu resumo semanal..."), com fundo tratado pra transparência (feather de alpha na faixa quase-branca, pra não deixar halo em fundo branco/cinza claro). Aplicado via `<img class="wordmark-inline">` (`height:0.85em`, escala com o tamanho da fonte do título) em 3 lugares: HERO H1, PROBLEMA H2 e PARA QUEM H2 — os únicos títulos que citam "News da Buzz" literalmente. `alt="News da Buzz"` preserva o texto pra acessibilidade/SEO. CTA, footer e rótulos da tabela comparativa continuam em texto puro (não são "título").

**Ajuste 2026-07-21 (7ª rodada):** 2 correções na tabela COMPARATIVO.
- **Bug de alinhamento do rótulo "Com a News da Buzz":** `.compare-table__labels` é um grid de 3 colunas (`1fr auto 1fr`) mas só tinha 2 elementos filhos, então o navegador auto-posicionava o 2º rótulo na coluna do meio (a `auto`, reservada pra seta) em vez da 3ª coluna — por isso ele aparecia deslocado à esquerda dos cards da coluna "com". Corrigido com `grid-column:1` / `grid-column:3` explícitos nos dois rótulos.
- **Cor do degradê:** a coluna "com" usava teal→roxo; trocado pra roxo→laranja (`var(--primary)` até 68%, transicionando pra `var(--secondary)` nos últimos 32%, diagonal 120deg) conforme pedido. Mantive a maior parte do card em roxo (não 50/50) porque o laranja da marca sozinho (#EB7C2E) não passa no contraste AA com texto branco (~2.8:1); concentrando o laranja só no canto final, o texto (alinhado à esquerda) sempre cai na zona roxa seguindo AA, e o laranja ainda aparece bem visível no degradê.

**Ajuste 2026-07-21 (8ª rodada):** 2 bugs de quebra de linha reportados pela Catharina via screenshot.
- **"e-mail" quebrando ao meio** (ex.: "um e-" numa linha, "mail" na próxima): o hífen interno da palavra estava sendo tratado como ponto de quebra de linha válido pelo navegador. Trocado o `-` por `&#8209;` (hífen não-quebrável, U+2011) em todas as 4 ocorrências visíveis de "e-mail" no HTML (HERO H1, ASSINATURA H2, COMPARATIVO, O QUE VOCE RECEBE). `copy.txt` mantido com hífen normal (é so uma correção tipográfica de renderização, não muda o texto-fonte).
- **H1 do hero e botão do menu vazando pra fora da tela no mobile:** bug clássico de CSS Grid — `.hero-content` é item de um grid (`.hero .container`) e por padrão todo item de grid tem `min-width:auto`, que impede o item de encolher abaixo do tamanho mínimo do seu conteúdo. Como o H1 agora tem uma `<img>` inline (o lettering), isso empurrava a largura mínima calculada pra além da viewport em telas estreitas, forçando overflow horizontal em vez de quebrar linha normalmente. Corrigido com `.hero-content{min-width:0}`, que é o fix padrão pra esse comportamento do Grid/Flexbox.

**Ajuste 2026-07-21 (9ª rodada):** revisão anti-IA + integração de formulário real, a pedido da Catharina.
- **Revisão anti-IA completa** contra `conhecimento/editorial/regras-anti-ia.md` em todo o texto visível (as 4 rodadas de mudança desde a geração original nunca tinham sido re-auditadas juntas). 1 achado: filler word "realmente" em LIST ITEM COM da seção COMPARATIVO ("...do que realmente vale acompanhar"). Corrigido pra "do que vale a pena acompanhar" (em `index.html` e `copy.txt`). Demais checks OK: em-dash 0, sem frases típicas de IA, antítese-por-negação 1/2 (sob o limite), exclamação 1/2 (só no mockup de e-mail do hero, não é copy de marketing).
- **Formulário real integrado — Mailchimp** (mesmo endpoint usado em buzzmonitor.com, descoberto inspecionando a página ao vivo). Não usei o fluxo padrão do `/lp-integrar-form` (wrapper `<div class="jotform-embed">` + iframe) porque o Mailchimp aqui **não é um embed de iframe** — é HTML de formulário cru que a própria página estiliza, então mantive nosso design de card já aprovado e só troquei os bastidores:
  - `action` do form aponta pro endpoint real (`buzzmonitor.us14.list-manage.com/subscribe/post?...`).
  - Campos renomeados pro schema do Mailchimp: `FNAME`, `LNAME` (**campo novo "Sobrenome"**, não existia no mock de 2 campos, adicionado pra bater com o formulário real e não perder segmentação), `EMAIL` (único obrigatório, igual ao original).
  - Campo oculto `tags=10371138` preservado (tag que identifica assinantes vindos desta LP).
  - JS de envio replicado do site (submit via iframe oculto, sem sair da página) + mensagem de sucesso inline no estilo do nosso design (`.form-success`, fundo teal-light) em vez do popup deles.
  - Testado localmente: sem erros no console, `form.action` e os 4 campos (`FNAME`, `LNAME`, `EMAIL`, `tags`) conferidos via JS. **Não testei o envio de verdade** pra não criar um assinante fake na lista real do Mailchimp — validação foi só de estrutura/código.

## Estado

- [x] HTML gerado
- [x] Validações técnicas: em-dash 0, `&mdash;` 0, JSON-LD parseia, SEO completo (1 description, 10 og:, 4 twitter:), fidelidade literal da copy conferida
- [x] OG image gerada (1200x630) — `assets/og-news-da-buzz.png`
- [x] Revisão — ver `REVISAO.md` (5 ajustes aplicados; 1 crítico de contraste do CTA sinalizado como decisão de marca, não corrigido sozinho; 2 melhorias e 1 nice-to-have opcionais)
- [x] Formulário integrado — **Form provider: Mailchimp** (2026-07-21), mesmo endpoint usado em buzzmonitor.com
- [ ] Publicado — rodar `/lp-publicar buzzmonitor news-da-buzz material.buzzmonitor.com`

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon + avatar no mockup de e-mail do hero)
- `./assets/newsletter-preview.png` (LP-local — banner original, sem recorte, fornecido pela Catharina; mantido como fonte, não referenciado direto no HTML)
- `./assets/newsletter-preview-cropped.png` (LP-local — recorte sem o espaço em branco embaixo; usado no masthead do HERO)
- `./assets/news-da-buzz-wordmark.png` (LP-local — lettering "News da Buzz" + tracinhos, recortado do banner original, fundo transparente; usado inline em HERO H1, PROBLEMA H2 e PARA QUEM H2)
- `./assets/og-news-da-buzz.png` (OG 1200×630, gerada)

## Pendências

- **Sem Notion:** esta copy não passou por `/lp-preparar` a partir de Notion — foi escrita diretamente para este pedido e estruturada manualmente nos mesmos rótulos (publicada em Entregas do Notion para registro: `Copy LP · Buzzmonitor · news-da-buzz · 2026-07-21`).
- **Form real:** mock por enquanto. Definir provedor (Jotform/RD Station/HubSpot) antes de `/lp-integrar-form`.
- **Working tree do branch estava 17 commits atrás de `origin/main`** com uma quantidade grande de mudanças não commitadas de trabalho anterior (não relacionadas a esta LP). O `git pull --rebase` do Passo 0.0 gerou conflitos em 3 LPs de webinar não relacionadas a este pedido — abortei o rebase para não arriscar o trabalho em andamento de outra sessão. Esta LP foi criada sobre o HEAD local (`cb78114`), sem rebase. Recomendo sincronizar o branch separadamente antes do merge final.
