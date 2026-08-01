# Revisão LP — buzzmonitor/plataforma-integral-social-media

**Data:** 2026-07-31
**Contexto:** substituição integral do design anterior (revisão de 2026-07-30 abaixo refere-se à versão antiga — ver git history). O conteúdo desta seção documenta a verificação **manual** feita nesta sessão para o novo design — não é uma auditoria automatizada `frontend-design`/`web-design-guidelines` (recomendado rodar `/lp-revisar` numa próxima iteração).

## Verificado manualmente nesta sessão (design novo, 2026-07-31)

- [x] Bug de CSS corrigido: `.audience { display:flex }` tinha a mesma especificidade que `[hidden]`, fazendo as 3 tabs de audiência (Agencias/Marcas/Gobierno) aparecerem empilhadas ao mesmo tempo. Corrigido com `.audience[hidden] { display: none; }`. Verificado via `getComputedStyle` + clique real simulando cada tab.
- [x] Paths de asset corrigidos pra convenção do repo (`landing-pages/CONTEXT.md` §3.2): brand assets (logo primário, ícone/favicon) apontam pra `../../brand/buzzmonitor/assets/logos/...`; logos LP-local (agências/clientes) usam `./assets/...` relativo — nenhum path absoluto (`/assets/...`) sobrando, que quebraria em modo guarda-chuva.
- [x] Placeholders de deploy (`{{DOMAIN}}`, `{{OG_IMAGE_PATH}}`, `{{BRAND_LOGO_PNG_PATH}}`) aplicados no `<head>` (canonical, og:url, og:image, twitter:image, JSON-LD) — mesma convenção da versão anterior desta LP, resolvidos automaticamente por `lp-publicar`/CI.
- [x] Hover de logos com texto branco (Eureka&Co, Havas) corrigido pra preto no hover — texto branco ficava invisível sobre o filtro `brightness(0) invert(.55)` do estado default.
- [x] Logo "Agencia Lead" com estados corretos: cinza no estado default (igual ao resto da fila), "LEAD" em vermelho + "DIGITAL" em preto no hover.
- [x] Interatividade verificada via simulação real (não só leitura de CSS): scroll-reveal (IntersectionObserver + fallback `setTimeout`), contadores animados (formatação de milhar com ponto, não vírgula — `toLocaleString('es-419')` dava vírgula, trocado por regex manual), tabs (clique real alternando `hidden`/`aria-selected`/`is-active`), carrossel de logos (`translateX` provado via 2 screenshots com conteúdo diferente).
- [x] `prefers-reduced-motion` já presente no arquivo (kill-switch global de animação/transição) cobre automaticamente as novas animações.
- [x] GTM `GTM-MKQBX2MG` mantido (mesmo ID já validado por `.tracking.lock` — fingerprint não muda pois região/ID não mudaram, selo permanece válido).

## Não verificado / pendente

- [ ] Auditoria formal de contraste AA (a paleta laranja `#ff6b16`/rosa `#ec174c` desta versão não passou pelo mesmo processo de tokens `--orange-ink` da versão anterior)
- [ ] Auditoria `web-design-guidelines` (Vercel Labs) — padding de seção, performance de animação (`box-shadow` vs `transform`), etc.
- [ ] Anti-IA formal (regras-anti-ia.md) — feita apenas varredura manual de em-dash, sem o processo completo dos 3 pilares

## Próximos passos

- Rodar `/lp-revisar buzzmonitor/plataforma-integral-social-media` pra auditoria formal, se desejado.
- `/lp-publicar buzzmonitor plataforma-integral-social-media content.buzzmonitor.com` — fluxo CI (domínio já migrado).

---

## Histórico — revisão do design anterior (substituído em 2026-07-31)

**Data:** 2026-07-30
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel Labs)

### Aplicado automaticamente (9 críticos)

- [x] Contraste AA: laranja (#EB7C2E) usado como cor de texto/ícone sobre fundo claro falhava (~2.6-2.8:1). Criado token `--orange-ink:#B34F15` (4.5-5:1 verificado matematicamente) e aplicado em `.kpi__delta`, `.compare-card--good svg`, `.fox-wrap svg`.
- [x] Contraste AA: texto branco sobre a ponta laranja do gradiente (`.btn-cta`, `.compare-card--good .compare-card__head`, `.race-bar--you`) falhava (~2.8:1). Criado `--gradient-safe` (rosa → laranja escurecido #B34F15) e aplicado nesses 3 componentes.
- [x] Texto de gradiente (H1/H2 `.grad`) sem fallback se `background-clip:text` não for suportado — adicionado `@supports not (background-clip:text)` com cor sólida de fallback nas 3 instâncias.
- [x] SVGs decorativos sem `aria-hidden="true"` explícito — todos corrigidos.
- [x] `#cta-final` sem `scroll-margin-top` — adicionado `scroll-margin-top:88px`.
- [x] `--subtitle` usava 'League Spartan' como fallback de HK Grotesk — trocado para 'Lato'.
- [x] Padding de seção abaixo do mínimo de GUIDELINES §2 — aumentado para 130px/84px.
- [x] GTM auditado via `check_gtm_region.py` — status `ok` (GTM-MKQBX2MG, região latam), selo `.tracking.lock` gravado.
- [x] Auditoria de fidelidade de copy — 0 vazamentos encontrados.
