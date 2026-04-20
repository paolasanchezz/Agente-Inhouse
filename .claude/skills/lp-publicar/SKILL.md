---
name: lp-publicar
description: Sincroniza LP para pasta sibling isolada, deploya via Vercel CLI, adiciona dominio opcional, roda validacao PageSpeed + headers e publica relatorio final no Notion. Garante zero vazamento do repo interno.
argument-hint: "[marca] [slug] [dominio-opcional] — ex: buzzmonitor monitoramento-maio webinar.buzzmonitor.com"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-pages, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-update-page
version: 1.2.0
---

# Skill: Publicar Landing Page

Voce sincroniza a LP do repo do agente para uma pasta sibling isolada fora do repo, roda deploy na Vercel, valida e publica relatorio no Notion. **Regra inegociavel: nenhum arquivo do repo interno (.env, skills, conhecimento/, brand/, meta-ads/) pode vazar para a pasta sibling ou para o deploy.**

## Passo 0: Parsing e Contexto

Leia `.claude/skills/lp-preparar/CONTEXT.md`.

Parsing de `$ARGUMENTS`:

| Argumento | Valores | Obrigatorio |
|---|---|---|
| `marca` | `buzzmonitor` \| `buzzcreators` \| `cxpress` \| `elife` | Sim |
| `slug` | kebab-case | Sim |
| `dominio` | FQDN (ex: `webinar.buzzmonitor.com`) | Nao |

Paths:
- Fonte: `landing-pages/{marca}/{slug}/index.html`
- Sibling: `C:/Users/titof/Downloads/Claude/{marca}-lp-{slug}/`
- Dentro da sibling: `{slug}/index.html` + `assets/` + `vercel.json` + `.gitignore` + `README.md`

Se fonte nao existe, PARE.

## Passo 1: Preparar Pasta Sibling

### Estrutura alvo

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

### 1.1 Criar pasta se nao existe

```bash
mkdir -p "{sibling}/{slug}"
mkdir -p "{sibling}/assets"
```

### 1.2 Copiar index.html

```bash
cp "landing-pages/{marca}/{slug}/index.html" "{sibling}/{slug}/index.html"
```

### 1.3 Descobrir assets referenciados

Grep `src=` e `url(` no index.html fonte. Capture qualquer path que:
- Contenha `brand/{marca}/assets/` (referencia relativa `../../brand/{marca}/assets/...`)
- OU `/assets/` (ja absoluto)
- OU `./assets/` (relativo a raiz do site)

Produza lista de filenames unicos.

### 1.4 Copiar **apenas** esses assets

Para cada asset na lista, copiar de `brand/{marca}/assets/...` para `{sibling}/assets/...` preservando subcaminho (logos/, icons/, images/).

**Nao** usar `cp -r brand/{marca}/` cego — isso copiaria todos os assets da marca, inclusive nao-usados. Copiar so os que o HTML referencia.

### 1.5 Reescrever paths no HTML copiado

No `{sibling}/{slug}/index.html`, substituir:
- `../../brand/{marca}/assets/` → `/assets/`
- `./assets/` → `/assets/`

Use `Edit` com `replace_all: true` por padrao.

Remover tambem do `<title>` qualquer sufixo de trabalho: `[REVISADO]`, `[TESTE]`, `[DRAFT]`.

### 1.6 Escrever vercel.json

Copiar `.claude/skills/lp-publicar/vercel.template.json` para `{sibling}/vercel.json` **sem modificacao**.

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

## Passo 2: Validacao de Isolamento (pre-deploy)

**Antes** de chamar `vercel deploy`, faca um grep defensivo na pasta sibling:

```bash
grep -ril "meta-ads\|\.env\|conhecimento/\|\.claude/" "{sibling}/" || true
```

Se a busca retornar **qualquer** arquivo, PARE e avise o usuario. Algo vazou. Nao deployar.

Tambem verifique:

```bash
ls "{sibling}/" | grep -E "^(meta-ads|conhecimento|brand|\.claude|\.env)$" && echo "VAZOU"
```

Se imprimir `VAZOU`, PARE.

## Passo 3: Deploy

```bash
cd "{sibling}" && npx --yes vercel deploy --prod --yes
```

Capturar:
- URL provisoria `.vercel.app` (stdout do comando, linha `https://...vercel.app`)
- Se primeiro deploy: aparecera prompt de projeto. Usar `--name {marca}-lp-{slug}` se necessario.

Se comando falhar, reportar erro integralmente. Nao tentar auto-resolver.

## Passo 4: Dominio (se fornecido)

Se `$dominio` nao vazio:

```bash
cd "{sibling}" && npx --yes vercel domains add "{dominio}"
```

Capturar as instrucoes de DNS que o Vercel retorna (tipo A com IP `76.76.21.21` ou CNAME). Guardar para o relatorio.

Se falhar (ja configurado, conflito de projeto), reportar mensagem e seguir — nao e bloqueante para o relatorio.

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

Crie pagina filha de `33b3934026fd80ceb414dd22cb7dbe1f` (pasta Entregas).

- **Titulo:** `Entrega LP · {Marca} · {Slug} · YYYY-MM-DD`
- **Icon:** 🚀
- **Conteudo:**

```markdown
## Resumo executivo

- **URL publica:** {URL final (dominio ou .vercel.app)}
- **URL provisoria:** {.vercel.app}
- **Data de deploy:** YYYY-MM-DD HH:MM
- **Evento (se aplicavel):** {extrair do copy.txt ou README}

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
