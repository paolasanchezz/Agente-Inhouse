# Revisao LP — buzzmonitor/primer-listening-5-pasos

**Data:** 2026-08-06
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel) + auditoria GTM/copy/SEO (lp-revisar)

## Aplicado automaticamente (2 criticos)

- [x] **Ellipsis literal (GUIDELINES §5 + Web Interface Guidelines)** — H2 da secao "Para quien es" usava `"..."` (3 pontos literais) em vez de `&hellip;`. Corrigido para `Este webinar es para ti si&hellip;`.
- [x] **CSS morto** — `.hero-actions .btn { width: 100%; }` (media query 520px) nao tinha mais elemento correspondente depois que o botao solto do hero foi substituido pelo formulario. Removido.

## Auditorias que passaram sem achados

- **Fidelidade de copy:** todo texto visivel bate literal com `copy.txt` (ja atualizado com os ajustes de CTA e body do CTA final feitos a pedido do usuario, com nota de rastreabilidade). Em-dash: 0.
- **GTM:** `GTM-MKQBX2MG` (regiao latam) presente no `<head>` e no `<noscript>` — bate com `tracking.json`.
- **SEO:** 1 description, 11 `og:`, 4 `twitter:`, JSON-LD parseia (Organization + WebPage + SoftwareApplication), 1 canonical, 3 hreflang (es-419, pt-BR, x-default) com codigos validos.
- **Logo:** header/footer apontam pra `regions.latam.home`, `target="_blank" rel="noopener"`, `aria-label` em ES ("página principal"). SVGs sem `<text>` vivo.
- **Acessibilidade:** skip-link, focus-visible, labels em todos os campos do form, alt em todas as imagens, decorativos com `aria-hidden`, `prefers-reduced-motion` coberto globalmente (alem do `.reveal`), `min-height:0` no `<img>` da foto do speaker (grid com aspect-ratio).
- **Estrutura "prova/speaker" (GUIDELINES §8):** layout horizontal (foto esquerda, nome/cargo direita) — corrige o desvio que essa mesma gramatica teve na LP anterior (`webinar-atencion-multicanal-latam`, que usava card vertical centralizado).

## Melhorias opcionais (2)

Para o usuario decidir. Nao alterei automaticamente.

- [ ] **Formulario no hero, nao na "2a secao"** — GUIDELINES §10 recomenda, por padrao, o form ToFu na 2a secao (logo apos o hero), nao dentro do proprio hero. Aqui o form fica dentro do hero-visual, espelhando literalmente o modelo `que-es-mcp` (decisao explicita do usuario). Documentado como override intencional, nao como erro.
- [ ] **Contraste do botao "Reserva tu lugar gratis"** (branco sobre laranja `--accent`, ~2.8:1) fica abaixo de AA para texto normal. Mesmo padrao ja usado em todos os botoes do guarda-chuva (inclusive no `que-es-mcp` ja publicado) — nao alterei pra nao divergir do sistema visual estabelecido. Se quiser, posso escurecer o laranja so nos botoes ou usar o roxo primario, mantendo o layout.

## Nice-to-haves (1)

- [ ] Secoes (`<section>`) sem `aria-labelledby` apontando pro heading correspondente — mesma lacuna do modelo `que-es-mcp` espelhado. Puramente incremental, nao e requisito "non-negotiable" do GUIDELINES §7.

## Proximos passos

- Formulario ainda e mock — quando tiver o provedor real (ClickMeeting/Jotform/HubSpot), rodar `/lp-integrar-form buzzmonitor/primer-listening-5-pasos "snippet"`.
- Publicar: `webinar.buzzmonitor.com` esta no fluxo CI — adicionar ao manifest + PR (ver `.claude/skills/lp-publicar/SKILL.md` Passo 0.0).
