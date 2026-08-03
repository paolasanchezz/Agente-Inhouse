#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes do guard_vercel_deploy (nivel DENY para projetos migrados + ASK legado).

Roda sem framework: `py .claude/hooks/test_guard_vercel_deploy.py`
Exercita `evaluate(...)` contra os manifestos REAIS do repo (fonte de verdade
dos projetos migrados), mais um caso filesystem com .vercel/project.json fake.
Sai 1 se qualquer caso falhar.
"""
import os
import sys
import json
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guard_vercel_deploy as g  # noqa: E402

ROOT = g.find_repo_root()
NAMES, IDS, DOMAINS = g.load_migrated(ROOT)

# Alvos reais esperados (falha cedo se o repo mudou de forma incompativel).
WEBINAR_PROJ = "buzzmonitor-lp-monitoramento-concorrentes"
WEBINAR_ID = "prj_bqOBy4RXCnPFu8Fn7csQ6wzyjwb6"
assert WEBINAR_PROJ in NAMES, "manifesto do webinar mudou de nome de projeto?"
assert WEBINAR_ID in IDS, "manifesto do webinar mudou de projectId?"
assert "webinar.buzzmonitor.com" in DOMAINS

_failures = []


def check(desc, tool_name, tool_input, expected, cwd="", override=False):
    res = g.evaluate(tool_name, tool_input, cwd, ROOT, override=override)
    got = res["action"]
    ok = got == expected
    print(("  ok  " if ok else "FAIL ") + desc + "  -> " + got +
          ("" if ok else "  (esperado " + expected + ")"))
    if not ok:
        _failures.append(desc)


def bash(cmd):
    return ("Bash", {"command": cmd})


SCOPE = "--scope team_nC991VqUuSU2jXZN152xqqEg"

# 1. Vetor EXATO do incidente: cd na sibling do projeto migrado -> DENY.
check("incidente: cd sibling migrado + vercel deploy",
      *bash('cd "/c/Users/x/lp-siblings/%s" && npx --yes vercel deploy --prod --yes %s'
            % (WEBINAR_PROJ, SCOPE)),
      expected="deny")

# 2. Dominio migrado citado no comando -> DENY.
check("dominio migrado no comando",
      *bash('npx vercel deploy --prod %s  # alias webinar.buzzmonitor.com' % SCOPE),
      expected="deny")

# 3. projectId migrado citado -> DENY.
check("projectId migrado no comando",
      *bash('vercel deploy --prod --project %s %s' % (WEBINAR_ID, SCOPE)),
      expected="deny")

# 4. Filesystem: cd num dir com .vercel/project.json de projeto migrado -> DENY,
#    mesmo sem nome/dominio no comando (path do tmp nao contem termo migrado).
with tempfile.TemporaryDirectory() as td:
    os.makedirs(os.path.join(td, ".vercel"))
    with open(os.path.join(td, ".vercel", "project.json"), "w", encoding="utf-8") as fh:
        json.dump({"projectId": WEBINAR_ID, "orgId": "team_x"}, fh)
    check("filesystem: .vercel/project.json migrado via cd",
          *bash('cd "%s" && npx --yes vercel deploy --prod --yes' % td),
          expected="deny")

    # 4b. Mesmo dir, override ativo -> vira ASK (escape consciente).
    check("override converte deny migrado em ask",
          *bash('cd "%s" && npx --yes vercel deploy --prod --yes' % td),
          expected="ask", override=True)

# 5. Projeto SOLO (nao migrado) -> ASK (comportamento legado preservado).
check("solo nao-migrado + vercel deploy",
      *bash('cd "/c/Users/x/buzzmonitor-lp-social-listening-julho" && npx vercel deploy %s' % SCOPE),
      expected="ask")

# 6. Boundary anti-FP: nome migrado como PREFIXO de um maior -> NAO deny.
check("boundary: 'buzzmonitor-content-latam' nao casa 'buzzmonitor-content'",
      *bash('cd "/c/Users/x/buzzmonitor-content-latam" && npx vercel deploy %s' % SCOPE),
      expected="ask")

# 7. Read-only Vercel -> passthrough.
check("vercel whoami (read-only)", *bash('npx vercel whoami %s' % SCOPE), expected="pass")
check("vercel alias ls (read-only)", *bash('npx vercel alias ls %s' % SCOPE), expected="pass")

# 8. Comando sem vercel -> passthrough.
check("comando nao-vercel", *bash('echo "webinar.buzzmonitor.com deploy"'), expected="pass")

# 9. MCP deploy_to_vercel mirando projeto migrado (via input) -> DENY.
check("MCP deploy_to_vercel migrado",
      "mcp__abc__deploy_to_vercel", {"project": WEBINAR_PROJ}, expected="deny")

# 10. MCP deploy_to_vercel sem sinal de migrado -> ASK.
check("MCP deploy_to_vercel generico",
      "mcp__abc__deploy_to_vercel", {"path": "/tmp/algum-projeto-solo"}, expected="ask")

print()
if _failures:
    print("FALHOU: %d caso(s) -> %s" % (len(_failures), ", ".join(_failures)))
    sys.exit(1)
print("todos os casos passaram")
