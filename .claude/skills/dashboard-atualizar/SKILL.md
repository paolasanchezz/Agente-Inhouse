---
name: dashboard-atualizar
description: Atualiza as dashboards CM dinamica-estaticas servidas no guarda-chuva unico do Vercel — Brasil (Buzzmonitor, Cxpress, Buzzcreators), LATAM e Portugal (Buzzmonitor, Cxpress, Elife), todas atras de um unico login em dashboards-elife.vercel.app. Roda o exportador Python (Supabase -> JSON de dados), monta a dist do guarda-chuva com build_umbrella.py, deploya na Vercel via CLI e valida (senha + noindex + as 7 rotas servidas). Manual-trigger.
argument-hint: "[buzz-br|cxpress|latam|buzzcreators|bm-pt|cxpress-pt|elife-pt|pt|todas] (sem arg = pergunta com chips)"
allowed-tools: AskUserQuestion, Read, Edit, Bash, Glob, Grep
version: 4.1.0
---

# Skill: Atualizar Dashboards CM (guarda-chuva unico)

Voce atualiza as dashboards de Content Marketing servidas **dinamica-estaticas** no Vercel. Todas seguem o MESMO modelo: os dados sao exportados aqui (onde o Supabase conecta) e embutidos num JSON; o navegador filtra/agrega em memoria com date-picker de intervalo livre (sem tocar no banco).

Desde 2026-09-09 elas nao sao mais 4 projetos Vercel soltos: vivem num **guarda-chuva unico** (`dashboards-elife`), cada uma numa rota, com **um unico Basic Auth** e uma **barra de navegacao compartilhada** no topo. Foi exatamente isso que motivou a unificacao — Basic Auth e por origem, entao 4 subdominios pediam a senha 4 vezes.

| Dashboard | Rota | Fonte no repo | Idioma/moeda |
|---|---|---|---|
| **buzz-br** | `/buzz-br/` | `dashboard-buzz-br-vercel/` | PT-BR / BRL |
| **cxpress** | `/cxpress/` | `dashboard-cxpress-vercel/` | PT-BR / BRL |
| **latam** | `/latam/` | `dashboard-latam-vercel/` | ES / USD |
| **buzzcreators** | `/buzzcreators/` | `dashboard-buzzcreators-vercel/` | PT-BR / BRL |
| **bm-pt** | `/bm-pt/` | `dashboard-pt-vercel/` | PT-PT / EUR |
| **cxpress-pt** | `/cxpress-pt/` | `dashboard-pt-vercel/` | PT-PT / EUR |
| **elife-pt** | `/elife-pt/` | `dashboard-pt-vercel/` | PT-PT / EUR |

Hub com os cards na raiz (`/`). Projeto: **`dashboards-elife`** · URL: **dashboards-elife.vercel.app**.

**As 3 de Portugal dividem uma fonte só.** Mesmo ActiveCampaign, mesmo schema de 84 colunas, mesmo dicionário de etapas — então `dashboard-pt-vercel/` tem UM `index.html` (que descobre a marca pelo path da rota), UM `motor.js`, UM `render.js` e um exportador com `--marca`. Não replique arquivo por marca: foi justamente a divergência entre BR/LATAM/Cxpress que criou o problema de sincronia manual. A lógica é fonte única em `dashboard/queries_portugal.py`.

**PT tem um modelo diferente do BR/LATAM** e isso é deliberado, não falta de acabamento: em Portugal nenhum marco de funil tem data (não há data de reunião, de proposta nem de fecho, e não existe histórico de etapa), então o período define uma **coorte por data de criação** e o painel mostra a **distribuição de etapa atual** — nunca conversão entre etapas. CM é **classificação** (`cm` / `nao_cm` / `sem_rastreio`), não filtro, porque 21% a 50% dos deals não têm rastreio nenhum. Evidências e decisões em `dashboard/AUDITORIA-PORTUGAL.md`.

**Regra inegociavel:** deploy NUNCA sai da pasta-fonte no repo. Sempre da **dist/sibling** fora do repo, montada pelo `dashboards-umbrella/build_umbrella.py` (que escreve `middleware.js` + `vercel.json` + `robots.txt` + `package.json`). Mesmo padrao do `lp-publicar`. Incidente 2026-05-25 (404 publico por deploy sem middleware) em `dashboard/DEPLOY.md`.

**Seguranca:** o dominio publico e protegido por **senha forte** (Basic Auth no middleware) — o Vercel SSO Standard so cobre URLs internas de deploy, nao o dominio principal ([[reference_vercel_deployment_protection]]). Credencial em `.env.local` (`DASHBOARD_BASIC_AUTH_USER`/`_PASS`); o build a injeta no middleware. Um login cobre as 7.

**O guarda-chuva deploya inteiro, sempre.** Nao existe deploy de uma rota so. Atualizar uma dashboard = exportar o JSON dela e rebuildar tudo; os JSONs das outras vem das pastas-fonte (ou, se faltarem, o build reusa o que ja esta na dist e **avisa** — nunca em silencio).

---

## Passo A: Resolver QUAIS dashboards exportar

1. Se `$ARGUMENTS` trouxer um slug, normalizar (case-insensitive):
   - `buzz-br`, `br`, `brasil`, `buzz`, `buzzmonitor`, `buzz-brasil` → **buzz-br**
   - `cxpress`, `cx`, `cxpress-brasil` → **cxpress**
   - `latam`, `lat`, `buzz-latam` → **latam**
   - `buzzcreators`, `creators`, `bc`, `buzzcreators-brasil` → **buzzcreators**
   - `bm-pt`, `buzz-pt`, `buzzmonitor-portugal` → **bm-pt**
   - `cxpress-pt`, `cx-pt`, `cxpress-portugal` → **cxpress-pt**
   - `elife-pt`, `elife`, `elife-portugal` → **elife-pt**
   - `pt`, `portugal` → **as 3 de Portugal** (um unico export cobre as 3)
   - `todas`, `all`, `tudo` → **as 7** (export sequencial; leva 8-15min)
2. Se ausente ou nao reconhecido, use **AskUserQuestion** (header "Dashboard") com: `Buzzmonitor Brasil` / `Cxpress Brasil` / `Buzzmonitor LATAM` / `Buzzcreators Brasil` / `Portugal (as 3)` / `Todas` (multiSelect ligado).

Fixe a lista resolvida em `$DASHES` (separada por espaco) e rode o bloco de config:

```bash
DASHES="<slugs separados por espaco>"   # resolvido no Passo A
SCOPE=team_nC991VqUuSU2jXZN152xqqEg
PROJ=dashboards-elife
URL=dashboards-elife.vercel.app

# config por dashboard: SRC | JSON | chave principal | marcador do motor | audita 3 superficies | args do exportador
cfg() {
  case "$1" in
    buzz-br)      echo "dashboard-buzz-br-vercel dados-2026.json leads MotorCM 1 -" ;;
    cxpress)      echo "dashboard-cxpress-vercel dados-cxpress.json deals MotorCxpress 0 -" ;;
    latam)        echo "dashboard-latam-vercel dados-latam.json leads MotorLatam 0 -" ;;
    buzzcreators) echo "dashboard-buzzcreators-vercel dados-buzzcreators.json deals MotorBuzzcreators 0 -" ;;
    bm-pt)        echo "dashboard-pt-vercel dados-pt-bm.json deals MotorPT 0 --marca=bm" ;;
    cxpress-pt)   echo "dashboard-pt-vercel dados-pt-cxpress.json deals MotorPT 0 --marca=cxpress" ;;
    elife-pt)     echo "dashboard-pt-vercel dados-pt-elife.json deals MotorPT 0 --marca=elife" ;;
    *) echo ""; return 1 ;;
  esac
}
# Atalho: `pt` exporta as 3 de Portugal numa passagem so (um exportador, 3 JSONs).
[ "$DASHES" = "pt" ] && DASHES="bm-pt cxpress-pt elife-pt"
for D in $DASHES; do cfg "$D" >/dev/null || { echo "ERRO: dashboard invalido: '$D'"; exit 1; }; done
echo "Vou exportar: $DASHES · projeto: $PROJ · url: $URL"
```

---

## Passo 0: Pre-flight

### 0.1 Resolver a dist (sibling do guarda-chuva)
```bash
SIBLING_BASE="${DASHBOARD_SIBLING_BASE}"
if [ -z "$SIBLING_BASE" ] && [ -f .env.local ]; then
  SIBLING_BASE=$(grep -E '^DASHBOARD_SIBLING_BASE=' .env.local | head -1 | sed 's/^[^=]*=//')
fi
[ -z "$SIBLING_BASE" ] && { echo "ERRO: DASHBOARD_SIBLING_BASE nao configurado em .env.local"; exit 1; }
SIBLING="$SIBLING_BASE/$PROJ"
```

### 0.2 Verificar repo + fontes + env do Supabase
- `git rev-parse --show-toplevel` deve resolver (rode da raiz do repo).
- `dashboards-umbrella/manifest.json` e `build_umbrella.py` devem existir.
- `dashboard/.env` (ou `dashboard-pessoal/.env`) deve ter `SUPABASE_PG_URL=` — o exportador reusa a conexao/queries da dash local.

### 0.2b Auditar sincronia do filtro CM — **so se `buzz-br` estiver em `$DASHES`**
O buzz-br tem o filtro CM em 3 superficies sincronizadas a mao (`dashboard/queries.py` oficial × `dashboard-pessoal/lib/queries.py` espelho, que o exportador usa). Se divergirem, sobe deals errados (caso ECHEF ROBOT, 2026-07-01):

```bash
case " $DASHES " in *" buzz-br "*)
uv run --python 3.12 python -c "
import importlib.util
def L(p,n):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
o=L('dashboard/queries.py','o'); e=L('dashboard-pessoal/lib/queries.py','e'); d=False
for a in ['CM_UTM_SOURCES','CM_UTM_SOURCE_PREFIXOS','EMAIL_WHITELIST','EMAIL_BLACKLIST','INTERNOS_EXCLUIR','HERANCA_SOURCES_INTERNAS','CM_SLUGS_PREFIXES']:
    A,B=set(getattr(o,a)),set(getattr(e,a))
    if A^B: d=True; print(f'{a}: so_oficial={sorted(A-B)} so_espelho={sorted(B-A)}')
for a in ['CM_DEALS_FORCADOS','FECHAMENTOS_FORCADOS','RECONVERSOES_MANUAIS','DEALS_EXCLUIDOS_URL_DATA']:
    if getattr(o,a)!=getattr(e,a): d=True; print(f'{a}: DIFERENTE')
for fn in ['filtro_cm','filtro_inbound','_sem_outbound']:
    if getattr(o,fn)() != getattr(e,fn)(): d=True; print(f'{fn}(): SQL DIFERENTE entre oficial e espelho')
print('FILTRO SINCRONIZADO' if not d else 'DESSINCRONIZADO — replicar no espelho ANTES de exportar')
" ;;
esac
```
Se **DESSINCRONIZADO**: replicar em `dashboard-pessoal/lib/queries.py` e so entao seguir.

> **cxpress / latam / buzzcreators:** superficie UNICA — o exportador importa `queries_cxpress.py` / `queries_latam.py` / `queries_buzzcreators.py` direto de `dashboard/` (sem espelho). Nao ha o que auditar aqui; a paridade (Passo 1.5) cobre a consistencia motor × queries.

### 0.3 Verificar a dist
Deve ter `$SIBLING/.vercel/project.json` apontando pro projeto `dashboards-elife`.
- Faltando `.vercel/`: `mkdir -p "$SIBLING" && (cd "$SIBLING" && npx vercel link --yes --project="$PROJ" --scope="$SCOPE")`
- `middleware.js`/`vercel.json`/`robots.txt`/`package.json` **nao** precisam existir: o `build_umbrella.py` regenera os quatro a cada build (essa e a diferenca pro modelo antigo de sibling, onde eles eram preservados a mao).

### 0.4 Vercel CLI auth
```bash
npx --yes vercel whoami --scope="$SCOPE"
```
Exit != 0: abortar (`Rode 'npx vercel login' e re-execute`).

### 0.5 Resolver credencial Basic Auth
```bash
BASIC_AUTH_USER=$(grep -E '^DASHBOARD_BASIC_AUTH_USER=' .env.local | head -1 | sed 's/^[^=]*=//')
BASIC_AUTH_PASS=$(grep -E '^DASHBOARD_BASIC_AUTH_PASS=' .env.local | head -1 | sed 's/^[^=]*=//')
[ -z "$BASIC_AUTH_PASS" ] && { echo "ERRO: DASHBOARD_BASIC_AUTH_PASS ausente em .env.local"; exit 1; }
TODAY=$(date +%Y-%m-%d); mkdir -p tmp
```
O build le a mesma fonte, entao aqui nao existe mais o risco de `.env.local` divergir do middleware.

---

## Passo 1: Exportar dados frescos + sanity (por dashboard escolhida)

```bash
for D in $DASHES; do
  set -- $(cfg "$D"); SRC=$1; JSON=$2; MAIN=$3; ARGS=$6
  [ "$ARGS" = "-" ] && ARGS=""
  echo "=== exportando $D"
  uv run --python 3.12 --with "psycopg[binary]" python "$SRC/exportar_dados.py" $ARGS 2>&1 | tee "tmp/dash-$D-export-$TODAY.log"
  [ "${PIPESTATUS[0]}" = "0" ] || { echo "ERRO no export de $D"; exit 1; }
  uv run --python 3.12 python -c "
import json,os
p='$SRC/$JSON'; d=json.load(open(p,encoding='utf-8')); sz=os.path.getsize(p)
assert d.get('gerado_em'), 'falta gerado_em'
assert isinstance(d.get('$MAIN'),list) and len(d['$MAIN'])>0, '$MAIN vazio/ausente'
assert sz < 3_400_000, f'JSON grande demais: {sz}b (rever campos/compressao)'
print(f'sanity OK ($D) — $MAIN={len(d[\"$MAIN\"])} gerado_em={d[\"gerado_em\"]} tamanho={sz//1024}KB')
" || { echo "ERRO no sanity de $D"; exit 1; }
done
```
- Export normal leva 1-3min por dashboard (conexao cold + queries). Exit != 0: abortar e propagar as ultimas 15 linhas do log (Supabase fora, statement_timeout, import).
- Falhou o sanity: abortar (nao buildar/deployar dados suspeitos).

---

## Passo 1.5: Paridade numero-a-numero (recomendado; **obrigatorio se mexeu no codigo**)

O motor JS so bate com a dash local se `motor.js`/`render.js`/as queries nao divergirem. Rode se voce **alterou** motor/render/queries desde o ultimo deploy (em atualizacao de dados rotineira o motor e o mesmo — pode pular):

```bash
for D in $DASHES; do
  set -- $(cfg "$D"); SRC=$1
  # Portugal nao tem harness de paridade: nao existe dash local PT com que comparar,
  # e a logica toda mora em queries_portugal.py (o motor.js so agrega a coorte).
  [ -f "$SRC/paridade_gerar_esperado.py" ] || { echo "$D: sem harness de paridade — pulando"; continue; }
  uv run --python 3.12 --with "psycopg[binary]" python "$SRC/paridade_gerar_esperado.py" && node "$SRC/paridade_check.mjs"
done
```
Deve terminar em **0 divergencias**. Qualquer divergencia: corrigir o motor/render antes de deployar (nao suba numeros errados).

---

## Passo 2: Montar a dist do guarda-chuva

Substitui a copia manual do modelo antigo. O build copia so os arquivos listados no manifesto, injeta a barra de navegacao no `<head>` de cada dashboard, gera o hub e regenera middleware/vercel.json/robots.txt/package.json:

```bash
py dashboards-umbrella/build_umbrella.py "$SIBLING" --dry-run   # confere o plano
py dashboards-umbrella/build_umbrella.py "$SIBLING"
```

**Leia os `AVISO` do build.** `REUSADO` significa que o JSON daquela dashboard nao existia na fonte e o build aproveitou o que ja estava no ar — os numeros dela vao subir com a data antiga. Se nao era isso que voce queria, exporte a dashboard e rebuilde.

Adicionar uma dashboard nova ao guarda-chuva = uma entrada em `dashboards-umbrella/manifest.json` (slug, nome, curto, cor, fonte, arquivos, dados) + uma entrada na `cfg()` do Passo A. Nada mais: nav, hub e rota saem do manifesto.

---

## Passo 3: Deploy

```bash
npx --yes vercel deploy --prod --yes --cwd "$SIBLING" --scope="$SCOPE" 2>&1 | tee "tmp/dash-deploy-$TODAY.log"
NEW_DPL_ID=$(grep -oE 'dpl_[a-zA-Z0-9]+' "tmp/dash-deploy-$TODAY.log" | head -1)
```
- Linha `▲ Aliased https://$URL` = alias bateu, seguir. Se nao aparecer (raro, pos-rollback): `npx vercel promote "$NEW_DPL_ID" --cwd "$SIBLING" --scope="$SCOPE"`.
- `FetchError` intermitente da CLI: nao retry cego — `npx vercel ls "$PROJ" --cwd "$SIBLING" --scope="$SCOPE" | head -5` e ver se ficou READY.
- O hook `guard_vercel_deploy.py` vai pedir confirmacao. Estar **dentro desta skill** e o contexto sancionado — confirme. Fora dela, recuse.

---

## Passo 4: Validacao (as garantias)

```bash
B="https://$URL"; A="$BASIC_AUTH_USER:$BASIC_AUTH_PASS"
echo "sem auth (espera 401):    $(curl -s -o /dev/null -w '%{http_code}' "$B/")"
echo "hub     (espera 200):     $(curl -s -u "$A" -o tmp/v-hub.html -w '%{http_code} %{size_download}b' "$B/")"
echo "nav.js  (espera 200):     $(curl -s -u "$A" -o /dev/null -w '%{http_code} %{size_download}b' "$B/nav.js")"
echo -n "senha fraca antiga (espera 401): "; curl -s -u "inhouse:inhouse@77" -o /dev/null -w '%{http_code}\n' "$B/"
curl -s -D - -o /dev/null -u "$A" "$B/" | grep -i 'x-robots-tag'

# as 7 rotas: 308 sem barra, 200 com barra, motor certo, JSON servido
for D in buzz-br cxpress latam buzzcreators bm-pt cxpress-pt elife-pt; do
  set -- $(cfg "$D"); JSON=$2; MARKER=$4
  R=$(curl -s -u "$A" -o /dev/null -w '%{http_code}' "$B/$D")
  H=$(curl -s -u "$A" -o "tmp/v-$D.html" -w '%{http_code}' "$B/$D/")
  J=$(curl -s -u "$A" -o /dev/null -w '%{http_code}' "$B/$D/$JSON")
  N=$(grep -c '/nav.js' "tmp/v-$D.html")
  M=$(grep -c "$MARKER" "tmp/v-$D.html")
  echo "$D: /$D=$R(308) /$D/=$H(200) $JSON=$J(200) nav=$N(1) $MARKER=$M(>=1)"
done
```
Esperado: 401 sem auth · 200 no hub e no `nav.js` · `X-Robots-Tag: noindex` · 401 com a senha fraca antiga · para cada rota **308 sem barra**, **200 com barra**, JSON 200, `nav.js` injetado, motor certo.

**Erros:**
- **401 com a credencial certa:** o build rodou com `.env.local` diferente do que voce esta testando. Rebuildar e re-deployar.
- **Rota 200 mas pagina quebrada / JSON 404:** provavel `trailingSlash` fora do lugar no `vercel.json` — as dashboards carregam `motor.js`/`estilo.css`/`dados-*.json` por caminho **relativo**, entao `/buzz-br` sem barra resolveria `/motor.js`. O 308 tem que vir antes de renderizar.
- **404 no root:** deploy saiu sem index.html (incidente 2026-05-25). Rollback: `npx vercel rollback <dpl_anterior_READY> --yes --cwd "$SIBLING" --scope="$SCOPE"`.
- **Rota servindo versao velha:** o build nao rodou depois do export — refazer o Passo 2.

---

## Passo 5: Relatorio

```
============================================================
Dashboards CM — guarda-chuva atualizado
============================================================
Hub:        https://dashboards-elife.vercel.app/  (login: inhouse + senha do .env.local)
Deploy ID:  $NEW_DPL_ID · READY
Exportadas: $DASHES
No ar:      /buzz-br/ · /cxpress/ · /latam/ · /buzzcreators/ · /bm-pt/ · /cxpress-pt/ · /elife-pt/
Navegacao:  barra no topo de todas as paginas; um unico login cobre as 7.

Rollback rapido: npx vercel rollback <dpl_anterior> --cwd "$SIBLING" --scope="$SCOPE"
Pra commitar mudancas de codigo (se houve): /commit
```

---

## Notas de seguranca e manutencao
- **Credencial Basic Auth** vive so em `.env.local` (`DASHBOARD_BASIC_AUTH_USER`/`_PASS`, gitignored). O `build_umbrella.py` a injeta no `middleware.js` da dist. Trocar a senha = editar o `.env.local` + rebuildar + deployar. Nunca hardcodar nesta skill nem no repo.
- **Nunca** rodar `vercel deploy` da pasta-fonte no repo (sem middleware = 404/exposto). So da dist.
- **Nunca** copiar arquivo pra dist a mao — o build e a unica porta de entrada, e ele remove o que nao esta no manifesto.
- **Dados gitignored:** `dados-*.json` (PII de leads + valores) e `paridade_esperado.json` sao regeneraveis e ficam fora do git; so o codigo versiona. Num clone novo, exporte todas antes do primeiro build (`--marca todas` cobre as 3 de Portugal de uma vez).
- **Projetos antigos** (`dashboard-buzzmonitor-brasil`, `dashboard-cxpress-brasil`, `dashboard-buzzmonitor-latam`, `dashboard-buzzcreators-brasil`) viraram **redirect 308** pro guarda-chuva — os links antigos continuam funcionando. Nao deployar dashboard neles.
- **Paridade dos numeros:** garantida por a logica CM viver no Python (o exportador reusa as `queries_*.py`); o `motor.js` so agrega. Rodar via `uv`, nao `python` direto (no Windows o `python` do PATH e o shim da Store, exit 49; o `uv` provisiona Python 3.12 com wheels de C-extension).
- **Escopo 2026:** os exportadores cobrem 2026 + cauda p/ as series 12m. Virar 2027: ajustar `ANO_INI`/cutoff nos `exportar_dados.py`.
- **Portugal:** as 3 rotas PT saem de `dashboard-pt-vercel/` (fonte compartilhada) e da logica unica
  em `dashboard/queries_portugal.py`. Modelo proprio — coorte por data de criacao, distribuicao de
  etapa atual (nao conversao), CM como classificacao. O porque esta em `dashboard/AUDITORIA-PORTUGAL.md`;
  nao "corrigir" isso pra parecer com o BR sem antes reler a auditoria.
- **Diferencas por dashboard:** buzz-br = funil 7 KPIs, filtro em 3 superficies (auditar 0.2b), CSS inline. cxpress = funil 7 KPIs PT-BR, superficie unica. latam = funil 5 fases ES/USD, leads de inbound∪outbound + fechamentos de contratos, superficie unica. buzzcreators = funil 5 KPIs (Lead/Agend./Reuniao/Fech./Perdidos — **sem Proposta**), fonte Pipedrive com **UTM recuperada por join com o contato** (o deal nao tem UTM), superficie unica. Runbooks: `dashboard/DEPLOY.md` (buzz-br) · `dashboard/DEPLOY-cxpress.md` · `dashboard/DEPLOY-latam.md` · `dashboard/DEPLOY-buzzcreators.md`.
