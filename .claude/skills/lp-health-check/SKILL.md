---
name: lp-health-check
description: Rotina de health check que descobre dinamicamente todas as LPs em producao via Vercel API, faz HTTP check em cada uma, e envia email para victor.lopes@buzzmonitor.com.br quando ha falha. Silenciosa quando tudo OK. Pode rodar manualmente ou via /schedule diario.
argument-hint: "[--dry-run] [--no-drift]"
allowed-tools: Read, Glob, Bash, Skill
version: 1.0.0
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

Pulado se `--no-drift`. Caso contrario, comparar slugs descobertos no Vercel com pastas-source no repo:

```bash
if [ "$INCLUDE_DRIFT" = "1" ]; then
  # Listar todos os index.html em landing-pages/{marca}/{slug}/index.html
  SOURCE_SLUGS=$(find landing-pages -mindepth 3 -maxdepth 3 -name index.html -printf "%h\n" 2>/dev/null | sed 's|^landing-pages/||')
  # Resultado: linhas tipo "buzzmonitor/pocket-events", "cxpress/playbook-whatsapp2026"
fi
```

Compor `drift[]`:

- **fonte sem deploy:** existe `landing-pages/{marca}/{slug}/index.html` mas slug nao aparece em nenhuma URL descoberta no Vercel. Pode ser legitimo (rascunho, despublicada) — reportar como warning, nao falha.
- **deploy orfao:** slug aparece no Vercel mas nao tem source em `landing-pages/{marca}/{slug}/`. Pode ser legitimo (hospeda LP de outra estrutura) — warning.

Anexar `drift[]` ao payload que vai pro Passo 4.

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
DRIFT_N=$(echo "$DRIFT_JSON" | python -c "import json,sys; print(len(json.load(sys.stdin)))" 2>/dev/null || echo 0)

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

(se houver — fonte sem deploy ou deploy orfao)

## URLs OK (N)

Lista comprida — manter so como confirmacao.

## Como agir

1. Para 404 em LP que deveria estar ativa: rodar `/lp-sync {dominio}` para inspecao read-only da sibling, depois decidir entre `/lp-publicar` (re-deploy) ou rollback via Vercel UI.
2. Para 5xx persistente: pode ser problema da Vercel (status.vercel.com), DNS, ou cert. Aguardar 10min e re-rodar `/lp-health-check`.
3. Para drift "fonte sem deploy": verificar se LP foi despublicada de proposito. Se nao, rodar `/lp-publicar` para re-deployar.
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
| Drift falso-positivo (LP listada no repo mas marcada como sem deploy) | Source em `landing-pages/{marca}/{slug}/` ainda nao foi publicada | Esperado — drift e warning, nao falha |

## Nao-objetivos (v1)

- Validacao de conteudo (so HTTP status; sem grep de elementos no body)
- PageSpeed / Lighthouse na rotina diaria (ja e parte do `lp-publicar` no deploy)
- Auto-remediacao (skill so reporta — Victor decide acao)
- Dashboard historico (so o relatorio do incidente atual)
