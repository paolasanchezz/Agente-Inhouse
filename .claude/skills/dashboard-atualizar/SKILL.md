---
name: dashboard-atualizar
description: Atualiza a dashboard CM Buzzmonitor Brasil — roda gerador Python contra Supabase, lida com gate de regressao (fechamentos novos via chips), copia HTML pra pasta sibling fora do repo, deploya na Vercel via CLI, e valida via HTTP + Basic Auth. Manual-trigger semanal. Single-purpose (so este dashboard).
argument-hint: "(sem args — totalmente automatico)"
allowed-tools: AskUserQuestion, Read, Edit, Bash, Glob, Grep
version: 1.0.2
---

# Skill: Atualizar Dashboard CM Buzzmonitor Brasil

Voce orquestra o fluxo semanal de atualizacao de https://dashboard-buzzmonitor-brasil.vercel.app: roda o gerador Python (consome Supabase), lida com o gate de regressao (que quase sempre falha quando entra fechamento novo), copia o HTML pra pasta sibling FORA do repo, deploya via Vercel CLI e valida.

**Regra inegociavel:** deploy NUNCA sai de `dashboard/` no repo. Sempre da pasta sibling (com `middleware.js` de Basic Auth + `vercel.json`). Padrao identico ao `lp-publicar`. Incidente 2026-05-25 documentado em `dashboard/DEPLOY.md`.

**Single-purpose:** so cobre o dashboard Buzzmonitor Brasil. Sem multi-marca, sem multi-regiao. Hardcoda nome do projeto Vercel (`dashboard-buzzmonitor-brasil`) e da sibling (`dashboard-buzzmonitor-brasil`).

---

## Passo 0: Pre-flight

### 0.1 Resolver `DASHBOARD_SIBLING_BASE`

Ordem: env var em runtime > linha em `.env.local` na raiz do repo.

```bash
SIBLING_BASE="${DASHBOARD_SIBLING_BASE}"
if [ -z "$SIBLING_BASE" ] && [ -f .env.local ]; then
  SIBLING_BASE=$(grep -E '^DASHBOARD_SIBLING_BASE=' .env.local | head -1 | sed 's/^[^=]*=//')
fi
if [ -z "$SIBLING_BASE" ]; then
  echo "ERRO: DASHBOARD_SIBLING_BASE nao configurado. Adicione em .env.local: DASHBOARD_SIBLING_BASE=/path/onde/fica/a/sibling"
  exit 1
fi
SIBLING="$SIBLING_BASE/dashboard-buzzmonitor-brasil"
```

### 0.2 Verificar repo e env do Supabase

- `git rev-parse --show-toplevel` deve resolver. Se nao, abortar (rode da raiz do repo).
- `dashboard/.env` deve existir com `SUPABASE_PG_URL=`. Se nao, instruir: copiar de `dashboard/.env.example` e preencher.

### 0.3 Verificar sibling

A sibling deve ter:
- `$SIBLING/.vercel/project.json` (link Vercel) com `projectId: prj_ck2DquIyOTmxz5Q823q0bgYVvDKe`
- `$SIBLING/middleware.js` (Basic Auth)
- `$SIBLING/vercel.json` (headers)
- `$SIBLING/package.json`

Se faltar `.vercel/`: abortar com:
```
Sibling nao linkada ao Vercel. Rode:
  cd "$SIBLING" && npx vercel link --yes --project=dashboard-buzzmonitor-brasil --scope=team_nC991VqUuSU2jXZN152xqqEg
```

Se faltar `middleware.js` ou `vercel.json` ou `package.json`: abortar com `Sibling corrompida em $SIBLING. Restaurar middleware.js + vercel.json + package.json antes de continuar (estao na sibling, nao no repo).`

### 0.4 Verificar Vercel CLI auth

```bash
npx --yes vercel whoami --scope=team_nC991VqUuSU2jXZN152xqqEg
```

Se exit != 0: abortar com `Rode 'npx vercel login' e re-execute /dashboard-atualizar.`

### 0.5 Capturar contexto

```bash
TODAY=$(date +%Y-%m-%d)
mkdir -p tmp
```

Ler `dashboard/gerar_relatorio.py` linhas 48-58 (Read). Extrair:
- `EXPECTED_OLD_N` = valor de `EXPECTED_FECH_YTD_2026`
- `EXPECTED_OLD_VALOR` = valor de `EXPECTED_FECH_VALOR_YTD_2026`
- `LAST_REVISAO` = data mais recente em `# Revisao YYYY-MM-DD:` no comentario (fallback: `2026-05-18` se nunca houve revisao)

---

## Passo 1: Gerar HTML + gate de regressao

### 1.1 Primeira tentativa

```bash
uv run --python 3.12 --with "psycopg[binary]" python dashboard/gerar_relatorio.py 2>&1 | tee "tmp/dashboard-run-$TODAY.log"
EXIT_CODE=${PIPESTATUS[0]}
```

### 1.2 Smoke test passou (exit 0)

Pular pro Passo 2. Log resumido: `[OK] gerar_relatorio.py exit 0 — nenhum fech novo desde $LAST_REVISAO. Seguindo pra Passo 2.`

### 1.3 Erro real (exit != 0 mas log NAO contem `[smoke test] FALHA`)

Algo quebrou alem do gate (Supabase fora do ar, import error, etc.). Abortar e propagar as ultimas 15 linhas do log pro Victor. Nao tentar gate.

### 1.4 Listar fechamentos YtD atuais (sem criar arquivo)

```bash
uv run --python 3.12 --with "psycopg[binary]" python -c "
import sys, json
from datetime import date
sys.path.insert(0, 'dashboard')
from datas import calcular_periodos
from queries import q_lista_fechamentos
from gerar_relatorio import load_url, fetch_dict
import psycopg
p = calcular_periodos()
with psycopg.connect(load_url()) as conn, conn.cursor() as cur:
    rows = fetch_dict(cur, q_lista_fechamentos(p['ytd_ini'], p['ytd_fim']))
soma = sum(float(r.get('valor') or 0) for r in rows)
out = {
    'n': len(rows),
    'soma': soma,
    'rows': [{
        'id': r['id'],
        'deal': str(r['deal'])[:70],
        'utm_source': r.get('utm_source') or '',
        'utm_content': str(r.get('utm_content') or '')[:40],
        'valor': float(r.get('valor') or 0),
        'data_evento': str(r['data_evento']),
        'email': r.get('email') or '',
        'bd': r.get('bd') or '',
    } for r in rows],
}
print(json.dumps(out, ensure_ascii=False, default=str))
" > "tmp/dashboard-fech-$TODAY.json" 2>&1
```

Parsear o JSON com `python -c "import json; print(json.load(open('tmp/dashboard-fech-$TODAY.json')))"` ou ler direto com Read.

### 1.5 Identificar fechamentos NOVOS

Filtrar `rows` por `data_evento > LAST_REVISAO`. Se LAST_REVISAO desconhecida, listar todos os fechamentos com `data_evento >= 2026-05-01` como suspeitos (heuristica).

Computar:
- `N_ATUAL` = numero total de fechamentos
- `SOMA_ATUAL` = soma total
- `NOVOS` = lista filtrada
- `DELTA_N` = `N_ATUAL - EXPECTED_OLD_N`
- `DELTA_SOMA` = `SOMA_ATUAL - EXPECTED_OLD_VALOR`

### 1.6 Divergencia NEGATIVA (n < EXPECTED) — abortar SEM perguntar

```
ERRO: divergencia NEGATIVA — fechamentos sumiram do banco.

  Esperado: $EXPECTED_OLD_N deals · R$ $EXPECTED_OLD_VALOR
  Atual:    $N_ATUAL deals · R$ $SOMA_ATUAL

Atualizar EXPECTED_* nesse caso esconderia regressao real.

Possiveis causas:
  - Filtro CM em dashboard/queries.py foi alterado
  - EMAIL_BLACKLIST cresceu / EMAIL_WHITELIST encolheu
  - Deal foi removido do CRM (raro — investigar)

Acao: leia tmp/dashboard-fech-$TODAY.json, compare com a lista esperada e
investigue queries.py antes de rodar /dashboard-atualizar de novo.
```

Aborta. Skill nao toca em EXPECTED_*.

### 1.7 Auditoria: queries.py mudou nos ultimos 7 dias?

```bash
QUERIES_CHANGES=$(git log --oneline --since="7 days ago" -- dashboard/queries.py 2>/dev/null)
```

Se nao-vazio, armazenar pra anexar ao bloco do gate (§1.8).

### 1.8 Bloco textual + AskUserQuestion (gate)

Imprimir antes da pergunta (texto plain, sem markdown, pra renderizar bem):

```
============================================================
GATE DE REGRESSAO — Fechamentos YtD 2026
============================================================

Esperado (EXPECTED_FECH_YTD_2026):  $EXPECTED_OLD_N deals · R$ $EXPECTED_OLD_VALOR
Atual no banco:                     $N_ATUAL deals · R$ $SOMA_ATUAL
Delta:                              +$DELTA_N deals · +R$ $DELTA_SOMA

Fechamentos NOVOS (data_evento > $LAST_REVISAO):

  YYYY-MM-DD · Cliente                · utm_source       · R$ valor · email
  ... (1 linha por novo fech)

(Demais $EXPECTED_OLD_N fechamentos ja contemplados — nao listados.)
```

Se `QUERIES_CHANGES` nao-vazio, anexar:

```
ATENCAO: dashboard/queries.py mudou nos ultimos 7 dias:
  <git log oneline output>

Fechamentos "novos" podem refletir mudanca de filtro CM, nao apenas fech genuinos.
Confirme que os novos batem com o que voce esperava antes de aprovar.
```

Entao chamar `AskUserQuestion`:

```
question: "Aprovar atualizacao de EXPECTED_FECH_YTD_2026 ($EXPECTED_OLD_N -> $N_ATUAL) e re-rodar o gerador?"
header: "Gate fechamentos"
multiSelect: false

Opcoes:
  1. "Sim — atualizar e deployar (Recomendado)"
     description: "Edita gerar_relatorio.py (EXPECTED_* + linha de comentario historico),
     re-roda gerador, se exit 0 segue pra Passo 2 (copia + deploy)."

  2. "Atualizar mas pular deploy"
     description: "Edita gerar_relatorio.py + re-roda gerador, ate HTML novo em disco,
     mas para antes do Passo 2. Util pra abrir o HTML local no browser antes de subir."

  3. "Investigar antes — abortar"
     description: "Para a skill sem editar nada. Voce inspeciona tmp/dashboard-fech-$TODAY.json
     e roda /dashboard-atualizar de novo quando estiver confiante."
```

**NAO PROSSEGUIR sem resposta explicita.**

### 1.9 Se aprovado (opcao 1 ou 2): patch automatico

a. **Backup:**
   ```bash
   cp dashboard/gerar_relatorio.py "tmp/gerar_relatorio.py.bak-$TODAY"
   ```

b. **Edit do `EXPECTED_FECH_YTD_2026`:**
   - `old_string`: `EXPECTED_FECH_YTD_2026 = $EXPECTED_OLD_N`
   - `new_string`: `EXPECTED_FECH_YTD_2026 = $N_ATUAL`

c. **Edit do `EXPECTED_FECH_VALOR_YTD_2026`:**
   - `old_string`: `EXPECTED_FECH_VALOR_YTD_2026 = $EXPECTED_OLD_VALOR`
   - `new_string`: `EXPECTED_FECH_VALOR_YTD_2026 = $SOMA_ATUAL`
   - Atencao: o valor no codigo tem decimal (ex: `16580.0`). Match exato.

d. **Edit pra inserir linha de comentario historico** (acima da linha `EXPECTED_FECH_YTD_2026`):

   Linha nova:
   ```
   # Revisao $TODAY: +$DELTA_N fechamento(s) ($lista enxuta — ate 3 — "Cliente, utm_source, R$ valor"). Total YtD 2026: $N_ATUAL deals · R$ $SOMA_ATUAL.
   ```

   Match pra Edit: a linha imediatamente acima (`# Total YtD 2026: ...` ou ultima linha `# Revisao ...:`). Inserir a nova linha apos.

e. **Mostrar diff no log:**
   ```bash
   git diff dashboard/gerar_relatorio.py >> "tmp/dashboard-run-$TODAY.log"
   git diff --stat dashboard/gerar_relatorio.py
   ```

f. **Re-rodar gerador:**
   ```bash
   uv run --python 3.12 --with "psycopg[binary]" python dashboard/gerar_relatorio.py 2>&1 | tee -a "tmp/dashboard-run-$TODAY.log"
   ```
   Exit != 0 aqui = algo alem do gate (raro). Restaurar backup (`cp tmp/gerar_relatorio.py.bak-$TODAY dashboard/gerar_relatorio.py`) e abortar com as ultimas linhas do log.

### 1.10 Se "Atualizar mas pular deploy" (opcao 2)

Parar apos §1.9.f com:

```
HTML pronto em dashboard/relatorio-semanal-buzzmonitor-brasil.html
EXPECTED_* atualizado em dashboard/gerar_relatorio.py
Sibling nao foi tocada.

Pra deployar quando estiver confiante: rode /dashboard-atualizar de novo.
```

---

## Passo 2: Copiar HTML pra sibling

### 2.1 Validar source

- `dashboard/relatorio-semanal-buzzmonitor-brasil.html` existe? `stat` ou `Get-Item`.
- Tamanho > 50KB (defesa contra HTML zerado por erro silencioso). HTML real fica em torno de 72KB. Se < 50KB, abortar.

### 2.2 Sanity: data "gerado em" presente

Extrair a data ja renderizada na tag `gerado_em`:

```bash
LOCAL_DATA=$(grep -oE 'gerado_em">[^<]+' dashboard/relatorio-semanal-buzzmonitor-brasil.html | head -1 | sed 's/gerado_em">//')
```

`LOCAL_DATA` deve ficar com algo no formato PT-BR `DD Mmm YYYY` (ex: `25 Mai 2026`).

Verificar:
- Nao-vazia. Se vazia, abortar com `Tag gerado_em nao encontrada no HTML — gerador pode ter falhado silenciosamente. Logs: tmp/dashboard-run-$TODAY.log`.
- Bate com o dia de hoje no formato `DD Mmm YYYY`. Computar a string esperada:

```bash
MESES_PT=("Jan" "Fev" "Mar" "Abr" "Mai" "Jun" "Jul" "Ago" "Set" "Out" "Nov" "Dez")
EXPECTED_DATA="$(date +%d) ${MESES_PT[$((10#$(date +%m) - 1))]} $(date +%Y)"
[ "$LOCAL_DATA" = "$EXPECTED_DATA" ] || echo "WARN: HTML diz '$LOCAL_DATA', hoje seria '$EXPECTED_DATA'. Pode ser regenerator stale; investigar gerar_relatorio.py."
```

Divergencia eh **warning**, nao abort — guardar `LOCAL_DATA` pra usar no §4.3.

### 2.3 Copiar

```bash
cp dashboard/relatorio-semanal-buzzmonitor-brasil.html "$SIBLING/index.html"
```

### 2.4 Validar tamanho

`stat -c "%s" "$SIBLING/index.html"` deve bater com o source (mesmo bytes). Se diverge, abortar.

---

## Passo 3: Deploy

### 3.1 `vercel deploy`

```bash
npx --yes vercel deploy --prod --yes --cwd "$SIBLING" --scope=team_nC991VqUuSU2jXZN152xqqEg 2>&1 | tee "tmp/dashboard-deploy-$TODAY.log"
```

Em caso de `FetchError: Unexpected end of JSON input` ou similar (bug intermitente da CLI): NAO retry cego. Rodar `npx vercel ls dashboard-buzzmonitor-brasil --cwd "$SIBLING" --scope=team_nC991VqUuSU2jXZN152xqqEg | head -5` e ver se o deploy ficou READY server-side. Se sim, prosseguir com o deploy id retornado.

### 3.2 Extrair deploy ID e URL do novo deploy

Do log do deploy:
- `NEW_DPL_ID`: padrao `dpl_[a-zA-Z0-9]+` no JSON final (`"id": "dpl_..."`)
- `NEW_DPL_URL`: padrao `https://dashboard-buzzmonitor-brasil-[a-z0-9]+-elife-group.vercel.app` (URL provisoria do deploy)

```bash
NEW_DPL_ID=$(grep -oE 'dpl_[a-zA-Z0-9]+' tmp/dashboard-deploy-$TODAY.log | head -1)
NEW_DPL_URL=$(grep -oE 'https://dashboard-buzzmonitor-brasil-[a-z0-9]+-elife-group\.vercel\.app' tmp/dashboard-deploy-$TODAY.log | head -1)
```

### 3.3 Conferir alias e promover se necessario

`vercel ls` lista URLs (subdomain), nao `dpl_id`. Comparar URL do top com `NEW_DPL_URL`:

```bash
LATEST_URL=$(npx vercel ls dashboard-buzzmonitor-brasil --cwd "$SIBLING" --scope=team_nC991VqUuSU2jXZN152xqqEg 2>&1 \
  | grep -oE 'https://dashboard-buzzmonitor-brasil-[a-z0-9]+-elife-group\.vercel\.app' \
  | head -1)
```

Se `$LATEST_URL` != `$NEW_DPL_URL` (acontece pos-rollback recente — alias trava no antigo ate promote explicito):

```bash
npx vercel promote "$NEW_DPL_ID" --cwd "$SIBLING" --scope=team_nC991VqUuSU2jXZN152xqqEg
```

**Atalho:** o output do `vercel deploy` no §3.1 ja indica se aliasing rodou automatico (linha `▲ Aliased https://dashboard-buzzmonitor-brasil.vercel.app`). Quando essa linha aparece, alias bateu — pular o `vercel ls` desse passo e ir direto pro Passo 4. Quando NAO aparece (raro — geralmente pos-rollback), entao rodar a checagem acima.

---

## Passo 4: Verificacao

### 4.1 HTTP check com Basic Auth

```bash
curl -s -u "inhouse:inhouse@77" "https://dashboard-buzzmonitor-brasil.vercel.app/" \
  -o "tmp/verify-$TODAY.html" \
  -w "%{http_code} %{size_download}\n"
```

Esperado: `200 NNNNN` com NNNNN > 50000 (mesmo piso do Passo 2.1; HTML real fica em ~72-76KB). A validacao firme e o Passo 4.2 (remote == local +/-100 bytes), nao um numero absoluto.

### 4.2 Comparar tamanho com sibling

```bash
LOCAL_SIZE=$(stat -c "%s" "$SIBLING/index.html")
REMOTE_SIZE=$(stat -c "%s" "tmp/verify-$TODAY.html")
DIFF=$((LOCAL_SIZE - REMOTE_SIZE))
DIFF=${DIFF#-}  # absolute value
```

Toleranca: ±100 bytes (edge pode reescrever metadata). Se `$DIFF > 100`, esperar 30s e re-testar 1x. Se persistir: warning no relatorio final (nao bloqueia — pode ser cache de edge).

### 4.3 Conteudo bate

Extrair a data renderizada do HTML servido pelo Vercel e comparar com a `LOCAL_DATA` capturada no §2.2:

```bash
REMOTE_DATA=$(grep -oE 'gerado_em">[^<]+' "tmp/verify-$TODAY.html" | head -1 | sed 's/gerado_em">//')
[ "$LOCAL_DATA" = "$REMOTE_DATA" ] && echo "OK: data '$REMOTE_DATA' bate com local"
```

Se nao bate (`LOCAL_DATA="25 Mai 2026"`, `REMOTE_DATA="18 Mai 2026"`): warning — provavel cache de edge servindo versao antiga. Esperar 30s, re-testar 1x. Se persistir, registrar no relatorio final mas nao bloquear (o deploy em si esta READY — edge se ajusta em minutos).

### 4.4 Erros

- **HTTP 401:** middleware quebrou ou credencial mudou. Abortar com `middleware.js da sibling esta diferente. Inspecione $SIBLING/middleware.js. Pra rollback: vercel rollback <dpl_anterior> --cwd "$SIBLING"`. Listar dpls anteriores com `vercel ls`.
- **HTTP 404:** REPETIU O INCIDENTE 2026-05-25 (sibling sem index.html ou deploy fora). Abortar com:
  ```
  ERRO: HTTP 404 no root. Deploy provavelmente saiu sem index.html.
  Rollback imediato:
    npx vercel rollback <dpl_anterior_READY> --yes --cwd "$SIBLING" --scope=team_nC991VqUuSU2jXZN152xqqEg

  Dpls recentes:
    <output de vercel ls | head -5>
  ```
- **Qualquer outro status:** parar e reportar.

---

## Passo 5: Relatorio no console

Imprimir resumo limpo:

```
============================================================
Dashboard CM Buzzmonitor — atualizada
============================================================

URL:           https://dashboard-buzzmonitor-brasil.vercel.app/
Deploy ID:     $NEW_DPL_ID
Status:        HTTP 200 · ${REMOTE_SIZE} bytes
Periodo:       $PERIODO_SEMANA · MtD $PERIODO_MTD · YtD $PERIODO_YTD
Fechamentos:   $N_ATUAL YtD · R$ $SOMA_ATUAL ($DELTA_TXT desde ultima revisao)

(Se gate foi disparado:)
EXPECTED_FECH_YTD_2026 atualizado: $EXPECTED_OLD_N -> $N_ATUAL
Novos fech contemplados:
  - cliente1 · utm_source1 · R$ valor1
  - cliente2 · utm_source2 · R$ valor2
Diff: dashboard/gerar_relatorio.py (rode 'git diff dashboard/gerar_relatorio.py' pra ver)

Pra commitar (opcional): /commit

Ultimos 3 deploys (rollback rapido):
  $NEW_DPL_ID  (atual)
  dpl_anterior_1
  dpl_anterior_2
```

(Sem Notion — dashboard eh interna, sem stakeholder esperando log publicado.)

---

## Anexo: Troubleshooting

| Sintoma | Causa provavel | Acao |
|---|---|---|
| `gerar_relatorio.py` falha com `[smoke test] FALHA` e divergencia positiva | Fech CM legitimo entrou na semana | Skill auto-trata via §1.8 |
| Divergencia NEGATIVA (n menor) | Filtro CM mudou, deal removido, whitelist diminuiu | §1.6 — aborta sem perguntar. Investigar `queries.py` |
| Smoke test passa mas valor R$ diverge em centavos | Reajuste de valor no CRM | Tratar como divergencia positiva (gate normal) |
| `vercel deploy` FetchError CLI | Bug intermitente | §3.1 — checar `vercel ls` antes de retry |
| HTTP 404 pos-deploy | Sibling sem index.html OU deploy saiu de dashboard/ | §4.4 — rollback comando exato |
| HTTP 401 pos-deploy | middleware.js da sibling mudou | §4.4 — verificar `$SIBLING/middleware.js` |
| Sibling sem `.vercel/project.json` | Nova maquina | §0.3 — `vercel link` comando exato |
| Alias nao atualiza pos-deploy | Promote travado por rollback recente | §3.3 — auto-promove |
| Erro de import `psycopg` no python -c | `uv run` esqueceu o `--with` | Confirmar pip install local OU usar comando completo do §1.4 |
| `dashboard/.env` sem `SUPABASE_PG_URL` | Setup incompleto | Copiar `dashboard/.env.example` e preencher |

---

## Notas de seguranca e manutencao

- **Nunca** rodar `vercel deploy` em `dashboard/` (anti-padrao do incidente 2026-05-25 — sem middleware = 404 publico).
- **Nunca** copiar outros arquivos do repo pra sibling alem do `index.html`. Sibling tem `middleware.js`, `vercel.json`, `package.json` proprios — preservar.
- **Nunca** commitar `dashboard/relatorio-*.html` (ja gitignored).
- **Nunca** atualizar `EXPECTED_FECH_YTD_2026` se a divergencia for NEGATIVA (sempre indica regressao real, nao fech novo legitimo).
- **Quando virar 2027:** o gate em `dashboard/gerar_relatorio.py:93` tem `if ytd_ini.year == 2026` hardcoded. Skill nao cobre essa migracao — criar `EXPECTED_FECH_YTD_2027` e ajustar a comparacao manualmente.
- **Comentario historico** em `gerar_relatorio.py:48-58` cresce 1 linha por execucao. Aceitavel por ~1 ano; refatorar pra arquivo separado se passar disso.
- **Concorrencia:** se rodar 2x em paralelo, o segundo run pode ler EXPECTED_* ja editado pelo primeiro. Manual-trigger via chat dificulta isso. Nao implementado lock.
