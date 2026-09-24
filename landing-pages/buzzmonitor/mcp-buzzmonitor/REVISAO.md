# Revisao LP — buzzmonitor/mcp-buzzmonitor

**Data:** 2026-09-18
**Auditores:** frontend-design (review mode) + web-design-guidelines (checks manuais equivalentes) + checks tecnicos (GTM, em-dash, SEO, fidelidade de copy)
**Contexto:** revisao apos a rodada de ajustes visuais pedida pelo Victor (hero preto/laranja, destaque Claude/ChatGPT, scroll-scrub no video, redesign da secao "Na pratica" no estilo `content.buzzmonitor.com/mcp-claude-latam`, fix do H2 de 2 linhas em "Menos tempo... Mais tempo...").

---

## Aplicado automaticamente (1 critico)

### Acessibilidade
- [x] **Efeito de digitacao no H2 "Na pratica" apagava o unico texto acessivel do heading** — a secao usa `aria-labelledby="na-pratica-title"`, e o script limpava `textContent` do proprio elemento com o `id` referenciado pra reconstruir char a char (~0.8s). Um leitor de tela que consultasse o nome acessivel da regiao nesse intervalo pegaria texto parcial ou vazio. Fix: o heading agora carrega um `<span class="sr-only">` permanente com o texto completo (nunca alterado) e a animacao visual roda num `<span aria-hidden="true">` irmao. Validado no navegador: o `sr-only` mantem "Na pr&aacute;tica, o que &eacute; o MCP da Buzzmonitor?" intacto do primeiro frame ao ultimo.

---

## Melhorias opcionais (3)

Para o Victor decidir. Aplicar via `Edit` manual ou pedir `/lp-revisar` novamente.

- [ ] **`.hero__label::before` (dot pulsante "Teste agora com dados publicos") usa `var(--teal)`** — o hero agora e preto com glow laranja/rosa, sem teal em nenhum outro elemento dele. Considerar trocar o dot para `--secondary` (laranja) pra manter a paleta do hero mais coesa (GUIDELINES §1).
- [ ] **`--secondary-light` referenciada via `var(--secondary-light, #FFD5C3)` em `.skill-card--1`/`.skill-card--5` nunca e definida em `:root`** — funciona pelo fallback do `var()` (renderiza a cor pessego certa), mas fica confuso pra quem for mexer depois. Definir `--secondary-light: #FFD5C3;` no `:root` ou remover a indirecao e usar o hex direto.
- [ ] **OG image (`assets/og-mcp-buzzmonitor.png`) ainda nao existe** — ja rastreado no `README.md` da LP desde a geracao inicial, reforcando aqui: gerar antes do `/lp-publicar` (GUIDELINES §18, 1200x630).

## Nice-to-haves (2)

Estilistico. Ignorar e aceitavel.

- [ ] **`<i data-prompts-rail>` usa a tag `<i>`** para a barra de progresso do rail (herdado 1:1 do padrao da LP de referencia). Semanticamente um `<span>` seria mais correto, mas como e `aria-hidden` via o pai, nao tem impacto real.
- [ ] **CSS morto:** `.chat-mock__caret` e `p.body-lg` estao definidos no `<style>` mas nao sao usados em nenhum elemento do HTML atual (sobras de geracoes anteriores). Remover numa limpeza futura.

---

## Auditorias automaticas (passaram)

- ✅ **GTM**: `GTM-WFJVK858` encontrado no head e no noscript, bate com a regiao Brasil (`brand/buzzmonitor/tracking.json`). Selo de tracking gravado (`--write-stamp`).
- ✅ **Em-dash**: 0 ocorrencias (`—` e `&mdash;`) — tolerancia zero respeitada, inclusive apos os 5 ajustes visuais.
- ✅ **Fidelidade de copy**: todo texto visivel bate literal com `copy.txt`. Os `<span class="hl">` em volta de "Claude"/"ChatGPT" so envolvem palavras que ja estavam la — nao e texto novo.
- ✅ **SEO**: 1 description, 1 robots, 10 og:*, 4 twitter:*, 1 JSON-LD (parseia e resolve `Organization.url` = `https://buzzmonitor.com/`, igual ao manifest), 1 canonical.
- ✅ **Multi-idioma**: LP unica (sem `-es`/`-pt`), hreflang correto omitido, so `canonical` + `x-default` proprios.
- ✅ **Logo regional**: header e footer apontam pra `https://buzzmonitor.com/` com `target="_blank" rel="noopener"`, nunca `href="/"`.
- ✅ **Logo web-safe**: `logo-primary.svg` e `logo-reversed.svg` sem `<text>` vivo (raster/base64) — nao serifa no browser.
- ✅ **Motion com fallback**: todas as animacoes novas (`.scrub`, `.prompt-card`, `.tw__caret`) tem estado final estatico garantido via `@media (prefers-reduced-motion: reduce)` e `.no-js`, testado no navegador desligando JS/scroll.
- ✅ **Mobile**: hero, cards de prompt (zigzag vira coluna unica) e rail testados em 375px sem overflow.

---

## Proximos passos

- Design aprovado? -> `/lp-integrar-form buzzmonitor/mcp-buzzmonitor "snippet"` (form ainda esta em mock)
- Rever mais algum critico? -> editar e rodar `/lp-revisar buzzmonitor/mcp-buzzmonitor` de novo
- Publicar so depois do form real e da OG image — `/lp-publicar buzzmonitor mcp-buzzmonitor [dominio]`
