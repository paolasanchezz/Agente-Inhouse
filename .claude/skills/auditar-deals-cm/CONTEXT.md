# CONTEXT — auditar-deals-cm

Contexto compartilhado da skill `/auditar-deals-cm`. Leia antes de executar.

## Restricao

- **SOMENTE LEITURA no Supabase** (role `looker_readonly`). A unica escrita possivel no repo e
  adicionar emails confirmados a `EMAIL_WHITELIST` em `dashboard/queries.py` — e SO depois do Victor
  confirmar no gate. Nunca grava no Supabase nem no ActiveCampaign.
- Recuperacao de UTM e **local/em memoria**. O Supabase nunca e alterado.

## Caminhos

| O que | Onde |
|---|---|
| Harness | `dashboard/auditar_deals_cm.py` |
| Filtro CM reaproveitado | `dashboard/queries.py` (`filtro_cm`, `EMAIL_WHITELIST`, `EMAIL_BLACKLIST`, `_sql_email_list`, `q_lista_leads`) |
| Conexao | `dashboard/.env` -> `SUPABASE_PG_URL` (mesmo da `/dashboard-atualizar`) |
| Saidas (gitignored, PII) | `dashboard/auditoria/AUDIT-CM-UTM-{data}.md` + CSVs |
| Spec/regras de CM | `dashboard/MAPEAMENTO-CAMPOS.md` (§2 filtro, §8 HOLD A, §9 apendice) |
| Protocolo/decisoes | `dashboard/AUDITORIA-DEALS-CM.md` |

## Definicao de candidato

Deal com **`utm_source` vazio E `url_conversao` vazio**, `cdate >= --desde`, com email, em
`deals_comercial_prod`, **tirando**:
- ruido: dominios de teste (`yopmail.com`, `webhook.com`, `teste.com`, `mailinator.com`,
  `dealpolitico.com`, ...) e internos do grupo (`@buzzmonitor.com.br`, `@buzzmonitor.com`,
  `@elife.com.br`, `@elife.com`);
- emails ja na `EMAIL_BLACKLIST`.

YtD 2026 (referencia 2026-06-02): ~9.893 deals, **5.237 sem utm+url**, **4.311 candidatos** apos ruido.

## Recuperacao e niveis de confianca

| Sinal | Como | Confianca | Vai pro headline? |
|---|---|---|---|
| **Doador por EMAIL** (2a) | outro deal do **mesmo email** que passa no `filtro_cm` cede utm/url | ALTA (mesmo contato — o que o Victor descreveu) | **SIM** (NET-NEW) |
| **Doador por CONTA** (2a) | outro deal da **mesma `account_id`** (empresa), outro contato | MEDIA | Nao — revisao |
| **Titulo** (2b) | prefixo `[BLOG]`, `webinar`, `web.*`, `checklist`, `meta`, `ig`, `linkedin`... | MEDIA | Nao — revisao |
| **Inbound/HOLD A** (2c) | `funil_inicial_lead_auto='Inbound'` + `tipo/origem` de LP/Proposta | MEDIA | Nao — revisao |

`account_id` no Supabase == **organization (empresa)** no AC: a mesma conta agrega contatos
diferentes. Por isso doador por conta != mesmo contato -> fica em revisao, fora do net-new.

Titulo e sinal **ruidoso**: termos claramente NAO-CM (`meetime`=SDR, `indicacao`=interno, `vtex`,
`ic.`, `rmkt`, `monit`, `sdr`, `outbound`) sao descartados ate da revisao; prefixos `[...]` nao
classificados sao listados em `prefixos-titulo-nao-mapeados.csv` pro Victor mapear (igual a whitelist
de slugs foi construida).

## Re-filtro (anti-drift)

O `is_cm_depois` aplica o **mesmo** `filtro_cm()` + whitelist/blacklist da dashboard sobre as colunas
EFETIVAS (`COALESCE(original, recuperada)`). Validado: ANTES (leads CM no periodo) == `q_count_leads`
da dashboard. Se a regra de CM mudar em `queries.py`, a auditoria acompanha sozinha.

## Mapa ActiveCampaign — Fase 2 (validado, ainda nao implementado)

Quando ligar a Fase 2 (so com `AC_API_KEY`+`AC_API_URL`; ver `enrich_from_ac()` no harness):

- **Supabase `deals.id` == AC deal id.** `get_deal(id)` devolve:
  - `contact` -> id do contato (UTM autoritativa vive no contato);
  - `organization` == Supabase `account_id`;
  - link `notes` -> `GET /api/3/deals/{id}/notes` (notas legiveis, onde aparece UTM + URL de conversao).
- **UTM no contato** via custom fields (de `list_contact_custom_fields`):
  - `845` UTM Source · `846` UTM Medium · `847` UTM Campaign · `848` UTM Content · `849` UTM Term
  - `851` URL Conversao · `850` Gclid · `389` UTM Source-Origem (antigo) · `457` URL de Origem
- Fluxo: pros candidatos sem doador, ler nota (regex de utm/url) + campos 845/851 do contato,
  preencher utm_source/url_conversao, e reentrar no re-filtro (mesmo `filtro_cm`). Com cache +
  rate-limit (a Meta/AC limita). Volume tipico de residuo: centenas — viavel via REST, inviavel via MCP.

## Comando relacionado

- `/dashboard-atualizar` — depois de confirmar emails na `EMAIL_WHITELIST`, a dashboard so reflete no
  proximo run dela.
