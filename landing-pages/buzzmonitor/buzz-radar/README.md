# Buzz Compass — protótipo funcional (Marketing Day)

> **Nome do produto: Buzz Compass** (antes Buzz Radar; trocado em 2026-10-16 porque um concorrente já usa "Radar". Passou por Buzz Scan no mesmo dia).
> Mudou só o que as pessoas leem (páginas, e-mail, prompts da IA). Continuam como estavam, de propósito, até haver
> decisão: nome da pasta (`buzz-radar`), arquivos e rotas (`api/radar.js`, `/api/radar`), projeto na Vercel
> (`buzzmonitor-lp-buzz-radar`), domínio antigo (`buzzradar.buzzmonitor.com`, registrado no projeto e sem DNS; pode ser removido), `canonical`/`og:url`/
> `og:image` do `index.html`, a tag do ActiveCampaign (hoje "Buzz Radar" no pedido
> original: criar/renomear para "Buzz Compass" antes de ligar o CRM).


LP interativa: o lead preenche empresa/site/segmento/cargo/e-mail, a function `api/radar.js`
cruza dados reais do Buzzmonitor Trends (versão guest, pública) para o segmento informado,
calcula scores determinísticos e pede pra uma IA escrever a narrativa em cima desses números. O
resultado abre numa página própria (`resultado.html`), com o diagnóstico, gráficos reais e CTA.
Racional completo da ideia e da investigação técnica: ver o plano da sessão que criou este
protótipo (`.claude/plans/playful-baking-forest.md` na máquina de quem gerou isto, se ainda
existir) — aqui fica só o operacional.

**Provedor de IA com fallback automático:** a function tenta `OPENAI_API_KEY` primeiro (Chat
Completions com `response_format: json_schema`, JSON garantido) e, se ausente ou a chamada
falhar, tenta `ANTHROPIC_API_KEY` (Claude, via tool-use forçado, schema igualmente garantido). As
duas podem ficar configuradas ao mesmo tempo — serve de rede de segurança pra não depender de um
único provedor estar com crédito disponível no momento da demo (já aconteceu na prática: a conta
Anthropic ficou sem saldo em 2026-09-02, resolvido trocando pra OpenAI sem precisar reescrever
nada além do provedor). Se nenhuma chave estiver configurada, ou as duas falharem, `narrativa`
vem `null` e a página cai no fallback (ver seção de env vars abaixo).

## Por que isto está fora do pipeline `lp-*` padrão

`landing-pages/CONTEXT.md` §9 é explícito: LP com backend está fora do escopo do pipeline
estático. Este projeto segue o único precedente real do repo,
`landing-pages/buzzmonitor/_clickmeeting-api/` (webinar.buzzmonitor.com): runtime de Vercel
Serverless Function zero-config (`module.exports = async (req, res) => {}`, `fetch` nativo, sem
dependências npm), documentado aqui em vez de só existir no sibling.

**`/lp-publicar` não deploya isto sozinho** — o passo de publicação (`vercel deploy`) precisa
incluir a pasta `api/` junto com `index.html` e `resultado.html`, e o hook
`guard_vercel_deploy.py` pede confirmação explícita antes de qualquer deploy manual (correto:
não pular essa confirmação).

## Arquivos

- `index.html` — LP principal (hero, problema, form, diferencial, prova, urgência, CTA, footer).
- `resultado.html` — página de diagnóstico. Recebe os dados via parâmetro `?d=` (JSON
  base64url-encoded na própria URL — sem banco de dados novo; o link em si é o relatório,
  compartilhável e permanente). `noindex, nofollow` de propósito (não é conteúdo pra indexar).
- `api/radar.js` — a function. Ver cabeçalho do arquivo pra o pipeline completo.
- `SCORING.md` — fórmula dos 4 sub-scores + Compass Score final, 100% determinística (não vem da
  IA). Serve de anexo pro pitch ("defesa data-driven").

## Variáveis de ambiente (configurar no painel Vercel do projeto, como Sensitive)

| Variável | Obrigatória | Efeito se ausente |
|---|---|---|
| `OPENAI_API_KEY` | Uma das duas (OpenAI ou Anthropic), pra narrativa em texto | Se também faltar `ANTHROPIC_API_KEY`, a function ainda responde com os scores reais; `narrativa` vem `null` e o front mostra um texto de fallback genérico em cima dos números (nunca quebra a página). |
| `OPENAI_MODEL` | Não (default `gpt-4o-mini`) | Usa o default. |
| `ANTHROPIC_API_KEY` | Opcional, usada se `OPENAI_API_KEY` faltar ou falhar | Mesmo efeito acima. |
| `ANTHROPIC_MODEL` | Não (default `claude-sonnet-5`) | Usa o default. |
| `ACTIVECAMPAIGN_API_URL` / `ACTIVECAMPAIGN_API_TOKEN` | Não | Sem as duas, a sincronização de contato no CRM é pulada silenciosamente (log apenas). Ver decisão abaixo. |
| `ACTIVECAMPAIGN_TAG_ID` | Não | Sem isso, sincroniza o contato mas não aplica tag. |

**Decisão de escopo — ActiveCampaign desligado por padrão:** o token do AC é full-access na conta
inteira, e existe um guardrail explícito no repo
(`integracoes/activecampaign/ESTUDO-form-api-vs-greatpages.md`) de não alterar nada em AC/n8n sem
pedido explícito do Victor. A function só faz `POST /contact/sync` + `POST /contactTags` (nunca
cria negócio via API — evita o risco de atropelar round-robin de owner documentado naquele
estudo). Fica pronta pra ligar quando autorizado.

## "Quem está falando sobre a [marca]" (posts reais)

Só dados da marca do lead. Uma busca por rede (a Trends, no ranking "top", devolve uma rede por vez quando a lista é inteira):
Instagram, Facebook, X e sites. A rede é decidida pelo **endereço** do post (X e sites chegam no campo `url`, Instagram e
Facebook em `link`). Fluxo: candidatos que citam a marca (palavra inteira no texto ou no autor) -> conferência por IA de
relevância (descarta "Natura 2000", "in natura"; sem IA, mantém todos) -> escolha final (um de cada rede primeiro, no máximo
2 por rede, até 6; quem fala de fora vem antes do perfil da própria marca).

- **Instagram, Facebook e X:** quadro oficial da rede (`iframe`). No totem o quadro roda em `sandbox` sem `allow-popups`
  (o visitante não sai da página); no celular os links abrem. Sem `loading="lazy"` de propósito: em alguns navegadores o
  quadro preguiçoso não carrega nem na tela. Exige `frame-src` no CSP (`vercel.json`) para instagram.com, facebook.com e
  platform.twitter.com. Post apagado ou privado mostra a mensagem da própria rede.
- **Sites:** quase nenhum deixa ser embutido (`X-Frame-Options`), então vira **prévia do link** (foto, título e resumo das
  meta tags `og:*`, lidas no servidor com limite de 4,5 s; falha cai para o texto da menção). Nunca busca endereço interno.
- Perfis ligados à marca: busca de influenciadores da Trends só em português.

## Pendências conhecidas (não bloqueiam o funcionamento, mas precisam de 1 decisão humana)

- **Domínio**: `buzzcompass.buzzmonitor.com` (custom domain, registrado no projeto Vercel
  `buzzmonitor-lp-buzz-radar` em 2026-09-02) é o domínio pretendido, já refletido no `<head>` de
  `index.html` (`canonical`, `og:url`, `og:image`, `twitter:image`, JSON-LD). **DNS configurado e
  verificado em 2026-10-20**: o domínio resolve, o certificado é válido e `/totem` e `/api/totem`
  respondem 200 nele. O QR code usa o endereço de onde o totem foi aberto (`location.origin`) e o
  e-mail usa o host da requisição, então abrir o totem por `https://buzzcompass.buzzmonitor.com/totem`
  faz o QR e o e-mail saírem com esse domínio. O `https://buzzmonitor-lp-buzz-radar.vercel.app`
  continua servindo a mesma aplicação em paralelo.
- **Domínio anterior mudou nesta sessão**: se um deploy futuro sair com outro domínio ainda
  (custom domain diferente ou hash), atualizar os mesmos campos acima em `index.html`.
- **OG image**: `assets/og-buzz-compass.png` (1200x630, 174 KB), gerada em 2026-10-20 a partir da tela inicial do totem e
  referenciada em `index.html` (`og:image` e `twitter:image`). Para regerar depois de mudar a tela inicial, capture o
  `/totem` em 1920x1008 e reduza para 1200x630.
- **E-mail comercial**: `resultado.html` usa `comercial@buzzmonitor.com.br` no CTA de contato,
  seguindo o padrão `comercial@{dominio}.com.br` usado por Cxpress/Buzzcreators em outras LPs —
  **não confirmado que essa caixa existe pra Buzzmonitor**. Verificar antes de divulgar.
- **Chave "guest" do Buzzmonitor Trends**: hardcoded em `api/radar.js` (comentário no topo do
  arquivo explica a origem — capturada por inspeção de rede da própria ferramenta gratuita
  pública, sem login). Não é API oficial documentada para este uso. Antes de escalar tráfego pago
  sobre isso, validar limite de uso com engenharia.

## Totem (evento): `/totem` e `/totem-resultado`

Segunda experiência do projeto, mais direta, para rodar em um totem touch no evento. A LP original (`index.html` +
`resultado.html`) continua existindo e funcionando do mesmo jeito. Visual preto com laranja (degradê laranja e rosa nos
destaques).

**Fluxo:** tela de atração (toque em qualquer lugar) -> marca + segmento (obrigatório) + até 3 concorrentes (opcionais) -> nome e e-mail ->
análise (menos de 1 minuto) -> resultado -> QR code + "Encerrar sessão". Botão X no topo, à direita, em todas as telas
da sessão. Sem toque por 2 minutos, volta sozinho ao início (aviso aos 110s) e limpa tudo. Teste com `/totem?idle=8000`.

**Resultado:** a tela separa, com etiqueta **Marca** ou **Segmento** acima de cada parte, o que é da marca e o que é do
segmento (a marca e os concorrentes estão dentro dele). Ordem: **Compass Score da marca** (Presença, Reputação, Ritmo de
crescimento e Vantagem competitiva, ver `SCORING.md`) -> **4 cards de insight pronto em texto** (oportunidade, risco,
tendência emergente e concorrentes; cada um com um parágrafo do segmento e um da marca, nenhum manda olhar gráfico) ->
números do segmento (sentimento, gênero, canais, volume dia a dia, nuvem de palavras) -> a marca e os concorrentes na
conversa (participação, % positivo, crescimento em 7 dias, ritmo diário) -> top posts e vozes influentes do segmento. Os
cards vêm da IA; sem IA o backend monta o texto só com o que a Trends devolveu (`narrativaPorDados`, coberto por
`tests/narrativa.test.js`). **Marca com pouca conversa não mostra "dados insuficientes"**: o score sempre aparece, com
Reputação e Ritmo completados pelo segmento e marcados como "estimado" (regra em `SCORING.md`).

**Como a pesquisa é montada** (`api/_lib/buscas.js`, método da skill `/anthropic-skills:buscas-buzz-radar`): uma busca
por grupo (marca, concorrentes, categoria), com as grafias reais, `#hashtag`, `@perfil` e exclusão de sentido errado;
idioma pt; concorrente informado tem prioridade e o que faltar a IA sugere (mesmo mercado e porte parecido, trocando
por outro candidato se não houver conversa). A skill em si só roda dentro de uma sessão do Claude, por isso a lógica foi
reescrita no backend. **A sintaxe da API guest é diferente da do MCP:** `OR`, aspas, parênteses, `-termo`, `#`, `@`
funcionam; `AND`, `NOT`, `&&` **não** são operadores (viram palavra literal e zeram o resultado); palavras soltas sem
aspas exigem todas no mesmo post. O sanitizador converte `NOT x` em `-x` e `AND` em espaço.

**Parâmetros da busca (da skill):** idioma pt, últimos 30 dias, fuso -3, todas as redes no volume. O **mercado** é uma
busca só: a categoria do segmento + a marca + os concorrentes, cada parte entre parênteses ligada por `OR`. Os temas de
oportunidade e risco saem de uma **amostra aleatória** (`sort_by: random`, como a skill, bem mais representativa que os
posts mais engajados, que são quase todos positivos); os top posts exibidos e o formato que performa saem dos mais
engajados. Cada marca da comparação tem também a própria série diária e uma amostra aleatória de posts, que alimentam o
card de concorrentes. Marca com menos de 50 menções não entra em ranking de sentimento ou crescimento (o percentual de
16 menções engana). Influenciadores: a API só entende uma palavra por vez, então tenta as palavras do segmento até achar
perfis e tira as marcas da comparação da lista.

**Checagem de homônimo (`corrigirHomonimos` em `api/_lib/analise.js`, revisão em `buscas.js`):** nome de marca que também
é outra coisa (Renner x a dupla Rick & Renner; Vivo, Claro, Oi) enche a busca de posts de outro assunto e infla o número.
Para a marca e cada concorrente, em paralelo, a IA lê uma amostra aleatória de até 20 posts da própria busca e conta
quantos não falam da marca; com 30% ou mais fora do assunto, devolve a mesma busca com exclusões (`-termo`) e âncoras, e o
volume é recalculado. Proteções: a correção só vale se ainda achar posts e não apagar mais de 97% do volume (exclusão errada é pior que o
homônimo); exclusão que contradiz a própria busca (`-"vivo"` numa busca que inclui "vivo") é descartada; se a IA acusa
que metade ou mais dos posts é de outro assunto e a correção não resolveu, entra o **modo âncora** (só `@perfil`,
`#hashtag` e frases compostas, sem o nome solto); se nada disso deixa a busca confiável, a marca recebe
`busca_incerta` e a tela mostra "nome comum: a busca pode misturar outros assuntos". Qualquer falha de rede ou de IA
mantém a busca original. O modo âncora prioriza precisão sobre alcance (Vivo: 164 mil -> 24 mil menções; Melissa:
4.700 -> 800). Sem IA, não roda. O que foi corrigido aparece em `meta.correcoes_de_busca` da
resposta. Casos reais em produção: Renner 70.039 -> 22.441; Vivo 164.103 -> 23.912 (modo âncora). Coberto por `tests/revisao.test.js`. Custa uma
consulta de posts e uma chamada de IA pequena por marca, em paralelo (cerca de 3 a 4 segundos a mais).

**Evidência e texto da IA (por que os cards são específicos):** a amostra aleatória de uma marca grande é quase só
anúncio, cupom e revenda (a Natura teve 1 post negativo em 30), então não há crítica para a IA ler. Por isso a busca de
cada marca também é cruzada com vocabulário de queixa e de elogio (`LEXICO_RECLAMACAO` e `LEXICO_ELOGIO`, `E` entre os
grupos): isso gera uma amostra de críticas e de elogios e dois números por marca (`reclamacao_pct` e `elogio_pct`). O exemplo
só vale se o texto citar a marca como palavra inteira. A IA (modelo mais forte, `OPENAI_MODEL_NARRATIVA`, padrão `gpt-4o`,
com reserva no modelo padrão) preenche primeiro uma lista de `temas` concretos e só depois escreve os 4 cards, e **não
compara números**: ranking, líder, maior crescimento e maior percentual vêm prontos no campo `fatos`. Auditoria em produção
(5 marcas, 44 números citados): nenhum número fora dos dados. `?debug=1` na `/api/totem` devolve o que a IA recebeu
(`debug.payload_ia`) e `meta.modelo_narrativa` diz qual modelo escreveu.

**Arquivos novos:**

- `totem.html` + `assets/totem-app.js`: quiosque (fluxo, inatividade, encerrar).
- `totem-resultado.html` + `assets/totem-resultado.js`: página aberta pelo QR code ou pelo e-mail (celular). Inclui o
  selo "Planos a partir de R$ 1.790" e o formulário de proposta (Jotform), liberados quando o resultado chega.
- `assets/totem-render.js` (resultado, compartilhado) · `assets/totem.css` · `assets/qr.js` (gerador de QR sem
  dependência, escrito aqui; CSP continua só com `'self'`).
- `api/totem.js` (GET, análise; parâmetros `m` marca, `s` segmento, `i` @ do Instagram, `c` concorrentes, nessa ordem, porque a URL é a chave do cache) · `api/totem-lead.js` (POST, lead + e-mail; aceita `instagram`) · `api/_lib/` (Trends, IA, buscas, análise, `perfil.js` com a limpeza do @).
- `dev-server.js` (servidor local) · `tests/` (`node tests/qr.test.js`, `buscas.test.js`, `narrativa.test.js`, `revisao.test.js`, `score.test.js`, `totem-lead.test.js`, `leads-destinos.test.js`, `ac-contato-existente.test.js`, `apps-script.test.js`, `totem-api.test.js`, `provas.test.js`, `relevancia.test.js`, `formato.test.js`).

**Por que a análise é GET:** a resposta não tem dado pessoal, então a borda da Vercel guarda por 24h. O totem consulta
primeiro; o QR code e o e-mail apontam para a mesma URL de análise, e o celular recebe o resultado pronto. Se o cache não
estiver na borda daquela região, a análise roda de novo (até ~30s) com uma tela de carregamento. A URL do QR/e-mail leva
só marca e concorrentes, nunca nome ou e-mail (vai para o Google Analytics).

**Lead:** sai no instante em que o visitante envia, independente da análise (se a Trends falhar, o contato não se perde).
Três destinos, independentes entre si (se um cair, os outros seguem) e todos opcionais:

1. **E-mail para o lead (Resend)**, com o **QR code** do resultado, o botão "Ver meu Compass" e o convite para encaminhar ao
   time. O QR é um PNG gerado por `api/qr.js` (Gmail e Outlook não mostram SVG nem imagem embutida); só gera QR de links
   `/totem-resultado` do próprio projeto. O link e o QR continuam valendo depois do evento (o resultado roda de novo se
   o cache da borda tiver expirado).
2. **Planilha do Google Sheets**, pelo webhook: o Apps Script `integracoes/google/buzz-compass-leads.gs` grava uma linha por
   lead (data e hora, nome, e-mail, marca, segmento, Instagram, concorrentes, link, origem). Passo a passo no cabeçalho do
   próprio script. O token (`TOTEM_LEADS_WEBHOOK_TOKEN`) impede que qualquer pessoa grave na planilha.
3. **ActiveCampaign:** tag **Buzz Compass** (buscada pelo nome e, se não existir, criada; não precisa copiar ID) e a URL de
   conversão no campo de contato **"URL Conversão [Auto]"** (achado pelo título, não por número). Nunca cria negócio.
   - **O e-mail já existe no AC** (busca exata, sem diferenciar maiúscula): **não cria contato novo**. Só atualiza o campo
     "URL Conversão [Auto]" e aplica a tag. Nome e empresa que já estão no AC **não são reescritos**.
   - **O e-mail é novo:** cria o contato completo (nome e sobrenome separados, marca na empresa), já com o campo e a tag.
   - A URL de conversão é a página do totem onde o lead foi gerado (`https://buzzcompass.buzzmonitor.com/totem`, com as UTMs
     se o QR/cartaz do evento as tiver; `idle`, `fbclid` e `#hash` saem). O servidor só aceita endereços do próprio projeto.
   - Se não existir nenhum campo de contato com "URL Conversão" no nome, o contato e a tag seguem normalmente e a resposta
     traz `crm_avisos: ["campo_url_conversao_nao_encontrado"]` (e o log também). `ACTIVECAMPAIGN_URL_CONVERSAO_FIELD_ID`
     força o ID do campo se for preciso.
   - Quem roda o Compass de novo não duplica nada (a tag repetida é aceita e o campo é atualizado com a conversão mais recente).

Se o AC ou a planilha derem erro passageiro (5xx), há uma segunda tentativa; erro de credencial (4xx) não repete e aparece no
log (`[buzz-radar-totem] ... falhou`). **Sem nenhum destino configurado, o lead só existe no log da função** (`[totem-lead]`
no painel da Vercel, retenção curta). Configurar os três antes do evento.

| Variável (projeto Vercel, Sensitive) | Efeito |
|---|---|
| `RESEND_API_KEY` | Liga o e-mail do resultado (chave `re_...` criada no painel do Resend com permissão só de envio). Sem ela, o lead não recebe e-mail (no totem o QR continua na tela). |
| `TOTEM_EMAIL_FROM` | Remetente, ex. `Buzzmonitor <compass@buzzmonitor.com.br>`. O remetente padrão (`onboarding@resend.dev`, o mesmo usado no health check e no Pocket Event) **só entrega para o dono da conta Resend**: para os leads receberem, o domínio do remetente precisa estar verificado no Resend (registros DNS SPF e DKIM). |
| `TOTEM_LEADS_WEBHOOK_URL` / `TOTEM_LEADS_WEBHOOK_TOKEN` | URL `/exec` do Apps Script da planilha e a senha que ele confere (`integracoes/google/buzz-compass-leads.gs`). Também serve para n8n ou outro destino que receba JSON. |
| `ACTIVECAMPAIGN_API_URL` / `ACTIVECAMPAIGN_API_TOKEN` | Liga o contato + tag no AC (URL da conta, ex. `https://CONTA.api-us1.com`, e a chave da API em Configurações > Desenvolvedor). |
| `TOTEM_AC_TAG_NOME` | Opcional: nome da tag no AC (padrão `Buzz Compass`, achada ou criada sozinha). |
| `ACTIVECAMPAIGN_TOTEM_TAG_ID` | Opcional: força o ID da tag e dispensa a busca pelo nome. |
| `ACTIVECAMPAIGN_URL_CONVERSAO_FIELD_ID` | Opcional: força o ID do campo de contato "URL Conversão [Auto]" (por padrão é achado pelo título). |
| `ACTIVECAMPAIGN_TOTEM_LIST_ID` | Opcional, desligado por padrão: também inscreve o contato nesta lista do AC. Inscrever em lista é decisão de marketing e de consentimento. |
| `TOTEM_BASE_URL` | Opcional: força o domínio do link e do QR do e-mail (padrão: o host da requisição). |
| `OPENAI_MODEL_NARRATIVA` | Opcional: modelo que escreve os 4 cards (padrão `gpt-4o`; se não existir na conta, cai no modelo padrão). Custa mais que o `gpt-4o-mini` por análise. |
| `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` | Mesmas da LP: montam as buscas e escrevem a leitura. Sem elas o totem funciona em modo reserva (busca pelo nome exato, só concorrentes informados, cards genéricos). |

**Rodar local:** `node landing-pages/buzzmonitor/buzz-radar/dev-server.js 8938` (ou a configuração
`buzz-radar-totem` do `.claude/launch.json`). Abrir `http://localhost:8938/totem`. Sem chave de IA, testa o modo reserva.

**Configurar o totem:** Chrome em quiosque, por exemplo
`chrome --kiosk --noerrdialogs --disable-pinch --overscroll-history-navigation=0 https://<dominio>/totem`. Funciona em
tela vertical e horizontal. Teclado: o do sistema; os formulários rolam quando o teclado cobre parte da tela.

**Pendências do totem (decisão ou ação humana):**

- Resend: criar a chave e **verificar o domínio remetente** (sem isso o e-mail só chega para o dono da conta Resend). Depois
  `RESEND_API_KEY` e `TOTEM_EMAIL_FROM` na Vercel.
- Planilha: criar a planilha, publicar o Apps Script e colocar `TOTEM_LEADS_WEBHOOK_URL` e `TOTEM_LEADS_WEBHOOK_TOKEN` na Vercel.
- ActiveCampaign: `ACTIVECAMPAIGN_API_URL` e `ACTIVECAMPAIGN_API_TOKEN` na Vercel (a tag Buzz Compass é criada sozinha).
- Depois de colocar qualquer variável: republicar o projeto (variável nova só vale no próximo deploy) e fazer 1 Compass de
  teste conferindo os três destinos.
- ~~Texto "Fale com a equipe da Buzzmonitor aqui no evento"~~ e ~~aviso de consentimento da tela de dados~~ ("Ao
  continuar, você concorda em receber o resultado por e-mail e contato da Buzzmonitor sobre o Buzz Compass"):
  **confirmados em 2026-10-20** (os textos que estão hoje em `totem.html` e `assets/totem-app.js`). Se alguém mudar a
  redação, mudar nos dois arquivos e avisar quem cuida de LGPD.
- **Sem limite de chamadas, de propósito (decisão de 2026-10-20):** a meta é que o maior número possível de pessoas faça o
  Compass. O que existe é só a proteção do cache: a URL de análise é normalizada (`api/totem.js`), então o mesmo pedido
  não gera análise nova. Cada marca nova gasta IA e consultas à Trends; acompanhar o custo durante o evento.
- A chave guest da Trends e o limite de uso valem para o totem também (ver pendência acima).
- Testar no totem real (1920x1080) antes do evento: teclado na tela (cobre cerca de 40% da altura), toque dentro dos
  quadros de posts do Instagram, Facebook e X, e leitura do QR code com um celular. A análise com IA já roda em produção.

## Logos

`brand/buzzmonitor/assets/logos/*.png` são quadrados (250x250) com o nome da marca minúsculo no centro: ilegíveis em
barra de topo, não importa a altura. As páginas usam os **SVG** (`logo-primary.svg`, `logo-reversed.svg`, proporção
5,2:1). No deploy, copiar os SVG para `{sibling}/assets/logos/` junto com os PNG (o favicon segue PNG).

## Antes de deployar: reescrever paths de asset

`index.html` e `resultado.html` usam a convenção padrão de **source** do repo pra logos/favicon
(`../../brand/buzzmonitor/assets/logos/*.png`, ver `landing-pages/GUIDELINES.md` §12) — aponta
certo pro repo, mas **não resolve sozinho** quando servido puro (é reescrito por `lp-publicar`
normalmente, que aqui não roda). Antes do deploy, replicar manualmente essa transformação:

1. Trocar todo `../../brand/buzzmonitor/assets/logos/X` por `/assets/logos/X` em todos os HTMLs (`index`, `resultado`, `totem`, `totem-resultado`).
2. Copiar os arquivos referenciados (`logo-primary.svg`, `logo-reversed.svg`, `logo-icon.png`)
   de `brand/buzzmonitor/assets/logos/` pra `{sibling}/assets/logos/` no projeto de deploy.

Confirmado localmente (servindo os arquivos puros via HTTP, sem passar pelo `lp-publicar`) que
sem esse passo os logos quebram — comportamento esperado da convenção, não bug do HTML.

## Como testar localmente

A lógica de chamada ao Buzzmonitor Trends não precisa de nenhuma chave (é `guest`) — pode ser
validada isolada com `curl` direto nos endpoints documentados no topo de `api/radar.js`. A etapa
de narrativa exige `ANTHROPIC_API_KEY` real; sem ela, a function ainda responde `ok:true` com
`narrativa: null` (comportamento esperado, não é bug).

Checklist pós-deploy:
1. Preencher o form de verdade → confirmar que `/resultado?d=...` renderiza os 4 cards, o Radar
   Score e os 3 gráficos.
2. Testar honeypot: preencher o campo `_hp` via devtools e submeter → resposta deve ser
   `{ok:true, honeypot:true}` sem gerar diagnóstico nem custo de API.
3. Testar segmento inexistente/ruído (ex.: nome de empresa pequena) → volume baixo não deve
   quebrar a página; scores caem, mas a narrativa deve tratar isso como insight, não como erro.
