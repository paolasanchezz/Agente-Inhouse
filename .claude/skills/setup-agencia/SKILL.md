---
name: setup-agencia
description: Guia interativo de primeiro setup para novos colaboradores do agente inhouse. Conduz do zero (instalar Python, conectar Notion, verificar MCP Bunzzai, autenticar Vercel CLI para Landing Pages, conectar o Supabase para consultar deals) ate a primeira skill rodando. Usar quando o usuario digitar /setup-agencia ou disser "e minha primeira vez" / "como comeco".
argument-hint: "(opcional) — texto livre. Ex: /setup-agencia | /setup-agencia 'so anuncios' | /setup-agencia 'so copy e newsletter' | /setup-agencia 'so lp' | /setup-agencia 'so supabase'"
allowed-tools: AskUserQuestion, Read, Bash, Glob
version: 0.7.0
---

# Skill: /setup-agencia — Setup guiado para newbies

Voce esta executando um **script deterministico** de onboarding. Nao improvise perguntas, nao pule passos, nao invente opcoes. Siga exatamente o roteiro abaixo.

## Principios invioláveis

1. **Uma pergunta por vez.** Nunca empilhe perguntas no mesmo `AskUserQuestion`.
2. **Sempre marque a opcao recomendada com `(Recomendado)`** no label.
3. **Linguagem PT-BR coloquial e didatica.** Assuma que o usuario pode nunca ter aberto um terminal.
4. **Apos cada acao tecnica (instalar, copiar, etc.), valide antes de seguir.** Nao acumule falhas silenciosas.
5. **Falhas → mensagem hardcoded de "Fallback"**, nao improviso.
6. **No final, valide cada modulo (Notion ping, MCP Bunzzai ping, Vercel CLI whoami, `SELECT` no Supabase) e ofereca um test drive.**
7. **Se o usuario travar em qualquer ponto, ofereca pausar.** O setup pode ser retomado depois rodando `/setup-agencia` de novo.

---

## Passo 0 — Boas-vindas (texto literal)

Exiba **literalmente**:

> Oi! Sou o assistente de setup do agente inhouse do Grupo Elife. Vou te ajudar a configurar tudo passo a passo. **No final dessa conversa, voce vai estar 100% pronto pra usar todas as skills que escolher.**
>
> Vou fazer perguntas simples, uma de cada vez. Se voce nao souber a resposta, escolha "nao sei" — eu te explico. Pode demorar 10-20 minutos na primeira vez. Bora?

Aguarde confirmacao livre (qualquer "sim/ok/bora/vai/manda" segue).

---

## Passo 1 — Diagnostico de ambiente

### 1.1 — Sistema operacional

`AskUserQuestion`:
- question: "Voce esta em qual sistema?"
- header: "Sistema"
- multiSelect: false
- options:
  1. "Windows" — "Windows 10 ou 11."
  2. "Mac" — "macOS."
  3. "Linux" — "Distribuicoes Linux (Ubuntu, Debian, Fedora, etc.)."

Guarde como `os_user`. Determina exemplos de comando ao longo da skill.

### 1.2 — O que voce vai usar?

`AskUserQuestion`:
- question: "O que voce vai usar mais nessa ferramenta? (pode marcar mais de um)"
- header: "Uso"
- multiSelect: true
- options:
  1. "Conteudo (/escrever, /newsletter, /traduzir)" — "Copy, newsletters e traducao para PT-PT ou ES-LATAM."
  2. "Analise de Meta Ads (/anuncios)" — "Relatorios de performance de campanhas via MCP Bunzzai (sem token Meta)."
  3. "Landing Pages (/landing-page)" — "Criar e publicar LPs no Vercel."
  4. "Dados de deals (Supabase)" — "Consultar deals e leads direto no banco, so leitura. Ex: 'quantos deals CM fechamos em setembro?'"

> O `AskUserQuestion` aceita no maximo 4 opcoes. Por isso newsletter, copy e traducao vem juntas: as tres dependem so do Notion.

Guarde como `modulos`. Determina quais blocos de setup vamos rodar:
- **Conteudo** → exige **Notion MCP** funcionando → **rodar Passo 2**
- **Meta Ads** → exige **MCP Bunzzai** conectado (zero setup local — sem token Meta) → **rodar Passo 3**
- **Landing Pages** → exige **Vercel CLI autenticado** + **Python 3.10+** (PageSpeed CLI) → **rodar Passo 3 (Python) + Passo 4**
- **Dados de deals** → exige **uv** + a variavel **`SUPABASE_PG_URL`** → **rodar Passo 5**. Nao precisa do Python do Passo 3: o uv baixa o Python que usa.
- Quem marca tudo, faz tudo.

---

## Passo 2 — Setup do Notion MCP

> **Pular este passo se `modulos` nao inclui Conteudo.**

### 2.1 — MCP do Notion

`AskUserQuestion`:
- question: "Voce ja conectou o MCP do Notion no Claude Code?"
- header: "Notion MCP"
- multiSelect: false
- options:
  1. "Sim, ja esta conectado" — "Ja configurei antes e funciona."
  2. "Nao / Nao sei o que e isso (Recomendado)" — "Quero que voce me explique e ajude a conectar."

Se "Sim" → pular para 2.3.
Se "Nao" → continuar com 2.2.

### 2.2 — Explicacao + passo-a-passo (newbie)

Exiba **literalmente**:

> **O que e o MCP do Notion?**
> MCP e um "plugin" que liga o Claude Code direto ao seu Notion. Sem isso, eu nao consigo publicar newsletters nem traducoes nas pastas certas.
>
> **Como conectar (passo a passo):**
> 1. No Claude Code, digite `/mcp` e de Enter.
> 2. Vai abrir uma lista de MCPs. Procure "Notion".
> 3. Clique em "Adicionar" / "Connect".
> 4. Vai abrir o navegador pedindo pra fazer login no Notion e autorizar.
> 5. Autorize **apenas o workspace do Grupo Elife** (nao autorize seu Notion pessoal).
> 6. Volte aqui e me diga "pronto".

Aguarde "pronto" / "ok" / "feito" (confirmacao livre).

### 2.3 — Validacao

Exiba **literalmente**:

> Vou testar a conexao. Por favor, no chat (fora dessa skill) digite: `liste meu workspace do notion`. Se aparecerem paginas, esta funcionando. Volte aqui e me diga o resultado.

`AskUserQuestion`:
- question: "Funcionou?"
- header: "Notion OK?"
- multiSelect: false
- options:
  1. "Sim, listou as paginas" — "Notion conectado com sucesso."
  2. "Nao, deu erro / nao listou" — "Algo deu errado, preciso de ajuda."

Se "Nao" → exibir Fallback "notion-mcp-falhou" e perguntar se quer pular esse modulo por enquanto.

Marque internamente: `notion_ok = true/false`.

---

## Passo 3 — Setup do Python + MCP Bunzzai

> **Pular este passo se `modulos` nao inclui nem Meta Ads nem Landing Pages.**

> **Contexto importante:** desde 2026-06-22, analise de Meta Ads roda 100% via MCP Bunzzai (sem token Meta nem instalacao Python local). Python aqui e validado so caso o usuario tambem va usar Landing Pages (PageSpeed CLI) ou auditorias pontuais em `meta-ads-legacy/scripts/`.

### 3.1 — Python instalado?

`AskUserQuestion`:
- question: "Voce tem Python instalado nessa maquina?"
- header: "Python"
- multiSelect: false
- options:
  1. "Sim, tenho Python 3.10 ou mais novo" — "Ja esta instalado e funciona."
  2. "Tenho mas nao sei a versao" — "Vou checar com voce."
  3. "Nao tenho / nao sei (Recomendado)" — "Quero que voce me ajude a instalar."

Roteamento:
- "Nao tenho" → bloco 3.2.A (instalar) → 3.2.B (validar)
- "Nao sei a versao" → bloco 3.2.B (validar direto)
- "Sim" → pular para 3.3

### 3.2.A — Instalar Python

Exiba **conforme `os_user`**:

**Se Windows:**
> 1. Abra https://www.python.org/downloads/ e baixe "Python 3.12" (ou mais nova).
> 2. **IMPORTANTE:** ao instalar, marque a caixa **"Add Python to PATH"** na primeira tela. Sem isso nao funciona.
> 3. Clique em "Install Now" e espere terminar.
> 4. Reinicie o Claude Code (feche e abra de novo).
> 5. Volte aqui e me diga "instalei".

**Se Mac:**
> 1. Abra o Terminal (Cmd+Espaco, digite "Terminal").
> 2. Cole: `xcode-select --install` e de Enter (se ja estiver instalado, vai dar mensagem rapida).
> 3. Cole: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` e de Enter (instala o Homebrew, demora 5min).
> 4. Depois cole: `brew install python@3.12` e de Enter.
> 5. Volte aqui e me diga "instalei".

**Se Linux:**
> 1. Abra o terminal.
> 2. Cole: `sudo apt update && sudo apt install python3.12 python3-pip` (ou equivalente da sua distro).
> 3. Volte aqui e me diga "instalei".

Aguarde "instalei". Depois rode 3.2.B.

### 3.2.B — Validar versao

Use `Bash`:
- Windows: `python --version`
- Mac/Linux: `python3 --version`

Interprete a saida:
- Versao >= 3.10 → exiba `[OK] Python {versao}` e siga para 3.3.
- Versao < 3.10 ou comando nao encontrado → Fallback "python-falhou".

### 3.3 — Verificar MCP Bunzzai

> **Pular este sub-passo se `modulos` NAO inclui Meta Ads.**

O `/bunzzai` e `/bunzzai-geral` rodam via MCP do Bunzzai (CRM proprio do Grupo Elife). Esse MCP normalmente esta configurado **globalmente** no Claude Code de cada colaborador (nao no repo). Vamos checar se esta ativo.

Exiba **literalmente**:

> Vou checar se o MCP Bunzzai esta conectado na sua maquina. Se nao estiver, te direciono pro Victor pegar as credenciais — e uma configuracao por colaborador, feita uma vez so.

Use `Bash`:
```
claude mcp list 2>/dev/null | grep -i bunzzai || echo "BUNZZAI_NAO_CONFIGURADO"
```

Interprete:
- **Achou "bunzzai" na lista** → exiba `[OK] MCP Bunzzai conectado.` e marcar `bunzzai_ok = true`.
- **"BUNZZAI_NAO_CONFIGURADO"** → Fallback "bunzzai-mcp-falhou".

### 3.4 — (Sem mais nada nesse passo)

Setup do Meta Ads acaba aqui — sem token, sem `.env`, sem `pip install`. Se voce **so** marcou Meta Ads (sem Landing Pages), pode pular pro Passo 5. O Python so e estritamente necessario para Landing Pages (`/lp-publicar` usa PageSpeed CLI) e auditorias pontuais em `meta-ads-legacy/scripts/`.

---

## Passo 4 — Setup do Vercel CLI (Landing Pages)

> **Pular este passo se `modulos` nao inclui Landing Pages.**

A skill `/lp-publicar` precisa do **Vercel CLI** instalado e autenticado na org `elife-group`. Importante: o **MCP Vercel** que aparece em `/mcp` no Claude Code e uma autenticacao SEPARADA — nao serve para a skill. Precisamos do CLI.

### 4.1 — Verificar se ja tem Vercel CLI

`AskUserQuestion`:
- question: "Voce ja usa Vercel CLI nessa maquina?"
- header: "Vercel CLI"
- multiSelect: false
- options:
  1. "Sim, ja tenho instalado e logado" — "Ja rodei `vercel login` aqui antes."
  2. "Nao / nao sei (Recomendado)" — "Quero que voce me ajude."

Se "Sim" → pular para 4.3 (validacao).
Se "Nao" → continuar com 4.2.

### 4.2 — Instalar e logar

Exiba **literalmente**:

> **O Vercel CLI vem via npm.** Vou usar `npx` (que baixa on-demand sem precisar instalar global). Na primeira chamada pode demorar 30-60s.

Use `Bash` (rodar em background com timeout 90s):
```
npx --yes vercel --version
```

- Sucesso (retorna versao tipo `41.x.x`) → exibir `[OK] Vercel CLI disponivel via npx` e seguir.
- Erro → Fallback "vercel-cli-falhou".

Em seguida, exiba **literalmente**:

> **Agora vou abrir o login.** Vou rodar `npx vercel login`. Vai abrir o navegador pedindo pra voce escolher um metodo (Google, GitHub, Email...). Use a conta vinculada ao Grupo Elife. Depois autoriza no navegador e volta aqui.

Use `Bash` (background, timeout 180s):
```
npx --yes vercel login
```

Aguarde retorno do CLI. Se falhar, Fallback "vercel-login-falhou".

### 4.3 — Validar autenticacao no escopo elife-group

Use `Bash`:
```
npx --yes vercel whoami --scope team_nC991VqUuSU2jXZN152xqqEg
```

- Sucesso (retorna o username) → exibir `[OK] Vercel autenticado em elife-group como {user}` e marcar `vercel_ok = true`.
- Erro "scope not found" / "not a member" → Fallback "vercel-org-falhou".
- Erro "please log in" → repetir 4.2.

### 4.4 — Configurar `LP_SIBLING_BASE` (escreve `.env.local`)

Exiba **literalmente**:

> **Sobre a "pasta sibling".** Quando voce publica uma LP, o pipeline copia os arquivos finais pra uma pasta IRMA do repo (fora dele) e roda `vercel deploy` la. Isso protege o repo interno de vazar pro deploy publico.
>
> Vou guardar essa preferencia em `.env.local` (na raiz do repo, gitignored). Voce so configura uma vez. **Importante:** evite OneDrive/iCloud/Dropbox (sync vai brigar com o vercel deploy) e nao escolha uma pasta dentro do repo.

Calcule a sugestao baseada no parent do repo:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
SUGGESTED_BASE=$(dirname "$REPO_ROOT")
```

Detecte se a sugestao cai em pasta sync-watched:

```bash
case "$SUGGESTED_BASE" in
  *OneDrive*|*iCloud*|*Dropbox*)
    SUGGESTED_BASE=""  # nao sugerir uma pasta sync
    ;;
esac
```

`AskUserQuestion`:
- question: "Onde guardar os artefatos de deploy de LPs? (sugestao: pasta-mae do repo, fora de sync)"
- header: "Sibling base"
- multiSelect: false
- options:
  1. Se `$SUGGESTED_BASE` nao vazia: `"Usar {$SUGGESTED_BASE} (Recomendado)"` — "A pasta-mae do seu repo, fora de qualquer sync."
  2. "Quero escolher outra pasta" — "Vou digitar o caminho manualmente."

Se "outra pasta" (ou se a sugestao foi vazia), pedir o path:

`AskUserQuestion`:
- question: "Qual o caminho? (use barras `/` mesmo no Windows; sem espacos no final)"
- header: "Caminho"
- multiSelect: false
- options:
  1. "Cancelar" — "Voltar atras, deixa pra configurar depois."

(O usuario respondera via "Other" com o caminho real.) Aceitar o input como `CHOSEN_BASE` e validar:

- Existe ou pode ser criado? `mkdir -p "$CHOSEN_BASE" 2>&1` deve dar exit 0.
- Nao e dentro do repo? `case "$CHOSEN_BASE" in $REPO_ROOT*) reject ;; esac`
- Nao e sync-watched? Mesmo case acima de OneDrive/iCloud/Dropbox.

Se reprovou em qualquer check, exiba o motivo e re-pergunte. Se passou, segue.

Escrever `.env.local` na raiz (criar se nao existe; substituir linha `LP_SIBLING_BASE=` se ja existe):

Use `Read` em `.env.local` (se existir). Se a linha `LP_SIBLING_BASE=` ja esta la, use `Edit` pra trocar o valor. Se nao existe ou nao tem a linha, use `Write` (para criar) ou `Edit` (para append) com:

```
LP_SIBLING_BASE={base-escolhida}
```

Confirme:
```bash
grep -E "^LP_SIBLING_BASE=" .env.local
```

- Sucesso → exibir `[OK] LP_SIBLING_BASE={base} salvo em .env.local` e marcar `vercel_ok = true`.
- Falha → Fallback "lp-sibling-falhou".

Em qualquer caso, seguir para Passo 4.5.

### 4.5 — Vercel API token (opcional, mas recomendado pra guarda-chuva)

Exiba **literalmente**:

> **Por que um token Vercel?**
> Quando voce publica uma LP num dominio guarda-chuva (ex: `content.cxpress.io`, `evento.buzzmonitor.com`), a skill `lp-publicar` precisa **baixar o ultimo deploy production** antes de adicionar a LP nova — pra nao apagar as vizinhas. Isso vai numa API que precisa de token.
>
> Sem token, a skill tenta ler do `auth.json` do CLI Vercel automaticamente. Funciona na maioria dos casos, mas em algumas configuracoes (Python da Microsoft Store no Windows, paths de auth diferentes) pode falhar. **Salvar um token agora deixa a skill 100% deterministica.**

`AskUserQuestion`:
- question: "Quer salvar um token Vercel agora? (Recomendado se voce vai publicar em guarda-chuva)"
- header: "Token Vercel"
- multiSelect: false
- options:
  1. "Sim, vou pegar e colar agora (Recomendado)" — "Vou abrir vercel.com e gerar um token."
  2. "Pular (uso o auth.json do CLI quando precisar)" — "A skill vai tentar resolver automaticamente; caso falhe, ela me avisa pra rodar setup de novo."

Se "Pular" → seguir pro Passo 5.

Se "Sim", exiba **literalmente**:

> **Como gerar:**
> 1. Acesse https://vercel.com/account/tokens
> 2. Clique em "Create Token"
> 3. Nome: `agente-inhouse` (ou o que preferir)
> 4. Scope: **Full Account** (precisa de read em deployments + files)
> 5. Expiration: 1 ano e ok
> 6. Copie o token gerado e cole abaixo.

`AskUserQuestion`:
- question: "Cole o token Vercel (comeca com sequencia alfanumerica longa):"
- header: "Token"
- multiSelect: false
- options:
  1. "Cancelar" — "Pular essa etapa, configurar depois."

(O usuario colara via "Other" com o token.) Capturar como `$VERCEL_TOKEN` e validar:

- Formato basico: `^[a-zA-Z0-9_-]{24,}$`
- Funciona? Testar com: `curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $VERCEL_TOKEN" "https://api.vercel.com/v2/user"` deve retornar `200`.

Se reprovou (formato invalido ou 401/403): exibir o erro, oferecer cancelar ou tentar de novo.

Se passou, append em `.env.local` (criar linha nova se nao existe; substituir se ja existe):

Use `Read` em `.env.local`. Se `VERCEL_TOKEN=` ja esta la, use `Edit` pra trocar valor. Senao, use `Edit` (append) com:

```
VERCEL_TOKEN={token}
```

Confirmar:
```bash
grep -E "^VERCEL_TOKEN=" .env.local && echo "OK" || echo "FALHA"
```

- Sucesso → exibir `[OK] VERCEL_TOKEN salvo em .env.local — pronto pra publicar em guarda-chuva.`
- Falha → Fallback "vercel-token-falhou" (mensagem hardcoded: `Nao consegui gravar VERCEL_TOKEN no .env.local. Voce pode adicionar manualmente: edite .env.local na raiz do repo e acrescente uma linha "VERCEL_TOKEN={seu-token}".`).

Em qualquer caso, seguir para Passo 5.

---

## Passo 5 — Conexao com o Supabase (dados de deals)

> **Pular este passo se `modulos` nao inclui Dados de deals.**

**Contexto pra voce, agente (nao exiba):** o servidor `supabase` do `.mcp.json` roda o `postgres-mcp` via `uvx`, so leitura (`--access-mode=restricted`), e pega a URL do banco em `${SUPABASE_PG_URL}`, no ambiente do Claude. **Ele nao le o `dashboard/.env`.** Sem a variavel, o servidor recebe o texto `${SUPABASE_PG_URL}` no lugar da URL, nao conecta e o Claude mostra "Connection closed". Tres armadilhas ja derrubaram colaboradores (2026-10-22), e os comandos abaixo evitam as tres:

1. O host direto `db.vymnlivcgokmyonqlkah.supabase.co` so funciona em IPv6 e falha na maioria das redes. O certo e o **pooler** `aws-1-sa-east-1.pooler.supabase.com:5432`, com o usuario `looker_readonly.vymnlivcgokmyonqlkah` (com o sufixo do projeto).
2. A senha tem caracteres especiais. Dentro da URL, `#` vira `%23` (sem isso a URL e cortada no `#`) e `$` vira `%24`.
3. No PowerShell, um `$` entre aspas duplas e lido como variavel e some da senha. E colar varias linhas de uma vez faz o `Read-Host` engolir a linha seguinte como senha. Por isso o comando do Windows e uma linha so, com aspas simples.

**A senha nunca passa pelo chat.** A pessoa digita a senha no terminal dela, e o `checar_supabase.py` nunca imprime a senha. Nao peca a senha, e se ela for colada no chat, nao repita.

Onde a variavel fica: no **Windows**, nas variaveis de usuario (o app herda). No **Mac/Linux**, no `env` do `~/.claude/settings.json`: o app do Mac ignora variaveis exportadas no `~/.zshrc`, e o `env` do settings vale em toda sessao.

### 5.1 — uv instalado?

Use `Bash`:
```
uvx --version 2>/dev/null || "$HOME/.local/bin/uvx" --version 2>/dev/null || echo "UV_NAO_INSTALADO"
```

- Retornou versao → exiba `[OK] uv {versao}` e siga para 5.2.
- `UV_NAO_INSTALADO` → exiba conforme `os_user`:

**Se Windows:**
> O `uv` e o programa que roda a conexao com o banco. Pra instalar:
> 1. Abra o **PowerShell** (tecla Windows, digite `PowerShell` e de Enter).
> 2. Cole a linha abaixo e de Enter:
>    `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
> 3. Quando terminar, me diga "instalei".

**Se Mac ou Linux:**
> O `uv` e o programa que roda a conexao com o banco. Pra instalar:
> 1. Abra o Terminal.
> 2. Cole a linha abaixo e de Enter:
>    `curl -LsSf https://astral.sh/uv/install.sh | sh`
> 3. Quando terminar, me diga "instalei".

Aguarde "instalei" e rode o mesmo comando de checagem. Se ainda der `UV_NAO_INSTALADO` → Fallback "uv-falhou".

### 5.2 — Senha do banco

`AskUserQuestion`:
- question: "Voce ja tem a senha do usuario de leitura do banco (looker_readonly)?"
- header: "Senha"
- multiSelect: false
- options:
  1. "Nao tenho / nao sei (Recomendado)" — "Te explico como pedir."
  2. "Sim, ja tenho" — "O Victor ja me passou."

Se "Nao tenho", exiba **literalmente**:

> Peca a senha do usuario `looker_readonly` ao Victor (`victor.lopes@buzzmonitor.com.br`). Se der, use um gerenciador de senhas em vez de mensagem.
>
> **Nao cole a senha aqui no chat.** No proximo passo ela vai direto num comando que voce roda no seu terminal, e eu nao vejo.
>
> Quando tiver a senha, me diga "tenho". Se for demorar, a gente pausa e voce roda `/setup-agencia` de novo depois.

Aguarde "tenho" (ou ofereca o Fallback "usuario-trava").

### 5.3 — Gravar a variavel (quem roda e a pessoa, no terminal dela)

Exiba **literalmente**, conforme `os_user`:

**Se Windows:**
> 1. Abra o **PowerShell** (tecla Windows, digite `PowerShell` e de Enter). Tem que ser o PowerShell, nao o Prompt de Comando.
> 2. Copie a linha abaixo **inteira** (e uma linha so), cole no PowerShell e de Enter:
>
> ```powershell
> $s = Read-Host 'Senha do looker_readonly' -AsSecureString; $p = [Runtime.InteropServices.Marshal]::PtrToStringBSTR([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s)); [Environment]::SetEnvironmentVariable('SUPABASE_PG_URL', 'postgresql://looker_readonly.vymnlivcgokmyonqlkah:' + [uri]::EscapeDataString($p.Trim()) + '@aws-1-sa-east-1.pooler.supabase.com:5432/postgres', 'User'); 'Variavel gravada.'
> ```
>
> 3. Quando ele pedir a senha, cole e de Enter. Vao aparecer asteriscos no lugar das letras, e normal.
> 4. Quando aparecer `Variavel gravada.`, me diga "pronto".

**Se Mac ou Linux:**
> 1. Abra o Terminal.
> 2. Copie a linha abaixo **inteira** (e uma linha so), cole e de Enter:
>
> ```bash
> python3 -c "import getpass,json,pathlib,urllib.parse as u; p=pathlib.Path.home()/'.claude'/'settings.json'; d=json.loads(p.read_text()) if p.exists() else {}; s=getpass.getpass('Senha do looker_readonly: ').strip(); d.setdefault('env',{})['SUPABASE_PG_URL']='postgresql://looker_readonly.vymnlivcgokmyonqlkah:'+u.quote(s,safe='')+'@aws-1-sa-east-1.pooler.supabase.com:5432/postgres'; p.parent.mkdir(exist_ok=True); p.write_text(json.dumps(d,indent=2)+'\n'); print('Variavel gravada.')"
> ```
>
> 3. Quando ele pedir a senha, cole e de Enter. Nada aparece enquanto voce digita, e normal.
> 4. Quando aparecer `Variavel gravada.`, me diga "pronto".

Aguarde "pronto".

### 5.4 — Validar a conexao

Use `Bash` (timeout 180s; na primeira vez o uv baixa o Python 3.12 e o driver do Postgres, entao pode levar uns 30s):
```
UV=$(command -v uv || echo "$HOME/.local/bin/uv"); "$UV" run --no-project --python 3.12 --with "psycopg[binary]" python .claude/skills/setup-agencia/checar_supabase.py
```

O script le a variavel de onde o 5.3 gravou, entao funciona sem reiniciar nada. Ele confere o formato, conecta, roda um `SELECT` e conta as tabelas de deals visiveis.

- `[OK] Conectado no Supabase ...` → exiba a linha, marque `supabase_ok = true` e siga para 5.5 com o valor de `ENV_ARQUIVO=`.
- `ERRO=...` → trate pelo codigo:

| Codigo | O que fazer |
|---|---|
| `VAR_AUSENTE` | A variavel nao foi gravada. Repita o 5.3 (no Windows, confira se colou no PowerShell e nao no Prompt de Comando). |
| `HOST_DIRETO`, `HOST_DESCONHECIDO`, `USUARIO_SEM_SUFIXO`, `CARACTERE_CRU`, `FORMATO_INVALIDO`, `SENHA_VAZIA` | A variavel foi gravada a mao, fora do comando do 5.3. Repita o 5.3: o comando sobrescreve o valor. |
| `SENHA_ERRADA` | A senha nao confere. Peca de novo ao Victor e repita o 5.3. **Nao fique tentando:** depois de varias senhas erradas o Supabase bloqueia o IP por um tempo, e o bloqueio pega todo mundo na mesma rede. |
| `USUARIO_ERRADO` | O pooler nao reconheceu o usuario → Fallback "supabase-falhou". |
| `REDE` | Esta rede nao alcanca o banco (firewall, VPN, sem internet) ou o IP foi bloqueado por senhas erradas. Tente outra rede; se continuar → Fallback "supabase-falhou". |
| `OUTRO` | Fallback "supabase-falhou", com o detalhe que o script mostrou (ele ja vem sem a senha). |

Depois de 2 tentativas sem sucesso, ofereca pular este modulo (Fallback "usuario-trava").

### 5.5 — Espelhar no `dashboard/.env`

Os scripts Python do repo (`/auditar-deals-cm`, a parte de conversao do `/seo-report`, os exportadores das dashboards) leem o `dashboard/.env`, nao a variavel. Deixar os dois iguais evita que um aponte pra um lugar e o outro pra outro.

Conforme o `ENV_ARQUIVO=` do 5.4:
- `igual` → exiba `[OK] dashboard/.env ja usa a mesma conexao.`
- `ausente` → rode o comando do 5.4 com `--gravar-env` no final (sem perguntar; o arquivo e gitignored). Espere `ENV_ARQUIVO=gravado` e exiba `[OK] Conexao gravada tambem em dashboard/.env.`
- `diferente` → `AskUserQuestion`:
  - question: "O dashboard/.env tem outra conexao com o banco. Troco pela que acabou de funcionar?"
  - header: "dashboard/.env"
  - multiSelect: false
  - options:
    1. "Sim, trocar (Recomendado)" — "O arquivo fica igual a variavel que acabou de conectar."
    2. "Nao, manter como esta" — "Nao mexo no arquivo."

  Se "Sim" → rode com `--gravar-env` e espere `ENV_ARQUIVO=gravado`. O script so troca a linha `SUPABASE_PG_URL=` e mantem as outras.

### 5.6 — Reiniciar o Claude (fica pro fim do setup)

O Claude so le variaveis novas quando abre, entao o servidor `supabase` so conecta depois de reiniciar. Nao peca isso agora (encerraria o setup). O lembrete vai no resumo final (Passo 7).

---

## Passo 6 — Test drive (opcional)

`AskUserQuestion`:
- question: "Quer fazer um teste rapido pra confirmar que tudo funciona?"
- header: "Teste"
- multiSelect: false
- options:
  1. "Sim, vamos testar (Recomendado)" — "Roda uma skill leve pra ver se esta OK."
  2. "Nao, depois eu testo" — "Termina o setup aqui."

Se "Sim":
- Se `bunzzai_ok == true` → sugerir: "Vou rodar `/bunzzai buzzmonitor_brl` (analise de tendencias de uma conta — leve e ja te mostra a interface). Posso?"
- Senao se `notion_ok == true` → sugerir: "Vou rodar `/news-pesquisar buzzmonitor brasil` como teste. Posso?"
- Senao → pular teste, ir direto ao Passo 7.

(O Supabase nao entra no test drive: o servidor `supabase` so conecta depois de reiniciar o Claude.)

Aguarde "sim". Depois envie literalmente:

> "Execute o fluxo completo da skill `/{skill}` com os argumentos `{argumentos}`. Consulte `.claude/skills/{skill}/SKILL.md` e execute todos os passos na integra."

---

## Passo 7 — Resumo final (texto literal)

Exiba (substitua os ✓/✗ conforme o estado real — omita as linhas que nao se aplicam ao perfil do usuario, ex: nao mostrar "Vercel CLI" se Landing Pages nao foi marcado):

> 🎉 **Setup completo!** Aqui esta o que esta pronto:
>
> - [✓ ou ✗] Notion MCP conectado
> - [✓ ou ✗] Python {versao} instalado (so necessario pra Landing Pages e auditorias pontuais)
> - [✓ ou ✗] MCP Bunzzai conectado (fonte unica de analise de Meta Ads — sem token expirando)
> - [✓ ou ✗] Vercel CLI autenticado em elife-group
> - [✓ ou ✗] Conexao com o Supabase testada (deals, so leitura)
>
> **Comandos pra comecar (todos abrem guias interativos):**
> - `/escrever` — copy
> - `/newsletter` — newsletters
> - `/traduzir` — traducao PT-PT / ES-LATAM
> - `/anuncios` — analise de Meta Ads (via Bunzzai)
> - `/landing-page` — landing pages
> - Dados de deals: pergunte direto no chat, ex: `quantos deals CM fechamos em setembro?`
>
> **Falta uma coisa pro Supabase:** o Claude so le a conexao nova quando abre. Feche o Claude **de vez** e abra de novo. No Windows, clique com o botao direito no icone dele perto do relogio e escolha Sair (fechar so a janela nao basta). No Mac, use Cmd+Q. Se aparecer um pedido pra aprovar o servidor `supabase` do projeto, aprove. Depois, numa conversa nova, peca `liste as tabelas de deals no Supabase` pra conferir.
>
> **Quando terminar alteracoes:** rode `/commit` — ele cria uma branch, commita e abre um Pull Request pro Victor revisar. Nunca commita em main.
>
> Qualquer duvida, leia `CLAUDE.md` na raiz do projeto ou pergunte aqui. Bom trabalho!

---

## Fallback (mensagens hardcoded)

### "python-falhou"
> Nao encontrei Python 3.10+. Reveja o passo de instalacao ou peca ajuda ao admin. Python so e estritamente necessario pra Landing Pages (PageSpeed CLI) e auditorias pontuais em `meta-ads-legacy/`. As skills `/escrever`, `/traduzir`, `/newsletter` e `/anuncios` (Bunzzai) funcionam sem Python local. Quer continuar sem Python?

(Se "sim", marque `python_ok = false` e pule pro proximo passo aplicavel.)

### "notion-mcp-falhou"
> A conexao com o Notion nao respondeu. Causas comuns:
> 1. Voce autorizou o workspace errado (autorize so o do Grupo Elife)
> 2. Sua conta Notion nao tem acesso ao workspace do Grupo Elife — peca ao admin pra te adicionar como membro
>
> Por enquanto, podemos pular esse passo e configurar os demais modulos. Quer seguir?

### "bunzzai-mcp-falhou"
> O MCP Bunzzai nao aparece na sua lista de MCPs conectados. Sem ele, `/bunzzai` e `/bunzzai-geral` (que sao a fonte unica de analise de Meta Ads desde 2026-06-22) nao funcionam.
>
> **Como resolver:**
> 1. Fale com o Victor (`victor.lopes@buzzmonitor.com.br`) ou com o admin do agente — eles tem as credenciais do MCP Bunzzai.
> 2. A configuracao e feita uma vez so, no seu Claude Code global (nao no repo).
> 3. Depois de configurar, reinicie o Claude Code e rode `/setup-agencia` de novo.
>
> Por enquanto, podemos pular esse passo e configurar os demais modulos. Quer seguir?

### "vercel-cli-falhou"
> Nao consegui rodar o Vercel CLI via npx. Causas comuns:
> 1. Sem internet ou firewall corporativo
> 2. Node.js nao instalado (Vercel CLI precisa de Node 16+)
>
> Tente abrir um terminal novo e rodar `node --version`. Se der "command not found", instale Node em https://nodejs.org/ (LTS). Depois retome com `/setup-agencia`.

### "vercel-login-falhou"
> O login no Vercel nao completou. Causas comuns:
> 1. Voce fechou o navegador antes de autorizar
> 2. Login com conta errada (use a conta vinculada ao Grupo Elife)
> 3. Timeout (mais de 3min sem clicar)
>
> Rode `npx vercel logout` pra limpar e me diga "tentar de novo". Vou refazer o login.

### "vercel-org-falhou"
> Voce esta logado mas nao esta na org `elife-group` (`team_nC991VqUuSU2jXZN152xqqEg`). Peca ao admin pra te adicionar como membro do team Vercel. Sem isso, `/lp-publicar` nao consegue acessar os projetos guarda-chuva.
>
> Pode pular esse modulo por enquanto e usar so as outras skills. Quer continuar?

### "lp-sibling-falhou"
> Nao consegui escrever `.env.local` na raiz do repo. Causas comuns:
> 1. Permissao de escrita negada (rode o terminal como admin se for Windows)
> 2. O caminho que voce escolheu nao existe e nao consegui criar
> 3. O caminho cai dentro do repo ou em pasta sync-watched (OneDrive/iCloud/Dropbox)
>
> Tente de novo escolhendo outra pasta, ou crie `.env.local` manualmente na raiz com:
> ```
> LP_SIBLING_BASE=/caminho/que/voce/quer
> ```

### "uv-falhou"
> Nao encontrei o `uv`, o programa que roda a conexao com o banco. Rode de novo o comando de instalacao num terminal novo e confira se terminou sem erro. Se continuar, peca ajuda ao Victor.
>
> Por enquanto, podemos pular a conexao com o Supabase e configurar os demais modulos. Quer seguir?

### "supabase-falhou"
> Nao consegui conectar no banco (`{codigo}`{: detalhe}). Isso costuma ser do lado da conta, nao seu. Mande esse codigo ao Victor (`victor.lopes@buzzmonitor.com.br`) pra ele conferir o usuario `looker_readonly`. O codigo nao contem a senha.
>
> Por enquanto, podemos pular a conexao com o Supabase e configurar os demais modulos. Quer seguir?

### "usuario-trava" (use a qualquer momento)
> Sem problemas. Voce pode parar aqui e voltar depois — basta rodar `/setup-agencia` de novo. O que ja configurou (Notion, Python, .env, Vercel, Supabase etc.) fica salvo. Quer parar?
