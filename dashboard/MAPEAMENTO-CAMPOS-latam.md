# Mapeamento de campos — Dashboard Content Marketing **LATAM** → Supabase

> **Propósito:** define o critério de "o que é Content Marketing" para a operação **Buzzmonitor LATAM**
> (mercado hispano) e mapeia os campos/funil contra o Supabase. É o equivalente LATAM do
> `dashboard/MAPEAMENTO-CAMPOS.md` (Brasil).
>
> **Status:** critério travado em 2026-05-29 a partir de auditoria read-only dos dados.
> Construção sobre tabelas `_staging` (decisão do Victor) — revalidar se forem promovidas a `_prod`.
>
> **Conexão:** mesmo banco do Brasil (`looker_readonly`), MCP `mcp__supabase__execute_sql`.

---

## 0. Resumo executivo (por que o critério LATAM ≠ Brasil)

O Brasil classifica CM por `utm_source` + domínio de conteúdo (`buzzmonitor.com.br`). A LATAM **pode
usar a mesma lógica**, com duas diferenças de fonte de dados descobertas na auditoria:

1. O domínio de conteúdo da LATAM é **`getbuzzmonitor.com` / `contenido.getbuzzmonitor.com`** (não `.com.br`).
2. Os dados de canal (UTM/URL) **só estão preenchidos nas tabelas `outbound` e `contratos`** — a tabela
   `inbound` está com UTM 100% vazio (gap de ETL, ver §6). Por isso **classificamos por sinal
   (utm_source + URL), não pelo nome da tabela nem por `origen_del_lead`** (ambos não confiáveis:
   há leads de conteúdo marcados como "Outbound").

**Tamanho atual (filtro abaixo, histórico / 2026):** ~1.011 / 207 leads CM · ~65 fechamentos CM.
A cobertura cresce quando o gap de ETL do `inbound` for corrigido.

---

## 1. Tabelas-fonte

| Papel | Tabela | Linhas | Observação |
|---|---|---|---|
| Leads + funil | `deals_latam_inbound_staging` ∪ `deals_latam_outbound_staging` | 10.498 + 5.795 | **Dedup por `id`** (sobreposição = 73 ids). Nomes das tabelas NÃO são critério. |
| Fechamentos | `deals_latam_contratos_staging` | 292 | Fechado = `status='Ganho'` (72). |

**Schema (difere do Brasil):** colunas em espanhol; **não há `account_id`**; **não há email** nas tabelas de
deal; `dim_contacts`/`dim_accounts` estão **vazias** (0 linhas) — sem dimensão de pessoa/conta hoje.
Campos-chave: `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `url_conversao`, `cdate`,
`status`, `stage`, `pais`, `currency`, `value`(text), `fee_mensual`(numeric), `contact`(bigint).

---

## 2. Filtro Content Marketing LATAM (universal — todo evento)

Mesma filosofia do Brasil (decisão "igual ao Brasil" no tráfego Google):

```sql
-- FILTRO_CM_LATAM
(
  -- (1) SINAL FORTE DE URL — conta como CM independente da UTM (sobrepõe até google+cpc)
  url_conversao ILIKE '%contenido.getbuzzmonitor.com/plataforma-completa%'
  OR url_conversao ILIKE '%oferta%'
  -- (2) REGRA GERAL
  OR (
    -- exclui Google Ads (google e google_es com cpc) — 730/732 dos 'google' são cpc
    NOT (lower(coalesce(utm_source,'')) LIKE 'google%' AND lower(coalesce(utm_medium,'')) = 'cpc')
    AND (
      -- (a) domínio de conteúdo próprio da LATAM
      url_conversao ILIKE '%getbuzzmonitor.com%'          -- contenido.getbuzzmonitor.com, getbuzzmonitor.com/es/...
      -- (b) fontes sociais / owned (whitelist)
      OR lower(utm_source) IN (
        'meta','ig','instagram','facebook','fb','fb-ig','linkedin',
        'email','emailmkt','emblue','chatgpt.com','notion','blog','tiktok','youtube','reddit',
        'paid social','an'
      )
      OR lower(utm_source) LIKE 'instagram%'   -- Instagram_Feed / Instagram_Stories / Instagram_Reels / Explore...
      OR lower(utm_source) LIKE 'facebook%'    -- Facebook_Mobile_Feed / Facebook_Mobile_Reels / Facebook_Stories...
    )
  )
)
```

> **Sinal forte de URL (1):** `contenido.getbuzzmonitor.com/plataforma-completa*` e qualquer URL com
> `oferta` são páginas de produto/oferta — contam como CM **mesmo sem UTM ou com UTM de Ads**. Hoje:
> 36 casos de `plataforma-completa` (todos já no domínio), 0 de `oferta` (à prova de futuro).

**Excluídos** (não entram na whitelist, logo não contam): `google`/`google_es` + cpc (Ads),
`Pamela_Sanchez`, `equipo_comercial`, `comercial`, `ActiveCampaign`, `Customer_Success_Team`
(canais internos/SDR), e lixo de template (`{utm_source}`, `null`, `Others`, `{{placement}}`).

**Webinar / material rico:** na LATAM caem sob o domínio de conteúdo (`getbuzzmonitor.com`, slugs como
`plataforma-completa`, `analytics-pro`, `ia-para-social-listening`) ou sob fontes `email`/social — já
capturados por (a)/(b). Quando os campos `oferta_evento` / `fecha_de_evento_o_webinar...` forem
populados, refinar aqui (hoje têm cobertura quase nula).

---

## 3. Atribuição (sem regra de 90 dias)

O Brasil usa `account_id` + janela de 90 dias para atribuir eventos pós-conversão. **A LATAM não tem
`account_id`** e a dimensão de contato está vazia. Portanto:

- **Leads e eventos de funil:** classificados pelo **próprio** `utm_source`/`url_conversao` do registro.
- **Fechamentos (`contratos`):** classificados pela **própria** UTM/URL do contrato (65 batem o filtro).
  Sem janela cross-table de 90 dias (não há chave de conta para ligar).
- **Dedup:** por `id` do deal (não há dedup por pessoa — `dim_contacts` vazia). Reativar dedup por email
  quando uma fonte de contatos for populada.

---

## 4. Funil LATAM (mais curto que o Brasil)

| KPI | Coluna de data | Tabela | Preenchimento | Obs |
|---|---|---|---|---|
| Leads | `cdate` | inbound ∪ outbound | 100% | filtro CM, sem 90d |
| Primer contacto (Contato Efetivo) | `fecha_de_primer_contacto` (fallback `fecha_y_hora_de_primer_contacto`) | leads | 4.301 | — |
| Reunión (Reunião) | `fecha_de_reunion` | leads | 1.932 | — |
| ~~Propuesta~~ | — | — | — | **Não existe coluna de proposta na LATAM** → estágio ausente |
| Perdido | `status='Perdido'` | leads | 662 | sem data dedicada → datar por `mdate` (limitação) |
| Fechamento (Cierre) | `DATA_FECHO` (cierre→inicio→primer pago) | contratos | 183 (def. ampliada) | `FECHADO_LATAM`; `status='Ganho'` quase não é mantido → ver nota |

**Valor do fechamento:** coluna **`value`** (USD; cast texto→numeric). `fee_mensual` foi **descartado** — inconsistente (às vezes `value`×100, às vezes não, ex.: value=1615/fee=90000).

> **⚠️ Definição e datação do cierre (decisão Victor, 2026-06-06):**
> **(1) Fechado ≠ só `status='Ganho'`.** Esse estado quase não é mantido no AC LATAM (no stage 176 do
> pipeline Contratos, **84 de 96** estão `Aberta` apesar de terem fee + contrato + data de cierre). A
> definição (`FECHADO_LATAM`) passou a ser `status='Ganho'` **OU** `primer_pago_realizado_automatico`
> **OU** `fecha_de_inicio_de_contrato` **OU** `fecha_de_cierre_de_negocio`.
> **(2) Datação por `COALESCE(fecha_de_cierre_de_negocio, fecha_de_inicio_de_contrato, fecha_de_primer_pago_automatico)`** (`DATA_FECHO`) — datas reais, **sem `mdate`** (re-syncs em massa jogam o `mdate` para a data do sync — ex.: **01/06/2026 carimbou 36 deals** — inflando janelas curtas). Deals sem **nenhuma** das três datas ficam **fora de qualquer janela temporal** (backlog a preencher no AC).
> **Impacto (cierres CM):** all-time **2 → 34** (USD 18.334) · 2026 **1 → 7** (USD 3.049). Ex.: La Firma
> (deal [43258](https://elifeeurope.activehosted.com/app/deals/43258)), fechado 25/05 com pagamento
> automático mas `status='Aberta'`, agora entra. Antes, por data real, "20 cierres em 15 dias" eram **1**
> (Madison Grill, deal [43294](https://elifeeurope.activehosted.com/app/deals/43294)). **Perdidos seguem
> datados por `mdate`** (não têm outra data). Aplicado em `q_count_fechamentos`, `q_lista_fechamentos`,
> `q_ranking`, `q_serie_12m`.
>
> **Link do deal no AC:** `https://elifeeurope.activehosted.com/app/deals/{id}` (o `id` da tabela = id do deal no ActiveCampaign).

---

## 5. País e moeda

- **`pais`** é recorte secundário, **não filtro** (34–66% nulo). A região "LATAM" = as próprias tabelas LATAM.
- **Normalizar** antes de agrupar: `México`/`Mexico`/`MExico`→México; `Perú`/`Peru`; `Panamá`/`Panama`;
  `Chile`/`CHILE`/`chile `. Inclui España (operação hispana) e ruído a tratar (United States, France, India).
- **Moeda de reporte:** USD (dominante; algum EUR).

---

## 6. ⚠️ Sinalizar para a engenharia de dados (gap de ETL)

**`deals_latam_inbound_staging` tem `utm_source`/`utm_medium`/`utm_campaign`/`url_conversao` 100% vazios**
(as colunas existem, mas o ETL AC→Supabase não as populou), embora `outbound` e `contratos` carreguem
esses campos. Efeito: ~10.498 leads inbound ficam invisíveis ao filtro CM (sem atribuição = não conta,
como no Brasil), subestimando o volume real de CM da LATAM.

Tabelas-dimensão `dim_contacts`, `dim_accounts`, `dim_accounts_enriched_full` estão **vazias** — quando
populadas, habilitam dedup por pessoa e atribuição por conta.

**Pedido:** backfill do UTM/URL na `inbound` (e popular as dims). Não é correção no repositório da agência —
é no pipeline AC→Supabase (dono externo). Decisão atual: construir já com a cobertura disponível.

---

## 7. Validação

- Reproduzir os números-âncora desta auditoria (1.011 / 207 leads CM; 65 fechamentos CM filtrados;
  72 `Ganho` em contratos) como smoke test inicial.
- Conferir 5–10 fechamentos CM manualmente com o time LATAM (igual à conferência 6/6 do Brasil).
- Fixar baseline YtD após a 1ª rodada validada.
