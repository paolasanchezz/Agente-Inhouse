"""
find_ad_by_url.py — Varre todas as contas de anuncio acessiveis pelo token e
procura ads que usem uma URL especifica em qualquer campo do criativo.

SOMENTE LEITURA: apenas GETs na Meta Marketing API.

Estrategia:
  1) Lista todas as contas via /me/adaccounts
  2) Para cada conta, pega ads com effective_status ACTIVE/PAUSED (ignora ARCHIVED/DELETED)
     expandindo o criativo inline (1 chamada paginada por conta).
  3) Faz match case-insensitive do trecho da URL em qualquer string do JSON do criativo
     (cobre link_url, object_story_spec, asset_feed_spec, template_data, url_tags, etc.)

Uso:
  python scripts/find_ad_by_url.py "plataforma-completa-monitorizacion-redes-sociales"
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / ".env")

# Campos do criativo onde URLs podem aparecer
CREATIVE_FIELDS = [
    "id",
    "name",
    "link_url",
    "object_story_spec",
    "asset_feed_spec",
    "template_url",
    "template_url_spec",
    "url_tags",
    "effective_object_story_id",
    "object_type",
    "thumbnail_url",
    "image_url",
]

AD_FIELDS = [
    "id",
    "name",
    "status",
    "effective_status",
    "campaign{id,name}",
    "adset{id,name}",
    f"creative{{{','.join(CREATIVE_FIELDS)}}}",
]


def collect_strings(obj, out=None):
    """Recursivamente extrai todas as strings de um objeto aninhado."""
    if out is None:
        out = []
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            collect_strings(v, out)
    elif isinstance(obj, list):
        for v in obj:
            collect_strings(v, out)
    return out


def find_url_in_creative(creative_dict, needle_lower, regex=None):
    """Retorna lista de strings do criativo onde a needle aparece (case-insensitive).
    Se regex for passado, usa match por regex; senao substring."""
    if not creative_dict:
        return []
    strings = collect_strings(creative_dict)
    matches = []
    for s in strings:
        if regex is not None:
            if regex.search(s):
                matches.append(s)
        else:
            if needle_lower in s.lower():
                matches.append(s)
    return matches


def list_all_accounts(api):
    """Retorna todas as contas de anuncio acessiveis pelo token."""
    from facebook_business.adobjects.user import User

    me = User(fbid="me")
    accounts = me.get_ad_accounts(
        fields=["id", "name", "account_status", "currency", "business_name"],
        params={"limit": 500},
    )
    return list(accounts)


def fetch_ads_for_account(account_id, account_label, include_archived=False, small_batch=False):
    """Busca ads com criativo expandido, paginado.
    small_batch: usa limit menor (50) e menos fields — fallback para contas que dao 500."""
    from facebook_business.adobjects.adaccount import AdAccount

    statuses = ["ACTIVE", "PAUSED"]
    if include_archived:
        statuses.append("ARCHIVED")

    fields = AD_FIELDS
    limit = 200
    if small_batch:
        # Versao leve do creative — so o essencial para procurar URL
        light_creative = "creative{id,name,link_url,object_story_spec,asset_feed_spec,url_tags}"
        fields = ["id", "name", "status", "effective_status", light_creative]
        limit = 50

    account = AdAccount(account_id)
    try:
        ads = account.get_ads(
            fields=fields,
            params={
                "effective_status": statuses,
                "limit": limit,
            },
        )
        return list(ads)
    except Exception as e:
        msg = str(e)
        # Auto-fallback para batch menor em caso de "reduce the amount of data"
        if not small_batch and ("reduce the amount of data" in msg.lower() or "code: 1" in msg.lower()):
            print(f"   [RETRY] {account_label}: batch menor")
            return fetch_ads_for_account(account_id, account_label, include_archived, small_batch=True)
        print(f"   [ERRO] {account_label}: {msg[:200]}")
        return []


def main():
    parser = argparse.ArgumentParser(
        description="Procura ads que usam uma URL especifica em qualquer conta acessivel."
    )
    parser.add_argument(
        "needle",
        help="Trecho da URL a procurar (ex: 'plataforma-completa-monitorizacion-redes-sociales')",
    )
    parser.add_argument(
        "--include-archived",
        action="store_true",
        help="Inclui ads ARCHIVED (padrao: apenas ACTIVE + PAUSED)",
    )
    parser.add_argument(
        "--regex",
        help="Padrao regex (case-insensitive) usado no lugar de substring. "
             "Ex: '(?:^|[^a-z])buzzmonitor\\.com/plataforma'",
    )
    args = parser.parse_args()

    needle_lower = args.needle.lower()
    needle_regex = re.compile(args.regex, re.IGNORECASE) if args.regex else None

    from facebook_business.api import FacebookAdsApi

    token = os.getenv("META_ACCESS_TOKEN")
    version = os.getenv("META_API_VERSION", "v21.0")
    if not token:
        print("[ERRO] META_ACCESS_TOKEN nao encontrado no .env")
        sys.exit(1)

    api = FacebookAdsApi.init(access_token=token, api_version=version)
    print(f"[OK] SDK Meta inicializado (API {version})")
    print(f">> Procurando ads com URL contendo: '{args.needle}'\n")

    accounts = list_all_accounts(api)
    print(f">> {len(accounts)} contas acessiveis pelo token\n")

    findings = []
    for i, acc in enumerate(accounts, 1):
        acc_id = acc["id"]
        acc_name = acc.get("name", "(sem nome)")
        acc_status = acc.get("account_status")  # 1 = ACTIVE
        status_label = "ATIVA" if acc_status == 1 else f"status={acc_status}"
        print(f"[{i}/{len(accounts)}] {acc_name} ({acc_id}) — {status_label}")

        ads = fetch_ads_for_account(acc_id, acc_name, include_archived=args.include_archived)
        status_filter = "ACTIVE+PAUSED+ARCHIVED" if args.include_archived else "ACTIVE+PAUSED"
        print(f"   {len(ads)} ads ({status_filter}) examinados")

        for ad in ads:
            ad_dict = ad.export_all_data() if hasattr(ad, "export_all_data") else dict(ad)
            creative = ad_dict.get("creative", {})
            matches = find_url_in_creative(creative, needle_lower, regex=needle_regex)
            if matches:
                findings.append({
                    "account_name": acc_name,
                    "account_id": acc_id,
                    "ad_id": ad_dict.get("id"),
                    "ad_name": ad_dict.get("name"),
                    "ad_status": ad_dict.get("effective_status"),
                    "campaign_name": (ad_dict.get("campaign") or {}).get("name"),
                    "campaign_id": (ad_dict.get("campaign") or {}).get("id"),
                    "adset_name": (ad_dict.get("adset") or {}).get("name"),
                    "adset_id": (ad_dict.get("adset") or {}).get("id"),
                    "matched_strings": matches[:10],
                })

        time.sleep(1.0)  # rate limit gentil

    print("\n" + "=" * 70)
    print(f">> RESULTADO — {len(findings)} ad(s) encontrado(s)\n")

    if not findings:
        print("Nenhum ad ativo ou pausado em nenhuma conta usa essa URL.")
    else:
        for f in findings:
            print(f"  Conta:    {f['account_name']} ({f['account_id']})")
            print(f"  Campanha: {f['campaign_name']} ({f['campaign_id']})")
            print(f"  Adset:    {f['adset_name']} ({f['adset_id']})")
            print(f"  Ad:       {f['ad_name']} ({f['ad_id']}) — {f['ad_status']}")
            print(f"  Match(es) no criativo:")
            for m in f["matched_strings"]:
                print(f"    - {m}")
            print()

    out_path = ROOT_DIR / "data" / "url_search_results.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(findings, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] Resultado salvo em {out_path}")


if __name__ == "__main__":
    main()
