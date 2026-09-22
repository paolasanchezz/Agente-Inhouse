# Revisao LP — cxpress/custo-atendimento-manual

**Data:** 2026-09-10
**Auditores:** frontend-design (review mode) + web-design-guidelines
**Gates deterministicos:** check_gtm_region.py · bump_mobile_type.py · fidelidade de copy · pacote SEO §15 · logo §17/§19 · OG §18

## Aplicado automaticamente (4 criticos)

- [x] **Anel de foco reprovava 3:1 em fundo claro** — linha 98, `:focus-visible`. O outline era amarelo `#F1A908`, que da **2,02:1 contra branco** e falha WCAG 1.4.11 (o indicador de foco e elemento de UI, minimo 3:1). Atingia formulario, botao do form, links de nav e CTA nas secoes claras. Corrigido: outline navy `#232960` como padrao (**10,4:1** no branco) e override pra amarelo dentro das bandas escuras (`header`, `.hero`, `.fecho`, `.total`, `.footer`, onde amarelo da **6,7:1** no navy). Regra dupla, cascata na ordem certa, verificada no DOM.
- [x] **Frase de fecho nao era heading** — linha 752. Estava em `<blockquote>`, entao quem navega por headings no leitor de tela nao alcancava a frase-ancora da LP. E `<blockquote>` implica citacao de terceiro, o que essa frase nao e. A `copy.txt` rotula ela como **H2**. Corrigido pra `<h2>`, seletor CSS `.fecho blockquote` renomeado pra `.fecho h2`. Renderiza identico (branco, 40px).
- [x] **Citacao real do case estava em `<p>`** — linha 667. A `copy.txt` rotula "A IA cuida do volume..." como **QUOTE** e era o unico texto da pagina que e de fato citacao. Trocado pra `<blockquote class="case__quote">` (com `margin:34px 0 0` pra neutralizar a margem default do elemento). Os dois estavam invertidos: a citacao em `<p>` e o nao-citacao em `<blockquote>`.
- [x] **`aria-label` do mostrador afirmava numero fora da copy** — linha 435. Dizia "turno de 8 horas", e a `copy.txt` nunca fixa a duracao do turno (fala "meio turno"). Trocado por "Meio turno de cada atendente consumido por trabalho manual", que usa o enquadramento literal da copy.

## Melhorias opcionais (4)

Para voce decidir. Aplicar via Edit manual ou pedir `/lp-revisar` de novo.

- [ ] **Check verde fraco em relacao ao X vermelho** — `.card__check`. Verde `#1AAE63` sobre `#E4F8EE` da **2,64:1**; o X vermelho da secao de cima (`.tarefa__x`) da **4,73:1**. Os dois formam a gramatica visual do §8 (X vermelho = problema, check verde = beneficio), e o verde vai parecer lavado ao lado do vermelho. Como o icone e `aria-hidden` e o H3 carrega o sentido, nao e violacao formal de contraste, mas e inconsistencia visivel. Sugestao: escurecer o icone pra algo na faixa de `#148A4E` (mantendo o fundo `#E4F8EE`), o que sobe pra ~4,6:1 e pareia com o vermelho.
- [ ] **Formulario sem nome acessivel** — linha 699, `<form class="form reveal">`. Sugestao: dar `id` ao H2 "Agende a sua demonstracao gratuita" e apontar `aria-labelledby` do form pra ele.
- [ ] **`<mark>` usado so pra cor** — hero H1. `<mark>` tem semantica de "trecho relevante marcado" e alguns leitores de tela anunciam isso; aqui a funcao e apenas pintar "4 horas por dia" de amarelo. Um `<span>` seria mais correto. **Nao alterei de proposito**: a `atendimento-domingo` usa o mesmo padrao, e divergir sozinha aqui quebra a consistencia entre as LPs Cxpress. Se for mudar, muda nas duas.
- [ ] **Esteira de logos sem controle de pausa** — `.clientes__track`. WCAG 2.2.2 pede mecanismo de pausar movimento que dura mais de 5s. Hoje tem pausa no hover e parada total sob `prefers-reduced-motion` (via `*{animation:none!important}`), o que e a mitigacao usada nas outras 10 LPs Cxpress. Botao de pausa explicito seria o unico jeito de cumprir ao pe da letra. Se mudar, e decisao pra todas as LPs, nao so essa.

## Nice-to-haves (2)

Estilistico. Ignorar e aceitavel.

- [ ] `.case__quote` tem `max-width:46ch` com `border-top`, entao o filete de cima para no meio do card. Herdado da `atendimento-domingo`.
- [ ] Na OG image, as duas pilulas decorativas do canto inferior direito (contorno laranja + pilula amarela) se sobrepoem de um jeito meio acidental. Vem da composicao do proprio `og-template.html`.

## Gates que passaram sem achado

| Gate | Resultado |
|---|---|
| `check_gtm_region.py` | `status: ok` — `GTM-T4XDWHL3` bate com regiao `brasil` (detectada por `<html lang='pt-BR'>`). Selo `.tracking.lock` gravado |
| em-dash / `&mdash;` | **0** (tolerancia zero, regras-anti-ia) |
| Fidelidade de copy | Nenhum vazamento. Zero pull-quote inventado, zero kicker novo, zero punchline de marketing. Frase-ancora integral. Sem sinonimo cosmetico. Fora da copy so o que e whitelist declarada (skip-link, nav derivada dos rotulos de secao, labels e opcoes de form, opt-out de compliance) mais a esteira de clientes, documentada como excecao no README |
| Pacote SEO §15 | description 1 · robots 1 · og 10 · twitter 4 · JSON-LD 1 (parseia) · canonical 1 |
| hreflang §16 | LP unica, sem irmas `-es`/`-pt` — omitir hreflang e o correto |
| Logo regional §17 | header e footer apontam pra `https://home.cxpress.io` com `target="_blank" rel="noopener"` e `aria-label` em PT. Zero `href="/"` |
| Logo web-safe §19 | `logo-reversed.svg` tem `<text>` = 0 (vetor outline, nao serifa no browser) |
| OG image §18 | **gerada nesta revisao** — `assets/og-custo-atendimento-manual.png`, 1200×630, 48 KB. Nenhum `og-image.png` orfao |
| Pisos de tipo mobile §20 | `bump_mobile_type --dry-run`: 0 clamps a corrigir |
| Overflow horizontal | nenhum a 375px nem a 1265px (`scrollWidth == clientWidth`) |
| Imagens em grid §14 | `min-height:0` em `.turno__dial`, `.hero__samir`, `.fecho__samir`; `.hero` e `.fecho` com `overflow:hidden` |
| Motion §4 | `.reveal` com fallback `<noscript>` + `prefers-reduced-motion` + `setTimeout(showAll, 2500)` |
| Assets referenciados | 0 quebrados |

## Desvios de guideline assumidos de proposito

- **§3 pede hero de fundo branco/neutral.** Este hero e banda navy. Foi decisao sua na `atendimento-domingo` ("gosto muito do fundo azul") e virou o padrao de identidade das LPs Cxpress novas. Registrado como desvio consciente, nao como achado.
- **§8 diz que fundo escuro aparece uma vez (secao de urgencia).** Aqui tem hero navy, faixa `.total` navy e fecho navy. A `.total` e card de somatoria dentro de uma secao clara, nao secao inteira, e e o ponto de virada da conta. Mantida.

## Proximos passos

1. **Voce aprovar o design** (checkpoint da GUIDELINES §11 — o embed real de formulario so entra depois, senao cada ajuste de layout vira retrabalho com iframe)
2. `/lp-integrar-form cxpress/custo-atendimento-manual "<script type=\"text/javascript\" src=\"https://form.jotform.com/jsform/261045149477663\"></script>"`
3. `/lp-publicar cxpress custo-atendimento-manual content.cxpress.io` — **precisa de worktree a partir de `origin/main`**: o manifest do `content.cxpress.io` tem 69 LPs na main e 66 nesta base local, entao editar o manifest aqui apagaria 3 LPs no ar
