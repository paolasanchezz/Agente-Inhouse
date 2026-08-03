#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRAVA DE DEPLOY VERCEL  (hook PreToolUse)

Intercepta qualquer tentativa de deploy no Vercel e decide em DOIS niveis:

  1. DENY (bloqueio duro) — o deploy mira um projeto ja MIGRADO pro CI
     (landing-pages/dominios/MIGRADOS.json). Esses dominios deployam
     EXCLUSIVAMENTE via GitHub Actions; um deploy manual/sibling neles e
     sobrescrito no proximo push da main e a LP some do ar. Nao ha
     confirmacao possivel — o caminho certo e a skill (fluxo CI) ou o
     workflow_dispatch. Escape consciente: env var LP_DEPLOY_CI_OVERRIDE=1.

  2. ASK (confirmacao) — deploy Vercel que NAO mira projeto migrado
     (modo solo da /lp-publicar, /dashboard-atualizar, /blog-publicar).
     Comportamento historico do hook: se voce esta dentro dessas skills,
     aprova; se digitou um `vercel deploy` a mao, recusa e roda a skill.

POR QUE O NIVEL 1 EXISTE (incidente que motivou, 2026-08-03)
------------------------------------------------------------
A LP `webinar-atencion-multicanal-latam` foi publicada por deploy manual
direto no projeto que serve webinar.buzzmonitor.com (guarda-chuva MIGRADO).
Funcionou na hora, mas o proximo deploy do CI reconstruiu o dominio a partir
do manifesto (que nao a lista) e a apagou -> 404. Causa estrutural: os dois
caminhos de deploy (CI e manual) coexistiam sobre o mesmo projeto. O
PLANO-MIGRACAO-CI.md ja previa fechar isso (Principio 2: "cutover seco e
exclusivo" e Fase 4.2: token so-CI); enquanto a trava na fonte nao existir,
esta trava no Claude Code fecha o vetor que passa por aqui.

A decisao 5.2 do plano tinha descartado o hard-block "por fragilidade em
resolver o projeto-alvo do comando". Reaberta apos o incidente: a resolucao
agora usa DOIS sinais independentes, e qualquer duvida cai no ASK de sempre
(nunca pior que o comportamento historico).

COMO RESOLVE O PROJETO-ALVO (dois sinais; basta um)
---------------------------------------------------
  - Textual: o comando/args contem o projectId (`prj_...`), o nome do projeto
    (`buzzmonitor-lp-...` — o path da sibling e `{BASE}/{nome}`, entao o `cd`
    ate ela carrega o nome) ou o dominio migrado. Match ancorado por
    boundary pra nao pegar prefixo de projeto solo homonimo.
  - Filesystem: resolve o cwd-alvo (`cd <path>` / `--cwd <path>` no comando,
    senao o cwd da sessao), le `<cwd>/.vercel/project.json` e cruza o
    projectId com os ids migrados.

O QUE COBRE / NAO COBRE (limites honestos)
------------------------------------------
  - Bash / PowerShell rodando `vercel (deploy|promote|rollback|redeploy)`
    (inclui `npx --yes vercel deploy ...`). Read-only (ls/whoami/link/pull/
    inspect) NAO dispara.
  - Tool MCP de deploy do Vercel (`mcp__*__deploy_to_vercel`).
  - NAO cobre: deploy pelo painel web do Vercel, `vercel deploy` escondido
    atras de `npm run <script>`, ou um shell cujo cwd ja e a sibling sem `cd`
    no comando (nesse ultimo, o sinal textual ainda costuma pegar pelo nome
    do projeto/dominio no comando; se nada pegar, cai no ASK — nao piora).
    A trava definitiva contra esses e o token so-CI (Fase 4.2 do plano).

Config em .claude/settings.json (COMMITADO -> vale para todos os colaboradores).
Contrato do hook: le JSON no stdin; imprime JSON de decisao no stdout; exit 0.
Em qualquer duvida/erro, cai no ASK (fail-safe pro comportamento historico) —
nunca libera deploy migrado em silencio, nunca trava deploy legitimo sem saida.
"""
import sys
import io
import os
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

# Mensagem do nivel ASK (deploy Vercel que nao mira projeto migrado).
REASON_ASK = (
    "TRAVA DE DEPLOY VERCEL. Deploy cru (fora da skill) ja derrubou LPs vizinhas em "
    "producao (incidentes 11/mai, 13/mai, 16/jun/2026) porque pula o sync da sibling. "
    "Se voce esta DENTRO de /lp-publicar (modo solo), /dashboard-atualizar ou /blog-publicar, "
    "pode APROVAR. Se voce digitou um 'vercel deploy' a mao, RECUSE e rode a skill. "
    "Detalhes: landing-pages/CONTEXT.md §7.1 (anti-padroes) e §7.2 (incidentes)."
)

TRUTHY = {"1", "true", "yes", "on", "sim"}


def _emit(decision, reason):
    """Emite a decisao PreToolUse ('deny' ou 'ask') e encerra com sucesso.

    ensure_ascii=True (default) -> saida puramente ASCII; § e acentos viram
    \\uXXXX e o Claude Code renderiza de volta em UTF-8 (evita
    UnicodeEncodeError no Windows).
    """
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def find_repo_root():
    """Raiz do repo, robusta a cwd. Prioridade: CLAUDE_PROJECT_DIR; senao
    deriva de __file__ (.../<root>/.claude/hooks/guard_vercel_deploy.py)."""
    env_root = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_root and os.path.isdir(env_root):
        return env_root
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_migrated(repo_root):
    """Le MIGRADOS.json + cada manifesto de dominio migrado. Devolve
    (nomes_projeto, ids_projeto, dominios). Fail-open parcial: um manifesto
    ilegivel nao derruba os demais (o dominio ainda entra pela lista)."""
    names, ids, domains = set(), set(), set()
    base = os.path.join(repo_root, "landing-pages", "dominios")
    try:
        with open(os.path.join(base, "MIGRADOS.json"), encoding="utf-8") as fh:
            doms = json.load(fh)
    except Exception:
        return names, ids, domains  # sem lista -> nada a bloquear (cai no ASK)
    for dom in doms:
        if not isinstance(dom, str) or not dom:
            continue
        domains.add(dom.lower())
        key = dom.replace(".", "-")
        domains.add(key.lower())  # forma hifenizada (nome da pasta do manifesto)
        try:
            with open(os.path.join(base, key, "manifest.json"), encoding="utf-8") as fh:
                man = json.load(fh)
        except Exception:
            continue
        if man.get("projeto_vercel"):
            names.add(str(man["projeto_vercel"]))
        if man.get("projeto_vercel_id"):
            ids.add(str(man["projeto_vercel_id"]))
    return names, ids, domains


def _boundary_hit(needle, haystack):
    """True se `needle` aparece em `haystack` como token (nao como prefixo de
    um nome maior). Boundary = nao ter [\\w-] colado antes/depois — assim
    'buzzmonitor-content' nao casa dentro de 'buzzmonitor-content-latam'."""
    return re.search(r"(?<![\w-])" + re.escape(needle) + r"(?![\w-])",
                     haystack, re.IGNORECASE) is not None


def textual_match(text, names, ids, domains):
    """Retorna (tipo, valor) do 1o sinal textual de projeto migrado, ou None."""
    if not text:
        return None
    for pid in ids:  # projectId e unico o suficiente -> substring basta
        if pid and pid in text:
            return ("projectId", pid)
    for nm in names:
        if nm and _boundary_hit(nm, text):
            return ("projeto", nm)
    for dm in domains:
        if dm and _boundary_hit(dm, text):
            return ("dominio", dm)
    return None


def extract_target_cwd(command, payload_cwd):
    """Melhor esforco pra achar o diretorio onde o `vercel deploy` roda:
    `cd <path>` ou `--cwd <path>` no comando; senao o cwd da sessao."""
    if command:
        m = re.search(r"--cwd(?:=|\s+)(['\"]?)([^'\"&|;\n]+)\1", command)
        if m:
            return m.group(2).strip()
        m = re.search(r"(?:^|[\n;&|]|&&)\s*cd\s+(['\"]?)([^'\"&|;\n]+)\1", command)
        if m:
            return m.group(2).strip()
    return payload_cwd


def project_id_from_dir(cwd):
    """projectId de <cwd>/.vercel/project.json, ou None."""
    if not cwd:
        return None
    try:
        with open(os.path.join(cwd, ".vercel", "project.json"), encoding="utf-8") as fh:
            return json.load(fh).get("projectId")
    except Exception:
        return None


def is_deploy(tool_name, tool_input):
    """(is_deploy, haystack_textual, command_ou_None)."""
    if tool_name.endswith("deploy_to_vercel"):
        # MCP: sem comando de shell; o haystack e o proprio input serializado.
        try:
            return True, json.dumps(tool_input, ensure_ascii=False), None
        except Exception:
            return True, "", None
    command = tool_input.get("command")
    if isinstance(command, str) and VERCEL_INVOKE.search(command):
        return True, command, command
    return False, "", None


def evaluate(tool_name, tool_input, payload_cwd, repo_root, override=False):
    """Decide a acao. Retorna dict {action: 'pass'|'ask'|'deny', reason: str,
    signal: (tipo, valor)|None}. Pura -> testavel sem I/O de hook."""
    deploy, haystack, command = is_deploy(tool_name, tool_input)
    if not deploy:
        return {"action": "pass", "reason": "", "signal": None}

    names, ids, domains = load_migrated(repo_root)

    signal = textual_match(haystack, names, ids, domains)
    if signal is None and command is not None:
        target_cwd = extract_target_cwd(command, payload_cwd)
        pid = project_id_from_dir(target_cwd)
        if pid and pid in ids:
            signal = ("project.json", pid)

    if signal is not None:
        tipo, valor = signal
        if override:
            return {
                "action": "ask",
                "signal": signal,
                "reason": (
                    "OVERRIDE ATIVO (LP_DEPLOY_CI_OVERRIDE). Este deploy mira um projeto "
                    "MIGRADO pro CI (%s: %s) e normalmente seria BLOQUEADO — sera sobrescrito "
                    "no proximo push da main. So aprove se for recovery de emergencia "
                    "consciente. Caminho normal: skill /lp-publicar (fluxo CI) ou "
                    "`gh workflow run lp-deploy.yml -f dominio=<dominio>`." % (tipo, valor)
                ),
            }
        return {
            "action": "deny",
            "signal": signal,
            "reason": (
                "BLOQUEADO: deploy manual em projeto MIGRADO pro CI (%s: %s). "
                "Esse dominio deploya EXCLUSIVAMENTE via GitHub Actions "
                "(landing-pages/dominios/MIGRADOS.json). Deploy manual/sibling e "
                "sobrescrito no proximo push da main e a LP some do ar (foi o que "
                "derrubou webinar-atencion-multicanal-latam em 2026-08-03). "
                "Publique pela skill /lp-publicar (fluxo CI: atualiza manifesto + PR) "
                "ou, em emergencia, dispare o deploy no CI com "
                "`gh workflow run lp-deploy.yml -f dominio=<dominio>`. "
                "Falso-positivo? Rode com LP_DEPLOY_CI_OVERRIDE=1 no ambiente. "
                "Contexto: landing-pages/PLANO-MIGRACAO-CI.md (Principio 2 e Fase 4.2)."
                % (tipo, valor)
            ),
        }

    # Deploy Vercel que nao mira projeto migrado -> confirmacao de sempre.
    return {"action": "ask", "reason": REASON_ASK, "signal": None}


def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        sys.exit(0)  # nao parseou -> nao interfere

    tool_name = data.get("tool_name") or ""
    tool_input = data.get("tool_input") or {}
    payload_cwd = data.get("cwd") or ""
    override = str(os.environ.get("LP_DEPLOY_CI_OVERRIDE", "")).strip().lower() in TRUTHY

    try:
        result = evaluate(tool_name, tool_input, payload_cwd, find_repo_root(), override)
    except Exception:
        # Qualquer erro inesperado na resolucao -> fail-safe: se e deploy, ASK;
        # senao, passthrough. Nunca deixa passar migrado por bug, nunca trava seco.
        _deploy, _hay, _cmd = is_deploy(tool_name, tool_input)
        if _deploy:
            _emit("ask", REASON_ASK)
        sys.exit(0)

    if result["action"] == "pass":
        sys.exit(0)
    _emit(result["action"], result["reason"])


if __name__ == "__main__":
    main()
