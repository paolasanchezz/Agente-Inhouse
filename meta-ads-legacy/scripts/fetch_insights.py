"""
fetch_insights.py — Coleta incremental de métricas via Meta Marketing API.

SOMENTE LEITURA: apenas operações GET na Meta Marketing API.

Estratégia de eficiência:
  Em vez de chamar a API por entidade (campanha por campanha, adset por adset),
  faz chamadas por CONTA e NÍVEL — 2 a 3 chamadas por período retornam dados
  de todas as entidades de uma vez.

  Exemplo: 30 campanhas + 90 adsets + período de 30 dias
    Abordagem antiga: ~120 chamadas (uma por entidade)
    Abordagem atual:  2-3 chamadas (uma por nível: campaign + adset)

  Dados de hoje nunca são coletados (dia incompleto contamina médias).
  Datas já no banco são puladas — zero chamadas desnecessárias.

Uso:
  python scripts/fetch_insights.py --account buzzmonitor_brl --period mes_atual
  python scripts/fetch_insights.py --account buzzmonitor_brl --period ultimos_30
"""

import argparse
import datetime
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cache_manager import (
    ACCOUNTS,
    get_account_id,
    check_token_expiry,
    setup_database,
    get_connection,
    save_insight,
    retry_on_throttle,
    BATCH_DELAY,
    RATE_LIMIT_DELAY,
    extract_leads,
    extract_cost_per_lead,
    extract_primary_conversions,
    extract_primary_cost,
    get_campaign_indicators,
    get_adset_campaign_map,
    get_ad_campaign_map,
    calc_lp_conversion_rate,
    count_ads_for_account,
    count_adsets_for_account,
    adsets_in_campaigns_with_indicator,
)

# Tabela `ads` é considerada defasada após este intervalo (forçará repopular).
ADS_STALE_HOURS = 24

import os
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent  # meta-ads/
load_dotenv(ROOT_DIR / ".env")

ASYNC_THRESHOLD = 7  # dias: acima disso usa async job

INSIGHT_FIELDS = [
    "date_start",
    "date_stop",
    "campaign_id",
    "adset_id",
    "ad_id",
    "spend",
    "impressions",
    "reach",
    "frequency",
    "clicks",
    "inline_link_clicks",
    "inline_link_click_ctr",
    "cpm",
    "cost_per_inline_link_click",
    "actions",
    "cost_per_action_type",
    "video_p25_watched_actions",
    "video_p50_watched_actions",
    "video_p75_watched_actions",
    "video_p100_watched_actions",
]


# ============================================================
# Utilitários de data
# ============================================================

def resolve_date_range(period_mode: str) -> tuple:
    today = datetime.date.today()
    if period_mode == "mes_atual":
        start = today.replace(day=1)
        end = today - datetime.timedelta(days=1)
    elif period_mode == "mes_anterior":
        last_day = today.replace(day=1) - datetime.timedelta(days=1)
        start = last_day.replace(day=1)
        end = last_day
    elif period_mode == "ultimos_30":
        start = today - datetime.timedelta(days=30)
        end = today - datetime.timedelta(days=1)
    else:
        raise ValueError(f"Período inválido: '{period_mode}'. Use: mes_atual | mes_anterior | ultimos_30")
    return start.isoformat(), end.isoformat()


def generate_date_range(date_start: str, date_end: str) -> list:
    start = datetime.date.fromisoformat(date_start)
    end = datetime.date.fromisoformat(date_end)
    return [(start + datetime.timedelta(days=i)).isoformat()
            for i in range((end - start).days + 1)]


def get_missing_dates_for_account(account_key: str, date_start: str, date_end: str,
                                   level: str = "campaign") -> list:
    """
    Retorna datas do intervalo que ainda não têm dados no banco para esta conta/nível.
    Por padrão usa 'campaign' como referência. Passe level='ad' para checar dados de anúncio.
    """
    conn = get_connection()
    existing = {
        row["date"] for row in conn.execute(
            "SELECT DISTINCT date FROM insights WHERE account_key=? AND entity_type=?",
            [account_key, level],
        ).fetchall()
    }
    conn.close()
    all_dates = generate_date_range(date_start, date_end)
    today = datetime.date.today().isoformat()
    return [d for d in all_dates if d not in existing and d < today]


def group_into_intervals(dates: list) -> list:
    """Agrupa datas contíguas em intervalos para minimizar chamadas."""
    if not dates:
        return []
    sorted_dates = sorted(dates)
    intervals = []
    start = prev = sorted_dates[0]
    for d in sorted_dates[1:]:
        curr = datetime.date.fromisoformat(d)
        prev_dt = datetime.date.fromisoformat(prev)
        if (curr - prev_dt).days == 1:
            prev = d
        else:
            intervals.append((start, prev))
            start = prev = d
    intervals.append((start, prev))
    return intervals


# ============================================================
# Parsing de resultado bruto da API
# ============================================================

def parse_insight_row(raw, entity_id: str, entity_type: str, account_key: str,
                      indicator: str = None) -> dict:
    actions = raw.get("actions", []) or []
    cost_per_action = raw.get("cost_per_action_type", []) or []
    link_clicks = int(raw.get("inline_link_clicks", 0) or 0)
    leads = extract_primary_conversions(actions, indicator)
    cost_per_lead = extract_primary_cost(cost_per_action, indicator)

    def get_video(field):
        v = raw.get(field, [])
        if isinstance(v, list) and v:
            return float(v[0].get("value", 0))
        return 0.0

    return {
        "entity_type": entity_type,
        "entity_id": entity_id,
        "account_key": account_key,
        "date": raw.get("date_start", ""),
        "spend": float(raw.get("spend", 0) or 0),
        "impressions": int(raw.get("impressions", 0) or 0),
        "reach": int(raw.get("reach", 0) or 0),
        "frequency": float(raw.get("frequency", 0) or 0),
        "link_clicks": link_clicks,
        "ctr_link": float(raw.get("inline_link_click_ctr", 0) or 0),
        "cpm": float(raw.get("cpm", 0) or 0),
        "cpc_link": float(raw.get("cost_per_inline_link_click", 0) or 0),
        "leads": leads,
        "cost_per_lead": cost_per_lead,
        "lp_conversion_rate": calc_lp_conversion_rate(leads, link_clicks),
        "video_p25": get_video("video_p25_watched_actions"),
        "video_p50": get_video("video_p50_watched_actions"),
        "video_p75": get_video("video_p75_watched_actions"),
        "video_p100": get_video("video_p100_watched_actions"),
    }


# ============================================================
# Coleta por conta e nível (síncrona — janelas <= ASYNC_THRESHOLD)
# ============================================================

@retry_on_throttle()
def _fetch_account_level_sync(account_id: str, level: str,
                               date_start: str, date_end: str) -> list:
    """
    Uma chamada: todos os dados do nível (campaign/adset/ad) para a conta inteira.
    Filtra spend > 0 para não trazer linhas vazias.
    """
    from facebook_business.adobjects.adaccount import AdAccount

    account = AdAccount(account_id)
    rows = account.get_insights(
        fields=INSIGHT_FIELDS,
        params={
            "level": level,
            "time_range": {"since": date_start, "until": date_end},
            "time_increment": 1,
            "filtering": [
                {"field": "spend", "operator": "GREATER_THAN", "value": "0"}
            ],
        },
    )
    return list(rows)


# ============================================================
# Coleta por conta e nível (assíncrona — janelas > ASYNC_THRESHOLD)
# ============================================================

@retry_on_throttle()
def _fetch_account_level_async(account_id: str, level: str,
                                date_start: str, date_end: str) -> list:
    """
    Async job para janelas > ASYNC_THRESHOLD dias.
    Evita timeout em períodos longos.
    """
    from facebook_business.adobjects.adaccount import AdAccount

    account = AdAccount(account_id)
    job = account.get_insights_async(
        fields=INSIGHT_FIELDS,
        params={
            "level": level,
            "time_range": {"since": date_start, "until": date_end},
            "time_increment": 1,
            "filtering": [
                {"field": "spend", "operator": "GREATER_THAN", "value": "0"}
            ],
        },
    )

    poll_interval = 15
    while True:
        job.remote_read(fields=["async_percent_completion", "async_status"])
        status = job["async_status"]
        pct = job.get("async_percent_completion", 0)
        print(f"  ~ Async job ({level}): {status} ({pct}%)    ", end="\r")

        if status == "Job Completed":
            print()
            return list(job.get_result(params={"limit": 500}))
        elif status in ["Job Failed", "Job Skipped"]:
            raise RuntimeError(f"Async job falhou: {status}")
        time.sleep(poll_interval)


# ============================================================
# Coleta por intervalo (decide sync vs async automaticamente)
# ============================================================

def fetch_level_for_interval(account_id: str, account_key: str,
                              level: str, date_start: str, date_end: str,
                              indicators: dict = None) -> int:
    """
    Busca todos os insights de um nível para o intervalo e salva no banco.
    indicators: {entity_id: results_indicator} — usado para extrair a conversão correta.
    Retorna número de linhas salvas.
    """
    num_days = (datetime.date.fromisoformat(date_end) -
                datetime.date.fromisoformat(date_start)).days + 1

    if num_days > ASYNC_THRESHOLD:
        rows = _fetch_account_level_async(account_id, level, date_start, date_end)
    else:
        rows = _fetch_account_level_sync(account_id, level, date_start, date_end)

    id_field = f"{level}_id"
    saved = 0
    for raw in rows:
        entity_id = raw.get(id_field)
        if not entity_id:
            continue
        indicator = (indicators or {}).get(entity_id)
        insight = parse_insight_row(raw, entity_id, level, account_key, indicator)
        if insight["date"]:
            save_insight(insight)
            saved += 1

    return saved


# ============================================================
# Garantia da estrutura de anúncios
# ============================================================

def _ads_table_is_stale(account_key: str) -> tuple:
    """
    Decide se a tabela `ads` precisa ser repopulada para a conta.
    Retorna (needs_populate: bool, reason: str).

    Heurística — repopular se:
      (a) tabela vazia para a conta; OU
      (b) há adsets de campanhas com `results_indicator` não-trivial mas zero ads
          registrados dessas mesmas campanhas (cobre o caso em que ads foram populados
          parcialmente e a coleta de insight de ad ficaria com leads=0); OU
      (c) último fetch > ADS_STALE_HOURS atrás.
    """
    n_ads, last_fetch = count_ads_for_account(account_key)
    n_adsets = count_adsets_for_account(account_key)

    if n_ads == 0 and n_adsets > 0:
        return True, f"tabela `ads` vazia ({n_adsets} adsets registrados sem ads)"

    # Cobertura por campanha com indicator: detecta caso de ads parciais
    adsets_needing_ads = adsets_in_campaigns_with_indicator(account_key)
    if adsets_needing_ads:
        conn = get_connection()
        ad_camps = {
            r["campaign_id"]
            for r in conn.execute(
                "SELECT DISTINCT campaign_id FROM ads WHERE account_key=?",
                [account_key],
            ).fetchall()
        }
        adset_camps = {
            r["campaign_id"]
            for r in conn.execute(
                "SELECT DISTINCT a.campaign_id "
                "FROM adsets a JOIN campaigns c ON c.id=a.campaign_id "
                "WHERE a.account_key=? AND c.results_indicator IS NOT NULL "
                "AND c.results_indicator != '' AND c.results_indicator != 'mixed'",
                [account_key],
            ).fetchall()
        }
        conn.close()
        uncovered = adset_camps - ad_camps
        if uncovered:
            return True, (
                f"{len(uncovered)} campanha(s) com `results_indicator` custom sem ads "
                f"na tabela — leads seriam salvos como 0"
            )

    # Idade
    if last_fetch:
        try:
            last_dt = datetime.datetime.fromisoformat(last_fetch.replace("Z", ""))
            age_h = (datetime.datetime.utcnow() - last_dt).total_seconds() / 3600
            if age_h > ADS_STALE_HOURS:
                return True, f"última atualização {age_h:.1f}h atrás (> {ADS_STALE_HOURS}h)"
        except Exception:
            return True, "fetched_at em formato inválido"

    return False, ""


def _ensure_ads_populated(account_key: str, days: int = 30) -> None:
    """
    Garante que a tabela `ads` esteja populada e fresca antes da coleta de insights
    no nível ad. Sem isso, `ad_camp_map` fica vazio/parcial, `ad_indicators` perde
    o pixel custom da campanha, e o `extract_primary_conversions` cai em fallback
    silencioso que conta 0 leads.

    Faz a chamada à API via `fetch_campaigns.fetch_all(..., include_ads=True)`.
    """
    needs, reason = _ads_table_is_stale(account_key)
    if not needs:
        return

    print(f"\n   [!] Estrutura de anuncios desatualizada: {reason}")
    print(f"   [!] Auto-populando via fetch_campaigns.fetch_all (1x antes da coleta)...")

    # Import lazy para evitar ciclo de import entre os scripts
    import fetch_campaigns
    fetch_campaigns.fetch_all(account_key, days=days, include_ads=True)
    print(f"   [OK] Estrutura de anuncios atualizada.\n")


# ============================================================
# Orquestrador principal
# ============================================================

def fetch_all_insights(account_key: str, period_mode: str,
                       include_ads: bool = False) -> None:
    """
    Coleta insights para todos os níveis da conta no período.

    Requisições por execução (dados ausentes):
      - 1 call por nível por intervalo contíguo de datas ausentes
      - Tipicamente: 2-3 calls no total (campaign + adset + opcional ad)
      - Se todos os dados já existem: 0 calls

    Quando `include_ads=True`, garante antes que a tabela `ads` está populada
    para evitar bug silencioso de leads=0 em campanhas com pixel custom.

    Dados de hoje nunca são coletados (dia incompleto).
    """
    account = ACCOUNTS[account_key]
    account_id = get_account_id(account_key)
    date_start, date_end = resolve_date_range(period_mode)

    print(f"\n>> Coletando insights: {account['label']}")
    print(f"   Período: {period_mode} ({date_start} -> {date_end})")

    # Pré-condição: estrutura de anúncios precisa estar pronta antes da coleta nível ad
    if include_ads:
        _ensure_ads_populated(account_key)

    # Pré-carrega indicadores de conversão por entidade (1 consulta SQL por nível)
    camp_indicators = get_campaign_indicators(account_key)
    adset_camp_map = get_adset_campaign_map(account_key)
    ad_camp_map = get_ad_campaign_map(account_key)
    adset_indicators = {
        adset_id: camp_indicators.get(camp_id)
        for adset_id, camp_id in adset_camp_map.items()
    }
    ad_indicators = {
        ad_id: camp_indicators.get(camp_id)
        for ad_id, camp_id in ad_camp_map.items()
    }
    level_indicators = {
        "campaign": camp_indicators,
        "adset": adset_indicators,
        "ad": ad_indicators,
    }

    # Validação final: alerta se ainda houver campanhas com indicator custom sem ads
    # mapeados (a auto-populate não cobriu — provável caso de campanha pausada há +30d
    # sem gasto no período de fetch_campaigns). Não aborta: a coleta continua nos níveis
    # campaign/adset (que continuam corretos), apenas avisa que o nível ad ficará incompleto.
    if include_ads:
        adsets_needing_ads = adsets_in_campaigns_with_indicator(account_key)
        ad_camps_covered = set(ad_camp_map.values())
        uncovered_camps = {
            adset_camp_map[adset_id]
            for adset_id in adsets_needing_ads
            if adset_id in adset_camp_map
            and adset_camp_map[adset_id] not in ad_camps_covered
        }
        if uncovered_camps:
            print(
                f"\n[AVISO] {len(uncovered_camps)} campanha(s) com `results_indicator` "
                f"custom NAO tem ads mapeados — leads do nivel ad podem ficar 0:"
            )
            for camp_id in list(uncovered_camps)[:10]:
                print(f"   - campaign_id={camp_id} (indicator={camp_indicators.get(camp_id)})")
            print(
                f"   Considere rodar `python scripts/fetch_campaigns.py "
                f"--account {account_key} --include-ads --days 90` para janela mais ampla.\n"
            )

    levels = ["campaign", "adset"]
    if include_ads:
        levels.append("ad")

    total_saved = 0
    for level in levels:
        # Verifica datas ausentes por nível — evita re-fetch do que já existe
        missing = get_missing_dates_for_account(account_key, date_start, date_end, level=level)
        if not missing:
            print(f"   {level.capitalize():10} -> ja no banco, nenhuma chamada necessaria")
            continue

        print(f"   {level.capitalize()}: {len(missing)} datas ausentes ({missing[0]} a {missing[-1]})")
        intervals = group_into_intervals(missing)

        level_saved = 0
        for date_start_i, date_end_i in intervals:
            n = fetch_level_for_interval(
                account_id, account_key, level, date_start_i, date_end_i,
                indicators=level_indicators.get(level, {}),
            )
            level_saved += n
            time.sleep(RATE_LIMIT_DELAY)

        print(f"   {level.capitalize():10} -> {level_saved} linhas salvas")
        total_saved += level_saved
        time.sleep(BATCH_DELAY)

    if total_saved == 0:
        print("   [OK] Todos os dados ja estao no banco — nenhuma chamada a API necessaria.")
    else:
        print(f"\n[OK] Total: {total_saved} linhas inseridas no banco.")


# ============================================================
# CLI
# ============================================================

def main():
    from facebook_business.api import FacebookAdsApi

    parser = argparse.ArgumentParser(
        description="Coleta incremental de insights Meta Ads por conta/nível (SOMENTE LEITURA)"
    )
    parser.add_argument("--account", required=True, choices=list(ACCOUNTS.keys()))
    parser.add_argument(
        "--period",
        required=True,
        choices=["mes_atual", "mes_anterior", "ultimos_30"],
    )
    parser.add_argument(
        "--include-ads",
        action="store_true",
        help="Inclui nível de anúncio (padrão: apenas campaign + adset)",
    )
    args = parser.parse_args()

    check_token_expiry()
    setup_database()

    token = os.getenv("META_ACCESS_TOKEN")
    version = os.getenv("META_API_VERSION", "v21.0")
    FacebookAdsApi.init(access_token=token, api_version=version)

    fetch_all_insights(args.account, args.period, include_ads=args.include_ads)


if __name__ == "__main__":
    main()
