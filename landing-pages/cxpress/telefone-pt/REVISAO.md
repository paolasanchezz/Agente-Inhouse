# Revisão LP — cxpress/telefone-pt

**Data:** 2026-10-21
**Auditores:** design-reviewer + a11y-auditor (ui-craft, só leitura) e verificações determinísticas (GTM, SEO, em-dash, logo). A LP vive no Leadpages (rascunho `wi0lec3sox66tqhms9t8fp1z`), por isso as passadas `frontend-design` e `web-design-guidelines` foram substituídas pelos agentes de revisão do ui-craft.

## Aplicado automaticamente (22 críticos)

- [x] GTM: `GTM-NW6V5KBM` bate com Portugal (status ok), selo `.tracking.lock` gravado
- [x] OG image ausente: criada `assets/og-telefone-pt.png` (1200x630), ligada via `update_page_seo` e nas tags da fonte
- [x] Tags og/twitter incompletas e JSON-LD sem Organization: completadas (Organization + FAQPage)
- [x] `.reveal` invisível sem JS: agora só esconde com `html.js` (script inline no head) + `<noscript>`
- [x] Animações sem pausa (WCAG 2.2.2): botão "Pausar animação" (palco, órbita, canvas, ciclos); pausa também ao focar os capítulos
- [x] Auto-avanço mudava `aria-pressed` sozinho: o encaminhamento só seleciona uma vez; os dispositivos param ao hover/foco/pausa
- [x] `.chap` sem nome e com 3 px em mobile: texto passa a visualmente oculto, alvo com padding
- [x] "Tabs" sem tabpanel: viraram botões `aria-pressed` num `role=group`
- [x] Cenas inativas do palco lidas pelo leitor de ecrã: `aria-hidden` dinâmico; rótulo do grupo curto
- [x] Contraste de `.note`, `.qhint`, `.chap` (55%/50% -> 78%) e tamanhos mínimos subidos
- [x] Diagrama de filas ilegível em 390 px: nomes maiores, sublegendas escondidas em mobile
- [x] KPIs a transbordar em 390 px: tamanhos fluidos
- [x] Foco laranja com contraste baixo em fundo claro: anel navy em claro, laranja em escuro
- [x] Palco mobile com altura insuficiente: 372 px
- [x] Form sem reserva de espaço: `min-height` no cartão
- [x] Selo "ao vivo" enganoso: agora "demonstração"; botão de gravação com rótulo honesto ("Simular a reprodução")
- [x] Contadores mostravam 0 sem JS: valor final no HTML
- [x] `text-wrap: balance/pretty`, `aria-current` na navegação, `main tabindex=-1`, fallback de cor no `h1 em` e `forced-colors`
- [x] Código morto removido (chatbot, condições, fecho, WhatsApp)

## Melhorias opcionais

- [ ] `canonical`, `og:url` e hreflang: aguardam o domínio final (Leadpages ou content.cxpress.io)
- [ ] Faixa de logos com 380 px de largura: pedir arquivo maior ou logos individuais
- [ ] Alvos de toque de `.qbtn`/`.devtabs` ficaram perto de 44 px, não garantidos
- [ ] FAQ e Quem somos agora alternam fundo; rever ritmo vertical (paddings 104/68 abaixo do 120/80 do §2)
- [ ] `target="_blank"` sem aviso "(abre num novo separador)"
- [ ] Prefixo "[PT]" no `<title>` e `noindex`: remover na publicação
- [ ] Rodapé: logo Elife Group e redes sociais do original ainda não replicados

## Nice-to-haves

- [ ] Efeito de elevação no hover dos cartões sem ação (Voicebot, Multicanal)
- [ ] `.diag` repete o CTA do formulário; `.video` tem um terceiro botão
- [ ] Gradientes e painéis escuros fora do §1 do GUIDELINES: assumidos como exceção "sistema voz"
- [ ] H1 abre pela promessa, não pela dor (§3 do fundamentos-copy): copy fixa por pedido, decisão de quem aprova

## Rodada 2 (2026-10-21, depois das correções do Bruno)

Auditores: design-reviewer + a11y-auditor (ui-craft). GTM ok (selo atual), og 9, twitter 4, JSON-LD válido, OG 1200x630, zero em-dash.

### Aplicado automaticamente (12)

- [x] Chips do voicebot com contraste 4,3:1: fundo navy translúcido, 13 px/600
- [x] Etiquetas flutuantes do vídeo cobriam os controlos do YouTube: `pointer-events:none` e reposicionadas fora da zona de controlos
- [x] Texto do diagrama de filas ilegível entre 681 e 960 px: nomes maiores e sublegendas escondidas até 960 px
- [x] Alturas fixas dos cartões podiam cortar conteúdo: passaram a `min-height` (460/352 px); removido o `min-height` inline do cartão digital
- [x] Anéis de ping/ripple congelavam a meio em pausa: forçados a invisíveis; `[hidden]` do botão de pausa respeitado
- [x] Botão de pausa renomeado "Pausar animações" (pausa a página inteira) e retoma sem salto de tempo
- [x] Timeout do nó "hot" do diagrama agora é cancelado ao trocar de fila
- [x] Big numbers: 1 coluna abaixo de 440 px, altura reservada do visual em mobile, "N1" lido como "Nível 1", forced-colors
- [x] YouTube em `youtube-nocookie.com` (RGPD)
- [x] Hover de elevação removido dos cartões de números; código morto da navbar removido; `scroll-padding-top` 68 px; alvo do logo e da pausa a 44 px
- [x] Patch do srcdoc do Jotform tolera valores não-string

### Fica para decidir

- [ ] O patch do `__CX_FORM_SRCDOC` vive no `<head>`; confirmar na página publicada que o telefone continua a renderizar (o Leadpages pode regenerar o head)
- [ ] Rótulo do dial "24h" vs número "24/7" e "N1" repetido no cartão d
- [ ] Etiquetas do vídeo ("Chamada atendida") parecem estado real: marcar como exemplo se preferir
- [ ] Botão de pausa só no hero: considerar controlo junto do vídeo
- [ ] Logo da navbar liga a cxpress.pt (saída do funil): decisão de produto
- [ ] Foco: os CTAs levam a `#agendar` mas o foco não passa para o formulário

## Pacote A + B (2026-10-21): desempenho, RGPD, hero e mobile

Medido em Chromium sem limitação (indicativo): CLS 0,096 -> 0; zero pedidos ao Google Fonts e ao YouTube antes do clique; formulário só carrega perto do ecrã, 2,5 s depois do load ou ao clicar num CTA.

- [x] Fontes alojadas na própria página (Open Sans, Source Sans 3, JetBrains Mono, só subconjunto latino, ~99 KB contra ~318 KB) com `preload`; sem Google Fonts (RGPD: o IP do visitante deixa de ir para a Google) e sem salto de texto no hero
- [x] Vídeo com facade: capa própria (`assets/video-capa.webp`) e botão de play; o YouTube (`youtube-nocookie`) só carrega ao clicar, e o clique envia o evento `video_play` ao `dataLayer`. Sem JS fica um link para o YouTube
- [x] Formulário em carga tardia (`data-cx-jotform="lazy"` + montagem por IntersectionObserver, repouso ou clique nos CTAs)
- [x] Nota de privacidade sob o formulário, com link para a Política de Privacidade (texto a validar por quem cuida do jurídico)
- [x] Hero em mobile: palco já espreita no primeiro ecrã; "Ver como funciona" virou ligação discreta e aponta para o vídeo; frase "Unifica, simplifica…" escondida em mobile e com `balance` em desktop; botão de pausa mais leve (área de toque mantida)

## Próximos passos

- Aprovar design e publicar: `publish_page_draft` (pedido explícito do Bruno)
