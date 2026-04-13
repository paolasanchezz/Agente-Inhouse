---
name: news-pipeline
description: Executa o pipeline completo de geracao de newsletters — pesquisa, geracao e revisao em sequencia, para a marca e regiao indicadas.
argument-hint: "[brand] [region] [foco-opcional]  — ex: buzzmonitor brasil | cxpress latam 'ia'"
allowed-tools: WebFetch, WebSearch, Read, Write, Edit, Agent, Bash, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-fetch, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-pages, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-update-page, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-search
version: 1.0.0
---

# Skill: Pipeline Completo de Newsletter

Voce e o orquestrador do processo de criacao de newsletters. Execute as 4 etapas abaixo em sequencia, verificando o output de cada uma antes de prosseguir.

## Passo 0: Parsing de Argumentos

Faca o parsing de `$ARGUMENTS`:
- **Argumento 1** (`brand`): `buzzmonitor` | `buzzcreators` | `cxpress` | `elife` — default: `buzzmonitor`
- **Argumento 2** (`region`): `brasil` | `latam` | `portugal` — default: `brasil`
- **Argumento 3** (foco opcional): tema para direcionar a pesquisa

Mapeamento de `region`:
- `brasil` → idioma: PT-BR | nome idioma: "Portugues Brasileiro" | pasta linguistico: nenhuma | pasta produto lang: nenhuma
- `latam` → idioma: ES-LATAM | nome idioma: "Espanol Latinoamericano" | pasta linguistico: `es-latam` | pasta produto lang: `es`
- `portugal` → idioma: PT-PT | nome idioma: "Portugues Europeu" | pasta linguistico: `pt-portugal` | pasta produto lang: `pt-pt`

---

## Etapa 1: Pesquisa

Execute o fluxo completo da skill `/news-pesquisar` com os argumentos `{brand} {region}` (e foco, se fornecido).

Consulte `.claude/skills/news-pesquisar/SKILL.md` e execute todos os passos na integra.

**Checkpoint**: Verificar que os 4 arquivos existem em `conhecimento/produto/{brand}/pesquisa/` (blog, noticias-mercado, analise-concorrentes, RESUMO) antes de continuar.

---

## Etapa 2: Geracao

Execute o fluxo completo da skill `/news-gerar` com os argumentos `{brand} {region}`.

Consulte `.claude/skills/news-gerar/SKILL.md` e execute todos os passos na integra.

**Checkpoint**: Verificar que 5 arquivos de newsletter + INDICE.md existem em `newsletter/{brand}/entregas/YYYY-MM/` e que as newsletters foram publicadas no Notion.

---

## Etapa 3: Revisao

Execute o fluxo completo da skill `/news-revisar` com os argumentos `{brand} {region} todas`.

Consulte `.claude/skills/news-revisar/SKILL.md` e execute todos os passos na integra.

**Checkpoint**: Verificar que REVISAO-LOG.md existe em `newsletter/{brand}/entregas/YYYY-MM/` e que todas as newsletters foram atualizadas.

---

## Etapa 4: Relatorio Final

Crie `newsletter/{brand}/entregas/YYYY-MM/RELATORIO-FINAL.md`:

```markdown
# Relatorio Final — Pipeline de Newsletters
**Data**: [DATA]
**Marca**: {NomeDaMarca}
**Regiao**: {region} | **Idioma**: {idioma}
**Foco**: [tema fornecido via $ARGUMENTS ou "geral"]

## Execucao
- [x] Pesquisa: X posts analisados, Y noticias, Z concorrentes
- [x] Geracao: 5 newsletters criadas em {idioma}
- [x] Revisao: 3 passadas por newsletter

## Newsletters Geradas

| # | Assunto | Tema | Status | Palavras |
|---|---|---|---|---|
| 01 | ... | ... | APROVADA/ATENCAO | ... |
| 02 | ... | ... | APROVADA/ATENCAO | ... |
| 03 | ... | ... | APROVADA/ATENCAO | ... |
| 04 | ... | ... | APROVADA/ATENCAO | ... |
| 05 | ... | ... | APROVADA/ATENCAO | ... |

## Alertas
[Itens que requerem atencao manual do usuario]

## Notion
[URL da pasta mensal publicada]

## Fontes Utilizadas
[Lista de URLs consultadas durante a pesquisa]

## Proximos Passos
- Revisar newsletters marcadas como ATENCAO
- Aprovar assuntos de email
- Agendar envios
```

---

## Notas Importantes
- Se qualquer etapa falhar, PARE e informe o usuario com detalhes do erro
- Nao pule checkpoints — cada etapa depende da anterior
- O processo completo pode levar alguns minutos devido as buscas web
- Se o contexto ficar muito grande, processe as newsletters em lotes de 2-3
