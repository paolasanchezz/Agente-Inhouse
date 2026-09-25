# LP Cxpress — sistema-de-atendimento

**Gerado em:** 2026-09-25 · **Pedido:** Bruno Silva
**Copy-fonte:** `copy.txt` (documento "LP - SISTEMA DE ATENDIMENTO", SEO: *sistema de atendimento ao cliente*, *software de atendimento*, *plataforma de atendimento*)
**Região:** brasil (pt-BR) · **Domínio alvo:** `content.cxpress.io` (guarda-chuva migrado pro CI) · **URL:** `https://content.cxpress.io/sistema-de-atendimento`
**Form provider:** Jotform `261034073026647`, nos dois pontos de captura (seção de contato + modal do botão flutuante), o mesmo das LPs irmãs
**Botão flutuante:** WhatsApp pulsante que abre o formulário num modal; no envio, a conversa segue em `wa.me/551150395028`
**Tracking:** `GTM-KN8BPFG` (container de Google Ads das LPs irmãs). Selo `.tracking.lock` com `grandfathered: true`; ver a nota no selo

## Referências seguidas

Mesmas diretrizes, tokens, navbar, rodapé, formulário, botão flutuante e esteira de clientes das três LPs construídas antes nesta sequência: `escolha-a-cxpress`, `whatsapp-business` e `chatbot-whatsapp`. As cenas animadas são novas e contam o tema da página.

## Seções

| # | Seção | Visual / animação |
|---|---|---|
| 1 | Hero | Tela da fila de tickets + painel de canais (flutua) + tickets novos entrando de WhatsApp, Instagram e e-mail, um por vez + card "Mensagem enviada" |
| — | Clientes | Esteira de 14 logos (padrão das irmãs) |
| 2 | Todos os canais | 4 cards de canal com contador de mensagens pulsando e linhas de conversa se preenchendo + card "Canais ativos 4 de 6" |
| 3 | Software | Tela de atendimento com holofote sequencial (fila → conversa → cliente) + card "Tickets recentes" + 6 recursos |
| 4 | Plataforma (visão única) | Diagrama Cliente → 4 canais → Cxpress → "Um único histórico", com pulsos correndo nos fios e a linha do tempo do cliente se montando |
| 5 | IA + humano (bloco navy) | Pipeline Cliente → IA → Agente acendendo em sincronia com a conversa ao lado (IA responde, transfere para a atendente com o histórico) |
| 6 | Produtividade | Antes × Depois: ferramentas soltas tremendo + celular sem resposta × plataforma única com os 5 blocos acendendo + celular com elogio |
| 7 | Filas e distribuição | Quadro "Distribuição automática": tickets saem da entrada e vão para Comercial, Suporte e Financeiro |
| 8 | Gestão | 5 KPIs (SLA, TMA, TME, Volume, Produtividade) com barras + dashboard real + card "Tickets por hora" |
| 9 | Escala | 3 pilares (Centralize, Automatize, Gerencie) com trilho que se desenha |
| 10 | Diferenciais | 6 cards |
| 11 | FAQ | 8 perguntas da copy (+ FAQPage no JSON-LD) |
| 12 | CTA final + form | Bloco navy com topo arredondado, Jotform |

Todas as cenas pausam fora da tela (`data-fx` → `.fx-idle`) e ficam paradas sob `prefers-reduced-motion`.

## Assets

| Arquivo | Origem |
|---|---|
| `assets/telas/tela-tickets.svg`, `tela-principal.svg`, `tela-dashboard.svg` | telas da plataforma já usadas em `whatsapp-business` |
| `assets/ui/painel-canais.webp`, `card-mensagem-enviada.webp`, `card-canais-ativos.webp` | recortes com transparência enviados pelo Bruno (`D:\Elife\174 - LP ClaudeCode\Imagens`, set/2026), redimensionados e convertidos |
| `assets/ui/card-tickets-recentes.webp`, `card-tickets-hora.webp` | idem, recortados no limite do conteúdo e colocados sobre card branco em CSS |
| `assets/ui/celular-sem-resposta.webp`, `celular-feedback.webp` | idem, fundo removido por preenchimento a partir das bordas |
| `assets/clientes/` | 14 logos da esteira das irmãs |
| `assets/og-sistema-de-atendimento.png` | gerado por `assets/render_og.py` a partir de `assets/og-template.html` (GUIDELINES §18) |

Ignorados por não caberem no tema: prints da Octadesk (referência de concorrente), a foto de campanha de despachante (o print de mobilidade urbana entrou só pelo celular com a conversa) e o card de disparos em massa.

## Copy

Títulos, subtítulos e textos são os da copy-fonte, sem reescrita. As notas de direção ("Eu colocaria aqui...", "Visual sugerido...") viraram as cenas acima e não aparecem na página. As **respostas do FAQ não vinham na copy** e foram redigidas com base no `brand/cxpress/BRANDBOOK.md` (API oficial, IA com ChatGPT no N1, handoff com histórico, múltiplos atendentes no mesmo número), passando pelas regras anti-IA (zero travessão).

## Verificado (2026-09-25)

- 1440px e 390px: sem scroll horizontal; H1 a 34px no mobile (piso §20)
- `bump_mobile_type.py` aplicado; `check_mobile_type.py`: só o skip-link fora da tela (intencional)
- `check_gtm_region.py`: aviso (selo grandfathered), sem bloqueio
