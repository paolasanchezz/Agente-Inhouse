# Blog cache — Buzzcreators

> Índice cumulativo de posts do blog Buzzcreators, usado para **dedupe** pelas skills `/blog-diario` e `news-*`.
> Disciplina **append-only**: nunca deletar entrada; só acrescentar e atualizar "Última verificação".
> A skill `/blog-diario` adiciona aqui os posts que cria, marcados `status: draft-notion` (troca para `publicado` + URL viva quando o time sobe no CMS).

**Blog:** https://www.buzzcreators.com.br/blog/ · **Última verificação:** 2026-07-02

---

## Estado do inventário (2026-07-02)

**O blog é greenfield — nenhum post publicado.**

- `https://www.buzzcreators.com.br/blog/` retorna **HTTP 404** (a rota de blog ainda não serve listagem/posts).
- O `sitemap.xml` (35 URLs) contém **apenas páginas institucionais, de recurso e de evento** — zero slug de post de blog. Páginas presentes: `/marcas`, `/institucional`, `/escolha-a-buzzcreators`, `/employee-advocacy`, `/agencias`, `/gestao-de-influenciadores`, `/encontrar-influenciadores`, `/creators`, `/creators-pills`, `/creators-research`, `/webinar-buzzcreators-para-influenciadores`, `/webinar-buzzcreators-o-fim-da-burocracia`, + páginas de evento (VTEX 2026, Influent Summit 2026, panorama presencial).

**Implicação para dedupe:** não há posts para colidir. Todo tema do plano editorial é **LACUNA**. A primeira leva de posts define a arquitetura de conteúdo do zero. Ao publicar no CMS, reconciliar este cache com o sitemap vivo.

---

## Posts indexados

| Data | Título (H1) | Slug | Cluster | Funil | Keyword principal | Status | URL |
|---|---|---|---|---|---|---|---|
| _(nenhum ainda — ver plano editorial)_ | | | | | | | |

> Plano dos 20 primeiros: `conhecimento/produto/buzzcreators/seo/plano-editorial-20-artigos.md`
> Arquitetura de clusters (fonte de temas): `conhecimento/produto/buzzcreators/seo/clusters-brasil.md`
