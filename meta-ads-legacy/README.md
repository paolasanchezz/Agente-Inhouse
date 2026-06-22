# meta-ads-legacy/ — scripts e historico arquivados

Pasta criada em 2026-06-22 com tudo da antiga `meta-ads/` que **nao e mais usado no fluxo ativo**. Substituido por `/bunzzai` + `/bunzzai-geral` (analises via MCP Bunzzai, sem dependencia de token Meta).

## Conteudo

| Item | O que e | Quando usar |
|---|---|---|
| `scripts/` | Pipeline Python original (fetch_campaigns, fetch_insights, full_analysis, trend_analyzer, report_generator, etc.) | Auditoria pontual quando precisar comparar Bunzzai vs Meta API direta. Ver `scripts/audit_vs_bunzzai.py`. |
| `scripts/stress_test_bunzzai.py` | Prova que a estrategia de diff de snapshots do Bunzzai bate com Meta diaria | Referencia tecnica — citada no `.claude/skills/bunzzai/CONTEXT.md` |
| `reports/` | Relatorios Markdown historicos (abril/maio 2026) | Lookback de comparativos passados |
| `cache/` | Cache HTTP da Meta API (gitignored) | Provavelmente stale — limpar antes de reusar |
| `meta_ads.db` | Banco SQLite local com campanhas + insights diarios (gitignored) | Stale — reativar so apos novo fetch |
| `SETUP.md` | Instrucoes de configuracao do `META_ACCESS_TOKEN` | Reativacao do pipeline antigo |
| `requirements.txt` | Dependencias Python (requests, facebook-business, etc.) | Reativacao do pipeline antigo |
| `credentials-snapshot.md` | Snapshot historico de credenciais | Auditoria |

## Como reativar (caso necessario)

1. Restaurar skills:
   ```bash
   git mv .claude/skills-desativadas/meta-ads        .claude/skills/meta-ads
   git mv .claude/skills-desativadas/meta-ads-fetch  .claude/skills/meta-ads-fetch
   # ... idem pro resto
   ```
2. Restaurar scripts e infraestrutura:
   ```bash
   git mv meta-ads-legacy/scripts meta-ads/scripts
   git mv meta-ads-legacy/SETUP.md meta-ads/SETUP.md
   git mv meta-ads-legacy/requirements.txt meta-ads/requirements.txt
   mv meta-ads-legacy/cache meta-ads/data/cache
   mv meta-ads-legacy/meta_ads.db meta-ads/data/meta_ads.db
   ```
3. Renovar token: `meta-ads/SETUP.md` tem o passo-a-passo.
4. Atualizar `CLAUDE.md` e advisor `/anuncios`.

## Por que ficou separado

Os scripts ainda compilam e funcionam — so estao fora do fluxo padrao. Manter aqui (em vez de apagar) permite:
- Auditorias Bunzzai vs Meta sem ressuscitar a skill inteira
- Reativacao rapida se o Bunzzai virar gargalo
- Historico de relatorios passados pra comparativos
