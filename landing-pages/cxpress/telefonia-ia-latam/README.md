# Cxpress · LP telefonia-ia-latam

LP de **Cxpress.voz** (telefonia em nuvem com IA) em ES-LATAM.

| | |
|---|---|
| **Marca / regiao** | Cxpress · LATAM (`es-419`) |
| **Dominio** | `content.cxpress.io/telefonia-ia-latam` |
| **Estagio de funil** | MoFu/BoFu (form na ultima secao, GUIDELINES §10) |
| **GTM** | `GTM-WRQ47B9R` (container LATAM) |
| **Fonte da copy** | https://www.cxpress.ai/telefono, adaptada de espanhol peninsular para ES-LATAM |
| **Fonte das features** | `brand/cxpress/BRANDBOOK.md` §2 (Modulos Principais, Features de IA, Diferenciais-Chave) |
| **Referencia de estilo** | `landing-pages/cxpress/agente-concierge-latam` |

## Estado

- [x] Copy estruturada (`copy.txt`)
- [x] HTML gerado
- [x] Revisao de design e acessibilidade
- [x] Formulario integrado
- [x] Publicado (a checkbox ficou desmarcada por engano; a LP ja servia 200 em
      `content.cxpress.io/telefonia-ia-latam` antes da reforma visual de 2026-09-18)

**Form provider:** Jotform `252398149653872` (integrado em 2026-09-01). E o formulario LATAM
padrao da Cxpress, compartilhado com outras 8 LPs da regiao. O CSP do guarda-chuva
(`landing-pages/dominios/content-cxpress-io/vercel.json`) ja libera `jotform.com` em
`script-src`, `frame-src`, `form-action` e `connect-src`.

## Estrutura

Hero → clientes → telefonia (Cxpress.voz, 6 blocos) → faixa de diagnostico → toda a plataforma
(5 modulos) → diferenciais (4) → quem somos → perguntas frequentes (5) → CTA com form.

## Decisoes de design

- **Sem arco no hero** (pedido do Victor). O arco canonico da marca segue no CTA final, na secao
  da plataforma e no bloco quem somos.
- **Elementos decorativos laranja:** pills e arcos, as duas formas canonicas do brandbook
  (secao "Elementos Decorativos"). Maximo de 5 por composicao.

## Reforma visual (2026-09-18): mesmo sistema da LP agente-concierge-latam

Pedido do Ulises: aplicar aqui o sistema grafico da `agente-concierge-latam` e somar uma
animacao do Samir **atendendo chamadas**, de modo que o produto leia como um assistente que
ajuda a atender e a encaminhar, e nao como uma URA.

O que entrou:

- **Hero em azul marinho** (`--navy`), com o segundo foco de luz (`.hero__glow`) atras do Samir.
  Sem ele o moletom marinho dele encosta no fundo marinho e a silhueta some.
- **Menu no header** com as quatro secoes, scroll-spy e painel com hamburguer abaixo de 1040px.
  Os rotulos sao os proprios kickers de cada secao, nenhum texto novo. O rotulo do CTA do header
  **continua "Quiero saber más"**: o menu e estrutura, o rotulo do botao e copy desta pagina.
- **Cursor fluido** (dardo com borda branca, laranja sobre bloco azul e marinho sobre claro).
- **Glow laranja que segue o cursor** nos cards do bento, com o texto acima do brilho. O circulo
  lilas fixo do canto saiu: duas luzes no mesmo card competiam.
- **Ritmo vertical mais apertado**: secao 62/92px (era 88/136), hero 58/86px de base.
- **Cena do hero refeita.** A janela da aplicacao (`.uicard`) saiu e virou tres cartoes que
  pousam em volta do Samir, num ciclo de 28s = 4 chamadas de 7s: quem liga e de que numero ->
  transcricao que se escreve letra a letra enquanto o cliente fala -> a chamada atribuida a um
  setor e a um agente. O conteudo da janela antiga nao se perdeu, mudou de suporte: sao os
  mesmos campos do ticket. A cada batida muda o setor (Soporte, Ventas, Agenda, Retención), que
  e o que mostra a distribuicao.

### O Samir desta LP

- **Textura:** `brand/cxpress/assets/mascot/samir-trabalhando.png`, o render oficial com headset
  e microfone de haste. Recortado no bbox, redimensionado pra 900x907 e exportado em WebP
  (`assets/samir/samir-voz.webp`, 90 KB). O coracaozinho solto do canto superior foi apagado da
  textura: ele caia exatamente em cima do cartao de transcricao.
- **Engine:** a mesma malha WebGL da `agente-concierge-latam`. A textura nunca e cortada, e uma
  folha de 82x72 vertices que se estica, entao nao existe borda de recorte pra aparecer e a
  palpebra fecha de verdade. Sem WebGL, ou com `prefers-reduced-motion`, fica o still.
- **Deformadores (outros, porque a acao e outra):** piscada assimetrica, inclinacao da cabeca
  quando a chamada entra (2,2 graus, rotacao rigida no pescoco), respiracao, balanco da cauda e
  **o coracao batendo em dois tempos**. O batimento e o ponto da cena: e o sinal de que do outro
  lado da linha tem gente.
- Nao ha giro de cabeca. Pelo mesmo motivo da outra LP: numa arte chapada o giro so existe como
  esticada, e sem arte de perfil nao da pra esconder.

### Coisas que decidi NAO portar

- **A seta do destaque.** Na outra LP ela liga "asistente personalizado" ao Samir. Aqui o
  destaque da H1 e "misma historia", que e a dor, nao o assistente: a seta apontaria a coisa
  errada. O laco fica por conta da etiqueta com o nome dele.
- **Cartoes atras da figura.** Na outra LP eles se escondem atras da laptop, que e larga e baixa.
  Aqui a figura e um quadrado no meio da coluna e engolia o texto dos tres cartoes, entao eles
  ficam na frente (`z-index:3`).

### Defeito corrigido de passagem

`body{cursor:none}` vale dentro de `@media (hover:hover)`, mas o JS do cursor desiste quando
`prefers-reduced-motion` esta ligado, e ai o `.fcur` nunca acende. Resultado: desktop com
reduced-motion ficava **sem ponteiro nenhum**. O bloco de reduced-motion agora devolve
`cursor:auto`. (A `agente-concierge-latam` ja tinha essa linha; ela faltou na copia.)

## Pendencia aberta

O bloco de telefonia afirma **voicebot** e **distribuicao inteligente de chamadas**. As duas
afirmacoes vem da pagina oficial `cxpress.ai/telefono`, mas **nao constam no BRANDBOOK**: o
modulo 5 (Atendimento por Voz) lista apenas telefonia em nuvem, transcricao automatica e tickets
originados por voz, e a tabela "Features de IA (Nomes Confirmados)" nao menciona voicebot.
**Segue em aberto, e a copy ja esta no ar** (a LP responde 200 desde antes da reforma visual).
Se o voicebot nao existir, revisar o chip do hero e a copy dos blocos 01 e 03. A cena do hero
evita o tema de proposito, antes e depois da reforma: mostra a chamada entrando, a transcricao e
a atribuicao a um **agente humano**, tudo confirmado no brandbook. Nenhum cartao diz voicebot.

## Como atualizar

Editar `index.html` aqui e rodar `/lp-publicar cxpress telefonia-ia-latam content.cxpress.io`.
