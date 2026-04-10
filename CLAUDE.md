# Agente Inhouse — Grupo Elife

Este agente automatiza a criacao de newsletters, traducoes de copy e analise de campanhas Meta Ads para as marcas do Grupo Elife: Buzzmonitor, Buzzcreators, Cxpress e Elife.

---

## Comandos Disponiveis

### Newsletters
Aceita `[brand]` e `[region]`. Default: `buzzmonitor brasil`.

| Comando | O que faz |
|---|---|
| `/news-pipeline [brand] [region]` | Pesquisa, gera 5 newsletters e revisa |
| `/news-pesquisar [brand] [region]` | So a pesquisa |
| `/news-gerar [brand] [region]` | So gera os rascunhos |
| `/news-revisar [brand] [region]` | So revisa os rascunhos |

- `[brand]`: `buzzmonitor` | `buzzcreators` | `cxpress` | `elife`
- `[region]`: `brasil` (PT-BR) | `latam` (ES-LATAM) | `portugal` (PT-PT)

### Traducao de Copy

| Comando | O que faz |
|---|---|
| `/trad-pipeline [arquivo] [pt-pt\|es-latam]` | Traduz e revisa |
| `/trad-traduzir [arquivo] [pt-pt\|es-latam]` | So traduz |
| `/trad-revisar [arquivo] [pt-pt\|es-latam]` | So revisa |
| `/trad-calibrar [pt-pt\|es-latam]` | Atualiza padrao linguistico |

### Meta Ads (SOMENTE LEITURA)

Requer Python 3.10+ e `meta-ads/.env` configurado (ver `.env.example`).

| Comando | O que faz |
|---|---|
| `/meta-ads [conta] [periodo]` | Pipeline completo: coleta + relatorio |
| `/meta-ads-fetch [conta] [periodo]` | So atualiza dados locais |
| `/meta-ads-report [conta] [periodo]` | So gera relatorio (sem nova coleta) |
| `/meta-ads-trends [conta]` | Tendencias temporais (3d/7d/15d/30d) |

- `[conta]`: `buzzmonitor_brl` | `buzzmonitor_usd` | `buzzmonitor_eur` | `cxpress_brl` | `cxpress_usd` | `cxpress_eur`
- `[periodo]`: `mes_atual` | `mes_anterior` | `ultimos_30`

**Primeira execucao:** `cd meta-ads && python -m pip install -r requirements.txt`
