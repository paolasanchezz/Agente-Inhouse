"""
report_generator.py — Geração de relatório Markdown completo de Meta Ads.

Zero chamadas à API — apenas leitura do banco SQLite e geração de texto.
Saída: data/reports/YYYY-MM-DD_{account_key}_{period}.md
"""

import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cache_manager import ACCOUNTS, get_campaigns, get_adsets, get_ads, get_insights
from benchmark_checker import (
    aggregate_metrics_for_period,
    check_entity_benchmarks,
    summarize_funnel_group,
)
from trend_analyzer import calculate_trends, format_trends_table

REPORTS_DIR = Path(__file__).parent.parent / "data" / "reports"


# ============================================================
# Formatação de valores monetários
# ============================================================

def fmt_currency(value: float, symbol: str) -> str:
    return f"{symbol} {value:,.2f}"


def fmt_pct(value: float) -> str:
    return f"{value:.2f}%"


def fmt_int(value) -> str:
    return f"{int(value):,}"


# ============================================================
# Tabela de métricas por entidade
# ============================================================

def build_metrics_table(entities: list, entity_type: str, account_key: str,
                         date_start: str, date_end: str, symbol: str,
                         campaign_type_map: dict = None) -> str:
    """
    Gera tabela Markdown com métricas agregadas para uma lista de entidades.
    campaign_type_map: {entity_id: campaign_type} — para classificação de benchmarks.
    """
    headers = [
        "Nome", f"Investido ({symbol})", "Impressões", "Cliques",
        "CTR", f"CPM ({symbol})", "Leads", f"CpL ({symbol})",
        "Freq.", "Conv. LP", "Status CpL", "Status CTR", "Status Conv.LP",
    ]
    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    rows = []

    for entity in entities:
        m = aggregate_metrics_for_period(
            entity["id"], entity_type, account_key, date_start, date_end
        )
        if not m or m.get("spend", 0) == 0:
            continue

        ctype = "nao_classificada"
        if campaign_type_map:
            ctype = campaign_type_map.get(entity["id"], "nao_classificada")

        statuses = check_entity_benchmarks(m, account_key, ctype)

        leads_str = fmt_int(m.get("leads", 0)) if m.get("leads", 0) > 0 else "—"
        cpl_str = fmt_currency(m.get("cost_per_lead", 0), symbol) if m.get("leads", 0) > 0 else "—"
        conv_str = fmt_pct(m.get("lp_conversion_rate", 0)) if m.get("leads", 0) > 0 else "—"

        row = [
            entity["name"][:45],
            fmt_currency(m.get("spend", 0), symbol),
            fmt_int(m.get("impressions", 0)),
            fmt_int(m.get("link_clicks", 0)),
            fmt_pct(m.get("ctr_link", 0)),
            fmt_currency(m.get("cpm", 0), symbol),
            leads_str,
            cpl_str,
            f"{m.get('frequency', 0):.2f}",
            conv_str,
            statuses.get("cost_per_lead", "[ ]"),
            statuses.get("ctr_link", "[ ]"),
            statuses.get("lp_conversion_rate", "[ ]"),
        ]
        rows.append(row)

    if not rows:
        return "_Sem dados no período selecionado._\n"

    data_lines = ["| " + " | ".join(str(v) for v in row) + " |" for row in rows]
    return "\n".join([header_line, sep_line] + data_lines) + "\n"


# ============================================================
# Tabela dia a dia
# ============================================================

def build_daily_table(entity_id: str, entity_type: str, account_key: str,
                       date_start: str, date_end: str, symbol: str) -> str:
    rows_data = get_insights(entity_id, entity_type, account_key, date_start, date_end)
    if not rows_data:
        return "_Sem dados diários no período._\n"

    headers = [
        "Data", f"Investido ({symbol})", "Impressões", "Cliques",
        "CTR", f"CPM ({symbol})", "Leads", f"CpL ({symbol})", "Freq.", "Conv. LP",
    ]
    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "| " + " | ".join(["---"] * len(headers)) + " |"

    lines = []
    totals = {"spend": 0, "impressions": 0, "link_clicks": 0, "leads": 0}
    avgs = {"ctr_link": [], "cpm": [], "frequency": []}

    for r in rows_data:
        leads_str = str(int(r["leads"])) if r["leads"] > 0 else "—"
        cpl_str = fmt_currency(r["cost_per_lead"], symbol) if r["leads"] > 0 else "—"
        conv_str = fmt_pct(r["lp_conversion_rate"]) if r["leads"] > 0 else "—"
        line = [
            r["date"],
            fmt_currency(r["spend"], symbol),
            fmt_int(r["impressions"]),
            fmt_int(r["link_clicks"]),
            fmt_pct(r["ctr_link"]),
            fmt_currency(r["cpm"], symbol),
            leads_str,
            cpl_str,
            f"{r['frequency']:.2f}",
            conv_str,
        ]
        lines.append("| " + " | ".join(str(v) for v in line) + " |")

        totals["spend"] += r["spend"]
        totals["impressions"] += r["impressions"]
        totals["link_clicks"] += r["link_clicks"]
        totals["leads"] += r["leads"]
        if r["ctr_link"] > 0: avgs["ctr_link"].append(r["ctr_link"])
        if r["cpm"] > 0: avgs["cpm"].append(r["cpm"])
        if r["frequency"] > 0: avgs["frequency"].append(r["frequency"])

    # Linha de totais/médias
    total_leads = int(totals["leads"])
    total_spend = totals["spend"]
    total_clicks = int(totals["link_clicks"])

    cpl_total = fmt_currency(total_spend / total_leads, symbol) if total_leads > 0 else "—"
    conv_total = fmt_pct((total_leads / total_clicks) * 100) if total_clicks > 0 else "—"
    ctr_avg = sum(avgs["ctr_link"]) / len(avgs["ctr_link"]) if avgs["ctr_link"] else 0
    cpm_avg = sum(avgs["cpm"]) / len(avgs["cpm"]) if avgs["cpm"] else 0
    freq_avg = sum(avgs["frequency"]) / len(avgs["frequency"]) if avgs["frequency"] else 0

    total_row = [
        "**TOTAL/MÉDIA**",
        fmt_currency(total_spend, symbol),
        fmt_int(totals["impressions"]),
        fmt_int(total_clicks),
        fmt_pct(ctr_avg),
        fmt_currency(cpm_avg, symbol),
        str(total_leads) if total_leads > 0 else "—",
        cpl_total,
        f"{freq_avg:.2f}",
        conv_total,
    ]
    lines.append("| " + " | ".join(str(v) for v in total_row) + " |")

    return "\n".join([header_line, sep_line] + lines) + "\n"


# ============================================================
# Visão geral
# ============================================================

def build_overview_section(all_campaigns: list, account_key: str,
                             date_start: str, date_end: str, symbol: str) -> str:
    totals = {"spend": 0, "impressions": 0, "link_clicks": 0, "leads": 0}
    ctr_vals, cpl_vals, conv_vals = [], [], []

    for camp in all_campaigns:
        m = aggregate_metrics_for_period(camp["id"], "campaign", account_key, date_start, date_end)
        if not m:
            continue
        totals["spend"] += m.get("spend", 0)
        totals["impressions"] += m.get("impressions", 0)
        totals["link_clicks"] += m.get("link_clicks", 0)
        totals["leads"] += m.get("leads", 0)
        if m.get("ctr_link", 0) > 0: ctr_vals.append(m["ctr_link"])
        if m.get("cost_per_lead", 0) > 0: cpl_vals.append(m["cost_per_lead"])
        if m.get("lp_conversion_rate", 0) > 0: conv_vals.append(m["lp_conversion_rate"])

    leads = int(totals["leads"])
    spend = totals["spend"]
    clicks = int(totals["link_clicks"])

    cpl_avg = spend / leads if leads > 0 else 0
    ctr_avg = sum(ctr_vals) / len(ctr_vals) if ctr_vals else 0
    conv_avg = sum(conv_vals) / len(conv_vals) if conv_vals else 0

    lines = [
        "| Métrica | Valor |",
        "| --- | --- |",
        f"| Total Investido | {fmt_currency(spend, symbol)} |",
        f"| Impressões | {fmt_int(totals['impressions'])} |",
        f"| Cliques no Link | {fmt_int(clicks)} |",
        f"| Leads | {fmt_int(leads) if leads > 0 else '—'} |",
        f"| CpL Médio | {fmt_currency(cpl_avg, symbol) if leads > 0 else '—'} |",
        f"| CTR Médio | {fmt_pct(ctr_avg)} |",
        f"| Conv. LP Média | {fmt_pct(conv_avg) if conv_avg > 0 else '—'} |",
    ]
    return "\n".join(lines) + "\n"


# ============================================================
# Geração do relatório completo
# ============================================================

def generate_report(account_key: str, period_mode: str,
                     date_start: str, date_end: str) -> Path:
    account = ACCOUNTS[account_key]
    symbol = account["currency_symbol"]
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    campaigns = get_campaigns(account_key)
    if not campaigns:
        raise RuntimeError(f"Nenhuma campanha encontrada para {account_key}. Execute fetch_campaigns.py primeiro.")

    # Separa por grupo de funil
    topo = [c for c in campaigns if c["funnel_group"] == "topo"]
    fundo = [c for c in campaigns if c["funnel_group"] == "fundo"]
    nao_classificadas = [c for c in campaigns if c["funnel_group"] == "nao_classificado"]

    sections = []

    # ── Cabeçalho ──────────────────────────────────────────────
    sections.append(f"# Relatório Meta Ads — {account['label']} — {period_mode}")
    sections.append(f"**Período:** {date_start} → {date_end}  \n**Gerado em:** {now_str}\n")
    sections.append("---\n")

    # ── Visão Geral ─────────────────────────────────────────────
    sections.append("## Visão Geral\n")
    sections.append(build_overview_section(campaigns, account_key, date_start, date_end, symbol))
    sections.append("\n---\n")

    # ── Função auxiliar por grupo ───────────────────────────────
    def render_funnel_group(group_campaigns: list, group_label: str) -> list:
        if not group_campaigns:
            return []
        group_sections = [f"## {group_label}\n"]

        # Mapa campaign_id → campaign_type para benchmarks de adsets/ads
        ctype_map = {c["id"]: c["campaign_type"] for c in group_campaigns}

        # Nível campanha
        group_sections.append("### Por Campanha\n")
        group_sections.append(
            build_metrics_table(group_campaigns, "campaign", account_key,
                                date_start, date_end, symbol, ctype_map)
        )

        # Nível adset
        group_sections.append("\n### Por Conjunto de Anúncios\n")
        all_adsets = []
        adset_ctype_map = {}
        for camp in group_campaigns:
            adsets = get_adsets(camp["id"])
            all_adsets.extend(adsets)
            for a in adsets:
                adset_ctype_map[a["id"]] = camp["campaign_type"]
        group_sections.append(
            build_metrics_table(all_adsets, "adset", account_key,
                                date_start, date_end, symbol, adset_ctype_map)
        )

        # Nível anúncio
        group_sections.append("\n### Por Anúncio\n")
        all_ads = []
        ad_ctype_map = {}
        for adset in all_adsets:
            ads = get_ads(adset["id"])
            all_ads.extend(ads)
            for a in ads:
                ad_ctype_map[a["id"]] = adset_ctype_map.get(adset["id"], "nao_classificada")
        group_sections.append(
            build_metrics_table(all_ads, "ad", account_key,
                                date_start, date_end, symbol, ad_ctype_map)
        )

        # Dia a dia — agregado do grupo
        group_sections.append("\n### Dia a Dia — Agregado do Grupo\n")
        group_sections.append("_Dados diários por campanha estão disponíveis no banco. Consulte via `/meta-ads-report` com campanha específica._\n")

        group_sections.append("\n---\n")
        return group_sections

    sections.extend(render_funnel_group(topo,  ">> Topo de Funil"))
    sections.extend(render_funnel_group(fundo, "[RUIM] Fundo de Funil"))

    # ── Não classificadas ───────────────────────────────────────
    if nao_classificadas:
        sections.append("## [ ] Campanhas Não Classificadas\n")
        sections.append("> [AVISO] Classificação manual necessária — estas campanhas não foram identificadas como Webinar, Material Rico ou Remarketing.\n")
        for c in nao_classificadas:
            sections.append(f"- **{c['name']}** (ID: `{c['id']}`)")
        sections.append("\n---\n")

    # ── Tendências ──────────────────────────────────────────────
    sections.append("## >> Análise de Tendências\n")
    sections.append("_Janelas: 3d / 7d / 15d / 30d. Calculado a partir do banco local, sem chamadas à API._\n")

    active_campaigns = [c for c in campaigns if c.get("status") == "ACTIVE"]
    if not active_campaigns:
        sections.append("_Nenhuma campanha ativa encontrada._\n")
    else:
        for camp in active_campaigns[:10]:  # limita a 10 para não inflar o relatório
            sections.append(f"\n#### {camp['name']}\n")
            trends = calculate_trends(camp["id"], "campaign", account_key)
            sections.append(format_trends_table(trends, symbol))

    sections.append("\n---\n")

    # ── Pontos Fortes ───────────────────────────────────────────
    sections.append("## ++ Pontos Fortes\n")
    sections.append("_Preencher após análise dos dados acima. Citar nome específico de campanha/conjunto/anúncio + dado que justifica._\n")
    sections.append("1. \n2. \n3. \n\n---\n")

    # ── Pontos de Atenção ───────────────────────────────────────
    sections.append("## [RUIM] Pontos de Atenção\n")
    sections.append("_Para cada ponto: o que está fora | onde | impacto estimado._\n")
    sections.append("1. \n2. \n3. \n\n---\n")

    # ── Sugestões de Ação ───────────────────────────────────────
    sections.append("## >> Sugestões de Ação\n")
    sections.append(
        "**Ação:** [o que fazer]  \n"
        "**Onde:** [campanha/conjunto/anúncio — nome exato]  \n"
        "**Por quê:** [dado específico que justifica]  \n"
        "**Prioridade:** Alta / Média / Baixa\n"
    )

    # ── Salvar relatório ────────────────────────────────────────
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{datetime.date.today().isoformat()}_{account_key}_{period_mode}.md"
    output_path = REPORTS_DIR / filename

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sections))

    print(f"[OK] Relatório salvo: {output_path}")
    return output_path
