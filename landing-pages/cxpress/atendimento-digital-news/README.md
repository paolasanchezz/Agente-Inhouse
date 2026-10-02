# atendimento-digital-news

LP do guarda-chuva **content.cxpress.io** — variante enxuta de [`atendimento-digital`](../atendimento-digital/), criada em 2026-10-02 para trafego de newsletter.

- **Origem:** copia do source de `atendimento-digital` (identico ao que estava no ar em 2026-10-02).
- **Removido:** as secoes "A estrutura que o seu atendimento ganha na plataforma", "Duvidas frequentes", "Quem somos" e o fecho "Seus clientes vao continuar chamando todos os dias...". O CSS dessas secoes e o `<symbol id="ico-wab">` (usado so no selo do Quem somos) sairam junto.
- **Mantido sem alteracao de copy:** hero, clientes, formulario (mesmo Jotform da LP-mae), beneficios e resultados. A pagina termina na secao de resultados, que ja tem CTA.
- **SEO:** `noindex, follow` — o conteudo e um subconjunto da LP-mae (mesmo title/description); indexar as duas canibalizaria a busca. Canonical aponta pra propria URL.
- **OG:** reusa a imagem da LP-mae (`og-atendimento-digital.png`, copia local mantida pro build resolver o asset independente da ordem do manifesto).
- `assets/plataforma/` nao foi copiado (nao era referenciado pelo HTML — ver pendencia no README da LP-mae).

## Secoes de /planos + estilo de /planos — 2026-10-02 (2a passagem)

- **Entraram, abaixo de Resultados:** "Duas formas de contratar. Uma plataforma completa." (cards Basic/Enterprise), "O que entra em cada plano" (tabela comparativa) e "Perguntas frequentes" — HTML e CSS copiados de `planos/` sem alterar copy. O rodape padrao foi trocado pelo rodape de `/planos` (`.k2x-footer`).
- **CTAs:** os `#proposta` de `/planos` apontam para `#agendar` (o form desta LP). O Jotform continua o `261045149477663`.
- **Estilo alinhado a `/planos`:** Open Sans em tudo (+ Inter no rodape; Source Sans 3 e Bitter sairam), corpo `#4a4a4a`, H1 `#4c4848` com a segunda frase em `#4a69bd`, botoes em pilula caixa-alta com brilho (`.pk-btn`), cards com borda azul de 2px e raio 15px, fundo cinza `#f9f9f9`, secao do form em gradiente navy->azul. O laranja/amarelo da marca saiu dos detalhes (pilulas, filete dos stats, foco).
- **Assets novos (copia de `planos/assets/`):** `Group-1707478254.png` (check), `icon-footer-1.png`, `imgi_1_...-1.png` (logo do rodape), `Cxpress_icons_social-scaled.png`. Mesmo nome e mesmos bytes da LP-mae no namespace `/assets/cxpress/`.
- **Script do FAQ:** acordeao de /planos (uma pergunta aberta por vez). Reveal usa a classe `.reveal` desta LP (as `.fade-in` coladas foram renomeadas).
- No mobile o CTA do hero agora quebra linha (`white-space:normal`): em caixa-alta, o texto longo com `nowrap` alargava a coluna e cortava o hero.
