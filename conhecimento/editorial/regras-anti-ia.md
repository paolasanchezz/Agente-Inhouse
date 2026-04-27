# Regras Anti-IA — Deteccao e Eliminacao

Estas regras se aplicam a TODO conteudo gerado (newsletters, copys, traducoes). Tolerancia zero.

---

## Frases Tipicas de IA (NUNCA usar)
- "No cenario atual..." / "No mundo de hoje..."
- "Em um mundo cada vez mais conectado/digital/competitivo..."
- "Nos ultimos anos..." / "Com o avanco da tecnologia..."
- "E inegavel que..." / "E fato que..."
- "Nesse sentido..." / "Diante disso..."
- "Vale ressaltar que..." / "E importante destacar que..."
- "Em suma..." / "Em resumo..." / "Para concluir..."
- "Voce ja parou para pensar...?" (como abertura — pode usar no meio do texto com moderacao)

## Filler Words (NUNCA usar)
- realmente, verdadeiramente, simplesmente, basicamente
- literalmente, definitivamente, absolutamente, certamente
- extremamente, incrivelmente, impressionantemente
- revolucionario, transformador, disruptivo (salvo com dados que comprovem)
- **"de forma X" / "de maneira X"** — "de forma clara", "de forma pontual", "de maneira eficiente". Substituir por adverbio direto ou cortar.

## Estruturas Viciadas (mesmo padrao em varias roupagens)

Estas formulas tem cara de "punch" mas viram mecanicas quando repetem. Conte instancias antes de fechar a copy.

### Antitese-por-negacao
A formula "afirma X, nega Y" tem multiplas roupagens — todas contam como o mesmo padrao:
- "X, nao Y"
- "X — nao Y"
- "X (nao Y)"
- "Nao X, mas Y"
- "Nao se trata de X, mas sim de Y"
- "Nao e X, e Y"

**Por que e armadilha:** AI usa pra dar contraste a afirmacoes fracas. Light Copy/Ladeira encoraja antitese como elemento literario, mas literatura usa contraste com **assuntos diferentes** ("Ela vai tocar seu coracao. Eu vou tocar seu bolso."). AI repete a estrutura no mesmo eixo ("dado de vaidade, nao de venda" + "uma narrativa, nao tres campanhas" + "com metodo, nao com achismo") ate virar tique.

**Limite:** maximo **2 instancias** dessa familia em peca de ate 500 palavras. Mais que isso, redo.
**Como testar:** busque ", nao ", " — nao ", "(nao ", "Nao se trata", "Nao e " no texto final. Conte.

### Em-dash (—) — TOLERANCIA ZERO
**Regra absoluta:** o caractere `—` (em-dash) nao aparece em nenhum conteudo gerado. Nenhuma ocorrencia. Nao tem "salvo se".

**Por que:** AI defaulta pra em-dash quando quer pausar com "punch". Pessoa real escrevendo em PT-BR usa virgula, ponto ou parenteses — em-dash em copy gerada e o tique mais facil de identificar (basta um Ctrl+F). A presenca de qualquer em-dash no output ja vaza IA, mesmo que todo o resto esteja impecavel.

**Substitutos diretos:**
| Funcao do em-dash | Substituto |
|---|---|
| Pausa curta dentro da frase | virgula |
| Pausa forte / quebra de pensamento | ponto (duas frases) |
| Aparte / informacao adicional | parenteses |
| Atribuicao de citacao (`— Autor`) | virgula ou nova linha |

**Excecao unica:** separadores de secao em markdown (`---` na linha sozinha — sao tres hifens, viram `<hr>`, nao sao em-dash).

**Como testar:** Ctrl+F por `—` no texto final. Resultado esperado: **0 ocorrencias.**

### Substitutos decorativos (filler 2.0)
Ao remover um filler, nao crie outro. A palavra que voce adiciona tem que responder "o que" ou "como" — nao so adicionar ritmo.

**Suspeitos comuns:** magica, real, verdadeiro, autentico, genuino, transformador, achismo (quando usado pra punch sem dado), feeling (quando vira ornamento).

**Exemplos:**
- ❌ "de forma clara" → "sem planilha magica" (magica nao explica como)
- ✅ "de forma clara" → "sem dashboard manual" ou apenas remover
- ❌ "trazer resultados" → "trazer resultado real" (real e filler)
- ✅ "trazer resultados" → "trazer X% de aumento" (numero) ou cortar
- ❌ "medir com precisao" → "medir com metodo, nao com achismo" (achismo aqui e enfeite)
- ✅ "medir com precisao" → "medir por receita gerada por creator"

**Teste:** se tirar a palavra adicionada e a frase continuar dizendo a mesma coisa, era enfeite. Remova ou substitua por algo concreto.

## Anti-Patterns Estruturais
- Listas de exatamente 3 itens sempre (variar: 2, 4, 5)
- Paragrafos que comecam com "Alem disso..." (max 1 por peca)
- Conclusoes com "Em resumo..." seguido de lista
- Metaforas aquaticas ("navegar", "mergulhar", "oceano de dados")
- Excesso de pontos de exclamacao (max 2 por peca inteira)
- Perguntas retoricas em sequencia (max 1 por secao)
- Emoji em excesso (max 2-3 por peca, apenas em assunto ou CTA)
- Tom excessivamente otimista e uniforme (falta de contraste emocional)
- Frases longas com muitas virgulas e conectivos ("que", "onde", "o qual")
- Adjetivos empilhados ("solucao inovadora, robusta e escalavel")
- Transicoes mecanicas entre paragrafos ("Alem disso", "Por outro lado", "Nesse contexto")
- **Ritmo sintatico repetitivo:** 2+ frases consecutivas com a mesma estrutura (mesmo comprimento + mesma forma) viram cantilena. Varie comprimento e quebre.

## Teste Final de Naturalidade
- A copy soa como uma pessoa real falando? Ou soa como texto gerado?
- Tem personalidade, opiniao, ponto de vista? Ou e generico e "seguro"?
- **Re-checagem pos-correcao:** quando o texto e fruto de revisao (skill `copy-revisar`, `news-revisar`, `trad-revisar`), as proprias correcoes podem ter introduzido IA. Releia o texto **corrigido** com este arquivo aberto e rode contagens das "Estruturas Viciadas" acima — antitese-por-negacao, em-dash, substitutos decorativos. A maioria dos vazamentos de IA pos-revisao acontece nessa zona.

---

## Anexo: Variacoes por idioma (PT-PT e ES-LATAM)

Mesmas regras acima, com as frases tipicas traduzidas para cada idioma. Usar estas listas ao revisar copy em PT-PT ou ES-LATAM — os anti-patterns estruturais e filler words da lista principal continuam aplicaveis (traduzidos conforme vocabulario do idioma).

### PT-PT (Portugues Europeu)
- "No cenário atual..."
- "Em um mundo cada vez mais..."
- "É inegável que..."
- "Vale ressaltar que..."
- "Cabe salientar que..."
- "Em suma..." seguido de lista repetindo o que foi dito
- "Além disso" a abrir mais de 1 parágrafo por texto

### ES-LATAM (Espanol Latinoamericano)
- "En el escenario actual..."
- "En un mundo cada vez más..."
- "Es innegable que..."
- "Vale la pena destacar que..."
- "Cabe mencionar que..."
- "En resumen..." seguido de lista repetindo o que foi dito
- "Además" a abrir mais de 1 parágrafo por texto

> Se identificar construcao de IA especifica de um idioma que nao esta aqui, adicionar nesta secao (nao no padrao-linguistico.md do idioma).
