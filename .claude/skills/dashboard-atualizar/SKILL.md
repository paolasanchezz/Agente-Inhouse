---
name: dashboard-atualizar
description: Atualiza agora as 7 dashboards CM do guarda-chuva (dashboards-elife.vercel.app — Buzzmonitor, Cxpress e Buzzcreators Brasil, LATAM e as 3 de Portugal) disparando o workflow do GitHub Actions que o n8n ja dispara sozinho todo dia as 07:00 BRT. O workflow exporta do Supabase, valida o contrato de dados, deploya com smoke e rollback. A skill tambem faz ensaio sem deploy, aceita queda legitima da catraca e mostra o estado das ultimas rodadas. Deploy manual da maquina local esta bloqueado pelo hook desde 2026-10-21. Manual-trigger.
argument-hint: "[agora|ensaio|status|aceitar <slug|tudo>] (sem arg = pergunta com chips)"
allowed-tools: AskUserQuestion, Read, Bash, Glob, Grep
version: 5.0.2
---

# Skill: Atualizar Dashboards CM

As 7 dashboards de Content Marketing **se atualizam sozinhas todo dia às 07:00 BRT**: o n8n dispara o workflow `.github/workflows/dashboards-deploy.yml` (`integracoes/n8n/dashboards-disparo-diario.json`) e elas ficam prontas por volta das 07:03. O agendamento do próprio GitHub (07:13) é só reserva — ele chega com horas de atraso neste repositório. Esta skill serve para o que foge da rotina: **atualizar fora de hora**, **ensaiar** sem deployar, **destravar a catraca** quando uma queda é legítima, ou **ver como foram as últimas rodadas**.

Ela **não** exporta nem deploya da máquina local. O hook `guard_vercel_deploy.py` nega deploy manual do projeto `dashboards-elife`: um deploy local subia o código da branch em que você estivesse, pulava o validador, e a rodada seguinte devolvia o da `main`. Agora há um caminho só, e ele passa pelo contrato de dados.

| Dashboard | Rota | Fonte no repo | Idioma/moeda |
|---|---|---|---|
| **buzz-br** | `/buzz-br/` | `dashboard-buzz-br-vercel/` | PT-BR / BRL |
| **cxpress** | `/cxpress/` | `dashboard-cxpress-vercel/` | PT-BR / BRL |
| **latam** | `/latam/` | `dashboard-latam-vercel/` | ES / USD |
| **buzzcreators** | `/buzzcreators/` | `dashboard-buzzcreators-vercel/` | PT-BR / BRL |
| **bm-pt** · **cxpress-pt** · **elife-pt** | `/bm-pt/` … | `dashboard-pt-vercel/` (fonte única) | PT-PT / EUR |

Um login (Basic Auth) cobre as 7. **O workflow sempre atualiza as 7 juntas** (~2 min): não existe atualizar uma só — o guarda-chuva é um deploy único. Arquitetura, contrato de dados e catraca: `dashboards-umbrella/README.md`.

---

## Passo A: O que fazer

Resolver pela `$ARGUMENTS` (case-insensitive):

| Argumento | Ação |
|---|---|
| `agora`, `atualizar`, `todas`, `tudo`, ou um slug (`buzz-br`, `pt`, `cxpress`…) | **Atualizar agora** (deploy). Se veio um slug, avise em uma linha que as 7 sobem juntas |
| `ensaio`, `dry-run`, `teste` | **Ensaio**: exporta, valida e builda, nada vai pro ar |
| `status`, `estado` | **Status**: últimas rodadas + checagem da produção. Não dispara nada |
| `aceitar <slug\|tudo>` | **Aceitar queda da catraca** — pergunte o motivo se não veio (é obrigatório) |

Sem argumento ou não reconhecido: **AskUserQuestion** (header "Dashboards") com `Atualizar agora` / `Ensaio (sem deploy)` / `Ver status` / `Aceitar queda da catraca`.

---

## Passo 0: Pre-flight

```bash
REPO=victorfmlopes/Agente-Inhouse
WF=dashboards-deploy.yml
gh auth status >/dev/null 2>&1 || { echo "ERRO: gh sem login — rode 'gh auth login'"; exit 1; }
# Rodada em andamento? O workflow enfileira (concurrency), mas vale avisar o usuario.
gh run list --repo $REPO --workflow $WF --status in_progress --limit 1 --json databaseId,event \
  --jq '.[] | "ja tem uma rodada em andamento (\(.event)): \(.databaseId)"'
```

---

## Passo 1: Disparar (pule no modo Status)

```bash
DESDE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
gh workflow run $WF --repo $REPO --ref main                                   # atualizar agora
# gh workflow run $WF --repo $REPO --ref main -f dry_run=true                 # ensaio
# gh workflow run $WF --repo $REPO --ref main -f aceitar_catraca="<slug|tudo>" -f motivo="<por que caiu>"
```

**Aceitar catraca** só quando a queda tem explicação (limpeza de CRM, recategorização em massa, início do período movido para um ano novo). Destrava só a catraca daquele slug — nunca uma violação de contrato. Se você não sabe explicar a queda, **não aceite**: queda inexplicada é o sintoma de query quebrada.

Achar o run que acabou de nascer (o `gh workflow run` não devolve o id em todas as versões):

```bash
for i in $(seq 1 12); do
  RUN=$(gh run list --repo $REPO --workflow $WF --event workflow_dispatch --limit 1 \
        --json databaseId,createdAt --jq ".[] | select(.createdAt >= \"$DESDE\") | .databaseId")
  [ -n "$RUN" ] && break; sleep 5
done
echo "run: https://github.com/$REPO/actions/runs/$RUN"
```

---

## Passo 2: Acompanhar

Leva ~2 min. Rode em background e espere a notificação (não fique consultando):

```bash
until [ "$(gh run view $RUN --repo $REPO --json status --jq .status)" = "completed" ]; do sleep 8; done
gh run view $RUN --repo $REPO --json conclusion,jobs \
  --jq '{conclusao: .conclusion, passos: [.jobs[0].steps[] | "\(.name): \(.conclusion)"]}'
```

---

## Passo 3: Relatar

**Verde:** extraia do log o deploy e o smoke, e confirme a data dos dados no ar:

```bash
gh run view $RUN --repo $REPO --log | sed -E 's/^[^\t]*\t[^\t]*\t[0-9TZ:.-]+ //' \
  | grep -E "^modo:|RESULTADO|\[deploy_ci\] (deploy ok|SMOKE OK|dry-run)"
```

**Vermelho:** descubra o passo que falhou (`gh run view $RUN --repo $REPO --json jobs`), mostre as últimas ~30 linhas do log dele e traduza. Em qualquer falha **nada foi para o ar** e o painel segue com os dados anteriores — exceto se o deploy subiu e o smoke reprovou, caso em que o rollback já devolveu a versão anterior (procure `ROLLBACK` no log).

| Passo que falhou | O que significa | O que fazer |
|---|---|---|
| Conectividade com o Supabase | runner não alcançou o banco | pooler fora, ou credencial/permissão do `looker_readonly` mudou. O secret `SUPABASE_PG_URL` tem que ser a URL do **pooler** |
| Filtro CM do buzz-br sincronizado | `dashboard/queries.py` e o espelho `dashboard-pessoal/lib/queries.py` divergiram | replicar a mudança no espelho (é ele que o exportador usa) |
| Exportar | um exportador quebrou | query, `statement_timeout`, coluna renomeada no banco |
| Validar — exit **2** (contrato) | campo que o painel lê sumiu, mudou de tipo, enum novo, literal sumido | o exportador mudou o formato sem atualizar `dashboards-umbrella/contratos/<x>.json` (ou o contrário). A mensagem diz o campo, quem lê e, em rename, a causa provável |
| Validar — exit **4** (versão) | `SCHEMA_VERSION` do exportador, `schema_version` do contrato e `SCHEMA_ESPERADO` do painel divergem | bumpar as três pontas juntas (política no README) |
| Validar — exit **3** (catraca) | contagem caiu (ou explodiu) contra o que está no ar | explicação legítima → rodar de novo com **Aceitar catraca**. Sem explicação → investigar |
| Build, deploy, smoke e rollback | build sem JSON, deploy falhou, ou smoke reprovou | ver a última linha do log: rollback concluído ou "INTERVENÇÃO MANUAL URGENTE" |

Toda falha de rodada noturna também chega por e-mail para o Victor, com a etapa e o fim do log.

### Modo Status

```bash
gh run list --repo $REPO --workflow $WF --limit 5 \
  --json databaseId,event,conclusion,createdAt --jq '.[] | "\(.createdAt)  \(.event)  \(.conclusion // "rodando")  \(.databaseId)"'
py dashboards-umbrella/deploy_ci.py --checar-producao      # read-only: 401, noindex, 308, nav, JSONs nas 7
```

---

## Mudou o código de uma dashboard?

O workflow sobe o que está na `main`. Para mudar painel, motor ou exportador:

1. Edite a fonte em `dashboard-*-vercel/` (ou as `queries*.py`).
2. **Teste local antes do PR:**
   ```bash
   uv run --python 3.12 --with "psycopg[binary]" python dashboard-<x>-vercel/exportar_dados.py
   py dashboards-umbrella/validar_contrato.py <slug> --baseline-url https://dashboards-elife.vercel.app
   py dashboards-umbrella/auditar_filtro_cm.py                       # se mexeu no filtro do buzz-br
   ```
   **Paridade número-a-número** (obrigatória se mexeu em `motor.js`/`render.js`/queries — o motor JS só bate com a dash local se não divergirem; o PT não tem harness):
   ```bash
   uv run --python 3.12 --with "psycopg[binary]" python dashboard-<x>-vercel/paridade_gerar_esperado.py \
     && node dashboard-<x>-vercel/paridade_check.mjs                 # tem que dar 0 divergencias
   ```
3. `/commit`. **O PR roda o ensaio no CI** (export + contrato + build, sem deploy) e fica vermelho se a mudança quebrar o contrato.
4. Merge → a rodada seguinte deploya (ou dispare **Atualizar agora**).

Mudou o **formato** do JSON (campo lido removido/renomeado/retipado, literal, enum de acumulador)? Bump nas três pontas e contrato atualizado — política em `dashboards-umbrella/README.md` ("Contrato de dados").

---

## Emergência: GitHub Actions fora do ar

Só se a atualização não puder esperar o Actions voltar. Com `LP_DEPLOY_CI_OVERRIDE=1` **no ambiente da sessão**, o hook troca o bloqueio por uma confirmação; aprove conscientemente. A próxima rodada do workflow devolve o estado da `main`.

> **Onde pôr a variável:** o hook lê o ambiente do processo do Claude Code, não o do comando — então **prefixar no comando (`LP_DEPLOY_CI_OVERRIDE=1 npx vercel …`) não funciona**, e o deploy segue negado. Ponha em `"env": {"LP_DEPLOY_CI_OVERRIDE": "1"}` no `.claude/settings.local.json` (vale na próxima sessão) ou exporte no terminal antes de abrir o `claude`. **Remova assim que terminar** — com ela ligada, o bloqueio das LPs migradas também vira só confirmação.

```bash
for d in buzz-br cxpress latam buzzcreators; do
  uv run --python 3.12 --with "psycopg[binary]" python dashboard-$d-vercel/exportar_dados.py || exit 1
done
uv run --python 3.12 --with "psycopg[binary]" python dashboard-pt-vercel/exportar_dados.py --marca todas || exit 1
py dashboards-umbrella/auditar_filtro_cm.py && py dashboards-umbrella/validar_contrato.py --baseline-url https://dashboards-elife.vercel.app || exit 1
SIBLING="$(grep -E '^DASHBOARD_SIBLING_BASE=' .env.local | sed 's/^[^=]*=//')/dashboards-elife"
py dashboards-umbrella/build_umbrella.py "$SIBLING"            # leia os AVISO: REUSADO = dado velho
npx --yes vercel deploy --prod --yes --cwd "$SIBLING" --scope team_nC991VqUuSU2jXZN152xqqEg   # com o override no ambiente
py dashboards-umbrella/deploy_ci.py --checar-producao
```

---

## Notas

- **Senha do Basic Auth vive em dois lugares:** `.env.local` (uso local) e os secrets `DASHBOARD_BASIC_AUTH_USER`/`_PASS` do GitHub (o build do CI). Trocar a senha = atualizar **os dois** e disparar **Atualizar agora**; esquecer o secret faz o CI buildar com a senha velha.
- **Dados gitignored:** `dados-*.json` têm PII de leads e valores comerciais. O workflow nunca os sobe como artifact; só vão para o deploy, atrás do login.
- **Virada de ano:** nada quebra sozinho em 1º de janeiro. O início do período é uma data fixa (`2026-01-01` nos exportadores e em `queries_latam.py`), não "o ano corrente", então a exportação segue acumulando 2026 + 2027 e a catraca não dispara. Ela só dispara quando alguém **mover** esse início para 2027 — mudança deliberada, num PR; aí rode a primeira atualização com **Aceitar catraca** `tudo` e motivo "novo ano". O que cresce com o tempo é o tamanho dos JSONs: o validador avisa em 80% do teto (o LATAM, maior, deve chegar lá por volta de meados de 2027).
- **Projetos antigos** (`dashboard-buzzmonitor-brasil`, `dashboard-cxpress-brasil`, `dashboard-buzzmonitor-latam`, `dashboard-buzzcreators-brasil`) são redirect 308 para o guarda-chuva. Não deployar dashboard neles.
- **Portugal** tem modelo próprio — coorte por data de criação, distribuição de etapa atual (não conversão), CM como classificação. O porquê está em `dashboard/AUDITORIA-PORTUGAL.md`; não "corrija" isso para parecer com o BR sem reler a auditoria.
- **Diferenças por dashboard:** buzz-br = funil 7 KPIs e filtro CM em duas cópias (auditadas a cada rodada). cxpress = funil 7 KPIs, superfície única. latam = funil 5 fases ES/USD, leads inbound∪outbound + fechamentos de contratos. buzzcreators = funil 5 KPIs (sem Proposta), fonte Pipedrive com UTM recuperada por join com o contato. Runbooks: `dashboard/DEPLOY*.md`.
