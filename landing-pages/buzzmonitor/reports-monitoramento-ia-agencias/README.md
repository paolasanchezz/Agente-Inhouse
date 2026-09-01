# LP Buzzmonitor — reports-monitoramento-ia-agencias

**Gerado em:** 2026-09-01
**Reconstruído em:** 2026-09-01 (para seguir o padrão visual das demais LPs de webinar Buzzmonitor)
**Copy-fonte:** `copy.txt` (output de /lp-preparar)
**Webinar:** Reports e Monitoramento com IA para Agências — 6 de outubro de 2026, 11h, online e ao vivo
**Domínio-alvo:** webinar.buzzmonitor.com (guarda-chuva migrado pro CI)

## Padrão de layout

A pedido da Catharina, o HTML foi reconstruído para reaproveitar literalmente o sistema de design (CSS vars, classes, componentes) de `gestao-de-crises-ia-agosto-2026/index.html` — a LP de webinar mais recente da marca — em vez do layout genérico gerado na primeira passada pela `frontend-design`. Isso inclui: nav absoluta com dot pulsante "Ao vivo", ticket card "Save the date", punchline em gradiente gigante, cards de problema com X circular, grid de programa com check, lista numerada "para quem", seção de urgência com círculos decorativos, e form no final da página (não na 2ª seção — esse é o padrão real usado em todas as LPs de webinar da marca, prevalece sobre o default genérico do GUIDELINES §10).

**Contador regressivo:** usa o widget `.box-countdown` de verdade (dias/horas/min/seg, ticando a cada segundo, número "flipa" pro laranja ao virar) — igual ao template-fonte. Uma tentativa inicial de simplificar pra um texto estático "Faltam X dias" foi revertida (ver histórico na 3ª rodada abaixo).

## Estrutura (atual, pós 5ª rodada)

1. Nav (logo + "Ao vivo" pulsante)
2. Hero (eyebrow + **H1 = título literal do webinar** "Reports e Monitoramento com IA para Agências" (com "IA" em destaque gradiente) + H2 método, sem negrito + CTA + ticket card com data e contador regressivo D/H/M/S)
3. Contexto de mercado (estatística "92%" em destaque + fonte citada, ver Notas)
4. Problema (5 itens em grid 2 colunas, cards com X vermelho circular, 5º card ocupa a linha inteira) + punchline em gradiente, tamanho reduzido (H3+BODY da seção Diferencial da copy) + CTA
5. Programa (grid 2 colunas, 4 itens com check roxo + 5º item em destaque roxo "Demonstração ao vivo")
6. Para quem (lista numerada 01-04 + ilustração SVG decorativa reaproveitada do template)
7. Prova social (grid de estatísticas, 4 métricas, números animados contando + gradiente roxo)
8. Perguntas frequentes (acordeão, fundo laranja em gradiente, 5 objeções reais de calls comerciais com agências, ver Notas)
9. Urgência (fundo roxo escuro, círculos decorativos, copy sem tom de exclusividade)
10. CTA final + formulário mock (Nome/E-mail/Empresa)
11. Footer (logo reversed + copyright + Política de Privacidade)

**Atualização 2026-09-01 (2ª rodada):** a pedido da Catharina, o H1 passou a usar o título literal do webinar (antes era o headline de dor recomendado pelo doc de insumo, "Seu cliente descobriu antes de você" — GUIDELINES §3 recomenda H1 pela dor, mas a decisão explícita da Catharina prevalece). O SUB também foi reescrito para "Como agências podem usar social listening e IA para automatizar processos, relatórios e atendimento." e teve o negrito removido a pedido dela. Foi adicionada a seção de Perguntas Frequentes, baseada no print de objeções recorrentes de calls comerciais que a Catharina enviou.

**Atualização 2026-09-01 (3ª rodada):** os eyebrows/kickers genéricos de seção ("O problema", "O programa", etc) foram removidos a pedido da Catharina (ver [[feedback-lp-sem-eyebrows-genericos]] na memória). O contador "Faltam X dias" foi substituído pelo widget regressivo D/H/M/S de verdade — a Catharina apontou que estava diferente do padrão das outras LPs de webinar (memória `feedback-lp-webinar-sem-ticker-contador-dias` estava com o resumo invertido, já corrigida). Foi adicionada a seção "Contexto de mercado" logo após o hero, seguindo a estrutura de `crescer-marca-influenciadores-setembro-2026` (que tem uma seção de dado de mercado nesse mesmo lugar).

**Atualização 2026-09-01 (4ª rodada):** lote grande de ajustes de conteúdo e visual pedidos pela Catharina:
- Contexto de mercado: `.wrap` mais largo (900px) e fonte do claim menor, pra "2026" não quebrar linha sozinho.
- Problema: H2 trocado para "Sem uma boa ferramenta, a realidade da sua agência é essa…"; adicionado elemento gráfico decorativo (SVG de papéis empilhados com X) no espaço vazio à direita da lista (só desktop largo, `@media max-width:1180px` esconde).
- Diferencial/punchline: H3 trocado para "Aprenda a usar IA e automações para otimizar relatórios"; BODY termina agora em "Isso muda tudo!" (1 exclamação, dentro do limite anti-IA).
- Programa: adicionado 5º item em destaque roxo (`.l-item--live`, `grid-column:1/-1`) com ícone de play: "Demonstração ao vivo da Buzzmonitor, com casos reais de agência".
- Clientes: mural trocado de slide vaivém (`mural-slide`) pra scroll contínuo unidirecional (`mural-scroll`, linear infinite 34s) — track com 4 cópias das 2 imagens (as 2 do meio com `aria-hidden`/`alt=""` pra não duplicar pro leitor de tela) e fade nas bordas do frame.
- Prova social: números agora contam animado (0 até o valor, `requestAnimationFrame`, formatado `toLocaleString('pt-BR')`) ao entrar em viewport, com fallback instantâneo se `prefers-reduced-motion` ou sem `IntersectionObserver`; cor trocada de roxo sólido pra gradiente roxo (`--grad-purple`, novo token).
- FAQ: título trocado para "Como a Buzzmonitor pode ser útil pra sua agência?"; virou acordeão de verdade (`<button aria-expanded>` + resposta com `max-height` animado, chevron gira 180°, tudo fechado por padrão); fundo mudou de branco pra roxo primário com 2 "orbs" decorativos desfocados (gradiente hot + roxo).
- Urgência: copy trocada pra tirar o tom de exclusividade/escassez — label "Vagas limitadas" virou "Inscrição gratuita"; H2 "O webinar é ao vivo. Sem replay liberado..." virou "Aprenda a automatizar o trabalho manual da sua agência com IA, na prática."; BODY também reescrito sem a pressão de "garanta agora".

**Atualização 2026-09-01 (5ª rodada):** ajustes finos pedidos pela Catharina após ver o preview:
- Problema: elemento gráfico decorativo (SVG de papéis) removido — ficou ruim visualmente. `.problem-list` virou grid 2 colunas (`repeat(2,1fr)`, 1 coluna abaixo de 720px) em vez de coluna única com espaço vazio à direita; o 5º card (`grid-column:1/-1`) ocupa a linha sozinho, cheio.
- Punchline (Diferencial): fonte reduzida de `clamp(44px,7.4vw,92px)` pra `clamp(26px,3.6vw,44px)` — texto muito grande pra uma frase longa (8 palavras), mais próximo de um H2/H3 forte do que de um "momento gigante".
- Seção Clientes (mural de logos) **removida por completo** — CSS, HTML e as imagens `mural-1.jpeg`/`mural-2.jpeg` foram deletadas da pasta `assets/logos/`.
- FAQ: fundo trocado de roxo sólido (`--c-primary`) pra gradiente laranja sólido, depois pra **`var(--grad-hot)`** (rosa→laranja, o mesmo gradiente usado no destaque "IA" do H1 e no punchline) — a pedido explícito da Catharina, pra reaproveitar o mesmo degradê já usado nas letras. Orbs decorativos ajustados pra contrastar com o novo fundo (orb 1 branco translúcido, orb 2 roxo `--c-primary`).

## Estado

- [x] HTML gerado, seguindo o padrão de layout Buzzmonitor
- [ ] OG image 1200×630 → `assets/og-reports-monitoramento-ia-agencias.png` (arquivo **único** — nunca também `og-image.png`)
- [ ] Revisão (frontend-design review + web-design-guidelines) — rodar `/lp-revisar buzzmonitor/reports-monitoramento-ia-agencias`
- [ ] Formulário integrado — rodar `/lp-integrar-form buzzmonitor/reports-monitoramento-ia-agencias [snippet]`
- [ ] Publicado — rodar `/lp-publicar buzzmonitor reports-monitoramento-ia-agencias webinar.buzzmonitor.com`

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (nav)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)

## Notas

- GTM: `GTM-WFJVK858` (região Brasil, `brand/buzzmonitor/tracking.json`) injetado no `<head>` e `<noscript>`.
- Sem LPs irmãs (idioma único, sem sufixo `-es`/`-pt`) — `hreflang` omitido, só `canonical`.
- JSON-LD tipo `Event`, com `startDate` 2026-10-06T11:00:00-03:00. Sem `endDate` (duração do webinar não confirmada no briefing — se houver um valor padrão da marca, ex. 60 min, adicionar antes de publicar).
- Ilustração SVG decorativa da seção "Para quem" foi reaproveitada tal como está no template-fonte (puramente decorativa, `aria-hidden`, sem texto).
- Todos os "eyebrows" de seção ("O problema", "O programa", "Para quem é", "Prova social", "Quem já confia", "Para fechar", "Vaga gratuita") são rótulos estruturais curtos que seguem a convenção do template-fonte, não texto extraído da copy.
- Sem seção de speakers (não informados no briefing) — decisão registrada no checkpoint com a Catharina.
- FAQ: as 5 perguntas vêm do doc de insumo (seção "Objeções recorrentes nas calls", print enviado pela Catharina). Respostas escritas de forma conservadora — sem inventar número de franquia, prazo de setup ou política de dado retroativo não confirmados na fonte. Só a resposta sobre licença multi-cliente é afirmativa direta, por já estar confirmada no doc (41% dos leads falam nisso). **Vale revisar com o time comercial antes de publicar**, já que são respostas a objeções reais de venda indo pro público.
- Estatística "92%" (contexto de mercado): não veio do blog da Buzzmonitor (busquei, não achei um post com stat equivalente acessível via busca) nem de memória de projeto anterior — é dado externo, de pesquisa de mercado (Índice de Maturidade Tecnológica em Marketing B2B, Live University + Ibramerc, 2026), via reportagem do E-Commerce Brasil. Fonte citada na própria seção. **Vale a Catharina confirmar se prefere esse dado ou se tem um da Buzzmonitor pra substituir.**
