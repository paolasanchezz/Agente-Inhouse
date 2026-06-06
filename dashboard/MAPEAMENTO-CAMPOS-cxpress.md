# Mapeamento de campos — Dashboard Funil Inbound **Cxpress Brasil** → Supabase

> **Propósito:** define o funil e mapeia os campos da dashboard `relatorio-semanal-cxpress-brasil.html`
> contra a tabela do Supabase. É o equivalente Cxpress do `dashboard/MAPEAMENTO-CAMPOS.md` (Buzzmonitor BR).
>
> **Status (2026-06-01):** a tabela `cxpress_deals_funil_principal_prod` **existe mas está vazia (0 linhas)**.
> O gerador roda e produz a dashboard zerada; os números reais aparecem assim que a tabela for sincronizada.
> Os critérios abaixo (parsing de datas, escopo inbound/CM) são **provisórios** e devem ser confirmados
> contra os dados reais na 1ª carga — exatamente como o filtro do Buzzmonitor foi construído auditando o banco.
>
> **Conexão:** mesmo banco do Brasil (`looker_readonly`), `SUPABASE_PG_URL` em `dashboard/.env`.

---

## 0. Resumo (por que difere do Buzzmonitor)

| Dimensão | Buzzmonitor BR | Cxpress BR |
|---|---|---|
| Tabelas | 2 (`deals_comercial_prod` + `deals_contratos_prod`) | **1** (`cxpress_deals_funil_principal_prod`) |
| Atribuição | `account_id` + janela 90d cross-table | **por linha** (todas as datas do funil estão na própria linha) |
| Dedup | por e-mail | **por deal** (a tabela não tem coluna de e-mail; há `contact` bigint) |
| Funil | Lead → CE → Reun. Agendada → Reun. Realizada → Proposta → Fechamento | Lead → **Triagem → Agendamento → Demo realizada** → Proposta → Fechamento |
| Idioma / moeda | PT-BR / BRL | PT-BR / BRL (igual) |

Como cada deal carrega todas as datas de etapa na própria linha, **não há CTE de conversões, nem
regra de 90 dias, nem UNION** — as queries (`queries_cxpress.py`) são mais simples que as do Brasil.

---

## 1. Tabela-fonte

`cxpress_deals_funil_principal_prod` — colunas relevantes:

**Básicas:** `id` (bigint, PK) · `title` · `cdate` (timestamptz — criação) · `mdate` · `status` (text) ·
`stage` (bigint) · `currency` · `contact` (bigint) · `owner` · `group` · `funil_auto` · `origem_do_lead`

**Datas das etapas (TEXTO — ver §5):** `data_de_criacao_auto` · `data_triagem_realizada_auto` ·
`data_do_agendamento_auto` · `data_de_demo_realizada_auto` · `data_do_envio_da_proposta_auto` ·
`data_do_fechamento_auto` · `data_do_lost_auto` · (apoio: `data_e_hora_da_demo`, `data_noshow_1..3`)

**Atribuição de canal:** `utm_source` · `utm_medium` · `utm_campaign` · `utm_content` · `utm_term` ·
`utm_creative` · `url_conversao` · `gclid`

**Valor (TEXTO):** `cxpress_fee_mensal` · `valor_atualizado_do_fee` · `valor_do_upsell`

**Responsáveis:** `closer_bd_auto` · `sdr_bdr_auto`

**Perda:** `data_do_lost_auto` · `motivo_de_perda_closer_sdr` · `contexto_do_lost_closer_sdr` · `etapa_do_lost`

---

## 2. Escopo (inbound + Content Marketing) — **NO-OP por padrão**

Em `queries_cxpress.py`, `filtro_inbound()` e `filtro_cm()` retornam `"TRUE"` por padrão — ou seja, a
dashboard conta **todas as linhas da tabela**. Isso é proposital: com 0 linhas não dá para calibrar
nenhum filtro sem chutar (e um whitelist errado esconde dados silenciosamente).

**Ao ter dados, calibrar nesta ordem:**

1. **Inbound** — inspecionar `SELECT funil_auto, origem_do_lead, count(*) ... GROUP BY 1,2`. Se a tabela
   misturar inbound/outbound, ligar `filtro_inbound()` para `funil_auto ILIKE '%inbound%'` (ou o valor real).
2. **Content Marketing** (opcional) — se a Victor quiser estreitar só a CM (como no Buzzmonitor), auditar
   `utm_source` / `url_conversao` reais e preencher `CM_UTM_SOURCES` + domínio de conteúdo Cxpress, depois
   trocar `filtro_cm()` para `return _filtro_cm_provisorio(alias)`. **Decisão pendente** se a dashboard é
   "todo o inbound" ou "só CM" — o chip/título atual diz **"Funil Inbound"** (não "Content Marketing"),
   condizente com o escopo no-op. Se virar CM, ajustar o rótulo em `gerar_relatorio_cxpress.py`.

Ambas as funções são pontos de extensão isolados — mudar só elas, sem tocar nas queries.

---

## 3. Sem regra de 90 dias

O Buzzmonitor atribui eventos pós-conversão via `account_id` + janela de 90d entre duas tabelas. A Cxpress
tem **uma tabela só**: cada deal já traz `data_triagem_realizada_auto`, `data_do_agendamento_auto`, etc. na
própria linha. Logo cada etapa é contada diretamente pela sua data, sem cross-join nem janela de atribuição.

---

## 4. Funil (contagem por data do evento)

| # | Etapa | Coluna de data | Observação |
|---|---|---|---|
| 1 | **Lead** | `cdate` | criação do deal (timestamptz) |
| 2 | **Triagem** | `data_triagem_realizada_auto` | — |
| 3 | **Agendamento** | `data_do_agendamento_auto` | demo/reunião agendada |
| 4 | **Demo realizada** | `data_de_demo_realizada_auto` | — |
| 5 | **Proposta** | `data_do_envio_da_proposta_auto` | valor em `cxpress_fee_mensal` |
| 6 | **Fechamento** | `data_do_fechamento_auto` | valor em `valor_atualizado_do_fee` (fallback `cxpress_fee_mensal`) |
| — | **Perdido** | `data_do_lost_auto` | + `motivo_de_perda_closer_sdr`, `etapa_do_lost` |

Cada KPI conta pela data da **sua** etapa (não pela criação) — igual à regra inegociável do Brasil.

---

## 5. ⚠️ Datas chegam como TEXTO

As colunas `data_*_auto` são `text` no Supabase (vêm assim do ActiveCampaign). O helper `_d()` em
`queries_cxpress.py` faz cast defensivo assumindo **ISO `YYYY-MM-DD`** (pega os 10 primeiros chars; devolve
NULL para qualquer outro formato, então um valor torto nunca quebra a query inteira).

**Conferir na 1ª carga:** rodar `SELECT data_triagem_realizada_auto FROM cxpress_deals_funil_principal_prod
WHERE data_triagem_realizada_auto <> '' LIMIT 20`. Se vier em `DD/MM/YYYY` ou `MM/DD/YYYY`, ajustar **só** o
`_d()` (ponto único) — senão a dashboard mostra zeros mesmo com dados.

---

## 6. Valor (texto → BRL)

`cxpress_fee_mensal` e `valor_atualizado_do_fee` são texto. O parse acontece em Python
(`render_helpers.parse_valor_text`, que trata `R$`, milhar `.` e decimal `,`). Fechamento usa
`COALESCE(valor_atualizado_do_fee, cxpress_fee_mensal)`. Moeda de reporte: **BRL**.

---

## 7. Validação / pendências

1. **Tabela vazia (2026-06-01):** fixar números-âncora YtD após a 1ª sincronização (igual à conferência 6/6
   do Brasil) e considerar um smoke test em `gerar_relatorio_cxpress.py` (hoje não há, porque não há baseline).
2. **Formato das datas** (§5) — confirmar ISO.
3. **Escopo** (§2) — decidir inbound-completo vs só-CM e calibrar os filtros.
4. **Dedup** — sem e-mail; se aparecerem deals duplicados por empresa, avaliar dedup por `contact`/`cnpj`.
5. **`stage`/`status`** — mapear os valores reais (ex.: `status='Ganho'` confirma fechamento? há `Perdido`?)
   e, se útil, cruzar com as datas de etapa.
