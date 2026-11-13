# LP — Webinar Gestão de canais de atendimento com IA em 2027

**URL:** https://content.cxpress.io/webinar-canais-ia-2027
**Quando:** 9 de dezembro de 2026, quarta-feira, 11h às 12h. Online e gratuito.
**Formulário:** Jotform 261033482583658 (webinar BR) · **GTM:** GTM-T4XDWHL3
**Conversão:** Conversão Webinar (1099190376613999)

## Origem

Adaptada da LP do evento presencial `gestao-canais-ia-2027` (12/11/2026), mantendo tema,
conteúdo e palestrantes. A campanha do evento fez CpL de R$ 23 a R$ 31 e 23,7% de conversão
na página, o melhor desempenho da conta junto com o SMB.

## O que mudou em relação à LP do evento

- Promessa passa de presença para conteúdo: o hero ganha uma linha de prova com o número da Cacau Show
- Palestrantes sobem para logo depois do hero, com foto, em vez de aparecerem no fim
- Case Cacau Show sobe para antes da programação
- Seção "Como chegar" removida
- Programação reescrita para 60 minutos (11h às 12h), 5 blocos
- Bloco de novidades vira retrospectiva de 2026 e perspectiva de 2027
- Formulário trocado do Jotform de evento (260995815122663) para o de webinar (261033482583658)
- Contagem regressiva reapontada para 09/12 às 11h

## Decisões técnicas

**Formulário direto, sem carregamento sob demanda.** A LP do evento carregava o Jotform por
IntersectionObserver. Esse padrão derrubou a conversão das LPs de help desk em outubro
(1,1% contra 8,0% depois da troca pelo embed direto), então aqui ele entra direto no HTML.
O observador que sobrou serve só para fixar o idioma como pt-BR, porque o formulário abre com
a bandeira de Portugal por padrão. Ele trata o iframe que já nasceu, já que o jsform escreve o
iframe durante o parsing e normalmente nenhuma mutação chega a ser observada.

**Rede de segurança do reveal.** O bloco noscript cobre JS desligado e há um ramo para navegador
sem IntersectionObserver, mas faltava o caso em que o observador existe e nunca dispara, comum
em webview de aplicativo. Sem isso a página fica em branco com JS ligado, que é a pior falha
possível em tráfego pago. Um setTimeout de 2,5s revela tudo como garantia.

**Contagem regressiva blindada.** O código saía com erro quando os elementos não existiam, e
como ele divide o bloco de script com o reveal, o erro derrubava a revelação da página inteira.
Foi exatamente o que aconteceu ao remover a seção "Como chegar", que era onde o markup da
contagem vivia. Agora a função sai silenciosamente se não encontrar os elementos, e o markup
foi reposto na seção de inscrição.

## Pendências

- Deck de tendências apresentado no evento de 12/11, para incrementar o conteúdo
- Imagem de capa (OG) ainda é a do evento, renomeada. Precisa de arte nova com a data de dezembro
- Criativos dos anúncios: copy em `conhecimento/copywriting/criacao/cxpress/2026-11-12/`
