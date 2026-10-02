# atendimento-digital-news

LP do guarda-chuva **content.cxpress.io** — variante enxuta de [`atendimento-digital`](../atendimento-digital/), criada em 2026-10-02 para trafego de newsletter.

- **Origem:** copia do source de `atendimento-digital` (identico ao que estava no ar em 2026-10-02).
- **Removido:** as secoes "A estrutura que o seu atendimento ganha na plataforma", "Duvidas frequentes", "Quem somos" e o fecho "Seus clientes vao continuar chamando todos os dias...". O CSS dessas secoes e o `<symbol id="ico-wab">` (usado so no selo do Quem somos) sairam junto.
- **Mantido sem alteracao de copy:** hero, clientes, formulario (mesmo Jotform da LP-mae), beneficios e resultados. A pagina termina na secao de resultados, que ja tem CTA.
- **SEO:** `noindex, follow` — o conteudo e um subconjunto da LP-mae (mesmo title/description); indexar as duas canibalizaria a busca. Canonical aponta pra propria URL.
- **OG:** reusa a imagem da LP-mae (`og-atendimento-digital.png`, copia local mantida pro build resolver o asset independente da ordem do manifesto).
- `assets/plataforma/` nao foi copiado (nao era referenciado pelo HTML — ver pendencia no README da LP-mae).
