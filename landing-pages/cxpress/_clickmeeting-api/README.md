# ClickMeeting serverless API — guarda-chuva `content.cxpress.io`

Fonte versionada das duas serverless functions que servem o registro de webinar das LPs
de webinar perpétuo Cxpress no guarda-chuva `content.cxpress.io`
(projeto Vercel `cxpress-lp-playbook-whatsapp2026`).

> **Por que estão aqui:** historicamente essas functions viviam **só na sibling** (fora do
> repo), sem versionamento — o mesmo débito que o guarda-chuva Buzzmonitor já resolveu
> (ver `landing-pages/buzzmonitor/_clickmeeting-api/`). Esta pasta passa a ser a fonte-verdade.
> `lp-publicar` **não** as deploya (o sync 0.5.d restaura sempre a versão do live), então
> mudanças aqui vão pro ar por deploy manual controlado (ver abaixo).

## Deploy alvo

```
{sibling}/cxpress-lp-playbook-whatsapp2026/api/next-webinar.js
{sibling}/cxpress-lp-playbook-whatsapp2026/api/clickmeeting-register.js
```

## Roteamento por LP (`?series=`)

`next-webinar.js` resolve a sala filtrando `/conferences/active` por `recurring_config_id`.
Sem parâmetro, usa `process.env.CLICKMEETING_RECURRING_CONFIG_ID` (série placeholder do
domínio — hoje `17529`, `conheca-a-cxpress`). Com `?series=<chave>`, usa o mapa `SERIES`:

| `series` | recurring_config_id | Webinar | LP |
|---|---|---|---|
| _(sem série)_ | `17529` (env) | Conheça a Cxpress (placeholder do domínio) | `/conheca-a-cxpress` (+ `-confirmado`) |
| `ia-voz` | `17671` | Cxpress Vozxpress — estudo de caso IA de Voz (conf id 10070428, room_pin 754-174-641, PT-BR) | `/case-ia-de-voz` |

Chave desconhecida → fallback no env padrão (nunca quebra as LPs vizinhas).
`clickmeeting-register.js` lê `series` do body e repassa pro `next-webinar` interno.
**E-mail de confirmação:** `SERIES_LANG` mapeia série → idioma; `ia-voz` é PT-BR e cai no
default `br`. Adicionar `'chave':'es'` quando existir série LATAM neste domínio.

## Como deployar uma mudança nas functions (fluxo manual controlado)

`lp-publicar` não carrega mudança de `api/` (o sync restaura a versão do live). Então:

1. `/lp-sync content.cxpress.io` — popula a sibling com o último deploy READY (todas as LPs vizinhas + functions vivas).
2. Copiar estes 2 arquivos por cima de `{sibling}/api/`.
3. Conferir vizinhas intactas (hash) e fazer deploy: `cd {sibling} && npx vercel deploy --prod --yes --force --scope team_nC991VqUuSU2jXZN152xqqEg`.
4. Smoke test: `/api/next-webinar` (padrão → série 17529) e `/api/next-webinar?series=ia-voz` (→ série 17671) devem responder `ok:true` com salas **diferentes**; registro com honeypot (`_hp` preenchido) não cria lead.

**Ordem inegociável:** a function precisa conhecer a chave ANTES de a LP mandar `?series=`,
senão `?series=ia-voz` cai no fallback `17529` (webinar errado). Como a LP `case-ia-de-voz`
já está no ar mandando `series=ia-voz`, deployar estas functions é o que efetivamente liga
o webinar correto.

A API key (`CLICKMEETING_API_KEY`) é env **Sensitive** no Vercel. Para uso local/diagnóstico
ela está no `.env.local` da raiz do repo (gitignored). Base `https://api.clickmeeting.com/v1`,
header `X-Api-Key`. Ver memória `clickmeeting-api-access`.
