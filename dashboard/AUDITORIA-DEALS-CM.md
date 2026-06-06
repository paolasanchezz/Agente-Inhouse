# Auditoria — Deals CM nao mapeados por falha de UTM

Protocolo e decisoes do harness `dashboard/auditar_deals_cm.py` (skill `/auditar-deals-cm`).
Documento de referencia, no espirito de `.claude/skills/bunzzai/AUDITORIA-vs-meta-ads.md`.

## 1. Premissa / problema

A dashboard CM decide se um deal e Content Marketing lendo `utm_source` + `url_conversao` **na propria
linha do deal** (`queries.py::filtro_cm`). Muitos deals chegam ao Supabase com esses campos **vazios**
por falha da automacao AC->Supabase. A origem CM existe noutro lugar:
- noutro deal do **mesmo contato** (mesmo email) que foi trackeado certo;
- noutro deal da **mesma empresa** (mesma `account_id`);
- no **titulo** do deal (`[BLOG]`, `[WEBINAR-RELATÓRIOS]`, ...);
- (Fase 2) numa **nota do deal** ou nos **custom fields do contato** no ActiveCampaign.

Esses deals viram CM invisivel — somem da dashboard. A doc ja registrava o sintoma:
`MAPEAMENTO-CAMPOS.md` §8 (HOLD A) e §9 (~17 emails sem trilha utm/url).

Escala real (YtD 2026, ref. 2026-06-02): de 9.893 deals, **5.237 sem utm+url** (~54%).

## 2. Metodo

1. **Candidato:** `utm_source` vazio E `url_conversao` vazio, no periodo, com email, menos ruido
   (dominios teste/internos) e `EMAIL_BLACKLIST`.
2. **Recuperacao local (em memoria, nunca grava):**
   - 2a. **Doador** CM (passa no `filtro_cm`) do **mesmo email** (ALTA) ou da **mesma conta** (MEDIA),
     escolhido por proximidade temporal (`LEFT JOIN LATERAL` / `DISTINCT ON`).
   - 2b. **Titulo** -> canal CM por prefixo curado (MEDIA, revisao).
   - 2c. **Inbound/HOLD A:** `funil_inicial_lead_auto='Inbound'` + `tipo/origem` de LP/Proposta (MEDIA).
3. **Re-filtro REAPROVEITANDO `queries.py`:** `is_cm_depois` aplica o mesmo `filtro_cm()` +
   whitelist/blacklist sobre colunas EFETIVAS (`COALESCE(original, recuperada)`). Zero reimplementacao.
4. **NET-NEW = emails CM DEPOIS − emails CM ANTES** (dedupe por email, igual a dashboard). Esses sao os
   "deals de CM nao mapeados por falha na automacao".

## 3. Por que harness, e nao "olhar no banco"

- O re-filtro precisa ser **identico** ao da dashboard. Reaproveitar `filtro_cm()` garante isso; copiar
  a regra na mao apodrece (drift). Validacao: ANTES == `q_count_leads(periodo)` da dashboard.
- O conjunto e grande (~4,3k candidatos/ano) e a logica de doador (proximidade, conta vs email,
  so-doador-CM) e chata de fazer no olho. O harness deixa explicito e idempotente.

## 4. Niveis de confianca (e por que email > conta)

`account_id` no Supabase == **organization (empresa)** no AC. A mesma conta agrega **contatos
diferentes**. Propagar UTM por conta atribuiria CM de uma pessoa ao deal de um colega — mais agressivo
que a propria metrica de Leads da dashboard (que nunca faz isso). Por isso:
- **email** (mesmo contato) -> ALTA -> entra no NET-NEW headline.
- **conta** (mesma empresa) -> MEDIA -> fila "revisao mesma empresa".
- **titulo/inbound** -> MEDIA -> fila "revisao titulo/inbound".

Titulo e ruidoso (`meetime`=SDR, `indicacao`=interno, `ic.`, `rmkt`, `monit`...). Termos claramente
nao-CM saem ate da revisao; prefixos `[...]` desconhecidos viram lista pro Victor mapear.

## 5. Resultado da 1a rodada (baseline — 2026-06-02, YtD 2026)

| Metrica | Valor |
|---|---:|
| Leads CM ANTES (dashboard) | 287 |
| Candidatos | 4.311 |
| **NET-NEW alta confianca (email)** | **43** (+15%) |
| Revisao mesma empresa (conta) | 573 |
| Revisao titulo/inbound | 575 |

Leitura: piso confiavel de **43** leads CM nao contados; **~1.148** em revisao que a Fase 2 (AC)
converteria de "provavel" em "confirmado". Como NET-NEW > 25, a remediacao recomendada **nao** e
whitelist inline e sim **corrigir a automacao AC->Supabase** (ou popular a tabela `cm_email_whitelist`
prevista em `queries.py:11`).

## 6. Riscos / nao-objetivos

- **Nao grava** no Supabase nem no AC. Recuperacao e local.
- **Nao auto-edita** `queries.py` — so propoe; Victor confirma caso a caso (padrao dos whitelists).
- Titulo/conta/inbound = revisao, nunca net-new automatico. So `email` auto-classifica.
- Tier 1 **aproxima** a "UTM do contato" via deals-irmaos. A leitura literal da **nota** e do **campo
  de contato** e a Fase 2 (AC).

## 7. Fase 2 — ActiveCampaign (desenhada, nao implementada)

Decisao do Victor (2026-06-02): "so Supabase por ora". Encaixe pronto: `enrich_from_ac()` (no-op).
Quando houver `AC_API_KEY`+`AC_API_URL`, ela enriquece SO os candidatos sem doador (cache + rate-limit):

- **Supabase `deals.id` == AC deal id.** `get_deal(id)`: `contact`->id do contato; `organization`==
  `account_id`; link `notes` -> `GET /api/3/deals/{id}/notes`.
- **Notas:** regex de `utm_*` e URL de conversao no texto.
- **Contato (UTM autoritativa), custom fields:** `845` source · `846` medium · `847` campaign ·
  `848` content · `849` term · `851` URL Conversao · `850` gclid · `389`/`457` origem (antigos).
- Preenche utm_source/url_conversao e **reentra no re-filtro** (mesmo `filtro_cm`). Sem mudar o resto.

Validado em 2026-06-02 com `get_deal(189099)` (`[BLOG]Pravaler`, organization 3375, contact 263594,
link notes presente) e `list_contact_custom_fields` (campos 845–851).
