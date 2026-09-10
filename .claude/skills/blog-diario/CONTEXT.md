# Contexto Compartilhado — Blog SEO/GEO (blog-diario)

> Lido pela skill `/blog-diario` antes de qualquer ação. Fonte única de marcas, regiões, idioma,
> IDs Notion SEO, pesos de score, database Semrush e convenção UTM.

---

## Marcas válidas

| Marca | BRANDBOOK | Cache de posts (dedupe) | Catálogo de LP |
|---|---|---|---|
| `buzzmonitor` | `brand/buzzmonitor/BRANDBOOK.md` | `conhecimento/produto/buzzmonitor/blog-cache.md` | `landing-pages/catalogo/lps-buzzmonitor.md` |
| `buzzcreators` | `brand/buzzcreators/BRANDBOOK.md` | `conhecimento/produto/buzzcreators/blog-cache.md` | `landing-pages/catalogo/lps-buzzcreators.md` |
| `cxpress` | `brand/cxpress/BRANDBOOK.md` | `conhecimento/produto/cxpress/blog-cache.md` | `landing-pages/catalogo/lps-cxpress.md` |
| `elife` | `brand/elife/BRANDBOOK.md` | `conhecimento/produto/elife/blog-cache.md` | `landing-pages/catalogo/lps-elife.md` |

Default de marca: `cxpress` (marca-foco do blog SEO hoje). Default de região: `brasil`.

## Regiões e mapeamento de idioma

| Região | Idioma | Nome idioma | Pasta linguístico | Pasta produto lang | Semrush database |
|---|---|---|---|---|---|
| `brasil` | PT-BR | Português Brasileiro | nenhuma | nenhuma | `br` |
| `latam` | ES-LATAM | Español Latinoamericano | `es-latam` | `es` | `mx` (default LATAM) |
| `portugal` | PT-PT | Português Europeu | `pt-portugal` | `pt-pt` | `pt` |

**Gate linguístico (3 pilares — CLAUDE.md):** se `regiao` != `brasil`, LER `conhecimento/linguistico/{pasta-linguistico}/padrao-linguistico.md` (se não carregar, **PARE** — rodar `/trad-calibrar`) + `conhecimento/produto/{marca}/{pasta-produto-lang}/{marca}.md`.

## Clusters (origem dos temas)

| O que | Onde |
|---|---|
| Clusters por marca/região | `conhecimento/produto/{marca}/seo/clusters-{regiao}.md` |

A skill escolhe temas **só daqui**. Se o arquivo não existir para `{marca} {regiao}`, **PARE** e peça ao Victor os clusters (ele envia, o agente transcreve no schema do `clusters-brasil.md` da Cxpress). Hoje pronto: **Cxpress · Brasil** e **Buzzcreators · Brasil** (este último acompanha `seo/plano-editorial-20-artigos.md` com a sequência de lançamento recomendada).

## Caminhos

| O que | Onde |
|---|---|
| Padrão editorial SEO/GEO | `conhecimento/copywriting/blog-seo-copy.md` |
| Checklist GEO | `conhecimento/editorial/geo-checklist.md` |
| Spec do bloco METADADOS | `conhecimento/editorial/metadados-seo-spec.md` |
| Tom por estágio de funil | `conhecimento/copywriting/funil-copy.md` |
| Fundamentos de copy | `conhecimento/copywriting/fundamentos-copy.md` |
| Artefato local (rascunho gerado) | `blog-seo/{marca}/{regiao}/{DATA}-{slug}.md` |
| Estado / anti-repetição | `blog-seo/{marca}/_state.json` |

> O blog-cache.md é **compartilhado** com as skills `news-*` — disciplina append-only: nunca deletar entrada; só acrescentar e atualizar "Última verificação". A skill blog-diario adiciona os posts que cria com `status: draft-notion`.

## Notion — IDs SEO

Raiz lida de `conhecimento/config/notion-ids.md`, chave `seo` (`2b53934026fd8154afeecdc8b68bb0df`). Estrutura: `SEO > {Marca} > Conteúdos complementares > [{DATA}] {H1}`.

| Marca · Região | Workspace SEO da marca | Conteúdos complementares (destino do rascunho) | Status |
|---|---|---|---|
| Cxpress · BR | `36c3934026fd80fd8e80e00ff8ca1456` | `3803934026fd80baa6c7f54b9809a5b5` (Conteúdos complementares) | **pronto** |
| Buzzmonitor · BR | `3803934026fd80afa636d00677b6bc96` | `36c3934026fd8029b511f08eac59c649` (página **"Blog Post"** — Buzzmonitor não usa "Conteúdos complementares") | **pronto** |
| Buzzcreators · BR | `3913934026fd81b4a2ecc500d9860970` (workspace **"Buzzcreators BR"**) | `3913934026fd81dfb24dd9db64f9528f` (Conteúdos complementares) | **pronto** |
| Demais | — | — | descobrir/criar via `notion-search` |

Quando o destino não estiver mapeado: `notion-search` por `Conteúdos complementares` sob `SEO > {NomeDaMarca}`; se não existir, criar a subpágina. Ao confirmar IDs novos, registrar nesta tabela.

> **MCP do Notion:** usar o servidor **ativo da sessão** (`mcp__051d3b1a-…__notion-*`). O id `mcp__d23bd62b-…` que aparece em skills antigas (news-*) está defasado — não copiar. Confirmar o servidor conectado antes de publicar (mesma ressalva do `/seo-report`).

## Blog URLs por marca/região (para crawl do sitemap + links internos)

| Marca | Brasil | LATAM | Portugal |
|---|---|---|---|
| cxpress | https://blog.cxpress.io/ | https://blog.cxpress.io/ | https://blog.cxpress.pt/blog/ |
| buzzmonitor | https://buzzmonitor.com/blog/ | https://buzzmonitor.com/blog/ | https://buzzmonitor.com/blog/ |
| buzzcreators | https://blog.buzzcreators.com.br | https://buzzcreators.com/blog/ | https://buzzcreators.com/blog/ |
| elife | (confirmar) | (confirmar) | (confirmar) |

Fonte canônica: `## 3. URLs e Contatos Oficiais` do BRANDBOOK de cada marca. Sitemap = `{BlogURL}sitemap*.xml` (tratar sitemap-index → filhos + paginação; tolerar ausência → cair pro cache).

## Pesos de score (seleção de tema)

```
score = 0.30·volume_validado + 0.25·gap + 0.20·prioridade_cluster + 0.15·relação_produto + 0.10·equilíbrio_funil
```
- `volume_validado` = volume ponderado pela concordância multi-fonte (Semrush sozinho vale menos que 2-3 fontes concordando).
- `gap` = LACUNA 1.0 · PARCIAL 0.5 · JÁ_COBERTO 0.0.
- `prioridade_cluster` = Alta 1.0 · Média 0.6 · Baixa 0.3.
- `relação_produto` = há módulo/LP claramente conectado? (potencial de conversão).
- `equilíbrio_funil` = puxa o estágio menos coberto nos últimos runs (anti-repetição).

Ajustáveis aqui sem mexer no SKILL.md.

## Convenção UTM

> Regra geral (source = fonte do lead, content = qual conteúdo e tipo de página): `conhecimento/config/convencao-utm.md`. O padrão abaixo é a aplicação dela no blog.

```
{LP_URL}?utm_source=blog&utm_campaign={campaign}&utm_content={slug-do-post}
```
`{campaign}` = token da LP no catálogo; se a LP não definir, usar o slug do tema do post. Exemplo: `utm_source=blog&utm_campaign=banimento-whatsapp&utm_content={slug}`. **`utm_source=blog` vale para TODAS as marcas** — link de conversão comercial sempre `utm_source=blog` + `utm_content={slug-do-post}`; a marca é identificada pelo domínio de destino (padronizado 2026-07-07, antes era `blog-{marca}`).

## Volume de busca — fontes

- **Base:** Semrush MCP (servidor ativo `mcp__ad5dce33-…`): `get_report_schema` → `execute_report`. Volume = `Nq`. Reports de keywords relacionadas/perguntas pra descobrir variações. `database` conforme tabela de regiões.
- **Complementares grátis (cross-check):** Google autocomplete / "As pessoas também perguntam" / buscas relacionadas via `WebSearch`; Google Trends (interesse relativo); GSC (só onde há credencial — hoje Buzzmonitor BR via `/seo-report`).
- **Triangulação:** registrar `fontes_que_confirmam` e `divergência` por termo; penalizar termo sustentado só pelo Semrush. Falha do Semrush → complementares assumem; nunca abortar.
- **Cache:** volumes em `_state.json` com TTL ~30 dias (poupa unidades).
