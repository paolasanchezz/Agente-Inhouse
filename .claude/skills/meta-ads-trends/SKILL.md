# Skill: /meta-ads-trends — Análise de Tendências

## Quando usar
Quando o usuário quer focar especificamente em tendências temporais de métricas —
se o CpL está melhorando, se o CTR caiu nos últimos 3 dias, se a frequência está subindo, etc.

## Restrição Absoluta
**SOMENTE LEITURA.** Zero chamadas à Meta API — apenas leitura do banco local.

---

## Fluxo

### 1. Garantir dados atualizados no banco
Se necessário, coletar primeiro:
```bash
cd meta-ads
python scripts/fetch_insights.py --account [conta] --period ultimos_30
```

### 2. Análise de tendências via Python interativo ou relatório
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
    if camp.get("status") != "ACTIVE":
        continue
    print(f"\n### {camp['name']}")
    trends = calculate_trends(camp["id"], "campaign", account_key)
    print(format_trends_table(trends, account["currency_symbol"]))
EOF
```

---

## Métricas de tendência disponíveis
| Métrica | Janelas | Direção positiva |
| --- | --- | --- |
| spend | 3d/7d/15d/30d | ↓ Caindo (custo menor) |
| leads | 3d/7d/15d/30d | ↑ Alta |
| link_clicks | 3d/7d/15d/30d | ↑ Alta |
| ctr_link | 3d/7d/15d/30d | ↑ Alta |
| cost_per_lead | 3d/7d/15d/30d | ↓ Caindo |
| cpm | 3d/7d/15d/30d | ↓ Caindo |
| frequency | 3d/7d/15d/30d | ↓ Caindo |
| lp_conversion_rate | 3d/7d/15d/30d | ↑ Alta |

## Legenda
- **Tendência recente**: compara janela 3d vs 7d (variação dos últimos 3 dias)
- **Tendência estrutural**: compara janela 7d vs 30d (tendência de médio prazo)
- Limiar de variação: ±10% para classificar como Alta/Queda (abaixo = Estável)
