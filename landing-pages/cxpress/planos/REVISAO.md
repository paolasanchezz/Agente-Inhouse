# Revisão — cxpress/planos

**Data:** 2026-08-27
**Escopo:** auditoria de design, acessibilidade e fidelidade de copy sobre o HTML gerado.

## Críticos aplicados

| # | Achado | Correção |
|---|---|---|
| 1 | Em-dash em comentário do JS (`grep -c "—"` retornava 1). Tolerância zero, `regras-anti-ia.md` | trocado por dois-pontos. Contagem final: 0 |
| 2 | `.pk-tag` (pílula "Mais contratado" / "Sob demanda") a 13px, abaixo do piso de 14px para label (GUIDELINES §20) | subido para 14px. `check_mobile_type` agora reporta `min=14` |
| 3 | Pisos de tipografia mobile abaixo do especificado em 11 regras (`.cxp-submit` 16px, `.k2x-block a` 16px, `.k2x-sub` 16px, `.skip-link` 16px, labels 14px etc.) | `bump_mobile_type.py` aplicado (só mobile; desktop intacto) |
| 4 | Preço do Enterprise quebrava em duas linhas com pesos diferentes ("Precificação" grande + "sob demanda" pequeno), invertendo a ênfase da frase | frase única em 28px, literal da copy: "Precificação sob demanda" |
| 5 | `:focus-visible` com outline navy `#232960` ficava quase invisível sobre o card Enterprise, a seção do formulário e o footer (todos escuros) | outline branco nesses três contextos |
| 6 | Faixa de canais do hero usava `role="list"` num `<div>` e `role="listitem"` em `<img>`, o que sobrescreve a semântica de imagem | trocado por `<ul>`/`<li>` real |
| 7 | Perguntas do FAQ estavam em `<span>`, mas a copy as rotula como `H3` (perdia navegação por headings em leitor de tela) | `<summary><h3>…</h3></summary>`, com `font:inherit` para não mudar o visual |
| 8 | Tabela comparativa sem `<caption>` | `<caption class="sr-only">` descrevendo o comparativo |
| 9 | **Logo e pílula "Planos Cxpress" desalinhados no hero** (reportado pelo Victor, 2026-08-27). `.pk-hero-logo` era `inline-block` e `.pk-overline` também, então os dois caíam na mesma linha do fluxo inline e o *par* é que ficava centralizado: logo à esquerda do eixo, pílula à direita | `.pk-hero-logo` virou `display:block` com `width` igual à da imagem e `margin:0 auto`, para ocupar a própria linha. A largura do bloco também foi acertada no `@media (max-width:600px)` (170px), senão o logo menor ficaria encostado à esquerda de uma caixa de 200px |

## Verificado e conforme

- **Fidelidade de copy (§9 e regra de fidelidade do `lp-gerar`):** todo texto visível vem literal
  de `copy.txt`. Fora dela, só o que a whitelist permite: labels do form (`Nome`, `E-mail
  corporativo`, `Telefone`, `Empresa`, `Pessoas no atendimento`, opções de faixa), o disclaimer
  de compliance, os cabeçalhos funcionais da tabela (`Recurso`, `Basic`, `Enterprise`), o
  skip-link, o `caption` e os `aria-label`. Nenhum pull-quote, kicker, tag rotacionada ou
  punchline inventada.
- **Contagem de blocos = contagem da copy:** 2 planos, 7 grupos na tabela, 6 perguntas no FAQ,
  3 bullets na seção do form. Nada arredondado para "ficar bonito".
- **§8 seções-tipo:** itens inclusos usam o check verde do brand; "não incluído" usa traço
  neutro em CSS (não o em-dash de texto) com `sr-only` "Não incluído".
- **§7 contraste:** texto sobre o lilás `#D7E2FF` usa navy `#232960` (≈10:1), nunca o royal.
  Branco sobre royal `#4A69BD` dá ≈5,2:1.
- **§11 formulário:** era mock nesta passada; o embed real (Jotform `261034073026647`) entrou depois, via `/lp-integrar-form`.
- **§10 posicionamento do form:** página BoFu, form na última seção, com CTA no hero rolando
  até lá.
- **§12 favicon:** um único link, PNG do brand.
- **§15 SEO:** description única, 10 `og:`, 4 `twitter:`, JSON-LD (Organization + WebPage +
  SoftwareApplication com AggregateOffer `lowPrice: 1290 BRL`) parseando.
- **§18 OG image:** `assets/og-planos.png`, 1200×630, 353 KB, sem `og-image.png` duplicado.
- **§4 animação:** reveal com dois caminhos idempotentes (IntersectionObserver + checador de
  scroll), `<noscript>` forçando `opacity:1` e bloco `prefers-reduced-motion`.
- **§16 hreflang:** não se aplica, LP única (sem irmã `-pt`/`-es`).
- **GTM:** `GTM-T4XDWHL3` (brasil) nos dois blocos; `check_gtm_region.py` = 1 OK, 0 bloqueios.

## Opcionais (não aplicados)

1. **Alturas dos dois cards de plano não se igualam** no desktop, porque o Basic lista mais
   itens. Igualar exigiria `align-items: stretch` com scroll interno ou cortar itens, e cortar
   item de plano é pior que a assimetria. Fica como está.
2. **Faixa de canais do hero sem rótulo.** Um texto tipo "canais no mesmo painel" ajudaria a
   leitura, mas não existe na copy e a whitelist não cobre. Se quiserem, é uma linha nova em
   `copy.txt` e um `/lp-gerar`.
3. **Mascote Samir** não entrou (a `institucional` também não usa). Cabe bem ao lado do bloco
   do formulário, se quiserem calor visual na última dobra.
4. **Sem seção de urgência** (§8). Deliberado: página de pricing perene não tem escassez real.

---

# Revisão 2 — alterações de copy pedidas pelo Victor (2026-08-27)

**Escopo:** 4 alterações de copy solicitadas no chat, aplicadas em `copy.txt` (fonte-verdade) e no `index.html`, seguidas das auditorias determinísticas.

## Aplicado

| # | Pedido | O que mudou |
|---|---|---|
| 1 | "basic embaixo pode colocar valor de licença adicional R$ 120,00" | nova linha ao pé do card Basic, em pílula lilás: "Acesso adicional de operador humano: R$ 120,00 por mês." (`.pk-addon`, 17px, navy sobre `#D7E2FF` ≈10:1) |
| 2 | tirar "em pacotes de até 5 mil ligações mensais" do Voice Agent | removido nos 2 lugares: card Enterprise ("Voice Agent: a IA de telefonia") e linha da tabela comparativa ("Voice Agent, IA de telefonia"). Zero ocorrências de "5 mil" restantes |
| 3 | nova frase principal do hero | subtítulo do hero trocado por "Centralize seus canais, organize toda a operação e potencialize o atendimento com inteligência artificial. Escolha o modelo mais adequado ao momento e aos objetivos da sua empresa." |
| 4 | título e texto da segunda seção | H2 virou "Duas formas de contratar. / Uma plataforma completa." (quebra entre as duas frases, a segunda em navy bold como destaque) e o subtítulo virou "Comece com o Basic, utilizando toda a tecnologia da Cxpress com sua própria equipe, ou escolha o Enterprise para uma solução personalizada, combinando canais, agentes de IA e especialistas dedicados à sua operação." |

**Leitura registrada:** "frase principal" foi aplicada como o **subtítulo** do hero, não como o H1. O texto tem duas frases descritivas e não caberia num H1 de 64px; o H1 segue "O plano certo para o seu atendimento". Trocar é uma linha, se a intenção era o H1.

**Nota de escopo:** o item 1 reverte, por decisão explícita do Victor, a escolha anterior de manter os preços unitários dos incrementos fora da página. Só o acesso de operador (R$ 120,00) entrou; os demais incrementos seguem sem preço, porque o Enterprise é sob demanda.

## Auditorias após a alteração (todas passaram, 0 críticos)

| Gate | Resultado |
|---|---|
| `check_gtm_region.py` | `status: ok`, `GTM-T4XDWHL3`, região brasil, `stamp_match: true` |
| em-dash (§5 / anti-IA) | 0 no HTML, 0 no `copy.txt` |
| SEO (§15) | description 1, robots 1, og 10, twitter 4, JSON-LD 1, canonical 1 |
| JSON-LD | parseia; `Organization` + `WebPage` + `SoftwareApplication`; `Organization.url` = `https://home.cxpress.io` (bate com o brand-manifest) |
| Logo regional (§17) | 0 ocorrências de `href="/"` |
| OG image (§18) | `og-planos.png` 1200×630, sem `og-image.png` duplicado |
| Tipografia mobile (§20) | `bump_mobile_type.py` dry-run limpo (0 regras a subir) |
| Overflow a 375px | só o `.skip-link` em `left:-9999px` (fora de tela por construção) |
| Fidelidade de copy | os 4 textos novos aparecem literais, 1× cada. Nenhum texto inventado |

## Melhorias opcionais desta passada

Todas do mesmo tema: agora que o preço do acesso adicional é público, há 3 lugares que falam de acesso extra sem citá-lo. Nenhuma é erro, só coerência.

- [ ] **Nota ao pé da seção de planos** diz "Acessos, canais, agentes de IA e serviços adicionais são cotados junto com o time comercial". Não contradiz (R$ 120 é preço de tabela), mas se quiser blindar, basta tirar "Acessos," dessa lista.
- [ ] **FAQ "O que conta como acesso de operador?"** diz que acessos adicionais "entram como incremento", sem o valor. Poderia citar os R$ 120,00.
- [ ] **Linha da tabela "Acessos de operador humano"** mostra "5 incluídos" no Basic. Poderia mostrar "5 incluídos (+R$ 120/acesso)".

---

# Revisão 3 — "Sob demanda" na linha de preço (2026-08-27)

**Pedido:** na tabela comparativa, trocar o preço "Sob demanda" do Enterprise por algo tipo "falar com especialista" (print da linha `Investimento > Valor mensal`).

## Aplicado

- **Linha `Investimento > Valor mensal`, coluna Enterprise:** de `Sob demanda` para **`Falar com especialista`**, como **link para `#proposta`** (`.pk-cell-cta`: royal `#4A69BD`, bold, sublinhado com `text-underline-offset`, navy no hover). Virou link e não rótulo estático porque numa célula de preço o convite serve mais que a etiqueta, e o destino (formulário) já existe na própria página.
- `copy.txt` acompanhou: `LIST ITEM: Valor mensal | A partir de R$ 1.290 | Falar com especialista`.

## Escopo: o que NÃO foi trocado, e por quê

Sobraram 11 ocorrências de "Sob demanda" na página. Nenhuma é preço, todas são **disponibilidade de recurso**, então ficaram:

| Onde | Quantas | O que significa |
|---|---|---|
| Células da tabela na coluna Enterprise | 10 | TikTok, Google Meu Negócio, Agente Concierge, Voice Agent, integração com terceiros, acessos de operador, e os 4 serviços gerenciados com a Elife. Aqui "sob demanda" responde "tem ou não tem?", não "quanto custa?" |
| Badge do card Enterprise | 1 | selo do card, par do "Mais contratado" do Basic |

## Melhoria opcional desta passada

- [ ] **O card Enterprise ainda anuncia preço como "Precificação sob demanda"** (28px, logo acima do botão "Pedir proposta"). É a outra declaração de preço da página com a mesma construção que você quis tirar da tabela. Não mexi porque o print apontava a tabela, e o card já tem o CTA logo abaixo. Se quiser o mesmo tratamento, dá para virar "Fale com um especialista" ou simplesmente sumir a linha e deixar o botão falar.

## Auditorias após a alteração (0 críticos)

| Gate | Resultado |
|---|---|
| `check_gtm_region.py` | `ok`, `GTM-T4XDWHL3`, `stamp_match: true` |
| em-dash | 0 |
| SEO (§15) | description 1, og 10, twitter 4, JSON-LD 1, canonical 1 |
| Tipografia mobile (§20) | dry-run limpo |
| Overflow a 375px | só o `.skip-link` fora de tela (por construção) |
| Render | conferido no desktop e no layout empilhado do mobile (a linha vira `ENTERPRISE  Falar com especialista`) |
| Fidelidade de copy | texto novo literal, 1× no HTML e 1× no `copy.txt` |

---

# Revisão 4 — e-mail junto das redes + Aplicativo mobile (2026-08-27)

Duas alterações de conteúdo, publicadas juntas.

## Aplicado

| Pedido | O que mudou |
|---|---|
| "onde temos canais no plano basic a opção e-mail pode entrar junto com as redes sociais" | o bloco **Canais** do card Basic passou de 4 para 3 linhas: `WhatsApp com API Oficial da Meta`, **`Instagram, Facebook, Webchat e e-mail`**, `Telefone com URA inteligente para encaminhamento de chamados`. A grafia é a que a tabela comparativa já usava, então card e tabela agora dizem a mesma coisa |
| "adicione nas features que temos app mobile" | **`Aplicativo mobile`** entrou no grupo `Gestão e operação`, nos dois lugares: última linha do card Basic e nova linha da tabela (Incluído nos dois planos, já que o Enterprise herda "tudo do Basic"). A tabela foi de 24 para 25 linhas |

## Decisões registradas

- **Grafia "Aplicativo mobile", sem adorno.** Não há registro de app mobile no `BRANDBOOK.md`, no `brand-manifest.json`, em `conhecimento/produto/cxpress/` nem em nenhuma outra LP Cxpress: a informação veio do Victor no chat. Por isso entrou como nome de feature puro, sem frase de benefício ("atenda de qualquer lugar", "gerencie no celular") que seria claim inventado. Se o app tiver escopo definido (iOS/Android, o que dá para fazer nele), vale virar linha própria no BRANDBOOK e aí a copy pode ganhar corpo.
- **Não mexi em dois lugares que também listam esses canais:** a faixa de ícones do hero (o e-mail continua com ícone próprio, é fileira de canais e não lista) e a linha `1 Agente de IA privado para WhatsApp, Instagram, Facebook e Webchat` (na planilha o agente de IA não cobre e-mail; incluí-lo mudaria o que o plano entrega).

## Auditorias (0 críticos)

| Gate | Resultado |
|---|---|
| `check_gtm_region.py` | `ok`, `stamp_match: true` |
| em-dash | 0 |
| SEO (§15) | description 1, og 10, twitter 4, JSON-LD 1, canonical 1 |
| Tipografia mobile (§20) | dry-run limpo |
| Coerência card × tabela | os dois trazem `Instagram, Facebook, Webchat e e-mail` e `Aplicativo mobile` |
| Render | conferido no card e na tabela |

---

# Revisão 5 — títulos, "Dá?" e acordeão do FAQ (2026-08-27)

## Aplicado

| # | Pedido | O que mudou |
|---|---|---|
| 1 | título da 2ª seção com cor e fonte uniformes | `.pk-plans-title` inteiro em navy `#232960` peso 700. Antes a 1ª frase era `#11110d` peso 400 e só a 2ª era navy bold, via `<span>`. O `<span>` saiu do HTML (o `<br>` entre as frases ficou) |
| 2 | "Perguntas frequentes" também | `.pk-faq-title` de `#11110d`/400 para `#232960`/700 |
| 3 | o "Dá" está muito informal | pergunta virou "Preciso de mais de um número de WhatsApp. **É possível?**" e a resposta abre com "**Sim.**". Aplicado no HTML e no `copy.txt` |
| 4 | abertura dos cards igual à seção de FAQ de elifeportugal.com/agentes-de-ia | acordeão refeito no padrão da referência (detalhes abaixo) |

### Leitura registrada no item 1

O pedido citava a mesma frase duas vezes ("na parte do 'Uma plataforma completa.' deve ser cor e fonte iguais a 'Uma plataforma completa.'"). Interpretei o primeiro trecho como "Duas formas de contratar." e o alvo como o estilo do "Uma plataforma completa." — que é o único dos dois em navy bold. O sinal decisivo foi o item 2: "Perguntas frequentes" já era `#11110d`/400, então se o alvo fosse esse estilo não haveria nada a mudar lá.

### Acordeão: o que foi copiado da referência

Levantei o padrão em `assets/css/styles.css` e `assets/js/main.js` daquela página (`.services-accordion` / `.service-acc-item` / `.sa-arrow` / `.sa-desc`) e reproduzi:

- **lista separada por linhas finas**, sem as caixas brancas com borda e raio que existiam antes (`border-top` na lista, `border-bottom` em cada item)
- **seta diagonal** (SVG "arrow out", `M7 17L17 7M7 7h10v10`) à direita, que **gira 45°** e passa de cinza para royal `#4A69BD` quando abre ou no hover
- **pergunta muda de cor** junto com a seta
- **resposta desliza** (altura animada em 0,4s) em vez do corte seco do `<details>`
- **uma pergunta aberta por vez**: abrir uma fecha a anterior, com animação nas duas

### O que NÃO foi copiado, de propósito

Na referência as respostas também abrem **no `:hover`**. No desktop isso faz painéis abrirem e fecharem sozinhos quando o mouse cruza a lista, e no touch não faz nada. Implementei só no clique.

### Decisões técnicas do acordeão

- **`<details>/<summary>` continuou sendo a base.** O JS faz `preventDefault()` e controla a animação, mas sem JS as perguntas ainda abrem e fecham (só sem animação) e a navegação por teclado segue funcionando. A referência usa `<div>` com listener, que perde os dois.
- **Sem o atributo `name` de accordion nativo.** Ele daria exclusividade de graça, mas o browser fecha os irmãos instantaneamente quando o `open` é setado por script, matando a animação de fechamento. A exclusividade ficou no JS.
- **`prefers-reduced-motion`** desliga a animação e faz o toggle direto.
- A pergunta é `<h3>` dentro do `<summary>` (mantido da revisão 1), então a navegação por headings continua listando as 6 perguntas.

## Auditorias (0 críticos)

| Gate | Resultado |
|---|---|
| `check_gtm_region.py` | `ok`, `stamp_match: true` |
| em-dash | 0 |
| SEO (§15) | description 1, og 10, twitter 4, JSON-LD 1, canonical 1 |
| Tipografia mobile (§20) | dry-run limpo |
| JS | chaves e parênteses balanceados; testado no Chrome real |
| Comportamento | clique abre; clicar em outra fecha a anterior; reclicar fecha; seta em `matrix(0.707…)` = 45°; altura da seção cresce só com item aberto (os fechados ocupam 0) |
| Console | limpo. O único 404 é `/favicon.ico`, que o navegador pede sozinho na raiz; o favicon declarado responde 200 local e em produção |
| Overflow | 0 |

## Melhoria opcional desta passada

- [ ] **Dois padrões de título convivem agora.** "Duas formas de contratar. / Uma plataforma completa." e "Perguntas frequentes" ficaram navy 700; **"O que entra em cada plano"** e **"Clientes que confiam na Cxpress..."** seguem em `#11110d` peso 400. Só os dois primeiros foram pedidos. Unificar os quatro é uma linha de CSS em cada.

---

# Revisão 6 — preço do Basic para R$ 1.750 (2026-08-27)

## Aplicado nesta LP (7 pontos)

| Onde | De | Para |
|---|---|---|
| Card Basic (`.pk-price`) | `A partir de R$ 1.290` | `A partir de R$ 1.750` |
| Tabela, linha `Investimento > Valor mensal` | `A partir de R$ 1.290` | `A partir de R$ 1.750` |
| `meta description` | R$ 1.290 | R$ 1.750 |
| `og:description` | R$ 1.290 | R$ 1.750 |
| `twitter:description` | R$ 1.290 | R$ 1.750 |
| JSON-LD `AggregateOffer` | `lowPrice: "1290"` | `lowPrice: "1750"` |
| **`assets/og-planos.png`** | PNG estampava "R$ 1.290" | **regenerada** via `render_og.py` (1200×630) |

`copy.txt` acompanhou (card + tabela). O `og-template.html` também, porque é a fonte da imagem.

**A OG image era o ponto fácil de esquecer.** Ela é um PNG, não texto: sem regenerar, o preview no WhatsApp e no LinkedIn continuaria anunciando o preço velho mesmo com a página correta. Conferi que o md5 do arquivo no dist bate com o regenerado.

## Cuidado que evitou um estrago

`R$ 1.290` aparecia na página **e** no README como preço do add-on **Voice Agent** (que por coincidência custa o mesmo valor). Um find/replace cego teria transformado o Voice Agent em R$ 1.750. As trocas foram uma a uma, por âncora de contexto, e o R$ 1.290 do Voice Agent está preservado no README.

## Fora desta LP: `evite-banimento-whatsapp` (5 pontos)

O texto `Planos a partir de R$ 990 com 3 acessos` vivia naquela LP, não nesta. Virou
**`Planos a partir de R$ 1.750 com 5 acessos`** no preço visível, no `og:description` e no
`twitter:description`; e `Planos a partir de R$ 1.750.` na `meta description` e na descrição do
JSON-LD (lá o fraseado era mais curto, sem contagem de acessos).

**Troquei 3 acessos por 5**, não só o número do preço: esta LP diz que R$ 1.750 inclui 5 acessos
de operador, então manter "R$ 1.750 com 3 acessos" criaria contradição entre as duas páginas.

## Ainda com o preço antigo (não pedido, não alterado)

Oito LPs Cxpress anunciam o preço velho em produção:

| LPs | Texto |
|---|---|
| `atendimento-clinicas` · `atendimento-digital` · `banimento-whatsapp` · `banimento-whatsapp-clinicas` · `banimento-whatsapp-comercial` · `coex-whatsapp` | `Planos a partir de R$ 1.290` |
| `whatsapp-business-smb` · `whatsapp-smb` | `Planos a partir de R$ 1.290/mês para até 5 acessos` |

As menções a "economia de R$ 4 mil na implantação" (4 LPs de oferta) são desconto de implantação,
não preço de plano, e ficaram fora do escopo.

## Auditorias (0 críticos)

| Gate | Resultado |
|---|---|
| `check_gtm_region.py` (planos) | `ok`, `stamp_match: true` |
| `check_gtm_region.py` (evite-banimento) | 1 aviso **pré-existente e grandfathered** (container `GTM-KN8BPFG` em vez do BR) — não é desta entrega, não bloqueia |
| em-dash nas duas | 0 |
| JSON-LD nas duas | parseia |
| SEO (planos) | description 1, og 10, twitter 4, JSON-LD 1, canonical 1 |
| Build do guarda-chuva | 54 LPs, 0 bloqueios (o único aviso é o asset ausente pré-existente da `case-ia-de-voz`) |
| `R$ 1.290` / `R$ 990` no dist | 0 nas duas LPs |

---

# Passada 7 — 2026-08-28 · frases de "e muito mais" + quebra de linha equilibrada

Pedido do Victor com as posições marcadas em print: duas frases novas, cada uma no ponto
apontado, mais a regra geral de **corrigir as quebras de linha** ("tem espaço para manter as
linhas equilibradas") valendo pras construções futuras.

## Copy — o que entrou e o que mudou na frase

| Onde | Texto pedido | Texto publicado | Por que mexi |
|---|---|---|---|
| Card Basic, entre o CTA "Ver a lista completa" e a caixa do R$ 120 (seta no print) | "E muito mais recursos para organizar, acompanhar e evoluir toda a sua operação **de atendimento**." | "E muito mais recursos para organizar, acompanhar e evoluir toda a sua operação." | "de atendimento" é redundante dentro de um card que só fala de atendimento; sem ele a frase cabe em 2 linhas equilibradas (13%) em vez de 3 |
| Abaixo da tabela do comparativo (X no print) | "Além **dessas funcionalidades**, você conta com **diversos** outros recursos para atendimento, gestão e produtividade." | "Além dos itens desta lista, a plataforma traz outros recursos de atendimento, gestão e produtividade, que o time comercial mostra na demonstração." | "dessas funcionalidades" era vago logo depois de uma tabela (quais?) → "dos itens desta lista"; "diversos" é filler; e a frase ganhou **onde** esses recursos aparecem, senão promete sem entregar |

## Altura dos cards

A frase nova cresceu o Basic. Em vez de padding, entrou **1 item real** no Enterprise
(autorizado pelo Victor, "buscando nas fontes que enviei"): **"Números adicionais de WhatsApp
com API Oficial da Meta"** — fonte é a própria linha do comparativo (`1 número` × `Números
adicionais`), e o item é diferenciador de verdade, não enchimento.

Resultado medido em 1440: Basic 1046px, Enterprise 1046px, **delta 0**.

## Quebra de linha equilibrada (regra nova — GUIDELINES §21)

Bloco único no `<style>` do `<head>`: `text-wrap: balance` em bloco curto, `text-wrap: pretty`
em parágrafo longo. Ganho medido (desequilíbrio = `1 − linha_menor / linha_maior`, desktop 1440):

| Bloco | Sem | Com |
|---|---|---|
| `.pk-note` (a que o Victor apontou) | 66% | **6%** |
| `.pk-hero-sub` | 38% | 6% |
| `.pk-plans-sub` | 53% | 8% |
| `.pk-card-desc` (Enterprise) | 53% | 2% |
| `.pk-clients-title` | 48% | 7% |
| `.cxp-form-title` | 33% | 9% |
| `.pk-more-note` (frase nova) | 86% | 13% |
| `.pk-cmp-note` (nota nova) | 27% | 7% |
| item "Integração entre a IA da Cxpress…" | 69% | 2% |
| `.pk-cmp-title` (mobile 375) | 73% | 18% |

Duas coisas que o `balance` **não** resolveu e precisaram de decisão:

1. **Célula de tabela o Chrome não balanceia** — testei wrapper `display:block`, `inline-block`
   e `width:100%`: nenhum funciona dentro de table layout. A única célula multi-linha era
   `Agentes adicionais por canal` ([147, 74] px = 50% de desequilíbrio); virou
   **`Adicionais por canal`**, que cabe em 1 linha (o rótulo da linha já diz "Agente de IA
   privado"). Agora **zero** células quebrando. O `td` fica na lista de `balance` porque no
   mobile a tabela vira cards (`display:block`) e aí pega.
2. **`<br>` manual briga com o balance** — `.pk-plans-title` no mobile ia pra 4 linhas com órfã
   de 139px ("completa."). Entrou `.pk-plans-title br{ display:none }` no ≤600px, mesmo padrão
   que o `.pk-hero-title` já usava: caiu pra 3 linhas sem órfã.

`.k2x-text` (parágrafo do rodapé) ficou em 54% de propósito: é corpo longo alinhado à esquerda,
onde reequilibrar atrapalha o ritmo de leitura. Leva `pretty`, que só mata órfã.

## Auditorias

| Gate | Resultado |
|---|---|
| Build do guarda-chuva | 54 LPs, 0 bloqueios (1 aviso pré-existente da `case-ia-de-voz`) |
| `check_gtm_region.py` | 51 ok, 0 bloqueios |
| em-dash | 0 |
| SEO | description 1, og 10, twitter 4, JSON-LD 1, canonical 1 |
| `check_mobile_type.py` | só o `.skip-link` em `left:-9999px`, que é by design |
| Overflow horizontal | 0 em 1440, 768 e 375 |
| Erros de JS no console | nenhum |
