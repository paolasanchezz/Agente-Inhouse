# Deploy do Dashboard Funil Inbound **Cxpress Brasil**


> ## 🔒 v3 — Guarda-chuva único (desde 2026-09-09) — **ESTE é o fluxo atual**
>
> A dashboard não tem mais projeto Vercel próprio: vive em **/cxpress/** dentro do guarda-chuva
> `dashboards-elife` (dashboards-elife.vercel.app), com **um único Basic Auth** e barra de
> navegação compartilhada. `dashboard-cxpress-brasil.vercel.app` agora é um **308** pra lá.
>
> **Deploy:** só pela skill `/dashboard-atualizar` (v4), que exporta → roda
> `dashboards-umbrella/build_umbrella.py` → deploya o guarda-chuva inteiro → valida.
> Arquitetura e pegadinhas em `dashboards-umbrella/README.md`.
>
> O que vem abaixo continua valendo pra **exportar dados, entender o funil e depurar
> números**. O que está aposentado é a parte de **sibling própria + deploy do projeto
> individual** (inclusive `sync_sibling.py`, que o build substituiu).

> ## ⚡ v2 — Dashboard dinâmica-estática (desde 2026-07-07) — **ESTE é o fluxo atual**
>
> A dashboard no Vercel virou **dinâmica-estática** (date-picker de intervalo livre + presets, igual à
> Buzzmonitor BR). Fonte em **`dashboard-cxpress-vercel/`**: `exportar_dados.py` reusa `queries_cxpress.py`
> e gera `dados-cxpress.json`; o navegador agrega por período com `motor.js` e desenha com `render.js`
> (port fiel de `gerar_relatorio_cxpress.render_html`), CSS em `estilo.css`. **Senha forte** (idêntica à do
> Buzzmonitor BR — não mais `inhouse@77`) + `X-Robots-Tag: noindex` + `robots.txt`.
> URL: https://dashboard-cxpress-brasil.vercel.app · projeto `dashboard-cxpress-brasil` (scope elife-group).
>
> **Redeploy (fluxo atual):**
> ```bash
> # 1. Exportar dados frescos (Supabase -> dados-cxpress.json)
> uv run --python 3.12 --with "psycopg[binary]" python dashboard-cxpress-vercel/exportar_dados.py
> # 2. (gate) paridade número-a-número vs a dash local (queries_cxpress) — 0 divergências pra seguir
> uv run --python 3.12 --with "psycopg[binary]" python dashboard-cxpress-vercel/paridade_gerar_esperado.py && node dashboard-cxpress-vercel/paridade_check.mjs
> # 3. Sincronizar a sibling (copia estáticos + gera middleware/vercel/robots com a senha do Buzz BR)
> uv run --python 3.12 python dashboard-cxpress-vercel/sync_sibling.py
> # 4. Deploy (dispara a trava guard_vercel_deploy — confirmar)
> vercel deploy --prod --yes --scope team_nC991VqUuSU2jXZN152xqqEg --cwd "C:/Users/titof/Downloads/Claude/dashboard-cxpress-brasil"
> # 5. Validar: sem auth = 401 · com a senha forte = 200 · dados-cxpress.json = 200
> ```
>
> O CÓDIGO em `dashboard-cxpress-vercel/` versiona; **`dados-cxpress.json`/`paridade_esperado.json` são
> gitignored** (PII de leads + valores). O restante deste doc descreve o **snapshot semanal estático
> (v1, aposentado)** — mantido só para histórico/recovery.

---

> Paralelo do `DEPLOY.md` (Buzzmonitor BR) e `DEPLOY-latam.md`. Mesmo padrão **sibling fora do repo**
> + Basic Auth na Vercel. Funil e mapeamento de campos: `dashboard/MAPEAMENTO-CAMPOS-cxpress.md`.

> **Inegociável:** deploy NUNCA sai de `dashboard/` no repo. Roda sempre da pasta sibling.
> O HTML gerado tem nomes de deals + valores → fica **fora do git** (`.gitignore`: `dashboard/relatorio-*.html`).

> **Status (2026-06-01):** a tabela `cxpress_deals_funil_principal_prod` está **vazia**. O gerador já roda
> (produz dashboard zerado). O **deploy só faz sentido depois da 1ª carga de dados** — e idealmente depois de
> calibrar escopo/datas (ver MAPEAMENTO §2/§5). Até lá, este doc fica pronto para o dia D.

## Componentes

| Item | Valor |
|---|---|
| Gerador | `dashboard/gerar_relatorio_cxpress.py` (usa `queries_cxpress.py` + `render_helpers_cxpress.py` + `render_helpers.py` + `datas.py`) |
| Dependência de CSS | O gerador **extrai o `<style>` de `relatorio-semanal-buzzmonitor-brasil.html`** em runtime (paridade visual; Cxpress tem 7 KPIs igual ao BR, então não há ajuste de grade). Esse arquivo do Brasil precisa existir localmente. |
| HTML gerado | `dashboard/relatorio-semanal-cxpress-brasil.html` (gitignored) |
| Sibling | `C:/Users/titof/Downloads/Claude/dashboard-cxpress-brasil/` (criar na 1ª vez) |
| Projeto Vercel | `dashboard-cxpress-brasil` (scope `team_nC991VqUuSU2jXZN152xqqEg` / elife-group) — criar no 1º deploy |
| URL (prevista) | https://dashboard-cxpress-brasil.vercel.app |
| Basic Auth | user `inhouse` · pass `inhouse@77` |
| Fonte de dados | Supabase `cxpress_deals_funil_principal_prod` (read-only, `SUPABASE_PG_URL` em `dashboard/.env`) |

## Conteúdo da sibling (espelhar a do BR/LATAM)

```
dashboard-cxpress-brasil/
├── index.html        ← cópia do dashboard/relatorio-semanal-cxpress-brasil.html
├── middleware.js     ← Basic Auth (user: inhouse, pass: inhouse@77) — copiar de dashboard-buzzmonitor-latam/
├── vercel.json       ← headers de segurança — copiar de dashboard-buzzmonitor-latam/
├── package.json
└── .vercel/          ← criado/linkado no 1º `vercel deploy`
```

## Fluxo (do zero) — versão publicada

```powershell
# 1. Gerar HTML novo (lê o Supabase, monta o HTML PT-BR/BRL com o funil Cxpress)
uv run --python 3.12 --with "psycopg[binary]" python dashboard/gerar_relatorio_cxpress.py

# 2. Copiar HTML pra sibling como index.html
cp "dashboard/relatorio-semanal-cxpress-brasil.html" "C:/Users/titof/Downloads/Claude/dashboard-cxpress-brasil/index.html"

# 3. Deploy da sibling (1ª vez: o Vercel pergunta o nome do projeto → dashboard-cxpress-brasil)
vercel deploy --prod --yes --scope team_nC991VqUuSU2jXZN152xqqEg --cwd "C:/Users/titof/Downloads/Claude/dashboard-cxpress-brasil"

# 4. Verificar (sem auth = 401; com auth = 200)
curl -s -o /dev/null -w "%{http_code}`n" "https://dashboard-cxpress-brasil.vercel.app/"                       # espera 401
curl -s -u "inhouse:inhouse@77" -o /dev/null -w "%{http_code}`n" "https://dashboard-cxpress-brasil.vercel.app/" # espera 200
```

## Rollback

```powershell
vercel rollback <dpl_id_anterior_READY> --yes --scope team_nC991VqUuSU2jXZN152xqqEg --cwd "C:/Users/titof/Downloads/Claude/dashboard-cxpress-brasil"
```

Listar deploys: `vercel ls dashboard-cxpress-brasil --cwd "C:/Users/titof/Downloads/Claude/dashboard-cxpress-brasil"`.

## Pendências antes do go-live (ver MAPEAMENTO-CAMPOS-cxpress.md)

- **Dados:** tabela vazia em 2026-06-01 — aguardando 1ª sincronização AC→Supabase.
- **Datas em texto** (§5): confirmar formato ISO das colunas `data_*_auto`; ajustar `_d()` se vier DMY/MDY.
- **Escopo** (§2): decidir inbound-completo vs só-CM e calibrar `filtro_inbound()`/`filtro_cm()`.
- **Baseline:** fixar números-âncora YtD após a 1ª carga validada (e considerar smoke test no gerador).
