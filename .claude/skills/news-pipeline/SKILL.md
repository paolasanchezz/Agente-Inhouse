---
name: news-pipeline
description: Executa o pipeline completo de geracao de newsletters — pesquisa, geracao e revisao em sequencia, para a marca e regiao indicadas.
argument-hint: "[brand] [region] [foco-opcional]  — ex: buzzmonitor brasil | cxpress latam 'ia'"
allowed-tools: WebFetch, WebSearch, Read, Write, Edit, Agent, Bash, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-fetch, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-pages, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-update-page, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-search
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

Execute todas as instrucoes da skill `/news-pesquisar`.

### Fase 1.0: Carregar Contexto e Configuracoes
Leia `conhecimento/produto/{brand}/{brand}.md` para obter: nome de exibicao (`NomeDaMarca`), URL do blog, assinatura.
Leia `conhecimento/produto/{brand}/concorrentes.md` para contexto competitivo.
Se `region` != `brasil`: leia tambem `conhecimento/produto/{brand}/{lang-pasta}/{brand}.md` e `conhecimento/linguistico/{lang-linguistico}/padrao-linguistico.md`.

### Fase 1.1: Arquivar Pesquisa Anterior
Antes de iniciar, verifique se existem arquivos em `conhecimento/produto/{brand}/pesquisa/` (exceto `conhecimento/produto/{brand}/pesquisa/arquivo/`). Se existirem, mova-os para `conhecimento/produto/{brand}/pesquisa/arquivo/YYYY-MM/`.

### Fase 1.2: Blog da Marca → `conhecimento/produto/{brand}/pesquisa/blog-{brand}.md`
- WebFetch na URL do blog extraida de `conhecimento/produto/{brand}/{brand}.md`
- WebFetch nos 5-8 posts mais recentes
- Extrair: titulo, resumo, case, metricas, diferencial, angulo para newsletter
- Se `$ARGUMENTS` incluiu foco tematico, priorize posts relacionados
- Escrever no idioma da regiao

### Fase 1.3: Noticias do Mercado → `conhecimento/produto/{brand}/pesquisa/noticias-mercado.md`
- Ler `## Visao Geral` de `conhecimento/produto/{brand}/{brand}.md` para identificar o setor e posicionamento da marca
- Construir 5 queries combinando: tema principal do produto + tendencias/IA + regiao + 2026
  - Exemplos: "social listening tendencias 2026 brasil" (Buzzmonitor), "atendimento omnichannel tendencias 2026 brasil" (Cxpress), "influencer marketing tendencias 2026 brasil" (Buzzcreators)
  - Se `$ARGUMENTS` incluiu foco tematico, adicionar esse tema as queries
- WebFetch nos 5-6 melhores resultados
- Extrair: dados surpreendentes, tendencias conectadas ao produto e ao mercado da regiao
- Escrever no idioma da regiao

### Fase 1.4: Concorrentes → `conhecimento/produto/{brand}/pesquisa/analise-concorrentes.md`
- WebSearch em 4-5 concorrentes da lista em `conhecimento/produto/{brand}/concorrentes.md` (rotacionar)
- Priorizar concorrentes relevantes para a `{region}`
- Extrair: novidades, posicionamento, gaps vs {NomeDaMarca}
- Escrever no idioma da regiao

### Fase 1.5: Resumo → `conhecimento/produto/{brand}/pesquisa/RESUMO.md`
- Top 5 angulos para newsletters
- Dados mais impactantes
- Temas prioritarios
- Escrever no idioma da regiao

### Fase 1.6: Atualizar Base de Conhecimento do Produto
Apos gravar o RESUMO.md, releia `conhecimento/produto/{brand}/{brand}.md` e `conhecimento/produto/{brand}/concorrentes.md` e aplique via Edit apenas o que mudou:

**Em `{brand}.md`**:
- Se vazio ou com secoes "a preencher": preencha com o que foi descoberto no site/blog (apenas informacoes verificadas)
- Se ja preenchido: adicione novos cases com metricas, novas features mencionadas no blog, correcoes de URL, atualizacoes de posicionamento

**Em `concorrentes.md`**:
- Se vazio: preencha com os concorrentes pesquisados na Fase 3
- Se ja preenchido: adicione novos movimentos de mercado (lancamentos, aquisicoes), novos players encontrados, dados de tendencias atualizados

Regra: nao invente features, cases ou diferenciais. Use apenas o que foi verificado na pesquisa.

**Checkpoint**: Verificar que os 4 arquivos existem em `conhecimento/produto/{brand}/pesquisa/` antes de continuar.

---

## Etapa 2: Geracao

Execute todas as instrucoes da skill `/news-gerar`.

### Passo 2.1: Carregar Contexto (ja carregado na Etapa 1 — reuse)
Confirmar que todos os arquivos de pesquisa existem em `conhecimento/produto/{brand}/pesquisa/`.

### Passo 2.2: Planejar Grade de Diversidade
Definir combinacao unica de gancho + tema + case + CTA para cada newsletter. Ganchos disponiveis: vies cognitivo, dado surpreendente, cenario real, insight contraintuitivo, tendencia silenciosa, efeito domino, analogia inesperada, pergunta incomoda, mito do mercado, numero invisivel. Consulte `conhecimento/editorial/estilo-newsletter.md` para descricao completa de cada tipo.

### Passo 2.3: Escrever 5 Newsletters
Gerar sequencialmente, salvando em `newsletter/{brand}/entregas/YYYY-MM/newsletter-01.md` ate `newsletter-05.md`.
Seguir template de 7 secoes. **Max 600 palavras cada.**
Substituir `[MARCA]` pelo `{NomeDaMarca}` em toda a newsletter.
**Escrever no idioma da regiao**, seguindo o padrao linguistico carregado (se region != brasil).

### Passo 2.4: Criar Indice
Salvar em `newsletter/{brand}/entregas/YYYY-MM/INDICE.md` com marca, regiao e idioma no cabecalho.

### Passo 2.5: Publicar no Notion
Notion Newsletter ID: `33c3934026fd80778073f1868c5bf11c`

1. Busque a sintaxe correta de toggles e outros blocos fazendo fetch de `notion://docs/enhanced-markdown-spec`
2. Localizar ou criar subpasta `{NomeDaMarca}` dentro da pagina Newsletter (icon: 📁, sem emoji no titulo)
3. Localizar ou criar pasta mensal `[Mes] de [Ano] — [IDIOMA-SIGLA]` dentro da subpasta da marca (icon: 📁, sem emoji no titulo)
   - IDIOMA-SIGLA: `PT-BR` | `ES` | `PT-PT`
4. Adicionar as 5 newsletters como toggles dentro da pasta mensal
5. Confirmar URL da pagina publicada

**Checkpoint**: Verificar que 5 arquivos de newsletter + INDICE.md existem em `newsletter/{brand}/entregas/YYYY-MM/` e que as newsletters foram publicadas no Notion.

---

## Etapa 3: Revisao

Execute todas as instrucoes da skill `/news-revisar` com argumento "{brand} {region} todas".

### Passada 3.1: Fact-Check
Verificar nomes, metricas, features contra `conhecimento/produto/{brand}/{brand}.md`.

### Passada 3.2: Estilo e Idioma
Eliminar construcoes proibidas, filler words, padroes IA conforme `conhecimento/editorial/estilo-newsletter.md`.
Se `region` != `brasil`: verificar consistencia de idioma e aplicar regras do padrao linguistico.

### Passada 3.3: Otimizacao
Enxugar texto, verificar fluxo, avaliar gancho e CTA.

Sobrescrever newsletters revisadas. Criar `newsletter/{brand}/entregas/YYYY-MM/REVISAO-LOG.md`.

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
