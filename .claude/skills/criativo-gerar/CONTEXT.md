# Contexto Compartilhado — Criativos

> Lido pela skill `criativo-gerar` (e pelo advisor `criativo`) antes de qualquer acao.
> Mesma estrutura dos CONTEXT de copy-criar, pauta-quente e lp-preparar.

A skill **renderiza** criativos estaticos (PNG) a partir de copy estruturada + brandbook da
marca. Ela NAO escreve copy — isso e `/copy-criar` ou `/pauta-quente`. Ela transforma palavras
+ marca em imagem, via HTML/CSS -> Playwright (Chromium headless) -> PNG em dimensao exata.

---

## Marcas Validas

| Marca | Manifest | Tokens | Regras de Geracao | Brandbook |
|---|---|---|---|---|
| `buzzmonitor` | `brand/buzzmonitor/brand-manifest.json` | `brand/buzzmonitor/tokens.json` | `brand/buzzmonitor/generation-rules.json` | `brand/buzzmonitor/BRANDBOOK.md` |
| `buzzcreators` | `brand/buzzcreators/brand-manifest.json` | `...tokens.json` | `...generation-rules.json` | `...BRANDBOOK.md` |
| `cxpress` | `brand/cxpress/brand-manifest.json` | `...tokens.json` | `...generation-rules.json` | `...BRANDBOOK.md` |
| `elife` | `brand/elife/brand-manifest.json` | `...tokens.json` | `...generation-rules.json` | `...BRANDBOOK.md` |

Ao gerar, carregar **nesta ordem**: `tokens.json` (cores/fontes exatas) -> `generation-rules.json`
(bloco `adCreative` — `static` e `carousel`) -> `brand-manifest.json` (tom + `nameUsage` p/ artigo) ->
`BRANDBOOK.md` secao Visual (paleta quando usar, decorativos, mascote, do's & don'ts).

## Regioes / Idiomas

| Regiao (CLI) | Idioma | Artigo da marca |
|---|---|---|
| `brasil` (default) | PT-BR | conforme `nameUsage` do manifest (a Cxpress, a Buzzmonitor, o Buzzcreators) |
| `portugal` | PT-PT | idem PT-BR; "voce" nunca "tu" |
| `latam` | ES-LATAM | **sem artigo** ("Cxpress unifica...") |

## Tipos de peca

| Tipo | Estrutura | Origem da copy |
|---|---|---|
| `carrossel` | 5 cards: **cover -> contexto -> insight -> conector -> CTA** (convencao do repo, ver pauta-quente CONTEXT) | `/copy-criar ... estatico` ou `/pauta-quente` ou copy colada |
| `estatico` | 1 card: hook (+ sub) + CTA | idem |

## Uso × Formato — MARGEM DE SEGURANCA (o coracao da skill)

`uso` define quanto a peca respeita as reservas de UI das plataformas. `formato` define a dimensao.

| formato | px | Plataforma |
|---|---|---|
| `1x1` | 1080×1080 | Feed quadrado (IG/FB/LinkedIn) |
| `4x5` | 1080×1350 | Feed vertical — **recomendado p/ feed** |
| `9x16` | 1080×1920 | Stories / Reels |

| uso | Feed (1x1, 4x5) | Stories/Reels (9x16) |
|---|---|---|
| `organico` | margem estetica ~7%; conteudo pode ir ate a borda, mascote pode sangrar | topo ~120px / base ~160px (evita so os cantos extremos) |
| `anuncio` | **safe margin ~10–12%**; logo/CTA/numeros longe da borda; menos densidade de texto (entrega Meta penaliza peca muito textual) | **safe-zone forte do Meta: topo 250px / base 340px / lados 64px** reservados pra UI (perfil no topo, CTA/swipe/legenda na base) |

Carrossel so roda em **feed** — entao p/ carrossel a diferenca organico↔anuncio e a margem leve (10–12%)
e conter o sangramento do mascote. O safe-zone agressivo (250/340) vale pros formatos 9x16.

**Implementacao:** `base.css` le dois data-attributes no `.canvas` e deriva `--safe-top/-bottom/-x`:
```html
<div class="canvas" data-uso="anuncio" data-fmt="4x5"> ... </div>
```
Em `anuncio`, renderizar tambem o **overlay-guia** (`data-guides="on"` -> faixas semitransparentes nas
zonas reservadas) num PNG `-guia.png` separado, pra QA visual de que nada critico invade a reserva.

> Numeros 250/340 sao conservadores e batem com a POC `criativos/2026-05-22-mcp-webinar-junho`.
> Fonte: Meta "asset customization" (topo ~14%, base ~20–35% podem ser cobertos por UI). Ajustaveis.

## Pipeline de renderizacao

1. HTML/CSS (um arquivo por card, estendendo `base.css`) — texto LITERAL da copy, fontes Google.
2. `render.py` (copiado do skill asset) renderiza cada card no(s) formato(s) pedido(s), DPR=1,
   espera `document.fonts.ready`. Em `anuncio`, gera tambem o `-guia.png`.
3. Verificacao VISUAL obrigatoria (Read de cada PNG) antes de entregar.

**Por que HTML e nao IA (Bloom):** criativo com texto/numero preciso (data, %, preco) tem que sair
pixel-perfect. Modelos de imagem erram tipografia PT-BR (ver memoria `feedback-bloom-mcp-detalhes`).
Bloom serve so como **key visual / fundo** sem texto critico — nunca pra a camada de texto.

## Convencoes de Output

```
criativos/{marca}/{regiao}/{slug}/
├── copy.txt                  (copy estruturada — fonte-verdade)
├── carousel.css | static.css (estende base.css; tokens da marca inline no topo)
├── card-1.html ... card-N.html
├── card-1-{fmt}.png ...      (ex: card-1-1080x1350.png)
├── card-1-{fmt}-guia.png     (so em uso=anuncio)
├── assets/                   (logos + mascote copiados do brand)
└── render.py
```

- `criativos/` e **gitignored** (PNGs pesados + copias de asset; upload manual — ver memoria
  `feedback-criativos-pasta-local`). Nao tentar upload automatizado pro Drive (base64 trunca >3KB).
- `slug`: kebab-case, sem acentos, max 60 chars. Prefixo de data opcional (`YYYY-MM-DD-tema`).
- Entrega: **caminho absoluto da pasta no chat** pro Victor abrir no Explorer e subir onde precisar.

## Pre-requisito tecnico

Playwright + Chromium (uma vez por maquina):
`python -m pip install playwright && python -m playwright install chromium`
Validar: `python -c "from playwright.sync_api import sync_playwright"` sem erro.

## Lembretes de marca (nao esquecer)

- **Contraste WCAG AA.** Cuidar do laranja claro: na Cxpress (`#EF863C`) e na Buzzmonitor, texto
  BRANCO sobre o laranja REPROVA — usar texto escuro (navy/primaryDark) sobre botao laranja.
- **Cxpress — cases pendentes.** BRANDBOOK marca "Cases de Sucesso Verificados" como vazio. Se a copy
  do criativo cita metrica/numero de cliente (BoFu/prova social), avisar que precisa validacao
  comercial antes de publicar (ver memoria `project_cxpress_cases_pendentes`).
- **Artigo gramatical** vem de `nameUsage` no manifest (a Cxpress / a Buzzmonitor / o Buzzcreators;
  ES-LATAM sem artigo). Grafia exata da marca conforme BRANDBOOK (ex: "Cxpress", nunca "CXPress").
- **Mascote** (se a marca tem): usar so renders oficiais de `brand/{marca}/assets/mascot/`, sem
  redesenhar. Opcional — calor humano, nao preenchimento.
