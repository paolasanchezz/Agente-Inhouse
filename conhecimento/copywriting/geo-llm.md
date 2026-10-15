# GEO — Estrutura para Citação por LLMs (AI Overviews, ChatGPT, Perplexity)

Orientações de **estrutura** (não de tom) para tornar um artigo mais citável por buscadores de IA. Complementa `blog-copy.md` — não substitui as regras de título, lead e ritmo de lá, mas adiciona uma camada extra de formatação pensada para extração automática.

**Quando usar:** qualquer artigo de blog SEO/comercial onde a meta declarada inclui aparecer em respostas de IA (AI Overview do Google, ChatGPT, Perplexity, Copilot) — não só ranquear organicamente. Hoje é o caso da skill `blog-criar-artigo` (Buzzmonitor BR).

---

## Por que isso é uma camada separada de SEO tradicional

SEO tradicional otimiza para o rastreador e para o clique (título, meta description, backlinks). GEO ("Generative Engine Optimization") otimiza para a **extração**: um LLM lendo a página precisa conseguir isolar uma frase, um dado ou um bloco e reproduzi-lo como resposta sem precisar reescrever ou interpretar o texto ao redor.

Isso muda a forma de estruturar o corpo, não o que se diz. As duas coisas convivem no mesmo artigo: o texto continua tendo lead, ritmo, transição orgânica (ver `blog-copy.md`) — só que em pontos estratégicos, o artigo passa por um bloco estruturado, autocontido e citável isoladamente.

Score baixo em ferramentas de AI visibility (ex: Semrush) geralmente significa que o conteúdo até responde a pergunta, mas espalha a resposta em vários parágrafos com contexto demais — o LLM não consegue extrair uma frase limpa pra citar.

---

## 1. Resposta direta na abertura (para artigos "o que é X" ou "como fazer X")

Se o tema do artigo é uma pergunta que alguém faria direto pra um assistente de IA ("o que é social listening", "como medir ROI de social media"), o primeiro ou segundo parágrafo deve conter uma definição objetiva **em até 3 frases**, sem depender do parágrafo anterior pra fazer sentido.

**Bom (citável isoladamente):**
> Social listening para e-commerce é o monitoramento contínuo de menções, avaliações e conversas sobre uma loja ou marca nas redes sociais e outros canais públicos. Ele serve para identificar picos de reclamação em datas promocionais, medir a percepção de um lançamento de produto e acompanhar o posicionamento da concorrência em tempo real.

**Ruim (não extraível sem o parágrafo anterior):**
> Como vimos, esse tipo de monitoramento é essencial. Ele funciona de um jeito parecido com o que descrevemos acima, mas aplicado a esse contexto específico.

## 2. Dado ou resultado isolado e citável

Quando o artigo tem um número forte (case, benchmark, estatística), isolar esse número numa frase autônoma — sujeito, ação, resultado, sem depender de contexto:

> A Youse reduziu seu SLA de atendimento de 36 horas para 3 horas utilizando monitoramento em tempo real.

Evitar diluir o dado dentro de um parágrafo longo de transição. Uma frase-resultado por case é suficiente; não é preciso repetir em vários formatos.

## 3. Bloco de definição/fórmula destacado

Fórmulas, metodologias e definições técnicas (ex: cálculo de ROI, cálculo de NPS a partir de menções) ganham mais citação quando aparecem como bloco visualmente isolado — pode ser uma citação em bloco, uma linha destacada ou uma pequena lista — em vez de descritas em prosa corrida.

## 4. Listas numeradas para processo ("como fazer X", "passo a passo")

Sempre que o artigo descreve um processo (configurar algo, responder a uma crise, montar um dashboard), estruturar como lista numerada com uma frase de explicação objetiva por item — não só o título do passo. É o formato mais reaproveitado por IA em respostas de "como fazer".

## 5. Tabela comparativa para "melhor X" / comparativos

Artigos de comparação (ferramentas, categorias, "X vs Y") devem ter uma tabela simples com poucos critérios claros (3-5 linhas), não só texto corrido comparando. Tabelas são o formato mais citado em respostas comparativas de IA — e também as que humanos escaneiam mais rápido.

## 6. Seção de perguntas frequentes (quando fizer sentido)

Para temas com dúvidas recorrentes e específicas (não genéricas), uma seção de FAQ ao final — pergunta como H3, resposta em 1-2 frases autocontidas — aumenta a chance de aparecer em buscas conversacionais. Não forçar FAQ em todo artigo; só quando existem perguntas reais e distintas do corpo do texto. Quando a seção existir, usar **3 perguntas como piso** (não 2) — um FAQ com só 2 itens costuma ler como preenchimento de espaço em vez de cobertura real do tema.

## 7. Resumo executivo no fechamento

Para artigos mais longos ou exploratórios (tendências, panoramas de mercado), fechar com um parágrafo ou lista curta que sintetiza os pontos principais em frases autocontidas — não é o mesmo que o "em resumo" clichê de IA (proibido por `regras-anti-ia.md`); é um bloco deliberado, rotulado ou não, que existe para ser extraído como resumo.

## 8. Subtítulos que espelham perguntas reais

Quando possível, formular H2/H3 como a pergunta que o público de fato faz ("Como funciona X", "Quanto custa X", "X vale a pena para Y") em vez de rótulos vagos ("Considerações finais", "Outros aspectos"). Isso alinha o subtítulo com a query que o LLM está tentando responder.

---

## Como isso convive com as regras de `blog-copy.md`

- Título, lead, ritmo de parágrafo, citação de fontes e anti-padrões continuam valendo (`blog-copy.md` + `conhecimento/editorial/regras-anti-ia.md`).
- A camada GEO desta página é **estrutural**: ela diz onde inserir blocos citáveis (definição, dado, tabela, lista, FAQ, resumo), não como escrever a prosa ao redor deles.
- Um artigo GEO-otimizado ainda deve ler como texto humano e fluido fora desses blocos — a citabilidade vem da estrutura pontual, não de transformar o artigo inteiro numa lista de bullets.

## Checklist de auto-auditoria (rodar antes de publicar)

- [ ] O artigo responde à pergunta central em até 3 frases isoladas, em algum lugar dos 2 primeiros parágrafos?
- [ ] Todo case/estatística forte tem pelo menos 1 frase-resultado autocontida (sujeito + ação + número)?
- [ ] Toda fórmula/metodologia aparece como bloco destacado, não só em prosa?
- [ ] Todo processo/passo-a-passo está em lista numerada com explicação por item?
- [ ] Todo comparativo ("melhor X", "X vs Y") tem tabela com critérios claros?
- [ ] Se o tema tem perguntas recorrentes distintas do corpo, existe uma seção de FAQ?
- [ ] Artigos longos/exploratórios fecham com resumo executivo extraível?
- [ ] Os blocos citáveis continuam entremeados num texto que lê como humano (não virou lista de bullets do início ao fim)?
