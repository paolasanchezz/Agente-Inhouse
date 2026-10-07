# Dados de Referência — Skill de Vídeo SEO/GEO

> Fonte: documento de referência consolidado pela Bárbara em agosto/2026.
> Atualizar este arquivo sempre que houver mudança de clusters, concorrentes ou escopo.

---

## Marcas e mercados

Duas marcas: **Buzzmonitor** (social listening) e **Cxpress** (atendimento via WhatsApp).
Três mercados cada: **BR**, **PT**, **LATAM** (Espanhol).

Total de combinações ativas: 6.

---

## Clusters de conteúdo por marca e mercado

### Cxpress — os mesmos 4 clusters nas três regiões

| # | Cluster | Funil | Prioridade |
|---|---|---|---|
| 1 | WhatsApp empresarial | Topo e meio | Alta |
| 2 | Atendimento ao cliente via WhatsApp | Topo | Média |
| 3 | Chatbot e automação no WhatsApp | Meio e fundo | Alta |
| 4 | CRM e gestão da experiência do cliente | Meio e fundo | Média |

**Ordem de prioridade para vídeo:** cluster 3 primeiro, depois cluster 1, depois 4 e 2.

### Buzzmonitor BR

1. Social Listening
2. Inteligência Artificial
3. Atendimento ao Cliente
4. Métricas & Analytics
5. Estratégia de Social Media

(Cases de Sucesso, Buzzmonitor na Prática e Institucional ficam fora da rotação automática.)

### Buzzmonitor PT

1. O Que É Social Listening
2. Inteligência Artificial
3. Relacionamento com o Cliente
4. Métricas & Desenvolvimento
5. Estratégia de Social Media

### Buzzmonitor LATAM

1. Qué Es Social Listening
2. Inteligencia Artificial
3. Atención al Cliente
4. Métricas y Performance
5. Estrategia en Social Media

---

## Concorrentes por combinação (para Keyword Gap Tool)

| Combinação | Domínios de concorrentes (máx. 4 por chamada ao Semrush) |
|---|---|
| Buzzmonitor BR | `brandwatch.com` · `sproutsocial.com` · `mention.com` |
| Buzzmonitor PT | `brandwatch.com` · `sprinklr.com` · `sproutsocial.com` · `ocoya.com` |
| Buzzmonitor LATAM | `brandwatch.com` · `sprinklr.com` · `sproutsocial.com` · `ocoya.com` |
| Cxpress BR | `zendesk.com` · `octadesk.com` · `zenvia.com` · `blip.ai` |
| Cxpress PT | `zendesk.com` · `octadesk.com` · `zenvia.com` · `blip.ai` |
| Cxpress LATAM | `zendesk.com` · `octadesk.com` · `zenvia.com` · `blip.ai` |

> `domain_domains` aceita até 5 domínios por chamada (brand + até 4 concorrentes). Socialbee fica fora do top-4 por ser menor — incluir numa segunda chamada se a primeira não gerar candidatos suficientes.

---

## Domínios da marca por combinação (para Keyword Gap)

| Combinação | Domínio da marca |
|---|---|
| Buzzmonitor BR | `buzzmonitor.com` |
| Buzzmonitor PT | `getbuzzmonitor.com/pt/` |
| Buzzmonitor LATAM | `getbuzzmonitor.com/es/` |
| Cxpress BR | `blog.cxpress.io` |
| Cxpress PT | `blog.cxpress.pt` |
| Cxpress LATAM | `blog.cxpress.ai` |

> Cxpress PT tem problema de hreflang ativo (agosto/2026): o blog.cxpress.pt ranqueia no Brasil, não em Portugal. Mencionar essa limitação na justificativa do tema escolhido — a análise de gap ainda é válida, mas os dados de posição atual podem estar distorcidos.

---

## Bases regionais do Semrush (regra fixa)

| Região | Base(s) a usar |
|---|---|
| BR | `br` |
| PT | `pt` |
| LATAM | `mx` (primário) + `es` + `co` — nunca uma única base isolada |

> Para LATAM: rodar Keyword Gap duas vezes (`mx` e `es`), consolidar keywords Missing que aparecem em ambas — são sinal mais forte. Keywords Missing em só uma base entram como secundárias.

---

## Ferramentas do Semrush usadas na Fase 1

- **Keyword Gap** (`domain_domains`, toolkit `competitors_research`): compara domínio da marca com os concorrentes acima, filtra por "Missing" (brand não ranqueia, concorrentes ranqueiam). É o sinal primário de oportunidade.
- **Perguntas relacionadas** (`phrase_questions`, toolkit `keyword_research`): perguntas que o público faz dentro do cluster prioritário — ângulos de conteúdo.
- **Keywords semânticas** (`phrase_related`, toolkit `keyword_research`): termos relacionados à keyword-semente, volume e variações.

**Filtro de SERP Feature = AI Overview:** não disponível via MCP nesta versão. Verificação manual no Semrush UI pela Bárbara para as keywords finalistas de cada combinação. A skill sinaliza quais keywords verificar — não assume o resultado.

---

## Escopo de entrega (definido pelo Victor, agosto/2026)

Meta mensal: **2 vídeos por mês**, em formato longo (horizontal, YouTube) ou curto (vertical, Instagram/TikTok). Cada tema se desdobra em **3 entregáveis**:

1. Vídeo longo para YouTube (horizontal)
2. YouTube Shorts — recorte do vídeo longo
3. Reel — reaproveitado para Instagram, Facebook e TikTok

Cronograma multicanal (carrossel, LinkedIn, TikTok solo, cadência semanal) **não é escopo desta skill**.

---

## Divisão de responsabilidade

A skill entrega o **roteiro-base**: fundação de SEO/GEO que o time de conteúdo adapta para linguagem, tom e produção de cada rede.

Não é responsabilidade da skill: legenda final de rede social, hashtags, indicação de take/corte de câmera, trilha sonora, decisões de edição.

---

## Responsáveis por combinação

| Combinação | Responsável |
|---|---|
| Buzzmonitor BR | Catharina (Cath) |
| Buzzmonitor PT | Catharina (Cath) |
| Buzzmonitor LATAM | Paola |
| Cxpress BR | Marielle |
| Cxpress PT | Marielle |
| Cxpress LATAM | Paola |

---

## Diretrizes GEO/LLM (aplicar em todo o roteiro-base)

- Sem emoji em título ou subtítulo.
- Abrir respondendo diretamente à pergunta central antes de contextualizar.
- Definições isoladas em frase clara e citável.
- Consistência do nome de entidade (marca, produto, termo técnico) ao longo do roteiro.
- Dados numéricos concretos quando existirem.
- Nada de travessão (em dash) no texto.

## Diretrizes específicas de YouTube

- Título deve espelhar como o público de fato pesquisa — não título criativo desconectado da keyword.
- Roteiro falado deve mencionar a keyword-alvo e termos relacionados nos primeiros segundos (YouTube indexa fala via legenda automática).
- Descrição deve aprofundar o tema com keywords relacionadas, não apenas repetir o título.
