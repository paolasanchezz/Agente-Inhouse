---
name: setup-agencia
description: Guia interativo de primeiro setup para novos colaboradores do agente inhouse. Conduz do zero (instalar Python, conectar Notion, configurar token Meta, autenticar Vercel CLI para Landing Pages) ate a primeira skill rodando. Usar quando o usuario digitar /setup-agencia ou disser "e minha primeira vez" / "como comeco".
argument-hint: "(opcional) — texto livre. Ex: /setup-agencia | /setup-agencia 'so meta ads' | /setup-agencia 'so copy e newsletter' | /setup-agencia 'so lp'"
allowed-tools: AskUserQuestion, Read, Bash, Glob
version: 0.5.0
---

# Skill: /setup-agencia — Setup guiado para newbies

Voce esta executando um **script deterministico** de onboarding. Nao improvise perguntas, nao pule passos, nao invente opcoes. Siga exatamente o roteiro abaixo.

## Principios invioláveis

1. **Uma pergunta por vez.** Nunca empilhe perguntas no mesmo `AskUserQuestion`.
2. **Sempre marque a opcao recomendada com `(Recomendado)`** no label.
3. **Linguagem PT-BR coloquial e didatica.** Assuma que o usuario pode nunca ter aberto um terminal.
4. **Apos cada acao tecnica (instalar, copiar, etc.), valide antes de seguir.** Nao acumule falhas silenciosas.
5. **Falhas → mensagem hardcoded de "Fallback"**, nao improviso.
6. **No final, rode `check_setup.py` (se Meta Ads foi configurado) e ofereca um test drive.**
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
  1. "Newsletters (/newsletter)" — "Gerar newsletters semanais para as marcas."
  2. "Copy / anuncios escritos (/escrever)" — "Criar, revisar ou pesquisar copy."
  3. "Traducao de copy (/traduzir)" — "Traduzir copy para PT-PT ou ES-LATAM."
  4. "Analise de Meta Ads (/anuncios)" — "Relatorios de performance de campanhas."
  5. "Landing Pages (/landing-page)" — "Criar e publicar LPs no Vercel."

Guarde como `modulos`. Determina quais blocos de setup vamos rodar:
- **Newsletter / Copy / Traducao** → exigem **Notion MCP** funcionando → **rodar Passo 2**
- **Meta Ads** → exige **Python + .env do meta-ads** → **rodar Passo 3**
- **Landing Pages** → exige **Vercel CLI autenticado** → **rodar Passo 4**
- Quem marca tudo, faz tudo.

---

## Passo 2 — Setup do Notion MCP

> **Pular este passo se `modulos` nao inclui nenhum dos: Newsletter, Copy, Traducao.**

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

## Passo 3 — Setup do Python + Meta Ads

> **Pular este passo se `modulos` nao inclui Meta Ads.**

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

### 3.3 — Instalar dependencias

Exiba:
> Vou instalar as bibliotecas Python que o modulo Meta Ads precisa. Pode demorar 1-2 minutos.

Use `Bash` (use `python3` se Mac/Linux):
```
cd meta-ads && python -m pip install -r requirements.txt
```

- Sucesso → exiba `[OK] Dependencias instaladas` e siga.
- Erro → Fallback "pip-falhou".

### 3.4 — Token Meta

Exiba **literalmente**:

> Agora a parte mais importante: voce precisa do **seu** token de acesso a API do Meta. Cada pessoa do time tem o proprio token (nao compartilhamos um unico, por seguranca).
>
> **Pre-requisito:** o admin do Grupo Elife ja te adicionou ao Business Manager? Se nao, pause aqui e peca primeiro — e uma pessoa especifica que faz isso.

`AskUserQuestion`:
- question: "Voce ja tem acesso ao Business Manager do Grupo Elife?"
- header: "Acesso BM"
- multiSelect: false
- options:
  1. "Sim, ja tenho acesso" — "Consigo entrar em business.facebook.com com minha conta."
  2. "Nao / nao tenho certeza" — "Preciso pedir acesso primeiro."

Se "Nao" → exibir **literalmente**:

> Pare aqui. Peca ao admin pra te adicionar como **Funcionario** com permissao **`ads_read`** nas contas que voce vai analisar. Quando tiver acesso, rode `/setup-agencia` de novo.

E sair da skill (nao prossiga).

Se "Sim" → exibir **literalmente**:

> **Como gerar seu token (passo a passo):**
> 1. Acesse https://business.facebook.com → entre com sua conta.
> 2. Clique no seu perfil (canto inferior esquerdo) → "Configuracoes de negocios".
> 3. No menu lateral: **Usuarios → Tokens de acesso → Gerar token**.
> 4. Selecione a App do Grupo Elife (peca ao admin se nao souber qual).
> 5. **Permissoes:** marque **APENAS `ads_read`**. Nao marque nada de escrita.
> 6. Clique em "Gerar token" e **copie o texto longo** (comeca com `EAA...`).
> 7. Anote a data de hoje no formato `YYYY-MM-DD`.

`AskUserQuestion`:
- question: "Conseguiu gerar e copiar o token?"
- header: "Token"
- multiSelect: false
- options:
  1. "Sim, copiei o token e anotei a data" — "Pronto pra colar no .env."
  2. "Nao consegui / deu erro" — "Preciso de ajuda."

Se "Nao" → Fallback "token-falhou".
Se "Sim" → 3.5.

### 3.5 — Criar e preencher o `.env` (so 2 valores!)

Use `Bash` para verificar se ja existe:
```
ls meta-ads/.env 2>/dev/null && echo EXISTE || echo NAO_EXISTE
```

Se EXISTE → perguntar:

`AskUserQuestion`:
- question: "Ja existe um meta-ads/.env. Quer sobrescrever ou manter?"
- header: ".env existe"
- multiSelect: false
- options:
  1. "Manter (Recomendado)" — "Vou editar o existente em vez de recriar."
  2. "Sobrescrever" — "Comeca do zero (perde o que ja estava)."

Se NAO_EXISTE ou "Sobrescrever":
```
cd meta-ads && cp .env.example .env
```
(Windows: `cd meta-ads && copy .env.example .env`)

Exiba **literalmente**:

> Pronto, o arquivo `meta-ads/.env` esta criado. **Boa noticia: voce so precisa preencher 2 linhas.** Os IDs das 6 contas ja estao configurados no codigo (sao iguais pra todo mundo do time).
>
> 1. Abra `meta-ads/.env` no editor de texto (Windows: bloco de notas; Mac: TextEdit; ou direto no Claude Code).
> 2. Em `META_ACCESS_TOKEN=`, cole o token que voce copiou (depois do `=`, sem aspas, sem espaco).
> 3. Em `META_TOKEN_CREATED_AT=`, coloque a data de hoje no formato `YYYY-MM-DD`.
> 4. Salve o arquivo e me diga "salvei".

Aguarde "salvei".

### 3.6 — Validar setup com check_setup.py

Use `Bash` (use `python3` se Mac/Linux):
```
cd meta-ads && python scripts/check_setup.py
```

Interprete a saida:
- **Exit 0** → exibir: `[OK] Tudo configurado! Suas 6 contas estao acessiveis.` e marcar `meta_ok = true`.
- **Exit 1** → identificar o erro na saida e usar Fallback correspondente:
  - "Token invalido" → Fallback "token-rejeitado"
  - "sem permissao" → Fallback "conta-sem-acesso"
  - Outro → mostrar a saida bruta e perguntar se quer parar ou tentar de novo.

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

## Passo 5 — Test drive (opcional)

`AskUserQuestion`:
- question: "Quer fazer um teste rapido pra confirmar que tudo funciona?"
- header: "Teste"
- multiSelect: false
- options:
  1. "Sim, vamos testar (Recomendado)" — "Roda uma skill leve pra ver se esta OK."
  2. "Nao, depois eu testo" — "Termina o setup aqui."

Se "Sim":
- Se `meta_ok == true` → sugerir: "Vou rodar `/meta-ads-fetch buzzmonitor_brl ultimos_30` (so sincroniza dados, sem gerar relatorio). Posso?"
- Senao se `notion_ok == true` → sugerir: "Vou rodar `/news-pesquisar buzzmonitor brasil` como teste. Posso?"
- Senao → pular teste, ir direto ao Passo 5.

Aguarde "sim". Depois envie literalmente:

> "Execute o fluxo completo da skill `/{skill}` com os argumentos `{argumentos}`. Consulte `.claude/skills/{skill}/SKILL.md` e execute todos os passos na integra."

---

## Passo 6 — Resumo final (texto literal)

Exiba (substitua os ✓/✗ conforme o estado real — omita as linhas que nao se aplicam ao perfil do usuario, ex: nao mostrar "Vercel CLI" se Landing Pages nao foi marcado):

> 🎉 **Setup completo!** Aqui esta o que esta pronto:
>
> - [✓ ou ✗] Notion MCP conectado
> - [✓ ou ✗] Python {versao} instalado
> - [✓ ou ✗] Token Meta valido (expira em ~60 dias, **anote na agenda pra renovar**)
> - [✓ ou ✗] 6 contas Meta acessiveis
> - [✓ ou ✗] Vercel CLI autenticado em elife-group
>
> **Comandos pra comecar (todos abrem guias interativos):**
> - `/escrever` — copy
> - `/newsletter` — newsletters
> - `/traduzir` — traducao PT-PT / ES-LATAM
> - `/anuncios` — analise de Meta Ads
> - `/landing-page` — landing pages
>
> **Quando terminar alteracoes:** rode `/commit` — ele cria uma branch, commita e abre um Pull Request pro Victor revisar. Nunca commita em main.
>
> **Quando o token expirar** (em ~60 dias), voce vai ver `[AVISO] Token Meta Ads expira em N dia(s)` ao rodar `/anuncios`. Quando aparecer, repita o Passo 1 deste setup ou veja `meta-ads/SETUP.md` (passo "Renovacao").
>
> Qualquer duvida, leia `CLAUDE.md` na raiz do projeto ou pergunte aqui. Bom trabalho!

---

## Fallback (mensagens hardcoded)

### "python-falhou"
> Nao encontrei Python 3.10+. Reveja o passo de instalacao ou peca ajuda ao admin. Voce ainda pode usar `/escrever`, `/traduzir` e `/newsletter` sem Python — so `/anuncios` precisa. Quer continuar sem Meta Ads?

(Se "sim", marque `meta_ok = false` e pule pro Passo 4.)

### "pip-falhou"
> A instalacao das bibliotecas falhou. Causas comuns:
> 1. Sem internet ou firewall corporativo
> 2. Python instalado em local protegido
>
> Tente: `python -m pip install --user -r requirements.txt` (com `--user`).
> Se persistir, mande o erro exato pro admin.

### "notion-mcp-falhou"
> A conexao com o Notion nao respondeu. Causas comuns:
> 1. Voce autorizou o workspace errado (autorize so o do Grupo Elife)
> 2. Sua conta Notion nao tem acesso ao workspace do Grupo Elife — peca ao admin pra te adicionar como membro
>
> Por enquanto, podemos pular esse passo e configurar so Meta Ads. Quer seguir?

### "token-falhou"
> Sem problema. Causas comuns de erro ao gerar token:
> 1. Voce nao foi adicionado ao Business Manager ainda
> 2. A App do Grupo Elife nao aparece na lista — peca o nome ao admin
> 3. Permissao `ads_read` nao aparece — voce esta logado na conta errada
>
> Resolva e me diga "consegui". Ou, se preferir parar aqui, diga "pausar" e voltamos depois com `/setup-agencia`.

### "token-rejeitado"
> A API recusou seu token. Causas:
> 1. Voce copiou so parte do token (eles tem 200+ caracteres — copie tudo)
> 2. O token foi revogado ou expirou
> 3. Voce gerou na conta Facebook errada
>
> Volte ao Business Manager, gere de novo (Passo 1) e cole no `.env`. Depois me diga "atualizei" pra eu validar de novo.

### "conta-sem-acesso"
> Sua conta foi criada, mas o admin ainda nao te deu permissao em alguma das 6 contas de anuncio. Peca pra te adicionar com `ads_read` em todas. Voce pode usar as contas que **estao** acessiveis enquanto isso. Quer continuar mesmo assim?

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

### "usuario-trava" (use a qualquer momento)
> Sem problemas. Voce pode parar aqui e voltar depois — basta rodar `/setup-agencia` de novo. O que ja configurou (Notion, Python, .env, Vercel etc.) fica salvo. Quer parar?
