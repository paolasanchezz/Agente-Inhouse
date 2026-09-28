# LP Cxpress — sistema-de-chamados

**Gerado em:** 2026-09-25 · **Pedido:** Bruno Silva
**Copy-fonte:** `copy.txt` (documento "LP - GESTÃO DE CHAMADOS E TICKETS", SEO: *sistema de chamados*, *sistema de tickets*, *gestão de chamados*, *software de chamados*)
**Região:** brasil (pt-BR) · **Domínio alvo:** `content.cxpress.io` (guarda-chuva migrado pro CI) · **URL:** `https://content.cxpress.io/sistema-de-chamados`
**Form provider:** Jotform `261034073026647`, nos dois pontos de captura (seção de contato + modal do botão flutuante)
**Botão flutuante:** WhatsApp pulsante que abre o formulário num modal; no envio, a conversa segue em `wa.me/551150395028`
**Tracking:** `GTM-KN8BPFG` (container de Google Ads das LPs irmãs). Selo `.tracking.lock` com `grandfathered: true`

## Base

Mesma base das LPs irmãs `sistema-de-atendimento` e `help-desk`, que seguem `escolha-a-cxpress`, `whatsapp-business` e `chatbot-whatsapp`.

## Seções

| # | Seção | Visual / animação |
|---|---|---|
| 1 | Hero | Lista de chamados + painel de canais + card do "Chamado #3107" percorrendo Aberto → Em andamento → Resolvido, com a barra de progresso andando e o selo "Resolvido dentro do SLA" |
| — | Clientes | Esteira de 14 logos |
| 2 | Centralização | Contadores de chamados recriados em HTML, contando ao entrar na tela (todos, meus, não atendidos, não lidos) + card "Canais ativos" + 4 destaques |
| 3 | Tickets e distribuição | Quadro de distribuição: chamados de WhatsApp, Instagram e e-mail indo para Suporte, Comercial e Financeiro + 4 destaques |
| 4 | Gestão | 4 KPIs (volume, SLA, TMA e TME, produtividade) + dashboard real da Cxpress + card "Tickets por hora" |
| 5 | IA (navy) | Pipeline Cliente → IA → Técnico em sincronia com a conversa (IA abre o chamado e informa a previsão, transfere para o suporte técnico) |
| 6 | Diferenciais | 5 cards (3 + 2 centralizados) |
| 7 | FAQ | 4 perguntas da copy (+ FAQPage no JSON-LD) |
| 8 | CTA final + form | Bloco navy, Jotform |

## Assets

| Arquivo | Origem |
|---|---|
| `assets/telas/tela-tickets.svg`, `tela-dashboard.svg` | telas da plataforma já usadas em `whatsapp-business` |
| `assets/ui/painel-canais.webp`, `card-canais-ativos.webp` | recortes com transparência enviados pelo Bruno (`D:\Elife\174 - LP ClaudeCode\Imagens`, set/2026) |
| `assets/ui/card-tickets-hora.webp` | idem, sobre card branco em CSS |
| `assets/pessoas/pessoa-1..3.webp` | avatares do hero, Unsplash (licença livre, uso comercial): `SJvDxw0azqw`, `AR9mvykzSOA`, `MQ2xYBHImKM` — crop 256×256 no rosto |
| `assets/og-sistema-de-chamados.png` | `assets/render_og.py` + `assets/og-template.html` |

Os cards de contador enviados como imagem ("8 Todos os tickets", "1 Tickets não atendidos"...) foram recriados em HTML no mesmo desenho, para os números poderem contar. Os valores são ilustrativos de interface, no papel dos prints da plataforma.

## Copy

Textos da copy-fonte sem reescrita; a nota "Aqui eu colocaria um dashboard real" virou o print do dashboard na seção 4. As respostas do FAQ não vinham na copy e foram redigidas com base no `BRANDBOOK.md`, passando pelas regras anti-IA.

## Verificado (2026-09-25)

- 1440px e 390px: sem scroll horizontal; H1 a 34px no mobile
- `check_mobile_type.py`: só o skip-link fora da tela
- `check_gtm_region.py`: aviso (selo grandfathered), sem bloqueio

## 2026-09-26 — formulário trocado pelo HTML aprovado

A pedido do Bruno, o formulário (Jotform `261034073026647`) passou a ser o HTML que ele enviou: Seu nome, E-mail corporativo, Sua empresa, Qual seu cargo? (dropdown), Seu WhatsApp, checkbox de newsletter e botão Enviar, com labels ocultos e campos arredondados. Antes a LP carregava o `jsform` público, que estava numa versão diferente (sem o campo de cargo).

- O source fica em `assets/form-cxpress.js` e é montado num iframe `srcdoc` isolado (mesmo mecanismo do `form-cxpress-v3.js` das LPs irmãs na Leadpages), com a altura informada por `postMessage`. Serve a seção de contato e o modal do botão flutuante (`cxFillFrame`).
- Removida do HTML enviado só a linha `JotForm.ownerView=true`, que veio da sessão logada no Jotform.
- Plano B: só troca para `form.jotform.com/261034073026647` se o formulário não carregou dentro do iframe em 12 s. Antes (v3) trocava após 6 s sem mensagem de altura, o que numa aba em segundo plano levava o visitante para a versão antiga do form.
- Na Leadpages, o mesmo arquivo está na biblioteca da org como `form-cxpress-v5.js` (`/api/library/pc6qqsnx4bcxrggnxvta0aqz`).

## 2026-09-26 — hero no modelo da Albato

Pedido do Bruno, com a página da Albato (`albato.com/br/automate`) como referência de H1: hero centralizado com pílula segmentada acima do título ("Tickets, filas e SLA" | "Sistema de chamados"), H1 em duas linhas com quebra manual (`<br class="hc__br">`, some no mobile), selos circulares de WhatsApp, Instagram, e-mail e telefone flutuando nas laterais (somem abaixo de 1180 px), fundo em grade e a cena do chamado #3107 grande logo abaixo. Classes `.hero--c` / `.hc*`.

## 2026-09-26 — CTAs em laranja degradê

Pedido do Bruno: tirar o verde dos CTAs. Entre o azul da escolha-a-cxpress e o laranja da marca, ele escolheu o laranja. Todos os `.btn--primary` e o CTA da navbar agora usam o degradê `#F1A908 → #EF863C → #E8702A` com texto navy (5,2:1 sobre `#EF863C`; branco reprovaria com 2,6:1). Nos botões do corpo da página há um pulinho com quique a cada 3,6 s e um brilho atravessando o botão; a animação para no hover/foco e some com `prefers-reduced-motion`. A navbar, que fica fixa no topo, recebe só o degradê, sem o pulinho. O botão flutuante do WhatsApp continua verde, porque ali a cor é da marca WhatsApp.
