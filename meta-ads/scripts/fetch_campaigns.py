"""
fetch_campaigns.py — Coleta de estrutura de campanhas com filtro por gasto recente.

SOMENTE LEITURA: apenas operações GET na Meta Marketing API.

Estratégia de filtro:
  Busca campanhas/adsets que tiveram gasto > 0 nos últimos N dias (padrão: 30).
  Isso captura tanto campanhas ativas quanto recentemente pausadas — ambas relevantes
  para análise de performance e comparação de criativos.

Requisições por execução:
  1  GET insights de campanhas com gasto (filtragem por spend > 0)
  1  GET insights de adsets com gasto
  N  GET detalhes de cada campanha com gasto (batch quando possível)
  N  GET adsets de cada campanha
  Total: ~2 + N*2 (tipicamente 30-70 requisições para contas médias)

Uso:
  python scripts/fetch_campaigns.py --account buzzmonitor_brl
  python scripts/fetch_campaigns.py --account buzzmonitor_brl --days 60
  python scripts/fetch_campaigns.py --account buzzmonitor_brl --include-ads
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
    infer_campaign_type,
    get_funnel_group,
    save_campaign,
    save_adset,
    save_ad,
    setup_database,
    retry_on_throttle,
    BATCH_DELAY,
)

import os
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent  # meta-ads/
load_dotenv(ROOT_DIR / ".env")


def init_api():
    from facebook_business.api import FacebookAdsApi
    token = os.getenv("META_ACCESS_TOKEN")
    version = os.getenv("META_API_VERSION", "v21.0")
    if not token:
        raise EnvironmentError("META_ACCESS_TOKEN não encontrado no .env.")
    FacebookAdsApi.init(access_token=token, api_version=version)
    print(f"[OK] SDK Meta inicializado (API {version})")


# ============================================================
# Passo 1: IDs com gasto recente (1 chamada por nível)
# ============================================================

@retry_on_throttle()
def get_ids_with_spend(account_id: str, level: str, days: int) -> set:
    """
    Retorna conjunto de IDs (campanha ou adset) que tiveram spend > 0
    nos últimos N dias. Uma única chamada à API por nível.
    """
    from facebook_business.adobjects.adaccount import AdAccount

    today = datetime.date.today()
    date_start = (today - datetime.timedelta(days=days)).isoformat()
    date_end = (today - datetime.timedelta(days=1)).isoformat()

    account = AdAccount(account_id)
    rows = account.get_insights(
        fields=[f"{level}_id", f"{level}_name", "spend"],
        params={
            "level": level,
            "time_range": {"since": date_start, "until": date_end},
            "filtering": [
                {"field": "spend", "operator": "GREATER_THAN", "value": "0"}
            ],
        },
    )
    ids = {row[f"{level}_id"] for row in rows}
    print(f"   {level.capitalize()}s com gasto nos últimos {days} dias: {len(ids)}")
    return ids


# ============================================================
# Passo 2: Detalhes das campanhas
# ============================================================

@retry_on_throttle()
def fetch_campaign_details(campaign_id: str, account_key: str) -> dict:
    """Busca detalhes de uma campanha pelo ID. SOMENTE LEITURA."""
    from facebook_business.adobjects.campaign import Campaign

    c = Campaign(campaign_id).api_get(
        fields=["id", "name", "objective", "status", "daily_budget", "lifetime_budget"]
    )
    name = c.get("name", "")
    campaign_type = infer_campaign_type(name)
    return {
        "id": c["id"],
        "account_key": account_key,
        "name": name,
        "objective": c.get("objective"),
        "status": c.get("status"),
        "campaign_type": campaign_type,
        "funnel_group": get_funnel_group(campaign_type),
        "daily_budget": float(c["daily_budget"]) / 100 if c.get("daily_budget") else None,
        "lifetime_budget": float(c["lifetime_budget"]) / 100 if c.get("lifetime_budget") else None,
    }


# ============================================================
# Passo 3: Adsets e anúncios
# ============================================================

@retry_on_throttle()
def fetch_adsets_for_campaign(campaign_id: str, account_key: str) -> list:
    from facebook_business.adobjects.campaign import Campaign
    fields = ["id", "name", "status", "optimization_goal"]
    adsets_raw = Campaign(campaign_id).get_ad_sets(fields=fields)
    return [
        {
            "id": a["id"],
            "campaign_id": campaign_id,
            "account_key": account_key,
            "name": a.get("name", ""),
            "status": a.get("status"),
            "optimization_goal": a.get("optimization_goal"),
        }
        for a in adsets_raw
    ]


@retry_on_throttle()
def fetch_ads_for_adset(adset_id: str, campaign_id: str, account_key: str) -> list:
    from facebook_business.adobjects.adset import AdSet
    ads_raw = AdSet(adset_id).get_ads(fields=["id", "name", "status"])
    return [
        {
            "id": a["id"],
            "adset_id": adset_id,
            "campaign_id": campaign_id,
            "account_key": account_key,
            "name": a.get("name", ""),
            "status": a.get("status"),
        }
        for a in ads_raw
    ]


# ============================================================
# Orquestrador principal
# ============================================================

def fetch_all(account_key: str, days: int = 30, include_ads: bool = False) -> None:
    """
    Coleta estrutura de campanhas/adsets com gasto > 0 nos últimos N dias.

    Inclui campanhas ativas E recentemente pausadas — ambas relevantes
    para análise e comparação de criativos.

    Requisições: ~2 (filtro de IDs) + N*2 (detalhes + adsets por campanha).
    """
    account = ACCOUNTS[account_key]
    account_id = get_account_id(account_key)

    print(f"\n>> Coletando estrutura: {account['label']} ({account_id})")
    print(f"   Filtro: spend > 0 nos últimos {days} dias\n")

    # Passo 1: IDs com gasto — 2 chamadas à API
    campaign_ids = get_ids_with_spend(account_id, "campaign", days)
    adset_ids_with_spend = get_ids_with_spend(account_id, "adset", days)

    if not campaign_ids:
        print("[AVISO] Nenhuma campanha com gasto no período. Verifique o período ou a conta.")
        return

    total_adsets = 0
    total_ads = 0
    unclassified = []

    for i, campaign_id in enumerate(campaign_ids, 1):
        # Detalhes da campanha
        camp = fetch_campaign_details(campaign_id, account_key)
        save_campaign(camp)

        if camp["campaign_type"] == "nao_classificada":
            unclassified.append(camp["name"])

        print(f"   [{i}/{len(campaign_ids)}] {camp['name'][:60]}")

        # Adsets da campanha
        adsets = fetch_adsets_for_campaign(campaign_id, account_key)
        for adset in adsets:
            save_adset(adset)
            total_adsets += 1

        # Anúncios (opcional)
        if include_ads:
            for adset in adsets:
                # Só busca anúncios do adset se o adset teve gasto
                if adset["id"] in adset_ids_with_spend:
                    ads = fetch_ads_for_adset(adset["id"], campaign_id, account_key)
                    for ad in ads:
                        save_ad(ad)
                    total_ads += len(ads)

        time.sleep(BATCH_DELAY)

    print(f"\n[OK] Coleta concluída: {len(campaign_ids)} campanhas | {total_adsets} adsets | {total_ads} anúncios")

    if unclassified:
        print(f"\n[AVISO] {len(unclassified)} campanha(s) NAO CLASSIFICADA(S) — revisão manual:")
        for name in unclassified:
            print(f"   • {name}")


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Coleta estrutura de campanhas Meta Ads com gasto recente (SOMENTE LEITURA)"
    )
    parser.add_argument("--account", required=True, choices=list(ACCOUNTS.keys()))
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Janela de dias para filtrar spend > 0 (padrão: 30)",
    )
    parser.add_argument(
        "--include-ads",
        action="store_true",
        help="Busca também anúncios por adset com gasto (padrão: não)",
    )
    args = parser.parse_args()

    check_token_expiry()
    setup_database()
    init_api()
    fetch_all(args.account, days=args.days, include_ads=args.include_ads)


if __name__ == "__main__":
    main()
