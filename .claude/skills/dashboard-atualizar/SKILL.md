---
name: dashboard-atualizar
description: Atualiza uma das dashboards CM dinamica-estaticas no Vercel — Buzzmonitor Brasil, Cxpress Brasil ou Buzzmonitor LATAM (o usuario escolhe qual, por arg ou chip). Roda o exportador Python (Supabase -> JSON de dados), copia os arquivos do site pra pasta sibling fora do repo, deploya na Vercel via CLI e valida (senha + noindex + arquivos servidos). Manual-trigger.
argument-hint: "[buzz-br|cxpress|latam] (sem arg = pergunta com chips)"
allowed-tools: AskUserQuestion, Read, Edit, Bash, Glob, Grep
version: 3.0.1
---

# Skill: Atualizar Dashboard CM (dinamica-estatica) — multi-dashboard

Voce atualiza UMA das 3 dashboards de Content Marketing servidas **dinamica-estaticas** no Vercel. Todas seguem o MESMO modelo: os dados sao exportados aqui (onde o Supabase conecta) e embutidos num JSON; o navegador filtra/agrega em memoria com date-picker de intervalo livre (sem tocar no banco). Sao projetos Vercel **solo** (1 projeto = 1 dashboard, sem vizinhas).

| Dashboard | Fonte no repo | Sibling (deploy) | URL | Idioma/moeda |
|---|---|---|---|---|
| **buzz-br** | `dashboard-buzz-br-vercel/` | `dashboard-buzzmonitor-brasil` | dashboard-buzzmonitor-brasil.vercel.app | PT-BR / BRL |
| **cxpress** | `dashboard-cxpress-vercel/` | `dashboard-cxpress-brasil` | dashboard-cxpress-brasil.vercel.app | PT-BR / BRL |
| **latam** | `dashboard-latam-vercel/` | `dashboard-buzzmonitor-latam` | dashboard-buzzmonitor-latam.vercel.app | ES / USD |

**Regra inegociavel:** deploy NUNCA sai da pasta-fonte no repo. Sempre da pasta **sibling** fora do repo (com `middleware.js` de Basic Auth + `vercel.json` + `robots.txt`). Mesmo padrao do `lp-publicar`. Incidente 2026-05-25 (404 publico por deploy sem middleware) em `dashboard/DEPLOY.md`.

**Seguranca:** o dominio publico e protegido por **senha forte** (Basic Auth no middleware) — o Vercel SSO Standard so cobre URLs internas de deploy, nao o dominio principal ([[reference_vercel_deployment_protection]]). As 3 dashboards usam a **mesma credencial** (`inhouse` + senha forte); vem de `.env.local` e DEVE bater com `const PASS` no `middleware.js` da sibling.

---

## Passo A: Resolver QUAL dashboard

1. Se `$ARGUMENTS` trouxer um slug, normalizar (case-insensitive):
   - `buzz-br`, `br`, `brasil`, `buzz`, `buzzmonitor`, `buzz-brasil` → **buzz-br**
   - `cxpress`, `cx`, `cxpress-brasil` → **cxpress**
   - `latam`, `lat`, `buzz-latam` → **latam**
2. Se ausente ou nao reconhecido, use **AskUserQuestion** (header "Dashboard") com 3 opcoes: `Buzzmonitor Brasil` / `Cxpress Brasil` / `Buzzmonitor LATAM`.

Fixe o slug resolvido em `$DASH` e rode o bloco de config (define TODAS as variaveis dos passos seguintes):

```bash
DASH="<buzz-br|cxpress|latam>"   # resolvido no Passo A
SCOPE=team_nC991VqUuSU2jXZN152xqqEg
case "$DASH" in
  buzz-br)
    SRC=dashboard-buzz-br-vercel;  SIB_NAME=dashboard-buzzmonitor-brasil
    URL=dashboard-buzzmonitor-brasil.vercel.app; JSON=dados-2026.json; MAIN=leads
    FILES="index.html motor.js dados-2026.json"; MARKER=MotorCM; AUDIT3=1 ;;
  cxpress)
    SRC=dashboard-cxpress-vercel;  SIB_NAME=dashboard-cxpress-brasil
    URL=dashboard-cxpress-brasil.vercel.app; JSON=dados-cxpress.json; MAIN=deals
    FILES="index.html estilo.css motor.js render.js dados-cxpress.json"; MARKER=MotorCxpress; AUDIT3=0 ;;
  latam)
    SRC=dashboard-latam-vercel;    SIB_NAME=dashboard-buzzmonitor-latam
    URL=dashboard-buzzmonitor-latam.vercel.app; JSON=dados-latam.json; MAIN=leads
    FILES="index.html estilo.css motor.js render.js dados-latam.json"; MARKER=MotorLatam; AUDIT3=0 ;;
  *) echo "ERRO: dashboard invalido: '$DASH'"; exit 1 ;;
esac
echo "Dashboard: $DASH · fonte: $SRC · sibling: $SIB_NAME · url: $URL"
```

---

## Passo 0: Pre-flight

### 0.1 Resolver a sibling
```bash
SIBLING_BASE="${DASHBOARD_SIBLING_BASE}"
if [ -z "$SIBLING_BASE" ] && [ -f .env.local ]; then
  SIBLING_BASE=$(grep -E '^DASHBOARD_SIBLING_BASE=' .env.local | head -1 | sed 's/^[^=]*=//')
fi
[ -z "$SIBLING_BASE" ] && { echo "ERRO: DASHBOARD_SIBLING_BASE nao configurado em .env.local"; exit 1; }
SIBLING="$SIBLING_BASE/$SIB_NAME"
```

### 0.2 Verificar repo + fonte + env do Supabase
- `git rev-parse --show-toplevel` deve resolver (rode da raiz do repo).
- `$SRC/exportar_dados.py` e `$SRC/$JSON`-geraveis devem existir (`ls "$SRC"`).
- `dashboard/.env` (ou `dashboard-pessoal/.env`) deve ter `SUPABASE_PG_URL=` — o exportador reusa a conexao/queries da dash local.

### 0.2b Auditar sincronia do filtro CM — **SO se `AUDIT3=1` (buzz-br)**
O buzz-br tem o filtro CM em 3 superficies sincronizadas a mao (`dashboard/queries.py` oficial × `dashboard-pessoal/lib/queries.py` espelho, que o exportador usa). Se divergirem, sobe deals errados (caso ECHEF ROBOT, 2026-07-01). Rode a auditoria de constantes:

```bash
if [ "$AUDIT3" = "1" ]; then
uv run --python 3.12 python -c "
import importlib.util
def L(p,n):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
o=L('dashboard/queries.py','o'); e=L('dashboard-pessoal/lib/queries.py','e'); d=False
for a in ['CM_UTM_SOURCES','EMAIL_WHITELIST','EMAIL_BLACKLIST','INTERNOS_EXCLUIR','HERANCA_SOURCES_INTERNAS','CM_SLUGS_PREFIXES']:
    A,B=set(getattr(o,a)),set(getattr(e,a))
    if A^B: d=True; print(f'{a}: so_oficial={sorted(A-B)} so_espelho={sorted(B-A)}')
for a in ['CM_DEALS_FORCADOS','FECHAMENTOS_FORCADOS','RECONVERSOES_MANUAIS','DEALS_EXCLUIDOS_URL_DATA']:
    if getattr(o,a)!=getattr(e,a): d=True; print(f'{a}: DIFERENTE')
print('FILTRO SINCRONIZADO' if not d else 'DESSINCRONIZADO — replicar no espelho ANTES de exportar')
"
fi
```
Se **DESSINCRONIZADO**: replicar em `dashboard-pessoal/lib/queries.py` e so entao seguir.

> **cxpress / latam:** superficie UNICA — o exportador importa `queries_cxpress.py` / `queries_latam.py` direto de `dashboard/` (sem espelho). Nao ha o que auditar aqui; a paridade (Passo 1.5) cobre a consistencia motor × queries.

### 0.3 Verificar sibling
Deve ter `$SIBLING/.vercel/project.json`, `middleware.js`, `vercel.json`, `robots.txt`, `package.json`.
- Faltando `.vercel/`: `cd "$SIBLING" && npx vercel link --yes --project="$SIB_NAME" --scope="$SCOPE"`
- Faltando middleware/vercel.json/robots.txt/package.json: abortar (`Sibling corrompida — restaurar arquivos de seguranca`). Para (re)criar do zero, veja `$SRC/sync_sibling.py` (cxpress/latam) ou `dashboard/DEPLOY.md` (buzz-br).

### 0.4 Vercel CLI auth
```bash
npx --yes vercel whoami --scope="$SCOPE"
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
uv run --python 3.12 --with "psycopg[binary]" python "$SRC/exportar_dados.py" 2>&1 | tee "tmp/dash-$DASH-export-$TODAY.log"
EXIT=${PIPESTATUS[0]}
```
- Exit != 0: abortar e propagar as ultimas 15 linhas do log (Supabase fora, statement_timeout, import). Normal levar 1-3min (conexao cold + queries).

**Sanity do JSON** (defesa contra dados corrompidos/vazios — usa `$MAIN` e `$JSON` da config):
```bash
uv run --python 3.12 python -c "
import json,os
p='$SRC/$JSON'; d=json.load(open(p,encoding='utf-8')); sz=os.path.getsize(p)
assert d.get('gerado_em'), 'falta gerado_em'
assert isinstance(d.get('$MAIN'),list) and len(d['$MAIN'])>0, '$MAIN vazio/ausente'
assert sz < 3_400_000, f'JSON grande demais: {sz}b (rever campos/compressao)'
print(f'sanity OK — $MAIN={len(d[\"$MAIN\"])} gerado_em={d[\"gerado_em\"]} tamanho={sz//1024}KB')
"
```
Falhou o sanity: abortar (nao copiar/deployar dados suspeitos).

---

## Passo 1.5: Paridade numero-a-numero (recomendado; **obrigatorio se mexeu no codigo**)

O motor JS so bate com a dash local se `motor.js`/`render.js`/as queries nao divergirem. Rode se voce **alterou** motor/render/queries desde o ultimo deploy (em atualizacao de dados rotineira o motor e o mesmo — pode pular):

```bash
uv run --python 3.12 --with "psycopg[binary]" python "$SRC/paridade_gerar_esperado.py" && node "$SRC/paridade_check.mjs"
```
Deve terminar em **0 divergencias**. Qualquer divergencia: corrigir o motor/render antes de deployar (nao suba numeros errados).

---

## Passo 2: Copiar os arquivos do site pra sibling

Copia **apenas** os arquivos de conteudo (`$FILES`) — preserva `middleware.js`/`vercel.json`/`robots.txt`/`package.json` da sibling (Basic Auth + seguranca):
```bash
for f in $FILES; do
  cp "$SRC/$f" "$SIBLING/$f"
  a=$(stat -c%s "$SRC/$f"); b=$(stat -c%s "$SIBLING/$f")
  [ "$a" = "$b" ] || { echo "ERRO copia $f: $a != $b"; exit 1; }
done
echo "copia OK ($FILES)"
```

---

## Passo 3: Deploy
```bash
npx --yes vercel deploy --prod --yes --cwd "$SIBLING" --scope="$SCOPE" 2>&1 | tee "tmp/dash-$DASH-deploy-$TODAY.log"
NEW_DPL_ID=$(grep -oE 'dpl_[a-zA-Z0-9]+' "tmp/dash-$DASH-deploy-$TODAY.log" | head -1)
```
- Linha `▲ Aliased https://$URL` = alias bateu, seguir. Se nao aparecer (raro, pos-rollback): `npx vercel promote "$NEW_DPL_ID" --cwd "$SIBLING" --scope="$SCOPE"`.
- `FetchError` intermitente da CLI: nao retry cego — `npx vercel ls "$SIB_NAME" --cwd "$SIBLING" --scope="$SCOPE" | head -5` e ver se ficou READY.

---

## Passo 4: Validacao (as garantias)
```bash
B="https://$URL"
echo "sem auth (espera 401):  $(curl -s -o /dev/null -w '%{http_code}' "$B/")"
echo "index   (espera 200):   $(curl -s -u "$BASIC_AUTH_USER:$BASIC_AUTH_PASS" -o tmp/v.html -w '%{http_code} %{size_download}b' "$B/")"
echo "$JSON:                  $(curl -s -u "$BASIC_AUTH_USER:$BASIC_AUTH_PASS" -o /dev/null -w '%{http_code} %{size_download}b' "$B/$JSON")"
grep -oq "$MARKER" tmp/v.html && echo "index e a dash nova ($MARKER): OK" || echo "ERRO: index servido nao referencia $MARKER"
echo -n "senha fraca antiga (espera 401): "; curl -s -u "inhouse:inhouse@77" -o /dev/null -w '%{http_code}\n' "$B/"
curl -s -D - -o /dev/null -u "$BASIC_AUTH_USER:$BASIC_AUTH_PASS" "$B/" | grep -i 'x-robots-tag'
```
Esperado: 401 sem auth · 200 no index · 200 no `$JSON` (bate com o local) · index referencia `$MARKER` · 401 com a senha fraca antiga · `X-Robots-Tag: noindex`.

**Erros:**
- **401 com a credencial certa:** `.env.local` != `const PASS` do `$SIBLING/middleware.js`. Sincronizar e re-deployar.
- **404 no root:** deploy saiu sem index.html (incidente 2026-05-25). Rollback: `npx vercel rollback <dpl_anterior_READY> --yes --cwd "$SIBLING" --scope="$SCOPE"`.
- **index no ar sem `$MARKER`:** subiu versao velha/errada — reconferir Passo 2 e re-deployar.

---

## Passo 5: Relatorio
```
============================================================
Dashboard CM $DASH (dinamica) — atualizada
============================================================
URL:        https://$URL/  (login: inhouse + senha do .env.local)
Deploy ID:  $NEW_DPL_ID · READY
Dados:      $MAIN=$N gerado_em=$GERADO_EM · $JSON
Intervalo:  date-picker livre no navegador (dados de 2026); troca de filtro instantanea.

Rollback rapido: npx vercel rollback <dpl_anterior> --cwd "$SIBLING" --scope="$SCOPE"
Pra commitar mudancas de codigo (se houve): /commit
```

---

## Notas de seguranca e manutencao
- **Credencial Basic Auth** (as 3 usam a MESMA) vive em `.env.local` (`DASHBOARD_BASIC_AUTH_USER`/`_PASS`, gitignored) e no `middleware.js` de cada sibling (fora do repo). Trocar a senha = editar o `.env.local` + os 3 middlewares (ou re-rodar `sync_sibling.py` de cxpress/latam, que le a senha do middleware do buzz-br). Nunca hardcodar nesta skill.
- **Nunca** rodar `vercel deploy` da pasta-fonte no repo (sem middleware = 404/exposto). So da sibling.
- **Nunca** copiar pra sibling alem de `$FILES` (os `.py`/`.mjs`/README/PLANO ficam so no repo).
- **Dados gitignored:** `dados-*.json` (PII de leads + valores) e `paridade_esperado.json` sao regeneraveis e ficam fora do git; so o codigo versiona.
- **Paridade dos numeros:** garantida por a logica CM viver no Python (o exportador reusa as `queries_*.py`); o `motor.js` so agrega. Rodar via `uv`, nao `python` direto (no Windows o `python` do PATH e o shim da Store, exit 49; o `uv` provisiona Python 3.12 com wheels de C-extension).
- **Escopo 2026:** os exportadores cobrem 2026 + cauda p/ as series 12m. Virar 2027: ajustar `ANO_INI`/cutoff nos `exportar_dados.py`.
- **Diferencas por dashboard:** buzz-br = funil 7 KPIs, filtro em 3 superficies (auditar 0.2b), copia 3 arquivos. cxpress = funil 7 KPIs PT-BR, superficie unica, copia 5 arquivos. latam = funil 5 fases ES/USD, leads de inbound∪outbound + fechamentos de contratos, superficie unica, copia 5 arquivos. Runbooks: `dashboard/DEPLOY.md` (buzz-br) · `dashboard/DEPLOY-cxpress.md` · `dashboard/DEPLOY-latam.md`.
```
