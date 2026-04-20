"""
full_trends_report.py — Relatório consolidado de tendências para as 6 contas.

Hierarquia: Conta → Etapa do Funil (Topo / Fundo / Não classificada) → Adset → Ad.
Zero chamadas à API — lê apenas o SQLite local.

Rodar após fetch_insights.py nas 6 contas com --include-ads.
"""

import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cache_manager import (
    ACCOUNTS,
    get_adsets,
    get_ads,
    get_campaigns,
    get_connection,
)
from trend_analyzer import calculate_trends, format_trends_table

# ============================================================
# Filtros de relevância
# ============================================================

ADSET_MIN_SPEND_30D = 0.01
AD_MIN_SPEND_30D = 0.01
AD_MIN_LEADS_30D = 1
AD_MIN_IMPRESSIONS_30D = 1000

FUNNEL_ORDER = [("topo", ">> Topo de Funil"),
                ("fundo", ">> Fundo de Funil"),
                ("nao_classificado", ">> Não Classificadas")]

# Mapeamento cenários do diagnóstico cruzado (matriz da /meta-ads-trends)
SCENARIO_OURO = "🏆 Ouro"
SCENARIO_FILTRO = "🔵 Filtro natural"
SCENARIO_GARGALO_LP = "⚠️ Gargalo de LP"
SCENARIO_PROMESSA = "🚨 Promessa × entrega"
SCENARIO_POTENCIAL = "🔄 Potencial travado"
SCENARIO_SUBSTITUIR = "💀 Substituir"
SCENARIO_SEM_DADOS = "❓ Sem dados"


# ============================================================
# Helpers de dados
# ============================================================

def _sum_window(entity_id: str, entity_type: str, account_key: str, days: int) -> dict:
    """Soma métricas base em uma janela de N dias (até ontem)."""
    conn = get_connection()
    row = conn.execute(
        f"""SELECT
              COALESCE(SUM(spend), 0)       as spend,
              COALESCE(SUM(impressions), 0) as impressions,
              COALESCE(SUM(link_clicks), 0) as link_clicks,
              COALESCE(SUM(leads), 0)       as leads,
              COALESCE(SUM(reach), 0)       as reach
            FROM insights
            WHERE entity_id = ? AND entity_type = ? AND account_key = ?
              AND date >= date('now', '-{days} days')
              AND date < date('now')""",
        [entity_id, entity_type, account_key],
    ).fetchone()
    conn.close()
    return dict(row) if row else {"spend": 0, "impressions": 0, "link_clicks": 0, "leads": 0, "reach": 0}


def _classify_scenario(trends: dict, benchmarks: dict, currency: str) -> str:
    """Aplica a matriz CpL × CTR × Conv.LP da /meta-ads-trends.

    benchmarks: dict com chaves cost_per_lead_bom, cost_per_lead_ruim,
                ctr_link_bom, ctr_link_ruim, lp_conversion_rate_bom,
                lp_conversion_rate_ruim. Opcionais.
    """
    cpl_30 = trends.get("cost_per_lead", {}).get("30d", 0)
    ctr_30 = trends.get("ctr_link", {}).get("30d", 0)
    conv_30 = trends.get("lp_conversion_rate", {}).get("30d", 0)
    leads_7d = trends.get("leads", {}).get("7d", 0)
    cpl_trend = trends.get("cost_per_lead", {}).get("trend_recente", "")

    if leads_7d <= 2 and cpl_30 == 0:
        return SCENARIO_SEM_DADOS

    # Limiares: usa benchmarks se disponíveis, senão usa heurística simples
    cpl_bom_max = benchmarks.get("cost_per_lead_bom", 0)
    cpl_ruim_min = benchmarks.get("cost_per_lead_ruim", 0)
    ctr_bom_min = benchmarks.get("ctr_link_bom", 1.0)
    ctr_ruim_max = benchmarks.get("ctr_link_ruim", 0.5)
    conv_bom_min = benchmarks.get("lp_conversion_rate_bom", 15.0)
    conv_ruim_max = benchmarks.get("lp_conversion_rate_ruim", 5.0)

    cpl_is_bom = cpl_bom_max > 0 and cpl_30 > 0 and cpl_30 <= cpl_bom_max
    cpl_is_ruim = cpl_ruim_min > 0 and cpl_30 >= cpl_ruim_min
    ctr_is_bom = ctr_30 >= ctr_bom_min
    ctr_is_ruim = ctr_30 > 0 and ctr_30 <= ctr_ruim_max
    conv_is_bom = conv_30 >= conv_bom_min
    conv_is_ruim = conv_30 > 0 and conv_30 <= conv_ruim_max

    if cpl_is_bom and "Caindo" in cpl_trend and ctr_is_bom and conv_is_bom:
        return SCENARIO_OURO
    if cpl_is_bom and ctr_is_ruim and conv_is_bom:
        return SCENARIO_FILTRO
    if cpl_is_bom and ctr_is_bom and conv_is_ruim:
        return SCENARIO_GARGALO_LP
    if cpl_is_ruim and ctr_is_bom and conv_is_ruim:
        return SCENARIO_PROMESSA
    if cpl_is_ruim and ctr_is_bom and conv_is_bom:
        return SCENARIO_POTENCIAL
    if cpl_is_ruim and ctr_is_ruim and (conv_is_ruim or conv_30 == 0):
        return SCENARIO_SUBSTITUIR
    return SCENARIO_SEM_DADOS


def _benchmarks_for(group: str, campaign_type: str) -> dict:
    """Extrai thresholds de bom/ruim para um grupo de moeda + tipo de campanha.

    Formato do benchmarks.json:
      { "brl": { "webinar": { "cost_per_lead": {"bom": {"max": 12.0},
                                                 "aceitavel": {"max": 18.0}}, ... } } }

    Retorna dict flat:
      { "cost_per_lead_bom": 12.0, "cost_per_lead_ruim": 18.0,
        "ctr_link_bom": 1.5, "ctr_link_ruim": 1.0, ... }

    "bom" usa max (para cost) ou min (para ctr/conv).
    "ruim" usa o limite do "aceitavel" (acima/abaixo dele é ruim).
    """
    try:
        from cache_manager import load_benchmarks
        all_bench = load_benchmarks()
    except Exception:
        return {}

    # Mapear webinar/material_rico/remarketing/evento_presencial
    group_data = all_bench.get(group, {})
    # evento_presencial cai em webinar se não houver bloco próprio
    type_key = campaign_type if campaign_type in group_data else "webinar"
    type_data = group_data.get(type_key, {})

    flat = {}
    for metric, levels in type_data.items():
        bom = levels.get("bom", {})
        aceit = levels.get("aceitavel", {})
        # cost_per_lead: bom=max menor, ruim=acima do aceitavel.max
        if "max" in bom:
            flat[f"{metric}_bom"] = bom["max"]
        if "max" in aceit:
            flat[f"{metric}_ruim"] = aceit["max"]
        # ctr/conv: bom=min maior, ruim=abaixo do aceitavel.min
        if "min" in bom:
            flat[f"{metric}_bom"] = bom["min"]
        if "min" in aceit:
            flat[f"{metric}_ruim"] = aceit["min"]
    return flat


# ============================================================
# Geração do relatório
# ============================================================

def render_ad_block(ad: dict, account_key: str, currency_symbol: str, indent: str) -> str:
    """Bloco de um anúncio. indent = nível de header (###### por padrão)."""
    trends = calculate_trends(ad["id"], "ad", account_key)
    lines = [f"{indent} Ad: {ad['name']}"]
    table = format_trends_table(trends, currency_symbol).strip()
    lines.append(table if table else "_Sem tendência — dados insuficientes._")
    lines.append("")
    return "\n".join(lines)


def render_adset_block(adset: dict, account_key: str, currency_symbol: str,
                       adset_indent: str, ad_indent: str) -> tuple[str, int, int]:
    """Bloco de um adset + seus ads relevantes.

    Retorna (markdown, n_ads_exibidos, n_ads_omitidos).
    """
    trends = calculate_trends(adset["id"], "adset", account_key)
    lines = [f"{adset_indent} Adset: {adset['name']}"]
    if adset.get("status"):
        lines.append(f"_Status: {adset['status']}_\n")
    table = format_trends_table(trends, currency_symbol).strip()
    lines.append(table if table else "_Sem tendência — dados insuficientes._")
    lines.append("")

    ads = get_ads(adset["id"])
    ads_relevantes = []
    omitidos = 0
    for ad in ads:
        win = _sum_window(ad["id"], "ad", account_key, 30)
        if win["spend"] < AD_MIN_SPEND_30D:
            omitidos += 1
            continue
        if win["leads"] < AD_MIN_LEADS_30D and win["impressions"] < AD_MIN_IMPRESSIONS_30D:
            omitidos += 1
            continue
        ads_relevantes.append(ad)

    for ad in ads_relevantes:
        lines.append(render_ad_block(ad, account_key, currency_symbol, ad_indent))

    if omitidos:
        lines.append(f"_{omitidos} ad(s) deste adset omitido(s) — dados insuficientes (spend=0 ou <1 lead e <1000 impressões em 30d)._\n")

    return "\n".join(lines), len(ads_relevantes), omitidos


def render_campaign_block(campaign: dict, account_key: str, currency_symbol: str,
                          benchmark_group: str) -> tuple[str, dict]:
    """Bloco de uma campanha + adsets + ads. Retorna (markdown, stats)."""
    trends = calculate_trends(campaign["id"], "campaign", account_key)
    tipo = campaign.get("campaign_type") or "—"
    benchmarks = _benchmarks_for(benchmark_group, tipo)

    lines = [f"#### Campanha: {campaign['name']}  _[tipo: {tipo}]_"]
    table = format_trends_table(trends, currency_symbol).strip()
    lines.append(table if table else "_Sem tendência — dados insuficientes._")
    lines.append("")

    total_ads_exibidos = 0
    total_ads_omitidos = 0
    adsets = get_adsets(campaign["id"])
    adsets_relevantes = []
    adsets_omitidos = 0

    for adset in adsets:
        win = _sum_window(adset["id"], "adset", account_key, 30)
        if win["spend"] < ADSET_MIN_SPEND_30D:
            adsets_omitidos += 1
            continue
        adsets_relevantes.append(adset)

    for adset in adsets_relevantes:
        block, n_ads, n_omit = render_adset_block(
            adset, account_key, currency_symbol, "#####", "######"
        )
        lines.append(block)
        total_ads_exibidos += n_ads
        total_ads_omitidos += n_omit

    if adsets_omitidos:
        lines.append(f"_{adsets_omitidos} adset(s) desta campanha omitido(s) — sem gasto nos últimos 30d._\n")

    cenario = _classify_scenario(trends, benchmarks, campaign.get("currency", ""))
    cpl_30 = trends.get("cost_per_lead", {}).get("30d", 0)
    spend_30 = trends.get("spend", {}).get("30d", 0)
    leads_30 = trends.get("leads", {}).get("30d", 0)
    ctr_30 = trends.get("ctr_link", {}).get("30d", 0)
    conv_30 = trends.get("lp_conversion_rate", {}).get("30d", 0)

    stats = {
        "name": campaign["name"],
        "tipo": tipo,
        "funnel_group": campaign.get("funnel_group", "nao_classificado"),
        "cenario": cenario,
        "cpl_30d": cpl_30,
        "ctr_30d": ctr_30,
        "conv_30d": conv_30,
        "spend_30d": spend_30,
        "leads_30d": leads_30,
        "cpl_trend_recente": trends.get("cost_per_lead", {}).get("trend_recente", ""),
        "ads_exibidos": total_ads_exibidos,
        "ads_omitidos": total_ads_omitidos,
        "adsets_exibidos": len(adsets_relevantes),
        "adsets_omitidos": adsets_omitidos,
    }

    return "\n".join(lines), stats


def render_funnel_section(funnel_group: str, funnel_title: str,
                          campaigns: list, account_key: str,
                          currency_symbol: str, benchmark_group: str) -> tuple[str, list]:
    """Seção de um grupo de funil (topo, fundo ou não classificado)."""
    filtered = [c for c in campaigns if (c.get("funnel_group") or "nao_classificado") == funnel_group]
    if not filtered:
        return "", []

    lines = [f"### {funnel_title}", ""]
    all_stats = []

    for camp in filtered:
        block, stats = render_campaign_block(camp, account_key, currency_symbol, benchmark_group)
        lines.append(block)
        all_stats.append(stats)

    # Tabela de diagnóstico cruzado
    lines.append(f"#### Diagnóstico — {funnel_title}")
    lines.append("")
    lines.append("| Campanha | CpL 30d | CTR 30d | Conv.LP 30d | Tendência CpL (7 vs 15) | Cenário |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for s in all_stats:
        cpl = f"{currency_symbol} {s['cpl_30d']:.2f}" if s["cpl_30d"] else "—"
        ctr = f"{s['ctr_30d']:.2f}%" if s["ctr_30d"] else "—"
        conv = f"{s['conv_30d']:.2f}%" if s["conv_30d"] else "—"
        trend = s["cpl_trend_recente"] or "—"
        # Truncar nome longo
        nome = s["name"] if len(s["name"]) <= 60 else s["name"][:57] + "..."
        lines.append(f"| {nome} | {cpl} | {ctr} | {conv} | {trend} | {s['cenario']} |")
    lines.append("")

    return "\n".join(lines), all_stats


def render_account_section(account_key: str) -> tuple[str, dict]:
    """Seção completa de uma conta. Retorna (markdown, stats_agregados)."""
    account = ACCOUNTS[account_key]
    currency_symbol = account["currency_symbol"]
    currency = account["currency"]
    label = account["label"]
    benchmark_group = account["benchmark_group"]

    lines = [f"## {label}", ""]

    campaigns = get_campaigns(account_key)
    if not campaigns:
        lines.append("_Sem campanhas no banco para esta conta._\n")
        return "\n".join(lines), {"account_key": account_key, "currency": currency,
                                   "by_funnel": {}, "total_campaigns": 0}

    by_funnel_stats = {}
    for funnel_key, funnel_title in FUNNEL_ORDER:
        block, stats_list = render_funnel_section(
            funnel_key, funnel_title, campaigns, account_key, currency_symbol, benchmark_group
        )
        if block:
            lines.append(block)
            by_funnel_stats[funnel_key] = stats_list

    return "\n".join(lines), {
        "account_key": account_key,
        "currency": currency,
        "currency_symbol": currency_symbol,
        "label": label,
        "by_funnel": by_funnel_stats,
        "total_campaigns": len(campaigns),
    }


def render_executive_summary(all_account_stats: list) -> str:
    """Resumo executivo consolidado — agrega só em % e contagem (nunca soma moedas)."""
    lines = ["## Resumo Executivo", ""]

    # Totais por funil cross-conta
    funnel_counts = {"topo": 0, "fundo": 0, "nao_classificado": 0}
    cenarios_count = {}
    cpl_direction = {"topo": {"Caindo": 0, "Subindo": 0, "Estável": 0, "—": 0},
                     "fundo": {"Caindo": 0, "Subindo": 0, "Estável": 0, "—": 0}}
    spend_by_currency_funnel = {}  # {(currency, funnel): total}

    for acc in all_account_stats:
        currency = acc["currency"]
        for funnel_key, stats_list in acc["by_funnel"].items():
            funnel_counts[funnel_key] = funnel_counts.get(funnel_key, 0) + len(stats_list)
            for s in stats_list:
                cenarios_count[s["cenario"]] = cenarios_count.get(s["cenario"], 0) + 1
                key = (currency, funnel_key)
                spend_by_currency_funnel[key] = spend_by_currency_funnel.get(key, 0) + s["spend_30d"]
                if funnel_key in cpl_direction:
                    if "Caindo" in s["cpl_trend_recente"]:
                        cpl_direction[funnel_key]["Caindo"] += 1
                    elif "Subindo" in s["cpl_trend_recente"]:
                        cpl_direction[funnel_key]["Subindo"] += 1
                    elif "Estável" in s["cpl_trend_recente"]:
                        cpl_direction[funnel_key]["Estável"] += 1
                    else:
                        cpl_direction[funnel_key]["—"] += 1

    # Bloco 1: Contagem por funil
    lines.append("### Contagem de campanhas por etapa do funil")
    lines.append("")
    lines.append("| Funil | Campanhas |")
    lines.append("| --- | --- |")
    lines.append(f"| Topo | {funnel_counts.get('topo', 0)} |")
    lines.append(f"| Fundo | {funnel_counts.get('fundo', 0)} |")
    lines.append(f"| Não classificadas | {funnel_counts.get('nao_classificado', 0)} |")
    lines.append("")

    # Bloco 2: Gasto 30d por moeda × funil
    lines.append("### Investido nos últimos 30 dias (por moeda × funil)")
    lines.append("")
    lines.append("_Valores nunca somados entre moedas diferentes._")
    lines.append("")
    lines.append("| Moeda | Topo | Fundo | Não classificadas |")
    lines.append("| --- | --- | --- | --- |")
    currencies_seen = sorted({c for (c, _) in spend_by_currency_funnel})
    symbol_map = {"BRL": "R$", "USD": "$", "EUR": "€"}
    for c in currencies_seen:
        topo = spend_by_currency_funnel.get((c, "topo"), 0)
        fundo = spend_by_currency_funnel.get((c, "fundo"), 0)
        naoc = spend_by_currency_funnel.get((c, "nao_classificado"), 0)
        sym = symbol_map.get(c, c)
        lines.append(f"| {c} | {sym} {topo:,.2f} | {sym} {fundo:,.2f} | {sym} {naoc:,.2f} |")
    lines.append("")

    # Bloco 3: Direção recente do CpL por funil (% de campanhas)
    lines.append("### Direção recente do CpL (7d vs 15d) — % de campanhas")
    lines.append("")
    lines.append("| Funil | ↓ Caindo (bom) | ↑ Subindo (alerta) | → Estável | — Sem dados |")
    lines.append("| --- | --- | --- | --- | --- |")
    for funnel_key in ["topo", "fundo"]:
        d = cpl_direction[funnel_key]
        total = sum(d.values()) or 1
        lines.append(
            f"| {funnel_key.title()} | "
            f"{d['Caindo']} ({d['Caindo']/total*100:.0f}%) | "
            f"{d['Subindo']} ({d['Subindo']/total*100:.0f}%) | "
            f"{d['Estável']} ({d['Estável']/total*100:.0f}%) | "
            f"{d['—']} ({d['—']/total*100:.0f}%) |"
        )
    lines.append("")

    # Bloco 4: Top cenários
    lines.append("### Distribuição de cenários (todas as contas)")
    lines.append("")
    lines.append("| Cenário | Campanhas |")
    lines.append("| --- | --- |")
    for cen, count in sorted(cenarios_count.items(), key=lambda x: -x[1]):
        lines.append(f"| {cen} | {count} |")
    lines.append("")

    return "\n".join(lines)


def generate_report() -> str:
    """Monta o relatório completo."""
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    generated_at = now.strftime("%Y-%m-%d %H:%M")

    header = [
        f"# Meta Ads — Tendências Gerais — {today}",
        "",
        f"**Período:** últimos 30 dias  ",
        f"**Contas:** 6 (Buzzmonitor BRL/USD/EUR + Cxpress BRL/USD/EUR)  ",
        f"**Gerado em:** {generated_at}",
        "",
        "> Tendência Recente = 7d vs 15d · Tendência Estrutural = 15d vs 30d · Limiar: ±10%.",
        "> Ads com spend=0 ou < 1 lead e < 1000 impressões em 30d são omitidos (contados no rodapé).",
        "",
        "---",
        "",
    ]

    # Renderizar cada conta
    account_sections = []
    all_account_stats = []
    account_order = ["buzzmonitor_brl", "buzzmonitor_usd", "buzzmonitor_eur",
                     "cxpress_brl", "cxpress_usd", "cxpress_eur"]
    for key in account_order:
        section, stats = render_account_section(key)
        account_sections.append(section)
        all_account_stats.append(stats)

    summary = render_executive_summary(all_account_stats)

    parts = header + [summary, "", "---", ""] + account_sections
    return "\n".join(parts)


def generate_notion_summary() -> str:
    """Versão condensada para publicação no Notion.

    Inclui: cabeçalho + Resumo Executivo + tabelas de diagnóstico de cada
    conta (sem as tabelas individuais de trends de cada campaign/adset/ad).
    """
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    generated_at = now.strftime("%Y-%m-%d %H:%M")

    all_stats = []
    account_order = ["buzzmonitor_brl", "buzzmonitor_usd", "buzzmonitor_eur",
                     "cxpress_brl", "cxpress_usd", "cxpress_eur"]
    for key in account_order:
        _, stats = render_account_section(key)
        all_stats.append(stats)

    parts = [
        f"# Meta Ads — Tendências Gerais — {today}",
        "",
        f"**Período:** últimos 30 dias  ",
        f"**Contas:** 6 (Buzzmonitor BRL/USD/EUR + Cxpress BRL/USD/EUR)  ",
        f"**Gerado em:** {generated_at}",
        "",
        "> Tendência Recente = 7d vs 15d · Tendência Estrutural = 15d vs 30d · Limiar: ±10%.",
        "",
        "---",
        "",
        render_executive_summary(all_stats),
        "",
        "---",
        "",
        "# Diagnóstico por Conta × Funil",
        "",
        "As tabelas abaixo listam, por conta e por etapa de funil, cada campanha com seus números "
        "de 30 dias, a direção recente do CpL e o cenário identificado pela matriz CpL × CTR × Conv.LP. "
        "Drill-down por adset e anúncio está no relatório local.",
        "",
    ]

    # Para cada conta: tabela por funil
    for stats in all_stats:
        if stats["total_campaigns"] == 0:
            continue
        label = stats.get("label", stats["account_key"])
        symbol = stats.get("currency_symbol", "")
        parts.append(f"## {label}")
        parts.append("")

        for funnel_key, funnel_title in FUNNEL_ORDER:
            funnel_stats = stats["by_funnel"].get(funnel_key, [])
            if not funnel_stats:
                continue
            parts.append(f"### {funnel_title}")
            parts.append("")
            parts.append("| Campanha | Investido 30d | Leads 30d | CpL 30d | CTR 30d | Conv.LP 30d | Tendência CpL (7 vs 15) | Cenário |")
            parts.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
            for s in funnel_stats:
                nome = s["name"] if len(s["name"]) <= 55 else s["name"][:52] + "..."
                spend = f"{symbol} {s['spend_30d']:,.2f}" if s["spend_30d"] else "—"
                leads = f"{int(s['leads_30d'])}" if s["leads_30d"] else "—"
                cpl = f"{symbol} {s['cpl_30d']:.2f}" if s["cpl_30d"] else "—"
                ctr = f"{s['ctr_30d']:.2f}%" if s["ctr_30d"] else "—"
                conv = f"{s['conv_30d']:.2f}%" if s["conv_30d"] else "—"
                trend = s["cpl_trend_recente"] or "—"
                parts.append(f"| {nome} | {spend} | {leads} | {cpl} | {ctr} | {conv} | {trend} | {s['cenario']} |")
            parts.append("")

    parts.append("---")
    parts.append("")
    parts.append("_Relatório completo com drill-down Conta→Funil→Adset→Ad disponível em_ "
                 f"`meta-ads/data/reports/{today}_geral_todas_contas.md`.")

    return "\n".join(parts)


def main():
    # Windows cp1252 não lida com setas/emojis — forçar UTF-8 no stdout
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    summary_mode = "--summary" in sys.argv

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    reports_dir = Path(__file__).parent.parent / "data" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    if summary_mode:
        out = generate_notion_summary()
        out_path = reports_dir / f"{today}_geral_todas_contas_resumo.md"
    else:
        out = generate_report()
        out_path = reports_dir / f"{today}_geral_todas_contas.md"

    out_path.write_text(out, encoding="utf-8")
    sys.stdout.write(out)
    sys.stdout.flush()
    sys.stderr.write(f"\n\n---\n[OK] Relatório salvo em: {out_path}\n")


if __name__ == "__main__":
    main()
