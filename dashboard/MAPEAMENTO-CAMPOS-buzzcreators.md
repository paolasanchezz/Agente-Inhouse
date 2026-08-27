# Mapeamento de campos — Dashboard CM **Buzzcreators Brasil**

Paralelo de `MAPEAMENTO-CAMPOS.md` (Buzzmonitor BR) e `MAPEAMENTO-CAMPOS-cxpress.md`.
Fonte única da lógica: `dashboard/queries_buzzcreators.py`. Criado em 2026-08-26.

---

## 1. A diferença estrutural: o deal não tem UTM

As outras três dashboards leem UTM direto da linha do deal (ActiveCampaign). Aqui não dá:
a fonte é o **Pipedrive** (`deals_pipedrive_vendas_buzzcreators`, 86 colunas + `custom_fields`
jsonb) e **não existe nenhum campo de UTM** — nem coluna, nem chave em `custom_fields`.
Rechecado em 26/08/2026.

A atribuição é **recuperada por join com o contato**:

```
deal.person_id ─→ dim_pipedrive_persons.custom_fields
                    '*UTM Source [AUTO]'   '*UTM Medium [AUTO]'   '*UTM Campaing [AUTO]'
                    '*UTM Content [AUTO]'  'URL Conversão [AUTO]' 'URL de Origem [AUTO]'
        │
        └─ fallback por e-mail ─→ dim_contacts (ActiveCampaign)
                    utm_source_auto · utm_source_origem_auto · utm_medium_auto
                    utm_campaing_auto · utm_content_auto · url_conversao_auto
```

Cobertura medida (26/08/2026, base de 3.047 deals):

| Caminho | Deals com atribuição | % |
|---|---|---|
| Só o deal (campo `Origem do negócio Inbound [AUTO]`) | 213, e ~0 desde março | 7% |
| `person_id` → `dim_pipedrive_persons` | 1.685 | 55% |
| + fallback por e-mail em `dim_contacts` | 2.154 | **71%** |
| — só `utm_source` (o que o filtro CM usa) | 1.925 | 63% |

No funil Inbound isolado: 1.560/1.928 (81%).

### Ressalvas do método (estão escritas na própria dashboard)

1. **Last touch.** Os campos `[AUTO]` do contato são sobrescritos a cada nova conversão. A UTM
   lida é o **último toque conhecido do contato**, não necessariamente o que gerou o deal —
   em 1.026 dos 1.685 casos o contato foi atualizado 7+ dias depois da criação do deal.
   O lado Pipedrive não guarda histórico datado. O AC guarda (`url_conversao_1..5`,
   `utm_campaign_1..5`, `data_ultima_conversao_auto`) — reconstruir o toque mais próximo da data
   do deal é a evolução natural desta dashboard, ainda não implementada.
2. **Lead sem UTM nas duas bases fica fora.** Não há propagação por empresa/domínio como no
   `/auditar-deals-cm` do BR.
3. **Degradação em jul/ago-2026.** Inbound sem atribuição por mês: 3 (jun) → 158 (jul) → 142 (ago),
   junto com uma importação de 19.070 contatos no Pipedrive em julho. Não diagnosticado ainda —
   pode ser lag do sync AC↔Pipedrive ou captura de UTM quebrada no fluxo novo de lead.
   **Não leia jul/ago como queda de performance de CM sem checar isso.**

---

## 2. Filtro de Content Marketing

Calibrado com o Victor em 2026-08-26 sobre a distribuição real dos 3.047 deals.
Constante: `CM_UTM_SOURCES` em `queries_buzzcreators.py`.

**Regra:** `utm_source` recuperado (lower/trim) ∈ whitelist. **O domínio não credita sozinho** —
um lead que converteu numa LP de conteúdo mas veio com `utm_source=cs` fica fora (decisão explícita).

### Entra

| Grupo | Sources |
|---|---|
| Meta / social | `meta`, `instagram`, `instagram_feed`, `instagram_stories`, `instagram_reels`, `reels`, `feed`, `ig`, `fb`, `facebook`, `tiktok` |
| Link na bio | `instabio`, `insta-bio`, `bio`, `link_in_bio` |
| LinkedIn | `linkedin`, `inmail` |
| E-mail / mensageria | `email`, `newsletter`, `sms`, `whatsapp` |
| Conteúdo próprio | `blog`, `notion`, `oferta` |
| Webinar / LP | `webinar`, `pos-webinar`, `apresentacao-webinar`, `apresentacao`, `webinar-ao-vivo`, `inscrito em webinar`, `lp-agradecimento`, `lp-pos-evento` |
| Eventos | `eventos`, `buzzsummit`, `influent-summit`, `panfleto-influent-summit`, `convites` |
| GEO / orgânico | `chatgpt.com`, `gemini`, `perplexity.ai`, `organic`, `organic/direct` |

### Fica fora (e por quê)

| Source | Volume | Motivo |
|---|---|---|
| `google` | 1.297 (1.291 com `medium=cpc`) | Search **pago**. Mesma decisão da dash BR, onde `google` está em `INTERNOS_EXCLUIR` |
| `cs`, `cs_buzz`, `cs-buzzmonitor`, `comercial`, `bds`, `sdr` | ≈100 | Toque do próprio time, não aquisição |
| `plataforma`, `app-buzzmonitor` | 2 | Link interno do produto |
| `redes-sociais` | 3 | Na dash BR o Victor confirmou que **não** é CM (era CS tagueando expansão de cliente) |
| `thebizness` | 1 | Newsletter parceira — fora até confirmação |
| `%utm_source_novo%`, `{{placement}}`, `teste_origem`, `null`, `others` | ≈80 | Tracking quebrado (macro não substituída) |

Resultado: **436 deals** no escopo CM (YtD 2026: 427 leads).

### Domínios de conteúdo (referência, não creditam sozinhos)

`conteudo.buzzmonitor.com.br` (319) · `pages.buzzcreators.com.br` (89) ·
`webinar.buzzmonitor.com` (20) · `evento.buzzmonitor.com` (9).
`www.buzzcreators.com.br` **não** é domínio de conteúdo: 932 das 1.420 conversões lá são google/cpc.

---

## 3. Funil e datas de etapa

| Etapa | Campo | Preenchimento |
|---|---|---|
| Lead | `add_time::date` | 100% |
| Agendamento | `custom_fields->>'Data do agendamento [SDR ou AUTO]'`, fallback `'[SDR\|BDR] Data da Reunião Agendada'` | 427 + 75 na base inteira |
| Reunião realizada | `custom_fields->>'Data da Reunião Realizada [BD ou AUTO]'` | 358 |
| Fechamento | `coalesce(won_time::date, data_aceite, custom_fields->>'Data do aceite [BD]*')` | 31 / 34 / 34 |
| Perdido | `lost_time::date` + `status='lost'` (coorte por data do lead) | 2.409 |

Todas as datas em `custom_fields` vêm como texto **ISO `YYYY-MM-DD`** (verificado 26/08/2026).

**A etapa Proposta foi omitida de propósito** (decisão Victor, 2026-08-26): o Pipedrive não registra
data de entrada em Proposta — só 34 deals têm `Data do aceite`. Contar Proposta por estágio atual
não seria comparável entre períodos, que é a premissa de toda a dashboard.

Estágios do pipeline "Vendas Buzzcreators", para referência: Lead Distribuído (23) · Prospecção (24) ·
Conexão (25) · Nutrição (26) · Qualificação (27) · Reunião Agendada (28) · Reunião Realizada (29) ·
Proposta (30) · Fechamento (31).

**Perdidos** não exigem `lost_reason` preenchido (2.302 de 2.409 têm) — exigir esconderia ~4% das
perdas reais. O motivo aparece só como coluna da lista.

---

## 4. Diferenças deliberadas vs as outras dashboards

| Item | Buzz BR / Cxpress / LATAM | Buzzcreators |
|---|---|---|
| Origem da UTM | coluna do próprio deal | recuperada do contato (2 hops) |
| Etapas | 6 + perdidos | **4 + perdidos** (sem Triagem, sem Proposta) |
| Filtro de funil | remove `Outbound` (`funil_bd_sdr`) | **não filtra** — `origem_lead` marca como o time abordou; um lead prospectado que já tinha convertido em conteúdo continua sendo CM. O filtro de source já segura o que importa. `origem_lead` vai exportado e aparece na lista de leads |
| Regra 90d de herança | sim (BR) | não se aplica (não há propagação por contato/empresa aqui) |
| Dedup por e-mail | BR sim | não — conta por deal |
| Link do deal | ActiveCampaign | `app.pipedrive.com/deal/{id}` |
| Moeda | BRL | BRL (`currency` 100% BRL na base) |

---

## 5. Gate de paridade

As outras dashboards comparam o motor.js contra a **dash local** em Python. A Buzzcreators nasceu
direto no modelo dinâmico-estático (não existe dash local), então o gate compara **duas
implementações independentes da mesma regra**:

- SQL — `q_kpis_periodo` / `q_ranking` agregando no Postgres
- JS — `motor.js` agregando no navegador sobre o JSON exportado

6 intervalos (7d, 30d, 90d, MtD, YtD e um intervalo livre atravessando meses), KPIs + tamanho das
5 listas + rankings de fonte e conteúdo. Última execução: **800 checagens, 0 divergências**.
