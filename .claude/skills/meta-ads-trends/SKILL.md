---
name: meta-ads-trends
description: Análise focada em tendências temporais de Meta Ads — CpL melhorando? CTR caiu nos últimos 7 dias? Frequência subindo? Compara janelas 7d/15d/30d.
argument-hint: "[conta] — ex: buzzmonitor_brl | cxpress_usd"
allowed-tools: Bash, Read, mcp__claude_ai_Notion__notion-create-pages
---

# Skill: /meta-ads-trends — Análise de Tendências

> Leia `.claude/skills/meta-ads/CONTEXT.md` antes de prosseguir.

## Quando usar
Quando o usuário quer focar especificamente em tendências temporais de métricas —
se o CpL está melhorando, se o CTR caiu nos últimos 7 dias, se a frequência está subindo, etc.

---

## Fluxo

### 1. Garantir dados atualizados no banco
Se necessário, coletar primeiro:
```bash
cd meta-ads
python scripts/fetch_insights.py --account [conta] --period ultimos_30
```

### 2. Análise de tendências via Python
```bash
cd meta-ads
python - <<'EOF'
import sys
sys.path.insert(0, 'scripts')
from trend_analyzer import calculate_trends, format_trends_table
from cache_manager import get_campaigns, ACCOUNTS

account_key = "[conta]"
account = ACCOUNTS[account_key]
campaigns = get_campaigns(account_key)

for camp in campaigns:
    print(f"\n### {camp['name']}")
    trends = calculate_trends(camp["id"], "campaign", account_key)
    print(format_trends_table(trends, account["currency_symbol"]))
EOF
```

---

## Métricas de tendência disponíveis
| Métrica | Janelas | Direção positiva | Cálculo |
| --- | --- | --- | --- |
| spend | 7d/15d/30d | Caindo (custo menor) | SUM |
| leads | 7d/15d/30d | Alta | SUM |
| link_clicks | 7d/15d/30d | Alta | SUM |
| ctr_link | 7d/15d/30d | Alta | SUM(cliques)/SUM(impressões) |
| cost_per_lead | 7d/15d/30d | Caindo | SUM(spend)/SUM(leads) |
| cpm | 7d/15d/30d | Caindo | SUM(spend)/SUM(impressões)×1000 |
| cpc_link | 7d/15d/30d | Caindo | SUM(spend)/SUM(cliques) |
| frequency | 7d/15d/30d | Caindo | SUM(impressões)/SUM(alcance) |
| lp_conversion_rate | 7d/15d/30d | Alta | SUM(leads)/SUM(cliques) |

## Legenda
- **Tendência recente**: compara janela 7d vs 15d
- **Tendência estrutural**: compara janela 15d vs 30d
- Limiar de variação: ±10% para classificar como Alta/Queda (abaixo = Estável)
- Métricas derivadas sempre calculadas sobre somas do período — nunca como média de médias diárias

---

## Passo final — Publicar no Notion (opcional)

Após apresentar a análise, perguntar ao usuário:

> "Deseja subir este relatório de tendências no Notion?"

Se sim:
1. Criar uma página com `mcp__claude_ai_Notion__notion-create-pages` com parent `33b3934026fd80ceb414dd22cb7dbe1f` (pasta Entregas — ID fixo, não buscar) contendo:
   - **Título:** `Tendências Meta Ads — [conta] — [data]`
   - **Conteúdo:** a análise completa apresentada ao usuário (tabelas + diagnóstico + resumo executivo)
