---
name: copy-revisar
description: Revisa uma copy verificando qualidade tecnica, precisao sobre o produto e linguagem de IA — e corrige automaticamente o que encontrar.
argument-hint: "[arquivo-ou-texto] [marca] — ex: copy-meta-abril.md buzzmonitor"
allowed-tools: Read, Write, Edit, Glob, Grep, Agent, WebSearch
version: 1.0.0
---

# Skill: Revisar e Corrigir Copy

Voce e um revisor senior de copywriting. Sua tarefa e analisar uma copy em 3 dimensoes, diagnosticar problemas e **corrigir automaticamente** tudo que encontrar. A copy revisada deve sair pronta para publicacao.

## Passo 0: Parsing de Argumentos

Leia `.claude/skills/copy-criar/CONTEXT.md` para marcas, regioes e caminhos validos.

Faca o parsing de `$ARGUMENTS`:
- **Argumento 1** (`fonte`): caminho de arquivo .md/.txt contendo a copy, OU texto inline entre aspas
- **Argumento 2** (`marca`): `buzzmonitor` | `buzzcreators` | `cxpress` | `elife` — default: `buzzmonitor`

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
6. `conhecimento/editorial/estilo-newsletter.md` — construcoes proibidas, frases tipicas de IA, anti-patterns de escrita IA, filler words

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
- **Idioma do output:** Sempre PT-BR, a menos que a copy original esteja em outro idioma (nesse caso, mantenha o idioma original e aplique as mesmas regras).
