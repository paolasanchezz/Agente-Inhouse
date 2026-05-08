---
name: news-revisar
description: Revisa a newsletter semanal gerada — fact-check, linguagem jornalistica, anti-IA, dedupe e tom nao-vendedor. Sobrescreve o arquivo da edicao com a versao corrigida.
argument-hint: "[brand] [region]  — ex: cxpress brasil | buzzmonitor latam"
allowed-tools: Read, Write, Edit, WebFetch
version: 2.1.0
---

# Skill: Revisar Newsletter Semanal

Voce e um editor jornalistico senior. Sua missao e transformar o rascunho em uma newsletter aprovada para envio: jornalistica, com edutainment, sem cara de campanha, com idioma nativo e zero anti-IA.

**Esta v2.0** revisa 1 newsletter por execucao (a v1 revisava 1-5). Argumento `[todas|N]` removido.

## Passo 0: Parsing de Argumentos

Leia `.claude/skills/news-pesquisar/CONTEXT.md` para marcas, regioes, caminhos e Notion IDs.

Faca o parsing de `$ARGUMENTS`:
- **Argumento 1** (`brand`): `buzzmonitor` | `buzzcreators` | `cxpress` | `elife` — default: `buzzmonitor`
- **Argumento 2** (`region`): `brasil` | `latam` | `portugal` — default: `brasil`

Calcule a semana ISO atual: `YYYY-WW`. Salve como `{SEMANA_ISO}`.

## Pre-requisitos

Verifique que existe `newsletter/{brand}/entregas/newsletter-{SEMANA_ISO}.md`. Se nao existir, INFORME o usuario para rodar `/news-gerar {brand} {region}` primeiro e PARE.

## Passo 1: Carregar Contexto

Leia:

1. `brand/{brand}/BRANDBOOK.md` — fact-checking de produto, cases verificados, anti-patterns
2. Se `region` != `brasil`: `conhecimento/produto/{brand}/{lang-pasta}/{brand}.md` e `conhecimento/linguistico/{lang-linguistico}/padrao-linguistico.md`
3. `conhecimento/editorial/estilo-newsletter.md` — secoes "Anatomia", "Linguagem jornalistica", "Edutainment", "Criterios de selecao"
4. `conhecimento/editorial/regras-anti-ia.md` — regras anti-IA aplicaveis
5. `.claude/skills/news-gerar/template-newsletter.md` — estrutura obrigatoria
6. `conhecimento/produto/{brand}/pesquisa/atual/dor-semana.md` — para conferir pergunta-eixo, posts-ancora e clipping
7. `conhecimento/produto/{brand}/pesquisa/atual/clipping-pr.md` (se existir) — para validar mencao de imprensa
8. `newsletter/{brand}/entregas/newsletter-{SEMANA_ISO}.md` — a edicao a revisar
9. Se existir: `newsletter/{brand}/entregas/_state.json` — historico para dedupe

## Passada 1: Fact-Check, Estrutura e Links

### Fact-check

1. **Pergunta-eixo**: bate com a definida em `dor-semana.md`?
2. **Posts-ancora**: as 3 URLs apontam para os posts-ancora reais de `dor-semana.md`? Frase-chave usada combina com o angulo prometido?
3. **Mencao da imprensa** (se houver bloco "Na imprensa"): bate com `clipping-pr.md`? URL e veiculo corretos? Data ≤ 7 dias?
4. **Cases nominais**: se a NL cita case real, esta na lista `### Cases de Sucesso Verificados` do BRANDBOOK?
5. **Nomes de features**: grafados exatamente como no BRANDBOOK?
6. **Conceitos nomeados**: se cita vies cognitivo ou efeito psicologico pelo nome, a definicao usada bate com a academica? Erros comuns:
   - "Efeito Spotlight" descrito como projecao de preferencias (ERRADO — Spotlight e autoconsciencia, nao projecao)
   - Qualquer conceito cuja descricao nao bate com a definicao padrao
   - Se errado: corrigir nome, ou descrever fenomeno sem nome tecnico

Para cada problema:
- Corrija diretamente se a informacao certa esta disponivel
- Marque com `[VERIFICAR]` se precisar de confirmacao do usuario

### Estrutura de blocos

Confirme que a edicao tem (na ordem):
- Cabecalho (Assunto + Pre-header + metadados; pergunta-eixo entra como comentario HTML interno, NAO como bloco visivel)
- Saudacao (`Oi, {{nome}}.`)
- Abertura jornalistica (30-50 palavras, 1 paragrafo)
- Resposta em capitulos (3 mini-blocos curtos, total 110-170 palavras)
- Blocos opcionais (Mais pra explorar, Na imprensa, Bloco extra) — somente se aplicaveis
- Rodape (assinatura + 3 links sociais)

**Pergunta-eixo NAO deve aparecer como bloco visivel**: confirmar que NAO existe `> ## A pergunta da semana`, callout/blockquote com a pergunta literal, nem heading com a pergunta. A pergunta vive em `dor-semana.md` (planejamento) e/ou comentario HTML no topo do arquivo. Se aparecer no corpo visivel, REMOVER e absorver na abertura/assunto.

Se faltar um bloco obrigatorio, RECONSTRUA a partir de `dor-semana.md`.

### Orcamento de links

Conte os links contextuais (excluindo rodape social):
- ≥3 links para o blog proprio (resposta em capitulos)
- 3-6 links totais
- ≤1 link de clipping PR
- ≤1 link extra (demo/landing/evento)
- 0 links para "noticias gerais de mercado" sem ligacao a marca

Se violar: ajustar (cortar links em excesso, ou alertar se faltarem ancoras).

### Dedupe (se _state.json existir)

Confira que:
- A pergunta-eixo desta edicao nao esta nas perguntas-dor das ultimas 6 semanas
- Os links contextuais nao estao em `links_usados` das ultimas 4 semanas

Se houver duplicidade que `news-pesquisar` deixou passar, alerte e marque `[VERIFICAR DEDUPE]`.

## Passada 2: Linguagem Jornalistica e Anti-IA

### Linguagem jornalistica

1. **Piramide invertida — abertura**:
   - A **primeira frase** da abertura contem o apex: O Que (fato/insight central)?
   - A abertura responde O Que + Por Que importa em ≤50 palavras?
   - A abertura e completa em si (se o leitor parar aqui, entendeu o ponto)?
   - Se a primeira frase for contexto/aquecimento em vez de apex: **reescrever pondo o apex primeiro**.

2. **Lead da abertura**: comeca com fato, dado, cena ou conflito? REJEITAR aberturas tipo:
   - "Imagine que voce..."
   - "Existe um momento que..."
   - "Sabe quando..."
   - "No mundo atual..."
   - "Vivemos uma era..."
   - "No cenario atual de..."

   Se algum aparecer: **reescrever a abertura** com lead direto.

3. **Mini-piramide invertida — capitulos**:
   - Cada mini-bloco comeca com a tese (resposta/conclusao) na primeira frase?
   - A evidencia/edutainment vem DEPOIS da tese (nao antes)?
   - Se um mini-bloco comecar com contexto antes da tese: **mover a tese para a primeira frase**.

4. **Frases curtas**:
   - Comprimento medio ≤22 palavras
   - Maximo 30 palavras numa unica frase
   - Sujeito-verbo-objeto, sem rodeios

   Se houver frases longas: **quebrar em 2-3 menores**.

5. **Tom nao-vendedor**:
   - Maximo 1 mencao a {NomeDaMarca} fora dos links de blog proprio
   - Nao descrever feature como diferencial (papel da landing)
   - Se >40% dos links contextuais apontam para domínio próprio fora do blog (demo/landing), alertar — sinal de campanha disfarcada

6. **Pergunta-eixo NAO visivel**: confirmar que a pergunta-eixo NAO aparece como bloco no corpo da NL (sem `> ## A pergunta da semana`, sem callout, sem heading). Ela vive como comentario HTML no topo do arquivo e em `dor-semana.md`. Se aparecer visivel, REMOVER e absorver no assunto/abertura.

### Edutainment

Cada um dos 3 mini-blocos da resposta deve conter PELO MENOS UM destes:
- Analogia util
- Dado verificavel (com fonte)
- Exemplo concreto (real ou ilustrativo)
- Definicao clara

Se um mini-bloco nao tiver nenhum: **adicionar evidencia** (sem inventar dados — usar do post-ancora citado).

### Anti-IA (carregar `regras-anti-ia.md`)

Aplicar TODAS as regras:
- Zero em-dashes ("—") como pontuacao narrativa (substituir por virgula, ponto, parenteses ou dois-pontos)
- Zero filler ("realmente", "de fato", "de forma X", "no mundo atual")
- Maximo 2 antiteses-por-negacao por edicao ("nao e X — e Y")
- Zero "em resumo" ou "em conclusao"
- Zero listas de 3 itens decorativas
- Acentuacao correta no idioma da regiao

Para cada item: corrigir diretamente.

### Idioma (CRITICO)

1. **Brasil (PT-BR)**: acentuacao + pontuacao corretas; sem hispanismos ou lusitanismos
2. **LATAM (ES-LATAM)**: aplicar `padrao-linguistico.md`. Zero "vosotros". Zero "vale" como concordancia. Zero "movil" (usar "celular"). Tratamento ("tu"/"usted") consistente.
3. **Portugal (PT-PT)**: aplicar `padrao-linguistico.md`. Zero brasileirismos. "Telemovel", "aplicacao", "casa de banho". Tratamento "voce" (3.a pessoa).

Reescrever trechos que escaparem ao padrao.

## Passada 3: Otimizacao e Impacto

1. **Enxugar**: cada palavra deve justificar sua existencia. Cortar adjetivos vazios, adverbios redundantes.
2. **Fluxo logico**: abertura → pergunta-eixo → 3 capitulos → opcionais → rodape. Cada bloco deve emendar no proximo sem quebra de tom.
3. **Cabecalho**:
   - Assunto ≤60 chars, jornalistico, sem clickbait
   - Pre-header ≤80 chars, complementa assunto
4. **Contagem**: corpo (sem cabecalho e rodape) ≤300 palavras. Se passar, cortar — priorizar enxugar abertura e mini-blocos da resposta, mantendo as 3 frases-chave.

## Output

### Newsletter Revisada

Sobrescreva `newsletter/{brand}/entregas/newsletter-{SEMANA_ISO}.md` com a versao revisada.

Adicione no topo do arquivo (acima do cabecalho de metadados):
```
<!-- Revisado em [DATA] | Passadas: fact-check, linguagem, otimizacao -->
```

### Log de Revisao

Crie `newsletter/{brand}/entregas/REVISAO-LOG-{SEMANA_ISO}.md`:

```markdown
# Log de Revisao — Newsletter Semanal {SEMANA_ISO}
**Marca**: {NomeDaMarca} | **Regiao**: {region} | **Idioma**: {idioma}
**Data da revisao**: {DATA}

## Edicao revisada
- **Assunto**: ...
- **Pergunta-eixo**: ...
- **Status**: APROVADA | REQUER ATENCAO

## Passada 1: Fact-check, estrutura, links
- Problemas encontrados: ...
- Correcoes aplicadas: ...
- Links contextuais: N (3-6 ✓ | violacao detectada)
- Dedupe: ok | duplicidade marcada [VERIFICAR DEDUPE]

## Passada 2: Linguagem jornalistica e anti-IA
- Aberturas narrativas reescritas: N
- Frases longas quebradas: N
- Em-dashes removidos: N
- Filler removidos: N
- Idioma: corrigido | ja estava ok
- Edutainment: adicionado em mini-bloco N | ja estava ok

## Passada 3: Otimizacao
- Palavras: antes [N] → depois [N]
- Cortes principais: ...
- Cabecalho ajustado: assunto / pre-header

## Pendencias para o usuario
- [Items marcados como VERIFICAR]

## Resumo
- APROVADA | REQUER ATENCAO
```

## Criterios de Aprovacao

Uma newsletter e **APROVADA** quando:
- Zero anti-IA (em-dashes, fillers, antiteses-por-negacao em excesso, "em resumo")
- ≥3 links para o blog proprio
- 3-6 links contextuais totais
- ≤1 link de clipping PR
- 0 links para noticias gerais de mercado
- Pergunta-eixo NAO aparece como bloco visivel (so no comentario HTML interno e em `dor-semana.md`)
- Estrutura: Abertura + Resposta em capitulos (Mais pra explorar, Clipping e Extra opcionais)
- Corpo ≤300 palavras
- **Piramide invertida — abertura**: primeira frase e o apex (O Que + Por Que importa); abertura completa em si
- **Piramide invertida — capitulos**: cada mini-bloco tem tese na primeira frase, evidencia depois
- Lead jornalistico (sem aberturas narrativas proibidas)
- Frases medias ≤22 palavras
- Tom nao-vendedor (max 1 mencao a {NomeDaMarca} fora dos links de blog)
- Edutainment em cada mini-bloco da resposta
- Cases nominais validados contra BRANDBOOK
- Conceitos nomeados validados contra definicao real
- Idioma e tom consistentes (PT-BR | ES-LATAM | PT-PT conforme regiao)
- Dedupe ok (pergunta-dor 6 semanas, links 4 semanas)
- ≤600 palavras no corpo

Uma newsletter **REQUER ATENCAO** quando:
- Algum dado marcado `[VERIFICAR]` ou `[VERIFICAR DEDUPE]`
- Mencao de imprensa nao validada na fonte
- Tom borderline vendedor (ex: 30-40% dos links sao para domínio próprio fora do blog)
- Abertura ainda fraca apos uma reescrita
