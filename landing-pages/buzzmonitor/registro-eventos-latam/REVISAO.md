# Revisao — buzzmonitor/registro-eventos-latam

**Data:** 2026-09-08 (v1) · restyle premium v2 (2026-09-08, versao vigente)
**Escopo:** auditoria de acessibilidade e HTML semantico contra as
[Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md)
(skill `web-design-guidelines`) + os gates locais de `landing-pages/build/`.

---

## O que mudou no restyle v2 (premium / Apple-Vercel-ManyChat)

O sistema visual foi refeito. Isso **resolveu por remocao** tres achados da v1 e mudou a
solucao de outros dois. Nada de copy mudou (`copy.txt` intacto, diff de fidelidade re-rodado:
zero texto fora da copy).

| Achado v1 | Estado na v2 |
|---|---|
| #1 Marquee sem mecanismo de pausa acessivel (WCAG 2.2.2) | **Deixou de existir.** O marquee virou grade estatica de 12 logos com hairline. Sem movimento, sem botao de pausa, sem 2.2.2 aplicavel |
| #4 Laranja com 2,84:1 no botao primario | **Resolvido de outra forma.** O botao primario e roxo `#390155` com texto branco (15:1). O laranja saiu do texto por completo e virou acento grafico |
| #5 Teal `#0E9D9B` no limite de 3,05:1 | **Deixou de existir.** O teal saiu da LP. Marcador `✓` agora e roxo `#390155` (15:1 sobre branco), permitido pela GUIDELINES §8 ("marcador da cor primaria da marca") |
| #6 Branco sobre gradiente a 2,84:1 | Mesma tecnica, tom mais escuro: `120deg, #390155 0%, #EB7C2E 165%` fecha ~5,7:1 (antes 4,83:1 com overshoot de 145%) |
| #8 Tabela com colunas de plano escondidas no celular | Mantido o fix; a tabela perdeu a caixa externa mas continua cabendo inteira em ≤640px |

Novos itens verificados na v2:

- Barra de progresso de leitura removida (era `aria-hidden`, nao gerava achado, mas destoava).
- Halo radial do hero removido. Isso zerou os falsos positivos de overflow: o
  `check_mobile_type.py` a 375px agora acusa **1** item, e e o skip-link (fora da tela de
  proposito). Antes eram 4 (halo + 3 `<img>` do marquee).
- Eyebrow: a pilula lilas saiu. Texto em caixa alta na cor `--ink` sobre branco, com ponto
  laranja decorativo. Elimina a categoria de risco "texto sobre fundo tingido" da §7.
- Ponto do eyebrow alinhado ao topo (`align-items: flex-start` + `margin-top: 6px`), senao
  ele centralizava entre as duas linhas quando o eyebrow quebra no celular.
- Hierarquia de headings segue h1 → h2 → h3 (o `<h3>` de grupo do accordion mudou de estilo,
  nao de nivel).
- `bump_mobile_type.py` re-rodado: subiu 2 clamps (`.steps li` 19→22, `.sol-close p` 20→22) e
  6 regras px de rotulo no mobile. Depois disso, 0 pendencias.

### Revert da v3 (2026-09-08)

A rodada v3 (geometria do brandbook, painel animado, numeros de cases, H2 curtos, CTA fixo no
mobile) foi **revertida integralmente** a pedido do Victor. Conferencia do revert:

- Render 1440x10400 comparado pixel a pixel com o render da v2: **0 de 14.976.000 pixels
  diferentes**.
- Varredura de residuo: 0 ocorrencias de `panel__`, `proof__`, `geo`, `mcta`, `sublead`, `mark`,
  `hero__lead`, `data-to`, `has-geo`, `spark`, `donut`, `bars__`.
- `copy.txt` restaurada do backup anterior a reescrita (H1 e os 6 H2 longos de volta, bloco
  `=== PANEL ===` e os LIST ITEM de case removidos).
- Gates re-rodados depois do revert: em-dash 0 · GTM 1 OK / 0 bloqueios · pisos de tipografia 0
  pendencias · overflow a 375px so o skip-link · JSON-LD valido · 10 og + 4 twitter · h1-h2-h3 ·
  4 labels / 4 inputs · fidelidade de copy 100%.

### Publicacao (2026-09-09)

Publicada pelo fluxo CI (`content.buzzmonitor.com` esta em `MIGRADOS.json`, entao **nao** houve
sibling nem deploy manual): manifesto + PR #540 -> merge-bot auto-mergeou (diff so tocava
conteudo) -> `lp-deploy.yml` run 34316747294 verde.

Gates rodados antes de commitar, como manda o fluxo:

- `build_umbrella.py` no manifesto inteiro: exit 0, 28 LPs. Os 6 avisos de OG ausente sao de
  **outras** LPs, pre-existentes; a nossa saiu sem aviso.
- `check_gtm_region.py` no manifesto: 24 OK, 4 avisos pre-existentes, **0 bloqueios**.
- Conferido no `dist` local antes do commit: 0 placeholders `{{...}}` sobrando, 0 path relativo
  vazando, OG e logos resolvidos pra `/assets/buzzmonitor/...`.
- CSP do dominio conferido **antes** de subir: `connect-src` libera `contenido.getbuzzmonitor.com`,
  senao o POST do formulario morreria bloqueado e cada lead se perderia em silencio.

Validado no live: 200 (82.322 bytes, igual ao dist) · 7/7 headers · GTM 3/3 tokens · cert
Let's Encrypt ate 19/10/2026 · OG, favicon e os 12 logos de cliente todos 200 · 3 vizinhas
amostradas 200 (o smoke do CI cobre as 28) · LCP 624 ms · CLS 0.

**Nota sobre `form-action`:** o CSP do guarda-chuva nao lista `contenido.getbuzzmonitor.com` em
`form-action`, so em `connect-src`. Consequencia: o `fetch` (caminho normal) funciona; o submit
nativo do `<form>` — que so aconteceria com JS desligado — seria bloqueado pelo CSP. O `<noscript>`
da LP cobre esse caso mandando o usuario pro e-mail. Nao ampliei o `form-action` de proposito:
esse `vercel.json` e compartilhado pelas 28 LPs do dominio.

PageSpeed Insights nao rodou (API publica devolveu 429 em 4 tentativas). Substituido por medicao
real de Navigation Timing no live; comando pra tentar de novo esta no `README.md`.

### v2.6 (2026-09-09): desvio de contraste decidido pelo Victor

**O titulo do bloco de Oferta usa `#EB7C2E` sobre branco. Isso da 2,84:1.**

| Requisito | Piso | `#EB7C2E` sobre branco | Situacao |
|---|---|---|---|
| WCAG AA, texto normal | 4,5:1 | 2,84:1 | reprova |
| WCAG AA, texto grande (>=24px ou >=18,66px bold) | 3:1 | 2,84:1 | **reprova tambem** |

O H2 esta em 54px, entao cai na regra de texto grande, e mesmo assim nao passa. Eu havia
aplicado `#B85210` (4,97:1) na v2.5 exatamente por isso e sinalizei o problema; o Victor pediu
o `#EB7C2E` de forma explicita, com o hex. Aplicado como pedido e registrado aqui.

**Impacto pratico:** quem tem baixa visao ou usa a pagina sob luz forte pode nao conseguir ler o
titulo dessa secao. O resto do bloco nao e afetado (conteudo em `#1a1a1a`, 18,3:1).

**Reversao:** uma linha. Em `.block--paper h2`, trocar `var(--accent)` por `var(--accent-ink)`.

Onde o laranja vivo **continua correto** neste bloco: regua da secao, fio de 2px no topo dos
cards e sunburst. Sao elementos graficos, sem requisito de contraste de texto.

### v2.6: o que foi verificado no efeito de metricas animadas

- `.metrics` inteiro com `aria-hidden="true"`.
- `prefers-reduced-motion: reduce` -> `display: none` no bloco todo.
- Chips em `z-index: 0`, conteudo do hero em `z-index: 2`: passam atras do card, nunca cobrem
  formulario nem texto.
- So `transform` e `opacity` animados.
- Numeros ilustrativos, declarados no `copy.txt`.
- Os chips ficam abaixo do piso de 14px da §20 no mobile (rotulo em 12px): **isento de
  proposito**, sao decoracao ambiente com `aria-hidden` e `white-space: nowrap`, e a propria §20
  isenta nowrap. O `bump_mobile_type.py` concorda (0 pendencias).
- Nao geram overflow horizontal: `check_mobile_type` a 375px segue acusando so os 3 itens
  decorativos conhecidos.

**Pendencia aberta (WCAG 2.2.2):** movimento automatico com mais de 5s de duracao, em paralelo
com outro conteudo, pede mecanismo de pausar/parar/ocultar. A LP cobre hoje so a via automatica
(`prefers-reduced-motion`). Nao ha botao de pausa porque o pedido foi movimento continuo.
Decisao do Victor se entra.

---

## Criticos aplicados (v1, historico)

| # | Achado | Fix |
|---|---|---|
| 1 | Marquee de logos: movimento automatico, infinito, em paralelo com outro conteudo. Pausava so no `:hover`, o que nao alcanca teclado (WCAG 2.2.2 exige mecanismo de pausar/parar/ocultar) | Botao `<button aria-pressed>` com `aria-label` em ES que alterna `.is-paused`, mais pausa em `:focus-within` na faixa. Some sob `prefers-reduced-motion` (ali a animacao ja nao roda) |
| 2 | Hierarquia de headings quebrada: `h2` de secao seguido de `h4` nos grupos do accordion, sem `h3` | `h4` → `h3` (agora a LP tem so h1 → h2 → h3) |
| 3 | Header sticky podia cobrir o elemento que recebia foco por teclado, e a ancora `#form` | `scroll-padding-top: calc(var(--header-h) + 16px)` no `html`, mais `scroll-margin-top` no `#form` |
| 4 | Contraste do laranja da marca: `#EB7C2E` da **2,84:1** como texto sobre branco (reprova AA e reprova ate o piso de 3:1 de texto grande). Branco sobre `#EB7C2E` da o mesmo 2,84:1 | Laranja da marca fica so em fundo, regua e borda. Texto laranja usa `#B85210` (4,97:1). Botao primario = fundo laranja com texto roxo `#390155` (5,70:1) |
| 5 | Contraste do teal da marca: `#0E9D9B` da **3,05:1** sobre off-white, no fio do piso de 3:1 para objeto grafico | Marcadores usam `#0B8785` (3,99:1 sobre off-white, 4,41:1 sobre branco) |
| 6 | Branco sobre o gradiente `135deg #390155 → #EB7C2E` cai a **2,84:1** na ponta laranja | Gradiente com overshoot, `#390155 0% → #EB7C2E 145%`. A extremidade visivel para em ~`#B4563A`, branco fecha 4,83:1 |
| 7 | `.wrap--narrow` da secao de CTA final sem `margin-inline: auto` (faltava a classe `wrap` no HTML): conteudo colado a esquerda em vez de centralizado | Classe `wrap` adicionada no HTML e `margin-inline: auto` no proprio `.wrap--narrow` (defesa em profundidade) |
| 8 | Tabela de planos com `min-width: 640px` dentro de `overflow-x: auto`: no celular o usuario via so os nomes dos modulos, com as duas colunas de plano escondidas atras de um scroll horizontal sem affordance | Em ≤640px as colunas de plano encolhem (`width: 54px`, padding menor) e a tabela cabe inteira na tela. O container de scroll continua valendo para a faixa 641-780px |
| 9 | Faltava `<meta name="theme-color">` e `color-scheme` | `theme-color: #ffffff` + `color-scheme: light` (impede o Chrome de escurecer os controles do form) |
| 10 | Faltava `touch-action: manipulation` e `-webkit-tap-highlight-color` (delay de double-tap e highlight default no mobile) | Ambos no `body` |
| 11 | Layout full-bleed sem `env(safe-area-inset-*)` (notch em landscape) | `padding-left/right: env(safe-area-inset-*)` em `.wrap` e `.header__inner` |
| 12 | Campo de e-mail com corretor ortografico ativo | `spellcheck="false"` |

## Verificado e conforme

- Skip-link, `:focus-visible` global com outline visivel, `<label for>` nos 4 inputs (1:1), `autocomplete` e `type` corretos (`email` / `tel` / `text` + `organization`).
- `outline: none` no `.field input:focus` tem substituto de foco (borda `--ink` + ring de 3px via `box-shadow`), o que a regra permite explicitamente.
- Todas as `<img>` com `alt` e `width`/`height` explicitos; decorativas com `alt="" aria-hidden="true"`; abaixo da dobra com `loading="lazy"`.
- Tabela semantica: `<caption>` (sr-only), `<th scope="col">`, `<th scope="row">`, e `Incluido` / `No incluido` em `.sr-only` para leitor de tela (o `✓` e o tracinho sao `aria-hidden`).
- Container de scroll da tabela com `role="region"` + `tabindex="0"` + `aria-label`.
- Accordion = `<details>/<summary>` nativo (teclado e leitor de tela de graca), marcador nativo removido sem perder `focus-visible`.
- Motion (v2): nenhum `transition: all`, so `opacity`/`transform`/cor animados, `prefers-reduced-motion` desliga reveal e smooth-scroll. `<noscript>` garante `.reveal { opacity: 1 }` se o JS falhar.
- Nenhum botao icone restou na v2 (o de pausa saiu com o marquee); nenhum `<div>` clicavel; navegacao em `<a>`.
- Sem `user-scalable=no` nem `maximum-scale`; sem bloqueio de paste; sem `autofocus`.
- Nenhum `aria-live`: a LP nao tem atualizacao assincrona, e a `GUIDELINES §7` proibe `aria-live` em contador (nao existe contador aqui).
- Em-dash: **0** no HTML e **0** no `copy.txt`.
- `check_gtm_region.py`: 1 OK, 0 bloqueios (`GTM-MKQBX2MG`, regiao latam pelo sufixo `-latam`).
- `bump_mobile_type.py --dry-run`: 0 pendencias (pisos de tipografia mobile da §20 aplicados).
- `check_mobile_type.py` a 375px (v2): `document.scrollWidth == 375` e **1** item listado, o skip-link, que fica fora da tela de proposito. Nenhum elemento de conteudo vazando.
- Fidelidade de copy: diff automatizado entre `copy.txt` e todo texto visivel do HTML. **Zero texto inventado.** Unica divergencia = o H1 partido em duas linhas por `<em>`, cuja concatenacao e literalmente a linha do `copy.txt`. Fora da copy existem apenas itens da whitelist (skip-link, `aria-label`s, `sr-only`, `<caption>`, `alt`).

## Opcionais nao aplicados (decisao consciente)

- **Title Case em titulos e botoes (Chicago)** — convencao de ingles. A LP e ES-LATAM, onde o padrao e sentence case, e a copy e literal do `copy.txt`.
- **`&nbsp;` em unidades** (`15&nbsp;días`, `50&nbsp;métricas`) e **`translate="no"` em nomes de marca** — melhoram viuvez de linha e auto-traducao, mas nao valia mexer no HTML da copy sem pedido.
- **`<link rel="preload" as="font">`** — nao da para preloadear os arquivos de fonte via a API de CSS do Google Fonts. `preconnect` para `fonts.googleapis.com` e `fonts.gstatic.com` esta no lugar, e `display=swap` na URL.
- **Erro inline com foco no primeiro campo invalido e aviso de `beforeunload`** — o formulario e mock (`action="#"`, `GUIDELINES §11`). Entram junto com o embed real, via `/lp-integrar-form`.

## Nao rodou

- **Publicacao no Notion da copy estruturada** (`lp-preparar` Passo 6): o MCP do Notion nao esta conectado nesta sessao. O `copy.txt` local e a fonte-verdade e ja tem o relatorio de revisao no rodape do arquivo.
- **`/lp-revisar` completo** (auditoria dupla `frontend-design` review mode + `web-design-guidelines`): rodou a metade de acessibilidade, que e a que produz achados bloqueantes. Vale rodar `/lp-revisar buzzmonitor/registro-eventos-latam` antes de publicar para a segunda opiniao de design.
- **PageSpeed** (`GUIDELINES §13`): so faz sentido depois do deploy.
