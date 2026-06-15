# conheca-o-buzzcreators-confirmado

Página de confirmação pós-inscrição da LP `conheca-o-buzzcreators`. Não é uma LP de captação: é a etapa intermediária entre o form custom ClickMeeting e a sala do webinar. Adaptada da família `cxpress/conheca-a-cxpress-confirmado` (mesma mecânica, brand Buzzcreators).

URL em produção: `https://webinar.buzzmonitor.com/conheca-o-buzzcreators-confirmado`

## Fluxo

1. O form da LP `conheca-o-buzzcreators` registra o lead via `POST /api/clickmeeting-register` (serverless na sibling do guarda-chuva `webinar.buzzmonitor.com`).
2. No sucesso, o JS da LP grava em `sessionStorage` a chave `bc_webinar_confirmation` e redireciona pra cá.
3. Esta página lê a chave e mostra o **estado A** (confirmação + data/hora + countdown + CTA pra sala). Quando o countdown zera, entra na sala automaticamente após aviso de 10s (cancelável).
4. Sem a chave (visita direta, outro dispositivo, storage bloqueado, sem JS), mostra o **estado B**: "seu link está no email" + próxima sessão via `GET /api/next-webinar`.

## Shape do sessionStorage (`bc_webinar_confirmation`)

Mesmo shape v1 da família Cxpress (`join_url`, `email`, `first_name`, `starts_at`, `formatted_full_pt`, `saved_at`). Gravado pelo submit handler da LP mãe. Chave diferente da Buzzmonitor (`bm_`) porque as duas LPs moram no mesmo domínio e compartilham o sessionStorage.

## Exceções deliberadas às GUIDELINES

- **`noindex, follow`** (exceção ao §15): página pós-ação, depende de sessionStorage. Precedente: `cxpress/conheca-a-cxpress-confirmado`.
- **Sem OG image** e sem placeholders `{{DOMAIN}}`: ninguém compartilha esta URL.
- **Sem estrutura mínima de LP** (§6): não há form nem captação aqui.
- **Sem GTM**: `brand/buzzcreators/tracking.json` está com containers null. Os pushes de `dataLayer` ficam no código (no-op) pra quando o container existir.

## Publicação

Sempre em batch com a LP mãe (deploy atômico, evita janela em que o form redireciona pra 404):

```
/lp-publicar buzzcreators "conheca-o-buzzcreators,conheca-o-buzzcreators-confirmado" webinar.buzzmonitor.com
```

## Placeholder ClickMeeting

Enquanto o Buzzcreators não tem automação própria no ClickMeeting, o guarda-chuva usa a série do webinar Cxpress (env `CLICKMEETING_RECURRING_CONFIG_ID` no projeto Vercel `buzzmonitor-lp-monitoramento-concorrentes`). Quando a automação da marca existir, será preciso decidir como servir séries distintas por LP (hoje o endpoint é único por domínio).
