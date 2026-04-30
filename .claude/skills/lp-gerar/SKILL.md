---
name: lp-gerar
description: Gera HTML estatico completo de landing page a partir de copy estruturada (output do lp-preparar), aplicando brand tokens da marca e as GUIDELINES universais. Orquestra a skill frontend-design.
argument-hint: "[marca] [slug] — ex: buzzmonitor monitoramento-maio (le copy.txt da pasta landing-pages/{marca}/{slug}/)"
allowed-tools: Read, Write, Glob, Grep, Skill
version: 1.5.0
---

# Skill: Gerar HTML de Landing Page

Voce transforma copy estruturada em HTML estatico completo, production-grade, usando brand tokens da marca e as guidelines universais de LP. **Nao inventa copy. Nao reordena blocos. Nao adiciona secoes que a copy nao pediu** (GUIDELINES §9).

## Passo 0: Parsing e Contexto

Leia `.claude/skills/lp-preparar/CONTEXT.md` (compartilhado pela familia lp-*).

Parsing de `$ARGUMENTS`:

| Argumento | Valores | Obrigatorio |
|---|---|---|
| `marca` | `buzzmonitor` \| `buzzcreators` \| `cxpress` \| `elife` | Sim |
| `slug` | kebab-case (deve existir `landing-pages/{marca}/{slug}/copy.txt`) | Sim |

Se copy.txt nao existe: PARE. Mostre:
```
Copy estruturada nao encontrada em landing-pages/{marca}/{slug}/copy.txt
Rode /lp-preparar {marca} {slug} [fonte] primeiro.
```

## Passo 1: Carregar Insumos

Leia, na ordem:

1. `landing-pages/{marca}/{slug}/copy.txt` — copy estruturada (fonte-verdade de conteudo e ordem).
2. `landing-pages/GUIDELINES.md` — todas as 10 secoes (regras de design).
3. `landing-pages/CONTEXT.md` — runbook operacional. Use principalmente §3 (convencao de assets — paths source vs deploy) e §5 (cascata de deteccao de regiao).
4. `brand/{marca}/tokens.json` — cores, tipografia, espacamento.
5. `brand/{marca}/generation-rules.json` — regras de composicao.
6. `brand/{marca}/brand-manifest.json` — tom.
7. `brand/{marca}/tracking.json` — GTM container id por regiao. Se o arquivo nao existir ou o id for `null`, pular injecao de GTM.
8. `ls brand/{marca}/assets/logos/` via Glob — inventariar logos disponiveis (primary, reversed, mark-only).

### Resolver regiao e GTM ID

Cascata de regiao + resolucao do GTM ID seguem `landing-pages/CONTEXT.md` §5.1 (fonte canonica). lp-gerar pula o passo 2 da cascata (HTML ainda nao existe — sem `<html lang>` para ler) e cai direto pro fallback `brasil` se o slug nao tiver sufixo.

Se `expected_gtm_id == null` apos cascata, omitir GTM (anotar em README que GTM nao foi injetado).

## Passo 2: Mapear Copy para Estrutura Visual

Antes de gerar HTML, faca uma **planta baixa** por secao:

```
HERO (eyebrow + h1 + sub + CTA primario)        → fundo branco, texto esq, elemento visual dir
PROBLEMA (lista vertical de dores)              → §8 — X vermelhos em lista vertical
BENEFICIOS (grid de beneficios)                 → §8 — ✓ verdes em grid (N colunas = N da copy)
URGENCIA (label + h2 + CTA)                     → §8 — fundo dark + tag rotacionada
PROVA (speakers/cases) [se houver na copy]
CTA FINAL (form mock)                           → §10 — form action="#", sem embed real
FOOTER
```

**Regra de ouro (GUIDELINES §9):** a contagem e ordem de blocos vem da copy. Nao "equilibrar" — se a copy tem 5 dores, problema tem 5 itens. Se nao tem secao de diferencial, LP nao tem.

## Passo 3: Invocar `frontend-design`

Use o Skill tool para invocar `frontend-design` com um briefing detalhado. **Nao reimplementar design — orquestrar a skill existente.**

Briefing a passar:

```
Gere HTML estatico completo (single-file, CSS inline em <style>) para landing page da marca {marca}.

Contexto de marca:
- Tokens: {cole resumo dos tokens — cores primarias, display font, body font, espacamento}
- Tom: {resumo do brand-manifest}
- Logos disponiveis: {lista dos logos encontrados}

Guidelines universais (obrigatorias — landing-pages/GUIDELINES.md):
- §1 Paleta 2-3 cores, 1 gradiente maximo
- §2 Respiro generoso (160px/100px secoes premium, 120px/80px padrao)
- §3 Hero: fundo branco/neutral, texto esq, elemento visual dir (1 elemento so)
- §4 Animacao: reveals com opacity + fallback prefers-reduced-motion
- §5 Copy: aspas curvas, em-dash, numeros em algarismos
- §7 Acessibilidade: skip-link, focus-visible, labels, alt/aria-hidden, prefers-reduced-motion
- §8 Secoes-tipo:
    * Problema = lista vertical com X vermelhos (nao grid)
    * Beneficios = grid com ✓ verdes (N colunas = N da copy)
    * Urgencia = fundo dark + tag cor quente rotacionada
- §9 Copy dita estrutura — ordem e contagem dos blocos NAO podem mudar
- §10 Form = mock <form action="#" onsubmit="event.preventDefault()"> (integracao real vira depois)

REGRA DE FIDELIDADE DA COPY (CRITICA — vale mais que qualquer escolha estetica):

TODO texto visivel ao usuario no HTML deve vir LITERAL da copy estruturada abaixo. Aplica a:
- titulos (h1/h2/h3), subtitulos, paragrafos, list items, eyebrows, CTAs, frase de fechamento;
- texto dentro de cards visuais, pull-quotes, kickers, taglines decorativas, captions;
- texto em tags rotacionadas, badges, banners, ticker/marquee, frases de suporte.

NAO inventar:
- pull-quotes, frases de impacto, slogans decorativos que "soam bem";
- kickers ou subtitulos novos para preencher art cards/hero panels;
- frases na tag de urgencia ou em ticker que nao venham da copy;
- disclaimers de marketing/UX punchy (ex: "sem spam", "sem enrolacao") — apenas boilerplate compliance estritamente necessario para form (ver whitelist);
- frases derivadas/parafraseadas — se a copy diz "X, sino Y", o HTML escreve "X, sino Y" (literal), nao um sinonimo.

NAO truncar nem encurtar:
- frases-ancora (ex: a frase de fechamento da LP) ficam na integra;
- se a copy tem 25 palavras e o layout pede 10, reduz tipografia ou quebra em multiplas linhas — nunca corta semantica.

NAO reescrever cosmeticamente:
- "utilizar" -> "usar", virgula+conjuncao -> ponto+frase, sinonimos por preferencia de ritmo NAO sao cosmeticos. Sao reescrita. Manter literal.
- ajustes permitidos: aspas curvas (`&ldquo; &rdquo;`), ellipsis (`&hellip;`), substituir `--` por `&mdash;` (nunca o inverso — em-dash so se ja estava no source).

Whitelist de TEXTOS PERMITIDOS fora da copy.txt (estritamente):
1. Nav meta minimal (ex: "Webinar gratuito", "En vivo") — texto curto, max 3 palavras, sem repetir info da copy.
2. Ticket card boilerplate factual: rotulos como "Formato", "Duracao", "Inversion" + valores do briefing (data, hora, "Online · En vivo", "Gratis", "60 min").
3. Form labels e disclaimer compliance generico (ex: "Email", "Empresa", "Al registrarte aceptas recibir comunicaciones de {marca}..."). Boilerplate punchy ("sem spam") NAO entra.
4. Footer: copyright, mailto contato, links institucionais.
5. Skip link e aria-labels (a11y) — texto funcional.

Tudo fora da whitelist: vem do copy.txt ou nao existe no HTML.

Pull-quote, kicker, tag rotacionada e ticker — se o briefing pede o componente visual mas a copy nao tem texto pra ele, faca o componente sem texto (apenas decoracao geometrica) OU repita literal a frase mais relevante da copy. Nunca inventar.

Copy estruturada (fonte-verdade, nao reescrever):
{cole o conteudo integral de copy.txt}

Paths de asset: usar "../../brand/{marca}/assets/logos/{filename}" nos <img src>. Atributo alt sempre presente. Logo em hero pode ser grande se for transparente.

Google Tag Manager: injetar OBRIGATORIAMENTE o snippet canonico de `landing-pages/CONTEXT.md` §5.3 (script no <head> apos viewport e antes de title; noscript imediatamente apos <body>) com {GTM_ID} substituido pelo valor resolvido (ex: GTM-WFJVK858). Se {GTM_ID} == null, omitir ambos os blocos. Nao parafrasear o snippet — copiar literal de §5.3.

Output: HTML completo, pronto para servir. CSS inline. Zero dependencia externa alem de Google Fonts + GTM se preciso.
```

Invocar: `Invoke Skill(frontend-design, args: "{briefing_acima}")` — montar o briefing como string unica, escapando aspas internas se necessario.

## Passo 4: Validar Output da frontend-design

Antes de escrever o arquivo, verifique o HTML retornado.

### 4.1 Checklist tecnico

- [ ] `<!doctype html>` + `<html lang="{idioma-marca}">`
- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1">`
- [ ] `<title>` preenchido (nao contem `[REVISADO]`, `[TESTE]`, nem placeholders)
- [ ] GTM injetado (se `{GTM_ID}` != null): `<script>` no `<head>` apos viewport **e** `<noscript>` apos `<body>`. ID correto em ambos os blocos.
- [ ] Todas as imagens tem `alt` ou `aria-hidden="true"`
- [ ] Form esta em mock (`action="#"`)
- [ ] Numero de itens em cada secao bate com a copy (GUIDELINES §9)
- [ ] Nenhum emoji decorativo injetado que nao estava na copy
- [ ] **Reveal-on-scroll com fallback robusto se JS quebrar.** Se houver classe `.reveal` com `opacity:0`, deve haver `<noscript><style>.reveal{opacity:1!important;transform:none!important}</style></noscript>` no `<head>` (ou esquema equivalente: `.no-js` + remocao via JS). So o `@media (prefers-reduced-motion: reduce)` nao basta — protege apenas usuarios com reduced motion, nao o caso geral de JS bloqueado/falhado.

### 4.2 Auditoria de fidelidade da copy (CRITICO)

Antes de aceitar o output, faca **diff textual** entre `copy.txt` e os textos visiveis do HTML.

Procedimento (manual — nao automatizar prematuramente):

1. **Extraia** os textos visiveis do HTML retornado pela `frontend-design`. Foco: conteudo entre tags (h1/h2/h3/p/li/span/em/strong/button/a/aside/blockquote), placeholders de input, valores de `<option>`, alt de imagem semantica.
2. **Compare** linha-por-linha com `copy.txt`. Para cada string do HTML, classifique:
   - **(a) Match literal com copy.txt** — OK.
   - **(b) Match apos normalizacao cosmetica** (aspas curvas, ellipsis, espacos) — OK.
   - **(c) Whitelist** (nav meta minimal, ticket boilerplate factual, form labels/disclaimer, footer, skip-link, aria-labels) — OK, anotar.
   - **(d) Texto novo nao-whitelist** — VIOLACAO. Reescreva, ou remova.
3. **Procure especificamente** os 4 padroes de vazamento mais comuns:
   - **Pull-quote inventado** (em `<aside>`, `<blockquote>`, ou cards "decorativos") com texto que nao esta na copy. Buscar `<aside`, `<blockquote`, `class*="quote"` no HTML e verificar match.
   - **Kicker/tagline** dentro de art cards/hero panels (ex: `.kicker`, `.hero-panel-tag`) com texto novo.
   - **Tag rotacionada** (ex: `transform: rotate`) com palavra ou frase fora da copy. A tag pode usar literal de label da copy ou ficar sem texto (so cor + decoracao geometrica).
   - **Disclaimer/punchline de marketing** em CTA final ou form (ex: "sem spam", "sem enrolacao", "100% gratis", "vagas limitadas") — so entra se for palavra-por-palavra do copy.txt.

4. **Procure especificamente reescrita cosmetica nao autorizada:**
   - **Frase-ancora truncada/encurtada.** Identifique a frase de fechamento da LP (geralmente ultima H2 antes do CTA final) e confirme que esta literal. AI tende a encurtar "no son las que mais X, sino las que melhor Y" para "no son X, sino Y" — isso vaza tom.
   - **Sinonimos.** Se copy diz "utilizar", HTML deve dizer "utilizar" (nao "usar"). Se copy tem "pero", HTML tem "pero" (nao ponto + frase nova). Se copy tem em-dash, HTML tem em-dash; se copy NAO tem em-dash, HTML NAO tem.
   - **Em-dash adicionado.** Contar em-dash (`—` ou `&mdash;`) no HTML e comparar com a contagem na copy.txt. Se HTML > copy = vazamento (regras-anti-ia.md tolerancia zero). Substituir por virgula/ponto/parenteses.

5. **Se encontrar qualquer item (d) ou padrao de vazamento:**
   - Re-invocar `frontend-design` com instrucao especifica `"REMOVER os seguintes textos inventados: [lista]. RESTAURAR a copy literal de copy.txt nestes pontos: [lista de seletores e valores corretos]"`.
   - Alternativa: aplicar fixes cirurgicos via `Edit` apos salvar (Passo 5). Documentar todos os fixes no `REVISAO.md` para o usuario validar.

Se algum item do 4.1 falhar, re-invocar `frontend-design` com a correcao especifica, nao editar a mao.
Se algum item do 4.2 falhar, decidir entre re-invocar ou aplicar fix cirurgico — documentar a escolha no `REVISAO.md`.

## Passo 5: Salvar Arquivos

```
landing-pages/{marca}/{slug}/
├── index.html                 (HTML completo)
├── copy.txt                   (ja existe)
└── README.md                  (novo/atualizado)
```

`README.md` deve conter:

```markdown
# LP {Marca} — {Slug}

**Gerado em:** YYYY-MM-DD
**Copy-fonte:** `copy.txt` (output de /lp-preparar)

## Estrutura

{Lista de secoes identificadas, uma por linha}

## Estado

- [x] HTML gerado
- [ ] Revisao (frontend-design review + web-design-guidelines) — rodar `/lp-revisar {marca}/{slug}`
- [ ] Formulario integrado — rodar `/lp-integrar-form {marca}/{slug} [snippet]`
- [ ] Publicado — rodar `/lp-publicar {marca} {slug} [dominio]`

## Assets referenciados

{Lista dos paths de ../../brand/{marca}/assets/... efetivamente usados no HTML}
```

## Passo 6: Relatorio Final

```
HTML gerado — {marca}/{slug}

Arquivo: landing-pages/{marca}/{slug}/index.html ({N} linhas, {M} KB)

Secoes: {lista}
Paleta usada: {cores citadas no CSS}
Assets referenciados: {lista}

Proximos passos:
- Revisar: /lp-revisar {marca}/{slug}
- Quando design aprovado, integrar form: /lp-integrar-form {marca}/{slug} "snippet"
```
