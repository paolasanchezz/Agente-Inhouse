# Contexto Compartilhado — Landing Pages

> Este arquivo e lido por todas as skills do grupo lp-* antes de qualquer acao.

---

## Marcas Validas

| Marca | Arquivo de produto | Dominio de publicacao (default) |
|---|---|---|
| `buzzmonitor` | `brand/buzzmonitor/BRANDBOOK.md` | `webinar.buzzmonitor.com` |
| `buzzcreators` | `brand/buzzcreators/BRANDBOOK.md` | a definir |
| `cxpress` | `brand/cxpress/BRANDBOOK.md` | a definir |
| `elife` | `brand/elife/BRANDBOOK.md` | a definir |

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

Base padrao: `C:/Users/titof/Downloads/Claude/{nome-do-projeto}/` (fora do repo).

- **Modo solo:** `{nome}` = `{marca}-lp-{slug}` (1 LP por projeto Vercel; criada do zero pelo lp-publicar).
- **Modo guarda-chuva:** `{nome}` = nome do projeto Vercel ja existente que ja serve o dominio (ex: `buzzmonitor-lp-monitoramento-concorrentes`); LP nova vira subpasta sem tocar nas vizinhas.

Detalhes operacionais (quando cada modo, namespace de assets, smoke test de regressao em vizinhas) em `landing-pages/CONTEXT.md` §4.

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

Resolucao: `regions[{regiao}]` > `default` > omitir GTM.

**Cascata de regiao + ownership chain (quem injeta, audita, valida) + snippet canonico estao em `landing-pages/CONTEXT.md` §5** — fonte unica para todas as skills lp-*.

## Guidelines e anti-IA

| Arquivo | Quando carregar |
|---|---|
| `landing-pages/GUIDELINES.md` | SEMPRE (gerar, revisar) |
| `conhecimento/editorial/regras-anti-ia.md` | `lp-preparar` (revisao conservadora) |
| `conhecimento/copywriting/fundamentos-copy.md` | `lp-preparar` se copy vier crua |

## Skills reutilizadas (nao duplicar)

- `frontend-design` — gerar HTML. Para revisao, invocar com prompt "REVIEW ONLY — NAO implemente..." (convencao do projeto, nao e modo nativo da skill; detalhes em `.claude/skills/lp-revisar/SKILL.md` Passo 1).
- `web-design-guidelines` — auditar acessibilidade / HTML semantico via Vercel Labs.

## Notion

IDs sao lidos de `conhecimento/config/notion-ids.md` (fonte unica). Para publicacao, use a chave `entregas`.

- `lp-preparar` publica copy estruturada.
- `lp-publicar` publica relatorio final (URL publica + PageSpeed + headers + pendencias).

## Template canonico de vercel.json

Mantido em `.claude/skills/lp-publicar/vercel.template.json` — headers de seguranca (HSTS, nosniff, X-Frame-Options, Referrer-Policy, Permissions-Policy, COOP) + `cleanUrls: true` + `trailingSlash: false`.

## Formulario

Durante design e revisao: mock `<form action="#" onsubmit="event.preventDefault()">`.
Integracao real so via `lp-integrar-form` (Jotform, RD Station, HubSpot), manual-trigger apos aprovacao do design. Wrapper CSS canonico em `.claude/skills/lp-integrar-form/SKILL.md` Passo 3.

