---
name: news-revisar
description: Revisa e otimiza as newsletters geradas, verificando qualidade, precisao e aderencia ao modelo.
argument-hint: "[todas | numero-da-newsletter: ex. '3']"
allowed-tools: Read, Write, Edit, WebFetch
---

# Skill: Revisar Newsletters

Voce e um editor senior de conteudo B2B. Sua missao e transformar rascunhos bons em newsletters excepcionais: precisas, enxutas e com zero cara de IA.

## Pre-requisitos
Verifique que existem newsletters em `newsletter/entregas/`. Se nao existirem, informe o usuario para rodar `/gerar-newsletter` primeiro.

## Escopo
- Se `$ARGUMENTS` e "todas" ou vazio: revisar newsletters 01 a 05
- Se `$ARGUMENTS` e um numero (1-5): revisar apenas essa newsletter

## Para Cada Newsletter, Executar 3 Passadas

### Passada 1: Fact-Check e Precisao
Leia `conhecimento/produto/buzzmonitor.md` e verifique:

1. **Nomes de features**: Estao grafados exatamente como na tabela? (ex: "Smart Replies", nao "Respostas Inteligentes")
2. **Metricas de cases**: Os numeros batem com os cases verificados? (ex: Youse SLA de 36h para 3h, nao "de 48h para 2h")
3. **Descricao do produto**: As capacidades descritas existem de fato?
4. **Dados de mercado**: As estatisticas citadas tem fonte na pesquisa?
5. **Nomes de empresas**: Os cases mencionam empresas reais do blog?
6. **Conceitos nomeados**: Se a newsletter citar um vies cognitivo, efeito psicologico ou conceito cientifico pelo nome, verifique se a descricao corresponde a definicao real. Erros comuns:
   - "Efeito Spotlight" descrito como projecao de preferencias (ERRADO — Spotlight e autoconsciencia, nao projecao)
   - Qualquer conceito cuja descricao nao bate com a definicao academica padrao
   - Se estiver errado: corrija o nome para o conceito correto, ou remova o nome tecnico e descreva o fenomeno diretamente

Para cada problema encontrado:
- Corrija diretamente se a informacao correta esta disponivel
- Marque com [VERIFICAR] se precisar de confirmacao do usuario
- Opcionalmente, use WebFetch no blog da Buzzmonitor para confirmar dados de cases

### Passada 2: Estilo e Anti-Patterns
Leia `conhecimento/editorial/estilo-newsletter.md` e verifique:

1. **Construcoes proibidas**: Busque e elimine TODAS:
   - "Nao e X, e Y" e variacoes
   - Aberturas genericas ("No cenario atual...", "Em um mundo...")
   - Filler words (realmente, simplesmente, basicamente, etc.)
   - "Alem disso" como abertura (max 1 por newsletter)
   - Metaforas aquaticas (navegar, mergulhar, oceano)

2. **Acentuacao e pontuacao**: Verifique todo o texto em busca de palavras sem acento. Corrija todas as ocorrencias (ex: "nao" → "não", "alem" → "além", "ate" → "até", "tambem" → "também", "e" → "é" quando verbo, "voce" → "você", "so" → "só", "historia" → "história"). O texto deve estar em portugues brasileiro correto.

3. **Padroes de IA**: Identifique e corrija:
   - Listas de exatamente 3 itens (variar para 2, 4 ou 5)
   - Paragrafos iniciando com "Alem disso..."
   - Conclusoes com "Em resumo..." + lista
   - Excesso de pontos de exclamacao (max 2 por newsletter)
   - Perguntas retoricas em sequencia (max 1 por secao)

4. **Tom e voz**: O texto soa como um especialista compartilhando insight ou como um vendedor?

Para cada problema: reescreva o trecho mantendo a informacao mas melhorando a forma.

### Passada 3: Otimizacao e Impacto

1. **Enxugar**: Remova palavras que nao adicionam significado. Cada frase deve justificar sua existencia.
2. **Fluxo logico**: Verifique a progressao: gancho → problema → case → insight → CTA. Cada secao deve fluir naturalmente para a proxima.
3. **Gancho**: Os primeiros 2 paragrafos prendem atencao? Se nao, reescreva.
4. **CTA**: E natural e contextual? Faz sentido apos o insight? Se nao, ajuste.
5. **Assunto do email**: Tem menos de 60 caracteres? Gera curiosidade genuina?
6. **Contagem**: O texto tem menos de 600 palavras? Se nao, corte — priorize eliminar contexto de mercado generico, nao o gancho ou o case.

## Output

### Newsletters Revisadas
Sobrescreva cada arquivo `newsletter/entregas/YYYY-MM/newsletter-0X.md` com a versao revisada.
Adicione no topo do arquivo:
```
<!-- Revisado em [DATA] | Passadas: fact-check, estilo, otimizacao -->
```

### Log de Revisao
Crie `newsletter/entregas/YYYY-MM/REVISAO-LOG.md`:

```markdown
# Log de Revisao — [DATA]

## Newsletter 01: [Assunto]
- **Fact-check**: [problemas encontrados e correcoes feitas]
- **Estilo**: [padroes IA removidos e reescritas feitas]
- **Otimizacao**: [palavras cortadas, fluxo ajustado]
- **Palavras**: [antes] → [depois]
- **Status**: APROVADA | REQUER ATENCAO

[repetir para cada newsletter revisada]

## Resumo Geral
- Newsletters aprovadas: X/5
- Newsletters que requerem atencao: X/5
- Problemas mais comuns encontrados: [listar]
```

## Criterios de Aprovacao
Uma newsletter e APROVADA quando:
- Zero construcoes proibidas
- Todas as informacoes sobre Buzzmonitor estao corretas
- Menos de 600 palavras
- Gancho prende atencao
- CTA e natural
- Nenhum dado sem fonte
- Acentuacao e pontuacao corretas em todo o texto
- Conceitos nomeados verificados contra definicao real (ou removidos se incertos)

Uma newsletter REQUER ATENCAO quando:
- Algum dado marcado como [VERIFICAR]
- Informacao sobre produto que nao pode ser confirmada
- Gancho fraco que precisa de input criativo do usuario
