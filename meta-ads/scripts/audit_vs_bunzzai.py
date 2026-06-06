"""
audit_vs_bunzzai.py — Audita os numeros do MCP BunzzAI contra a Meta API (modulo meta-ads).

Compara, para uma tripla campanha -> adset -> ad, os dados das duas fontes:
  - META  : insights DIARIOS no SQLite local (meta_ads.db), agregados na janela.
  - BUNZZAI: snapshots CUMULATIVOS (monitoring_history) salvos em arquivo pelo MCP.

Por que um harness e nao "olhar os dois e comparar":
  1. Alinhamento de janela e a parte que mais erra no olho. BunzzAI nao tem dado diario;
     a janela e reconstruida por diff de snapshots cumulativos. Aqui isso fica explicito.
  2. Metricas derivadas (CTR/CPM/CPC/CpL/Conv.LP) PRECISAM ser recalculadas dos primitivos
     com a MESMA formula nos dois lados. O agregador da meta-ads guarda CTR/CPM/CPC como
     MEDIA DAS DIARIAS (AVG), nao total/total — comparar o campo cru contra o BunzzAI e erro.
  3. BunzzAI nao expoe metrica propria de adset/campanha: reconstruimos somando os ads.

SOMENTE LEITURA. Nao chama Meta API nem MCP — consome o DB local + arquivos ja baixados
via `tool_get_ad_performance` (o agente alimenta os caminhos no spec).

Uso:
    cd meta-ads
    python scripts/audit_vs_bunzzai.py --spec ../tmp/audit_spec.json

Spec JSON (ver tmp/audit_spec.json):
    {
      "account": "buzzmonitor_brl",
      "today": "2026-05-29",              # data de referencia; a janela termina em today-1
      "windows": [7, 15, 30],
      "cumulative_start": "2026-04-01",
      "campaign": {"meta_id": "...", "bunzzai_id": 123, "name": "..."},
      "adset":    {"meta_id": "...", "bunzzai_id": 363, "name": "..."},
      "ad":       {"meta_id": "...", "bunzzai_id": 443, "name": "..."},
      "bunzzai_ad_history": { "<ad_meta_id>": "<caminho ao .txt do MCP>", ... }
    }
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from benchmark_checker import aggregate_metrics_for_period  # noqa: E402
from cache_manager import get_adsets, get_ads  # noqa: E402

TOL_MATCH = 3.0   # % — diferenca aceitavel p/ metricas de mesma definicao (spend, impressions)
TOL_SOFT = 10.0   # % — acima de MATCH mas explicavel por borda de dia/snapshot


# ------------------------------------------------------------------ BunzzAI
def load_history(path: str) -> list:
    """Le o arquivo salvo pelo MCP ({result: "<json string>"}) e devolve monitoring_history."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    obj = json.loads(raw["result"]) if isinstance(raw, dict) and "result" in raw else raw
    return obj["monitoring_history"]


def daily_cumulative(history: list) -> dict:
    """{ 'YYYY-MM-DD': {spend, impressions, clicks, conversions} } — pega o snapshot
    de MAIOR recorded_at por dia (cumulativo de fim de dia)."""
    by_day = {}
    for s in history:
        d = s["recorded_at"][:10]
        ra = s["recorded_at"]
        cum = {
            "spend": float(s["investimento_acumulado"] or 0),
            "impressions": int(s["impressoes"] or 0),
            "clicks": int(s["cliques"] or 0),
            "conversions": int(s["conversoes"] or 0),
        }
        if d not in by_day or ra > by_day[d][0]:
            by_day[d] = (ra, cum)
    return {d: v[1] for d, v in by_day.items()}


def nearest_before(by_day: dict, target_iso: str):
    """(data_usada, cumulativo) do dia mais proximo <= target. None se nao houver."""
    cands = [d for d in by_day if d <= target_iso]
    if not cands:
        return None
    d = max(cands)
    return d, by_day[d]


def bz_window(by_day: dict, today: dt.date, days: int):
    """Janela por diff de snapshots: cum(today-1) - cum(today-1-days).
    Devolve (primitivos, data_inicio_usada, data_fim_usada) ou None."""
    end_t = (today - dt.timedelta(days=1)).isoformat()
    start_t = (today - dt.timedelta(days=days + 1)).isoformat()
    e = nearest_before(by_day, end_t)
    s = nearest_before(by_day, start_t)
    if not e or not s:
        return None
    ed, ec = e
    sd, sc = s
    prim = {k: ec[k] - sc[k] for k in ("spend", "impressions", "clicks", "conversions")}
    return prim, sd, ed


def frozen_streak(by_day: dict, today: dt.date) -> tuple:
    """(n_dias_congelados, data_inicio) — 2+ snapshots cumulativos identicos consecutivos
    nos ultimos 30 dias = cron travado."""
    last = None
    streak = 0
    start = None
    for d in sorted(by_day):
        if (today - dt.date.fromisoformat(d)).days > 30 or d > today.isoformat():
            continue
        c = by_day[d]
        key = (c["spend"], c["impressions"], c["clicks"], c["conversions"])
        if key == last:
            streak += 1
            start = start or d
        else:
            if streak >= 2:
                return streak, start
            streak, start, last = 0, None, key
    return (streak, start) if streak >= 2 else (0, None)


# ------------------------------------------------------------------ Meta
def meta_primitives(meta_id: str, level: str, account: str, ds: str, de: str) -> dict:
    """Primitivos Meta na janela [ds, de]. link_clicks/leads sao os campos crus;
    derivados sao recalculados a parte (NAO usar ctr_link/cpm/cpc_link do agregador:
    aqueles sao MEDIA das diarias)."""
    m = aggregate_metrics_for_period(meta_id, level, account, ds, de)
    if not m:
        return {}
    return {
        "spend": float(m.get("spend", 0) or 0),
        "impressions": int(m.get("impressions", 0) or 0),
        "reach": int(m.get("reach", 0) or 0),
        "clicks": int(m.get("link_clicks", 0) or 0),   # Meta = link_clicks
        "conversions": int(m.get("leads", 0) or 0),     # Meta = leads (pixel primario)
    }


# ------------------------------------------------------------------ comum
def derived(p: dict) -> dict:
    """Recalcula taxas dos primitivos — MESMA formula nos dois lados."""
    spend, imp, cli, conv = p["spend"], p["impressions"], p["clicks"], p["conversions"]
    return {
        "ctr": round(cli / imp * 100, 4) if imp else 0,
        "cpm": round(spend / imp * 1000, 4) if imp else 0,
        "cpc": round(spend / cli, 4) if cli else 0,
        "cpl": round(spend / conv, 4) if conv else 0,
        "conv_lp": round(conv / cli * 100, 4) if cli else 0,
    }


def pct(meta_v, bz_v):
    if meta_v is None or bz_v is None:
        return None
    if not meta_v:
        return None if bz_v else 0.0
    return (bz_v - meta_v) / meta_v * 100


def classify(metric: str, meta_v, bz_v) -> str:
    if metric == "reach":
        return "N/A — BunzzAI nao expoe reach"
    p = pct(meta_v, bz_v)
    if metric in ("spend", "impressions", "cpm"):
        if p is None:
            return "DIVERGENCIA (Meta=0)"
        a = abs(p)
        if a <= TOL_MATCH:
            return f"MATCH ({p:+.1f}%)"
        if a <= TOL_SOFT:
            return f"~ borda de dia ({p:+.1f}%)"
        return f"DIVERGENCIA ({p:+.1f}%)"
    if metric == "clicks":
        if p is None:
            return "checar (Meta=0)"
        if bz_v >= meta_v:
            return f"DIF. ESPERADA: BunzzAI(total) >= Meta(link). {p:+.1f}%"
        if abs(p) <= TOL_SOFT:
            return f"~ iguais ({p:+.1f}%) — BunzzAI levemente < por borda de snapshot"
        return f"INVERTIDO forte ({p:+.1f}%) — investigar"
    if metric == "conversions":
        if p is None:
            return "checar (Meta=0)"
        if bz_v >= meta_v:
            return f"DIF. ESPERADA: BunzzAI(todas) >= Meta(lead custom). {p:+.1f}%"
        if abs(p) <= TOL_SOFT:
            return f"~ iguais ({p:+.1f}%) — borda de snapshot"
        return f"INVERTIDO forte ({p:+.1f}%) — investigar"
    # derivadas
    base = {"ctr": "clicks", "cpc": "clicks", "conv_lp": "clicks/conv", "cpl": "conversions"}.get(metric, "")
    return f"derivada (herda dif. de {base}); {p:+.1f}%" if p is not None else "derivada"


ROWS = [
    ("spend", "Investimento", "R$"),
    ("impressions", "Impressoes", ""),
    ("reach", "Alcance (reach)", ""),
    ("clicks", "Cliques (link vs total)", ""),
    ("conversions", "Conversoes (lead vs todas)", ""),
    ("ctr", "CTR %", "%"),
    ("cpm", "CPM", "R$"),
    ("cpc", "CPC", "R$"),
    ("cpl", "CpL / Custo-conv", "R$"),
    ("conv_lp", "Conv. LP %", "%"),
]


def fmt(v):
    if isinstance(v, float):
        return f"{v:,.2f}"
    return str(v)


def table(meta_p, bz_p):
    if not meta_p or not bz_p:
        return "_(sem dados de um dos lados)_\n"
    meta = {**meta_p, **derived(meta_p)}
    bz = {**bz_p, "reach": None, **derived(bz_p)}
    out = ["| Metrica | Meta | BunzzAI | Classificacao |", "|---|---|---|---|"]
    for key, label, _u in ROWS:
        mv = meta.get(key)
        bv = bz.get(key)
        out.append(f"| {label} | {fmt(mv) if mv is not None else '—'} | "
                   f"{fmt(bv) if bv is not None else '—'} | {classify(key, mv, bv)} |")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Auditoria BunzzAI vs Meta (read-only)")
    ap.add_argument("--spec", required=True)
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    account = spec["account"]
    today = dt.date.fromisoformat(spec["today"])
    windows = spec.get("windows", [7, 15, 30])
    cum_start = spec.get("cumulative_start", "2026-01-01")
    end_iso = (today - dt.timedelta(days=1)).isoformat()

    camp, adset, ad = spec["campaign"], spec["adset"], spec["ad"]

    # Estrutura Meta: ads do adset e da campanha (p/ reconstruir BunzzAI somando ads)
    camp_ads = [a["id"] for ads in (get_ads(s["id"]) for s in get_adsets(camp["meta_id"])) for a in ads]
    adset_ads = [a["id"] for a in get_ads(adset["meta_id"])]

    # BunzzAI: by_day por ad_meta_id
    hist_paths = spec["bunzzai_ad_history"]
    by_day_map = {amid: daily_cumulative(load_history(p)) for amid, p in hist_paths.items()}

    def bz_sum(ad_ids, days):
        tot = {"spend": 0.0, "impressions": 0, "clicks": 0, "conversions": 0}
        miss = []
        for amid in ad_ids:
            bd = by_day_map.get(amid)
            w = bz_window(bd, today, days) if bd else None
            if not w:
                miss.append(amid)
                continue
            for k in tot:
                tot[k] += w[0][k]
        return tot, miss

    print(f"# Auditoria BunzzAI vs Meta — {camp['name']}\n")
    print(f"- Conta: `{account}`  |  hoje (ref): {today}  |  janela termina: {end_iso}")
    print(f"- Campanha: meta `{camp['meta_id']}` / bz `{camp['bunzzai_id']}`")
    print(f"- Adset: meta `{adset['meta_id']}` / bz `{adset['bunzzai_id']}`  ({len(adset_ads)} ad)")
    print(f"- Ad: meta `{ad['meta_id']}` / bz `{ad['bunzzai_id']}`  — {ad['name']}")
    print(f"- Ads da campanha (meta_id): {camp_ads}\n")

    # Cron travado por ad
    print("## Checagem de cron travado (BunzzAI, 30d)")
    for amid, bd in by_day_map.items():
        n, since = frozen_streak(bd, today)
        flag = f"[CRON TRAVADO: {n} dias desde {since}]" if n else "ok (sem congelamento)"
        rng = f"{min(bd)}..{max(bd)} ({len(bd)} dias)" if bd else "sem snapshots"
        print(f"- ad `{amid}`: {flag}  | cobertura {rng}")
    print()

    # Janela primaria (a primeira de `windows`, ex 7d) nos 3 niveis
    dprime = windows[0]
    ds_prime = (today - dt.timedelta(days=dprime)).isoformat()
    print(f"## Janela {dprime}d — Meta [{ds_prime}..{end_iso}] vs BunzzAI [diff de snapshots]\n")

    ad_w = bz_window(by_day_map.get(ad["meta_id"]), today, dprime)
    if ad_w:
        print(f"> Snapshots BunzzAI usados (ad): inicio={ad_w[1]}  fim={ad_w[2]}\n")

    print(f"### AD — {ad['name']}")
    print(table(meta_primitives(ad["meta_id"], "ad", account, ds_prime, end_iso),
                ad_w[0] if ad_w else None))

    adset_bz, adset_miss = bz_sum(adset_ads, dprime)
    print(f"### ADSET  (BunzzAI = soma de {len(adset_ads)} ad(s); faltando: {adset_miss or 'nenhum'})")
    print(table(meta_primitives(adset["meta_id"], "adset", account, ds_prime, end_iso), adset_bz))

    camp_bz, camp_miss = bz_sum(camp_ads, dprime)
    print(f"### CAMPANHA  (BunzzAI = soma de {len(camp_ads)} ad(s); faltando: {camp_miss or 'nenhum'})")
    print(table(meta_primitives(camp["meta_id"], "campaign", account, ds_prime, end_iso), camp_bz))

    # Janelas extras (so o ad, p/ contexto de tendencia)
    print("## Janelas extras (somente AD, p/ tendencia)\n")
    for d in windows[1:]:
        w = bz_window(by_day_map.get(ad["meta_id"]), today, d)
        ds = (today - dt.timedelta(days=d)).isoformat()
        print(f"### AD — janela {d}d  [Meta {ds}..{end_iso}]")
        print(table(meta_primitives(ad["meta_id"], "ad", account, ds, end_iso), w[0] if w else None))

    # Cumulativo (lifetime)
    print(f"## Cumulativo (lifetime) — Meta [{cum_start}..{end_iso}] vs BunzzAI (ultimo snapshot)\n")

    def bz_cum(ad_ids):
        tot = {"spend": 0.0, "impressions": 0, "clicks": 0, "conversions": 0}
        for amid in ad_ids:
            bd = by_day_map.get(amid)
            if bd:
                last = bd[max(bd)]
                for k in tot:
                    tot[k] += last[k]
        return tot

    print(f"### AD — {ad['name']}")
    print(table(meta_primitives(ad["meta_id"], "ad", account, cum_start, end_iso),
                bz_cum([ad["meta_id"]])))
    print("### CAMPANHA")
    print(table(meta_primitives(camp["meta_id"], "campaign", account, cum_start, end_iso),
                bz_cum(camp_ads)))


if __name__ == "__main__":
    main()
