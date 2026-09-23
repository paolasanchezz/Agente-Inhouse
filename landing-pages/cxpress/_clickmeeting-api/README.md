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
Sem parâmetro, usa `process.env.CLICKMEETING_RECURRING_CONFIG_ID`. Hoje esse env aponta pra
`17689`, série **apagada** em 2026-08-19 — e está certo assim: nenhuma LP do domínio depende
mais do padrão, então chave errada falha em `no_upcoming` em vez de anunciar o webinar de outra
LP. Com `?series=<chave>`, usa o mapa `SERIES`:

| `series` | recurring_config_id | Webinar | LP |
|---|---|---|---|
| `bloqueo-whatsapp` | `17929` | Por qué bloquean tu WhatsApp (ES-LATAM, room_pin 184-935-658, tz America/Mexico_City, 14:00 MX) | `/webinar-bloqueo-whatsapp` (+ `-confirmado`) |

Aposentadas em 2026-08-19 (apagadas no ClickMeeting por limite de disco, zero inscritos):
`ia-voz` (`17671`, Cxpress Vozxpress) e `17689` (Conheça a Cxpress, a antiga série padrão do
domínio). As LPs `/case-ia-de-voz` e `/conheca-a-cxpress` seguiram no ar com aviso de encerradas.

Chave desconhecida → fallback no env padrão (nunca quebra as LPs vizinhas).
`clickmeeting-register.js` lê `series` do body e repassa pro `next-webinar` interno.
**E-mail de confirmação:** `SERIES_LANG` mapeia `bloqueo-whatsapp` → `es`. Novas séries LATAM
entram do mesmo jeito; as demais usam o default `br`.
**Thank-you de segurança:** `SERIES_THANK_YOU` dá a página `-confirmado` de cada série, usada
só quando a API não devolve a URL da sala.
**Janela da sessão:** o filtro usa `ends_at`, não `starts_at` — numa série diária a próxima
sessão só nasce ~10 min depois desta terminar, e filtrar pelo início deixava o formulário fora
do ar ~30-40 min por dia.

**Histórico do env default (`CLICKMEETING_RECURRING_CONFIG_ID`):** `17497` (encerrada 11/jun) →
`17529` (12/jun) → **`17689`** (06/jul — sala `10074506` "Conheça Cxpress", room_pin
786-934-264, tz America/Sao_Paulo, `automated`/`type:2`). Toda troca dessas = PATCH da env var
no Vercel (instâncias production + development) + redeploy via `/lp-publicar` — **sem** mudança
de HTML (a LP é fixa e resolve a série pelo env em runtime). Ao trocar, atualizar também o
mapping da skill `/convites-moderador` (`config.json`) para a série nova, senão o convite diário
de moderador para de sair para o webinar Cxpress.

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
copia servida vive em `landing-pages/dominios/content-cxpress-io/extras/api/` e entra no dist pelo
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
