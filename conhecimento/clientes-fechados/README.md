# Clientes fechados — Dor + Funcionalidades que converteram

Snapshot dos deals **fechados** (contratos assinados) das 3 unidades comerciais do Grupo Elife,
com foco em **dor declarada** e **funcionalidade que atraiu** o cliente. Material primário do
ActiveCampaign (via Supabase), filtrado pra incluir apenas deals com pelo menos 1 campo de dor
ou feature preenchido.

| Arquivo | Unidade | Linhas | Fonte (tabela Supabase) |
|---|---|---|---|
| `dor-features-buzzmonitor-brasil.csv` | Buzz BR | 1.167 | `deals_contratos_prod` |
| `dor-features-buzzmonitor-latam.csv` | Buzz LATAM | 177 | `deals_latam_contratos_staging` |
| `dor-features-cxpress-brasil.csv` | Cxpress BR | 116 | `cxpress_deals_funil_principal_prod` |

---

## ⏱️ Frescor dos dados

- **Última atualização:** `2026-06-08`
- **Próxima atualização recomendada:** `2026-08-08` (a cada 2 meses)

> Se hoje passou de **08/08/2026**, sugira ao Victor reatualizar antes de usar os dados pra
> decisão comercial — dois meses sem refresh perdem dores e features de vendas recentes.
> Comando em [§ Como atualizar](#como-atualizar).

---

## Pra que serve

Responder rápido a perguntas do tipo:

1. **"Qual a dor mais comum dos clientes que fecham com Buzzmonitor no BR?"**
   → agrupar `dor_dores_atuais` + `dor_spin_problema` por palavras-chave / tema.

2. **"Qual feature mais chamou atenção dos clientes Cxpress?"**
   → cruzar `feature_canais_a_integrar` + `feature_necessidade_lead` + `feature_spin_necessidade`.

3. **"Que concorrentes os clientes LATAM avaliavam antes de fechar conosco?"**
   → coluna `concorrentes_avaliados` (LATAM) / `plataforma_atual` (todas).

4. **Material pra copywriting:** dores reais com a linguagem do cliente ajudam a escrever
   anúncio, LP, email e newsletter com tom verdadeiro — basta usar como referência pras skills
   `/copy-criar`, `/copy-pesquisar`, `/lp-preparar`.

5. **Pesquisa de produto:** ver que features clientes pediram em quais tipos de empresa.

---

## Estrutura das colunas

Todas as 3 tabelas seguem o mesmo padrão **prefixado por categoria**:

### 🟥 `dor_*` — campos descritivos de dor

| Coluna semântica | Buzz BR | Buzz LATAM | Cxpress BR |
|---|---|---|---|
| Dor declarada (campo livre principal) | `dor_dores_atuais` | `dor_areas_oportunidade` | `dor_principal_queixa` |
| Dor formal SPIN (Problema) | `dor_spin_problema` | `dor_spin_problema` | `dor_spin_problema` |
| Implicação SPIN (urgência) | `dor_spin_implicacao` | `dor_spin_implicacao` | `dor_spin_implicacao` |
| Necessidade qualitativa | `dor_bant_need` | `dor_problema_lead` | `dor_bant_needs` |

**Cobertura observada (08/06/2026):**
Buzz BR ~100% no campo principal, SPIN ~35%. LATAM ~55% no principal, SPIN ~4%. Cxpress ~29% no principal, SPIN ~11%.

### 🟩 `feature_*` — funcionalidade que atraiu / atratores

| Coluna semântica | Buzz BR | Buzz LATAM | Cxpress BR |
|---|---|---|---|
| Features destacadas | `feature_principais_modulos` | `feature_principais_modulos` | `feature_canais_a_integrar` |
| Objetivo declarado | `feature_objetivo` | `feature_objetivo` | `feature_necessidade_lead` |
| Necessidade SPIN | `feature_spin_necessidade` | `feature_spin_necessidade` | `feature_spin_necessidade` |
| Outros (varia por unidade) | — | `feature_oportunidades_futuras` | `feature_prioridade_implementacao` |

### 🟦 Contexto (cortes para agrupar)

| Buzz BR | Buzz LATAM | Cxpress BR |
|---|---|---|
| `plataforma_atual` | `plataforma_atual` | `area_atendida` |
| `concorrentes_avaliados` | `concorrentes_avaliados` | `volume_atendimentos` |
| `canais` | `canais` | `qualificacoes_adicionais` |
| `particularidades` | `quem_e_o_cliente`, `description`, `observacoes` | `automacao_atendimento_atual`, `concorrente_avaliado` |

### Identificação (comum a todas)

`id` · `title` · `data_fechamento` · `valor` · `currency` · `bd` (closer) · `sdr` · `utm_source` · `utm_content` · `link_ac`

**Atributos por unidade:**
- **Buzz BR:** `email` (do contato principal)
- **Buzz LATAM:** `pais` + `status`
- **Cxpress BR:** `contact` (id do contato no AC)

---

## Critério de "deal fechado"

Cada unidade tem sua definição operacional travada com a área comercial:

| Unidade | Definição |
|---|---|
| Buzz BR | `data_fechamento_auto IS NOT NULL` em `deals_contratos_prod` |
| Buzz LATAM | `status='Ganho' OR primer_pago_realizado_automatico IS NOT NULL OR fecha_de_inicio_de_contrato IS NOT NULL OR fecha_de_cierre_de_negocio IS NOT NULL` (definição **FECHADO_LATAM** travada em 06/jun/2026 — `status='Ganho'` sozinho perde ~85% dos cierres reais no AC LATAM) |
| Cxpress BR | `data_do_fechamento_auto` preenchido e não-vazio em `cxpress_deals_funil_principal_prod` |

**Filtro adicional aplicado:** o deal só entra no CSV se tiver pelo menos 1 dos 7-8 campos de
dor ou feature listados acima preenchido. Deals fechados sem qualquer texto descritivo são
ruído pra análise — ficam de fora.

---

## Como atualizar

```bash
uv run --python 3.12 --with "psycopg[binary]" python dashboard/exportar_dor_features.py
```

O script lê `dashboard/.env` (variável `SUPABASE_PG_URL`, mesmo `looker_readonly` da dashboard
CM), executa as 3 queries e sobrescreve os 3 CSVs nesta pasta.

**Depois de rodar:**

1. Atualizar o campo `Última atualização` no topo deste README pra data de hoje.
2. Atualizar `Próxima atualização recomendada` pra hoje + 2 meses.
3. (Opcional) Rodar `uv run --python 3.12 --with "psycopg[binary]" python dashboard/analisar_cobertura_spin.py`
   pra ver se a cobertura dos campos descritivos mudou — útil pra notar quando algum time
   comercial parou de preencher um campo (sinal pra avisar a liderança).
4. Commit via `/commit`.

---

## Como ajustar o que entra

Os campos exportados estão no próprio script (`dashboard/exportar_dor_features.py`) — 3 blocos
`QUERY_BUZZ_BR`, `QUERY_BUZZ_LATAM`, `QUERY_CXPRESS_BR`. Cada um é uma SQL `SELECT` simples
com os campos rotulados via `AS dor_*`/`feature_*`.

**Quando alterar:**

- Surgiu um campo novo no AC que vale a pena trackear → adicionar à query e ao `WHERE` (que
  garante que o deal entra se houver pelo menos algum descritivo).
- O time parou de usar um campo → mover de "dor" pra contexto, ou deixar mas saber que
  cobertura baixou (script de cobertura mostra).
- Quer mudar definição de "fechado" (ex: incluir só ganhos com `status='Ganho'` no LATAM) →
  trocar o `WHERE` da query LATAM.

Antes de alterar, considere rodar `analisar_cobertura_spin.py` pra fundamentar a mudança em
dado, não em hunch.

---

## Notas técnicas

- **Conexão:** psycopg + Supabase Postgres, usuário `looker_readonly` (somente SELECT).
- **Cobertura desigual:** o BR é o melhor — 100% nos campos principais. LATAM e Cxpress têm
  cobertura mais baixa porque o time comercial preenche menos campos descritivos no AC. Não é
  bug de query.
- **Formato:** UTF-8 com BOM (lê direto no Excel sem mojibake), separador vírgula.
- **JSON arrays no Cxpress:** alguns campos vêm com `["valor1","valor2"]` (ex: `feature_canais_a_integrar`).
  É como o AC armazena multi-select — fica legível em texto, mas se for processar
  programaticamente, faça `json.loads()` na coluna.
- **Sem PII sensível:** emails, IDs e nomes de empresa estão presentes (é deal comercial,
  não consumidor final). Manter o repositório privado, como o restante do agente inhouse.
