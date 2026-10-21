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
- [ ] Navegação de secções some abaixo de 1040 px (sem menu alternativo)
- [ ] Rodapé: logo Elife Group e redes sociais do original ainda não replicados

## Nice-to-haves

- [ ] Efeito de elevação no hover dos cartões sem ação (Voicebot, Multicanal)
- [ ] `.diag` repete o CTA do formulário; `.video` tem um terceiro botão
- [ ] Gradientes e painéis escuros fora do §1 do GUIDELINES: assumidos como exceção "sistema voz"
- [ ] H1 abre pela promessa, não pela dor (§3 do fundamentos-copy): copy fixa por pedido, decisão de quem aprova

## Próximos passos

- Aprovar design e publicar: `publish_page_draft` (pedido explícito do Bruno)
