# Revisao LP — buzzcreators/buzzcreators-early-access

**Data:** 2026-11-13
**Auditores:** revisao de design + Web Interface Guidelines (agente independente, sem editar) + checagens deterministicas (GTM, SEO, em-dash, ancora, logo)

## Checagens deterministicas

- GTM (`check_gtm_region.py`): `ok`, regiao `latam`, sem container esperado (`tracking.json` null). Selo `.tracking.lock` gravado.
- SEO: description 1, robots 1, og 10, twitter 4, JSON-LD 1 (parseia), canonical 1. LP unica, sem hreflang.
- Em-dash: 0. Sem JS que grava `#` na URL. Logos SVG referenciados sem `<text>` vivo.
- Fidelidade da copy: todos os textos visiveis vem de `copy.txt` ou da whitelist (labels do form, "Selecciona", nav "Próximamente", footer, skip-link).
- Contraste medido (todos AA): violet/branco 8.0, ink-soft/branco 9.5, rodape 9.5, botao (#3a1652 sobre #ec7c29) 5.3, branco/roxo 14.8.

## Aplicado automaticamente (4 criticos)

- [x] OG image ausente — gerada `assets/og-buzzcreators-early-access.png` (1200×630, 86 KB, Playwright) + `og:image:alt` alinhado ao conteudo da imagem
- [x] Foco invisivel em secao escura — `:focus-visible` violet sobre #3a1652 dava 1.84:1; `.final` e `.footer` agora usam contorno branco
- [x] Borda dos campos do form #e2e8f0 (1.23:1) — trocada por #7b8799 (~3.6:1, WCAG 1.4.11); hover #5d6879
- [x] "Que recibes" usava lista com bolinhas laranja (secao-tipo diferente do outro bloco de beneficios) — agora grid de 2 cards com ✓, igual a "Que es" (§8; 2 itens = 2 cards, §9)

## Melhorias opcionais (6) — aplicadas a pedido do Ulises em 2026-11-13

- [x] Gradiente em 3 lugares — anel do simbolo do hero agora em violet solido; gradiente fica so no traco da pausa e na faixa do CTA final (§1)
- [x] Pilula do header repetia a overline do hero (§3) — trocada para "Lista de espera"
- [x] Overline dividida: espaco real fora do span `aria-hidden` (leitor de tela le "Latinoamérica · Acceso anticipado")
- [x] `.card:hover` removido (cards nao sao clicaveis)
- [x] Form: nota "Todos los campos son obligatorios." + borda de erro com `:user-invalid` + `spellcheck="false"` no e-mail. Ao integrar o embed real, conferir se o embed traz isso proprio
- [x] `.pause` usa `aria-labelledby="pause-title"` no lugar do `aria-label`

## Favicon (2026-11-13, pedido do Ulises)

O `logo-icon.png` do brand (1210x1324, nao quadrado, fundo branco opaco, traco fino) ficava ilegivel na aba (caixa branca com linha roxa quase invisivel). Criado `brand/buzzcreators/assets/logos/favicon-square.png` (512x512, simbolo branco sobre Rich Purple, cantos arredondados, traco engrossado pra ler em 16px) e a LP aponta pra ele. Desvio da GUIDELINES §12 (que manda usar `logo-icon.png`): um link so, PNG do brand, path absoluto no deploy; so muda o arquivo. As outras LPs Buzzcreators seguem no `logo-icon.png` ate alguem decidir trocar.

## Redesign v3 "experiencia" (2026-11-13, pedido do Ulises)

O Ulises achou a versao dark "com cara de LP feita por IA" (vidro, glow, texto em degradê) e pediu algo diferenciado, com mais animacao, otimizado pra celular, copy mais curta e com impacto imediato pra agencias/marcas. Mudou:

- **Copy nova** (`copy.txt`, backup em `copy.txt.2026-11-13_1402.bak`): H1 de dor "Deja de perseguir creadores por WhatsApp.", sub de 1 linha explicando o que e, 4 passos curtos, tabs por perfil (Agencia/Marca/Creador), registro "Entra antes que nadie.", fecho "Tus campañas, por fin en orden.". Textos dos mockups animados tambem estao na copy (fidelidade). Fatos conferidos no BRANDBOOK. Anti-IA: em-dash 0, antitese 1/2.
- **Conceito "del caos al orden"**: no hero, um celular enche de mensagens de campanha no WhatsApp (badge contando) e vira o cartao "Campaña al día" com checks e barra de progresso, em loop so enquanto esta na tela.
- **Experiencia mobile-first**: carrossel deslizavel com scroll-snap e pontos (4 passos, cada um com mini-interface animada que so roda visivel, pra poupar bateria), tabs de perfil com pilula animada e navegacao por setas, CTA fixo no rodape do celular (aparece depois do hero e some quando o form esta na tela), fitas cruzadas em movimento, palavras do H1 subindo + sublinhado desenhado.
- **Visual**: sai vidro/glow; entra tipografia gigante, bloco claro (paper) na secao de perfis pra quebrar o ritmo, form em cartao branco sobre roxo solido com sticker laranja. Degradê preto -> Rich Purple so no hero e no fecho.
- **A11y/robustez**: `prefers-reduced-motion` mostra o estado final sem animar; mockups `aria-hidden`; tabs com roles ARIA; CTA fixo duplicado fora da ordem de tab; sem JS gravando `#`; `noscript` mostra tudo.
- OG image refeita com o H1 novo + celular.

Verificado em Playwright (390×844 e 1440×900): sem overflow horizontal, sem erro de JS, GTM `ok`, JSON-LD valido, 10 og:.

## Redesign "dark premium" (substituido pela v3) (2026-11-13, pedido do Ulises)

O Ulises achou a versao clara generica e pediu algo mais premium/moderno/disruptivo, com o degradê preto -> roxo como identidade da pagina inteira e laranja so como acento. Aplicado:

- Fundo da pagina inteira em degradê `#08040d -> #2a1040 -> #08040d`, auroras roxas por secao, grao sutil, CTA final com degradê preto -> Rich Purple -> Violet e brilho laranja.
- Laranja Sundown so em: botoes, pontos das overlines, checks dos cards, fim do degradê de texto ("correos y chats", "Más tiempo para la idea creativa.", "Tú puedes llegar primero.").
- Form em vidro (glass) com borda em degradê; inputs escuros com borda `rgba(255,255,255,.34)`.
- Ticker decorativo (`aria-hidden`) repetindo literal a overline do hero ("Próximamente en Latinoamérica" / "Acceso anticipado").
- Logo branca (`logo-branca-2.svg`, paths) no header e no rodape; simbolo branco no hero e no CTA final.
- OG image refeita no mesmo estilo.
- Copy intacta (mesmos textos de `copy.txt`), SEO intacto, em-dash 0, JSON-LD ok, GTM `ok`.

**Desvios conscientes das regras (decisao do usuario, validar com o Victor):**
- GUIDELINES §3: hero padrao e fundo branco/neutral. Aqui e escuro.
- GUIDELINES §1 e `generation-rules.json`: gradiente nao deveria ser fundo de secao, e a base da marca e branco/cinza claro (BRANDBOOK §7 "Fazer"). Aqui o degradê e a identidade da pagina.
- §8: a secao escura deixa de ser "uma so"; a pagina toda e escura, o CTA final se destaca pelo degradê mais claro + brilho laranja.

Contraste checado sobre os tons mais claros do fundo: texto principal `#f6f1fb` > 12:1; texto secundario (72%) > 8:1; lilas `#c9b2e6` > 8:1; laranja `#f59a52` do degradê de texto > 5:1; botao (`#08040d` sobre `#ec7c29`) ~ 7.6:1; foco em contorno branco em todas as secoes.

## Nice-to-haves (5)

- [ ] Overline peso 300 a 14px pode ficar fina em tela de baixa densidade — peso 400 no mobile
- [ ] `loading="lazy"` + `decoding="async"` no simbolo do CTA final e no logo do rodape
- [ ] Simbolo do papagaio aparece sem o wordmark (hero e CTA final); o brandbook reserva o icone isolado pra favicon/avatar — validar com o Victor
- [ ] JSON-LD: `@id` usa buzzcreators.com.br e `url` usa buzzcreators.com (heranca do manifest sem `regions`)
- [ ] `id="top"` no header sem uso

## Proximos passos

- Design aprovado? -> `/lp-integrar-form buzzcreators/buzzcreators-early-access "{snippet}"`
- Publicar -> `/lp-publicar buzzcreators buzzcreators-early-access {dominio}` (sugestao: `content.buzzmonitor.com`)
