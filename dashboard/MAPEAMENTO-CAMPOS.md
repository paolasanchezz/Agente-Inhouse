# Mapeamento de campos — Dashboard Content Marketing → Supabase

> **Propósito:** este documento é a ponte entre os blocos visuais da dashboard `dashboard/relatorio-semanal-buzzmonitor-brasil.html` (hoje com dados mock) e as queries SQL que devem rodar contra o Supabase Postgres para popular dados reais.
>
> **Como usar:** cada bloco da dashboard tem uma seção abaixo com pergunta de negócio, coluna(s) de origem no schema, e query SQL pronta com placeholders `:ini_atual`, `:fim_atual`, `:ini_ant`, `:fim_ant`, `:mtd_inicio`, `:ytd_inicio`. O Python (ou wrapper Supabase) injeta as datas em runtime.
>
> **Conexão:** via `dashboard/explore.py` ou MCP `mcp__supabase__execute_sql`. Usuário `looker_readonly` no banco — todas as queries são SELECT.

---

## 1. Schema relevante

**Duas tabelas formam o pipeline completo:**

### `deals_comercial_prod` (primária)
34.192 linhas, range 30/08/2019 → 18/05/2026. Vive aqui:
- Geração de leads (`cdate`)
- Eventos do funil: Contato Efetivo, Reunião Agendada, Reunião Realizada, Proposta
- Perda (`data_negocio_perdido_auto`, `motivo_perda_bd_sdr`)

### `deals_contratos_prod` (Fechamentos)
1.862 linhas, mesma estrutura de colunas. **Quando um deal fecha, vira contrato aqui.** Vive aqui:
- Evento Fechamento (`data_fechamento_auto`)
- Valor do contrato (`value` numeric, mais confiável que o `value` text de `deals_comercial_prod`)

A ligação entre as tabelas é via **`account_id`** (a mesma conta pode ter múltiplos deals comerciais e múltiplos contratos).

### Colunas-chave por categoria

**ID e dados básicos**
- `id` (bigint, PK) · `title` (text) · `cdate` (timestamp tz — criação) · `mdate` · `status` · `value` · `currency` · `group` · `account_id`

**Identificação Content Marketing**
- `utm_source`, `utm_content`, `utm_campaign`, `utm_medium`, `utm_term`, `utm_id` (text)
- `url_conversao` (text)
- `gclid` (text — Google Click ID; pode ser sticky de sessão anterior, **não usar isoladamente como sinal**)

**Email do contato**
- `email_contato_principal_bd_sdr` (text) ← **campo correto**
- `quick_email` ← **NÃO usar** (legado, baixa cobertura)

**Datas dos eventos do funil**
| Evento | Coluna | Tabela onde vive |
|---|---|---|
| Leads | `cdate` | comercial |
| Contato Efetivo | `data_efetividade_contato_auto` | comercial |
| Reunião Agendada | `data_agendamento_auto` | comercial |
| Reunião Realizada | `data_inicio_reuniao_realizada` | comercial |
| Proposta | `data_envio_proposta_auto` | comercial |
| Fechamento | `data_fechamento_auto` | **contratos** |
| Perdido | `data_negocio_perdido_auto` | comercial |

**Perda**
- `motivo_perda_bd_sdr` · `justificativa_perda_bd_sdr`

**Responsáveis**
- `sdr_responsavel` · `bd_auto` · `sdr_sdr` · `owner` (bigint)

### Valores reais relevantes (validados no banco)

| Campo | Valor | Significado |
|---|---|---|
| `status` em comercial | `Ganho` | Fechamento confirmado |
| `status` em comercial | `Perdido` | Perda (deal saiu do pipeline) |
| `status` em comercial | `Aberta` | Em andamento |
| `status` em contratos | (qualquer) | Estado do contrato — usar `data_fechamento_auto IS NOT NULL` para "fechado" |

---

## 2. Filtro Content Marketing (universal — todo evento)

Esta é a regra fundamental de "o que é CM". Aplica a TODOS os eventos da dashboard.

### Lista de utm_source CM

```
meta, lp-agradecimento, ig, instagram, linkedin, notion, email, checklist,
whatsapp, pos-webinar, sms, webinar-ao-vivo, apresentacao-webinar,
lp-agradecimento-oferta-trends, lp-agradecimento-evento, tiktok, chatgpt.com, gemini, blog
```

**Excluídos explicitamente** (canais internos ou pagos):
- `comercial`, `sdr`, `cs`, `crm` — distribuição interna do time (não geração CM)
- `google` (com `utm_medium='cpc'`) — Google Ads, canal pago

### URLs CM (qualquer domínio próprio do conteúdo)

- `https://buzzmonitor.com/blog/*` — blog principal
- `https://buzzmonitor.com.br/blog/*` — blog principal (variação .com.br)
- `https://material.buzzmonitor.com/*` — materiais ricos (whitepapers, e-books, MCP)
- `https://evento.buzzmonitor.com/*` — landing pages de eventos
- `https://conteudo.buzzmonitor.com.br/<slug CM>` — whitelist de slugs (lista abaixo)

### Whitelist de slugs em `conteudo.buzzmonitor.com.br/`

O subdomínio recebe tráfego misto (CM + Google Ads + formulários internos). Só estes slugs contam como CM:

`plataforma-completa`, `plataforma-completa-atendimento`, `plataforma-completa-listening`, `monitoramento-de-redes-sociais-2`, `oferta-*` (todos), `conteudo-que-converte`, `webinar-*` (todos), `report-trends-*`, `masterclass-trends-*`, `gestao-de-crises-*`, `relatorios-estrategicos`, `buzz-talks-*`, `buzztalk-*`, `buzzmonitor-connect-*`

**Excluídos:** `indicacoes-internas` (form interno), `buzz-pills` (newsletter CRM), `monitoramento-com-ia`, `buzzmonitor-ia`, `escolha-a-buzzmonitor`, `social-listening-com-ia`, `ia-para-social-listening` (Google Ads).

### CTE base — `deals_cm` (cole no início de qualquer query)

```sql
WITH cm_whitelist AS (
  -- Emails forçados a entrar como CM (override positivo)
  SELECT email FROM cm_email_whitelist  -- ou inline VALUES
),
cm_blacklist AS (
  -- Emails forçados a sair (override negativo)
  SELECT email FROM cm_email_blacklist
),
deals_cm AS (
  SELECT *
  FROM deals_comercial_prod
  WHERE
    lower(trim(email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM cm_blacklist)
    AND (
      -- Override manual via whitelist
      lower(trim(email_contato_principal_bd_sdr)) IN (SELECT email FROM cm_whitelist)
      -- Filtro CM normal:
      OR (
        -- exclui Google Ads. COALESCE protege contra utm_source/medium NULL:
        -- sem ele, `NULL = 'google'` vira NULL, `NOT NULL` vira NULL e o WHERE
        -- descarta o lead silenciosamente (bug corrigido em 2026-05-26).
        NOT (COALESCE(utm_source, '') = 'google' AND COALESCE(utm_medium, '') = 'cpc')
        AND (
          utm_source IN (
            'meta','lp-agradecimento','ig','instagram','linkedin','notion','email',
            'checklist','whatsapp','pos-webinar','sms','webinar-ao-vivo',
            'apresentacao-webinar','lp-agradecimento-oferta-trends',
            'lp-agradecimento-evento','tiktok','chatgpt.com','gemini','blog'
          )
          OR url_conversao ILIKE 'https://buzzmonitor.com/blog/%'
          OR url_conversao ILIKE 'https://buzzmonitor.com.br/blog/%'
          OR url_conversao ILIKE 'https://material.buzzmonitor.com/%'
          OR url_conversao ILIKE 'https://evento.buzzmonitor.com/%'
          OR (
            (utm_source IS NULL OR utm_source NOT IN ('cs','comercial','sdr','crm','google'))
            AND (
              url_conversao ILIKE 'https://conteudo.buzzmonitor.com.br/plataforma-completa%'
              OR url_conversao ILIKE 'https://conteudo.buzzmonitor.com.br/monitoramento-de-redes-sociais-2%'
              OR url_conversao ILIKE 'https://conteudo.buzzmonitor.com.br/oferta-%'
              OR url_conversao ILIKE 'https://conteudo.buzzmonitor.com.br/conteudo-que-converte%'
              OR url_conversao ILIKE 'https://conteudo.buzzmonitor.com.br/webinar-%'
              OR url_conversao ILIKE 'https://conteudo.buzzmonitor.com.br/report-trends-%'
              OR url_conversao ILIKE 'https://conteudo.buzzmonitor.com.br/masterclass-trends-%'
              OR url_conversao ILIKE 'https://conteudo.buzzmonitor.com.br/gestao-de-crises-%'
              OR url_conversao ILIKE 'https://conteudo.buzzmonitor.com.br/relatorios-estrategicos%'
              OR url_conversao ILIKE 'https://conteudo.buzzmonitor.com.br/buzz-talks-%'
              OR url_conversao ILIKE 'https://conteudo.buzzmonitor.com.br/buzztalk-%'
              OR url_conversao ILIKE 'https://conteudo.buzzmonitor.com.br/buzzmonitor-connect-%'
            )
          )
        )
      )
    )
)
```

### Tabelas auxiliares de override (criar quando viável)

```sql
CREATE TABLE cm_email_whitelist (
  email TEXT PRIMARY KEY,
  reason TEXT,                -- "Veio por blog mas tracking não preservou URL"
  added_at TIMESTAMP DEFAULT now(),
  added_by TEXT
);

CREATE TABLE cm_email_blacklist (
  email TEXT PRIMARY KEY,
  reason TEXT,                -- "Veio por Google Ads antes (info externa ao Supabase)"
  added_at TIMESTAMP DEFAULT now(),
  added_by TEXT
);
```

Casos atuais conhecidos:
- **Whitelist:** `jessica.rua@wealthmoney.com.br` (Wealth — converteu via blog, tracking não preservou no banco), `ronaldozottolo@gmail.com` (Agência CROP — sem trilha no banco)
- **Blacklist:** `julianacastro@idwcompany.com.br` (IDW — sinal Google Ads em outra ferramenta, não capturado pelo Supabase)

Enquanto as tabelas não existirem, usar `VALUES` inline:
```sql
SELECT email FROM (VALUES
  ('jessica.rua@wealthmoney.com.br'),
  ('ronaldozottolo@gmail.com')
) AS w(email)
```

---

## 3. Regra dos 90 dias (universal — eventos pós-conversão)

> **Um evento (Contato Efetivo, Reunião Agendada, Realizada, Proposta, Fechamento, Perdido) só conta como CM se houver uma conversão CM no mesmo `account_id` ≤ 90 dias antes do evento.**

**Motivação:** se um lead converteu via CM há 100+ dias e só hoje agendou uma reunião, o esforço de CM já foi "diluído" — outros canais (outbound, SDR, relacionamento) provavelmente impulsionaram o avanço. Não é mais resultado CM.

**Exceção: Leads.** O "evento" de Leads é o próprio `cdate` (nascimento) — não há "última conversão antes" para olhar. Para Leads, aplica-se apenas o filtro CM normal.

### CTE de conversões CM (UNION das duas tabelas)

A conversão CM pode ter sido registrada em `deals_comercial_prod` ou em `deals_contratos_prod` (caso o lead foi criado já como contrato). Precisamos olhar as duas:

```sql
WITH conversoes_cm AS (
  SELECT account_id, cdate AS data_conv, email_contato_principal_bd_sdr AS email
  FROM deals_comercial_prod
  WHERE account_id IS NOT NULL
    AND cdate >= :periodo_inicio - INTERVAL '90 days'  -- janela alargada
    AND <filtro_cm_universal>  -- mesmas regras da seção 2
  UNION ALL
  SELECT account_id, cdate, email_contato_principal_bd_sdr
  FROM deals_contratos_prod
  WHERE account_id IS NOT NULL
    AND cdate >= :periodo_inicio - INTERVAL '90 days'
    AND <filtro_cm_universal>
)
```

**Janela alargada de 90d antes do `:periodo_inicio`:** garante que captamos conversões antigas que ainda estão dentro da janela de atribuição para eventos no período.

### Padrão de query para eventos pós-conversão

> **Implementação:** centralizada no helper `_atrib_cm_90d(col, alias)` em `queries.py` (revisão 2026-06-15). Não reescrever o `EXISTS` inline — usar o helper.

```sql
SELECT d.*
FROM deals_comercial_prod d
WHERE d.<coluna_data_evento>::date BETWEEN :ini AND :fim
  AND (
    -- atribuição normal: conversão CM na mesma conta ≤ 90d antes
    EXISTS (
      SELECT 1 FROM conversoes_cm cm
      WHERE cm.account_id = d.account_id
        AND cm.data_conv::date <= d.<coluna_data_evento>::date
        AND d.<coluna_data_evento>::date - cm.data_conv::date <= 90
    )
    -- auto-atribuição: deal sem empresa no CRM (account_id NULL) cujo próprio row é CM
    OR (
      d.account_id IS NULL
      AND <filtro_cm_universal aplicado em d>
      AND d.cdate::date <= d.<coluna_data_evento>::date
      AND d.<coluna_data_evento>::date - d.cdate::date <= 90
    )
  )
```

Para Fechamento, trocar `deals_comercial_prod` por `deals_contratos_prod` e `<coluna_data_evento>` por `data_fechamento_auto`.

**Duas correções (2026-06-15) sobre a versão ingênua — ambas causavam subcontagem:**

1. **Comparar em `::date`, não timestamp cru.** As colunas de evento são gravadas à meia-noite (`data_agendamento_auto = 'YYYY-MM-DD 00:00:00'`) enquanto `cdate` é `timestamptz` com hora real. Em timestamp cru, um evento no **mesmo dia** da conversão falha (`cdate 07:39 <= agendamento 00:00` = falso) e some da contagem. `::date` normaliza (ver §6). Recupera ~26 reuniões agendadas YtD 2026.
2. **Auto-atribuição quando `account_id IS NULL`.** A CTE `conversoes_cm` exige `account_id NOT NULL` e o `EXISTS` casa por conta — então deals de leads **sem empresa** no CRM (ex.: campanha Monitoramento Político: pré-candidatos, jornalistas) nunca contavam CE/RA/RR/Proposta, só Leads. Quando o próprio row é CM, o deal se atribui a si mesmo dentro dos 90d.

**Fora da janela por padrão, mas overridável (`CM_DEALS_FORCADOS`):** um evento cuja conversão CM foi há >90d ou veio de `account_id` diferente **não** entra pela regra automática. Quando o Victor confirma que o deal é CM mesmo assim — ex.: deal 189715 *Assembleia Legislativa do MA*, lead que converteu na **página de oferta webinar** (CM legítimo) mas teve um deal novo criado pelo CRM **sem UTM, em conta diferente e 108 dias depois** — adiciona-se o `id` do deal a `CM_DEALS_FORCADOS` em `queries.py`. Isso força os **eventos** daquele deal (CE/RA/RR/Proposta) a contarem como CM, **sem** afetar Leads (o lead original já conta pela conversão real) nem Fechamentos (gate §7 — override de fechamento continua via `EMAIL_WHITELIST`). Override nominal, não heurístico — só `deals_comercial_prod`. Para casos sistemáticos de UTM perdida, ver `/auditar-deals-cm`.

---

## 4. Conceito de datas — regra inegociável

> **Métricas de evento contam por data do EVENTO, não pela data de criação do deal.**

Exemplo: um deal criado em janeiro que teve reunião realizada em maio conta para "Reuniões Realizadas em Maio", não "Reuniões Realizadas em Janeiro".

A única métrica que usa `cdate` (criação) é **Leads**.

| KPI da dashboard | Coluna de data | Tabela | Filtro adicional |
|---|---|---|---|
| Leads | `cdate` | comercial | filtro CM (sem 90d — cdate é o próprio evento) |
| Contato Efetivo | `data_efetividade_contato_auto` | comercial | 90d |
| Reunião Agendada | `data_agendamento_auto` | comercial | 90d |
| Reunião Realizada | `data_inicio_reuniao_realizada` | comercial | 90d |
| Proposta | `data_envio_proposta_auto` | comercial | 90d |
| Fechamento | `data_fechamento_auto` | **contratos** | 90d |
| Perdido | `data_negocio_perdido_auto` | comercial | 90d + `motivo_perda_bd_sdr IS NOT NULL` |

---

## 5. Mapeamento bloco a bloco da dashboard

> Em todas as queries abaixo, `<filtro_cm_universal>` se refere ao bloco da seção 2 (whitelist/blacklist + lista UTM + URLs + slugs).

### Header
Parâmetros derivados em Python/template — não SQL.

### Bloco 1.a — Big Numbers Semana (7 KPIs)

**Pergunta de negócio:** quanto a semana atual produziu em cada estágio do funil, vs semana anterior, vs ritmo médio YtD?

#### Lead atual + anterior + μ YtD
```sql
WITH cm_whitelist AS (...),
     cm_blacklist AS (...)
SELECT
  COUNT(*) FILTER (WHERE cdate::date BETWEEN :ini_atual AND :fim_atual) AS leads_atual,
  COUNT(*) FILTER (WHERE cdate::date BETWEEN :ini_ant AND :fim_ant) AS leads_ant,
  ROUND(
    COUNT(*) FILTER (WHERE cdate >= :ytd_inicio AND cdate::date < :ini_atual)::numeric
    / GREATEST(1, EXTRACT(week FROM :ini_atual::date) - 1),
    1
  ) AS leads_mu_ytd_sem
FROM deals_comercial_prod d
WHERE d.cdate >= :ytd_inicio
  AND d.email_contato_principal_bd_sdr IS NOT NULL
  AND <filtro_cm_universal aplicado em d>;
```

#### CE/RA/RR/Prop/Fech/Perd atual + anterior (com regra 90d)
Padrão geral — repetir para cada KPI trocando `<coluna_data_evento>` e a tabela quando for Fechamento:

```sql
WITH conversoes_cm AS (...)  -- janela alargada 90d antes de :ini_ant
SELECT
  COUNT(*) FILTER (WHERE d.<coluna_data_evento>::date BETWEEN :ini_atual AND :fim_atual) AS atual,
  COUNT(*) FILTER (WHERE d.<coluna_data_evento>::date BETWEEN :ini_ant AND :fim_ant) AS ant
FROM deals_comercial_prod d  -- ou deals_contratos_prod para Fechamento
WHERE d.<coluna_data_evento> BETWEEN :ini_ant AND :fim_atual
  AND EXISTS (
    SELECT 1 FROM conversoes_cm cm
    WHERE cm.account_id = d.account_id
      AND cm.data_conv <= d.<coluna_data_evento>
      AND d.<coluna_data_evento> - cm.data_conv <= INTERVAL '90 days'
  );
```

Para Fechamento, adicionar override por whitelist e blacklist:
```sql
  AND (
    lower(trim(d.email_contato_principal_bd_sdr)) IN (SELECT email FROM cm_whitelist)
    OR EXISTS (...regra 90d...)
  )
  AND lower(trim(d.email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM cm_blacklist)
```

### Bloco 1.b — Big Numbers YtD (7 KPIs)
Mesma estrutura sem `:ini_ant/:fim_ant` — só conta total YtD com filtro CM + regra 90d.

**Taxas de conversão entre estágios** (sub do card YtD) — calcular em Python a partir dos COUNTs.

### Bloco 2 — Perdas

#### 2.a — 3 percentuais (Semana / MtD / YtD)
```sql
WITH conversoes_cm AS (...)
SELECT
  COUNT(*) FILTER (WHERE d.data_negocio_perdido_auto BETWEEN :ini_atual AND :fim_atual
                       AND d.motivo_perda_bd_sdr IS NOT NULL
                       AND EXISTS (...regra 90d em data_negocio_perdido_auto...)) AS perd_semana,
  COUNT(*) FILTER (WHERE d.cdate::date BETWEEN :ini_atual AND :fim_atual
                       AND <filtro_cm_universal>) AS leads_semana,
  -- MtD e YtD seguem o mesmo padrão trocando o período
FROM deals_comercial_prod d;
```

Percentuais calculados em Python.

#### 2.b — Tabela de leads perdidos MtD
```sql
WITH conversoes_cm AS (...)
SELECT
  d.title AS deal,
  d.email_contato_principal_bd_sdr AS email,
  d.utm_source, d.utm_content,
  COALESCE(d.data_efetividade_contato_auto, d.data_primeiro_contato_sdr, d.cdate::timestamp)::date AS ultima_conversao,
  d.motivo_perda_bd_sdr AS motivo
FROM deals_comercial_prod d
WHERE d.data_negocio_perdido_auto BETWEEN :mtd_inicio AND :mtd_fim
  AND d.motivo_perda_bd_sdr IS NOT NULL
  AND EXISTS (
    SELECT 1 FROM conversoes_cm cm
    WHERE cm.account_id = d.account_id
      AND cm.data_conv <= d.data_negocio_perdido_auto
      AND d.data_negocio_perdido_auto - cm.data_conv <= INTERVAL '90 days'
  )
ORDER BY d.data_negocio_perdido_auto DESC;
```

### Bloco 3 — Listas de Acesso Fácil (5 tabelas)

#### 3.1 Leads da semana (cdate no período, sem 90d)
```sql
WITH cm_whitelist AS (...), cm_blacklist AS (...)
SELECT
  d.title AS deal, d.email_contato_principal_bd_sdr AS email,
  d.utm_source, d.utm_content,
  d.cdate::date AS data_conversao,
  COALESCE(d.sdr_responsavel, d.sdr_sdr) AS bd
FROM deals_comercial_prod d
WHERE d.cdate::date BETWEEN :ini AND :fim
  AND <filtro_cm_universal>
ORDER BY d.cdate;
```

#### 3.2–3.5 (Reuniões Agendadas, Realizadas, Propostas) — usar regra 90d
```sql
WITH conversoes_cm AS (...)
SELECT d.title, COALESCE(d.bd_auto, d.sdr_responsavel) AS bd, d.utm_source, d.utm_content,
       d.<coluna_evento>::date AS data_evento, ...
FROM deals_comercial_prod d
WHERE d.<coluna_evento>::date BETWEEN :ini AND :fim
  AND EXISTS (SELECT 1 FROM conversoes_cm cm
              WHERE cm.account_id = d.account_id
                AND cm.data_conv <= d.<coluna_evento>
                AND d.<coluna_evento> - cm.data_conv <= INTERVAL '90 days')
ORDER BY d.<coluna_evento>;
```

#### 3.5 Fechamentos (usa `deals_contratos_prod` + whitelist/blacklist)
```sql
WITH conversoes_cm AS (...), cm_whitelist AS (...), cm_blacklist AS (...)
SELECT
  ct.title, COALESCE(ct.bd_auto, ct.sdr_responsavel) AS bd,
  ct.utm_source, ct.utm_content,
  ct.data_fechamento_auto::date AS data_fechamento,
  ct.value, ct.currency
FROM deals_contratos_prod ct
WHERE ct.data_fechamento_auto::date BETWEEN :ini AND :fim
  AND lower(trim(ct.email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM cm_blacklist)
  AND (
    lower(trim(ct.email_contato_principal_bd_sdr)) IN (SELECT email FROM cm_whitelist)
    OR EXISTS (
      SELECT 1 FROM conversoes_cm cm
      WHERE cm.account_id = ct.account_id
        AND cm.data_conv <= ct.data_fechamento_auto
        AND ct.data_fechamento_auto - cm.data_conv <= INTERVAL '90 days'
    )
  )
ORDER BY ct.data_fechamento_auto;
```

### Bloco 4 — Detalhamento (Rankings Atual vs YtD)

**Importante:** para evitar mistura de "leads criados na semana com source X" com "eventos da semana de deals com source X", construir CTEs separadas por métrica e LEFT JOIN ao final.

#### 4.a Sources Semana — esqueleto
```sql
WITH conversoes_cm AS (...),
leads_p AS (
  SELECT utm_source, COUNT(*) AS leads FROM deals_comercial_prod d
  WHERE d.cdate::date BETWEEN :ini AND :fim AND <filtro_cm_universal>
  GROUP BY utm_source
),
ce_p AS (
  SELECT d.utm_source, COUNT(*) AS ce FROM deals_comercial_prod d
  WHERE d.data_efetividade_contato_auto::date BETWEEN :ini AND :fim
    AND EXISTS (...regra 90d em data_efetividade_contato_auto...)
  GROUP BY d.utm_source
),
-- repetir CTEs para ra, rr, prop, fech (usar deals_contratos_prod) ...
all_src AS (SELECT utm_source FROM leads_p UNION SELECT utm_source FROM ce_p UNION ...)
SELECT s.utm_source,
  COALESCE(l.leads, 0) AS leads,
  COALESCE(c.ce, 0) AS ce,
  CASE WHEN COALESCE(l.leads,0) > 0 THEN ROUND(100.0 * COALESCE(c.ce,0) / l.leads, 1) END AS pct_ce,
  ...
FROM all_src s
LEFT JOIN leads_p l USING (utm_source)
LEFT JOIN ce_p c USING (utm_source)
...
ORDER BY leads DESC;
```

#### 4.b Sources YtD — trocar período pelo YtD nas CTEs.

#### 4.c Content Semana / 4.d Content YtD — mesma estrutura agrupando por `utm_content`.

### Bloco 5 — Gráficos 12 meses

#### 5.1 Série temporal semanal
```sql
WITH conversoes_cm AS (
  -- janela alargada para 12m + 90d antes (≈ 15 meses)
  ... cdate >= now() - INTERVAL '15 months'
),
eventos AS (
  SELECT date_trunc('week', cdate)::date AS semana, 'leads' AS metrica, account_id
  FROM deals_comercial_prod d
  WHERE cdate >= now() - INTERVAL '52 weeks' AND <filtro_cm_universal>
  UNION ALL
  SELECT date_trunc('week', d.data_agendamento_auto)::date, 'agendadas', d.account_id
  FROM deals_comercial_prod d
  WHERE d.data_agendamento_auto >= now() - INTERVAL '52 weeks'
    AND EXISTS (...regra 90d em data_agendamento_auto...)
  UNION ALL
  SELECT date_trunc('week', d.data_envio_proposta_auto)::date, 'propostas', d.account_id
  FROM deals_comercial_prod d
  WHERE d.data_envio_proposta_auto >= now() - INTERVAL '52 weeks'
    AND EXISTS (...regra 90d em data_envio_proposta_auto...)
  UNION ALL
  SELECT date_trunc('week', ct.data_fechamento_auto)::date, 'fechamentos', ct.account_id
  FROM deals_contratos_prod ct
  WHERE ct.data_fechamento_auto >= now() - INTERVAL '52 weeks'
    AND (whitelist OR (...regra 90d...))
    AND email NOT IN (blacklist)
)
SELECT semana, metrica, COUNT(*) FROM eventos GROUP BY semana, metrica ORDER BY semana;
```

#### 5.2 Proporção de reuniões por source 12m
```sql
WITH conversoes_cm AS (...)
SELECT d.utm_source,
  COUNT(*) FILTER (WHERE d.data_agendamento_auto >= now() - INTERVAL '12 months') AS ra_12m,
  COUNT(*) FILTER (WHERE d.data_inicio_reuniao_realizada >= now() - INTERVAL '12 months') AS rr_12m
FROM deals_comercial_prod d
WHERE EXISTS (
  SELECT 1 FROM conversoes_cm cm
  WHERE cm.account_id = d.account_id
    AND cm.data_conv <= COALESCE(d.data_inicio_reuniao_realizada, d.data_agendamento_auto)
    AND COALESCE(d.data_inicio_reuniao_realizada, d.data_agendamento_auto) - cm.data_conv <= INTERVAL '90 days'
)
GROUP BY d.utm_source
ORDER BY ra_12m DESC;
```

Pegar top 6 em Python, agregar resto como "outros".

---

## 6. Notas e ressalvas

- **Email do contato:** sempre `email_contato_principal_bd_sdr`. O campo `quick_email` é legado e baixa cobertura.
- **Status de fechamento em `deals_contratos_prod`:** ignorar `status`, usar `data_fechamento_auto IS NOT NULL`. O status do contrato é estado do contrato, não confirmação de venda.
- **Tipos de data:** mistos (`cdate` = `timestamptz` com hora real; colunas de evento `_auto` = `timestamp without time zone`; `data_negocio_perdido_auto` = `date`). **`data_agendamento_auto` é gravada à meia-noite** (`00:00:00`), enquanto `data_inicio_reuniao_realizada` carrega hora real. Por isso comparar evento × `cdate`/`data_conv` em timestamp cru perde casos do mesmo dia. **Use `::date` em todas as comparações de data** — períodos E janela de atribuição 90d (ver §3).
- **Normalização:** sempre `lower(trim(email))` em comparações.
- **`gclid` sticky:** o `gclid` pode persistir entre sessões — um usuário que clicou em Google Ads há semanas e hoje converteu via Meta pode ter `gclid` preenchido com `utm_source=meta`. Por isso a regra de exclusão é `NOT (utm_source='google' AND utm_medium='cpc')`, **não** `gclid IS NULL`.

---

## 7. Casos validados (verificação manual)

### Fechamentos YtD 2026 (validados com Victor — 6/6 acerto)

| Deal | Como bateu | Conv → Fech | Valor |
|---|---|---|---|
| ACALANTA (id 175222) | regra normal (utm_source=meta no contrato) | 8d | R$ 2.050 |
| Agência CROP (id 174753) | **whitelist** (`ronaldozottolo@gmail.com`) | — | R$ 3.200 |
| Wealth Tecnologia (id 175422) | **whitelist** (`jessica.rua@wealthmoney.com.br`) | — | R$ 1.650 |
| NEIVA / Alya Company (id 179039) | regra normal (utm_source=meta) | 20d | R$ 3.500 |
| Prefeitura Jataí (id 179749) | regra normal (utm_source=meta) | 25d | R$ 2.180 |
| FABRIKA (id 183535) | regra 90d via account (Sharlene Meta no comercial) | 7d | R$ 4.000 |

**Total YtD 2026: 6 fechamentos · R$ 16.580**

### Casos excluídos corretamente
- **180 Seguros** (`utm_source=cs` — canal interno)
- **modó, CULLIGAN** (`utm_source=comercial` — canal interno)
- **NUPIXEL MARKETING** (deal anterior do account era Google Ads cpc — não há conversão CM real). Desde 2026-05-26 a exclusão é explícita via blacklist (`stella.santana@parceiros-npx.com.br`, email do contrato): o fix do bug NULL passou a aceitar o contrato (URL `report-trends-2026` + utm_source NULL), então a blacklist garante que ele continue fora.
- **IDW ENTRETENIMENTO** (blacklist — Google Ads antes em outra ferramenta)
- **Hypera Pharma** (conversão CM em jul/2025, fechamento em fev/2026 = 225 dias, fora dos 90)
- **Catraca Livre, GWA, AGIS** (conversão CM antiga, fora dos 90 dias)
- **Jobhome** (URL `conteudo.buzzmonitor.com.br/indicacoes-internas` — slug não-CM)
- **Sinter Futura** (URL `conteudo.buzzmonitor.com.br/buzz-pills` + `utm_source=crm` — newsletter interna)

---

## 8. Propostas que ficaram em hold

Investigadas mas não ativadas. Documentadas para referência futura.

### HOLD A — Recuperar deals sem UTM via formulário Solicitação de Proposta

**Critério:**
```sql
OR (utm_source IS NULL AND url_conversao IS NULL
    AND origem_negocio_inbound_auto = 'LP'
    AND tipo_inbound_auto = 'Solicitação de Proposta'
    AND funil_inicial_lead_auto = 'Inbound')
```
**Status:** decisão foi mantê-lo fora do filtro V2. Adicionar à whitelist por email caso a caso.

### HOLD B — Buscar Leads também em `deals_contratos_prod`

Atualmente Leads conta só `deals_comercial_prod`. Existem casos (~16 emails da auditoria) onde o lead foi criado direto como contrato (Acalanta, Wealth, etc.). **Status:** decisão foi manter Leads apenas em `deals_comercial_prod` por simplicidade.

---

## 9. Apêndice — Auditoria dos 218 emails fornecidos pelo Victor

Resultado consolidado com o filtro V2 final (cláusula 5 conversões em hold):

| Métrica | Quantidade |
|---|---|
| Emails únicos fornecidos | 225 |
| Leads CM YtD 2026 no banco (filtro V2) | ~252 |
| Interseção (batem em ambos) | 164 |
| Da lista do Victor, fora da query | 61 |
| Da query, fora da lista do Victor | 88 |

**Causas conhecidas das discrepâncias** (sem ajuste ativo):
- ~17 emails sem trilha (utm/url NULL) que entrariam via Proposta A (HOLD)
- ~16 emails que estão só em `deals_contratos_prod` (HOLD B)
- Resto: emails do Victor que existem no banco mas com fontes não-CM (`comercial`, `sdr`, formulários internos, etc.) — exclusão correta do filtro
- Lado da query: ~88 leads CM legítimos que o Victor não tinha mapeado (provavelmente lista do Victor era subconjunto, não exaustiva)

**Decisão:** aceitar a margem de discrepância. O filtro V2 captura corretamente o conceito de CM (utm/url legítimos + 90d + whitelist/blacklist).
