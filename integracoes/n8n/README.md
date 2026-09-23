# ClickMeeting → Google Sheets (inscritos de webinars)

Workflow do n8n que copia os inscritos dos webinars do ClickMeeting para a aba
**Leads-global** da planilha, com **presença** (participou ou não da sessão ao vivo),
e mantém tudo atualizado sozinho (roda a cada 2h).

- **Arquivo:** `clickmeeting-inscritos-google-sheets.json` (v2, reescrito 2026-07-14)
- **Na instância:** workflow id `fjI42CSkkWyH2nJs` em `n8n-marketing-u54305.vm.elestio.app`
- **Planilha destino:** https://docs.google.com/spreadsheets/d/1CTmui4aWRDoj3rgBEXVa1B0SKDcsznZdLmR2uA_2s8E/edit
  → aba **Leads-global** (gid `2014321175`). A aba antiga ("Inscritos", gid 1423963986)
  ficou congelada como histórico do modelo anterior.

## O que ele faz

1. Lê todas as conferências da conta (`/conferences/active` + `/conferences/inactive`).
2. **Seleciona toda sala com página de inscrição** (`registration_enabled`) — recorrente
   OU avulsa, **sem lista fixa de séries/nomes**: webinar novo do marketing entra sozinho.
   Inativas só dentro da **janela de 7 dias** (ver "Por que a janela" abaixo).
3. **Loop A** — para cada sala, busca os inscritos (`/conferences/{id}/registrations`).
4. **Loop B** — para cada sala, busca a sessão realizada (`/sessions`) e os presentes
   (`/sessions/{sid}/attendees`), que trazem **e-mail** de quem esteve ao vivo.
5. Monta **1 linha por inscrição** (pessoa × sessão) e grava na Leads-global em modo
   **Append or Update** com chave **`Chave` = email|salaId** — re-runs nunca duplicam.

### Colunas (14)
`Data inscrição · Nome · Email · Empresa · País · Cidade · Marca/Sala · Série · Sessão · Origem · Link de acesso · Participou? · Chave · Telefone`

- **Telefone** (desde 2026-09-23) = campo 11 do formulário da sala, que as LPs de perpétuo
  mandam obrigatório: só dígitos, DDI + número, sem `+` (`5511987654321`). A chave em `fields`
  vem como `Phone`; o nó procura por nome (`phone|telefon|teléfono`) e limpa pra dígitos.
  Inscrição anterior a essa data fica vazia. Coluna nova no fim, depois de `Chave`, pra não
  deslocar fórmula que usa posição.

- **Sessão** = `starts_at` real da ocorrência (ISO com offset). Não é mais o `session_id`
  opaco do ClickMeeting (que vinha `null` pra sessão futura — bug do modelo antigo).
- **Participou?** = `Sim` (e-mail do inscrito está nos attendees da sessão realizada),
  `Não` (sessão realizada, consulta OK, e-mail ausente = no-show), vazio (sessão ainda
  não aconteceu, ou presença indisponível no momento do run). O run seguinte à sessão
  (~2h depois) preenche o Sim/Não sozinho, enquanto a sala está na janela de 7 dias.
  Nota: moderador/apresentador que se inscreveu também conta como `Sim` (factual).
- **Chave** = coluna técnica de dedup (`email|salaId`). Não apagar.
- **Modelo: 1 linha por (pessoa, sessão)** — decisão Victor 2026-07-14, supersede o
  Email-only de 2026-07-07. Pessoa inscrita em 3 sessões = 3 linhas, cada uma com sua
  presença. Leads únicos = `COUNTUNIQUE` na coluna Email.

## Decisões de desenho (por quê é assim)

- **Zero lista de inclusão.** Único critério é `registration_enabled`. A `BLOQUEIO_RID`
  (hoje só `17643` = série "teste1") é **exclusão fail-open**: se desatualizar, o pior
  caso é linha a mais na planilha — nunca lead perdido. O regex de nome (`/\btest/i`)
  do modelo antigo foi removido: excluiria silenciosamente um webinar real com "teste"
  no título.
- **Janela de 7 dias nas inativas** (ativas entram sempre): ninguém se inscreve *depois*
  da sessão, então revarrer o histórico inteiro a cada 2h (134+ salas, crescendo ~6/dia)
  era volume sem teto e risco de rate limit. As linhas antigas já gravadas nunca são
  apagadas (append-or-update). Se a instância ficar >7 dias fora do ar, rodar o backfill
  de novo (abaixo) pra cobrir o buraco.
- **Join determinístico por iteração** (`runIndex`): os 2 loops processam 1 sala por vez
  na MESMA ordem do nó Selecionar, então a execução *i* de cada nó é exatamente a sala
  *i*. Sem `pairedItem`, sem parsing de `room_pin` do link (heurísticas do modelo antigo).
- **Cadeia linear** `ativas → inativas → Selecionar` (com `executeOnce` nos GETs):
  a topologia paralela com merge implícito falhou na prática — o motor v1 seguiu o ramo
  das ativas em profundidade e o Selecionar rodou sem as inativas (exec 7287069,
  2026-07-14). Linear não tem semântica de merge; o Selecionar lê os dois nós via `$()`.
- **`alwaysOutputData` + `onError: continueRegularOutput`** nos HTTP dos loops: sala com
  0 inscritos ou erro pontual não trava o loop nem derruba o lote; presença indisponível
  vira `Participou?` vazio (nunca um `Não` falso).

## Backfill (transição — já executado)

`backfill-leads-global-clickmeeting.json` — clone do fluxo com **webhook** de disparo e
**sem janela** (LOOKBACK 36500 dias) e Sheets em **append** (cria o cabeçalho na aba
vazia; o appendOrUpdate exige colunas existentes). Executado em 2026-07-14 (workflow
`Cw5ua9pgbgsJ8SeZ`, exec `7287075`, success): varreu 134 salas históricas e gravou
**29 linhas** (11 Sim · 14 Não · 4 futuras) — populou a Leads-global do zero.
O workflow ficou **desativado** na instância; pode ser apagado (o JSON aqui é a fonte).
Se precisar re-rodar (ex.: buraco >7 dias): importar/ativar, `POST` no webhook
`/webhook/backfill-leads-global-2026-07-14`, conferir execução, desativar.
Atenção: re-rodar com Sheets em `append` **duplica** linhas existentes — pra re-rodar
sobre aba já populada, trocar a operação do nó Sheets pra `appendOrUpdate` (matching
`Chave`) antes.

## Setup no n8n (se recriar do zero)

1. **Importar** o JSON. Credenciais esperadas: Header Auth `ClickMeeting API`
   (id `Cn3XXNfzZXoS9DS8`, header `X-Api-Key`) nos nós CM, e Google Sheets OAuth2
   (conta dona da planilha) no nó Sheets. Nada de segredo no JSON.
2. Garantir que a aba **Leads-global** existe com os 13 cabeçalhos (ou rodar o backfill
   primeiro, que os cria).
3. Testar com *Execute Workflow* e ativar.

## Manutenção

- **Novo webinar/sala?** Nada a fazer — entra sozinho na próxima execução.
- **Excluir uma sala de teste:** adicionar o `recurring_config_id` em `BLOQUEIO_RID`
  no nó *Selecionar salas com inscrição* (e apagar as linhas já gravadas na mão).
- **Mudar cadência/janela:** nó *A cada 2 horas* / const `LOOKBACK_DIAS` no Selecionar.
- **Editar via API:** `GET/PUT /api/v1/workflows/fjI42CSkkWyH2nJs` (ver
  `reference_n8n_api`); manter este JSON em paridade com o live.

## Troubleshooting

| Sintoma | Causa provável | Fix |
|---|---|---|
| Erro "Missing columns … Column to Match On" | Aba sem linha de cabeçalho | Rodar o backfill (append cria headers) ou colar os 14 cabeçalhos na linha 1 |
| Linhas duplicadas | Alguém rodou o backfill (append) sobre aba já populada | Dedup na planilha por `Chave`; re-rodar backfill só com appendOrUpdate |
| `Participou?` vazio em sessão passada | Presença indisponível no run (erro pontual na API) | Aguardar próximo run dentro da janela de 7d; senão, backfill |
| Sala sumiu da varredura | `starts_at` fora da janela de 7d (inativa antiga) | Normal — linhas dela já estão gravadas |
