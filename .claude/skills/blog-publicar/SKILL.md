---
name: blog-publicar
description: Publica o blog Astro estatico da marca (hoje Buzzcreators) no Vercel — valida o build (schema de meta tags), builda com env de producao (indexavel), deploya no projeto Vercel correto, valida a versao no ar (posts, noindex OFF, sitemap/rss/llms) e reporta. Manual-trigger. Contexto sancionado para a trava de deploy Vercel (guard_vercel_deploy.py).
argument-hint: "[marca]  — default buzzcreators (unica com blog hoje)"
allowed-tools: AskUserQuestion, Read, Edit, Bash, Glob, Grep
version: 1.0.0
---

# Skill: Publicar blog (Astro estatico) no Vercel

Você publica o blog **estatico** da marca — hoje `blog/buzzcreators/` (Astro 5) — no projeto Vercel correspondente. O blog é a face pública de SEO/GEO: os posts vivem em `src/content/blog/*.md`, o `content.config.ts` é o **contrato de meta tags** (o `astro build` FALHA se um post estiver fora dos limites), e o layout gera JSON-LD (BlogPosting + FAQPage + Breadcrumb), sitemap, RSS e `llms.txt`.

**Esta skill é o contexto sancionado do deploy Vercel.** O hook `guard_vercel_deploy.py` vai pedir confirmação no Passo 2 — **dentro desta skill, aprovar é o esperado** (mesma filosofia de `lp-publicar`/`dashboard-atualizar`). Fora dela, o `vercel deploy` do blog deve ser recusado.

**Por que NÃO usa sibling** (diferente de `lp-publicar`/`dashboard-atualizar`): aquelas skills deployam de uma pasta fora do repo porque têm `middleware.js` de auth, `robots.txt` e risco de PII/vizinhas. O blog é **estático, self-contained, sem segredo, sem middleware e é um projeto Vercel só dele** (sem vizinhas). O deploy sai da própria pasta do projeto (`blog/{marca}/`), que o Vercel trata como raiz e sobe isolada — sem vazar o resto do repo. Se um dia o blog ganhar auth/middleware, migrar para o padrão sibling.

---

## Configuração por marca

| marca | Pasta do projeto | Vercel project | Vercel org (team) | Domínio de produção |
|---|---|---|---|---|
| `buzzcreators` | `blog/buzzcreators` | `buzzcreators-blog` · `prj_0LHFECIs21P0yJwUvCpB2Wi675YA` | `elife-group` · `team_nC991VqUuSU2jXZN152xqqEg` | `https://blog.buzzcreators.com.br` (fallback: `https://buzzcreators-blog.vercel.app`) |

> Só Buzzcreators tem blog hoje. Ao criar o blog de outra marca (Astro no mesmo molde), acrescentar a linha aqui e nada mais muda.

Env de produção do Astro (lidas no build — ver `astro.config.mjs` e `src/consts.ts`):
- `PUBLIC_SITE_URL` = domínio de produção (define `site`, canonical, sitemap, RSS).
- `PUBLIC_NOINDEX=false` = **liga a indexação** (o default é `true`, para não indexar staging).

---

## Passo 0 — Pré-flight

Parse de `$ARGUMENTS`: **Arg 1** (`marca`) — default `buzzcreators`. Resolva `DIR`, `VERCEL_PROJECT_ID`, `VERCEL_ORG_ID`, `PROD_DOMAIN`, `FALLBACK_URL` da tabela. `TODAY=$(date +%Y-%m-%d)`.

### 0.1 Repo + projeto
```bash
git rev-parse --show-toplevel >/dev/null || { echo "ERRO: rode da raiz do repo"; exit 1; }
test -f "$DIR/package.json" && test -f "$DIR/astro.config.mjs" && test -d "$DIR/src/content/blog" \
  || { echo "ERRO: $DIR nao parece um blog Astro valido"; exit 1; }
mkdir -p tmp
```

### 0.2 Vercel CLI autenticado (read-only — NÃO dispara a trava)
```bash
npx --yes vercel whoami --scope="$VERCEL_ORG_ID" || { echo "ERRO: rode 'npx vercel login' e re-execute"; exit 1; }
```

### 0.3 Resolver a URL de produção (domínio custom ou fallback .vercel.app)
```bash
PROD_URL="$PROD_DOMAIN"
if ! curl -s -o /dev/null --max-time 8 "$PROD_URL/"; then
  echo "AVISO: $PROD_DOMAIN nao resolve/responde (dominio custom ainda nao atrelado)."
  echo "       Vou publicar em $FALLBACK_URL. Para usar o dominio proprio, atrele-o ao projeto:"
  echo "       npx vercel domains add ${PROD_DOMAIN#https://} --scope=$VERCEL_ORG_ID  (e aponte o CNAME no DNS)"
  PROD_URL="$FALLBACK_URL"
fi
echo "URL de producao desta publicacao: $PROD_URL"
```
> Se quiser **forçar** o domínio custom (porque acabou de atrelar), rode a skill e responda quando ela perguntar, ou edite `PROD_URL` no passo. Nunca indexe dois domínios com o mesmo conteúdo — mantenha um canonical só.

---

## Passo 1 — Build local = gate de meta tags (SEO/GEO)

O build local roda ANTES do deploy e é a validação barata: se qualquer post violar o schema (title 10–75, meta description 110–165, `tldr` 2–6, `tags` 1–6, etc.), o build falha aqui e nada sobe.

```bash
( cd "$DIR" && PUBLIC_SITE_URL="$PROD_URL" PUBLIC_NOINDEX=false npm run build ) 2>&1 | tee "tmp/blog-build-$TODAY.log"
BUILD_EXIT=${PIPESTATUS[0]}
[ "$BUILD_EXIT" = 0 ] || { echo "ERRO: build falhou — corrija o post apontado no log (limite de meta tag) e re-execute"; exit 1; }
```

**Sanity do output** (defesa contra deploy vazio/quebrado):
```bash
POSTS=$(ls "$DIR"/src/content/blog/*.md | grep -v '/_' | wc -l | tr -d ' ')
BUILT=$(find "$DIR/dist/blog" -name index.html | wc -l | tr -d ' ')
echo "posts-fonte=$POSTS  paginas-de-post=$BUILT"
[ "$BUILT" -ge "$POSTS" ] || { echo "ERRO: menos paginas que posts (algum draft:true nao intencional?)"; exit 1; }
for f in dist/sitemap-index.xml dist/rss.xml dist/llms.txt dist/index.html; do
  test -s "$DIR/$f" || { echo "ERRO: faltou $f no build"; exit 1; }
done
echo "sanity do build OK"
```

---

## Passo 2 — Deploy de produção (a trava vai pedir confirmação — aprove)

Sem `.vercel/` no repo: passamos `VERCEL_ORG_ID`/`VERCEL_PROJECT_ID` por env (padrão CI do Vercel), então o deploy vai pro projeto certo sem `vercel link` (não cria `.vercel/` versionável). O Vercel builda o Astro com as `--build-env` (indexável, canonical certo).

```bash
export VERCEL_ORG_ID="$VERCEL_ORG_ID"
export VERCEL_PROJECT_ID="$VERCEL_PROJECT_ID"
npx --yes vercel deploy --prod --yes --cwd "$DIR" --scope="$VERCEL_ORG_ID" \
  --build-env PUBLIC_NOINDEX=false --build-env PUBLIC_SITE_URL="$PROD_URL" \
  2>&1 | tee "tmp/blog-deploy-$TODAY.log"
NEW_DPL_ID=$(grep -oE 'dpl_[a-zA-Z0-9]+' "tmp/blog-deploy-$TODAY.log" | head -1)
```
- Aguarde a linha `▲ Aliased ... $PROD_DOMAIN` (ou o alias .vercel.app). Se não aliasar (raro): `npx vercel promote "$NEW_DPL_ID" --scope="$VERCEL_ORG_ID"`.
- `FetchError`/timeout da CLI: **não** re-deployar cego — `npx vercel ls buzzcreators-blog --scope="$VERCEL_ORG_ID" | head -5` e ver se ficou READY.
- Se o Vercel não souber buildar (projeto sem framework/build setting): configurar UMA vez no painel do projeto — Framework **Astro**, Root Directory `blog/buzzcreators`, Build `npm run build`, Output `dist` — e re-executar.

---

## Passo 3 — Validação da versão no ar

```bash
echo "home:      $(curl -s -o tmp/blog-home.html -w '%{http_code}' "$PROD_URL/")"
SLUG=$(ls "$DIR"/src/content/blog/*.md | grep -v '/_' | head -1 | xargs basename | sed 's/\.md$//')
echo "post $SLUG: $(curl -s -o /dev/null -w '%{http_code}' "$PROD_URL/blog/$SLUG")"
echo "sitemap:   $(curl -s -o /dev/null -w '%{http_code}' "$PROD_URL/sitemap-index.xml")"
echo "rss:       $(curl -s -o /dev/null -w '%{http_code}' "$PROD_URL/rss.xml")"
echo "llms.txt:  $(curl -s -o /dev/null -w '%{http_code}' "$PROD_URL/llms.txt")"
echo "-- indexacao (produção deve estar SEM noindex) --"
if curl -s "$PROD_URL/" | grep -iq 'name="robots"[^>]*noindex'; then
  echo "ERRO: home com noindex em producao — PUBLIC_NOINDEX nao pegou. Rever build-env e re-deployar."
else
  echo "OK: sem noindex (indexavel)"
fi
```
Esperado: **200** em home, post, sitemap, rss, llms.txt · **sem** `noindex` na home. Qualquer 4xx/5xx ou noindex presente → investigar antes de considerar publicado.

---

## Passo 4 — Relatório

```
============================================================
Blog {marca} publicado no Vercel
============================================================
URL:        $PROD_URL
Deploy ID:  $NEW_DPL_ID · READY
Posts:      $BUILT paginas de post no ar (fonte: $POSTS)
Indexacao:  ligada (PUBLIC_NOINDEX=false) · sitemap + rss + llms.txt servidos

Proximos passos manuais:
- Submeter $PROD_URL/sitemap-index.xml no Google Search Console.
- Se ainda em .vercel.app: atrelar blog.buzzcreators.com.br (Passo 0.3) e re-publicar com o dominio proprio.
Rollback rapido: npx vercel rollback <dpl_anterior_READY> --scope=$VERCEL_ORG_ID
```

Se houve mudança de **código** (posts, layout, config), entregar via `/commit` (branch + PR) — esta skill só publica, não commita.

---

## Regras críticas e notas

- **Nunca** `vercel deploy` do blog fora desta skill (a trava manda recusar). Só inspeção/leitura (`vercel ls/inspect/whoami`) fora dela.
- **Build local é o gate**: se falhar por meta tag, corrigir o post — nunca burlar o schema.
- **Um canonical só**: não deixar o mesmo conteúdo indexável em `.vercel.app` **e** no domínio próprio. Ao atrelar o domínio, ele passa a ser o `PUBLIC_SITE_URL`.
- **`.vercel/` não versiona**: o deploy usa `VERCEL_ORG_ID`/`VERCEL_PROJECT_ID` por env; não rode `vercel link` (evita criar `.vercel/` no repo). Se existir, garanta que está no `.gitignore`.
- **Windows/Git Bash**: se `npm`/`node` não estiverem no PATH da sessão, usar o caminho absoluto; `python` aqui é shim quebrado (usar `py`) — mas esta skill não usa Python.
- **Multi-marca**: para publicar o blog de outra marca, adicionar a linha na tabela de Configuração; os passos são genéricos.
- **Conteúdo público**: os posts já passam pelo anti-IA mínimo do `blog-diario` (precisão factual + grafia de marca). Se um post entrou "na mão" fora daquele fluxo, revisar antes de publicar.
