# LP Cxpress — chatbot-whatsapp

**Importada em:** 2026-09-04
**Origem:** projeto Vercel solo [`cxpress-chatbot-whatsapp.vercel.app`](https://cxpress-chatbot-whatsapp.vercel.app/) — a LP já estava no ar fora do guarda-chuva. Pedido do Bruno: colocá-la num domínio da Cxpress.
**Região:** brasil (pt-BR) · **Domínio alvo:** `content.cxpress.io` (guarda-chuva migrado pro CI)
**URL de produção:** `https://content.cxpress.io/chatbot-whatsapp`
**Form provider:** Jotform `261034073026647` — o mesmo das LPs irmãs `whatsapp-business` e `banimento-de-whatsapp`. Dois pontos de captura: a seção "Solicite uma apresentação gratuita" (jsform) e o modal do botão flutuante (iframe com `data-src`, carregado só ao abrir)
**Tracking:** GTM-T4XDWHL3 (padrão Cxpress BR, `brand/cxpress/tracking.json`) — **adicionado na importação**; a versão solo não tinha container nenhum

## O que mudou da versão solo para esta

Nenhuma palavra de copy foi reescrita — a copy publicada está transcrita em `copy.txt`. As mudanças são de infraestrutura, para a página se comportar como as vizinhas do guarda-chuva:

| # | Mudança | Por quê |
|---|---|---|
| 1 | GTM-T4XDWHL3 no `<head>` + `noscript` no topo do `<body>` | A versão solo não tinha tracking: a página não gerava dado nenhum. Container de BR, como manda `brand/cxpress/tracking.json` |
| 2 | Logos via `../../brand/cxpress/assets/logos/` | Antes eram URLs absolutas para `https://content.cxpress.io/assets/cxpress/logos/...` — funcionavam, mas por acidente. O `build_umbrella.py` reescreve a referência de brand para `/assets/cxpress/` no deploy |
| 3 | 7 imagens baixadas do espelho WordPress para `./assets/` | Vinham de `home.cxpress.io/wp-content/plugins/cxpress-campaign-pages/mirrors/assets/{hash}.webp`. Dependência externa com nome de hash: se o plugin do WP mudar, a LP perde as imagens. Agora são locais e com nome legível |
| 4 | `<link rel="canonical">`, `robots`, `author`, favicon, Open Graph e Twitter Card | A versão solo não tinha nenhum deles. O canonical aponta para `content.cxpress.io/chatbot-whatsapp`, que passa a ser a URL oficial |
| 5 | `assets/og-chatbot-whatsapp.png` (1200×630) | Gerado por `assets/render_og.py` a partir de `assets/og-template.html`, no mesmo padrão da LP irmã `whatsapp-business` (GUIDELINES §18) |

## Assets

| Arquivo | Onde aparece |
|---|---|
| `painel-atendimento.webp` | hero |
| `atendimento-integrado.png` | plataforma, bloco 1 |
| `atendimento-ia.webp` | plataforma, bloco 2 |
| `cadastros-clientes.webp` | plataforma, bloco 3 |
| `gestao-tickets.webp` | plataforma, bloco 4 |
| `dashboards.webp` | plataforma, bloco 5 |
| `especialista-atendimento.webp` | faixa "Fale com um especialista no WhatsApp" |
| `og-chatbot-whatsapp.png` | Open Graph / Twitter Card |
| `og-template.html` + `render_og.py` | fonte da imagem de OG (não vão pro deploy) |

## Pendências

- **Projeto solo `cxpress-chatbot-whatsapp` continua no ar.** Com a LP publicada no guarda-chuva, o ideal é apontar o solo para a URL nova (ou pausar o projeto) para não competir no índice. Precisa de decisão do Bruno/Victor — não foi mexido.
- **Sem JSON-LD.** As LPs irmãs (`whatsapp-business`) têm `Organization` + `FAQPage`. Esta tem FAQ na página mas não tem o schema. Nice-to-have para SEO, não bloqueia.
- **Faixa de resultados sem fonte visível.** Os números da faixa do topo (14%, 9%, 25%, 45%) trazem `*` e `**` mas a página só tem a nota de rodapé dos big numbers. Herdado da versão solo — vale conferir a origem antes da próxima revisão.
