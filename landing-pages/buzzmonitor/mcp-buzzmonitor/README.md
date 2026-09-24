# LP Buzzmonitor — mcp-buzzmonitor

**Gerado em:** 2026-09-17
**Copy-fonte:** `copy.txt` (copy final entregue pelo Victor via PDF anexado, estruturada via `/lp-preparar`)

## O que é

LP de campanha nova sobre o MCP da Buzzmonitor (integração com Claude/ChatGPT), com ângulo duplo: divulgar a integração em si **e** mostrar que a Buzzmonitor já disponibiliza Skills prontas. Distinta da LP já publicada em `landing-pages/buzzmonitor/mcp/` (`material.buzzmonitor.com/mcp`, foco em "4 módulos") e das variantes de webinar (`mcp-na-pratica-p`, `mcp-para-social-listening`) — são páginas irmãs que continuam no ar.

Direção visual pedida pelo Victor: "layout super moderno e dinâmico, com gifs e animações". Resolvido com CSS/JS leve (sem arquivos de imagem pesados):
- Mockup de chat no hero com efeito de digitação em loop (pergunta some pra bubble ficar vazia, "digita" caractere a caractere, mostra indicador de digitando, revela a resposta, repete).
- Scroll-reveal com stagger em todos os grids (fontes de dados, Skills).
- Seção "Do prompt ao insight": 4 pares pergunta/resposta em bolhas de chat reais, cada resposta some e reaparece com indicador de "digitando" ao entrar na viewport.
- Hover rico nos cards de Skills (lift + sombra + accent colorido por card).
- Gradiente único da LP (roxo → laranja, oficial da marca) animado bem lentamente no hero.
- Tudo com fallback: sem JS ou com `prefers-reduced-motion: reduce`, todo texto essencial aparece direto, sem animação.

## Estrutura (9 seções, ordem ditada pela copy — GUIDELINES §9)

1. HERO — dor (abas/planilha) + promessa + CTA "Quero usar o MCP da Buzzmonitor"
2. VIDEO-DEMO — placeholder de player (vídeo do Breno Soutto ainda não subiu no YouTube) + CTA "Agendar uma demonstração gratuita"
3. NA-PRATICA — o que é o MCP + 4 exemplos de prompt + 3 fontes de dados (Trends/Projetos/CRM) + CTA "Fale com um especialista"
4. SKILLS — 6 Skills prontas (Dashboard de Campanha, Report de Crise, Marca x Concorrentes, Tendências de Categoria, Filtro de Região, Exploring)
5. EXEMPLOS-CHAT — 4 pares pergunta/resposta animados + CTA "Quero potencializar o listening com IA"
6. BENEFICIO-TEMPO — seção de "pausa" (fundo escuro, único 2º momento dramático da LP) + CTA "Quero conhecer o MCP da Buzzmonitor" + mensagem dupla cliente/não-cliente
7. FORM — Jotform embutido ao lado do H2 (form `form/jsform/252995108251662`, o mesmo já usado na LP irmã `mcp/`)
8. SEGURANCA — faixa curta antes do rodapé (não é seção inteira, conforme pedido explícito do autor da copy)
9. FOOTER

## Estado

- [x] HTML gerado e validado localmente (preview via `py -m http.server` + junction `landing-pages/brand`, removida após o teste)
- [ ] OG image 1200×630 → `assets/og-mcp-buzzmonitor.png` (arquivo **único** — nunca também `og-image.png`)
- [x] Revisão (frontend-design review + web-design-guidelines) — ver `REVISAO.md` (1 crítico de acessibilidade corrigido)
- [x] Formulário integrado — Jotform (2026-09-24)
- [ ] Vídeo do Breno Soutto — assim que subir no YouTube, substituir o placeholder da seção VIDEO-DEMO por embed real
- [ ] Publicado em `content.buzzmonitor.com/mcp-buzzmonitor` (guarda-chuva, mesmo dominio da LP irma ES `mcp-claude-latam`) — fluxo CI via manifesto `landing-pages/dominios/content-buzzmonitor-com/manifest.json`

**Form provider:** Jotform (`form/jsform/252995108251662`, 2026-09-24)

## Pendências de conteúdo (não bloqueiam o design, mas precisam de decisão do Victor)

- Confirmar se "transformar essas informações em insights, em segundos" está correto — o PDF original tinha "em insights, sem segundos" (tratado como typo, ver nota em `copy.txt`).
- Domínio decidido: `content.buzzmonitor.com` (pedido do Victor, 2026-09-24) — HTML usa placeholders `{{DOMAIN}}` e `{{OG_IMAGE_PATH}}` que o build do CI resolve a partir do manifesto.

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header, fundo claro)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer, fundo escuro)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- Google Fonts: League Spartan (700/800/900) + Lato (400/600/700, 400 itálico)
- GTM: `GTM-WFJVK858` (Buzzmonitor Brasil)
