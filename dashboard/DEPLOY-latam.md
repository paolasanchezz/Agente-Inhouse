# Deploy do Dashboard CM Buzzmonitor **LATAM**

> Paralelo do `DEPLOY.md` (Brasil). Mesmo padrão **sibling fora do repo** + Basic Auth na Vercel.
> Critério de CM e mapeamento de campos: `dashboard/MAPEAMENTO-CAMPOS-latam.md`.

> **Inegociável:** deploy NUNCA sai de `dashboard/` no repo. Roda sempre da pasta sibling.
> O HTML gerado tem nomes de deals + valores → fica **fora do git** (`.gitignore`: `dashboard/relatorio-*.html`).

## Componentes

| Item | Valor |
|---|---|
| Gerador | `dashboard/gerar_relatorio_latam.py` (usa `queries_latam.py` + `render_helpers_latam.py` + `datas.py`) |
| Dependência de CSS | O gerador **extrai o `<style>` de `relatorio-semanal-buzzmonitor-brasil.html`** em runtime (paridade visual; muda só KPI 7→5 colunas). Esse arquivo do Brasil precisa existir localmente para gerar. |
| HTML gerado | `dashboard/relatorio-semanal-buzzmonitor-latam.html` (gitignored) |
| Sibling | `C:/Users/titof/Downloads/Claude/dashboard-buzzmonitor-latam/` |
| Projeto Vercel | `dashboard-buzzmonitor-latam` (scope `team_nC991VqUuSU2jXZN152xqqEg` / elife-group) |
| URL | https://dashboard-buzzmonitor-latam.vercel.app |
| Basic Auth | user `inhouse` · pass `inhouse@77` |
| Fonte de dados | Supabase `deals_latam_*_staging` (read-only, `SUPABASE_PG_URL` em `dashboard/.env`) |

## Duas versões

| Versão | O que é | Seletor de data | Onde roda |
|---|---|---|---|
| **Publicada** (esta) | Snapshot semanal estático | Não (3 períodos fixos: Semana/MtD/YtD) | Vercel (URL acima) |
| **Dinâmica** | Date-picker livre + presets, consulta ao vivo | **Sim** | **Local** (`dashboard-latam/server.py` → http://127.0.0.1:8010) — ver `dashboard-latam/README.md` |

As duas usam o mesmo critério CM e o mesmo render (`gerar_relatorio_latam.render_html`).

## Fluxo (do zero) — versão publicada

```bash
# 1. Gerar HTML novo (lê o Supabase, monta o HTML em ES/USD)
uv run --python 3.12 --with "psycopg[binary]" python dashboard/gerar_relatorio_latam.py

# 2. Copiar HTML pra sibling como index.html
cp "dashboard/relatorio-semanal-buzzmonitor-latam.html" "C:/Users/titof/Downloads/Claude/dashboard-buzzmonitor-latam/index.html"

# 3. Deploy da sibling
vercel deploy --prod --yes --scope team_nC991VqUuSU2jXZN152xqqEg --cwd "C:/Users/titof/Downloads/Claude/dashboard-buzzmonitor-latam"

# 4. Verificar (sem auth = 401; com auth = 200)
curl -s -o /dev/null -w "%{http_code}\n" "https://dashboard-buzzmonitor-latam.vercel.app/"           # espera 401
curl -s -u "inhouse:inhouse@77" -o /dev/null -w "%{http_code}\n" "https://dashboard-buzzmonitor-latam.vercel.app/"  # espera 200
```

## Rollback

```bash
vercel rollback <dpl_id_anterior_READY> --yes --scope team_nC991VqUuSU2jXZN152xqqEg --cwd "C:/Users/titof/Downloads/Claude/dashboard-buzzmonitor-latam"
```

## Pendências conhecidas (ver MAPEAMENTO-CAMPOS-latam.md §6/§7)

- **Gap de ETL (UTM):** `deals_latam_inbound_staging` está com UTM/URL vazios → cobertura parcial de CM.
  Pedir backfill à engenharia de dados. Quando resolver, a contagem de leads CM sobe.
- **Gap de ETL (pipeline Nutrición) — leads/perdidos SUBESTIMADOS:** o Supabase só sincroniza os pipelines
  `Processo Inbound Latam` e `Processo Outbound Latam`. Leads perdidos e movidos para o pipeline **Nutrición**
  saem do conjunto (ex.: deal 43318 e a faixa 43318–43322 não estão em nenhuma tabela). Efeito: **Perdidos**
  conta só os `status='Perdido'` ainda no Inbound (≈616 hist.); **Leads** encolhe à medida que deals migram.
  Conserto: pedir à engenharia para **sincronizar o pipeline Nutrición** (e quaisquer outros) no Supabase.
- **Fechamentos a validar:** `fee_mensual` (valor) e datas de cierre são aproximados — validar com o time LATAM e fixar baseline.
- **Tabelas `_staging`:** revalidar schema/números se forem promovidas a `_prod`.
