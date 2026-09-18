# Perpétuos — grade de webinars (página interna)

Página de referência interna publicada em **https://content.buzzmonitor.com/perpetuos**.
Expõe a tabela dos webinars perpétuos ativos no ClickMeeting: região do público, horário BR,
horário MX e link da landing page de inscrição de cada um. Feita para ser compartilhada com o time.

Não é uma LP de captação: `noindex, nofollow`, sem formulário, sem GTM.

## Fonte dos dados

Os horários e os links **não** são gerados em runtime — a página é HTML estático. O conteúdo
espelha o doc vivo **"🔁 Perpétuos"** no Notion (`3a73934026fd80849748e6f6073ce143`), que por
sua vez é reconstruído a partir de:

- **Horários e séries ativas:** API do ClickMeeting, `GET /conferences/active` (filtrar
  `type: 2` + `automated_enabled: 1`; ler `starts_at`, `timezone`, `recurring_config_id`).
- **Região (BR / PT / LATAM):** inferida da própria LP de inscrição — `<html lang>` + `og:locale`
  do `index.html` da LP (`pt-BR` -> BR, `pt-PT` -> PT, `es-419`/`es_LA`/`es_MX` -> LATAM). Não
  usar o idioma do título do webinar como critério: português do Brasil e de Portugal se
  confundem, e é por isso que a coluna existe.
- **Links das LPs:** mapa `SERIES` em `landing-pages/{buzzmonitor,cxpress}/_clickmeeting-api/next-webinar.js`
  (`recurring_config_id` → chave `?series=`) cruzado com o domínio de cada guarda-chuva.

## Como atualizar

Quando entrar webinar novo, mudar horário ou uma série for encerrada:

1. Reconsultar a API do ClickMeeting e o mapa `SERIES` (fontes acima).
2. Editar as linhas da tabela em `index.html` e a data no selo "Atualizado em ...".
3. Atualizar o doc do Notion na mesma passada — as duas superfícies têm que contar a mesma história.
4. Publicar com `/lp-publicar buzzmonitor perpetuos content.buzzmonitor.com`.

## Estado registrado nesta versão

Última verificação: **18/09/2026** — 9 séries ativas, todas rodando diariamente (inclusive
fim de semana). Entrou **18086** "Como criar uma monitorização de concorrentes Portugal"
(PT-PT, 10:05 hora de Lisboa, tz `Europe/Lisbon`, LP `/perpetuo-monitoramento-concorrentes-pt`).
A série já existia no mapa `SERIES` desde antes, mas nunca tinha entrado na tabela — era a
lacuna apontada em 18/09.

A linha PT abre a tabela porque a ordenação é pelo horário BR e 10:05 de Lisboa dá 06:05 em
Brasília. Esse é o único webinar da grade cujo fuso tem horário de verão: a partir de
**25/10/2026** (último domingo de outubro, Lisboa volta pra WET/UTC+0) as mesmas 10:05 passam
a cair às 07:05 no Brasil e às 04:05 no México — as colunas BR e MX dessa linha precisam ser
corrigidas nessa data, e de novo na virada pra WEST no fim de março. As duas ressalvas estão
escritas na própria página, no aviso "Fuso".

Histórico anterior:

- **02/09/2026** — entrou **18043** "Como construir um monitoramento de concorrentes" (PT-BR,
  09:00 BRT, sessão de 25 min) e **17727** (Case Buzzcreators) esgotou as sessões, sendo
  recriada como **18050**, que roda **10:20 BRT** — era 09:40.
- **04/09/2026** — a coluna de idioma ("Português" / "Espanhol · LATAM") saiu e entrou a coluna
  **Região**, com bandeira: 🇧🇷 BR, 🇵🇹 PT e 🌎 LATAM (globo porque LATAM não é um país).
- **19/08/2026** — as três séries em português que existiam antes (17671 Vozxpress, 17689
  Conheça a Cxpress, 17601 Buzzmonitor MCP) foram encerradas e não constam na tabela.

Nos webinars em português do Brasil o horário foi escolhido para o Brasil, então a coluna de
México cai bem cedo (06:00 e 07:20) de propósito — está ali só como referência de fuso.
