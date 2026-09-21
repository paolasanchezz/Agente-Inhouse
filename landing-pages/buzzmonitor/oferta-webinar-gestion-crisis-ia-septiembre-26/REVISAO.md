# Revisao — buzzmonitor/oferta-webinar-gestion-crisis-ia-septiembre-26

**Data:** 2026-09-21
**Passadas:** design review (GUIDELINES) + Web Interface Guidelines (Vercel Labs) + checks deterministicos (GTM, fidelidade de copy, pisos tipograficos, contraste medido no browser)

Contraste medido no navegador (Chromium, 1440 e 375), com o fundo efetivo composto por secao. Overflow horizontal medido nos dois breakpoints.

---

## CRITICOS — aplicados

1. **Texto invisivel no formulario.** `.form-note` (aviso de compliance) perdia por especificidade para `.final p` (`color: rgba(255,255,255,.94)`) e renderizava branco sobre o card branco. Reescrito como `.form-card .form-note`.
2. **Foco de teclado removido nos campos.** `.field input:focus, .field select:focus` tinha `outline:none` com especificidade maior que o `:focus-visible` global, apagando o anel de foco nos 7 campos (WCAG 2.4.7). O `outline:none` foi removido; a borda laranja continua como reforco visual.
3. **Eyebrow de CLIENTES reprovava AA.** "Quiénes ya confían" em laranja `#EB7C2E` sobre off-white `#f5f5f5` dava **2.58:1** (14px, precisa 4.5). Trocado para roxo `#390155` (padrao GUIDELINES §7: quanto mais claro o fundo, mais escuro o texto).
4. **Secao CTA FINAL reprovava AA inteira.** Fundo laranja solido com texto branco: H2 **2.82:1** (texto grande precisa 3) e corpo **2.66:1** (precisa 4.5). Trocado para o gradiente da marca com scrim escuro (`rgba(28,1,45,.62)`), que leva o texto branco a ~9.8:1.
5. **Botoes primarios reprovavam AA.** `.btn-primary` e `.nav-cta` eram branco sobre laranja: **2.82:1** em 17px/15px bold. Texto trocado para roxo `#390155` sobre o mesmo laranja = **5.70:1**. O hover (fundo roxo) passou a forcar `color:#fff`, senao ficaria roxo sobre roxo.
6. **Badge do hero reprovava AA na ponta laranja.** O pill com o gradiente cheio deixava "OFERTA EXCLUSIVA DEL WEBINAR" em branco sobre laranja na metade direita. Recebeu scrim `rgba(28,1,45,.45)` (~7:1).
7. **Numeracao dos modulos reprovava AA.** `.module-idx` ("01".."04") em laranja sobre branco: **2.82:1** em 14px bold. Trocada para roxo.
8. **Gradiente atras de texto corrido.** A secao OFERTA usava `var(--grad)` como fundo de toda a secao, com paragrafo, 3 cards e bonus por cima (risco de AA na metade laranja, e GUIDELINES §1 pede o gradiente em 1-2 momentos de impacto, nao como fundo de secao). Virou roxo solido; o gradiente ficou restrito a 2 momentos: badge do hero e CTA final.

Resultado apos os fixes: **nenhum texto da pagina reprova AA** (varredura automatizada em todos os `h1,h2,h3,p,li,span,a,label,button,option`).

---

## MELHORIAS — aplicadas (baratas, sem risco)

- `touch-action: manipulation` no `<html>` (remove o atraso de 300ms do duplo-toque).
- `<meta name="theme-color" content="#390155">`.
- `inputmode="email"` + `spellcheck="false"` no e-mail e `inputmode="tel"` no telefone.
- `loading="lazy"` no logo do rodape (below the fold).

---

## MELHORIAS — nao aplicadas (decisao do Victor)

- ~~**Data de encerramento da oferta.**~~ **Resolvido em 2026-09-21:** o usuario definiu **30 de setembro**. Aplicada na pilula da secao OFERTA ("válida hasta el 30 de septiembre") e no corpo da URGENCIA ("La oferta cierra el 30 de septiembre."). O selo da URGENCIA ficou generico de proposito, pra nao repetir a data tres vezes na mesma tela.
- **O laranja `#EB7C2E` com texto branco reprova AA em toda a marca**, nao so aqui: a LP irma publicada `webinar.buzzmonitor.com/gestion-crisis` tem o mesmo CTA em 2.82:1, e `brand/buzzmonitor/generation-rules.json` prescreve `ctaButton: secondary (#EB7C2E) com neutral.0 como texto`. **Resolvido nesta LP pelo restyle** (ver secao abaixo): o CTA primario passou a ser roxo com texto branco (16:1), que e tambem o tratamento do criativo do webinar e ja e o padrao do CTA de navbar da LP irma. A divida segue aberta nas demais LPs da marca: corrigir a regra no `generation-rules.json` e propagar e uma decisao de marca, fora do escopo desta pagina.
- **Numeracao "01".."04"** nos cards da OFERTA e nos MODULOS nao vem do `copy.txt`. Sao ordinais decorativos, sem carga semantica, e foram pedidos na direcao de arte. Se a leitura estrita de GUIDELINES §9 valer tambem para ordinais, e so remover os `<span class="offer-num">` e `<span class="module-idx">`.

---

## NICE-TO-HAVE

- O mural de clientes e um JPEG (2 imagens, ~310 KB somados) herdado da LP de agosto. Versoes WebP cortariam ~60% do peso.
- O count-up das metricas formata com `toLocaleString('es-419')` e depois restaura o texto literal da copy. Funciona, mas um `font-variant-numeric: tabular-nums` evitaria o leve tremor de largura durante a contagem.
- Os 3 cards da OFERTA tem alturas diferentes (o terceiro item da copy e bem mais longo). Alinham no topo, o que esta ok, mas encurtar o item 3 na copy equilibraria o grid.

---

## Checks deterministicos

| Check | Resultado |
|---|---|
| `check_gtm_region.py` | `ok` — regiao `latam` (via `<html lang="es-419">`), esperado e encontrado `GTM-MKQBX2MG`. Selo `.tracking.lock` gravado. |
| Em-dash (`—` / `&mdash;`) | 0 ocorrencias |
| Fidelidade da copy | Nenhum texto fora do `copy.txt` alem da whitelist (labels e disclaimer do form, opcoes de select, footer, skip-link, `<title>`, ordinais decorativos) |
| SEO (GUIDELINES §15) | 1 description, 10 `og:`, 4 `twitter:`, canonical, robots, JSON-LD com 3 nos (parseia) |
| Favicon | 1 unico `rel="icon"` apontando pro `logo-icon.png` do brand |
| Logos SVG (§19) | `grep -c '<text'` = 0 nos 3 logos (sao raster base64, web-safe) |
| Header/footer (§17) | Ambos apontam pra `https://getbuzzmonitor.com/es/` com `target="_blank" rel="noopener"` e `aria-label` em espanhol. Nenhum `href="/"`. |
| Pisos tipograficos mobile (§20) | Aplicados via `bump_mobile_type.py`: H1 38px, H2 34px, corpo/botao 17px, labels 14px+ |
| Overflow horizontal | 0 em 1440px e 0 em 375px (`scrollWidth == clientWidth`) |
| Ordem no mobile (§3) | `.hero-content` antes de `.hero-visual`, sem `order` no breakpoint |
| OG image (§18) | `assets/og-oferta-webinar-gestion-crisis-ia-septiembre-26.png`, 1200×630, 59 KB. Nenhum `og-image.png` sobrando. |

---

## Restyle sobre o criativo do webinar (2026-09-21)

O Victor mandou o criativo do webinar "Gestión de Crisis con IA" (24/set, speakers Raquel Oliveira e Luis Perez) e pediu um estilo mais moderno com base nele. A LP foi restilizada; **nenhum texto mudou** (a auditoria de fidelidade foi re-rodada e nao acusou nada fora da copy e da whitelist).

O que veio do criativo:

| Elemento do criativo | Como entrou na LP |
|---|---|
| Fundo creme | `--cream:#FBF6F1` como fundo base, alternando com branco e `#F4ECE4` |
| Trama de pontos coral (halftone) | `.dots` em CSS puro (`radial-gradient` + `mask`), em 6 pontos da pagina, escondida no mobile |
| Display preta com palavra em coral/degrade | H1 preto `#131313` com "en tiempo real." em coral; display da oferta no gradiente 3 do brand |
| Pill roxa "WEBINAR GRATUITO" com sombra deslocada | `.badge` do hero e `.seal` da urgencia, com `box-shadow:6px 6px 0` coral |
| Badge coral "SPEAKER" | `.eyebrow` virou pilula coral com texto branco |
| Icones de linha (radar, escudo, balao) | Icones X e check redesenhados como stroke fino dentro de circulo |
| Radar com aneis concentricos | Painel do hero com `repeating-radial-gradient` + blip coral |

Decisoes que o restyle forcou, todas re-validadas:

1. **Gradiente trocado.** Saiu `#390155 -> #EB7C2E`, entrou o **gradiente 3 do brand** (`tokens.json`: `#DE2451 -> #EB7C2E`), que e o do criativo. Continua sendo um gradiente so (GUIDELINES §1).
2. **CTA primario virou roxo com texto branco** (16:1), hover coral (4.7:1). Fecha o furo de AA do item 5 sem inventar cor e alinha com as pills roxas do criativo.
3. **Coral `#DE2451` entrou na paleta.** E o `pink` do `tokens.json`, nao uma cor nova. A LP roda com roxo + coral + laranja sobre creme.
4. **Gradiente como texto** no display da oferta (`background-clip:text`) tem fallback `color:var(--orange)` fora do `@supports`, e fica sobre roxo solido: pior ponto do gradiente da 4.47:1, acima do minimo de 3 pra texto grande.

Bug encontrado e corrigido no restyle:

- **Count-up podia congelar num numero errado.** Se o `requestAnimationFrame` fosse interrompido (aba em segundo plano, dispositivo lento), a metrica ficava em "999+" em vez de "1.000+". Reproduzido em captura headless. Agora um `setTimeout` de 2.2s restaura o valor literal da copy independentemente do estado da animacao.

Revalidacao pos-restyle: **0 falhas AA** em 1440 e 375, **0 overflow horizontal** nos dois, pisos tipograficos §20 ok (`bump_mobile_type.py` nao acusou nada), GTM `ok`, em-dash 0, fidelidade de copy limpa. OG image regerada no novo estilo.

---

## Ajustes de 2026-09-21 (pos-restyle)

### Hero: grafico de social listening no lugar do radar generico

O usuario achou o painel da direita generico demais e pediu um elemento grafico que remeta a social listening ou a um beneficio da Buzzmonitor. O radar de aneis concentricos (e a marca d'agua "15") saiu e entrou um **SVG inline de volume de mencoes**: linha de base com ruido, **umbral de alerta tracejado**, escalada cruzando o umbral com pontos em coral (sentimento negativo) e **pico destacado com halo pulsante**.

Por que este e nao outro: conta exatamente a promessa da LP, que ja esta na copy. "La señal débil identificada antes del pico de menciones", "El ruido separado de la amenaza real" e "Alertas automáticas" viram uma imagem so. O H1 ("De la primera señal a la respuesta correcta") passa a ter um correspondente visual direto.

Detalhes tecnicos:
- SVG inline, `aria-hidden="true"` e `focusable="false"`. **Zero texto** no grafico, entao nao abre excecao na regra de fidelidade de copy (GUIDELINES §9).
- O halo pulsa com `transform: scale()` sobre `transform-box: fill-box; transform-origin: center` (recomendacao das Web Interface Guidelines pra transform em SVG), nao com animacao do atributo `r`.
- Sob `prefers-reduced-motion` a animacao ja e neutralizada pela regra global da LP.
- A marca d'agua "15" foi removida: com o grafico, o painel passaria a ter dois elementos fortes disputando atencao (GUIDELINES §3 pede um so).

### Formulario real integrado (Jotform 241825239057661)

Mock substituido pelo embed `jsform` indicado pelo usuario. O bloco `.form-card` inteiro foi trocado (nao so o `<form>`), pra nao sobrar o card do mock em volta do card do provedor.

**Excecao consciente a regra de "wrapper sem card" da `lp-integrar-form`.** A skill manda nao dar `background`/`padding` ao wrapper porque os provedores costumam trazer card proprio (incidente 2026-04-30). **Este formulario nao traz**: renderiza com fundo transparente e rotulos escuros. Sem card, o texto do form caia direto sobre o fundo escuro da secao de CTA final e ficava ilegivel, com destaque pro rotulo do checkbox de newsletter. O wrapper `.jotform-embed` recebeu entao `background: #fff` + `border-radius` + `padding` + sombra, replicando o card que o mock tinha. No mobile o padding cai pra 18px/14px pra nao espremer o iframe. O racional esta comentado no proprio CSS.

Verificado no navegador: iframe carrega, ocupa 100% da largura do wrapper, `parentURL` e transmitido (alimenta o *Get Parent URL* e portanto o `url_conversao` no CRM), **zero erro no console**, nenhum `.form-card` orfao e nenhum handler de submit em JS sobrando.

### Revalidacao apos os 3 ajustes

| Check | Resultado |
|---|---|
| Contraste AA (1440 e 375, varredura automatizada) | 0 falhas |
| Overflow horizontal (1440 e 375) | 0 |
| Pisos tipograficos §20 | `bump_mobile_type.py` nao acusou nada |
| GTM | `ok` (latam / `GTM-MKQBX2MG`), selo regravado |
| Em-dash | 0 |
| Form mock remanescente | 0 |
| Erros no console | nenhum |

---

## Troca do visual do hero por imagem (2026-09-21)

O grafico SVG de sinal saiu e entrou a imagem enviada pelo usuario (`Webinar LATAM ADS  Monitoreo de competidores.png`, 1080x1080, fundo transparente): notebook com painel de atividade da concorrencia e lupa ampliando publicacoes recentes, com circulo laranja e trama de pontos roxa ja na propria arte.

Tratamento do arquivo:
- Recortado no bounding box (a arte tinha 156 px de transparencia a esquerda), redimensionado pra 1000 px de largura e quantizado pra 256 cores: **1.303 KB -> 157 KB** no PNG.
- Gerado tambem WebP (**117 KB**), servido por `<picture>` com o PNG como fallback (convencao de `landing-pages/CONTEXT.md` §3.6).
- `<img>` com `width`/`height` explicitos (evita CLS), `fetchpriority="high"` (e acima da dobra), `decoding="async"` e `min-height: 0` (GUIDELINES §14, bug do Safari iOS em grid item).
- `alt` descritivo em espanhol, sem copy de marketing.

Ajuste de composicao: a trama de pontos coral do canto inferior direito do hero (`.dots--b`) foi removida, porque a propria imagem traz uma trama roxa naquele mesmo canto e as duas empilhadas viravam ruido.

O painel roxo com o "15" e a linha "15 días gratis de Buzzmonitor" saiu junto. A frase segue na secao OFERTA, que e onde a copy a coloca. O hero ficou com exatamente os blocos que o `copy.txt` pede (BADGE, H1, SUB, CTA) mais o visual.

### Ponto de atencao de conteudo (nao bloqueante)

A imagem tem texto embutido: "Actividad de la competencia", "Menciones por periodo", "Competencia A / B / C", "Nuevo lanzamiento", "Promocion limitada", "Campana de verano". Duas consequencias:

1. **Tema.** E um painel de *monitoreo de competidores*; esta LP vende *gestion de crisis*. Um painel de sentimento ou de alertas casaria melhor com a copy ("La señal débil identificada antes del pico de menciones", "Alertas automáticas"). Decisao do usuario, mantida.
2. **Fidelidade de copy.** Esse texto vive dentro de um PNG, entao nao entra na auditoria de fidelidade (que cobre texto no HTML) e nao viola GUIDELINES §9. Mas e texto visivel na pagina e nao foi revisado pelo pipeline de copy. Vale saber que ele existe.

### Revalidacao

| Check | Resultado |
|---|---|
| Contraste AA (375) | 0 falhas |
| Overflow horizontal (375) | 0 (`scrollWidth == clientWidth`) |
| Imagens com `alt` + `width`/`height` | 5/5 |
| Pisos tipograficos §20 | nada a ajustar |
| GTM | `ok`, selo regravado |
| Em-dash | 0 |

---

## CTA do header (2026-09-21)

A pedido do usuario: texto trocado de "Quiero aprovechar la oferta" para **"Acceder a la oferta"** e botao reduzido em 20% nos dois breakpoints.

| | antes | depois |
|---|---|---|
| Desktop | 15px / padding 13px 24px | **12px / 10px 19px** (altura 40px) |
| Mobile | 14px / padding 11px 18px | **11px / 9px 14px** (altura 36px) |

O novo texto foi registrado num bloco `=== HEADER ===` no `copy.txt`, pra sobreviver a um `/lp-gerar` futuro e nao virar texto orfao na auditoria de fidelidade.

**Dois desvios conscientes, decididos pelo usuario:**

1. **Abaixo do piso tipografico.** GUIDELINES §20 poe botao em 17px e label/caption em 14px como minimo. O CTA da navbar ja vivia abaixo disso (15/14px) pela excecao de `white-space: nowrap` da propria §20; com o corte de 20% vai pra 12/11px, agora claramente abaixo do piso de 14px.
2. **Alvo de toque abaixo de 44px.** No mobile o botao fica com 36px de altura, abaixo dos 44px recomendados para alvo de toque. Continua clicavel, mas exige mais pontaria em tela pequena.

Meio-termo se algum dos dois incomodar depois: manter a fonte em 14px e tirar os 20% so do `padding`. O botao encolhe visivelmente e os dois pisos sobrevivem.

Contraste nao mudou: branco sobre roxo `#390155`, 16:1.

---

## Hero sangrado no canto inferior direito (2026-09-21)

O usuario reportou sobra de fundo creme a direita e abaixo da imagem, visivel sobretudo com zoom de 100-110% (viewport efetivo ~1070 px). Causa: a imagem era uma coluna do grid dentro do `.shell` (max-width 1200 + padding 28), entao sempre sobrava o padding do shell a direita e o padding da secao embaixo.

O que mudou:

- **`.hero-visual` saiu do `.shell`** e virou filho direto de `.hero`, depois do `.shell` no DOM. Fora do shell, pode ancorar no proprio limite da secao; e depois do texto no DOM, continua empilhando abaixo dele no mobile (GUIDELINES §3, headline sempre primeiro, sem `order`).
- **Ancorada em `right:0; bottom:0`** com `width: clamp(360px, 43vw, 740px)`. Encosta nos dois lados em qualquer largura, e como escala por `vw`, acompanha qualquer nivel de zoom sem precisar de regra especial.
- **`.hero` virou flex com `min-height: min(680px, 86vh)`** e alinhamento central, pra o texto ficar verticalmente centrado com a arte.
- **Coluna de texto limitada** a `clamp(420px, 46vw, 640px)`, pra nao correr por baixo da imagem. Como efeito colateral bom, o H1 fecha em 4 linhas em vez de 5 nas larguras grandes.
- **Mobile**: imagem full-bleed (`width:100%`) abaixo do texto, com `padding-bottom:0` no hero, colada na base da secao.

Por que ancorar exatamente nesses dois lados: a arte ja sangra em cima, a direita e embaixo (o notebook e cortado no topo e na direita, a lupa e a trama de pontos alcancam a base). Medindo o canal alfa do PNG, a coluna da direita tem 91% de cobertura e a linha da base 46%. Colar em `right/bottom` aproveita esse sangramento; colar na esquerda exporia a area transparente da arte.

Medido no navegador a 1440: folga a direita **0 px**, folga abaixo **0 px**, folga entre o bloco de texto e a imagem 25 px (a arte comeca bem depois disso, entao a respiracao visual e maior).

Conferido em 1024, 1070, 1280, 1440, 1680 e 375: sem borda sobrando, sem sobreposicao de texto e sem scroll horizontal (`scrollWidth == clientWidth`).

Revalidacao: 0 falhas AA, pisos tipograficos §20 sem pendencias, GTM `ok`, em-dash 0, `build_umbrella.py` sem avisos para esta LP.
