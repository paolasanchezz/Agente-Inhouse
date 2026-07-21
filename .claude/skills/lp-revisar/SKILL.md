---
name: lp-revisar
description: Auditoria dupla de landing page (frontend-design em review mode + web-design-guidelines). Aplica achados criticos automaticamente, marca melhorias e nice-to-haves como opcionais em REVISAO.md.
argument-hint: "[marca]/[slug] — ex: buzzmonitor/monitoramento-maio"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, WebFetch
version: 1.8.0
---

# Skill: Revisar Landing Page

Voce audita uma LP em 2 passadas independentes (design + acessibilidade/HTML), aplica **apenas os achados criticos automaticamente**, e deixa tudo acima de critico marcado em `REVISAO.md` para o usuario decidir.

## Passo 0.0: Sincronizar o repo (v1.7.0 — migracao CI)

Antes de ler ou editar qualquer arquivo, atualize a working tree — o repo e compartilhado
e, com o deploy via CI (PLANO-MIGRACAO-CI.md), outras pessoas publicam LPs por PR direto
na main. Editar em cima de copia velha gera conflito evitavel no PR.

```bash
git pull --rebase 2>&1 | tail -2 && git branch --show-current
```

Se o rebase conflitar: `git rebase --abort`, avise o usuario e resolva antes de editar.
Nao siga com a skill em working tree desatualizada.

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

A verificacao e **deterministica** — rode o script (mesma logica do gate de CI),
nao audite GTM "no olho". E barato (~zero token) e sem erro humano:

```bash
py landing-pages/build/check_gtm_region.py landing-pages/{marca}/{slug} --json
```

(Use `python3`/`python` se `py` nao existir nesta maquina.) Aja pelo `status`:

| status | Significado | Acao |
|---|---|---|
| `ok` | Container bate com a regiao | Nada. Se `stamp_match=false`, rode com `--write-stamp` pra registrar. |
| `wrong` | Container != regiao (o classico "traduziu e herdou o pixel da origem") | **CRITICO.** `Edit` com `replace_all` do ID errado (`found`) → `expected` (pega head + noscript de uma vez). Re-rodar com `--write-stamp`. |
| `absent` | Regiao tem GTM esperado mas a LP nao tem | **CRITICO.** Injetar o snippet CONTEXT §5.3 com o ID `expected`. Re-rodar com `--write-stamp`. |
| `no_expected` | LP tem GTM mas `tracking.json` da marca esta null pra regiao | MELHORIA — anotar em REVISAO.md. |
| `no_tracking` | Marca sem `tracking.json` | Nada a checar. |

**Skip (economia real):** se `stamp_match=true` e `status=ok`, o tracking nao mudou
desde a ultima verificacao — nao re-audite, siga. Trocar so titulo/corpo **nao** muda
o fingerprint (regiao + GTM esperado + GTM encontrado), entao nao re-dispara.

Cascata de regiao + resolucao do ID: CONTEXT §5.1 (o script ja implementa). O selo
`.tracking.lock` gravado por `--write-stamp` vai junto no commit e alimenta o
grandfathering do gate de CI (CONTEXT §5.4). Registrar achados de GTM com os demais
criticos para aplicacao no Passo 4.

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
   - **(c) Cosmetico permitido** — copy literal apos substituir aspas retas por curvas e `...` por `…`. OK. **`--` (hifen duplo) NUNCA vira `—` (em-dash) — isso e VAZAMENTO, nao cosmetica.** Em-dash tem tolerancia zero por `regras-anti-ia.md` e GUIDELINES §5; substituir `--` por virgula/ponto/parenteses conforme contexto.
   - **(d) VAZAMENTO** — texto visivel que nao bate com nenhum bucket acima. Registrar como CRITICO.

4. **Procurar especificamente os 4 padroes mais comuns:**

   | Padrao | Onde procurar | Como detectar |
   |---|---|---|
   | **Pull-quote inventado** | `<aside>`, `<blockquote>`, `class*="quote"`, `class*="pull"` | Texto multiline em destaque que nao esta em `copy.txt` |
   | **Kicker/tagline em art card** | `class*="kicker"`, `class*="tag"`, `class*="art"` dentro de hero panels | Frase curta decorativa que nao e label da copy |
   | **Tag rotacionada com texto novo** | `transform: rotate` no CSS + texto dentro | Palavra dentro do badge que nao aparece em outro lugar da copy |
   | **Punchline de marketing** | `class*="disclaimer"`, `class*="punch"`, paragrafos curtos perto de CTAs | "sem spam", "sem enrolacao", "100% gratis", "vagas limitadas", "demo" — qualquer slogan punchy nao-literal |

5. **Auditoria especifica de em-dash (regras-anti-ia.md + GUIDELINES §5 tolerancia zero):**

   ```bash
   # Contagem absoluta no HTML — qualquer ocorrencia e CRITICO (tolerancia zero)
   grep -oE "—|&mdash;" "landing-pages/{marca}/{slug}/index.html" | wc -l
   ```

   **Esperado: 0.** Se > 0, CRITICO **sempre** — independe do que tem em `copy.txt`. A regra anti-IA proibe em-dash em **todo conteudo renderizado**, nao so o "adicionado pelo gerador". Se a copy.txt tambem tem em-dash, o gap esta upstream (lp-preparar Passo 4.1 falhou) — registrar tambem para corrigir copy.txt no Passo 4 deste revisor.

   Para cada ocorrencia, identificar o substituto conforme contexto (tabela em regras-anti-ia.md):

   | Funcao do em-dash | Substituto |
   |---|---|
   | Pausa curta dentro da frase | virgula |
   | Pausa forte / quebra de pensamento | ponto (duas frases) |
   | Aparte / informacao adicional | parenteses |
   | Atribuicao de citacao (`— Autor`) | virgula ou nova linha |

   Fix aplicado no Passo 4 (criticos), com `Edit` ocorrencia por ocorrencia.

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
| Em-dash (`—` ou `&mdash;`) presente no HTML | CRITICO (tolerancia zero) | Substituir cada ocorrencia por virgula/ponto/parenteses (tabela regras-anti-ia.md). Se copy.txt tambem tem em-dash, corrigir copy.txt no mesmo passo |
| Disclaimer compliance generico | OK (whitelist) | Anotar mas nao alterar — eh boilerplate de form |

Registrar todos os achados de fidelidade junto com os criticos do Passo 3 e GTM (Passo 3.5) para aplicacao no Passo 4.

### Formato sugerido para o registro

```
- COPY-VAZAMENTO: pull-quote inventado em <aside class="for-quote"> linha 1027 — remover bloco; copy.txt nao tem essa frase
- COPY-VAZAMENTO: cierre H2 (linha 1042) truncou frase-ancora — restaurar "...sino las que mejor entienden lo que se dice de ellas"
- COPY-VAZAMENTO: 5 em-dashes adicionados ao body (linhas 858, 876, 902, 929, 1097) — substituir por virgula/ponto
- COPY-COSMETICA: hero h1 (linha 787) "usar" -> restaurar "utilizar" da copy.txt
```

## Passo 3.7: Auditoria SEO + multi-idioma + logo regional (v1.5.0, CRITICO)

Audita o pacote SEO obrigatorio (GUIDELINES §15), hreflang (§16), logo regional (§17) e OG image (§18). Vazamentos sao CRITICOS — afetam ranking, social previews e clickthrough.

### 3.7.a Pacote SEO obrigatorio (GUIDELINES §15)

```bash
HTML="landing-pages/{marca}/{slug}/index.html"
DESC=$(grep -c '<meta name="description"' "$HTML")          # esperado: 1
ROBOTS=$(grep -c '<meta name="robots"' "$HTML")             # esperado: 1
OG=$(grep -c '<meta property="og:' "$HTML")                 # esperado: >= 8
TW=$(grep -c '<meta name="twitter:' "$HTML")                # esperado: >= 4
JSONLD=$(grep -c 'application/ld+json' "$HTML")             # esperado: 1
CANONICAL=$(grep -c '<link rel="canonical"' "$HTML")        # esperado: 1
```

| Check | Threshold | Severidade se falha |
|---|---|---|
| `meta description` | == 1 | CRITICO (sem description, Google usa snippet aleatorio) |
| `meta robots` | == 1 | MELHORIA (default index,follow funciona, mas explicito e melhor) |
| `og:` count | >= 8 | CRITICO (preview social quebrado) |
| `twitter:` count | >= 4 | MELHORIA (X aceita fallback de og:) |
| JSON-LD | == 1 | CRITICO (sem rich results no Google) |
| canonical | == 1 | CRITICO (Google pode tratar como duplicado) |

### 3.7.b JSON-LD parseia + referencia regions corretas

```bash
# Python resiliente ao shim da Store no Windows (testa execucao; macOS/Linux -> python3). Single-token.
PYBIN=""; for _c in py python3 python; do command -v "$_c" >/dev/null 2>&1 && "$_c" -c '' >/dev/null 2>&1 && { PYBIN="$_c"; break; }; done; PYBIN="${PYBIN:-python}"
"$PYBIN" -c "
import re, json, sys
html = open('$HTML', encoding='utf-8').read()
m = re.search(r'<script type=\"application/ld\+json\">(.*?)</script>', html, re.S)
if not m:
    print('FAIL: JSON-LD ausente')
    sys.exit(1)
try:
    obj = json.loads(m.group(1))
except Exception as e:
    print(f'FAIL: JSON-LD nao parseia: {e}')
    sys.exit(1)
graph = obj.get('@graph', [obj])
types = [item.get('@type') for item in graph]
print('OK', types)
"
```

Validar tambem que `Organization.url` bate com `brand/{marca}/brand-manifest.json#regions.{regiao}.home` e que `Organization.sameAs[]` inclui o Instagram regional + LinkedIn da marca. Se nao bate, CRITICO — alguem hardcodou URL no HTML em vez de ler do manifest.

### 3.7.c Multi-idioma (GUIDELINES §16)

Detectar LPs irmas (mesma marca, slug-base + sufixo `-es`/`-pt`):

```bash
SLUG_BASE=$(echo "{slug}" | sed -E 's/-(es|pt)$//')
SIBLINGS=$(ls landing-pages/{marca}/ | grep -E "^${SLUG_BASE}(-es|-pt)?$")
SIBLING_COUNT=$(echo "$SIBLINGS" | wc -l)
```

| Cenario | hreflang esperado | Severidade se falta |
|---|---|---|
| LP unica (sem irmas) | apenas `canonical` proprio, sem hreflang | OK omitir hreflang |
| LP com 1+ irmas | `<link rel="alternate" hreflang>` para cada irma + `x-default` | CRITICO se ausente |

Validar:

```bash
HREFLANG_COUNT=$(grep -c '<link rel="alternate" hreflang=' "$HTML")
# Esperado: == SIBLING_COUNT + 1 (x-default)
```

Codigo de hreflang da LP atual deve bater com `regions.{regiao}.hreflang` do manifest (`pt-BR`, `es-419`, `pt-PT`). `es-LA` ou `es-LATAM` sao INVALIDOS — abortar com critico "codigo hreflang nao reconhecido pelo Google".

### 3.7.d Logo regional (GUIDELINES §17)

```bash
# Logo navbar+footer NAO pode ter href="/" — precisa apontar pra home regional
BAD_LOGO=$(grep -E 'class="(navbar|footer)__logo"[^>]*href="/"' "$HTML" | wc -l)
# Esperado: 0
```

Se BAD_LOGO > 0, CRITICO. Fix: substituir `href="/"` por `href="{regions.{regiao}.home}"` + adicionar `target="_blank" rel="noopener"`.

Validar tambem que a URL no href bate com o manifest (defesa contra hardcode):

```bash
grep -oE 'class="navbar__logo"[^>]*href="[^"]*"' "$HTML"
# A URL deve == manifest.regions.{regiao}.home
```

**Logo web-safe (GUIDELINES §19) — CRITICO:** o SVG de logo referenciado no header/footer NAO pode ter `<text>` vivo — sem a fonte embarcada, o browser troca por serifada e a logo sai errada (ex.: "BUZZ" sans + "CREATORS" serifada). Identificar os SVG de logo referenciados e checar:

```bash
# Listar os logos .svg referenciados
grep -oE 'src="[^"]*logo[^"]*\.svg"' "$HTML" | sed 's/.*src="\([^"]*\)".*/\1/' | sort -u
# Para cada um, resolver no source (../../brand/{marca}/assets/logos/ ou ./assets/) e checar:
#   grep -c '<text' {arquivo}.svg   → TEM que ser 0 (se > 0, serifa no browser)
#   grep -c base64 {arquivo}.svg    → raster (renderiza certo) e aceitavel
```

Qualquer logo SVG com `<text>` > 0 = CRITICO. Fix: trocar a referencia pelo raster (base64), PNG, ou SVG outline (§19). Buzzcreators: `logo-color.png` (sem tagline) ou o raster `logo-full-color.svg` do deploy.

### 3.7.e OG image (GUIDELINES §18)

```bash
OG_IMAGE_URL=$(grep -oE '<meta property="og:image" content="[^"]*"' "$HTML" | head -1 | sed 's/.*content="\([^"]*\)".*/\1/')
OG_IMAGE_FILE_SOURCE="landing-pages/{marca}/{slug}/assets/og-image.png"

# Check 1: og:image e URL absoluta com https://
echo "$OG_IMAGE_URL" | grep -qE '^https://' || echo "CRITICO: og:image nao e URL absoluta"

# Check 2: arquivo existe no source
test -f "$OG_IMAGE_FILE_SOURCE" || echo "CRITICO: og-image.png ausente em $OG_IMAGE_FILE_SOURCE"

# Check 3: dimensoes 1200x630 (Pillow ja vem no py 3.14 desta maquina)
# Python resiliente ao shim da Store no Windows (testa execucao; macOS/Linux -> python3). Single-token.
PYBIN=""; for _c in py python3 python; do command -v "$_c" >/dev/null 2>&1 && "$_c" -c '' >/dev/null 2>&1 && { PYBIN="$_c"; break; }; done; PYBIN="${PYBIN:-python}"
"$PYBIN" -c "
from PIL import Image
im = Image.open('$OG_IMAGE_FILE_SOURCE')
if im.size != (1200, 630):
    print(f'CRITICO: og-image.png tem {im.size}, esperado (1200, 630)')
"
```

### Registrar achados

Adicionar todos os criticos de SEO/hreflang/logo/OG no bucket principal de criticos para aplicacao no Passo 4. Formato sugerido:

```
- SEO-MISSING: meta description ausente — adicionar derivando da copy (~155 chars, localizada para {regiao})
- SEO-JSONLD-BROKEN: JSON-LD nao parseia — erro em linha N
- SEO-ORG-URL-MISMATCH: Organization.url hardcoded ({url-encontrada}), deveria ser {manifest.regions.{regiao}.home}
- I18N-HREFLANG-MISSING: 3 LPs irmas detectadas (mcp, mcp-es, mcp-pt) mas 0 hreflang no HTML — adicionar bloco
- I18N-HREFLANG-INVALID: hreflang="es-LA" nao e codigo valido — usar "es-419"
- LOGO-BAD-HREF: navbar logo aponta para "/" (linha 977) — trocar para "{manifest.regions.{regiao}.home}" + target=_blank
- OG-IMAGE-MISSING: og:image referenciado mas arquivo nao existe em landing-pages/{marca}/{slug}/assets/og-image.png
- OG-IMAGE-DIMENSIONS: og-image.png tem (1024, 512), esperado (1200, 630)
- LOGO-SERIF: logo-color.svg (header, linha N) tem <text> vivo — serifa no browser; trocar por logo-color.png ou raster (§19)
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
