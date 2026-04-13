---
name: meta-ads-trends
description: Análise focada em tendências temporais de Meta Ads — CpL melhorando? CTR caiu nos últimos 7 dias? Frequência subindo? Compara janelas 7d/15d/30d.
argument-hint: "[conta] — ex: buzzmonitor_brl | cxpress_usd"
allowed-tools: Bash, Read, mcp__claude_ai_Notion__notion-create-pages
version: 1.0.0
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
| hook_rate *(vídeo)* | 7d/15d/30d | Alta | SUM(video_p25)/SUM(impressões) |
| completion_rate *(vídeo)* | 7d/15d/30d | Alta | SUM(video_p100)/SUM(impressões) |

## Legenda
- **Tendência recente**: compara janela 7d vs 15d
- **Tendência estrutural**: compara janela 15d vs 30d
- Limiar de variação: ±10% para classificar como Alta/Queda (abaixo = Estável)
- Métricas derivadas sempre calculadas sobre somas do período — nunca como média de médias diárias
- Métricas de vídeo aparecem apenas para anúncios com dados de vídeo (video_p25 > 0)

---

## Diagnóstico Cruzado (obrigatório após as tabelas)

**O CpL é o indicador mestre.** As outras métricas explicam *por que* o CpL está onde está — e o que fazer.

Após apresentar as tabelas de tendência, sempre executar o diagnóstico cruzado para cada entidade com dados suficientes (7d+), usando os valores de 30d como base absoluta e as tendências recentes como direção.

### Matriz de Cenários

| Cenário | CpL | CTR | Conv. LP | Diagnóstico | Ação recomendada |
| --- | --- | --- | --- | --- | --- |
| 🏆 **Ouro** | Bom + ↓ | Bom | Boa | Tudo funcionando e melhorando | Escalar budget. **Marcar como referência de criativo.** |
| 🔵 **Filtro natural** | Bom | Ruim | Boa | CTR baixo mas quem clica converte. O criativo filtra a audiência com qualidade. Pode ser que o hook seja nichado — proposital. | Manter. Testar variação com hook mais amplo mantendo o mesmo ângulo. |
| ⚠️ **Gargalo de LP** | Bom | Bom | Ruim | Ad atrai e converte bem *por enquanto*, mas Conv. LP baixa é um teto de escala. A LP não sustenta o volume. | Otimizar LP antes de escalar. Verificar alinhamento entre promessa do ad e conteúdo da LP. |
| 🚨 **Promessa × entrega** | Ruim | Bom | Ruim | CTR alto = criativo atrai curiosidade/cliques. LP não entrega. Dois diagnósticos possíveis: (1) a LP não reflete o que o ad promete; (2) o ad promete algo que o produto não resolve. | Auditar LP: ela espelha o ângulo do ad? Se sim, o problema é o ângulo — o produto não fecha essa promessa. Se não, alinhar LP ao criativo. **Ângulo pode ser reaproveitado com nova LP.** |
| 🔄 **Potencial travado** | Ruim | Bom | Boa | Ad atrai e LP converte — mas leads são poucos. Pode ser orçamento baixo, audiência pequena ou dados insuficientes. | Checar volume de impressões. Se audiência estiver ampla, aumentar budget. |
| 💀 **Substituir** | Ruim | Ruim | Ruim/— | Criativo não atrai, LP não converte. Nada funciona. | Pausar. Não investir mais sem criativo novo. |
| ❓ **Sem dados** | — | — | — | Leads insuficientes (0 ou 1) para diagnóstico confiável. CpL pontual não é estatisticamente válido. | Aguardar mais dados antes de agir. |

### Regras de aplicação

1. **Leads insuficientes**: se os leads nos últimos 7d forem ≤ 2, o CpL do período curto é ruído estatístico — informar ao usuário e usar o 30d como base.
2. **CTR em contexto**: para anúncios de remarketing, o CTR esperado é maior que prospecção (audiência quente). Um CTR baixo em remarketing é mais grave do que o mesmo valor em prospecção.
3. **Conv. LP ausente**: se não houver dados de Conv. LP, focar no binômio CpL + CTR para o diagnóstico.
4. **CPM alto isolado**: CPM alto sem impacto no CpL (CpL bom) não é problema — é característica do segmento. Reportar como observação, não como alerta.
5. **Tendência > valor absoluto**: um CpL de R$ 300 caindo para R$ 150 em 7d é mais saudável que um CpL de R$ 100 subindo para R$ 200. A direção importa mais que o snapshot.

### Diagnóstico para vídeos (quando hook_rate e completion_rate disponíveis)

| hook_rate (25%) | completion_rate (100%) | Diagnóstico |
| --- | --- | --- |
| < 15% | qualquer | Hook fraco — primeiros 3 segundos não prendem. Testar novo frame de abertura ou primeira frase. |
| > 30% | < 5% | Início forte, retenção cai — vídeo perde o espectador no meio. Problema de ritmo ou CTA tardio. |
| > 30% | > 10% | Vídeo forte. Se CpL ruim, problema está na LP ou no ângulo, não no criativo em si. |
| qualquer | > 15% | Retenção excelente — público engajado. Se CpL ruim, investigar LP. |

---

## Criativos de Referência

Ao final do diagnóstico, sempre listar os **criativos de referência** — aqueles cujo CpL está no melhor quartil do grupo analisado (ou abaixo do benchmark da conta):

```
### Criativos de Referência (para gerar variações)

| Criativo | CpL 30d | CTR | Conv. LP | Por que é referência |
| --- | --- | --- | --- | --- |
| [nome] | R$ X | X% | X% | [cenário aplicável] |
```

Esses criativos devem ser usados como base para novas variações: **mesmo ângulo, mesmo posicionamento, nova execução visual ou novo hook**. Informar isso explicitamente ao usuário.

---

## Passo final — Publicar no Notion (opcional)

Após apresentar a análise, perguntar ao usuário:

> "Deseja subir este relatório de tendências no Notion?"

Se sim:
1. Criar uma página com `mcp__claude_ai_Notion__notion-create-pages` com parent `33b3934026fd80ceb414dd22cb7dbe1f` (pasta Entregas — ID fixo, não buscar) contendo:
   - **Título:** `Tendências Meta Ads — [conta] — [data]`
   - **Conteúdo:** a análise completa apresentada ao usuário (tabelas + diagnóstico + resumo executivo)
