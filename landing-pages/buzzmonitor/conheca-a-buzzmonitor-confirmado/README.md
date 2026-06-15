# conheca-a-buzzmonitor-confirmado

Página de confirmação pós-inscrição da LP `conheca-a-buzzmonitor`. Não é uma LP de captação: é a etapa intermediária entre o form custom ClickMeeting e a sala do webinar. Adaptada da família `cxpress/conheca-a-cxpress-confirmado` (mesma mecânica, brand Buzzmonitor).

URL em produção: `https://webinar.buzzmonitor.com/conheca-a-buzzmonitor-confirmado`

## Fluxo

1. O form da LP `conheca-a-buzzmonitor` registra o lead via `POST /api/clickmeeting-register` (serverless na sibling do guarda-chuva `webinar.buzzmonitor.com`).
2. No sucesso, o JS da LP grava em `sessionStorage` a chave `bm_webinar_confirmation` e redireciona pra cá.
3. Esta página lê a chave e mostra o **estado A** (confirmação + data/hora + countdown + CTA pra sala). Quando o countdown zera, entra na sala automaticamente após aviso de 10s (cancelável).
4. Sem a chave (visita direta, outro dispositivo, storage bloqueado, sem JS), mostra o **estado B**: "seu link está no email" + próxima sessão via `GET /api/next-webinar`.

## Shape do sessionStorage (`bm_webinar_confirmation`)

Mesmo shape v1 da família Cxpress (`join_url`, `email`, `first_name`, `starts_at`, `formatted_full_pt`, `saved_at`). Gravado pelo submit handler da LP mãe.

## Exceções deliberadas às GUIDELINES

- **`noindex, follow`** (exceção ao §15): página pós-ação, depende de sessionStorage. Precedente: `cxpress/conheca-a-cxpress-confirmado`.
- **Sem OG image** e sem placeholders `{{DOMAIN}}`: ninguém compartilha esta URL.
- **Sem estrutura mínima de LP** (§6): não há form nem captação aqui.

## Eventos GTM (container GTM-WFJVK858)

- `webinar_confirmation_view` (`has_join_url: true|false`) no load.
- `webinar_room_enter` (`method: 'click'|'auto'`) ao entrar na sala.
- O push sozinho não reporta nada: triggers/tags precisam ser criados no container.

## Publicação

Sempre em batch com a LP mãe (deploy atômico, evita janela em que o form redireciona pra 404):

```
/lp-publicar buzzmonitor "conheca-a-buzzmonitor,conheca-a-buzzmonitor-confirmado" webinar.buzzmonitor.com
```

## Placeholder ClickMeeting

Enquanto a Buzzmonitor não tem automação própria no ClickMeeting, o guarda-chuva usa a série do webinar Cxpress (env `CLICKMEETING_RECURRING_CONFIG_ID` no projeto Vercel `buzzmonitor-lp-monitoramento-concorrentes`). Quando a automação da marca existir, basta atualizar a env var e redeployar via `lp-publicar`.
