# Template — Newsletter Semanal [MARCA]

Estrutura fixa: 2 blocos obrigatorios (Abertura, Resposta em capitulos) + 3 blocos opcionais (Mais pra explorar, Na imprensa, Bloco extra).

**Limite de palavras: ≤300 (corpo, sem rodape e sem cabecalho).**
**Links contextuais: 3-6 totais.** Minimo 3 sao posts proprios (resposta em capitulos). Maximo 1 clipping externo. Maximo 1 link extra (demo/landing/evento). Rodape mantem 3 links sociais (nao contam nos 3-6).

**Pergunta-eixo da semana**: e elemento INTERNO de planejamento (vive em `dor-semana.md`). Direciona o assunto, o pre-header e o tom da abertura — mas **NAO aparece como bloco visivel para o leitor**. Nada de blockquote+bold "A pergunta da semana" no corpo da newsletter.

---

## 1. Cabecalho do email

- **Assunto**: maximo 60 chars, jornalistico, sem clickbait — pode ser a pergunta-eixo encurtada
  - Exemplos bons: "Atendimento que nao escala: o que fazer", "Tres respostas para uma pergunta antiga"
  - Exemplos ruins: "IMPERDIVEL: descubra como...", "5 dicas incriveis"
- **Pre-header**: 80 chars, complementa o assunto (segunda linha que aparece na caixa de entrada)

## 2. Abertura jornalistica (30-50 palavras, 1 paragrafo)

Lead direto. Comeca com fato, dado ou contexto — nunca com gancho narrativo de marketing. A abertura pode ja "embutir" a tese da pergunta-eixo (sem formula-la como pergunta visivel ao leitor).

**FORMATO**: [O que aconteceu / foi discutido / e tendencia sobre essa dor] + [por que importa pra quem le].

**A evitar**:
- "Imagine que voce..."
- "Existe um momento que..."
- "Sabe quando..."
- "No mundo atual..."
- "Vivemos uma era..."
- "No cenario atual de..."

**A buscar**:
- Cena vivida ("Uma rede de varejo em Sao Paulo...")
- Dado impactante ("Entre janeiro e marco, X cresceu Y%...")
- Conflito ("O setor diz X. Os dados mostram Y.")
- Contexto direto ("A discussao na ultima semana voltou a um problema antigo...")

## 3. Resposta em capitulos (110-170 palavras, 3 mini-blocos)

Tres mini-respostas. Cada mini-bloco aponta para 1 post do blog proprio. **Os 3 links sao obrigatorios — eles formam o minimo de links da edicao.**

**A pergunta-eixo nao aparece como bloco**. Os mini-blocos sao apresentados como recortes/teses — nao como "respostas" a uma pergunta visivel.

**Estrutura por mini-bloco** (~35-55 palavras cada):
- **Subtitulo curto** (frase-chave do recorte, 6-10 palavras, em negrito)
- **Tese + evidencia/exemplo** (1-2 frases curtas, com edutainment)
- **Link**: → [Ler no blog](URL_post)

**Edutainment por mini-bloco** — cada um deve ter PELO MENOS UM destes:
- **Definicao clara** de um conceito relevante
- **Analogia util** (curta, especifica, nao forcada)
- **Exemplo concreto** (cena ou caso, real ou ilustrativo)
- **Dado verificavel** (estatistica com fonte)

**A evitar**:
- Repetir o mesmo angulo nos 3 mini-blocos
- Citar a {NomeDaMarca} fora desses links como produto a vender
- Frases longas — alvo medio ≤22 palavras por frase

## 4. Mais pra explorar (OPCIONAL — 1 bullet, 15-25 palavras)

So incluir se ainda houver orcamento de palavras (≤300 corpo).

**Formato**:
**Mais pra explorar:** [Titulo do post](link) — 1 frase com o angulo correlato.

Posts secundarios do blog que aprofundam pontos colaterais.

## 5. Na imprensa esta semana (OPCIONAL — 1 menção, 25-40 palavras)

So incluir se `clipping-pr.md` da pesquisa tiver mencao relevante (data ≤7 dias).

**Formato**:
**[Veiculo]** publicou [contexto: entrevista | citacao | premio | parceria]. [1-2 frases sobre o que foi dito.]
→ [Ler materia completa](URL)

Maximo 1 mencao por edicao (mesmo se a pesquisa coletou 2). Escolher a mais relevante.

## 6. Bloco extra (OPCIONAL — 1 frase, ate 20 palavras)

So incluir se houver gancho real da semana: lancamento, evento, webinar, vaga aberta, atualizacao do produto. **Sem cadencia fixa** — nao e um slot rotativo. Pode passar varias edicoes sem.

**Formato**:
P.S.: [1 frase contextual + link].

Exemplos:
- "P.S.: na quinta tem webinar sobre X — [inscreva-se aqui](URL)."
- "P.S.: lancamos o modulo Y esta semana — [veja como funciona](URL)."

## 7. Rodape

```
—
Equipe [MARCA]

[LinkedIn] · [Instagram] · [Site]
```

Os 3 links sociais sao fixos e NAO contam nos 3-6 links contextuais.

---

## Especificacoes Gerais

- **Palavras totais (corpo, sem cabecalho e rodape)**: ≤300
- **Links contextuais**: 3-6, sendo ≥3 para o blog proprio
- **Frases**: medias ≤22 palavras, max 30 numa frase
- **Idioma**: PT-BR (brasil) | ES-LATAM (latam) | PT-PT (portugal)
- **Saudacao**: "Oi, {{nome}}." (sem emoji)
- **Tom**: editor jornalistico — nao vendedor, nao narrativo
- **Edutainment**: cada mini-bloco da resposta tem analogia, dado, exemplo ou definicao
- **Pergunta-eixo**: elemento INTERNO de `dor-semana.md`. Pode informar assunto/abertura mas NAO aparece como bloco visivel

## Anti-IA aplicado (de regras-anti-ia.md)

- Zero em-dashes ("—") como pontuacao narrativa (usar virgula, ponto ou parenteses)
- Zero filler ("realmente", "de fato", "de forma X", "no mundo atual")
- Maximo 2 antiteses-por-negacao por edicao ("nao e X — e Y")
- Zero "em resumo" ou "em conclusao" como fechamento
- Zero listas de 3 itens decorativas
- Acentuacao correta no idioma da regiao
