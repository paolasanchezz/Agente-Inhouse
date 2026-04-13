---
name: newsletter
description: Guia interativo de geração de newsletters. Faz perguntas com chips clicáveis e dispara a skill correta do pipeline news-*. Usar quando o usuário digitar /newsletter sem saber qual comando rodar.
argument-hint: "(opcional) — texto livre. Ex: /newsletter | /newsletter buzzmonitor brasil | /newsletter 'newsletter da Cxpress pra LATAM'"
allowed-tools: AskUserQuestion, Read, Glob
---

# Skill: /newsletter — Guia interativo de newsletters

Você está executando um **script determinístico**. Não improvise perguntas, não pule passos, não invente opções. Siga exatamente o roteiro abaixo.

## Princípios invioláveis

1. Uma pergunta por vez. Não junte perguntas.
2. Sempre marque a opção recomendada com `(Recomendado)` no label.
3. Antes de cada pergunta, verifique se a resposta já está em `$ARGUMENTS` — se sim, **pule a pergunta**.
4. Antes de disparar a skill final, mostre 1 frase de confirmação e aguarde "sim".
5. Para casos fora de escopo, use as mensagens hardcoded da seção "Fallback".
6. Linguagem: PT-BR coloquial.
7. Você só monta argumentos e delega — toda lógica de newsletter está nas skills `/news-*`.

---

## Passo 0 — Pré-checagens

Nenhuma.

---

## Passo 1 — Pergunta-raiz

Use `AskUserQuestion`:

- **question:** "O que você quer fazer com newsletters?"
- **header:** "Tarefa"
- **multiSelect:** false
- **options:**
  1. label: "Pipeline completo (Recomendado)" — description: "Pesquisa, gera 5 rascunhos e revisa. Fluxo de ponta a ponta — recomendado para newsletter semanal."
  2. label: "Só pesquisar" — description: "Coleta material do blog da marca, notícias do mercado e concorrentes. Não gera rascunho."
  3. label: "Só gerar rascunhos" — description: "Gera os 5 rascunhos a partir da pesquisa já feita. Requer pesquisa anterior."
  4. label: "Só revisar rascunhos" — description: "Revisa e otimiza rascunhos já gerados. Requer rascunhos anteriores."

Guarde como `tarefa`.

### Aviso hardcoded para "Só gerar" e "Só revisar"

Se `tarefa` ∈ {"Só gerar rascunhos", "Só revisar rascunhos"}, exiba **antes** de seguir:

> "Atenção: essa etapa só funciona se `/news-pesquisar` (ou pipeline completo) já tiver sido executado para essa marca/região. Se não foi, é melhor rodar `/news-pipeline` em vez disso."

Não bloqueie — apenas avise. Continue para o Passo 2.

---

## Passo 2 — Coleta de parâmetros (igual para todas as 4 opções)

**2.A Marca** (pular se já em `$ARGUMENTS`):

`AskUserQuestion`:
- question: "Qual marca?"
- header: "Marca"
- multiSelect: false
- options:
  1. "Buzzmonitor (Recomendado)" — "Plataforma de social listening e BI de redes sociais."
  2. "Buzzcreators" — "Plataforma de gestão de campanhas com creators."
  3. "Cxpress" — "Plataforma de atendimento e CX em redes sociais."
  4. "Elife" — "Holding/agência Grupo Elife."

Guarde lowercase: `marca`.

**2.B Região** (pular se já em `$ARGUMENTS`):

`AskUserQuestion`:
- question: "Qual região/idioma?"
- header: "Região"
- multiSelect: false
- options:
  1. "Brasil (PT-BR) (Recomendado)" — "Português brasileiro."
  2. "LATAM (ES-LATAM)" — "Espanhol Latino-Americano."
  3. "Portugal (PT-PT)" — "Português Europeu."

Guarde lowercase: `regiao` ∈ {`brasil`, `latam`, `portugal`}.

---

## Passo 3 — Confirmação e disparo

### Mapeamento `tarefa` → skill

| `tarefa` | Skill final | Argumentos |
|---|---|---|
| Pipeline completo | `/news-pipeline` | `{marca} {regiao}` |
| Só pesquisar | `/news-pesquisar` | `{marca} {regiao}` |
| Só gerar rascunhos | `/news-gerar` | `{marca} {regiao}` |
| Só revisar rascunhos | `/news-revisar` | `{marca} {regiao}` |

### Frase de confirmação (envie literalmente)

> "Vou rodar `/{skill} {marca} {regiao}`. Posso seguir? (responda 'sim' ou ajuste)"

Aguarde resposta. Se "sim" (ou: "vai", "pode", "ok", "manda"), disparar. Se ajuste, voltar ao passo correspondente.

### Disparo (envie literalmente)

> "Execute o fluxo completo da skill `/{skill}` com os argumentos `{marca} {regiao}`. Consulte `.claude/skills/{skill}/SKILL.md` e execute todos os passos na íntegra."

---

## Fallback (mensagens hardcoded)

- **Quer criar uma copy de ad/post:**
  > "Para copy de ad/post/email use `/escrever`. `/newsletter` é só para newsletters do blog."

- **Quer traduzir uma newsletter já pronta:**
  > "Para tradução use `/traduzir` e me passe o arquivo `.md` da newsletter."

- **Marca fora da lista** (qualquer coisa diferente de Buzzmonitor / Buzzcreators / Cxpress / Elife):
  > "As marcas suportadas são Buzzmonitor, Buzzcreators, Cxpress e Elife. Para outra marca, fale com quem mantém o repositório (precisa adicionar arquivo de produto em `conhecimento/produto/`)."

- **Quer agendar a newsletter / publicar direto:**
  > "Eu só gero e reviso o conteúdo (publico no Notion). Agendamento e disparo de email ficam fora desse pipeline — combine com o time."
