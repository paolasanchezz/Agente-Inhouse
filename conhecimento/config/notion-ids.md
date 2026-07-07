# Notion IDs — Fonte Unica de Verdade

> Este arquivo e o unico lugar onde IDs de paginas/pastas do Notion ficam hardcoded.
> Qualquer skill que precise publicar no Notion le os IDs daqui.
> Se um ID mudar no workspace, atualizar SO este arquivo.

---

## Paginas raiz por tipo de entrega

| Chave | ID | Uso |
|---|---|---|
| `entregas` | `33b3934026fd80ceb414dd22cb7dbe1f` | Pasta **Entregas** — copy, traducao, landing page, relatorios meta-ads |
| `newsletter` | `33c3934026fd80778073f1868c5bf11c` | Pagina raiz **Newsletter** — publicacoes semanais por marca |
| `redes-sociais` | `3603934026fd8158876dd38d432aceef` | Pagina raiz **Redes Sociais** — planejamentos editoriais mensais (skill social-plan) |
| `redes-sociais-relatorios` | `37d3934026fd81048ee1d3749aa21851` | Subpagina **Relatórios de Performance** — arquivo historico pre-2026-07 (Maio e anteriores). A partir de junho/2026 o relatorio do mes mora dentro da propria pagina-hub do mes, nao mais aqui |
| `seo` | `2b53934026fd8154afeecdc8b68bb0df` | Pagina raiz **SEO** — por marca: clusters, rastreio de paginas e rascunhos de blog (skill blog-diario). Rascunhos vao em `SEO > {Marca} > Conteúdos complementares`. IDs por marca/regiao em `.claude/skills/blog-diario/CONTEXT.md`. |

---

## Padrao de pagina por mes (redes-sociais) — obrigatorio desde 2026-07

**Regra fixa: 1 pagina-hub por mes, nunca mais de uma.** Incidente de 2026-07: rodadas repetidas de `/social-plan` criaram 5 paginas de planejamento diferentes pra junho e 2 pra julho, nenhuma marcada como "a valida" — a Catharina teve que pedir limpeza manual. Pra nao repetir:

1. **Antes de criar qualquer coisa**, rode `notion-fetch` na pagina `redes-sociais` (ID acima) e procure um child page cujo titulo seja **exatamente** o mes/ano (ex: `Julho 2026`).
2. **Se a pagina-hub do mes ja existe**: NAO criar uma nova. Entre nela, ache os children `Planejamento`, `Copies`, `Calendário` (database) e `Relatório de Performance` (quando aplicavel) e **atualize esses em vez de criar novos** (`notion-update-page` com `replace_content`/`update_content`, ou recriar so a database do calendario se o schema mudou — nesse caso mova a nova pra dentro do hub e arquive a antiga movendo pra fora do `redes-sociais` antes, nunca deixando duas soltas no mesmo hub).
3. **Se a pagina-hub nao existe**: crie com `notion-create-pages` (title = `{Mes} {Ano}`, ex: `Julho 2026`, icone 🗓️, parent = `redes-sociais`), depois crie `Planejamento`, `Copies` e a database `📅 Calendário` como children dela (parent = o ID recem-criado do hub, nao mais `redes-sociais` diretamente).
4. **Relatorio de performance** (`social-analytics`): mesma logica — o relatorio do mes vai como child `Relatório de Performance` dentro da pagina-hub daquele mes (nao mais em `redes-sociais-relatorios`). Essa chave antiga so serve pra consultar relatorios de Maio/2026 pra tras.
5. **Mes fechado nao precisa de update automatico** — so mexer se a Catharina pedir explicitamente (ex: reanalise historica).

---

## Como usar nas skills

Sempre que uma skill precisar de um `parent` id para `mcp__*__notion-create-pages`:

1. Leia este arquivo.
2. Selecione a chave apropriada (`entregas` para copy/traducao/LP/meta-ads; `newsletter` para newsletters).
3. Use o valor da coluna ID **exatamente** — sem buscar via `notion-search`, sem hardcode local na skill.

---

## Quem consome

| Skill / CONTEXT | Chave usada |
|---|---|
| `copy-criar`, `copy-revisar` | `entregas` |
| `trad-traduzir`, `trad-revisar`, `trad-pipeline` | `entregas` |
| `lp-preparar`, `lp-publicar` | `entregas` |
| `meta-ads-trends`, `meta-ads-geral` | `entregas` |
| `bunzzai` | `entregas` |
| `news-gerar`, `news-pesquisar`, `news-pipeline` | `newsletter` |
| `social-plan` | `redes-sociais` (via padrao de pagina-hub por mes, ver secao acima) |
| `social-analytics` | `redes-sociais` (relatorio vai dentro do hub do mes; `redes-sociais-relatorios` so pra consulta historica pre-2026-07) |
| `blog-diario` | `seo` |

---

## Quando atualizar

- Pasta do Notion foi movida ou renomeada → atualizar o ID da chave correspondente aqui.
- Nova pasta raiz para outro tipo de entrega (ex: pesquisa, planejamento) → adicionar nova linha na tabela e documentar em "Quem consome".
- Nunca espalhar o ID novamente nas skills — sempre apontar para este arquivo.
