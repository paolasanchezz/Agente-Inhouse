---
name: pipeline
description: Executa o pipeline completo de geracao de newsletters — pesquisa, geracao e revisao em sequencia.
argument-hint: "[foco-opcional: tema para direcionar a pesquisa]"
allowed-tools: WebFetch, WebSearch, Read, Write, Edit, Agent, Bash
---

# Skill: Pipeline Completo de Newsletter

Voce e o orquestrador do processo de criacao de newsletters da Buzzmonitor. Execute as 4 etapas abaixo em sequencia, verificando o output de cada uma antes de prosseguir.

---

## Etapa 1: Pesquisa
Execute todas as instrucoes da skill `/pesquisar`.

Leia `conhecimento/buzzmonitor.md` e `conhecimento/concorrentes.md` para contexto.

### Fase 1.0: Arquivar pesquisa anterior
Antes de iniciar, verifique se existem arquivos em `pesquisa/` (exceto `pesquisa/arquivo/`). Se existirem, mova-os para `pesquisa/arquivo/YYYY-MM/` conforme instrucoes na skill `/pesquisar`.

### Fase 1.1: Blog da Buzzmonitor → `pesquisa/blog-buzzmonitor.md`
- WebFetch em `https://buzzmonitor.com/blog/`
- WebFetch nos 5-8 posts mais recentes
- Extrair: titulo, resumo, case, metricas, diferencial, angulo para newsletter

### Fase 1.2: Noticias do Mercado → `pesquisa/noticias-mercado.md`
- WebSearch: "social listening tendencias 2026", "atendimento ao cliente IA novidades", "social media monitoring news", "customer experience trends 2026"
- WebFetch nos 5-6 melhores resultados
- Extrair: dados surpreendentes, tendencias conectadas ao produto

### Fase 1.3: Concorrentes → `pesquisa/analise-concorrentes.md`
- WebSearch em 4-5 concorrentes (rotacionar da lista em `conhecimento/concorrentes.md`)
- Extrair: novidades, posicionamento, gaps vs Buzzmonitor

### Fase 1.4: Resumo → `pesquisa/RESUMO.md`
- Top 5 angulos para newsletters
- Dados mais impactantes
- Temas prioritarios

**Checkpoint**: Verificar que os 4 arquivos existem em `pesquisa/` antes de continuar.

---

## Etapa 2: Geracao
Execute todas as instrucoes da skill `/gerar-newsletter`.

### Passo 2.1: Carregar Contexto
Leia na ordem: `conhecimento/buzzmonitor.md`, `conhecimento/estilo-newsletter.md`, `.claude/skills/gerar-newsletter/template-newsletter.md`, e todos os arquivos em `pesquisa/`.

### Passo 2.2: Planejar Grade de Diversidade
Definir combinacao unica de gancho + tema + case + CTA para cada newsletter. Ganchos disponiveis: vies cognitivo, dado surpreendente, cenario real, insight contraintuitivo, tendencia silenciosa, efeito domino, analogia inesperada, pergunta incomoda, mito do mercado, numero invisivel. Consulte `conhecimento/estilo-newsletter.md` para descricao completa de cada tipo.

### Passo 2.3: Escrever 5 Newsletters
Gerar sequencialmente, salvando em `newsletters/YYYY-MM/newsletter-01.md` ate `newsletter-05.md` (onde YYYY-MM e o mes corrente).
Seguir template de 7 secoes. **Max 600 palavras cada.**

### Passo 2.4: Criar Indice
Salvar em `newsletters/YYYY-MM/INDICE.md`.

### Passo 2.5: Publicar no Notion
Executar o Passo 5 da skill `/gerar-newsletter`:
- Verificar ou criar a pasta mensal `📁 [Mês] de [Ano]` dentro da pagina Newsletter no Notion (ID: `3363934026fd80418a1fdb6ffad0896c`)
- Adicionar as 5 newsletters como toggles dentro da pasta mensal
- Confirmar URL da pagina publicada

**Checkpoint**: Verificar que 5 arquivos de newsletter + INDICE.md existem em `newsletters/YYYY-MM/` e que as newsletters foram publicadas no Notion.

---

## Etapa 3: Revisao
Execute todas as instrucoes da skill `/revisar` com argumento "todas".

### Passada 3.1: Fact-Check
Verificar nomes, metricas, features contra `conhecimento/buzzmonitor.md`.

### Passada 3.2: Estilo
Eliminar construcoes proibidas, filler words, padroes IA conforme `conhecimento/estilo-newsletter.md`.

### Passada 3.3: Otimizacao
Enxugar texto, verificar fluxo, avaliar gancho e CTA.

Sobrescrever newsletters revisadas. Criar `newsletters/YYYY-MM/REVISAO-LOG.md`.

**Checkpoint**: Verificar que REVISAO-LOG.md existe em `newsletters/YYYY-MM/` e que todas as newsletters foram atualizadas.

---

## Etapa 4: Relatorio Final
Crie `newsletters/YYYY-MM/RELATORIO-FINAL.md`:

```markdown
# Relatorio Final — Pipeline de Newsletters
**Data**: [DATA]
**Foco**: [tema fornecido via $ARGUMENTS ou "geral"]

## Execucao
- [x] Pesquisa: X posts analisados, Y noticias, Z concorrentes
- [x] Geracao: 5 newsletters criadas
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
