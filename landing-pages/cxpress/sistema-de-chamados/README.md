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
| `assets/og-sistema-de-chamados.png` | `assets/render_og.py` + `assets/og-template.html` |

Os cards de contador enviados como imagem ("8 Todos os tickets", "1 Tickets não atendidos"...) foram recriados em HTML no mesmo desenho, para os números poderem contar. Os valores são ilustrativos de interface, no papel dos prints da plataforma.

## Copy

Textos da copy-fonte sem reescrita; a nota "Aqui eu colocaria um dashboard real" virou o print do dashboard na seção 4. As respostas do FAQ não vinham na copy e foram redigidas com base no `BRANDBOOK.md`, passando pelas regras anti-IA.

## Verificado (2026-09-25)

- 1440px e 390px: sem scroll horizontal; H1 a 34px no mobile
- `check_mobile_type.py`: só o skip-link fora da tela
- `check_gtm_region.py`: aviso (selo grandfathered), sem bloqueio
