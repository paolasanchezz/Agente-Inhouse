#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRAVA DE CAMPANHA META  (hook PreToolUse)

Intercepta tentativas de (1) ATIVAR/RELIGAR ou (2) gastar ACIMA DO TETO em Meta Ads
e pede CONFIRMACAO explicita antes de prosseguir. Decisao = "ask" (nunca bloqueio
cego): se voce esta dentro da skill /meta-campanha e ja revisou o plano, aprova;
se a chamada veio sem voce ter revisado, recusa.

POR QUE EXISTE
--------------
A skill /meta-campanha escreve de verdade no Meta (gasta verba). Duas coisas nunca
podem acontecer "no automatico":
  - ATIVAR (PAUSADO -> ATIVO) ou RELIGAR uma campanha/adset/ad -> comeca a gastar.
  - Criar/editar com orcamento muito acima da media da conta.
A skill ja mostra o plano e confirma (camada 1). Este hook e a camada 2 (trava
tecnica) — vale mesmo se o modelo errar. Mesma filosofia do guard_vercel_deploy.py.

O QUE COBRE
-----------
  MCP oficial da Meta (qualquer server id -> matcher regex uuid-agnostico):
    - ads_activate_entity                      -> sempre ask (liga verba)
    - ads_update_entity com status=ACTIVE      -> ask (religacao)
    - ads_update_entity / ads_create_campaign / ads_create_ad_set com orcamento
      diario/lifetime acima do teto da moeda    -> ask (trava de orcamento)
  Defense-in-depth no MCP do BunzzAI (que tambem escreve no Meta):
    - ativar_campanha / ativar_adset / ativar_anuncio (e variantes *_meta) -> ask
    - alterar_orcamento (e *_meta)             -> ask
    - criar_campanha_conversacional            -> ask

O QUE NAO COBRE (limites honestos)
----------------------------------
  - Pausar / renomear / editar nao-orcamentario -> liberados (sem gasto novo).
  - Edicoes pela UI do Ads Manager (fora do Claude Code) -> so a propria Meta gateia.

Config dos tetos: meta-ads/data/budget-guardrails.json (valores em CENTAVOS).
Contrato do hook: le JSON no stdin; imprime JSON de decisao no stdout; exit 0.
Em qualquer duvida/erro de parsing da ENTRADA, NAO interfere (fail-open) para nunca
travar trabalho legitimo. Se a config sumir, cai em tetos conservadores embutidos.
"""
import sys
import io
import os
import json

# stdin/stdout em UTF-8 (Windows default cp1252 quebra com acentos/simbolos)
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Tetos embutidos (fallback se a config sumir). Centavos. Conservador.
FALLBACK = {
    "BRL": {"adset_daily_cents": 5000, "campaign_daily_cents": 20000, "lifetime_cents": 150000},
    "USD": {"adset_daily_cents": 1200, "campaign_daily_cents": 4800, "lifetime_cents": 36000},
    "EUR": {"adset_daily_cents": 1200, "campaign_daily_cents": 4800, "lifetime_cents": 36000},
}
SYMBOL = {"BRL": "R$", "USD": "US$", "EUR": "EUR "}

ACT_REASON = (
    "TRAVA META — ATIVACAO. Esta acao tira a entidade de PAUSADO e comeca a GASTAR verba real. "
    "Se voce esta dentro de /meta-campanha e ja revisou o plano (conta, publico, orcamento, criativo), "
    "pode APROVAR. Se nao revisou ou nao era pra ligar agora, RECUSE. Lembre: ativar o pai nao ativa os filhos."
)
REACT_REASON = (
    "TRAVA META — RELIGACAO. Voce esta mudando o status para ATIVO (volta a gastar). "
    "Aprove so se for proposital e revisado; senao RECUSE."
)
BUNZZAI_REASON = (
    "TRAVA META (via BunzzAI) — esta tool ativa/altera orcamento de campanha real no Meta. "
    "A analise de Meta Ads e SOMENTE LEITURA (/bunzzai). Para escrita, use /meta-campanha. "
    "Aprove so se for proposital e revisado; senao RECUSE."
)


def ask(reason):
    """Emite decisao 'ask' (confirmacao do usuario) e encerra com sucesso."""
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def load_config():
    proj = os.environ.get("CLAUDE_PROJECT_DIR")
    candidates = []
    if proj:
        candidates.append(os.path.join(proj, "meta-ads", "data", "budget-guardrails.json"))
    candidates.append(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", "meta-ads", "data", "budget-guardrails.json"))
    for path in candidates:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            continue
    return None


def to_int_cents(value):
    """Coage orcamento (int ou string numerica) para int de centavos; None se nao der."""
    if value is None:
        return None
    try:
        return int(str(value).strip())
    except Exception:
        return None


def fmt(cents, currency):
    try:
        return "{}{:,.2f}".format(SYMBOL.get(currency, ""), cents / 100.0)
    except Exception:
        return str(cents)


def currency_for(account_id, cfg):
    amap = (cfg or {}).get("account_currency", {})
    default = (cfg or {}).get("default_currency", "BRL")
    return amap.get(str(account_id), default)


def ceilings_for(currency, cfg):
    table = (cfg or {}).get("ceilings_by_currency", {})
    return table.get(currency) or FALLBACK.get(currency) or FALLBACK["BRL"]


def check_budget(account_id, budget_fields, cfg):
    """budget_fields: dict com possiveis chaves de orcamento (em centavos).
    Se algum valor passar o teto da moeda, emite ask (nao retorna)."""
    currency = currency_for(account_id, cfg)
    ceil = ceilings_for(currency, cfg)
    sym = SYMBOL.get(currency, "")

    checks = [
        ("daily_budget", "adset_daily_cents", "orcamento diario do adset"),
        ("campaign_daily_budget", "campaign_daily_cents", "orcamento diario da campanha (CBO)"),
        ("lifetime_budget", "lifetime_cents", "orcamento total (lifetime) do adset"),
        ("campaign_lifetime_budget", "lifetime_cents", "orcamento total (lifetime) da campanha"),
    ]
    for field, ceil_key, label in checks:
        cents = to_int_cents(budget_fields.get(field))
        limit = ceil.get(ceil_key)
        if cents is not None and limit is not None and cents > limit:
            ask(
                "TRAVA META — ORCAMENTO ALTO. {label}: {val}/dia (ou total), acima do teto de {lim} "
                "da conta ({cur}). Confirme so se for proposital — senao ajuste o valor. "
                "Tetos editaveis em meta-ads/data/budget-guardrails.json.".format(
                    label=label,
                    val=fmt(cents, currency),
                    lim=fmt(limit, currency),
                    cur=currency,
                )
            )


def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        sys.exit(0)  # nao parseou -> nao interfere

    tool_name = (data.get("tool_name") or "")
    tool_input = data.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        sys.exit(0)

    # short name (sufixo apos o ultimo "__") para casar independente do server id
    short = tool_name.rsplit("__", 1)[-1]

    # --- BunzzAI (defense-in-depth): ativar_* / alterar_orcamento* / criar_campanha_conversacional
    if short.startswith("ativar_") or short.startswith("alterar_orcamento") or short == "criar_campanha_conversacional":
        ask(BUNZZAI_REASON)

    # --- MCP oficial da Meta ---
    cfg = load_config()

    # Ativacao direta -> sempre ask
    if short == "ads_activate_entity":
        ask(ACT_REASON)

    # Edicao de entidade: religacao (status=ACTIVE) e/ou orcamento acima do teto
    if short == "ads_update_entity":
        fields = tool_input.get("fields")
        if isinstance(fields, str):
            try:
                fields = json.loads(fields)
            except Exception:
                fields = {}
        if not isinstance(fields, dict):
            fields = {}
        status = str(fields.get("status", "")).upper()
        if status == "ACTIVE":
            ask(REACT_REASON)
        check_budget(tool_input.get("ad_account_id"), fields, cfg)
        sys.exit(0)

    # Criacao de campanha (CBO budgets ficam na campanha)
    if short == "ads_create_campaign":
        check_budget(tool_input.get("ad_account_id"), tool_input, cfg)
        sys.exit(0)

    # Criacao de adset (ABO budgets ficam no adset)
    if short == "ads_create_ad_set":
        check_budget(tool_input.get("ad_account_id"), tool_input, cfg)
        sys.exit(0)

    # Qualquer outra coisa -> fluxo normal (sem JSON, exit 0).
    sys.exit(0)


if __name__ == "__main__":
    main()
