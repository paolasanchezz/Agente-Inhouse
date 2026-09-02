# Cxpress — LP telefonia-ia-latam

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
- [ ] Publicado

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
- **Visual do hero:** janela da aplicacao Cxpress em HTML/CSS, sem imagem. Reproduz o chrome do
  produto (rail de navegacao + area cinza + cartoes brancos) seguindo as capturas reais em
  `landing-pages/cxpress/whatsapp-business/assets/telas/`. A cena se monta sozinha num ciclo de
  11s e respeita `prefers-reduced-motion`. Custo: 0 KB de asset.
- **Escala da janela:** uma unica alavanca, o `font-size` de `.uicard`, atado a largura via `cqw`.
  Mexer nesse valor escala a janela inteira sem deformar. Piso 14px (mobile) e teto 19px.
- **Mascote no rail:** os 12 paths do mascote extraidos de `logo-primary.svg`, inline. O
  `logo-icon.png` (48x48, sem alfa) so serve de favicon; no rail aparecia como quadrado escuro.
- **Elementos decorativos laranja:** pills e arcos, as duas formas canonicas do brandbook
  (secao "Elementos Decorativos"). Maximo de 5 por composicao.

## Pendencia aberta

O bloco de telefonia afirma **voicebot** e **distribuicao inteligente de chamadas**. As duas
afirmacoes vem da pagina oficial `cxpress.ai/telefono`, mas **nao constam no BRANDBOOK**: o
modulo 5 (Atendimento por Voz) lista apenas telefonia em nuvem, transcricao automatica e tickets
originados por voz, e a tabela "Features de IA (Nomes Confirmados)" nao menciona voicebot.
**Confirmar com produto antes de publicar.** Se o voicebot nao existir, revisar tambem o chip do
hero e a copy dos blocos 01 e 03. A animacao do hero ja evita o tema de proposito: mostra a
chamada entrando, virando ticket, sendo atribuida e transcrita, tudo confirmado no brandbook.

## Como atualizar

Editar `index.html` aqui e rodar `/lp-publicar cxpress telefonia-ia-latam content.cxpress.io`.
