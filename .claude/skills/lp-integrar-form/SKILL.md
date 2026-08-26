---
name: lp-integrar-form
description: Substitui o form mock de uma LP por embed real (Jotform, RD Station, HubSpot ou outro). Manual-trigger — so rodar apos design aprovado (GUIDELINES §11).
argument-hint: "[marca]/[slug] \"snippet HTML do embed\" — ex: buzzmonitor/monitoramento-maio \"<script src=...jotform.com/jsform/...></script>\""
allowed-tools: Read, Edit, Glob, Grep
version: 1.6.0
---

# Skill: Integrar Formulario em Landing Page

Substitui o form mock (`<form action="#">`) por um embed externo. Aplica o CSS wrapper canonico para manter layout. **Nao roda dentro do pipeline** — usuario invoca manualmente quando o design esta aprovado.

## Caso especial: form compartilhado entre varias LPs (webinar perpetuo)

Se o usuario disser que **nao pode gastar um formulario novo** por LP, ou que a pagina de
agradecimento precisa ser decidida pela LP e nao pelo formulario, faca a integracao normal
(Passos 1-5) e **depois** aplique o mecanismo de destino descrito em
`landing-pages/GUIA-webinar-perpetuo-destino.md`: a LP grava o destino num `data-perpetuo-next` e a
pagina onde o provedor aterrissa encaminha.

Duas tentativas que **nao** funcionam (verificadas em 2026-08-26, detalhes no §1 do guia) — nao
gastar tempo redescobrindo:

- **Trocar o embed por form nativo postando em `submit.jotform.com/submit/{id}`** — o Jotform
  responde `Please Complete` com CAPTCHA pra POST fora de uma sessao dele. Nao grava nada.
- **Escutar `submission-started` / `submission-completed` via postMessage** — o primeiro e enviado
  sem `targetOrigin` (default `"/"`, mesma origem) e o segundo nao existe no JS do formulario.
  Nenhum dos dois chega num parent cross-origin.

Manter o embed tem ainda uma vantagem concreta: ele transmite o `parentURL`, que alimenta o widget
*Get Parent URL* e portanto o `url_conversao` no CRM (ver Notas, no fim). Form nativo perde isso.

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
- **NAO** herdar a classe `form` do mock. O `.form` no `lp-gerar` e um card visual (`background: #fff`, `padding: 40px`, `border`, `box-shadow`) e os provedores (Jotform/RD/HubSpot) ja vem com card proprio — manter `form` causa "card dentro de card" no live (incidente 2026-04-30).
- Preserve animacao reveal: se o form mock tinha `class="form reveal"` com `style="--d: XXms"`, replicar **apenas o `reveal` + `style`** no `<div>` wrapper (descartar o `form`).

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

Arquivo: landing-pages/{marca}/{slug}/index.html

Testar antes de publicar:
1. Abrir index.html no browser local
2. Conferir que iframe carrega dentro do wrapper (sem overflow)
3. Submeter form-teste para ver resposta do provedor

Proximo: /lp-publicar {marca} {slug} [dominio]
```

## Notas

- Nao validar o snippet (nao fazer HTTP request para ver se URL e valida — risco de bloquear por CSP ou timeout).
- Nao configurar CSP automaticamente — embeds externos + CSP estrito e complicado, deixar para ajuste manual caso usuario queira endurecer.
- Se o usuario quiser reverter: `Edit` manual (trocar wrapper por `<form action="#" onsubmit="event.preventDefault()">` novamente).
- GTM e responsabilidade de `lp-revisar` (Passo 3.5). Se a LP nao foi revisada antes, rode `/lp-revisar {marca}/{slug}` — ele injeta/corrige o snippet certo para marca+regiao.
- **URL de conversao ja funciona sozinha — nao inventar shim pra isso.** O campo `url` do
  formulario Jotform chega vazio, mas ele NAO e a fonte do `url_conversao` no CRM: quem alimenta
  e o campo interno de URL de pagina do proprio Jotform, que resolve a URL da LP a partir do
  `parentURL` que o embed sempre transmite. Verificado em 2026-08-11 no Supabase LATAM: leads de
  LP **sem** qualquer shim (ex: `content.buzzmonitor.com/plataforma-integral-social-media`)
  chegam com `url_conversao` completa, com query string e ate fragmento `#hash`. Um shim de
  `window.qsProxy` pra preencher o campo `url` foi adicionado e revertido no mesmo dia — enche um
  campo que ninguem consome. Antes de "consertar" atribuicao de LP, olhar o **destino**
  (`deals_latam_*_staging` / dashboards), nao o campo vazio no formulario.
