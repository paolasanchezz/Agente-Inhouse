---
name: lp-publicar
description: Sincroniza LP para pasta sibling — solo (1 projeto = 1 LP) ou guarda-chuva (N LPs num mesmo projeto Vercel quando o dominio ja esta atribuido). Deploya via Vercel CLI, valida PageSpeed + headers, publica relatorio Notion. Garante zero vazamento do repo interno e zero regressao em LPs vizinhas.
argument-hint: "[marca] [slug-ou-slugs-CSV] [dominio-opcional] — ex: buzzcreators vendendo-com-creators evento.buzzmonitor.com OU buzzmonitor mcp,mcp-es,mcp-pt material.buzzmonitor.com"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, Skill, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-pages, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-update-page
version: 3.9.3
---

# Skill: Publicar Landing Page

Voce sincroniza a LP do repo do agente para uma pasta sibling isolada fora do repo, roda deploy na Vercel, valida e publica relatorio no Notion. **Regra inegociavel: nenhum arquivo do repo interno (.env, skills, conhecimento/, brand/, meta-ads/) pode vazar para a pasta sibling ou para o deploy.**

A skill opera em dois modos:

| Modo | Quando | Sibling | Resultado URL |
|---|---|---|---|
| **solo** | dominio nao fornecido OU fornecido mas sem projeto Vercel atribuido | `{SIBLING_BASE}/{marca}-lp-{slug}/` (novo) | `https://{marca}-lp-{slug}-{hash}.vercel.app/{slug}` ou dominio fresco |
| **guarda-chuva** | dominio ja atribuido a outro projeto Vercel (Passo 0.5 detecta) | `{SIBLING_BASE}/{nome-do-projeto-detectado}/` (existente) | `https://{dominio}/{slug}` (LP nova convive com vizinhas) |

`{SIBLING_BASE}` e resolvido em runtime pelo Passo 0.1 (env var `LP_SIBLING_BASE` > linha em `.env.local` na raiz). Configurado uma vez via `/setup-agencia`. Nunca hardcodar path absoluto da maquina aqui.

A diferenca pratica: no modo guarda-chuva voce **nao cria projeto Vercel novo**, **anexa a LP** como subpasta ao sibling existente, **namespaceia assets por marca** (`/assets/{marca}/X`) para evitar colisao com vizinhas, e o relatorio inclui smoke test de **todas** as LPs do projeto.

## Passo 0: Parsing e Contexto

Leia, na ordem:

1. `landing-pages/CONTEXT.md` — runbook operacional. Use principalmente §3 (convencao de assets — paths source vs deploy, namespace solo vs guarda-chuva), §4 (modos de deploy), §6 (troubleshooting de erros conhecidos: favicon 404, mascote 404, CSP, smoke test divergente, FetchError CLI), §7 (anti-padroes documentados).
2. `.claude/skills/lp-preparar/CONTEXT.md` — convencoes de marca, IDs Notion, formato `tracking.json`.

Parsing de `$ARGUMENTS`:

| Argumento | Valores | Obrigatorio |
|---|---|---|
| `marca` | `buzzmonitor` \| `buzzcreators` \| `cxpress` \| `elife` | Sim |
| `slug` | kebab-case unico OU multiplos slugs em CSV (`mcp,mcp-es,mcp-pt`) — ver "Modo batch" abaixo | Sim |
| `dominio` | FQDN (ex: `evento.buzzmonitor.com`, `material.buzzmonitor.com`, `content.cxpress.io`, `webinar.buzzmonitor.com`) | Nao |

### Modo batch (v3.6.0)

Quando `slug` contem virgula, a skill entra em **modo batch**: publica N LPs irmas no mesmo guarda-chuva em **1 unico deploy**. Cenario tipico: familia multi-idioma (`mcp`, `mcp-es`, `mcp-pt`) que precisa ir pro live junta — sem isso, deployar uma de cada vez gera 3 entradas no historico Vercel + 3 syncs redundantes + janela em que so 1 das 3 esta atualizada.

```bash
# Detectar modo batch
if echo "$slug" | grep -q ','; then
  MODE_BATCH=true
  SLUGS=$(echo "$slug" | tr ',' '\n' | sed 's/^ *//;s/ *$//')   # array de slugs
  SLUG_COUNT=$(echo "$SLUGS" | wc -l)
else
  MODE_BATCH=false
  SLUGS="$slug"
  SLUG_COUNT=1
fi
```

**Quais passos rodam N vezes vs 1 vez em modo batch:**

| Passo | Quantas vezes em batch |
|---|---|
| 0.1, 0.5.a-c (pre-flight, deteccao de modo) | 1x |
| 0.5.d sync via Vercel API | **1x** (mesma sibling baixa o live inteiro uma vez) |
| 1.0 drift-check pre-overwrite | **Nx** (1 por slug) |
| 1.1-1.5 copy + assets + rewrite + grep VAZOU | **Nx** (1 por slug) |
| 1.6 CSP drift-check | 1x |
| 2.1-2.3 validacao isolamento | 1x |
| 2.4 baseline vizinhas | 1x (vizinhas = LPs no sibling que NAO estao em SLUGS) |
| 3.2 deploy | **1x** (1 entry no historico Vercel) |
| 3.4 smoke test | 1x (loop sobre SLUGS + baseline) |
| 5.1-5.4 PageSpeed + headers + GTM + cert | **Nx** (1 por slug) |
| 6 relatorio Notion | 1 relatorio agregado das N LPs |

**Restricoes:**

- Modo batch so faz sentido em **guarda-chuva** (todas as LPs no mesmo dominio). Em solo, batch nao se aplica — cada LP teria projeto Vercel proprio. Se `MODE_BATCH=true` e Passo 0.5.b detecta `solo`, abortar com: "Modo batch requer guarda-chuva (dominio compartilhado). Slugs detectados: $SLUGS. Sem dominio fornecido ou dominio nao atribuido — rode `/lp-publicar {marca} {slug-individual}` para cada um."
- Todos os slugs no batch devem ser da MESMA marca. Misturar (`buzzmonitor/mcp,cxpress/playbook`) nao e suportado.
- Se algum slug do batch nao tem fonte em `landing-pages/{marca}/{slug}/index.html`, abortar antes de iniciar — listar todos os ausentes.

**Historico:** convencao estabelecida em 2026-05-18 (sessao MCP `material.buzzmonitor.com`). 3 LPs irmas publicadas em 1 deploy via fluxo manual da skill — virou suporte nativo na v3.6.0.

### 0.1 Resolver `SIBLING_BASE`

Duas fontes, em ordem de precedencia:

1. **Env var `LP_SIBLING_BASE`** no shell (override pontual).
2. **Linha `LP_SIBLING_BASE=...` em `.env.local`** na raiz do repo (gitignored — escrito pelo `/setup-agencia`). Em worktrees, o `.env.local` mora no repo principal — usar `git rev-parse --git-common-dir` pra resolver corretamente.

```bash
SIBLING_BASE="$LP_SIBLING_BASE"

if [ -z "$SIBLING_BASE" ]; then
  # Tentar .env.local no CWD (caso normal) e no repo principal (caso worktree)
  for ENV_DIR in . "$(git rev-parse --git-common-dir 2>/dev/null | sed 's|/.git$||')"; do
    [ -z "$ENV_DIR" ] && continue
    if [ -f "$ENV_DIR/.env.local" ]; then
      SIBLING_BASE=$(grep -E "^LP_SIBLING_BASE=" "$ENV_DIR/.env.local" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'" | tr -d '\r')
      [ -n "$SIBLING_BASE" ] && break
    fi
  done
fi
```

**Se `SIBLING_BASE` ficar vazio** (nem env var nem `.env.local` existem com a chave): NAO abortar com erro seco. Em vez disso:

1. Avise o usuario em uma frase: "Falta `LP_SIBLING_BASE`. Vou rodar `/setup-agencia` agora pra configurar — depois retomo este deploy."
2. Use o tool `Skill` invocando `setup-agencia` com argumento `"so lp"` (escopo restrito a Landing Pages — pula Notion/Meta).
3. Apos o setup-agencia terminar (ele escreve `.env.local`), **re-execute o comando de leitura acima**. Agora deve resolver. Se ainda falhar (usuario abortou setup), pare com mensagem clara.

Garantir que `SIBLING_BASE` existe (`mkdir -p "$SIBLING_BASE"`, no-op se ja existe).

**Por que sem fallback automatico (parent-do-repo)?** Tinhamos isso em v2.0.0 com sanity check de OneDrive/iCloud/Dropbox. Removido em v3.0.0 porque adicionava complexidade significativa pra cobrir um caso que o setup-agencia ja resolve melhor (perguntando ao usuario qual path quer, sem adivinhacao).

### 0.2 Paths derivados

Paths default (modo solo):
- Fonte: `landing-pages/{marca}/{slug}/index.html`
- Sibling: `${SIBLING_BASE}/{marca}-lp-{slug}/`
- Dentro da sibling: `{slug}/index.html` + `assets/` + `vercel.json` + `.gitignore` + `README.md`

Se fonte nao existe, PARE.

### 0.3 Convencao OBRIGATORIA: path Windows-style ao passar pro Python

**No Windows, o `python`/`python3` no PATH e o Python do Windows** (tipicamente o da Microsoft Store em `AppData/Local/Microsoft/WindowsApps/`). Ele **nao entende paths estilo MSYS** (`/c/Users/...`) que o Git Bash usa internamente. As ferramentas bash (`find`, `grep`, `cp`, `md5sum`) entendem as duas formas — entao o desencontro acontece **so na fronteira com o Python**:

- `python -c "...open('/c/Users/.../vercel.json')..."` → **`FileNotFoundError`** (leitura).
- `SIBLING=/c/Users/... python sync_sibling.py` → escreve em `C:\c\Users\...` **em silencio** (escrita — pior, nao falha).

**Regra:** todo path passado ao Python — seja `python -c` inline, seja env var consumida por um helper `.py` (`sync_sibling.py`, `csp_drift_check.py`) — DEVE ser normalizado para formato Windows (`C:/...`, com barra normal) **antes** de chegar ao Python. Snippet canonico (no-op em macOS/Linux e em path que ja e Windows-style):

```bash
# cygpath -m devolve a forma "mixed" (C:/Users/..., barra normal) — funciona em open()
# do Python no Windows e nao tem backslash pra escapar no bash nem no raw-string Python.
# Fallback sem cygpath: /c/Users/... -> C:/Users/...  (em Unix nao casa nada -> no-op).
to_win_path() { cygpath -m "$1" 2>/dev/null || printf '%s' "$1" | sed -E 's#^/([a-zA-Z])/#\1:/#'; }
```

Como cada bloco bash roda em shell proprio (a funcao acima nao persiste entre execucoes), **cada snippet abaixo que toca o Python ja inlina essa normalizacao** — nao remover.

**Corolario (igualmente obrigatorio):** **nunca** suprimir o stderr (`2>/dev/null`) de um `python -c` que le um path. Um `FileNotFoundError` silenciado vira saida vazia, e a logica seguinte le esse vazio como "nao ha nada" em vez de "a leitura falhou" — foi exatamente isso que gerou o falso positivo de "REGRESSAO" do smoke test em 2026-06-30 (REDIRECT_MAP vazio; ver `landing-pages/CONTEXT.md` §7.2). Se um valor derivado de path Python sair vazio quando nao deveria, **abortar**, nao seguir.

> Mesma pegadinha do `/tmp` Python-vs-bash no Windows (Python grava `/tmp` em `C:\tmp`, bash usa o `/tmp` do MSYS): formas de path MSYS e Windows apontam pro mesmo lugar pras ferramentas bash, mas o Python do Windows so entende a forma Windows.

### 0.4 Convencao OBRIGATORIA: interpretador Python resiliente ao shim do Windows

**No Windows, `python`/`python3` no PATH costumam ser o shim da Microsoft Store** (`AppData/Local/Microsoft/WindowsApps/python.exe`). O arquivo **existe** (`command -v python` acha), mas ao rodar ele **falha com exit 49** imprimindo `Python was not found; run without arguments to install from the Microsoft Store`. O launcher **`py`** aponta pro Python real. Em macOS/Linux nao ha `py` e `python3`/`python` sao os corretos. Um recovery de LP em 2026-07-02 travou exatamente aqui: `python sync_sibling.py` deu exit 49 e o sync nao rodou.

Por isso **nunca** chame `python` literal num snippet bash. Resolva o interpretador testando **execucao** (nao so existencia — o shim passa no `command -v` e so quebra ao rodar de fato) e use `$PYBIN`:

```bash
# Fica com o 1o interpretador que RODA de verdade. Windows: pula o shim da Store (exit 49) e
# acha `py`. macOS/Linux: `py` nao existe -> cai em `python3`/`python`. Single-token de proposito:
# os scripts desta skill (sync_sibling.py, csp_drift_check.py) sao stdlib-only e rodam em qualquer
# versao. Skills com C-extension (pandas/psycopg) NAO usam este resolver — usam `uv run --python 3.12`,
# que provisiona o proprio Python 3.12 (o `py -3.12` nem sempre esta instalado nesta maquina).
PYBIN=""; for _c in py python3 python; do command -v "$_c" >/dev/null 2>&1 && "$_c" -c '' >/dev/null 2>&1 && { PYBIN="$_c"; break; }; done; PYBIN="${PYBIN:-python}"
```

Como cada bloco bash roda em shell proprio (o `PYBIN` nao persiste entre execucoes), **cada snippet abaixo que toca o Python ja inlina esse resolver** junto do `to_win_path` — nao remover. As duas convencoes sao ortogonais e complementares: `$PYBIN` escolhe **qual** interpretador roda, `to_win_path` normaliza **o path** que chega nele.

## Passo 0.5: Detectar modo (solo vs guarda-chuva)

### 0.5.a Pre-flight do Vercel CLI (cross-platform)

Antes de qualquer chamada Vercel, validar que o CLI esta instalado e autenticado. **Nao** ler `$APPDATA/.../auth.json` direto — path varia por SO e por versao do CLI.

```bash
TEAM=team_nC991VqUuSU2jXZN152xqqEg  # elife-group

# 1. CLI disponivel? (npx baixa on-demand se nao existir global)
npx --yes vercel --version >/dev/null 2>&1 || {
  echo "ERRO: Vercel CLI indisponivel. Instale com 'npm i -g vercel' ou aguarde npx baixar."
  exit 1
}

# 2. Autenticado na org elife-group?
npx --yes vercel whoami --scope "$TEAM" >/dev/null 2>&1 || {
  echo "ERRO: nao autenticado no Vercel CLI (escopo $TEAM)."
  echo "Rode 'npx vercel login' e autorize no navegador. Importante: o MCP Vercel do Claude Code"
  echo "e uma autenticacao SEPARADA do CLI — esta skill precisa do CLI autenticado."
  exit 1
}
```

### 0.5.b Detectar guarda-chuva via `vercel alias ls`

Se `$dominio` foi fornecido, descobrir se algum projeto Vercel da org ja serve esse dominio. **Nao** precisar do token na shell — o CLI ja gerencia auth internamente em qualquer SO. Basta chamar `vercel alias ls` e procurar o dominio.

```bash
DOMAIN="$dominio"  # vem do parsing do Passo 0

# Lista os aliases da org. Cada linha tem colunas: source-deployment-url | alias-url | age.
# Quando $DOMAIN aparece como alias (coluna 2), extrair o nome do projeto do prefixo da
# source URL (formato: {projeto}-{hash7-12}-elife-group.vercel.app).
#
# PAGINACAO (obrigatorio): `vercel alias ls` retorna ~20 aliases por pagina (mais recentes
# primeiro) e imprime no rodape `... --next <token>` quando ha mais. Guarda-chuvas ANTIGOS
# (criados ha semanas) caem em paginas posteriores — sem paginar, a deteccao retorna vazio,
# a skill cai erroneamente em modo solo e cria projeto duplicado que NAO serve o dominio.
# Bug encontrado 2026-06-25: webinar.buzzmonitor.com estava na pagina 2.
PROJECT=""; NEXT=""; PAGE=0
while [ "$PAGE" -lt 50 ]; do   # teto ~1000 aliases por seguranca
  PAGE=$((PAGE+1))
  if [ -z "$NEXT" ]; then
    ALIAS_OUT=$(npx --yes vercel alias ls --scope "$TEAM" 2>&1)
  else
    ALIAS_OUT=$(npx --yes vercel alias ls --next "$NEXT" --scope "$TEAM" 2>&1)
  fi
  PROJECT=$(printf '%s\n' "$ALIAS_OUT" | awk -v d="$DOMAIN" '
    $2 == d { src = $1; sub(/-[a-z0-9]+-elife-group\.vercel\.app$/, "", src); print src; exit }
  ')
  [ -n "$PROJECT" ] && break
  NEXT=$(printf '%s\n' "$ALIAS_OUT" | sed -n 's/.*--next \([0-9]\{10,\}\).*/\1/p' | head -1)
  [ -z "$NEXT" ] && break   # sem mais paginas
done
```

Possiveis saidas:

| `$PROJECT` | Modo | Decisao |
|---|---|---|
| Vazio | **solo** | Sibling = `${SIBLING_BASE}/{marca}-lp-{slug}` (novo). Comportamento default. |
| Nome do projeto | **guarda-chuva** | Sibling = `${SIBLING_BASE}/{$PROJECT}` (existente OU recem-criado-localmente). Anexar LP como subpasta. |

**Por que nao `curl` + API V9 direto?** Porque exigia ler o token Vercel do filesystem (`$APPDATA/com.vercel.cli/Data/auth.json`), e isso quebra em pelo menos 3 cenarios reais: (a) Python da Microsoft Store rodando em sandbox AppContainer no Windows nao consegue acessar paths absolutos em `AppData/Roaming/` (testado e confirmado em 2026-05-04); (b) macOS e Linux usam paths totalmente diferentes; (c) versoes futuras do CLI podem mudar o local. `vercel alias ls` deixa o CLI cuidar de auth — funciona em qualquer SO/versao.

**Por que nao `vercel projects ls`?** Esse comando so retorna a "Latest Production URL" de cada projeto, que vem como `.vercel.app` quando o projeto ainda nao teve deploy production aliasado ao dominio custom (cenario "guarda-chuva recem-criado, em popularizacao"). `vercel alias ls` lista TODOS os aliases (inclusive subdomains custom atribuidos sem deploy proprio ainda), evitando o falso-negativo. Validado em 2026-05-04: detecta corretamente `material.buzzmonitor.com` → `buzzmonitor-material` mesmo o projeto ainda mostrando `.vercel.app` em `projects ls`.

**Edge case:** projeto sem dominio custom (so `.vercel.app`) nao aparece como alias para nenhum FQDN externo, entao `$PROJECT` fica vazio = modo solo. Correto.

### 0.5.c Garantir `.vercel/project.json` no sibling de guarda-chuva

Se modo guarda-chuva: pode ser que o sibling local nao exista nesta maquina (primeira vez que alguem que nao seja o dono original roda em guarda-chuva). Sempre garantir:

1. Pasta existe: `mkdir -p "${SIBLING_BASE}/{nome-do-projeto}"`.
2. `.vercel/project.json` existe e bate com o que a API retornou:
   ```bash
   SIBLING="${SIBLING_BASE}/{nome-do-projeto}"
   if [ ! -f "$SIBLING/.vercel/project.json" ]; then
     cd "$SIBLING" && npx --yes vercel link --yes --project="{nome-do-projeto}" --scope "$TEAM"
   fi
   ```
3. Se ja existe mas `projectId`/`orgId` nao batem com a API (sibling local stale), re-rodar o `vercel link` acima para regenerar.

**Importante:** dominio nao fornecido sempre = modo solo, mesmo se outro projeto da org ja serve um dominio. Sem dominio, a skill nao tem sinal pra inferir guarda-chuva.

### 0.5.d Sync sibling com ultimo deploy production (guarda-chuva e solo re-publicacao)

**Quando rodar:**

| Cenario | Sibling tem `.vercel/project.json`? | Acao |
|---|---|---|
| **Guarda-chuva** (qualquer execucao) | sim (garantido pelo 0.5.c) | rodar sync |
| **Solo, re-publicacao** | sim (de execucao anterior) | rodar sync |
| **Solo, primeira publicacao** | nao | **pular sync** com mensagem clara: "Solo, primeira publicacao — sem deploy anterior para sincronizar" |

```bash
if [ ! -f "$SIBLING/.vercel/project.json" ]; then
  echo "Solo, primeira publicacao — sem deploy anterior para sincronizar. Pulando 0.5.d."
  # Pular para Passo 1
else
  # Executar 0.5.d.i a 0.5.d.iv
fi
```

**Por que sync tambem em solo:** historicamente o 0.5.d so rodava em guarda-chuva (v3.1.0) porque o incidente motivador era de regressao em vizinha. Mas o **buraco simetrico** existe em solo re-publicacao: se outra pessoa deployou de outra maquina sem commitar (ou aplicou hotfix manual via Vercel UI), o `lp-publicar` solo sobrescreve sem aviso. Fechado em v3.3.0 — sync popula a sibling com a versao do live antes do drift-check do Passo 1.0.

No modo guarda-chuva, popular a sibling local com arquivos do ultimo deploy production **antes** do Passo 1 modificar nada. Sem isso, primeira execucao numa maquina sem sibling local resulta em deploy que apaga vizinhas em silencio — `BASELINES_OTHERS` (Passo 2.4) e capturado da sibling LOCAL, e se ela esta vazia, o smoke test 3.4.b nao detecta a regressao. Incidente motivador documentado em `landing-pages/CONTEXT.md` §7.2 (2026-05-07).

#### 0.5.d.i Resolver e validar VERCEL_TOKEN

Precedencia:

1. Env var `VERCEL_TOKEN` no shell.
2. Linha `VERCEL_TOKEN=...` em `.env.local` na raiz do repo (gitignored). Em worktrees, o `.env.local` mora no repo principal — usar `git rev-parse --git-common-dir` pra resolver.
3. Parse de `auth.json` do CLI Vercel — sempre dentro de `.../com.vercel.cli/Data/auth.json` (note `/Data/` no meio):
   - Linux/WSL: `~/.local/share/com.vercel.cli/Data/auth.json`
   - macOS: `~/Library/Application Support/com.vercel.cli/Data/auth.json`
   - Windows: `$APPDATA/com.vercel.cli/Data/auth.json`

**Atencao:** o token do `auth.json` tem `expiresAt` curto (horas). O CLI Vercel renova automaticamente via `refreshToken` quando voce roda `vercel <cmd>`, MAS chamadas API REST direta (que esta skill usa pra sync) nao tem esse fallback. Por isso, **sempre validar o token resolvido** com `curl /v2/user` antes de usar — se 200, OK; se 401/403, descartar e tentar fonte alternativa.

```bash
# 1. Tentar env var
TOKEN_CANDIDATE="$VERCEL_TOKEN"

# 2. Tentar .env.local (CWD primeiro, depois repo principal — suporta worktree)
if [ -z "$TOKEN_CANDIDATE" ]; then
  for ENV_DIR in . "$(git rev-parse --git-common-dir 2>/dev/null | sed 's|/.git$||')"; do
    [ -z "$ENV_DIR" ] && continue
    if [ -f "$ENV_DIR/.env.local" ]; then
      TOKEN_CANDIDATE=$(grep -E "^VERCEL_TOKEN=" "$ENV_DIR/.env.local" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'" | tr -d '\r')
      [ -n "$TOKEN_CANDIDATE" ] && break
    fi
  done
fi

# 3. Tentar auth.json do CLI (cross-platform, sempre com /Data/)
if [ -z "$TOKEN_CANDIDATE" ]; then
  for AUTH_PATH in \
    "$HOME/.local/share/com.vercel.cli/Data/auth.json" \
    "$HOME/Library/Application Support/com.vercel.cli/Data/auth.json" \
    "$APPDATA/com.vercel.cli/Data/auth.json"; do
    [ -f "$AUTH_PATH" ] || continue
    # bash extrai sem dependencia em python (que pode falhar lendo AppData no Windows sandbox)
    TOKEN_CANDIDATE=$(sed -n 's/.*"token"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$AUTH_PATH" | head -1)
    [ -n "$TOKEN_CANDIDATE" ] && break
  done
fi

# 4. Validar token via /v2/user (descarta se expirado/invalido)
if [ -n "$TOKEN_CANDIDATE" ]; then
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $TOKEN_CANDIDATE" "https://api.vercel.com/v2/user")
  if [ "$STATUS" = "200" ]; then
    VERCEL_TOKEN="$TOKEN_CANDIDATE"
  else
    echo "Token resolvido nao valida (HTTP $STATUS) — provavelmente expirado. Tentando proxima fonte..."
    VERCEL_TOKEN=""
  fi
fi
```

Se ainda vazio apos 4 tentativas: invocar `setup-agencia` com argumento `"so lp"` (que vai coletar e gravar em `.env.local`) e re-resolver. Se ainda falhar (usuario abortou), parar com mensagem clara: `Sem VERCEL_TOKEN valido — nao posso sincronizar sibling em modo guarda-chuva. Sem sync, deploy pode apagar vizinhas. Aborte ou rode setup-agencia.`

**Notas de bash cross-platform:**
- Usar `sed -n 's/.*"token"...//p' | head -1` em vez de Python pra extrair o token. Python da Microsoft Store no Windows roda em sandbox AppContainer e NAO consegue abrir paths absolutos em `AppData/Roaming/` (testado e confirmado em 2026-05-04 e 2026-05-07). bash via Git Bash tem acesso normal.
- A regex do `sed` e nao-greedy o suficiente porque `auth.json` tem `"token"` como primeira chave (apos as anotacoes `// Note` e `// Docs`). Se a estrutura mudar e `creator.uid` ou `userId` aparecer antes de `token`, o `sed` ainda pega o primeiro match correto pelo nome da chave.

**Por que API direto e nao MCP Vercel:** o MCP Vercel disponivel no Claude Code expoe `list_deployments` / `get_deployment` mas NAO os endpoints `/v6/deployments/{id}/files` (tree) nem `/v7/.../files/{uid}` (download de bytes). Pra sincronizar a sibling precisa ir na REST API direto.

#### 0.5.d.ii Pegar ultimo deploy production READY

Ler IDs do projeto a partir do `.vercel/project.json` que o 0.5.c garantiu existir:

```bash
# Path Windows-style pro Python (ver convencao Passo 0.3). Sem isso, no Windows o
# Python recebe /c/Users/... e da FileNotFoundError -> PROJECT_ID/ORG_ID vazios.
to_win_path() { cygpath -m "$1" 2>/dev/null || printf '%s' "$1" | sed -E 's#^/([a-zA-Z])/#\1:/#'; }
PROJECT_JSON_WIN="$(to_win_path "$SIBLING")/.vercel/project.json"
# Interpretador Python resiliente ao shim da Store no Windows (ver Passo 0.4). Single-token.
PYBIN=""; for _c in py python3 python; do command -v "$_c" >/dev/null 2>&1 && "$_c" -c '' >/dev/null 2>&1 && { PYBIN="$_c"; break; }; done; PYBIN="${PYBIN:-python}"

PROJECT_ID=$("$PYBIN" -c "import json; print(json.load(open(r'$PROJECT_JSON_WIN'))['projectId'])")
ORG_ID=$("$PYBIN" -c "import json; print(json.load(open(r'$PROJECT_JSON_WIN'))['orgId'])")

# Leitura falhou (path errado, json quebrado)? Abortar — sem IDs nao da pra sincronizar.
if [ -z "$PROJECT_ID" ] || [ -z "$ORG_ID" ]; then
  echo "ERRO: nao consegui ler projectId/orgId de $PROJECT_JSON_WIN."
  echo "  No Windows, confira que o path chegou Windows-style (C:/...), nao MSYS (/c/...)."
  exit 1
fi

RESPONSE=$(curl -s -H "Authorization: Bearer $VERCEL_TOKEN" \
  "https://api.vercel.com/v6/deployments?projectId=$PROJECT_ID&teamId=$ORG_ID&target=production&state=READY&limit=1")

# Distinguir 3 casos: erro de API (token sem read), sem deploys ainda, deploy encontrado
PARSED=$(echo "$RESPONSE" | "$PYBIN" -c "
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    print('ERR:invalid_json:resposta nao e JSON valido')
    sys.exit(0)
if 'error' in d:
    err = d['error']
    print('ERR:' + err.get('code', 'unknown') + ':' + err.get('message', ''))
elif d.get('deployments'):
    print('OK:' + d['deployments'][0]['uid'])
else:
    print('EMPTY:')
")

case "$PARSED" in
  ERR:forbidden:*|ERR:not_found:*)
    echo "ERRO: VERCEL_TOKEN nao tem permissao de read no projeto $PROJECT_ID."
    echo "  Causa: token foi gerado com escopo restrito, ou projeto nao esta na org $TEAM."
    echo "  Solucao: regere o token em https://vercel.com/account/tokens com escopo 'Full Account'"
    echo "  na org elife-group, ou rode '/setup-agencia so lp' para reconfigurar."
    echo "  Detalhe da API: ${PARSED#ERR:}"
    exit 1
    ;;
  ERR:*)
    echo "ERRO inesperado da API Vercel: ${PARSED#ERR:}. Aborte e investigue."
    exit 1
    ;;
  EMPTY:)
    echo "Nenhum deploy production READY ainda — pulando sync (projeto sem deploy anterior)."
    DEPLOY_ID=""
    ;;
  OK:*)
    DEPLOY_ID="${PARSED#OK:}"
    ;;
esac
```

**Por que distinguir os 3 casos:** antes da v3.3.0, qualquer falha caia silenciosamente no "projeto sem deploy anterior" — confundia debugging quando o problema real era token sem permissao de read. Agora forbidden/not_found abortam com mensagem acionavel, e EMPTY (caso legitimo de projeto recem-criado) segue normalmente.

Se `DEPLOY_ID` vazio (caso EMPTY): skip sync. Continuar para Passo 1 — o deploy desta sessao sera o primeiro do projeto.

#### 0.5.d.iii Baixar arquivos do deploy recursivamente

A API V6 retorna uma arvore de nos `{ name, type: "file" | "directory", uid, children?[] }`. Recursar ate folhas, baixar cada arquivo via V7.

A logica vive em `.claude/skills/lp-publicar/sync_sibling.py` (script Python helper). Invocar via env vars:

```bash
[ -n "$DEPLOY_ID" ] && {
  # sync_sibling.py ESCREVE arquivos em $SIBLING. No Windows, um path MSYS (/c/Users/...)
  # faz o Python escrever em C:\c\Users\... em silencio. Passar Windows-style (ver Passo 0.3).
  to_win_path() { cygpath -m "$1" 2>/dev/null || printf '%s' "$1" | sed -E 's#^/([a-zA-Z])/#\1:/#'; }
  SIBLING="$(to_win_path "$SIBLING")"
  # Interpretador Python resiliente ao shim da Store no Windows (ver Passo 0.4). Single-token.
  PYBIN=""; for _c in py python3 python; do command -v "$_c" >/dev/null 2>&1 && "$_c" -c '' >/dev/null 2>&1 && { PYBIN="$_c"; break; }; done; PYBIN="${PYBIN:-python}"
  export DEPLOY_ID ORG_ID VERCEL_TOKEN SIBLING
  "$PYBIN" "$(git rev-parse --show-toplevel)/.claude/skills/lp-publicar/sync_sibling.py" || {
    echo "ERRO: sync_sibling.py falhou. Aborte e investigue."
    exit 1
  }
}
```

**Por que script externo e nao heredoc inline:** heredoc tem 3 problemas combinados:
- Interpolacao de `$variable` quebra com paths que tem espaco/parenteses (windows usuario "Program Files (x86)" etc).
- Escape de backslash no Python heredoc fica fragil (`r"$SIBLING"` vira raw string com backslash literal em paths Windows).
- Heredoc redireciona stdin do Python — se quiser pipe `curl | python`, conflita com `<<EOF`.

Script externo isola tudo, le env vars com `os.environ`, e da pra testar isolado: `DEPLOY_ID=dpl_xxx ORG_ID=team_xxx VERCEL_TOKEN=xxx SIBLING=/tmp/test python sync_sibling.py`.

#### 0.5.d.iv Validacao pos-sync (presenca + integridade)

Dois checks independentes. Qualquer um que falhe → abortar.

**Check 1 — presenca:** confirmar que cada slug que responde 200 no dominio agora tem `{sibling}/{slug}/index.html`. Se algum esta faltando, sync nao foi completo (token sem read, bug no sync recursivo, etc.).

```bash
[ -n "$DEPLOY_ID" ] && {
  # Slugs com index.html na sibling apos sync
  SIBLING_SLUGS=$(find "$SIBLING" -mindepth 2 -maxdepth 2 -name "index.html" -type f 2>/dev/null | \
    awk -F/ '{print $(NF-1)}' | sort -u)

  # Slugs candidatos: marcas/slugs no repo
  REPO_SLUGS=$(find landing-pages -mindepth 3 -maxdepth 3 -name "index.html" -type f 2>/dev/null | \
    awk -F/ '{print $3}' | sort -u)

  # Slugs vivos no dominio (responde 200)
  MISSING=""
  for SLUG in $REPO_SLUGS; do
    [ "$SLUG" = "{slug}" ] && continue  # a LP nova nao precisa estar no live ainda
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://$DOMAIN/$SLUG" 2>/dev/null)
    if [ "$STATUS" = "200" ]; then
      echo "$SIBLING_SLUGS" | grep -q "^$SLUG$" || MISSING="$MISSING $SLUG"
    fi
  done

  if [ -n "$MISSING" ]; then
    echo "ERRO: Sync incompleto. Slugs vivos em $DOMAIN mas faltando na sibling:$MISSING"
    echo "Causas possiveis: VERCEL_TOKEN sem permissao de read, slug fora de landing-pages/{marca}/, ou bug no sync recursivo."
    echo "Aborte e investigue — deploy agora apagaria essas LPs."
    exit 1
  fi
}
```

**Check 2 — integridade:** confirmar que cada `index.html` na sibling pos-sync comeca com HTML valido (`<!doctype html>` ou `<html>`). JSON wrapper, pagina em branco ou outro lixo no live indica que o **ultimo deploy production esta corrompido** — propagar via lp-publicar republicaria o lixo em silencio.

**Por que este check existe (motivacao real, 2026-05-08):** o `sync_sibling.py` baixa o conteudo dos arquivos exatamente como esta no deploy. Se o deploy publicou `{"data":"<base64>"}` (cenario do incidente 2026-05-07 tarde 2 e do **re-incidente 2026-05-08** quando outra colaboradora rodou versao antiga do helper sem `base64.b64decode`), o sync traz esse JSON cru pra sibling local, sobrescrevendo versoes integras que existiam ali. Sem este check: baseline (2.4) captura hash do JSON wrapper, deploy publica, smoke test (3.4.b) confirma que live mantem o mesmo hash → bug propagado, skill reporta sucesso. O que evitou propagacao em 2026-05-08 foi intuicao do operador, nao a skill. Fechado em v3.3.1.

```bash
[ -n "$DEPLOY_ID" ] && {
  CORRUPTED=""
  for SLUG_DIR in "$SIBLING"/*/; do
    [ -d "$SLUG_DIR" ] || continue
    HTML="$SLUG_DIR/index.html"
    [ -f "$HTML" ] || continue
    # HTML valido comeca com <!doctype html> ou <html (case-insensitive, ignora whitespace inicial)
    if ! head -c 100 "$HTML" | tr 'A-Z' 'a-z' | grep -qE '^[[:space:]]*<(!doctype|html)'; then
      CORRUPTED="$CORRUPTED $(basename $SLUG_DIR)"
    fi
  done

  if [ -n "$CORRUPTED" ]; then
    echo "ERRO: Sync trouxe LP(s) corrompida(s) do live:$CORRUPTED"
    echo "Conteudo nao comeca com <!doctype html> nem <html — provavelmente JSON wrapper,"
    echo "pagina em branco ou outro lixo. Ultimo deploy production esta corrompido."
    echo ""
    echo "Causa-raiz tipica: outra maquina rodou versao antiga do sync_sibling.py"
    echo "(sem base64.b64decode) e propagou JSON cru como conteudo do index.html."
    echo ""
    echo "Recovery (NAO rode lp-publicar enquanto live estiver corrompido — propagaria o bug):"
    echo "1. Sua sibling local pre-sync foi sobrescrita por este sync. Veja se voce tem backup."
    echo "2. Se outra maquina (ex: do Victor) tem sibling com versoes integras das vizinhas, use ela."
    echo "3. Recovery manual: atualize so a LP nova/alterada na sibling integra, mantenha vizinhas,"
    echo "   deploy direto via 'cd \$SIBLING && npx vercel deploy --prod --yes --force --scope \$TEAM'."
    echo "4. Documente em landing-pages/CONTEXT.md §7.2."
    echo ""
    echo "Historico: ver §7.2 incidentes 2026-05-07 (tarde 2) e 2026-05-08."
    exit 1
  fi
}
```

**Falsos positivos previstos:** apenas `index.html` que comecam com BOM UTF-8 (`\xEF\xBB\xBF`) podem disparar o check. Se isso aparecer, ajustar o regex pra `^(\xEF\xBB\xBF)?[[:space:]]*<(!doctype|html)`. Em pratica, lp-gerar nunca gera BOM — entao falso positivo so apareceria se HTML viesse de outro pipeline.

#### 0.5.d.v Edge case: re-publicacao

Se `{slug}` (a LP que voce esta publicando) ja existe na sibling pos-sync, e re-publicacao (nao LP nova). **Nao** sobrescrever ainda — o **Passo 1.0** (drift-check) compara o conteudo do live com o que seu source local geraria, e pede confirmacao se divergir. Sem este check, alteracoes feitas por outra pessoa (deploy de outra maquina sem commit, hotfix manual no Vercel) seriam apagadas em silencio.

---

## Passo 1: Preparar Pasta Sibling

### Estrutura alvo (modo solo)

```
{sibling}/
├── {slug}/
│   └── index.html
├── assets/
│   └── logos/
│       ├── logo-primary.svg
│       └── logo-reversed.svg
├── vercel.json
├── .gitignore
└── README.md
```

### Estrutura alvo (modo guarda-chuva)

Sibling ja existe e ja tem LPs vizinhas. Voce **adiciona** sua LP como mais uma subpasta sem tocar nas outras.

```
{sibling}/
├── {outro-slug-1}/         ← LP existente (NAO TOCAR)
├── {outro-slug-2}/         ← LP existente (NAO TOCAR)
├── {slug}/                 ← LP que voce esta adicionando
│   └── index.html
├── assets/
│   ├── logos/              ← assets de marca legacy / da primeira LP do guarda-chuva (NAO TOCAR)
│   ├── {marca}/            ← seus assets (namespace por marca pra nao colidir com vizinhas)
│   │   └── ...
│   └── ...
├── vercel.json             ← NAO sobrescrever (ja configurado para multi-LP)
├── .gitignore
└── README.md               ← anexar nova LP a tabela existente
```

### 1.0 Drift-check pre-overwrite

**Quando rodar:** apos sync (0.5.d), antes de qualquer copia source → sibling. Pular se 0.5.d foi pulado (solo primeira publicacao) ou se `DEPLOY_ID` ficou vazio (caso EMPTY).

**O que protege:** se outra pessoa publicou esta LP de outra maquina sem commitar (ou aplicou hotfix manual via Vercel UI), o source local pode estar stale. Sem este check, Passo 1.2 sobrescreve o trabalho dela em silencio. Buraco fechado em v3.3.0.

**Logica:**

```bash
# So roda se sync trouxe a LP atual do live para a sibling
if [ -f "$SIBLING/{slug}/index.html" ] && [ -n "$DEPLOY_ID" ]; then
  # 1. Copiar source para temp e simular reescrita do Passo 1.5 antes de comparar.
  #    Hash bruto sempre divergiria — source tem '../../brand/...', live tem '/assets/...'.
  TEMP_HTML=$(mktemp --suffix=.html 2>/dev/null || mktemp -t drift.html)
  cp "landing-pages/{marca}/{slug}/index.html" "$TEMP_HTML"

  if [ "$MODE" = "guarda-chuva" ]; then
    sed -i.bak "s|\.\./\.\./brand/{marca}/assets/|/assets/{marca}/|g; s|\./assets/|/assets/{marca}/|g" "$TEMP_HTML"
  else
    sed -i.bak "s|\.\./\.\./brand/{marca}/assets/|/assets/|g; s|\./assets/|/assets/|g" "$TEMP_HTML"
  fi
  rm -f "$TEMP_HTML.bak"

  # 2. Hash dos dois (normalizando \r de line-ending Windows pra evitar falso-positivo)
  EXPECTED=$(tr -d '\r' < "$TEMP_HTML" | md5sum | awk '{print $1}')
  LIVE=$(tr -d '\r' < "$SIBLING/{slug}/index.html" | md5sum | awk '{print $1}')

  if [ "$EXPECTED" != "$LIVE" ]; then
    echo "AVISO: a versao de '{slug}' no Vercel NAO bate com o que seu source local geraria."
    echo "  Hash esperado (do source local + reescrita):  $EXPECTED"
    echo "  Hash do live (sincronizado agora):            $LIVE"
    echo ""
    echo "Possiveis causas:"
    echo "  - Outra pessoa publicou de outra maquina sem commitar."
    echo "  - Hotfix manual aplicado fora deste fluxo."
    echo "  - Seu git esta desatualizado (rode: git pull --rebase)."
    echo ""
    echo "Para diff detalhado antes de decidir:"
    echo "  diff '$TEMP_HTML' '$SIBLING/{slug}/index.html'"
    # Mantem $TEMP_HTML para o usuario inspecionar — limpar depois da decisao
  else
    rm -f "$TEMP_HTML"
  fi
fi
```

**Se hashes divergirem:** pare e pergunte ao usuario via `AskUserQuestion` com 3 opcoes (NAO seguir adiante por conta propria — esta e uma decisao de quem opera):

| Opcao | Acao |
|---|---|
| **Continuar — sobrescrever live com meu source** | Aceita o risco, segue para Passo 1.1. Limpar `$TEMP_HTML`. Logar a decisao. |
| **Abortar — vou investigar o diff** | Parar a skill. Mostrar comando `diff` no relatorio final. NAO limpar `$TEMP_HTML` para o usuario inspecionar. |
| **Pull primeiro — rode `git pull --rebase` e me chame de novo** | Parar a skill. Limpar `$TEMP_HTML`. Mensagem final: "Rode `git pull --rebase` na raiz do repo, confira se a LP foi atualizada por colega, depois rode `/lp-publicar` de novo." |

**Por que comparar hash normalizado e nao diff completo inline:** mostrar diff inline polui o contexto e o usuario nao consegue ler bem em multiplos resultados. Hash + comando para diff manual mantem ruido baixo e da controle.

**Falsos positivos previstos:** mtime de `$TEMP_HTML` afetando hash NAO é problema — md5 calcula sobre conteudo, nao metadata. Line-ending `\r\n` (Windows) vs `\n` (Linux) NAO é problema — o `tr -d '\r'` normaliza ambos antes do hash. Se mesmo assim aparecer drift inesperado em re-publicacao logo apos publicacao bem-sucedida da mesma maquina, investigar (pode ser bug na reescrita do Passo 1.5).

### 1.1 Criar pasta da LP

```bash
mkdir -p "{sibling}/{slug}"
mkdir -p "{sibling}/assets"
```

No modo guarda-chuva, **assert** que `{sibling}` ja existe (com `.vercel/project.json` la dentro). Se nao existe quando esperado, abortar — significa que a deteccao do Passo 0.5 retornou um nome de projeto sem sibling local correspondente. Caso: rodar `npx vercel link --yes --project={nome} --cwd={sibling-path}` para popular `{sibling}/.vercel/`.

### 1.2 Copiar index.html

```bash
cp "landing-pages/{marca}/{slug}/index.html" "{sibling}/{slug}/index.html"
```

### 1.3 Descobrir assets referenciados

Grep `src=`, `srcset=`, `href=` e `url(` no index.html fonte. Para cada referência, classificar pela origem do path **e o modo da skill**:

#### Modo solo

| Padrão no source | Vem do disco em | Vai para no deploy |
|---|---|---|
| `../../brand/{marca}/assets/X` | `brand/{marca}/assets/X` | `/assets/X` |
| `./assets/X` | `landing-pages/{marca}/{slug}/assets/X` | `/assets/X` |
| `/assets/X` (já absoluto) | checar `brand/{marca}/assets/X` primeiro, senão `landing-pages/{marca}/{slug}/assets/X` | `/assets/X` |

#### Modo guarda-chuva (namespace de marca obrigatorio)

| Padrão no source | Vem do disco em | Vai para no deploy |
|---|---|---|
| `../../brand/{marca}/assets/X` | `brand/{marca}/assets/X` | `/assets/{marca}/X` |
| `./assets/X` | `landing-pages/{marca}/{slug}/assets/X` | `/assets/{marca}/X` |
| `/assets/{marca}/X` (já absoluto e namespaceado) | `brand/{marca}/assets/X` ou `landing-pages/{marca}/{slug}/assets/X` | `/assets/{marca}/X` |

**Por que namespace por marca em guarda-chuva:** sem namespace, dois assets com o mesmo filename (ex: Buzzmonitor `logo-icon.png` e Buzzcreators `logo-icon.png`) colidem em `{sibling}/assets/logos/logo-icon.png` — sobrescrever quebra a LP vizinha.

**Detecção de colisão (modo guarda-chuva):** antes de copiar, comparar md5 do source com `{sibling}/assets/{nome-base}/{filename}` se existir. Se filename identico mas md5 diferente, abortar com erro claro: `asset {filename} colide com vizinha em {sibling-asset-path} (md5 diferente). Use namespace por marca.` (Em pratica isso nunca dispara se a regra acima for respeitada — o trigger e seguranca contra erro de skill futuro.)

**Padrao bare `assets/X` (sem `./`) — v3.8.0:** alguns HTMLs referenciam asset LP-local como `src="assets/X"`, sem o prefixo `./` (precedente real: `conheca-a-cxpress`, `src="assets/enrico-chiari.jpg"`). Tratar EXATAMENTE como `./assets/X` em toda a cadeia: descoberta (1.3), copia (1.4), rewrite (1.5) e simulacao do drift-check (1.0). Dois cuidados: (a) **ordem do sed** — substituir o padrao brand (`../../brand/...`) ANTES do bare, porque o path brand contem a substring `assets/` e um replace global ingenuo o corromperia; ancorar o bare em `src="assets/` (ou `href="assets/`) em vez de `assets/` solto; (b) **namespace por slug** — em guarda-chuva, LP-local bare pode ja estar publicado como `/assets/{marca}/{slug}/X` (caso `conheca-a-cxpress` → `/assets/cxpress/conheca-a-cxpress/enrico-chiari.jpg`) para evitar colisao entre LPs irmas da mesma marca; ao re-publicar, conferir com grep no HTML sincronizado do live qual namespace esta em uso e manter.

Produzir lista de triplas: `(path-no-source, disco-origem, alvo-no-sibling-com-modo)`.

### 1.4 Copiar **apenas** esses assets

Para cada tripla, copiar `disco-origem` para `{sibling}/assets/...` preservando subcaminho. No modo guarda-chuva, prefixar com `{marca}/`.

Se `disco-origem` não existe, PARE com erro: `asset referenciado em linha {N} mas arquivo não encontrado nem em brand/ nem em landing-pages/{marca}/{slug}/assets/`.

**Não** usar `cp -r brand/{marca}/` cego — copiaria assets não-usados.

### 1.4.1 Caso especial: OG image (v3.6.0, GUIDELINES §18)

`og-image.png` (LP-local em `landing-pages/{marca}/{slug}/assets/og-image.png`) **NAO** segue a heuristica de grep do 1.3 — ela e referenciada via URL absoluta no `<meta property="og:image" content="https://...">`, nao via `src`/`href` relativo. Tratar manualmente:

| Modo | Source | Destino na sibling | Renomear? |
|---|---|---|---|
| **solo** | `landing-pages/{marca}/{slug}/assets/og-image.png` | `{sibling}/assets/og-image.png` | nao (nome unico no projeto solo) |
| **guarda-chuva** | `landing-pages/{marca}/{slug}/assets/og-image.png` | `{sibling}/assets/{marca}/og-{slug}.png` | **sim** — sufixo de slug evita colisao com LPs irmas |

```bash
SRC_OG="landing-pages/{marca}/{slug}/assets/og-image.png"
if [ -f "$SRC_OG" ]; then
  if [ "$MODE" = "guarda-chuva" ]; then
    DST_OG="{sibling}/assets/{marca}/og-{slug}.png"
  else
    DST_OG="{sibling}/assets/og-image.png"
  fi
  mkdir -p "$(dirname "$DST_OG")"
  cp "$SRC_OG" "$DST_OG"
fi
```

**Logo PNG da marca (para JSON-LD)**: alem dos SVGs ja copiados via grep do 1.4, garantir que `logo-primary.png` tambem esta na sibling — JSON-LD `Organization.logo` aponta para esse arquivo via URL absoluta, e a heuristica do grep nao pega (referencia esta dentro de `<script type="application/ld+json">`, nao em atributo). Mesma logica de namespace:

| Modo | Source | Destino |
|---|---|---|
| **solo** | `brand/{marca}/assets/logos/logo-primary.png` | `{sibling}/assets/logos/logo-primary.png` |
| **guarda-chuva** | `brand/{marca}/assets/logos/logo-primary.png` | `{sibling}/assets/{marca}/logos/logo-primary.png` |

**Historico:** 2026-05-18 (sessao MCP) — JSON-LD novo referenciou `logo-primary.png` mas o sync trouxe apenas o `.svg` (do live anterior, sem JSON-LD). Resultado: `Organization.logo` apontava pra URL com 404 ate copiar manualmente. Convencao agora explicita.

### 1.5 Reescrever paths no HTML copiado

No `{sibling}/{slug}/index.html`, substituir todos para absoluto:

#### Modo solo

- `../../brand/{marca}/assets/` → `/assets/`
- `./assets/` → `/assets/`

#### Modo guarda-chuva

- `../../brand/{marca}/assets/` → `/assets/{marca}/`
- `./assets/` → `/assets/{marca}/`
- `src="assets/` (bare, sem `./`) → `src="/assets/{marca}/X` ou `src="/assets/{marca}/{slug}/X` conforme namespace vigente no live (ver nota do 1.3; substituir DEPOIS do padrao brand)
- (`/assets/{marca}/X` ja absoluto: nao reescreve)

Use `Edit` com `replace_all: true`.

#### Substituir placeholders SEO (v3.6.0)

`lp-gerar` produz HTML com placeholders absolutos para URLs SEO que so podem ser resolvidos no momento do deploy (porque dependem do `{dominio}`):

| Placeholder | Substituir por (solo) | Substituir por (guarda-chuva) |
|---|---|---|
| `{{DOMAIN}}` | `{dominio}` (ou `.vercel.app` se solo sem dominio) | `{dominio}` |
| `{{OG_IMAGE_PATH}}` | `assets/og-image.png` | `assets/{marca}/og-{slug}.png` |
| `{{BRAND_LOGO_PNG_PATH}}` | `assets/logos/logo-primary.png` | `assets/{marca}/logos/logo-primary.png` |

```bash
# Resolver dominio (em batch, todas as LPs compartilham o mesmo dominio do guarda-chuva)
EFFECTIVE_DOMAIN="$dominio"
[ -z "$EFFECTIVE_DOMAIN" ] && EFFECTIVE_DOMAIN="$VERCEL_FALLBACK_DOMAIN"  # vindo do output do deploy em solo

# Substituir
if [ "$MODE" = "guarda-chuva" ]; then
  OG_PATH="assets/{marca}/og-{slug}.png"
  LOGO_PATH="assets/{marca}/logos/logo-primary.png"
else
  OG_PATH="assets/og-image.png"
  LOGO_PATH="assets/logos/logo-primary.png"
fi

sed -i \
  -e "s|{{DOMAIN}}|$EFFECTIVE_DOMAIN|g" \
  -e "s|{{OG_IMAGE_PATH}}|$OG_PATH|g" \
  -e "s|{{BRAND_LOGO_PNG_PATH}}|$LOGO_PATH|g" \
  "{sibling}/{slug}/index.html"
```

**Verificacao obrigatoria pos-substituicao:**

```bash
grep -nE '\{\{(DOMAIN|OG_IMAGE_PATH|BRAND_LOGO_PNG_PATH|[A-Z_]+)\}\}' "{sibling}/{slug}/index.html" && echo "PLACEHOLDER NAO RESOLVIDO"
```

Se aparecer qualquer placeholder `{{...}}` sobrando, PARE — alguem (lp-gerar futuro ou hotfix manual) adicionou placeholder novo nao previsto aqui. Adicionar ao mapeamento acima ou tratar manualmente.

**Verificação obrigatória pós-rewrite** — grep no HTML do sibling:

```bash
grep -nE "\\.\\./assets/|\\./assets/|\\.\\./\\.\\./brand/" "{sibling}/{slug}/index.html" && echo "VAZOU"
```

Se aparecer qualquer match, PARE — o rewrite não cobriu todos os casos. Caminho relativo + `cleanUrls: true` + `trailingSlash: false` resolve `./assets/X` para `/assets/X` na raiz do site (não para a pasta da LP), então qualquer `./` ou `../` sobrando vai 404 no live.

**Incidentes documentados:**
- 2026-04-27 (mascot 404): `mascot.png` da Buzzmonitor LP `monitoramento-concorrentes-maio-2026` deu 404 por dois deploys consecutivos com asset LP-local não copiado e path relativo intacto. Motivou §1.3-1.5 (v1.4.0) suportar `./assets/`.
- 2026-04-27 (multi-LP guarda-chuva): LP Buzzcreators `vendendo-com-creators` foi inicialmente publicada em projeto Vercel separado em vez de usar o guarda-chuva ja existente para `webinar.buzzmonitor.com`. Consolidacao manual + dois deploys. Motivou Passo 0.5 + namespace por marca (v1.5.0).

Remover também do `<title>` qualquer sufixo de trabalho: `[REVISADO]`, `[TESTE]`, `[DRAFT]`.

### 1.6 Escrever vercel.json

**Modo solo:** copiar `.claude/skills/lp-publicar/vercel.template.json` para `{sibling}/vercel.json` **sem modificacao**.

**Modo guarda-chuva:** **NAO sobrescrever** o `{sibling}/vercel.json` existente. Ele ja foi configurado para servir multi-LP. Em vez disso, rodar **drift-check ativo de CSP** comparando com o template:

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
# Paths Windows-style pro Python (ver Passo 0.3): csp_drift_check.py abre os dois arquivos.
to_win_path() { cygpath -m "$1" 2>/dev/null || printf '%s' "$1" | sed -E 's#^/([a-zA-Z])/#\1:/#'; }
# Interpretador Python resiliente ao shim da Store no Windows (ver Passo 0.4). Single-token.
PYBIN=""; for _c in py python3 python; do command -v "$_c" >/dev/null 2>&1 && "$_c" -c '' >/dev/null 2>&1 && { PYBIN="$_c"; break; }; done; PYBIN="${PYBIN:-python}"
SIBLING_VERCEL_JSON="$(to_win_path "{sibling}/vercel.json")" \
  TEMPLATE_VERCEL_JSON="$(to_win_path "$REPO_ROOT/.claude/skills/lp-publicar/vercel.template.json")" \
  "$PYBIN" "$REPO_ROOT/.claude/skills/lp-publicar/csp_drift_check.py"
```

Saidas possiveis:

| Exit | Significado | Acao |
|---|---|---|
| 0 | CSP do sibling cobre todos os dominios do template | Continuar (modo guarda-chuva nao mexe em vercel.json) |
| 1 | DRIFT — template tem dominio que sibling nao tem | Decidir entre patch automatico (default) ou pausa, ver logica abaixo |
| 2 | Erro de leitura, parsing ou env var faltando | Abortar e investigar |

**Quando exit 1 (drift detectado):** o stdout do helper traz JSON com `missing_in_sibling` (dominios novos no template ausentes no sibling — drift que precisa de patch) e `extra_in_sibling` (customizacoes do sibling que NAO estao no template — preservar se o operador escolher patch). A acao depende de `extra_in_sibling`:

**Caso 1 — `extra_in_sibling == {}` (sem customizacoes divergentes, caso comum):** patch automatico sem perguntar.

1. Reportar ao usuario em uma frase o que vai ser adicionado (lista compacta de `missing_in_sibling`).
2. Substituir o valor inteiro do `Content-Security-Policy` em `{sibling}/vercel.json` pelo do template via `Edit replace_all: false` cirurgico (1 troca atomica do CSP completo). Preserva `redirects`, `$schema`, `cleanUrls`, `trailingSlash` e os outros 6 headers porque a troca afeta apenas o valor do CSP.
3. Re-rodar o drift-check pos-patch — esperar exit 0. Se nao zerar, abortar.
4. Logar a acao no relatorio Notion (Passo 6) em "Mudancas desta entrega".

**Caso 2 — `extra_in_sibling != {}` (sibling tem dominios custom fora do template):** NAO decidir por conta. Pausar via `AskUserQuestion` mostrando `missing_in_sibling` E `extra_in_sibling`, com 3 opcoes:

| Opcao | Acao |
|---|---|
| **Patch CSP preservando customizacoes (Recomendado)** | Reescrever CSP combinando template + `extra_in_sibling` (concatenar dominios custom de volta as directives correspondentes). Re-rodar drift-check pos-patch. |
| **Deixar como esta — anotar em pendencias** | Continua o deploy sem alterar CSP. Anota em "Pendencias" do relatorio Notion. |
| **Abortar e investigar manualmente** | Para a skill. |

**Por que automatizar Caso 1:** o cenario `extra_in_sibling == {}` significa que o sibling esta apenas atrasado em relacao ao template — nao ha decisao real ali, so trabalho de copia. Antes da v3.5.0 a skill perguntava sempre, e o operador respondia sempre "patch recomendado" porque era o unico caminho que destravava o pixel sem perder customizacoes (que nao existem nesse caso). Cada deploy guarda-chuva em sibling defasado pagava o custo de uma pergunta extra. Mantemos `AskUserQuestion` apenas quando ha decisao real a tomar (`extra_in_sibling != {}` — risco de remover dominio custom do sibling sem querer).

**Por que existe esse drift-check (motivacao real, 2026-05-08):** apos v3.2.0 atualizar o template para liberar Meta Pixel via Facebook, apenas o sibling guarda-chuva redeployado em seguida (`cxpress-lp-playbook-whatsapp2026`) recebeu o patch. Os 3 outros guarda-chuvas Buzzmonitor (`webinar.*`, `evento.*`, `material.*`) continuaram com CSP antigo bloqueando o pixel em runtime — `Refused to load https://connect.facebook.net` no DevTools. O `diff` generico que existia antes flagava a divergencia, mas o operador podia nao notar (CR/LF + multiplas linhas) e o problema ficou silencioso por dias ate alguem reportar. v3.4.0 fechou o gap com helper programatico + pausa via AskUserQuestion. v3.5.0 reduziu friccao quando nao ha decisao real a tomar (`extra_in_sibling == {}`).

O template inclui 7 headers de seguranca, incluindo **Content-Security-Policy (CSP)** ja configurado para permitir os provedores de form mais comuns (Jotform, RD Station, HubSpot), Google Fonts, analytics (GA, GTM), video (YouTube, Vimeo), **Meta Pixel via GTM** (`connect.facebook.net` em `script-src`/`connect-src`; `www.facebook.com` em `connect-src`/`frame-src` — desde v3.2.0) e **TikTok Pixel via GTM** (`analytics.tiktok.com` em `script-src`/`connect-src`; `ads.tiktok.com` em `connect-src` — desde v3.7.0).

**Quando ajustar o CSP:**
- LP usa provedor de form fora do default (ex: Typeform, Tally, Formspree) → adicionar dominio em `script-src`, `frame-src` e `form-action`.
- LP carrega script de terceiro nao listado (pixel de conversao custom, chatbot, etc.) → adicionar em `script-src` e `connect-src`.
- LP embeda iframe de outro servico → adicionar em `frame-src`.

Faca essa decisao **antes** do deploy grep-ando scripts e iframes no HTML:

```bash
grep -oiE "src=\"https?://[^\"]+\"|<iframe[^>]*src=\"[^\"]+\"" "{sibling}/{slug}/index.html" | sort -u
```

**Check proativo Meta Pixel (GTM dispara o pixel mesmo sem snippet inline na LP):**

```bash
grep -oE "fbq\(|connect\.facebook\.net|fbevents\.js|www\.facebook\.com/tr" "{sibling}/{slug}/index.html"
```

Se houver match, validar que o CSP cobre `connect.facebook.net` (script + connect) e `www.facebook.com` (connect + frame). Coberto por padrao desde o template v3.2.0 — se voce esta editando o sibling em modo guarda-chuva e ele ainda esta no CSP antigo (pre-v3.2.0), adicione manualmente.

**Check proativo TikTok Pixel (mesma logica do Meta — GTM dispara mesmo sem snippet inline):**

```bash
grep -oE "ttq\(|ttq\.|analytics\.tiktok\.com|tiktok-pixel" "{sibling}/{slug}/index.html"
```

Se houver match, validar que o CSP cobre `analytics.tiktok.com` (script + connect) e `ads.tiktok.com` (connect). Coberto por padrao desde o template v3.7.0 — em sibling de guarda-chuva pre-v3.7.0, o drift-check do 1.6 ja patcha automaticamente quando `extra_in_sibling == {}`.

Se algum dominio nao estiver coberto pelo CSP default, edite `{sibling}/vercel.json` antes de deployar. Nao use `*` permissivo — quebra o sentido do header.

### 1.7 Escrever .gitignore

```
.vercel/
node_modules/
.DS_Store
```

### 1.8 Escrever README.md da sibling

**Modo solo:** criar README do zero.

```markdown
# {Marca} — LP {slug}

Artefato **publicado** da LP.

## Fonte-verdade

A fonte editavel vive no repo do agente inhouse:

```
Agente Inhouse/landing-pages/{marca}/{slug}/
```

Esta pasta e apenas o artefato de deploy — isolada do repo interno. Para atualizar: rodar `/lp-publicar {marca} {slug}` no repo do agente.

## Deploy

`npx vercel deploy --prod --yes` desta pasta.
```

**Modo guarda-chuva:** README ja existe (formato multi-LP). **Nao sobrescrever.** Em vez disso, ler o README existente e anexar a LP nova a tabela "LPs ativas" (se houver) ou em uma secao similar. Modelo:

```markdown
| Path | Marca | Fonte no repo |
|---|---|---|
| `/{slug-existente-1}` | {marca-1} | `Agente Inhouse/landing-pages/{marca-1}/{slug-existente-1}/` |
| `/{slug}` | **{Marca-da-nova} (novo)** | `Agente Inhouse/landing-pages/{marca}/{slug}/` |
```

Se o README do sibling nao seguir formato tabular, escolher: ou apenas anexar uma linha "Adicionada {marca}/{slug} em YYYY-MM-DD" ao final, ou regenerar o README inteiro pra padronizar. Nao decidir silenciosamente — perguntar ao usuario se o README precisa ser regenerado.

## Passo 2: Validacao de Isolamento (pre-deploy)

**Antes** de chamar `vercel deploy`, rode **3 checks** na pasta sibling. Qualquer um que retorne hit → PARE e avise o usuario. Nao deployar.

### 2.1 Paths/nomes sensíveis (estrutura)

```bash
grep -ril "meta-ads\|\.env\|conhecimento/\|\.claude/" "{sibling}/" || true
```

### 2.2 Diretorios do repo interno na raiz da sibling

```bash
ls "{sibling}/" | grep -E "^(meta-ads|conhecimento|brand|\.claude|\.env)$" && echo "VAZOU"
```

### 2.3 Strings sensíveis no conteudo (tokens, segredos)

Grep procura por padroes de credencial que nao deveriam estar num HTML/JS publico:

```bash
grep -rEil "VERCEL_TOKEN|META_ACCESS_TOKEN|FB_ACCESS_TOKEN|api[_-]?key[\"'=: ]|secret[\"'=: ]|bearer [A-Za-z0-9_-]{20,}|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY" "{sibling}/" || true
```

Exceções legítimas: nada. Se um provedor de form usa uma public key/publishable key, documentar como falso-positivo conhecido antes de prosseguir — nunca silenciar o check globalmente.

Se qualquer um dos 3 retornar hit, PARE. Corrija a origem (lp-gerar, sync) e rode de novo. Nao deployar com vazamento.

### 2.4 Baseline de hashes das LPs vizinhas (modo guarda-chuva)

Pular esta validacao em modo solo.

No modo guarda-chuva, capturar hash MD5 do `index.html` de **cada outra LP** do sibling **antes** do deploy. Esses hashes sao o baseline para o smoke test do Passo 3.4 — qualquer divergencia depois do deploy = regressao.

**Pos-Passo 0.5.d (v3.1.0):** a sibling agora sempre reflete o live antes deste passo (sync via Vercel API). Antes da v3.1.0, primeira execucao numa maquina nova podia capturar baseline vazio (sibling sem vizinhas), o que ocultava regressoes. Se mesmo assim o baseline ficar vazio aqui, e porque: (a) projeto guarda-chuva nunca teve deploy anterior — caso legitimo, OK seguir; (b) sync do 0.5.d falhou silenciosamente — investigar antes de prosseguir.

**Vizinha que e SOURCE de redirect (v3.9.0):** se um slug vizinho aparece como `source` em `redirects` no `{sibling}/vercel.json`, o live serve **3xx** (nao o `index.html` que existe na pasta). Comparar hash de conteudo daria **falso "REGRESSAO"** em todo deploy — o smoke test do 3.4.b usa `curl` sem `-L`, entao captura o corpo do 308, que nunca bate com o hash do arquivo. Essas vizinhas vao para uma lista separada (`REDIRECT_OTHERS`, formato `slug:destino`) e sao validadas por `Location` no 3.4.b, nao por hash. Incidente motivador 2026-06-16 (§7.2).

```bash
# Path Windows-style pro Python (ver Passo 0.3) — sem isso, no Windows o Python recebe
# /c/Users/... e da FileNotFoundError; REDIRECT_MAP ficaria vazio e as vizinhas-source-de-
# redirect cairiam no baseline-por-hash -> FALSO POSITIVO de "REGRESSAO" no smoke test 3.4.b.
to_win_path() { cygpath -m "$1" 2>/dev/null || printf '%s' "$1" | sed -E 's#^/([a-zA-Z])/#\1:/#'; }
VERCEL_JSON_WIN="$(to_win_path "{sibling}/vercel.json")"
# Interpretador Python resiliente ao shim da Store no Windows (ver Passo 0.4). Single-token.
PYBIN=""; for _c in py python3 python; do command -v "$_c" >/dev/null 2>&1 && "$_c" -c '' >/dev/null 2>&1 && { PYBIN="$_c"; break; }; done; PYBIN="${PYBIN:-python}"

# Sonda de leitura: quantos redirects o vercel.json declara? NAO suprimir stderr — um erro
# de leitura precisa aparecer (era o 2>/dev/null que mascarava a falha em 2026-06-30).
REDIRECT_COUNT=$("$PYBIN" -c "import json; print(len(json.load(open(r'$VERCEL_JSON_WIN', encoding='utf-8')).get('redirects', [])))")
if ! printf '%s' "$REDIRECT_COUNT" | grep -qE '^[0-9]+$'; then
  echo "ERRO: nao consegui ler 'redirects' de $VERCEL_JSON_WIN (saida: '$REDIRECT_COUNT')."
  echo "  Causa provavel no Windows: path MSYS (/c/...) passado ao Python do Windows (ver Passo 0.3)."
  echo "  Abortar — seguir geraria falso positivo de regressao no smoke test 3.4.b."
  exit 1
fi

# Mapa de redirects: "source-sem-barra<TAB>destino-com-barra" (sem 2>/dev/null, de proposito).
REDIRECT_MAP=$("$PYBIN" -c "
import json
d = json.load(open(r'$VERCEL_JSON_WIN', encoding='utf-8'))
for r in d.get('redirects', []):
    s = (r.get('source') or '').strip('/'); dest = r.get('destination') or ''
    if s: print(s + '\t' + dest)
")

# Sanity: declara redirects mas o mapa saiu vazio? Leitura inconsistente -> abortar (sem isso,
# vizinhas-source-de-redirect cairiam no baseline-por-hash e o 3.4.b daria falso "REGRESSAO").
if [ "$REDIRECT_COUNT" -gt 0 ] && [ -z "$REDIRECT_MAP" ]; then
  echo "ERRO: vercel.json declara $REDIRECT_COUNT redirect(s) mas REDIRECT_MAP ficou vazio."
  echo "  Investigar a leitura do vercel.json antes de prosseguir."
  exit 1
fi

for OTHER_DIR in "{sibling}"/*/; do
  OTHER_SLUG=$(basename "$OTHER_DIR")
  # Em batch, trocar este teste por: "pular se OTHER_SLUG esta em $SLUGS"
  [ "$OTHER_SLUG" = "{slug}" ] && continue
  # E source de redirect? Guarda o destino (validado por Location no 3.4.b), nao o hash.
  DEST=$(printf '%s\n' "$REDIRECT_MAP" | awk -F'\t' -v s="$OTHER_SLUG" '$1==s{print $2; exit}')
  if [ -n "$DEST" ]; then
    echo "baseline-redirect /$OTHER_SLUG -> $DEST"   # -> REDIRECT_OTHERS  (slug:destino)
  elif [ -f "$OTHER_DIR/index.html" ]; then
    OTHER_HASH=$(md5sum "$OTHER_DIR/index.html" | awk '{print $1}')
    echo "baseline /$OTHER_SLUG: $OTHER_HASH"         # -> BASELINES_OTHERS (slug:hash)
  fi
done
```

Guardar `BASELINES_OTHERS` (lista `(slug, hash)`) **e** `REDIRECT_OTHERS` (lista `(slug, destino)`) para usar em 3.4.

Excecoes legitimas: nada. Se voce **intencionalmente** mudou outra LP do sibling neste deploy (ex: refatorou asset compartilhado), abortar e usar `/lp-publicar` separado para cada LP afetada — nao misturar entregas no mesmo deploy.

## Passo 3: Deploy

### 3.1 Baseline antes do deploy

Capture o hash do HTML que voce **quer** publicar. Ele e o ground-truth para validar depois se a live bate com o que voce subiu.

```bash
LOCAL_HASH=$(md5sum "{sibling}/{slug}/index.html" | awk '{print $1}')
LOCAL_MTIME=$(stat -c "%Y" "{sibling}/{slug}/index.html")
echo "local: $LOCAL_HASH (mtime $LOCAL_MTIME)"
```

Se `{sibling}/.vercel/project.json` existe, leia `projectId` e `orgId` dele — sao uteis no fallback do 3.3.

### 3.2 Rodar deploy

LP e site estatico (sem build step real) — use `--force` por padrao. Ele ignora cache de build server-side, o que evita o caso de a Vercel reusar um build anterior quando so os assets mudaram. Custo: zero (build estatico completa em <100ms).

```bash
cd "{sibling}" && npx --yes vercel deploy --prod --yes --force
```

**Rodar sempre em background** (`run_in_background: true` no Bash tool) com timeout >= 240s. O upload inicial costuma dedup 90%+ via content-hash (Vercel reconhece assets ja subidos em deploys anteriores), entao o passo demorado costuma ser o `Building...` e o alias swap, nao o upload.

Capturar do stdout final, que tem este formato quando sucesso:

```
Production: https://{hash}.vercel.app [Ns]
Aliased: https://{dominio} [Ns]
{ "status": "ok", "deployment": { "id": "dpl_...", ... } }
```

- URL provisoria: linha `Production: ...`
- Deploy ID: campo `deployment.id` do JSON final
- Alias confirmado: linha `Aliased: ...` (so aparece se o projeto ja tem alias configurado)

Se primeiro deploy do projeto, o comando pede confirmacao de projeto — passar `--name {marca}-lp-{slug}` na primeira vez e deixar o CLI salvar `.vercel/project.json`.

### 3.3 Se a CLI falhar — checar API antes de retry

A CLI da Vercel tem um bug intermitente onde o upload sobe corretamente, o deploy fica **READY server-side**, mas a CLI nao recebe a resposta final e aborta com:

```
FetchError: invalid json response body at https://api.vercel.com/v2/files?teamId=... reason: Unexpected end of JSON input
```

**Nao faca retry cego.** Em vez disso, consulte o estado real via CLI (cross-platform, sem precisar de token na shell):

```bash
# Lista o deployment production mais recente do projeto.
# Output JSON inclui state, createdAt, url, etc.
cd "{sibling}" && npx --yes vercel ls --prod --scope "$TEAM" --json 2>&1 | head -50
```

Alternativa via MCP Vercel (se MCP estiver registrado no Claude Code):

```
mcp__{vercel-mcp}__list_deployments
  projectId: <projectId de .vercel/project.json>
  teamId:    <orgId>
```

O deployment mais recente tem `createdAt` em ms-epoch (ou ISO). Se ele foi criado **nos ultimos ~120s** e `state == "READY"` e `target == "production"`, o deploy passou — ignore o erro da CLI e siga para 3.4 com esse `deployment.id`.

Caso contrario (mais antigo, ou state != READY), re-rode o comando do 3.2 **com o sibling igualzinho** — nao edite nada entre tentativas, senao voce arrisca publicar versao intermediaria como aconteceu na entrega de 2026-04-20.

### 3.4 Verificar que a live tem o conteudo certo

#### 3.4.a LP nova (sempre)

O teste de fumaca mais confiavel e comparar hash local com ETag/MD5 do HTML servido:

```bash
LIVE_URL="https://{dominio-ou-vercel-app}/{slug}"
LIVE_HASH=$(curl -s "$LIVE_URL" | md5sum | awk '{print $1}')
echo "local: $LOCAL_HASH"
echo "live:  $LIVE_HASH"
```

- **Hashes iguais:** perfeito, siga para 3.4.b (se aplicavel) ou Passo 4.
- **Hashes diferentes + headers mostram `X-Vercel-Cache: HIT` com `Age` alto:** cache de borda ainda nao rotacionou. Aguarde 60s e re-teste. Se persistir > 3 min, deploy falhou silenciosamente (3.3 acertou mas o alias nao mudou) — re-rode 3.2 com `--force`.
- **Hashes diferentes + `X-Vercel-Cache: MISS`:** a live serve um build antigo. Re-rode 3.2 com `--force`. Nao publique relatorio enquanto nao bater.

#### 3.4.b Vizinhas intactas (modo guarda-chuva)

Pular em modo solo.

**Vizinhas de conteudo** — para cada `(slug, hash)` em `BASELINES_OTHERS` (capturado em 2.4), comparar hash:

```bash
for OTHER_SLUG_HASH in "${BASELINES_OTHERS[@]}"; do
  SLUG_OTHER=${OTHER_SLUG_HASH%:*}
  HASH_BASELINE=${OTHER_SLUG_HASH#*:}
  HASH_LIVE=$(curl -s "https://{dominio}/$SLUG_OTHER" | md5sum | awk '{print $1}')
  if [ "$HASH_BASELINE" = "$HASH_LIVE" ] ; then
    echo "OK /$SLUG_OTHER intacta"
  else
    echo "REGRESSAO /$SLUG_OTHER: baseline=$HASH_BASELINE live=$HASH_LIVE"
  fi
done
```

**Vizinhas que sao SOURCE de redirect (v3.9.0)** — para cada `(slug, destino)` em `REDIRECT_OTHERS`, validar o **redirect**, nao o conteudo (servem 3xx; comparar hash daria falso "REGRESSAO" — incidente 2026-06-16). `curl -sI` (HEAD, sem `-L`) e conferir status 3xx + `Location` == destino:

```bash
for SLUG_DEST in "${REDIRECT_OTHERS[@]}"; do
  SLUG_R=${SLUG_DEST%%:*}
  DEST_R=${SLUG_DEST#*:}
  HDRS=$(curl -sI "https://{dominio}/$SLUG_R")
  STATUS=$(printf '%s' "$HDRS" | head -1 | tr -d '\r')
  LOC=$(printf '%s' "$HDRS" | grep -i '^location:' | head -1 | tr -d '\r' | awk '{print $2}')
  case "$STATUS" in
    *" 30"[1278]*)
      if [ "$LOC" = "$DEST_R" ]; then
        echo "OK /$SLUG_R redireciona -> $LOC"
      else
        echo "REGRESSAO /$SLUG_R: Location=$LOC (esperado $DEST_R)"
      fi ;;
    *)
      echo "REGRESSAO /$SLUG_R: esperava 3xx -> $DEST_R, veio: $STATUS" ;;
  esac
done
```

Se **qualquer** vizinha quebrou:
1. Investigar imediatamente (provavelmente vercel.json sobrescrito, asset removido, rewrite agressivo de path).
2. NAO publicar relatorio. Reverter mudanca.
3. O modo guarda-chuva tem promessa de zero regressao — qualquer divergencia inesperada e bug.

Comparacao bit-a-bit e paranoia necessaria: em static sites sem teste de build, o unico sinal de que o deploy publicou o que voce queria e o conteudo servido bater com o fonte-sibling. Em multi-LP, esse sinal precisa cobrir cada LP.

**Defesa em camadas (v3.1.0):** este smoke test e a **segunda** linha de defesa contra regressao em vizinhas. A primeira e o sync do Passo 0.5.d, que garante que a sibling local esteja em paridade com o live antes de qualquer modificacao. Sync falho seria capturado aqui — se uma vizinha quebrou, ou (a) o sync do 0.5.d nao baixou esse slug (bug), ou (b) o deploy realmente quebrou a vizinha (asset removido, vercel.json sobrescrito). Em ambos os casos: NAO publicar relatorio, reverter, investigar.

## Passo 4: Dominio (se fornecido)

Comportamento depende do modo (Passo 0.5):

### Modo solo

Se `$dominio` nao vazio e o Passo 0.5 confirmou que ele NAO esta atribuido a outro projeto:

```bash
cd "{sibling}" && npx --yes vercel domains add "{dominio}"
```

Capturar as instrucoes de DNS que o Vercel retorna (tipo A com IP `76.76.21.21` ou CNAME). Guardar para o relatorio.

Se falhar (ja configurado fora deste projeto, conflito), reportar mensagem e seguir — pode ser que voce devia estar no modo guarda-chuva (Passo 0.5 deve ter detectado, mas se passou direto, esse e o sinal). Se tiver duvida, abortar e reanalisar Passo 0.5.

### Modo guarda-chuva

Pular `vercel domains add` — o dominio ja esta atribuido ao sibling guarda-chuva. Tentar adicionar de novo retorna conflito.

URL final ja e `https://{dominio}/{slug}` — registrar para o relatorio sem chamar a CLI.

## Passo 5: Validacoes Pos-Deploy

URL alvo: se dominio configurado, usar dominio final; senao, URL `.vercel.app`.

### 5.1 PageSpeed Insights

Use `WebFetch`. URL do site alvo deve ser **URL-encoded** no parametro `url=` (ex: `:` vira `%3A`, `/` vira `%2F`). Exemplo com `https://evento.buzzmonitor.com/vendendo-com-creators`:

```
https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https%3A%2F%2Fevento.buzzmonitor.com%2Fvendendo-com-creators&strategy=mobile&category=performance&category=accessibility&category=seo&category=best-practices
```

Extrair do JSON de resposta:
- `lighthouseResult.categories.performance.score` * 100
- `lighthouseResult.categories.accessibility.score` * 100
- `lighthouseResult.categories.seo.score` * 100
- `lighthouseResult.categories.best-practices.score` * 100
- Core Web Vitals: LCP, CLS, TBT, FCP

### 5.2 Headers de seguranca

```bash
curl -sI "https://{URL}" | grep -iE "strict-transport-security|x-content-type-options|x-frame-options|referrer-policy|permissions-policy|cross-origin-opener-policy|content-security-policy"
```

Confirmar que todos os 7 headers estao presentes.

**Teste de CSP (opcional mas recomendado):** abrir a URL no navegador, abrir DevTools → Console, e verificar se ha `Refused to load...` ou `Content Security Policy directive...`. Se aparecer, algum recurso legitimo esta sendo bloqueado — ajustar o CSP em `{sibling}/vercel.json` e re-deployar. Common offenders: pixel de conversao nao listado, chatbot, fonte custom de outro CDN.

### 5.3 GTM servido

Ler `brand/{marca}/tracking.json`. Se houver GTM id resolvido (regions[{regiao}] ou default != null):

```bash
curl -s "https://{URL}" | grep -oE "(googletagmanager\.com/(gtm\.js|ns\.html)|GTM-[A-Z0-9]+)" | sort -u
```

Esperado: **3 linhas distintas**:
- `googletagmanager.com/gtm.js` (script loader IIFE no `<head>`)
- `googletagmanager.com/ns.html` (iframe noscript apos `<body>`)
- `GTM-XXXXXXX` (o container id resolvido)

Por que 3 e nao 2: o snippet oficial do GTM concatena o ID em runtime (`j.src='...gtm.js?id='+i`), entao o `GTM-` nao aparece colado a URL do script — so no argumento da IIFE e dentro do `ns.html?id=`. Validacao correta checa os 3 tokens separadamente.

- **3 matches:** OK, GTM servido corretamente.
- **2 matches (sem `GTM-XXX`):** provavelmente o placeholder `{GTM_ID}` nao foi substituido — critico, re-gerar ou editar manualmente.
- **1 match:** integracao parcial (um dos blocos foi perdido) — critico.
- **0 matches:** LP sem tracking — registrar em "Pendencias".

Se `tracking.json` nao existe ou esta todo null, pular esta validacao.

### 5.4 Certificado

```bash
echo | openssl s_client -servername {DOMAIN} -connect {DOMAIN}:443 2>/dev/null | openssl x509 -noout -issuer -dates
```

Capturar emissor (Let's Encrypt) e validade.

## Passo 6: Relatorio Notion

Crie pagina filha da pasta Entregas — ID lido de `conhecimento/config/notion-ids.md` (chave `entregas`).

- **Titulo:** `Entrega LP · {Marca} · {Slug} · YYYY-MM-DD`
- **Icon:** 🚀
- **Conteudo:**

```markdown
## Resumo executivo

- **URL publica:** {URL final (dominio ou .vercel.app)}
- **URL provisoria:** {.vercel.app}
- **Modo:** {solo | guarda-chuva}
- **Project Vercel:** `{nome-do-projeto}` (`{prj_id}`)
- **Sibling:** `{path-da-sibling}`
- **Data de deploy:** YYYY-MM-DD HH:MM
- **Evento (se aplicavel):** {extrair do copy.txt ou README}

{Se modo guarda-chuva, adicionar tabela de LPs ativas no projeto:}

## Domínio multi-LP (modo guarda-chuva)

`{dominio}` hospeda {N} LPs simultaneamente:

| Path | Marca | Estado |
|---|---|---|
| `/{slug-novo}` | {Marca-da-nova} (esta entrega) | live |
| `/{slug-vizinho-1}` | {marca-vizinha-1} | intacta (smoke test ok) |
| `/{slug-vizinho-N}` | ... | ... |

## Performance (PageSpeed mobile)

| Categoria | Score |
|---|---|
| Performance | {N}/100 |
| Accessibility | {N}/100 |
| SEO | {N}/100 |
| Best Practices | {N}/100 |

**Core Web Vitals:**
- LCP: {X}s
- CLS: {X}
- TBT: {X}ms
- FCP: {X}s

## Seguranca

Headers ativos:
- [{x}] Strict-Transport-Security
- [{x}] X-Content-Type-Options
- [{x}] X-Frame-Options
- [{x}] Referrer-Policy
- [{x}] Permissions-Policy
- [{x}] Cross-Origin-Opener-Policy
- [{x}] Content-Security-Policy

Certificado: {CA, validade}

## Tracking

- GTM container: `{GTM_ID ou "nao configurado"}`
- Snippets ativos: `{2/2 (script + noscript) | 1/2 parcial | 0/2 ausente}`

## Pontos de atencao opcionais

{Colar conteudo da secao "Melhorias opcionais" de REVISAO.md, se existir}

## Pendencias

- {Domino pendente de DNS (se for o caso, colar instrucoes)}
- {Speakers reais se ainda forem placeholder}
- {Integracao CRM se o provedor nao for oficial}

## Como atualizar

```
/lp-publicar {marca} {slug} {dominio}
```

A fonte vive em `landing-pages/{marca}/{slug}/`. Editar la, rodar o comando acima.
```

## Passo 7: Relatorio Final ao Usuario

```
LP publicada — {marca}/{slug}

URL: {dominio ou .vercel.app}
Scores: Perf {N} / A11y {N} / SEO {N} / BP {N}
Headers de seguranca: {N}/6 ativos
Relatorio Notion: {URL}

{Se dominio: "DNS: {tipo} {valor} — encaminhar para admin do dominio"}
{Se isolamento detectou vazamento: texto do erro e passos para re-executar}
```

## Notas de seguranca

- **Nunca** rodar `vercel deploy` dentro do repo do agente (`$(git rev-parse --show-toplevel)`). So na pasta sibling (`${SIBLING_BASE}/{nome}/`).
- **Nunca** copiar `.env`, `meta-ads/`, `conhecimento/`, `.claude/` para a sibling.
- Se o usuario pedir para deployar direto sem pasta sibling, PARE e explique o risco.
- **Modo guarda-chuva** tem promessa de zero regressao. Qualquer divergencia de hash em LP vizinha apos deploy = bug bloqueante. Reverter, investigar, replanejar.
- **Nao misturar entregas** num mesmo deploy guarda-chuva. Uma rodada de `/lp-publicar` = uma LP nova ou atualizada. Se voce precisa atualizar duas LPs na mesma sessao, rode duas vezes.

## Anti-padroes documentados

Lista canonica em `landing-pages/CONTEXT.md` §7.1 (categoria) e §7.2 (historico de incidentes). Os anti-padroes especificos a `lp-publicar` (criar projeto duplicado, sobrescrever vercel.json em guarda-chuva, colidir asset sem namespace, path relativo sobrando, misturar 2 LPs no mesmo deploy) estao documentados la com referencia cruzada de versao.
