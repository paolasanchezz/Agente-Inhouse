---
name: lp-health-check
description: Rotina de health check que descobre dinamicamente todas as LPs em producao via Vercel API, faz HTTP check em cada uma, e envia email para victor.lopes@buzzmonitor.com.br quando ha falha. Silenciosa quando tudo OK. Pode rodar manualmente ou via /schedule diario.
argument-hint: "[--dry-run] [--no-drift]"
allowed-tools: Read, Glob, Bash, Skill
version: 1.1.0
---

# Skill: Health Check Diario das LPs

Voce descobre dinamicamente todas as LPs em producao na org `elife-group` da Vercel, valida que cada uma responde HTTP 200, e dispara email de alerta se alguma estiver fora do ar. **Silenciosa quando tudo OK** — sem ruido, sem arquivos, sem notificacoes desnecessarias.

## Quando usar esta skill

- **Rotina diaria automatizada** via `/schedule` (cron `0 9 * * *` America/Sao_Paulo) — uso primario.
- **Verificacao manual on-demand** apos suspeita de incidente: campanha rodando, trafego comecou a reclamar, vai dar uma janela de manutencao, quer auditar antes de saida pra feriado, etc.
- **Pos-deploy de larga escala** — voce publicou varias LPs no mesmo guarda-chuva em sequencia e quer confirmar que nenhuma vizinha quebrou alem do smoke test do `lp-publicar`.

## Quando NAO usar esta skill

- **Apos deploy unitario:** `lp-publicar` ja faz smoke test pos-deploy nas vizinhas (Passo 3.4.b). Health check diario e complemento, nao substitui.
- **Validacao de design / a11y / performance:** isso e `lp-revisar` no momento do deploy ou PageSpeed manual.
- **Pra descobrir qual LP esta deployada onde:** essa skill imprime no console como parte do fluxo, mas se voce so quer a lista, rode `python .claude/skills/lp-health-check/discover.py` direto (mais rapido).

## Argumentos opcionais

- `--dry-run` — descobre + checa + imprime tudo no console; NAO salva relatorio nem envia email. Use pra testar sem efeitos colaterais.
- `--no-drift` — pula a etapa de cross-check com source no repo. Use se voce so quer saber se as LPs deployadas estao no ar, sem se preocupar com drift entre repo e producao.

Default (sem args): descoberta + check + drift + notifica se houver problema.

## Passo 0: Pre-flight

### 0.1 Resolver VERCEL_TOKEN

Mesma logica do `lp-publicar` §0.5.d.i — precedencia: env var → `.env.local` na raiz → `auth.json` do CLI (cross-platform) → validacao via `/v2/user`.

```bash
TEAM=team_nC991VqUuSU2jXZN152xqqEg
TOKEN_CANDIDATE="$VERCEL_TOKEN"

# 1. Tentar .env.local (CWD primeiro, depois repo principal — suporta worktree)
if [ -z "$TOKEN_CANDIDATE" ]; then
  for ENV_DIR in . "$(git rev-parse --git-common-dir 2>/dev/null | sed 's|/.git$||')"; do
    [ -z "$ENV_DIR" ] && continue
    if [ -f "$ENV_DIR/.env.local" ]; then
      TOKEN_CANDIDATE=$(grep -E "^VERCEL_TOKEN=" "$ENV_DIR/.env.local" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'" | tr -d '\r')
      [ -n "$TOKEN_CANDIDATE" ] && break
    fi
  done
fi

# 2. Tentar auth.json do CLI (Windows/macOS/Linux)
if [ -z "$TOKEN_CANDIDATE" ]; then
  for AUTH_PATH in \
    "$HOME/.local/share/com.vercel.cli/Data/auth.json" \
    "$HOME/Library/Application Support/com.vercel.cli/Data/auth.json" \
    "$APPDATA/com.vercel.cli/Data/auth.json"; do
    [ -f "$AUTH_PATH" ] || continue
    TOKEN_CANDIDATE=$(sed -n 's/.*"token"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$AUTH_PATH" | head -1)
    [ -n "$TOKEN_CANDIDATE" ] && break
  done
fi

# 3. Validar token
if [ -n "$TOKEN_CANDIDATE" ]; then
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $TOKEN_CANDIDATE" "https://api.vercel.com/v2/user")
  if [ "$STATUS" = "200" ]; then
    export VERCEL_TOKEN="$TOKEN_CANDIDATE"
    export ORG_ID="$TEAM"
  else
    echo "ERRO: token nao valida (HTTP $STATUS). Rode /setup-agencia so lp pra reconfigurar." >&2
    exit 1
  fi
else
  echo "ERRO: VERCEL_TOKEN nao encontrado. Rode /setup-agencia so lp pra configurar." >&2
  exit 1
fi
```

### 0.2 Resolver RESEND_API_KEY (so se nao for --dry-run)

```bash
if [ "$DRY_RUN" != "1" ]; then
  RESEND_CANDIDATE="$RESEND_API_KEY"

  if [ -z "$RESEND_CANDIDATE" ]; then
    for ENV_DIR in . "$(git rev-parse --git-common-dir 2>/dev/null | sed 's|/.git$||')"; do
      [ -z "$ENV_DIR" ] && continue
      if [ -f "$ENV_DIR/.env.local" ]; then
        RESEND_CANDIDATE=$(grep -E "^RESEND_API_KEY=" "$ENV_DIR/.env.local" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'" | tr -d '\r')
        [ -n "$RESEND_CANDIDATE" ] && break
      fi
    done
  fi

  if [ -z "$RESEND_CANDIDATE" ]; then
    echo "AVISO: RESEND_API_KEY nao encontrado. Health check vai rodar, mas em caso de falha NAO vai enviar email." >&2
    echo "  Configure a key em .env.local na raiz do repo (linha RESEND_API_KEY=re_...)." >&2
    echo "  Conta gratuita em https://resend.com (free tier 100 emails/dia)." >&2
  else
    export RESEND_API_KEY="$RESEND_CANDIDATE"
  fi
fi
```

## Passo 1: Descoberta dinamica das URLs

Roda `discover.py` (este diretorio) que faz 3 chamadas Vercel API:

1. `GET /v9/projects?teamId=$TEAM` — lista todos os projetos da org.
2. Para cada projeto, `GET /v9/projects/{id}/domains?teamId=$TEAM` — pega dominios custom (filtra `*.vercel.app`).
3. Para cada projeto com FQDN custom, `GET /v6/deployments?...&state=READY&limit=1` + `GET /v6/deployments/{uid}/files` — walk no file tree, identifica modo solo (`index.html` na raiz) vs guarda-chuva (subpastas com `index.html`).

```bash
DISCOVERED=$(python .claude/skills/lp-health-check/discover.py)
echo "$DISCOVERED" | python -m json.tool > /dev/null || { echo "ERRO: discover.py retornou JSON invalido" >&2; exit 1; }
N_URLS=$(echo "$DISCOVERED" | python -c "import json,sys; print(len(json.load(sys.stdin)['urls']))")
echo "Descobertas $N_URLS URLs em producao."
```

Se `errors` tiver itens no JSON, **abortar e mostrar pro usuario** — descoberta falhou, nao podemos confiar no resultado.

## Passo 2: Cross-check com source no repo (drift detection)

Pulado se `--no-drift`. Caso contrario, `drift.py` (este diretorio) faz o cross-check **deterministico**: le o output do `discover.py` via stdin e escaneia `landing-pages/{marca}/{slug}/index.html` no disco.

```bash
if [ "$INCLUDE_DRIFT" = "1" ]; then
  DRIFT_JSON=$(echo "$DISCOVERED" | python .claude/skills/lp-health-check/drift.py)
else
  DRIFT_JSON="[]"
fi
```

`drift.py` classifica cada item num `kind`:

- **`fonte_sem_deploy`** (ACIONAVEL) — `landing-pages/{marca}/{slug}/index.html` existe mas nao ha deploy em producao em lugar nenhum. Provavel rascunho ou LP despublicada. Acao: confirmar se foi de proposito; se nao, `/lp-publicar`.
- **`deploy_orfao`** (ACIONAVEL) — slug deployado num guarda-chuva sem source no repo. Acao: trazer o source pro repo (pull do deploy live) ou despublicar.
- **`vercel_app_only`** (INFORMATIVO) — source deployado **apenas** em `*.vercel.app` (projeto sem dominio custom). Estado legitimo (preview/experimento); **nao dispara email**.

Slugs com prefixo `_` (ex: `_placeholder`, raiz de guarda-chuva) sao estruturais e ignorados dos dois lados.

Anexar `DRIFT_JSON` ao payload que vai pro Passo 4. So os kinds acionaveis (`fonte_sem_deploy`, `deploy_orfao` — ver `drift.ACTIONABLE_KINDS`) contam pra decisao de notificar; `vercel_app_only` aparece no relatorio mas nao gera alerta.

## Passo 3: HTTP check em paralelo

Pipe do output do `discover.py` direto pro `check.py`:

```bash
RESULTS=$(echo "$DISCOVERED" | python .claude/skills/lp-health-check/check.py)
SUMMARY=$(echo "$RESULTS" | python -c "import json,sys; s=json.load(sys.stdin)['summary']; print(f\"{s['ok']}/{s['total']} OK, {s['warning']} warning, {s['fail']} fail\")")
echo "Resultado: $SUMMARY"
```

## Passo 4: Decidir notificacao + relatorio

```bash
FAIL=$(echo "$RESULTS" | python -c "import json,sys; print(json.load(sys.stdin)['summary']['fail'])")
WARN=$(echo "$RESULTS" | python -c "import json,sys; print(json.load(sys.stdin)['summary']['warning'])")
# So drift ACIONAVEL (fonte_sem_deploy/deploy_orfao) conta — vercel_app_only e informativo.
DRIFT_N=$(echo "$DRIFT_JSON" | python -c "import json,sys; sys.path.insert(0,'.claude/skills/lp-health-check'); from drift import ACTIONABLE_KINDS; d=json.load(sys.stdin); print(sum(1 for x in d if x.get('kind') in ACTIONABLE_KINDS))" 2>/dev/null || echo 0)

if [ "$FAIL" = "0" ] && [ "$WARN" = "0" ] && [ "$DRIFT_N" = "0" ]; then
  echo "Tudo verde. Sem relatorio, sem email."
  exit 0
fi
```

### 4.1 Salvar relatorio markdown

```bash
TIMESTAMP=$(date -u +"%Y-%m-%d-%H%M")
REPORT="landing-pages/health-checks/INCIDENT-${TIMESTAMP}.md"
```

Conteudo do `INCIDENT-...md`:

```markdown
# Incidente de health check — YYYY-MM-DD HH:MM UTC

**Resumo:** N/total OK | W warning | F falha | D drift

## Falhas (F)

| URL | Status | Diagnostico | Proximo passo |
|---|---|---|---|
| https://content.cxpress.io/playbook-whatsapp2026 | 404 | 404 Not Found | Rodar `/lp-sync content.cxpress.io` pra inspecionar |

## Avisos (W)

(se houver)

## Drift (D)

Acionavel: `fonte_sem_deploy` + `deploy_orfao`. O `vercel_app_only` (no ar so em `*.vercel.app`) vai numa secao **Informativo** separada e nao dispara email.

## URLs OK (N)

Lista comprida — manter so como confirmacao.

## Como agir

1. Para 404 em LP que deveria estar ativa: rodar `/lp-sync {dominio}` para inspecao read-only da sibling, depois decidir entre `/lp-publicar` (re-deploy) ou rollback via Vercel UI.
2. Para 5xx persistente: pode ser problema da Vercel (status.vercel.com), DNS, ou cert. Aguardar 10min e re-rodar `/lp-health-check`.
3. Para `fonte_sem_deploy`: verificar se a LP foi despublicada de proposito; se nao, `/lp-publicar` pra re-deployar. Para `deploy_orfao`: trazer o source pro repo (pull do deploy live) ou despublicar. `vercel_app_only` e informativo — sem acao.
```

Se `--dry-run`, NAO criar o arquivo — so imprimir o conteudo no console.

### 4.2 Enviar email via Resend

```bash
if [ "$DRY_RUN" != "1" ] && [ -n "$RESEND_API_KEY" ]; then
  PAYLOAD=$(python -c "
import json
results = json.loads('''$RESULTS''')
drift = json.loads('''$DRIFT_JSON''') if '''$DRIFT_JSON''' else []
print(json.dumps({
  'summary': results['summary'],
  'results': results['results'],
  'drift': drift,
  'report_path': '$REPORT',
}))
  ")
  echo "$PAYLOAD" | python .claude/skills/lp-health-check/notify.py
fi
```

Se `RESEND_API_KEY` nao foi resolvido no Passo 0.2: skip silencioso (ja avisou no Passo 0).

## Passo 5: Saida final pro console

```
✅ Tudo verde  (caso 0 problemas)

OU

⚠️  N URLs com problema. Relatorio: landing-pages/health-checks/INCIDENT-YYYY-MM-DD-HHMM.md
   Email enviado para victor.lopes@buzzmonitor.com.br
   (ou: 'Email NAO enviado — RESEND_API_KEY ausente.')
```

## Agendamento

Apos validar manualmente:

```
/schedule create "Health check diario das LPs" --cron "0 9 * * *" --tz "America/Sao_Paulo" --command "/lp-health-check"
```

`/schedule` roda no cloud Anthropic — independente da maquina do Victor estar ligada. Para o cron remoto enviar email, precisa que `VERCEL_TOKEN` e `RESEND_API_KEY` estejam acessiveis no ambiente do worker remoto. Validar no momento da configuracao do schedule.

## Custos e limites

- Vercel API: read-only, dentro dos limites do plano (no Hobby/Pro nao tem limite pratico pra essa volumetria — ~10-20 chamadas por execucao).
- Resend: free tier 100 emails/dia, 3k/mes. Health check diario silencioso quase nunca envia email — provavel 0-3 emails/mes.

## Troubleshooting

| Sintoma | Causa provavel | Fix |
|---|---|---|
| `discover.py` retorna `errors: ['VERCEL_TOKEN nao definido']` | Passo 0.1 nao exportou a var pro env do subprocess | Conferir que `export VERCEL_TOKEN=...` rodou antes do python |
| `discover.py` retorna 401/403 | Token expirado (auth.json do CLI tem TTL curto) | Regerar token em vercel.com/account/tokens com escopo Full Account na org elife-group |
| Nenhuma URL descoberta | Org sem projetos com FQDN custom, OU filtro de FQDN excluiu todos | Conferir `npx vercel ls --scope team_nC991VqUuSU2jXZN152xqqEg` |
| Email nao chega | (a) RESEND_API_KEY invalido, (b) dominio nao verificado em Resend, (c) email caiu no spam | Logs do Resend em https://resend.com/emails; usar `onboarding@resend.dev` como FROM provisoriamente (so envia pra dono da conta) |
| LP no repo aparece como `fonte_sem_deploy` mas voce sabe que esta no ar | Deployada so em `*.vercel.app` → `drift.py` classifica como `vercel_app_only` (informativo). Se ainda cai em `fonte_sem_deploy`, o projeto Vercel tem nome diferente do slug da pasta | Conferir nome do projeto vs slug; promover pra dominio custom se for LP de verdade |
| `deploy_orfao` recorrente numa LP live legitima | Source nunca foi versionado no repo | Trazer o source: pull do `index.html` do deploy live pra `landing-pages/{marca}/{slug}/` |

## Nao-objetivos (v1)

- Validacao de conteudo (so HTTP status; sem grep de elementos no body)
- PageSpeed / Lighthouse na rotina diaria (ja e parte do `lp-publicar` no deploy)
- Auto-remediacao (skill so reporta — Victor decide acao)
- Dashboard historico (so o relatorio do incidente atual)
