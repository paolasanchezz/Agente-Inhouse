#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRAVA DE DEPLOY VERCEL  (hook PreToolUse)

Intercepta qualquer tentativa de deploy no Vercel e pede CONFIRMACAO explicita
antes de prosseguir. Decisao = "ask" (nunca bloqueio cego): se voce esta dentro
da skill /lp-publicar ou /dashboard-atualizar, aprova; se voce digitou um
`vercel deploy` a mao, recusa e roda a skill.

POR QUE EXISTE
--------------
Deploy cru (fora da skill) ja derrubou LPs vizinhas em producao 3x:
  - 2026-05-11  latam-webinar-atencionalcliente -> 404 por ~3 dias
  - 2026-05-13  mesma LP -> 404 por ~1h40 (4 `vercel deploy --force` seguidos)
  - 2026-06-16  webinar.buzzmonitor.com inteiro (6 LPs) -> 404; vitima: atencion-al-cliente-es
Causa-raiz sempre a mesma: `vercel deploy` publica o que esta na sibling LOCAL;
se ela esta desatualizada, as LPs vizinhas ausentes somem do ar. As 4 camadas de
defesa (sync 0.5.d, drift-check, baseline, smoke test) vivem DENTRO da lp-publicar
e sao todas puladas no deploy manual. Documentacao sozinha ja falhou 3x -> trava tecnica.

O QUE COBRE
-----------
  - Bash / PowerShell rodando `vercel (deploy|promote|rollback|redeploy)`
    (inclui `npx --yes vercel deploy ...`). Read-only (ls/whoami/link/pull/inspect)
    NAO dispara.
  - Tool MCP de deploy do Vercel (`mcp__*__deploy_to_vercel`).

O QUE NAO COBRE (limites honestos)
----------------------------------
  - Deploy pelo painel web do Vercel (fora do Claude Code) -> so documentacao.
  - `vercel deploy` escondido atras de `npm run <script>` (o hook ve "npm run",
    nao "vercel"). As skills do repo chamam vercel direto, entao na pratica pega.

Config em .claude/settings.json (COMMITADO -> vale para todos os colaboradores).
Contrato do hook: le JSON no stdin; imprime JSON de decisao no stdout; exit 0.
Em qualquer duvida/erro, NAO interfere (fail-open) para nunca travar trabalho legitimo.
"""
import sys
import io
import json
import re

# stdin/stdout em UTF-8 (Windows default cp1252 quebra com acentos/§ no comando ou na razao)
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# `vercel ... (deploy|promote|rollback|redeploy)` quando vercel e invocado como comando:
#   (a) no inicio de um segmento de comando (^ ; & | ` $( ), ou
#   (b) apos um runner de pacote (npx / bunx / pnpm / yarn).
# Mantido dentro do mesmo segmento ([^\n;&|]) para nao casar verbo de outro comando.
# Verbos read-only (ls/whoami/link/pull/inspect/env/domains) ficam de fora de proposito.
VERCEL_INVOKE = re.compile(
    r"(?:^|[\n;&|`]|\$\()\s*vercel\b[^\n;&|]*?\b(?:deploy|promote|rollback|redeploy)\b"
    r"|"
    r"\b(?:npx|bunx|pnpm|yarn)\b[^\n;&|]*?\bvercel\b[^\n;&|]*?\b(?:deploy|promote|rollback|redeploy)\b",
    re.IGNORECASE,
)

REASON = (
    "TRAVA DE DEPLOY VERCEL. Deploy cru (fora da skill) ja derrubou LPs vizinhas em "
    "producao 3x (11/mai, 13/mai, 16/jun/2026) porque pula o sync da sibling. "
    "Se voce esta DENTRO de /lp-publicar (LP) ou /dashboard-atualizar (dashboard), pode APROVAR. "
    "Se voce digitou um 'vercel deploy' a mao, RECUSE e rode a skill. "
    "So inspecao/snapshot, sem deploy? Use /lp-sync. "
    "Detalhes: landing-pages/CONTEXT.md §7.1 (anti-padroes) e §7.2 (incidentes)."
)


def ask(reason):
    """Emite decisao 'ask' (confirmacao do usuario) e encerra com sucesso."""
    # ensure_ascii=True (default) -> saida puramente ASCII; § e acentos viram \uXXXX,
    # o Claude Code renderiza de volta em UTF-8. Evita UnicodeEncodeError no Windows.
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        sys.exit(0)  # nao parseou -> nao interfere

    tool_name = (data.get("tool_name") or "")
    tool_input = data.get("tool_input") or {}

    # Vetor 1: tool MCP de deploy do Vercel (qualquer server id).
    if tool_name.endswith("deploy_to_vercel"):
        ask("Deploy via MCP do Vercel detectado (ignora CLI e sibling). " + REASON)

    # Vetor 2: vercel CLI via Bash / PowerShell.
    command = tool_input.get("command")
    if isinstance(command, str) and VERCEL_INVOKE.search(command):
        ask(REASON)

    # Qualquer outra coisa -> fluxo normal (sem JSON, exit 0).
    sys.exit(0)


if __name__ == "__main__":
    main()
