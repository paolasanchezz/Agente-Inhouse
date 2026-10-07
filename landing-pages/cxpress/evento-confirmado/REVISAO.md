# Revisao LP — cxpress/evento-confirmado

**Data:** 2026-10-06
**Auditores:** design review + web-design-guidelines + checks deterministicos (GTM, copy, em-dash) + preview no browser (1280px e 375px)

## Aplicado automaticamente (0 criticos)

Nenhum achado critico.

## Checks deterministicos — todos OK

- **GTM** (`check_gtm_region.py`): `1 OK, 0 aviso(s), 0 bloqueio(s)`. Container `GTM-T4XDWHL3` (Cxpress Brasil) nas 2 posições.
- **Em-dash**: 0 ocorrências (`—` e `&mdash;`).
- **Fidelidade de copy**: os 6 textos visíveis (etiqueta, H1, subtítulo, H2, 3 passos) são cópia literal de `copy.txt`. Footer = padrão do domínio (whitelist). Nenhum texto inventado.
- **GUIDELINES §9**: 3 passos na copy = 3 itens na lista.
- **Logos §19**: `logo-primary.svg` e `logo-reversed.svg` sem `<text>`.
- **Preview**: imagens carregam, sem scroll horizontal em 375px, footer e card renderizam no desktop.

## A11y

- skip-link, `:focus-visible`, `aria-labelledby` na seção e no card, medalhão inteiro `aria-hidden`, logos com `alt=""` + `aria-label` no link, ícones sociais `aria-hidden` com `aria-label` no link (alvo de 44px).
- Lista numerada semântica (`<ol>`), número via CSS counter (leitor de tela anuncia a ordem pela lista).
- Reveal com fallback triplo (noscript / sem IntersectionObserver / timeout 1.5s) + `prefers-reduced-motion`.
- Contraste: etiqueta navy sobre `#D7E2FF` (~10:1), números navy sobre `#FFF3DA`, texto `#4a4a4a` sobre branco (~8.9:1), footer `#D7E2FF` sobre navy. Todos acima de AA.

## Exceções deliberadas (não são achados — documentadas no README.md)

- `noindex, follow`, sem OG/Twitter/JSON-LD, sem form, sem estrutura mínima de LP.

## Nice-to-haves (opcionais)

- [ ] Se algum evento tiver canal de contato diferente do e-mail (ex.: WhatsApp), o 3º passo precisaria de variante. Hoje a página assume que o e-mail de confirmação aceita resposta.

---

# v2 (2026-10-06) — checks

**Escopo:** novo H1, saiu "O que fazer agora", entraram QUEM SOMOS e CLIENTES.

- **GTM**: `1 OK, 0 aviso(s), 0 bloqueio(s)`.
- **Em-dash**: 0.
- **Fidelidade de copy**: textos visíveis literais de `copy.txt` v2. Número "Mais de 800 empresas no Brasil, LATAM e Portugal" vem literal da `escolha-a-cxpress` (publicada).
- **Preview** 1280px e 375px: todas as imagens carregam, sem scroll horizontal, quem-somos empilha no mobile.
- **Ajuste aplicado**: selo "Um produto Elife" virou texto (o PNG do brand é cinza claro opaco e sumia na pílula lilás).
- **Contraste**: overline em `#B4561A` sobre branco (~4.9:1; o `#EF863C` puro reprova AA); selos navy sobre `#D7E2FF`; botão branco sobre navy.
- O nice-to-have da v1 (variante do 3º passo) deixou de existir junto com a seção.
