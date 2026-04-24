---
name: lp-gerar
description: Gera HTML estatico completo de landing page a partir de copy estruturada (output do lp-preparar), aplicando brand tokens da marca e as GUIDELINES universais. Orquestra a skill frontend-design.
argument-hint: "[marca] [slug] — ex: buzzmonitor monitoramento-maio (le copy.txt da pasta landing-pages/{marca}/{slug}/)"
allowed-tools: Read, Write, Glob, Grep, Skill
version: 1.2.0
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
2. `landing-pages/GUIDELINES.md` — todas as 10 secoes.
3. `brand/{marca}/tokens.json` — cores, tipografia, espacamento.
4. `brand/{marca}/generation-rules.json` — regras de composicao.
5. `brand/{marca}/brand-manifest.json` — tom.
6. `brand/{marca}/tracking.json` — GTM container id por regiao. Se o arquivo nao existir ou o id for `null`, pular injecao de GTM.
7. `ls brand/{marca}/assets/logos/` via Glob — inventariar logos disponiveis (primary, reversed, mark-only).

### Resolver regiao e GTM ID

Detectar regiao pela cascata (ver CONTEXT.md "Deteccao de regiao"):

1. Sufixo do `{slug}`: `-pt` → portugal, `-latam`/`-es` → latam, `-br` → brasil.
2. Se ainda nao resolvido, `lp-gerar` esta criando a LP do zero (sem HTML ainda) — usar default `brasil`.

Com a regiao em maos, resolver GTM ID em `tracking.json`:

1. `regions[{regiao}]` != null → usar.
2. Senao, `gtm.default`.
3. Ambos null → omitir (anotar em README que GTM nao foi injetado).

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

Copy estruturada (fonte-verdade, nao reescrever):
{cole o conteudo integral de copy.txt}

Paths de asset: usar "../../brand/{marca}/assets/logos/{filename}" nos <img src>. Atributo alt sempre presente. Logo em hero pode ser grande se for transparente.

Google Tag Manager ({GTM_ID}): injetar OBRIGATORIAMENTE se {GTM_ID} != null.
- No <head>, logo APOS o <meta name="viewport"> e ANTES do <title>:

  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','{GTM_ID}');</script>
  <!-- End Google Tag Manager -->

- Imediatamente APOS a <body>:

  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->

Substituir {GTM_ID} pelo valor resolvido (ex: GTM-WFJVK858). Se null, omitir ambos os blocos.

Output: HTML completo, pronto para servir. CSS inline. Zero dependencia externa alem de Google Fonts + GTM se preciso.
```

Invocar: `Invoke Skill(frontend-design, args: "{briefing_acima}")` — montar o briefing como string unica, escapando aspas internas se necessario.

## Passo 4: Validar Output da frontend-design

Antes de escrever o arquivo, verifique o HTML retornado:

- [ ] `<!doctype html>` + `<html lang="{idioma-marca}">`
- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1">`
- [ ] `<title>` preenchido (nao contem `[REVISADO]`, `[TESTE]`, nem placeholders)
- [ ] GTM injetado (se `{GTM_ID}` != null): `<script>` no `<head>` apos viewport **e** `<noscript>` apos `<body>`. ID correto em ambos os blocos.
- [ ] Todas as imagens tem `alt` ou `aria-hidden="true"`
- [ ] Form esta em mock (`action="#"`)
- [ ] Numero de itens em cada secao bate com a copy (GUIDELINES §9)
- [ ] Nenhum emoji decorativo injetado que nao estava na copy

Se algum item falhar, re-invocar `frontend-design` com a correcao especifica, nao editar a mao.

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
