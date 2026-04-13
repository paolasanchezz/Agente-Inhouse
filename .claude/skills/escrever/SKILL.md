---
name: escrever
description: Guia interativo de copywriting. Faz perguntas com chips clicáveis e dispara a skill correta do pipeline copy-*. Usar quando o usuário digitar /escrever sem saber qual comando rodar.
argument-hint: "(opcional) — texto livre. Ex: /escrever | /escrever 'quero criar copy de remarketing pra Buzzmonitor'"
allowed-tools: AskUserQuestion, Read, Glob
---

# Skill: /escrever — Guia interativo de copywriting

Você está executando um **script determinístico**. Não improvise perguntas, não pule passos, não invente opções. Siga exatamente o roteiro abaixo.

## Princípios invioláveis

1. Uma pergunta por vez. Não junte perguntas.
2. Sempre marque a opção recomendada com `(Recomendado)` no label.
3. Antes de cada pergunta, verifique se a resposta já está em `$ARGUMENTS` — se sim, **pule a pergunta**.
4. Antes de disparar a skill final, mostre 1 frase de confirmação e aguarde "sim".
5. Para casos fora de escopo, use as mensagens hardcoded da seção "Fallback".
6. Linguagem: PT-BR coloquial.
7. Você só monta argumentos e delega — toda lógica de copy está nas skills `/copy-*`.

---

## Passo 0 — Pré-checagens

Nenhuma.

---

## Passo 1 — Pergunta-raiz

Use `AskUserQuestion`:

- **question:** "O que você quer fazer com copy?"
- **header:** "Tarefa"
- **multiSelect:** false
- **options:**
  1. label: "Criar copy nova (Recomendado)" — description: "Gera 3 variações de copy com hooks e ângulos diferentes a partir de um briefing."
  2. label: "Revisar copy existente" — description: "Revisa qualidade técnica, precisão sobre o produto e linguagem de IA. Corrige automaticamente."
  3. label: "Pesquisar referências" — description: "Coleta exemplos frescos de copy (ads, orgânico, email) de concorrentes e mercado."
  4. label: "Swipe file (banco de referências)" — description: "Adicionar exemplo ao banco ou buscar exemplos salvos."

Guarde como `tarefa`.

---

## Passo 2 — Coleta de parâmetros por fluxo

### Fluxo A — Se `tarefa` == "Criar copy nova"

**A.1 Marca** (pular se já em `$ARGUMENTS`):

`AskUserQuestion`:
- question: "Qual marca?"
- header: "Marca"
- multiSelect: false
- options:
  1. "Buzzmonitor" — "Plataforma de social listening e BI de redes sociais."
  2. "Buzzcreators" — "Plataforma de gestão de campanhas com creators."
  3. "Cxpress" — "Plataforma de atendimento e CX em redes sociais."
  4. "Elife" — "Holding/agência Grupo Elife."

Guarde lowercase: `marca` ∈ {`buzzmonitor`, `buzzcreators`, `cxpress`, `elife`}.

**A.2 Região** (pular se já em `$ARGUMENTS`):

`AskUserQuestion`:
- question: "Qual região/idioma?"
- header: "Região"
- multiSelect: false
- options:
  1. "Brasil (PT-BR) (Recomendado)" — "Português brasileiro."
  2. "Portugal (PT-PT)" — "Português Europeu."
  3. "LATAM (ES-LATAM)" — "Espanhol Latino-Americano."

Guarde lowercase: `regiao` ∈ {`brasil`, `portugal`, `latam`}.

**A.3 Tipo** (pular se já em `$ARGUMENTS`):

`AskUserQuestion`:
- question: "Qual tipo de copy?"
- header: "Tipo"
- multiSelect: false
- options:
  1. "Vídeo curto" — "Reels, TikTok, Shorts. Roteiro com hook + desenvolvimento + CTA."
  2. "Estático" — "Post de feed, banner, criativo de imagem."
  3. "Email" — "Email marketing (assunto + corpo + CTA)."
  4. "Geral" — "Outro formato (LP, anúncio Google, etc.)."

Guarde kebab-case: `tipo` ∈ {`video-curto`, `estatico`, `email`, `geral`}.

**A.4 Estágio do funil** (pular se já em `$ARGUMENTS`):

`AskUserQuestion`:
- question: "Qual estágio do funil?"
- header: "Funil"
- multiSelect: false
- options:
  1. "ToFu (Recomendado)" — "Topo do funil. Descoberta — pessoa ainda não conhece o problema/solução."
  2. "MoFu" — "Meio do funil. Consideração — comparando soluções."
  3. "BoFu" — "Fundo do funil. Decisão, remarketing, lead quente."

Guarde lowercase: `estagio` ∈ {`tofu`, `mofu`, `bofu`}.

**A.5 Briefing** (sempre pergunta — texto livre):

> "Descreva o briefing em uma frase. Ex: 'remarketing para gestores de marketing que clicaram no ebook X' ou 'apresentar Buzzmonitor para agências em LATAM'."

Aguarde resposta. Guarde como `briefing` (string entre aspas).

→ **Disparo:** `/copy-criar {marca} {regiao} {tipo} {estagio} "{briefing}"`

---

### Fluxo B — Se `tarefa` == "Revisar copy existente"

**B.1 Copy a revisar** (texto livre):

> "Cole a copy aqui ou informe o caminho do arquivo (ex: `conhecimento/copywriting/criacao/buzzmonitor/2025-11-04/variacao-1.md`)."

Guarde como `arquivo-ou-texto`.

**B.2 Marca** (pular se já em `$ARGUMENTS`): igual à pergunta A.1.

→ **Disparo:** `/copy-revisar {arquivo-ou-texto} {marca}`

---

### Fluxo C — Se `tarefa` == "Pesquisar referências"

**C.1 Marca:** igual à A.1.

**C.2 País de referência:**

`AskUserQuestion`:
- question: "Qual país de referência?"
- header: "País"
- multiSelect: false
- options:
  1. "Brasil" — "Referências em PT-BR."
  2. "Portugal" — "Referências em PT-PT."
  3. "LATAM" — "Referências em ES-LATAM."

Guarde como `pais`.

**C.3 Tipo:** igual à A.3.

→ **Disparo:** `/copy-pesquisar {marca} {pais} {tipo}`

---

### Fluxo D — Se `tarefa` == "Swipe file"

**D.1 Ação:**

`AskUserQuestion`:
- question: "O que fazer no swipe file?"
- header: "Ação"
- multiSelect: false
- options:
  1. "Adicionar exemplo" — "Salvar uma copy/URL no banco de referências."
  2. "Buscar exemplo" — "Procurar exemplos já salvos por tema."

Guarde como `acao`.

**D.2 Conteúdo (texto livre):**

- Se `acao` == "Adicionar exemplo": pergunte > "Cole a URL ou o texto da copy a salvar."
- Se `acao` == "Buscar exemplo": pergunte > "Qual tema/palavra-chave buscar? (ex: 'remarketing', 'video curto BoFu')"

Guarde como `conteudo`.

→ **Disparo:**
- Se "Adicionar": `/copy-swipefile add {conteudo}`
- Se "Buscar": `/copy-swipefile buscar {conteudo}`

---

## Passo 3 — Confirmação e disparo (todos os fluxos)

### Frase de confirmação (envie literalmente)

> "Vou rodar `/{skill} {argumentos}`. Posso seguir? (responda 'sim' ou ajuste)"

Aguarde resposta. Se "sim" (ou: "vai", "pode", "ok", "manda"), disparar. Se ajuste, voltar ao passo correspondente.

### Disparo (envie literalmente)

> "Execute o fluxo completo da skill `/{skill}` com os argumentos `{argumentos}`. Consulte `.claude/skills/{skill}/SKILL.md` e execute todos os passos na íntegra."

---

## Fallback (mensagens hardcoded)

- **Quer traduzir uma copy:**
  > "Para tradução use `/traduzir`. `/escrever` é só para criar/revisar/pesquisar copy original."

- **Quer criar newsletter:**
  > "Para newsletters use `/newsletter`. `/escrever` é para copys de ad/post/email — não para newsletters do blog."

- **Quer analisar performance da copy:**
  > "Para análise de performance de anúncios use `/anuncios`. Eu só ajudo a escrever — não meço resultado."

- **Marca fora da lista** (qualquer coisa diferente das 4):
  > "As marcas suportadas são Buzzmonitor, Buzzcreators, Cxpress e Elife. Para outra marca, fale com quem mantém o repositório (precisa adicionar arquivo de produto em `conhecimento/produto/`)."
