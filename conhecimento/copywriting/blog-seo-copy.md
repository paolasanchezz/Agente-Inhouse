# Copy para Blog SEO/GEO (pillar / cluster)

Padrão editorial para **blogpost otimizado para busca e motores de resposta com IA** — o artigo informativo/educativo, ancorado em keyword, que entra na arquitetura de clusters. É o formato da skill `/blog-diario` e do post de referência "Banimento no WhatsApp".

**Pré-requisito:** ler `fundamentos-copy.md` (princípios) e `funil-copy.md` (tom por estágio). Pareia com `conhecimento/editorial/geo-checklist.md` (gates GEO) e `conhecimento/editorial/metadados-seo-spec.md` (bloco METADADOS + frontmatter).

> **Não confundir com `blog-copy.md`.** Aquele é o estilo **notícia/pauta quente** (O que aconteceu → Por que importa → fontes; 600–1000 palavras; produto só na antepenúltima H2; sem METADADOS, sem TOC, sem FAQ). **Este** é o estilo **SEO/GEO**: keyword-anchored, METADADOS-first, resposta-primeiro, FAQ, links internos densos, CTA pra produto/LP no meio e no fim quando o funil pede. São formatos diferentes pra objetivos diferentes — não misturar.

---

## Postura de tom (anti-IA MÍNIMO)

Decisão do projeto: o blog SEO **não** roda a varredura completa de `regras-anti-ia.md`. É texto informativo/educativo, não copy de choque. Em-dash, "além disso", listas de 3 — tolerados se ajudam a clareza. **O que permanece obrigatório:**

1. **Precisão factual** — zero estatística/case/data inventados. Stat sempre com fonte linkada. Case nominal só do BRANDBOOK `### Cases de Sucesso Verificados`; senão, exemplo genérico ("uma rede de clínicas…").
2. **Grafia exata** — features e nome da marca conforme BRANDBOOK §2 + tabela de grafias INCORRETAS (ex.: sempre "a Cxpress", nunca "o Cxpress"; "Centralização de Canais", não "central de canais").
3. **Idioma nativo da região** — PT-BR / PT-PT / ES-LATAM conforme o pilar linguístico. Não é anti-IA, é correção regional (gate separado).

O objetivo é **ser útil e ranquear/ser citado**, não soar provocativo.

---

## Estrutura do artigo

```
[bloco METADADOS]               ← ver metadados-seo-spec.md
---                             ← divisor

# H1  (keyword principal perto do início, ≤~60 chars visíveis)

[Lead resposta-primeiro]
  - 2-3 frases que respondem DIRETO à query principal (extraível p/ snippet/IA)
  - + 1-2 frases de contexto (por que importa, o que o artigo entrega)
  - abertura informativa-neutra OK; pode ancorar em cena/dado se couber

## O que você vai encontrar neste artigo
  - bullets dos H2 seguintes (TOC)

## [H2 — pergunta ou definição]
  - 1ª frase responde direto / define ("X é …")
  - desenvolve em parágrafos curtos (2-5 frases)
  - link(s) interno(s) pra posts reais, âncora descritiva
  - H3 só se a H2 passar de ~5 parágrafos
  [CTA inline — só MoFu/BoFu: 1-2 linhas, módulo + LP + UTM]

## [demais H2 — mistura definicional / como-fazer / comparação conforme a intenção]

## Perguntas frequentes
  ### [pergunta real]?
  [resposta auto-contida, ≤~50 palavras, responde na 1ª frase]
  (3 a 6 perguntas)

## [CTA final]
  - MoFu/BoFu: heading + benefício + LP + UTM
  - ToFu: suave (guia relacionado / newsletter) ou nenhum

**Leia também:** [post real 1] · [post real 2] · [post real 3]
```

---

## Lead — resposta primeiro

A 1ª-2ª frase **responde a pergunta do título**. É o que vira featured snippet e citação de IA.

**Bom (do post de referência):**
> "O banimento no WhatsApp é a suspensão ou desativação permanente de um número pela Meta. Quando acontece, a conta perde acesso imediato a conversas, contatos e histórico — e, em muitos casos, não dá pra recuperar."

Responde "o que é banimento" na 1ª frase, dá a consequência na 2ª. Depois contextualiza (por que importa pra empresa) e diz o que o artigo cobre.

**Evitar:** abrir com cenário genérico ("No mundo do atendimento digital…") ou adiar a resposta pro meio do texto. Em GEO, lead que enrola é descartado.

---

## TOC, H2/H3 e ritmo

- **TOC obrigatório** ("## O que você vai encontrar neste artigo") — lista os H2. Ajuda leitor e crawler.
- **H2 em pergunta/definição** sempre que possível ("Por que o WhatsApp Business comum não é suficiente?", "O que é a API Oficial?"). Casa com busca conversacional.
- **1ª frase de cada H2 responde/define** antes de desenvolver.
- **Parágrafos curtos** (2–5 frases), um raciocínio cada — viram chunks extraíveis.
- **H3 só dentro de H2 longa** (>5 parágrafos). Não fragmentar por padrão.

---

## Links internos

- **Só URLs reais** do inventário (cache de blog + sitemap vivo). Nunca inventar slug.
- **3–8 no corpo** + **2–3 em "Leia também"** ao final.
- **Âncora descritiva** com a keyword do destino: `[WhatsApp Business vs API oficial](url)` > "clique aqui".
- Apontar pra pillar do cluster quando existir (passa autoridade pro hub).
- Slug sugerido pelo cluster que **ainda não existe** → não linkar (ou marcar "(a criar)" no METADADOS), nunca forjar.

---

## CTA + LP por estágio de funil

Estágio vem da "Intenção de busca" do cluster. Detalhe operacional em `funil-copy.md`.

| Funil | CTA inline (meio) | CTA final |
|---|---|---|
| **ToFu** (informacional) | nenhum, ou 1 link interno suave (sem UTM) | suave: guia relacionado / newsletter |
| **MoFu** (comercial) | 1 inline após H2 relevante — módulo + LP + UTM | seção final — módulo + LP + UTM |
| **BoFu** (transacional) | inline mais direto (demo/migração) — LP + UTM | direto ("solicite uma demonstração") — LP + UTM |

**Regras do CTA:**
- **1 módulo por CTA**, nomeado pela grafia exata do BRANDBOOK (Cxpress: *Centralização de Canais · Automação com IA (ChatGPT integrado) · Gestão de Tickets · Dashboards Analíticos · Atendimento por Voz (PABX em nuvem) · Chatbots com Voz Personalizada*). Não empilhar features.
- **LP** escolhida do catálogo (`landing-pages/catalogo/lps-{marca}.md`) por casamento dor↔cluster + estágio↔intenção. Sem LP compatível → CTA suave + flag no relatório (não forçar link de conversão).
- Mesmo no BoFu, **tom informativo** — sem urgência fabricada, sem caps-lock. O post de referência fecha com "Conheça como a Cxpress funciona e solicite uma demonstração gratuita", linkando a LP com UTM.
- Respeitar gênero gramatical ("a Cxpress").

**UTM (mesma string no CTA inline e final):**
```
{LP_URL}?utm_source=blog-{marca}&utm_campaign={campaign}&utm_content={slug-do-post}
```
`{campaign}` = token da LP no catálogo (ou slug do tema, se a LP não definir). Ex. do post de referência:
`https://home.cxpress.io/atendimento-omnicanal-whatsapp?utm_source=blog-cxpress&utm_campaign=banimento-whatsapp&utm_content=banimento-no-whatsapp-por-que-acontece-e-como-evitar-com-a-api-oficial`

---

## Extensão

| Tipo | Palavras | Quando |
|---|---|---|
| Subtópico de cluster | **1200–1800** | padrão diário |
| Pillar page | **1800–2500+** | conteúdo-âncora do cluster (mais raro) |

Profundidade real, não enchimento. Abaixo de ~1000 o tema provavelmente não sustenta um post próprio — considerar reforçar um post existente.

---

## Conexão com produto (quando e como)

Diferente do `blog-copy.md` (produto só no fim), aqui o produto **pode aparecer no meio** quando o funil é MoFu/BoFu — é conteúdo de conversão. Mas:
- Surge **depois** de o artigo ter entregado valor real (definição, comparação, passo-a-passo).
- Conecta a **uma dor concreta** que o módulo resolve, não como "somos a plataforma mais completa".
- Cita 1 módulo + 1 benefício concreto. Se houver case verificado, usar; senão, qualitativo.
- ToFu informacional puro: produto fica de fora (ou menção mínima) — forçar conversão em topo de funil derruba a leitura e o ranking.

---

## Checklist pré-publicação (SEO/GEO)

- [ ] Bloco METADADOS completo e dentro dos limites (`metadados-seo-spec.md`)?
- [ ] Slug kebab ≤60, keyword principal no H1 e no início do lead?
- [ ] Lead responde a query nas 2-3 primeiras frases?
- [ ] TOC presente; ≥2 H2 em forma de pergunta; ≥1 definição "X é…"?
- [ ] FAQ com 3–6 perguntas, respostas ≤~50 palavras, auto-contidas?
- [ ] `tldr` com 2–6 bullets autônomos?
- [ ] 3–8 links internos reais no corpo + 2–3 em "Leia também" (todos existem no inventário)?
- [ ] CTA coerente com o funil (módulo grafia-exata + LP do catálogo + UTM bem-formado)? ToFu sem CTA duro?
- [ ] Toda estatística com fonte linkada; zero dado/case inventado?
- [ ] Grafia exata da marca/features; idioma nativo consistente (PT-BR/PT-PT/ES-LATAM)?
- [ ] Rodou `geo-checklist.md` e todos os gates passaram?
