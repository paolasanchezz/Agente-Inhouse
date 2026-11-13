# Buzz Compass LATAM (totem + resultado no celular, em espanhol do México)

Cópia do Buzz Compass Brasil (`landing-pages/buzzmonitor/buzz-radar/`, no ar em `https://buzzcompass.buzzmonitor.com`)
traduzida para **espanhol do México** e com a busca da Buzzmonitor Trends rodando em **espanhol**. Toda a arquitetura,
o método de busca, o score e as proteções são os mesmos: o README do Brasil continua sendo a referência técnica
completa (como a pesquisa é montada, homônimos, posts reais, cache, scoring). Aqui fica só o que muda na versão LATAM
e o que falta para ela ir ao ar.

Criado em 2026-11-05 a partir da versão em produção (`dpl_8YJcDGhdYqWDTXZyJbSVuB2jABK3`, idêntica ao `main`).

## Endereço: `https://buzzcompass.buzzmonitor.com/es`

Decisão de 2026-11-05: a versão LATAM vive no **mesmo domínio do Brasil, no caminho `/es`**. O domínio continua no
projeto do Brasil (`buzzmonitor-lp-buzz-radar`); o `vercel.json` dele tem só um **proxy** (`rewrites` externos) que manda
`/es` e `/es/*` para este projeto (`buzzmonitor-lp-buzz-compass-latam`). Assim cada país tem as próprias variáveis de
ambiente (o token do AC LATAM nunca entra no projeto do Brasil) e o código do Brasil não muda.

- Todos os caminhos absolutos do front têm `/es` (`TotemRender.base`): CSS, scripts, `/es/api/totem`, `/es/api/totem-lead`,
  `/es/totem-resultado`, logos em `/es/assets/logos/` (o `montar-deploy.py` reescreve).
- Este projeto também atende `/es/*` sozinho (`rewrites` internos `/es/:path*` -> `/:path*` no `vercel.json`), então o
  endereço direto `https://buzzmonitor-lp-buzz-compass-latam.vercel.app/es` funciona igual.
- O link do QR, do e-mail e a URL de conversão saem sempre como `https://buzzcompass.buzzmonitor.com/es/...`, mesmo quando
  a requisição chega pelo proxy com o host `.vercel.app` (`baseUrl` em `api/totem-lead.js`; `TOTEM_BASE_URL` força outro).
- **Ordem de publicação:** primeiro este projeto (criar + deploy), depois o projeto do Brasil com o `vercel.json` novo.
  Se o Brasil subir antes, `/es` responde erro do proxy até o LATAM existir.

## Seletor de país (2026-11-10)

Na tela "¿Qué marca vamos a analizar?" o visitante escolhe o país (obrigatório): **México, Colombia, Chile, Argentina e
Perú**, e só esses. A lista fica em `api/_lib/paises.js` (servidor) e em `assets/totem-render.js` (front), com o mesmo
código ISO nos dois.

**A Trends não filtra post por país.** Testado em 2026-11-10 na API guest: `location`, `country` e `countries` em
`general_params` ou no corpo são ignorados (o volume não muda), e cerca de 90% dos posts não trazem a localização do
autor, então nem dá para filtrar depois. O país segmenta a análise por estes caminhos:

- **Buscas** (`api/_lib/buscas.js`, `planSystem`): a IA monta a busca para o mercado do país: concorrentes sugeridos que
  competem ali, `@perfil` e `#hashtag` locais da marca além do global, a categoria como se diz naquele país. Sem IA (modo
  reserva) o país não muda a busca.
- **Perfis ligados à marca:** a busca de influenciadores aceita `countries` com o código ISO (essa sim filtra). Se não houver
  perfil do país (depois de tirar as marcas da comparação), vale a lista geral em espanhol.
- **Fuso** das séries diárias e das chamadas da Trends (`comFuso` em `api/_lib/trends.js`, por análise, sem misturar duas
  análises simultâneas).
- **Leitura da IA:** o país vai no payload (`pais`), com a regra de nunca apresentar os números como sendo só daquele país.

O país entra na URL de análise como `p` (ordem `m, s, p, i, c`, a chave do cache), no link do QR/e-mail e no lead
(`pais` no log e no webhook da planilha; o Apps Script só grava a coluna se for atualizado). Links antigos sem `p`
continuam valendo, com México como referência. Testes: `tests/pais.test.js`.

## O que entrou (e o que ficou de fora)

- **Entrou:** o totem da raiz (`index.html` + `assets/totem-app.js`), o resultado compartilhado (`assets/totem-render.js`),
  a página aberta pelo QR e pelo e-mail (`totem-resultado.html` + `assets/totem-resultado.js`), a API (`api/totem.js`,
  `api/totem-lead.js`, `api/qr.js`, `api/_lib/`), testes, `dev-server.js` e `montar-deploy.py`.
- **Ficou de fora:** a LP antiga `/lp` (`lp.html`, `resultado.html`, `api/radar.js`). É o fluxo anterior ao totem e não é
  o que roda em `buzzcompass.buzzmonitor.com/`.

## O que muda em relação ao Brasil

| Ponto | Brasil | LATAM |
|---|---|---|
| Idioma da busca na Trends | `language: ['pt']` | `language: ['es']` (`api/_lib/trends.js`). **A Trends não filtra por país**: entram México, resto da América Latina e Espanha. |
| Fuso (séries diárias e datas) | `-3` (Brasília) | o do país escolhido (México `-6`, Colômbia e Peru `-5`, Argentina `-3`, Chile `-3`/`-4` conforme o horário de verão); sem país, `-6` |
| Prompts da IA (buscas, homônimo, relevância, narrativa) | português | espanhol do México, com exemplos mexicanos (Bimbo, Corona, Liverpool, OXXO) e as regras do `padrao-linguistico.md` ES-LATAM (tuteo, "celular", "reporte", "monitoreo") |
| Formato de número | 40.459 e 2,4% | 40,459 e 2.4% (`formatarNumerosEsMx` em `api/_lib/analise.js`) |
| Léxico de queixa/elogio | "reclamação", "péssimo", "amei"... | "queja", "pésimo", "estafa", "profeco", "me encanta", "lo recomiendo"... |
| Influenciadores | perfis em `pt` | perfis em `es`, primeiro os do país escolhido |
| País | não tem | seletor **País** (México, Colômbia, Chile, Argentina, Peru), ver seção abaixo |
| Textos sem IA (`narrativaPorDados`) | português | espanhol |
| E-mail do resultado | "Seu Buzz Compass de X está pronto" | "Tu Buzz Compass de X ya está listo" |
| Botão de demo do e-mail | `promo.buzzmonitor.com/plataforma-completa` | `content.buzzmonitor.com/plataforma-completa-social-media-latam` (LP LATAM no ar, `lang=es-419`) |
| Formulário de proposta (página do QR) | Jotform `252995108251662` + selo "Planos a partir de R$ 1.790" | Jotform `241825239057661` (o da LP `plataforma-completa-social-media-latam`), **sem selo de preço** |
| GTM | `GTM-WFJVK858` | `GTM-MKQBX2MG` (container LATAM) |
| Tag no ActiveCampaign | `Buzz Compass` | `Buzz Compass LATAM` (`TOTEM_AC_TAG_NOME` troca) |
| Campo `origem` do lead | `buzz-compass-totem` | `buzz-compass-totem-latam` |
| Campos do AC | títulos em português (`URL Conversão [AUTO]`, `UTM Source [AUTO]`...) | aceita também títulos em espanhol (`URL Conversión`, `Fuente`, `Medio`, `Campaña`, `Contenido`, `Término`), sempre com `[AUTO]` |
| Projeto Vercel | `buzzmonitor-lp-buzz-radar` | `buzzmonitor-lp-buzz-compass-latam` (**ainda não criado**) |

## Como os dados chegam ao ActiveCampaign LATAM

O lead sai pela function `api/totem-lead.js` no momento em que a pessoa toca em "Quiero mi Compass", antes da análise
terminar. O código já faz tudo (busca o contato pelo e-mail, cria ou atualiza, grava URL de conversão + UTMs nos campos
`[AUTO]`, aplica a tag, nunca cria deal). Para ligar no AC LATAM basta configurar as variáveis **no projeto Vercel
LATAM** (Sensitive), sem mexer em código:

| Variável | Valor |
|---|---|
| `ACTIVECAMPAIGN_API_URL` | URL da conta AC que recebe os leads LATAM (`https://CONTA.api-us1.com`) |
| `ACTIVECAMPAIGN_API_TOKEN` | chave da API dessa conta (Configurações > Desenvolvedor) |
| `TOTEM_AC_TAG_NOME` | opcional; padrão `Buzz Compass LATAM` (criada sozinha se não existir) |
| `ACTIVECAMPAIGN_TOTEM_LIST_ID` | opcional; inscreve numa lista. Decisão de marketing e consentimento |
| `TOTEM_EMAIL_VIA_AC` | `1` = o e-mail do resultado sai pela automação do AC (seção abaixo), sem SendGrid |
| `TOTEM_UTM_CAMPAIGN_PADRAO` | ex.: `[LATAM][Evento]-nome-do-evento`, para o lead não chegar sem campanha |

Como o projeto é separado, o token LATAM nunca se mistura com o do Brasil. O token do AC é full-access: só no painel
da Vercel, nunca no repositório nem no navegador.

Duas rotas extras, se o AC não for o único destino: `TOTEM_LEADS_WEBHOOK_URL` / `TOTEM_LEADS_WEBHOOK_TOKEN` (planilha via
`integracoes/google/buzz-compass-leads.gs` ou um webhook n8n) e o **Jotform da página do QR**, que já é o formulário que
alimenta o fluxo LATAM hoje.

**Atenção à dashboard CM LATAM:** o filtro `FILTRO_CM_LATAM` (`dashboard/MAPEAMENTO-CAMPOS-latam.md`) reconhece lead CM por
URL de conteúdo conhecida ou `utm_source` da whitelist. Um domínio novo do Compass LATAM não está na lista de URLs: se
esses leads tiverem de aparecer como CM, incluir o domínio no filtro ou garantir uma `utm_source` da whitelist no QR/link
do evento. Decisão do Victor.

## E-mail pelo ActiveCampaign (LATAM)

Na LATAM o e-mail do resultado sai por uma **automação do ActiveCampaign**, não pelo SendGrid. Basta a variável
`TOTEM_EMAIL_VIA_AC=1` no projeto Vercel: aí o SendGrid/Resend não é chamado (mesmo que a chave exista) e a function grava
no contato, numa atualização só, os campos que o e-mail usa e o **carimbo de envio** que dispara a automação.

**No AC (uma vez):**

1. **Campos do contato** (Contatos > Gerenciar campos > Adicionar campo). O título precisa ter `[AUTO]`:
   | Título | Tipo | O que recebe |
   |---|---|---|
   | `Buzz Compass Link [AUTO]` | Área de texto | link do resultado (`https://buzzcompass.buzzmonitor.com/es/totem-resultado?...`) |
   | `Buzz Compass QR [AUTO]` | Área de texto | endereço do PNG do QR (`.../es/api/qr?d=...`) |
   | `Buzz Compass Marca [AUTO]` | Texto | marca analisada (opcional; para o assunto) |
   | `Buzz Compass Envío [AUTO]` | Texto (ou data/hora) | data e hora do envio em UTC (`2026-11-13T21:05:01Z`), **muda a cada lead**: é o gatilho da automação. Tag no AC: `%BUZZ_COMPASS_ENVIO_AUTO%` |
   URL de conversão e UTMs: na conta AC LATAM os campos de último toque se chamam `URL_CONVERSAO`, `utm_source`,
   `utm_medium`, `utm_campaign`, `utm_content` e `utm_term` (sem `[AUTO]`, os mesmos que a dashboard CM LATAM lê). O código
   aceita esses títulos exatos; o jogo secundário (`utm_source_`, com `_` no fim) e os numerados ficam de fora. Se existir
   também um campo `[AUTO]`, ele tem prioridade. Campo que faltar: o contato e a tag seguem e a resposta avisa (`crm_avisos`).
   O campo `Buzz Compass Marca [AUTO]` é do tipo "Entrada de texto" (`text` na API).
2. **Automação:** gatilho "**Campo muda: Buzz Compass Envío [AUTO]**" (qualquer valor), **executa várias vezes** -> ação
   "Enviar e-mail". (Até 2026-11-13 o gatilho era a tag; trocado porque tag repetida não dispara de novo, ver abaixo.)
   Corpo: colar `email-ac/resultado-buzz-compass-es.html` (gerado a partir do e-mail do SendGrid). Conferir no editor do AC
   se as tags de personalização dos campos são as mesmas do arquivo (`%BUZZ_COMPASS_LINK_AUTO%`, `%BUZZ_COMPASS_QR_AUTO%`,
   `%BUZZ_COMPASS_MARCA_AUTO%`); o AC gera a tag a partir do título. Assunto sugerido:
   `Tu Buzz Compass de %BUZZ_COMPASS_MARCA_AUTO% ya está listo`.
3. Desligar o rastreio de cliques nesse e-mail, se possível (o AC reescreve links e as UTMs do botão de demo podem mudar).

**Por que o gatilho é o campo Envío e não a tag:** o AC responde **200** (não 422) quando a tag já está no contato e não
"adiciona" de novo, então quem rodava o Compass pela segunda vez (ou um teste repetido) não recebia o e-mail. Visto em
produção em 2026-11-13. O carimbo de envio muda a cada lead, inclusive da mesma pessoa e da mesma marca, e o link, o QR e a
marca vão no mesmo update, então já estão gravados quando a automação roda. A tag **Buzz Compass LATAM** continua sendo
aplicada, só para segmentar quem fez o Compass.

**Sem os campos Link, QR ou Envío no AC**, a resposta vem com `email: "falhou"` e `crm_avisos` nomeia o campo
(ex.: `campo_compass_envio_nao_encontrado`); o totem não promete o e-mail.

## De onde vem cada variável

| Variável | De onde tirar |
|---|---|
| `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` | As mesmas do projeto do Brasil. Vercel não mostra valor de variável Sensitive: pegar com quem as cadastrou (conta `contentmkt-9826`) ou gerar nova em platform.openai.com / console.anthropic.com. A Anthropic é só reserva. |
| `ACTIVECAMPAIGN_API_URL` / `ACTIVECAMPAIGN_API_TOKEN` | No AC LATAM: Configurações > Desenvolvedor (URL e chave da API). |
| `TOTEM_EMAIL_VIA_AC` | `1` (e-mail pela automação acima). |
| `TOTEM_UTM_CAMPAIGN_PADRAO` (opcional) | Texto livre, escolhido por quem organiza o evento, em minúsculas e com hífens (`conhecimento/config/convencao-utm.md`), ex.: `marketing-day-cdmx-2026`. Vale para todo lead que chegar sem `utm_campaign` na URL. Se o QR/cartaz de cada evento já levar `?utm_campaign=...`, não precisa. |
| `TOTEM_LEADS_WEBHOOK_URL` / `TOTEM_LEADS_WEBHOOK_TOKEN` (opcional) | Só se quiser os leads também numa planilha do Google. Seguir o passo a passo no topo de `integracoes/google/buzz-compass-leads.gs` (cria planilha, cola o script, define o TOKEN, publica como app da web, copia a URL `/exec`). Pode ser a planilha do Brasil (mesmos valores do projeto do Brasil; a coluna Origem separa `buzz-compass-totem-latam`) ou uma nova. |

## Como funciona o QR e o e-mail

São dois QR diferentes, e nenhum leva dado pessoal (nome e e-mail nunca entram na URL):

1. **QR na tela do totem** (fim do resultado, "Llévate tu Compass en el celular"): gerado no navegador por `assets/qr.js`
   com o link `/totem-resultado?m=MARCA&s=SETOR&c=CONCORRENTE...`. A pessoa aponta a câmera, abre a mesma análise no
   celular (vem do cache da Vercel, 24h; se expirou, roda de novo em até ~30s) e vê o formulário de proposta.
2. **QR no e-mail**: no mesmo instante do lead, `api/totem-lead.js` envia o e-mail com um PNG gerado por `api/qr.js`
   (Gmail e Outlook não mostram SVG) apontando para o mesmo link, mais o botão "Ver mi Compass". `api/qr.js` só gera QR
   de links `https` do próprio projeto. O link continua valendo depois do evento.

Para o e-mail sair: `SENDGRID_API_KEY` + `TOTEM_EMAIL_FROM` com remetente verificado no SendGrid (ou `RESEND_API_KEY` com
domínio verificado). Sem isso, o lead ainda vê o QR na tela, mas não recebe nada por e-mail.

## Estado e pendências (2026-11-13)

**No ar** em `https://buzzcompass.buzzmonitor.com/es` desde 2026-11-05 (projeto `buzzmonitor-lp-buzz-compass-latam`, proxy no
projeto do Brasil; visitante de país hispano que abre a raiz vai para `/es`). Variáveis no projeto: `OPENAI_API_KEY`,
`ANTHROPIC_API_KEY`, `ACTIVECAMPAIGN_API_URL`, `ACTIVECAMPAIGN_API_TOKEN`, `TOTEM_EMAIL_VIA_AC`.

1. **OpenAI sem crédito.** Em 2026-11-13 a chave do projeto LATAM respondia `429 credit_balance_exhausted` em toda chamada.
   A IA segue funcionando pelo Claude (`ANTHROPIC_API_KEY`), e desde esta data a reserva recebe o prazo cheio quando o OpenAI
   cai na hora (`api/_lib/llm.js`, `tests/llm-reserva.test.js`). Resolver: recarregar crédito na organização dessa chave ou
   trocar por uma chave de uma organização com saldo e republicar o projeto LATAM.
2. **Teste de ponta a ponta com lead real** (contato no AC LATAM, campos, tag, automação e e-mail): ainda não feito.
3. **Preço LATAM:** se houver um "Planes desde USD X", recolocar o selo em `totem-resultado.html`.
4. **Revisão nativa:** leitura de alguém do time LATAM, principalmente do texto de consentimento ("Al continuar, aceptas
   recibir el resultado por correo y que Buzzmonitor te contacte sobre Buzz Compass"), que no Brasil passou por quem cuida
   de LGPD.

**Publicar mudanças:** `python montar-deploy.py ~/Documents/buzzmonitor-lp-buzz-compass-latam` e deploy `--prod` desse projeto
(confirmação do hook `guard_vercel_deploy.py`). Nunca deployar este código no projeto do Brasil. Variável nova ou alterada na
Vercel só vale depois de um novo deploy.

## Rodar local

```
node landing-pages/buzzmonitor/buzz-compass-latam/dev-server.js 8939
```

Abrir `http://localhost:8939/es` (totem; `/es?idle=8000` para testar a volta ao início). O servidor local tira o `/es`. Testes:
`for t in landing-pages/buzzmonitor/buzz-compass-latam/tests/*.test.js; do node $t; done` (13 arquivos, todos passando
em 2026-11-05).

Testado em 2026-11-05 sem IA, com busca real na Trends: OXXO x 7-Eleven x Circle K, setor "Tiendas de conveniencia"
(4,716 menções de OXXO; 43,427 posts com polaridade no setor). Tela do totem (1440x900) e página do QR no celular (375x812)
renderizaram tudo em espanhol, com QR, PNG do QR do e-mail (200) e Jotform LATAM carregado.
