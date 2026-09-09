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

**Dashboard nova** = uma entrada no `manifest.json` + uma entrada na `cfg()` do Passo A da skill. Rota, card no hub e item no seletor saem sozinhos.

**Duas rotas podem dividir a mesma fonte.** É o caso de Portugal: os 3 slugs apontam para `dashboard-pt-vercel/` e diferem só no `dados`. O `index.html` descobre a marca pelo primeiro segmento do path (`/cxpress-pt/` → `dados-pt-cxpress.json`), então o mesmo ficheiro serve as três e elas não conseguem divergir. Quando marcas compartilham schema, prefira isto a duplicar a pasta — foi a duplicação entre BR, LATAM e Cxpress que criou o problema de sincronia manual que o repo carrega até hoje.

**Os 4 projetos antigos** (`dashboard-buzzmonitor-brasil`, `dashboard-cxpress-brasil`, `dashboard-buzzmonitor-latam`, `dashboard-buzzcreators-brasil`) viraram **308** para a rota correspondente — os links antigos continuam funcionando. As stubs de redirect vivem em `$DASHBOARD_SIBLING_BASE/redirects-dashboards/`. Não deployar dashboard neles.

**Rollback.** As siblings antigas (`$DASHBOARD_SIBLING_BASE/dashboard-*`) seguem intactas com o conteúdo pré-migração: se for preciso voltar, é um `vercel deploy` de cada uma (o que desfaz o 308 daquele projeto).
