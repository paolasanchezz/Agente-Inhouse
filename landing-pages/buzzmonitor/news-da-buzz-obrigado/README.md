# LP Buzzmonitor — news-da-buzz-obrigado

Thanks page da LP `news-da-buzz`: confirma a inscrição na newsletter logo após o envio do form. Página de confirmação pura, sem CTA de venda (só um convite leve pra seguir no LinkedIn enquanto a primeira edição não chega).

**Gerado em:** 2026-08-27
**Página mãe:** `landing-pages/buzzmonitor/news-da-buzz/` (publicar sempre em batch)
**Motivo:** o form da LP-mãe usa Mailchimp via endpoint cru (submit por iframe oculto, sem navegação) — sem uma URL própria de sucesso, o Meta Ads não tinha como trackear a conversão. Esta página existe pra dar esse destino.

## Estrutura

- HERO (eyebrow "Inscrição confirmada" + H1 + card de reforço "confira sua caixa de entrada" + CTA leve pra LinkedIn)
- FOOTER

## Integração com a LP-mãe

- `landing-pages/buzzmonitor/news-da-buzz/index.html`: o handler de submit do form (`mc-embedded-subscribe-form`) dispara o POST pro Mailchimp via iframe oculto (como antes) e, 700ms depois (tempo só pra mostrar o estado "Inscrito" no botão), redireciona via `window.location.href = '/news-da-buzz-obrigado'`.
- Como o envio ao Mailchimp é fire-and-forget (cross-origin, sem confirmação real), o redirect acontece sempre que o form é submetido client-side — igual ao comportamento anterior da mensagem de sucesso inline, que também não esperava confirmação do Mailchimp.

## Configuração pendente (fora do repo)

- **Trigger no GTM:** configurar no container `GTM-WFJVK858` um trigger de Page View (ou evento customizado) na URL `/news-da-buzz-obrigado`, disparando o Pixel/CAPI da Meta como evento de conversão (Lead). Isso é feito na interface do GTM, não no código.

## Estado

- [x] HTML gerado
- [ ] Revisão
- [ ] Publicado — adicionado ao manifesto `landing-pages/dominios/material-buzzmonitor-com/manifest.json` junto com a LP-mãe

## Exceções deliberadas às GUIDELINES (precedente: estudo-diversidade-2026-obrigado, cxpress/video-atendimento-obrigado)

- **`noindex, follow`** (exceção ao §15): página pós-ação; validação de crawlability do lp-publicar vai apontar isso como esperado, não como erro.
- **Sem OG image, sem og/twitter completos, sem JSON-LD**: ninguém compartilha esta URL.
- **Sem estrutura mínima de LP** (§6): não há form nem captação aqui, é só confirmação.

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)

## Notas

- GTM injetado: `GTM-WFJVK858` (região brasil), mesmo container da LP-mãe.
- Paleta usa `--teal` (`#0E9D9B`) como cor de destaque do eyebrow/ícone, reforçando "sucesso/confirmação" — diferente do roxo/laranja predominantes na LP-mãe, pra essa página se ler visualmente como um estado diferente (pós-ação) sem sair da identidade Buzzmonitor.
