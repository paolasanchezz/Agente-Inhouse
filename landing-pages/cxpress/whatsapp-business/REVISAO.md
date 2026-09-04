# Revisão — LP Cxpress `whatsapp-business`

**Rodada:** 2026-09-04 (troca integral de copy para a da `home.cxpress.io/app-whatsapp`)
**Medições:** Chrome 148, viewport 1280×720 e 375×812, servidor local na raiz do repo.

---

## 1. Decisões pendentes (para o Victor / Bruno)

Nada aqui foi resolvido por conta própria: são escolhas de conteúdo que a troca de copy provocou.

- [ ] **`Organizado` com O maiúsculo no meio do H1.** Vem assim da página de origem e ficou literal, pela regra de fidelidade. Se for erro de digitação da página institucional, corrigir nos dois lugares (aqui e lá) para não descasar.
- [ ] **"Tiktok e Google meu negócio" saiu da resposta de canais no FAQ.** O briefing de agosto tinha somado esses dois canais; a página de origem não traz. Se os canais existem de fato, vale recolocar (e somar na origem também).
- [ ] **As 2 métricas próprias da Cxpress saíram** (85 % de redução de SLA, +220 % de interações nas redes sociais). A prova numérica agora é a da origem (NBER/McKinsey). As métricas próprias são mais fortes que estudo de terceiro, mas continuavam **sem atribuição definida** (pendência aberta desde 2026-08-28: caso de qual cliente? média da base? recorte de período?). Se a atribuição sair, cabe uma faixa própria.
- [ ] **Seções DORES e INTEGRAÇÕES saíram** (a origem não tem). A copy das dores foi escrita pelo protocolo em agosto e a lista de 7 integrações veio do Victor. Nada foi perdido: está no histórico do git e no `copy.txt` anterior. Reintroduzir exige decidir se esta LP passa a divergir da página institucional.
- [ ] **Links de condições de uso e política de privacidade saíram do rodapé** junto com a adoção do rodapé padrão da `banimento-de-whatsapp` (que traz redes sociais no lugar). Se os links jurídicos precisam ficar em toda LP, o ajuste é no padrão, não só aqui.
- [ ] **OG image desatualizada.** `assets/og-whatsapp-business.png` foi gerada com o H1 antigo ("Centralize seus canais…"). Regerar com `assets/og-template.html` + `assets/render_og.py` antes de publicar, senão o preview no WhatsApp e no LinkedIn contradiz a página.

---

## 1.1 Achados da publicação (2026-09-04, pós-deploy)

- **[corrigido] Vídeo bloqueado pelo CSP.** A fachada carregava o iframe em `www.youtube-nocookie.com` (escolha de privacidade), mas o `frame-src` do `vercel.json` de `content.cxpress.io` libera só `www.youtube.com`. No live o clique no play não fazia nada e o console acusava `Framing 'https://www.youtube-nocookie.com/' violates the following Content Security Policy directive`. Trocado para `www.youtube.com/embed/`, que o CSP já cobre e é o domínio que a LP irmã `whatsapp-smb` usa. Verificado no navegador contra o live, não só por leitura do header.
- **[para o Victor, mecânica do guarda-chuva] `form-action` do CSP bloqueia o Meta Pixel.** O console do live acusa `Sending form data to 'https://www.facebook.com/tr/' violates ... "form-action 'self' https://*.jotform.com https://*.rdstation.com.br https://*.hubspot.com https://*.list-manage.com"`. O pixel dispara por GTM em toda LP do domínio, então **não é específico desta LP**: o `form-action` do template (e do `vercel.json` do guarda-chuva) não tem `https://www.facebook.com`. O `script-src` e o `frame-src` já foram liberados na v3.2.0 do template; o `form-action` ficou de fora. Corrigir mexe em mecânica compartilhada (path protegido, PR não auto-mergeado), então fica registrado aqui em vez de entrar numa entrega de conteúdo.

## 2. Aplicado nesta rodada

### Diagramação (GUIDELINES §21)

Medido com Range + `getClientRects()` agrupado por `top`, tomando a extensão `right − left` de cada linha (somar as larguras dos rects superestima quando o Chrome devolve um rect por palavra **mais** um por linha, e foi o que gerou número falso na primeira medição).

| Bloco | Antes | Depois | Alavanca |
|---|---|---|---|
| `.hero h1` | 6 linhas, 29 % (com 46 px/26ch) e 4 linhas, 44 % (com 43 px/32ch) | **3 linhas, 15 %** | coluna do hero de `1.06fr` para `1.32fr`, teto de 46 px para 40 px, medida para 28ch |
| `.cta h2` | 2 linhas, 47 % ("Entre em" / "contato conosco!") | **1 linha, 0 %** | teto de 40 px para 32 px, medida para 26ch |
| `.consult h2` | 4 linhas, 29 % | **2 linhas, 20 %** | medida de 21ch para 30ch |
| `.video h2` | 4 linhas, 37 % com órfã na última | **3 linhas, 23 %** | teto de 40 px para 36 px, medida para 24ch |

Confirmação da ressalva 4 do §21: **o teto de fonte é a alavanca, não o `balance`.** O `balance` não junta linhas, então em bloco que já caiu em 4 ou 6 linhas ele só redistribui a raggedness. Os três blocos acima só melhoraram quando o teto (ou a medida) mudou o número de linhas.

Sobrou em 27 %: `.feat-title` da feature 01 ("Organize seu atendimento de forma integrada", 2 linhas). Sem órfã, e as duas linhas têm 4+ palavras. Fica como está.

### Contraste (GUIDELINES §7)

Varredura de 31 elementos de texto contra o fundo efetivo. Uma reprovação real:

- `.cta-lead` em `#E4EAFB` sobre o topo do gradiente `#4A69BD` dava **4.27:1** e reprovava o AA de texto normal (17 px). Trocado para `#F4F7FF` = **4.80:1**. O gradiente escurece para `#3C58A6` daí para baixo, então o contraste só melhora ao longo da seção.

Escolhas de cor que já entraram pensando em contraste:
- **"WhatsApp" em verde no H1 e no H2 da faixa do consultor** usa `#12703E` (6.5:1), não o verde oficial `#25D366` (1.98:1 no branco, reprova como texto). A página de origem usa o verde claro; aqui o realce mantém a intenção sem reprovar.
- **CTA laranja "Fale agora!"** usa laranja como preenchimento e **texto navy** (5.6:1). Laranja Cxpress nunca como cor de texto.
- **FAB do WhatsApp**: o glifo branco no verde oficial é a marca e fica; quem cumpre o 3:1 de limite de controle (WCAG 1.4.11) é o anel `--wa-ink` (`#15884D`, 3.4:1) no `box-shadow`. O pulso anima só o `::after`, então o anel de contraste nunca é redesenhado.

### Movimento

- Cena do hero pausa fora de vista (`.fx-idle` por IntersectionObserver) e **não existe** sob `prefers-reduced-motion` nem abaixo de 720 px.
- Escurecimento do holofote baixado de 30 % para 20 %: em 30 % a tela do produto ficava suja no primeiro quadro do ciclo, que é justamente o que o visitante vê antes de a animação começar.
- **Conectores tracejados removidos do hero.** Com holofote, digitação, selos de canal, malha de pontos, halo verde e anel inclinado, o hero passava do "um elemento visual forte, não encher de formas" da §3. O CSS morto foi removido junto (zero ocorrência de `.conn` no arquivo).

### Fidelidade da copy

Extraídas as 78 strings visíveis da página renderizada e comparadas com o `copy.txt`. Resultado: **todas** casam literal com a página de origem, fora a whitelist prevista (skip link, rótulo curto da navbar em telas estreitas, rótulos e boilerplate do formulário e do modal, linha legal do rodapé, "Carregando o formulário…"). Zero pull-quote inventado, zero kicker novo, zero punchline de marketing.

Nenhum texto foi encurtado, parafraseado ou trocado por sinônimo. A quebra do parágrafo de "Quem somos" em dois é escolha de leitura: nenhuma palavra mudou.

### Anti-IA

- Em-dash: **0** ocorrências (`—` e `&mdash;`), na copy e no HTML.
- Aspas curvas e ellipsis (`&hellip;`) aplicados.

---

## 3. Checklist determinístico

| Verificação | Resultado |
|---|---|
| `meta name="description"` | 1 |
| `meta property="og:` | 10 (mínimo 8) |
| `meta name="twitter:` | 4 (mínimo 4) |
| `application/ld+json` | 1, parseia; grafo com Organization, WebPage, SoftwareApplication e FAQPage |
| FAQPage vs FAQ visível | 5 e 5, mesmas perguntas |
| `rel="canonical"` | 1 |
| `meta name="robots"` | 1 |
| GTM `GTM-T4XDWHL3` | 2 ocorrências (script no `<head>`, `noscript` após `<body>`) |
| Logo com `href="/"` | 0 (navbar e rodapé apontam para `https://home.cxpress.io`, `target="_blank" rel="noopener"`) |
| `<img>` sem `alt` | 0 |
| Assets referenciados que não existem | 0 |
| `noscript` de fallback do `.reveal` | presente |
| Ordem das seções vs página de origem | igual |
| Overflow horizontal, 1280 px | 0 |
| Overflow horizontal, 375 px | 0 |
| Pisos tipográficos mobile (§20), 20 papéis | todos cumpridos |
| Fachada do vídeo | clique cria o iframe `youtube-nocookie` com `autoplay=1` e remove o botão |
| FAB e modal | abre, trava o scroll do body, carrega o Jotform sob demanda, marca `aria-expanded`, move o foco para o fechar; fecha por botão, clique no fundo e Esc, e destrava o body |

Um detalhe que já custou caro antes e está coberto: a página tem **dois embeds do mesmo formulário** (a seção e o modal), e o resizer do `jsform` acha o iframe pelo id do **formulário**, não do elemento. Sem o listener registrado antes do `jsform`, os dois embeds se redimensionariam entre si. O listener aplica a altura no iframe do modal e barra a mensagem ali.

---

## 4. Nice-to-haves (nada quebra hoje)

- [ ] `tela-chatbot-whatsapp.svg` aparece **duas vezes**: no hero (recortada pelo holofote, animada) e na feature 02 (inteira, estática). É a tela certa para as duas ("IA no primeiro contato" não tem outra), e os tratamentos são bem diferentes, mas se incomodar a saída é dar à feature 02 um card de badge "Api Oficial do ChatGPT", como a página de origem faz.
- [ ] `CONSULTOR` e `PLATAFORMA` são duas seções brancas seguidas. Separadas por filete mais 128 px de respiro, e o card cheio do CONSULTOR dá identidade à faixa. Tingir uma das duas resolveria, mas encostaria tint em tint com a PROVA (ou apagaria o halo azul-claro que fica atrás das telas da PLATAFORMA).
- [ ] Números da PROVA entram estáticos. As LPs irmãs animam a contagem ao entrar na tela; aqui o valor final já está no HTML e não há JS de contagem. Vale se quiser o mesmo brilho da `banimento-de-whatsapp`.
- [ ] `assets/telas/tela-agentes.svg`, `tela-disparo-ativo.svg` e `tela-tickets.svg` ficaram sem uso. Mantidos de propósito (telas já otimizadas), mas são 3 arquivos pesados sem referência.
