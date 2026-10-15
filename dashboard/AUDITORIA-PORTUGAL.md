# Auditoria das tabelas de Portugal — viabilidade das dashboards CM PT

Data: 2026-09-09 · Read-only, direto no Supabase (`SUPABASE_PG_URL`) · escopo: as 7 tabelas `deals_*_portugal`.

Feita **antes** de construir as 3 dashboards PT (Buzzmonitor, Cxpress, Elife), para saber se os campos que o filtro CM e o funil precisam estão realmente preenchidos.

---

## 1. O que existe

| Marca | Tabelas | Linhas | 2026 |
|---|---|---|---|
| **Buzzmonitor PT** | `deals_bm_inbound_portugal` · `deals_bm_outbound_portugal` · `deals_bm_contratos_portugal` | 773 · 1520 · **0** | 311 |
| **Cxpress PT** | `deals_cxpress_inbound_portugal` · `deals_cxpress_outbound_portugal` | 493 · 6 | 267 |
| **Elife PT** | `deals_elife_inbound_portugal` · `deals_elife_outbound_portugal` | 1066 · 44 | 91 |

Apoio: `dim_accounts_portugal` (15.697), `dim_contacts_portugal` (20.409), `dim_stages_portugal` (66), `dim_users_portugal` (5), `dim_tags_portugal` (519), `dim_notes_portugal` (2.449), `dim_tasks_portugal` (61).

**As 7 tabelas têm exatamente as mesmas 84 colunas.** Mesma família da LATAM, com os campos em PT-PT (`conteudo_conversao` onde a LATAM tem `contenido_conversao`, `data_de_fecho_do_negocio` onde tem `fecha_de_cierre_de_negocio`). Uma diferença a favor: **PT tem `account_id`**, que a LATAM não tem.

**Ingestão está viva:** `last_synced_at` = 2026-09-08 nas 7, `mdate` mais recente entre 04 e 08/09. Não há tabela parada.

`deals_bm_contratos_portugal` existe mas está **vazia** — e não há equivalente para Cxpress nem Elife. Ou seja, o padrão da LATAM (fechamentos vindos de `contratos_staging`) **não se repete aqui**.

---

## 2. Rastreio — recorte 2026 (o escopo das dashboards)

Os percentuais sobre a tabela inteira enganam: 2023 responde por metade do histórico e quase não tem UTM. O que vale é 2026.

| | deals 2026 | `utm_source` | `url_conversao` | **sem rastreio nenhum** |
|---|---|---|---|---|
| Buzzmonitor PT | 311 | 25,7% | 78,5% | **21,5%** |
| Cxpress PT | 267 | 40,1% | 46,8% | **49,8%** |
| Elife PT | 91 | 72,5% | 86,8% | **13,2%** |

"Sem rastreio nenhum" = `utm_source` **e** `url_conversao` vazios — o deal fica invisível para o filtro CM.

**Comparação que importa:** o baseline do Brasil é 40-54% de deals sem rastreio ([[reference_br_deals_sem_rastreio]]). Então **Buzzmonitor PT e Elife PT estão melhores que o BR**, e Cxpress PT está no teto do baseline — ruim, mas não é anomalia nem automação quebrada.

`evento_conversao` (1-7%) e `conteudo_conversao` (0-3%) são praticamente inúteis em PT. Na LATAM esses campos são o rastro de 1º toque que salva lead "sumido" ([[reference_dashboard_latam_dominio_material]]); aqui esse recurso não existe.

### Domínios de conversão PT (base do filtro CM)

Diferentes dos de BR/LATAM — a lista precisa ser própria:

- **Buzzmonitor:** `conteudo.getbuzzmonitor.com` (184) · `getbuzzmonitor.com` (44) · `material.buzzmonitor.com` (12) · `buzzmonitor.pt`
- **Cxpress:** `www.cxpress.pt` (103) · `cx.elifeportugal.com` (11) · `content.cxpress.io` (5)
- **Elife:** `cx.elifeportugal.com` (54) · `conteudo.getbuzzmonitor.com` (21) · `www.elifeportugal.com`

Note o cruzamento: deals de Cxpress e Elife convertem em LPs do Buzzmonitor e vice-versa. Agrupar por domínio **não** separa marca.

### Higiene de UTM (2026)

Poucos valores distintos, mas com lixo que precisa de normalização no filtro:

- **Placeholder não substituído:** `{utm_source}` (2) e `{{site_source_name}}` (1) na Cxpress — tag do Meta que não resolveu.
- **Teste em produção:** `test_Source` (2) e `Test_source` (1) no Buzzmonitor.
- **Mesma fonte em 3 grafias:** `meta` / `fb` / `ig` convivem (Cxpress: fb=39, ig=35, meta=6). E `linkedin` (9) × `Linkedin` (3) no Elife.
- **`url_conversao` nem sempre é URL:** aparecem `Formulário Cxpress`, `Formulário Elife Portugal Inglês - 14/09/22`. Qualquer parse por domínio precisa tolerar isso.

---

## 3. Funil e fechamento — onde trava

### 3.1 `status` funciona, e é texto legível

Ao contrário do BR/LATAM (0/1/2), em PT o `status` já vem como **`Aberta` / `Ganho` / `Perdido`**.

| | Ganhos (histórico) | com `mdate` em 2026 | criados em 2026 | soma `value` |
|---|---|---|---|---|
| Buzzmonitor PT | 27 | 13 | 6 | € 22.817,61 |
| Cxpress PT | 11 | 11 | 3 | € 4.660,00 |
| Elife PT | 11 | 3 | 0 | € 15.825,00 |

Só **1 deal perdido** marcado em toda a base (`deals_bm_outbound_portugal`). Ou seja: **`Perdido` não é usado** — o time PT arrasta o deal para a etapa "Perdidos" mas não muda o status. Um KPI de perdidos tem que sair de `stage`, não de `status`.

### 3.2 Nenhum evento de funil é datável — este é o bloqueador

Não é só o fechamento. **Nenhum marco intermediário tem data em PT.** Varredura de todos os 19 campos de data/evento nos 669 deals de 2026:

| Campo | Preenchido em 2026 |
|---|---|
| `data_de_criacao` | 2,2% |
| `data_de_fecho_prevista` | 1,8% |
| `data_de_atualizacao` | 0,9% |
| `data_de_fecho_do_negocio` | **0,6%** (4 deals) |
| `data_do_primeiro_contacto` | 0,3% |
| `score_pos_reuniao` · `data_do_evento_ou_webinar…` · `evento_que_impulsionou_o_fecho` | **0%** |

E, o mais importante: **não existe `data_de_reuniao` nem data de proposta enviada nas tabelas PT.** A LATAM tem `fecha_de_reunion`; o schema PT não herdou esse campo. Também **não há tabela de histórico de mudança de etapa** — `dim_stages_portugal` é o dicionário de etapas, não o registo de movimentos. `dim_tasks_portugal` tem 61 linhas no total (irrelevante).

`dim_notes_portugal` cobre 23% dos deals de 2026, mas as notas são captura automática de formulário ("Dados de Contacto… registou-se na página https://…"): em 246 notas de 2026, **1 menciona reunião e 2 mencionam proposta**. Não serve para datar marco de funil.

Consequência: **usar data de reunião ou de proposta como proxy é impossível — o dado não existe.** As saídas reais são:

1. **Coorte por `cdate`** (única data 100% preenchida). O date-picker filtra os deals *criados* no período e o funil mostra até onde essa coorte chegou hoje. É a convenção COORTE que a dashboard BR já usa nos perdidos ([[feedback_dashboard_paridade_buzz]]) e responde à pergunta que interessa a Content Marketing: *dos leads que entraram em agosto, quantos chegaram a reunião, proposta e fecho.* Contrapartida: é uma foto "até hoje", então meses recentes parecem piores porque a coorte ainda não amadureceu.
2. **`mdate` como proxy** de data de fecho. Rejeitado na LATAM ([[project_dashboard_latam]]) porque muda a cada edição e empurra fechamento antigo para a frente. Para deal já ganho o erro é menor, mas continua sendo data de "último toque", não de fecho.
3. **Corrigir na origem:** criar o campo de data de reunião no ActiveCampaign PT e passar a preencher `data_de_fecho_do_negocio`. É correção de coleta, não de dashboard — e só passa a valer dali para a frente.

O volume relativiza a discussão: com 3 a 13 fechamentos por marca no ano, nenhuma série temporal de fechamento se sustenta — no máximo um número absoluto.

### 3.3 `closer` / `sdr` vazios

`closer` 0,7-3,7% e `sdr` 0,4-1,6% (fora a Cxpress outbound, que tem 6 deals). `origem_do_lead_negocio` 0,7-4,4%.

Consequência: **não dá para fazer o corte Inbound × Outbound por campo curado** (o `funil_bd_sdr` do BR — [[reference_dashboard_funil_bd_sdr]]). Em PT a separação vem da **tabela de origem** (`_inbound_` × `_outbound_`), que é o que a LATAM já faz. Também não dá para fazer funil de SDR nem tempo de resposta.

### 3.4 Stages: 9 pipelines com nomes repetidos

`dim_stages_portugal` tem 66 etapas espalhadas por 9 `group_id`. O mesmo nome aparece em vários pipelines com ids diferentes — "Iniciar Contato" é id 1, 4, 29, 43, 52, 55. Mapear por **`title_normalized`**, nunca por `stage` id.

As etapas PT também não batem 1:1 com as de BR/LATAM. Além das comuns (Iniciar Contato, Tentando Contato, Em Contato, Reunião, Proposta, Follow-Up, Fecho de Negócio, Perdidos), existem: **Reciclagem, Desqualificado, Material Rico, Curso, Stand-By, Trial (Buzzmonitor), Review, Forecast/Negociação, A formalizar contrato, Clientes, Churn**.

"Material Rico" é especialmente relevante: é o equivalente PT do lead de conteúdo — provavelmente a etapa que mais interessa numa dashboard de Content Marketing.

---

## 4. Volume — Elife PT é magra

Buzzmonitor PT (311 deals em 2026) e Cxpress PT (267) sustentam uma dashboard. **Elife PT tem 91 deals em 2026, nenhum ganho criado no ano, e 0 deals outbound em 2026** — o histórico dela é 2023 (548) e 2024 (418). Uma dashboard de Elife PT hoje mostra sobretudo passado.

---

## 5. Veredito

| Pergunta | Resposta |
|---|---|
| As tabelas PT existem e estão sincronizadas? | Sim, as 7, sync de 08/09. |
| Os deals têm UTM? | Parcialmente — 26-73% conforme a marca. |
| Os deals têm `url_conversao`? | Sim, e é o campo forte: 47-87%. |
| Dá para rodar um filtro CM? | **Sim**, com lista de domínios própria e normalização de UTM. A cobertura é comparável à do Brasil. |
| Dá para medir fechamento? | **Não com data.** Nem fechamento, nem reunião, nem proposta — nenhum marco é datável (§3.2). |
| Dá para separar Inbound × Outbound? | Sim, pela tabela de origem. Não por campo curado. |
| Dá para funil por etapa? | Sim, via `title_normalized` — com mapa PT próprio. |

**Decidido com o Victor (09/09):** as **3 dashboards** saem juntas, incluindo Elife PT apesar do volume magro.

**Datação decidida (09/09):** coorte por `cdate`. O pedido inicial era usar data de reunião ou de proposta como proxy; o §3.2 mostra que esses campos não existem em PT e que não há como derivá-los. As 3 dashboards foram construídas com esse modelo e estão no ar em `dashboards-elife.vercel.app/bm-pt/`, `/cxpress-pt/` e `/elife-pt/`.

**Reuniões e Fechamento por etapa (decidido com o Victor, 15/10):** continuam sem data. São contadas pela etapa atual dentro da mesma coorte por `cdate`:

- **Fechamento** = etapa atual Fecho de Negócio ou Cliente (Contrato, A formalizar contrato, Clientes). O `status` não entra. O KPI antigo "Ganhos" somava etapa **e** `status = 'Ganho'`: no Buzzmonitor PT davam 7 em 2026, sendo 3 em Fecho de Negócio, 2 em Contrato e 2 parados em Proposta com status Ganho. A página agora mostra 5 e lista à parte os deals com status Ganho fora da etapa de fecho, pra o time corrigir no CRM.
- **Reunião** = etapa atual na Reunião ou depois dela, pelo `stage_order` do próprio pipeline. A ordem muda de pipeline para pipeline (o Follow-Up vem antes da Reunião no pipeline 1 e depois da Proposta nos pipelines 5 a 8), por isso a comparação é feita dentro do `group_id`. Etapas laterais (Perdidos, Desqualificado, Reciclagem, Stand-By, Material Rico, Curso, Churn) ficam de fora mesmo quando vêm depois da Reunião na ordem. **É um piso:** quem teve reunião e hoje está em Perdidos não aparece, porque nada registra a passagem.
- A lista "Deals da coorte" perdeu o corte de 300 linhas. Com 338 deals no YtD do Buzzmonitor PT, o corte escondia os criados em jan/fev, e com eles 2 dos fechamentos que o KPI contava.

Lógica em `queries_portugal.chegou_reuniao()` e `ETAPAS_GANHAS`.

**Se um dia o dado melhorar:** basta o time PT passar a preencher `data_de_fecho_do_negocio` (e, idealmente, ganhar um campo de data de reunião no ActiveCampaign) para que a coorte possa conviver com uma série temporal de fechamento de verdade. A lógica está isolada em `dashboard/queries_portugal.py`.

Scripts da auditoria ficaram no scratchpad da sessão (descartáveis) — tudo aqui é reproduzível com os `SELECT` descritos acima.
