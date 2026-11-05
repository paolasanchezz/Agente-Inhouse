# Buzz Compass LATAM (totem + resultado no celular, em espanhol do México)

Cópia do Buzz Compass Brasil (`landing-pages/buzzmonitor/buzz-radar/`, no ar em `https://buzzcompass.buzzmonitor.com`)
traduzida para **espanhol do México** e com a busca da Buzzmonitor Trends rodando em **espanhol**. Toda a arquitetura,
o método de busca, o score e as proteções são os mesmos: o README do Brasil continua sendo a referência técnica
completa (como a pesquisa é montada, homônimos, posts reais, cache, scoring). Aqui fica só o que muda na versão LATAM
e o que falta para ela ir ao ar.

Criado em 2026-11-05 a partir da versão em produção (`dpl_8YJcDGhdYqWDTXZyJbSVuB2jABK3`, idêntica ao `main`).

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
| Fuso (séries diárias e datas) | `-3` (Brasília) | `-6` (Cidade do México, sem horário de verão desde 2022) |
| Prompts da IA (buscas, homônimo, relevância, narrativa) | português | espanhol do México, com exemplos mexicanos (Bimbo, Corona, Liverpool, OXXO) e as regras do `padrao-linguistico.md` ES-LATAM (tuteo, "celular", "reporte", "monitoreo") |
| Formato de número | 40.459 e 2,4% | 40,459 e 2.4% (`formatarNumerosEsMx` em `api/_lib/analise.js`) |
| Léxico de queixa/elogio | "reclamação", "péssimo", "amei"... | "queja", "pésimo", "estafa", "profeco", "me encanta", "lo recomiendo"... |
| Influenciadores | perfis em `pt` | perfis em `es` |
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

## Pendências antes de ir ao ar

1. **Domínio e projeto Vercel.** Decidir o endereço (sugestão: `buzzcompass-latam.buzzmonitor.com` ou similar), criar o
   projeto `buzzmonitor-lp-buzz-compass-latam` e apontar o DNS. Depois trocar `og:url`/`og:image` em `index.html` (hoje
   `buzzmonitor-lp-buzz-compass-latam.vercel.app`) e, se quiser, `TOTEM_BASE_URL`. O host da requisição já é aceito
   automaticamente pelo QR e pela URL de conversão.
2. **Variáveis de ambiente** no projeto novo: IA (`OPENAI_API_KEY` e/ou `ANTHROPIC_API_KEY`, `OPENAI_MODEL_NARRATIVA`),
   AC LATAM (tabela acima), e-mail (SendGrid) e, opcional, planilha. Sem IA o totem roda em modo reserva (busca pelo nome
   exato, categoria = palavras do setor, textos montados só com os números): funciona, mas a categoria fica genérica
   (no teste com "Tiendas de conveniencia" entrou conversa de política com a palavra "conveniencia").
3. **Publicação.** É projeto solo com backend (fora do pipeline estático): `python montar-deploy.py` monta a pasta e o
   deploy passa pela confirmação do hook `guard_vercel_deploy.py`. Nunca deployar este código no projeto do Brasil.
4. **Preço LATAM:** se houver um "Planes desde USD X", recolocar o selo em `totem-resultado.html`.
5. **Revisão nativa:** a copy passou pelos 3 pilares (linguístico ES-LATAM, fundamentos, anti-IA), mas vale uma leitura
   de alguém do time LATAM antes do evento, principalmente do texto de consentimento ("Al continuar, aceptas recibir el
   resultado por correo y que Buzzmonitor te contacte sobre Buzz Compass"), que no Brasil passou por quem cuida de LGPD.
6. **Teste com IA ligada** em preview da Vercel (1 Compass real de ponta a ponta conferindo e-mail, AC e QR).

## Rodar local

```
node landing-pages/buzzmonitor/buzz-compass-latam/dev-server.js 8939
```

Abrir `http://localhost:8939/` (totem; `/?idle=8000` para testar a volta ao início). Testes:
`for t in landing-pages/buzzmonitor/buzz-compass-latam/tests/*.test.js; do node $t; done` (13 arquivos, todos passando
em 2026-11-05).

Testado em 2026-11-05 sem IA, com busca real na Trends: OXXO x 7-Eleven x Circle K, setor "Tiendas de conveniencia"
(4,716 menções de OXXO; 43,427 posts com polaridade no setor). Tela do totem (1440x900) e página do QR no celular (375x812)
renderizaram tudo em espanhol, com QR, PNG do QR do e-mail (200) e Jotform LATAM carregado.
