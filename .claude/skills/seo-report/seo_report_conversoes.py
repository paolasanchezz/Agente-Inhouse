"""
SEO Report - item (e): artigos que mais convertem (Supabase)

Reusa AS MESMAS queries de "Fechamentos CM" já validadas nas dashboards locais
(dashboard/queries.py e dashboard/queries_cxpress.py) — não reimplementa a
lógica de atribuição CM, só agrupa o resultado por utm_content (post) e soma
receita/ticket médio. Escopo: só Buzzmonitor BR e Cxpress BR — únicas marcas
com tabela de deals em PRODUÇÃO (LATAM só tem staging; Portugal não tem
nenhuma tabela ainda — decisão registrada em 2026-07-27).

Conexão: mesma de todas as dashboards — lê SUPABASE_PG_URL de dashboard/.env
(Postgres read-only, usuário looker_readonly). Nunca commitar esse .env.

Saídas:
  {SEO_REPORT_DIR}/seo_conversoes.json — visão de 6 meses (buzzmonitor-br /
    cxpress-br) + tendencia_3m (leads CRIADOS mês a mês nos 3 meses anteriores
    ao mês de análise, com status de fechamento e receita por artigo).

Como usar:
    uv run --python 3.12 --with "psycopg[binary]" python seo_report_conversoes.py

Período padrão: janela de 180 dias para a seção principal (fechamentos);
últimos 3 meses completos antes do mês de análise para a seção de tendência.
Overrides via env:
  SEO_REPORT_CONV_INICIO / SEO_REPORT_CONV_FIM (YYYY-MM-DD): janela da seção
    principal (fechamentos). O mês de análise é derivado de SEO_REPORT_CONV_FIM
    (ou date.today() se não definido) para calcular os 3 meses da tendência.
"""

from __future__ import annotations

import os
import re
import sys
import json
import unicodedata
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent  # .../.claude/skills/seo-report
REPO_ROOT = HERE.parents[2]  # seo-report -> skills -> .claude -> repo root
DASHBOARD_DIR = REPO_ROOT / "dashboard"
sys.path.insert(0, str(DASHBOARD_DIR))

import psycopg  # noqa: E402
import queries as QB  # noqa: E402  — Buzzmonitor (deals_comercial_prod / deals_contratos_prod)
import queries_cxpress as QC  # noqa: E402  — Cxpress (cxpress_deals_funil_principal_prod)

BASE_DIR = Path(os.environ.get("SEO_REPORT_DIR", Path.home() / ".seo-report-buzzmonitor"))
BASE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_JSON = BASE_DIR / "seo_conversoes.json"

CLUSTER_MAP = json.loads((HERE / "cluster_mapping.json").read_text(encoding="utf-8"))

# Janela maior que GSC/GA4/Semrush (28d): conversao de post de blog se acumula ao
# longo de meses, nao de semanas — 28d teria amostra pequena demais pra ser util.
PERIODO_DIAS = 180


def load_url() -> str:
    env_path = DASHBOARD_DIR / ".env"
    if not env_path.exists():
        raise SystemExit(
            f"ERRO: {env_path} nao existe. Copie dashboard/.env.example para "
            "dashboard/.env e preencha SUPABASE_PG_URL antes de rodar."
        )
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("SUPABASE_PG_URL="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("ERRO: SUPABASE_PG_URL nao encontrado em dashboard/.env")


def fetch_all(cur, sql: str) -> list[dict]:
    cur.execute(sql)
    cols = [d.name for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


# ============ SEÇÃO PRINCIPAL: fechamentos no período ============

def q_fechamentos_blog_buzzmonitor(ini: date, fim: date) -> str:
    """Como QB.q_lista_fechamentos, mas restrito a conversao de BLOG de verdade.

    Descoberto testando com dado real (2026-07-28): o utm_content dos fechamentos no
    escopo CM completo costuma ser nome de CRIATIVO DE ANUNCIO/remarketing (ex: "RMKT 7 -
    UGC computador"), nao slug de post — filtro_cm() cobre social/email/webinar/blog juntos
    de proposito (visao ampla de CM), mas o pedido aqui e especificamente "artigo de blog
    que mais converte". Isolar por utm_source='blog' OU URL de blog e o que faz isso de fato.
    """
    cte = QB.cte_conversoes_cm(ini)
    wl = QB._sql_email_list(QB.EMAIL_WHITELIST)
    bl = QB._sql_email_list(QB.EMAIL_BLACKLIST)
    return f"""
{cte},
wl AS ({wl}),
bl AS ({bl})
SELECT
  ct.utm_content, ct.utm_source, ct.value AS valor_text, ct.currency
FROM deals_contratos_prod ct
WHERE ct.data_fechamento_auto::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND lower(trim(ct.email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
  AND (
    lower(trim(ct.email_contato_principal_bd_sdr)) IN (SELECT email FROM wl)
    OR (
      {QB.filtro_inbound("ct")}
      AND {QB._atrib_cm_90d("data_fechamento_auto", "ct")}
    )
  )
  AND (
    LOWER(COALESCE(ct.utm_source, '')) = 'blog'
    OR ct.url_conversao ILIKE 'https://buzzmonitor.com/blog/%'
    OR ct.url_conversao ILIKE 'https://buzzmonitor.com.br/blog/%'
  )
"""


def q_fechamentos_blog_cxpress(ini: date, fim: date) -> str:
    """Como QC.q_lista_fechamentos, mas restrito a conversao de blog (mesma razao acima —
    Cxpress tambem teve deal com utm_content de anuncio ("ad_03") no escopo CM completo)."""
    esc = QC._escopo("d")
    return f"""
SELECT d.id, {QC._content('d')} AS utm_content, d.utm_source,
       {QC.COL_VALOR} AS valor_text, d.currency
FROM {QC.TABELA} d
WHERE {QC._d('d.' + QC.COL_FECHAMENTO)} BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {esc}
  AND (
    LOWER(COALESCE(d.utm_source, '')) = 'blog'
    OR d.url_conversao ILIKE 'https://blog.cxpress.io/%'
  )
"""


# ============ SEÇÃO TENDÊNCIA: leads CRIADOS mês a mês ============

def q_leads_blog_buzzmonitor(ini: date, fim: date) -> str:
    """Leads CRIADOS no período com atribuição de blog (deals_comercial_prod.cdate).

    Diferença da q_fechamentos_*: filtra por data de CRIAÇÃO (cdate), não por data
    de fechamento. Inclui status de fechamento via LEFT JOIN lateral com contratos
    (email-based — mesma semântica da CTE conversoes_cm). Só conta contrato fechado
    a partir da criação do lead, e pega o primeiro: sem essa trava, um cliente antigo
    que volta pelo blog aparecia como "Fechado" com a receita de um contrato de anos atrás.

    Escopo: blog direto (utm_source='blog' OU url /blog/) sem a regra de 90d de
    atribuição CM — o pedido é "quais leads vieram especificamente do blog".
    """
    wl = QB._sql_email_list(QB.EMAIL_WHITELIST)
    bl = QB._sql_email_list(QB.EMAIL_BLACKLIST)
    return f"""
WITH wl AS ({wl}),
bl AS ({bl})
SELECT
  d.id,
  COALESCE(NULLIF(TRIM(d.utm_content), ''), '(sem utm_content)') AS utm_content,
  d.utm_source,
  d.cdate::date AS data_criacao,
  CASE
    WHEN fech.data_fechamento_auto IS NOT NULL THEN 'Fechado'
    ELSE 'Nao fechado'
  END AS status_fechamento,
  fech.value AS valor_text,
  fech.currency
FROM deals_comercial_prod d
LEFT JOIN LATERAL (
  SELECT ct.data_fechamento_auto, ct.value, ct.currency
  FROM deals_contratos_prod ct
  WHERE lower(trim(ct.email_contato_principal_bd_sdr)) = lower(trim(d.email_contato_principal_bd_sdr))
    AND ct.data_fechamento_auto::date >= d.cdate::date
  ORDER BY ct.data_fechamento_auto ASC
  LIMIT 1
) fech ON TRUE
WHERE d.cdate::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND d.email_contato_principal_bd_sdr IS NOT NULL
  AND lower(trim(d.email_contato_principal_bd_sdr)) NOT IN (SELECT email FROM bl)
  AND {QB.filtro_inbound("d")}
  AND (
    LOWER(COALESCE(d.utm_source, '')) = 'blog'
    OR d.url_conversao ILIKE 'https://buzzmonitor.com/blog/%'
    OR d.url_conversao ILIKE 'https://buzzmonitor.com.br/blog/%'
  )
"""


def q_leads_blog_cxpress(ini: date, fim: date) -> str:
    """Leads CRIADOS no período com atribuição de blog (Cxpress — tabela única).

    Usa cdate (COL_LEAD) como data de criação. O status de fechamento e o valor
    estão na mesma linha (data_do_fechamento_auto / status).
    """
    esc = QC._escopo("d")
    return f"""
SELECT
  d.id,
  {QC._content('d')} AS utm_content,
  d.utm_source,
  d.{QC.COL_LEAD}::date AS data_criacao,
  CASE
    WHEN {QC._d('d.' + QC.COL_FECHAMENTO)} IS NOT NULL THEN 'Fechado'
    WHEN d.status = 'Perdido' THEN 'Perdido'
    ELSE 'Em progresso'
  END AS status_fechamento,
  {QC.COL_VALOR} AS valor_text,
  d.currency
FROM {QC.TABELA} d
WHERE d.{QC.COL_LEAD}::date BETWEEN '{ini.isoformat()}' AND '{fim.isoformat()}'
  AND {esc}
  AND (
    LOWER(COALESCE(d.utm_source, '')) = 'blog'
    OR d.url_conversao ILIKE 'https://blog.cxpress.io/%'
  )
"""


# ============ HELPERS ============

def parse_valor_numeric(v) -> float | None:
    """Mesma limpeza de dashboard/render_helpers.parse_valor_text, mas devolve
    float (pra somar/tirar media) em vez de string formatada BR."""
    if not v:
        return None
    s = str(v).strip()
    if not s:
        return None
    clean = s.replace("R$", "").replace("r$", "").strip()
    if "/" in clean:
        clean = clean.split("/")[0].strip()
    if "," in clean:
        clean = clean.replace(".", "").replace(",", ".")
    try:
        return float(clean)
    except (ValueError, TypeError):
        return None


def _slugify(s: str) -> str:
    s = str(s or "").lower()
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def _match_cluster(post: str, clusters: list[dict]) -> str:
    """Fuzzy match best-effort (slugify + contains). Ver cluster_mapping.json
    pra contexto — nao e garantia de 100% de cobertura, so aproximacao."""
    post_slug = _slugify(post)
    melhor, melhor_len = None, 0
    for entry in clusters:
        for kw in entry.get("keywords", []):
            kw_slug = _slugify(kw)
            if kw_slug and (kw_slug in post_slug or post_slug in kw_slug):
                if len(kw_slug) > melhor_len:
                    melhor, melhor_len = entry["cluster"], len(kw_slug)
    return melhor or "Sem cluster mapeado"


# ============ AGREGAÇÕES ============

def agregar_por_post(rows: list[dict], marca: str) -> dict:
    """Agrega fechamentos da seção principal por post (utm_content)."""
    clusters = CLUSTER_MAP.get(marca, [])
    posts: dict[str, dict] = {}
    moedas = set()
    for r in rows:
        content = (r.get("utm_content") or "").strip() or "(sem utm_content)"
        valor = parse_valor_numeric(r.get("valor_text") if r.get("valor_text") is not None else r.get("valor"))
        moedas.add(r.get("currency") or "BRL")
        p = posts.setdefault(content, {"post": content, "deals": 0, "receita": 0.0})
        p["deals"] += 1
        if valor:
            p["receita"] += valor
    for p in posts.values():
        p["ticket_medio"] = round(p["receita"] / p["deals"], 2) if p["deals"] else 0
        p["receita"] = round(p["receita"], 2)
        p["cluster"] = _match_cluster(p["post"], clusters)
    ordenado = sorted(posts.values(), key=lambda x: x["receita"], reverse=True)
    return {
        "moeda": moedas.pop() if len(moedas) == 1 else "mista",
        "total_deals": sum(p["deals"] for p in posts.values()),
        "total_receita": round(sum(p["receita"] for p in posts.values()), 2),
        "posts": ordenado[:20],
    }


def agregar_leads_mes(rows: list[dict], marca: str) -> dict:
    """Agrega leads CRIADOS num mês por post, com status de fechamento e receita."""
    clusters = CLUSTER_MAP.get(marca, [])
    posts: dict[str, dict] = {}
    total_leads = 0
    total_fechados = 0
    receita_total = 0.0

    for r in rows:
        total_leads += 1
        content = (r.get("utm_content") or "").strip() or "(sem utm_content)"
        status = r.get("status_fechamento", "Nao fechado")
        fechou = status == "Fechado"
        if fechou:
            total_fechados += 1

        valor = parse_valor_numeric(r.get("valor_text")) if fechou else None
        if valor:
            receita_total += valor

        p = posts.setdefault(content, {"post": content, "leads": 0, "fechados": 0, "receita": 0.0})
        p["leads"] += 1
        if fechou:
            p["fechados"] += 1
            if valor:
                p["receita"] += valor

    for p in posts.values():
        p["receita"] = round(p["receita"], 2)
        p["cluster"] = _match_cluster(p["post"], clusters)

    ordenado = sorted(posts.values(), key=lambda x: x["leads"], reverse=True)
    return {
        "total_leads": total_leads,
        "total_fechados": total_fechados,
        "total_nao_fechados": total_leads - total_fechados,
        "receita_total": round(receita_total, 2),
        "posts": ordenado[:20],
    }


def _primeiro_e_ultimo_dia(ano: int, mes: int) -> tuple[date, date]:
    ini = date(ano, mes, 1)
    fim = date(ano, mes + 1, 1) - timedelta(days=1) if mes < 12 else date(ano, 12, 31)
    return ini, fim


def meses_tendencia(mes_analise: date) -> list[tuple[date, date, str]]:
    """Retorna os 3 meses completos anteriores ao mês de análise, em ordem crescente.

    Exemplo: mes_analise = 2026-07-31 → [(2026-04-01, 2026-04-30, '2026-04'),
                                          (2026-05-01, 2026-05-31, '2026-05'),
                                          (2026-06-01, 2026-06-30, '2026-06')]
    """
    resultado = []
    ano, mes = mes_analise.year, mes_analise.month
    for _ in range(3):
        mes -= 1
        if mes == 0:
            mes = 12
            ano -= 1
        ini, fim = _primeiro_e_ultimo_dia(ano, mes)
        resultado.insert(0, (ini, fim, f"{ano}-{mes:02d}"))
    return resultado


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    # Janela padrao da secao principal: ultimos PERIODO_DIAS. Pra mes fechado
    # (ex: relatorio mensal pra diretoria), defina SEO_REPORT_CONV_INICIO/FIM (YYYY-MM-DD).
    if os.environ.get("SEO_REPORT_CONV_INICIO"):
        ini = date.fromisoformat(os.environ["SEO_REPORT_CONV_INICIO"])
        hoje = date.fromisoformat(os.environ["SEO_REPORT_CONV_FIM"])
    else:
        hoje = date.today()
        ini = hoje - timedelta(days=PERIODO_DIAS)

    # Mês de análise = mês de hoje (ou do FIM definido) — determina os 3 meses de tendência.
    mes_analise = hoje

    print(f"Coletando conversoes CM por post ({ini.isoformat()} a {hoje.isoformat()})...")
    url = load_url()
    with psycopg.connect(url, autocommit=True) as conn, conn.cursor() as cur:
        cur.execute("SET statement_timeout = '300s'")

        # --- Secao principal: fechamentos no periodo ---
        print("  [1/2] Buzzmonitor BR (deals_contratos_prod, fechamentos de BLOG)...")
        rows_bzm = fetch_all(cur, q_fechamentos_blog_buzzmonitor(ini, hoje))
        print("  [2/2] Cxpress BR (cxpress_deals_funil_principal_prod, fechamentos de BLOG)...")
        rows_cx = fetch_all(cur, q_fechamentos_blog_cxpress(ini, hoje))

        # --- Tendencia 3 meses: leads CRIADOS mes a mes ---
        meses = meses_tendencia(mes_analise)
        print(f"\nColetando tendencia de leads ({meses[0][0].isoformat()} a {meses[-1][1].isoformat()})...")
        tendencia: dict = {}
        for ini_m, fim_m, label in meses:
            label_exibir = ini_m.strftime("%B/%Y")
            print(f"  [{label_exibir}] Buzzmonitor BR — leads blog criados...")
            rows_bzm_t = fetch_all(cur, q_leads_blog_buzzmonitor(ini_m, fim_m))
            print(f"  [{label_exibir}] Cxpress BR — leads blog criados...")
            rows_cx_t = fetch_all(cur, q_leads_blog_cxpress(ini_m, fim_m))
            tendencia[label] = {
                "periodo": {"inicio": ini_m.isoformat(), "fim": fim_m.isoformat()},
                "buzzmonitor-br": agregar_leads_mes(rows_bzm_t, "buzzmonitor"),
                "cxpress-br": agregar_leads_mes(rows_cx_t, "cxpress"),
            }

    saida = {
        "gerado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "periodo": {"inicio": ini.isoformat(), "fim": hoje.isoformat(), "dias": PERIODO_DIAS},
        "mes_analise": f"{mes_analise.year}-{mes_analise.month:02d}",
        "buzzmonitor-br": agregar_por_post(rows_bzm, "buzzmonitor"),
        "cxpress-br": agregar_por_post(rows_cx, "cxpress"),
        "tendencia_3m": tendencia,
    }
    OUTPUT_JSON.write_text(json.dumps(saida, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

    print(f"\nOK -> {OUTPUT_JSON}")
    print(f"  Fechamentos Buzzmonitor BR: {len(rows_bzm)} em {len(saida['buzzmonitor-br']['posts'])} posts")
    print(f"  Fechamentos Cxpress BR:     {len(rows_cx)} em {len(saida['cxpress-br']['posts'])} posts")
    for label_m, dado_m in tendencia.items():
        bzm_t = dado_m["buzzmonitor-br"]
        cx_t = dado_m["cxpress-br"]
        print(
            f"  Tendencia {label_m}: Buzz={bzm_t['total_leads']} leads "
            f"({bzm_t['total_fechados']} fech) | "
            f"Cx={cx_t['total_leads']} leads ({cx_t['total_fechados']} fech)"
        )
