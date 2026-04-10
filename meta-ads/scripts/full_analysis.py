"""
full_analysis.py — Orquestrador end-to-end de análise Meta Ads.

Fluxo:
  1. Verifica token e banco
  2. Atualiza estrutura (campanhas → adsets → ads) de forma incremental
  3. Atualiza insights para o período solicitado
  4. Gera relatório Markdown em data/reports/

SOMENTE LEITURA: nenhuma operação POST/PUT/DELETE na Meta Marketing API.

Uso:
    python scripts/meta_ads/full_analysis.py --account buzzmonitor_brl --period mes_atual
    python scripts/meta_ads/full_analysis.py --account cxpress_usd --period ultimos_30 --only-report
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
ROOT_DIR = Path(__file__).parent.parent  # meta-ads/
load_dotenv(ROOT_DIR / ".env")

from cache_manager import ACCOUNTS, check_token_expiry, setup_database
from fetch_insights import resolve_date_range, fetch_all_insights
from report_generator import generate_report


def init_api():
    from facebook_business.api import FacebookAdsApi
    token = os.getenv("META_ACCESS_TOKEN")
    version = os.getenv("META_API_VERSION", "v21.0")
    if not token:
        raise EnvironmentError(
            "META_ACCESS_TOKEN não encontrado. Configure o .env antes de continuar."
        )
    FacebookAdsApi.init(access_token=token, api_version=version)
    print(f"[OK] SDK Meta inicializado (API {version})")


def run_full_analysis(account_key: str, period_mode: str, only_report: bool = False) -> None:
    account = ACCOUNTS[account_key]
    date_start, date_end = resolve_date_range(period_mode)

    print(f"\n{'='*60}")
    print(f"  Meta Ads — Análise Completa")
    print(f"  Conta:   {account['label']}")
    print(f"  Período: {period_mode} ({date_start} → {date_end})")
    print(f"{'='*60}\n")

    # ── Etapa 1: Verificações ────────────────────────────────────
    check_token_expiry()
    setup_database()

    if not only_report:
        init_api()

        # ── Etapa 2: Estrutura (incremental) ────────────────────────
        print("\n[1/3] Atualizando estrutura de campanhas...")
        from fetch_campaigns import fetch_all
        fetch_all(account_key)

        # ── Etapa 3: Insights (incremental) ─────────────────────────
        print(f"\n[2/3] Atualizando insights ({period_mode})...")
        fetch_all_insights(account_key, period_mode)
    else:
        print("[INFO] Modo --only-report: pulando coleta da API, usando dados do banco.\n")

    # ── Etapa 4: Relatório ───────────────────────────────────────
    print("\n[3/3] Gerando relatório...")
    report_path = generate_report(account_key, period_mode, date_start, date_end)

    print(f"\n{'='*60}")
    print(f"  [OK] Análise concluída!")
    print(f"  Relatório: {report_path}")
    print(f"{'='*60}\n")

    # Exibe primeiras linhas do relatório como preview
    with open(report_path, "r", encoding="utf-8") as f:
        preview = "".join(f.readlines()[:30])
    print("── Preview do relatório (primeiras 30 linhas) ──\n")
    print(preview)
    print("... (arquivo completo em data/reports/)\n")


def main():
    parser = argparse.ArgumentParser(
        description="Análise completa Meta Ads (SOMENTE LEITURA)"
    )
    parser.add_argument(
        "--account",
        required=True,
        choices=list(ACCOUNTS.keys()),
        help="Conta a analisar",
    )
    parser.add_argument(
        "--period",
        required=True,
        choices=["mes_atual", "mes_anterior", "ultimos_30"],
        help="Período de análise",
    )
    parser.add_argument(
        "--only-report",
        action="store_true",
        help="Pula a coleta da API e gera relatório apenas com dados já no banco",
    )
    args = parser.parse_args()

    run_full_analysis(args.account, args.period, only_report=args.only_report)


if __name__ == "__main__":
    main()
