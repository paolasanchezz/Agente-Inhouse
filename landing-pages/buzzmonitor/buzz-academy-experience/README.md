# LP Buzzmonitor — buzz-academy-experience

**Gerado em:** 2026-08-03 (v2 no mesmo dia)
**Copy-fonte:** `copy.txt` (output de /lp-preparar; fonte bruta: doc interno "Buzz Academy Experience — Universidade do Buzz")
**Briefing especial (v2):** a Universidade do Buzz tem **identidade visual própria**, fora do brandbook Buzzmonitor — base **preta** (#060608, não o roxo da marca) + **botões azuis** (#3E9BFF, azul vibrante claro com texto escuro por AA; decisão do Victor, mesmo fora da paleta). Trilhas mantêm codificação de cor: Intelligence=lilás, Growth=teal, Branding=laranja. **Sem formulário**: todo CTA "Cadastrar gratuitamente" aponta direto pra plataforma (`https://universidadedobuzz.com/local/staticpage/view.php?page=BuzzAcademyExperienceProjeto`). Animações CSS fluidas (blobs orgânicos em morph, `.det__fx`) dentro de cada trilha expandida + gradient-text animado no "Experience" do hero.

## Estrutura (v2)

- HERO (preto, H1 com "Experience" em gradient-text animado, 3 pills de trilha, CTA → plataforma)
- PROBLEMA (4 dores, lista vertical com X)
- PONTE (seção de pausa aérea — §2)
- TRILHAS overview (grid 3 cards)
- TRILHAS detalhe (3 `<details>` expansíveis com campo de blobs fluidos animados por trilha, 5 cursos cada, CTA por trilha)
- COMO-FUNCIONA (4 passos, teal)
- PARA-QUEM (3 perfis, check teal)
- CTA-FINAL (preto + aurora azul, tag azul rotacionada)
- FOOTER

Sem seção de cadastro/form (removida na v2 — CTA vai direto pra plataforma).

## Estado

- [x] HTML gerado (+ v2: ID própria preta/azul, sem form, animações fluidas)
- [x] Revisão (frontend-design review + web-design-guidelines) — 2026-08-03; contraste v2 re-verificado por script (20 pares AA OK)
- [x] OG image 1200×630 (`assets/og-buzz-academy-experience.png`)
- [x] Publicado em content.buzzmonitor.com via CI (PR #183; v2 em PR seguinte)
- [x] Deep link de trilha (`#trilha-growth`, `#trilha-branding`, `#trilha-intelligence`) abre o `<details>` e alinha o scroll no load e no `hashchange` — 2026-08-12. Antes, chegar pelo link deixava o acordeão fechado (o abrir só estava ligado ao clique interno). Clique nas pills segue com scroll suave nativo.

OG image regenerada na v2 (preta/azul, gradient no "Experience") — consistente com a página.

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (nav + footer, raster base64 web-safe §19)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon §12)

## GTM

- Região: brasil (slug sem sufixo → fallback §5.1) → container `GTM-WFJVK858` injetado (head + noscript). Gate `check_gtm_region.py`: OK.

## Pendências de conteúdo (ver toggle no Notion da copy)

- [FACT-CHECK] "certificado" (COMO-FUNCIONA) — confirmar com o time da Buzz Academy.
- [OBSERVACAO] Nomes quase iguais de curso de IA nas trilhas Intelligence e Branding (literal do catálogo-fonte).
- [OBSERVACAO] "Universidade do Buzz" (doc-fonte) vs "Buzz Academy" (briefing) — copy segue o briefing.
