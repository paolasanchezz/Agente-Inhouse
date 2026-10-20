# ancoras-sem-hash

Trava que impede o `#secao` de ficar na URL quando o visitante clica num botão de âncora
(`href="#inscricao"`, `#form`, `#agendar`, skip-link...). O botão continua rolando até a seção;
só a URL não muda. Regra e motivo: [GUIDELINES §22](../../GUIDELINES.md).

Entrou em 2026-10-20 em **todas** as LPs dos guarda-chuvas (pedido do Victor). Antes disso,
45 LPs LATAM tinham uma versão própria colada uma a uma (#709).

## Como chega na LP

Não se cola na LP. `build/build_umbrella.py` lê `ancoras-sem-hash.js` e injeta inline, antes do
último `</body>`, em toda LP de todo manifesto (sem opt-in). O marcador `data-lp="ancoras-sem-hash"`
deixa a injeção idempotente. Editou o JS aqui, o próximo deploy do CI leva pra todas.

Conferir num build local:

```bash
py landing-pages/build/build_umbrella.py landing-pages/dominios/content-cxpress-io/manifest.json /tmp/dist-cx
```

```bash
grep -c 'data-lp="ancoras-sem-hash"' /tmp/dist-cx/*/index.html
```

Cada LP tem que dar `1` (páginas de `extra_files`, como `_placeholder`, não passam pelo build e dão `0`).

**Fora do CI** (LP solo, Webflow) não tem build: colar o conteúdo do `.js` num `<script>` antes do
`</body>`.

## O que o script faz

| Caso | Comportamento |
|---|---|
| Clique em `<a href="#x">` | `preventDefault` + `location.replace('#x')`: o browser rola, move o foco e dispara `hashchange` como no clique normal, sem empilhar entrada no histórico. Logo depois, a URL volta a ser `pathname + search`. |
| LP com handler próprio que já dá `preventDefault` (script LATAM da #709) | Não mexe: o listener fica na `window` e respeita `defaultPrevented`. |
| LP que carrega o Jotform no clique do CTA (as Cxpress com `carregaJot`) | O form carrega depois da limpeza, então o `parentURL` que o Jotform grava já sai sem `#`. |
| JS que grava hash por conta própria (`webflow.js` faz `pushState('#secao')`) | `history.pushState`/`replaceState` passam a descartar o fragmento de URL da mesma origem. |
| `location.hash = 'x'` ou qualquer outra mudança de hash | Limpa no `hashchange`. |
| Visitante chega por link com `#secao` | O browser rola no carregamento; a URL é limpa depois do `load`. |
| Ctrl/Cmd/Shift+clique, `target="_blank"`, `download` | Não mexe. |

Os scripts da própria LP vêm antes deste no HTML, então os `hashchange` deles leem o hash antes da
limpeza (a `buzz-academy-experience` abre `<details>` pelo hash e continua abrindo).

## Testado em 2026-10-20 (build local, Chromium)

- `cxpress/webinar-whatsapp-equipe`: clique de mouse no CTA do hero rola até `#inscricao`, URL fica
  `?utm_source=…&utm_content=…`, `history.length` não muda, dois cliques seguidos também não.
- `buzzmonitor/buzz-academy-experience`: chegada com `#trilha-growth` abre a trilha e alinha no topo;
  clique em `#trilha-branding` abre a trilha. Mesmas posições da versão sem o script, só sem o hash.
- `buzzmonitor/plataforma-buzzmonitor` (Webflow): a rolagem continua do `webflow.js` e o `#recursos`
  some da URL.
- `buzzmonitor/agencias-es` (script da #709): sem rolagem dupla nem entrada nova no histórico;
  skip-link com Enter manda o próximo Tab pra dentro do `<main>`.
