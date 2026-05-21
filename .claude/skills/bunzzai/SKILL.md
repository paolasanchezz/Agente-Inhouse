---
name: bunzzai
description: Analise de tendencias de Meta Ads via MCP do Bunzzai (snapshots cumulativos). Drill-down Conta -> Campanha -> Adset -> Ad com diff de janelas 7d/15d/30d, diagnostico cruzado (CpL × CTR × Conv. LP) e detecao de cron travado. Aceita apenas contas Buzzmonitor e Cxpress.
argument-hint: "[conta] — ex: buzzmonitor_brl | cxpress_eur"
allowed-tools: Bash, Read, mcp__claude_ai_Notion__notion-create-pages
version: 1.0.0
---

# Skill: /bunzzai — Analise via MCP Bunzzai

> Leia `.claude/skills/bunzzai/CONTEXT.md` antes de prosseguir.
> Leia `.claude/skills/meta-ads/CONTEXT.md` para benchmarks compartilhados.

## Quando usar

- O usuario quer analisar performance de uma conta Buzzmonitor ou Cxpress usando dados do **Bunzzai** (CRM proprio com snapshots acumulados), nao da Meta API.
- Quer cross-check rapido contra o que `/meta-ads-trends` mostra.
- Quer rastrear cron travado do Bunzzai por ad (snapshots congelados).

## Nao usar quando

- A conta nao for Buzzmonitor ou Cxpress (recusar — Bunzzai cobre outros clientes do CRM, mas estao fora do escopo desta skill).
- O usuario quer dados crus diarios da Meta -> use `/meta-ads-fetch` + `/meta-ads-trends`.
- O usuario quer comparativo entre Bunzzai e Meta API -> rodar `/meta-ads-trends` em paralelo e comparar manualmente (ou pedir orquestracao explicita).

## Restricao Absoluta

**SOMENTE LEITURA.** Nunca chamar tools de escrita do MCP Bunzzai. Apenas tools que comecam com `tool_get_*`, `tool_find_*`, `list_*`, `get_*_insights`, `tool_get_ad_performance`, `tool_get_campaign_monitoring`, `compare_*`, `search_entity`. Nunca pausar, editar, criar ou aprovar nada.

---

## Inputs — confirmar com o usuario antes de iniciar

### 1. Conta (obrigatorio)

```
buzzmonitor_brl | buzzmonitor_usd | buzzmonitor_eur
cxpress_brl     | cxpress_usd     | cxpress_eur
```

Se vier vazio, perguntar com chips clicaveis. Se vier conta fora dessa lista, recusar e explicar que a skill so cobre Elife.

---

## Fluxo de Execucao

### Passo 1 — Resolver empresa no Bunzzai

```
mcp__bunzzai__tool_find_company(query="Buzzmonitor")  # ou "Cxpress"
```

Pegar o `company_id` do match com maior confianca. Se houver multiplos (improvavel, mas vale checar), preferir o que tenha `confidence > 0.9` no `matched_by="exact"`.

**Cache mental:** anotar o `company_id` resolvido — vai ser usado nos proximos passos. Nao chamar `find_company` de novo.

### Passo 2 — Listar campanhas e filtrar por moeda

```
mcp__bunzzai__list_campaigns(company_id=<id>)
```

Filtrar pelo nome conforme heuristica do CONTEXT.md (`buzzmonitor_brl` -> sem token de pais ou com "BR"; `_usd` -> "Latam"/"USD"; `_eur` -> "Portugal"/"EU"/"PT"). Se nenhuma campanha filtrar, **listar todas e perguntar ao usuario quais incluir** — nunca chutar.

Para cada campanha filtrada, anotar:
- `id`, `name`, `status`, `type` classificado (webinar / material_rico / remarketing / nao_classificada — ver tabela do CONTEXT.md)

### Passo 3 — Drill-down por campanha: adsets e ads

Para cada campanha filtrada:

```
mcp__bunzzai__list_campaign_ads(campaign_id=<id>)
```

Anotar lista de adsets e ads (cada ad com seu `id` interno do Bunzzai).

### Passo 4 — Historico de monitoramento por ad

Para cada ad:

```
mcp__bunzzai__tool_get_ad_performance(ad_id=<id>)
```

Resposta tem `monitoring_history`: lista de snapshots com `(timestamp, spend, impressions, clicks, ctr, cpc, cpm, frequency, conversions)` — todos **acumulados desde o inicio da campanha**.

### Passo 5 — Calcular janelas 7d / 15d / 30d via diff de snapshots

Para cada ad, rodar Python embed:

```bash
cd meta-ads
python - <<'EOF'
import json, sys, datetime as dt
from pathlib import Path

# Cole aqui o JSON de monitoring_history vindo do MCP (lista de snapshots).
HIST = json.loads(sys.stdin.read())

# Ordenar por data (snapshots vem geralmente em ordem, mas garantir)
HIST.sort(key=lambda s: s["timestamp"][:10])
by_date = {s["timestamp"][:10]: s for s in HIST}

today = dt.date.today()  # ou data passada pelo agente
end_date = today - dt.timedelta(days=1)  # ontem (dia completo)

def nearest_before(target_date):
    """Snapshot mais proximo anterior a target_date (inclusive)."""
    for d in sorted(by_date.keys(), reverse=True):
        if d <= target_date.isoformat():
            return by_date[d]
    return None

def window(days):
    start_date = today - dt.timedelta(days=days+1)  # dia anterior ao inicio da janela
    s_end = nearest_before(end_date)
    s_start = nearest_before(start_date)
    if not s_end or not s_start:
        return None
    return {
        "spend":       float(s_end["spend"])       - float(s_start["spend"]),
        "impressions": int(s_end["impressions"])   - int(s_start["impressions"]),
        "clicks":      int(s_end["clicks"])        - int(s_start["clicks"]),
        "conversions": int(s_end["conversions"])   - int(s_start["conversions"]),
    }

def derived(w):
    if not w: return None
    spend, imp, cli, conv = w["spend"], w["impressions"], w["clicks"], w["conversions"]
    return {
        "spend": round(spend, 2),
        "impressions": imp,
        "clicks": cli,
        "conversions": conv,
        "cpl": round(spend/conv, 2)        if conv else 0,
        "ctr": round(cli/imp*100, 2)       if imp  else 0,
        "conv_lp": round(conv/cli*100, 2)  if cli  else 0,
        "cpc": round(spend/cli, 2)         if cli  else 0,
        "cpm": round(spend/imp*1000, 2)    if imp  else 0,
    }

def frozen_streak():
    """Retorna (n_dias_congelados, data_inicio_congelamento) — checa janela de 30d."""
    last = None; streak = 0; start = None
    for d in sorted(by_date.keys()):
        if today.isoformat() < d or (today - dt.date.fromisoformat(d)).days > 30:
            continue
        s = by_date[d]
        key = (s["spend"], s["impressions"], s["clicks"], s["conversions"])
        if last == key:
            streak += 1
            if not start: start = d
        else:
            if streak >= 2:  # 2+ snapshots iguais = travado
                return streak, start
            streak = 0; start = None; last = key
    return (streak, start) if streak >= 2 else (0, None)

trends = {
    "7d":  derived(window(7)),
    "15d": derived(window(15)),
    "30d": derived(window(30)),
}
streak, start = frozen_streak()
print(json.dumps({"trends": trends, "frozen": {"days": streak, "since": start}}, indent=2))
EOF
```

Passar o `monitoring_history` via stdin. O script entrega trends + alerta de cron travado.

### Passo 6 — Classificar tendencia (recente vs estrutural)

Para cada metrica e cada par de janelas:

```
trend_recente   = compare(7d,  15d)   # variacao > +10% -> Alta | < -10% -> Queda | senao -> Estavel
trend_estrutural= compare(15d, 30d)   # mesmas regras
```

Direcao positiva (Alta = bom): `conversions`, `clicks`, `ctr`, `conv_lp`, `impressions`
Direcao negativa (Alta = ruim): `cpl`, `cpm`, `cpc`

Se cron travado intersecta a janela 7d:
- Marcar `trend_recente = "[cron travado] N/A"`
- Usar 15d como `recente` no diagnostico, comparando 15d vs 30d.

### Passo 7 — Aplicar benchmarks e diagnostico cruzado

Para cada entidade com `dados_suficientes` (conversoes ≥ 3 na maior janela usada como base):

1. **Status de cada metrica** vs benchmark da moeda × tipo de campanha (ver `meta-ads/data/benchmarks.json`):
   - `cost_per_lead` ≤ threshold -> `[OK]`, senao `[RUIM]`
   - `ctr` ≥ threshold -> `[OK]`, senao `[RUIM]`
   - `conv_lp` ≥ threshold -> `[OK]`, senao `[RUIM]`

2. **Cenario** aplicando a matriz do CONTEXT.md (Ouro / Filtro natural / Gargalo de LP / Promessa × entrega / Potencial travado / Substituir / Sem dados).

3. **Acao recomendada** conforme cenario.

### Passo 8 — Apresentar relatorio

Estrutura:

```markdown
# Bunzzai — Tendencias [Conta] — YYYY-MM-DD

## Resumo Executivo
- Empresa Bunzzai: <nome> (company_id=<id>)
- Conta mapeada: <chave>  |  Moeda: <simbolo>
- Campanhas analisadas: <N>  |  Adsets: <N>  |  Ads: <N>
- Ads com cron travado: <N> (listar quais)
- Distribuicao de cenarios (em campanhas):
  - 🏆 Ouro: <N> | 🔵 Filtro natural: <N> | ⚠️ Gargalo LP: <N> | ...

## >> [Tipo de funil] — [Topo / Fundo / Nao classificadas]

### Campanha: <nome> [<tipo classificado>]
<tabela: Metrica | 30d | 15d | 7d | Tend. Recente | Tend. Estrutural>

#### Adset: <nome>
<tabela trends>

##### Ad: <nome>  <[CRON TRAVADO: N dias congelados a partir de YYYY-MM-DD] se aplicavel>
<tabela trends>

#### Diagnostico — Campanha <nome>
| CpL | CTR | Conv. LP | Cenario | Acao |
|---|---|---|---|---|
| [OK/RUIM] valor | [OK/RUIM] valor | [OK/RUIM] valor | 🏆 Ouro | Escalar... |

## Avisos
- <Cron travado em X ads, listar quais e desde quando>
- <Campanhas nao classificadas (revisar nome)>
- <Janelas com dados insuficientes>

## Cross-check sugerido
Quando o CpL Bunzzai estiver perto do limite ([OK] mas dentro de ~20% do threshold) ou quando a decisao for >R$ 1.000 movimentados, rodar `/meta-ads-trends <conta>` e comparar — Bunzzai conta cliques totais e conversoes amplas, enquanto a skill meta-ads usa link_clicks + leads custom.
```

### Passo 9 — Publicar no Notion (opcional)

Perguntar:

> "Deseja publicar este relatorio Bunzzai no Notion?"

Se sim:
1. Ler `conhecimento/config/notion-ids.md`, pegar o ID da chave `entregas`.
2. Criar pagina com `mcp__claude_ai_Notion__notion-create-pages`:
   - **parent**: ID da chave `entregas` — fixo, nao buscar
   - **title**: `Bunzzai — Tendencias <conta> — <YYYY-MM-DD>`
   - **content**: relatorio completo apresentado
3. Confirmar com link da pagina criada.

---

## Regras de Apresentacao

- Todos os valores monetarios usam o simbolo da moeda da conta (R$, $ ou €).
- Se um ad tem conversoes < 3 na janela 30d: marcar `[ ] Sem dados — aguardar acumular`. Nunca diagnosticar.
- Cron travado: badge `[CRON TRAVADO: N dias congelados desde YYYY-MM-DD]` aparece DIRETO ao lado do nome do ad afetado, no cabecalho da subsecao.
- Nunca inventar dados — sempre citar a fonte (MCP Bunzzai, `tool_get_ad_performance` para metricas, `tool_find_company`/`list_campaigns` para estrutura).
- Quando reportar "Ouro" para um ad: ressaltar que a metrica e do Bunzzai (cliques totais e conversoes amplas) e sugerir confirmar com `/meta-ads-trends` antes de escalar budget.
- Adsets com `spend_30d = 0` ou ads com `(spend_30d = 0 OR conversions_30d < 1)` podem ser omitidos do relatorio detalhado — incluir no contador do rodape "<N> adsets/ads omitidos por baixo volume".

---

## Comportamento de erro

- **Empresa nao encontrada no Bunzzai** -> alertar que a marca pode nao estar cadastrada e abortar.
- **Nenhuma campanha encontrada apos filtro de moeda** -> listar todas as campanhas da empresa e pedir confirmacao.
- **Ad sem `monitoring_history`** -> reportar "Sem snapshots — nao analisavel" e seguir nos demais.
- **Snapshots todos congelados (>30 dias)** -> reportar "Cron sem atualizacao ha mais de 30 dias — pedir engenharia destravar" e abortar a entidade especifica.

---

## Diferencas vs `/meta-ads-trends`

| Aspecto | `/meta-ads-trends` | `/bunzzai` |
|---|---|---|
| Fonte | Meta API + cache SQLite local | MCP Bunzzai (snapshots cumulativos) |
| Granularidade temporal | Diaria | Diaria (reconstituida via diff) |
| Cliques | `link_clicks` (so link) | `clicks` totais |
| Conversoes | `leads` (pixel custom) | `conversions` (todas do pixel) |
| Reach / Frequencia | Disponivel | Pode faltar |
| Video metrics | hook_rate + completion_rate | Nao expostas |
| Cron-travado | Nao aplicavel | Detecta e alerta |
| Cobre quais marcas | Buzzmonitor + Cxpress (todos paises) | Buzzmonitor + Cxpress (todos paises) — mesma cobertura, fonte alternativa |

**Quando preferir Bunzzai:** o usuario quer dado vivo sem rodar fetch da Meta (token Meta expirou, contornar rate limit, validacao cruzada).

**Quando preferir meta-ads-trends:** decisao final de budget, comparacao com benchmarks calibrados, video metrics.
