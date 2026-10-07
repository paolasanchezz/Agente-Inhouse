# Clusters de conteúdo — Buzzmonitor · Brasil (PT-BR)

> Lido por `/blog-criar-artigo` (consumidor principal desde 2026-07-24) e, historicamente, por `/blog-diario`. **Fonte de verdade dos temas/clusters da marca.**
> Atualizado em 2026-07-24 com o mapa de clusters mais completo da Barbara (dados de SERP/competitivos, CTR, formato esperado por cluster). Mantido pelo time — reabastecer/atualizar quando houver dado novo.
>
> **Blog:** https://buzzmonitor.com/blog/
> **Schema por cluster:** nome · papel no funil · prioridade · observações de SERP/competitivas · foco/formato esperado.

---

## Nota sobre uso por skill

- **`/blog-criar-artigo`** (ativa): quando a Barbara pedir "escolhe você o tema", a skill escolhe entre os clusters **em rotação** (abaixo), cruzando com `blog-cache.md` + crawl do sitemap real + histórico de clusters já usados no `_state.json` — pra não repetir o mesmo cluster sequencialmente. Também aceita tema trazido diretamente pela Barbara, dentro ou fora dos clusters listados aqui.
- **`/blog-diario`**: decisão de 2026-07-23 (Barbara) — não usar mais para Buzzmonitor BR; a `/blog-criar-artigo` cobre esse papel agora. Este arquivo permanece como registro/schema caso a `/blog-diario` volte a servir Cxpress/Buzzcreators (marcas onde ela continua ativa, sem alteração).

## Clusters fora de rotação (nunca escolher automaticamente, em nenhuma skill)

Feitos por outro time — só entram como peça avulsa se a Barbara trouxer o tema/case específico diretamente, nunca por seleção automática.

- **Cases de Sucesso** — prioridade máxima de conversão (50% de conversão de leads orgânicos justifica o investimento). Formato padronizado: problema → solução → resultado com números.
- **Buzzmonitor na Prática** — tutoriais e how-tos da plataforma, pra resolver sub-utilização (4 posts identificados). CTA direto para trial — conteúdo de ativação/retenção, não de aquisição orgânica.

## Cluster: Institucional
- **Papel no funil:** N/A — não é conteúdo de aquisição orgânica
- **Prioridade:** Baixa — não priorizado para SEO orgânico
- **Foco:** novidades de produto e marca; público-alvo é a base de clientes existente e CRM, não busca orgânica
- Disponível se a Barbara trouxer o tema diretamente. A skill não deve escolher este cluster sozinha quando pedido "escolhe você" — não serve o objetivo de SEO da skill.

---

## Cluster 1 — Social Listening
- **Papel no funil:** Fundo (decisão de compra)
- **Prioridade:** Alta — maior cluster de tráfego
- **Keywords comerciais:** "ferramentas de social listening" (#1 no Semrush), "melhores ferramentas [de social listening]"
- **Foco/formato esperado:** conteúdo de decisão de compra (comparativos, "melhor ferramenta de X")
- **Subtópico já existente no blog:** "melhores ferramentas de social listening 2026" (ranqueia pos. 1 no Semrush) — **atualizar com dados novos, não recriar**. Tratar como JÁ_COBERTO → sugerir atualização do post existente, nunca duplicata.

## Cluster 2 — Inteligência Artificial
- **Papel no funil:** Meio (comercial)
- **Prioridade:** Alta — AI Overview presente em várias SERPs estratégicas
- **Foco:** IA aplicada a resultado de negócio (SLA, produtividade, automação)
- **Tom:** técnico
- **Observação:** boa oportunidade de GEO (AI Overview já aparece nessas buscas) — usar dados próprios da Buzzmonitor quando possível

## Cluster 3 — Atendimento ao Cliente
- **Papel no funil:** Meio (comercial)
- **Prioridade:** Alta — "SAC 2.0" rankeia #1
- **Foco/formato esperado:** conteúdo orientado a decisão — comparativos de ferramentas, guias de implementação
- **Prova social:** cases com dados duros — **só citar case nominal se estiver em `brand/buzzmonitor/BRANDBOOK.md` § Cases Verificados**; senão, usar qualitativo e sinalizar a pendência no relatório

## Cluster 4 — Métricas & Analytics
- **Papel no funil:** Fundo (decisão de compra)
- **Prioridade:** Alta — CTR médio-alto
- **Foco:** engajamento + dashboards + relatórios
- **Foco/formato esperado:** "como medir X" e "quais métricas acompanhar"

## Cluster 5 — Estratégia de Social Media
- **Papel no funil:** Meio
- **Prioridade:** Alta — absorve o catch-all de "Análises e insights"
- **Foco:** planejamento estratégico, benchmarking e tomada de decisão com dados

---

## Histórico — lote de junho/2026 (já executado, referência apenas — não é fila viva)

Os itens abaixo vieram do slide "BR · Artigos Prioritários — Foco: Converter" (junho 2026) e já foram escritos e publicados como draft pela `/blog-criar-artigo` (dentro do briefing `2026-07-artigos-prioritarios-br.md`, hoje encerrado — ver nota em `.claude/skills/blog-criar-artigo/CONTEXT.md`).

| Categoria | Keyword / Tema | Intenção | Status |
|---|---|---|---|
| Social Listening | social listening para e-commerce | Comercial | Escrito (item 01) |
| Social Listening | melhores ferramentas de social listening 2026 | Comercial | Não escrito — tratar como "atualizar existente" (ver Cluster 1), não criar |
| Métricas & Analytics | como medir ROI de social media | Comercial | Escrito (item 03) |
| Atendimento ao Cliente | como reduzir SLA no atendimento digital | Comercial | Escrito (item 05) |
| IA | IA para atendimento ao cliente: guia completo | Comercial | Escrito (item 08) |
| Estratégia Social Media | benchmarking de social media: como fazer | Informacional | Escrito (item 16) |

## Flags gerais (válidas pra qualquer skill que ler este arquivo)

- **Cases nominais (Turbi, Youse, etc.):** citar número exato só se verificado em `brand/buzzmonitor/BRANDBOOK.md` § Cases Verificados. Se não estiver lá, usar qualitativo e sinalizar a pendência no relatório final.
- **"Atualizar artigo existente"** (ex: melhores ferramentas de social listening): tratar como `JÁ_COBERTO` → sugestão de atualização do post existente, nunca criar duplicata.
- **CTA de trial:** confirmar a URL do trial/demo em `landing-pages/catalogo/lps-buzzmonitor.md` antes de usar como CTA — se ainda for stub, usar CTA suave.
