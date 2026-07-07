# Checklist GEO / AEO — blogpost SEO

> GEO = Generative Engine Optimization: ser **citado e extraído** por motores de resposta com IA
> (ChatGPT, Perplexity, Google AI Overviews, Gemini), não só ranquear no SERP clássico.
> Estes são os **gates de aceite** que a skill `/blog-diario` roda contra o post antes de publicar.
> Pareia com `blog-seo-copy.md` (estrutura) e `metadados-seo-spec.md` (campos).

---

## Por que GEO (e por que é diferente de SEO clássico)

SEO clássico otimiza pra um humano clicar num link azul. GEO otimiza pra um LLM **extrair um trecho** e citar a marca como fonte. O que muda na prática:

- O LLM lê em **chunks**: ele pega um parágrafo ou uma resposta de FAQ e usa fora de contexto. Cada trecho precisa ser verdadeiro e completo sozinho.
- O LLM premia **resposta direta + entidade nomeada + dado com fonte**. Texto que enrola antes de responder é descartado.
- **FAQ e definições** são o que mais vira citação — são auto-contidos por natureza.

O post de referência ("Banimento no WhatsApp") já faz isso: lead que responde direto, TOC, H2 em pergunta, FAQ longa, definições ("O banimento no WhatsApp é…").

---

## Gates de aceite (todos obrigatórios)

- [ ] **Resposta-primeiro no lead.** As 2–3 primeiras frases respondem direto à query principal (extraíveis como featured snippet / resposta de IA). Sem "imagine que…", sem rodeio de cenário.
- [ ] **≥2 headings em forma de pergunta.** Pelo menos dois H2/H3 escritos como a pergunta real que a pessoa (ou o LLM) faria — casam com buscas conversacionais.
- [ ] **≥1 frase definicional por conceito-chave.** Padrão "X é …" / "X significa …" logo no início da seção que trata do conceito (entity-defining, o que o LLM cita).
- [ ] **`tldr` com 2–6 bullets autônomos.** Cada bullet verdadeiro fora de contexto (não "veja abaixo"). É o resumo extraível por IA — obrigatório no schema.
- [ ] **FAQ com 3–6 perguntas (H3).** Cada resposta auto-contida, **≤ ~50 palavras**, respondendo a pergunta na primeira frase. Vira FAQPage schema no CMS real.
- [ ] **Entidades nomeadas explicitamente.** Módulos com a **grafia exata** do BRANDBOOK §2; canais reais ("API oficial do WhatsApp", "ChatGPT integrado"); sem pronomes ambíguos ("ela", "isso") onde o sujeito é a entidade. O LLM precisa do nome, não do pronome.
- [ ] **Toda estatística tem fonte externa linkada.** Número/claim → link inline pra fonte de autoridade (ex.: Zendesk CX Trends 2026, que o BRANDBOOK da Cxpress já sanciona). **Nunca inventar dado.** Sem fonte confiável → afirmar qualitativamente, sem número.
- [ ] **Chunks extraíveis.** Parágrafos curtos (2–5 frases), um raciocínio por parágrafo; evitar parágrafos-monstro onde a informação-chave fica enterrada.
- [ ] **TOC presente** ("## O que você vai encontrar neste artigo") — ajuda humano e crawler a mapear a estrutura.
- [ ] **Links internos: 3–8 no corpo + 2–3 em "Leia também"**, todos pra URLs **reais** do inventário; âncora descritiva com a keyword do destino (nunca "clique aqui").
- [ ] **Hierarquia de heading limpa.** Um H1; H2 pras seções; H3 só dentro de H2 longa (>5 parágrafos). Sem pular níveis.
- [ ] **Schema declarado na intenção do frontmatter:** Article + FAQPage (+ BreadcrumbList no CMS). Lembrar: **só vale quando publicado no CMS real**, não no rascunho Notion.

---

## Estrutura que favorece extração (resumo)

```
Lead resposta-primeiro      → featured snippet / resposta de IA
TOC                         → mapa pro crawler
H2 em pergunta + def. "X é" → match de query + citação
parágrafos curtos           → chunks extraíveis
FAQ (H3, resposta ≤50p)     → FAQPage, alta taxa de citação
tldr (frontmatter)          → resumo extraível obrigatório
stats com fonte             → confiança (LLM prefere claim citado)
```

---

## O que NÃO é GEO (não confundir)

- Encher de keyword (keyword stuffing) — o LLM penaliza, não premia.
- FAQ inventada só pra ter schema — perguntas têm que ser as reais (vêm do bake-off / "People Also Ask").
- Dado sem fonte pra "soar autoritário" — destrói confiança e é o oposto de GEO.
- Texto longo por ser longo — profundidade real sim, enchimento não. Ver word count em `blog-seo-copy.md`.

> **Nota de escopo (anti-IA mínimo).** Por decisão do projeto, o blog **não** roda a varredura completa de `regras-anti-ia.md` (em-dash, filler etc. são tolerados). Os gates acima são de **SEO/GEO e precisão factual**, não de estilo anti-IA. A única regra de estilo que permanece é a de precisão: zero stat/case inventado e grafia exata de features.
