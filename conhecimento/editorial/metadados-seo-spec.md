# Spec do bloco METADADOS — SEO ↔ Rank Math ↔ Astro

> Fonte única do **bloco METADADOS** que abre todo blogpost SEO/GEO (skill `/blog-diario`).
> Define cada campo, seu limite de caractere e como ele mapeia para o CMS real (Rank Math/WordPress hoje)
> e para o frontmatter Astro (posting via API no futuro).
> Acompanha: `conhecimento/copywriting/blog-seo-copy.md` (estrutura do artigo) e
> `conhecimento/editorial/geo-checklist.md` (gates GEO).

---

## As duas faces do mesmo metadado

1. **Face humana (Notion):** um bloco `METADADOS SEO` em português, renderizado como callout no topo do rascunho, que o time de SEO lê e cola no Rank Math. É o formato do post de referência ("Banimento no WhatsApp").
2. **Face máquina (artefato local):** o mesmo conteúdo como **frontmatter YAML** no arquivo `blog-seo/{marca}/{regiao}/{DATA}-{slug}.md`, válido contra o schema Astro (`blog/{marca}/src/content.config.ts`) — pronto pra cair em `src/content/blog/{slug}.md` quando o posting via API existir.

A skill gera **as duas** a partir dos mesmos valores. Os limites abaixo valem para ambas.

---

## Bloco METADADOS SEO (face humana — vai no topo do Notion, antes do `---`)

```
**METADADOS SEO**
**Slug:** /kebab-do-post/
**Title tag:** {título SERP, ideal ≤60, máx. 75}
**Title tag alternativo:** {variante curta, ≤65}
**Meta description:** {resumo, 110–165 caracteres}
**Palavra-chave principal:** {keyword vencedora do bake-off}
**Palavras-chave secundárias:** {variação · variação · variação}
**Intenção de busca:** {Informacional|Comercial|Transacional} — {ToFu|MoFu|BoFu}
**Cluster:** {nome do cluster}
**Categoria:** {categoria de menu do cluster}
**Links internos sugeridos:** /slug-real-1/ · /slug-real-2/ · /slug-real-3/
```

---

## Mapa de campos (limites + destino)

| Campo METADADOS | Limite / regra | Rank Math (CMS atual) | Frontmatter Astro (futuro) |
|---|---|---|---|
| **Slug** | kebab-case, minúsculo, sem acento, ≤60 chars | permalink/slug | nome do arquivo `{slug}.md` |
| **Title tag** | ideal ≤60 (Google trunca ~60), **máx. 75** | "Title" (SEO title) | `title` (min 10, **máx 75**) |
| **Title tag alternativo** | **≤65** | OG/A-B title | `metaTitle` (opcional, **máx 65**) — só preencher se ≤65; senão deixar vazio |
| **Meta description** | **110–165** caracteres (inclusivo) | "Description" | `description` (min 110, máx 165) |
| **Palavra-chave principal** | 1 termo | "Focus Keyword" (principal) | 1ª tag (ou tag dedicada) |
| **Palavras-chave secundárias** | `·`-separado, até 5 | Focus Keywords adicionais | demais `tags` (total `tags` ≤6) |
| **Intenção de busca** | enum + estágio de funil | nota interna (não é campo) | — (dirige a lógica de CTA, não vira schema) |
| **Cluster** | nome do cluster do arquivo local | nota interna | — |
| **Categoria** | categoria de menu do cluster | categoria do post | `category` (opcional) |
| **Links internos sugeridos** | `·`-separado, **só slugs reais** (existem no inventário) | links manuais no corpo | links inline no corpo |
| **(GEO) Principais pontos** | 2–6 bullets autônomos | — (vira intro/resumo) | `tldr` (**min 2, máx 6**) — obrigatório no Astro |
| **(GEO) FAQ** | 3–6 pares Q/A | bloco FAQ / schema FAQPage | `faq: [{q,a}]` → FAQPage schema |
| **Autor** | fixo por marca (default `Equipe {Marca}`) | autor do post | `author` |
| **pubDate / updatedDate** | ISO | data de publicação | `pubDate` / `updatedDate` |
| **cover / coverAlt** | path `/assets/...`; `coverAlt` obrigatório SE houver cover | imagem destacada/OG | `cover` / `coverAlt` — **v1 deixa vazio** (capa fora de escopo) |
| **canonical** | URL absoluta (só se republicação) | Canonical URL | `canonical` (opcional) |

---

## Contrato Astro (alvo de validação do artefato local)

Copiado de `blog/buzzcreators/src/content.config.ts` — o `astro build` **falha** se algum obrigatório faltar ou sair do limite. O artefato local deve validar contra isto:

```
title:        string  min 10  max 75            (obrigatório)
metaTitle:    string  max 65                     (opcional)
description:  string  min 110 max 165            (obrigatório)
pubDate:      date                               (obrigatório)
updatedDate:  date                               (opcional)
author:       string  default "Equipe {Marca}"   (default por marca)
tags:         string[] min 1 max 6               (obrigatório)
category:     string                             (opcional)
tldr:         string[] min 2 max 6               (obrigatório — GEO)
faq:          {q,a}[]  default []                (FAQPage schema)
cover:        string startsWith "/assets/"       (opcional; v1 vazio)
coverAlt:     string                             (obrigatório SE cover)
draft:        boolean default false              (rascunho → true)
canonical:    url                                (opcional)
```

> O projeto Astro hoje só existe para `buzzcreators`. Para Cxpress/Buzzmonitor o CMS provável é **WordPress + Rank Math** (o bloco de referência mapeia pra Rank Math). Logo: trate os limites como **guia SEO** e mantenha o frontmatter Astro-válido por garantia — quando o blog de cada marca ganhar projeto Astro próprio, o artefato já encaixa. `draft: true` em todo rascunho gerado.

---

## Decisões de mapeamento (resolver ambiguidades)

- **H1 do artigo = `title` (Title tag).** No post de referência o H1 é igual ao Title tag — mantemos isso por padrão. Se o time quiser um H1 mais "leitor" e um Title tag mais "SERP", o Title tag vive no METADADOS/Rank Math e o H1 no corpo; o `title` do frontmatter segue o Title tag.
- **Title tag alternativo → `metaTitle`** só quando ≤65 chars. O bloco humano sempre mostra o alternativo (é útil pro time); o `metaTitle` do frontmatter fica vazio se o alternativo passar de 65.
- **Autor por marca:** `Equipe Cxpress`, `Equipe Buzzmonitor`, `Equipe Buzzcreators`, `Equipe Elife` (campo "Assinatura" do BRANDBOOK §2). Ajustável se o time definir bylines nominais (E-E-A-T).
- **FAQPage só materializa no CMS real.** No rascunho Notion a FAQ é texto; o schema (rich result + extração por IA) só passa a valer quando publicado no Astro/WordPress. O handoff editorial deixa isso explícito.
- **Links internos = só slugs reais.** Nunca inventar slug. A skill puxa do inventário de posts existentes (cache + sitemap). Slug sugerido pelo cluster que ainda não existe no blog → omitir do bloco (ou marcar `(a criar)`), nunca linkar.
