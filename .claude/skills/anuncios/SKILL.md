---
name: anuncios
description: Guia interativo de análise de Meta Ads. Faz perguntas com chips clicáveis e dispara a skill correta do pipeline meta-ads-*. Usar quando o usuário digitar /anuncios sem saber qual comando rodar.
argument-hint: "(opcional) — texto livre. Ex: /anuncios | /anuncios buzzmonitor_brl | /anuncios 'CpL da Cxpress USD subiu, o que aconteceu?'"
allowed-tools: AskUserQuestion, Read, Glob
---

# Skill: /anuncios — Guia interativo de Meta Ads

Você está executando um **script determinístico**. Não improvise perguntas, não pule passos, não invente opções. Siga exatamente o roteiro abaixo.

## Princípios invioláveis

1. Uma pergunta por vez. Não junte perguntas.
2. Sempre marque a opção recomendada com `(Recomendado)` no label.
3. Antes de cada pergunta, verifique se a resposta já está em `$ARGUMENTS` — se sim, **pule a pergunta**.
4. Antes de disparar a skill final, mostre 1 frase de confirmação e aguarde "sim".
5. Para casos fora de escopo, use as mensagens hardcoded da seção "Fallback".
6. Linguagem: PT-BR coloquial.
7. Você só monta argumentos e delega — toda lógica de Meta Ads está nas skills `/meta-ads*`.
8. **Restrição absoluta**: nunca sugerir ação de escrita na Meta API (criar, pausar, editar, duplicar, excluir). SOMENTE LEITURA.

---

## Passo 0 — Pré-checagens (aviso hardcoded)

Antes de qualquer pergunta, exiba **literalmente** este aviso (não bloqueia o fluxo):

> **Antes de começar:** Meta Ads aqui é **SOMENTE LEITURA** — nunca crio, pauso ou edito anúncios.
>
> Requer Python instalado e token configurado em `meta-ads/.env`. Se for sua primeira vez, antes de continuar:
> ```
> cd meta-ads && python -m pip install -r requirements.txt
> cp .env.example .env   # depois preencha com seu token e IDs de conta
> ```

Continue para o Passo 1.

---

## Passo 1 — Pergunta-raiz

Use `AskUserQuestion`:

- **question:** "O que você quer saber dos anúncios?"
- **header:** "Análise"
- **multiSelect:** false
- **options:**
  1. label: "Performance geral (Recomendado)" — description: "Coleta os dados e gera relatório completo do período. Use quando quiser saber como uma conta está indo."
  2. label: "Tendências (CpL/CTR caindo?)" — description: "Compara janelas de 3d / 7d / 15d / 30d para ver evolução. Use para investigar se algo melhorou ou piorou."
  3. label: "Só atualizar dados locais" — description: "Sincroniza o banco local com a API sem gerar relatório. Use antes de uma análise manual."
  4. label: "Re-gerar relatório (sem nova coleta)" — description: "Usa os dados que já estão no banco. Zero chamadas à API. Use para refazer relatório rápido."

Guarde como `tarefa`.

---

## Passo 2 — Coleta de parâmetros

### 2.A Conta (todas as opções)

Como `AskUserQuestion` aceita no máximo 4 opções e temos 6 contas, **divida em 2 perguntas**.

**2.A.1 Marca da conta** (pular se `$ARGUMENTS` já contém `buzzmonitor_*` ou `cxpress_*`):

`AskUserQuestion`:
- question: "Qual marca da conta?"
- header: "Marca"
- multiSelect: false
- options:
  1. "Buzzmonitor" — "Conta de anúncios da Buzzmonitor."
  2. "Cxpress" — "Conta de anúncios da Cxpress."

Guarde lowercase: `marca_conta`.

**2.A.2 Moeda da conta** (pular se já em `$ARGUMENTS`):

`AskUserQuestion`:
- question: "Qual moeda?"
- header: "Moeda"
- multiSelect: false
- options:
  1. "BRL (R$)" — "Conta em Reais — mercado Brasil."
  2. "USD ($)" — "Conta em Dólares — mercado internacional."
  3. "EUR (€)" — "Conta em Euros — mercado Europa."

Guarde lowercase: `moeda` ∈ {`brl`, `usd`, `eur`}.

**Combinar:** `conta = "{marca_conta}_{moeda}"` (ex: `buzzmonitor_brl`, `cxpress_eur`).

Contas válidas: `buzzmonitor_brl`, `buzzmonitor_usd`, `buzzmonitor_eur`, `cxpress_brl`, `cxpress_usd`, `cxpress_eur`.

### 2.B Período

**Pular se `tarefa` == "Tendências (CpL/CTR caindo?)"** — essa skill não usa período (já cobre todas as janelas internamente).

Para as outras 3 opções, se `$ARGUMENTS` não trouxe período:

`AskUserQuestion`:
- question: "Qual período analisar?"
- header: "Período"
- multiSelect: false
- options:
  1. "Mês atual (Recomendado)" — "Do dia 1 do mês corrente até ontem."
  2. "Mês anterior" — "Mês completo anterior (do dia 1 ao último dia)."
  3. "Últimos 30 dias" — "Janela móvel dos últimos 30 dias corridos."

Guarde lowercase mapping:
- "Mês atual" → `mes_atual`
- "Mês anterior" → `mes_anterior`
- "Últimos 30 dias" → `ultimos_30`

Salve como `periodo`.

---

## Passo 3 — Confirmação e disparo

### Mapeamento `tarefa` → skill

| `tarefa` | Skill final | Argumentos |
|---|---|---|
| Performance geral | `/meta-ads` | `{conta} {periodo}` |
| Tendências (CpL/CTR caindo?) | `/meta-ads-trends` | `{conta}` |
| Só atualizar dados locais | `/meta-ads-fetch` | `{conta} {periodo}` |
| Re-gerar relatório (sem nova coleta) | `/meta-ads-report` | `{conta} {periodo}` |

### Frase de confirmação (envie literalmente)

> "Vou rodar `/{skill} {argumentos}`. Posso seguir? (responda 'sim' ou ajuste)"

Aguarde resposta. Se "sim" (ou: "vai", "pode", "ok", "manda"), disparar. Se ajuste, voltar ao passo correspondente.

### Disparo (envie literalmente)

> "Execute o fluxo completo da skill `/{skill}` com os argumentos `{argumentos}`. Consulte `.claude/skills/{skill}/SKILL.md` e execute todos os passos na íntegra."

---

## Fallback (mensagens hardcoded)

- **Quer pausar/criar/editar/duplicar campanha:**
  > "Não posso fazer isso — Meta Ads aqui é **SOMENTE LEITURA**. Para qualquer alteração, use o Ads Manager direto."

- **Quer analisar Google Ads / TikTok Ads / LinkedIn Ads:**
  > "Hoje só temos pipeline para Meta Ads (Facebook + Instagram). Para outras plataformas ainda não há skill — fale com quem mantém o repositório."

- **Conta fora das 6 listadas:**
  > "As 6 contas configuradas são: `buzzmonitor_brl`, `buzzmonitor_usd`, `buzzmonitor_eur`, `cxpress_brl`, `cxpress_usd`, `cxpress_eur`. Para adicionar outra, fale com quem mantém o repositório (precisa atualizar `meta-ads/.env` e o CONTEXT.md do meta-ads)."

- **Token expirado / API recusou:**
  > "Parece que o token Meta expirou ou não está configurado. Verifique `meta-ads/.env` (a variável `META_ACCESS_TOKEN`). Tokens duram ~60 dias — gere um novo no Business Manager se necessário."

- **Quer projeção/forecast/recomendação de orçamento:**
  > "Eu só leio dados históricos e gero relatório. Para projeção/forecast/realocação de budget, faça você mesmo a partir dos números — eu não chuto futuro."
