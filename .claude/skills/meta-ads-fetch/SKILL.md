# Skill: /meta-ads-fetch — Atualização de Dados

## Quando usar
Quando o usuário quer só atualizar os dados locais sem gerar relatório,
ou antes de uma análise manual dos dados brutos no banco.

## Restrição Absoluta
**SOMENTE LEITURA.** Apenas GET na Meta Marketing API.

---

## Fluxo

### Atualizar estrutura (campanhas → adsets → ads)
```bash
cd meta-ads
python scripts/fetch_campaigns.py --account [conta] --incremental
```

### Atualizar insights para um período
```bash
cd meta-ads
python scripts/fetch_insights.py --account [conta] --period [mes_atual|mes_anterior|ultimos_30]
```

### Ambos em sequência
```bash
cd meta-ads
python scripts/fetch_campaigns.py --account [conta] --incremental && \
python scripts/fetch_insights.py --account [conta] --period [periodo]
```

---

## Comportamento incremental (by design)
- Campanhas inativas já no banco são ignoradas automaticamente
- Datas de insights já presentes no banco não geram nova chamada à API
- Dados de hoje nunca são coletados (dia incompleto)
- Se a saída indicar "0 novas linhas inseridas", é correto — dados já estavam no cache

## Contas válidas
```
buzzmonitor_brl | buzzmonitor_usd | buzzmonitor_eur
cxpress_brl     | cxpress_usd     | cxpress_eur
```
