---
name: auditar-deals-cm
description: Audita deals de Content Marketing que somem da dashboard CM Buzzmonitor Brasil por falha de UTM (campo vazio no deal por erro de automacao AC->Supabase). Roda harness Python read-only contra Supabase, recupera a UTM localmente (propagacao por contato/empresa + sinais de titulo/inbound), re-roda o filtro CM REAPROVEITADO da dashboard e entrega os "deals CM nao mapeados". Manual-trigger. Single-purpose (Buzzmonitor Brasil).
argument-hint: "[--desde YYYY-MM-DD] [--ate YYYY-MM-DD]  (default: 2026-01-01 -> hoje)"
allowed-tools: AskUserQuestion, Read, Edit, Bash, Glob, Grep
version: 1.0.0
---

# Skill: Auditar Deals CM nao mapeados por falha de UTM

Voce orquestra uma auditoria **read-only** que descobre deals de Content Marketing que a dashboard
(`https://dashboards-elife.vercel.app/buzz-br/`) **nao conta** porque chegaram ao Supabase com
`utm_source` e `url_conversao` vazios — falha da automacao AC->Supabase que deveria preencher a UTM
do deal a partir do contato / da nota.

O harness recupera a UTM **localmente** (nunca grava no Supabase), re-roda o filtro CM
**reaproveitando `dashboard/queries.py`** (zero drift), e devolve os "deals CM nao mapeados" em
3 niveis de confianca.

**Leia `.claude/skills/auditar-deals-cm/CONTEXT.md` antes de prosseguir** (definicao de candidato,
filtros de ruido, niveis de confianca, mapa AC da Fase 2).

**Single-purpose:** so Buzzmonitor Brasil (`deals_comercial_prod` + `deals_contratos_prod`). A unica
escrita possivel e adicionar emails confirmados a `EMAIL_WHITELIST` em `queries.py` — e SO depois do
Victor confirmar no gate (Passo 3). Tudo o mais e leitura.

---

## Passo 0: Pre-flight

- `git rev-parse --show-toplevel` deve resolver (rodar da raiz do repo).
- `dashboard/.env` deve existir com `SUPABASE_PG_URL=`. Se nao: instruir a copiar de
  `dashboard/.env.example` e preencher (mesmo `.env` da `/dashboard-atualizar`).
- `uv` deve estar no PATH (`uv --version`). Se nao: apontar `/setup-agencia`.

Capturar args: `--desde` (default `2026-01-01`) e `--ate` (default: sem limite = hoje). Se o Victor
pedir outro periodo em linguagem natural ("ultimos 90 dias", "maio"), traduzir pra datas ISO.

---

## Passo 1: Rodar o harness

```bash
uv run --python 3.12 --with "psycopg[binary]" python dashboard/auditar_deals_cm.py --desde 2026-01-01 2>&1 | tee "tmp/audit-cm-$(date +%Y-%m-%d).log"
```

(Acrescentar `--ate YYYY-MM-DD` se o Victor delimitou o fim.)

O harness é determinístico e read-only. Se quebrar:
- erro de conexao/timeout do Supabase -> propagar as ultimas linhas do log e abortar.
- `ModuleNotFoundError: queries` -> rodou de fora da raiz; reexecutar da raiz.

Saidas em `dashboard/auditoria/` (gitignored — contem PII):
- `AUDIT-CM-UTM-{data}.md` (relatorio)
- `net-new-contato-{data}.csv` (alta confianca)
- `revisao-mesma-empresa-{data}.csv`, `revisao-titulo-inbound-{data}.csv`
- `prefixos-titulo-nao-mapeados-{data}.csv`

---

## Passo 2: Ler e resumir

Ler `dashboard/auditoria/AUDIT-CM-UTM-{data}.md`. Resumir pro Victor em PT-BR, com foco no que importa:

- **Quanto a dashboard conta hoje** (ANTES) vs **NET-NEW alta confianca** (mesmo contato) — o numero
  em que pode confiar — e o **% de ganho**.
- O tamanho das filas de **revisao** (mesma empresa / titulo-inbound) — potencial, mas precisa
  confirmacao (e o que a Fase 2 com AC fecha).
- Top canais recuperados.

Nao despejar os CSVs inteiros no chat (sao PII). Citar contagens + alguns exemplos.

---

## Passo 3: Gate de remediacao (AskUserQuestion)

A recomendacao depende do volume de **NET-NEW alta confianca** (o harness ja imprime a sua sugestao
na secao "Remediacao sugerida" do relatorio). Apresentar opcoes com `AskUserQuestion`:

- **Se NET-NEW <= 25:** oferecer **"Adicionar a EMAIL_WHITELIST"** como 1a opcao. Se escolhida:
  ler o bloco `python` sugerido no relatorio, abrir `dashboard/queries.py`, e inserir os emails
  confirmados em `EMAIL_WHITELIST` (cada um com o comentario `# {id} — {origem} via doador {donor}`),
  **um a um, so os que o Victor aprovar**. Depois, lembrar que a dashboard so reflete isso no proximo
  `/dashboard-atualizar`.
- **Se NET-NEW > 25** (caso atual YtD): NAO propor whitelist inline (inviavel). 1a opcao =
  **"So guardar o relatorio + sinalizar fix de automacao"** — o certo é corrigir a automacao
  AC->Supabase (ou criar a tabela `cm_email_whitelist` prevista em `queries.py:11`).
- Sempre oferecer **"Abrir Fase 2 (AC)"** — enriquecer as filas de revisao com notas + UTM do contato
  via ActiveCampaign pra transformar revisao em confirmado (requer chave de API do AC; ver
  `dashboard/AUDITORIA-DEALS-CM.md` §Fase 2 e a funcao `enrich_from_ac()` no harness).
- Sempre oferecer **"Nao mexer agora"** (so o relatorio).

**Nunca** editar `queries.py` sem o Victor confirmar caso a caso. Nunca tocar no Supabase.

---

## Passo 4: Resumo final

Imprimir no chat: periodo auditado, ANTES, NET-NEW alta confianca (+%), filas de revisao, caminho do
relatorio, e a acao tomada (whitelist editada / Fase 2 aberta / nada). Se editou `queries.py`, lembrar
de rodar `/dashboard-atualizar` e revisar via `/commit`.

---

## Notas

- **Reuso, nao reimplementacao:** o harness importa `filtro_cm`, `EMAIL_WHITELIST`, `EMAIL_BLACKLIST`,
  `_sql_email_list`, `q_lista_leads` de `queries.py`. Se a definicao de CM mudar la, a auditoria
  acompanha automaticamente. Validado: ANTES == `q_count_leads` da dashboard (anti-drift).
- **Niveis de confianca:** `email` (mesmo contato) = alta; `conta` (mesma empresa, outro contato) e
  `titulo/inbound` = revisao. So o `email` entra no headline net-new.
- **Re-rodar:** seguro e idempotente. Pode rodar quando quiser, com `--desde/--ate` a vontade.
