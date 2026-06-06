# Auditoria BunzzAI × Meta Ads — protocolo, dicionário de campos e log

> **Propósito:** auditar se os dados do **MCP BunzzAI** batem com a **Meta API** (módulo `meta-ads/`)
> em nível de **campanha → adset → ad**, e registrar o que cada métrica significa em cada sistema.
> Este doc é lido sempre que o Victor pedir "compara BunzzAI vs Meta" / "audita o BunzzAI". Ele é
> reusável: o protocolo + o harness (`meta-ads/scripts/audit_vs_bunzzai.py`) reproduzem o teste.
>
> **Status:** 1ª rodada concluída em **2026-05-29** (ver §7 — Log). Veredito: **BunzzAI correto** —
> divergências explicadas 100% por (a) definição de métrica e (b) horário do snapshot.
>
> **Leia junto:** `CONTEXT.md` (deste mesmo diretório) tem a tabela de diferenças e a matriz de
> diagnóstico. Este doc é o **complemento operacional** (como rodar o teste e o que esperar).

---

## 0. TL;DR — o que aprendi (cola rápida)

1. **Casar SEMPRE por `meta_id`, nunca por nome.** O BunzzAI expõe `meta_id` em campanha, adset
   e ad. Nesta campanha dois adsets têm o **nome idêntico** (`[Lookalike 1% Visitantes Social Listening]`)
   e só o `meta_id` os distingue.
2. **3 classes de métrica** definem o veredito:
   - **Igualdade** (`spend`, `impressions`, `CPM`) → têm a mesma definição → **devem bater** (deram ±2,5%).
   - **Diferença esperada** (`clicks`, `conversions`) → BunzzAI conta mais amplo → **maior por design**.
   - **Derivadas** (`CTR`, `CPC`, `CpL`, `Conv. LP`) → herdam a diferença dos primitivos; recalcular.
3. **BunzzAI não entrega janela diária.** São snapshots **cumulativos**; a janela vem por **diff**
   (`cum(fim) − cum(início)`). Não tem `reach` nem métricas de vídeo.
4. **BunzzAI não tem métrica nativa de adset/campanha** — reconstrói-se **somando os ads**.
5. **Borda de snapshot** (≈16h) causa ±1-2% em spend/impressions/clicks. Não é erro.
6. **`leads` (Meta) ≠ `conversoes` (BunzzAI):** Meta conta só o pixel **primário** (`results_indicator`),
   BunzzAI conta **todas** as conversões → BunzzAI sempre um pouco maior.
7. **Pegadinha do agregador Meta:** `ctr_link`/`cpm`/`cpc_link` no banco são **média das diárias**
   (AVG), não `total/total`. **Recalcular derivadas dos primitivos** — o harness já faz isso.

---

## 1. Como rodar o teste (protocolo passo a passo)

Hoje a parte BunzzAI **passa por mim** (MCP só existe na minha sessão); o lado Meta e a matemática
são automatizados pelo harness. Sequência:

### Passo 0 — Token Meta
```
python meta-ads/scripts/check_setup.py
```
Se expirado → avisar o Victor e parar o lado Meta (renovar via `meta-ads/SETUP.md`). Sem token,
só dá pra olhar o BunzzAI (sem comparação).

### Passo 1 — Fetch fresco do lado Meta (a janela precisa estar no banco)
```
python meta-ads/scripts/fetch_campaigns.py --account buzzmonitor_brl --days 30 --include-ads
python meta-ads/scripts/fetch_insights.py  --account buzzmonitor_brl --period ultimos_30 --include-ads
```
> **⚠️ Pegadinha de rate limit (vivida nesta rodada).** O `fetch_insights --include-ads` chama
> `_ensure_ads_populated`, que **re-coleta a estrutura inteira** sempre que alguma campanha com
> `results_indicator` custom estiver sem ads na tabela (condição **permanente** p/ campanhas
> pausadas sem gasto — ver `fetch_insights._ads_table_is_stale`, cond. (b)). São ~28 chamadas
> redundantes → estoura o **código 17 (User request limit reached)**. A coleta real de insight é
> leve (~3 chamadas via async job). **Workaround:** rodar com `_ensure_ads_populated` neutralizado
> depois que a estrutura já foi populada uma vez (ver `tmp/fetch_insights_light.py` desta rodada).
> *(Candidato a melhoria na skill meta-ads: pular o re-fetch quando a estrutura é recente.)*

### Passo 2 — Selecionar a tripla (aleatória entre as ELEGÍVEIS)
Elegível = **ACTIVE** + com `spend>0` na janela + presente no BunzzAI + com pixel custom (pra
`conversions` ser interessante) + snapshots cobrindo a janela. Drill-down nesta ordem:
campanha → 1 adset dentro → 1 ad dentro. Pegar `meta_id` de cada nível no banco
(`get_campaigns/ get_adsets/ get_ads` do `cache_manager`).

### Passo 3 — Lado BunzzAI (via MCP, casando por `meta_id`)
```
tool_find_company("Buzzmonitor")          → company_id (= 3)
list_campaigns(company_id=3)              → acha a campanha por meta_id  (expõe meta_id!)
list_campaign_ads(campaign_id=<bz_id>)    → adsets + ads, cada um com meta_id
tool_get_ad_performance(ad_id=<bz_id>)    → monitoring_history (snapshots cumulativos) de CADA ad
```
- Para a **campanha/adset**, puxar o `tool_get_ad_performance` de **todos os ads** envolvidos
  (o harness soma os ads). `get_campaign_data(campaign_id)` dá o **último** snapshot por ad
  (bom p/ cumulativo, mas **não** dá histórico p/ janela).
- O `monitoring_history` é grande (~77 KB/ad) → vem salvo em arquivo `tool-results/...txt`.
  Anotar o caminho de cada arquivo (vai no spec).
> **⚠️ Instabilidade do `tool_get_ad_performance`.** Nesta rodada ele derrubou a conexão Postgres
> do backend (`psycopg2.OperationalError: server closed the connection` → depois `Session terminated`)
> em ~5 de 6 tentativas. **Não é bug fatal — é flaky: re-tentar resolve.** `get_campaign_data`
> usa outro caminho de query e **sobreviveu sempre** — bom plano B para o cumulativo.

### Passo 4 — Montar o spec e rodar o harness
Spec JSON (modelo em `tmp/audit_spec.json`): conta, `today`, janelas, os `meta_id` da tripla e o
mapa `{ad_meta_id: caminho_do_arquivo}` de **todos os ads da campanha**.
```
python meta-ads/scripts/audit_vs_bunzzai.py --spec tmp/audit_spec.json
```
O harness: lê o banco Meta + os arquivos BunzzAI → reconstrói janelas por diff → detecta cron
travado → **recalcula as derivadas dos primitivos nos dois lados** → imprime as tabelas de
comparação (janela 7d nos 3 níveis + 15d/30d do ad + cumulativo) já classificadas.

---

## 2. Dicionário de campos (o que cada coisa significa)

| Conceito | Campo BunzzAI (PT) | Campo Meta (`meta-ads`) | Definição / pegadinha | Esperado bater? |
|---|---|---|---|---|
| Investimento | `investimento_acumulado` (cumulativo) | `spend` (soma diária) | Mesma definição. BunzzAI é cumulativo; janela = diff. | **Sim** (±2%) |
| Investimento do dia | `investimento` (incremental do snapshot) | — | Gasto só daquele snapshot; **não** é cumulativo. Não usar p/ janela. | n/a |
| Impressões | `impressoes` (cumulativo) | `impressions` (soma) | Mesma definição. | **Sim** (±2%) |
| Cliques | `cliques` (cumulativo) | `link_clicks` | **BunzzAI = cliques TOTAIS; Meta = só link.** Tende a BunzzAI ≥ Meta, mas se o ad quase só tem clique de link, ficam **quase iguais** (foi o caso). | Direção, não igualdade |
| Conversões | `conversoes` (cumulativo) | `leads` | **BunzzAI = TODAS do pixel; Meta = só a primária** (`results_indicator` = `actions:offsite_conversion.custom.<id>`). BunzzAI sempre **maior**. | Direção (BunzzAI ≥) |
| CTR | `taxa_cliques` (pontual) | `ctr_link` (**AVG diária**) | Recalcular `cliques/impressoes`. O campo Meta cru é média das diárias — não comparar direto. | Recalculado |
| CPM | `cpm` (pontual) | `cpm` (**AVG diária**) | Recalcular `spend/impressoes*1000`. | **Sim** (±2%) |
| CPC | `cpc` (pontual) | `cpc_link` (**AVG diária**) | Recalcular `spend/cliques`. Herda a dif. de cliques. | Recalculado |
| CpL / Custo-conv | (derivar) | `cost_per_lead` (total-based) | `spend/conversoes`. BunzzAI **menor** (mais conversões no denominador). | Derivada |
| Conv. LP | (derivar) | `lp_conversion_rate` (total-based) | `conversoes/cliques*100`. BunzzAI **maior**. | Derivada |
| Frequência | `frequencia` (cumulativa lifetime) | `frequency` (**AVG diária**) | Conceitos diferentes: cumulativa (impr/reach lifetime ≈ 1,9) vs média das diárias (≈ 1,06). **Não comparar.** | Não |
| Alcance | — | `reach` (soma diária) | **BunzzAI não expõe.** E `SUM(reach)` diário do Meta ≠ reach único lifetime (infla). | N/A |
| Vídeo (p25/50/75/100) | — | `video_p25..p100` | BunzzAI não expõe. `hook_rate`/`completion_rate` ficam fora. | N/A |
| URL de conversão | `conversion_url` | — | Útil pra cruzar com a LP (UTMs). Ex.: `conteudo.buzzmonitor.com.br/relatorios-estrategicos`. | — |

> **Re-verificado em 2026-05-29 (a pedido — "já temos reach e vídeo no BunzzAI?"):** alcance e
> vídeo **continuam ausentes da camada MCP**. Confirmado na **união de TODAS as 120 snapshots** de
> `tool_get_ad_performance` (só os 18 campos: `investimento_acumulado, impressoes, cliques, conversoes,
> cpm, cpc, taxa_cliques, frequencia, custo_aquisicao, investimento, monitoring_id, recorded_at,
> source, conversion_url, utm_*`) — **zero** ocorrência de reach/alcance/video/p25-p100/thruplay/play.
> Também: `get_campaign_data` não traz; `get_campaign_insights` → `facebook_insights` **vazio**
> (testado nas campanhas 123 e 197); `tool_get_campaign_monitoring` (schema) e `tool_get_campaign`
> (só metadados) idem. A Meta TEM esses dados e o **produto/UI do BunzzAI pode exibi-los**, mas o
> **MCP não os expõe hoje** — provável que o writer de snapshot/insights ainda não inclua essas
> colunas. Se passar a expor: estender o harness lendo o campo direto do snapshot — **reach NÃO se
> soma entre ads** (é métrica deduplicada); só vídeo (p25..p100) é somável.

`cost_per_lead`/`lp_conversion_rate` do agregador Meta **são** recalculados dos totais
(`benchmark_checker.aggregate_metrics_for_period`, linhas 132-133). Já `ctr_link`/`cpm`/`cpc_link`
**não** — ficam como AVG das diárias. Por isso o harness ignora os campos derivados crus e recalcula
tudo dos primitivos.

---

## 3. Alinhamento de janela (a parte que mais confunde)

BunzzAI = snapshots **cumulativos** (vários por dia; pegar o de maior `recorded_at` = fim do dia).
Para uma janela de **N dias** terminando ontem (`today−1`):

```
BunzzAI janela(N) = cum(today−1) − cum(today−1−N)      # diff de snapshots
Meta    janela(N) = SUM(insights diários) de [today−N .. today−1]   # inclusive
```

Exemplo desta rodada (`today = 2026-05-29`, N = 7):
- **Meta**: agrega dias **2026-05-22 a 2026-05-28** (7 linhas).
- **BunzzAI**: `cum(2026-05-28) − cum(2026-05-21)` → mesmos 7 dias de incremento.
- Snapshots reais usados pelo harness: início **2026-05-21**, fim **2026-05-28**.

> **Borda de snapshot:** os snapshots do BunzzAI são de ≈16h, não meia-noite. Então a janela
> BunzzAI cobre "21/05 16h → 28/05 16h" enquanto a Meta cobre dias-calendário cheios. Isso gera
> ±1-2% e pode até **inverter o sinal** de `clicks` numa janela (BunzzAI levemente menor). É ruído
> de borda, **não** erro. Janelas onde as duas bordas são snapshots BunzzAI (15d/30d) tendem a
> casar melhor que o cumulativo (cujo fim trunca o último dia às 16h).

---

## 4. Framework de veredito (o que conta como "correto")

| Classe | Métricas | Critério | Resultado nesta rodada |
|---|---|---|---|
| **Igualdade** | `spend`, `impressions`, `CPM` | Mesma definição → bater dentro de ~3% (até ~10% = borda de dia). Acima disso = **erro real**. | ✅ ±2,5% em todas as janelas |
| **Diferença esperada** | `clicks` (link vs total), `conversions` (lead vs todas) | Direção: BunzzAI ≥ Meta. Validar direção + magnitude plausível, não igualdade. | ✅ conversões sempre maiores; cliques ≈ iguais |
| **Derivadas** | `CTR`, `CPC`, `CpL`, `Conv. LP` | Recalcular dos primitivos nos 2 lados; herdam a dif. dos primitivos. | ✅ coerentes (CpL menor, Conv.LP maior no BunzzAI) |
| **Ausentes** | `reach`, `frequency`, `video_*` | BunzzAI não expõe (ou conceito diferente) → `N/A`, sem veredito. | ✅ marcado N/A |
| **Borda de janela** | todas | Registrar datas de snapshot usadas; ±1-2% = timing, não erro. | ✅ documentado |

Tolerâncias do harness: `TOL_MATCH = 3%` (bate), `TOL_SOFT = 10%` (borda de dia). Ajustar lá se preciso.

---

## 5. Pegadinhas descobertas (cheat-sheet de erros a evitar)

1. **Casar por `meta_id`, não por nome** — nomes se repetem (2 adsets idênticos nesta campanha).
2. **BunzzAI duplica registros de campanha** com o **mesmo `meta_id`** e ids internos diferentes
   (ex.: meta `6976702618916` aparece como bz 191/192/193). Ao listar, deduplicar por `meta_id`.
3. **BunzzAI não tem métrica nativa de adset/campanha** → somar os ads. (Confere: ad442 + ad443 =
   campanha, tanto no cumulativo `727,59 + 723,67 = 1.451,26` quanto na janela.)
4. **Snapshots cumulativos, vários por dia (~3-4)** → usar o de maior `recorded_at`; janela = diff.
5. **Agregador Meta dá CTR/CPM/CPC como AVG das diárias** → recalcular dos primitivos (o harness faz).
6. **`tool_get_ad_performance` é flaky** (derruba a conexão; re-tentar) → `get_campaign_data` é plano B.
7. **Rate limit Meta (cód. 17)**: `fetch_insights --include-ads` re-coleta estrutura inteira →
   estoura. Bypass: estrutura já populada + `_ensure_ads_populated` neutralizado.
8. **`leads` = pixel primário; `conversoes` = todas** → BunzzAI maior por design (não é erro).
9. **`SUM(reach)` diário ≠ reach único** e **frequência cumulativa ≠ AVG diária** → não auditar reach/freq. Além disso, **reach e vídeo nem existem no MCP** (re-verificado 2026-05-29 — ver nota em §2): podem estar no produto/UI, mas não nos endpoints.
10. **CpL "bom demais" no BunzzAI** pode ser inflado pelas conversões amplas — confirmar com
    `/meta-ads-trends` antes de decisão de budget grande (regra que já estava no `CONTEXT.md`).

---

## 6. Arquivos

| Arquivo | Papel |
|---|---|
| `meta-ads/scripts/audit_vs_bunzzai.py` | **Harness** — Meta (SQLite) + arquivos BunzzAI → tabelas classificadas. Read-only. |
| `tmp/audit_spec.json` | Spec da rodada (tripla + caminhos dos `monitoring_history`). Modelo reusável. |
| `tmp/fetch_insights_light.py` | Workaround do rate limit (coleta sem re-fetch de estrutura). |
| `meta-ads/scripts/cache_manager.py` | `get_campaigns/get_adsets/get_ads`, mapa de contas, `get_connection`. |
| `meta-ads/scripts/benchmark_checker.py` | `aggregate_metrics_for_period` (agregador oficial Meta). |
| `tmp/*.py`, `tmp/*.txt`, `tmp/audit_report.md` | Throwaway desta rodada (untracked; podem ser apagados). |

---

## 7. Log de auditorias

### 2026-05-29 — Buzzmonitor Brasil (`buzzmonitor_brl`)

**Tripla auditada** (casada por `meta_id`):

| Nível | Meta ID | BunzzAI ID | Nome |
|---|---|---|---|
| Campanha | `6947326506716` | 123 | `[BR][CONVERSÃO[Guia-Social-Listening]` (material_rico; pixel `custom.979489544615879`) |
| Adset | `6947326506916` | 363 | `[Lookalike 1% Visitantes Social Listening]` (1 ad) |
| Ad | `6947326506516` | 443 | `GUIA 01 - Dados não mudam` |

Janela: **7d = 2026-05-22..2026-05-28** (snapshots BunzzAI usados: 05-21 → 05-28).
Cron travado: **nenhum** (ambos os ads com cobertura 04-24..05-28, 35 dias).

**Janela 7d — AD (GUIA 01):**

| Métrica | Meta | BunzzAI | Δ | Leitura |
|---|---|---|---|---|
| Investimento | R$ 141,76 | R$ 143,01 | +0,9% | ✅ MATCH |
| Impressões | 7.547 | 7.456 | −1,2% | ✅ MATCH |
| Alcance | 7.229 | — | — | N/A (BunzzAI não expõe) |
| Cliques | 83 (link) | 87 (total) | +4,8% | dif. esperada (BunzzAI ≥) |
| Conversões | 23 (lead) | 28 (todas) | +21,7% | dif. esperada (BunzzAI ≥) |
| CPM | R$ 18,78 | R$ 19,18 | +2,1% | ✅ MATCH |
| CpL / custo-conv | R$ 6,16 | R$ 5,11 | −17,1% | derivada (mais conversões) |
| Conv. LP | 27,71% | 32,18% | +16,1% | derivada |

**Janela 7d — CAMPANHA (soma de 2 ads):** Investimento R$ 284,32 vs 286,26 (+0,7% ✅); Impressões
13.835 vs 13.735 (−0,7% ✅); Cliques 163 vs 166 (+1,8%); Conversões 43 vs 51 (+18,6% esperado);
CPM R$ 20,55 vs 20,84 (+1,4% ✅). *(Adset = ad, pois o adset tem 1 ad só.)*

**Cumulativo (lifetime até 05-28) — AD:** Investimento R$ 732,40 vs 723,67 (−1,2%); Impressões
40.954 vs 40.447 (−1,2%); Cliques 510 vs 505 (−1,0%, ≈ iguais — borda); Conversões 159 vs 171
(+7,5% esperado). **CAMPANHA:** R$ 1.469,41 vs 1.451,26 (−1,2%); 77.033 vs 76.114 impr (−1,2%);
1.033 vs 1.020 cliques (−1,3%); 306 vs 323 conversões (+5,6%).

**Tendência do ad (BunzzAI vs Meta):** 15d e 30d batem ainda melhor (spend/impr ±2,4% e ±0,2%);
conversões sempre BunzzAI maior (+11,9% a +21,7%); cliques oscilam ±2% em torno de zero (borda).

**Veredito:** ✅ **BunzzAI está correto.** `spend`/`impressions`/`CPM` batem dentro de ±2,5% em todas
as janelas — o resíduo é horário do snapshot (≈16h). `conversions` é sistematicamente maior porque
conta **todas** as conversões do pixel (Meta conta só a primária). `clicks` total ≈ link aqui (poucos
cliques não-link). Nenhuma divergência inexplicada. Cron sem congelamento.

**Achados extra (qualidade de dado do BunzzAI):** registros de campanha **duplicados** por `meta_id`;
`tool_get_ad_performance` **instável** (derruba conexão; precisou retry). Ambos não afetam a corretude
dos números, mas valem reporte ao time do BunzzAI.
