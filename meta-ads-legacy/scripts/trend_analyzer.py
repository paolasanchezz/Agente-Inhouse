"""
trend_analyzer.py — Análise de tendências temporais por janelas de 7/15/30 dias.

Todos os cálculos são feitos localmente no SQLite. Zero chamadas à API.

Métricas derivadas (CpL, CTR, CPM, CPC, Conv. LP) são calculadas a partir das
somas brutas de cada janela — nunca como média de médias diárias.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cache_manager import get_connection

# ============================================================
# Configuração das janelas
# ============================================================

TREND_WINDOWS = [7, 15, 30]  # dias — do mais recente ao mais longo

# Métricas base somadas diretamente do banco
BASE_METRICS = ["spend", "impressions", "link_clicks", "leads", "reach",
                "video_p25", "video_p50", "video_p100"]

# Métricas derivadas calculadas a partir das somas brutas (nunca AVG de médias)
# Cada lambda recebe o dict {metric: valor} da janela e retorna o valor derivado
DERIVED_METRICS = {
    "cost_per_lead":      lambda d: d["spend"] / d["leads"]      if d["leads"] > 0       else 0.0,
    "ctr_link":           lambda d: d["link_clicks"] / d["impressions"] * 100 if d["impressions"] > 0 else 0.0,
    "cpm":                lambda d: d["spend"] / d["impressions"] * 1000      if d["impressions"] > 0 else 0.0,
    "cpc_link":           lambda d: d["spend"] / d["link_clicks"]             if d["link_clicks"] > 0 else 0.0,
    "lp_conversion_rate": lambda d: d["leads"] / d["link_clicks"] * 100      if d["link_clicks"] > 0 else 0.0,
    "frequency":          lambda d: d["impressions"] / d["reach"]             if d["reach"] > 0       else 0.0,
    # Vídeo: hook_rate = % que assistiu 25%+ do vídeo (mede força do gancho)
    "hook_rate":          lambda d: d["video_p25"] / d["impressions"] * 100  if d["impressions"] > 0 and d["video_p25"] > 0 else 0.0,
    # Vídeo: completion_rate = % que assistiu até o fim
    "completion_rate":    lambda d: d["video_p100"] / d["impressions"] * 100 if d["impressions"] > 0 and d["video_p100"] > 0 else 0.0,
}

# Direção positiva: aumento é BOM
POSITIVE_DIRECTION = ["leads", "link_clicks", "ctr_link", "lp_conversion_rate",
                      "impressions", "reach", "hook_rate", "completion_rate"]

# Direção negativa: aumento é RUIM (custos)
NEGATIVE_DIRECTION = ["cost_per_lead", "cpm", "cpc_link", "frequency", "spend"]

# Limiar de variação para classificar como tendência (10%)
TREND_THRESHOLD = 0.10


def classify_trend(recent: float, baseline: float, metric: str) -> str:
    """
    Classifica a direção da tendência comparando dois valores.
    recent: janela mais curta (ex: 7d)
    baseline: janela mais longa (ex: 15d ou 30d)
    """
    if baseline == 0 or recent == 0:
        return "[ ] sem dados"

    delta = (recent - baseline) / baseline

    if metric in POSITIVE_DIRECTION:
        if delta > TREND_THRESHOLD:
            return "↑ Alta"
        if delta < -TREND_THRESHOLD:
            return "↓ Queda"
        return "→ Estável"
    elif metric in NEGATIVE_DIRECTION:
        if delta > TREND_THRESHOLD:
            return "↑ Subindo [AVISO]"
        if delta < -TREND_THRESHOLD:
            return "↓ Caindo ✓"
        return "→ Estável"
    else:
        if delta > TREND_THRESHOLD:
            return "↑ Alta"
        if delta < -TREND_THRESHOLD:
            return "↓ Queda"
        return "→ Estável"


# ============================================================
# Cálculo de tendências para uma entidade
# ============================================================

def calculate_trends(entity_id: str, entity_type: str, account_key: str) -> dict:
    """
    Retorna dict com as métricas agregadas por janela + classificação de tendência.

    Janelas: 7d / 15d / 30d
    Tend. Recente: compara 7d vs 15d
    Tend. Estrutural: compara 15d vs 30d

    CpL, CTR, CPM, CPC e Conv. LP são calculados como SUM(numerador)/SUM(denominador)
    por janela — nunca como AVG de valores diários.

    Exemplo de retorno:
    {
      "cost_per_lead": {
        "7d": 210.50, "15d": 280.00, "30d": 334.59,
        "trend_recente": "↓ Caindo ✓",
        "trend_estrutural": "↓ Caindo ✓",
        "dados_suficientes": True
      },
      ...
    }
    """
    conn = get_connection()

    # Passo 1: somar métricas base por janela
    base_by_window = {}
    for days in TREND_WINDOWS:
        sums = {}
        for metric in BASE_METRICS:
            row = conn.execute(
                f"""SELECT SUM({metric}) as val
                    FROM insights
                    WHERE entity_id=? AND entity_type=? AND account_key=?
                    AND date >= date('now', '-{days} days')
                    AND date < date('now')""",
                [entity_id, entity_type, account_key],
            ).fetchone()
            sums[metric] = float(row["val"] or 0)
        base_by_window[days] = sums

    conn.close()

    # Passo 2: calcular métricas derivadas por janela
    results = {}

    all_metrics = BASE_METRICS + list(DERIVED_METRICS.keys())
    for metric in all_metrics:
        windows = {}
        for days in TREND_WINDOWS:
            base = base_by_window[days]
            if metric in BASE_METRICS:
                windows[f"{days}d"] = round(base[metric], 4)
            else:
                windows[f"{days}d"] = round(DERIVED_METRICS[metric](base), 4)

        # Tend. Recente: 7d vs 15d | Tend. Estrutural: 15d vs 30d
        results[metric] = {
            **windows,
            "trend_recente":     classify_trend(windows["7d"],  windows["15d"], metric),
            "trend_estrutural":  classify_trend(windows["15d"], windows["30d"], metric),
            "dados_suficientes": windows["7d"] > 0,
        }

    return results


# ============================================================
# Cálculo de tendências para múltiplas entidades (batch local)
# ============================================================

def calculate_trends_batch(entities: list, entity_type: str, account_key: str) -> dict:
    """
    Recebe lista de dicts com 'id' e 'name'. Retorna dict {entity_id: trends_dict}.
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

    | Métrica | 30d | 15d | 7d | Tend. Recente | Tend. Estrutural |
    Tend. Recente = 7d vs 15d | Tend. Estrutural = 15d vs 30d
    """
    headers = ["Métrica", "30d", "15d", "7d", "Tend. Recente (7d vs 15d)", "Tend. Estrutural (15d vs 30d)"]
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
        "hook_rate":           "Hook Rate — % assistiu 25%+ (vídeo)",
        "completion_rate":     "Completion Rate — % assistiu até o fim (vídeo)",
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
            data["trend_recente"],
            data["trend_estrutural"],
        ]
        rows.append(row)

    if not rows:
        return "_Dados insuficientes para análise de tendências (menos de 7 dias de dados)._\n"

    header_line = "| " + " | ".join(headers) + " |"
    sep_line    = "| " + " | ".join(["---"] * len(headers)) + " |"
    data_lines  = ["| " + " | ".join(str(v) for v in row) + " |" for row in rows]
    return "\n".join([header_line, sep_line] + data_lines) + "\n"
