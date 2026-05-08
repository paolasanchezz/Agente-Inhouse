# Relatório — Pipeline Newsletter Semanal 2026-W19
**Data**: 2026-05-08 (v2 — pirâmide invertida aplicada)
**Marca**: Cxpress
**Região**: brasil | **Idioma**: PT-BR

---

## Pipeline executado

- [x] **Etapa 1: Pesquisa** — dores mapeadas, blog indexado, clipping verificado
- [x] **Etapa 2: Pausa de aprovação de pauta** — PULADA (dor escolhida tem cobertura suficiente, ≥3 posts-âncora)
- [x] **Etapa 3: Criação de post de blog** — PULADA (sem lacuna a preencher nesta semana)
- [x] **Etapa 4: Newsletter gerada**
- [x] **Etapa 5: Newsletter revisada** (3 passadas: fact-check, linguagem, otimização)

Tempo aproximado: pesquisa profunda do blog + clipping PR + geração + revisão = pipeline completo numa execução.

---

## Newsletter

| Campo | Valor |
|---|---|
| Edição | 2026-W19 (semana de 04-mai a 10-mai-2026) |
| Assunto | Quando o atendimento trava, o problema é volume ou sistema? |
| Pré-header | Mais atendentes não resolvem um sistema fragmentado. |
| Pergunta-eixo (INTERNA — não visível na NL) | Quando o atendimento da sua empresa trava, o problema é o volume ou o sistema? |
| Posts-âncora | 3 (todos do blog Cxpress) |
| Posts secundários | 1 |
| Clipping PR | 0 |
| Bloco extra | NÃO |
| Total de links contextuais | 4 (≥3 blog próprio ✓ / 3-6 ✓ / ≤1 clipping ✓) |
| Palavras (corpo) | ~175 (≤ 300 ✓) |
| Status | **APROVADA** — v2 com pirâmide invertida aplicada |

### Posts-âncora citados
1. **O problema do atendimento ao cliente não é o volume. É o sistema** (mar/26) — https://blog.cxpress.io/o-problema-do-atendimento-ao-cliente-nao-e-o-volume-e-o-sistema/
2. **Centralização de canais: como organizar WhatsApp, chat e e-mail em um só lugar** (fev/26) — https://blog.cxpress.io/centralizacao-de-canais-otimize-whatsapp-chat-e-email-centralizacao-de-canais/
3. **Como reduzir o tempo médio de atendimento (TMA) sem perder qualidade** (fev/26) — https://blog.cxpress.io/reduzir-tma-melhore-atendimento-satisfacao/

### Posts secundários
4. **Check-list completo para implantar atendimento IA em sua empresa** (fev/26) — https://blog.cxpress.io/implantar-atendimento-ia-em-sua-empresa/
5. **Atendimento remoto e suporte híbrido: tendências em 2026** (fev/26) — https://blog.cxpress.io/atendimento-remoto-e-suporte-hibrido-2026/

### URL Notion (página da edição)
https://www.notion.so/3563934026fd81dc890de4f475b30dac

---

## Post de blog
Não aplicável nesta semana — Etapa 3 (`news-criar-post`) pulada porque a dor escolhida tem cobertura suficiente no blog (≥3 posts).

---

## Pendências

1. **`[VERIFICAR]` URLs de redes sociais no rodapé** — BRANDBOOK confirma existência das contas (LinkedIn, Instagram, Facebook, YouTube) mas não lista os URLs exatos. NL usa estimativas:
   - LinkedIn: `https://www.linkedin.com/company/cxpress/`
   - Instagram: `https://www.instagram.com/cxpress.io/`
   - Site: `https://home.cxpress.io/` (este confirmado)
   - **Ação**: confirmar antes do disparo; se diferentes, atualizar arquivo local + Notion.

2. **Lacuna editorial detectada (não bloqueia esta NL)**: Dor 6 do mapeamento — Voz/PABX/transcrição — tem 0 posts indexados no blog. A Cxpress tem o produto (PABX em nuvem + transcrição lançada em mar/26), mas o blog não comunica essa dor. Recomendação: rodar `/news-pesquisar cxpress brasil` em alguma semana futura instruindo o agente a priorizar a Dor 6 — quando ela virar dor da semana, o pipeline vai gerar `pauta-sugerida.md` automaticamente e a `news-criar-post` cria o draft.

3. **Cases nominais ausentes**: BRANDBOOK §2 marca "Cases de Sucesso Verificados" como "a preencher pelo time com casos reais e métricas verificadas". A NL usa apenas exemplo genérico ("uma clínica com cinco canais"). Quando o time validar cases, a próxima geração pode usá-los.

---

## Notas operacionais

- Primeira execução pós-migração v2.0 — `_state.json` criado nesta semana com 1 pergunta-dor + 5 links registrados (cooldown: 6 semanas para pergunta-dor, 4 semanas para links)
- `blog-cache.md` criado com 26 posts indexados — o cache é cumulativo e não será deletado em execuções futuras
- Arquivos antigos da v1 em `conhecimento/produto/cxpress/pesquisa/` (raiz, não `atual/`) preservados como histórico
- Arquivos antigos da v1 em `newsletter/cxpress/entregas/2026-04/` (5 NLs mensais) preservados como histórico

## Cadência automática (opcional)

Para automatizar a execução semanal desta marca:
- `/loop 7d /news-pipeline cxpress brasil` (modo recorrente in-session)
- ou `/schedule` para criar routine cron remota

Decisão pendente do usuário — pipeline não auto-agenda.

---

## Arquivos gerados nesta execução

### Pesquisa (`conhecimento/produto/cxpress/pesquisa/atual/`)
- `dores-candidatas.md` — 7 dores mapeadas
- `indice-blog.md` — 26 posts indexados
- `dor-semana.md` — dor escolhida + 3 posts-âncora + 2 secundários
- `clipping-pr.md` — sem menções
- `RESUMO.md` — resumo executivo

### Cache cumulativo (`conhecimento/produto/cxpress/`)
- `blog-cache.md` — 26 posts indexados (criado nesta semana)

### Entrega (`newsletter/cxpress/entregas/`)
- `newsletter-2026-W19.md` — newsletter gerada e revisada
- `REVISAO-LOG-2026-W19.md` — log da revisão (3 passadas)
- `RELATORIO-2026-W19.md` — este relatório
- `_state.json` — estado para dedupe de futuras execuções (criado nesta semana)

### Notion
- `[2026-W19] Quando o atendimento trava, o problema é volume ou sistema?` em `Entregas > Newsletter > Cxpress`
- URL: https://www.notion.so/3563934026fd81dc890de4f475b30dac
