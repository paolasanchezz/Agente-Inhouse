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

Na prática, quem chama isso é o workflow noturno, via `deploy_ci.py` (seção "Atualização automática" abaixo). Deploy manual deste projeto é negado pelo hook.

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

**Virada de ano:** nada quebra sozinho em 1º de janeiro. O início do período é uma **data fixa** (`2026-01-01` nos exportadores e em `dashboard/queries_latam.py`), não "o ano corrente" — a exportação segue acumulando 2026 + 2027 e as contagens não caem. A catraca só dispara quando alguém **mover** esse início para 2027, uma mudança deliberada, num PR: aí a primeira rodada depois do merge precisa de `--aceitar-catraca tudo --motivo "novo ano"`. O que cresce com o tempo é o tamanho dos JSONs; o validador avisa ao passar de 80% do teto (o LATAM, o maior, deve chegar lá por volta de meados de 2027).

### Mudou o formato? A política de versão

Inteiro simples, um por contrato. **Bumpe** quando um campo que o painel lê for removido, renomeado ou mudar de tipo; quando um literal comparado mudar; quando um enum de acumulador ganhar valor; ou quando a **semântica** mudar sem mudar a forma (`d_fechamento` passa a ser data de assinatura) — esse último é o que mais escapa. **Não** bumpe ao adicionar campo nem ao remover campo com `consumidor: null`.

Regra prática: *se a mudança faria um painel antigo mostrar número errado em vez de simplesmente ignorar, bumpe.*

O bump é num PR só, nas **três pontas**: `SCHEMA_VERSION` do exportador, `schema_version` do contrato e `const SCHEMA_ESPERADO` no `index.html` do painel. O validador sai com 4 se qualquer uma divergir — e como o ensaio do workflow roda em todo PR de dashboard, não dá para mergear um bump pela metade.

**No painel**, versão diferente da esperada mostra uma faixa logo abaixo da barra de navegação e **renderiza assim mesmo** (o número já foi conferido no CI antes do deploy; bloquear transformaria uma aba em cache em indisponibilidade). JSON com versão **maior** = "página em cache, recarregue com Ctrl+Shift+R"; **menor ou sem versão** = "dados fora do contrato, confirme antes de usar". O PT avisa também se `etapas`, `ganhas` ou `terminais` faltarem, porque lá a ausência zera fechamentos e perdidos sem erro. Os textos saem na língua de cada painel (PT-BR, ES-LATAM em "tú", PT-PT).

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

## Atualização automática (todo dia às 07:00)

Desde **2026-10-21** o workflow `.github/workflows/dashboards-deploy.yml` faz sozinho o que a `/dashboard-atualizar` fazia à mão. **Quem dispara é o n8n, todo dia às 07:00 BRT** (`integracoes/n8n/dashboards-disparo-diario.json`), e as dashboards ficam prontas por volta das 07:03.

O `cron` do próprio workflow (07:13) ficou só como **reserva**: o agendamento do GitHub é "melhor esforço" e, neste repositório, chega com 4h30 a 9h30 de atraso (medido em 2026-10 — na primeira manhã, às 09:10, a rodada agendada ainda não tinha saído). Se o n8n falhar, o GitHub ainda atualiza, só que tarde.

```
conectividade → filtro CM do buzz-br → exportar as 7 → validar contrato + catraca → build → deploy → smoke → (rollback)
```

Qualquer etapa que falha para a cadeia: **nada vai para o ar e o painel segue com os dados de ontem**, que é melhor que dado de hoje errado. Nesse caso chega um e-mail para o Victor dizendo em que etapa parou, com o fim do log (o validador já escreve o que consertar). No verde, silêncio.

| Peça | Papel |
|---|---|
| `deploy_ci.py` | Build numa dist temporária, deploy, smoke e rollback. Irmão do `landing-pages/build/deploy_ci.py`. O smoke usa Basic Auth e confere, por rota, 308 sem barra, 200 com barra e o `index.html` **e o JSON** servidos byte a byte iguais aos da dist — prova que o que está no ar é exatamente o que o validador aprovou. Se reprovar, promove de volta o deploy que o alias servia antes. |
| `auditar_filtro_cm.py` | Confere se o filtro CM do buzz-br está igual em `dashboard/queries.py` (oficial) e `dashboard-pessoal/lib/queries.py` (o espelho, que é o que o exportador usa). A skill manual rodava isso antes de cada export; ficou de fora na primeira versão do workflow e voltou na Fase 5. |
| `notificar_falha.py` | O e-mail de falha. Apaga do texto qualquer valor de secret antes de enviar, porque o log vai bruto, sem a máscara que o GitHub aplica na tela. |

**Em PR também roda — só como ensaio.** Todo PR que mexe em código de dashboard (`dashboard-*-vercel/`, `queries*.py`, `dashboards-umbrella/`) exporta, valida o contrato e builda, **sem deployar**. É o que pega, antes do merge, uma mudança no painel ou no exportador que quebraria o contrato.

### Rodar à mão

Actions → *Dashboards — atualizacao noturna* → **Run workflow**:

| Campo | Para quê |
|---|---|
| `dry_run` | ensaio: exporta, valida e builda, nada vai pro ar |
| `aceitar_catraca` + `motivo` | a catraca barrou uma queda **legítima** (limpeza de CRM, início do período movido para um ano novo): slug ou `tudo`, e o porquê. Nunca destrava violação de contrato |
| `force_fail` | ensaia o rollback: deploya, simula smoke reprovado e promove o deploy anterior. Deixa no ar a versão **anterior** — rode um normal em seguida |

### Secrets usados

`SUPABASE_PG_URL` (a URL do **pooler**, usuário `looker_readonly` — o host direto `db.<ref>.supabase.co` é só IPv6 e o runner do GitHub é só IPv4), `DASHBOARD_BASIC_AUTH_USER`/`_PASS`, `VERCEL_TOKEN` e `RESEND_API_KEY`.

### Checar a produção sem deployar

```bash
py dashboards-umbrella/deploy_ci.py --checar-producao   # 401 sem login, noindex, 308, index com nav, JSON 200 nas 7
py dashboards-umbrella/deploy_ci.py --dry-run           # só o build, numa dist temporária
```

### Uma porta só

O hook `.claude/hooks/guard_vercel_deploy.py` **nega** deploy manual do projeto `dashboards-elife` (por nome, `projectId`, domínio ou `.vercel/project.json` do diretório) — mesma trava das LPs migradas. Antes, um deploy local subia o código da branch em que a pessoa estivesse, pulava o validador, e a rodada seguinte devolvia o da `main`. A `/dashboard-atualizar` v5 virou disparo do workflow + acompanhamento.

**Emergência (GitHub Actions fora do ar):** `LP_DEPLOY_CI_OVERRIDE=1` no **ambiente da sessão** do Claude Code troca o bloqueio por confirmação. Prefixar no comando não funciona — o hook lê o ambiente do processo, não o do comando. Passo a passo na seção "Emergência" da skill; remova a variável assim que terminar.
