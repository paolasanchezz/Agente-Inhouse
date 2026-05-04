# Resumo da Pesquisa — Semana 2026-W19
**Marca**: Cxpress | **Região**: brasil | **Idioma**: PT-BR
**Data**: 2026-05-04

## Dor da semana
**Atendimento que não escala — mais gente não resolve um sistema fragmentado**

## Pergunta-eixo
**Quando o atendimento da sua empresa trava, o problema é o volume ou o sistema?**

## Cobertura
- Posts-âncora encontrados: **3** (status: SUFICIENTE)
- Posts secundários: **2** (Check-list IA + Atendimento remoto/híbrido)
- Posts novos adicionados ao cache nesta semana: **26** (primeira execução pós-migração v2.0)

## Clipping PR
- Menções encontradas: **0**
- Bloco "Na imprensa esta semana" NÃO entra nesta edição

## Lacunas detectadas (NÃO geram pauta nesta semana)
- **Dor 6 (Voz / PABX / transcrição)**: 0 posts indexados — lacuna real, mas não é a dor escolhida; vale registrar como **sugestão de pauta futura** quando a dor virar pergunta-eixo. A skill `news-criar-post` pode ser disparada manualmente em outra semana se essa dor for escolhida.
- **Dor 7 (Atendimento remoto/híbrido)**: cobertura baixa (1 post) — pauta de oportunidade.

## Próximas etapas
Cobertura SUFICIENTE — pipeline segue direto para `news-gerar` (sem `pauta-sugerida.md` nesta semana, sem invocação de `news-criar-post`).

## Notas operacionais
- Primeira execução v2.0 — `_state.json` ainda não existe (será criado pelo `news-gerar`)
- `blog-cache.md` será criado nesta execução com os 26 posts indexados
- Arquivos antigos da v1 (`pesquisa/blog-cxpress.md`, `pesquisa/noticias-mercado.md`, `pesquisa/analise-concorrentes.md`, `pesquisa/RESUMO.md`) ficam preservados na raiz da pasta `pesquisa/` como histórico — não foram movidos para `arquivo/` porque não estavam em `pesquisa/atual/` (a Fase 0 só arquiva conteúdo de `atual/`)
