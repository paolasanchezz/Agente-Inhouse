# Convites de Moderador ClickMeeting (n8n · diário 07h BRT)

Workflow do n8n que envia, **todo dia às 07:00 (America/Sao_Paulo)**, 1 convite de
moderador (`role=presenter`) para a **próxima sessão futura** de cada série recorrente de
webinar do ClickMeeting. Substitui o disparo que rodava no GitHub Actions (migrado em
2026-07-07).

- **Arquivo:** `convites-moderador-clickmeeting.json`
- **Na instância:** workflow id `1TFA4xHvFEZQ5lns` em `n8n-marketing-u54305.vm.elestio.app`
  ([editor](https://n8n-marketing-u54305.vm.elestio.app/workflow/1TFA4xHvFEZQ5lns))
- **Espelha:** a lógica de `.claude/skills/convites-moderador/send_invites.py`

## Fluxo

```
Disparo manual (teste) ┐
                       ├─→ CM: conferências ativas ─→ Montar plano de convites ─→ CM: enviar convite (presenter)
Todo dia 07:00 (BRT) ──┘        GET /active            (Code: filtra + escolhe)      POST /invitation/email/{lang}
```

1. **GET** `https://api.clickmeeting.com/v1/conferences/active`.
2. **Code** — para cada série do mapa `SERIES`: filtra `recurring_config_id` + `registration_enabled` + `starts_at` futuro, pega a **mais próxima**, e emite 1 item por (sessão, e-mail de moderador).
3. **POST** `…/conferences/{roomId}/invitation/email/{lang}` com `attendees[0][email]`, `template=advanced`, `role=presenter`. `onError: continueRegularOutput` (uma falha não derruba o lote). **Sem retry** — a API não deduplica, retry = e-mail em dobro.

## Séries (estado 2026-09-02 — igual ao config.json da skill)

Ordenadas pelo horário da sessão no dia (BRT).

| recurring_config_id | Rótulo | Moderador(es) | lang |
|---|---|---|---|
| 18050 | Buzzcreators (10:20 BRT) | gabriel.leal@buzzmonitor.com.br · lucas.campos@buzzmonitor.com.br | br |
| 17927 | Buzzmonitor Tu primer listening (LATAM, 12:00 BRT) | daniel.topete@buzzmonitor.com | es |
| 17646 | Buzzmonitor ¿Qué es MCP? (LATAM, 13:00 BRT) | milagro.pantoja@buzzmonitor.com · daniel.topete@buzzmonitor.com | es |
| 17701 | Buzzmonitor Atención al Cliente (LATAM, 14:00 BRT) | milagro.pantoja@buzzmonitor.com · daniel.topete@buzzmonitor.com | es |
| 17933 | Buzzmonitor Gestión de Crisis (LATAM, 15:00 BRT) | milagro.pantoja@buzzmonitor.com | es |
| 17928 | Buzzmonitor Caso Smart Fit (LATAM, 16:00 BRT) | milagro.pantoja@buzzmonitor.com | es |
| 17929 | Cxpress Por qué bloquean tu WhatsApp (LATAM, 17:00 BRT) | laura.leon@cxpress.ai | es |

Histórico: em 2026-08-19 saíram 17689 (Conheça a Cxpress) e 17671 (Cxpress Vozxpress) — séries
apagadas no ClickMeeting por limite de disco, com zero inscritos — e entraram 17927, 17928 e 17929.
Em 2026-08-24 a 17927 ficou só com o Daniel e a 17933 + 17928 ficaram só com a Milagro.

## Detalhes que importam

- **Timezone:** o gatilho fixa `settings.timezone = America/Sao_Paulo`. A instância roda em
  **UTC−4** (confirmado por timestamps de execução), então sem esse override "7h" dispararia
  08:00 BRT. NÃO remover o timezone do workflow.
- **Credencial:** reaproveita a credencial Header Auth `ClickMeeting API` (id `Cn3XXNfzZXoS9DS8`,
  header `X-Api-Key`) que já existia na instância — bindada nos dois nós HTTP.
- **Editar séries/moderadores:** altere o node **Montar plano de convites** no editor, **ou**
  edite este JSON e dê `PUT /workflows/1TFA4xHvFEZQ5lns` (mantenha a paridade com o
  `config.json` da skill se quiser os dois em sincronia).
- **Testar sem esperar o cron:** clique **Test workflow** no editor — mas atenção, isso **envia
  convite de verdade** (não há dry-run embutido). Para só inspecionar o plano, rode até o node
  *Montar plano de convites* e veja a saída, ou use o `send_invites.py --dry-run` local.

## Fallback

`.github/workflows/convites-moderador.yml` continua no repo como **fallback manual desabilitado**
(sem cron, só `workflow_dispatch`). Se o n8n falhar: `gh workflow enable convites-moderador.yml`
+ aba Actions → Run workflow. Nunca deixar os dois agendados ao mesmo tempo (convite duplicado).

## Como foi criado

Gerado e publicado via a API pública do n8n (`POST /workflows` + `PUT` pra bindar credencial),
não pela UI. Se precisar recriar do zero, o builder está documentado no histórico do PR desta
migração; o JSON deste diretório é a fonte de verdade re-importável.
