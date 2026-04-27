---
name: lp-publicar
description: Sincroniza LP para pasta sibling — solo (1 projeto = 1 LP) ou guarda-chuva (N LPs num mesmo projeto Vercel quando o dominio ja esta atribuido). Deploya via Vercel CLI, valida PageSpeed + headers, publica relatorio Notion. Garante zero vazamento do repo interno e zero regressao em LPs vizinhas.
argument-hint: "[marca] [slug] [dominio-opcional] — ex: buzzmonitor monitoramento-maio webinar.buzzmonitor.com"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-pages, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-update-page
version: 1.5.0
---

# Skill: Publicar Landing Page

Voce sincroniza a LP do repo do agente para uma pasta sibling isolada fora do repo, roda deploy na Vercel, valida e publica relatorio no Notion. **Regra inegociavel: nenhum arquivo do repo interno (.env, skills, conhecimento/, brand/, meta-ads/) pode vazar para a pasta sibling ou para o deploy.**

A skill opera em dois modos:

| Modo | Quando | Sibling | Resultado URL |
|---|---|---|---|
| **solo** | dominio nao fornecido OU fornecido mas sem projeto Vercel atribuido | `C:/Users/titof/Downloads/Claude/{marca}-lp-{slug}/` (novo) | `https://{marca}-lp-{slug}-{hash}.vercel.app/{slug}` ou dominio fresco |
| **guarda-chuva** | dominio ja atribuido a outro projeto Vercel (Passo 0.5 detecta) | `C:/Users/titof/Downloads/Claude/{nome-do-projeto-detectado}/` (existente) | `https://{dominio}/{slug}` (LP nova convive com vizinhas) |

A diferenca pratica: no modo guarda-chuva voce **nao cria projeto Vercel novo**, **anexa a LP** como subpasta ao sibling existente, **namespaceia assets por marca** (`/assets/{marca}/X`) para evitar colisao com vizinhas, e o relatorio inclui smoke test de **todas** as LPs do projeto.

## Passo 0: Parsing e Contexto

Leia `.claude/skills/lp-preparar/CONTEXT.md`.

Parsing de `$ARGUMENTS`:

| Argumento | Valores | Obrigatorio |
|---|---|---|
| `marca` | `buzzmonitor` \| `buzzcreators` \| `cxpress` \| `elife` | Sim |
| `slug` | kebab-case | Sim |
| `dominio` | FQDN (ex: `webinar.buzzmonitor.com`) | Nao |

Paths default (modo solo):
- Fonte: `landing-pages/{marca}/{slug}/index.html`
- Sibling: `C:/Users/titof/Downloads/Claude/{marca}-lp-{slug}/`
- Dentro da sibling: `{slug}/index.html` + `assets/` + `vercel.json` + `.gitignore` + `README.md`

Se fonte nao existe, PARE.

## Passo 0.5: Detectar modo (solo vs guarda-chuva)

Se `$dominio` foi fornecido, checar se ja esta atribuido a algum projeto Vercel da org.

```bash
VERCEL_TOKEN=$(cat "$APPDATA/com.vercel.cli/Data/auth.json" | python -c "import sys,json;print(json.load(sys.stdin).get('token',''))")
TEAM=team_nC991VqUuSU2jXZN152xqqEg  # elife-group

curl -s -H "Authorization: Bearer $VERCEL_TOKEN" \
  "https://api.vercel.com/v9/projects?teamId=$TEAM&limit=100" | \
  python -c "
import sys, json, os
data = json.load(sys.stdin)
target = os.environ['DOMAIN']
for p in data.get('projects', []):
    targets = p.get('targets', {}) or {}
    aliases = []
    for tgt in targets.values():
        if isinstance(tgt, dict):
            aliases.extend(tgt.get('alias') or [])
    if target in aliases:
        print(f'{p[\"name\"]}|{p[\"id\"]}')
        break
" DOMAIN="$DOMAIN"
```

Tres saidas possiveis:

| Saida | Modo | Decisao |
|---|---|---|
| Nenhum projeto encontrado | **solo** | Sibling = `{marca}-lp-{slug}` (novo). Comportamento default. |
| 1 projeto encontrado | **guarda-chuva** | Sibling = nome do projeto retornado pela API. Anexar LP como subpasta nele. |
| Erro de auth/API | **solo, com aviso** | Reportar erro mas seguir como solo. Anotar em "Pendencias" pra revisar. |

Se modo guarda-chuva: ler `{sibling-detectado}/.vercel/project.json` para confirmar `projectId` e `orgId` batem com o que a API retornou. Se nao baterem (sibling local stale), regenerar via `cd "{sibling}" && npx vercel link --yes --project={nome}` antes de seguir.

**Importante:** dominio nao fornecido sempre = modo solo, mesmo se outro projeto da org ja serve um dominio. Sem dominio, a skill nao tem sinal pra inferir guarda-chuva.

## Passo 1: Preparar Pasta Sibling

### Estrutura alvo (modo solo)

```
{sibling}/
├── {slug}/
│   └── index.html
├── assets/
│   └── logos/
│       ├── logo-primary.svg
│       └── logo-reversed.svg
├── vercel.json
├── .gitignore
└── README.md
```

### Estrutura alvo (modo guarda-chuva)

Sibling ja existe e ja tem LPs vizinhas. Voce **adiciona** sua LP como mais uma subpasta sem tocar nas outras.

```
{sibling}/
├── {outro-slug-1}/         ← LP existente (NAO TOCAR)
├── {outro-slug-2}/         ← LP existente (NAO TOCAR)
├── {slug}/                 ← LP que voce esta adicionando
│   └── index.html
├── assets/
│   ├── logos/              ← assets de marca legacy / da primeira LP do guarda-chuva (NAO TOCAR)
│   ├── {marca}/            ← seus assets (namespace por marca pra nao colidir com vizinhas)
│   │   └── ...
│   └── ...
├── vercel.json             ← NAO sobrescrever (ja configurado para multi-LP)
├── .gitignore
└── README.md               ← anexar nova LP a tabela existente
```

### 1.1 Criar pasta da LP

```bash
mkdir -p "{sibling}/{slug}"
mkdir -p "{sibling}/assets"
```

No modo guarda-chuva, **assert** que `{sibling}` ja existe (com `.vercel/project.json` la dentro). Se nao existe quando esperado, abortar — significa que a deteccao do Passo 0.5 retornou um nome de projeto sem sibling local correspondente. Caso: rodar `npx vercel link --yes --project={nome} --cwd={sibling-path}` para popular `{sibling}/.vercel/`.

### 1.2 Copiar index.html

```bash
cp "landing-pages/{marca}/{slug}/index.html" "{sibling}/{slug}/index.html"
```

### 1.3 Descobrir assets referenciados

Grep `src=`, `srcset=`, `href=` e `url(` no index.html fonte. Para cada referência, classificar pela origem do path **e o modo da skill**:

#### Modo solo

| Padrão no source | Vem do disco em | Vai para no deploy |
|---|---|---|
| `../../brand/{marca}/assets/X` | `brand/{marca}/assets/X` | `/assets/X` |
| `./assets/X` | `landing-pages/{marca}/{slug}/assets/X` | `/assets/X` |
| `/assets/X` (já absoluto) | checar `brand/{marca}/assets/X` primeiro, senão `landing-pages/{marca}/{slug}/assets/X` | `/assets/X` |

#### Modo guarda-chuva (namespace de marca obrigatorio)

| Padrão no source | Vem do disco em | Vai para no deploy |
|---|---|---|
| `../../brand/{marca}/assets/X` | `brand/{marca}/assets/X` | `/assets/{marca}/X` |
| `./assets/X` | `landing-pages/{marca}/{slug}/assets/X` | `/assets/{marca}/X` |
| `/assets/{marca}/X` (já absoluto e namespaceado) | `brand/{marca}/assets/X` ou `landing-pages/{marca}/{slug}/assets/X` | `/assets/{marca}/X` |

**Por que namespace por marca em guarda-chuva:** sem namespace, dois assets com o mesmo filename (ex: Buzzmonitor `logo-icon.png` e Buzzcreators `logo-icon.png`) colidem em `{sibling}/assets/logos/logo-icon.png` — sobrescrever quebra a LP vizinha.

**Detecção de colisão (modo guarda-chuva):** antes de copiar, comparar md5 do source com `{sibling}/assets/{nome-base}/{filename}` se existir. Se filename identico mas md5 diferente, abortar com erro claro: `asset {filename} colide com vizinha em {sibling-asset-path} (md5 diferente). Use namespace por marca.` (Em pratica isso nunca dispara se a regra acima for respeitada — o trigger e seguranca contra erro de skill futuro.)

Produzir lista de triplas: `(path-no-source, disco-origem, alvo-no-sibling-com-modo)`.

### 1.4 Copiar **apenas** esses assets

Para cada tripla, copiar `disco-origem` para `{sibling}/assets/...` preservando subcaminho. No modo guarda-chuva, prefixar com `{marca}/`.

Se `disco-origem` não existe, PARE com erro: `asset referenciado em linha {N} mas arquivo não encontrado nem em brand/ nem em landing-pages/{marca}/{slug}/assets/`.

**Não** usar `cp -r brand/{marca}/` cego — copiaria assets não-usados.

### 1.5 Reescrever paths no HTML copiado

No `{sibling}/{slug}/index.html`, substituir todos para absoluto:

#### Modo solo

- `../../brand/{marca}/assets/` → `/assets/`
- `./assets/` → `/assets/`

#### Modo guarda-chuva

- `../../brand/{marca}/assets/` → `/assets/{marca}/`
- `./assets/` → `/assets/{marca}/`
- (`/assets/{marca}/X` ja absoluto: nao reescreve)

Use `Edit` com `replace_all: true`.

**Verificação obrigatória pós-rewrite** — grep no HTML do sibling:

```bash
grep -nE "\\.\\./assets/|\\./assets/|\\.\\./\\.\\./brand/" "{sibling}/{slug}/index.html" && echo "VAZOU"
```

Se aparecer qualquer match, PARE — o rewrite não cobriu todos os casos. Caminho relativo + `cleanUrls: true` + `trailingSlash: false` resolve `./assets/X` para `/assets/X` na raiz do site (não para a pasta da LP), então qualquer `./` ou `../` sobrando vai 404 no live.

**Incidentes documentados:**
- 2026-04-27 (mascot 404): `mascot.png` da Buzzmonitor LP `monitoramento-concorrentes-maio-2026` deu 404 por dois deploys consecutivos com asset LP-local não copiado e path relativo intacto. Motivou §1.3-1.5 (v1.4.0) suportar `./assets/`.
- 2026-04-27 (multi-LP guarda-chuva): LP Buzzcreators `vendendo-com-creators` foi inicialmente publicada em projeto Vercel separado em vez de usar o guarda-chuva ja existente para `webinar.buzzmonitor.com`. Consolidacao manual + dois deploys. Motivou Passo 0.5 + namespace por marca (v1.5.0).

Remover também do `<title>` qualquer sufixo de trabalho: `[REVISADO]`, `[TESTE]`, `[DRAFT]`.

### 1.6 Escrever vercel.json

**Modo solo:** copiar `.claude/skills/lp-publicar/vercel.template.json` para `{sibling}/vercel.json` **sem modificacao**.

**Modo guarda-chuva:** **NAO sobrescrever** o `{sibling}/vercel.json` existente. Ele ja foi configurado para servir multi-LP. Em vez disso, comparar com o template:

```bash
diff "{sibling}/vercel.json" ".claude/skills/lp-publicar/vercel.template.json"
```

Se o sibling tem CSP/headers desatualizados em relacao ao template (ex: novo provedor de form recem-adicionado ao template), **avisar** o usuario e perguntar antes de patch-ar — outras LPs vizinhas podem depender de configuracao especifica nao-padrao.

O template inclui 7 headers de seguranca, incluindo **Content-Security-Policy (CSP)** ja configurado para permitir os provedores de form mais comuns (Jotform, RD Station, HubSpot), Google Fonts, analytics (GA, GTM) e video (YouTube, Vimeo).

**Quando ajustar o CSP:**
- LP usa provedor de form fora do default (ex: Typeform, Tally, Formspree) → adicionar dominio em `script-src`, `frame-src` e `form-action`.
- LP carrega script de terceiro nao listado (pixel de conversao custom, chatbot, etc.) → adicionar em `script-src` e `connect-src`.
- LP embeda iframe de outro servico → adicionar em `frame-src`.

Faca essa decisao **antes** do deploy grep-ando scripts e iframes no HTML:

```bash
grep -oiE "src=\"https?://[^\"]+\"|<iframe[^>]*src=\"[^\"]+\"" "{sibling}/{slug}/index.html" | sort -u
```

Se algum dominio nao estiver coberto pelo CSP default, edite `{sibling}/vercel.json` antes de deployar. Nao use `*` permissivo — quebra o sentido do header.

### 1.7 Escrever .gitignore

```
.vercel/
node_modules/
.DS_Store
```

### 1.8 Escrever README.md da sibling

**Modo solo:** criar README do zero.

```markdown
# {Marca} — LP {slug}

Artefato **publicado** da LP.

## Fonte-verdade

A fonte editavel vive no repo do agente inhouse:

```
Agente Inhouse/landing-pages/{marca}/{slug}/
```

Esta pasta e apenas o artefato de deploy — isolada do repo interno. Para atualizar: rodar `/lp-publicar {marca} {slug}` no repo do agente.

## Deploy

`npx vercel deploy --prod --yes` desta pasta.
```

**Modo guarda-chuva:** README ja existe (formato multi-LP). **Nao sobrescrever.** Em vez disso, ler o README existente e anexar a LP nova a tabela "LPs ativas" (se houver) ou em uma secao similar. Modelo:

```markdown
| Path | Marca | Fonte no repo |
|---|---|---|
| `/{slug-existente-1}` | {marca-1} | `Agente Inhouse/landing-pages/{marca-1}/{slug-existente-1}/` |
| `/{slug}` | **{Marca-da-nova} (novo)** | `Agente Inhouse/landing-pages/{marca}/{slug}/` |
```

Se o README do sibling nao seguir formato tabular, escolher: ou apenas anexar uma linha "Adicionada {marca}/{slug} em YYYY-MM-DD" ao final, ou regenerar o README inteiro pra padronizar. Nao decidir silenciosamente — perguntar ao usuario se o README precisa ser regenerado.

## Passo 2: Validacao de Isolamento (pre-deploy)

**Antes** de chamar `vercel deploy`, rode **3 checks** na pasta sibling. Qualquer um que retorne hit → PARE e avise o usuario. Nao deployar.

### 2.1 Paths/nomes sensíveis (estrutura)

```bash
grep -ril "meta-ads\|\.env\|conhecimento/\|\.claude/" "{sibling}/" || true
```

### 2.2 Diretorios do repo interno na raiz da sibling

```bash
ls "{sibling}/" | grep -E "^(meta-ads|conhecimento|brand|\.claude|\.env)$" && echo "VAZOU"
```

### 2.3 Strings sensíveis no conteudo (tokens, segredos)

Grep procura por padroes de credencial que nao deveriam estar num HTML/JS publico:

```bash
grep -rEil "VERCEL_TOKEN|META_ACCESS_TOKEN|FB_ACCESS_TOKEN|api[_-]?key[\"'=: ]|secret[\"'=: ]|bearer [A-Za-z0-9_-]{20,}|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY" "{sibling}/" || true
```

Exceções legítimas: nada. Se um provedor de form usa uma public key/publishable key, documentar como falso-positivo conhecido antes de prosseguir — nunca silenciar o check globalmente.

Se qualquer um dos 3 retornar hit, PARE. Corrija a origem (lp-gerar, sync) e rode de novo. Nao deployar com vazamento.

### 2.4 Baseline de hashes das LPs vizinhas (modo guarda-chuva)

Pular esta validacao em modo solo.

No modo guarda-chuva, capturar hash MD5 do `index.html` de **cada outra LP** do sibling **antes** do deploy. Esses hashes sao o baseline para o smoke test do Passo 3.4 — qualquer divergencia depois do deploy = regressao.

```bash
for OTHER_DIR in "{sibling}"/*/; do
  OTHER_SLUG=$(basename "$OTHER_DIR")
  if [ "$OTHER_SLUG" != "{slug}" ] && [ -f "$OTHER_DIR/index.html" ]; then
    OTHER_HASH=$(md5sum "$OTHER_DIR/index.html" | awk '{print $1}')
    echo "baseline /$OTHER_SLUG: $OTHER_HASH"
  fi
done
```

Guardar como `BASELINES_OTHERS` (lista `(slug, hash)`) para usar em 3.4.

Excecoes legitimas: nada. Se voce **intencionalmente** mudou outra LP do sibling neste deploy (ex: refatorou asset compartilhado), abortar e usar `/lp-publicar` separado para cada LP afetada — nao misturar entregas no mesmo deploy.

## Passo 3: Deploy

### 3.1 Baseline antes do deploy

Capture o hash do HTML que voce **quer** publicar. Ele e o ground-truth para validar depois se a live bate com o que voce subiu.

```bash
LOCAL_HASH=$(md5sum "{sibling}/{slug}/index.html" | awk '{print $1}')
LOCAL_MTIME=$(stat -c "%Y" "{sibling}/{slug}/index.html")
echo "local: $LOCAL_HASH (mtime $LOCAL_MTIME)"
```

Se `{sibling}/.vercel/project.json` existe, leia `projectId` e `orgId` dele — sao uteis no fallback do 3.3.

### 3.2 Rodar deploy

LP e site estatico (sem build step real) — use `--force` por padrao. Ele ignora cache de build server-side, o que evita o caso de a Vercel reusar um build anterior quando so os assets mudaram. Custo: zero (build estatico completa em <100ms).

```bash
cd "{sibling}" && npx --yes vercel deploy --prod --yes --force
```

**Rodar sempre em background** (`run_in_background: true` no Bash tool) com timeout >= 240s. O upload inicial costuma dedup 90%+ via content-hash (Vercel reconhece assets ja subidos em deploys anteriores), entao o passo demorado costuma ser o `Building...` e o alias swap, nao o upload.

Capturar do stdout final, que tem este formato quando sucesso:

```
Production: https://{hash}.vercel.app [Ns]
Aliased: https://{dominio} [Ns]
{ "status": "ok", "deployment": { "id": "dpl_...", ... } }
```

- URL provisoria: linha `Production: ...`
- Deploy ID: campo `deployment.id` do JSON final
- Alias confirmado: linha `Aliased: ...` (so aparece se o projeto ja tem alias configurado)

Se primeiro deploy do projeto, o comando pede confirmacao de projeto — passar `--name {marca}-lp-{slug}` na primeira vez e deixar o CLI salvar `.vercel/project.json`.

### 3.3 Se a CLI falhar — checar API antes de retry

A CLI da Vercel tem um bug intermitente onde o upload sobe corretamente, o deploy fica **READY server-side**, mas a CLI nao recebe a resposta final e aborta com:

```
FetchError: invalid json response body at https://api.vercel.com/v2/files?teamId=... reason: Unexpected end of JSON input
```

**Nao faca retry cego.** Em vez disso, consulte o estado real via MCP Vercel (ou API direta):

```
mcp__{vercel-mcp}__list_deployments
  projectId: <orgId+projectId de .vercel/project.json>
  teamId:    <orgId>
```

Ou via HTTP com token (`VERCEL_TOKEN`):

```bash
curl -s -H "Authorization: Bearer $VERCEL_TOKEN" \
  "https://api.vercel.com/v6/deployments?projectId={projectId}&teamId={orgId}&limit=1" | jq .
```

O deployment mais recente tem `createdAt` em ms-epoch. Se ele foi criado **nos ultimos ~120s** e `state == "READY"` e `target == "production"`, o deploy passou — ignore o erro da CLI e siga para 3.4 com esse `deployment.id`.

Caso contrario (mais antigo, ou state != READY), re-rode o comando do 3.2 **com o sibling igualzinho** — nao edite nada entre tentativas, senao voce arrisca publicar versao intermediaria como aconteceu na entrega de 2026-04-20.

### 3.4 Verificar que a live tem o conteudo certo

#### 3.4.a LP nova (sempre)

O teste de fumaca mais confiavel e comparar hash local com ETag/MD5 do HTML servido:

```bash
LIVE_URL="https://{dominio-ou-vercel-app}/{slug}"
LIVE_HASH=$(curl -s "$LIVE_URL" | md5sum | awk '{print $1}')
echo "local: $LOCAL_HASH"
echo "live:  $LIVE_HASH"
```

- **Hashes iguais:** perfeito, siga para 3.4.b (se aplicavel) ou Passo 4.
- **Hashes diferentes + headers mostram `X-Vercel-Cache: HIT` com `Age` alto:** cache de borda ainda nao rotacionou. Aguarde 60s e re-teste. Se persistir > 3 min, deploy falhou silenciosamente (3.3 acertou mas o alias nao mudou) — re-rode 3.2 com `--force`.
- **Hashes diferentes + `X-Vercel-Cache: MISS`:** a live serve um build antigo. Re-rode 3.2 com `--force`. Nao publique relatorio enquanto nao bater.

#### 3.4.b Vizinhas intactas (modo guarda-chuva)

Pular em modo solo.

Para cada `(slug, hash)` em `BASELINES_OTHERS` (capturado em 2.4), refazer smoke test:

```bash
for OTHER_SLUG_HASH in "${BASELINES_OTHERS[@]}"; do
  SLUG_OTHER=${OTHER_SLUG_HASH%:*}
  HASH_BASELINE=${OTHER_SLUG_HASH#*:}
  HASH_LIVE=$(curl -s "https://{dominio}/$SLUG_OTHER" | md5sum | awk '{print $1}')
  if [ "$HASH_BASELINE" = "$HASH_LIVE" ] ; then
    echo "OK /$SLUG_OTHER intacta"
  else
    echo "REGRESSAO /$SLUG_OTHER: baseline=$HASH_BASELINE live=$HASH_LIVE"
  fi
done
```

Se **qualquer** vizinha quebrou:
1. Investigar imediatamente (provavelmente vercel.json sobrescrito, asset removido, rewrite agressivo de path).
2. NAO publicar relatorio. Reverter mudanca.
3. O modo guarda-chuva tem promessa de zero regressao — qualquer divergencia inesperada e bug.

Comparacao bit-a-bit e paranoia necessaria: em static sites sem teste de build, o unico sinal de que o deploy publicou o que voce queria e o conteudo servido bater com o fonte-sibling. Em multi-LP, esse sinal precisa cobrir cada LP.

## Passo 4: Dominio (se fornecido)

Comportamento depende do modo (Passo 0.5):

### Modo solo

Se `$dominio` nao vazio e o Passo 0.5 confirmou que ele NAO esta atribuido a outro projeto:

```bash
cd "{sibling}" && npx --yes vercel domains add "{dominio}"
```

Capturar as instrucoes de DNS que o Vercel retorna (tipo A com IP `76.76.21.21` ou CNAME). Guardar para o relatorio.

Se falhar (ja configurado fora deste projeto, conflito), reportar mensagem e seguir — pode ser que voce devia estar no modo guarda-chuva (Passo 0.5 deve ter detectado, mas se passou direto, esse e o sinal). Se tiver duvida, abortar e reanalisar Passo 0.5.

### Modo guarda-chuva

Pular `vercel domains add` — o dominio ja esta atribuido ao sibling guarda-chuva. Tentar adicionar de novo retorna conflito.

URL final ja e `https://{dominio}/{slug}` — registrar para o relatorio sem chamar a CLI.

## Passo 5: Validacoes Pos-Deploy

URL alvo: se dominio configurado, usar dominio final; senao, URL `.vercel.app`.

### 5.1 PageSpeed Insights

Use `WebFetch`. URL do site alvo deve ser **URL-encoded** no parametro `url=` (ex: `:` vira `%3A`, `/` vira `%2F`). Exemplo com `https://webinar.buzzmonitor.com/monitoramento-maio`:

```
https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https%3A%2F%2Fwebinar.buzzmonitor.com%2Fmonitoramento-maio&strategy=mobile&category=performance&category=accessibility&category=seo&category=best-practices
```

Extrair do JSON de resposta:
- `lighthouseResult.categories.performance.score` * 100
- `lighthouseResult.categories.accessibility.score` * 100
- `lighthouseResult.categories.seo.score` * 100
- `lighthouseResult.categories.best-practices.score` * 100
- Core Web Vitals: LCP, CLS, TBT, FCP

### 5.2 Headers de seguranca

```bash
curl -sI "https://{URL}" | grep -iE "strict-transport-security|x-content-type-options|x-frame-options|referrer-policy|permissions-policy|cross-origin-opener-policy|content-security-policy"
```

Confirmar que todos os 7 headers estao presentes.

**Teste de CSP (opcional mas recomendado):** abrir a URL no navegador, abrir DevTools → Console, e verificar se ha `Refused to load...` ou `Content Security Policy directive...`. Se aparecer, algum recurso legitimo esta sendo bloqueado — ajustar o CSP em `{sibling}/vercel.json` e re-deployar. Common offenders: pixel de conversao nao listado, chatbot, fonte custom de outro CDN.

### 5.3 GTM servido

Ler `brand/{marca}/tracking.json`. Se houver GTM id resolvido (regions[{regiao}] ou default != null):

```bash
curl -s "https://{URL}" | grep -oE "(googletagmanager\.com/(gtm\.js|ns\.html)|GTM-[A-Z0-9]+)" | sort -u
```

Esperado: **3 linhas distintas**:
- `googletagmanager.com/gtm.js` (script loader IIFE no `<head>`)
- `googletagmanager.com/ns.html` (iframe noscript apos `<body>`)
- `GTM-XXXXXXX` (o container id resolvido)

Por que 3 e nao 2: o snippet oficial do GTM concatena o ID em runtime (`j.src='...gtm.js?id='+i`), entao o `GTM-` nao aparece colado a URL do script — so no argumento da IIFE e dentro do `ns.html?id=`. Validacao correta checa os 3 tokens separadamente.

- **3 matches:** OK, GTM servido corretamente.
- **2 matches (sem `GTM-XXX`):** provavelmente o placeholder `{GTM_ID}` nao foi substituido — critico, re-gerar ou editar manualmente.
- **1 match:** integracao parcial (um dos blocos foi perdido) — critico.
- **0 matches:** LP sem tracking — registrar em "Pendencias".

Se `tracking.json` nao existe ou esta todo null, pular esta validacao.

### 5.4 Certificado

```bash
echo | openssl s_client -servername {DOMAIN} -connect {DOMAIN}:443 2>/dev/null | openssl x509 -noout -issuer -dates
```

Capturar emissor (Let's Encrypt) e validade.

## Passo 6: Relatorio Notion

Crie pagina filha da pasta Entregas — ID lido de `conhecimento/config/notion-ids.md` (chave `entregas`).

- **Titulo:** `Entrega LP · {Marca} · {Slug} · YYYY-MM-DD`
- **Icon:** 🚀
- **Conteudo:**

```markdown
## Resumo executivo

- **URL publica:** {URL final (dominio ou .vercel.app)}
- **URL provisoria:** {.vercel.app}
- **Modo:** {solo | guarda-chuva}
- **Project Vercel:** `{nome-do-projeto}` (`{prj_id}`)
- **Sibling:** `{path-da-sibling}`
- **Data de deploy:** YYYY-MM-DD HH:MM
- **Evento (se aplicavel):** {extrair do copy.txt ou README}

{Se modo guarda-chuva, adicionar tabela de LPs ativas no projeto:}

## Domínio multi-LP (modo guarda-chuva)

`{dominio}` hospeda {N} LPs simultaneamente:

| Path | Marca | Estado |
|---|---|---|
| `/{slug-novo}` | {Marca-da-nova} (esta entrega) | live |
| `/{slug-vizinho-1}` | {marca-vizinha-1} | intacta (smoke test ok) |
| `/{slug-vizinho-N}` | ... | ... |

## Performance (PageSpeed mobile)

| Categoria | Score |
|---|---|
| Performance | {N}/100 |
| Accessibility | {N}/100 |
| SEO | {N}/100 |
| Best Practices | {N}/100 |

**Core Web Vitals:**
- LCP: {X}s
- CLS: {X}
- TBT: {X}ms
- FCP: {X}s

## Seguranca

Headers ativos:
- [{x}] Strict-Transport-Security
- [{x}] X-Content-Type-Options
- [{x}] X-Frame-Options
- [{x}] Referrer-Policy
- [{x}] Permissions-Policy
- [{x}] Cross-Origin-Opener-Policy
- [{x}] Content-Security-Policy

Certificado: {CA, validade}

## Tracking

- GTM container: `{GTM_ID ou "nao configurado"}`
- Snippets ativos: `{2/2 (script + noscript) | 1/2 parcial | 0/2 ausente}`

## Pontos de atencao opcionais

{Colar conteudo da secao "Melhorias opcionais" de REVISAO.md, se existir}

## Pendencias

- {Domino pendente de DNS (se for o caso, colar instrucoes)}
- {Speakers reais se ainda forem placeholder}
- {Integracao CRM se o provedor nao for oficial}

## Como atualizar

```
/lp-publicar {marca} {slug} {dominio}
```

A fonte vive em `landing-pages/{marca}/{slug}/`. Editar la, rodar o comando acima.
```

## Passo 7: Relatorio Final ao Usuario

```
LP publicada — {marca}/{slug}

URL: {dominio ou .vercel.app}
Scores: Perf {N} / A11y {N} / SEO {N} / BP {N}
Headers de seguranca: {N}/6 ativos
Relatorio Notion: {URL}

{Se dominio: "DNS: {tipo} {valor} — encaminhar para admin do dominio"}
{Se isolamento detectou vazamento: texto do erro e passos para re-executar}
```

## Notas de seguranca

- **Nunca** rodar `vercel deploy` dentro do repo do agente (`C:/Users/titof/Downloads/Claude/Agente Inhouse/`). So na pasta sibling.
- **Nunca** copiar `.env`, `meta-ads/`, `conhecimento/`, `.claude/` para a sibling.
- Se o usuario pedir para deployar direto sem pasta sibling, PARE e explique o risco.
- **Modo guarda-chuva** tem promessa de zero regressao. Qualquer divergencia de hash em LP vizinha apos deploy = bug bloqueante. Reverter, investigar, replanejar.
- **Nao misturar entregas** num mesmo deploy guarda-chuva. Uma rodada de `/lp-publicar` = uma LP nova ou atualizada. Se voce precisa atualizar duas LPs na mesma sessao, rode duas vezes.

## Anti-padroes documentados

| Anti-padrao | Por que evitar | Quando aconteceu |
|---|---|---|
| Criar projeto Vercel novo quando dominio ja esta atribuido | Domino fica conflitando, e voce acaba com projeto orfao depois de consolidar manualmente | 2026-04-27, LP Buzzcreators `vendendo-com-creators` (Passo 0.5 nao existia) |
| Sobrescrever `vercel.json` no sibling guarda-chuva | Pode mudar CSP/headers e quebrar form/script de outras LPs vizinhas | Risco hipotetico (motivou §1.6 nao-sobrescrever em guarda-chuva) |
| Copiar asset com filename igual ao de uma LP vizinha sem namespace | Ultima LP a publicar sobrescreve assets das anteriores em silencio (favicon errado, mascot trocado) | Risco real evitado em 2026-04-27 (Buzzmonitor e Buzzcreators ambos com `logo-icon.png`) |
| Path relativo (`./assets/X` ou `../../brand/X`) sobrando no HTML do sibling | `cleanUrls: true` + `trailingSlash: false` resolve `./` na raiz, gerando 404 | 2026-04-27, mascot 404 Buzzmonitor (motivou verificacao pos-rewrite v1.4.0) |
| Misturar atualizacao de duas LPs no mesmo deploy guarda-chuva | Quebra a promessa de "1 deploy = 1 LP nova/atualizada" e dificulta debugging quando algo quebra | Risco hipotetico (motivou nota em §2.4) |
