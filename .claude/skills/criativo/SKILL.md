---
name: criativo
description: Gera imagens de criativo (estatico/carrossel) ponta a ponta — adapta a copy, carrega brandbook + GUIDELINES, gera (HTML/Playwright por padrao ou Bloom sob pedido), revisa as imagens e entrega numa pasta local. Aplica margem de seguranca por uso (organico|anuncio) e formato (1x1|4x5|9x16). Texto pixel-perfect no caminho HTML.
argument-hint: "[marca] [regiao] [tipo] [uso] [formato] [slug] + copy (colada/arquivo/Notion). Sem args, pergunta com chips. Ex: cxpress brasil carrossel anuncio 4x5 case-10-para-4"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, mcp__2b376cfc-3735-4db6-b756-53e1c3b8b48a__bloom_check_credits, mcp__2b376cfc-3735-4db6-b756-53e1c3b8b48a__bloom_list_brands, mcp__2b376cfc-3735-4db6-b756-53e1c3b8b48a__bloom_get_brand, mcp__2b376cfc-3735-4db6-b756-53e1c3b8b48a__bloom_onboard_brand, mcp__2b376cfc-3735-4db6-b756-53e1c3b8b48a__bloom_create_logo_upload_url, mcp__2b376cfc-3735-4db6-b756-53e1c3b8b48a__bloom_generate_image, mcp__2b376cfc-3735-4db6-b756-53e1c3b8b48a__bloom_edit_image, mcp__2b376cfc-3735-4db6-b756-53e1c3b8b48a__bloom_get_image
version: 1.2.0
---

# Skill: /criativo — gerar criativo ponta a ponta

Voce gera imagens de criativo (estatico/carrossel) do comeco ao fim: **adapta a copy → carrega
brandbook + GUIDELINES → gera (engine HTML ou Bloom) → revisa as imagens → entrega numa pasta local**.

**Leia `criativos/GUIDELINES.md` ANTES de gerar e de revisar.** Ele e a fonte das REGRAS (formato,
safe-zone, cor, tipografia, fidelidade, revisao, entrega). Este SKILL.md e o PROCESSO. Nao duplicar
regras — citar `GUIDELINES §N`.

## Dados de referencia

| marca | regiao (CLI) | idioma | artigo |
|---|---|---|---|
| `buzzmonitor` `buzzcreators` `cxpress` `elife` | `brasil` (PT-BR) · `portugal` (PT-PT) · `latam` (ES-LATAM) | — | de `nameUsage` no manifest; ES-LATAM sem artigo |

Marca: `brand/{marca}/` (`tokens.json`, `generation-rules.json`, `brand-manifest.json`, `BRANDBOOK.md`,
`assets/logos/`, `assets/mascot/`). Saida: `criativos/{marca}/{regiao}/{slug}/`. Scaffold da engine
HTML: `.claude/skills/criativo/assets/` (`base.css`, `render.py`).

## Passo 0 — Parsing + perguntas (chips)

Parse de `$ARGUMENTS`:

| Arg | Valores | Default |
|---|---|---|
| `marca` | buzzmonitor·buzzcreators·cxpress·elife | — (obrigatorio) |
| `regiao` | brasil·portugal·latam | brasil |
| `tipo` | carrossel·estatico | carrossel |
| `uso` | organico·anuncio | organico |
| `formato` | 1x1·4x5·9x16 (CSV) | 4x5 (GUIDELINES §1) |
| `slug` | kebab-case | — (obrigatorio) |

Para qualquer parametro ausente, pergunte com `AskUserQuestion` (chips). **Engine:** verifique se o
MCP do Bloom esta disponivel (tente `bloom_check_credits` ou `ToolSearch "bloom"`). Se SIM, pergunte
"Bloom ou HTML?" (GUIDELINES §3). Se NAO, **nao mencione Bloom** — siga HTML (degrada sem erro).
**Copy:** colada no chat, caminho de arquivo, ou URL Notion. Se nao houver copy, sugira
`/copy-criar {marca} {regiao} estatico {estagio} "{tema}"` e pare.

## Passo 1 — Copy (adaptativo · GUIDELINES §9)

**Se `regiao` != `brasil`, carregue ANTES o padrao linguistico** (`conhecimento/linguistico/{pt-portugal|es-latam}/padrao-linguistico.md`): qualquer enxugue/reescrita/diagramacao tem que sair em PT-PT/ES **nativo**. Se o arquivo nao carregar, PARE e avise. Sem ele, "enxugar" copy estrangeira reintroduz brasileirismo ("esta a fazer" vira "esta fazendo", "utilizador" vira "usuario").

Avalie a qualidade da copy recebida:
- **Ja bem estruturada e encaixa no layout → LITERAL** (so diagrama, nao mexe nas palavras).
- **Crua/desestruturada → adapta** estrutura (quebra em cards/blocos) + enxuga leve + passa anti-IA
  (`conhecimento/editorial/regras-anti-ia.md` + anexo do idioma se `regiao` != `brasil`).
- **Sempre** preserva numeros/dados/claims exatos; nunca inventa frase/hook/CTA. Rotulos neutros de
  organizacao ("Antes"/"Depois") sao OK.
- **Se `regiao` != `brasil`:** confira a copy final contra o padrao linguistico (vocabulario, "estar a + infinitivo", tratamento, CTAs nativos). Zero brasileirismo no criativo.

Salve a copy final em `criativos/{marca}/{regiao}/{slug}/copy.txt` (blocos rotulados por card).
A estrutura SAI DA COPY — sem template fixo (GUIDELINES §4).

## Passo 2 — Marca

Leia (nao confie na memoria): `tokens.json` → `generation-rules.json` (bloco `adCreative` +
`constraints.neverDo`) → `brand-manifest.json` (`nameUsage` + tom) → `BRANDBOOK.md` (secao Visual:
paleta/decorativos/mascote/grafia). Glob `assets/logos/` e `assets/mascot/` pra inventariar.

## Passo 3 — Gerar (pela engine escolhida)

### 3A — Engine HTML/Playwright (padrao)

1. Scaffold: `mkdir -p criativos/{marca}/{regiao}/{slug}/assets`; copie `.claude/skills/criativo/assets/base.css`
   e `render.py` pra pasta da peca; copie os assets de marca USADOS (logo do fundo certo, poses de
   mascote escolhidas) pra `assets/` (referencie por caminho relativo simples, ex: `assets/logo-reversed.svg`).
2. Crie `{carousel|static}.css` que **`@import url("base.css");`** no topo + define os tokens da marca
   (`--brand-*`, fontes) + layout dos cards. Crie `card-N.html` (um por card/peca) ligando esse css +
   Google Fonts da marca, estrutura `.canvas > .topbar + .core + (deco/mascot)`.
3. Aplique as regras de design do GUIDELINES: §5 tipografia (display vs body), §6 cor + **auto-AA**
   (nunca branco sobre laranja — texto escuro), §7 decorativos canonicos, §8 mascote so quando agrega.
   `render.py` injeta `data-uso`/`data-fmt` no `.canvas` — nao hardcodar safe-zone no css da peca.
4. Render (Pre-req Playwright+Chromium — GUIDELINES §Lembretes; em `anuncio` gera tambem `-guia.png`).
   Se o Playwright nao carregar (no Windows o greenlet falha com `DLL load failed while importing
   _greenlet`), o `render.py` cai sozinho no Chrome headless e segue — mesma saida, mesmo contrato:
   ```bash
   # Python resiliente ao shim da Store no Windows (testa execucao; macOS/Linux -> python3). Single-token.
   PYBIN=""; for _c in py python3 python; do command -v "$_c" >/dev/null 2>&1 && "$_c" -c '' >/dev/null 2>&1 && { PYBIN="$_c"; break; }; done; PYBIN="${PYBIN:-python}"
   cd "criativos/{marca}/{regiao}/{slug}" && "$PYBIN" render.py {formato-csv} {uso}
   ```

### 3B — Engine Bloom (opt-in · so se escolhida E MCP disponivel)

Bloom monta a **peca inteira** por IA (GUIDELINES §3). Use so quando o conceito e um key-visual generativo.
1. Marca no Bloom: `bloom_list_brands` → se ja onboarded (ver memoria `reference_bloom_buzzmonitor`),
   reusa o brand id; senao `bloom_onboard_brand`. Se voltar `logo_required`: `bloom_create_logo_upload_url`
   + upload do logo do brand com **≥300px** (upscale via Pillow se preciso; token single-use) — memoria
   `feedback_bloom_mcp_detalhes`.
2. `bloom_generate_image` com o DNA da marca + prompt. **Texto curto** no prompt (Bloom erra tipografia
   PT-BR). Baixe o PNG com `curl -sL -A "Mozilla/5.0" -o ...` (URL e redirect — `-L` obrigatorio).
3. Salve em `criativos/{marca}/{regiao}/{slug}/`. Trate como peca inteira (sem camada HTML de texto —
   este e o caminho independente; pra texto preciso, o usuario usa a engine HTML).

## Passo 4 — Revisao automatica (GUIDELINES §10)

**Leia (Read) cada PNG.** Checklist: copy fiel (numero/texto literal), marca (paleta/fontes/grafia/artigo),
contraste AA, layout (sem overflow/colisao), safe-zone em `anuncio` (abrir `-guia.png` — nada critico no
vermelho), tipografia (sem caractere torto — **forte no Bloom**). Em `anuncio`, **avise se a peca estiver
muito textual** (entrega Meta) e sugira enxugar.

Comportamento: **auto-corrige o corrigivel e re-renderiza** ate passar (HTML). Bloom com texto corrompido
→ `bloom_edit_image` ou regenerar. Nao pausa pra aprovacao (GUIDELINES §11).

## Passo 5 — Entrega (GUIDELINES §11)

Entregue o **caminho absoluto da pasta no chat**. Liste os PNGs por card/formato; em `anuncio`, cite os
`-guia.png`. Sem upload automatico. **Cxpress + prova social:** se a copy cita metrica de cliente, avise
que os cases verificados estao pendentes. Sugira proximos: outro formato/uso, ou copy via `/copy-criar`.

## Erro recorrente → melhorar a skill

Bug/regra de marca recorrente durante a geracao (contraste, vazamento de IA, path de asset, safe-zone,
tipografia Bloom): conserte a skill / `base.css` / `GUIDELINES.md` **antes de fechar** (memoria
`feedback_skill_improvement`). Bumpe `version` e registre no CHANGELOG.
