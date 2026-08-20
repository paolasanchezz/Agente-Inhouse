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
Sem parâmetro, usa `process.env.CLICKMEETING_RECURRING_CONFIG_ID`. Hoje esse env aponta pra
`17529`, uma série **morta** — e está certo assim: nenhuma LP do domínio depende mais do
padrão (todas mandam `?series=`), então o env morto faz chave errada falhar em `no_upcoming`
em vez de anunciar silenciosamente o webinar de outra LP. Com `?series=<chave>`, usa `SERIES`:

| `series` | recurring_config_id | Webinar | LP |
|---|---|---|---|
| `atencion` | `17701` | Buzzmonitor Atención al Cliente (ES-LATAM) — série recriada 2026-07-08 (antiga `17544` esgotou as sessões) | `/atencion-al-cliente-es` (+ `-confirmado`) |
| `buzzcreators` | `17727` | Conheça o Buzzcreators — série recriada 2026-07-14 (antiga `17560` esgotou as sessões), room_pin 276-382-621 | `/conheca-o-buzzcreators` (+ `-confirmado`) |
| `mcp-es` | `17646` | Buzzmonitor Que es MCP (ES-LATAM, room_pin 224-255-882, tz America/Mexico_City) | `/que-es-mcp` (+ `-confirmado`) |
| `listening-es` | `17927` | Tu primer listening en 5 pasos (ES-LATAM, room_pin 568-312-489, tz America/Mexico_City, 09:00 MX) | `/primer-listening-5-pasos` (+ `-confirmado`) |
| `smartfit-es` | `17928` | Caso Smart Fit Latam (ES-LATAM, room_pin 854-775-474, tz America/Mexico_City, 13:00 MX) | `/caso-smartfit` (+ `-confirmado`) |

Aposentada em 2026-08-19: `mcp` (`17601`, Buzzmonitor MCP PT-BR). Série apagada no ClickMeeting
por limite de disco, com zero inscritos em 57 sessões. A LP `/mcp-na-pratica-p` seguiu no ar com
aviso de encerrada e não chama mais estas functions.

Chave desconhecida → cai no env padrão. Se o env também não resolver, a function responde
`no_series` em vez de devolver a próxima sessão de qualquer série da conta (era esse o risco:
a LP anunciar o webinar errado).
`clickmeeting-register.js` lê `series` do body e repassa pro `next-webinar` interno.
**E-mail de confirmação ES:** `SERIES_LANG` mapeia `atencion`, `mcp-es`, `listening-es` e
`smartfit-es` → `es`. As demais usam o default `br`.
**Thank-you de segurança:** `SERIES_THANK_YOU` dá a página `-confirmado` de cada série, usada
só quando a API não devolve a URL da sala. Até 2026-08-19 isso apontava pra `home.cxpress.io`
mesmo aqui no domínio da Buzzmonitor.
**Janela da sessão:** o filtro usa `ends_at`, não `starts_at`. Numa série diária a próxima
sessão só nasce ~10 min depois desta terminar; filtrando pelo início, o formulário de todas as
LPs ficava fora do ar ~30-40 min por dia.

## Como deployar uma mudanca nas functions

Desde a migracao pro CI (2026-07-15) estes arquivos sobem **junto com o guarda-chuva**: a
copia servida vive em `landing-pages/dominios/webinar-buzzmonitor-com/extras/api/` e entra no dist pelo
`extra_files` do manifesto. O fluxo e: editar **as duas copias** (esta, canonica, e a de
`extras/api/`), abrir PR, deixar o `lp-deploy.yml` publicar.

**Nao rodar `vercel deploy` a mao.** O hook `guard_vercel_deploy.py` bloqueia deploy manual em
dominio migrado, e mesmo que passasse seria sobrescrito no push seguinte (incidente 2026-08-03).
O fluxo antigo com `/lp-sync` + `vercel deploy --force` que estava documentado aqui morreu junto
com o modelo sibling: a skill `/lp-sync` foi desativada.

Smoke test depois do deploy: `/api/next-webinar?series=<chave>` de cada serie viva responde
`ok:true` com salas diferentes; chave inexistente responde `no_upcoming`; registro com honeypot
(`_hp` preenchido) nao cria lead.


A API key (`CLICKMEETING_API_KEY`) é env **Sensitive** no Vercel. Para uso local/diagnóstico
ela está no `.env.local` da raiz do repo (gitignored). Base `https://api.clickmeeting.com/v1`,
header `X-Api-Key`. Ver memória `clickmeeting-api-access`.
