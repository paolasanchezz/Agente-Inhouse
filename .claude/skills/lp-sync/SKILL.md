---
name: lp-sync
description: Popula a sibling local de um guarda-chuva com o estado do ultimo deploy production READY no Vercel. Read-only — nao modifica nada no live nem deploya. Use antes de qualquer fluxo manual (debug, inspecao, recovery, edicao direta) para garantir que a sibling reflete o que esta no ar. Fluxo regular de alteracao/deploy continua sendo `lp-publicar`, que ja faz este sync internamente no Passo 0.5.d.
argument-hint: "[dominio] — ex: content.cxpress.io | webinar.buzzmonitor.com"
allowed-tools: Read, Bash, Skill
version: 1.0.1
---

# Skill: Sincronizar Sibling com Live

Voce baixa o conteudo do **ultimo deploy production READY** do projeto Vercel atribuido a um dominio guarda-chuva e popula a sibling local com esse snapshot. **Nao modifica o live, nao deploya, nao toca em fonte no repo.** Output e a sibling local atualizada + relatorio do que mudou.

## Quando usar esta skill

- **Antes de fluxo manual** em sibling guarda-chuva — qualquer edicao direta, debug local, inspeção, recovery. Garante que a sibling local nao esta dias atrasada em relacao ao live.
- **Primeira execucao numa maquina** que vai mexer com um guarda-chuva ja em producao — popula a sibling com tudo que esta no ar, em vez de comecar com pasta vazia.
- **Apos suspeita de drift** — alguem deployou de outra maquina, hotfix manual via Vercel UI, ou simplesmente passou alguns dias sem rodar `lp-publicar`.

## Quando NAO usar esta skill

- **Vai deployar uma LP nova ou alterada:** rode `/lp-publicar` direto. Ela ja faz este sync internamente no Passo 0.5.d com checks de presenca, integridade e drift-check pre-overwrite. Esta skill nao tem essas camadas porque nao toca em deploy.
- **Modo solo:** sibling solo e linkada a um unico projeto/LP. Re-publicacao solo via `lp-publicar` ja faz sync (v3.3.0+). Sync standalone aqui nao agrega valor — `/lp-publicar` faz tudo.
- **Sibling vazia que vai ser criada do zero:** sem `.vercel/project.json` ainda nao da pra sync. Rode `npx vercel link` primeiro (ou rode `lp-publicar` que faz isso automatico no Passo 0.5.c).

## Anti-padrao que esta skill mata

Fluxo manual com `cd sibling && vercel deploy --force` + `curl live > sibling/{slug-conhecido}/index.html` em lista hardcoded **inventada pelo Claude da sessao**. Esse padrao falha silenciosamente quando uma LP foi adicionada de outra maquina sem o sibling local saber: a LP nova nao aparece na lista hardcoded, o deploy substitui o conteudo do projeto, e a LP some do live. Documentado em `landing-pages/CONTEXT.md` §7.2 (2026-05-13). Esta skill da o snapshot fresh em uma chamada — sem hardcode, sem inferencia, sem buraco.

## Passo 0: Parsing e Contexto

Argumento unico: `[dominio]` FQDN do guarda-chuva (ex: `content.cxpress.io`, `webinar.buzzmonitor.com`, `evento.buzzmonitor.com`, `material.buzzmonitor.com`).

Leia `landing-pages/CONTEXT.md` §4.2 (guarda-chuvas ativos) para entender o universo.

### 0.1 Resolver `SIBLING_BASE`

Mesma logica do `lp-publicar` Passo 0.1 — env var `LP_SIBLING_BASE` > linha em `.env.local` na raiz (com fallback para repo principal em worktrees). Se vazio, invocar `Skill` com `setup-agencia` argumento `"so lp"` e re-resolver.

```bash
SIBLING_BASE="$LP_SIBLING_BASE"

if [ -z "$SIBLING_BASE" ]; then
  for ENV_DIR in . "$(git rev-parse --git-common-dir 2>/dev/null | sed 's|/.git$||')"; do
    [ -z "$ENV_DIR" ] && continue
    if [ -f "$ENV_DIR/.env.local" ]; then
      SIBLING_BASE=$(grep -E "^LP_SIBLING_BASE=" "$ENV_DIR/.env.local" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'" | tr -d '\r')
      [ -n "$SIBLING_BASE" ] && break
    fi
  done
fi
```

Se vazio: avisar usuario, invocar `setup-agencia "so lp"`, re-resolver. Se ainda vazio (usuario abortou), parar.

### 0.2 Pre-flight Vercel CLI

Mesma logica do `lp-publicar` Passo 0.5.a:

```bash
TEAM=team_nC991VqUuSU2jXZN152xqqEg

npx --yes vercel --version >/dev/null 2>&1 || { echo "ERRO: Vercel CLI indisponivel."; exit 1; }
npx --yes vercel whoami --scope "$TEAM" >/dev/null 2>&1 || { echo "ERRO: nao autenticado no Vercel CLI (escopo $TEAM). Rode 'npx vercel login'."; exit 1; }
```

## Passo 1: Detectar projeto guarda-chuva

Mesma logica do `lp-publicar` Passo 0.5.b — `vercel alias ls` + extrair nome do projeto da source URL.

```bash
DOMAIN="$dominio"

# PAGINACAO (obrigatorio): `vercel alias ls` pagina (~20/pagina, mais recentes primeiro) e
# imprime `... --next <token>` no rodape. Guarda-chuvas antigos caem em paginas posteriores —
# sem paginar, dominio nao e encontrado e a skill aborta por engano. Match na coluna 2
# (alias-url == $DOMAIN), nao `$0 ~ d`, pra nao casar substring na source URL.
# Bug encontrado 2026-06-25: webinar.buzzmonitor.com estava na pagina 2.
PROJECT=""; NEXT=""; PAGE=0
while [ "$PAGE" -lt 50 ]; do
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
  [ -z "$NEXT" ] && break
done
```

Se `$PROJECT` vazio: dominio nao esta atribuido a nenhum projeto da org `elife-group` → abortar com mensagem "Dominio $DOMAIN nao encontrado como alias de nenhum projeto Vercel. Verifique se voce esta autenticado na conta certa (`vercel whoami --scope $TEAM`) e se o dominio realmente esta atribuido a um projeto da org elife-group."

Se nao vazio: `SIBLING="${SIBLING_BASE}/${PROJECT}"`.

## Passo 2: Garantir `.vercel/project.json`

Mesma logica do `lp-publicar` Passo 0.5.c:

```bash
mkdir -p "$SIBLING"

if [ ! -f "$SIBLING/.vercel/project.json" ]; then
  cd "$SIBLING" && npx --yes vercel link --yes --project="$PROJECT" --scope "$TEAM"
fi
```

Se o `.vercel/project.json` existir mas `projectId`/`orgId` nao baterem com o que a API retorna, re-rodar o link (sibling stale).

## Passo 3: Resolver `VERCEL_TOKEN`

Mesma logica do `lp-publicar` Passo 0.5.d.i — env var > `.env.local` (CWD + repo principal para worktree) > parse `auth.json` do CLI (Linux/macOS/Windows). Validar via `/v2/user` antes de aceitar (descarta tokens expirados).

Se nao resolver: invocar `setup-agencia "so lp"` e re-resolver. Se ainda vazio, parar com mensagem clara.

## Passo 4: Pegar ultimo deploy production READY

Mesma logica do `lp-publicar` Passo 0.5.d.ii. Distinguir 3 casos:

```bash
PROJECT_ID=$(python -c "import json; print(json.load(open(r'$SIBLING/.vercel/project.json'))['projectId'])")
ORG_ID=$(python -c "import json; print(json.load(open(r'$SIBLING/.vercel/project.json'))['orgId'])")

RESPONSE=$(curl -s -H "Authorization: Bearer $VERCEL_TOKEN" \
  "https://api.vercel.com/v6/deployments?projectId=$PROJECT_ID&teamId=$ORG_ID&target=production&state=READY&limit=1")

PARSED=$(echo "$RESPONSE" | python -c "
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    print('ERR:invalid_json:resposta nao e JSON valido'); sys.exit(0)
if 'error' in d:
    print('ERR:' + d['error'].get('code', 'unknown') + ':' + d['error'].get('message', ''))
elif d.get('deployments'):
    print('OK:' + d['deployments'][0]['uid'])
else:
    print('EMPTY:')
")
```

Tratamento:

| Caso | Acao |
|---|---|
| `ERR:forbidden:*` / `ERR:not_found:*` | Token sem permissao de read no projeto. Mensagem: "Regere o token em https://vercel.com/account/tokens com escopo Full Account na org elife-group, ou rode `/setup-agencia so lp`." Parar. |
| `ERR:*` (qualquer outro) | Erro inesperado da API. Reportar e parar. |
| `EMPTY:` | Projeto nao tem deploy production READY ainda. Mensagem: "Projeto $PROJECT nao tem deploy production READY ainda — nada para sincronizar." Sair com sucesso (no-op valido). |
| `OK:dpl_...` | Continuar com `DEPLOY_ID="${PARSED#OK:}"` |

## Passo 5: Baixar arquivos do deploy

Reusa o helper canonico `sync_sibling.py` da skill `lp-publicar` — nao duplicar logica. Invocar via env vars:

```bash
export DEPLOY_ID ORG_ID VERCEL_TOKEN SIBLING

python "$(git rev-parse --show-toplevel)/.claude/skills/lp-publicar/sync_sibling.py" 2>&1 | tee /tmp/lp-sync-output.log
SYNC_EXIT=${PIPESTATUS[0]}

if [ "$SYNC_EXIT" != "0" ]; then
  echo "ERRO: sync_sibling.py falhou (exit $SYNC_EXIT). Veja /tmp/lp-sync-output.log."
  exit 1
fi
```

O helper:
- Baixa a arvore de arquivos do deploy via `/v6/deployments/{id}/files`.
- Para cada arquivo folha, baixa via `/v7/deployments/{id}/files/{uid}?teamId=...` decodificando `base64` corretamente.
- Escreve em `$SIBLING/` preservando estrutura. **Nao deleta arquivos locais que nao estao no deploy** — apenas escreve. Pastas locais com slugs ausentes do live (ex: LP em rascunho ainda nao publicada) ficam intactas.

## Passo 6: Validar pos-sync (presenca + integridade)

Mesma logica do `lp-publicar` Passo 0.5.d.iv. Dois checks independentes.

### Check 1 — presenca

Confirmar que cada slug que responde 200 no dominio agora tem `{sibling}/{slug}/index.html`. Se faltar, sync incompleto.

```bash
SIBLING_SLUGS=$(find "$SIBLING" -mindepth 2 -maxdepth 2 -name "index.html" -type f 2>/dev/null | awk -F/ '{print $(NF-1)}' | sort -u)

# Slugs candidatos: o que o live tem hoje, descoberto via curl + parse de qualquer index
# Como nao temos lista de slugs do live, comparamos com os do repo + curl direto
REPO_SLUGS=$(find landing-pages -mindepth 3 -maxdepth 3 -name "index.html" -type f 2>/dev/null | awk -F/ '{print $(NF-1)}' | sort -u)

MISSING=""
for SLUG in $REPO_SLUGS; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://$DOMAIN/$SLUG" 2>/dev/null)
  if [ "$STATUS" = "200" ]; then
    echo "$SIBLING_SLUGS" | grep -q "^$SLUG$" || MISSING="$MISSING $SLUG"
  fi
done

if [ -n "$MISSING" ]; then
  echo "AVISO: Sync incompleto. Slugs vivos em $DOMAIN mas faltando na sibling:$MISSING"
  echo "Causa possivel: VERCEL_TOKEN sem permissao de read em alguns arquivos, bug no sync recursivo, ou LP que existe no live mas nao tem source no repo (anti-padrao §7.1 — 'LP publicada so na sibling')."
  echo "Verifique o token e o source antes de fluxo manual."
fi
```

Note: aviso e nao erro fatal. Diferente de `lp-publicar` Passo 0.5.d.iv (que aborta porque ia deployar), aqui apenas avisa — esta skill nao deploya nada, entao sibling incompleta nao causa regressao automatica.

### Check 2 — integridade

Confirmar que cada `index.html` na sibling pos-sync comeca com `<!doctype html>` ou `<html>`. Se nao, sync trouxe lixo (JSON wrapper, pagina em branco) — **abortar** com mesma mensagem do `lp-publicar`, porque qualquer acao manual sobre sibling corrompida vai propagar o lixo.

```bash
CORRUPTED=""
for SLUG_DIR in "$SIBLING"/*/; do
  [ -d "$SLUG_DIR" ] || continue
  HTML="$SLUG_DIR/index.html"
  [ -f "$HTML" ] || continue
  if ! head -c 100 "$HTML" | tr 'A-Z' 'a-z' | grep -qE '^[[:space:]]*<(!doctype|html)'; then
    CORRUPTED="$CORRUPTED $(basename "$SLUG_DIR")"
  fi
done

if [ -n "$CORRUPTED" ]; then
  echo "ERRO: Sync trouxe LP(s) corrompida(s) do live:$CORRUPTED"
  echo "Ultimo deploy production esta corrompido. NAO use esta sibling para fluxo manual."
  echo "Ver landing-pages/CONTEXT.md §7.2 (2026-05-07 tarde + 2026-05-08) para historico de JSON wrapper."
  exit 1
fi
```

## Passo 7: Relatorio final ao usuario

Sucesso (caso comum):

```
Sibling sincronizada com live de {dominio}

Projeto Vercel: {PROJECT} ({PROJECT_ID})
Sibling local:  {SIBLING}
Deploy baixado: {DEPLOY_ID}
Arquivos:       {N} sincronizados (ver log acima)

LPs presentes na sibling pos-sync:
  - /{slug-1}
  - /{slug-2}
  - ...

Status no live:
  - /{slug-1}: HTTP 200
  - /{slug-2}: HTTP 200
  - ...

{Se houver MISSING do Check 1: "AVISO: {slug-x} vivo no live mas nao apareceu na sibling — investigar antes de fluxo manual."}

Proximo passo recomendado:
  - Para deploy/alteracao: rode `/lp-publicar {marca} {slug} {dominio}` (sync ja foi feito, mas a skill re-sincroniza por seguranca antes do deploy).
  - Para inspecao local: a sibling agora reflete o live. Edite com cuidado — qualquer `vercel deploy` direto sem rodar `/lp-publicar` perde os guard rails (ver §7.1 anti-padrao "Rodar vercel deploy direto").
```

Caso EMPTY (projeto sem deploy READY ainda):

```
Projeto Vercel: {PROJECT}
Sibling local:  {SIBLING}
Status:         projeto nao tem deploy production READY ainda — nada para sincronizar (no-op).

Proximo passo recomendado:
  - Para primeira publicacao: rode `/lp-publicar {marca} {slug} {dominio}` — ela cria projeto e deploya do zero.
```

Caso ERRO (token sem permissao, sync corrompido, etc):

Reportar erro especifico + acao corretiva conforme tabela do Passo 4 ou Passo 6 Check 2.

## Notas de seguranca

- **Read-only no live.** Esta skill so consome a API Vercel via GET. Nao faz POST/PUT/DELETE em nada. Token usado tem o mesmo escopo que `lp-publicar` usa, mas aqui so chama endpoints de leitura.
- **Read-only no repo.** Nao escreve em `landing-pages/{marca}/{slug}/` nem em qualquer outro path do repo do agente. Output e apenas na sibling fora do repo.
- **Nao deletar nada na sibling.** O `sync_sibling.py` so escreve. Pastas locais com slugs em rascunho (nao publicados) ficam intactas. Se voce quer "limpar e re-sincronizar do zero", apague a sibling manualmente antes de rodar esta skill.
