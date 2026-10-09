# LP Cxpress — webinar-whatsapp-equipe

**Gerado em:** 2026-10-06
**Copy-fonte:** `copy.txt`
**Evento:** 27 de outubro de 2026, terça-feira, 11h (horário de Brasília)
**Destino:** `content.cxpress.io/webinar-whatsapp-equipe`
**Região:** brasil · `<html lang="pt-BR">` · GTM `GTM-T4XDWHL3`
**Formulário:** Jotform `261033482583658` (inscrição de webinar, já integrado)

## Origem

Reformulação da copy da `whatsapp-comercial-bloqueado`, que é a LP do webinar que já aconteceu.
A gravação será reaproveitada na sessão de 27/10. Pedido da Marielle em 06/10: trazer público
mais selecionado e qualificado.

## Estrutura

1. Hero (eyebrow, H1, lead, CTA, nota de data, linha de prova) + ficha lateral (Quando · Formato · Para quem)
2. **Inscrição** (formulário Jotform) — logo após o hero
3. O problema — 3 práticas com X vermelho, nota de fecho, CTA
4. O que você vai ver — 4 pontos com check
5. Para quem é / Para quem não serve — duas listas, check e X
6. Fecho + esteira de clientes (42 logos)
7. Footer

## O que foi reformulado em relação à LP antiga

| | `whatsapp-comercial-bloqueado` | esta LP |
|---|---|---|
| Eixo | medo de perder o número (universal) | teto técnico do aplicativo e o improviso para passar dele |
| Público declarado | **"Para empresas de qualquer porte"** | operação que já passou, ou está perto de passar, dos dispositivos que o app conecta |
| Filtro negativo | não tinha | seção "Para quem este webinar não serve" |
| Formulário | **nenhum** (CTA rolava até vídeo do YouTube) | Jotform na 2ª seção |
| Overline | "Webinar ao vivo" | "Webinar online e gratuito" |

A LP antiga, com os anúncios da campanha `[meta][fundo][conversao][banimento]`, consumiu
**R$ 1.008,09**, levou **47 pessoas** à página e gerou **zero Novo Lead**, porque não havia onde
converter.

## Decisões registradas

**É reprise, e a página não diz isso.** Decisão da Marielle em 06/10. O que a página também **não**
diz: "ao vivo", "perguntas ao vivo", "tire suas dúvidas com o palestrante". Afirmar presença ao
vivo numa reprise seria falso, e isso é diferente de omitir. Pelo mesmo motivo não há seção de
palestrantes. **Atenção em qualquer edição futura:** a LP antiga tem "Webinar ao vivo" no overline;
essa linha não pode ser herdada.

**H1.** A Marielle preferiu a força do H1 antigo, que abre com três palavras concretas antes de
qualquer explicação. A versão adotada mantém essa abertura e move o filtro para a segunda frase.
"Começa quando" em vez de "é porque": aparelho compartilhado é uma das três causas, não a única.

**Formulário na 2ª seção.** Medido: a 1,7 tela de scroll no celular, 21% da página. Decisão vem do
dado desta conta, não de preferência: `tempo-de-resposta` convertia 3,2% com form a 7,9 telas,
contra 20,0% da `banimento-whatsapp` com form a 1,9 tela e o mesmo provedor. A primeira montagem
desta LP tinha o form a 6 telas e foi corrigida antes de publicar.

**O filtro continua funcionando acima do formulário**, mesmo com ele no alto: o H1 nomeia a
teto do aplicativo, a ficha do hero diz para quem é e o próprio formulário pergunta
o tamanho do time. A seção "para quem não serve" reforça para quem rola.


## ⛔ Correção factual de 06/10 (PR #744)

A primeira versão desta LP, publicada no PR #743, afirmava que **"o WhatsApp Business foi
desenhado para uma pessoa"** e que **três, seis ou dez atendentes no mesmo número configuram
"uso irregular"** aos olhos da Meta.

**As duas afirmações são falsas.** O WhatsApp Business conecta **até quatro dispositivos**, e
**até dez em alguns planos do Meta Verified**, com atribuição de conversa. A própria Central de
Ajuda posiciona isso como vários funcionários respondendo clientes. O que a Meta sinaliza como
risco de bloqueio temporário ou permanente é o **uso de aplicativos e sites não oficiais**.

Erro de quem escreveu a copy, apontado pela Marielle. A premissa sustentava o hero, a seção do
problema, dois dos quatro módulos e o primeiro item do "para quem". Tudo foi reescrito.

**Título atual, definido pela Marielle:** "WhatsApp Business em escala: como proteger sua
operação de bloqueios."

**De onde veio o erro, e o que não foi corrigido.** A afirmação foi copiada do FAQ da
`banimento-whatsapp`, que lista *"várias pessoas atendendo pelo aplicativo num celular
compartilhado"* como causa de banimento. Esse FAQ segue em produção, e a mesma frase está na
legenda do anúncio `SMB03_Mesmo celular entre atendentes`, que roda hoje. **A Marielle decidiu
em 06/10 corrigir apenas esta LP.** Fica o registro: quem for escrever a partir daquele FAQ vai
reproduzir o erro.

**Para qualquer edição futura desta página:** não voltar a tratar número de atendentes como causa
de banimento. O eixo correto é o teto de dispositivos do aplicativo e o improviso usado para
passar dele.

## Sistema de design

Reaproveitado da `black-friday-atendimento-b` (CSS e componentes idênticos): paleta de 2 cores
(preto `#0E1116` + azul `#2B5CE6`) mais neutros, `ficha` no hero, `dor`/`dor__x` para lista
negativa, `ver__ck` para lista positiva, `insc__grid`, `fecho`, esteira de clientes.

Desvio consciente da GUIDELINES §8: o check das listas positivas é **azul**, não verde, porque
esta LP roda a paleta de 2 cores da família. Trocar por verde introduziria uma terceira cor.

## Camada de movimento v3 (10/10)

Pedido do Bruno: usar o aprendizado das LPs Cxpress da Leadpages (`chatbot-whatsapp`) para dar mais movimento e foco em conversão, **sem alterar a copy** (texto da página idêntico; só entrou o micro-texto da conversa simulada, ilustrativo e `aria-hidden`).

- **Conversa simulada de WhatsApp** na seção "Entenda quando..." (coluna fixa ao lado dos tópicos): mensagens entram uma a uma com "digitando" e chips "Conversa distribuída / Histórico salvo", que ecoam tópicos da própria copy (filas, distribuição, histórico). O loop só roda em vista; sem JS ou com `prefers-reduced-motion` aparece inteira. Sem "ao vivo", exclamação ou travessão. Para tirar a simulação, remova o `<figure class="ver__fig">`.
- **Logo WhatsApp Business** (`#ico-wab`, o mesmo do chatbot-whatsapp): ícones flutuando na ficha do hero, ponto "online" pulsante no eyebrow, marca d'água na inscrição e no fecho.
- **Inscrição**: brilhos de fundo e borda de gradiente girando no painel do form (`@property`, com fallback sem animação).
- **CTA**: brilho no hover, pulso suave no CTA do hero e **barra fixa "Garantir minha vaga" no celular**, que aparece depois do CTA do hero e some quando o form está na tela.
- Tópicos: X e checks "estalam" com escalonamento e trilha ligando os 4 tópicos; o fecho acende palavra a palavra com a rolagem; luz que segue o mouse na ficha e nos palestrantes.
- **Não levado das LPs Leadpages, de propósito:** botão flutuante de WhatsApp (abre outro formulário e competiria com a inscrição). Hero com a mesma altura de antes (846px em 1440): o form não desceu.

## Validações rodadas

| Checagem | Resultado |
|---|---|
| Tags balanceadas | section 6/6 · main 1/1 · body 1/1 · script 4/4 |
| Pacote SEO §15 | title 1 · canonical 1 · robots 1 · og 10 · twitter 4 |
| JSON-LD | parseia; `Event` com `startDate` 2026-10-27T11:00:00-03:00 |
| GTM | `GTM-T4XDWHL3` no head e no noscript |
| Jotform | `261033482583658`, um único embed |
| em-dash / exclamação | 0 / 0 |
| "ao vivo" no texto visível | ausente |
| `<img>` sem `alt` | 0 |
| Assets quebrados | 0 |
| `href="/"` na logo | 0 (aponta para `home.cxpress.io`, target `_blank`) |
| Logo web-safe §19 | `logo-primary.svg` tem `<text>` = 0 |
| Overflow horizontal a 375px | nenhum |
| Posição do formulário | 1,7 tela · 21% da página |

## Estado

- [x] HTML gerado
- [x] Formulário integrado (veio integrado do modelo, não precisa de `/lp-integrar-form`)
- [ ] OG image 1200×630 → `assets/og-webinar-whatsapp-equipe.png` (template e script em `assets/`)
- [ ] Revisão — `/lp-revisar cxpress/webinar-whatsapp-equipe`
- [ ] Publicado — `/lp-publicar cxpress webinar-whatsapp-equipe content.cxpress.io`

⚠️ **A publicação precisa de worktree a partir de `origin/main`.** O tree local está numa branch
de outra tarefa e dezenas de commits atrás; editar o manifest daqui apagaria LPs que estão no ar.

## Assets

- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `./assets/clientes/cliente-01.png` … `cliente-42.png`
- `./assets/og-template.html` e `./assets/render_og.py` (para gerar a OG image)

## Pendências

1. **OG image** ainda não gerada.
2. **Duração** confirmada pela Marielle em 06/10: cerca de 40 minutos.
3. Se houver alguém no chat respondendo durante a sessão, vale acrescentar "com espaço para
   perguntas" na ficha do hero. Ganho de conversão, e aí deixa de ser falso.
