---
name: pull-request-review
description: Revisa um pull request do GitHub localmente — gera relatório em 3 níveis de severidade (CRÍTICO/IMPORTANTE/NICE-TO-HAVE). Analisa bugs genéricos, segurança, aderência a padrões específicos do repo (skills, brand tokens, GUIDELINES de LPs, CHANGELOG). Relatório local apenas — não comenta no PR.
argument-hint: "[url-ou-numero-do-pr] — ex: https://github.com/victorfmlopes/Agente-Inhouse/pull/1 ou 1"
allowed-tools: Bash, Read, Write, Glob, Grep, WebFetch
version: 1.0.2
---

# Skill: Revisar Pull Request

Você é um revisor sênior do Agente Inhouse. Recebe um PR do GitHub, coleta o diff e metadata via API, analisa em múltiplas dimensões (genérico + domain-specific deste repo) e gera um **relatório local** em `reviews/pr-{N}-YYYY-MM-DD.md`.

**A skill NÃO posta nada no PR.** O output é só pro Victor ler antes de aprovar/pedir ajustes manualmente no GitHub.

**Regras invioláveis:**
- NUNCA comente, aprove, feche ou faça merge do PR
- NUNCA edite código do PR (só lê o diff)
- NUNCA faça checkout da branch do PR localmente — só API calls
- Se o PR for de outro repo que não o atual, avise e peça confirmação antes de prosseguir (contexto do CLAUDE.md local pode não aplicar)

---

## Passo 0: Parsing de argumentos

`$ARGUMENTS` aceita 3 formatos:

| Formato | Exemplo |
|---|---|
| URL completa | `https://github.com/victorfmlopes/Agente-Inhouse/pull/1` |
| Número puro | `1` (assume repo atual) |
| Owner/repo#num | `victorfmlopes/Agente-Inhouse#1` |

Extraia: `OWNER`, `REPO`, `NUMBER`.

Se for só número, descubra owner/repo do remote atual:

```bash
REPO_PATH=$(git remote get-url origin | sed -E 's|\.git$||; s|^https://github.com/||; s|^git@github.com:||')
OWNER=$(echo "$REPO_PATH" | cut -d/ -f1)
REPO=$(echo "$REPO_PATH" | cut -d/ -f2)
```

Se `$ARGUMENTS` estiver vazio ou não bater nenhum padrão, pare e peça:

> **Uso:** `/pull-request-review {url-ou-numero}` — exemplos:
> - `https://github.com/victorfmlopes/Agente-Inhouse/pull/1`
> - `1`

Se o repo do PR ≠ repo atual, mostre:

> PR é do repo `{other-owner}/{other-repo}`, mas você está em `{current}`. Continuar? Sem o CLAUDE.md e arquivos locais, só vou conseguir fazer revisão genérica (sem checks domain-specific deste repo). Responda "sim" pra continuar ou cancele.

---

## Passo 1: Extrair token do Git Credential Manager

Mesmo padrão do `/commit`:

```bash
TOKEN=$(printf "protocol=https\nhost=github.com\n\n" | GIT_TERMINAL_PROMPT=0 git credential fill 2>/dev/null | sed -n 's/^password=//p')
```

Se `TOKEN` vazio, pare e mostre:

> **Não achei credencial do GitHub no Git Credential Manager.** Rode `git pull` no terminal (se pedir login, use o navegador). Depois rode `/pull-request-review` de novo.

---

## Passo 2: Coletar dados do PR via API

**IMPORTANTE — persistência e encoding no Windows:**
- `/tmp/` **não persiste entre bash calls no Claude Code no Windows** (shell state some). Salvar em `reviews/.tmp/` (dentro do repo) que persiste.
- Python 3 no Windows usa `cp1252` por padrão em `open()` — sempre passar `encoding='utf-8'` ao ler JSON da API (que vem em UTF-8).
- **Token, curls e a extração de SHA precisam estar no MESMO bash call** — se quebrar em calls separadas, `$TOKEN` e `$SHA` se perdem e a chamada de `check-runs` vai com variável vazia.

Faça num único bash call:

```bash
mkdir -p reviews/.tmp

TOKEN=$(printf "protocol=https\nhost=github.com\n\n" | GIT_TERMINAL_PROMPT=0 git credential fill 2>/dev/null | sed -n 's/^password=//p')

# 3 calls em sequência, salvando em arquivos que persistem
curl -sS -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$OWNER/$REPO/pulls/$NUMBER" > reviews/.tmp/pr-$NUMBER-meta.json

curl -sS -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$OWNER/$REPO/pulls/$NUMBER/files?per_page=100" > reviews/.tmp/pr-$NUMBER-files.json

curl -sS -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$OWNER/$REPO/pulls/$NUMBER/commits" > reviews/.tmp/pr-$NUMBER-commits.json

# Passo 2.1 (check-runs) NO MESMO bash call pra garantir que $TOKEN e $SHA estão setados
# Python resiliente ao shim da Store no Windows (testa execucao; macOS/Linux -> python3). Single-token.
PYBIN=""; for _c in py python3 python; do command -v "$_c" >/dev/null 2>&1 && "$_c" -c '' >/dev/null 2>&1 && { PYBIN="$_c"; break; }; done; PYBIN="${PYBIN:-python}"
SHA=$("$PYBIN" -c "import json; print(json.load(open('reviews/.tmp/pr-$NUMBER-meta.json', encoding='utf-8'))['head']['sha'])" 2>/dev/null)
if [ -n "$SHA" ]; then
  curl -sS -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/check-runs" > reviews/.tmp/pr-$NUMBER-checks.json
fi
```

Tratamento:
- Se `META` contém `"message": "Not Found"` → pare. "PR #$NUMBER não encontrado em $OWNER/$REPO."
- Se `"Bad credentials"` → pare. "Token sem permissão — rode `git pull` para revalidar o credential."
- Se `META` contém `"state": "closed"` com `"merged": true` → mostre aviso "PR já foi mergeado em {merged_at}. Continuar revisão (útil pra post-mortem)?" — prossiga se sim.

Extraia metadata lendo o arquivo salvo (use heredoc `<< 'PYEOF'` pra evitar escape de aspas):

```bash
# Python resiliente ao shim da Store no Windows (testa execucao; macOS/Linux -> python3). Single-token.
PYBIN=""; for _c in py python3 python; do command -v "$_c" >/dev/null 2>&1 && "$_c" -c '' >/dev/null 2>&1 && { PYBIN="$_c"; break; }; done; PYBIN="${PYBIN:-python}"
"$PYBIN" << 'PYEOF'
import json
m = json.load(open('reviews/.tmp/pr-{N}-meta.json', encoding='utf-8'))
print(f"TITLE: {m.get('title','')}")
print(f"AUTHOR: @{m.get('user',{}).get('login','')}")
print(f"STATE: {m.get('state','')} (merged={m.get('merged',False)}, draft={m.get('draft',False)})")
print(f"BASE: {m.get('base',{}).get('ref','')}")
print(f"HEAD: {m.get('head',{}).get('ref','')}")
print(f"SIZE: +{m.get('additions',0)} / -{m.get('deletions',0)} in {m.get('changed_files',0)} files")
print(f"URL: {m.get('html_url','')}")
print('BODY:')
print(m.get('body') or '(vazio)')
PYEOF
```

Substitua `{N}` pelo número real do PR. Sempre `encoding='utf-8'` no `open()` — sem isso, Python 3 no Windows usa cp1252 e quebra em qualquer caractere não-latin1 (≤, ↗, emoji, etc.).

### 2.1 Status de CI (já está em Passo 2)

Como mostrado no bloco único acima, `check-runs` é chamado no mesmo bash call da coleta, com `$SHA` extraído de dentro desse mesmo call. Se rodar em call separada, `$TOKEN` e `$SHA` ficam vazios e a API retorna `422 "No commit found for SHA: /check-runs"`.

Conte `conclusion: "success"`, `"failure"`, `"pending"` lendo `reviews/.tmp/pr-$NUMBER-checks.json`. Se a resposta contém `"status": "422"` ou `"No commit found"`, o repo provavelmente não tem CI configurado — reporte "sem check-runs" no relatório, não é erro.

---

## Passo 3: Classificar arquivos alterados por domínio

Para cada arquivo em `$FILES`, classifique por path:

| Prefixo do path | Domínio |
|---|---|
| `.claude/skills/*/SKILL.md` | `skill` |
| `.claude/skills/*/CONTEXT.md` | `skill-context` |
| `brand/*/tokens.json` | `brand-tokens` |
| `brand/*/generation-rules.json` | `brand-rules` |
| `brand/*/brand-manifest.json` | `brand-manifest` |
| `brand/*/BRANDBOOK.md` | `brand-book` |
| `brand/*/assets/` | `brand-assets` |
| `landing-pages/*/*/` | `lp` |
| `landing-pages/GUIDELINES.md` | `lp-guidelines` |
| `meta-ads/` | `meta-ads` |
| `conhecimento/copywriting/` | `conhecimento-copy` |
| `conhecimento/editorial/` | `conhecimento-editorial` |
| `conhecimento/produto/` | `conhecimento-produto` |
| `newsletter/` | `entrega-newsletter` |
| `traducao/` | `entrega-traducao` |
| `CLAUDE.md` | `root-config` |
| `CHANGELOG.md` | `changelog` |
| `README.md` (root) | `readme` |
| outros | `misc` |

Construa uma lista `[{path, status, additions, deletions, patch, domain}]`.

### 3.1 Salvar patches em arquivos individuais

Patches vêm inline em `files.json` mas podem conter unicode (→, ≤, emojis) que quebra `print()` no Windows cp1252. Salve cada patch em arquivo separado e leia via `Read` tool depois:

```bash
# Python resiliente ao shim da Store no Windows (testa execucao; macOS/Linux -> python3). Single-token.
PYBIN=""; for _c in py python3 python; do command -v "$_c" >/dev/null 2>&1 && "$_c" -c '' >/dev/null 2>&1 && { PYBIN="$_c"; break; }; done; PYBIN="${PYBIN:-python}"
"$PYBIN" << 'PYEOF'
import json, os
files = json.load(open('reviews/.tmp/pr-{N}-files.json', encoding='utf-8'))
os.makedirs('reviews/.tmp/patches', exist_ok=True)
for f in files:
    fname = f['filename'].replace('/', '__')
    out = open(f'reviews/.tmp/patches/{fname}.patch', 'w', encoding='utf-8')
    out.write(f"# {f['filename']}\n")
    out.write(f"# status={f['status']} +{f.get('additions',0)}/-{f.get('deletions',0)}\n\n")
    out.write(f.get('patch') or '(binary or too large)')
    out.close()
print(f"Saved {len(files)} patches")
PYEOF
```

Depois use `Read` na skill pra abrir cada patch que quiser analisar (evita problemas de encoding no stdout do terminal).

---

## Passo 4: Carregar contexto local para domain checks

Baseado nos domínios presentes no PR, leia os arquivos de referência:

- Sempre: `CLAUDE.md`, `CHANGELOG.md` (lê pra saber se foi atualizado no PR)
- Se qualquer `skill` ou `skill-context` mudou: leia o `SKILL.md` correspondente **antes** do PR (via API em `main`) pra comparar, e o `SKILL.md` de um exemplo saudável (`.claude/skills/commit/SKILL.md`)
- Se qualquer `brand-*` mudou: leia `brand/DESIGN.md` + `brand/_shared/` se existir
- Se qualquer `lp` mudou: leia `landing-pages/GUIDELINES.md`
- Se `meta-ads` mudou: leia `meta-ads/SETUP.md`
- Se `root-config` mudou: leia o CLAUDE.md antes e depois (comparar tamanho — memory: manter ~40 linhas)

Para pegar versão "antes" de um arquivo via API:

```bash
BEFORE=$(curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github.raw" \
  "https://api.github.com/repos/$OWNER/$REPO/contents/{path}?ref=$BASE")
```

---

## Passo 5: Análise multi-dimensional

Aplique TODAS as dimensões abaixo. Para cada achado, registre:
- `severity`: `CRITICO` | `IMPORTANTE` | `NICE-TO-HAVE`
- `file`: path:line (se aplicável)
- `issue`: o que está errado
- `why`: por que é problema
- `suggestion`: como corrigir (texto, não código reescrito)

### Dimensão A — Genérico (sempre aplicar)

**🔴 CRÍTICO:**
- **Secrets hardcoded:** procure no diff por `api_key=`, `password=`, `token=`, `secret=`, `Authorization: Bearer `, strings longas que parecem JWT/AWS key (regex `AKIA[0-9A-Z]{16}`, `ghp_[a-zA-Z0-9]{36}`, etc.)
- **Command injection:** `os.system()`, `subprocess.call(shell=True)`, `eval()`, `exec()` com input vindo de argumento/env sem sanitização
- **SQL injection:** string formatting em query SQL (`f"SELECT ... {var}"`, `"... " + var + " ..."`)
- **Path traversal:** concatenação de path com input sem validação, uso de `../` não filtrado
- **Bug lógico claro:** off-by-one, condicional invertida, retorno em lugar errado, loop infinito
- **Break de CI:** se `CHECKS` tem failures, reporte cada um
- **Dependência nova sem justificativa:** `package.json`/`requirements.txt` com pacote novo sem menção no body do PR

**🟡 IMPORTANTE:**
- **Código morto:** import/variável/função declarada e não usada
- **Error handling defensivo:** try/except em cima de código que não pode falhar, fallbacks pra cenários impossíveis, validação redundante
- **Over-engineering:** abstração prematura (classe/helper usado uma vez só), feature flag pra mudança simples
- **Scope creep:** mudanças não relacionadas ao título do PR (refatoração + feat no mesmo PR)
- **Comentários inúteis:** comentários que explicam o óbvio, referenciam a task/issue, ou descrevem O QUÊ (o código já diz)
- **Testes:** se o PR adiciona lógica nova não-trivial e não tem teste, flagar
- **Arquivos grandes:** arquivo novo > 500 linhas — sugerir split

**🟢 NICE-TO-HAVE:**
- Clareza: nomes de variável melhores, estrutura mais legível
- Estilo: inconsistência menor com o resto do arquivo
- Docstrings/type hints faltando em função pública

---

### Dimensão B — Domain-specific do Agente Inhouse

Aplique apenas as seções correspondentes aos domínios do PR.

#### B.1 — Skills (`.claude/skills/*/SKILL.md`)

**🔴 CRÍTICO:**
- Frontmatter inválido ou faltando campos obrigatórios: `name`, `description`, `allowed-tools`, `version`
- `name` no frontmatter não bate com nome do diretório (`.claude/skills/{X}/SKILL.md` precisa ter `name: {X}`)
- Skill nova sem `version` (todas começam em `1.0.0`)

**🟡 IMPORTANTE:**
- `CHANGELOG.md` NÃO foi atualizado no mesmo PR quando `SKILL.md` mudou (regra do repo: mudanças de skill vão no CHANGELOG no mesmo PR)
- `version` não foi bumpada quando SKILL.md teve mudança significativa
- `description` vaga ou longa demais (>300 chars) — deve dizer o que faz em 1-2 frases
- `allowed-tools` pede ferramentas que não são usadas no corpo, ou não lista uma que é usada
- Referência a arquivos/skills que não existem (`.claude/skills/xyz/CONTEXT.md` citado mas não existe)
- Skill modifica `main` de qualquer forma (força-push, merge) — **nunca** deve

**🟢 NICE-TO-HAVE:**
- `argument-hint` ausente ou não-descritiva
- Docs de skill não tem exemplos de uso
- Sem separação por `Passos` claros

#### B.2 — Brand tokens (`brand/*/tokens.json`)

**🔴 CRÍTICO:**
- JSON malformado (parse falha)
- Estrutura fora do padrão W3C DTCG: todo token precisa ter `$value` e `$type` (ex: `{"primary": {"$value": "#FF0000", "$type": "color"}}`)

**🟡 IMPORTANTE:**
- Cor em formato não-hex sem justificativa (preferir `#RRGGBB` ou `#RRGGBBAA`)
- Token novo sem paralelo nas outras marcas (se uma marca tem `tokens.spacing.lg`, outras devem ter também por consistência de DX)
- `generation-rules.json` referencia token que não existe em `tokens.json` (drift)

**🟢 NICE-TO-HAVE:**
- Falta comentário `$description` em tokens não-óbvios

#### B.3 — Landing pages (`landing-pages/*/*/`)

Memory context aplicável:
- **2-3 cores por LP, hero clean branco, muito respiro** (`feedback_lp_design.md`)
- **Favicon path absoluto `/assets/logos/logo-icon.png`**, relativo quebra com cleanUrls (`feedback_favicon_png.md`)
- **Cxpress BoFu:** BRANDBOOK Cxpress não tem cases reais — se LP tem seção "Cases" ou "Clientes" com dados específicos, sinalizar pra verificar (`project_cxpress_cases_pendentes.md`)

**🔴 CRÍTICO:**
- Form ainda em mock (HTML form sem `action` ou com action fake) — se o PR é pra publicar, deve ter form real via `/lp-integrar-form`
- Favicon path relativo (`./assets/...` ou `assets/...`) — deve ser absoluto `/assets/logos/logo-icon.png`
- Secrets expostos em scripts inline (analytics keys, form IDs tudo OK expor, mas tokens de API não)
- Quebra de `landing-pages/GUIDELINES.md` em regra crítica (ler o GUIDELINES.md e checar)

**🟡 IMPORTANTE:**
- Mais de 3 cores principais no CSS (memory feedback)
- Hero não é "clean branco" (se mudança mexeu no hero)
- Falta meta tags essenciais (`<title>`, `<meta description>`, OG tags)
- Alt text faltando em imagens
- LP de Cxpress com seção de cases/números específicos — flagar pra validar com Victor (BRANDBOOK não tem dados)

**🟢 NICE-TO-HAVE:**
- Typography: mais de 2 famílias de fonte
- Espaçamento inconsistente entre seções
- Imagens sem otimização (>500KB)

#### B.4 — Meta Ads (`meta-ads/`)

**🔴 CRÍTICO:**
- Scripts Python com erro de sintaxe (tentar `py -m py_compile {file}`, ou `python3` no Mac/Linux, se possível)
- Credenciais/token commitado em arquivo rastreado (`.env` deve estar em `.gitignore`)
- Operação de escrita na API Meta (skill é SOMENTE LEITURA — qualquer `POST`/`PUT`/`DELETE` pra Graph API é crítico)

**🟡 IMPORTANTE:**
- Mudança em lógica de agregação sem teste
- Nova dependência em `requirements.txt` sem versão fixada

#### B.5 — Conhecimento (`conhecimento/`)

**🟡 IMPORTANTE:**
- Duplicação de regra que já existe em outro arquivo (procure por regras similares em `conhecimento/editorial/regras-anti-ia.md` se a mudança é em `copywriting/`)
- Regra nova contradiz uma existente
- Mudança em `fundamentos-copy.md` sem atualizar skills que dependem (copy-criar, copy-revisar)

#### B.6 — CLAUDE.md

Memory: **manter ~40 linhas** (detalhes vão nas skills, não no arquivo raiz).

**🟡 IMPORTANTE:**
- PR adiciona >10 linhas novas ao CLAUDE.md — questionar se não deveria ir pra uma skill ou CONTEXT.md
- Arquivo passou de 200 linhas — alerta forte (regra memory)

#### B.7 — CHANGELOG.md

**🟡 IMPORTANTE:**
- Entrada nova sem data ISO (`YYYY-MM-DD`)
- Data fora de ordem (entrada nova mais antiga que a última)
- Seção da skill não existe (skill listada em CHANGELOG mas sem diretório em `.claude/skills/`)
- Bump de MAJOR sem documentar breaking change

---

### Dimensão C — PR meta (estrutura do PR em si)

**🟡 IMPORTANTE:**
- Título não segue padrão PT-BR imperativo (convention do repo — olhar últimos commits em `main`): "Adicionar", "Atualizar", "Corrigir", "Remover", "Criar"
- Título > 70 chars
- Body vazio ou só 1 linha sem `## Resumo`
- PR gigante: > 1000 linhas mudadas OU > 20 arquivos — sugerir split
- Escopo misto: se os domínios mudados são totalmente distintos (ex: LP + meta-ads + brand tokens), questionar se não deveriam ser PRs separados
- Branch name não segue `claude/{slug}` (convenção `/commit`)

**🟢 NICE-TO-HAVE:**
- Body não tem seção "Arquivos alterados"
- Commits com mensagens genéricas (`update`, `fix`, `wip`)

---

## Passo 6: Consolidar e gerar veredicto

Conte achados por severidade. Veredicto:

| Condição | Veredicto |
|---|---|
| 0 críticos, 0 importantes | ✅ **Aprovar** |
| 0 críticos, ≤3 importantes | 🟡 **Aprovar com ressalvas** (importantes opcionais) |
| 0 críticos, >3 importantes | 🟡 **Pedir ajustes** (vários importantes) |
| ≥1 crítico | 🔴 **Rejeitar — resolver críticos antes** |

---

## Passo 7: Gerar relatório em `reviews/`

Crie o diretório se não existir:

```bash
mkdir -p reviews
```

Arquivo: `reviews/pr-{NUMBER}-YYYY-MM-DD.md` (se já existir com o mesmo nome, adicione sufixo `-v2`, `-v3`).

**Template:**

```markdown
# Review PR #{NUMBER} — {TITLE}

**URL:** {URL}
**Autor:** @{AUTHOR}
**Branch:** `{HEAD}` → `{BASE}`
**Tamanho:** +{ADD}/-{DEL} em {CHANGED_FILES} arquivo(s)
**CI:** {N}✅ {N}❌ {N}⏳
**Estado:** {STATE} {MERGED?}{DRAFT?}
**Revisado em:** YYYY-MM-DD

---

## Veredicto

{emoji} **{veredicto}**

{1-2 frases explicando a decisão}

**Achados:** {N} críticos · {N} importantes · {N} nice-to-have

---

## Resumo do PR

**Título:** {TITLE}

**Body original:**
> {primeiro parágrafo do body, truncado em 300 chars}

**Escopo dos domínios tocados:**
- `{domínio 1}`: {N} arquivos
- `{domínio 2}`: {N} arquivos
...

---

## 🔴 Críticos ({N})

{Se N=0, escrever "Nenhum.":}

### 1. {issue curto}

- **Arquivo:** `{path}:{linha}` (ou "N/A" se for meta)
- **Problema:** {detalhe}
- **Por quê:** {razão — cita regra do CLAUDE.md/GUIDELINES se aplicável}
- **Sugestão:** {correção em texto}

### 2. ...

---

## 🟡 Importantes ({N})

{mesma estrutura}

---

## 🟢 Nice-to-have ({N})

{mesma estrutura, mais conciso}

---

## Contexto adicional

{Observações que não são achados mas ajudam a decidir:}
- {Se mudou skill, resumir o que mudou funcionalmente}
- {Se é LP, resumir aderência ao GUIDELINES}
- {Se tem scope creep, sugerir divisão}
- {Se CI falhou, resumir quais jobs}

---

## Próximos passos

- [ ] Ler críticos e importantes acima
- [ ] Se aprovar: comentar no GitHub e mergear (Squash and merge)
- [ ] Se pedir ajustes: copiar os críticos/importantes e postar como review comment no PR
- [ ] Links úteis: [PR no GitHub]({URL}) · [Diff]({URL}/files)
```

---

## Passo 8: Output final no terminal

```
✅ Review gerado — PR #{NUMBER}

Veredicto:  {emoji} {veredicto}
Achados:    {N} críticos · {N} importantes · {N} nice-to-have
Relatório:  reviews/pr-{NUMBER}-YYYY-MM-DD.md

Leia o relatório e decida no GitHub: {URL}
```

**Nada mais.** Não ofereça postar no PR, não ofereça fazer merge, não ofereça re-revisar.

---

## Regras finais

- **Rigor > volume.** Prefira 3 críticos bem fundamentados a 20 nice-to-haves genéricos.
- **Cite a regra.** Todo achado importante/crítico deve citar por que é problema (CLAUDE.md, GUIDELINES, memory feedback, princípio geral). Se não consegue citar, provavelmente é nice-to-have.
- **Não reescreva.** Sugestão é texto descritivo, não bloco de código completo. Deixa a decisão de implementação pro autor do PR.
- **Sem autopromoção.** Não adicione "Gerado por Claude" no relatório nem assinatura de IA.
- **PR de outro repo:** se o usuário confirmar prosseguir, rode só Dimensão A (genérico) — pule Dimensão B (domain-specific deste repo).
- **PR grande e genérico:** se o PR tem >50 arquivos e é de outro repo, avise que a revisão vai ficar superficial — ofereça focar em N arquivos específicos se o usuário indicar.
