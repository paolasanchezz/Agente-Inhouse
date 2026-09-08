# LP Buzzmonitor — teste-de-maturidade-resultado-inicial

**Gerado em:** 2026-09-08
**Copy-fonte:** `copy.txt` (a partir do doc Notion "Novas respostas das categorias", faixa 0-5 pontos)

## Contexto

Primeira de 5 LPs irmas de resultado do Teste de Maturidade em Redes Sociais (o teste roda no Jotform externo: https://form.jotform.com/261735831186058). Cada faixa de pontuacao vai ter sua propria LP estatica, com o Jotform redirecionando o respondente pra URL certa conforme o total:

| LP | Faixa | Status |
|---|---|---|
| `teste-de-maturidade-resultado-inicial` | 0-5 pontos, Nivel Inicial | ✅ gerada (esta, aprovada) |
| `teste-de-maturidade-resultado-basico` | 6-10 pontos, Nivel Basico | ✅ gerada |
| `teste-de-maturidade-resultado-intermediario` | 11-15 pontos, Nivel Intermediario | ✅ gerada |
| `teste-de-maturidade-resultado-avancado` | 16-18 pontos, Nivel Avancado | ✅ gerada |
| `teste-de-maturidade-resultado-maduro` | 19-20 pontos, Nivel Maduro | ✅ gerada |

As outras 4 foram geradas por script reaproveitando 100% desta estrutura (ja com a capa-dissolve da iteracao 4) — so trocando badge/H2/paragrafos e o segmento/agulha ativos do gauge.

## Revisao (2026-09-08, aplicada via /lp-revisar nas 4 LPs irmas)

A revisao completa (design + web-interface-guidelines + auditorias deterministicas) rodou sobre `teste-de-maturidade-resultado-basico` (ver `REVISAO.md` la, os achados valem pra estrutura compartilhada das 5). Achado critico corrigido **retroativamente nesta LP tambem** pra manter a familia consistente:

- **Foco de teclado "fantasma" atras da capa** — links dentro do resultado/footer eram alcancaveis por Tab mesmo escondidos atras da capa opaca antes do clique em "Ver resultado" (WCAG 2.4.3). Corrigido com `inert` em `#resultado-gate`/`<footer>`, sincronizado com o `aria-hidden` existente.

Melhoria registrada mas **nao aplicada** (decisao do Victor, afeta a familia toda e a LP-mae): contraste ~2,82:1 do texto branco sobre `--orange` nos botoes `.btn-orange` fica abaixo do minimo WCAG AA. Detalhe completo no `REVISAO.md` da LP `-basico`.

Mesma identidade visual de `landing-pages/buzzmonitor/teste-de-maturidade/index.html` (a LP-mae que gera a pontuacao): paleta roxo `#2E0044` + laranja `#EB7C2E`, fontes League Spartan + Lato, header/footer e padrao de secao "CTA em fundo roxo escuro" reaproveitados.

## Estrutura (atual, pos-iteracao 3)

- HEADER/NAV — fixo, logo + CTA "Agende uma demonstracao gratuita" (sempre visivel)
- **CAPA (1 dobra so)** — `min-height:100vh`, fundo em degrade animado (tons de roxo, sem laranja solido — ver nota de contraste abaixo), eyebrow + H1 (com "pronto" em gradiente) + sub + botao **"Ver resultado"** que revela o resto
- **PAINEL DE RESULTADO (`#resultado-gate`, escondido ate o clique)** — gauge/medidor de nivel (agulha aponta pro segmento laranja = Nivel Inicial) + badge "Nivel Inicial" (carimbo) + H2 + 5 paragrafos de diagnostico + CTA final (fundo roxo com watermark) + FOOTER, tudo dentro do mesmo "desenrolar"
- Sem JS, tudo fica visivel normalmente (progressive enhancement — nunca esconde conteudo de bot/SEO/no-JS)

## Iteracao 3 — capa unica + reveal "tipo jogo" (pedido do Victor: fundo roxo sem pontilhado, mais espaco antes da 2ª dobra, e "no inicio so uma dobra com degrade animado e botao Ver resultado; ao clicar, desenrola a resposta")

- **Capa vira `100vh`** com fundo `linear-gradient` animado (`background-position` em loop, 16s) só na familia de roxos (`--purple` / `#4A0A6B` / `#1F0030`) — a primeira versão passava por um tom laranja solido no meio do ciclo e derrubava o contraste do texto branco (quase ilegivel); trocado por um degrade 100% roxo pra manter contraste alto o tempo todo. Laranja continua so nos blobs (bem transparentes) e no botao.
- **Pontilhado removido da capa** (o `radial-gradient` de bolinhas que tinha antes) — mantido so no CTA final, que nao foi mencionado no feedback.
- **Botao "Ver resultado"** (texto literal pedido pelo Victor no chat — nao veio do copy.txt, autorizado diretamente por ele) com pulso continuo (glow) convidando o clique. Ao clicar: painel expande (`max-height` 0 → altura real, animado), conteudo interno dispara os `reveal`/gauge na hora (sem esperar scroll), e a pagina rola suave ate o painel depois que a expansao termina.
- **Gauge voltou pra paleta roxo/laranja** (estava branco/laranja quando morava no fundo roxo da capa; agora mora num fundo branco dentro do painel, entao os segmentos neutros voltaram a ser roxo transluzido e a agulha roxa solida).
- **Mais espaco antes do gauge**: `padding-top:140px` (88px mobile) na secao que abre o painel, antes vinha logo colado.
- **Progressive enhancement:** com JS desligado, `html` nunca ganha a classe `js`, entao a regra `html.js .reveal-gate{max-height:0}` nunca ativa e a pagina cai de volta a um scroll normal, tudo visivel (bots, leitores de tela sem JS, SEO — nada fica preso atras do botao).
- Nenhum texto novo alem do "Ver resultado" pedido explicitamente pelo Victor.

**Nota de verificacao (iteracao 3):** testei a logica de expansao/scroll via DOM e confirmei que abria certinho pro tamanho real do conteudo, mas o Victor testou visualmente e nao gostou da mecanica de "expandir + rolar" — pediu um dissolve no lugar (ver iteracao 4 abaixo).

## Iteracao 4 — capa vira overlay que se dissolve (pedido do Victor: "a pagina podia se dissolver e aparecer o texto dos resultados, do jeito que ta nao gostei")

Trocada a mecanica de "painel colapsado que expande + rola a pagina" (iteracao 3) por um **cross-fade no lugar**, mais proximo de uma transicao de tela de jogo:

- A capa (`.hero`) vira **overlay fixo em tela cheia** (`position:fixed;inset:0;z-index:50`) só quando JS esta ativo (`html.js .hero{...}`). O resultado (`#resultado-gate`) fica **sempre no fluxo normal**, sentado logo abaixo do header, o tempo todo — so fica coberto pela capa opaca por cima.
- Ao clicar em "Ver resultado": a capa recebe `opacity:0` (transicao de ~1s) e, ao terminar, `display:none` — revelando o resultado que ja estava ali embaixo, **na mesma posicao de scroll** (sem pulo, sem scroll automatico pro botao principal).
- Os elementos internos do resultado (`gauge`, badge, paragrafos) **nao animam mais pelo scroll** — ficam de fora do `IntersectionObserver` generico e disparam a entrada (`is-visible`) exatamente no momento do clique, sincronizados com a capa sumindo.
- O link "Agende..." do menu tambem foi religado: se clicado antes do "Ver resultado", dispara a mesma dissolucao e ai sim rola suave ate o CTA final (unico caso que ainda usa `scrollIntoView`).
- Sem JS: a capa nunca vira `position:fixed` (a regra so ativa com `html.js`), entao a pagina cai pra um scroll normal de cima a baixo, tudo visivel — nada fica preso atras de um overlay pra bot/leitor de tela sem JS.
- Removida toda a logica antiga de `max-height` colapsado/expandido (nao e mais necessaria).

**Nota de verificacao:** confirmei via DOM (opacity/display computados, monkey-patch em `scrollIntoView`) que o dissolve do botao principal funciona 100% — capa vai a opacidade 0 e some em menos de 1s, resultado aparece na mesma posicao, sem mexer no scroll. Peguei screenshot limpo confirmando visualmente. O scroll automatico do link do menu (pro `#cta`) fica marcado como nao 100% confirmado nesta sessao — o preview interno teve dificuldade de mover o scroll via JS quando a janela do Claude ficava minimizada (limitacao da ferramenta, nao do codigo). Vale um teste manual rapido clicando em "Agende..." no menu antes de clicar "Ver resultado".

## Decisao de design registrada

Copy.txt so trazia UMA linha de CTA para o bloco final ("Agende uma demonstracao gratuita"), sem headline separada. Em vez de duplicar o mesmo texto como H2 + botao (ficava redundante visualmente), a secao ficou so com o botao em destaque (maior, centralizado) sobre o fundo roxo com watermark. Nenhum texto novo foi inventado — decisao puramente de layout.

## Pendencias

- [x] HTML gerado
- [x] **Formulario integrado** (2026-09-08) — CTA final trocado pelo embed real do Jotform (`jsform/252995108251662`), com UTM propria desta LP (`utm_campaign=resultado-inicial`) pra rastrear de qual faixa de pontuacao o lead veio. Wrapper `.jotform-embed` aplicado.
- [ ] OG image 1200×630 → `assets/og-teste-de-maturidade-resultado-inicial.png` (arquivo **unico**)
- [ ] Revisao — rodar `/lp-revisar buzzmonitor/teste-de-maturidade-resultado-inicial`
- [ ] Publicado — rodar `/lp-publicar buzzmonitor teste-de-maturidade-resultado-inicial [dominio]`
- [ ] **Jotform:** Victor precisa configurar o redirecionamento pos-envio, uma URL por faixa (as 5 LPs ja existem):
  - 0-5 pontos → `teste-de-maturidade-resultado-inicial`
  - 6-10 pontos → `teste-de-maturidade-resultado-basico`
  - 11-15 pontos → `teste-de-maturidade-resultado-intermediario`
  - 16-18 pontos → `teste-de-maturidade-resultado-avancado`
  - 19-20 pontos → `teste-de-maturidade-resultado-maduro`

  O doc-mae no Notion menciona um bug de calculo no form atual ("respondi pra pontuar 7, ele disse 20") — confirmar que foi corrigido antes de ativar os redirects.

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
