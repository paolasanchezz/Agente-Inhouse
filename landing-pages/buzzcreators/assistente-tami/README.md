# LP Buzzcreators: assistente-tami

**Gerado em:** 2026-10-07
**Copy-fonte:** `copy.txt` (estruturada no padrão `/lp-preparar`)
**Briefing-fonte:** PDF "Tami, MVP multi-agente de Real-Time Marketing" (9 p.) + `brand/buzzcreators/assistente-tami/BRANDBOOK.md` (BETA)
**Região:** brasil (PT-BR) · **Domínio previsto:** `content.buzzmonitor.com/assistente-tami` (guarda-chuva migrado para o CI, mesmo destino da `encontrar-creators`)
**Funil:** MoFu (produto em beta, captação de interesse qualificado). Formulário na última seção (GUIDELINES §10), com CTA do hero rolando até ele.

## Identidade: sistema "Aurora" (v2, 2026-10-07)

Pedido do Victor: visual mais inovador e moderno, com degradê fluido de roxo, laranja e vermelho, mantendo o Tami com notebook. A versão anterior (editorial clara, "Sinal ao vivo") ficou guardada fora do repo e pode ser recuperada se precisar. Regras completas em `brand/buzzcreators/assistente-tami/BRANDBOOK.md` §9.

- **Aurora (v3, sem círculos):** roxo `#3a1652`/`#6a3895`, laranja `#ff8119` e vermelho `#F05A28`/`#D2401C` sobre a base `#1d0a2b`, em duas camadas:
  - uma malha de faixas diagonais que desliza;
  - fitas longas e irregulares, cada uma com degradê próprio, que mudam de forma devagar.

  A composição põe roxo atrás do Tami e laranja/vermelho escorrendo pelo canto inferior direito. Tem grão sutil por cima.
  - Fica só nos **painéis**: hero, card de destaque do bento e seção Beta.
  - No desktop, uma faixa de luz elíptica segue o cursor no hero.
  - No celular fica só a malha de faixas, para nenhum elemento vazar da tela.
- **Véu de leitura:** escurece o lado do texto, então o branco sempre lê. O H1 usa degradê quente (`#FFD3C2 → #FFB27A`) sobre a aurora.
- **Painéis arredondados** (raio 32px, margem 12px), **nav em pílula de vidro** (transparente com logo branco no hero; vidro claro com logo colorido ao rolar) e **pílula de fluxo** flutuando sobre a borda do hero.
- **Tami com notebook** de pé direto sobre a aurora, só com sombra projetada e um leve flutuar. Na v3 saíram o balão de vidro, o halo e os arcos que ficavam atrás dele.
- **Seções de conteúdo** em branco e off-white, com títulos em degradê (`#6a3895 → #D2401C → #E0661A`, só em título grande), trilho e nós da linha do tempo em degradê, e guardrails em **bento**.
- **Exceções à GUIDELINES**, a pedido do Victor (2026-10-07):
  - §1: degradê como fundo de painel, e mais de um degradê, todos da mesma família.
  - §1/§8: dois painéis escuros (hero e Beta).
  - §3: hero em degradê full-bleed, em vez de fundo branco.
- **Mascote:** Tami, o tamanduá do Buzzmonitor, em asset LP-local (`assets/tami.webp` 797×972 + `tami.png`), copiado de `buzzmonitor/registro-eventos-latam`. É recorte de captura de flyer, sem arquivo original.
- A regra "não misturar a paleta com o Buzzmonitor" (BRANDBOOK Buzzcreators §7) tem **exceção autorizada** para o Tami.

## Estrutura (5 seções, ordem e contagem da copy)

| # | Seção | Blocos | Fundo |
|---|---|---|---|
| 1 | Hero | overline de vidro com ponto ao vivo, H1 de oferta (2ª metade em degradê quente), lead com o que o Tami faz, 2 CTAs (botão branco + link) · Tami direto sobre a aurora + card "Exemplo ilustrativo" com o log de 4 etapas | **painel aurora** |
| n/a | Faixa de fluxo | pílula branca sobre a borda do hero: Buzzmonitor → Triagem → Contato → Negociação → Buzzcreators + "24 horas por dia, 7 dias por semana" | branco |
| 2 | Problema | H2 sticky (2ª frase em degradê) + 5 dores em cartões com X vermelho (§8) + frase de fecho com barra em degradê | branco |
| 3 | Como funciona | H2 + linha do tempo com trilho em degradê que acende na rolagem + 1 artefato por etapa (chips de busca, 4 critérios, canais, medidor de teto, handoff de 5 passos) + legenda | off-white com brilhos desfocados |
| 4 | Guardrails | bento: Teto de budget (destaque em aurora com medidor) + 5 cards + "Depois do beta" | branco |
| 5 | Beta + form | H2 (destaque quente), body, "Faz sentido para você se" em vidro (4 itens) + form branco com barra em degradê e o Tami espiando por trás | **painel aurora** |
| n/a | Footer | logo, copyright, mailto, "Escuta em tempo real com Buzzmonitor" | branco |

## Decisões de copy

- **Hero pela oferta (override da GUIDELINES §3, pedido do Victor em 2026-10-07):** H1 "O assistente de marketing em tempo real que trabalha 24/7 para a sua marca." O lead descreve o que o Tami faz (encontra, seleciona, contata, negocia; o time aprova e libera o pagamento). A dor abre a seção 2 ("O problema"). O H1 anterior, que abria pela dor, ficou registrado no BRANDBOOK como abertura para anúncio ToFu.
- **Bordão:** "Do post ao contrato", tirado do próprio PDF (p. 2). É H2 da seção 3 e headline da OG.
- **Hero mock:** a linha "Contato · mensagem enviada citando o post" deixou de dizer "DM enviada" de propósito. Pela API oficial da Meta, empresa não inicia DM no Instagram nem manda WhatsApp sem opt-in (BRANDBOOK do Tami §10, P1). A etapa 3 continua listando os canais do PDF; **revisar se o produto mudar os canais**.
- **Anti-IA:**
  - em-dash: 0.
  - antítese por negação: 1, literal do PDF.
  - exclamação: 0.
  - listas com 5, 4, 6 e 4 itens.
- **Fidelidade:** todo texto visível vem da `copy.txt`. As exceções são whitelist: skip-link, "Etapa" (sr-only), campos e opções do form e o aviso de consentimento.

## Configuração

- **GTM:** `GTM-WFJVK858`, o container aprovado para `content.buzzmonitor.com`, o mesmo da `encontrar-creators`. `brand/buzzcreators/tracking.json` continua `null`. O gate do CI só avisa e não bloqueia.
- **Form:** mock (`action="#"`) com os campos nome, e-mail corporativo, empresa, cargo, marca/categoria e budget mensal (select). Integrar via `/lp-integrar-form buzzcreators/assistente-tami "<snippet>"` depois de aprovado.
- **SEO:**
  - description (153 caracteres), 10 tags OG, 4 de Twitter.
  - JSON-LD com Organization + WebPage + SoftwareApplication "Tami".
  - Placeholders `{{DOMAIN}}` e `{{OG_IMAGE_PATH}}` são resolvidos no build.
- **OG:** `assets/og-assistente-tami.png` (1200×630), gerada de `og-template-assistente-tami.html` com Playwright, já no visual aurora.

## Validações (2026-10-07)

- [x] `grep —` = 0 e `&mdash;` = 0
- [x] JSON-LD parseia; contagem de SEO ok
- [x] `check_gtm_region.py`: 0 bloqueios (1 aviso esperado: tracking.json null)
- [x] `bump_mobile_type.py` aplicado na v2 (3 clamps + 17 regras). O H2 tem teto de 42px para manter o piso em 28px; o selo Beta tem 14px.
- [x] `check_mobile_type.py`: overflow 0 · H1 34px · corpo 17px · menor fonte 14px
- [x] Console sem erros; assets 200
- [x] Revisão visual da v2 em 1440px e 375px: a primeira dobra fecha com a pílula de fluxo visível; no celular, o Tami fica no topo do visual e o card empilha embaixo. A v3 (fitas sem círculos) foi revisada em 1440px e 375px, com `check_mobile_type.py` limpo.
- [x] Reveal com fallback: classe `.js`, `noscript` e timer de 2,6s. As animações de entrada do hero (texto, Tami, card) usam só `transform` e nunca dependem de opacidade.
- [x] Copy: diff de texto visível × `copy.txt` sem nada fora da whitelist.

## Estado

- [x] Copy estruturada (`copy.txt`)
- [x] HTML gerado e revisado localmente
- [x] OG image 1200×630 → `assets/og-assistente-tami.png`
- [ ] Validar pendência P1 (canais do 1º contato) com Produto e Jurídico **antes de publicar**
- [ ] Formulário real: `/lp-integrar-form buzzcreators/assistente-tami "<snippet>"`
- [ ] Publicar: `/lp-publicar buzzcreators assistente-tami content.buzzmonitor.com` (entra no `manifest.json` do guarda-chuva via PR; o CI deploya)

## Assets referenciados

- `../../brand/buzzcreators/assets/logos/logo-branca-2.svg` (header sobre a aurora e OG; vetor com paths, sem `<text>`, ok pela §19)
- `../../brand/buzzcreators/assets/logos/logo-color.png` (header ao rolar e footer)
- `../../brand/buzzcreators/assets/logos/logo-icon.png` (favicon)
- `./assets/tami.webp` + `./assets/tami.png` (hero e seção Beta)
- `./assets/og-assistente-tami.png` (OG)
