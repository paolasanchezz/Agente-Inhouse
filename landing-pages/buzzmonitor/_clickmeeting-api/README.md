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
| `buzzcreators` | `18050` | Conheça o Buzzcreators (PT-BR, room_pin 983-466-465, tz America/Sao_Paulo, 10:20 BRT, sessão de 25 min) — série recriada 2026-09-02 (antiga `17727` esgotou as sessões) | `/conheca-o-buzzcreators` (+ `-confirmado`) |
| `mcp-es` | `17646` | Buzzmonitor Que es MCP (ES-LATAM, room_pin 224-255-882, tz America/Mexico_City) | `/que-es-mcp` (+ `-confirmado`) |
| `listening-es` | `17927` | Tu primer listening en 5 pasos (ES-LATAM, room_pin 568-312-489, tz America/Mexico_City, 09:00 MX) | `/primer-listening-5-pasos` (+ `-confirmado`) |
| `smartfit-es` | `17928` | Caso Smart Fit Latam (ES-LATAM, room_pin 854-775-474, tz America/Mexico_City, 13:00 MX) | `/caso-smartfit` (+ `-confirmado`) |
| `crisis-es` | `17933` | Gestión de Crisis (ES-LATAM, room_pin 361-697-942, tz America/Mexico_City) | `/gestion-crisis` (+ `-confirmado`) |
| `concorrentes-br` | `18043` | Como construir um monitoramento de concorrentes (PT-BR, room_pin 692-573-549, tz America/Sao_Paulo, 09:00 BRT, sessão de 25 min) | `/perpetuo-monitoramento-concorrentes` (+ `-confirmado`) |
| `concorrentes-pt` | `18086` | Como construir um monitoramento de concorrentes Portugal (PT-PT, room_pin 355-724-775, tz Europe/Lisbon, 10:00 hora de Lisboa = 06:00 BRT, sessão de 30 min) | `/perpetuo-monitoramento-concorrentes-pt` (+ `-confirmado`) |

Aposentada em 2026-08-19: `mcp` (`17601`, Buzzmonitor MCP PT-BR). Série apagada no ClickMeeting
por limite de disco, com zero inscritos em 57 sessões. A LP `/mcp-na-pratica-p` seguiu no ar com
aviso de encerrada e não chama mais estas functions.

Chave desconhecida → cai no env padrão. Se o env também não resolver, a function responde
`no_series` em vez de devolver a próxima sessão de qualquer série da conta (era esse o risco:
a LP anunciar o webinar errado).
`clickmeeting-register.js` lê `series` do body e repassa pro `next-webinar` interno.
**Idioma por série:** `SERIES_LANG` escolhe **duas** coisas ao mesmo tempo: o pack de
mensagens devolvido ao visitante (`MESSAGES`) e o idioma do e-mail de confirmação do ClickMeeting.
Mapeia `atencion`, `mcp-es`, `listening-es`, `smartfit-es` e `crisis-es` → `es`, e
`concorrentes-pt` → `pt` (PT-PT). As demais usam o default `br` (é o caso de `buzzcreators` e
`concorrentes-br`). Como o ClickMeeting **não tem código pt-PT** (aceita só pl, en, de, ru, es,
fr, it, br), `CM_EMAIL_LANG` traduz `pt` → `br` na hora de pedir o e-mail de confirmação: a LP
responde em PT-PT, o e-mail sai no pack português da própria ferramenta.

**Data formatada: só serve para BR.** Os campos `formatted_date_pt` / `formatted_time_pt` /
`formatted_full_pt` do `next-webinar.js` são gerados em `pt-BR` + `America/Sao_Paulo`, fixo. LP de
outra região **não** deve usá-los, senão anuncia a hora de Brasília: as LPs ES (Cidade do México)
e a LP PT (Lisboa) formatam no cliente a partir de `starts_at`, que é ISO com offset. Se uma
série nova for de fora do Brasil, repetir esse padrão.
**Thank-you de segurança:** `SERIES_THANK_YOU` dá a página `-confirmado` de cada série, usada
só quando a API não devolve a URL da sala. Até 2026-08-19 isso apontava pra `home.cxpress.io`
mesmo aqui no domínio da Buzzmonitor.
**Janela da sessão:** o filtro usa `ends_at`, não `starts_at`. Numa série diária a próxima
sessão só nasce ~10 min depois desta terminar; filtrando pelo início, o formulário de todas as
LPs ficava fora do ar ~30-40 min por dia.

## Campos de inscricao (`clickmeeting-register.js`)

| ClickMeeting | Payload da LP | Obrigatorio |
|---|---|---|
| `registration[1]` Nome | `first_name` | sim |
| `registration[2]` Sobrenome | `last_name` | sim na LP (a sala nao tem o campo 2; a API ignora campo que a sala nao tem) |
| `registration[3]` E-mail | `email` | sim (e-mail corporativo, regra da conta) |
| `registration[10]` Empresa | `company` | sim, na sala e na LP |
| `registration[11]` Telefone | `phone` | sim na LP desde 2026-09-23 |

**Telefone:** vai **so com digitos, DDI + numero, sem `+`** (`5511987654321`). Quem monta e o
componente `landing-pages/_componentes/campo-telefone/` (bandeira + DDI na LP); a function
refaz a limpeza e exige 8 a 15 digitos (E.164). A API do ClickMeeting **nao valida** o formato
do telefone (sondado em 2026-09-23), entao essa checagem e a unica.

**Serie nova:** no painel do ClickMeeting, o formulario de inscricao precisa ter o campo
**Telefone** (id 11). Conferir sem criar lead: `curl -sL https://elifegroup.clickmeeting.com/{slug}/register`
e procurar `"11":{"id":11,...,"type":"phoneNumber"` no HTML. Se o campo estiver marcado como
obrigatorio na sala e a LP nao mandar, a API devolve 422 e a inscricao se perde (o que
aconteceu com Empresa em 2026-08-25). Ordem segura: sala com o campo opcional, LP enviando,
so depois obrigatorio na sala.

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
