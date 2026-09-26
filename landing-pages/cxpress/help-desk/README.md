# LP Cxpress — help-desk

**Gerado em:** 2026-09-25 · **Pedido:** Bruno Silva
**Copy-fonte:** `copy.txt` (documento "LP - HELP DESK", SEO: *software de help desk*, *sistema de help desk*, *ferramenta de help desk*, *help desk para empresas*)
**Região:** brasil (pt-BR) · **Domínio alvo:** `content.cxpress.io` (guarda-chuva migrado pro CI) · **URL:** `https://content.cxpress.io/help-desk`
**Form provider:** Jotform `261034073026647`, nos dois pontos de captura (seção de contato + modal do botão flutuante)
**Botão flutuante:** WhatsApp pulsante que abre o formulário num modal; no envio, a conversa segue em `wa.me/551150395028`
**Tracking:** `GTM-KN8BPFG` (container de Google Ads das LPs irmãs). Selo `.tracking.lock` com `grandfathered: true`

## Base

Mesma base da LP irmã `sistema-de-atendimento` (tokens, navbar, rodapé, formulário, botão flutuante, esteira de clientes, FAQ, bloco de IA), que por sua vez segue `escolha-a-cxpress`, `whatsapp-business` e `chatbot-whatsapp`. Componentes próprios desta página: hero com notebook e indicadores, quadro de tickets (kanban), mockup de produto com selos de canal e checklist.

## Seções

| # | Seção | Visual / animação |
|---|---|---|
| 1 | Hero | Notebook da plataforma + 3 cards de indicador flutuando (Total de tickets com contagem, Tempo médio de resposta, Tickets em atendimento) + "Mensagem enviada" |
| — | Clientes | Esteira de 14 logos |
| 2 | Contexto / dor | 4 cards (canais, tickets, histórico, gestão) com contador pulsando |
| 3 | Produto | Mockup grande da fila de tickets com selos de WhatsApp, Instagram, e-mail e telefone surgindo em volta + cards de configuração do WhatsApp e de canais ativos + 4 canais |
| 4 | Gestão de tickets | Quadro Novo → Em andamento → Resolvido com um ticket de WhatsApp avançando e trocando de status + 8 recursos + CTA "Veja como funciona" |
| 5 | IA + humano (navy) | Pipeline Cliente → IA → Atendente em sincronia com a conversa (IA tenta resolver o acesso, transborda para o N2 com o histórico) |
| 6 | Produtividade | Sem plataforma centralizada × Com a Cxpress |
| 8 | Empresas | 3 pilares + dashboard real + card "Tickets por hora" |
| 9 | Diferenciais | 6 cards |
| 10 | FAQ | 7 perguntas da copy (+ FAQPage no JSON-LD) |
| 11 | CTA final + form | Bloco navy, Jotform |

A numeração segue a copy-fonte, que não tem seção 7.

## Assets

| Arquivo | Origem |
|---|---|
| `assets/telas/tela-tickets.svg`, `tela-dashboard.svg` | telas da plataforma já usadas em `whatsapp-business` |
| `assets/ui/notebook-canais.webp`, `card-whatsapp-config.webp`, `card-mensagem-enviada.webp` | recortes com transparência enviados pelo Bruno (`D:\Elife\174 - LP ClaudeCode\Imagens`, set/2026) |
| `assets/ui/card-canais-lista.webp`, `card-tickets-hora.webp` | idem, sobre card branco em CSS |
| `assets/ui/celular-sem-resposta.webp`, `celular-feedback.webp` | idem, fundo removido |
| `assets/og-help-desk.png` | `assets/render_og.py` + `assets/og-template.html` |

Os números dos cards do hero (1.284 tickets, 2min 40s, 37 em atendimento) são ilustrativos de interface, marcados `aria-hidden`, no mesmo papel dos valores que aparecem nos prints da plataforma.

## Copy

Textos da copy-fonte sem reescrita. Dois pontos:

1. **A meta description da copy veio cortada** ("Software de Help Desk para centralizar atendimentos, organizar t"). Completei com: "Software de Help Desk para centralizar atendimentos, organizar tickets, distribuir demandas entre equipes e responder clientes com IA em uma única plataforma." Revisar se houver versão oficial.
2. **As respostas do FAQ não vinham na copy** e foram redigidas com base no `BRANDBOOK.md`, passando pelas regras anti-IA.

"Help&nbsp;Desk" vai com espaço inseparável no H1 para o nome não quebrar entre linhas.

## Verificado (2026-09-25)

- 1440px e 390px: sem scroll horizontal; H1 a 34px no mobile
- `check_mobile_type.py`: só o skip-link fora da tela; o menor texto (9,5px) é a pílula de status do quadro, com `nowrap` (exceção da §20)
- `check_gtm_region.py`: aviso (selo grandfathered), sem bloqueio

## 2026-09-26 — formulário trocado pelo HTML aprovado

A pedido do Bruno, o formulário (Jotform `261034073026647`) passou a ser o HTML que ele enviou: Seu nome, E-mail corporativo, Sua empresa, Qual seu cargo? (dropdown), Seu WhatsApp, checkbox de newsletter e botão Enviar, com labels ocultos e campos arredondados. Antes a LP carregava o `jsform` público, que estava numa versão diferente (sem o campo de cargo).

- O source fica em `assets/form-cxpress.js` e é montado num iframe `srcdoc` isolado (mesmo mecanismo do `form-cxpress-v3.js` das LPs irmãs na Leadpages), com a altura informada por `postMessage`. Serve a seção de contato e o modal do botão flutuante (`cxFillFrame`).
- Removida do HTML enviado só a linha `JotForm.ownerView=true`, que veio da sessão logada no Jotform.
- Plano B: só troca para `form.jotform.com/261034073026647` se o formulário não carregou dentro do iframe em 12 s. Antes (v3) trocava após 6 s sem mensagem de altura, o que numa aba em segundo plano levava o visitante para a versão antiga do form.
- Na Leadpages, o mesmo arquivo está na biblioteca da org como `form-cxpress-v5.js` (`/api/library/pc6qqsnx4bcxrggnxvta0aqz`).

## 2026-09-26 — CTAs em laranja degradê

Pedido do Bruno: tirar o verde dos CTAs. Entre o azul da escolha-a-cxpress e o laranja da marca, ele escolheu o laranja. Todos os `.btn--primary` e o CTA da navbar agora usam o degradê `#F1A908 → #EF863C → #E8702A` com texto navy (5,2:1 sobre `#EF863C`; branco reprovaria com 2,6:1). Nos botões do corpo da página há um pulinho com quique a cada 3,6 s e um brilho atravessando o botão; a animação para no hover/foco e some com `prefers-reduced-motion`. A navbar, que fica fixa no topo, recebe só o degradê, sem o pulinho. O botão flutuante do WhatsApp continua verde, porque ali a cor é da marca WhatsApp.
