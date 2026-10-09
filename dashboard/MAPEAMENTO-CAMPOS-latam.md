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

**Tamanho atual (filtro abaixo, histórico / 2026):** ~5.716 / 694 leads CM · ~30 fechamentos CM
(USD 16.195), sendo 4 em 2026 (USD 1.760). A cobertura cresce quando o gap de ETL do `inbound`
for corrigido.

> **ESCOPO (decisão Victor 2026-08-11):** esta dashboard mede **conteúdo + webinar online**.
> **Evento presencial não entra** — Café con Buzz, Merca2.0, BuzzTalks, Buzzmonitor Connect e
> Spark Summit têm dashboard própria, mesmo tendo LP no nosso domínio de conteúdo. Ver §2.3.

> **Atualização 2026-08-11 — origem própria.** O filtro passou a ler `evento_conversao` e
> `contenido_conversao`, e o subquery de leads passou a ser enriquecido pela linha de mesmo `id`
> em `contratos`. Ver §2.1 e §3.1. Delta líquido: **histórico** +492 leads, cierres 30 → 30
> (USD −70: entrou La Firma +390, saíram Doblegiro −460 e Pipe Toro, ambos presenciais);
> **2026** +13 leads, +5 reuniões, cierres 3 → 4 (USD 1.370 → 1.760).

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
  OR url_conversao ILIKE '%material.buzzmonitor.com/mcp-es%'   -- LP MCP-ES (domínio material.*, fora de getbuzzmonitor.com)
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
> A LP **MCP-ES** (`material.buzzmonitor.com/mcp-es`) foi adicionada aqui (decisão Victor 2026-07-06):
> vive no domínio `material.buzzmonitor.com`, que **não** cai no domínio de conteúdo `getbuzzmonitor.com`,
> então sem esta regra só os leads com `utm_source` na whitelist (ex.: `meta`) contavam. Escopo restrito
> à `mcp-es` (não o domínio inteiro — as irmãs mcp/mcp-pt/que-es-mcp seguem a regra geral).

**Excluídos** (não entram na whitelist, logo não contam): `google`/`google_es` + cpc (Ads),
`Pamela_Sanchez`, `equipo_comercial`, `comercial`, `ActiveCampaign`, `Customer_Success_Team`
(canais internos/SDR), e lixo de template (`{utm_source}`, `null`, `Others`, `{{placement}}`).

**`chatgptads` (ChatGPT Ads) fora sempre** — barrado no wrapper externo do filtro (`CM_UTM_SOURCES_EXCLUIR_LATAM`), acima até da URL forte e do sinal de origem própria. `chatgpt.com` (orgânico/GEO) segue na whitelist. Decisão Victor 2026-10-08 (caso deal 66908).

**Webinar / material rico:** na LATAM caem sob o domínio de conteúdo (`getbuzzmonitor.com`, slugs como
`plataforma-completa`, `analytics-pro`, `ia-para-social-listening`) ou sob fontes `email`/social — já
capturados por (a)/(b). Quando os campos `oferta_evento` / `fecha_de_evento_o_webinar...` forem
populados, refinar aqui (hoje têm cobertura quase nula).

---

## 2.1 Sinal de origem própria — `evento_conversao` / `contenido_conversao`

> Decisão Victor 2026-08-11. Implementado em `sinal_origem_propria()` (branch **1b** do filtro).

`url_conversao` guarda o **último toque**; `evento_conversao` e `contenido_conversao` guardam o
**primeiro** — a URL da LP com a UTM inteira, inclusive campanha, criativo e adset. Quando o último
toque é uma página comercial sem UTM, o filtro antigo jogava fora um lead perfeitamente rastreado.

**Caso que motivou a regra — deal 43258, Agencia La Firma (Chile), USD 390:**

| Coluna | Valor |
|---|---|
| `url_conversao` | `https://getbuzzmonitor.com/es/freetrial/` (página comercial, `utm_source` = `'null'`) |
| `evento_conversao` | `https://webinar.buzzmonitor.com/social-listening-mayo-2026-latam?utm_source=meta&utm_medium=Instagram_Feed&utm_campaign=[LATAM][Webinar-Social-Listening]&utm_content=WEBINAR+Social+Listening+Feed+AD+4&adset=01+-+Interesses+Marca` |

Anúncio Meta → LP do webinar → freetrial. CM puro, e mesmo assim caía na regra
`URLS_COMERCIAIS_SEM_UTM_EXCLUIR` ("sem atribuição, sem CM") porque a atribuição estava na coluna ao lado.

**Regra:** a origem conta como CM quando `evento_conversao` **ou** `contenido_conversao` aponta para
domínio próprio (`ORIGEM_DOMINIOS_PROPRIOS`: `getbuzzmonitor.com` — cobre `contenido.*` e `conteudo.*` —,
`webinar.`, `material.` e `content.buzzmonitor.com`). Domínio basta: na prática essas duas colunas **só**
aparecem preenchidas com LP nossa, então não há risco de arrastar tráfego de terceiro.
`evento.buzzmonitor.com` ficou **de fora** — é o domínio dos eventos presenciais (§2.3).

Três guardas deliberadas:

1. **Não sobrepõe a exclusão de Google Ads.** Diferente do sinal forte de URL (1), campanha de Search
   que cai numa LP nossa continua sendo Ads. Sem essa guarda entravam ~37 leads de `[CA]`/`[CH]`/`[CO][Search]`
   no histórico.
2. **Não sobrepõe `URLS_FORA_CM`.** Tentamos permitir o override e deu errado: o deal 40128
   (New Athletic, USD 590) entrou como CM tendo `url_conversao` =
   `buzzmonitor-institucional?utm_source=google&utm_medium=cpc&utm_campaign=[LATAM][Search][Competencia-listening]&utm_term=synthesio`
   — busca paga por concorrente. Revertido em 2026-08-11.
3. **Escopo conteúdo/webinar.** LP de evento presencial derruba o sinal, mesmo no domínio de conteúdo (§2.3).

> **⚠️ `evento_conversao` NÃO é garantidamente o primeiro toque.** Ele registra a LP de evento em que o
> contato se inscreveu **em qualquer momento**, inclusive depois de fechar. No deal 40128 a inscrição no
> Café con Buzz é de **24/06** e o negócio fechou em **29/01** — cinco meses antes. Ao usar esse campo para
> atribuir, confira a cronologia (`fecha_de_inscripcion_evento` no contato) antes de concluir.

## 2.2 Campanhas e fontes próprias de evento/webinar

Quando o lead vem de webinar ao vivo, o `utm_source` gravado costuma ser o **material do último toque**
(o deck exibido na tela, o e-mail pós-webinar, o QR do evento presencial) e não o anúncio que trouxe a
pessoa. Exemplo: `Oferta_Webinar_Social_Listening` / `Slides` / `Stream_en_vivo` — os leads
`emendoza@preciso.pe` (deal 43327), `wmarshall@grupodiniz.com.mx` (43328) e
`lauracastanedalemus@gmail.com` (43332), todos com reunião marcada.

Esses casos já passavam pelo domínio de conteúdo na `url_conversao`. Para que **não dependam** dela
(mesmo modo de falha da La Firma), foram adicionados:

- **`CM_UTM_SOURCES_LATAM`** += `slides`, `qr_code`, `newsletter`, `sitio_web`.
- **`CM_CAMPANHAS_LIKE`** (novo): `oferta_%`, `%webinar%`, `%material rico%` / `%material+rico%`
  — match sobre `lower(utm_campaign)`.

Ambos ficam **dentro** da regra geral (2), logo a exclusão de Google Ads continua valendo por cima.
Hoje as duas adições somam **0 leads novos** (todos já entravam pela URL): são rede de proteção para
quando a `url_conversao` vier vazia.

`qr_code` foi avaliado e **rejeitado** — QR é crachá de evento presencial (§2.3).

---

## 2.3 Escopo: conteúdo + webinar ONLINE (evento presencial fica fora)

> Decisão Victor 2026-08-11, a partir da auditoria dos 8 cierres de 2026.

Esta dashboard mede Content Marketing: material rico, blog, estudos e **webinar online**.
**Evento presencial tem dashboard própria e não conta aqui**, mesmo com LP hospedada em
`contenido.getbuzzmonitor.com`.

Reprovados na auditoria (todos saíram):

| Deal | Valor | Por quê |
|---|---|---|
| 40128 New Athletic | USD 590 | `cafe-con-buzz-peru-2026` — e o último toque real era Google Search |
| 39162 Smilehood | USD 605 | campanha `BuzzTalks_Argentina`, `origen_del_lead = Outbound` |
| 43197 TLP MX | USD 390 | `merca20-mayo-2026` |
| 43484 News Monitor | USD 390 | `cafe-con-buzz-peru-2026`, `como_conocio = OUTBOUND` |

`EVENTO_PRESENCIAL_MARCADORES` cobre `buzztalk`, `cafe-con-buzz` / `cafeconbuzz`, `merca20`,
`merca-25`, `buzzmonitor-connect`, `buzzconnect`, `spark`, `registro-evento` e o domínio
`evento.buzzmonitor.com`.

**O marcador é aplicado em dois lugares, com escopos diferentes de propósito:**

1. **Em `sinal_origem_propria()`** — testado contra `evento_conversao`, `contenido_conversao` **e**
   `utm_campaign`. A LP presencial nunca pode ser o que faz o lead virar CM. O teste precisa incluir a
   campanha porque a LP do BuzzTalks Argentina tem slug de conteúdo
   (`social-listening-que-guia-decisiones-no-reportes`) e só o nome da campanha a denuncia.
2. **No wrapper (4) do filtro** — testado **só contra `utm_campaign`**, porque a campanha é o que gerou
   o lead. Deliberadamente **não** aplicamos ao `evento_conversao`/`url_conversao` aqui: o deal 43327
   (Preciso, campanha `Oferta_Webinar_Social_Listening`) converteu **no webinar** e tem `cafe-con-buzz`
   apenas como toque posterior — segue CM. Mesma lógica no 42834 (`[LATAM][Remarketing]` →
   `plataforma-completa`, com `buzztalk` de toque lateral).

Um wrapper cego em qualquer coluna derrubaria esses dois. A pergunta certa não é "esse lead
encostou num evento presencial?", e sim "**o evento presencial foi a conversão dele?**".

---

## 3. Atribuição (sem regra de 90 dias)

O Brasil usa `account_id` + janela de 90 dias para atribuir eventos pós-conversão. **A LATAM não tem
`account_id`** e a dimensão de contato está vazia. Portanto:

- **Leads e eventos de funil:** classificados pelo **próprio** `utm_source`/`url_conversao` do registro.
- **Fechamentos (`contratos`):** classificados pela **própria** UTM/URL do contrato (65 batem o filtro).
  Sem janela cross-table de 90 dias (não há chave de conta para ligar).
- **Dedup:** por `id` do deal (não há dedup por pessoa — `dim_contacts` vazia). Reativar dedup por email
  quando uma fonte de contatos for populada.

## 3.1 Enriquecimento do lead pela linha de `contratos`

> Decisão Victor 2026-08-11. Implementado em `_leads_subquery()`.

A mesma deal existe nas duas pontas com preenchimento **diferente**. O deal 43258 está 100% cego no
`inbound` (`utm_*` e `url_conversao` todos `NULL`) enquanto a linha de `contratos` do mesmo `id` guarda
`url_conversao` + `evento_conversao` com a UTM inteira. Como o subquery de leads só lia
inbound ∪ outbound, esse rastro era descartado.

Depois do dedup por `id`, entra um `LEFT JOIN deals_latam_contratos_staging ON id`, com três limites:

1. **Só preenche buraco.** Cada coluna de `_COLS_ATRIBUICAO` fica com o valor do lead e cai para
   contratos apenas quando o lead vem vazio. O que já estava preenchido nunca é sobrescrito.
2. **Não cria linha.** `contratos` não é fonte de leads novos — a população continua sendo
   inbound ∪ outbound. Só a atribuição é completada.
3. **Não toca o funil.** Data, status, dono, `fecha_de_reunion` seguem sendo os da linha do lead.

`''` e a string literal `'null'` contam como ausente **nos dois lados** — sem isso um `'null'` textual
venceria o `COALESCE` e mascararia o dado bom (é exatamente o `utm_source` da linha de contratos da
La Firma).

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
