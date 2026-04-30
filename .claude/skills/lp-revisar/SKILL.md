---
name: lp-revisar
description: Auditoria dupla de landing page (frontend-design em review mode + web-design-guidelines). Aplica achados criticos automaticamente, marca melhorias e nice-to-haves como opcionais em REVISAO.md.
argument-hint: "[marca]/[slug] — ex: buzzmonitor/monitoramento-maio"
allowed-tools: Read, Write, Edit, Glob, Grep, Skill, WebFetch
version: 1.4.0
---

# Skill: Revisar Landing Page

Voce audita uma LP em 2 passadas independentes (design + acessibilidade/HTML), aplica **apenas os achados criticos automaticamente**, e deixa tudo acima de critico marcado em `REVISAO.md` para o usuario decidir.

## Passo 0: Parsing e Contexto

Leia, na ordem:

1. `landing-pages/GUIDELINES.md` — regras de design (filtro para os achados de design review).
2. `landing-pages/CONTEXT.md` — runbook operacional. Use principalmente §5 (cascata de regiao — usada no Passo 3.5 GTM) e §6 (troubleshooting — para reconhecer sintomas conhecidos durante a auditoria).
3. `.claude/skills/lp-preparar/CONTEXT.md` — convencoes de marca e formato canonico de `tracking.json`.

Parsing de `$ARGUMENTS`:
- Aceita `{marca}/{slug}` ou `{marca} {slug}` ou path completo `landing-pages/{marca}/{slug}/`.
- Normalize para `landing-pages/{marca}/{slug}/index.html`.

Se arquivo nao existe: PARE e avise.

## Passo 1: Passada 1 — Design Review

> **Nota sobre "review mode":** `frontend-design` e uma skill upstream da Anthropic voltada a GERAR UI. Ela nao tem modo de revisao nativo. O "review mode" aqui e uma **convencao de prompt deste projeto**: a primeira linha do argumento instrui explicitamente "NAO implemente — apenas liste achados", e a skill obedece ao texto do prompt. Se a chamada voltar com HTML gerado em vez de uma lista de achados, o prompt foi mal formatado — refaca com o bloco exato abaixo.

Invoque `frontend-design` com o prompt exato abaixo (primeira linha obrigatoria, nao remover):

```
REVIEW ONLY — NAO implemente nem reescreva codigo. Apenas liste achados em bullets.

Audite a landing page em `landing-pages/{marca}/{slug}/index.html`.

Contexto: LP da marca {marca}, brand em brand/{marca}/, guidelines vivas em landing-pages/GUIDELINES.md (10 secoes).

Reporte em bullets agrupados por severidade:
- CRITICO — quebra visivel, copy invisivel, hierarquia colapsada, contraste < AA, motion sem fallback, secao-tipo errada (ex: problema em grid, beneficios em lista)
- MELHORIA — ajuste que melhora mas nao quebra (espacamento, micro-ajuste tipografico, refinement de cor)
- NICE-TO-HAVE — estilistico, opiniao

Para cada achado: citar linha ou seletor CSS, dizer o que esta errado, sugerir a correcao (texto, nao codigo).
```

Se o output voltar contendo blocos de codigo HTML/CSS novos em vez de lista, descartar e reinvocar reforcando "REVIEW ONLY — apenas texto, zero codigo".

Salve o output inteiro em memoria (nao escrever em disco ainda).

## Passo 2: Passada 2 — Web Interface Guidelines

Invoque `web-design-guidelines`:

```
Audite landing-pages/{marca}/{slug}/index.html contra as Web Interface Guidelines da Vercel Labs.

Foco: acessibilidade, HTML semantico, estrutura, performance basica. Reporte achados em:
- CRITICO — violacoes WCAG AA, labels faltando, alt faltando, tab order quebrado, skip-link ausente, motion sem reduced-motion
- MELHORIA — melhoria de semantica ou a11y nao bloqueante
- NICE-TO-HAVE — polish
```

Salve o output em memoria.

## Passo 3: Consolidar Achados

Unifique as 2 listas. Deduplicate (se os dois auditores pegaram o mesmo problema, contar uma vez). Agrupe final em 3 buckets:

- CRITICOS (apply now)
- MELHORIAS (marcar em REVISAO.md, nao aplicar)
- NICE-TO-HAVES (marcar em REVISAO.md, nao aplicar)

## Passo 3.5: Auditoria de GTM (CRITICO)

### Resolver regiao + GTM esperado

Cascata de deteccao de regiao + resolucao do GTM ID seguem `landing-pages/CONTEXT.md` §5.1 (fonte canonica). lp-revisar usa a cascata completa (3 passos — sufixo do slug → `<html lang>` → fallback `brasil`), porque o HTML ja existe.

### Auditar HTML

Grep em `landing-pages/{marca}/{slug}/index.html` por `GTM-` (script no `<head>` e `<noscript>` apos `<body>`). Comparar com `expected_gtm_id`:

| Estado no HTML | expected_gtm_id | Severidade | Acao |
|---|---|---|---|
| Ausente | != null | CRITICO | Injetar script + noscript com ID correto |
| Presente, ID bate | != null | OK | Nenhuma |
| Presente, ID diferente | != null | CRITICO | Substituir ID nos 2 blocos |
| Presente (qualquer ID) | null | MELHORIA | Anotar em REVISAO.md — `tracking.json` da marca esta null mas LP tem GTM |
| Ausente | null | OK | Nenhuma |

### Snippet canonico para injetar (se ausente)

Snippet em `landing-pages/CONTEXT.md` §5.3 — copiar literal de la, substituindo `{GTM_ID}` pelo valor resolvido (ex: `GTM-NCFT22CW`). Para substituir ID errado em LP que ja tem GTM, usar `Edit` com `replace_all` no ID antigo → novo (pega os 2 blocos numa operacao).

Registrar o achado com os demais criticos para aplicacao no Passo 4. Formato sugerido:

- `GTM ausente para {marca}/{regiao} (esperado {expected_gtm_id}) — injetar script em <head> e noscript apos <body>`
- `GTM com ID errado: encontrado {found_id}, esperado {expected_gtm_id} para {marca}/{regiao}`

## Passo 3.6: Auditoria de Fidelidade da Copy (CRITICO)

Verifica se o HTML respeita literal a copy aprovada em `landing-pages/{marca}/{slug}/copy.txt`. Vazamentos sao tratados com a mesma prioridade do GTM — sao CRITICOS, nao opcionais.

### Por que existir

Durante `lp-gerar`, a `frontend-design` (skill upstream) recebe a copy + a estrutura visual desejada. Em casos com elementos visuais ricos (pull-quotes, kickers, tags rotacionadas, art cards), ela tende a inventar texto novo para preencher esses componentes — porque a propria descricao da estrutura sugere "tem espaco visual aqui". Resultado: pull-quotes inventados, frase-ancora truncada, em-dashes adicionados, sinonimos cosmeticos. Isso vaza tom de IA.

`lp-gerar` v1.5.0+ ja tem guard no Passo 4.2, mas e prudente ter uma segunda verificacao independente em `lp-revisar` (defesa em camadas — o agente que gera nao e o melhor a auditar a si mesmo).

### Procedimento

1. **Carregar `copy.txt`** da pasta da LP. Se nao existir, registrar a auditoria como "skipped (copy-fonte ausente)" e seguir.

2. **Extrair textos visiveis do HTML** (`landing-pages/{marca}/{slug}/index.html`):
   - Conteudo entre tags inline e block: h1/h2/h3/h4/h5/p/li/span/em/strong/button/a/aside/blockquote/figcaption/dt/dd/small.
   - Atributos de `placeholder`, `alt` (so de imagem semantica, nao decorativa), `value` de `<option>`, `aria-label` (so se contem palavra de copy, nao label funcional curto).
   - Excluir: scripts, styles, comentarios HTML, atributos `aria-hidden=true` SVGs decorativos, microformat de SEO (og:, twitter:).

3. **Classificar cada string** em 4 buckets:
   - **(a) Literal da copy.txt** — match exato (apos normalizar aspas curvas e ellipsis para Unicode). OK.
   - **(b) Whitelist** — pertence a uma das categorias permitidas:
     * Nav meta minimal (max 3 palavras, sem repetir info de outra parte do hero)
     * Ticket/badge boilerplate factual (rotulos como "Formato", "Duracao", valores como datas, horarios, "Online", "Gratis")
     * Form labels (campos do `<form>`) e disclaimer compliance generico (consentimento de comunicacao)
     * Footer: copyright, mailto, links institucionais
     * Skip-link, aria-labels funcionais ("Encabezado", "Saltar al contenido")
     * `<title>`, `<meta description>`, `og:*` (textos de SEO derivados, OK se nao introduzem copy nova)
   - **(c) Cosmetico permitido** — copy literal apos substituir `--` por `—`, aspas retas por curvas, `...` por `…`. OK.
   - **(d) VAZAMENTO** — texto visivel que nao bate com nenhum bucket acima. Registrar como CRITICO.

4. **Procurar especificamente os 4 padroes mais comuns:**

   | Padrao | Onde procurar | Como detectar |
   |---|---|---|
   | **Pull-quote inventado** | `<aside>`, `<blockquote>`, `class*="quote"`, `class*="pull"` | Texto multiline em destaque que nao esta em `copy.txt` |
   | **Kicker/tagline em art card** | `class*="kicker"`, `class*="tag"`, `class*="art"` dentro de hero panels | Frase curta decorativa que nao e label da copy |
   | **Tag rotacionada com texto novo** | `transform: rotate` no CSS + texto dentro | Palavra dentro do badge que nao aparece em outro lugar da copy |
   | **Punchline de marketing** | `class*="disclaimer"`, `class*="punch"`, paragrafos curtos perto de CTAs | "sem spam", "sem enrolacao", "100% gratis", "vagas limitadas", "demo" — qualquer slogan punchy nao-literal |

5. **Auditoria especifica de em-dash (regras-anti-ia.md tolerancia zero):**

   ```bash
   # Contar em-dash no HTML (excluindo comentarios CSS e scripts)
   grep -oE "[^&]—|&mdash;" "landing-pages/{marca}/{slug}/index.html" | wc -l
   # Contar em-dash na copy.txt
   grep -oE "—|&mdash;" "landing-pages/{marca}/{slug}/copy.txt" | wc -l
   ```

   Se HTML > copy.txt, o gerador adicionou em-dashes durante a expansao de bullets. CRITICO. Substituir por virgula, ponto ou parenteses conforme regras-anti-ia.md tabela.

6. **Auditoria especifica de frase-ancora:**

   Identificar a ultima H2 antes do CTA final (geralmente seccao "cierre"/"urgencia"). Comparar com a frase H2 marcada como CIERRE/URGENCIA na `copy.txt`. Diferenca em **comprimento de palavras** ou **estrutura semantica** (ex: "no son X, sino Y entendien lo que se dice de ellas" virou "no son X, sino Y escuchan") = CRITICO.

7. **Auditoria de sinonimos cosmeticos:**

   Comparar as primeiras 20 palavras de cada H1/H2/H3/SUB com as linhas correspondentes em `copy.txt`. Trocas de "utilizar"/"usar", virgula+conjuncao por ponto+frase, ou qualquer parafraseamento = CRITICO.

### Severidade e acao

| Achado | Severidade | Acao |
|---|---|---|
| Pull-quote inventado em `<aside>`/`<blockquote>` | CRITICO | Remover o bloco, ou substituir o texto por extracao literal de uma frase da copy (geralmente do CIERRE) |
| Kicker/tagline novo em art card | CRITICO | Remover o texto (deixar so decoracao geometrica) ou repetir literal o H3 da secao adjacente |
| Tag rotacionada com palavra inventada | CRITICO | Trocar por palavra de label da copy (ex: data, horario, "Gratis") ou esvaziar o texto e manter so a forma rotacionada |
| Punchline de marketing nao-literal | CRITICO | Remover. So volta se aparecer literal em copy.txt apos discussao com o autor |
| Frase-ancora truncada | CRITICO | Restaurar literal, mesmo que exija ajuste de tipografia/quebra de linha |
| Sinonimos cosmeticos | CRITICO | Restaurar literal |
| Em-dash adicionado | CRITICO | Substituir por virgula/ponto/parenteses (tabela regras-anti-ia.md) |
| Disclaimer compliance generico | OK (whitelist) | Anotar mas nao alterar — eh boilerplate de form |

Registrar todos os achados de fidelidade junto com os criticos do Passo 3 e GTM (Passo 3.5) para aplicacao no Passo 4.

### Formato sugerido para o registro

```
- COPY-VAZAMENTO: pull-quote inventado em <aside class="for-quote"> linha 1027 — remover bloco; copy.txt nao tem essa frase
- COPY-VAZAMENTO: cierre H2 (linha 1042) truncou frase-ancora — restaurar "...sino las que mejor entienden lo que se dice de ellas"
- COPY-VAZAMENTO: 5 em-dashes adicionados ao body (linhas 858, 876, 902, 929, 1097) — substituir por virgula/ponto
- COPY-COSMETICA: hero h1 (linha 787) "usar" -> restaurar "utilizar" da copy.txt
```

## Passo 4: Aplicar Criticos

Para cada critico, use `Edit` em `landing-pages/{marca}/{slug}/index.html` com a correcao minima possivel. Nao refatorar — so fixar o critico.

Se um critico exige mudanca estrutural grande (ex: re-arquitetar secao-tipo), PARE antes de aplicar e pergunte ao usuario. Nao faca cirurgia grande silenciosamente.

## Passo 5: Gerar REVISAO.md

Caminho: `landing-pages/{marca}/{slug}/REVISAO.md`.

Formato:

```markdown
# Revisao LP — {marca}/{slug}

**Data:** YYYY-MM-DD
**Auditores:** frontend-design (review mode) + web-design-guidelines

## Aplicado automaticamente ({N} criticos)

- [x] {achado 1} — linha {X} — {correcao aplicada}
- [x] {achado 2} — seletor `.xyz` — {correcao}

## Melhorias opcionais ({N})

Para o usuario decidir. Aplicar via Edit manual ou pedir `/lp-revisar` novamente.

- [ ] {achado} — {onde} — {sugestao}

## Nice-to-haves ({N})

Estilistico. Ignorar e aceitavel.

- [ ] {achado}

## Proximos passos

- Design aprovado? -> /lp-integrar-form {marca}/{slug} "{snippet}"
- Rever mais algum critico? -> editar e rodar /lp-revisar novamente
```

## Passo 6: Relatorio Final

```
Revisao concluida — {marca}/{slug}

Criticos aplicados: {N}
Melhorias opcionais: {N} (em REVISAO.md)
Nice-to-haves: {N} (em REVISAO.md)

HTML atualizado: landing-pages/{marca}/{slug}/index.html
Relatorio: landing-pages/{marca}/{slug}/REVISAO.md

Proximo: aprovar design e rodar /lp-integrar-form {marca}/{slug} "snippet"
```
