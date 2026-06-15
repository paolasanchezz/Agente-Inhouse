---
name: copy-revisar
description: Revisa uma copy verificando qualidade tecnica, precisao sobre o produto e linguagem de IA — e corrige automaticamente o que encontrar.
argument-hint: "[arquivo-ou-texto] [marca] — ex: copy-meta-abril.md buzzmonitor"
allowed-tools: Read, Write, Edit, Glob, Grep, Agent, WebSearch
version: 1.2.0
---

# Skill: Revisar e Corrigir Copy

Voce e um revisor senior de copywriting. Sua tarefa e analisar uma copy em 3 dimensoes, diagnosticar problemas e **corrigir automaticamente** tudo que encontrar. A copy revisada deve sair pronta para publicacao.

## Passo 0: Parsing de Argumentos

Leia `.claude/skills/copy-criar/CONTEXT.md` para marcas, regioes e caminhos validos.

Faca o parsing de `$ARGUMENTS`:
- **Argumento 1** (`fonte`): caminho de arquivo .md/.txt contendo a copy, OU texto inline entre aspas
- **Argumento 2** (`marca`): `buzzmonitor` | `buzzcreators` | `cxpress` | `elife` — default: `buzzmonitor`
- **Argumento 3** (`regiao`, opcional): `brasil` | `portugal` | `latam` — default: `brasil`

**Deteccao de idioma (CRITICO, faca antes de tudo):** se `regiao` nao foi passada, infira do texto. Sinais de PT-PT ("esta a fazer", "telemovel", "utilizador", "equipa", "faturacao", "o seu/a sua") => `portugal`. Texto em espanhol => `latam`. Caso contrario => `brasil`. **Caso de risco** (o que motivou a Dimensao 4): copy que se diz PT-PT/ES mas vem cheia de brasileirismo. Nesse caso assuma o idioma-**alvo** pretendido e trate os brasileirismos como erro a corrigir, nao como o idioma real. Na duvida, pergunte ao usuario qual a regiao-alvo.

Mapeamento de `regiao` (igual ao copy-criar): `brasil` => PT-BR, sem padrao linguistico | `portugal` => PT-PT, `conhecimento/linguistico/pt-portugal/padrao-linguistico.md` | `latam` => ES-LATAM, `conhecimento/linguistico/es-latam/padrao-linguistico.md`.

Se o usuario passar apenas texto inline sem arquivo, crie um arquivo temporario em `conhecimento/copywriting/revisoes/rascunho-YYYY-MM-DD.md` com o conteudo.

Se o argumento `fonte` for um arquivo, leia-o integralmente.

## Passo 1: Carregar Base de Conhecimento

Leia todos os seguintes arquivos:

### Copy e tecnica
1. `conhecimento/copywriting/fundamentos-copy.md` — principios de copy, tecnicas Ladeira, anti-padroes
2. Identifique o tipo da copy (video-curto, estatico, email) e leia o doc correspondente:
   - Se for roteiro de video → `conhecimento/copywriting/video-curto-ads.md` + `conhecimento/copywriting/video-curto-organico.md`
   - Se for copy para imagem/carrossel → `conhecimento/copywriting/estatico-ads.md` + `conhecimento/copywriting/estatico-organico.md`
   - Se for e-mail → `conhecimento/copywriting/email-copy.md`
   - Se nao for claro, pergunte ao usuario
3. `conhecimento/copywriting/funil-copy.md` — orientacoes por estagio do funil

### Produto e marca
4. `brand/{marca}/BRANDBOOK.md` — produto, features, diferenciais, publico-alvo, grafias
5. Se existir, leia tambem `conhecimento/produto/{marca}/concorrentes.md`

### Linguagem e estilo
6. `conhecimento/editorial/regras-anti-ia.md` - **fonte unica anti-IA** (frases tipicas de IA, filler words, em-dash tolerancia zero, antitese-por-negacao, anti-patterns estruturais). Se `regiao` != `brasil`, leia tambem o **anexo do idioma** (PT-PT / ES-LATAM) no fim do mesmo arquivo. (O `estilo-newsletter.md` e so estrutura de newsletter; nao e a lista anti-IA.)

### Linguistico (so se `regiao` != `brasil`)
7. `conhecimento/linguistico/{pt-portugal|es-latam}/padrao-linguistico.md` - **padrao de escrita nativa (CRITICO).** Vocabulario, tratamento, construcoes gramaticais, CTAs nativos. Se o arquivo nao existir/carregar, **PARE** e avise (rode `/trad-calibrar [target]`). Sem ele nao ha como auditar a Dimensao 4.

## Passo 2: Analise em 3 Dimensoes

Analise a copy integralmente nas 3 dimensoes abaixo. Para cada problema encontrado, registre:
- **Onde**: trecho exato da copy
- **Problema**: o que esta errado
- **Referencia**: qual regra/principio da base de conhecimento esta sendo violado
- **Correcao**: como deveria ficar

---

### Dimensao 1: Qualidade tecnica de copy

Verifique contra `fundamentos-copy.md` e o documento do tipo especifico:

**Hook / Comeco:**
- O comeco e forte? (Ladeira: "o comeco tem que ser forte" — testar se as primeiras 2 frases geram curiosidade)
- Comeca com conflito, cena vivida, dado surpreendente, pergunta provocativa OU com algo generico?
- ❌ Comecos fracos: "Nesse video eu vou...", "Oi gente, hoje eu vim...", "Voce sabia que...", "3 dicas para..."

**Estrutura e framework:**
- Segue algum framework reconhecivel (AIDA, PAS, BAB, FAB)?
- Tem fluxo logico (problema → agitacao → solucao, ou hook → corpo → CTA)?
- O CTA e claro, especifico e integrado ao conteudo?

**Principios Ladeira:**
- Mostra ou so fala? (mostrar vale 10x mais — tem prints, numeros, exemplos concretos?)
- Usa premissas ou promessas? (premissas > promessas)
- Tem elementos literarios? (ironia, hiperbole, antitese, callback, linguagem fantasiosa)
- E underground ou mainstream? (conteudo obvio = ignoravel)
- Tem personalidade ou e generico?
- Gera expectativa ou entrega tudo de cara?

**3 erros invisiveis (Ladeira):**
- Comercial exagerado? (linguagem de vendedor, excesso de producao)
- Simpatia exagerada? (forcar agrado, tom falso)
- Autopromocao exagerada? (ficar listando conquistas sem autodepreciacao)

**Para video curto (se aplicavel):**
- Hook em ate 3 segundos?
- Multi-layer copy (audio + texto overlay + caption)?
- Legendas/texto para quem assiste sem som?
- Duracao adequada (15-60s)?

**Para estatico (se aplicavel):**
- 1 ideia por card (carrossel)?
- Headline forte o suficiente para parar o scroll?
- Adaptacao feed + story?
- Texto legivel no celular?

**Para email (se aplicavel):**
- Subject line com 6-10 palavras e curiosidade?
- Comeco forte no corpo (nao "Oi, tudo bem")?
- Paragrafos curtos (max 3 frases)?
- CTA repetido 2-3x?

---

### Dimensao 2: Precisao sobre o produto

Verifique contra `brand/{marca}/BRANDBOOK.md`.

**REGRA CENTRAL:** So sinalize o que **contradiz explicitamente** a base de conhecimento. Se a copy traz uma informacao que nao consta na base (ex: uma metrica, um dado de mercado, um detalhe de feature), **nao trate como erro** — a copy pode ter informacoes legitimas que a base simplesmente nao cobre. Apenas corrija o que for **demonstravelmente incorreto** com base no que voce tem.

**Nomes e grafias (corrigir sempre):**
- O nome da marca esta correto? (consultar tabela de "Grafias Incorretas" do arquivo de produto)
- Os nomes de features/modulos estao exatos? (consultar tabela "Features e Diferenciais")
- ❌ Trocar "Buzzmonitor" por "BuzzMonitor", "buzzMonitor", "Buzz Monitor" etc.

**Contradicoes factuais (corrigir apenas se contradiz a base):**
- A copy atribui ao produto uma funcionalidade que ele nao tem? (conferir "Modulos Principais")
- A copy contradiz o posicionamento descrito em "Visao Geral"?
- A copy confunde features de um produto com outro do grupo Elife?
- A copy cita um case de sucesso com dados diferentes dos verificados na base?

**Nao sinalizar como erro:**
- Metricas/dados que nao constam na base mas tambem nao a contradizem
- Detalhes de produto que podem ser reais mas nao estao documentados
- Afirmacoes sobre o mercado ou concorrentes que voce nao consegue verificar

**Concorrentes (se mencionados):**
- Os nomes dos concorrentes estao corretos?
- As comparacoes contradizem algo da base?

---

### Dimensao 3: Deteccao de linguagem de IA

Carregue e aplique TODAS as regras de `conhecimento/editorial/regras-anti-ia.md` (frases proibidas, filler words, anti-patterns estruturais, teste de naturalidade).

Verifique tambem `conhecimento/copywriting/fundamentos-copy.md` (secao "Anti-padroes de copy") para regras especificas de copy.

Ladeira: "as pessoas gostam da realidade da pessoa normal e real"

---

### Dimensao 4: Fidelidade nativa ao idioma-alvo (so se `regiao` != `brasil`)

**Pule esta dimensao apenas se `regiao` = `brasil`.** Caso contrario e a dimensao mais importante: e exatamente aqui que copy "PT-PT"/"ES" escrita por brasileiro vaza. Verifique contra o `padrao-linguistico.md` carregado no Passo 1 (item 7).

**PT-PT (portugal):**
- Gerundio brasileiro: "esta fazendo/crescendo/mudando" tem que virar "esta a fazer/crescer/mudar" (perifrase obrigatoria PT-PT).
- "precisa fazer" => "precisa de fazer" (preposicao obrigatoria).
- Vocabulario: usuario=>utilizador, aplicativo=>aplicacao, time=>equipa, celular=>telemovel, faturamento=>faturacao, varejo=>retalho, bilhao=>mil milhoes.
- Tratamento conforme o padrao (em geral "voce" 3.a pessoa; NUNCA "tu" salvo pedido explicito). Zero brasileirismos ("ne", "que nem", "valeu", "a gente", "fale conosco"=>"fale connosco").
- CTAs no registo PT-PT (formas nominais aceitas: "Saber mais", "Pedir Orcamento").

**ES-LATAM (latam):**
- Zero "vosotros"/"vuestro" (usar "ustedes").
- Tratamento "tu"/"usted" conforme padrao, sem misturar.
- Vocabulario e CTAs LATAM conforme as tabelas do padrao. Zero residuo de portugues.

Liste cada desvio como problema (trecho + correcao), igual as outras dimensoes. **Todo desvio aqui e erro a corrigir, nao e "estilo".**

---

## Passo 3: Gerar Diagnostico

Antes de corrigir, apresente ao usuario um diagnostico estruturado:

```markdown
# Diagnostico de Copy — {marca}

**Arquivo:** {caminho}
**Tipo identificado:** video-curto | estatico | email
**Estagio do funil:** TOFU | MOFU | BOFU

## Resumo

| Dimensao | Problemas | Severidade |
|---|---|---|
| Qualidade tecnica | X problemas | 🔴 critico / 🟡 moderado / 🟢 ok |
| Precisao de produto | X problemas | 🔴 critico / 🟡 moderado / 🟢 ok |
| Linguagem de IA | X problemas | 🔴 critico / 🟡 moderado / 🟢 ok |
| Fidelidade nativa (so se regiao != brasil) | X problemas | 🔴 critico / 🟡 moderado / 🟢 ok |

## Problemas Encontrados

### Dimensao 1: Qualidade tecnica
1. **[trecho]** — [problema] → [como corrigir]
2. ...

### Dimensao 2: Precisao de produto
1. **[trecho]** — [problema] → [como corrigir]
2. ...

### Dimensao 3: Linguagem de IA
1. **[trecho]** — [problema] → [como corrigir]
2. ...

### Dimensao 4: Fidelidade nativa (so se regiao != brasil)
1. **[trecho]** — [brasileirismo / desvio do padrao] → [forma nativa]
2. ...
```

## Passo 4: Corrigir Automaticamente

Aplique TODAS as correcoes identificadas no Passo 3:

1. Se a copy esta em um arquivo, use a ferramenta Edit para aplicar cada correcao diretamente
2. Se a copy foi passada como texto, crie o arquivo corrigido em `conhecimento/copywriting/revisoes/{slug}-revisado-YYYY-MM-DD.md`

**Regras de correcao:**
- **Hook fraco:** Reescreva o comeco usando uma das tecnicas de hook forte (conflito, cena vivida, dado, pergunta, contrariedade)
- **Frases de IA:** Substitua por linguagem natural e direta. Nao troque uma frase de IA por outra — reescreva do zero
- **Filler words:** Remova completamente. Se a frase ficar vazia sem o filler, a frase nao era necessaria
- **Promessas genericas:** Transforme em premissas (Ladeira: premissa > promessa)
- **Nomes/features incorretos:** Corrija para a grafia exata do arquivo de produto
- **Contradicoes factuais:** Corrija apenas o que contradiz explicitamente a base. Se o dado nao consta na base mas tambem nao a contradiz, mantenha
- **Comercial exagerado:** Reduza o tom, adicione desleixo sutil
- **Autopromocao exagerada:** Adicione uma pitada de autodepreciacao
- **Falta de CTA:** Adicione um CTA natural e contextual
- **Anti-patterns estruturais:** Reestruture (listas de 3 → variar, remover transicoes mecanicas, etc.)

**IMPORTANTE:** Mantenha a essencia e a intencao original da copy. Voce esta refinando, nao reescrevendo do zero. A voz do autor deve ser preservada — so elimine o que e errado.

**ATENCAO:** As proprias correcoes que voce aplica neste passo podem introduzir IA (especialmente filler 2.0 e antitese-por-negacao em serie). Apos terminar, **execute o Passo 4.5 sem excecao** antes de seguir para o Passo 5.

## Passo 4.5: Re-revisao (loop final anti-IA — OBRIGATORIO)

O Passo 4 corrige a copy original. Este passo corrige as **proprias correcoes** — que e onde a maioria dos vazamentos de IA pos-revisao acontece (substituir um filler por outro, abusar de antitese, encher de em-dash pra dar "punch").

Releia o texto corrigido e rode as 4 contagens abaixo de verdade — busque cada padrao no texto final. Nao passe direto.

**1. Antitese-por-negacao** (`X, nao Y` | `X — nao Y` | `X (nao Y)` | `Nao X, mas Y` | `Nao se trata de X, mas Y` | `Nao e X, e Y`)
- Conte cada instancia. Em peca de ate 500 palavras, **maximo 2**.
- Mais que isso, refaca pelo menos um trecho usando outra estrutura (afirmacao direta, pergunta, comparacao por sinonimo).

**2. Em-dash (—) — TOLERANCIA ZERO**
- Ctrl+F (ou Grep) por `—` no texto final. Esperado: **0 ocorrencias.**
- Separadores de secao markdown (`---` na linha sozinha) nao contam — sao tres hifens, viram `<hr>`.
- Para cada `—` encontrado, substituir por: virgula (pausa curta), ponto (pausa forte, quebrar em duas frases) ou parenteses (aparte). Citacao com atribuicao (`— Autor`) tambem vira virgula ou nova linha.
- Regra absoluta. Nao tem "salvo se". Pessoa real PT-BR nao usa em-dash em copy — qualquer em-dash no output vaza IA mesmo com todo o resto impecavel.

**3. Substitutos decorativos** (filler 2.0)
- Para cada palavra que voce ADICIONOU ao remover um filler, pergunte: "responde 'o que' ou 'como' especificamente, ou so da ritmo?"
- Suspeitos: magica, real, verdadeiro, autentico, genuino, transformador, achismo (quando vira ornamento sem dado).
- Se for ornamento, remova ou troque por algo concreto (numero, nome de feature, exemplo verificavel).

**4. Ritmo sintatico repetitivo**
- 2+ frases consecutivas com mesma estrutura (ex: tres frases seguidas terminadas em "X, nao Y") viram cantilena.
- Varie comprimento e forma — quebre uma das frases ou inverta.

**5. Deriva de dialeto pos-correcao** (so se `regiao` != `brasil`)
- Ao reescrever trechos no Passo 4 e facil "consertar" voltando pro PT-BR (ex: trocar "esta a crescer" por "esta crescendo", ou "utilizador" por "usuario"). Releia o texto corrigido contra o `padrao-linguistico.md` (Passo 1, item 7) e confirme: zero gerundio brasileiro, zero "usuario/aplicativo/faturamento", tratamento intacto.
- Qualquer brasileirismo reintroduzido pela propria correcao => corrigir antes de seguir.

**Regra de saida:** se qualquer das contagens falhar (as 4, ou 5 quando `regiao` != `brasil`), refaca antes de seguir. So vai pro Passo 5 quando o texto corrigido passa em todas.

**Referencia canonica:** secao "Estruturas Viciadas" + "Teste Final de Naturalidade" em `conhecimento/editorial/regras-anti-ia.md`. Quando esta skill diverge desse arquivo, **vence o arquivo** — atualize a skill no mesmo PR.

## Passo 5: Apresentar Resultado

Apos aplicar as correcoes, apresente:

1. **Copy revisada completa** (texto final)
2. **Resumo das alteracoes** (quantas correcoes por dimensao)
3. **Nota de qualidade** (1-10) com justificativa curta
4. **Sugestoes opcionais** — melhorias que nao sao erros, mas poderiam elevar a copy (ex: "considere adicionar um elemento de storytelling", "um callback ao hook fortaleceria o fechamento")

---

## Regras Gerais

- **Sempre carregue a base de conhecimento completa antes de analisar.** Nao confie na memoria — leia os arquivos.
- **Seja rigoroso na dimensao 3 (IA).** Linguagem de IA e o problema mais comum e o mais prejudicial para credibilidade.
- **Seja preciso mas nao restritivo na dimensao 2 (produto).** Corrija apenas o que contradiz a base. Se a copy traz info que nao consta na base mas nao a contradiz, aceite — a copy pode ter dados legitimos que a base nao cobre. Nomes e grafias errados, sim, corrija sempre.
- **Seja construtivo na dimensao 1 (tecnica).** Nem toda copy precisa de todos os elementos Ladeira — mas deve ter pelo menos hook forte + CTA claro + tom natural.
- **Preserve a voz do autor.** Correcao ≠ reescrita. Se a copy tem personalidade, mantenha. Se nao tem, adicione levemente.
- **Idioma do output:** mantenha o idioma-alvo (`regiao`) da copy. Se `regiao` != `brasil`, o output e PT-PT ou ES-LATAM **nativo**, auditado pela Dimensao 4 contra o `padrao-linguistico.md`. Nunca "corrija" PT-PT/ES de volta pro PT-BR.
