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
    get_campaigns,
    save_campaign,
    save_adset,
    save_ad,
    update_campaign_indicator,
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
def get_active_campaign_ids(account_id: str) -> set:
    """
    Retorna IDs de campanhas com status ACTIVE atualmente — independente de spend.
    Garante que campanhas recém-criadas sem gasto ainda sejam incluídas.
    """
    from facebook_business.adobjects.adaccount import AdAccount

    account = AdAccount(account_id)
    campaigns = account.get_campaigns(
        fields=["id"],
        params={"effective_status": ["ACTIVE"]},
    )
    ids = {c["id"] for c in campaigns}
    print(f"   Campanhas ACTIVE atualmente: {len(ids)}")
    return ids


def fetch_campaign_indicators(account_id: str, account_key: str, days: int = 30) -> None:
    """
    Busca o indicador de conversão primária (results) de cada campanha.
    Uma única chamada à API — atualiza campaigns.results_indicator no banco.
    """
    import warnings
    import datetime
    from facebook_business.adobjects.adaccount import AdAccount

    today = datetime.date.today()
    date_start = (today - datetime.timedelta(days=days)).isoformat()
    date_end = (today - datetime.timedelta(days=1)).isoformat()

    account = AdAccount(account_id)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        rows = list(account.get_insights(
            fields=["campaign_id", "results"],
            params={
                "level": "campaign",
                "time_range": {"since": date_start, "until": date_end},
                "filtering": [{"field": "spend", "operator": "GREATER_THAN", "value": "0"}],
            },
        ))

    updated = 0
    for row in rows:
        campaign_id = row.get("campaign_id")
        results = row.get("results") or []
        if campaign_id and results and results[0].get("indicator"):
            update_campaign_indicator(campaign_id, results[0]["indicator"])
            updated += 1

    print(f"   Indicadores de conversao atualizados: {updated} campanhas")


@retry_on_throttle()
def fetch_adsets_for_campaign(campaign_id: str, account_key: str) -> list:
    from facebook_business.adobjects.campaign import Campaign
    fields = ["id", "name", "status", "optimization_goal", "daily_budget", "lifetime_budget"]
    adsets_raw = Campaign(campaign_id).get_ad_sets(fields=fields)
    return [
        {
            "id": a["id"],
            "campaign_id": campaign_id,
            "account_key": account_key,
            "name": a.get("name", ""),
            "status": a.get("status"),
            "optimization_goal": a.get("optimization_goal"),
            "daily_budget": float(a["daily_budget"]) / 100 if a.get("daily_budget") else None,
            "lifetime_budget": float(a["lifetime_budget"]) / 100 if a.get("lifetime_budget") else None,
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
    print(f"   Filtro: ACTIVE atualmente + spend > 0 nos ultimos {days} dias\n")

    # Passo 1: IDs via dual approach incremental — 3 chamadas à API
    campaign_ids_with_spend = get_ids_with_spend(account_id, "campaign", days)
    existing_ids = {c["id"] for c in get_campaigns(account_key)}
    all_active_ids = get_active_campaign_ids(account_id)
    new_active_ids = all_active_ids - existing_ids  # apenas as que ainda não estão no banco
    campaign_ids = campaign_ids_with_spend | new_active_ids
    adset_ids_with_spend = get_ids_with_spend(account_id, "adset", days)

    if new_active_ids:
        print(f"   Campanhas novas (ACTIVE, fora do banco): {len(new_active_ids)}")
    print(f"   Total unico: {len(campaign_ids)} campanhas\n")

    if not campaign_ids:
        print("[AVISO] Nenhuma campanha encontrada. Verifique a conta.")
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

    print(f"\n[OK] Coleta concluida: {len(campaign_ids)} campanhas | {total_adsets} adsets | {total_ads} anuncios")

    print("\n>> Buscando indicadores de conversao primaria...")
    fetch_campaign_indicators(account_id, account_key, days=days)

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
