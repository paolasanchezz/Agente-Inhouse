# Contexto Compartilhado — news-criar-post

> Esta skill e parte da familia news-*. Para marcas, regioes, caminhos e mapeamento de idioma, ler `.claude/skills/news-pesquisar/CONTEXT.md` (fonte unica da familia).

---

## Especifico desta skill

### Output local
- Path: `newsletter/{brand}/posts-sugeridos/post-{SLUG}-{SEMANA_ISO}.md`
- Sem subpasta por semana — todos os drafts ficam direto na pasta `posts-sugeridos/` de cada marca, identificados pelo slug + semana

### Output Notion
- Hierarquia: `Entregas > Drafts de Blog > {NomeDaMarca} > [{SEMANA_ISO}] {H1}`
- Parent ID raiz: chave `entregas` em `conhecimento/config/notion-ids.md`
- Subpastas (`Drafts de Blog`, `{NomeDaMarca}`) sao criadas pela skill na primeira execucao se nao existirem

### Pre-requisito
- `conhecimento/produto/{brand}/pesquisa/atual/pauta-sugerida.md` deve existir (gerada por `news-pesquisar` quando detecta cobertura insuficiente)
- A pauta deve ter sido aprovada pelo usuario antes da skill rodar (o `news-pipeline` faz a pausa de aprovacao)

### Estado consumido/atualizado
- `newsletter/{brand}/entregas/_state.json`:
  - Adiciona entrada em `pautas_sugeridas_consumidas`
  - Adiciona entrada em `links_usados` (tipo: `post-proprio-novo`)
- `conhecimento/produto/{brand}/pesquisa/atual/dor-semana.md`:
  - Adiciona o novo post como `post-ancora 1`
  - Atualiza status para SUFICIENTE

### Tamanho alvo do post
1500-2500 palavras (do plano de v2.0 da familia news-*)

### Tom e formato
- Edutainment + jornalistico + edutainment (definicao + analogia + exemplo + acao)
- Sem CTA vendedor no final
- Lead jornalistico (sem "imagine que...", sem "vivemos uma era...")

---

## Quando NAO usar esta skill

- Quando o blog ja tem ≥3 posts cobrindo a dor da semana → `news-pesquisar` nao gera `pauta-sugerida.md` e o pipeline pula esta skill
- Quando o usuario rejeita a pauta sugerida → o `news-pipeline` escolhe a proxima dor com cobertura suficiente
- Standalone: tecnicamente possivel rodar `/news-criar-post buzzmonitor brasil` direto, mas requer que `pauta-sugerida.md` exista (caso contrario a skill informa e para)
