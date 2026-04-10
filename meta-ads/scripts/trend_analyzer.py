"""
trend_analyzer.py — Análise de tendências temporais por janelas de 3/7/15/30 dias.

Todos os cálculos são feitos localmente no SQLite. Zero chamadas à API.

Métricas de soma (spend, leads, etc.) usam SUM por janela.
Métricas de média (CTR, CPM, etc.) usam AVG por janela.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cache_manager import get_connection

# ============================================================
# Configuração das janelas e classificação de métricas
# ============================================================

TREND_WINDOWS = [3, 7, 15, 30]  # dias

# Métricas que somam para o período (não faz sentido fazer média de totais)
SUM_METRICS = ["spend", "impressions", "link_clicks", "leads", "reach"]

# Métricas que usam média ponderada (são taxas ou custos por unidade)
AVG_METRICS = [
    "ctr_link", "cpm", "cpc_link", "cost_per_lead",
    "frequency", "lp_conversion_rate",
]

# Métricas onde aumento é POSITIVO (mais = melhor)
POSITIVE_DIRECTION = ["leads", "link_clicks", "ctr_link", "lp_conversion_rate", "impressions", "reach"]

# Métricas onde aumento é NEGATIVO (menos = melhor — custos)
NEGATIVE_DIRECTION = ["cost_per_lead", "cpm", "cpc_link", "frequency", "spend"]


def classify_trend(recent: float, baseline: float, metric: str) -> str:
    """
    Classifica a direção da tendência comparando dois valores.
    recent: valor da janela curta (ex: 3d)
    baseline: valor da janela longa (ex: 7d)
    """
    if baseline == 0 or recent == 0:
        return "[ ] sem dados"

    delta = (recent - baseline) / baseline

    if metric in POSITIVE_DIRECTION:
        if delta > 0.10:
            return "↑ Alta"
        if delta < -0.10:
            return "↓ Queda"
        return "→ Estável"
    elif metric in NEGATIVE_DIRECTION:
        if delta > 0.10:
            return "↑ Subindo [AVISO]"
        if delta < -0.10:
            return "↓ Caindo ✓"
        return "→ Estável"
    else:
        if delta > 0.10:
            return "↑ Alta"
        if delta < -0.10:
            return "↓ Queda"
        return "→ Estável"


# ============================================================
# Cálculo de tendências para uma entidade
# ============================================================

def calculate_trends(entity_id: str, entity_type: str, account_key: str) -> dict:
    """
    Retorna dict com as métricas agregadas por janela + classificação de tendência.

    Exemplo de retorno:
    {
      "cost_per_lead": {
        "3d": 8.50, "7d": 10.20, "15d": 11.00, "30d": 12.30,
        "trend_recente": "↓ Caindo ✓",
        "trend_estrutural": "↓ Caindo ✓",
        "dados_suficientes": True
      },
      ...
    }
    """
    conn = get_connection()
    results = {}

    all_metrics = SUM_METRICS + AVG_METRICS

    for metric in all_metrics:
        agg_func = "SUM" if metric in SUM_METRICS else "AVG"
        windows = {}

        for days in TREND_WINDOWS:
            row = conn.execute(
                f"""SELECT {agg_func}({metric}) as val
                    FROM insights
                    WHERE entity_id=? AND entity_type=? AND account_key=?
                    AND date >= date('now', '-{days} days')
                    AND date < date('now')""",
                [entity_id, entity_type, account_key],
            ).fetchone()
            windows[f"{days}d"] = round(float(row["val"] or 0), 4)

        results[metric] = {
            **windows,
            "trend_recente":     classify_trend(windows["3d"],  windows["7d"],  metric),
            "trend_estrutural":  classify_trend(windows["7d"],  windows["30d"], metric),
            "dados_suficientes": windows["7d"] > 0,
        }

    conn.close()
    return results


# ============================================================
# Cálculo de tendências para múltiplas entidades (batch local)
# ============================================================

def calculate_trends_batch(entities: list, entity_type: str, account_key: str) -> dict:
    """
    Recebe lista de dicts com 'id' e 'name'. Retorna dict {entity_id: trends_dict}.
    Mais eficiente que chamar calculate_trends individualmente.
    """
    return {
        e["id"]: calculate_trends(e["id"], entity_type, account_key)
        for e in entities
    }


# ============================================================
# Formatação para relatório
# ============================================================

def format_trends_table(trends: dict, currency_symbol: str = "R$") -> str:
    """
    Gera tabela Markdown de tendências para uma entidade.

    | Métrica    | 30d | 15d | 7d | 3d | Tend. Recente | Tend. Estrutural |
    """
    headers = ["Métrica", "30d", "15d", "7d", "3d", "Tend. Recente", "Tend. Estrutural"]
    rows = []

    METRIC_LABELS = {
        "spend":               f"Investido ({currency_symbol})",
        "impressions":         "Impressões",
        "reach":               "Alcance",
        "link_clicks":         "Cliques no Link",
        "leads":               "Leads",
        "ctr_link":            "CTR Link (%)",
        "cpm":                 f"CPM ({currency_symbol})",
        "cpc_link":            f"CPC Link ({currency_symbol})",
        "cost_per_lead":       f"CpL ({currency_symbol})",
        "frequency":           "Frequência",
        "lp_conversion_rate":  "Conv. LP (%)",
    }

    for metric, data in trends.items():
        if not data.get("dados_suficientes"):
            continue
        label = METRIC_LABELS.get(metric, metric)
        row = [
            label,
            data["30d"],
            data["15d"],
            data["7d"],
            data["3d"],
            data["trend_recente"],
            data["trend_estrutural"],
        ]
        rows.append(row)

    if not rows:
        return "_Dados insuficientes para análise de tendências (menos de 7 dias de dados)._\n"

    # Monta tabela Markdown manualmente
    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    data_lines = [
        "| " + " | ".join(str(v) for v in row) + " |"
        for row in rows
    ]
    return "\n".join([header_line, sep_line] + data_lines) + "\n"
