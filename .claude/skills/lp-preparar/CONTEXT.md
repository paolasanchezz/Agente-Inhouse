# Contexto Compartilhado — Landing Pages

> Este arquivo e lido por todas as skills do grupo lp-* antes de qualquer acao.

---

## Marcas Validas

| Marca | Arquivo de produto | Dominio de publicacao (default) |
|---|---|---|
| `buzzmonitor` | `conhecimento/produto/buzzmonitor/buzzmonitor.md` | `webinar.buzzmonitor.com` |
| `buzzcreators` | `conhecimento/produto/buzzcreators/buzzcreators.md` | a definir |
| `cxpress` | `conhecimento/produto/cxpress/cxpress.md` | a definir |
| `elife` | `conhecimento/produto/elife/elife.md` | a definir |

Dominios sao sugeridos, nao impostos. `lp-publicar` so adiciona dominio quando o usuario passa `[dominio]` explicitamente.

## Estrutura de arquivos

Toda LP vive em `landing-pages/{marca}/{slug}/`:

```
landing-pages/
├── GUIDELINES.md                                  (regras universais — §1 a §10)
├── buzzmonitor/
│   ├── monitoramento-concorrentes-maio-2026/
│   │   ├── index.html
│   │   ├── README.md
│   │   └── copy.txt                               (output do lp-preparar)
│   └── ...
├── cxpress/
└── buzzcreators/
```

### Convencao de `slug`

kebab-case descritivo do evento ou oferta. Dois padroes aceitos:

- **Curto (evergreen)** — 2-3 palavras, sem data. Ex.: `conteudo-que-converte`, `trends-q2`. Use quando a LP e reutilizavel ou nao e datada.
- **Com mes-ano (evento datado)** — `{evento}-{mes}-{ano}`. Ex.: `monitoramento-concorrentes-maio-2026`. Use quando o path precisa comunicar edicao especifica (SEO, compartilhamento) e quando voce planeja rodar novas edicoes com paths distintos.

Evitar dia no slug (o README guarda a data completa). Manter tudo minusculo, apenas hifens.

## Pasta sibling (deploy artifact)

Base: `C:/Users/titof/Downloads/Claude/{marca}-lp-{slug}/`

- Existe **fora** do repo do agente — nunca commitar path dela.
- Contem apenas `{slug}/index.html`, `assets/` (so arquivos referenciados pelo HTML), `vercel.json`, `.gitignore`, `README.md`.
- `lp-publicar` sincroniza via rsync seletivo e roda `vercel deploy`.
- Isolamento: **zero** arquivos do repo interno (.env, skills, conhecimento/, brand/, meta-ads/) podem vazar pra pasta sibling.

## Identidade de Marca

Ao gerar ou revisar LP, carregar:

| Arquivo | Uso |
|---|---|
| `brand/DESIGN.md` | Visao geral do sistema de brand |
| `brand/{marca}/tokens.json` | Cores, tipografia, espacamento (W3C DTCG) |
| `brand/{marca}/generation-rules.json` | Regras de composicao para AI |
| `brand/{marca}/brand-manifest.json` | Tom de voz, messaging |
| `brand/{marca}/tracking.json` | GTM container id por regiao (`default` + `regions.{brasil,latam,portugal}`). Se `null`, LP nao recebe GTM. |
| `brand/{marca}/assets/logos/` | Logos (primary, reversed) — referenciar apenas os usados |

### tracking.json — formato canonico

```json
{
  "$schema": "tracking/v1",
  "gtm": {
    "default": "GTM-XXXXXXX",
    "regions": {
      "brasil": "GTM-XXXXXXX",
      "latam": "GTM-XXXXXXX",
      "portugal": "GTM-XXXXXXX"
    },
    "notes": "livre — ex: container unico ou splits futuros"
  }
}
```

Resolucao: `regions[{regiao}]` > `default` > omitir GTM. `lp-gerar` injeta no HTML; `lp-revisar` audita se o snippet esta presente quando esperado.

## Guidelines e anti-IA

| Arquivo | Quando carregar |
|---|---|
| `landing-pages/GUIDELINES.md` | SEMPRE (gerar, revisar) |
| `conhecimento/editorial/regras-anti-ia.md` | `lp-preparar` (revisao conservadora) |
| `conhecimento/copywriting/fundamentos-copy.md` | `lp-preparar` se copy vier crua |

## Skills reutilizadas (nao duplicar)

- `frontend-design` — gerar HTML ou auditar em review mode (argumento: "review mode: ...").
- `web-design-guidelines` — auditar acessibilidade / HTML semantico via Vercel Labs.

## Notion

- Pasta Entregas (publicacao): `33b3934026fd80ceb414dd22cb7dbe1f`
- `lp-preparar` publica copy estruturada.
- `lp-publicar` publica relatorio final (URL publica + PageSpeed + headers + pendencias).

## Template canonico de vercel.json

Mantido em `.claude/skills/lp-publicar/vercel.template.json` — headers de seguranca (HSTS, nosniff, X-Frame-Options, Referrer-Policy, Permissions-Policy, COOP) + `cleanUrls: true` + `trailingSlash: false`.

## Formulario

Durante design e revisao: mock `<form action="#" onsubmit="event.preventDefault()">`.
Integracao real so via `lp-integrar-form` (Jotform, RD Station, HubSpot), manual-trigger apos aprovacao do design.

Wrapper CSS canonico:

```css
.form.jotform-embed { padding: 16px; overflow: hidden; }
.form.jotform-embed iframe { width: 100% !important; max-width: 100% !important; border: 0; display: block; }
```

## PageSpeed Insights (validacao pos-deploy)

Endpoint (sem chave, usado via WebFetch):

```
https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={URL}&strategy=mobile&category=performance&category=accessibility&category=seo&category=best-practices
```

Metas: performance >= 85, accessibility = 100, seo >= 90, best-practices >= 90. Incluir no relatorio Notion.
