# Revisao LP — cxpress/cadastro-realizado

**Data:** 2026-08-11
**Auditores:** frontend-design (review mode) + web-design-guidelines + checks deterministicos (GTM, copy, SEO)

## Aplicado automaticamente (1 critico)

- [x] Footer sem logo — GUIDELINES §17 exige logo+link regional tanto no header quanto no footer; a versão inicial só tinha texto de copyright. Adicionado `footer__logo` (logo-reversed.svg, link para home.cxpress.io, `target="_blank" rel="noopener"`), igual ao padrão usado em `video-atendimento-obrigado` e nas demais LPs.

## Checks deterministicos — todos OK

- **GTM** (`check_gtm_region.py`): `status=ok`, container `GTM-T4XDWHL3` bate com região `brasil` (detectada via `<html lang="pt-BR">`). Selo `.tracking.lock` gravado.
- **Em-dash**: 0 ocorrências.
- **Fidelidade de copy** (`copy.txt` vs HTML renderizado): sem vazamento — os dois textos visíveis ("Cadastro realizado com sucesso.", "Em breve você receberá nosso contato.") são cópia literal da fonte (`home.cxpress.io/obrigado`); footer é boilerplate de copyright (whitelist).
- **A11y**: skip-link presente e funcional, `:focus-visible`, `aria-hidden` no ícone decorativo, `aria-labelledby` na seção, alt="" nos logos com `aria-label` no link pai, reduced-motion + fallback triplo (noscript / sem IntersectionObserver / timeout 1.5s) para o reveal — sem texto essencial dependente de animação.
- **Contraste**: H1 (navy sobre branco) e subtítulo (neutral-700 sobre branco) e footer (primary-light sobre navy) — todos acima de AA.

## Exceções deliberadas (não são achados — já documentadas no README.md)

Esta é uma thanks page pós-ação, mesmo tratamento de `video-atendimento-obrigado` e `conheca-a-cxpress-confirmado`:

- Sem OG image, sem tags OG/Twitter/JSON-LD, sem hreflang — ninguém compartilha essa URL.
- `robots: noindex, follow` deliberado.

## Nice-to-haves (1)

- [x] Ícone do check usa `stroke="#EF863C"` fixo em vez de `stroke="currentColor"` + `color: var(--accent)` no CSS — cosmético, sem impacto funcional. **Aplicado no redesign de 2026-08-13.**

---

# Redesign 2026-08-13 — checks

**Escopo:** mascote + acabamento visual. Copy, GTM, robots e estrutura de blocos inalterados.

## Checks deterministicos — todos OK

- **GTM** (`check_gtm_region.py landing-pages/cxpress/cadastro-realizado`): `1 OK, 0 aviso(s), 0 bloqueio(s)`. Container `GTM-T4XDWHL3` preservado nas 2 posições (script no `<head>` + `<noscript>` no `<body>`).
- **Sem WhatsApp**: `grep -ci 'whatsapp\|wa.me' index.html` = 0.
- **Em-dash**: 0 ocorrências (`—` e `&mdash;`).
- **Fidelidade de copy**: os 2 textos visíveis seguem cópia literal da fonte. Nenhum bloco de texto novo (GUIDELINES §9).
- **Build do guarda-chuva** (`build_umbrella.py` sobre `content-cxpress-io/manifest.json`): 46 LPs, sem aviso para `cadastro-realizado`. Paths reescritos para `/assets/cxpress/...` e `samir-joinha-web.png` (84 KB) copiado pro dist.

## Design / a11y

- **Paleta (GUIDELINES §1)**: navy `#232960` (texto/rodapé) + âmbar `#FFD98A`–`#FFF4D6` (medalhão) + laranja `#EF863C` (selo). 1 gradiente de fundo, 1 gradiente radial no disco — mesma família, sem colcha de retalhos.
- **Contraste**: H1 navy sobre `#F7FAFF` ≈ 14:1; subtítulo `#4a4a4a` sobre `#E9F1FF` ≈ 7,8:1; rodapé `#C1C7FF` sobre navy — todos acima de AA.
- **GUIDELINES §14**: `min-height: 0` no `<img>` do mascote (defesa Safari iOS) + `overflow: hidden` no disco e na seção.
- **Motion**: entrada do medalhão e traço do check só decoram; `aria-hidden="true"` no bloco inteiro e `prefers-reduced-motion` desliga animação e transição. Texto essencial nunca depende de animação (fallback triplo mantido).
- **Overflow horizontal**: medido em viewport de 375px — `documentElement.scrollWidth == innerWidth`, único elemento fora da viewport é o `.skip-link` (esperado, `left: -9999px`).
- ⚠️ **Armadilha de harness**: Chrome headless no Windows força largura mínima de **500px** de janela. `--window-size=390,844` renderiza a 500 e recorta o print em 390, o que aparenta conteúdo deslocado/cortado. Não é bug da LP — validar mobile a 500px ou medindo `scrollWidth` no browser.

## Renders conferidos

1440×900 (desktop), 1024×768 (tablet) e 500×900 (estreito) — composição centralizada e mascote inteiro dentro do medalhão (o joinha não é recortado; o que o disco corta é a manga, de propósito).

Em 1440×900 a página fecha na dobra, rodapé incluído. Em viewport baixa (768px de altura) o rodapé fica abaixo da dobra e a página rola alguns pixels — comportamento esperado de `min-height: 100dvh` com conteúdo de altura fixa, não é defeito.

## Próximos passos

- Sem form nesta LP — não há integração de form a fazer.
- Aprovado? -> `/lp-publicar cxpress cadastro-realizado content.cxpress.io`
