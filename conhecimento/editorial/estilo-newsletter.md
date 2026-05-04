# Guia de Estilo — Newsletter Semanal Grupo Elife

## Tom e Voz

- **Editor jornalistico, nao vendedor**: voz de quem cura e contextualiza, nao de quem vende
- **Direta**: sujeito-verbo-objeto, sem rodeios
- **Edutainment**: educacao + entretenimento — definicao + analogia util + exemplo concreto + acao pratica
- **Confiante sem hype**: a marca facilita aprendizado, nao salva o leitor

## Referencia de Estilo

Modelo baseado na **newsletter oficial Buzzmonitor**:
- Voz de editor humano contextualizando a edicao
- Eixo em uma pergunta-dor (nao em um case)
- 3 recortes apontando para posts do blog proprio (resposta em capitulos)
- Alta densidade de links — predominantemente para o blog proprio (90% — diretriz Alessandro)
- Lead jornalistico (fato/dado/cena), sem gancho narrativo de marketing
- Sem CTA unico forte — links contextuais distribuidos onde fazem sentido

Calibracao detalhada: ler `conhecimento/copywriting/swipe-file/buzzmonitor-newsletter.md` (popular com 3-5 edicoes reais).

---

## Construcoes PROIBIDAS

Consulte `conhecimento/editorial/regras-anti-ia.md` para a lista completa de frases de IA, filler words e anti-patterns estruturais. Todas se aplicam integralmente a newsletters.

---

## Anatomia da Newsletter Semanal

2 blocos obrigatorios + ate 3 opcionais. **A pergunta-eixo da semana vive em `dor-semana.md` como planejamento interno**: direciona o assunto, o pre-header e a abertura, mas NAO aparece como bloco visivel para o leitor.

| # | Bloco | Funcao | Itens | Palavras |
|---|---|---|---|---|
| 1 | **Abertura jornalistica** | Lead direto que embute a tese (sem formular a pergunta-eixo explicitamente) | 1 paragrafo | 30-50 |
| 2 | **Resposta em capitulos** | 3 mini-respostas (uma por post-ancora do blog), cada uma com 1-2 frases curtas + link | 3 itens | 110-170 |
| 3 (opcional) | **Mais pra explorar** | 1 bullet de outro post do blog que aprofunda angulo correlato | 1 bullet | 0-25 |
| 4 (opcional) | **Na imprensa** | 1 mencao da marca em midia externa (clipping PR), data ≤ 7 dias | 0-1 item | 0-40 |
| 5 (opcional) | **Bloco extra** | Demo/webinar/landing — so se houver gancho real da semana, sem cadencia fixa | 1 frase | 0-20 |

**Limites totais**:
- ≤300 palavras no corpo (sem cabecalho e rodape)
- 3-6 links contextuais (excluindo rodape social)
- Minimo 3 links para o blog proprio (resposta em capitulos)
- Maximo 1 clipping externo
- Maximo 1 link extra (demo/landing/evento)
- Pergunta-eixo NUNCA aparece como bloco visivel (nem blockquote, nem callout)

---

## Aberturas jornalisticas

Comecar com fato, dado, cena ou conflito. **Nunca** com gancho narrativo de marketing.

### A buscar

- **Cena vivida**: "Uma rede de varejo em Sao Paulo demitiu 30 atendentes em janeiro. Nao por corte de custos — porque o chatbot passou a resolver 62% dos tickets sozinho."
- **Dado impactante**: "Entre janeiro e marco, o tempo medio de resposta no WhatsApp Business caiu de 8 minutos para 47 segundos."
- **Conflito**: "O setor diz que IA cuida do volume. Os dados mostram que ela mantem o ticket, mas perde o cliente."
- **Contexto direto**: "A discussao na ultima semana voltou a um problema antigo: como dimensionar atendimento omnichannel sem aumentar headcount."

### A evitar (rejeitar na revisao)

- "Imagine que voce..."
- "Existe um momento que..."
- "Sabe quando..."
- "No mundo atual..."
- "Vivemos uma era de..."
- "No cenario atual de..."

---

## Linguagem jornalistica e direta

1. **Lead 5W1H simplificado**: o que aconteceu / quem / quando / por que importa.
2. **Frases curtas**: comprimento medio ≤22 palavras, max 30 numa unica frase.
3. **Sujeito-verbo-objeto**: evitar inversoes elaboradas, oracoes encaixadas em excesso.
4. **Sem hype**: zero "incrivel", "imperdivel", "revolucionario", "definitivo".
5. **Verbos no presente** quando possivel — newsletter editorial vive no presente.

---

## Edutainment

Cada um dos 3 mini-blocos da resposta em capitulos deve conter PELO MENOS UM destes:

- **Definicao clara** de um conceito relevante (em poucas palavras)
- **Analogia util** (curta, especifica, que ilumina — nao decorativa)
- **Exemplo concreto** (cena ou caso, real ou ilustrativo)
- **Dado verificavel** (estatistica com fonte)

A estrutura ideal de um mini-bloco:
1. **Subtitulo curto** (frase-chave do recorte)
2. **Tese** (1 frase clara que responde a pergunta sob esse angulo)
3. **Edutainment** (analogia / dado / exemplo / definicao)
4. **Link**: → [Aprofunde no blog](URL)

---

## Criterios de selecao de post proprio

A pesquisa (`news-pesquisar`) escolhe os 3 posts-ancora aplicando:

- **Cobertura de angulo**: cada post-ancora cobre um angulo distinto da pergunta-dor (nao 3 sinonimos)
- **Idade do post**: preferir <18 meses (mas posts mais antigos com conteudo evergreen valem)
- **Ultima vez citado**: ≥4 semanas (evitar repeticao em janela curta — controlado por `_state.json`)

Posts secundarios ("Mais pra explorar") seguem os mesmos criterios, com tolerancia maior em recencia.

---

## Criterios de clipping PR (bloco "Na imprensa")

- **Mencao da marca** em veiculo terceiro (entrevista, citacao em reportagem, premio, ranking, parceria)
- **Data ≤ 7 dias**
- **Maximo 1 mencao por edicao** (mesmo se a pesquisa coletar 2)
- **Veiculos relevantes**: imprensa de marketing/CX/digital — sem agregadores nem listagem em diretorio

---

## Bloco extra (sem cadencia fixa)

Diferente de "CTA rotativo" — o bloco extra entra somente se houver **gancho real da semana**:

- Lancamento de produto/feature
- Evento/webinar com data
- Vaga aberta
- Atualizacao relevante para a base

Pode passar varias edicoes seguidas SEM bloco extra. Nao for car CTA inventado.

---

## Tipos de Aberturas (referencia opcional para inspirar a abertura curta)

A v1 listava 10 tipos de gancho como eixo da newsletter. Na v2, esses tipos viram inspiracao apenas para a **abertura de 40-60 palavras** — o eixo agora e a pergunta-dor + resposta em capitulos. Use os tipos abaixo como referencia se a abertura ficar travada.

### 1. Cena vivida
> "Uma operadora de plano de saude demitiu 30 atendentes em janeiro. Nao por corte de custos — porque o chatbot resolveu 62% dos tickets sozinho."

### 2. Dado surpreendente
> "76% dos consumidores esperam resposta nas redes sociais em ate 24 horas. Apenas 12% das empresas brasileiras conseguem cumprir."

### 3. Conflito
> "O setor diz que IA cuida do volume. Os dados mostram que ela mantem o ticket, mas perde o cliente."

### 4. Contexto direto
> "A discussao da semana voltou a um problema antigo no atendimento omnichannel."

---

## Uso Correto de Conceitos

Se o texto usar um vies cognitivo ou efeito psicologico pelo nome, a descricao deve corresponder a definicao real. Erros comuns e correcoes:

| Conceito (nome correto) | Definicao real | Confundido erroneamente com |
|---|---|---|
| Efeito Spotlight | Superestimar o quanto os outros nos notam (autoconsciencia excessiva) | Projecao de preferencias proprias sobre os outros |
| Vies de Confirmacao | Buscar e lembrar informacoes que confirmam crencas preexistentes | Qualquer distorcao cognitiva generica |
| Vies de Projecao / Efeito do Falso Consenso | Acreditar que os outros pensam, sentem ou preferem o mesmo que nos | Efeito Spotlight |
| Efeito Dunning-Kruger | Incompetentes superestimam sua habilidade; competentes subestimam | Qualquer excesso de confianca |
| Vies de Disponibilidade | Superestimar probabilidade de eventos que vem facilmente a mente | Qualquer forma de pensamento rapido |

**Regra**: se nao tiver certeza da definicao exata, descreva o fenomeno sem usar nome tecnico. Uma descricao precisa sem nome vale mais do que um nome errado.

---

## Checklist Pre-Publicacao

- [ ] Pergunta-eixo definida em `dor-semana.md` e NAO aparece como bloco visivel na NL?
- [ ] Abertura jornalistica (30-50 palavras), sem "imagine que...", "no mundo atual..."?
- [ ] 3 mini-blocos curtos na resposta, cada um com edutainment (analogia/dado/exemplo/definicao)?
- [ ] ≥3 links para o blog proprio?
- [ ] 3-6 links contextuais totais (excluindo rodape)?
- [ ] ≤1 clipping externo, com data ≤ 7 dias?
- [ ] ≤300 palavras no corpo?
- [ ] Frases medias ≤22 palavras?
- [ ] Tom nao-vendedor (max 1 mencao a marca fora dos links de blog)?
- [ ] Anti-IA aplicado (em-dashes, fillers, antiteses-por-negacao em excesso)?
- [ ] Idioma e acentuacao corretos para a regiao?
- [ ] Conceitos nomeados verificados contra definicao real?
- [ ] Dedupe ok (pergunta-dor 6 semanas, links 4 semanas) via `_state.json`?
- [ ] Cases nominais validados contra `### Cases de Sucesso Verificados` do BRANDBOOK?
