# Pasta meta-ads/ — enxuta

Sobrou aqui apenas o que `/bunzzai` ainda usa:

| Arquivo | Pra que serve |
|---|---|
| `data/benchmarks.json` | Thresholds de CpL/CTR/Conv.LP por moeda × tipo de campanha — referenciado pela skill bunzzai pra classificar metricas como `[OK]`/`[RUIM]` |

## O que saiu daqui

As skills `meta-ads-*` foram desativadas em 2026-06-22 (decisao Victor — analises devem rodar via `/bunzzai`, sem dependencia de token Meta que expira a cada ~60 dias).

| Arquivo / pasta | Foi pra |
|---|---|
| `scripts/` (fetch_*.py, full_analysis.py, trend_analyzer.py, etc.) | `meta-ads-legacy/scripts/` |
| `data/reports/` (relatorios historicos) | `meta-ads-legacy/reports/` |
| `data/cache/` + `data/meta_ads.db` | `meta-ads-legacy/` |
| `SETUP.md` (token Meta) | `meta-ads-legacy/SETUP.md` |
| `requirements.txt` | `meta-ads-legacy/requirements.txt` |
| `.claude/skills/meta-ads*/` (5 skills) | `.claude/skills-desativadas/` |

Pra reativar tudo: ver `.claude/skills-desativadas/README.md`.

## Sobre o `.env`

O `meta-ads/.env` (com `META_ACCESS_TOKEN`) **nao e mais necessario** pra analises do dia-a-dia. Pode permanecer pra auditorias pontuais via `meta-ads-legacy/scripts/audit_vs_bunzzai.py`, mas o token nao precisa estar fresh.
