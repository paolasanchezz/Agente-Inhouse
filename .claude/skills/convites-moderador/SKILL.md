---
name: convites-moderador
description: Envia convite diario de moderador (role=presenter) para a proxima sessao de cada serie recorrente do ClickMeeting (webinars perpetuos das LPs "conheca a marca" e "atencion al cliente"). Le config.json com mapping serie -> email do moderador, descobre a proxima sessao via API e dispara o invite nativo do ClickMeeting. 1 email por serie configurada. Roda manual (`/convites-moderador`) ou agendada diariamente via `/schedule`.
argument-hint: "[--dry-run] [--series RECURRING_CONFIG_ID]"
allowed-tools: Read, Bash, Skill
version: 1.0.0
---

# Skill: Convites diarios de moderador (ClickMeeting)

Voce envia, todo dia, 1 convite de moderador para a proxima sessao agendada de cada serie recorrente do ClickMeeting. O ClickMeeting nao tem feature nativa de "fixar moderador na serie", entao a gente automatiza o disparo diario externamente.

## Quando usar

- **Rotina diaria** via `/schedule` (cron sugerido: `0 8 * * *` em `America/Sao_Paulo`, mesmo horario da `/pauta-ia`) — uso primario.
- **Manual on-demand** apos editar o `config.json` (mudou o email do moderador, adicionou nova serie) e quiser disparar logo o convite do dia em vez de esperar o cron.
- **Dry-run para auditoria:** `/convites-moderador --dry-run` lista a proxima sessao de cada serie + email do moderador sem enviar nada.

## Quando NAO usar

- Para mandar convite a inscritos comuns — isso e o fluxo de registro (`clickmeeting-register.js`) que ja roda pelas LPs.
- Para alterar a configuracao da serie no ClickMeeting (room title, layout, etc.) — isso vive na propria UI do ClickMeeting; esta skill so dispara invite.
- Para configurar uma role que nao seja `presenter` — a API `/invitation/email` so aceita `listener` ou `presenter`. Para entregar role `moderator` (chat-only), seria outro fluxo (autologin_hash + email custom via SMTP) — fora desta skill por enquanto.

## Como rodar

```bash
# do CWD do repo
python .claude/skills/convites-moderador/send_invites.py            # envio normal
python .claude/skills/convites-moderador/send_invites.py --dry-run   # so imprime o plano
python .claude/skills/convites-moderador/send_invites.py --series 17560   # so Buzzcreators
```

Exit code: `0` = tudo enviado. `1` = alguma falha (ver stdout pra detalhe).

A skill em si e basicamente "rode o script e cole o stdout no chat". Sem args, default e envio real para todas as series em `config.json`.

## Configuracao

`config.json` na pasta da skill mantem o mapping serie -> moderador:

```jsonc
{
  "series": {
    "17529": { "label": "Cxpress", "moderator_email": "...", "lang": "br" },
    "17544": { "label": "Buzzmonitor Atencion (LATAM)", "moderator_email": "...", "lang": "es" },
    "17560": { "label": "Buzzcreators", "moderator_email": "...", "lang": "br" }
  }
}
```

- `recurring_config_id` (chave) deve bater com o que aparece em `landing-pages/buzzmonitor/_clickmeeting-api/next-webinar.js` (mapa `SERIES`).
- `lang` = idioma do email de convite enviado pelo ClickMeeting (pl|en|de|ru|es|fr|it|br). Alinhe ao idioma de quem recebe, nao do webinar.
- Para **adicionar** uma serie nova: edite o JSON, salve, e ela ja entra no proximo run. Sem deploy.
- Para **remover** temporariamente: apague o bloco da serie.

## Pre-requisitos

- `CLICKMEETING_API_KEY` em `.env.local` na raiz do repo (gitignored). Mesma chave usada por `clickmeeting-register.js` no Vercel — ver memoria `clickmeeting-api-access`.
- Python 3.10+ (usa typing moderno tipo `dict | None`).
- Acesso de rede a `api.clickmeeting.com`.

## Como o script funciona (passo a passo)

1. Carrega `config.json` e `CLICKMEETING_API_KEY`.
2. `GET /conferences/active` — retorna todas as sessoes ativas/agendadas da conta.
3. Para cada serie configurada: filtra `recurring_config_id` igual + `registration_enabled=1` + `starts_at` futuro, ordena por data e pega a **primeira**.
4. Para essa sessao: `POST /conferences/{room_id}/invitation/email/{lang}` com `attendees[0][email]=<moderador>`, `template=advanced`, `role=presenter`.
5. Imprime resultado linha-a-linha + resumo final.

Se uma serie nao tem sessao futura ativa, e ignorada (com SKIP no log) — nao quebra o run inteiro.

## Limitacoes conhecidas (1.0.0)

- **Role real entregue e `presenter`, nao `moderator`.** A API `/invitation/email` so aceita `listener|presenter`. Presenter ja inclui acesso de moderar chat + ver painel inteiro + ferramentas; se voce quiser estritamente chat-only (role nova "Chat Moderator" da UI), e outra arquitetura — autologin_hash + SMTP custom — fora desta v1.
- **Idempotencia:** a API nao deduplica convites por email. Se voce rodar 3x no mesmo dia, a Maira recebe 3 emails. Por isso o cron e 1x/dia.
- **Sem fallback de notificacao:** se o script falhar (rede caiu, API key revogada), nao notifica ninguem alem do exit code 1. Se rodar via `/schedule`, o stdout fica no log do schedule.

## Troubleshooting

| Sintoma | Causa | Fix |
|---|---|---|
| `[FATAL] CLICKMEETING_API_KEY ausente` | `.env.local` nao tem a chave ou foi rodado fora do repo | Setar a env var na sessao ou conferir `.env.local` na raiz |
| `[SKIP] ... — nenhuma sessao futura ativa` | Serie sem sessao agendada na conta no momento do run | Conferir no painel ClickMeeting se a recorrencia esta criando sessoes; eventualmente o `recurring_config_id` mudou |
| `[ERR] HTTP 422` ou erro de validacao | role=presenter pode ser rejeitada se o plano da conta nao tiver slots disponiveis | Conferir slots presenter livres no plano; usar `listener` (so participante, sem moderacao) como fallback temporario |
| Convite enviado mas pessoa nao recebe | Spam folder; ou email errado em `config.json` | Conferir spam; corrigir email; rodar de novo |

## Nao-objetivos (v1)

- Multiplos moderadores por serie (1 email por serie por dia).
- Role `moderator` (chat-only) — exigiria autologin_hash + SMTP.
- Agendamento embutido — agendamento e externo via `/schedule` ou `create_scheduled_task`.
- Verificar se moderador ja foi adicionado manualmente no painel ClickMeeting — sempre dispara, dependendo do cron pra cadencia.
