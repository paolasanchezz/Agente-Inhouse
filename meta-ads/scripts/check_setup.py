"""
check_setup.py — Valida configuracao do meta-ads/.env antes do primeiro uso.

Verifica:
  1. .env existe e tem META_ACCESS_TOKEN + META_TOKEN_CREATED_AT preenchidos
  2. Token nao esta expirado (usa check_token_expiry de cache_manager)
  3. Cada uma das 6 contas em ACCOUNTS responde a uma chamada read-only

Uso:
    cd meta-ads
    python scripts/check_setup.py

Exit codes:
    0 — tudo OK
    1 — qualquer falha
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / ".env")

from cache_manager import ACCOUNTS, check_token_expiry  # noqa: E402

# Cores ANSI (funcionam no Windows Terminal, Mac e Linux modernos)
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def ok(msg: str) -> None:
    print(f"{GREEN}[OK]{RESET} {msg}")


def fail(msg: str) -> None:
    print(f"{RED}[ERRO]{RESET} {msg}")


def warn(msg: str) -> None:
    print(f"{YELLOW}[AVISO]{RESET} {msg}")


def check_env_vars() -> bool:
    """Verifica que as variaveis essenciais do .env estao preenchidas."""
    print("\n--- 1. Variaveis de ambiente ---")
    all_ok = True

    token = os.getenv("META_ACCESS_TOKEN")
    if not token:
        fail("META_ACCESS_TOKEN nao definido. Edite meta-ads/.env e cole seu token.")
        all_ok = False
    elif not token.startswith("EAA"):
        warn("META_ACCESS_TOKEN nao comeca com 'EAA' — pode estar incorreto.")
    else:
        ok(f"META_ACCESS_TOKEN presente ({len(token)} caracteres).")

    created_at = os.getenv("META_TOKEN_CREATED_AT")
    if not created_at:
        fail("META_TOKEN_CREATED_AT nao definido. Coloque a data de hoje (YYYY-MM-DD) no .env.")
        all_ok = False
    else:
        ok(f"META_TOKEN_CREATED_AT = {created_at}")

    api_version = os.getenv("META_API_VERSION", "v21.0")
    ok(f"META_API_VERSION = {api_version}")

    return all_ok


def check_expiry() -> None:
    """Roda check_token_expiry de cache_manager (alerta 10 dias antes)."""
    print("\n--- 2. Validade do token ---")
    try:
        check_token_expiry()
        ok("Token dentro da validade.")
    except RuntimeError as e:
        fail(str(e))
        sys.exit(1)


def check_accounts() -> bool:
    """Para cada conta em ACCOUNTS, faz GET /act_XXX?fields=name,account_status."""
    print("\n--- 3. Acesso as 6 contas ---")
    try:
        from facebook_business.api import FacebookAdsApi
        from facebook_business.adobjects.adaccount import AdAccount
    except ImportError:
        fail("facebook-business nao instalado. Rode: cd meta-ads && python -m pip install -r requirements.txt")
        return False

    token = os.getenv("META_ACCESS_TOKEN")
    api_version = os.getenv("META_API_VERSION", "v21.0")
    FacebookAdsApi.init(access_token=token, api_version=api_version)

    all_ok = True
    for key, account in ACCOUNTS.items():
        account_id = account["account_id"]
        label = account["label"]
        try:
            data = AdAccount(account_id).api_get(fields=["name", "account_status"])
            status = data.get("account_status")
            status_str = "ativa" if status == 1 else f"status={status}"
            ok(f"{key:<20} {label} ({status_str})")
        except Exception as e:
            err_msg = str(e)
            if "190" in err_msg or "Invalid OAuth" in err_msg:
                fail(f"{key:<20} {label} — token invalido ou expirado")
                all_ok = False
                # Token invalido afeta tudo, parar de tentar.
                break
            elif "100" in err_msg or "permission" in err_msg.lower():
                fail(f"{key:<20} {label} — sem permissao (peca ads_read ao admin do BM)")
                all_ok = False
            else:
                fail(f"{key:<20} {label} — {err_msg[:120]}")
                all_ok = False

    return all_ok


def main() -> int:
    print("="*60)
    print("  Validador de setup — Meta Ads")
    print("="*60)

    if not (ROOT_DIR / ".env").exists():
        fail(f".env nao encontrado em {ROOT_DIR / '.env'}")
        print("\nRode: cd meta-ads && cp .env.example .env (Windows: copy .env.example .env)")
        print("Depois edite o .env e preencha META_ACCESS_TOKEN + META_TOKEN_CREATED_AT.")
        return 1

    env_ok = check_env_vars()
    if not env_ok:
        print("\n" + "="*60)
        fail("Setup incompleto — preencha o .env e rode de novo.")
        return 1

    check_expiry()  # Pode dar sys.exit(1) se expirado.

    accounts_ok = check_accounts()

    print("\n" + "="*60)
    if env_ok and accounts_ok:
        ok("Tudo configurado! Voce esta pronto para usar /meta-ads e /anuncios.")
        return 0
    else:
        fail("Algumas verificacoes falharam — veja os erros acima.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
