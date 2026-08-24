# Perpétuos — grade de webinars (página interna)

Página de referência interna publicada em **https://content.buzzmonitor.com/perpetuos**.
Expõe a tabela dos webinars perpétuos ativos no ClickMeeting: horário BR, horário MX e link
da landing page de inscrição de cada um. Feita para ser compartilhada com o time.

Não é uma LP de captação: `noindex, nofollow`, sem formulário, sem GTM.

## Fonte dos dados

Os horários e os links **não** são gerados em runtime — a página é HTML estático. O conteúdo
espelha o doc vivo **"🔁 Perpétuos"** no Notion (`3a73934026fd80849748e6f6073ce143`), que por
sua vez é reconstruído a partir de:

- **Horários e séries ativas:** API do ClickMeeting, `GET /conferences/active` (filtrar
  `type: 2` + `automated_enabled: 1`; ler `starts_at`, `timezone`, `recurring_config_id`).
- **Links das LPs:** mapa `SERIES` em `landing-pages/{buzzmonitor,cxpress}/_clickmeeting-api/next-webinar.js`
  (`recurring_config_id` → chave `?series=`) cruzado com o domínio de cada guarda-chuva.

## Como atualizar

Quando entrar webinar novo, mudar horário ou uma série for encerrada:

1. Reconsultar a API do ClickMeeting e o mapa `SERIES` (fontes acima).
2. Editar as linhas da tabela em `index.html` e a data no selo "Atualizado em ...".
3. Atualizar o doc do Notion na mesma passada — as duas superfícies têm que contar a mesma história.
4. Publicar com `/lp-publicar buzzmonitor perpetuos content.buzzmonitor.com`.

## Estado registrado nesta versão

Última verificação: **24/08/2026** — 7 séries ativas, todas rodando diariamente (inclusive
fim de semana). As três séries em português (17671 Vozxpress, 17689 Conheça a Cxpress,
17601 Buzzmonitor MCP) foram encerradas em 19/08/2026 e não constam na tabela.
