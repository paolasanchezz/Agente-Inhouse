# Contexto Compartilhado — Meta Ads

> Este arquivo é lido por todas as skills do grupo meta-ads antes de qualquer ação.

---

## Restrição Absoluta

**SOMENTE LEITURA.** Nunca executar, sugerir nem insinuar qualquer operação de escrita na Meta Marketing API. Apenas GET. Nunca criar, pausar, editar, duplicar ou excluir campanhas, adsets ou anúncios.

---

## Contas Válidas

| Chave | Marca | Moeda | Símbolo |
|---|---|---|---|
| `buzzmonitor_brl` | Buzzmonitor | BRL | R$ |
| `buzzmonitor_usd` | Buzzmonitor | USD | $ |
| `buzzmonitor_eur` | Buzzmonitor | EUR | € |
| `cxpress_brl` | Cxpress | BRL | R$ |
| `cxpress_usd` | Cxpress | USD | $ |
| `cxpress_eur` | Cxpress | EUR | € |

## Períodos Válidos

| Valor | Descrição |
|---|---|
| `mes_atual` | Do dia 1 do mês corrente até ontem |
| `mes_anterior` | Mês completo anterior |
| `ultimos_30` | Últimos 30 dias corridos |

---

## Localização dos Arquivos

| O que | Onde |
|---|---|
| Scripts Python | `meta-ads/scripts/` |
| Banco de dados local | `meta-ads/data/meta_ads.db` (gitignored) |
| Relatórios gerados | `meta-ads/data/reports/` |
| Benchmarks editáveis | `meta-ads/data/benchmarks.json` |
| Configuração de token | `meta-ads/.env` (gitignored) |

---

## Classificação de Campanhas

A ordem abaixo é a ordem de prioridade das regras (mais específico primeiro):

| Tipo | Palavras-chave no nome da campanha | Grupo de funil |
|---|---|---|
| `evento_presencial` | buzztalk, buzztalks, presencial | Topo |
| `webinar` | webinar, live, aula, evento, workshop, masterclass | Topo |
| `material_rico` | ebook, guia, kit, template, checklist, playbook, manual, material, whitepaper, planilha, rico | Topo |
| `remarketing` | remarketing, retargeting, remarket, rmkt, rtg | Fundo |
| `nao_classificada` | (nenhuma das acima) | — |

---

## Benchmarks por Grupo

Os benchmarks ficam em `meta-ads/data/benchmarks.json`. Grupos: `brl`, `usd`, `eur`.
Métricas avaliadas: `cost_per_lead`, `ctr_link`, `lp_conversion_rate`, `frequency` (global).

Status: `[BOM]` / `[OK] Aceitável` / `[RUIM]`

---

## Verificação de Token

Antes de qualquer chamada à API, verificar:
- `META_ACCESS_TOKEN` presente no `.env`
- `META_TOKEN_CREATED_AT` indica validade (tokens expiram em ~60 dias)
- Se token expirado ou ausente: interromper e pedir novo token ao usuário
