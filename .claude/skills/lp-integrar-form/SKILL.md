---
name: lp-integrar-form
description: Substitui o form mock de uma LP por embed real (Jotform, RD Station, HubSpot ou outro). Manual-trigger — so rodar apos design aprovado (GUIDELINES §11).
argument-hint: "[marca]/[slug] \"snippet HTML do embed\" — ex: buzzmonitor/monitoramento-maio \"<script src=...jotform.com/jsform/...></script>\""
allowed-tools: Read, Edit, Glob, Grep
version: 1.5.0
---

# Skill: Integrar Formulario em Landing Page

Substitui o form mock (`<form action="#">`) por um embed externo. Aplica o CSS wrapper canonico para manter layout. **Nao roda dentro do pipeline** — usuario invoca manualmente quando o design esta aprovado.

## Passo 0.0: Sincronizar o repo (v1.4.0 — migracao CI)

Antes de ler ou editar qualquer arquivo, atualize a working tree — o repo e compartilhado
e, com o deploy via CI (PLANO-MIGRACAO-CI.md), outras pessoas publicam LPs por PR direto
na main. Editar em cima de copia velha gera conflito evitavel no PR.

```bash
git pull --rebase --autostash 2>&1 | tail -2 && git branch --show-current
```

Se o rebase conflitar: `git rebase --abort`, avise o usuario e resolva antes de editar.
Nao siga com a skill em working tree desatualizada.

## Passo 0: Parsing e Contexto

Leia, na ordem:

1. `landing-pages/CONTEXT.md` — runbook operacional. Use principalmente §6 (troubleshooting) — entradas "Form nao carrega no live", "Form duplicado / erro no console".
2. `.claude/skills/lp-preparar/CONTEXT.md` — convencoes de marca.

Parsing de `$ARGUMENTS`:

| Argumento | Formato | Obrigatorio |
|---|---|---|
| `target` | `{marca}/{slug}` ou `{marca} {slug}` | Sim |
| `snippet` | HTML do embed, entre aspas | Sim |

Normalize target para `landing-pages/{marca}/{slug}/index.html`. Se nao existe, PARE.

### Identificar provedor (heuristica do snippet)

- Contem `jotform.com` → Jotform
- Contem `rdstation` → RD Station
- Contem `hsforms.net` ou `hubspot` → HubSpot
- Outro → "embed generico"

So serve para rotular o log. Nao muda a logica de substituicao.

## Passo 1: Localizar Form Mock

Grep em `landing-pages/{marca}/{slug}/index.html`:

- Procurar `<form` (primeira ocorrencia com `action="#"` ou com classe `form` que contenha `onsubmit="event.preventDefault()"`).
- Capturar do `<form` ate o `</form>` correspondente (incluindo atributos e filhos).

Se nao encontrar form mock — talvez ja tenha embed. PARE e avise o usuario: "LP parece ja ter form integrado. Reverter para mock primeiro se quiser trocar."

## Passo 2: Substituir pelo Embed

Use `Edit` para trocar o bloco `<form ... >...</form>` por:

```html
<div class="jotform-embed" {preservar_data_attrs_se_houver}>
  {snippet}
</div>
```

Observacoes:
- A classe `jotform-embed` vale para qualquer provedor (ativa o wrapper CSS canonico). Nao renomear por provedor.
- **Jotform (`jsform`): incluir tambem o shim de `url` do Passo 2.2.** Sem ele o lead chega sem URL de conversao.
- **NAO** herdar a classe `form` do mock. O `.form` no `lp-gerar` e um card visual (`background: #fff`, `padding: 40px`, `border`, `box-shadow`) e os provedores (Jotform/RD/HubSpot) ja vem com card proprio — manter `form` causa "card dentro de card" no live (incidente 2026-04-30).
- Preserve animacao reveal: se o form mock tinha `class="form reveal"` com `style="--d: XXms"`, replicar **apenas o `reveal` + `style`** no `<div>` wrapper (descartar o `form`).

## Passo 2.2: Shim de URL de conversao (v1.5.0 — so Jotform `jsform`)

O script `jsform` monta a query do iframe com **a query string da LP** + `parentURL` + o que
estiver em `window.qsProxy` (`FrameBuilder.get = qsProxy`). Resultado: UTM funciona (vem na URL
do anuncio), mas o campo `url` do form **chega vazio** — e o campo interno que grava a URL da
pagina guarda `form.jotform.com/...`, nao a LP. Lead entra no CRM sem `url_conversao`
(diagnosticado em 2026-08-11 na `buzzmonitor/mcp-es`).

Se o snippet e Jotform `jsform`, insira **antes** do `<script src=...>`, dentro do mesmo wrapper:

```html
<script type="text/javascript">
  /* Entrega a URL da LP ao campo "url" do Jotform (vira url_conversao no CRM).
     Sem isso o campo chega vazio e a conversao fica sem origem.
     Accessor em vez de atribuicao simples: o proprio jsform roda
     "var qsProxy = {}" e sobrescreveria um valor atribuido direto. */
  Object.defineProperty(window, 'qsProxy', {
    configurable: true,
    get: function () { return { url: location.origin + location.pathname }; },
    set: function () {}
  });
</script>
```

Regras:
- **Nao** trocar por `var qsProxy = {...}` — o jsform sobrescreve e o shim vira no-op (testado).
- `origin + pathname` de proposito: URL limpa, sem `fbclid`/UTM sujando o `url_conversao`. Os UTM
  ja viajam nos campos proprios (`utm_source`, `utm_medium`, ...), preenchidos pela query da LP.
- `qsProxy` e global: se a LP tiver dois embeds Jotform, um shim so — nao duplicar o bloco.
- Nao se aplica a RD Station / HubSpot / embed generico. Nesses, pular este passo.
- Isso garante o campo preenchido **no Jotform**. Se o mapeamento Jotform -> ActiveCampaign nao
  ler esse campo, a dashboard continua sem enxergar — checar com o Victor, nao mexer na automacao
  por conta propria.

Como validar depois do deploy (console da LP no ar):

```js
document.querySelector('.jotform-embed iframe').src.includes('&url=')
```

## Passo 2.5: Remover JS placeholder do form

O `lp-gerar` inclui um bloco JS placeholder que escuta `submit` no `<form>` mock (mostra "Inscricao registrada", valida campos, etc). Com o embed real, esse form nao existe mais como `<form>` na pagina (Jotform/HubSpot renderizam via iframe) — `document.querySelector('form')` retorna `null` e dispara `Cannot read properties of null (reading 'addEventListener')` no console.

Grep em `<script>` inline por `querySelector('form')` ou `addEventListener('submit'`. Se encontrar, remover o bloco inteiro — do comentario `// Placeholder form` (se existir) ou da linha `var form = document.querySelector('form');` ate o `});` de fechamento do handler de submit.

Nao confundir com outros scripts da LP (reveal on scroll, countdown, etc). So remover o handler do form.

## Passo 3: Garantir CSS Wrapper

Grep no `<style>` inline por `.jotform-embed iframe`. Se **nao** existe, inserir no final do `<style>`:

```css
/* ----- Jotform embed wrapper (canonico) -----
   Sem padding/background/border: o provedor ja vem com card proprio.
   A regra do iframe garante que, se o provedor renderizar via iframe, ele
   ocupa 100% da largura sem borda. */
.jotform-embed iframe { width: 100% !important; max-width: 100% !important; border: 0; display: block; }
```

Se ja existe regra antiga `.form.jotform-embed { padding... }` (versao <=1.2.0), substituir pela versao acima — a regra antiga adiciona um card visual extra que colide com o card do provedor (incidente 2026-04-30).

Se ja existe a versao nova, nao duplicar.

## Passo 4: Atualizar README

Em `landing-pages/{marca}/{slug}/README.md`:

- Marcar checkbox `- [x] Formulario integrado` (se a secao existir).
- Adicionar linha: `**Form provider:** {provedor identificado} ({data integracao})`

Se o README nao existe, criar minimalista com essas informacoes.

## Passo 5: Relatorio Final

```
Form integrado — {marca}/{slug}

Provedor: {provedor}
Form mock substituido: sim
Wrapper CSS: aplicado ({"novo" ou "ja existia"})
Shim de URL de conversao: {"aplicado" | "nao se aplica (provedor != Jotform jsform)"}

Arquivo: landing-pages/{marca}/{slug}/index.html

Testar antes de publicar:
1. Abrir index.html no browser local
2. Conferir que iframe carrega dentro do wrapper (sem overflow)
3. Submeter form-teste para ver resposta do provedor
4. Jotform: conferir no console que a src do iframe traz `&url=` (Passo 2.2)

Proximo: /lp-publicar {marca} {slug} [dominio]
```

## Notas

- Nao validar o snippet (nao fazer HTTP request para ver se URL e valida — risco de bloquear por CSP ou timeout).
- Nao configurar CSP automaticamente — embeds externos + CSP estrito e complicado, deixar para ajuste manual caso usuario queira endurecer.
- Se o usuario quiser reverter: `Edit` manual (trocar wrapper por `<form action="#" onsubmit="event.preventDefault()">` novamente).
- GTM e responsabilidade de `lp-revisar` (Passo 3.5). Se a LP nao foi revisada antes, rode `/lp-revisar {marca}/{slug}` — ele injeta/corrige o snippet certo para marca+regiao.
