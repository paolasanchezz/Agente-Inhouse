"""
Stress test: skill (Meta API diaria) vs Bunzzai (snapshots acumulados).
Campanha 124 - Webinar-Analise-Preditiva, 4 ads, ultimos 15 dias.

Janelas:
  7d  = 12/mai a 18/mai  (ultimos 7 dias antes de hoje 19/mai)
  15d = 04/mai a 18/mai  (ultimos 15 dias)

Bunzzai entrega 'investimento_acumulado' por snapshot.
Para reconstituir 'dia X', fazemos: acumulado(X) - acumulado(X-1).
Quando o acumulado nao muda entre dois dias = 0 atividade naquele dia (ad pausado ou cron travado).
"""
import sys, io, json
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, str(Path(__file__).parent))

from cache_manager import get_connection
from trend_analyzer import calculate_trends

# ===== Bunzzai data (extraida do monitoring_history, 1 snapshot por dia) =====
# Cada lista: (data, acum_spend, acum_imp, acum_cliques, acum_conv)
BUNZZAI = {
    445: {  # Voce - adset 365
        "name": "WEB APP - Ad04 - Voce",
        "history": [
            ("2026-04-30", 6.61,   333,    4,  1),  # primeiro snapshot tinha conv=1
            ("2026-05-01", 65.61,  3273,  40,  6),
            ("2026-05-02", 98.45,  5389,  62, 10),
            ("2026-05-03", 130.95, 7440,  77, 11),
            ("2026-05-04", 181.63, 9590, 105, 15),
            ("2026-05-05", 219.49,12339, 154, 25),
            ("2026-05-06", 219.49,12339, 154, 25),  # congelou
            ("2026-05-07", 219.49,12339, 154, 25),
            ("2026-05-08", 219.49,12339, 154, 25),
            ("2026-05-09", 219.49,12339, 154, 25),
            ("2026-05-10", 219.49,12339, 154, 25),
            ("2026-05-11", 219.49,12339, 154, 25),
            ("2026-05-12", 219.49,12339, 154, 25),
            ("2026-05-13", 219.49,12339, 154, 25),
            ("2026-05-14", 219.49,12339, 154, 25),
            ("2026-05-15", 219.49,12339, 154, 25),
            ("2026-05-16", 219.49,12339, 154, 25),
            ("2026-05-17", 219.49,12339, 154, 25),
            ("2026-05-18", 219.49,12339, 154, 25),
            ("2026-05-19", 219.49,12339, 154, 25),
        ],
    },
    446: {  # Cachorro - adset 366
        "name": "WEB APP - Ad03 - Cachorro",
        "history": [
            ("2026-04-30",   5.46,  299,   6,  2),
            ("2026-05-01",  57.16, 3172,  51,  9),
            ("2026-05-02",  91.91, 5011,  73, 12),
            ("2026-05-03", 135.67, 7216, 109, 19),
            ("2026-05-04", 179.15, 8718, 135, 24),
            ("2026-05-05", 212.96, 9923, 156, 25),
            ("2026-05-06", 212.96, 9923, 156, 25),  # congelou
            ("2026-05-07", 212.96, 9923, 156, 25),
            ("2026-05-08", 212.96, 9923, 156, 25),
            ("2026-05-09", 212.96, 9923, 156, 25),
            ("2026-05-10", 212.96, 9923, 156, 25),
            ("2026-05-11", 212.96, 9923, 156, 25),
            ("2026-05-12", 212.96, 9923, 156, 25),
            ("2026-05-13", 212.96, 9923, 156, 25),
            ("2026-05-14", 212.96, 9923, 156, 25),
            ("2026-05-15", 212.96, 9923, 156, 25),
            ("2026-05-16", 212.96, 9923, 156, 25),
            ("2026-05-17", 212.96, 9923, 156, 25),
            ("2026-05-18", 212.96, 9923, 156, 25),
            ("2026-05-19", 212.96, 9923, 156, 25),
        ],
    },
    447: {  # Seu concorrente - adset 367
        "name": "WEB APP - Ad02 - Seu concorrente",
        "history": [
            ("2026-04-30",    5.69,   231,   0,  0),
            ("2026-05-01",   62.94,  2226,  16,  5),
            ("2026-05-02",   98.95,  3416,  27, 10),
            ("2026-05-03",  143.30,  4898,  33, 13),
            ("2026-05-04",  199.88,  6495,  44, 18),
            ("2026-05-05",  273.69,  8820,  69, 23),
            ("2026-05-06",  368.72, 12875, 102, 32),
            ("2026-05-07",  449.57, 16496, 127, 40),
            ("2026-05-08",  534.00, 19333, 150, 47),
            ("2026-05-09",  583.20, 20557, 160, 57),
            ("2026-05-10",  623.93, 21909, 166, 60),
            ("2026-05-11",  679.24, 23335, 178, 65),
            ("2026-05-12",  735.80, 25127, 192, 75),
            ("2026-05-13",  777.86, 26311, 196, 79),
            ("2026-05-14",  830.79, 27622, 207, 90),
            ("2026-05-15",  874.47, 28864, 217, 98),
            ("2026-05-16",  915.76, 30237, 230,107),
            ("2026-05-17",  958.56, 31725, 238,115),
            ("2026-05-18", 1015.98, 33227, 250,122),
            ("2026-05-19", 1065.31, 34701, 259,128),
        ],
    },
    448: {  # Como utilizar - adset 368
        "name": "WEB APP - Ad01 - Como utilizar",
        "history": [
            ("2026-04-30",    7.76,   187,   2,  1),
            ("2026-05-01",   61.97,  2004,  19,  4),
            ("2026-05-02",   98.50,  3343,  31,  5),
            ("2026-05-03",  153.80,  5771,  60, 15),
            ("2026-05-04",  207.96,  8432,  68, 20),
            ("2026-05-05",  274.97, 11653,  90, 29),
            ("2026-05-06",  359.22, 16665, 116, 34),
            ("2026-05-07",  446.72, 21678, 140, 42),
            ("2026-05-08",  535.39, 26731, 184, 52),
            ("2026-05-09",  586.42, 29233, 211, 75),
            ("2026-05-10",  628.91, 31698, 225, 82),
            ("2026-05-11",  681.48, 34940, 250,101),
            ("2026-05-12",  735.33, 38039, 268,113),
            ("2026-05-13",  789.37, 41143, 283,126),
            ("2026-05-14",  840.31, 43392, 306,141),
            ("2026-05-15",  880.56, 45697, 326,160),
            ("2026-05-16",  919.94, 48129, 338,169),
            ("2026-05-17",  962.64, 50709, 359,185),
            ("2026-05-18", 1010.41, 53627, 377,204),
            ("2026-05-19", 1060.08, 56397, 398,219),
        ],
    },
}

AD_META_IDS = {
    445: "6953040710116",  # Voce
    446: "6953037981516",  # Cachorro
    447: "6953035259116",  # Seu concorrente
    448: "6953018154316",  # Como utilizar
}

def bunzzai_window(ad_id, days):
    """
    Reconstroi totais da janela via diff de snapshots.
    Janela 'days' = ultimos N dias antes de hoje (19/mai).
    7d => somar diarios de 12/mai a 18/mai (= acum(18/mai) - acum(11/mai))
    15d => somar diarios de 04/mai a 18/mai (= acum(18/mai) - acum(03/mai))
    """
    hist = BUNZZAI[ad_id]["history"]
    by_date = {d: (s, i, c, cv) for (d, s, i, c, cv) in hist}
    end_acum = by_date["2026-05-18"]
    start_idx_date = {7: "2026-05-11", 15: "2026-05-03"}[days]
    start_acum = by_date[start_idx_date]
    return {
        "spend": end_acum[0] - start_acum[0],
        "impressions": end_acum[1] - start_acum[1],
        "clicks": end_acum[2] - start_acum[2],
        "conversions": end_acum[3] - start_acum[3],
    }

def skill_window(meta_ad_id, days):
    """Soma direta no banco — janela 'ultimos N dias antes de hoje'."""
    conn = get_connection()
    row = conn.execute(f"""
        SELECT SUM(spend) s, SUM(impressions) i, SUM(link_clicks) lc, SUM(leads) l
        FROM insights
        WHERE entity_id=? AND entity_type='ad' AND account_key='buzzmonitor_brl'
          AND date >= date('now','-{days} days') AND date < date('now')
    """, [meta_ad_id]).fetchone()
    conn.close()
    return {
        "spend": float(row["s"] or 0),
        "impressions": int(row["i"] or 0),
        "link_clicks": int(row["lc"] or 0),
        "leads": int(row["l"] or 0),
    }

def fmt(n, digits=2):
    if n is None: return "—"
    if isinstance(n, int): return f"{n:,}".replace(",", ".")
    return f"{n:,.{digits}f}".replace(",", "_").replace(".", ",").replace("_", ".")

def derived(d, leads_key, clicks_key):
    spend = d["spend"]; imp = d["impressions"]; cli = d[clicks_key]; lds = d[leads_key]
    return {
        "cpl": (spend/lds) if lds else 0,
        "ctr": (cli/imp*100) if imp else 0,
        "conv_lp": (lds/cli*100) if cli else 0,
    }

def trend_arrow(recent, baseline, lower_is_better):
    if baseline == 0 or recent == 0: return "—"
    delta = (recent-baseline)/baseline
    if abs(delta) < 0.10: return "→"
    if lower_is_better:
        return "↓ ✓" if delta < 0 else "↑ ⚠"
    return "↑" if delta > 0 else "↓"

print("="*92)
print("STRESS TEST — Webinar-Analise-Preditiva (campanha 124, buzzmonitor_brl, ad-level)")
print("Janelas: 7d (12-18/mai) | 15d (04-18/mai)  |  Hoje = 19/mai/2026")
print("="*92)

for ad_id in [445, 446, 447, 448]:
    meta_id = AD_META_IDS[ad_id]
    name = BUNZZAI[ad_id]["name"]
    print(f"\n### {name} (ad_id Bunzzai={ad_id} / meta_id={meta_id})\n")

    skill_7 = skill_window(meta_id, 7)
    skill_15 = skill_window(meta_id, 15)
    bz_7 = bunzzai_window(ad_id, 7)
    bz_15 = bunzzai_window(ad_id, 15)

    # Derivadas — Skill usa link_clicks (CTR link) e leads (CpL custom)
    sk_d_7 = derived(skill_7, "leads", "link_clicks")
    sk_d_15 = derived(skill_15, "leads", "link_clicks")
    # Bunzzai usa cliques totais e conversoes agregadas
    bz_d_7 = derived(bz_7, "conversions", "clicks")
    bz_d_15 = derived(bz_15, "conversions", "clicks")

    print("**Volume bruto na janela (skill vs Bunzzai):**\n")
    print("| Metrica         | Skill 15d | Bunzzai 15d | Skill 7d | Bunzzai 7d |")
    print("| --------------- | --------- | ----------- | -------- | ---------- |")
    print(f"| Investido R$    | {fmt(skill_15['spend'])} | {fmt(bz_15['spend'])} | {fmt(skill_7['spend'])} | {fmt(bz_7['spend'])} |")
    print(f"| Impressoes      | {fmt(skill_15['impressions'])} | {fmt(bz_15['impressions'])} | {fmt(skill_7['impressions'])} | {fmt(bz_7['impressions'])} |")
    print(f"| Cliques link    | {fmt(skill_15['link_clicks'])} | {fmt(bz_15['clicks'])}* | {fmt(skill_7['link_clicks'])} | {fmt(bz_7['clicks'])}* |")
    print(f"| Conversoes/Lds  | {fmt(skill_15['leads'])} | {fmt(bz_15['conversions'])} | {fmt(skill_7['leads'])} | {fmt(bz_7['conversions'])} |")

    print("\n**Derivadas + tendencia 7d vs 15d:**\n")
    print("| Metrica   | Skill 15d | Skill 7d | Tend Skill | Bunzzai 15d | Bunzzai 7d | Tend Bunzzai |")
    print("| --------- | --------- | -------- | ---------- | ----------- | ---------- | ------------ |")
    print(f"| CpL R$    | {fmt(sk_d_15['cpl'])} | {fmt(sk_d_7['cpl'])} | {trend_arrow(sk_d_7['cpl'], sk_d_15['cpl'], True)} | {fmt(bz_d_15['cpl'])} | {fmt(bz_d_7['cpl'])} | {trend_arrow(bz_d_7['cpl'], bz_d_15['cpl'], True)} |")
    print(f"| CTR % link| {fmt(sk_d_15['ctr'])} | {fmt(sk_d_7['ctr'])} | {trend_arrow(sk_d_7['ctr'], sk_d_15['ctr'], False)} | {fmt(bz_d_15['ctr'])} | {fmt(bz_d_7['ctr'])} | {trend_arrow(bz_d_7['ctr'], bz_d_15['ctr'], False)} |")
    print(f"| Conv LP % | {fmt(sk_d_15['conv_lp'])} | {fmt(sk_d_7['conv_lp'])} | {trend_arrow(sk_d_7['conv_lp'], sk_d_15['conv_lp'], False)} | {fmt(bz_d_15['conv_lp'])} | {fmt(bz_d_7['conv_lp'])} | {trend_arrow(bz_d_7['conv_lp'], bz_d_15['conv_lp'], False)} |")

    # Discrepancia de spend e leads na janela 15d
    sp_diff = (bz_15['spend'] - skill_15['spend']) / skill_15['spend'] * 100 if skill_15['spend'] else 0
    ld_diff = (bz_15['conversions'] - skill_15['leads']) / skill_15['leads'] * 100 if skill_15['leads'] else 0
    print(f"\n_Discrepancia 15d: spend Bunzzai vs skill = {sp_diff:+.1f}%  |  conv Bunzzai vs leads skill = {ld_diff:+.1f}%_")

print("\n" + "="*92)
print("CONSOLIDADO DA CAMPANHA (soma dos 4 ads, janela 15d)")
print("="*92)
sk_tot = {"spend":0,"impressions":0,"link_clicks":0,"leads":0}
bz_tot = {"spend":0,"impressions":0,"clicks":0,"conversions":0}
for ad_id in [445, 446, 447, 448]:
    s = skill_window(AD_META_IDS[ad_id], 15)
    b = bunzzai_window(ad_id, 15)
    for k in sk_tot: sk_tot[k] += s[k]
    for k in bz_tot: bz_tot[k] += b[k]
print(f"\nSkill   15d: R$ {fmt(sk_tot['spend'])} | {fmt(sk_tot['impressions'])} imp | {fmt(sk_tot['link_clicks'])} link clicks | {fmt(sk_tot['leads'])} leads")
print(f"Bunzzai 15d: R$ {fmt(bz_tot['spend'])} | {fmt(bz_tot['impressions'])} imp | {fmt(bz_tot['clicks'])} cliques tot | {fmt(bz_tot['conversions'])} conv")
print(f"\nDeltas Bunzzai vs Skill:")
print(f"  Spend: {(bz_tot['spend']-sk_tot['spend'])/sk_tot['spend']*100:+.1f}%   ({fmt(bz_tot['spend']-sk_tot['spend'])} R$)")
print(f"  Impr:  {(bz_tot['impressions']-sk_tot['impressions'])/sk_tot['impressions']*100:+.1f}%")
print(f"  Conv:  {(bz_tot['conversions']-sk_tot['leads'])/sk_tot['leads']*100:+.1f}%   (Bunzzai conta {bz_tot['conversions']-sk_tot['leads']:+d} 'a mais')")
