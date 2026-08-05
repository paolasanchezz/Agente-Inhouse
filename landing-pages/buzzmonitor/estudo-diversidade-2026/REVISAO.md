# Revisão LP — buzzmonitor/estudo-diversidade-2026

**Data:** 2026-08-03 (revisão anterior: 2026-07-01, ver histórico no fim do arquivo)
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel Labs) + auditoria própria (GTM, SEO, copy-fidelidade)

## Aplicado automaticamente (3 críticos)

- [x] Em-dash em string JS (linha ~519, `quiz.explicacao`) — substituído por vírgula: "...3.455 interações por mil pessoas, bem acima..."
- [x] Em-dash em string JS (linha ~563, `renderResultado`) — substituído por ponto: "A realidade surpreendeu seu instinto. O estudo completo tem o retrato inteiro..."
- [x] Contraste AA reprovado no `.overline` do hero — `var(--laranja)` (#EB7C2E) sobre o fundo claro do gradiente do hero dava ~2,4:1 (reprova até o limiar de large text, 3:1). Trocado para `var(--roxo)` (#390155), ~16:1 de contraste, consistente com o `.kicker` já usado nas demais seções.
- [x] GTM auditado — container `GTM-WFJVK858` bate com a região `brasil` (`brand/buzzmonitor/tracking.json`). Selo `.tracking.lock` regravado (`stamp_match: true`).

## Já resolvido desde a revisão anterior (não é mais crítico)

- [x] **OG image 1200×630** — `assets/og-estudo-diversidade-2026.png` existe e tem as dimensões corretas (verificado: 1200×630). O crítico pendente de 2026-07-01 está fechado.

## Decisão do usuário — resolvida (2026-08-03)

- **[x] Seção QUIZ ("Teste seu feeling") não existe em `copy.txt`.** O `copy.txt` define 7 blocos (HERO, DESTAQUE, ACHADOS, PREMIO, POR QUE IMPORTA, CTA FINAL, FOOTER) — a seção de quiz interativo é uma adição sem copy-fonte formal. Usuária decidiu **manter e revisar pelo pilar anti-IA antes de publicar** (em vez de remover). Revisão feita contra `conhecimento/editorial/regras-anti-ia.md` completo (frases típicas de IA, filler words, antítese-por-negação, em-dash, estruturas viciadas): as 3 perguntas + opções + textos de resultado passam limpos — sem frases de IA, sem filler, sem antítese-por-negação, 0 em-dash (os 2 que existiam já foram corrigidos como crítico). Único ponto notado: a palavra "feeling" é um termo emprestado casual, mas usado com sentido concreto (é o próprio conceito do quiz, já no kicker "Teste seu feeling") — não é enfeite substituível, mantido como está.

## Melhorias opcionais (6)

- [ ] `.hero__mini` (2 fotos pequenas do hero, acima da dobra) usam `loading="lazy"` — pode atrasar o paint de elementos visíveis no load inicial. Considerar remover o lazy ou usar `fetchpriority="high"` como o `.hero__photo` já tem.
- [ ] Feedback do quiz (`.quiz__explain` / `.quiz__result`) é injetado via `innerHTML` sem `aria-live="polite"` no container `#quiz` — leitor de tela não anuncia automaticamente se a resposta estava certa/errada.
- [ ] SVGs com classe `.spin` aplicam `transform-box:fill-box` diretamente no `<svg>`; a recomendação Vercel é aplicar num `<g>` interno. Funciona hoje, mas diverge do padrão recomendado.
- [ ] Placeholders do form mock ("Seu nome", "voce@empresa.com", "Nome da empresa") não seguem a convenção "terminar com …". Sem urgência — form mock será substituído por embed real via `/lp-integrar-form`.
- [ ] `og:url` / `og:image` / JSON-LD apontam para `material.buzzmonitor.com` (guarda-chuva) — confirmar que esse é o domínio final no `/lp-publicar`; se mudar, atualizar as 2 URLs absolutas.
- [ ] `<link rel="alternate" hreflang="x-default">` presente mesmo sem LPs irmãs em outro idioma (GUIDELINES §16 só exige isso quando há variantes). Inofensivo, pode remover se quiser 100% aderência ao spec.

## Nice-to-haves (3)

- [ ] `.hero__mini`, `.pcard img`, `.pic img` não têm `width`/`height` HTML explícitos (o container já fixa o tamanho via CSS/aspect-ratio, então risco de CLS é baixo, mas os atributos fechariam 100% a regra de performance).
- [ ] Sem `<link rel="preload" as="font">` para a fonte crítica — a URL do Google Fonts já usa `display=swap`, então o impacto é pequeno.
- [ ] Paleta usa 6 cores base + 5 tints (mais que as "2-3 cores" da GUIDELINES §1) — decisão já documentada e aprovada pela cliente como estética "mosaico multicolor" (ver README, seção "Direção de design"). Não é um achado novo, só registrando que a regra §1 foi conscientemente flexibilizada aqui.

## Próximos passos

- Decidir sobre a seção QUIZ (ver acima) — sugestão: revisar as 3 perguntas pelo pilar anti-IA antes do próximo deploy, ou remover.
- Publicar: `/lp-publicar buzzmonitor estudo-diversidade-2026 material.buzzmonitor.com`
- Depois de aprovado o design: `/lp-integrar-form buzzmonitor/estudo-diversidade-2026 "<snippet>"`

---

## Histórico — revisão 2026-07-01 (arquivada)

**Aplicado automaticamente (6 fixes):**
- `scroll-margin-top:88px` em `#conteudo` e `#baixar`
- `fetchpriority="high"` na foto do hero
- `spellcheck="false"` + `inputmode="email"` no input de e-mail
- `.fcard__num` opacidade 0.65 → 0.85
- `<meta name="theme-color">` + `touch-action:manipulation` no body
- Removido CSS órfão `.porque__grid`

**Observação de marca (desvio consciente):** uso de degradês em vários pontos foge da regra conservadora do GUIDELINES §1 ("1 gradiente por LP") — pedido explícito da cliente para visual moderno, mantido dentro da família de cores da marca.
