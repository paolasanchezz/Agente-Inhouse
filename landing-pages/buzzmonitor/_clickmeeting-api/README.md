# ClickMeeting serverless API — guarda-chuva `webinar.buzzmonitor.com`

Fonte versionada das duas serverless functions que servem o registro de webinar das LPs
"conheça a marca / atención al cliente" no guarda-chuva `webinar.buzzmonitor.com`
(projeto Vercel `buzzmonitor-lp-monitoramento-concorrentes`).

> **Por que estão aqui:** historicamente essas functions viviam **só na sibling** (fora do
> repo), sem versionamento — débito anotado na memória `clickmeeting-webinar-perpetuo`.
> Esta pasta passa a ser a fonte-verdade. `lp-publicar` **não** as deploya (o sync 0.5.d
> restaura sempre a versão do live), então mudanças aqui vão pro ar por deploy manual
> controlado (ver abaixo).

## Deploy alvo

```
{sibling}/buzzmonitor-lp-monitoramento-concorrentes/api/next-webinar.js
{sibling}/buzzmonitor-lp-monitoramento-concorrentes/api/clickmeeting-register.js
```

## Roteamento por LP (`?series=`)

`next-webinar.js` resolve a sala filtrando `/conferences/active` por `recurring_config_id`.
Sem parâmetro, usa `process.env.CLICKMEETING_RECURRING_CONFIG_ID` (série placeholder
compartilhada — hoje `17529`, Cxpress). Com `?series=<chave>`, usa o mapa `SERIES`:

| `series` | recurring_config_id | Webinar | LP |
|---|---|---|---|
| `atencion` | `17544` | Buzzmonitor Atención al Cliente | `/atencion-al-cliente-es` |
| `buzzcreators` | `17560` | Conheça o Buzzcreators (room_pin 286-555-426) | `/conheca-o-buzzcreators` (+ `-confirmado`) |

Chave desconhecida → fallback no env padrão (nunca quebra as LPs vizinhas).
`clickmeeting-register.js` lê `series` do body e repassa pro `next-webinar` interno.

## Como deployar uma mudança nas functions (fluxo manual controlado)

`lp-publicar` não carrega mudança de `api/` (o sync restaura a versão do live). Então:

1. `/lp-sync webinar.buzzmonitor.com` — popula a sibling com o último deploy READY (todas as LPs vizinhas + functions vivas).
2. Copiar estes 2 arquivos por cima de `{sibling}/api/`.
3. Conferir vizinhas intactas (hash) e fazer deploy: `cd {sibling} && npx vercel deploy --prod --yes --force --scope team_nC991VqUuSU2jXZN152xqqEg`.
4. Smoke test: `/api/next-webinar` (padrão) e `/api/next-webinar?series=atencion` devem responder `ok:true` com salas diferentes; registro com honeypot (`_hp` preenchido) não cria lead.

A API key (`CLICKMEETING_API_KEY`) é env **Sensitive** no Vercel. Para uso local/diagnóstico
ela está no `.env.local` da raiz do repo (gitignored). Base `https://api.clickmeeting.com/v1`,
header `X-Api-Key`. Ver memória `clickmeeting-api-access`.
