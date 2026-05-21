"""queries.py — copia de dashboard/queries.py para o dashboard pessoal.

Mantem regras CM identicas ao dashboard oficial. Quando o filtro CM oficial
mudar, replicar aqui (ou criar import compartilhado depois).

Espelha dashboard/MAPEAMENTO-CAMPOS.md (Brasil-only por enquanto).
"""
from __future__ import annotations

from datetime import date, timedelta


# ============ CONSTANTES ============

CM_UTM_SOURCES: list[str] = [
    'meta', 'lp-agradecimento', 'ig', 'instagram', 'linkedin', 'notion', 'email',
    'checklist', 'whatsapp', 'pos-webinar', 'sms', 'webinar-ao-vivo',
    'apresentacao-webinar', 'lp-agradecimento-oferta-trends',
    'lp-agradecimento-evento', 'tiktok', 'chatgpt.com', 'gemini', 'blog',
]

INTERNOS_EXCLUIR: list[str] = ['cs', 'comercial', 'sdr', 'crm', 'google']


def filtro_inbound(alias: str = '') -> str:
    """No-op (espelha dashboard oficial). Retorna 'TRUE'."""
    return "TRUE"


EMAIL_WHITELIST: list[str] = [
    'jessica.rua@wealthmoney.com.br',
    'ronaldozottolo@gmail.com',
    'equipelarissaneiva@gmail.com',
    'm.lima@blankschool.com.br',
    'para.fabianogomes@gmail.com',
]

EMAIL_BLACKLIST: list[str] = [
    'julianacastro@idwcompany.com.br',
    'valdofmendes@gmail.com',
    'raissaboniolo.consultoria@gmail.com',
]

CM_SLUGS_PREFIXES: list[str] = [
    'plataforma-completa',
    'monitoramento-de-redes-sociais-2',
    'oferta-',
    'conteudo-que-converte',
    'webinar-',
    'report-trends-',
    'masterclass-trends-',
    'gestao-de-crises-',
    'relatorios-estrategicos',
    'buzz-talks-',
    'buzztalk-',
    'buzzmonitor-connect-',
]

COLUNA_EVENTO = {
    'leads': 'cdate',
    'ce':    'data_efetividade_contato_auto',
    'ra':    'data_agendamento_auto',
    'rr':    'data_inicio_reuniao_realizada',
    'prop':  'data_envio_proposta_auto',
    'perd':  'data_negocio_perdido_auto',
    'fech':  'data_fechamento_auto',
}


def _sql_list(items: list[str]) -> str:
    return ", ".join(f"'{s}'" for s in items)


def _sql_email_list(emails: list[str]) -> str:
    if not emails:
        return "SELECT ''::text WHERE FALSE"
    rows = ", ".join(f"('{e.lower().strip()}')" for e in emails)
    return f"SELECT lower(trim(email)) AS email FROM (VALUES {rows}) AS t(email)"


def filtro_cm() -> str:
    sources = _sql_list(CM_UTM_SOURCES)
    internos = _sql_list(INTERNOS_EXCLUIR)
    slugs_clauses = "\n          OR ".join(
        f"url_conversao ILIKE 'https://conteudo.buzzmonitor.com.br/{slug}%'"
        for slug in CM_SLUGS_PREFIXES
    )
    return f"""(
    NOT (utm_source = 'google' AND utm_medium = 'cpc')
    AND (
      utm_source IN ({sources})
      OR url_conversao ILIKE 'https://buzzmonitor.com/blog/%'
      OR url_conversao ILIKE 'https://buzzmonitor.com.br/blog/%'
      OR url_conversao ILIKE 'https://material.buzzmonitor.com/%'
      OR url_conversao ILIKE 'https://evento.buzzmonitor.com/%'
      OR (
        (utm_source IS NULL OR utm_source NOT IN ({internos}))
        AND (
          {slugs_clauses}
        )
      )
    )
  )"""


def cte_conversoes_cm(janela_inicio: date) -> str:
    janela = (janela_inicio - timedelta(days=90)).isoformat()
    f = filtro_cm()
    return f"""WITH conversoes_cm AS (
  SELECT account_id, cdate AS data_conv
  FROM deals_comercial_prod
  WHERE account_id IS NOT NULL
    AND cdate >= '{janela}'
    AND {f}
  UNION ALL
  SELECT account_id, cdate
  FROM deals_contratos_prod
  WHERE account_id IS NOT NULL
    AND cdate >= '{janela}'
    AND {f}
)"""


def q_count_leads(ini: date, fim: date) -> str:
    f = filtro_cm()
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    return f"""
WITH wl AS ({wl}), bl AS ({bl})
SELECT COUNT(DISTINCT lower(trim(email_contato_principal_bd_sdr))) AS n
FROM deals_comercial_prod
WHERE cdate::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND email_contato_principal_bd_sdr IS NOT NULL
  AND lower(trim(email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
  AND (
    lower(trim(email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
    OR {f}
  )
"""


def q_count_evento(kpi: str, ini: date, fim: date) -> str:
    col = COLUNA_EVENTO[kpi]
    cte = cte_conversoes_cm(ini)
    return f"""
{cte}
SELECT COUNT(*) AS n
FROM deals_comercial_prod d
WHERE d.{col}::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {filtro_inbound("d")}
  AND EXISTS (
    SELECT 1 FROM conversoes_cm cm
    WHERE cm.account_id = d.account_id
      AND cm.data_conv <= d.{col}
      AND d.{col} - cm.data_conv <= INTERVAL '90 days'
  )
"""


def q_count_perdidos(ini: date, fim: date) -> str:
    f = filtro_cm()
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    return f"""
WITH wl AS ({wl}), bl AS ({bl})
SELECT COUNT(DISTINCT lower(trim(email_contato_principal_bd_sdr))) AS n
FROM deals_comercial_prod
WHERE cdate::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND email_contato_principal_bd_sdr IS NOT NULL
  AND data_negocio_perdido_auto IS NOT NULL
  AND motivo_perda_bd_sdr IS NOT NULL
  AND lower(trim(email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
  AND (
    lower(trim(email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
    OR {f}
  )
"""


def q_count_fechamentos(ini: date, fim: date) -> str:
    cte = cte_conversoes_cm(ini)
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    return f"""
{cte},
wl AS ({wl}),
bl AS ({bl})
SELECT COUNT(*) AS n
FROM deals_contratos_prod ct
WHERE ct.data_fechamento_auto::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND lower(trim(ct.email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
  AND (
    lower(trim(ct.email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
    OR (
      {filtro_inbound("ct")}
      AND EXISTS (
        SELECT 1 FROM conversoes_cm cm
        WHERE cm.account_id = ct.account_id
          AND cm.data_conv <= ct.data_fechamento_auto
          AND ct.data_fechamento_auto - cm.data_conv <= INTERVAL '90 days'
      )
    )
  )
"""


def q_lista_leads(ini: date, fim: date) -> str:
    f = filtro_cm()
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    return f"""
WITH wl AS ({wl}), bl AS ({bl}),
filtrados AS (
  SELECT DISTINCT ON (lower(trim(d.email_contato_principal_bd_sdr)))
    d.id, d.title AS deal,
    d.email_contato_principal_bd_sdr AS email,
    d.utm_source, d.utm_content,
    d.cdate::date AS data_conversao,
    COALESCE(d.sdr_responsavel, d.sdr_sdr) AS bd,
    d.cdate
  FROM deals_comercial_prod d
  WHERE d.cdate::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
    AND d.email_contato_principal_bd_sdr IS NOT NULL
    AND lower(trim(d.email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
    AND (
      lower(trim(d.email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
      OR {f}
    )
  ORDER BY lower(trim(d.email_contato_principal_bd_sdr)), d.cdate DESC
)
SELECT id, deal, email, utm_source, utm_content, data_conversao, bd
FROM filtrados
ORDER BY cdate
"""


def q_lista_evento(kpi: str, ini: date, fim: date) -> str:
    col = COLUNA_EVENTO[kpi]
    cte = cte_conversoes_cm(ini)
    extras = ""
    if kpi == 'ra':
        extras = ", d.data_inicio_reuniao_realizada::date AS data_realizada"
    elif kpi == 'rr':
        extras = ", d.data_envio_proposta_auto::date AS data_proposta"
    return f"""
{cte}
SELECT
  d.id, d.title AS deal,
  COALESCE(d.bd_auto, d.sdr_responsavel, d.sdr_sdr) AS bd,
  d.utm_source, d.utm_content,
  d.{col}::date AS data_evento{extras}
FROM deals_comercial_prod d
WHERE d.{col}::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {filtro_inbound("d")}
  AND EXISTS (
    SELECT 1 FROM conversoes_cm cm
    WHERE cm.account_id = d.account_id
      AND cm.data_conv <= d.{col}
      AND d.{col} - cm.data_conv <= INTERVAL '90 days'
  )
ORDER BY d.{col}
"""


def q_lista_propostas(ini: date, fim: date) -> str:
    cte = cte_conversoes_cm(ini)
    return f"""
{cte}
SELECT
  d.id, d.title AS deal,
  COALESCE(d.bd_auto, d.sdr_responsavel, d.sdr_sdr) AS bd,
  d.utm_source, d.utm_content,
  d.data_envio_proposta_auto::date AS data_evento,
  d.value AS valor_text,
  d.currency
FROM deals_comercial_prod d
WHERE d.data_envio_proposta_auto::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {filtro_inbound("d")}
  AND EXISTS (
    SELECT 1 FROM conversoes_cm cm
    WHERE cm.account_id = d.account_id
      AND cm.data_conv <= d.data_envio_proposta_auto
      AND d.data_envio_proposta_auto - cm.data_conv <= INTERVAL '90 days'
  )
ORDER BY d.data_envio_proposta_auto
"""


def q_lista_fechamentos(ini: date, fim: date) -> str:
    cte = cte_conversoes_cm(ini)
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    return f"""
{cte},
wl AS ({wl}),
bl AS ({bl})
SELECT
  ct.id, ct.title AS deal,
  COALESCE(ct.bd_auto, ct.sdr_responsavel, ct.sdr_sdr) AS bd,
  ct.utm_source, ct.utm_content,
  ct.data_fechamento_auto::date AS data_evento,
  ct.value AS valor,
  ct.currency,
  ct.email_contato_principal_bd_sdr AS email
FROM deals_contratos_prod ct
WHERE ct.data_fechamento_auto::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND lower(trim(ct.email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
  AND (
    lower(trim(ct.email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
    OR (
      {filtro_inbound("ct")}
      AND EXISTS (
        SELECT 1 FROM conversoes_cm cm
        WHERE cm.account_id = ct.account_id
          AND cm.data_conv <= ct.data_fechamento_auto
          AND ct.data_fechamento_auto - cm.data_conv <= INTERVAL '90 days'
      )
    )
  )
ORDER BY ct.data_fechamento_auto
"""


def q_lista_perdidos(ini: date, fim: date) -> str:
    f = filtro_cm()
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    return f"""
WITH wl AS ({wl}), bl AS ({bl}),
filtrados AS (
  SELECT DISTINCT ON (lower(trim(d.email_contato_principal_bd_sdr)))
    d.id, d.title AS deal,
    d.email_contato_principal_bd_sdr AS email,
    d.utm_source, d.utm_content,
    COALESCE(
      d.data_efetividade_contato_auto::date,
      d.cdate::date
    ) AS ultima_conversao,
    d.motivo_perda_bd_sdr AS motivo,
    d.data_negocio_perdido_auto::date AS data_perda
  FROM deals_comercial_prod d
  WHERE d.cdate::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
    AND d.email_contato_principal_bd_sdr IS NOT NULL
    AND d.data_negocio_perdido_auto IS NOT NULL
    AND d.motivo_perda_bd_sdr IS NOT NULL
    AND lower(trim(d.email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
    AND (
      lower(trim(d.email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
      OR {f}
    )
  ORDER BY lower(trim(d.email_contato_principal_bd_sdr)), d.data_negocio_perdido_auto DESC
)
SELECT id, deal, email, utm_source, utm_content, ultima_conversao, motivo, data_perda
FROM filtrados
ORDER BY data_perda DESC
"""


def q_ranking(dim: str, ini: date, fim: date) -> str:
    if dim not in ('utm_source', 'utm_content'):
        raise ValueError(f"dim invalido: {dim}")

    cte = cte_conversoes_cm(ini)
    f = filtro_cm()
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    d1, d2 = ini.isoformat(), fim.isoformat()

    return f"""
{cte},
wl AS ({wl}),
bl AS ({bl}),
leads_p AS (
  SELECT {dim} AS dim, COUNT(*) AS leads
  FROM deals_comercial_prod
  WHERE cdate::date BETWEEN '{d1}' AND '{d2}'
    AND email_contato_principal_bd_sdr IS NOT NULL
    AND lower(trim(email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
    AND (
      lower(trim(email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
      OR {f}
    )
  GROUP BY {dim}
),
ce_p AS (
  SELECT d.{dim} AS dim, COUNT(*) AS ce
  FROM deals_comercial_prod d
  WHERE d.data_efetividade_contato_auto::date BETWEEN '{d1}' AND '{d2}'
    AND {filtro_inbound("d")}
    AND EXISTS (
      SELECT 1 FROM conversoes_cm cm
      WHERE cm.account_id = d.account_id
        AND cm.data_conv <= d.data_efetividade_contato_auto
        AND d.data_efetividade_contato_auto - cm.data_conv <= INTERVAL '90 days'
    )
  GROUP BY d.{dim}
),
ra_p AS (
  SELECT d.{dim} AS dim, COUNT(*) AS ra
  FROM deals_comercial_prod d
  WHERE d.data_agendamento_auto::date BETWEEN '{d1}' AND '{d2}'
    AND {filtro_inbound("d")}
    AND EXISTS (
      SELECT 1 FROM conversoes_cm cm
      WHERE cm.account_id = d.account_id
        AND cm.data_conv <= d.data_agendamento_auto
        AND d.data_agendamento_auto - cm.data_conv <= INTERVAL '90 days'
    )
  GROUP BY d.{dim}
),
rr_p AS (
  SELECT d.{dim} AS dim, COUNT(*) AS rr
  FROM deals_comercial_prod d
  WHERE d.data_inicio_reuniao_realizada::date BETWEEN '{d1}' AND '{d2}'
    AND {filtro_inbound("d")}
    AND EXISTS (
      SELECT 1 FROM conversoes_cm cm
      WHERE cm.account_id = d.account_id
        AND cm.data_conv <= d.data_inicio_reuniao_realizada
        AND d.data_inicio_reuniao_realizada - cm.data_conv <= INTERVAL '90 days'
    )
  GROUP BY d.{dim}
),
prop_p AS (
  SELECT d.{dim} AS dim, COUNT(*) AS prop
  FROM deals_comercial_prod d
  WHERE d.data_envio_proposta_auto::date BETWEEN '{d1}' AND '{d2}'
    AND {filtro_inbound("d")}
    AND EXISTS (
      SELECT 1 FROM conversoes_cm cm
      WHERE cm.account_id = d.account_id
        AND cm.data_conv <= d.data_envio_proposta_auto
        AND d.data_envio_proposta_auto - cm.data_conv <= INTERVAL '90 days'
    )
  GROUP BY d.{dim}
),
fech_p AS (
  SELECT ct.{dim} AS dim, COUNT(*) AS fech
  FROM deals_contratos_prod ct
  WHERE ct.data_fechamento_auto::date BETWEEN '{d1}' AND '{d2}'
    AND lower(trim(ct.email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
    AND (
      lower(trim(ct.email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
      OR (
        {filtro_inbound("ct")}
        AND EXISTS (
          SELECT 1 FROM conversoes_cm cm
          WHERE cm.account_id = ct.account_id
            AND cm.data_conv <= ct.data_fechamento_auto
            AND ct.data_fechamento_auto - cm.data_conv <= INTERVAL '90 days'
        )
      )
    )
  GROUP BY ct.{dim}
),
all_dim AS (
  SELECT dim FROM leads_p
  UNION SELECT dim FROM ce_p
  UNION SELECT dim FROM ra_p
  UNION SELECT dim FROM rr_p
  UNION SELECT dim FROM prop_p
  UNION SELECT dim FROM fech_p
)
SELECT
  COALESCE(a.dim, '(vazio)') AS dim,
  COALESCE(l.leads, 0) AS leads,
  COALESCE(c.ce, 0) AS ce,
  COALESCE(r.ra, 0) AS ra,
  COALESCE(rr.rr, 0) AS rr,
  COALESCE(p.prop, 0) AS prop,
  COALESCE(f.fech, 0) AS fech
FROM all_dim a
LEFT JOIN leads_p l USING (dim)
LEFT JOIN ce_p c USING (dim)
LEFT JOIN ra_p r USING (dim)
LEFT JOIN rr_p rr USING (dim)
LEFT JOIN prop_p p USING (dim)
LEFT JOIN fech_p f USING (dim)
ORDER BY leads DESC, ra DESC
"""


def q_source_por_content(ini: date, fim: date) -> str:
    f = filtro_cm()
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    return f"""
WITH wl AS ({wl}), bl AS ({bl}),
ranked AS (
  SELECT
    utm_content,
    utm_source,
    COUNT(*) AS n,
    ROW_NUMBER() OVER (PARTITION BY utm_content ORDER BY COUNT(*) DESC) AS rn
  FROM deals_comercial_prod
  WHERE cdate::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
    AND email_contato_principal_bd_sdr IS NOT NULL
    AND lower(trim(email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
    AND (
      lower(trim(email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
      OR {f}
    )
    AND utm_content IS NOT NULL
  GROUP BY utm_content, utm_source
)
SELECT utm_content, utm_source
FROM ranked
WHERE rn = 1
"""


def q_serie_temporal_12m(hoje: date) -> str:
    janela_inicio = (hoje - timedelta(days=365 + 90))
    cte = cte_conversoes_cm(janela_inicio)
    f = filtro_cm()
    wl = _sql_email_list(EMAIL_WHITELIST)
    bl = _sql_email_list(EMAIL_BLACKLIST)
    hoje_iso = hoje.isoformat()
    janela_12m_inicio = (hoje - timedelta(weeks=52)).isoformat()

    return f"""
{cte},
wl AS ({wl}),
bl AS ({bl}),
eventos AS (
  SELECT date_trunc('week', cdate)::date AS semana, 'leads' AS metrica
  FROM deals_comercial_prod
  WHERE cdate::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
    AND email_contato_principal_bd_sdr IS NOT NULL
    AND lower(trim(email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
    AND (
      lower(trim(email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
      OR {f}
    )
  UNION ALL
  SELECT date_trunc('week', d.data_efetividade_contato_auto)::date, 'ce'
  FROM deals_comercial_prod d
  WHERE d.data_efetividade_contato_auto::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
    AND {filtro_inbound("d")}
    AND EXISTS (
      SELECT 1 FROM conversoes_cm cm
      WHERE cm.account_id = d.account_id
        AND cm.data_conv <= d.data_efetividade_contato_auto
        AND d.data_efetividade_contato_auto - cm.data_conv <= INTERVAL '90 days'
    )
  UNION ALL
  SELECT date_trunc('week', d.data_agendamento_auto)::date, 'agendadas'
  FROM deals_comercial_prod d
  WHERE d.data_agendamento_auto::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
    AND {filtro_inbound("d")}
    AND EXISTS (
      SELECT 1 FROM conversoes_cm cm
      WHERE cm.account_id = d.account_id
        AND cm.data_conv <= d.data_agendamento_auto
        AND d.data_agendamento_auto - cm.data_conv <= INTERVAL '90 days'
    )
  UNION ALL
  SELECT date_trunc('week', d.data_envio_proposta_auto)::date, 'propostas'
  FROM deals_comercial_prod d
  WHERE d.data_envio_proposta_auto::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
    AND {filtro_inbound("d")}
    AND EXISTS (
      SELECT 1 FROM conversoes_cm cm
      WHERE cm.account_id = d.account_id
        AND cm.data_conv <= d.data_envio_proposta_auto
        AND d.data_envio_proposta_auto - cm.data_conv <= INTERVAL '90 days'
    )
  UNION ALL
  SELECT date_trunc('week', ct.data_fechamento_auto)::date, 'fechamentos'
  FROM deals_contratos_prod ct
  WHERE ct.data_fechamento_auto::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
    AND lower(trim(ct.email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
    AND (
      lower(trim(ct.email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
      OR (
        {filtro_inbound("ct")}
        AND EXISTS (
          SELECT 1 FROM conversoes_cm cm
          WHERE cm.account_id = ct.account_id
            AND cm.data_conv <= ct.data_fechamento_auto
            AND ct.data_fechamento_auto - cm.data_conv <= INTERVAL '90 days'
        )
      )
    )
)
SELECT semana, metrica, COUNT(*) AS n
FROM eventos
GROUP BY semana, metrica
ORDER BY semana, metrica
"""


def q_proporcao_sources_12m(hoje: date) -> str:
    janela_inicio = hoje - timedelta(days=365 + 90)
    cte = cte_conversoes_cm(janela_inicio)
    janela_12m_inicio = (hoje - timedelta(weeks=52)).isoformat()
    hoje_iso = hoje.isoformat()

    return f"""
{cte}
SELECT
  COALESCE(d.utm_source, '(vazio)') AS source,
  COUNT(*) FILTER (
    WHERE d.data_agendamento_auto::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
      AND EXISTS (
        SELECT 1 FROM conversoes_cm cm
        WHERE cm.account_id = d.account_id
          AND cm.data_conv <= d.data_agendamento_auto
          AND d.data_agendamento_auto - cm.data_conv <= INTERVAL '90 days'
      )
  ) AS ra_12m,
  COUNT(*) FILTER (
    WHERE d.data_inicio_reuniao_realizada::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
      AND EXISTS (
        SELECT 1 FROM conversoes_cm cm
        WHERE cm.account_id = d.account_id
          AND cm.data_conv <= d.data_inicio_reuniao_realizada
          AND d.data_inicio_reuniao_realizada - cm.data_conv <= INTERVAL '90 days'
      )
  ) AS rr_12m
FROM deals_comercial_prod d
WHERE {filtro_inbound("d")}
  AND (
    d.data_agendamento_auto::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
    OR d.data_inicio_reuniao_realizada::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
  )
GROUP BY d.utm_source
HAVING COUNT(*) FILTER (
  WHERE d.data_agendamento_auto::date BETWEEN '{janela_12m_inicio}' AND '{hoje_iso}'
    AND EXISTS (
      SELECT 1 FROM conversoes_cm cm
      WHERE cm.account_id = d.account_id
        AND cm.data_conv <= d.data_agendamento_auto
        AND d.data_agendamento_auto - cm.data_conv <= INTERVAL '90 days'
    )
) > 0
ORDER BY ra_12m DESC
"""
