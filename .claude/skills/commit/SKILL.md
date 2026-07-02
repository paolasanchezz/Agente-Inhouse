---
name: commit
description: Cria branch, commita, faz push e abre pull request para a main automaticamente via API do GitHub. NUNCA commita em main, nunca faz merge, nunca usa --force. Use ao final das alterações para entregar ao Victor revisar.
argument-hint: "(sem args — totalmente automático)"
allowed-tools: Bash, Read, Grep
version: 2.0.1
---

# Skill: Commit + Pull Request para revisão

Você é um assistente de entrega para colaboradores do Agente Inhouse. Ao final das alterações do usuário, você cria branch nova, commita, faz push e abre um pull request para a main via API do GitHub — **totalmente autônomo, zero cliques**. O Victor revisa e aprova no GitHub.

A skill reusa o token do GitHub que o Git Credential Manager já guardou (o mesmo que faz `git push` funcionar sem pedir senha). Não requer `gh auth login`, não abre navegador.

**Regras invioláveis** (nunca quebre, mesmo se o usuário pedir):
- NUNCA commite em `main` — sempre em branch nova
- NUNCA use `--force`, `--force-with-lease`, `--no-verify`, `--amend`
- NUNCA faça merge, rebase ou `git reset --hard`
- NUNCA ignore arquivos sensíveis (`.env`, credenciais, tokens) — aborte e peça ação manual
- NUNCA adicione `Co-Authored-By: Claude` ou assinatura "Generated with Claude" em commits ou PRs

---

## Passo 0: Pre-flight checks

Rode estas verificações. Se qualquer uma falhar, **pare** e mostre a mensagem indicada — não tente contornar.

### 0.1 É um repo git?

```bash
git rev-parse --is-inside-work-tree
```

Se erro: mostre "Este diretório não é um repositório git. Rode `/commit` dentro do repo Agente Inhouse." e pare.

### 0.2 Rebase ou merge em andamento?

```bash
if [ -f "$(git rev-parse --git-path MERGE_HEAD)" ] || [ -f "$(git rev-parse --git-path REBASE_HEAD)" ]; then echo PENDING; else echo CLEAN; fi
```

Se `PENDING`, pare e mostre:

> **Há um rebase ou merge em andamento.** Resolva manualmente antes de rodar `/commit`:
> - Para abortar: `git merge --abort` ou `git rebase --abort`
> - Para continuar: resolva os conflitos, `git add` nos arquivos, depois `git rebase --continue` ou `git commit`

### 0.3 Há o que commitar?

```bash
git status --porcelain
```

Se vazio, mostre "Nada pra commitar — working tree limpo. Suas alterações já foram salvas em um commit anterior?" e pare.

---

## Passo 1: Inspecionar mudanças

Rode em paralelo:

```bash
git status --porcelain
git diff --stat
git diff --cached --stat
git branch --show-current
git diff | head -500
git diff --cached | head -500
```

Extraia da saída:
- **Lista de arquivos alterados** (modified, added, deleted, untracked) — do `git status --porcelain`
- **Branch atual** — do `git branch --show-current`
- **Natureza das mudanças** — do `git diff` (novos arquivos? só texto? copy? código? assets?)

### 1.1 Verificar arquivos sensíveis

Procure nos **nomes** dos arquivos alterados qualquer padrão sensível (use Grep com `-i`):

```
\.env$
\.env\.
credentials
secrets?\.(json|ya?ml)
\.pem$
id_rsa
\.key$
[Tt]oken
```

Se achar **qualquer** arquivo que bata, **aborte** e mostre:

> **Achei arquivos que parecem sensíveis no diff:**
> - `{arquivo 1}`
> - `{arquivo 2}`
>
> Não vou commitar isso. Se for intencional, peça ao Victor antes. Para remover do stage: `git restore --staged {arquivo}`. Para ignorar de vez: adicione ao `.gitignore`.

Só prossiga se a verificação passar limpa.

---

## Passo 2: Decidir branch

```bash
git branch --show-current
```

### Caso A — está em `main`

Crie branch nova seguindo a lógica abaixo.

**Lógica de nome da branch:**

1. **Tente inferir do path dominante** do diff. Olhe os diretórios top-level dos arquivos alterados:
   - Se ≤3 diretórios top-level E há um claramente dominante (>60% dos arquivos), use `claude/{tipo}-{slug-curto}`:
     - `landing-pages/buzzmonitor/xyz/` → `claude/lp-{slug}` (ex: `claude/lp-conteudo-que-converte`)
     - `brand/cxpress/` → `claude/brand-cxpress`
     - `.claude/skills/{nome}/` → `claude/skill-{nome}`
     - `conhecimento/copywriting/` → `claude/copy-{topico}`
     - `meta-ads/` → `claude/meta-ads-{topico}`
     - `newsletter/` ou `traducao/` → `claude/{pasta}-{slug}`
   - Slug em kebab-case, ≤30 caracteres, sem acentos

2. **Fallback random** se não for possível inferir:
   - Formato: `claude/{adjetivo}-{sobrenome}`
   - Adjetivos (escolha 1 ao acaso): `admiring`, `vibrant`, `flamboyant`, `eager`, `jolly`, `keen`, `lucid`, `sharp`, `quirky`, `nifty`, `brave`, `clever`, `stoic`, `witty`, `serene`
   - Sobrenomes (escolha 1 ao acaso): `yonath`, `elgamal`, `volhard`, `curie`, `turing`, `hopper`, `noether`, `lovelace`, `ritchie`, `knuth`, `dijkstra`, `hamilton`, `mcclintock`, `darwin`, `feynman`

3. **Verificar colisão:**
   ```bash
   git show-ref --quiet refs/heads/{nome-proposto}
   ```
   Se existir, gere outro (novo random ou adicione sufixo `-2`).

4. **Criar e trocar:**
   ```bash
   git checkout -b {nome-final}
   ```

### Caso B — está em branch != main

**Reuse a branch atual.** Mostre: "Usando branch existente: `{nome}`". Não crie outra. Vá direto para o Passo 3.

---

## Passo 3: Stage + commit

### 3.1 Stage dos arquivos

Adicione **arquivo por arquivo nomeado** — nunca use `git add -A` ou `git add .`:

```bash
git add "caminho/arquivo1" "caminho/arquivo2" ...
```

Liste apenas os arquivos identificados no Passo 1 que **passaram** na verificação de sensíveis. Pule arquivos que foram flaggeados.

### 3.2 Montar mensagem de commit (PT-BR imperativo)

**Regras:**
- 6 a 12 palavras
- Verbo inicial em imperativo no infinitivo, PT-BR:
  - Novo arquivo (status `??` ou `A`) → "**Adicionar**"
  - Modificação (status `M`) → "**Atualizar**"
  - Remoção (status `D`) → "**Remover**"
  - Se o diff menciona "fix", "bug", "corrige", "erro" → "**Corrigir**"
- Objeto: feature/path dominante em linguagem humana, não path completo
  - Bom: `Atualizar LP buzzmonitor conteudo-que-converte`
  - Ruim: `Atualizar landing-pages/buzzmonitor/conteudo-que-converte/index.html`
- Múltiplos paths sem dominante: resumo humano
  - Ex: `Atualizar 3 LPs buzzmonitor + assets brand Cxpress`
- **Sem** ponto final
- **Sem** `Co-Authored-By`, **sem** menção a "Claude", **sem** emojis

**Exemplos reais do repo pra se guiar:**
- `Reduzir H1 da LP PT para acomodar "deveria ser o seu" em uma linha`
- `Criar versao PT-PT da LP Webinar Monitoramento de Concorrentes`
- `Otimizar skills advisors: cortar 50-60% do SKILL.md`
- `Adicionar versionamento leve de skills + CHANGELOG`

### 3.3 Commitar

```bash
git commit -m "{mensagem}"
```

**Se o hook pre-commit falhar:**
- Mostre o stderr completo para o usuário
- Aborte a skill
- **NUNCA** retente com `--no-verify`
- Peça ao usuário: "O hook de pre-commit bloqueou. Resolva o problema apontado acima e rode `/commit` de novo."

Capture o hash curto do commit criado:

```bash
git rev-parse --short HEAD
```

---

## Passo 4: Push

```bash
git push -u origin {branch}
```

**Tratamento de erros:**

| Sintoma no stderr | Ação |
|---|---|
| `Updates were rejected because the remote contains work` (non-fast-forward) | Pare. Mostre: "A branch remota tem commits que você não tem local. Rode `git pull --rebase origin {branch}`, resolva conflitos se houver, e rode `/commit` de novo. **Não use --force.**" |
| `Permission denied`, `403`, `authentication failed` | Pare. Mostre: "Falha de autenticação no push — o Git não tem suas credenciais do GitHub salvas. Abra o terminal e rode `git pull` — se pedir login, use o navegador. Isso faz o Windows salvar seu token. Depois rode `/commit` de novo." |
| `fatal: The current branch ... has no upstream branch` (sem `-u`) | Não deve acontecer porque usamos `-u`. Se acontecer, mostre o erro e pare. |

**Nunca** use `--force` ou `--force-with-lease`, mesmo que o usuário peça.

---

## Passo 5: Abrir pull request via API do GitHub

Usa o token que o Git Credential Manager já tem salvo (o mesmo que autenticou o push do Passo 4). **Zero interação com o usuário**.

### 5.1 Montar título e body

**Título** = mensagem do commit (Passo 3.2). ≤70 caracteres.

**Body** em markdown plano, escrito num temp file (para não ter problema com aspas/newlines ao montar o JSON depois):

```bash
BODY_FILE=$(mktemp)
cat > "$BODY_FILE" << 'EOF'
## Resumo
- {bullet 1 descrevendo a mudança principal}
- {bullet 2 se houver mudança secundária}

## Arquivos alterados
- {path1}
- {path2}
- {path3}
EOF
```

Regras do body:
- 1 a 4 bullets no Resumo — foco no "o quê" e "por quê", não "como"
- Liste até 10 arquivos. Se forem mais, mostre os 10 primeiros + "_... e mais {N} arquivos._"
- **Sem** seção Test plan (simplicidade pro newbie)
- **Sem** linha "Generated with Claude Code" ou similar
- **Sem** `Co-Authored-By`

### 5.2 Extrair token do Git Credential Manager

```bash
TOKEN=$(printf "protocol=https\nhost=github.com\n\n" | GIT_TERMINAL_PROMPT=0 git credential fill 2>/dev/null | sed -n 's/^password=//p')
```

`GIT_TERMINAL_PROMPT=0` impede que o git abra prompt interativo se não houver credencial salva — ele falha silenciosamente e o `TOKEN` fica vazio.

**Se `TOKEN` estiver vazio**, pare e mostre:

> **Não achei sua credencial do GitHub salva no Git Credential Manager.**
>
> Isso é inesperado — normalmente o Windows guarda automaticamente quando você cloou ou pushou pela primeira vez. Rode no terminal:
> ```
> git pull
> ```
> Se pedir login, use o navegador (o Windows salva o token automaticamente). Depois rode `/commit` de novo.

### 5.3 Descobrir owner/repo

```bash
REPO_PATH=$(git remote get-url origin | sed -E 's|\.git$||; s|^https://github.com/||; s|^git@github.com:||')
OWNER=$(echo "$REPO_PATH" | cut -d/ -f1)
```

Resultado esperado: `REPO_PATH=victorfmlopes/Agente-Inhouse`, `OWNER=victorfmlopes`.

### 5.4 Verificar se PR já existe

```bash
EXISTING=$(curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$REPO_PATH/pulls?head=${OWNER}:{branch}&state=open")

# Python resiliente ao shim da Store no Windows (testa execucao; macOS/Linux -> python3). Single-token.
PYBIN=""; for _c in py python3 python; do command -v "$_c" >/dev/null 2>&1 && "$_c" -c '' >/dev/null 2>&1 && { PYBIN="$_c"; break; }; done; PYBIN="${PYBIN:-python}"
EXISTING_URL=$("$PYBIN" -c "import json,sys; p=json.loads(sys.stdin.read()); print(p[0]['html_url'] if isinstance(p, list) and p else '')" <<< "$EXISTING")
```

Os blocos resolvem `$PYBIN` (testa execução; prefere `py` no Windows — onde `python`/`python3` no PATH costumam ser o shim da Store, exit 49 — e cai em `python3` no Mac/Linux). Nunca chame `python` literal.

Se `EXISTING_URL` não estiver vazio: **pule para o Passo 6** com essa URL e mostre como "PR já aberto: {url} — adicionei seu novo commit nele."

### 5.5 Criar o PR

```bash
# Python resiliente ao shim da Store no Windows (testa execucao; macOS/Linux -> python3). Single-token.
PYBIN=""; for _c in py python3 python; do command -v "$_c" >/dev/null 2>&1 && "$_c" -c '' >/dev/null 2>&1 && { PYBIN="$_c"; break; }; done; PYBIN="${PYBIN:-python}"
PAYLOAD=$("$PYBIN" -c "
import json,sys
print(json.dumps({
  'title': sys.argv[1],
  'body': open(sys.argv[2]).read(),
  'head': sys.argv[3],
  'base': 'main'
}))
" "{title}" "$BODY_FILE" "{branch}")

RESPONSE=$(curl -sS -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -d "$PAYLOAD" \
  "https://api.github.com/repos/$REPO_PATH/pulls")

rm "$BODY_FILE"

PR_URL=$("$PYBIN" -c "import json,sys; d=json.loads(sys.stdin.read()); print(d.get('html_url', ''))" <<< "$RESPONSE")
```

**Tratamento da resposta:**

| Condição | Ação |
|---|---|
| `PR_URL` não vazio | ✅ Sucesso. Guarda URL, vai ao Passo 6. |
| Response contém `"Bad credentials"` (401) ou `"Resource not accessible"` (403) | Pare. Mostre: "Seu token do GitHub salvo não tem permissão pra abrir PR via API. Pode ser escopo insuficiente ou token expirado. Abra `{REPO_URL}/compare/main...{branch}?expand=1` no navegador e crie o PR manualmente — título e body eu imprimo abaixo pra você colar." Imprima o título e o conteúdo de `$BODY_FILE` depois. |
| Response contém `"pull request already exists"` (422) | Refaça o GET do passo 5.4 sem `&state=open` pra pegar URL. Use como "PR já aberto". |
| Outros erros | Mostre o conteúdo de `$RESPONSE` bruto pro usuário e pare. |

---

## Passo 6: Output final

```
✅ Entregue!

Branch:  {nome-da-branch}
Commit:  {hash-curto} — "{mensagem}"
PR:      {url-do-pr}

Mande essa URL pro Victor revisar. Não dê merge você mesmo — ele aprova no GitHub.
```

**Nada mais.** Não sugira próximos passos, não ofereça fazer merge, não pergunte se quer criar outra branch.

---

## Lembretes finais

- Se em qualquer momento você ficar em dúvida sobre destruir algo (force push, amend, reset), **pare e mostre o estado atual pro usuário**. É melhor ele perguntar ao Victor do que você tentar adivinhar.
- A skill é uma via de mão única: cria PR, entrega. Não faz parte do escopo resolver conflitos, rebase interativo, ou cleanup de branch antiga.
- Se o usuário pedir algo fora desse escopo ("faz merge pra mim", "apaga essa branch", "reverte o último commit"), responda: "Isso está fora do escopo do `/commit`. Peça ao Victor — ele resolve pelo GitHub."
