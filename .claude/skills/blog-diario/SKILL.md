---
name: blog-diario
description: Gera 1 blogpost SEO/GEO por execucao, de forma autonoma, a partir dos clusters de tema da marca. Faz bake-off de volume de busca multi-fonte (Semrush + fontes gratis), evita duplicar posts existentes, escreve no idioma nativo da regiao, monta bloco METADADOS completo (slug, title, meta description, keywords) e CTA pra modulo+LP em conteudo de meio/fundo de funil, e publica rascunho no Notion. Multi-marca. Pensada pra rodar diariamente via /schedule.
argument-hint: "[marca] [regiao] [tema?]  — ex: cxpress brasil | cxpress brasil \"chatbot whatsapp pequenas empresas\""
allowed-tools: Read, Write, Edit, Bash, WebSearch, WebFetch, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-fetch, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-search, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-create-pages, mcp__051d3b1a-1085-41d4-96c0-ee1719c740c3__notion-update-page, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__get_report_schema, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__execute_report, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__keyword_research, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__organic_research, mcp__ad5dce33-9482-461f-9925-8595fad14e6a__trends_research
version: 1.0.2
---

# Skill: Blogpost SEO/GEO diário (autônomo, multi-marca)

Você é um estrategista de conteúdo SEO + redator. A cada execução, escolhe **autonomamente** o melhor tema dos clusters da marca, escreve **1 blogpost otimizado para busca e para motores de resposta com IA (GEO)** no idioma da região, com bloco METADADOS completo e CTA pra módulo+LP quando o funil pede, e publica como rascunho no Notion. Sem pausa de aprovação — pensada pra rodar diariamente via `/schedule` ou `/loop 1d`.

> **MCP ids variam por ambiente.** Os ids no `allowed-tools` (Notion `051d3b1a`, Semrush `ad5dce33`) são os ativos desta sessão. Confirme os servidores conectados antes de chamar; se diferentes, use os ativos (mesma ressalva do `/seo-report`).

---

## Passo 0 — Parsing & contexto

Leia `.claude/skills/blog-diario/CONTEXT.md` (marcas, regiões, idioma, IDs Notion SEO, pesos de score, database Semrush, UTM, paths).

Parse de `$ARGUMENTS`:
- **Arg 1** (`marca`): `buzzmonitor` | `buzzcreators` | `cxpress` | `elife` — default `cxpress`
- **Arg 2** (`regiao`): `brasil` | `latam` | `portugal` — default `brasil`
- **Arg 3** (`tema`, opcional, entre aspas): força um tema/keyword e **pula a seleção** (Passos 2–4 viram validação leve: confira que o tema cai num cluster da marca; se não cair, registre como tema avulso e siga).

Resolva idioma e pastas de idioma. Calcule `{DATA}` = data de hoje em `YYYY-MM-DD`.

## Passo 1 — Carrega conhecimento + inventário de posts existentes

**Ler arquivos, nunca confiar em memória.**

**Marca/copy:**
1. `brand/{marca}/BRANDBOOK.md` → **NomeDaMarca** ("Nome de exibicao", §2), **BlogURL/SiteURL** da região (§3), **módulos** com grafia exata (§2), **dores/público** (§1), **Diferenciais**, **Cases verificados** (§2 — só usar se citar case nominal), tabela de **grafias INCORRETAS**.
2. `conhecimento/copywriting/blog-seo-copy.md` (estrutura SEO/GEO + postura anti-IA mínimo).
3. `conhecimento/editorial/geo-checklist.md` (gates de aceite GEO).
4. `conhecimento/editorial/metadados-seo-spec.md` (bloco METADADOS + frontmatter + limites).
5. `conhecimento/copywriting/funil-copy.md` (tom por estágio — pra classificar/escrever ToFu/MoFu/BoFu).

**Clusters:**
6. `conhecimento/produto/{marca}/seo/clusters-{regiao}.md`. **Se ausente → PARE:** "Não há clusters para {marca} {regiao}. Peça ao Victor os clusters; eu transcrevo no schema do clusters-brasil.md da Cxpress."

**Catálogo de LP:**
7. `landing-pages/catalogo/lps-{marca}.md` (pode estar em stub vazio → CTAs suaves).

**🔑 Inventário de posts existentes (anti-duplicação) — SEMPRE, antes de qualquer seleção:**
8. Leia `conhecimento/produto/{marca}/blog-cache.md` (índice cumulativo: título, URL, dores cobertas, tags).
9. **Atualize com a realidade de hoje:**
   - `WebFetch` no sitemap vivo: `{BlogURL}sitemap.xml` ou `{BlogURL}sitemap_index.xml` (trate sitemap-index → sitemaps filhos + paginação). Extraia URLs/slugs de posts. Tolere sitemap ausente/bloqueado → caia pro cache.
   - `notion-search` por `Conteúdos complementares` sob `SEO > {NomeDaMarca}` → rascunhos já criados.
   - Leia `posts_criados[]` de `blog-seo/{marca}/_state.json` (se existir).
   - Reconcilie: acrescente ao `blog-cache.md` posts vivos ainda não indexados (entrada nova, "Última verificação" = {DATA}); nunca delete entradas.
10. Resultado: **índice de existentes atualizado** (título + slug + keyword/intenção + dores). É a base de dedupe.

**Gate linguístico:** se `regiao` != `brasil`, LER `conhecimento/linguistico/{pasta-linguistico}/padrao-linguistico.md` (**PARE se não carregar**) + `conhecimento/produto/{marca}/{pasta-produto-lang}/{marca}.md`.

## Passo 2 — Shortlist de candidatos + variações de keyword

(Se `tema` foi passado, pule pra validação leve descrita no Passo 0.)

Dos clusters, monte **3–4 candidatos** de tema:
- Fonte primária: os **"Subtópicos a criar"** de todos os clusters.
- Fonte secundária: qualquer **"Palavra-chave principal"** de cluster que não tenha post correspondente no inventário.

Cada candidato herda: `cluster`, `papel_no_funil`, `prioridade`, `categoria`, `keyword_principal`.

Para CADA candidato, derive **2–3 variações de keyword** cobrindo ângulos/intenções diferentes — head vs long-tail; informacional ("o que é X", "como funciona X") vs comercial ("melhor X", "X preço", "X para pequenas empresas"). Total: ~8–12 termos a testar.

## Passo 3 — Análise de volume multi-fonte (corrobora ou refuta)

Para cada variação, meça demanda cruzando fontes (lógica completa em `blog-seo-copy.md` não — em `CONTEXT.md` e na seção "Seleção" abaixo):

- **Semrush (base):** `get_report_schema` (validar colunas) → `execute_report` (volume `Nq`, dificuldade quando houver) e/ou `keyword_research` pra keywords relacionadas/perguntas (descobre variações novas). `database` conforme região (br · mx · pt). Batche termos quando o report permitir, pra poupar unidades.
- **Complementares grátis:** `WebSearch` pra Google autocomplete / "As pessoas também perguntam" / buscas relacionadas (revela fraseado real e confirma que o termo é buscado); `trends_research` (ou WebSearch no Google Trends) pra interesse relativo; GSC só onde houver credencial (hoje Buzzmonitor BR via `/seo-report`).
- Cada termo recebe: `volume` (número ou estimativa), `fontes_que_confirmam` (lista), `divergencia` (sim/não).
- **Triangulação:** Semrush alto mas autocomplete/Trends/PAA vazios → marque **suspeito** (pondera pra baixo). Semrush baixo/null mas autocomplete forte + PAA + (se houver) impressões GSC → **corrobora** demanda.
- **Degradação:** falha do Semrush (unidades/erro) → as complementares assumem; **nunca aborte**. Cacheie volumes em `_state.json` (TTL ~30 dias).

## Passo 4 — Escolhe o melhor match combinado

Calcule o score por candidato (pesos em `CONTEXT.md`):
```
score = 0.30·volume_validado + 0.25·gap + 0.20·prioridade_cluster + 0.15·relação_produto + 0.10·equilíbrio_funil
```
- `volume_validado`: volume ponderado pela concordância entre fontes.
- `gap`: LACUNA 1.0 / PARCIAL 0.5 / JÁ_COBERTO 0.0 (do dedupe — Passo 5 da seção Seleção).
- `prioridade_cluster`: Alta 1.0 / Média 0.6 / Baixa 0.3.
- `relação_produto`: há módulo/LP claramente conectado? (potencial de conversão).
- `equilíbrio_funil`: puxa o estágio menos coberto nos últimos runs (`_state.json.funnel_balance`).

**Escolha autonomamente 1 candidato + 1 keyword principal vencedora.** As outras variações testadas viram **secundárias** no METADADOS. Guarde a tabela de avaliação (todos os candidatos, volume por fonte, score) — vai no relatório, deixa a escolha auditável.

## Passo 5 — Slug + METADADOS

Gere o **slug**: kebab-case, minúsculo, sem acento, sem caractere especial, ≤60 chars. Cheque colisão contra o inventário (cache + rascunhos Notion); se colidir, é sinal de duplicata → reavalie (escolha o próximo candidato) ou ajuste o ângulo.

Monte o **bloco METADADOS** conforme `metadados-seo-spec.md` (keyword vencedora = principal; variações testadas = secundárias). Valide limites: Title tag ≤~60 (máx 75), alternativo ≤65, meta description 110–165, tags ≤6, tldr 2–6.

## Passo 6 — CTA: módulo + LP

Estágio de funil vem do cluster ("papel no funil" + intenção da keyword):
- **ToFu** → sem CTA duro (link interno suave, sem UTM) ou nenhum.
- **MoFu** → 1 CTA inline após H2 relevante + CTA final, ambos LP + UTM.
- **BoFu** → CTA inline mais direto + CTA final direto, LP + UTM.

Escolha **1 módulo** (grafia exata do BRANDBOOK §2) que resolve a dor do tema. Escolha a **LP** do catálogo por (dor↔cluster) + (estágio↔intenção); sem LP compatível → CTA suave + **flag** no relatório. Monte a UTM: `{LP_URL}?utm_source=blog&utm_campaign={campaign}&utm_content={slug}` (`utm_source=blog` pra todas as marcas; regra em `CONTEXT.md` §Convenção UTM). Respeite o gênero gramatical da marca ("a Cxpress").

## Passo 7 — Escreve o artigo

Siga o esqueleto e as regras de `blog-seo-copy.md` + os gates de `geo-checklist.md`. No **idioma nativo** da região.

Obrigatório:
- Lead **resposta-primeiro** (responde a query nas 2–3 primeiras frases).
- TOC ("## O que você vai encontrar neste artigo").
- H2 em pergunta/definição; 1ª frase de cada H2 responde/define; H3 só em H2 longa.
- **Links internos: 3–8 no corpo + 2–3 em "Leia também"**, SÓ pra URLs reais do inventário (Passo 1). Nunca inventar slug.
- CTA conforme Passo 6.
- **FAQ** (3–6 perguntas em H3, respostas auto-contidas ≤~50 palavras).
- `tldr` 2–6 bullets autônomos.

**Anti-IA mínimo** (decisão do projeto): só **precisão factual** (zero estatística/case/data inventados — stat sempre com fonte externa linkada; case nominal só do BRANDBOOK, senão genérico) + **grafia exata** de marca/features + **correção linguística** regional. NÃO rodar a varredura de em-dash/filler de `regras-anti-ia.md`.

## Passo 8 — Salva artefato local

Salve em `blog-seo/{marca}/{regiao}/{DATA}-{slug}.md`. Se a pasta não existir, crie via Bash (`mkdir -p`). Estrutura:
- **Frontmatter YAML válido pro Astro** (ver `metadados-seo-spec.md`): `title, metaTitle?, description, pubDate: {DATA}, author: "Equipe {NomeDaMarca}", tags, category, tldr, faq, draft: true`.
- **Sem `cover`/`coverAlt`**: a capa (foto Pexels) é gerada na publicação pelo Passo 0.6 da `blog-publicar` (`pexels_cover.py`), que só atua em post sem `cover:` — deixar de fora aqui é o que aciona o fluxo certo lá.
- Em seguida, o **bloco METADADOS** (face humana) como comentário/HTML comment + `---` + o artigo completo em markdown.

## Passo 9 — Publica rascunho no Notion

Estrutura alvo: `SEO > {NomeDaMarca} > Conteúdos complementares > [{DATA}] {H1}`.

1. Leia o ID `seo` em `conhecimento/config/notion-ids.md` e a tabela de IDs SEO em `CONTEXT.md`.
2. Resolva o destino:
   - **Cxpress · BR**: parent = `3803934026fd80baa6c7f54b9809a5b5` (Conteúdos complementares — já mapeado).
   - Outros: `notion-search` por `Conteúdos complementares` sob `SEO > {NomeDaMarca}`; se não existir, crie a subpágina (parent = workspace SEO da marca; se este também não existir, crie sob a raiz `seo`). Registre o ID novo (peça pra anotar no CONTEXT.md).
3. (Opcional) `notion-fetch` em `notion://docs/enhanced-markdown-spec` pra confirmar sintaxe.
4. `notion-create-pages`: parent = destino, title = `[{DATA}] {H1}`, icon = `📝`. Conteúdo:
   - **Callout/quote no topo** com o bloco METADADOS (renderizado, igual ao post de referência).
   - `---`
   - O artigo completo.
5. Anote a URL como `{URL_NOTION}`.

## Passo 10 — Atualiza estado

**`blog-seo/{marca}/_state.json`** (crie se não existir):
```json
{
  "ultima_atualizacao": "{DATA}",
  "posts_criados": [
    { "data": "{DATA}", "slug": "{slug}", "h1": "{H1}", "cluster": "{cluster}",
      "funil": "{ToFu|MoFu|BoFu}", "primary_kw": "{kw}", "volume": 0,
      "url_notion": "{URL_NOTION}", "lp": "{lp-slug|null}", "utm_content": "{slug}",
      "status": "draft-notion" }
  ],
  "temas_rejeitados": [],
  "clusters_cobertura": { "{cluster}": { "posts": 0, "ultimo": "{DATA}" } },
  "funnel_balance": { "ToFu": 0, "MoFu": 0, "BoFu": 0 },
  "volume_cache": { "{termo}": { "volume": 0, "fontes": [], "ts": "{DATA}" } }
}
```
Incremente `clusters_cobertura` e `funnel_balance`. Mantenha só os últimos ~60 dias de `volume_cache`.

**`blog-cache.md`**: acrescente o post novo (URL = `{URL_NOTION}`, marcado `status: draft-notion`). Nunca delete entradas.

## Passo 11 — Relatório

Imprima:
```markdown
## Blogpost criado — {NomeDaMarca} / {regiao}
- **H1**: {H1}
- **Slug**: {slug}
- **Keyword principal**: {kw}  ·  **Volume por fonte**: Semrush {n} · autocomplete {ok/—} · Trends {ok/—} · GSC {n/—}
- **Cluster / Funil / Categoria**: {cluster} / {funil} / {categoria}
- **CTA**: módulo "{modulo}" → LP {lp ou "nenhuma (CTA suave)"} → UTM {utm_content}
- **Links internos**: {n} no corpo + {n} em "Leia também"  ·  **FAQ**: {n} perguntas
- **Arquivo local**: blog-seo/{marca}/{regiao}/{DATA}-{slug}.md
- **Notion**: {URL_NOTION}

### Candidatos avaliados (por que o vencedor ganhou)
| # | Tema | Cluster | Funil | Vol (validado) | Gap | LP match | Score |
|---|------|---------|-------|----------------|-----|----------|-------|
| ... shortlist completa ... |

### Handoff editorial
1. Revisar o rascunho no Notion.
2. Publicar no blog real ({BlogURL}) — o schema FAQPage/Article só passa a valer aí.
3. Trocar a URL Notion pela URL viva no blog-cache.md (status: publicado).
```

---

## Seleção de tema: bake-off + dedupe (detalhe)

**Dedupe (Passo 5 lógico, roda dentro da seleção)** — combina o inventário do Passo 1: sitemap vivo + blog-cache.md + "Subtópicos existentes" dos clusters + rascunhos Notion + `_state.json`. A xlsx "Rastreio de páginas" do Notion é **ignorada** (anexo binário ilegível).

Veredicto por candidato:
- `JÁ_COBERTO`: hit forte (sitemap/cache) com **mesma intenção** → descarte, ou rebaixe pra sugestão "atualizar post existente".
- `PARCIAL`: existe post adjacente, **intenção diferente** (informacional vs comercial coexistem) → mantenha, registre o diferencial.
- `LACUNA`: sem hit → prioridade.

> Compare **intenção**, não só keyword. "o que é chatbot" (informacional, já coberto) não bloqueia "melhor chatbot whatsapp 2026" (comercial, lacuna).

## Regras críticas

- **Autônoma**: nunca pause pra aprovar tema. Escolha pelo score e siga.
- **Só temas dos clusters** (ou o `tema` passado). Nunca inventar pauta fora dos clusters.
- **Nunca duplicar**: se o melhor candidato é `JÁ_COBERTO`, vá pro próximo.
- **Links internos só reais**; nunca forjar slug.
- **Zero stat/case/data inventado**; stat sempre com fonte. Case nominal só do BRANDBOOK.
- **Grafia exata** de marca/features; idioma nativo da região (gate linguístico obrigatório fora do Brasil).
- **Não publica no blog real** — só rascunho no Notion. O schema GEO só materializa quando o time publica no CMS.
- **PARE** se faltar clusters da marca/região, ou se o pilar linguístico não carregar (regiões não-BR).
