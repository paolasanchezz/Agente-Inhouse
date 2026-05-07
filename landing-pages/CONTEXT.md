# CONTEXT — Landing Pages (runbook operacional)

> **Quando carregar este doc.** Toda skill `lp-*` (preparar, gerar, revisar, integrar-form, publicar, pipeline) abre este arquivo no início, junto com `landing-pages/GUIDELINES.md`. Os dois são complementares:
>
> - **GUIDELINES.md** = regras de design (paleta, hero, motion, copy, seções-tipo, favicon).
> - **CONTEXT.md** (este) = runbook operacional (fluxos, assets, deploy, troubleshooting).

---

## 1. Mapa mental

- **Fonte-verdade:** `landing-pages/{marca}/{slug}/` (no repo). É o que o pipeline edita.
- **Sibling (artefato de deploy):** `${SIBLING_BASE}/{nome}/` — fora do repo, isolada. NUNCA editar lá direto: o próximo `lp-publicar` sobrescreve.
- **`SIBLING_BASE` é resolvido em runtime** pela skill `lp-publicar` (Passo 0.1) em ordem de precedência: env var `LP_SIBLING_BASE` no shell → linha `LP_SIBLING_BASE=...` em `.env.local` (raiz, gitignored — escrito pelo `/setup-agencia`). Se nenhum estiver setado, `lp-publicar` invoca `/setup-agencia` automaticamente. Nunca hardcodar paths absolutos neste doc.
- **Pipeline:** preparar → gerar → revisar → [integrar-form manual] → publicar.
- **Dois modos de deploy:** SOLO (1 LP/projeto Vercel) e GUARDA-CHUVA (N LPs/domínio).
- **Versionamento:** cada skill `lp-*` tem `version` no frontmatter. Bump minor ao mudar comportamento; entry no `CHANGELOG.md` no mesmo PR.

---

## 2. Fluxos

### 2.1 LP nova (fluxo padrão)

```
/lp-pipeline {marca} {slug} {fonte} [dominio]
```

Passa por: preparar → gerar → revisar → checkpoint manual de form/aprovação → publicar.

Para invocar uma etapa só, ver tabela de comandos no `CLAUDE.md` raiz.

### 2.2 Fluxo de alteração (LP que já está no ar)

Matriz **"o que mudou → o que rodar"**. Sempre editar a fonte (`landing-pages/{marca}/{slug}/`), nunca a sibling.

| Mudança | Editar | Rodar | Re-deploy |
|---|---|---|---|
| Typo / palavra em copy | `copy.txt` (ou `index.html` direto se trivial) | `/lp-gerar {marca} {slug}` (se mexeu em copy.txt) | `/lp-publicar {marca} {slug} [dominio]` |
| Mudança grande de copy (nova seção, reordenar) | `copy.txt` (ou rodar `/lp-preparar` de novo) | `/lp-gerar` → `/lp-revisar` | `/lp-publicar` |
| Ajuste visual / micro CSS no HTML | `index.html` direto | `/lp-revisar` opcional (recomendado se mexeu em estrutura) | `/lp-publicar` |
| Trocar form mock por embed real | — | `/lp-integrar-form {marca}/{slug} "<snippet>"` | `/lp-publicar` |
| Atualizar embed do form (snippet novo) | — | `/lp-integrar-form` de novo | `/lp-publicar` |
| Adicionar/trocar imagem do brand | colocar arquivo em `brand/{marca}/assets/...` + editar `<img>`/`<link>` no HTML com path `../../brand/{marca}/assets/...` | — | `/lp-publicar` (copia automaticamente) |
| Adicionar imagem LP-local (mascote pontual, hero específico) | colocar em `landing-pages/{marca}/{slug}/assets/` + referenciar no HTML como `./assets/X` | — | `/lp-publicar` |
| Atualizar GTM ID | `brand/{marca}/tracking.json` | `/lp-revisar {marca}/{slug}` (Passo 3.5 audita+corrige) | `/lp-publicar` |
| Mudar domínio | — | `/lp-publicar {marca} {slug} {novo-dominio}` (Passo 0.5 detecta solo vs guarda-chuva) | já é o deploy |
| Sibling apagada por engano | — | `/lp-publicar` recria do zero | sim |
| Sibling divergente (alguém editou direto na sibling) | reaplicar mudança em `landing-pages/{marca}/{slug}/` (recuperar via `git diff` na sibling se preciso) | `/lp-publicar` sobrescreve sibling com source | sim |

### 2.3 Anti-padrões de fluxo

Ver §7.1 (lista canônica completa de anti-padrões, incluindo os de fluxo, deploy, assets e favicon).

---

## 3. Convenção de assets / imagens (UNIFICADA)

### 3.1 Onde mora cada coisa

| Tipo de asset | Localização | Quando usar |
|---|---|---|
| **Brand assets** (logos, mascote integrado ao brand, patterns institucionais) | `brand/{marca}/assets/{logos\|mascot\|patterns\|social}/` | Reutilizável por TODAS as LPs da marca |
| **LP-local assets** (mascote pontual de campanha, hero específico, ilustração da pauta) | `landing-pages/{marca}/{slug}/assets/` | Só dessa LP — não vai pro brand |

### 3.2 Paths em source (no repo)

| Asset | Path no `index.html` |
|---|---|
| Brand asset | `../../brand/{marca}/assets/logos/logo-icon.png` (relativo, 2 níveis acima) |
| LP-local asset | `./assets/mascot.png` (relativo simples) |

### 3.3 Paths no deploy (reescritos automaticamente por `lp-publicar`)

| Padrão no source | Modo SOLO | Modo GUARDA-CHUVA |
|---|---|---|
| `../../brand/{marca}/assets/X` | `/assets/X` | `/assets/{marca}/X` |
| `./assets/X` | `/assets/X` | `/assets/{marca}/X` |

### 3.4 Por que namespace em guarda-chuva

Sem `/assets/{marca}/`, dois `logo-icon.png` (Buzzmonitor e Buzzcreators no mesmo `webinar.buzzmonitor.com`) colidem em `{sibling}/assets/logos/logo-icon.png` e a última publicação sobrescreve a anterior. UX disaster: favicon errado, mascote trocado em LP vizinha.

### 3.5 Validação pós-rewrite (em `lp-publicar` Passo 1.5)

Sempre rodar grep no HTML do sibling. Qualquer caminho relativo sobrando = 404 garantido (porque `cleanUrls: true` + `trailingSlash: false` resolve `./` no root, não na subpasta da LP).

```bash
grep -nE "\.\./assets/|\./assets/|\.\./\.\./brand/" "{sibling}/{slug}/index.html" && echo "VAZOU"
```

Se aparecer match → PARE, corrija o rewrite.

### 3.6 Formatos por tipo

| Tipo | Formato | Tamanho alvo | Notas |
|---|---|---|---|
| **Favicon** | PNG | ~13 KB | NUNCA SVG (>100 KB, Edge/Chrome rejeitam silenciosamente, vira globinho genérico). Sempre `logo-icon.png` do brand. |
| **Logo** | PNG ou SVG | SVG só se for limpo, não auto-traceado | PNG transparente é mais seguro pra hero |
| **Mascote/ilustração** | PNG (obrigatório) | varia | Opcional WebP via `<picture>` para perf — Buzzmonitor usa em `monitoramento-concorrentes-maio-2026` |
| **OG image** | JPG ou PNG | 1200×630 | — |
| **Pattern de fundo** | PNG ou SVG simples | — | — |

### 3.7 Favicon — regra inegociável

GUIDELINES §11 manda. Resumindo aqui em modo operacional:

- **Source:** `<link rel="icon" type="image/png" href="../../brand/{marca}/assets/logos/logo-icon.png" />`
- **Deploy SOLO:** `<link rel="icon" type="image/png" href="/assets/logos/logo-icon.png" />`
- **Deploy GUARDA-CHUVA:** `<link rel="icon" type="image/png" href="/assets/{marca}/logos/logo-icon.png" />`
- **Um link só.** Nunca duplicar com `apple-touch-icon` ou `<link rel="icon" type="image/svg+xml">`.
- **Nunca** criar `favicon.png` na pasta da LP — sempre apontar pro `logo-icon.png` do brand.
- **Validação pós-deploy:** `curl -I https://{dominio}/assets/logos/logo-icon.png` (solo) ou `https://{dominio}/assets/{marca}/logos/logo-icon.png` (guarda-chuva) deve dar 200. Favicon resolve em path absoluto na raiz do domínio, não na subpasta da LP.

### 3.8 Mascotes — onde está cada um

| Marca | Mascote | Localização |
|---|---|---|
| **Cxpress (Samir)** | integrado ao brand | `brand/cxpress/assets/mascot/samir-{laptop,dashboard,joinha,sticker,trabalhando}.png` |
| **Buzzmonitor** | sem mascote brand fixo | mascote pontual de campanha vai LP-local em `landing-pages/buzzmonitor/{slug}/assets/mascot.{png,webp}` |
| **Buzzcreators** | sem mascote definido | — |
| **Elife** | sem mascote definido | — |

---

## 4. Modos de deploy

### 4.1 Quando SOLO

- LP única no domínio (ex: `criativo.buzzmonitor.com` dedicada à LP)
- Domínio não fornecido → default `.vercel.app`
- Primeira LP a usar um domínio novo

Sibling: `${SIBLING_BASE}/{marca}-lp-{slug}/` (criada do zero pelo `lp-publicar`).

### 4.2 Quando GUARDA-CHUVA

- Domínio já tem projeto Vercel ativo com outras LPs (ex: `evento.buzzmonitor.com` hospeda eventos presenciais Buzzmonitor + Buzzcreators; `content.cxpress.io` hospeda materiais Cxpress)
- Detecção automática: `lp-publicar` Passo 0.5 consulta API Vercel
- Multi-marca: namespace `/assets/{marca}/` evita colisão (ex: assets Buzzcreators dentro do guarda-chuva Buzzmonitor ficam em `/assets/buzzcreators/`)

Sibling: a do projeto existente (`${SIBLING_BASE}/{nome-detectado}/`). LP nova é anexada como subpasta sem tocar nas vizinhas.

#### Guarda-chuvas ativos hoje

| Subdomínio | Tipo de LP | Projeto Vercel | LPs ativas |
|---|---|---|---|
| `evento.buzzmonitor.com` | Eventos presenciais Buzzmonitor + Buzzcreators | `buzzmonitor-evento` | `vendendo-com-creators` (Buzzcreators) |
| `material.buzzmonitor.com` | Material rico evergreen Buzzmonitor | `buzzmonitor-material` | (em popularização) |
| `webinar.buzzmonitor.com` | Eventos online Buzzmonitor (legacy) | `buzzmonitor-lp-monitoramento-concorrentes` | BR + PT |
| `content.cxpress.io` | Material rico Cxpress (subdomínio único, qualquer tipo) | `cxpress-lp-playbook-whatsapp2026` | `playbook-whatsapp2026` |

LPs novas devem priorizar o subdomínio mais específico (ex: evento presencial Buzzmonitor → `evento.*`, não `webinar.*`). Convenção completa em [`.claude/skills/lp-preparar/CONTEXT.md`](../.claude/skills/lp-preparar/CONTEXT.md).

### 4.3 Promessa do guarda-chuva: ZERO regressão em vizinhas

`lp-publicar` aplica três camadas de defesa em modo guarda-chuva:

1. **Sync prévio (Passo 0.5.d, v3.1.0+)** — antes de qualquer modificação, baixa o último deploy production via Vercel API e popula a sibling local. Garante que a sibling reflete o live mesmo em primeira execução numa máquina nova.
2. **Hash baseline (Passo 2.4)** — captura MD5 do `index.html` de cada vizinha na sibling pós-sync.
3. **Smoke test pós-deploy (Passo 3.4.b)** — refaz hash via curl no live e compara com o baseline. Se vizinha mudou → reverter, não publicar relatório.

Antes da v3.1.0 só existiam as camadas 2 e 3, e baseline era capturado da sibling local — vazia em primeira execução, ocultando regressões. v3.1.0 fechou esse buraco; ver §7.2 (2026-05-07) para o quase-incidente motivador.

---

## 5. GTM — fonte canônica

Esta seção é a **única** fonte da verdade para cascata de região, snippet GTM e divisão de responsabilidades. Skills `lp-*` referenciam aqui em vez de duplicar.

### 5.1 Cascata de detecção de região

Determinística — primeiro critério que resolver ganha:

1. Sufixo do slug: `-pt` → portugal | `-latam`/`-es` → latam | `-br` → brasil
2. `<html lang>` do HTML existente: `pt-PT` → portugal | `es-*` → latam | `pt-BR` → brasil
3. Fallback: `brasil`

**Exceção:** `lp-gerar` está criando o HTML do zero, então **pula o passo 2** (não há `<html lang>` ainda para ler). Cai direto pro fallback `brasil` se o slug não resolver. As outras skills (`lp-revisar`, `lp-publicar`) usam a cascata completa.

Resolução do GTM ID em `brand/{marca}/tracking.json`:

```
expected_gtm_id = gtm.regions[{regiao}] || gtm.default || null
```

Se null nos dois → omitir GTM (anotar em README/REVISAO).

### 5.2 Ownership chain — quem faz o quê com GTM

| Skill | Papel | Quando |
|---|---|---|
| `lp-gerar` Passo 1 + 3 | **Injeta** o snippet inicial (script no `<head>` + noscript após `<body>`) com o ID resolvido pela cascata | Na criação do HTML |
| `lp-revisar` Passo 3.5 | **Audita + corrige** — se ausente, injeta; se ID divergente do `tracking.json`, substitui nos 2 blocos | Em toda revisão |
| `lp-publicar` Passo 5.3 | **Valida no live** — `curl` + grep procurando 3 matches (`gtm.js`, `ns.html`, `GTM-XXXXXXX`) | Pós-deploy |

Mudou o ID em `tracking.json`? Rodar `lp-revisar` (corrige no source) + `lp-publicar` (re-deploy + valida).
LP nunca recebeu GTM mas devia? Rodar `lp-revisar` (injeta como CRITICO).
GTM aparece com ID errado no live? Sempre detecção de região errada — ver §5.1, ajustar slug ou `<html lang>`, rodar `lp-revisar`.

### 5.3 Snippet canônico

Este é o snippet único que `lp-gerar` injeta e `lp-revisar` reinjeta quando ausente. Substituir `{GTM_ID}` pelo valor resolvido (ex: `GTM-WFJVK858`).

No `<head>`, **após** `<meta name="viewport">` e **antes** de `<title>`:

```html
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->
```

Imediatamente **após** `<body>`:

```html
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
```

Para corrigir ID errado, fazer `Edit` com `replace_all` no ID antigo → novo (pega os 2 blocos numa só operação).

Se o snippet oficial do Google mudar, **atualizar este arquivo** — todas as skills lêem daqui.

---

## 6. Troubleshooting (sintoma → causa → solução)

| Sintoma | Causa provável | Solução |
|---|---|---|
| Favicon 404 ao vivo | Path relativo sobrando, ou `favicon.png`/`favicon.svg` na pasta da LP em vez de aponta pro brand | Garantir `<link rel="icon" href="../../brand/{marca}/assets/logos/logo-icon.png">` no source. Rodar `lp-publicar` de novo. |
| Mascote / imagem 404 ao vivo | Asset LP-local com path relativo não reescrito, ou referenciado mas não copiado pro sibling | Conferir grep do Passo 1.5 do `lp-publicar`. Confirmar que o arquivo existe em `brand/{marca}/assets/` ou `landing-pages/{marca}/{slug}/assets/`. Re-deploy. |
| Asset de uma LP aparece em outra (guarda-chuva) | Mesmo nome de arquivo sem namespace (logo-icon.png, mascot.png, etc.) | Confirmar que `lp-publicar` resolveu modo GUARDA-CHUVA (Passo 0.5) e que paths no live têm `/assets/{marca}/`. Se solo em domínio errado, mover pro projeto guarda-chuva. |
| Form não carrega no live (iframe vazio) | CSP bloqueia provedor — domínio não está em `frame-src` / `form-action` / `script-src` | Editar `{sibling}/vercel.json` adicionando o domínio do provedor às 3 directives. Re-deploy. Em modo guarda-chuva, NÃO sobrescrever — patch cirúrgico. |
| Form duplicado, ou erro `Cannot read properties of null (reading 'addEventListener')` | Placeholder JS do form mock não foi removido pelo `lp-integrar-form` | Re-rodar `lp-integrar-form` (Passo 2.5 remove o handler) ou editar manual. |
| Form com "card-dentro-de-card" no live (dois cards brancos aninhados) | Wrapper `<div class="form jotform-embed">` herdou estilos do mock (`.form` é card visual no `lp-gerar`) e o provedor já vem com card proprio | Editar wrapper removendo a classe `form` (deixar só `jotform-embed reveal`), reduzir CSS para `.jotform-embed iframe { width: 100% !important; ... }`. Versão atualizada em `lp-integrar-form` v1.3.0. |
| GTM não aparece no live (curl retorna 0 matches) | `tracking.json` sem ID pra região, ou snippet não injetado | Validar `brand/{marca}/tracking.json` tem `regions[{regiao}]` ou `default`. Rodar `lp-revisar` (Passo 3.5 injeta automático se ausente). Re-deploy. |
| GTM aparece com ID errado | Detecção de região errada (cascata) | Renomear slug com sufixo `-pt`/`-latam`/`-br`, ou setar `<html lang>` correto, rodar `lp-revisar`. |
| PageSpeed Performance < 85 | Imagens grandes, fonts não otimizadas, JS bloqueante | Comprimir imagens (WebP via `<picture>`), `<link rel="preload">` para fonts críticas, `font-display: swap` no `@font-face`. |
| Vercel CLI falha com `FetchError: invalid json response body` | Bug intermitente da CLI — deploy chega READY server-side mas CLI aborta antes da resposta | Consultar API Vercel direto (`lp-publicar` Passo 3.3). Se state=READY nos últimos 120s, ignorar erro CLI. NÃO retry cego. |
| Smoke test acusa hash divergente em LP vizinha (guarda-chuva) | `vercel.json` foi sobrescrito, asset removido, ou rewrite agressivo de path | NÃO publicar relatório. Reverter mudança. Investigar diff. Promessa do guarda-chuva é zero regressão. |
| LPs vizinhas viraram 404 após deploy guarda-chuva | Sibling local sem vizinhas + deploy substituiu prod (cenário pré-v3.1.0 ou sync do 0.5.d falhou) | Reverter via Vercel UI (Promote do penúltimo deploy READY). Confirmar que `VERCEL_TOKEN` resolve em `.env.local`/env/auth.json. Re-rodar `lp-publicar` — o sync do 0.5.d deve agora popular a sibling antes do deploy. |
| `lp-publicar` aborta com "Sync incompleto. Slugs vivos em {dominio} mas faltando na sibling" | Token Vercel sem permissão de read no projeto, ou bug no sync recursivo do 0.5.d | Confirmar que o token tem escopo do team Inhouse-Elife. Se persistir, baixar manualmente o último deploy (Vercel UI → Deployments → Source) e popular a sibling antes de re-rodar. |
| Sibling apagada por engano | Pasta `${SIBLING_BASE}/{nome}/` foi deletada | `lp-publicar` recria do zero a partir do source. |
| Sibling divergente do source | Alguém editou direto na sibling (anti-padrão) | `lp-publicar` sobrescreve sibling com source. Se a edição era importante, recuperar antes do deploy via `git diff` na sibling (se for git) ou copiar manualmente pro source antes. |
| `<title>` com sufixo `[REVISADO]` / `[TESTE]` / `[DRAFT]` no live | Sufixo de trabalho não foi removido no Passo 1.5 do `lp-publicar` | Editar source `index.html` removendo sufixo. Re-deploy. |
| Vazamento de path interno (`.env`, `meta-ads/`, `conhecimento/`, `.claude/`) na sibling | Algo do repo interno foi copiado pra sibling | `lp-publicar` Passo 2 (validação de isolamento) deveria ter abortado. Se passou, é bug — investigar a origem do vazamento (provavelmente em `lp-gerar` ou step de cópia). |
| `vercel domains add` retorna conflito | Domínio já está atribuído a outro projeto (deveria ser modo guarda-chuva) | Voltar ao Passo 0.5. Se API Vercel não detectou, rodar manualmente `curl /v9/projects` com `VERCEL_TOKEN` e ajustar. |
| `npx vercel link` não popula `.vercel/project.json` | Sem `VERCEL_TOKEN` ou sem permissão na org | Rodar `npx vercel login` antes. Confirmar `team_nC991VqUuSU2jXZN152xqqEg` (elife-group) na conta. |

---

## 7. Anti-padrões documentados

Fonte canônica única — `lp-publicar` e outras skills referenciam aqui em vez de duplicar.

### 7.1 Por categoria (o quê / por quê)

| Anti-padrão | Por que evitar |
|---|---|
| **Editar HTML direto na sibling** | Próximo `lp-publicar` sobrescreve silenciosamente — perde mudança. Sempre voltar à fonte em `landing-pages/{marca}/{slug}/`. |
| **Pular `lp-gerar` quando `copy.txt` mudou** | HTML fica defasado da copy aprovada. |
| **Pular `lp-revisar` em mudança grande no HTML** | Auditoria de GTM (Passo 3.5) e checklist a11y existem por motivo. |
| **Criar projeto Vercel novo quando o domínio já é guarda-chuva** | Resulta em projeto órfão e dois deploys de consolidação manual. `lp-publicar` Passo 0.5 detecta automaticamente — confiar. |
| **Sobrescrever `vercel.json` no sibling guarda-chuva** | CSP/headers podem ter sido customizados para vizinhas. Patch cirúrgico ou perguntar antes. |
| **Copiar asset com filename igual ao de uma LP vizinha sem namespace** | Última publicação sobrescreve assets das anteriores em silêncio (favicon errado, mascote trocado). Modo guarda-chuva sempre namespaceia em `/assets/{marca}/`. |
| **Path relativo (`./assets/X` ou `../../brand/X`) sobrando no HTML do sibling** | `cleanUrls: true` + `trailingSlash: false` resolve `./` na raiz, gerando 404. `lp-publicar` Passo 1.5 tem grep obrigatório. |
| **Misturar atualização de duas LPs no mesmo deploy guarda-chuva** | Quebra a promessa "1 deploy = 1 LP nova/atualizada" e dificulta debugging quando algo quebra. Rodar `lp-publicar` separado para cada. |
| **`favicon.png` ou `favicon.svg` na pasta da LP** | Path relativo + cleanUrls = 404. SVG do brand pesa >100KB e Edge/Chrome rejeitam silenciosamente. Sempre apontar pro `brand/{marca}/assets/logos/logo-icon.png` (PNG ~13KB). |

### 7.2 Histórico de incidentes

| Data | Incidente | Skill afetada | Versão que corrigiu |
|---|---|---|---|
| 2026-04-20 | LP PT-PT recebendo GTM Brasil | lp-gerar / lp-revisar | lp-gerar v1.2.0 + lp-revisar v1.1.0 (cascata de detecção de região — §5.1) |
| 2026-04-23 | `favicon.png` / `favicon.svg` na pasta da LP causando 404 | — | GUIDELINES §11 + CONTEXT §3.7 (sempre apontar pro brand) |
| 2026-04-27 | mascot.png 404 (path relativo `./assets/` não reescrito) | lp-publicar | v1.4.0 (suporte `./assets/` + grep validation pós-rewrite — §3.5) |
| 2026-04-27 | Buzzcreators publicada em projeto separado em vez de guarda-chuva existente | lp-publicar | v1.5.0 (Passo 0.5 detecção via API Vercel + namespace por marca — §3.4) |
| 2026-04-30 | Card-dentro-de-card no embed Jotform (LP `social-listening-mayo-2026-latam`) | lp-integrar-form | v1.3.0 (wrapper sem heranca de `.form`, CSS canonico reduzido) |
| 2026-05-07 | **Incidente real**: deploy de `webinar-tecnologia-maio2026` em `content.cxpress.io` (deploy `dpl_3rKKvvAfdinBXbQB1MeFFdJP51Au`, ~11h) feito de máquina sem `livraria/` na sibling — production substituída sem livraria, `/livraria` virou 404 por ~2h. `BASELINES_OTHERS` ficou vazio (sibling sem vizinhas), smoke test 3.4.b iterou sobre lista vazia, skill reportou sucesso. Restaurado por `/lp-publicar cxpress livraria` em v3.1.0 (sync via Vercel API baixou playbook + webinar do live, sibling local manteve livraria, deploy preservou as 3 LPs). | lp-publicar | v3.1.0 (Passo 0.5.d sync via Vercel API antes de modificar a sibling — §4.3). LP `webinar-tecnologia-maio2026` recuperada pro repo via download do live + reverse de paths absolutos. |

---

## 8. Checklist pré-deploy

Antes de chamar `lp-publicar`, conferir:

- [ ] Copy aprovada (Notion ou inline)
- [ ] `index.html` sem placeholders esquecidos (`[REVISADO]`, `[TESTE]`, `[Speaker TBD]`, `Lorem ipsum`)
- [ ] Imagens existem em disco (brand ou LP-local) e os paths no HTML batem
- [ ] Form: mock tudo bem pra deploy interno; se for público, ter o snippet do provedor pronto
- [ ] `brand/{marca}/tracking.json` tem GTM ID pra região (ou explicitamente null)
- [ ] Domínio: solo (deixar default) ou guarda-chuva (passar o domínio existente como 3º arg)
- [ ] Modo guarda-chuva: vizinhas estão estáveis (curl rápido nas URLs antes de adicionar nova LP)

---

## 9. Quando NÃO usar este pipeline

- **Site institucional / app:** repo dedicado, não `landing-pages/`
- **Página com backend (DB, auth, server-side):** pipeline é estático puro (Vercel CDN + HTML)
- **Email HTML / template de e-mail:** usar pipeline de copy + ferramenta de email separada (não há rota Vercel para inbox)
- **Microsite com várias páginas internas + navegação:** pode até funcionar em modo guarda-chuva, mas avaliar se vale criar repo dedicado

---

## 10. Referências cruzadas

- **`landing-pages/GUIDELINES.md`** — regras de design (§1 paleta, §3 hero, §11 favicon, etc.)
- **`.claude/skills/lp-preparar/CONTEXT.md`** — convenções de marca, IDs do Notion, formato de `tracking.json`
- **`.claude/skills/lp-publicar/vercel.template.json`** — headers de segurança + CSP padrão (Jotform, RD Station, HubSpot, GTM, Google Fonts, YouTube, Vimeo)
- **`brand/{marca}/`** — `tokens.json`, `generation-rules.json`, `brand-manifest.json`, `tracking.json`, `assets/`
- **`CHANGELOG.md`** raiz — histórico de versões das skills `lp-*`

Este arquivo é vivo. Quando aparecer um sintoma novo de troubleshooting (ou um anti-padrão novo), adicionar aqui na mesma branch da correção.
