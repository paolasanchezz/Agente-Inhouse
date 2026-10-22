# Dashboards CM — disparo diário 07h BRT (n8n)

Workflow do n8n que, **todo dia às 07:00 (America/Sao_Paulo)**, pede ao GitHub para rodar o
`.github/workflows/dashboards-deploy.yml` — a atualização das 7 dashboards CM (exporta do
Supabase → valida o contrato de dados → deploya com smoke e rollback).

```
Todo dia 07:00 (BRT) ──► POST api.github.com/.../actions/workflows/dashboards-deploy.yml/dispatches
                          {"ref": "main"}  →  GitHub responde 204 e enfileira a rodada (~2 min)
```

## Por que existe

O agendamento do próprio GitHub (`cron` no workflow) é "melhor esforço": em 2026-10 os horários
deste repositório chegavam com **4h30 a 9h30 de atraso** todo dia (o Pocket Event, agendado para
07:23 BRT, rodava entre 11:55 e 16:52 BRT), e o GitHub pode descartar a rodada sob carga alta.
Na primeira manhã depois da automação (2026-10-22), às 09:10 a rodada agendada ainda não tinha
saído. Um disparo por `workflow_dispatch` não passa por essa fila: roda na hora.

O `cron` do workflow continua lá como **reserva** — se o n8n falhar, o GitHub ainda atualiza, só
que atrasado. Nos dias normais isso dá duas rodadas (a das 07:00 e a atrasada do GitHub), o que é
inofensivo: elas entram em fila no mesmo grupo de concorrência e a segunda só reatualiza.

## Peças

| Peça | Detalhe |
|---|---|
| Gatilho | `scheduleTrigger` 07:00. **`settings.timezone = America/Sao_Paulo` é obrigatório**: a instância roda em UTC−4, então sem isso "7h" vira 08:00 BRT (mesma pegadinha do workflow de convites) |
| Disparo | `httpRequest` POST, 3 tentativas com 5 s entre elas (instabilidade momentânea da API) |
| Credencial | Header Auth `GitHub - disparar dashboards` — `Authorization: Bearer <token>`. Token **fine-grained** do `victorfmlopes`, só no repositório `Agente-Inhouse`, permissão **Actions: Read and write** e nada mais. Criado e colado no n8n pelo Victor; nunca passa por chat nem pelo repo |
| Teste manual | nó `Disparo manual (teste)` — *Execute workflow* na UI dispara uma rodada na hora |
| Alerta | nenhum, por decisão do Victor (2026-10-22). Se o disparo falhar, a execução fica vermelha no n8n e a reserva do GitHub cobre |

## Manutenção

- **Token:** `n8n — disparar dashboards`, criado em 2026-10-22 **sem data de expiração**. Se for
  revogado ou trocado, o disparo passa a dar 401 no n8n (sem alerta) e as dashboards voltam a
  depender do `cron` atrasado do GitHub. Token novo = mesmas permissões, e trocar só o valor da
  credencial `GitHub - disparar dashboards` (id `yIFq6rWEvNDfmSkn`) no n8n — o workflow não muda.
- **Workflow na instância:** id `0OAzSVco0PniHE54`. Testado em 2026-10-22 com o gatilho adiantado:
  n8n disparou às 09:57:44, a rodada nasceu no GitHub 1 s depois e ficou verde em ~2 min.
- **Mudar horário:** só o nó do gatilho. Lembre que 07:00 dispara e a rodada fica pronta ~07:03.
- **Editar pela API:** `GET /workflows/{id}` → alterar → `PUT` com apenas `{name, nodes,
  connections, settings}` (mesma receita do workflow de convites). Manter este JSON em sincronia.
- O JSON aqui versionado é o espelho do que roda; o ID da credencial é identificador, não segredo.
