---
name: seo-report
description: Dashboard de SEO multi-marca e multi-regiao (Buzzmonitor, Cxpress e Elife x BR/LATAM/PT). Semrush via MCP, artigos que mais convertem via Supabase (so BR) e GSC + GA4 onde houver acesso. Gera HTML interativo e, sob pedido, relatorio executivo no Notion.
argument-hint: "[contexto?] — buzzmonitor-br | buzzmonitor-latam | buzzmonitor-pt | cxpress-br | cxpress-latam | cxpress-pt | elife-br | elife-pt | todos (default)"
allowed-tools: Bash, Read, Write, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__execute_report, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__get_report_schema, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__domain_overview, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__organic_research, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-fetch, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-create-pages, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-update-page, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-search
version: 2.6.1
---

# /seo-report — Dashboard SEO multi-marca (Buzzmonitor + Cxpress + Elife)

## O que esta skill faz

Gera 1 dashboard HTML com até **8 contextos** (marca × região), cada um trazendo:

1. **Semrush** (via MCP, todos os 8 contextos, sempre disponível):
   a. Evolução histórica de keywords ranqueadas (série mensal completa)
   b. Distribuição Top3 / Top10 (buckets nativos do Semrush)
   c. Ganho/perda de posicionamento (keywords novas, perdidas, subindo, caindo)
   d. Páginas que mais ranqueiam (por nº de keywords/tráfego)
   e. **Interesse de marca por país — BM LATAM** (Alessandro, v2.6.0): volume de busca mensal de "buzzmonitor" + "buzz monitor" nos 4 principais países da LATAM (México, Argentina, Colombia, Chile) — gráfico de linhas multi-série por país, últimos 12 meses
   f. **Visibilidade em AI Overviews do Google** (Alexandre, v2.6.0): quais keywords ranqueadas acionam AI Overview na SERP; contagem e % por contexto; tabela das keywords Top10 com AI Overview presente
2. **Supabase** (item e — artigos que mais convertem em vendas): só **Buzzmonitor BR** e **Cxpress BR**, únicas marcas com tabela de deals em produção. Por post: nº de fechamentos, receita somada, ticket médio, cluster (best-effort). Elife não entra nesse item — sem tabela de deals equivalente mapeada ainda.
3. **Google Search Console + GA4**: só nos contextos com credencial configurada (ver tabela de cobertura abaixo). Onde não houver, a seção fica com um card "fonte não configurada" (ou "fonte não existe ainda", quando for o caso — ver Cxpress LATAM/PT) — não bloqueia o resto do dashboard.

> **Por que não tem chave de API no repo:** Semrush vem do MCP (autenticado fora do código). Google usa OAuth com credenciais **locais por usuário** (`client_secret.json`/`token.json`, fora do repo). Supabase usa o mesmo Postgres read-only já usado pelas dashboards CM (`dashboard/.env`, gitignored).

---

## Cobertura por contexto (atualizada 2026-10-07)

| Contexto | Semrush (a-d) | Supabase (e) | GSC | GA4 |
|---|---|---|---|---|
| Buzzmonitor BR | ✅ | ✅ | ✅ `sc-domain:buzzmonitor.com` | ✅ `347467970` |
| Buzzmonitor LATAM | ✅ | — (só staging, fora de escopo) | ✅ `sc-domain:buzzmonitor.com` (filtro `/es/`) | ✅ `347502824` (mesma property da BM PT; tag `GTM-PC4TJ6H`) |
| Buzzmonitor Portugal | ✅ | — (sem tabela) | ✅ `sc-domain:buzzmonitor.com` (filtro `/pt-pt/`) | ✅ `347502824` (mesma property da BM LATAM; blog em `/blog/pt-pt/`) |
| Cxpress BR | ✅ | ✅ | ✅ `sc-domain:cxpress.io` (site+blog, split por hostname) | ✅ `339689858` site + `345714231` blog |
| Cxpress LATAM | ✅ | — (sem tabela) | ❌ não existe (sem pixel/verificação — depende de dev instalar) | ❌ não existe |
| Cxpress Portugal | ✅ | — (sem tabela) | ❌ não existe | ❌ não existe |
| Elife BR | ✅ | — (fora de escopo, sem tabela mapeada) | ❌ sem GSC | ⚠️ `369456629` existe mas **sem tag instalada no site** (confirmado via Tag Assistant 2026-07-29) — vai ficar zerado até o dev instalar |
| Elife Portugal | ✅ | — | ❌ sem GSC | ❌ sem GA4 |

Pra atualizar essa tabela (ex: acesso GSC/GA4 novo liberado, ou o property ID da Elife BR chegando), edite também `CONTEXTS` em `seo_report_google.py` — é a fonte de config real que o script usa.

**Cxpress LATAM/PT — nota importante:** confirmado com o Maretto (2026-07-28) que GA4/GSC nunca foram configurados nesses domínios (sem pixel instalado, sem verificação de propriedade) — não é "acesso pendente de aprovação", é infraestrutura que ainda não existe. Depende de pedir pro dev instalar o pixel e, só depois de um tempo captando sinal real, o Search Console/Analytics passam a ter dado pra mostrar. Sem prazo curto — a skill segue rodando normalmente pros outros 7 contextos.

**Elife — 2 marcas, sites:** BR = `elife.com.br` · Portugal = `elifeportugal.com`. Sem tabela de deals no Supabase mapeada (item e fica de fora dos dois). Achado real testando o Semrush (2026-07-28): Elife BR **não** usa `/blog/` no path — os posts ficam em `/index.php/AAAA/MM/DD/slug/` (permalink WordPress por data); o domínio também mistura subdomínios de projetos de cliente (`volkswagen-web.elife.com.br`, `koin.elife.com.br` — portais brancos que a Elife constrói pra clientes, não conteúdo próprio) no mesmo Semrush target, que caem corretamente no bucket "site" por não baterem o path de blog. Elife Portugal tem presença orgânica quase nula no Semrush hoje — sem padrão de blog identificado ainda. GA4 da Elife BR existe (`369456629`) mas **sem tag instalada no site** (confirmado via Tag Assistant, 2026-07-29) — vai ficar zerado até o dev instalar.

**Buzzmonitor LATAM/PT depois da migração (~20/set/2026):** os dois saíram de `getbuzzmonitor.com` e passaram a viver em `buzzmonitor.com/es/` e `buzzmonitor.com/pt-pt/` (o `/pt/` dá 404), com blog em `/blog/es/` e `/blog/pt-pt/`. Dividem o `sc-domain` com o BR e, entre si, a property GA4 `347502824` (tag `GTM-PC4TJ6H`; o BR usa `GTM-PDSV26W`, property `347467970`). O filtro por substring resolve: `region_match` (`/es/` ou `/pt-pt/`) recorta a região e `blog_match` (`/blog/`) separa o blog. A lista de URLs de posts (`blog_urls_intl.json`), que separava blog de produto no `getbuzzmonitor.com`, saiu do repo junto com a migração (está no histórico do git, se um dia precisar).

---

## Paths

```
seo_report_google.py       (no repo) — coletor GA4+GSC multi-contexto (OAuth)
seo_report_conversoes.py   (no repo) — coletor Supabase (item e), só BR
cluster_mapping.json       (no repo) — de-para utm_content -> cluster (best-effort, ver nota abaixo)
WORK_DIR    = ~/.seo-report-buzzmonitor/   (por usuário, fora do repo; ou defina SEO_REPORT_DIR)
  ├─ client_secret.json    (você baixa do Google Cloud Console — entrada)
  ├─ token.json            (gerado no 1º login — gitignored)
  ├─ seo_data.json         (saída de seo_report_google.py: 1 entrada "contexts" por marca/região)
  └─ seo_conversoes.json   (saída de seo_report_conversoes.py: buzzmonitor-br + cxpress-br [fechamentos 6m] + tendencia_3m [leads criados mês a mês, 3 meses anteriores ao mês de análise])
```

`dashboard/.env` (fora deste diretório, na raiz do repo) precisa ter `SUPABASE_PG_URL` preenchido — é o MESMO `.env` usado por `auditar-deals-cm` e pelos exportadores das dashboards CM. Nunca commitar.

O `.gitignore` da pasta da skill já protege `client_secret.json`, `token.json` e os `.json` de saída caso apareçam no diretório do repo.

---

## Fluxo de execução

### Passo 1 — Resolver origem dos dados Google + Supabase

Se o usuário passou um `[contexto]` específico, rodar só esse (mais rápido). Sem argumento, rodar todos os 8.

Verificar se `seo_data.json` existe no `WORK_DIR` e tem menos de 24h (campo `gerado_em`). Se sim, perguntar com chips:
- **"Usar dados de hoje (gerado em {gerado_em})"** → Passo 3
- **"Coletar dados novos agora"** → Passo 2

Se não existir ou tiver mais de 24h → Passo 2.

### Passo 2 — Rodar os scripts Python (Google + Supabase)

Verificar pré-condições (PowerShell no Windows):

```powershell
# 0. Resolver o interpretador. No Windows, `python`/`python3` no PATH costumam ser o shim da
#    Microsoft Store: existem (Get-Command acha), mas falham com exit 49. O launcher `py` aponta
#    pro Python real. Testamos EXECUCAO (nao so existencia) e ficamos com o 1o que roda de verdade.
$PYBIN='python'; foreach($c in 'py','python3','python'){ if(Get-Command $c -ErrorAction SilentlyContinue){ & $c -c 'import sys' 2>$null | Out-Null; if($LASTEXITCODE -eq 0){ $PYBIN=$c; break } } }

# 1. Python disponível?
& $PYBIN --version

# 2. Dependências Google instaladas?
& $PYBIN -c "import google.oauth2; from google.analytics.data_v1beta import BetaAnalyticsDataClient"

# 3. Dependência Supabase instalada?
& $PYBIN -c "import psycopg"
```

Se faltarem, instalar:
```powershell
$PYBIN='python'; foreach($c in 'py','python3','python'){ if(Get-Command $c -ErrorAction SilentlyContinue){ & $c -c 'import sys' 2>$null | Out-Null; if($LASTEXITCODE -eq 0){ $PYBIN=$c; break } } }
& $PYBIN -m pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client google-analytics-data "psycopg[binary]"
```

**2.1 — Google (GSC+GA4, todos os contextos com credencial configurada):**
```powershell
$PYBIN='python'; foreach($c in 'py','python3','python'){ if(Get-Command $c -ErrorAction SilentlyContinue){ & $c -c 'import sys' 2>$null | Out-Null; if($LASTEXITCODE -eq 0){ $PYBIN=$c; break } } }
& $PYBIN .claude/skills/seo-report/seo_report_google.py
```
Se `client_secret.json` não estiver no `WORK_DIR`, o script para com instrução clara. Oriente o usuário: "Coloque o `client_secret.json` (credencial OAuth2 tipo Desktop, baixada do Google Cloud Console) em `~/.seo-report-buzzmonitor/`. No 1º uso abre o navegador para login; depois o `token.json` fica salvo e as execuções são silenciosas." Se falhar com erro de autenticação, orientar: deletar `token.json` no `WORK_DIR` e rodar de novo.

**2.2 — Supabase (item e, só se o contexto pedido for `buzzmonitor-br`, `cxpress-br` ou "todos"):**
```powershell
$PYBIN='python'; foreach($c in 'py','python3','python'){ if(Get-Command $c -ErrorAction SilentlyContinue){ & $c -c 'import sys' 2>$null | Out-Null; if($LASTEXITCODE -eq 0){ $PYBIN=$c; break } } }
& $PYBIN .claude/skills/seo-report/seo_report_conversoes.py
```
Se `dashboard/.env` não existir ou não tiver `SUPABASE_PG_URL`, o script para com instrução (copiar `dashboard/.env.example` e preencher). **Não é bloqueante** — se falhar, o dashboard segue sem a seção de conversão, com card de aviso.

### Passo 3 — Ler os JSONs coletados

Ler `seo_data.json` (`contexts.{contexto}.gsc` / `.ga4` — cada um pode vir `null` se a fonte não estiver configurada pro contexto, ou `{"erro": "..."}` se falhou) e `seo_conversoes.json` (`buzzmonitor-br` / `cxpress-br`) com Read. Não abortar em nenhum dos dois casos — ausência de fonte é estado normal, não erro.

### Passo 4 — Coletar Semrush via MCP (todos os 8 contextos)

Alvos e database por contexto (ver também `CONTEXTS` em `seo_report_google.py` pro resto da config):

| Contexto | `target` (Semrush) | `database` |
|---|---|---|
| buzzmonitor-br | `buzzmonitor.com` | `br` |
| buzzmonitor-latam | `buzzmonitor.com/es/` (**subpasta** — migração de getbuzzmonitor.com/es/ concluída ~Set/26; blog em /blog/es/) | `mx` |
| buzzmonitor-pt | `buzzmonitor.com/pt/` (**subpasta** — migração de getbuzzmonitor.com/pt/ concluída ~Set/26; blog em /blog/pt/) | `pt` |
| cxpress-br | `cxpress.io` (domínio raiz — cobre `home.` e `blog.` juntos) | `br` |
| cxpress-latam | `cxpress.ai` (domínio raiz) | `mx` (confirmado 2026-07-29 via `domain_ranks`: `cxpress.ai` tem tráfego orgânico ~zero em TODAS as bases regionais — ar/br/cl/es/mx/us, no máximo 6 keywords e 0 tráfego em qualquer uma. Não é erro de base, é domínio ainda sem presença orgânica real — bate com não ter GSC/GA4 configurado) |
| cxpress-pt | `cxpress.pt` (domínio raiz) | `pt` |
| elife-br | `elife.com.br` (domínio raiz — inclui subdomínios de projetos de cliente, ex. `volkswagen-web.`, `koin.`; caem no bucket "site", não "blog") | `br` |
| elife-pt | `elifeportugal.com` (domínio raiz) | `pt` |

Pra cada contexto (pular os que o usuário não pediu, se passou `[contexto]` específico), rodar via `get_report_schema` + `execute_report`:

**4.a — Evolução histórica de keywords** (`resource_rank_history`):
- `params = {"target": <target>, "database": <database>, "export_columns": ["date","organic_keywords","organic_traffic","organic_traffic_cost","positions_1_3","positions_4_10","rank"]}`
- Retorna a série mensal INTEIRA numa chamada só (não loopar por data). Guardar os últimos ~13 meses pro gráfico; o resto fica disponível mas não precisa exibir tudo.
- Usar só pro **gráfico de evolução ao longo do tempo** (série histórica) — os buckets exatos de Top3/Top5/Top10 do snapshot ATUAL vêm do passo 4.a-bis abaixo, não daqui (`positions_1_3`/`positions_4_10` desse report não tem Top5 e ficam só como contexto histórico).

**4.a-bis — Top3/Top5/Top10 exatos + branded vs. non-branded, COM as keywords** (`resource_organic`, snapshot atual, 2 chamadas por contexto):
- Pedido explícito do Maretto (diretoria) — Top5 não existe como bucket nativo do Semrush, e branded/non-branded não vem em nenhum report pronto. Solução: buscar a lista COMPLETA de keywords ranqueadas e calcular os dois em Python.
- **Não é só contagem — o Maretto/diretoria querem ver as keywords em si** (decisão de 2026-07-31, depois de entregar só números num primeiro relatório). Toda execução da skill precisa reter e mostrar, além das contagens: a lista completa de Top3, a lista completa de branded, e uma amostra das non-branded de maior volume (ver formato no Passo 6).
- **Chamada 1 — snapshot completo:** `params = {"target": <target>, "database": <database>, "display_limit": 1000, "display_sort": "position_asc", "export_columns": ["keyword","position","volume","traffic","url"]}` (1000 é o MÁXIMO aceito por essa API — confirmado 2026-07-31. Cobre com folga todos os contextos atuais, o maior deles com ~720 keywords no snapshot mais recente. Se algum contexto um dia ultrapassar 1000 keywords ranqueadas, os buckets ficam subestimados — nesse caso seria necessário paginar com `display_offset`)
- **⚠️ Deduplicar por keyword ANTES de contar/listar** (achado 2026-07-31): a mesma keyword aparece 1x por URL que ranqueia pra ela — um domínio pequeno pode ter a mesma keyword repetida dezenas de vezes (ex: "buzz monitor" rankeando pra 30+ páginas diferentes). Sem dedupe, os buckets Top3/Top5/Top10 e a contagem branded ficam superestimados. Dedupe = manter só a MELHOR (menor) posição por string de keyword (normalizada lowercase/trim) antes de qualquer contagem.
- Do resultado deduplicado, calcular em Python:
  - `top3 = keywords com position <= 3` (guardar a lista, não só a contagem) · `top5 = position <= 5` · `top10 = position <= 10`
  - `branded = keywords que contém algum termo de marca` (guardar a lista completa — normalmente são poucas, 0-4 por contexto) · `non_branded = total - branded`
- **Chamada 2 — top non-branded por volume** (pra não precisar vasculhar a lista toda de non-branded, que pode ter centenas/milhares de linhas): `params = {"target": <target>, "database": <database>, "display_filter": [{"field":"keyword","operation":"contains","value":"<termo1>","sign":"-"}, {"field":"keyword","operation":"contains","value":"<termo2>","sign":"-"}], "display_limit": 15, "display_sort": "volume_desc", "export_columns": ["keyword","position","volume","url"]}` — um filtro `sign:"-"` (exclui) por termo de marca do contexto. Dedupe por keyword aqui também (mesma keyword pode repetir por URL).
- **Termos de marca (branded) por contexto** — substring case-insensitive na keyword:
  | Marca | Termos |
  |---|---|
  | Buzzmonitor (BR/LATAM/PT) | `buzzmonitor`, `buzz monitor` |
  | Cxpress (BR/LATAM/PT) | `cxpress`, `c xpress` |
  | Elife (BR/PT) | `elife`, `e-life`, `e life` |
- Isso SUBSTITUI o antigo comportamento de só usar os buckets nativos do `resource_rank_history` (decisão de 2026-07-27 revertida em 2026-07-31 a pedido do Maretto — a build de amostra pequena por contexto, ~2 chamadas extra, torna o cálculo exato viável e não é mais um trade-off necessário).

**4.b — Ganho/perda de posicionamento** (`resource_organic`, 4 chamadas por contexto):
- `params = {"target": <target>, "database": <database>, "display_positions": "new"|"lost"|"rise"|"fall", "display_limit": 15, "display_sort": "traffic_desc"}`
- Rodar uma vez pra cada valor de `display_positions`. Não precisa de projeto de Position Tracking — esse filtro já existe na API paga-por-consulta padrão.
- **Atenção:** no bucket `lost`, `position` vem `0` (= "fora do Top 100", não uma posição real) — nunca badgear como Top3 (ver §Badges de posição).

**4.c — Páginas que mais ranqueiam** (`resource_organic_unique`):
- `params = {"target": <target>, "database": <database>, "display_limit": 15, "display_sort": "keywords_count_desc"}`
- Retorna `url`, `keywords_count`, `traffic`, `traffic_share` por página.

**4.d — Interesse de marca por país — BM LATAM** (`phrase_this`, 8 chamadas — só para o contexto `buzzmonitor-latam`):
- Verificar schema antes: `get_report_schema(report="phrase_this")` — confirmar nome do campo de volume histórico (esperado: `trends` ou `Td`, array de 12 valores mensais, do mais antigo pro mais recente).
- Para cada combinação keyword × database abaixo, rodar `execute_report(report="phrase_this", params={"phrase": <keyword>, "database": <database>, "export_columns": ["Ph","Nq","Td"]})`:
  | Keyword | Database | País |
  |---|---|---|
  | `buzzmonitor` | `mx` | México |
  | `buzzmonitor` | `ar` | Argentina |
  | `buzzmonitor` | `co` | Colombia |
  | `buzzmonitor` | `cl` | Chile |
  | `buzz monitor` | `mx` | México |
  | `buzz monitor` | `ar` | Argentina |
  | `buzz monitor` | `co` | Colombia |
  | `buzz monitor` | `cl` | Chile |
- Somar os valores de `trends` de "buzzmonitor" + "buzz monitor" para cada país → 1 série de 12 pontos por país.
- Se `trends` vier como string separada por vírgulas, converter para array de números.
- No dashboard HTML (aba BM LATAM): gráfico de linhas multi-série, 1 linha por país, eixo X = últimos 12 meses (rótulos `MMM/YYYY`), eixo Y = volume de busca. Título: **"Interesse de marca por país"**. Subtítulo: `"'buzzmonitor' + 'buzz monitor' · Semrush · últimos 12 meses"`. Cores sugeridas: México `#8b7cf6`, Argentina `#34d399`, Colombia `#fbbf24`, Chile `#f87171`.
- Se todos os países retornarem volume 0 ou erro: card informativo "Volume branded ainda abaixo do threshold de medição nestas regiões."

**4.e — Visibilidade em AI Overviews do Google** (integrado à chamada 4.a-bis — todos os contextos Buzzmonitor; Cxpress e Elife coleta opcional):
- Adicionar `"triggered_serp_features"` ao `export_columns` da chamada 4.a-bis (snapshot completo): `["keyword","position","volume","traffic","url","triggered_serp_features"]`.
- O campo retorna string de códigos numéricos separados por vírgula (ex: `"6,9,20,52"`). Com base em observação de agosto/2026, o código **`52` corresponde a AI Overview** — ver nota completa em Notas técnicas. Na primeira execução deste passo, fazer cross-check: pegar 1-2 keywords conhecidas por ter AI Overview (buscar manualmente no Google) e confirmar que o código `52` aparece; se o código real for diferente, registrar aqui e usar o correto.
- Após dedupe do passo 4.a-bis, para cada keyword, flagear `has_ai_overview = "52" in triggered_serp_features.split(",")`.
- Calcular por contexto:
  - `total_ai_overview` = count de keywords com `has_ai_overview = true`
  - `pct_ai_overview` = `total_ai_overview / total_keywords * 100`
  - `top10_com_ai` = lista de keywords com `position ≤ 10` E `has_ai_overview = true`
- No dashboard HTML:
  - Card de KPI em cada contexto: `"Keywords em AI Overviews: X (Y%)"` — junto ao bloco de distribuição Top3/Top5/Top10.
  - Tabela "Top 10 — com AI Overview": keyword · posição · volume · URL. Se lista vazia, exibir: `"Nenhuma keyword no Top 10 aciona AI Overview para este contexto."`.
- No relatório executivo do Notion (Passo 8 e 8.4): coluna `"AI Overview"` na tabela de Top Keywords (`✅` ou `—`); mencionar no resumo de cada marca o total de keywords Top10 com AI Overview.

Se o MCP falhar ou vier vazio (limite de unidades atingido) pra algum contexto, setar card de aviso só naquele contexto — **nunca abortar os outros 7**.

> Se algum parâmetro divergir do que está aqui (a API do Semrush muda o schema ocasionalmente), chamar `get_report_schema(report=...)` antes do `execute_report` pra confirmar.

### Passo 5 — Calcular deltas e variações

Para métricas com `_anterior` (GSC/GA4, quando disponíveis):
```
delta_pct = round(((atual - anterior) / anterior) * 100, 1) se anterior > 0 senão None
sinal     = "▲" se delta_pct > 0 | "▼" se delta_pct < 0 | "—" se None
cor       = verde (#16a34a) se positivo | vermelho (#dc2626) se negativo (exceto bounce_rate: invertido) | cinza se None
```

Pra Semrush (a/b/c/d), os "deltas" já vêm prontos nos próprios reports (série histórica, e novo/perdido/subiu/caiu já SÃO o delta) — não precisa recalcular.

### Passo 6 — Gerar o dashboard HTML

Usar a skill `frontend-design` como referência de qualidade. HTML completo, **totalmente inline** (sem CDN), dados embutidos como variáveis JS. Paleta: fundo branco/cinza claro, texto escuro, acento `#1e40af` (azul Buzzmonitor) — usar o acento da marca correspondente se disponível em `brand/{marca}/tokens.json`, senão manter o azul default. Font-family: system-ui.

#### Seletor de contexto

Dashboard único com **abas** (ou dropdown) pra trocar entre os 8 contextos no topo — não gerar 8 arquivos HTML separados. Contextos sem nenhuma fonte configurada além de Semrush ainda aparecem na aba (Semrush nunca falta), só com as seções Google/Supabase mostrando o card de aviso.

#### Estrutura por contexto

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: "SEO Report — {Label do Contexto}"                      │
│          Badge período  •  Badge gerado em  •  [avisos fonte]    │
├────────────────────────────────────────────────────────────────────┤
│  BLOCO "Total" (destaque, cards maiores, acento de cor)          │
│  GSC:  [Cliques] [Impressões] [CTR] [Posição]  (se configurado)  │
│  GA4:  [Sessões] [Usuários] [Bounce] [Duração]  (se configurado) │
├──────────────────────────┬────────────────────────────────────────┤
│  BLOCO "Site" (discreto)  │  BLOCO "Blog" (discreto)              │
│  cards menores, cor neutra│  cards menores, cor neutra            │
├────────────────────────────────────────────────────────────────────┤
│  SEÇÃO "Semrush — Evolução de Keywords Ranqueadas"               │
│  Gráfico de linha (últimos 13 meses): organic_keywords ao longo  │
│  do tempo + área empilhada Top3 vs Top4-10 vs resto              │
├───────────────────────────┬────────────────────────────────────────┤
│  Distribuição atual (4.a-bis)│  Canais de Tráfego (GA4, se houver) │
│  Top3 · Top5 · Top10 · Resto │  barras horizontais por canal        │
│  Branded vs. Non-branded     │                                       │
│  (barras/donut)              │                                       │
│  AI Overviews: X kws (Y%)    │                                       │
├────────────────────────────────────────────────────────────────────┤
│  TABELA "Top 3 Keywords" · keyword · posição · volume · AI OV · URL│
│  TABELA "Keywords Branded" · keyword · posição · volume · URL    │
│  TABELA "Top 10 — com AI Overview" · keyword · pos · vol · URL  │
│  TABELA "Top Non-branded (por volume)" · top 10-15, não a lista  │
│  inteira — non-branded costuma ter centenas de linhas de cauda   │
│  longa; mostrar as de maior volume de busca (mais relevantes) e  │
│  anotar o total (ex: "10 de 716 non-branded, ordenadas por       │
│  volume"). NUNCA omitir essa seção silenciosamente — pedido      │
│  explícito da diretoria (2026-07-31): números sozinhos não bastam,│
│  precisam ver as keywords em si.                                  │
├────────────────────────────────────────────────────────────────────┤
│  TABELA "Ganho de Posição"      · keyword · pos. atual · trafego │
│  TABELA "Perda de Posição"      · keyword · pos. atual · trafego │
│  TABELA "Keywords Novas"        · keyword · posição · volume     │
│  TABELA "Keywords Perdidas"     · keyword · última posição       │
├────────────────────────────────────────────────────────────────────┤
│  TABELA "Páginas que Mais Ranqueiam" (Semrush)                   │
│  URL · Nº Keywords · Tráfego Est. · % Tráfego                    │
├────────────────────────────────────────────────────────────────────┤
│  TABELA "Top Páginas — GSC" (se configurado, 28 dias)            │
│  TABELA "Top Páginas — GA4" (se configurado, 28 dias)            │
│  TABELA "Top Keywords — GSC" (se configurado, 28 dias)           │
├────────────────────────────────────────────────────────────────────┤
│  TABELA "Artigos que Mais Convertem" (Supabase, só BR)           │
│  Post (utm_content) · Cluster · Fechamentos · Receita · Ticket   │
│  médio — ordenado por receita desc, top 20                       │
└────────────────────────────────────────────────────────────────────┘
```

#### Regras de formatação de números
- ≥ 1.000.000 → `X.XM` · ≥ 1.000 → `X.XK` · CTR → `X.XX%` · Posição → `XX.X` · Duração (seg) → `Xm XXs` · Bounce → `XX.X%` · Moeda → `R$ X.XXX` (sem casas decimais em valores ≥ R$1.000)

#### Seção adicional — aba BM LATAM: Interesse de marca por país (4.d)

Inserir **acima** do bloco de distribuição Top3/Top5/Top10, logo após os cards de KPI totais:

```
┌────────────────────────────────────────────────────────────────────┐
│  GRÁFICO "Interesse de marca por país"                             │
│  "buzzmonitor" + "buzz monitor" · Semrush · últimos 12 meses      │
│  Linhas: MX (roxo) · AR (verde) · CO (âmbar) · CL (vermelho)      │
└────────────────────────────────────────────────────────────────────┘
```

#### Bloco "Total" em destaque vs. "Site"/"Blog" discretos
Decisão do usuário (2026-07-27): sempre que houver Google configurado, mostrar os 3 (Total, Site, Blog) — Total com cards maiores/acento de cor no topo, Site e Blog lado a lado abaixo em cards menores/cor neutra. Isso vale mesmo quando site+blog tecnicamente vêm da mesma property/propriedade (Buzzmonitor) — consistência visual entre os 8 contextos, mesmo que o esforço de coleta seja diferente por trás (filtro de path vs. soma de properties distintas).

#### Badges de posição (tabelas de keywords)
```
posição 0     → "Fora do Top 100" (fundo cinza claro #e5e7eb, texto escuro) — NUNCA tratar como Top 3
posição 1–3   → fundo verde escuro (#166534), texto branco, "Top 3"
posição 4–10  → fundo azul (#1e3a8a), texto branco
posição 11–20 → fundo cinza (#374151), texto branco
posição > 20  → fundo cinza claro (#e5e7eb), texto escuro
```
**Atenção (bug real encontrado 2026-07-31):** no bucket `lost` do `resource_organic`, o Semrush retorna `position=0` pra dizer "não aparece mais no Top 100" — não é uma posição de verdade. Uma regra `if (pos <= 3) → Top 3` cai nessa armadilha e mostra a keyword perdida como se estivesse rankeando excelente (o oposto do real). Sempre tratar `position === 0` como caso especial ANTES de qualquer comparação numérica.

#### Cards de KPI
Fundo branco, borda `1px solid #e5e7eb`, radius 8px, padding 20px. Label cinza no topo, valor grande bold, delta abaixo com ▲/▼ e cor. Bloco "Total": mesmo padrão + borda de acento de 2-3px ou fundo levemente tintado.

#### Cards de aviso de fonte ausente/erro
- Fonte NUNCA configurada pro contexto (ex: GSC de Buzzmonitor LATAM hoje): banner cinza neutro — "ℹ️ {Fonte} ainda não configurado para {contexto}."
- Fonte configurada mas retornou erro na coleta: banner laranja — "⚠️ Dados do {fonte} indisponíveis — {mensagem}."

### Passo 7 — Salvar e abrir o dashboard

Salvar o HTML no `WORK_DIR` (fora do repo), com a data de hoje:
```
~/.seo-report-buzzmonitor/seo-report-{YYYY-MM-DD}.html
```
(Use o caminho absoluto resolvido — `$env:USERPROFILE\.seo-report-buzzmonitor\...` no Windows, ou `SEO_REPORT_DIR` se definido.)

Abrir no navegador padrão:
```powershell
Start-Process "$env:USERPROFILE\.seo-report-buzzmonitor\seo-report-{YYYY-MM-DD}.html"
```
(macOS: `open ...` · Linux: `xdg-open ...`.)

Informar ao usuário o caminho do arquivo gerado. Depois, resumir no chat em até 5 linhas (1 por contexto rodado, no máximo):
- Contexto · keyword que mais ganhou posição · post que mais converteu (se aplicável) · 1 alerta (fonte ausente relevante ou queda forte)

---

### Passo 8 — Relatório executivo pro Notion (sob pedido — "manda pra diretoria", "publica no Notion")

Diferente do dashboard HTML (Passo 7 — ferramenta de exploração pra quem já conhece o contexto), o relatório de Notion é pra **público executivo com pouco tempo e pouco contexto técnico**. Regras fixadas com feedback real do Victor (2026-08-05), aplicam sempre:

**8.1 — Pirâmide invertida (ordem obrigatória):**
1. **Resumo** — 3-5 frases, o mínimo que alguém precisa saber se só ler isso e fechar.
2. **Visão por Marca** — pra cada marca: **Positivos** / **Negativos** / **Próximos passos** em bullets curtos. Isso substitui e ANTECEDE qualquer tabela — é a segunda camada da pirâmide, não a última.
3. **Detalhamento** (só depois de 1 e 2) — todas as tabelas abertas (Visão Geral, Top3/5/10, keywords, posts) pra quem quiser conferir com os próprios olhos.

Nunca inverter essa ordem — a lógica é "quem só ler o topo já sai satisfeito"; detalhe no topo obriga todo mundo a rolar a página inteira.

**8.2 — Contexto de negócio (perguntar antes de gerar, se for relatório pra diretoria/gestão):** perguntar ao usuário se há trabalho em andamento que explique quedas de métrica antes de fechar o relatório — publicações recentes em volume, correções técnicas já delegadas, migração/internacionalização, sazonalidade conhecida etc. Sem isso, quedas reais (que existem, ex: migração de site) podem ser lidas por quem não acompanha o dia a dia como "não está sendo feito nada". Colocar esse contexto num callout no TOPO do relatório (antes do Resumo) e reforçar (1 frase) nos "Negativos" da marca afetada, não só uma vez no topo.

**8.3 — Tabelas transpostas:** métricas em LINHA, propriedades em COLUNA (não o oposto). Ex: linha "Cliques", colunas "Buzzmonitor BR / LATAM / PT / Cxpress BR" — permite comparar todas as propriedades numa métrica só, lendo uma linha.

**8.4 — Keywords em destaque (keyword · posição · URL) — inspirado na planilha de controle da Thamires, mas simplificado a pedido do Victor:** só a keyword, a posição e a URL pra qual ela aponta (dado puro do Semrush — `resource_organic` já retorna isso). NÃO replicar as colunas de controle manual da planilha original (observação, ação necessária, snippet) — são de acompanhamento humano dela, não dado que a skill tem de onde tirar. Escopo por contexto: Top3 completo + branded completo (normalmente cabe numa tabela pequena). Coluna "Destaque de IA" (AI Overview): incluir só se o cross-check do mês confirmou o código (ver Passo 4.e e Notas técnicas). Sem cross-check, omitir a coluna e avisar no relatório — nunca publicar palpite.

**8.5 — Posts mais visitados (post · cliques · impressões · posição):** tabela por contexto, fonte primária GSC `top_paginas_blog` (dado real de clique/impressão/posição), ordenado por cliques desc, top 10. Se o contexto não tem GSC, fallback pra `resource_organic_unique` do Semrush (nº keywords + tráfego estimado) com aviso explícito de que não é visita real medida.

**8.6 — Gotcha técnico do Notion (ache isso 2x, documentar pra nunca mais acontecer):**
- **Tabelas SEMPRE em formato verboso** — cada `<table>`, `<tr>` e `<td>` na sua PRÓPRIA linha. Formato compacto (`<tr><td>x</td><td>y</td></tr>` tudo numa linha, ou múltiplas linhas `<tr>` sem quebra entre elas) quebra o parser da Notion e vira texto escapado (`\<table\>`) em vez de tabela de verdade.
- **URLs/domínios nus (sem `https://`, tipo `home.cxpress.io/`) dentro de `<td>` viram link automático da Notion e corrompem a tag ao redor.** Sempre envolver em crase (code span, `` `dominio.com/path/` ``) dentro de células de tabela — code span não sofre autolinkificação.
- Depois de qualquer `create-pages`/`update-page`, sempre rodar `notion-fetch` de novo pra conferir que renderizou certo antes de considerar pronto — o erro só aparece no conteúdo já salvo, não no retorno da chamada de escrita.

**8.7 — Onde publicar:** perguntar ao usuário o link/pasta do Notion se não for óbvio pelo contexto da conversa. Rodar `notion-fetch` na pasta indicada primeiro pra ver se já existe um relatório anterior — se existir, seguir o MESMO formato/seções dele antes de inventar um novo layout do zero (foi assim que o layout atual desse relatório nasceu, herdando de um "Relatório de Balanço SEO — H1 2026" que já existia na pasta).

---

### Passo 9 — Evolução dos últimos 3 meses (sempre que gerar relatório pro Notion)

Capacidade permanente desde v2.5.0. Exibida no relatório do Notion como nova seção **"Evolução dos Últimos 3 Meses"**, após o bloco de Detalhamento do mês (Passo 8). Cobre os **3 meses completos imediatamente anteriores** ao mês de análise — para o relatório de julho: abril, maio, junho.

#### 9.a — Oscilação de Top5 keywords (Semrush, via MCP)

Rodar para os contextos com volume relevante (Buzzmonitor BR, Buzzmonitor LATAM, Cxpress BR — pelo menos). Para cada um dos 3 meses anteriores, buscar o snapshot mensal via `resource_organic` com `display_date`:

```
params = {
  "target": <target>, "database": <database>,
  "display_date": "YYYYMM15",   ← formato: YYYYMM15, ex: "20260415" para abril/2026
  "display_limit": 1000, "display_sort": "position_asc",
  "export_columns": ["keyword","position","url"]
}
```

> **Verificar o schema antes** com `get_report_schema(report="resource_organic")` caso `display_date` não apareça nos parâmetros documentados — o Semrush atualiza o schema ocasionalmente. Se não houver suporte a `display_date`, usar o snapshot atual de 4.a-bis como única referência e omitir a análise mensal.

Para cada snapshot (3 meses + mês atual de 4.a-bis):
- **Deduplicar** por keyword (mesma regra de 4.a-bis: melhor posição por string normalizada).
- Extrair a lista de Top5 do snapshot.

Com os 4 snapshots, calcular por contexto:

| Status | Critério |
|---|---|
| **Entrou no Top5** | aparece no mês atual, não aparecia (ou estava fora do Top5) no mês anterior |
| **Saiu do Top5** | estava no Top5 em algum dos 3 meses, não está no mês atual |
| **Subiu** | estava no Top5 antes e melhorou posição no mês atual |
| **Caiu** | estava no Top5 antes e piorou posição no mês atual |
| **Estável** | Top5 nos 4 snapshots, variação ≤ 1 posição |

Formato no Notion — tabela por contexto (uma linha por keyword única que aparece em algum dos 4 snapshots e está ou esteve no Top5):

```
| Keyword | Abr | Mai | Jun | Mês atual | URL | Status |
```

Onde "Abr/Mai/Jun/Mês atual" é a posição naquele snapshot (ou "—" se estava fora do Top5/Top100).

#### 9.b — Oscilação de leads por blog (Supabase)

Dados já coletados por `seo_report_conversoes.py` e disponíveis em `seo_conversoes.json → tendencia_3m`. Ler com Read antes de montar o relatório — não é necessário rodar o script de novo se o JSON já existir.

Estrutura do JSON por mês e por marca:
```json
{
  "tendencia_3m": {
    "2026-04": {
      "periodo": {"inicio": "2026-04-01", "fim": "2026-04-30"},
      "buzzmonitor-br": {
        "total_leads": 5,
        "total_fechados": 2,
        "total_nao_fechados": 3,
        "receita_total": 15000.00,
        "posts": [
          {"post": "monitoramento-redes-sociais", "leads": 3, "fechados": 1, "receita": 10000.0, "cluster": "Social Listening"},
          ...
        ]
      },
      "cxpress-br": { ... }
    },
    "2026-05": { ... },
    "2026-06": { ... }
  }
}
```

Formato no Notion — **2 tabelas transpostas** (meses em coluna, marcas em linha separadas):

**Tabela resumo de leads por mês** (Buzzmonitor BR e Cxpress BR em seções separadas):
```
| Métrica         | Abril | Maio | Junho |
| Leads criados   |   5   |   8  |   6   |
| Fechamentos     |   2   |   3  |   2   |
| Receita (R$)    | 15.000| 22.000| 18.000|
```

#### 9.c — Artigos que mais geraram leads por mês

Derivado de `tendencia_3m[mes][marca].posts` — já está no JSON. Top 5 artigos considerando os 3 meses combinados (soma de leads de cada post nos 3 meses), mostrando distribuição por mês:

```
| Artigo (utm_content)       | Cluster        | Abr | Mai | Jun | Total leads | Fechamentos |
| monitoramento-redes-sociais| Social Listening|  3  |  2  |  4  |      9      |      3      |
```

> **Nota sobre escopo:** `tendencia_3m` cobre só Buzzmonitor BR e Cxpress BR (únicas marcas com tabela de deals no Supabase em produção). Para as demais marcas no Notion, omitir essa seção com um aviso simples: "Dados de leads disponíveis só para Buzzmonitor BR e Cxpress BR — demais marcas sem tabela de deals em produção."

---

## Cluster mapping (item e)

`cluster_mapping.json` faz um de-para **best-effort** entre `utm_content` (slug do post) e os clusters definidos em `conhecimento/produto/{buzzmonitor|cxpress}/seo/clusters-brasil.md` (mesma fonte que a `/blog-diario` usa). Matching é fuzzy (slugify + contains) — posts sem correspondência caem em `"Sem cluster mapeado"`. **Revisar manualmente** sempre que os arquivos de cluster forem atualizados pelo time; o mapeamento não se regenera sozinho.

---

## Tratamento de erros comuns

| Erro | O que fazer |
|---|---|
| `client_secret.json` não encontrado | Explicar como baixar do Google Cloud Console e onde salvar (`WORK_DIR`); parar só a parte Google |
| `token.json` expirado / inválido | Deletar `token.json` no `WORK_DIR` e reautenticar |
| `dashboard/.env` sem `SUPABASE_PG_URL` | Orientar copiar `dashboard/.env.example` → `dashboard/.env` e preencher; parar só a parte Supabase |
| MCP Semrush sem unidades / erro num contexto | Card de aviso só nesse contexto; seguir com os outros 7 |
| GSC/GA4 não configurado pro contexto | Card informativo (não é erro) — visto na tabela de cobertura |
| Linha do Semrush vazia / malformada | Tratar silenciosamente, exibir `—` nas células |
| Script Python não encontrado | Confirmar os caminhos em `.claude/skills/seo-report/` |
| Python não instalado | Instalar via **python.org** (registra o launcher `py`). Evitar o alias "python" da Microsoft Store — shim que falha com exit 49. |
| `python`/`python3` retorna exit 49 | Alias da Microsoft Store no PATH. O resolver `$PYBIN` já pula pro `py`. |

---

## Exemplos de uso

```
/seo-report
# → roda os 8 contextos: coleta Google onde configurado, Supabase (BR), Semrush (todos), gera dashboard com abas

/seo-report cxpress-br
# → roda só Cxpress BR (mais rápido; útil pra iterar sem esperar os outros 5)
```

---

## Notas técnicas

- **Sem chave de API no repositório.** Semrush vem do MCP; Google usa OAuth com `client_secret.json`/`token.json` locais por usuário; Supabase usa o Postgres read-only já configurado em `dashboard/.env` (usuário `looker_readonly`) — nenhum dos três fica no repo.
- **Config central dos contextos GA4/GSC** vive em `CONTEXTS` no topo de `seo_report_google.py` — é ali que se adiciona um property ID ou GSC site novo quando o acesso for liberado (não precisa reabrir a arquitetura da skill, só editar essa config).
- **Período:** Semrush usa a série histórica completa (item a) e o snapshot mais recente disponível (itens b-d). GSC/GA4 usam 28 dias vs 28 dias anteriores. Supabase (item e) usa uma janela de 180 dias — conversão de conteúdo se acumula ao longo de meses, 28 dias daria amostra pequena demais.
- **Escopo de Supabase:** só Buzzmonitor BR e Cxpress BR (únicas com tabela de deals em produção — LATAM só tem staging, Portugal não tem tabela ainda). Reusa a MESMA lógica de atribuição de `queries.q_lista_fechamentos`/`queries_cxpress.q_lista_fechamentos` (CTE, whitelist/blacklist, inbound, 90d) via `q_fechamentos_blog_buzzmonitor`/`q_fechamentos_blog_cxpress` em `seo_report_conversoes.py` — mas com um filtro adicional restringindo a **conversão de blog de verdade** (`utm_source='blog'` OU `url_conversao` batendo em `/blog/`). Achado testando com dado real (2026-07-28): o `filtro_cm()` original cobre TODO Content Marketing (social, email, webinar, remarketing — não só blog), e o `utm_content` de fechamentos nesse escopo mais amplo costuma ser nome de criativo de anúncio (ex: "RMKT 7 - UGC computador"), não slug de post. Sem esse filtro extra, o item (e) responderia "o que mais converte em CM", não "qual artigo de blog mais converte" — que foi o pedido original.
- **Subpasta vs. domínio raiz no Semrush:** Buzzmonitor LATAM/PT dividem o domínio `getbuzzmonitor.com` — o `target` tem que ser a subpasta (`/es/`, `/pt/`), nunca o domínio raiz, senão os dois contextos se misturam. Cxpress usa domínios raiz distintos por região (`.io`/`.ai`/`.pt`) — sem esse risco.
- **AI Overview no Semrush — código `52` (hipótese a confirmar todo mês — v2.6.0):** `resource_organic` com `export_columns: ["triggered_serp_features"]` retorna string de códigos numéricos por keyword (ex: `"6,9,20,21,36,52"`). Observação de agosto/2026: o código `52` aparece com frequência consistente com a prevalência real de AI Overview na SERP; o `51` é raro. Sem fonte oficial de referência dos códigos do Semrush, a skill usa `52` como proxy — mas **na primeira execução de um novo mês, fazer cross-check obrigatório**: pegar 2-3 keywords reconhecidamente com AI Overview (pesquisar no Google), confirmar que `52` está presente na string retornada pelo Semrush para essas keywords. Se o cross-check revelar um código diferente, atualizar esta nota e o Passo 4.e com o código correto antes de publicar o relatório. Nunca publicar dado de AI Overview sem ter feito esse cross-check no mês em questão.
- **Relatório executivo pro Notion:** ver Passo 8. É uma entrega DIFERENTE do dashboard HTML (Passo 7) — pirâmide invertida, tabelas transpostas, tom pra quem tem pouco tempo/contexto. Não confundir os dois formatos nem tentar unificá-los; servem públicos diferentes (a própria Bárbara explorando dado vs. diretoria lendo um resumo).
