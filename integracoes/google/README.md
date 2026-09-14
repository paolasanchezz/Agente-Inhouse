# Pocket Events — LP automatica a partir de formulario

BD ou SDR preenche um Google Form, e a landing page do encontro entra no ar
sozinha em poucos minutos. Nenhum modelo de linguagem participa: o conteudo vem
de listas fechadas e de um template versionado, e um script Python substitui os
tokens.

## O caminho inteiro

```
Google Form (BDs e SDRs)
   -> planilha de solicitacoes
   -> Apps Script (pocket-event-solicitacao.gs)
        onFormSubmit -> repository_dispatch no GitHub          [instantaneo]
   -> .github/workflows/pocket-event-novo.yml
        pocket_event_job.py: valida -> renderiza -> inscreve no manifesto
        abre PR
   -> lp-pr.yml       (auto-merge: o diff so toca conteudo)
   -> lp-deploy.yml   (build + deploy + smoke + rollback automatico)
   -> https://evento.buzzmonitor.com/pocket-{nicho}-{AAAA-MM-DD}

visitante se inscreve na LP
   -> Apps Script (pocket-event-inscricoes.gs) -> planilha de inscricoes
```

A varredura diaria (07:23 BRT, dias uteis) refaz o mesmo caminho lendo as linhas
sem status. Ela existe porque o webhook pode falhar; como o job ignora slug que
ja existe, rodar duas vezes nao cria nada duas vezes.

## O que e fixo e o que e escolhido

| Na LP | De onde vem |
|---|---|
| Titulo (H1) | unico campo de texto livre do formulario |
| Nicho, modulo, horario | listas fechadas (`config.json`) |
| Nome, cargo, bio e foto do speaker | cadastro `speakers.json`, nunca digitados |
| Data por extenso, dia da semana, DD/MM | derivados da data por tabela fixa |
| Slug e URL | `pocket-{nicho}-{AAAA-MM-DD}` |
| Title, meta description, OG | montados por modelo em `config.json` |
| Depoimentos, mural de clientes, KPIs, rodape | fixos no template |

O titulo e recusado se tiver menos de 12 ou mais de 60 caracteres, terminar em
ponto, ou conter `< > " ' \ { } |` travessao | aspas curvas. Travessao e regra
anti-IA de tolerancia zero, e o renderer recusa ate se ele vier na copy fixa.

## Instalacao (uma vez)

### 1. Cadastrar quem apresenta

Sem isso o formulario nao tem o que oferecer. Editar
`landing-pages/build/templates/pocket-event/speakers.json`, um bloco por pessoa
(id, nome, cargo, bio de 1 a 2 linhas). Foto e opcional: com foto, salvar em
`brand/buzzmonitor/assets/speakers/{id}.jpg` (quadrada, minimo 336x336); sem
foto, a LP mostra as iniciais no degrade da marca.

Abrir PR. Esse arquivo esta em path protegido, entao passa pela revisao do Victor.

### 2. Planilha e formulario de solicitacao

1. Criar planilha "Pocket Events - solicitacoes" no Drive.
2. Extensoes > Apps Script, colar `pocket-event-solicitacao.gs` inteiro.
3. Gerar as opcoes e colar no `OPCOES` do script:
   ```bash
   py landing-pages/build/render_pocket_event.py --form-spec
   ```
4. Configuracoes do projeto > Propriedades do script:
   - `GITHUB_TOKEN` — PAT classico com escopo `repo`
   - `GITHUB_REPO` — `victorfmlopes/Agente-Inhouse`
   - `POCKET_TOKEN` — senha longa inventada agora (anotar, vai virar secret)
5. Rodar `criarFormulario` (cria o Form com as listas certas) e depois `configurar`
   (instala o gatilho e as colunas de controle).
6. Implantar > Nova implantacao > Aplicativo da Web, "Executar como: Eu",
   "Quem tem acesso: Qualquer pessoa". Guardar a URL `/exec`.
7. Compartilhar o link de resposta do Form com o time de BD e SDR.

### 3. Planilha de inscricoes (o formulario da LP)

1. Criar planilha "Pocket Events - inscricoes", copiar o ID da URL.
2. Extensoes > Apps Script, colar `pocket-event-inscricoes.gs`, preencher
   `ID_PLANILHA`, rodar `prepararCabecalhos`.
3. Implantar como aplicativo da Web, mesmas opcoes do item anterior.
4. Colar a URL `/exec` em `form_endpoint` do
   `landing-pages/build/templates/pocket-event/config.json` e commitar.

Enquanto `form_endpoint` estiver vazio, a LP vai ao ar e o formulario valida os
campos, mas nao grava nada. O renderer avisa isso em toda execucao.

### 4. Secrets no GitHub

`Settings > Secrets and variables > Actions`:

| Secret | Para que | Sem ele |
|---|---|---|
| `POCKET_EVENT_PAT` | abrir o PR como usuario | PR aberto, mas o `lp-pr.yml` nao roda e o merge fica manual |
| `POCKET_SHEET_URL` | URL `/exec` do script de solicitacoes | varredura diaria pulada; webhook continua funcionando |
| `POCKET_SHEET_TOKEN` | mesmo valor do `POCKET_TOKEN` | idem |
| `RESEND_API_KEY` | e-mail de resumo (ja existe no repo) | resumo so no log do Actions |

O `POCKET_EVENT_PAT` e o unico que muda o comportamento de verdade: PR aberto com
o `GITHUB_TOKEN` padrao nao dispara outros workflows (regra anti-recursao do
GitHub), entao o merge-bot nunca o veria.

### 5. Ensaio antes de soltar pro time

```bash
# 1. so validar, sem escrever nada
py landing-pages/build/pocket_event_job.py solicitacao.json --dry-run

# 2. pelo GitHub, sem tocar na planilha: Actions > "Pocket Event - nova LP"
#    > Run workflow, colando o JSON e marcando dry_run
```

Depois repetir com `dry_run` desmarcado e acompanhar: PR aberto -> auto-merge ->
`Deploy LPs` -> URL respondendo.

## Operacao

**Trocar o texto de todas as edicoes** (hero fixo, depoimentos, rodape):
`landing-pages/build/templates/pocket-event/index.html.tmpl`. Path protegido,
entra por PR revisado, e vale da proxima edicao em diante. Edicoes ja no ar nao
sao reescritas.

**Corrigir uma edicao ja publicada:** a pasta gerada nao deve ser editada a mao
(ela e recriada se a linha for reprocessada). Ajustar a linha na planilha, apagar
o status e deixar a varredura refazer. Para mudar data ou nicho, o slug muda:
sai uma LP nova, e a antiga continua no ar ate alguem tira-la do manifesto (e
remover slug do manifesto nunca auto-mergeia, por desenho).

**Nao vai pro ar:** ver primeiro a coluna `Status` da planilha (`erro` traz o
motivo em `Detalhe`), depois Actions > "Pocket Event - nova LP", depois
"Deploy LPs".

## Limites que o automatismo respeita

- no maximo 5 LPs por execucao (planilha com defeito nao vira enxurrada de deploy);
- data entre amanha e 180 dias a frente;
- so o guarda-chuva `evento.buzzmonitor.com`, so o template pocket-event;
- nunca edita nem remove LP existente;
- solicitacao invalida nao gera PR nenhum, so o e-mail com os motivos.
