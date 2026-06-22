# Skills Desativadas

Skills que estavam ativas em `.claude/skills/` mas foram tiradas de circulacao. Ficam aqui por referencia historica e pra facilitar reativacao caso a decisao seja revertida.

Claude Code so carrega skills de `.claude/skills/` — pastas aqui dentro **NAO** sao descobertas pelo agente. Pra reativar, basta `git mv` de volta.

## Skills aqui

### Pipeline `meta-ads-*` (desativado em 2026-06-22)

Substituido por `/bunzzai` + `/bunzzai-geral` (fonte unica via MCP Bunzzai).

| Skill | O que fazia | Substituto |
|---|---|---|
| `meta-ads` | Pipeline completo (fetch + report) por conta via API Meta direta | `/bunzzai [conta]` |
| `meta-ads-fetch` | Atualizar dados locais (SQLite) sem gerar relatorio | (nao tem — Bunzzai e tempo real via MCP) |
| `meta-ads-report` | Re-gerar relatorio do banco local sem nova coleta | (nao tem — Bunzzai e tempo real) |
| `meta-ads-trends` | Tendencias 3d/7d/15d/30d por conta | `/bunzzai [conta]` (cobre 7d/15d/30d) |
| `meta-ads-geral` | Consolidado das 6 contas no Notion | `/bunzzai-geral` |

**Por que foi desativado:** decisao 2026-06-22 (Victor) — colegas devem rodar analises somente via Bunzzai (CRM proprio, sem dependencia de token Meta que expira a cada ~60 dias). Mantemos os scripts originais aqui caso precise auditar discrepancia entre Bunzzai e Meta API direta.

**Pasta auxiliar:** `meta-ads-legacy/` (raiz do repo) tem os scripts Python originais (`fetch_*.py`, `full_analysis.py`, `trend_analyzer.py`, etc.) e relatorios historicos.

**Pasta ativa:** `meta-ads/` continua existindo no raiz com apenas o que o bunzzai usa: `CONTEXT.md` (matriz de cenarios, classificacao de campanhas) + `data/benchmarks.json` (thresholds calibrados por moeda × tipo de campanha).

## Como reativar

```bash
git mv .claude/skills-desativadas/meta-ads        .claude/skills/meta-ads
# ... etc por skill
```

E restaurar os scripts:

```bash
git mv meta-ads-legacy/scripts meta-ads/scripts
# ... etc
```
