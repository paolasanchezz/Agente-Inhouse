---
name: dashboard-atualizar
description: Atualiza a dashboard CM Buzzmonitor Brasil (dinamica-estatica no Vercel) — roda o exportador Python (Supabase -> dados-2026.json), copia index.html + motor.js + dados pra pasta sibling fora do repo, deploya na Vercel via CLI e valida (senha + noindex + arquivos servidos). Manual-trigger semanal. Single-purpose (so este dashboard).
argument-hint: "(sem args — totalmente automatico)"
allowed-tools: AskUserQuestion, Read, Edit, Bash, Glob, Grep
version: 2.0.1
---

# Skill: Atualizar Dashboard CM Buzzmonitor Brasil (dinamica-estatica)

Voce atualiza https://dashboard-buzzmonitor-brasil.vercel.app — a dash **dinamica** (date-picker de intervalo livre + todos os dados de 2026), servida **estatica** no Vercel: os dados sao exportados aqui (onde o Supabase conecta) e embutidos num JSON; o navegador filtra/agrega em memoria (sem tocar no banco).

**Modelo (desde v2.0.0, 2026-07-01):** substituiu o snapshot semanal (`dashboard/gerar_relatorio.py`). A fonte agora e `dashboard-buzz-br-vercel/` (index.html + motor.js + exportador). O motivo, a arquitetura e a garantia de paridade estao em `dashboard-buzz-br-vercel/PLANO-VERCEL.md`.

**Regra inegociavel:** deploy NUNCA sai de `dashboard-buzz-br-vercel/` no repo. Sempre da pasta **sibling** fora do repo (com `middleware.js` de Basic Auth + `vercel.json` + `robots.txt`). Mesmo padrao do `lp-publicar`. Incidente 2026-05-25 (404 publico por deploy sem middleware) documentado em `dashboard/DEPLOY.md`.

**Seguranca:** o dominio publico e protegido por **senha forte** (Basic Auth no middleware) — o Vercel SSO Standard so cobre as URLs internas de deploy, nao o dominio principal (ver [[reference_vercel_deployment_protection]] na memoria). A credencial vem de `.env.local` e DEVE bater com `const PASS` no `middleware.js` da sibling.

---

## Passo 0: Pre-flight

### 0.1 Resolver `DASHBOARD_SIBLING_BASE`
```bash
SIBLING_BASE="${DASHBOARD_SIBLING_BASE}"
if [ -z "$SIBLING_BASE" ] && [ -f .env.local ]; then
  SIBLING_BASE=$(grep -E '^DASHBOARD_SIBLING_BASE=' .env.local | head -1 | sed 's/^[^=]*=//')
fi
if [ -z "$SIBLING_BASE" ]; then echo "ERRO: DASHBOARD_SIBLING_BASE nao configurado em .env.local"; exit 1; fi
SIBLING="$SIBLING_BASE/dashboard-buzzmonitor-brasil"
```

### 0.2 Verificar repo + fonte + env do Supabase
- `git rev-parse --show-toplevel` deve resolver (rode da raiz do repo).
- `dashboard-buzz-br-vercel/{exportar_dados.py,index.html,motor.js}` devem existir.
- `dashboard-pessoal/.env` (ou `dashboard/.env`) deve ter `SUPABASE_PG_URL=` — o exportador reusa a `queries.py`/conexao da dash local.

### 0.2b Auditar sincronia do filtro CM (espelho × oficial)

O filtro CM vive em DOIS lugares sincronizados **a mao**: `dashboard/queries.py` (oficial) e `dashboard-pessoal/lib/queries.py` (espelho, que o exportador usa). Se divergirem, a dash de producao mostra deals errados — foi o que trouxe o **ECHEF ROBOT** de volta em 2026-07-01 (blacklist estava so no oficial). Checar ANTES de exportar:

```bash
uv run --python 3.12 python -c "
import importlib.util
def L(p,n):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
o=L('dashboard/queries.py','o'); e=L('dashboard-pessoal/lib/queries.py','e'); d=False
for a in ['CM_UTM_SOURCES','EMAIL_WHITELIST','EMAIL_BLACKLIST','INTERNOS_EXCLUIR','CM_SLUGS_PREFIXES']:
    A,B=set(getattr(o,a)),set(getattr(e,a))
    if A^B: d=True; print(f'{a}: so_oficial={sorted(A-B)} so_espelho={sorted(B-A)}')
for a in ['CM_DEALS_FORCADOS','RECONVERSOES_MANUAIS','DEALS_EXCLUIDOS_URL_DATA']:
    if getattr(o,a)!=getattr(e,a): d=True; print(f'{a}: DIFERENTE')
print('FILTRO SINCRONIZADO' if not d else 'DESSINCRONIZADO — replicar a mudanca no espelho ANTES de exportar')
"
```
Se **DESSINCRONIZADO**: replicar a diferenca em `dashboard-pessoal/lib/queries.py` e so entao seguir (senao a dash sobe com deals errados).

### 0.3 Verificar sibling
Deve ter: `$SIBLING/.vercel/project.json` (projectId `prj_ck2DquIyOTmxz5Q823q0bgYVvDKe`), `middleware.js`, `vercel.json`, `robots.txt`, `package.json`.
- Faltando `.vercel/`: `cd "$SIBLING" && npx vercel link --yes --project=dashboard-buzzmonitor-brasil --scope=team_nC991VqUuSU2jXZN152xqqEg`
- Faltando middleware/vercel.json/robots.txt/package.json: abortar (`Sibling corrompida — restaurar arquivos de seguranca antes de continuar`).

### 0.4 Verificar Vercel CLI auth
```bash
npx --yes vercel whoami --scope=team_nC991VqUuSU2jXZN152xqqEg
```
Exit != 0: abortar (`Rode 'npx vercel login' e re-execute`).

### 0.5 Resolver credencial Basic Auth (de .env.local; deve bater com o middleware)
```bash
BASIC_AUTH_USER=$(grep -E '^DASHBOARD_BASIC_AUTH_USER=' .env.local | head -1 | sed 's/^[^=]*=//')
BASIC_AUTH_PASS=$(grep -E '^DASHBOARD_BASIC_AUTH_PASS=' .env.local | head -1 | sed 's/^[^=]*=//')
[ -z "$BASIC_AUTH_PASS" ] && { echo "ERRO: DASHBOARD_BASIC_AUTH_PASS ausente em .env.local"; exit 1; }
MW_PASS=$(grep -oE "const PASS = '[^']*';" "$SIBLING/middleware.js" | sed "s/const PASS = '//;s/';//")
[ "$MW_PASS" = "$BASIC_AUTH_PASS" ] || echo "WARN: senha do .env.local != middleware.js — vai dar 401 na validacao. Sincronizar antes."
TODAY=$(date +%Y-%m-%d); mkdir -p tmp
```

---

## Passo 1: Exportar dados frescos + sanity

```bash
uv run --python 3.12 --with "psycopg[binary]" python dashboard-buzz-br-vercel/exportar_dados.py 2>&1 | tee "tmp/dash-export-$TODAY.log"
EXIT=${PIPESTATUS[0]}
```
- Exit != 0: abortar e propagar as ultimas 15 linhas do log (Supabase fora, statement_timeout, import). O exportador seta `statement_timeout=120s`; as queries com CTE de 90d sao lentas (~8s) — normal levar 1-3min.

**Sanity do JSON** (defesa contra dados corrompidos/vazios):
```bash
uv run --python 3.12 python -c "
import json,sys
d=json.load(open('dashboard-buzz-br-vercel/dados-2026.json',encoding='utf-8'))
import os; sz=os.path.getsize('dashboard-buzz-br-vercel/dados-2026.json')
assert d.get('leads') and len(d['leads'])>0, 'leads vazio'
for k in ('leads','ce','ra','rr','prop','fech','perdidos','serie_12m','proporcao_sources','gerado_em'): assert k in d, f'falta {k}'
assert sz < 3_000_000, f'JSON grande demais: {sz}b (rever campos/compressao)'
print(f'sanity OK — leads={len(d[\"leads\"])} fech={len(d[\"fech\"])} gerado_em={d[\"gerado_em\"]} tamanho={sz//1024}KB')
"
```
Falhou o sanity: abortar (nao copiar/deployar dados suspeitos).

---

## Passo 2: Copiar os 3 arquivos do site pra sibling

**So estes 3** (preservar middleware.js/vercel.json/robots.txt/package.json da sibling):
```bash
cp dashboard-buzz-br-vercel/index.html      "$SIBLING/index.html"
cp dashboard-buzz-br-vercel/motor.js        "$SIBLING/motor.js"
cp dashboard-buzz-br-vercel/dados-2026.json "$SIBLING/dados-2026.json"
# conferir tamanhos identicos
for f in index.html motor.js dados-2026.json; do
  a=$(stat -c%s "dashboard-buzz-br-vercel/$f"); b=$(stat -c%s "$SIBLING/$f")
  [ "$a" = "$b" ] || { echo "ERRO copia $f: $a != $b"; exit 1; }
done
echo "copia OK"
```

---

## Passo 3: Deploy
```bash
npx --yes vercel deploy --prod --yes --cwd "$SIBLING" --scope=team_nC991VqUuSU2jXZN152xqqEg 2>&1 | tee "tmp/dash-deploy-$TODAY.log"
NEW_DPL_ID=$(grep -oE 'dpl_[a-zA-Z0-9]+' tmp/dash-deploy-$TODAY.log | head -1)
```
- Linha `▲ Aliased https://dashboard-buzzmonitor-brasil.vercel.app` = alias bateu, seguir. Se nao aparecer (raro, pos-rollback): `npx vercel promote "$NEW_DPL_ID" --cwd "$SIBLING" --scope=team_nC991VqUuSU2jXZN152xqqEg`.
- `FetchError` intermitente da CLI: nao retry cego — `npx vercel ls dashboard-buzzmonitor-brasil --cwd "$SIBLING" --scope=team_nC991VqUuSU2jXZN152xqqEg | head -5` e ver se ficou READY.

---

## Passo 4: Validacao (as 3 garantias)
```bash
B="https://dashboard-buzzmonitor-brasil.vercel.app"
echo "sem auth (espera 401):  $(curl -s -o /dev/null -w '%{http_code}' "$B/")"
echo "index   (espera 200):   $(curl -s -u "$BASIC_AUTH_USER:$BASIC_AUTH_PASS" -o tmp/v.html -w '%{http_code} %{size_download}b' "$B/")"
echo "motor.js:               $(curl -s -u "$BASIC_AUTH_USER:$BASIC_AUTH_PASS" -o /dev/null -w '%{http_code}' "$B/motor.js")"
echo "dados-2026.json:        $(curl -s -u "$BASIC_AUTH_USER:$BASIC_AUTH_PASS" -o /dev/null -w '%{http_code} %{size_download}b' "$B/dados-2026.json")"
grep -oq 'MotorCM' tmp/v.html && echo "index e a dash nova: OK" || echo "ERRO: index servido nao referencia MotorCM"
curl -s -D - -o /dev/null -u "$BASIC_AUTH_USER:$BASIC_AUTH_PASS" "$B/" | grep -i 'x-robots-tag'
```
Esperado: 401 sem auth · 200 no index (~65KB) · 200 motor.js · 200 dados-2026.json (bate com o local) · index referencia MotorCM · X-Robots-Tag noindex.

**Erros:**
- **401 com a credencial certa:** `.env.local` != `const PASS` do `$SIBLING/middleware.js`. Sincronizar e re-deployar.
- **404 no root:** deploy saiu sem index.html (incidente 2026-05-25). Rollback: `npx vercel rollback <dpl_anterior_READY> --yes --cwd "$SIBLING" --scope=team_nC991VqUuSU2jXZN152xqqEg`.
- **index no ar sem `MotorCM`:** subiu versao velha/errada — reconferir Passo 2 e re-deployar.

---

## Passo 5: Relatorio
```
============================================================
Dashboard CM Buzzmonitor (dinamica) — atualizada
============================================================
URL:        https://dashboard-buzzmonitor-brasil.vercel.app/  (login: inhouse + senha do .env.local)
Deploy ID:  $NEW_DPL_ID · READY
Dados:      leads=$N_LEADS · fech=$N_FECH · gerado_em=$GERADO_EM
Intervalo:  date-picker livre no navegador (dados de 2026); troca de filtro instantanea.

Rollback rapido: npx vercel rollback <dpl_anterior> --cwd "$SIBLING" --scope=team_nC991VqUuSU2jXZN152xqqEg
Pra commitar mudancas de codigo (se houve): /commit
```

---

## Notas de seguranca e manutencao
- **Credencial Basic Auth** vive em `.env.local` (`DASHBOARD_BASIC_AUTH_USER`/`_PASS`, gitignored) e no `middleware.js` da sibling (fora do repo). Trocar a senha = editar os DOIS lugares. Nunca hardcodar nesta skill.
- **Nunca** rodar `vercel deploy` de `dashboard-buzz-br-vercel/` (sem middleware = 404/exposto). So da sibling.
- **Nunca** copiar pra sibling alem de index.html + motor.js + dados-2026.json (o `.py`/`.mjs`/PLANO ficam so no repo).
- **Paridade dos numeros:** garantida por a logica CM viver no Python (`exportar_dados.py` reusa `dashboard-pessoal/lib/queries.py`); o `motor.js` so agrega. Se mudar a regra CM, re-exportar reflete automatico. Pra re-validar apos mudar motor/queries: `uv run --python 3.12 --with "psycopg[binary]" python dashboard-buzz-br-vercel/paridade_gerar_esperado.py` + `node dashboard-buzz-br-vercel/paridade_check.mjs` (deve dar 0 divergencias). (Rodar via `uv`, nao `python` direto — no Windows o `python` do PATH costuma ser o shim da Store, que falha com exit 49; o `uv` provisiona o proprio Python 3.12 com wheels de C-extension.)
- **Escopo 2026:** o exportador cobre 2026 + cauda p/ as series 12m. Intervalos inteiramente em 2025 nao entram (virar 2027: ajustar `ANO_INI` em `exportar_dados.py`).
- **Snapshot antigo** (`dashboard/gerar_relatorio.py` + gate de EXPECTED) foi aposentado nesta v2.0.0 — mantido no repo so para auditoria historica.
