---
name: traduzir
description: Guia interativo de tradução. Faz perguntas com chips clicáveis e dispara a skill correta do pipeline trad-*. Usar quando o usuário digitar /traduzir sem saber qual comando rodar.
argument-hint: "(opcional) — texto livre. Ex: /traduzir | /traduzir copy.md pt-pt | /traduzir 'tenho uma copy em PT pra LATAM'"
allowed-tools: AskUserQuestion, Read, Glob
---

# Skill: /traduzir — Guia interativo de tradução

Você está executando um **script determinístico**. Não improvise perguntas, não pule passos, não invente opções. Siga exatamente o roteiro abaixo.

## Princípios invioláveis

1. Uma pergunta por vez. Não junte perguntas.
2. Sempre marque a opção recomendada com `(Recomendado)` no label.
3. Antes de cada pergunta, verifique se a resposta já está em `$ARGUMENTS` — se sim, **pule a pergunta**.
4. Antes de disparar a skill final, mostre 1 frase de confirmação e aguarde "sim".
5. Para casos fora de escopo, use as mensagens hardcoded da seção "Fallback".
6. Linguagem: PT-BR coloquial.
7. Você só monta argumentos e delega — toda lógica de tradução está nas skills `/trad-*`.

---

## Passo 0 — Pré-checagens

Nenhuma.

---

## Passo 1 — Pergunta-raiz

Use `AskUserQuestion` com exatamente este conteúdo:

- **question:** "O que você quer fazer com tradução?"
- **header:** "Tarefa"
- **multiSelect:** false
- **options:**
  1. label: "Traduzir + revisar (Recomendado)" — description: "Traduz a copy e revisa como nativo, publica no Notion. Fluxo completo."
  2. label: "Só traduzir" — description: "Apenas traduz, sem revisão final."
  3. label: "Só revisar tradução" — description: "Você já tem a tradução pronta e quer só a revisão nativa."
  4. label: "Calibrar idioma" — description: "Atualiza o padrão linguístico (vocabulário, expressões) de PT-PT ou ES-LATAM."

Guarde a resposta como `tarefa`.

---

## Passo 2 — Coleta de parâmetros

### Se `tarefa` ∈ {"Traduzir + revisar", "Só traduzir", "Só revisar tradução"}:

**2.A — Arquivo** (se não veio em `$ARGUMENTS` como `.md` ou caminho):

Pergunte em texto livre (sem `AskUserQuestion`):
> "Qual o caminho do arquivo a traduzir? (ex: `traducao/copy-buzzmonitor.md`)"

Aguarde resposta. Guarde como `arquivo`.

**2.B — Idioma alvo** (se não veio em `$ARGUMENTS` como `pt-pt` ou `es-latam`):

Use `AskUserQuestion`:
- **question:** "Para qual idioma traduzir?"
- **header:** "Idioma"
- **multiSelect:** false
- **options:**
  1. label: "PT-PT" — description: "Português Europeu (Portugal)."
  2. label: "ES-LATAM" — description: "Espanhol Latino-Americano."

Guarde como `target` (formato lowercase: `pt-pt` ou `es-latam`).

### Se `tarefa` == "Calibrar idioma":

Use `AskUserQuestion`:
- **question:** "Qual idioma calibrar?"
- **header:** "Idioma"
- **multiSelect:** false
- **options:**
  1. label: "PT-PT" — description: "Português Europeu (Portugal)."
  2. label: "ES-LATAM" — description: "Espanhol Latino-Americano."

Guarde como `target`.

---

## Passo 3 — Confirmação e disparo

### Mapeamento `tarefa` → skill

| `tarefa` | Skill final | Argumentos |
|---|---|---|
| Traduzir + revisar | `/trad-pipeline` | `{arquivo} {target}` |
| Só traduzir | `/trad-traduzir` | `{arquivo} {target}` |
| Só revisar tradução | `/trad-revisar` | `{arquivo} {target}` |
| Calibrar idioma | `/trad-calibrar` | `{target}` |

### Frase de confirmação (envie literalmente, substituindo `{...}`)

> "Vou rodar `/{skill} {argumentos}`. Posso seguir? (responda 'sim' ou ajuste)"

Aguarde resposta. Se "sim" (ou equivalente: "vai", "pode", "ok", "manda"), disparar. Se ajuste, voltar ao passo correspondente.

### Disparo (envie literalmente)

> "Execute o fluxo completo da skill `/{skill}` com os argumentos `{argumentos}`. Consulte `.claude/skills/{skill}/SKILL.md` e execute todos os passos na íntegra."

---

## Fallback (mensagens hardcoded)

Se em qualquer momento o usuário pedir algo fora de escopo, responda exatamente:

- **Idioma diferente de PT-PT/ES-LATAM** (inglês, francês, alemão, etc.):
  > "Esse pipeline só suporta PT-PT (Português de Portugal) e ES-LATAM (Espanhol Latino-Americano). Para outros idiomas, ainda não temos skill — fale com o time de copy."

- **Arquivo não-texto** (PDF, imagem, vídeo):
  > "Hoje só processo arquivos `.md` ou texto colado. Cole o texto direto no chat ou converta o PDF para markdown primeiro."

- **Quer criar copy do zero**:
  > "Para criar copy nova use `/escrever`. Eu só traduzo copy que já existe."

- **Quer traduzir newsletter**:
  > "Newsletters já são geradas no idioma certo pelo `/newsletter [marca] [região]`. Se você tem uma newsletter pronta em PT-BR e quer ela em PT-PT/ES-LATAM, eu posso — me passe o arquivo `.md`."
