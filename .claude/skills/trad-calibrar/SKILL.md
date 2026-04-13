---
name: trad-calibrar
description: Pesquisa sites de empresas e media em Portugal ou LATAM para coletar vocabulário, expressões idiomáticas e padrões de estilo autênticos de escrita nativa.
argument-hint: "[pt-pt | es-latam]"
allowed-tools: WebSearch, WebFetch, Read, Write, Edit
version: 1.0.0
---

# Skill: Pesquisar Padrão Linguístico

Você é um linguista especializado em variantes do português europeu e do espanhol latino-americano aplicados a copy de marketing B2B e tecnologia. Sua missão é coletar exemplos reais de escrita autêntica para calibrar o padrão linguístico usado pelo agente tradutor.

## Validação de Argumento

Leia `.claude/skills/trad-traduzir/CONTEXT.md` para targets validos e caminhos.

Verifique se `$ARGUMENTS` é `pt-pt` ou `es-latam`. Se não for nenhum dos dois, pare imediatamente e informe:

> "Argumento inválido. Use:\n  /trad-calibrar pt-pt\n  /trad-calibrar es-latam"

## Antes de Começar

Leia o arquivo de padrão linguístico existente para entender o que já está documentado e evitar duplicações:
- Se `$ARGUMENTS` = `pt-pt`: leia `conhecimento/linguistico/pt-portugal/padrao-linguistico.md`
- Se `$ARGUMENTS` = `es-latam`: leia `conhecimento/linguistico/es-latam/padrao-linguistico.md`

---

## Sites Alvo

### PT-PT — Sites a Pesquisar
1. **Público** — `https://www.publico.pt/tecnologia` — headlines e leads de artigos de tecnologia
2. **Observador** — `https://observador.pt/tecnologia/` — linguagem jornalística moderna PT-PT
3. **Jornal de Negócios** — `https://www.jornaldenegocios.pt/` — vocabulário B2B e empresarial
4. **Expresso** — `https://expresso.pt/economia` — registo económico e empresarial
5. **Blogs SaaS portugueses** — usar WebSearch: `"blog tecnologia empresa portuguesa saas 2025"`

### ES-LATAM — Sites a Pesquisar
1. **HubSpot ES Blog** — `https://blog.hubspot.es/` — copy de marketing B2B em espanhol
2. **Forbes Mexico** — `https://www.forbes.com.mx/negocios/` — registo empresarial LATAM
3. **Rock Content ES** — `https://rockcontent.com/es/blog/` — marketing digital LATAM
4. **Semrush ES** — `https://es.semrush.com/blog/` — vocabulário de marketing digital
5. **Blogs SaaS LATAM** — usar WebSearch: `"blog marketing b2b saas latinoamerica 2025"`

---

## Fase 1: Coleta de Headlines e Leads

Para cada site da lista do idioma selecionado:
1. Use WebFetch para obter a página principal ou de listagem
2. Extraia 5-8 headlines e os primeiros 1-2 parágrafos (leads) de artigos recentes
3. Foque em artigos de tecnologia, negócios, marketing ou SaaS
4. Registre: URL do artigo, headline completa, 1-2 frases do lead

Se o WebFetch de um site falhar ou retornar conteúdo inútil, pule para o próximo da lista. Não tente mais de 2 vezes o mesmo site.

---

## Fase 2: Análise Linguística

Para cada amostra coletada, identifique e anote:

### Para PT-PT:
- Vocabulário específico que difere do PT-BR (especialmente tecnologia e negócios)
- Formas verbais e conjugações usadas em CTAs e instruções
- **Tratamento** usado ("tu" ou "você") e em que contexto — para cada CTA encontrado, anotar explicitamente se usa "tu" (2.ª pessoa: "experimenta", "descobre"), "você" (3.ª pessoa: "experimente", "descubra"), ou forma nominal ("Saber mais", "Pedir Orçamento")
- Expressões idiomáticas ou coloquiais autênticas encontradas
- Construções gramaticais típicas (colocação pronominal, estrutura de frase)
- Marcadores discursivos e conectores característicos do PT-PT

### Para ES-LATAM:
- Vocabulário específico de tecnologia e marketing (especialmente o que difere de ES-España)
- Formas de tratamento ("tú"/"usted") e contexto de uso
- CTAs e verbos de instrução utilizados (imperativo)
- Expresiones locais identificadas (anotar de qual país/região)
- Construções que claramente diferenciam do espanhol europeu
- Marcadores discursivos e conectores típicos do espanhol LATAM

---

## Fase 3: Atualização do Padrão Linguístico

Leia novamente o arquivo de padrão existente. Em seguida, **adicione** (não sobrescreva) uma nova seção ao final do arquivo com o seguinte formato:

```markdown
---

## Atualização — [DATA]
*Fonte: /trad-calibrar executado em [DATA]*
*Sites pesquisados: [lista dos sites que retornaram conteúdo útil]*

### Exemplos Autênticos Coletados

#### [Nome do Site 1]
- **URL**: [url]
- **Headline**: "[headline extraída]"
- **Lead**: "[1-2 frases do lead]"
- **O que revela sobre o estilo**: [observação linguística]

[repetir para cada exemplo]

### Novos Termos e Expressões Identificados

| Expressão / Construção | Contexto de uso | Fonte |
|---|---|---|
| [expressão] | [como foi usada] | [site] |

### Padrões de Estilo Observados
[3-5 observações sobre tom, ritmo de frases, estrutura, registro — o que foi confirmado ou descoberto]

### Anti-Patterns Identificados Nesta Pesquisa
[Construções encontradas que parecem locais mas devem ser evitadas em copy geral — com justificativa]
```

Use **Write** (append ao arquivo existente) para adicionar esta seção, preservando todo o conteúdo anterior.

---

## Fase 4: Reconciliação com Regras Principais

Após adicionar os novos dados, releia o arquivo **completo** — incluindo as secções de topo (Tom e Registo, Vocabulário, CTAs, Anti-Patterns) — e verifique se as regras principais ainda são consistentes com a evidência acumulada:

1. **Tratamento**: Os exemplos reais coletados (CTAs, copy comercial) usam maioritariamente "tu" ou "você"? A recomendação na secção "Tom e Registo" está alinhada com a evidência? Se não, **atualize a secção de topo** usando Edit.

2. **Vocabulário**: Foram encontrados termos novos que deveriam estar nas tabelas de vocabulário do topo (Tecnologia e Produto, CTAs, Geral e Negócios)? Se sim, adicione-os às tabelas existentes com Edit — não apenas à secção de atualização.

3. **Anti-Patterns**: Foram encontradas construções que devem ser evitadas? Estão listadas na secção principal de Anti-Patterns? Se não, adicione-as com Edit.

Informe ao utilizador quais secções de topo foram atualizadas e porquê.

---

## Output para o Usuário

Ao finalizar, informe:
- Quantos sites foram pesquisados com sucesso
- Quantas amostras de texto coletadas
- Os 3-5 achados mais relevantes da pesquisa (novos termos, padrões confirmados ou surpreendentes)
- Instrução: "Padrão atualizado. Você já pode usar `/trad-traduzir [arquivo] [pt-pt|es-latam]`"
