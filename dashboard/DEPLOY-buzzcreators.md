# Deploy do Dashboard CM **Buzzcreators Brasil**

Paralelo de `DEPLOY.md` (Buzzmonitor BR), `DEPLOY-cxpress.md` e `DEPLOY-latam.md`.
Mesmo padrão **sibling fora do repo** + Basic Auth com a senha forte do Buzz BR.
Funil, filtro CM e mapeamento de campos: `dashboard/MAPEAMENTO-CAMPOS-buzzcreators.md`.

> **Inegociável:** deploy NUNCA sai do repo. Roda sempre da pasta sibling.
> O JSON de dados tem nome de deal + valores → fica **fora do git** (`.gitignore`).

> **A dashboard nasce dinâmica-estática** (date-picker de intervalo livre + presets, igual às
> outras três). Não existe versão local em Python nem snapshot estático.

## Componentes

| Item | Valor |
|---|---|
| Lógica CM (fonte única) | `dashboard/queries_buzzcreators.py` |
| Fonte no repo | `dashboard-buzzcreators-vercel/` (`exportar_dados.py`, `motor.js`, `render.js`, `estilo.css`, `index.html`) |
| Dados | `dados-buzzcreators.json` (gitignored — PII) |
| Sibling | `{DASHBOARD_SIBLING_BASE}/dashboard-buzzcreators-brasil/` (criada pelo `sync_sibling.py`, que gera tambem o `package.json`) |
| Projeto Vercel | `dashboard-buzzcreators-brasil` (scope `team_nC991VqUuSU2jXZN152xqqEg` / elife-group) |
| URL | https://dashboard-buzzcreators-brasil.vercel.app (no ar desde 26/08/2026) |
| Basic Auth | user + senha forte, copiados do middleware do Buzz BR (ninguém digita senha) |
| Fonte de dados | Supabase: `deals_pipedrive_vendas_buzzcreators` + `dim_pipedrive_persons` + `dim_contacts` (read-only, `SUPABASE_PG_URL` em `dashboard/.env`) |

## Redeploy (fluxo atual)

```bash
# 1. Exportar dados frescos (Supabase -> dados-buzzcreators.json)
uv run --python 3.12 --with "psycopg[binary]" python dashboard-buzzcreators-vercel/exportar_dados.py
```

```bash
# 2. (gate) paridade SQL x motor.js — 0 divergências pra seguir
uv run --python 3.12 --with "psycopg[binary]" python dashboard-buzzcreators-vercel/paridade_gerar_esperado.py && node dashboard-buzzcreators-vercel/paridade_check.mjs
```

```bash
# 3. Sincronizar a sibling (estáticos + middleware/vercel/robots com a senha do Buzz BR)
uv run --python 3.12 python dashboard-buzzcreators-vercel/sync_sibling.py
```

```bash
# 4. Deploy (dispara a trava guard_vercel_deploy — confirmar; só dentro de /dashboard-atualizar)
vercel deploy --prod --yes --scope team_nC991VqUuSU2jXZN152xqqEg --cwd "C:/Users/titof/Downloads/Claude/dashboard-buzzcreators-brasil"
```

```bash
# 5. Validar: sem auth = 401 · com a senha forte = 200 · dados-buzzcreators.json = 200
curl -s -o /dev/null -w "%{http_code}\n" "https://dashboard-buzzcreators-brasil.vercel.app/"
```

## Preview local (sem deploy)

```bash
py -m http.server 8030 --bind 127.0.0.1 --directory dashboard-buzzcreators-vercel
```

Porta 8030 — as outras dashboards locais usam 8000 (Buzz BR), 8010 (LATAM) e 8020 (Cxpress).

## Rollback

```bash
vercel rollback <dpl_id_anterior_READY> --yes --scope team_nC991VqUuSU2jXZN152xqqEg --cwd "C:/Users/titof/Downloads/Claude/dashboard-buzzcreators-brasil"
```

## Antes de mostrar pra alguém de fora do time de CM

Três avisos que precisam ir junto com o link (e que a própria dashboard exibe no rodapé):

1. A atribuição é **recuperada do contato** e é **last touch** — não é o toque que gerou o deal.
2. **Não existe etapa Proposta** neste funil (o Pipedrive não registra a data).
3. **Julho e agosto de 2026 estão com a captura de UTM degradada** — a queda aparente pode ser
   instrumentação, não performance. Ver §1 do MAPEAMENTO.
