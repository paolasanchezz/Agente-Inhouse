# LP Buzzmonitor — monitoramento-manual-pt (PT-PT)

**Gerado em:** 2026-08-11
**Copy-fonte:** `copy.txt` (tradução PT-PT via `/trad-traduzir` da copy de `landing-pages/buzzmonitor/plataforma-completa-monitoramento/copy.txt`)
**Deliverable de tradução:** `traducao/entregas/2026-08/plataforma-completa-monitoramento-original.md` + `plataforma-completa-monitoramento-pt-pt.md`
**Uso:** Réplica em Português Europeu da LP da Dor 1 (monitoramento manual, sem ferramenta)
**Publicado em:** `content.buzzmonitor.com/monitoramento-manual-pt` (guarda-chuva migrado para CI — live desde 2026-08-21)

## Formato

HTML e CSS **idênticos** ao original `plataforma-completa-monitoramento/index.html` (mesmas 706 linhas, mesma estrutura, mesmas 11 seções, mesmos 6 cards de benefício, 5 itens de problema, 4 cases) — só a copy muda de idioma. Assets visuais (SVG hero, GIF/WebP de demo, insights.png, crise-1/2.png, logo-wall.png) foram copiados sem alteração do original.

## Estrutura

- HEADER (logo + CTA `.btn-glow`, href da logo apontando para `https://getbuzzmonitor.com/pt/`)
- HERO (overline + H1 + sub + CTA + ilustração SVG inline, reaproveitada sem alteração)
- PROBLEMA (lista vertical, 5 itens)
- SOLUCAO (fundo `.bg-gradient` animado, grid de 6 cards)
- DESTAQUE-IA (GIF/WebP de demonstração à direita, reaproveitado)
- INSIGHTS (layout espelhado, imagem `insights.png` à esquerda)
- GESTAO-DE-CRISE (colunas invertidas, composição `crise-1.png` + `crise-2.png`)
- PARA-QUEM (fundo `.bg-aurora`)
- PROVA (case Caffeine Army)
- CASES (4 cards: Oi, Betnacional, Grupo Casas Bahia, Camil — mesmos dados do original)
- CTA-FINAL (fundo gradiente, embed Jotform próprio de Portugal — ver Estado)
- LOGO-WALL (imagem `logo-wall.png` reaproveitada — **com texto em PT-BR embutido nos píxeis**, ver Pendências)
- DEPOIMENTOS — **PENDENTE**, mesma pendência do original
- FOOTER

## Adaptações linguísticas PT-PT aplicadas (além da tradução literal)

- "monitoramento" → "monitorização" / "monitorar" → "monitorizar" em toda a página
- "time"/"equipe" → "equipa"; possessivos com artigo ("a sua marca", "os seus resultados")
- "customizável" → "personalizável"; "controle" → "controlo"; "economizar" → "poupar"
- "na mão" → "à mão"; "aba" (browser) → "separador"; "celular" → "telemóvel"; "usuários" → "utilizadores"
- "gerencie crises" → "faça a gestão de crises"; "exploda" → "rebente" (idiomático PT-PT)
- "um real" (moeda BR) → "um cêntimo" (adaptado para não referenciar moeda brasileira)
- CTA padronizado: "Agendar demonstração gratuita" → "Pedir demonstração gratuita" (forma nominal, padrão PT-PT — golden rule #6 do `padrao-linguistico.md`)
- `og:locale`/`inLanguage`/`html lang` → `pt_PT`/`pt-PT`
- GTM: container **`GTM-NCFT22CW`** (Portugal), diferente do BR (`GTM-WFJVK858`) — conforme `brand/buzzmonitor/tracking.json`
- Header/footer: logo aponta para `https://getbuzzmonitor.com/pt/` (home regional Portugal), não para o `.com` brasileiro
- JSON-LD: `Organization.url` = home PT, `sameAs` inclui Instagram PT (`buzzmonitor.pt`); `Organization.@id` mantido no domínio BR (canônico entre regiões, conforme convenção do `lp-gerar`)

## Estado

- [x] Tradução PT-PT (via `/trad-traduzir`)
- [x] HTML gerado (réplica estrutural do original, copy substituída)
- [x] Formulário integrado — **Form provider:** Jotform (integrado em 2026-08-11, via `/lp-integrar-form`) — embed próprio `https://form.jotform.com/jsform/261405305585859`, distinto do form BR (`252995108251662`). Wrapper CSS `.jotform-embed iframe` já existia (herdado do original), sem necessidade de ajuste.
- [x] OG image `assets/og-monitoramento-manual-pt.png` (1200x630, ~90 KB) — gerada em 2026-08-21 a partir de `assets/og-source.html` (clone do original com o H1 em PT-PT, `lang="pt-PT"`), via `assets/render_og.py` / Chrome headless. O path do logo foi corrigido para `../../../../brand/` (o original usa 3 níveis e renderiza sem logo) e passou a usar `logo-primary.svg`: o `.png` é uma tela quadrada de 250x250 com o lockup de 227x46 centrado, então `height:56px` reduzia a marca a ~10 px.
- [x] Revisão (`/lp-revisar buzzmonitor/monitoramento-manual-pt`) — ver `REVISAO.md`: 5 críticos aplicados (hreflang recíproco com a LP BR, og:locale:alternate, fallback de `prefers-reduced-motion` em 2 animações contínuas, `transition:all` trocado por lista explícita); 2 melhorias pendentes de decisão do usuário (contraste do CTA laranja/branco e overline sem copy-fonte, ambas herdadas do original — corrigir aqui exigiria sincronizar a LP BR também); 3 nice-to-haves documentados
- [x] Adicionada ao manifest do guarda-chuva — `slug: "monitoramento-manual-pt"` em `landing-pages/dominios/content-buzzmonitor-com/manifest.json`, URL final `content.buzzmonitor.com/monitoramento-manual-pt`
- [x] `hreflang` recíproco fechado em 2026-08-21 — as 3 tags (`pt-BR`, `pt-PT`, `x-default`) foram espelhadas no `index.html` da LP BR `plataforma-completa-monitoramento`, mais `og:locale:alternate=pt_PT`. Sem isso o cluster era unilateral e o Google descartava a anotação.
- [x] Publicado — PR #241 mergeado pelo Victor em 2026-08-21 (commit `d8a06ca`), CI buildou e deployou `content.buzzmonitor.com/monitoramento-manual-pt` com sucesso (smoke test, OG image e hreflang recíproco confirmados no ar)

## Pendências

- **Depoimentos:** seção "Ainda não está convencido?" pendente também no original — aguardando o usuário reenviar o texto completo dos 3 depoimentos.
- **LOGO-WALL com texto embutido:** `assets/logo-wall.png` traz o título ("Empresas que já confiam na Buzzmonitor"), as estatísticas e a grade de logótipos desenhados diretamente na imagem, em PT-BR. Uma tradução de copy não altera texto de imagem — reaproveitado por ora para manter o formato idêntico ao original, mas a página só fica 100% localizada em PT-PT se este asset for recriado (ou a secção recriada em HTML).
- **OG image do original (LP BR):** resolvida aqui, mas a LP BR `plataforma-completa-monitoramento` segue com o mesmo bug de path do logo no `og-source.html` (3 níveis em vez de 4) e com o `.png` de tela quadrada — a OG dela está no ar sem logo. Correção fora do escopo deste PR.
- **Claim do case Caffeine Army** ("o lançamento foi um sucesso porque a marca ouviu o cliente"): mesma pendência de verificação do original — não confirmado no case do BRANDBOOK.
- **Case Betnacional** menciona "o maior reality do Brasil" — mantido como no original (mesmos clientes/dados), mas é uma referência de mercado brasileiro numa LP de Portugal; decisão de manter ou não é do usuário, não uma questão de tradução.

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header) e `logo-reversed.svg` (footer) — mesmos do original, validados sem `<text>` vivo
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `./assets/destaque-ia.webp` + `./assets/destaque-ia.gif` (copiados do original, sem texto embutido)
- `./assets/insights.png`, `./assets/crise-1.png`, `./assets/crise-2.png` (copiados do original, sem texto em português embutido)
- `./assets/logo-wall.png` (copiado do original — **com texto em PT-BR embutido**, ver Pendências)
