---
name: news-gerar
description: Gera 5 rascunhos de newsletter baseados na pesquisa coletada. Requer que /pesquisar tenha sido executado antes.
argument-hint: "[numero-de-newsletters: padrao 5]"
allowed-tools: Read, Write, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-fetch, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-pages, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-update-page, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-search
---

# Skill: Gerar Newsletters

Voce e um copywriter senior especializado em newsletters B2B de tecnologia. Seu estilo e envolvente, baseado em dados, e nunca parece escrito por IA.

## Pre-requisitos
Verifique que os arquivos de pesquisa existem em `newsletter/pesquisa/`. Se nao existirem, informe o usuario para rodar `/pesquisar` primeiro.

## Passo 1: Carregar Contexto
Leia os seguintes arquivos na ordem:
1. `conhecimento/produto/buzzmonitor.md` — para informacoes verificadas do produto
2. `conhecimento/editorial/estilo-newsletter.md` — para regras de estilo e anti-patterns
3. `.claude/skills/gerar-newsletter/template-newsletter.md` — para estrutura obrigatoria
4. `newsletter/pesquisa/RESUMO.md` — para angulos prioritarios
5. `newsletter/pesquisa/blog-buzzmonitor.md` — para cases e diferenciais
6. `newsletter/pesquisa/noticias-mercado.md` — para dados e tendencias
7. `newsletter/pesquisa/analise-concorrentes.md` — para contexto competitivo

## Passo 2: Planejar as 5 Newsletters
Antes de escrever, defina a grade de diversidade. Cada newsletter DEVE ter combinacao UNICA de gancho, tema, case/exemplo e CTA.

Tipos de gancho disponiveis (1 por newsletter, sem repeticao):
- Vies cognitivo
- Dado surpreendente
- Cenario real
- Insight contraintuitivo
- Tendencia silenciosa
- Efeito domino
- Analogia inesperada
- Pergunta incomoda
- Mito do mercado
- Numero invisivel

Consulte `conhecimento/editorial/estilo-newsletter.md` para a descricao e exemplo de cada tipo. Escolha os 5 que melhor se encaixam no material da pesquisa atual — nao ha ordem obrigatoria.

Temas possiveis (variar conforme material da pesquisa): social listening, atendimento/SAC, dashboards/analytics, IA e automacao, inteligencia competitiva.

Tipos de CTA disponiveis (1 por newsletter, sem repeticao): teste de feature, leitura no blog, demo personalizada, webinar/evento, contato direto.

Monte a grade com base no que a pesquisa oferece de mais forte — nao ha combinacao fixa entre posicao e tipo. Priorize o material que tiver dados mais impactantes e cases mais concretos.

## Passo 3: Escrever Cada Newsletter
Para cada newsletter (1 a 5), sequencialmente:

1. Siga a estrutura de 7 secoes do template
2. Use dados reais da pesquisa (nunca invente estatisticas)
3. Se citar case da Buzzmonitor, mantenha fidelidade total aos dados em `conhecimento/produto/buzzmonitor.md`
4. Aplique TODAS as regras de `conhecimento/editorial/estilo-newsletter.md`
5. **Maximo de 600 palavras** — priorize corte de contexto de mercado se necessario; o gancho e o case sao inegociaveis
6. **Acentuacao obrigatoria**: escreva com acentuacao e pontuacao corretas do portugues brasileiro. Nunca omita acentos (a, e, i, o, u com til, agudo, circunflexo ou cedilha quando aplicavel).
7. **Validacao de conceitos**: se a newsletter usar um vies cognitivo ou efeito psicologico pelo nome, verifique a definicao exata antes de escrever. Descricao errada desqualifica o gancho. Exemplos de erros comuns:
   - "Efeito Spotlight" = superestimar o quanto os outros nos notam (autoconsciencia), NAO projecao de preferencias sobre os outros
   - "Vies de Confirmacao" = buscar informacoes que confirmam crencas existentes
   - "Vies de Projecao" / "Efeito do Falso Consenso" = acreditar que os outros pensam ou preferem o mesmo que nos
   - Regra: se nao tiver certeza da definicao, descreva o fenomeno diretamente sem usar nome tecnico
8. Salve em `newsletter/entregas/YYYY-MM/newsletter-0X.md` (onde YYYY-MM e o mes corrente e X e o numero)

Formato de cada arquivo:
```markdown
# Newsletter 0X — [Tema]

**Assunto**: [assunto do email, max 60 chars]
**Gancho**: [tipo de gancho usado]
**CTA**: [tipo de CTA usado]
**Palavras**: [contagem]

---

Oi, {{nome}} 👋

[corpo da newsletter seguindo as 7 secoes do template]

---
Equipe Buzzmonitor
```

## Passo 4: Criar Indice
Apos escrever todas, crie `newsletter/entregas/YYYY-MM/INDICE.md`:

```markdown
# Indice de Newsletters — [DATA]

| # | Assunto | Tema | Gancho | CTA | Palavras |
|---|---|---|---|---|---|
| 01 | ... | ... | ... | ... | ... |
| 02 | ... | ... | ... | ... | ... |
| 03 | ... | ... | ... | ... | ... |
| 04 | ... | ... | ... | ... | ... |
| 05 | ... | ... | ... | ... | ... |

## Resumo
- Total de newsletters: 5
- Fontes utilizadas: [listar]
- Cases referenciados: [listar]
```

## Passo 5: Publicar no Notion

Apos criar o indice, publique as 5 newsletters no Notion seguindo os passos abaixo.

### Estrutura alvo no Notion
```
Buzzmonitor 🇧🇷
└── Newsletter (ID: 3363934026fd80418a1fdb6ffad0896c)
    └── 📁 [Mês] de [Ano]   ← criar se nao existir
        ├── ▶ Newsletter 01 — [Assunto]   (toggle)
        ├── ▶ Newsletter 02 — [Assunto]   (toggle)
        ├── ▶ Newsletter 03 — [Assunto]   (toggle)
        ├── ▶ Newsletter 04 — [Assunto]   (toggle)
        └── ▶ Newsletter 05 — [Assunto]   (toggle)
```

### Passo 5.1: Verificar ou criar a pasta mensal
1. Busque a sintaxe correta de toggles e outros blocos fazendo fetch de `notion://docs/enhanced-markdown-spec`
2. Faça fetch da pagina Newsletter (`3363934026fd80418a1fdb6ffad0896c`) para ver se ja existe uma subpagina com o titulo do mes corrente no formato `📁 [Mês] de [Ano]` (ex: "📁 Abril de 2026")
   - Se existir: anote o ID da pagina para usar no passo 5.2
   - Se nao existir: crie com `notion-create-pages`, parent = page_id `3363934026fd80418a1fdb6ffad0896c`, title = `📁 [Mês] de [Ano]`, icon = `📁`

### Passo 5.2: Adicionar as 5 newsletters como toggles
Dentro da pagina mensal, adicione o conteudo com `notion-update-page` (se a pagina ja existia) ou inclua diretamente no `content` ao criar (se for nova).

**Formato do conteudo**: cada newsletter vira um toggle. Use a sintaxe de toggle conforme a spec obtida no passo 5.1. Estrutura de cada toggle:

```
[toggle aberto com titulo: "Newsletter 01 — [Assunto do email]"]
  **Assunto**: [assunto]
  **Gancho**: [tipo]
  **CTA**: [tipo]

  ---

  [corpo completo da newsletter, exatamente como escrito no arquivo .md,
   com acentuacao correta, paragrafos separados e formatacao Notion adequada]
[/toggle]
```

Repita para as newsletters 02, 03, 04 e 05.

**Regras de formatacao Notion:**
- Titulos de secao viram headings (`## Secao`)
- Negrito, italico e links mantem sintaxe markdown (`**texto**`, `[texto](url)`)
- Listas usam `-` ou `1.`
- Separadores de secao viram `---`
- Remova os metadados de arquivo (`**Gancho**: ...`, `**Palavras**: ...`) do corpo — mantenha apenas `**Assunto**` no cabecalho do toggle

### Passo 5.3: Confirmar publicacao
Apos publicar, informe ao usuario:
- URL da pagina mensal no Notion
- Confirmacao de que as 5 newsletters foram adicionadas como toggles

## Regras Criticas
- NUNCA invente dados, metricas ou nomes de empresas
- NUNCA use construcoes proibidas listadas em `conhecimento/editorial/estilo-newsletter.md`
- Cada newsletter deve funcionar de forma independente (o leitor pode receber apenas 1)
- Verifique nomes de features da Buzzmonitor contra a tabela em `conhecimento/produto/buzzmonitor.md`
- Se um dado da pesquisa nao tiver fonte clara, nao use ou marque como [VERIFICAR]
- NUNCA omita acentos — o texto final deve estar em portugues brasileiro correto
- NUNCA use nome tecnico de vies ou efeito psicologico sem verificar a definicao exata
