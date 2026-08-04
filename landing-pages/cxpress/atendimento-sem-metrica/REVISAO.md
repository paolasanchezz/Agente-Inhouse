# Revisão LP — cxpress/atendimento-sem-metrica

**Data:** 2026-08-03
**Auditores:** frontend-design (review mode) + web-design-guidelines + checagens determinísticas (SEO/GTM/OG/em-dash)

## Aplicado automaticamente (1 crítico)

- [x] **Contraste AA do rótulo de seção sobre fundo lavanda** — `.section-label` (royal `#4A69BD`) na seção `.program` ("O webinar", fundo `#D7E2FF`) dava ≈4.0:1, abaixo do AA 4.5:1 para texto 13px (GUIDELINES §7 marca essa combinação como reprovada). Override adicionado: `.program .section-label, .cta-final .section-label { color: var(--primary-dark); }` (≈10:1). Os outros 4 rótulos estão sobre branco e já passavam.

## Determinísticas (todas verdes, nada a corrigir)

- Em-dash: 0 · Pacote SEO completo (description, robots, og×10, twitter×4, JSON-LD, canonical)
- JSON-LD parseia (`Organization`/`WebPage`/`Event`), `Organization.url` = home oficial
- GTM × região: `GTM-T4XDWHL3` = brasil (selo `.tracking.lock` gravado)
- OG image 1200×630, URL absoluta · logos SVG sem `<text>` vivo · hreflang não requerido (LP única)

## Melhorias opcionais (não aplicadas — decisão do autor)

- [ ] **CTA final sem peso visual (§8)** — `.cta-final` usa lavanda claro; a última chamada devia "gritar" (gradiente/primary + texto claro, igual ao bloco `.signup`). Hoje a abertura tem mais impacto que o fechamento.
- [ ] **`.ribbon-txt` sem cor sólida de fallback** — o H2 "Garanta sua vaga" depende de `background-clip:text` + `-webkit-text-fill-color:transparent`; sem suporte, o título some. Add `color: var(--primary-dark)` como base (suporte é amplo, risco baixo, mas fix é 1 linha).
- [ ] **Copy duplicada hero ↔ inscrição** — `hero-support` repete quase literal o `signup-sub` ("Descubra como empresas com clientes felizes..."). Variar uma das duas.
- [ ] **Kicker duplica a pílula (§3)** — kicker "Webinar gratuito" + pílula "Gratuito". Tirar "Gratuito" de um dos dois.
- [ ] **JSON-LD sem `sameAs` (§15)** — `Organization` não lista LinkedIn/Instagram. Puxar de `brand/cxpress/brand-manifest.json`. (Padrão herdado das outras LPs Cxpress — vale um passe amplo, não só nesta.)
- [ ] **Contraste do placeholder** — `::placeholder rgba(74,74,74,0.5)` ≈2.3:1; escurecer p/ ~`#6b6b6b`.
- [ ] **Newsletter abre nova aba sem aviso** — form Mailchimp `target="_blank"` sem texto oculto "(abre em nova aba)" p/ leitor de tela.
- [ ] **Skip-link só com `:focus-visible`** — adicionar `.skip-link:focus` como rede de segurança.
- [ ] **`rel` inconsistente** — padronizar todos os `target="_blank"` com `rel="noopener noreferrer"`.
- [ ] **`scroll-padding-top: 80px` vs header 72px** — alinhar à altura real do header.

## Nice-to-haves (estilístico, ignorar é aceitável)

- [ ] H1 "Atendimento sem métrica" nomeia o tema; poderia ser mais dor explícita (ex: "Você toca o atendimento no escuro") — a linha atual funciona.
- [ ] `.audience` sem `overflow: hidden` — blindagem §14 (Safari iOS) de custo zero.
- [ ] `inputmode="tel"` no campo WhatsApp.
- [ ] Fontes bloqueiam render — carregar via `preload`/`media=print onload`.
- [ ] `<meta robots index,follow>` é redundante (default).
- [ ] Header sem `<nav>` (só logo + 1 CTA; landmark explícita seria melhor).
- [ ] `alt="Cxpress"` do logo do header duplica o `aria-label` do link — poderia ser `alt=""`.

## Verificado e OK (não são achados)

- Números laranja dos cards (`.program-number` #EF863C sobre branco): uso sancionado pelo BRANDBOOK ("highlight de número").
- `.btn-accent` (branco sobre laranja) definido no CSS mas **não usado** no markup — sem violação em tela.
- Fallbacks de motion completos (`<noscript>` + `prefers-reduced-motion` + branch sem IntersectionObserver).
- Landmarks, ordem de headings, labels, alt, aria-hidden, `:focus-visible`, skip-link, favicon — todos presentes.
- Form da inscrição é mock intencional, bem estruturado (labels/autocomplete/required) — troca via `/lp-integrar-form` sem retrabalho de a11y.

## Próximos passos

- Publicar o crítico: vai pelo fluxo CI (`/lp-publicar cxpress atendimento-sem-metrica content.cxpress.io` → PR → merge → deploy).
- Aprovar melhorias? Aplico as marcadas e subo no mesmo PR.
- Design aprovado + form pronto? `/lp-integrar-form cxpress/atendimento-sem-metrica "{snippet}"`.
