# Guarda-chuva das dashboards internas

Desde **2026-09-09** as 4 dashboards de Content Marketing param de ser 4 projetos Vercel soltos e passam a viver num **projeto único**, cada uma numa rota:

```
dashboards-elife.vercel.app
├── /               → hub com os cards (gerado)
├── /buzz-br/       ← dashboard-buzz-br-vercel/
├── /cxpress/       ← dashboard-cxpress-vercel/
├── /latam/         ← dashboard-latam-vercel/
├── /buzzcreators/  ← dashboard-buzzcreators-vercel/
├── /bm-pt/         ┐
├── /cxpress-pt/    ├ dashboard-pt-vercel/  (fonte compartilhada, 1 JSON por marca)
└── /elife-pt/      ┘
```

As 3 de Portugal saíram juntas em 09/09/2026, depois de uma auditoria do dado
(`dashboard/AUDITORIA-PORTUGAL.md`).

## Por quê

Basic Auth é **por origem**. Com 4 subdomínios, mesmo usando a mesma senha, o navegador pedia a credencial de novo a cada dashboard — o que inviabilizava um seletor de navegação. Um projeto só = **um login** cobre todas, e a barra do topo vira navegação normal.

De brinde: uma superfície de segurança em vez de quatro (um `middleware.js`, um `vercel.json`), e adicionar dashboard nova passa a ser uma entrada no manifesto.

## Como funciona

- **`manifest.json`** — fonte única. Slug, nome, rótulo curto, cor de destaque, pasta-fonte no repo, arquivos a copiar e nome do JSON de dados. A ordem do array é a ordem no seletor e no hub.
- **`templates/nav.js.tpl`** — a barra compartilhada. Autocontida de propósito: as 4 dashboards têm CSS próprio e não compartilham design system, então tudo é prefixado `dnav-` para não colidir com `.top`/`.picker`/`.container`. `position: fixed` (não `sticky`) porque as páginas têm `html { overflow-x: hidden }`, que quebraria sticky.
- **`templates/hub.html.tpl`** — a página raiz. Os cards saem do manifesto; a data de "Atualizada em" sai do `gerado_em` de cada JSON de dados, o que denuncia dashboard com dados velhos.
- **`build_umbrella.py`** — monta a dist. Copia os arquivos do manifesto, injeta `<script defer src="/nav.js">` no `<head>` de cada `index.html`, gera hub, `nav.js`, `middleware.js`, `vercel.json`, `robots.txt` e `package.json`.

As pastas-fonte no repo **não mudaram** e continuam sendo o lugar de editar código de dashboard. A barra e o hub só existem na dist — quem abre um `index.html` de fonte direto vê a dashboard sozinha, sem barra.

## Rodar

```bash
py dashboards-umbrella/build_umbrella.py <dist_dir> --dry-run   # mostra o plano
py dashboards-umbrella/build_umbrella.py <dist_dir>
```

Na prática, quem chama isso é a skill **`/dashboard-atualizar`** (exportar → build → deploy → validar). Não deploye a mão.

`<dist_dir>` é a sibling **fora do repo** (`$DASHBOARD_SIBLING_BASE/dashboards-elife`) — o build recusa qualquer caminho dentro do repositório. A credencial do Basic Auth vem de `.env.local` e só é escrita na dist, nunca no repo.

## Detalhes que não são óbvios

**`trailingSlash: true` no `vercel.json` é obrigatório.** As dashboards carregam `motor.js`, `estilo.css` e `dados-*.json` por caminho **relativo**. Em `/buzz-br` (sem barra) o relativo resolveria `/motor.js` e a página subiria quebrada; o 308 para `/buzz-br/` acontece antes de renderizar.

**O deploy é sempre do guarda-chuva inteiro.** Não existe deploy de uma rota só. Atualizar uma dashboard significa exportar o JSON dela e rebuildar tudo — os JSONs das outras vêm das pastas-fonte. Se um JSON faltar na fonte e já existir na dist, o build **reusa e avisa** (`REUSADO`), para nunca apagar os dados de uma dashboard ao deployar outra. Um `REUSADO` inesperado quer dizer que aquela dashboard vai ao ar com dados antigos.

**Dashboard nova** = uma entrada no `manifest.json` + uma entrada na `cfg()` do Passo A da skill + um contrato em `contratos/` (gere com `validar_contrato.py --sugerir <slug>` e revise — seção abaixo). Rota, card no hub e item no seletor saem sozinhos.

**Duas rotas podem dividir a mesma fonte.** É o caso de Portugal: os 3 slugs apontam para `dashboard-pt-vercel/` e diferem só no `dados`. O `index.html` descobre a marca pelo primeiro segmento do path (`/cxpress-pt/` → `dados-pt-cxpress.json`), então o mesmo ficheiro serve as três e elas não conseguem divergir. Quando marcas compartilham schema, prefira isto a duplicar a pasta — foi a duplicação entre BR, LATAM e Cxpress que criou o problema de sincronia manual que o repo carrega até hoje.

**Os 4 projetos antigos** (`dashboard-buzzmonitor-brasil`, `dashboard-cxpress-brasil`, `dashboard-buzzmonitor-latam`, `dashboard-buzzcreators-brasil`) viraram **308** para a rota correspondente — os links antigos continuam funcionando. As stubs de redirect vivem em `$DASHBOARD_SIBLING_BASE/redirects-dashboards/`. Não deployar dashboard neles.

**Rollback.** As siblings antigas (`$DASHBOARD_SIBLING_BASE/dashboard-*`) seguem intactas com o conteúdo pré-migração: se for preciso voltar, é um `vercel deploy` de cada uma (o que desfaz o 308 daquele projeto).

## Contrato de dados

Desde **2026-10-21**. Prepara o deploy noturno automático, mas vale já para a skill manual.

### O problema

O painel lê os campos do JSON pelo nome e compara strings cruas, sem validar nada. O modo de falha mais perigoso é mudo: um campo renomeado no exportador (`d_lead` → `data_lead`) faz `_inRange(undefined, …)` devolver `false`, todos os KPIs viram 0 e **a dashboard renderiza bonita e inteiramente zerada**, sem erro e sem faixa vermelha. Chave de topo ausente também é muda em alguns lugares — `dashboard-pt-vercel/motor.js` faz `new Set(DADOS.ganhas || [])`, então sem `ganhas` o fechamento zera em silêncio.

Quem roda a skill à mão lê o output e percebe. Um deploy às 07:00 não tem ninguém olhando. O contrato é o que torna esse silêncio impossível.

### As peças

| Arquivo | Papel |
|---|---|
| `contratos/<contrato>.json` | O que o **painel lê** de cada dashboard: chaves de topo, campos por registro, tipos, enums, literais comparados, referências entre listas e as métricas da catraca. As 3 rotas PT dividem o contrato `pt` (campo `contrato` no manifesto). |
| `validar_contrato.py` | Roda depois do export e **antes do build**. Exit ≠ 0 = não deploya. Stdlib pura. |
| `testar_contrato.py` | Prova que o validador pega cada modo de falha conhecido: corrompe cópias dos JSONs reais de 19 jeitos e confere o código de saída e a mensagem. Rode depois de mexer no validador. |
| `SCHEMA_VERSION` em cada `exportar_dados.py` | Versão do formato, carimbada no JSON como `schema_version`. |

O campo `consumidor` diz **onde** o painel lê cada campo. `consumidor: null` = o exportador emite e ninguém lê; pode sumir sem quebrar nada (vira só aviso). É isso que faz o contrato não engessar o export: ele congela o **acoplamento**, não o formato inteiro.

### O que é erro e o que é aviso

**Fatal** (bloqueia o deploy) só para quebra estrutural: campo que o painel lê sumiu ou mudou de tipo, data que deixou de ser `YYYY-MM-DD` (comparação de string erra **só no último dia** do período — o erro mais sutil de todos), enum novo em campo usado como índice de acumulador (`kpis[x.c] += 1`), literal comparado que sumiu (`status === 'Perdido'`), referência quebrada entre listas, `gerado_em` velho.

**Aviso** para o resto: campo novo não declarado, opcional ausente, enum novo em campo que não é acumulador. Um único registro com campo nulo **não** derruba o deploy — gate que falha à toa é desligado em duas semanas. Quem pega nulificação **em massa** é a catraca.

### Catraca

Compara as contagens do export de hoje com o **JSON que está no ar** (`--baseline-url`). Só rodada verde chega a deployar, então produção é, por definição, o último estado verde — sem baseline para persistir (o que obrigaria o CI a commitar na `main` toda noite).

Toda métrica é **cumulativa**, nunca janelada: num sábado ela não cresce, mas também não cai, então feriado não dá falso positivo. Piso = `min(base × 0,98, base − 5)` (percentual manda em volume alto, absoluto em volume baixo). Alta de +100% numa noite também é fatal — JOIN duplicando linhas **dobra** os KPIs em vez de zerá-los, e ninguém reclama de número alto.

**Queda legítima** (limpeza de CRM, recategorização): rode com `--aceitar-catraca <slug> --motivo "…"`. Destrava só a catraca daquele slug — **nunca** aceita violação de contrato. Deixar a rodada deployar já re-ancora: a noite seguinte compara contra o número novo.

**Virada de ano:** as listas são do ano corrente, então em 1º de janeiro tudo zera e a catraca dispara em todas. É esperado — rode com `--aceitar-catraca tudo --motivo "virada de ano"`, junto com o ajuste de `ANO_INI` nos exportadores que essa data já exige.

### Mudou o formato? A política de versão

Inteiro simples, um por contrato. **Bumpe** quando um campo que o painel lê for removido, renomeado ou mudar de tipo; quando um literal comparado mudar; quando um enum de acumulador ganhar valor; ou quando a **semântica** mudar sem mudar a forma (`d_fechamento` passa a ser data de assinatura) — esse último é o que mais escapa. **Não** bumpe ao adicionar campo nem ao remover campo com `consumidor: null`.

Regra prática: *se a mudança faria um painel antigo mostrar número errado em vez de simplesmente ignorar, bumpe.*

O bump é num PR só: `SCHEMA_VERSION` do exportador + `schema_version` do contrato. O validador sai com 4 se divergirem.

**E mudar só a visualização?** CSS, layout, rótulo, gráfico novo sobre campos que já existem: não toca o contrato e não tem como quebrar os dados. Se a mudança precisa de um campo novo, ele entra no exportador **e** no contrato (com o `consumidor`), e o validador avisa se faltar um.

### Gerar ou regenerar um contrato

```bash
py dashboards-umbrella/validar_contrato.py --sugerir <slug> > rascunho.json
```

Infere tipos e nulabilidade de 100% dos registros reais. Depois: preencha os `consumidor` (grep no `motor.js`/`render.js`/`index.html`), transforme em `enums`/`literais` só os campos que o painel **compara**, e **apague os `$valores_observados`** antes de commitar — em campos como `bd` eles são nomes de pessoas do time comercial, e os contratos vão para o git. Escrever o contrato à mão não é alternativa: o inventário manual errou quatro de quatro séries quando tentamos.

### Rodar

```bash
py dashboards-umbrella/validar_contrato.py --baseline-url https://dashboards-elife.vercel.app   # o que a skill faz
py dashboards-umbrella/validar_contrato.py cxpress --sem-catraca                                # só contrato, uma dash
py dashboards-umbrella/testar_contrato.py                                                       # o validador ainda pega tudo?
```
