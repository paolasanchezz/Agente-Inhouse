# Revisão LP — buzzmonitor/gestao-de-crises

**Data:** 2026-10-02
**Auditores:** design review + Web Interface Guidelines (a11y/HTML), com checagens automáticas: axe-core 4.10 (1440 px e 390 px), `check_gtm_region.py`, `bump_mobile_type.py` + `check_mobile_type.py` (GUIDELINES §20), pacote SEO (§15–§18) e fidelidade de copy contra `copy.txt`.

## Aplicado automaticamente (6 críticos)

- [x] **Pisos de tipografia mobile (GUIDELINES §20)**: corpo, itens de lista e botões estavam em 15–16 px no celular, labels em 12–13 px e 4 títulos com `clamp` abaixo do piso. Rodado `bump_mobile_type.py` (4 clamps + 33 regras) e completado à mão: lead do hero 18 px, botões, cards de benefício, depoimentos e legendas dos big numbers do MCP em 17 px, pílulas (overline do hero, tags REELS/ÁUDIO) em 14 px. `check_mobile_type.py`: H1 34 px, sem overflow novo (o único overflow é o marquee de logos, que é proposital).
- [x] **Contraste do laranja de texto**: `--orange-text` `#b85613` dava 4,48:1 sobre `#f7f7f7` (abaixo de AA nos overlines "IA + Triggers" e "Case E-CLIK"). Trocado por `#a34b10` (5,5:1). Diferença visual mínima.
- [x] **CTA do header quebrando em 2 linhas no celular**: o `white-space:normal` dos botões no mobile vencia o `nowrap` do `.nav__cta`. Corrigido com `!important`; o botão volta a ter uma linha (43 px de altura a 375 px).
- [x] **Área de toque dos ícones sociais do rodapé**: tinham 26 px. No mobile agora são 44×44 px.
- [x] **Meta description com 166 caracteres** (passava do limite de ~160 e seria cortada no Google). Encurtada para 148 caracteres, no `<meta>` e no JSON-LD.
- [x] **Selo de GTM**: `check_gtm_region.py` deu `ok` (GTM-WFJVK858, região brasil). Gravado `.tracking.lock` com `--write-stamp`.

### Checagens que passaram sem ajuste

- Travessão (em-dash): 0 no HTML e no `copy.txt`.
- SEO: description 1, robots 1, `og:` 10, `twitter:` 4, JSON-LD 1 (parseia), canonical 1. LP sem irmãs de idioma, então não precisa de hreflang.
- Logos do header/rodapé: `href` para `https://buzzmonitor.com/` com `target="_blank" rel="noopener"`. SVGs sem `<text>` vivo.
- OG image: `assets/og-gestao-de-crises.png`, 1200×630, sem `og-image.png` duplicado.
- Fidelidade de copy: 101 blocos de texto visível, todos literais do `copy.txt`, exceto itens da whitelist (skip-link, estrelas decorativas) e 2 rótulos de mock agora registrados no `copy.txt` ("Buzzmonitor + IA" e "Alerta via e-mail ou WhatsApp").
- axe-core: nenhuma violação além de contraste (ver decisões abaixo).

## Críticos sinalizados: decisões tomadas (2026-10-02)

Não apliquei porque mexem na identidade visual que você aprovou:

- [x] **MANTIDO por decisão da usuária. Botões laranja com texto branco**: `#EB7C2E` com branco dá **2,81:1**, abaixo do AA (4,5:1). É o mesmo caso da LP de referência e das LPs das dores, já aceito conscientemente antes. Se quiser resolver sem mudar o clima da página: escurecer o fundo dos botões para `#c75300` (4,5:1).
- [x] **APLICADO (#d4691a). Números laranja de "Junte-se a empresas…"** (pedido seu): `#EB7C2E` sobre `#f7f7f7` dá **2,63:1**. Por ser texto grande, o mínimo AA seria 3:1. Para manter o laranja e passar: `#d4691a` (3,36:1), que é o laranja de hover do próprio botão. Diferença visual pequena.

## Melhorias opcionais (5): todas aplicadas a pedido da usuária

- [x] **Uso público do exemplo do report** (liberado pela usuária em 2026-10-02: o report usa dados públicos) (Nike e Seleção Brasileira, no tablet da seção MCP): confirmar que o material pode aparecer em LP pública. Ele cita marcas de terceiros e uma narrativa de crise.
- [x] **Movimento reduzido** (aplicado: destaque do plano de mitigação fixo): para quem desativa animações, o tablet fica parado no topo do report e os 3 destaques não aparecem. Sugestão: nesse modo, mostrar fixo o destaque do plano de mitigação.
- [x] **Formulário sem título próprio** (aplicado: "Experimente agora" no topo do card): desde a troca para o Jotform, o card não tem chamada. Uma linha curta acima do form ajudaria quem chega pelo CTA do topo (por exemplo, voltar o "Experimente agora" que estava na copy).
- [x] **Passo 2 da seção "Saiba da crise antes da diretoria"**: ainda diz "Alerta no seu e-mail", enquanto o benefício e a seção "Sinais de crise" já falam em e-mail e/ou WhatsApp.
- [x] **Faixa de logos no celular** (aplicado: 64 px no mobile): com 90 px de altura, cabem 1 ou 2 logos por vez na tela. Dá para reduzir para ~64 px só no mobile.

## Nice-to-haves (3)

- [ ] O CTA "Agendar demonstração grátis" se repete 8 vezes na página. Um ou dois poderiam variar (por exemplo, "Ver os alertas na prática" no passo a passo).
- [ ] `assets/og-source.html` é publicado junto com a LP. Não faz mal, mas pode ir para fora de `assets/`.
- [ ] O texto do report dentro do tablet é pequeno para ler. Os 3 destaques já resolvem a leitura do que importa; outra opção seria um zoom leve no tablet durante o scroll.

## Próximos passos

- Publicar: `/lp-publicar buzzmonitor gestao-de-crises content.buzzmonitor.com`
