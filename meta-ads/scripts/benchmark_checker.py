"""
benchmark_checker.py — Classificação de métricas contra valores de referência.

Carrega benchmarks.json e classifica cada métrica em:
  [BOM] Bom / [OK] Aceitável / [RUIM] Ruim / [ ] N/A

Zero chamadas à API — apenas lógica local.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cache_manager import load_benchmarks, ACCOUNTS


# ============================================================
# Classificação de status por métrica
# ============================================================

def get_metric_status(metric: str, value: float,
                      benchmark_group: str, campaign_type: str) -> str:
    """
    Retorna string com ícone de status:
      [BOM] Bom | [OK] Aceitável | [RUIM] Ruim | [ ] N/A
    """
    if campaign_type == "nao_classificada":
        return "[ ] N/A"
    if value == 0:
        return "[ ] Sem dados"

    benchmarks = load_benchmarks()

    # Frequência: benchmark global (independe de moeda)
    if metric == "frequency":
        b = benchmarks.get("global", {}).get("frequency", {})
        if not b:
            return "[ ] Sem benchmark"
        if value <= b["bom"]["max"]:
            return "[BOM] Bom"
        if value <= b["aceitavel"]["max"]:
            return "[OK] Aceitável"
        return "[RUIM] Ruim"

    # Outras métricas: por grupo de moeda e tipo de campanha
    b = (
        benchmarks
        .get(benchmark_group, {})
        .get(campaign_type, {})
        .get(metric)
    )
    if not b:
        return "[ ] Sem benchmark"

    # Métricas onde menor = melhor (custo)
    if metric == "cost_per_lead":
        if value <= b["bom"]["max"]:
            return "[BOM] Bom"
        if value <= b["aceitavel"]["max"]:
            return "[OK] Aceitável"
        return "[RUIM] Ruim"

    # Métricas onde maior = melhor (taxa/conversão)
    if metric in ["ctr_link", "lp_conversion_rate"]:
        if value >= b["bom"]["min"]:
            return "[BOM] Bom"
        if value >= b["aceitavel"]["min"]:
            return "[OK] Aceitável"
        return "[RUIM] Ruim"

    return "[ ] Sem benchmark"


# ============================================================
# Verificação completa de uma entidade
# ============================================================

def check_entity_benchmarks(metrics: dict, account_key: str, campaign_type: str) -> dict:
    """
    Recebe dict de métricas agregadas de uma entidade e retorna dict com status por métrica.

    metrics: {"spend": 500.0, "ctr_link": 1.8, "cost_per_lead": 10.5, ...}
    Retorna: {"ctr_link": "[BOM] Bom", "cost_per_lead": "[BOM] Bom", "frequency": "[OK] Aceitável", ...}
    """
    account = ACCOUNTS.get(account_key, {})
    benchmark_group = account.get("benchmark_group", "brl")

    benchmarked_metrics = ["cost_per_lead", "ctr_link", "lp_conversion_rate", "frequency"]
    return {
        m: get_metric_status(m, float(metrics.get(m, 0)), benchmark_group, campaign_type)
        for m in benchmarked_metrics
        if m in metrics
    }


# ============================================================
# Agregação de métricas de período para uma entidade
# ============================================================

def aggregate_metrics_for_period(entity_id: str, entity_type: str,
                                  account_key: str, date_start: str, date_end: str) -> dict:
    """
    Agrega métricas do banco para o período solicitado.
    SUM para totais, médias calculadas a partir dos totais (para evitar distorção de AVG de AVG).
    """
    from cache_manager import get_connection

    conn = get_connection()
    row = conn.execute(
        """SELECT
               SUM(spend)         as spend,
               SUM(impressions)   as impressions,
               SUM(reach)         as reach,
               SUM(link_clicks)   as link_clicks,
               SUM(leads)         as leads,
               AVG(frequency)     as frequency,
               AVG(ctr_link)      as ctr_link,
               AVG(cpm)           as cpm,
               AVG(cpc_link)      as cpc_link,
               AVG(cost_per_lead) as cost_per_lead,
               AVG(lp_conversion_rate) as lp_conversion_rate,
               SUM(video_p25)     as video_p25,
               SUM(video_p50)     as video_p50,
               SUM(video_p75)     as video_p75,
               SUM(video_p100)    as video_p100
           FROM insights
           WHERE entity_id=? AND entity_type=? AND account_key=?
           AND date >= ? AND date <= ?""",
        [entity_id, entity_type, account_key, date_start, date_end],
    ).fetchone()
    conn.close()

    if not row or row["spend"] is None:
        return {}

    result = dict(row)

    # Recalcula CpL e conv. LP a partir dos totais (mais preciso que AVG de AVG)
    leads = int(result.get("leads", 0) or 0)
    spend = float(result.get("spend", 0) or 0)
    link_clicks = int(result.get("link_clicks", 0) or 0)

    result["cost_per_lead"] = round(spend / leads, 2) if leads > 0 else 0.0
    result["lp_conversion_rate"] = round((leads / link_clicks) * 100, 2) if link_clicks > 0 else 0.0

    return {k: (round(float(v), 4) if v is not None else 0) for k, v in result.items()}


# ============================================================
# Resumo por grupo de funil
# ============================================================

def summarize_funnel_group(campaigns: list, account_key: str,
                            date_start: str, date_end: str) -> dict:
    """
    Agrega métricas de todas as campanhas de um grupo de funil.
    Retorna dict com totais e médias do grupo.
    """
    totals = {
        "spend": 0.0, "impressions": 0, "link_clicks": 0, "leads": 0,
        "reach": 0,
    }
    avgs = {"ctr_link": [], "cpm": [], "frequency": []}

    for camp in campaigns:
        m = aggregate_metrics_for_period(
            camp["id"], "campaign", account_key, date_start, date_end
        )
        if not m:
            continue
        for k in totals:
            totals[k] += m.get(k, 0)
        for k in avgs:
            if m.get(k, 0) > 0:
                avgs[k].append(m[k])

    result = {**totals}
    for k, vals in avgs.items():
        result[k] = round(sum(vals) / len(vals), 4) if vals else 0.0

    # Recalcula métricas derivadas dos totais
    leads = int(result["leads"])
    spend = float(result["spend"])
    link_clicks = int(result["link_clicks"])

    result["cost_per_lead"] = round(spend / leads, 2) if leads > 0 else 0.0
    result["lp_conversion_rate"] = round((leads / link_clicks) * 100, 2) if link_clicks > 0 else 0.0

    return result
