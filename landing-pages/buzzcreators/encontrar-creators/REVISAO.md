# Revisao LP — buzzcreators/encontrar-creators

**Data:** 2026-09-11
**Auditores:** design review contra `GUIDELINES.md` + `web-design-guidelines` (Vercel Web Interface Guidelines) + checks determinísticos do repo

## Aplicado automaticamente (9 críticos)

- [x] **COPY-VAZAMENTO: kicker inventado** na seção escura, `<p class="kicker">Depois da descoberta</p>` — trocado por "Conexão com o Buzzcreators", que é o nome da seção no briefing e já está no `copy.txt`.
- [x] **COPY-VAZAMENTO: rótulo decorativo fora da copy** no painel da seção escura, `panel__label` "Entregas" — a copy diz "briefing, convites, aprovações, acompanhamento e pagamentos". Trocado para "Acompanhamento" e a coluna do label foi de 96px para 124px para caber.
- [x] **COPY-FALTANTE: confirmação de registro** ("Registramos seu contexto...") existia no HTML e não no `copy.txt` — acrescentada ao `copy.txt` na seção FORMULÁRIO, com a nota de que só aparece depois de a captura ser salva.
- [x] **A11Y: âncora coberta pelo header sticky** — `[id] { scroll-margin-top: 92px }`. Sem isso, o CTA do hero rolava até `#formulario` com o topo do bloco escondido atrás do header.
- [x] **A11Y: erro de campo não anunciado** — `aria-live="polite"` nos 6 parágrafos `.field__error`. A validação já movia o foco para o primeiro campo inválido (`aria-describedby` cobria esse), mas os demais erros ficavam mudos.
- [x] **A11Y/QA: skip-link gerava overflow horizontal** — saiu de `left: -9999px` para deslocamento vertical (`top: -100px`, `:focus { top: 0 }`). O `check_mobile_type.py` acusava 1 overflow por causa dele; agora acusa 0.
- [x] **MOBILE: pisos de tipografia (GUIDELINES §20)** — `bump_mobile_type.py` aplicado, 27 regras no bloco `@media (max-width:640px)`. H1 34px, corpo 17px no celular.
- [x] **MOBILE: rótulo de compliance pequeno demais** — "Exemplo de interface" (`.mock__tag`) subiu de 12px para 14px. É rótulo exigido pelo briefing, não decoração.
- [x] **FORM: `<select>` nativo sem cor explícita** — `color` e `background-color` fixados. Sem isso o Windows em modo escuro pinta o texto do select por conta própria.

## Melhorias aplicadas junto (6)

- [x] `<meta name="theme-color" content="#ffffff">` e `color-scheme: light` no `html`.
- [x] `touch-action: manipulation` e `-webkit-tap-highlight-color` em elementos interativos (tira o atraso de 300ms do duplo toque).
- [x] `loading="lazy" decoding="async"` nas duas imagens abaixo da dobra (logo do bloco de confiança e do footer).
- [x] `spellcheck="false"` no campo de email.
- [x] `env(safe-area-inset-bottom)` no padding do footer (iPhone com notch).
- [x] `text-wrap: balance` em h1/h2/h3 (evita viúva na quebra de linha das headlines longas).

## Checks determinísticos

| Check | Resultado |
|---|---|
| Em-dash (`—` e `&mdash;`) | 0 / 0 |
| Fidelidade de copy | só whitelist sobrou (skip-link, "Voltar para a etapa anterior") |
| SEO | description 1 · canonical 1 · robots 1 · og 10 · twitter 4 · JSON-LD parseia |
| OG image | `assets/og-encontrar-creators.png`, 1200×630, sem `og-image.png` órfão |
| `check_gtm_region.py` | 0 bloqueios, 1 aviso (`tracking.json` do Buzzcreators está null) |
| `check_mobile_type.py` (375×812) | ovf=0 · h1=34 · corpo=17 |
| Logo SVG com `<text>` vivo (§19) | `logo-branca-2.svg` = 0. Header usa PNG |
| Simulação do build do guarda-chuva | 0 path relativo sobrando · 0 placeholder · 4/4 assets resolvem |
| Fluxo do formulário (Playwright) | etapa 1 → 2 OK · campo de agência condicional OK · submit mock não confirma nada |
| Modo conectado (endpoint falso) | 2 cards renderizados com motivo, evidência e ações · metadados da consulta OK |

## Desvios de GUIDELINES assumidos (documentados, não são achados)

- **§10, posição do formulário.** O default para ToFu é a 2ª seção; aqui o form é a 5ª. O briefing prescreve literalmente a ordem hero → o que entrega → como funciona → formulário (Seções 1 a 4), e a GUIDELINES permite override quando o briefing pede explicitamente. Os 3 CTAs acima do form rolam até ele.
- **§8, seção escura.** A gramática visual reserva o fundo escuro para urgência. Esta LP não tem seção de urgência (o briefing proíbe falsa urgência), então o escuro foi para a seção comercial, que é o outro momento de virada da página. Aparece uma vez só.
- **§8, marcador dos benefícios.** Os 3 cards de "o que a consulta entrega" usam marcador roxo da marca em vez do ✓ verde. A GUIDELINES autoriza a cor primária da marca, e verde brigaria com a paleta de 2 cores (roxo + laranja).

## Melhorias opcionais (3)

Para o Victor decidir. Nenhuma bloqueia publicação.

- [ ] **H1 lidera com a solução, não com a dor** (`GUIDELINES §5` + `fundamentos-copy §0`). O H1 é prescrito literalmente pelo briefing, então não foi trocado. Alternativa registrada no `copy.txt` e no Notion: H1 "Escolher creator por número de seguidores é um chute caro" com a linha do briefing indo para o H2. O recorte da dor hoje vive na faixa "Decisão", logo abaixo do hero.
- [ ] **Bloco de confiança magro** — hoje é só logo + assinatura institucional, porque não há prova social aprovada. Quando houver depoimento, case ou logo de cliente com indicação do produto, a seção ganha corpo.
- [ ] **FAQ ocupa 900px num container de 1180px** — deliberado (linha de leitura curta). Se preferir ocupar a largura toda, é uma linha de CSS.

## Nice-to-haves (2)

- [ ] `translate="no"` nos nomes de marca, para evitar que a tradução automática do navegador vire "Zumbido" em "Buzzmonitor".
- [ ] Title Case nos botões é regra das Vercel Guidelines pensada para inglês. Em PT-BR o padrão da casa é sentence case, mantido.

## Próximos passos

- Design aprovado? → `/lp-integrar-form buzzcreators/encontrar-creators "{snippet}"`
- Publicar: `content.buzzmonitor.com` é domínio migrado pro CI. Entrar no `landing-pages/dominios/content-buzzmonitor-com/manifest.json` e abrir PR. **Nunca `vercel deploy` à mão.**
