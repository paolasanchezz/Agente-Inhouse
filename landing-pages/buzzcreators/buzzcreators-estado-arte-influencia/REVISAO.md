# Revisão LP — buzzcreators/buzzcreators-estado-arte-influencia

**Data:** 2026-05-26
**Auditor:** revisão focada (em-dash + fidelidade + a11y essencial)

## Atualização pós-review (PR #10, 2026-05-27)

Aplicados os importantes do review do PR #10:

- **SEO completo (GUIDELINES §15):** adicionados robots, Open Graph (10 tags), Twitter Card (4), JSON-LD (Organization + WebPage) e canonical. Supersede a observação antiga "a LP não tem og:image" das seções abaixo.
- **OG image 1200x630:** gerada em `assets/og-buzzcreators-estado-arte-influencia.png` (118KB), apontada em og:image/twitter:image com URL absoluta do deploy.
- **Logo (GUIDELINES §12/§17):** `logo-full-color.svg` trocado de raster base64 (113KB) pelo vetor limpo do brand (18KB); footer passou a usar `logo-full-white.svg` (sem o filtro brightness/invert); header e footer agora linkam para a home da marca com `target="_blank"`.
- **a11y:** `min-height: 0` no mascote (§14, Safari iOS); glifo ▶ do jogo embrulhado em `aria-hidden`.

## Aplicado automaticamente (0 críticos)

Nenhuma violação crítica encontrada.

### Validações executadas

- **Em-dash (regras-anti-ia §em-dash + GUIDELINES §5):** 0 ocorrências de `—` ou `&mdash;` no HTML. ✓
- **GTM (CONTEXT §5):** `tracking.json` da Buzzcreators está todo null. HTML não tem snippet GTM injetado. ✓ (alinhado com tracking.json)
- **Favicon (GUIDELINES §12):** link único PNG `../../brand/buzzcreators/assets/logos/logo-icon.png`. ✓
- **A11y essencial (GUIDELINES §7):**
  - Skip-link presente ✓
  - `:focus-visible` com outline laranja ✓
  - `prefers-reduced-motion: reduce` honrado (animações + marquee) ✓
  - Todas as `<img>` com atributo `alt` ✓
  - Labels associados a todos os `input` ✓
  - `aria-hidden="true"` em SVGs decorativos ✓
- **Hero mobile (GUIDELINES §3):** hero centralizado, sem grid 2-cols — N/A o problema de card-acima-da-headline.
- **Fidelidade de copy:** títulos e bodies do HTML conferem com `copy.txt` (após atualização "agora"). Marquee usa labels curtas derivadas dos items principais — whitelist permitida (cabeçalho decorativo factual, mesma terminologia da copy).
- **Form (GUIDELINES §11):** mock com `action="#"` + `onsubmit="event.preventDefault()"`. Integração real virá via `/lp-integrar-form`.
- **Form na 2ª seção (GUIDELINES §10):** ToFu / material rico — ✓ form imediatamente após hero.
- **Paleta (GUIDELINES §1):** 3 cores (roxo escuro `#3a1652`, roxo médio `#6a3895`, laranja `#ff8119`). Gradiente assinatura aplicado em 2 momentos de impacto: hero word "agora" + número "US$ 32 bi". Tem-se margem para um terceiro só se necessário.

## Melhorias opcionais (3)

Não bloqueiam publicação — anote pra próxima rodada se quiser.

- [ ] **Performance**: considerar comprimir SVGs inline (alguns ícones têm paths verbosos). Ganho mínimo em página com poucos assets.
- [ ] **Marquee em mobile**: a animação roda em telas pequenas. Para LPs futuras consideramos pausar < 480px (a quantidade de pills tem boa leitura mesmo rolando, mas pode distrair). Não crítico.
- [ ] **Decoração `.hero-spark`**: removida na refatoração; se quiser, dá pra reintroduzir como marcador editorial discreto no canto.

## Nice-to-haves (2)

- [ ] Considerar substituir `box-shadow` em alguns hovers por `transform: translateY(...)` puro + `transition` mais curta (perf marginal).
- [ ] OG image custom (1200×630) com cover do material — hoje a LP não tem `og:image` setado; para compartilhamento social vale criar.

## Próximos passos

- Design aprovado ✓
- Form: publicar com mock (integração real depois via `/lp-integrar-form buzzcreators/buzzcreators-estado-arte-influencia "<snippet>"`)
- **Publicar:** `/lp-publicar buzzcreators buzzcreators-estado-arte-influencia material.buzzmonitor.com`
