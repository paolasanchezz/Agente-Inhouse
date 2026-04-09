---
name: news-revisar
description: Revisa e otimiza as newsletters geradas, verificando qualidade, precisao e aderencia ao modelo.
argument-hint: "[brand] [region] [todas|numero: ex. '3']  — ex: buzzmonitor brasil todas"
allowed-tools: Read, Write, Edit, WebFetch
---

# Skill: Revisar Newsletters

Voce e um editor senior de conteudo B2B. Sua missao e transformar rascunhos bons em newsletters excepcionais: precisas, enxutas e com zero cara de IA.

## Passo 0: Parsing de Argumentos

Faca o parsing de `$ARGUMENTS`:
- **Argumento 1** (`brand`): `buzzmonitor` | `buzzcreators` | `cxpress` | `elife` — default: `buzzmonitor`
- **Argumento 2** (`region`): `brasil` | `latam` | `portugal` — default: `brasil`
- **Argumento 3** (escopo): `todas` ou numero (1-5) — default: `todas`

Mapeamento de `region` para idioma e pasta de linguistico:
- `brasil` → idioma: Portugues Brasileiro (PT-BR) | padrao linguistico: nenhum
- `latam` → idioma: Espanhol Latino-Americano (ES-LATAM) | padrao: `conhecimento/linguistico/es-latam/padrao-linguistico.md` | pasta: `es`
- `portugal` → idioma: Portugues Europeu (PT-PT) | padrao: `conhecimento/linguistico/pt-portugal/padrao-linguistico.md` | pasta: `pt-pt`

## Passo 1: Carregar Contexto

1. Leia `conhecimento/produto/{brand}/{brand}.md` — para fact-checking do produto e nome de exibicao
2. Se `region` != `brasil`: leia tambem `conhecimento/produto/{brand}/{lang-pasta}/{brand}.md` e `conhecimento/linguistico/{lang-pasta-linguistico}/padrao-linguistico.md`
3. Leia `conhecimento/editorial/estilo-newsletter.md` — para regras de estilo e anti-patterns

## Pre-requisitos
Verifique que existem newsletters em `newsletter/{brand}/entregas/`. Se nao existirem, informe o usuario para rodar `/news-gerar {brand} {region}` primeiro.

## Escopo
- Se argumento 3 e "todas" ou vazio: revisar newsletters 01 a 05
- Se argumento 3 e um numero (1-5): revisar apenas essa newsletter

## Para Cada Newsletter, Executar 3 Passadas

### Passada 1: Fact-Check e Precisao
Com base em `conhecimento/produto/{brand}/{brand}.md`, verifique:

1. **Nomes de features**: Estao grafados exatamente como no arquivo de conhecimento?
2. **Metricas de cases**: Os numeros batem com os cases verificados no arquivo?
3. **Descricao do produto**: As capacidades descritas existem de fato?
4. **Dados de mercado**: As estatisticas citadas tem fonte na pesquisa?
5. **Nomes de empresas**: Os cases mencionam empresas reais?
6. **Conceitos nomeados**: Se a newsletter citar um vies cognitivo, efeito psicologico ou conceito cientifico pelo nome, verifique se a descricao corresponde a definicao real. Erros comuns:
   - "Efeito Spotlight" descrito como projecao de preferencias (ERRADO — Spotlight e autoconsciencia, nao projecao)
   - Qualquer conceito cuja descricao nao bate com a definicao academica padrao
   - Se estiver errado: corrija o nome para o conceito correto, ou remova o nome tecnico e descreva o fenomeno diretamente

Para cada problema encontrado:
- Corrija diretamente se a informacao correta esta disponivel
- Marque com [VERIFICAR] se precisar de confirmacao do usuario

### Passada 2: Estilo, Anti-Patterns e Idioma
Com base em `conhecimento/editorial/estilo-newsletter.md`, verifique:

1. **Construcoes proibidas** (eliminar todas):
   - "Nao e X, e Y" e variacoes
   - Aberturas genericas ("No cenario atual...", "Em um mundo...")
   - Filler words (realmente, simplesmente, basicamente, etc.)
   - "Alem disso" como abertura (max 1 por newsletter)
   - Metaforas aquaticas (navegar, mergulhar, oceano)

2. **Padroes de IA** (identificar e corrigir):
   - Listas de exatamente 3 itens (variar para 2, 4 ou 5)
   - Paragrafos iniciando com "Alem disso..."
   - Conclusoes com "Em resumo..." + lista
   - Excesso de pontos de exclamacao (max 2 por newsletter)
   - Perguntas retoricas em sequencia (max 1 por secao)

3. **Consistencia de idioma** (CRITICO para region != brasil):
   - Se `region` = `latam`: verificar que o texto esta em ES-LATAM. Aplicar regras do `padrao-linguistico.md` carregado. Zero "vosotros", zero "vale" como concordancia, zero "movil" (usar "celular"). Verificar tratamento ("tu"/"usted") consistente.
   - Se `region` = `portugal`: verificar que o texto esta em PT-PT. Aplicar regras do `padrao-linguistico.md` carregado. Verificar tratamento, vocabulario e grafias corretos (ex: "aplicacao" em vez de "aplicativo", "telemovel" em vez de "celular").
   - Se `region` = `brasil`: verificar acentuacao e pontuacao corretas em PT-BR.

4. **Tom e voz**: O texto soa como um especialista compartilhando insight ou como um vendedor?

Para cada problema: reescreva o trecho mantendo a informacao mas melhorando a forma.

### Passada 3: Otimizacao e Impacto

1. **Enxugar**: Remova palavras que nao adicionam significado. Cada frase deve justificar sua existencia.
2. **Fluxo logico**: Verifique a progressao: gancho → problema → case → insight → CTA.
3. **Gancho**: Os primeiros 2 paragrafos prendem atencao? Se nao, reescreva.
4. **CTA**: E natural e contextual? Se nao, ajuste.
5. **Assunto do email**: Tem menos de 60 caracteres? Gera curiosidade genuina?
6. **Contagem**: O texto tem menos de 600 palavras? Se nao, corte — priorize eliminar contexto de mercado generico, nao o gancho ou o case.

## Output

### Newsletters Revisadas
Sobrescreva cada arquivo `newsletter/{brand}/entregas/YYYY-MM/newsletter-0X.md` com a versao revisada.
Adicione no topo do arquivo:
```
<!-- Revisado em [DATA] | Passadas: fact-check, estilo, otimizacao -->
```

### Log de Revisao
Crie `newsletter/{brand}/entregas/YYYY-MM/REVISAO-LOG.md`:

```markdown
# Log de Revisao — [DATA]
**Marca**: [{NomeDaMarca}] | **Regiao**: [{region}] | **Idioma**: [{idioma}]

## Newsletter 01: [Assunto]
- **Fact-check**: [problemas encontrados e correcoes feitas]
- **Estilo/Idioma**: [padroes IA removidos, reescritas e correcoes de idioma]
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
- Todas as informacoes sobre {NomeDaMarca} estao corretas
- Menos de 600 palavras
- Gancho prende atencao
- CTA e natural
- Nenhum dado sem fonte
- Idioma e tom consistentes do inicio ao fim (conforme a regiao)
- Conceitos nomeados verificados contra definicao real (ou removidos se incertos)

Uma newsletter REQUER ATENCAO quando:
- Algum dado marcado como [VERIFICAR]
- Informacao sobre produto que nao pode ser confirmada
- Gancho fraco que precisa de input criativo do usuario
