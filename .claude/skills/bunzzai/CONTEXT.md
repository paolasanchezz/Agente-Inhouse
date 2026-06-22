# Contexto Compartilhado — Bunzzai

> Este arquivo e lido pela skill `/bunzzai` antes de qualquer acao.

---

## Restricao Absoluta

**SOMENTE LEITURA.** Nunca chamar tools de escrita do MCP Bunzzai (criacao/edicao/pausa de campanha, adset, ad ou creative). Apenas tools `tool_get_*`, `list_*`, `tool_find_*`, `get_*_insights`, `tool_get_ad_performance`, `tool_get_campaign_monitoring`, `compare_*`, `search_entity`. Nada que altere estado.

---

## Fonte de dados — diferenca crucial vs Meta API

O Bunzzai **nao entrega dados diarios**. Ele entrega **snapshots cumulativos** — uma fotografia por dia do total acumulado de cada metrica desde o inicio da campanha.

Para reconstituir uma janela:
- `janela(X dias) = snapshot(ontem) - snapshot(ontem - X dias)`
- 7d = snapshot(hoje-1) − snapshot(hoje-8)
- 15d = snapshot(hoje-1) − snapshot(hoje-16)
- 30d = snapshot(hoje-1) − snapshot(hoje-31)

Se um snapshot de borda nao existir exatamente nessa data (raro mas acontece), usar o **mais proximo anterior** dentro da janela.

### Snapshot congelado (cron travado)
Se dois ou mais snapshots consecutivos tem o mesmo acumulado em todas as metricas (spend, impressions, clicks, conversions identicos), o cron do Bunzzai esta travado naquela janela.

Comportamento (decidido com Victor 2026-05-19):
1. **Detectar** snapshots congelados consecutivos por ad.
2. **Alertar** no relatorio com badge explicito: `[CRON TRAVADO: N dias congelados a partir de YYYY-MM-DD]`.
3. **Seguir com a analise** das janelas nao contaminadas. Se 7d esta contaminada mas 15d e 30d nao, basear diagnostico em 15d/30d e marcar 7d como "dado nao confiavel".
4. Nunca alterar dados — so reportar.

Exemplo real: ads 445 e 446 da campanha Webinar-Analise-Preditiva ficaram com snapshots identicos de 2026-05-05 em diante (13 dias congelados). A janela 7d para esses ads e ruido.

---

## Diferencas metricas Bunzzai vs Meta API

| Campo Bunzzai | Equivalente Meta API skill | Observacao |
|---|---|---|
| `spend` (acumulado) | `spend` (diario) | Mesma escala, mas cumulativo |
| `impressions` (acumulado) | `impressions` (diario) | Mesma escala, mas cumulativo |
| `clicks` (acumulado) | `link_clicks` (diario) | **Bunzzai conta cliques TOTAIS, nao apenas link** — tende a ser maior |
| `conversions` (acumulado) | `leads` (diario, pixel custom) | **Bunzzai conta TODAS conversoes do pixel, nao apenas a primaria** — tende a ser maior |
| `frequency` (instantaneo) | `frequency` (diario) | Bunzzai pode dar valor pontual; recalcular sempre que precisar via `impressions/reach` |
| (nao tem) | `reach` | Bunzzai nao expoe reach na maioria das tools |
| (nao tem) | `video_p25/50/100` | Bunzzai nao expoe metricas de video; **hook_rate/completion_rate ficam de fora da skill bunzzai** |

### Impacto nos benchmarks
Os benchmarks de `meta-ads/data/benchmarks.json` foram calibrados originalmente sobre **link_clicks + leads custom** (Meta API). Aplicados sobre `clicks + conversions` do Bunzzai, vao ficar:
- **CTR Bunzzai > CTR Meta** (denominador igual, numerador maior) — leitura mais otimista que a realidade do pixel
- **CpL Bunzzai < CpL Meta** (numerador igual, denominador maior) — leitura mais otimista
- **Conv. LP Bunzzai pode ir em qualquer direcao** (numerador e denominador mudam)

**Conclusao:** trate os benchmarks como referencia aproximada. Quando o Bunzzai mostra metrica `[OK]` mas pertinho do threshold, sinalize "limite — provavelmente real, mas inflado pela definicao mais ampla do Bunzzai". So conclua `[RUIM]` definitivo quando o gap for grande. Pra auditoria definitiva (caso a decisao envolva budget grande), rodar manualmente `meta-ads-legacy/scripts/audit_vs_bunzzai.py` (requer token Meta fresh — ver `meta-ads-legacy/SETUP.md`).

---

## Contas Validas

Apenas marcas do Grupo Elife mapeadas na Meta. Bunzzai pode cobrir outras empresas (CRM externo) — **estao fora do escopo desta skill**. Se o usuario pedir analise de empresa que nao seja Buzzmonitor ou Cxpress, recusar gentilmente e propor abrir uma issue pra expandir a skill no futuro.

| Chave de input | Marca Bunzzai (`company_name` no MCP) | Moeda | Simbolo | Heuristica de filtro de campanha |
|---|---|---|---|---|
| `buzzmonitor_brl` | Buzzmonitor | BRL | R$ | Nome de campanha sem token de pais OU contendo "BR", "Brasil", "brl" |
| `buzzmonitor_usd` | Buzzmonitor | USD | $ | Nome contendo "Latam", "Latin", "USD", "ES", "MX", "CO", "AR" |
| `buzzmonitor_eur` | Buzzmonitor | EUR | € | Nome contendo "EU", "Portugal", "PT", "ES Europa", "EUR" |
| `cxpress_brl` | Cxpress | BRL | R$ | (mesma heuristica de buzzmonitor_brl) |
| `cxpress_usd` | Cxpress | USD | $ | (idem buzzmonitor_usd) |
| `cxpress_eur` | Cxpress | EUR | € | (idem buzzmonitor_eur) |

**Quando a heuristica falha:** se a campanha nao tem token de pais no nome e a empresa Bunzzai e unica para a marca, listar todas e pedir confirmacao do usuario antes de filtrar. Nunca chutar.

---

## Localizacao dos Arquivos

| O que | Onde |
|---|---|
| Benchmarks (thresholds CpL/CTR/Conv.LP por moeda × tipo) | `meta-ads/data/benchmarks.json` |
| Notion ID destino | `conhecimento/config/notion-ids.md` (chave `entregas`) |
| Stress test de referencia (arquivado) | `meta-ads-legacy/scripts/stress_test_bunzzai.py` (prova que diff de snapshots funciona) |
| Pipeline meta-ads-* original (desativado em 2026-06-22) | `.claude/skills-desativadas/meta-ads*/` |

Bunzzai e tempo real via MCP — sem banco SQLite local. A pasta `meta-ads/` no raiz foi enxugada e mantem apenas `benchmarks.json` (referencia desta skill). Scripts/reports historicos foram pra `meta-ads-legacy/`.

---

## Classificacao de Campanhas

Mesma logica do meta-ads — aplicada ao **nome da campanha** retornado pelo MCP Bunzzai. Ordem de prioridade (mais especifico primeiro):

| Tipo | Palavras-chave no nome | Grupo de funil |
|---|---|---|
| `evento_presencial` | buzztalk, buzztalks, presencial | Topo |
| `webinar` | webinar, live, aula, evento, workshop, masterclass | Topo |
| `material_rico` | ebook, guia, kit, template, checklist, playbook, manual, material, whitepaper, planilha, rico | Topo |
| `remarketing` | remarketing, retargeting, remarket, rmkt, rtg | Fundo |
| `nao_classificada` | (nenhuma das acima) | — |

---

## Benchmarks

Carregar `meta-ads/data/benchmarks.json` e indexar por `benchmark_group` (`brl`/`usd`/`eur`) × `campaign_type` (`webinar`/`material_rico`/`remarketing`). Status: `[OK]` (dentro do minimo aceitavel) / `[RUIM]` (fora) / `[ ] N/A` (campanha nao classificada).

### Padroes atuais (minimo aceitavel)

**CTR link** (cliques no link ÷ impressoes)
- Topo (webinar / material rico / evento presencial): **≥ 1,0%**
- Fundo (remarketing): **≥ 0,6%**

**Taxa de conversao da LP** (leads ÷ cliques no link)
- Topo: **≥ 15%**
- Fundo (remarketing): **≥ 5%**

**CpL** (gasto ÷ leads) — varia por moeda

| Moeda | Webinar | Material rico | Remarketing |
|---|---|---|---|
| BRL (Brasil) | ≤ R$ 18 | ≤ R$ 12 | ≤ R$ 220 |
| USD (Latam) | ≤ US$ 5 | ≤ US$ 3 | ≤ US$ 60 |
| EUR (Portugal) | ≤ € 6 | ≤ € 6 | ≤ € 60 |

**Frequencia** (global, todas etapas e moedas): **≤ 7,0** — mas o Bunzzai pode nao expor frequencia em todas as tools. Se faltar dado, marcar `[ ] Sem dados`.

> Editar valores diretamente em `meta-ads/data/benchmarks.json` conforme realidade historica de cada conta.

**Atencao especial CpL Bunzzai:** as conversoes do Bunzzai sao mais amplas que os `leads custom` da Meta API. Um CpL ate ~30% melhor que o threshold pode ser inflado pela definicao mais larga. Sinalize "limite — provavelmente real, mas inflado pela definicao Bunzzai" em vez de cravar `[OK]` quando o gap for pequeno. Para auditoria definitiva, ver `meta-ads-legacy/scripts/audit_vs_bunzzai.py`.

---

## Matriz de Diagnostico Cruzado

Aplicada **no nivel da entidade** (campanha, adset ou ad) que tem `dados_suficientes` (snapshots cobrindo 7d sem cron travado).

| Cenario | CpL | CTR | Conv. LP | Diagnostico | Acao recomendada |
| --- | --- | --- | --- | --- | --- |
| 🏆 **Ouro** | Bom + ↓ | Bom | Boa | Tudo funcionando e melhorando | Escalar budget. **Marcar como referencia de criativo.** |
| 🔵 **Filtro natural** | Bom | Ruim | Boa | CTR baixo mas quem clica converte. O criativo filtra a audiencia com qualidade — pode ser hook nichado, proposital. | Manter. Testar variacao com hook mais amplo mantendo o mesmo angulo. |
| ⚠️ **Gargalo de LP** | Bom | Bom | Ruim | Ad atrai e converte bem por enquanto, mas Conv. LP baixa e um teto de escala. A LP nao sustenta o volume. | Otimizar LP antes de escalar. Verificar alinhamento entre promessa do ad e conteudo da LP. |
| 🚨 **Promessa × entrega** | Ruim | Bom | Ruim | CTR alto = criativo atrai curiosidade. LP nao entrega. Dois diagnosticos possiveis: (1) a LP nao reflete o que o ad promete; (2) o ad promete algo que o produto nao resolve. | Auditar LP: ela espelha o angulo do ad? Se sim, o problema e o angulo. Se nao, alinhar LP ao criativo. |
| 🔄 **Potencial travado** | Ruim | Bom | Boa | Ad atrai e LP converte — mas leads sao poucos. Pode ser orcamento baixo, audiencia pequena ou dados insuficientes. | Checar volume de impressoes. Se audiencia estiver ampla, aumentar budget. |
| 💀 **Substituir** | Ruim | Ruim | Ruim/— | Criativo nao atrai, LP nao converte. Nada funciona. | Pausar. Nao investir mais sem criativo novo. |
| ❓ **Sem dados** | — | — | — | Conversoes insuficientes (0 ou 1) para diagnostico confiavel. CpL pontual nao e estatisticamente valido. | Aguardar mais dados antes de agir. |

### Regras de aplicacao

1. **Conversoes insuficientes**: se conversoes 7d ≤ 2, o CpL e ruido estatistico — informar ao usuario e usar 30d como base.
2. **CTR em contexto**: remarketing tem CTR esperado maior (audiencia quente). CTR baixo em remarketing e mais grave que em prospeccao.
3. **Conv. LP ausente**: se nao houver cliques, focar no binomio CpL + CTR.
4. **CPM alto isolado**: CPM alto sem impacto no CpL nao e problema — e caracteristica do segmento. Reportar como observacao.
5. **Tendencia > valor absoluto**: CpL de R$ 300 caindo para R$ 150 e mais saudavel que R$ 100 subindo para R$ 200.
6. **[NOVO] Cron travado contamina recente**: se a janela 7d esta dentro do periodo congelado, use 15d como `recente` no diagnostico e diga isso explicitamente no relatorio.
