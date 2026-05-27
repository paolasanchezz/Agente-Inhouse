---
name: criativo-gerar
description: Gera imagens de criativo estatico/carrossel (PNG) a partir de copy estruturada + brandbook da marca, via HTML/CSS -> Playwright. Tem flag uso (organico|anuncio) e formato (1x1|4x5|9x16) que aplicam as margens de seguranca do Meta automaticamente. Texto pixel-perfect (nao usa IA de imagem para a camada de texto).
argument-hint: "[marca] [regiao] [tipo] [uso] [formato] [slug] — ex: cxpress brasil carrossel anuncio 4x5 case-10-para-4 (copy em copy.txt da pasta ou colada no chat)"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
version: 1.0.0
---

# Skill: Gerar Criativo (estatico / carrossel)

Voce transforma copy estruturada em **imagens de criativo** production-grade, com a identidade
visual exata da marca e as margens de seguranca corretas para o uso (organico vs anuncio).
Renderiza HTML/CSS via Playwright — **texto sempre pixel-perfect**. Voce NAO escreve a copy
(isso e `/copy-criar`) e NAO inventa numeros, claims ou frases.

## Passo 0: Parsing e Contexto

**Leia `.claude/skills/criativo-gerar/CONTEXT.md` primeiro** (marcas, regioes, tipos, specs de
safe-zone, pipeline, lembretes de marca).

Parsing de `$ARGUMENTS`:

| Argumento | Valores | Default | Obrigatorio |
|---|---|---|---|
| `marca` | `buzzmonitor` \| `buzzcreators` \| `cxpress` \| `elife` | — | Sim |
| `regiao` | `brasil` \| `portugal` \| `latam` | `brasil` | Nao |
| `tipo` | `carrossel` \| `estatico` | `carrossel` | Nao |
| `uso` | `organico` \| `anuncio` | `organico` | Nao |
| `formato` | `1x1` \| `4x5` \| `9x16` (aceita CSV) | `4x5` | Nao |
| `slug` | kebab-case sem acentos | — | Sim |

Se `marca` ou `slug` faltarem, ou se a copy nao foi fornecida, PARE e mostre o uso. Se algum
parametro de enquadramento estiver ambiguo, use `AskUserQuestion` com chips (e o que o advisor
`/criativo` faz).

A **copy** chega de uma destas formas (em ordem de prioridade):
1. Ja existe `criativos/{marca}/{regiao}/{slug}/copy.txt` -> use-a.
2. Colada no chat / arg `fonte` (texto, caminho de arquivo, ou URL Notion) -> estruture e salve em copy.txt.
3. Via advisor `/criativo`: os parametros vem na 1a linha de `$ARGUMENTS` e a copy logo apos um
   marcador `COPY:` (multi-linha). Se vier `usar existente` sem bloco COPY, leia o copy.txt da pasta.

## Passo 1: Carregar Marca

Leia, nesta ordem (nao confie na memoria — leia os arquivos):

1. `brand/{marca}/tokens.json` — cores (hex), tipografia (familias/pesos), radius (pill=9999, botao).
2. `brand/{marca}/generation-rules.json` — bloco **`adCreative`** (`static` e `carousel`) + `constraints.neverDo`.
3. `brand/{marca}/brand-manifest.json` — tom de voz e **`nameUsage`** (artigo gramatical da marca).
4. `brand/{marca}/BRANDBOOK.md` — secao Visual (paleta "quando usar", decorativos pill/arco, mascote, do's & don'ts) + grafia exata da marca.
5. Glob `brand/{marca}/assets/logos/` e `brand/{marca}/assets/mascot/` — inventariar logos (primary/reversed) e poses de mascote disponiveis.

Fixe na cabeca as regras de composicao da marca, ex. Cxpress: 60/30/10, capa/CTA em fundo
primaryDark com mascote, cards internos alternando branco/primaryLighter, destacar numero em
laranja/amarelo (nunca vermelho), max 5 formas, Bitter nunca em corpo.

## Passo 2: Estruturar a Copy (fidelidade total)

Estruture a copy nos blocos do `tipo`, **sem reescrever**:

- `carrossel` -> 5 cards rotulados: **cover / contexto / insight / conector / CTA** (convencao do repo).
- `estatico` -> hook (+ sub opcional) + CTA.

Salve em `criativos/{marca}/{regiao}/{slug}/copy.txt` (formato rotulado, como o exemplo abaixo).
Regra de ouro: **todo texto visivel no PNG vem LITERAL da copy.** Voce pode dar enfase tipografica
(tamanho/cor/peso) a numeros e palavras-chave, mas nao trocar palavra, nao parafrasear, nao
truncar frase-ancora, nao inventar eyebrow/CTA que mudem o sentido (rotulos curtos neutros tipo
"Antes"/"Depois" sao OK como organizacao visual).

Confira a grafia da marca e o **artigo** (`nameUsage`): PT "a Cxpress / a Buzzmonitor / o Buzzcreators";
ES-LATAM sem artigo.

## Passo 3: Montar a Pasta

```bash
mkdir -p criativos/{marca}/{regiao}/{slug}/assets
cp .claude/skills/criativo-gerar/assets/base.css   criativos/{marca}/{regiao}/{slug}/
cp .claude/skills/criativo-gerar/assets/render.py  criativos/{marca}/{regiao}/{slug}/
# copiar SO os assets que a peca usa (logo certo p/ o fundo, poses de mascote escolhidas):
cp brand/{marca}/assets/logos/logo-reversed.svg    criativos/.../assets/   # fundos escuros
cp brand/{marca}/assets/logos/logo-primary.svg     criativos/.../assets/   # fundos claros
cp brand/{marca}/assets/mascot/<poses-escolhidas>  criativos/.../assets/   # se usar mascote
```
`criativos/` ja e gitignored — nao versiona. Referencie assets por caminho relativo simples
(`assets/logo-reversed.svg`), nunca `../../../brand/...` (quebra com a profundidade da pasta).

## Passo 4: Construir os Cards (HTML + CSS da peca)

Crie `{carousel|static}.css` que **importa base.css** e define os tokens da marca + layout:

```css
/* topo do css da peca */
:root{ --navy:#232960; --royal:#4A69BD; --orange:#EF863C; /* ...tokens da marca... */
       --ff-head:"Open Sans",system-ui,sans-serif; --ff-body:"Source Sans 3",system-ui,sans-serif; }
```
E `card-N.html` (um por card) com `<link rel="stylesheet" href="base.css">` ANTES do css da peca,
o Google Fonts da marca, e a estrutura:
```html
<div class="canvas">           <!-- render.py injeta data-uso/data-fmt -->
  <span class="glow ..."></span> <span class="deco pill ..."></span>
  <div class="topbar"><img class="logo" src="assets/..."><span class="counter"><b>01</b> / 05</span></div>
  <div class="core"> ... conteudo do card ... </div>
  <img class="mascot bleed" src="assets/...">   <!-- opcional -->
</div>
```

Regras de design (valem p/ qualquer marca):
- **Uma ideia por card.** Hierarquia: hook (display/Open Sans) > corpo (body font, peso leve) > stat/CTA.
  Corpo NUNCA na fonte de display da marca quando a marca separa display/body (ex: corpo = Source Sans, nao Open Sans bold).
- **Cor:** seguir 60/30/10 e `generation-rules.adCreative`. Capa/CTA podem inverter (fundo cor dominante).
- **Numeros/stats:** destacar com cor de acento OU chip de fundo — mas o TEXTO do numero fica numa
  cor que passe **WCAG AA** no fundo. Ex.: nunca laranja-claro como cor de texto sobre branco
  (reprova); use o numero em navy e o acento como chip/sublinhado.
- **CTA:** botao preenchido. Cuidado com contraste do texto — **na Cxpress/Buzzmonitor, texto BRANCO
  sobre laranja REPROVA**; usar texto escuro sobre laranja, ou fundo navy + texto branco.
- **Decorativos:** so pills/arcos canonicos, cor da paleta, max 5, em cantos longe do texto/mascote.
- **Mascote:** so poses oficiais; `.bleed` pode sangrar em organico. Em anuncio o base.css ja
  contem o sangramento — confira no Passo 6 que nada critico fica fora da safe zone.
- **NAO** desenhar a camada de texto com IA de imagem (Bloom). Se quiser key visual gerado, ele
  entra como `<img>` de fundo SEM texto critico, e o texto vai por cima em HTML.

Multi-formato: se `formato` tem mais de um, adicione media-queries por aspect-ratio (padrao da POC
`criativos/.../2026-05-22-mcp-webinar-junho/criativo-1/index.html`) ajustando tamanhos de fonte.

## Passo 5: Renderizar

```bash
cd criativos/{marca}/{regiao}/{slug} && python render.py {formato-csv} {uso}
```
Saida: `card-N-{dim}.png` (+ `card-N-{dim}-guia.png` quando `uso=anuncio`).
Se Playwright/Chromium nao estiver instalado, instale (CONTEXT, "Pre-requisito tecnico"). Zero
request failures esperado — se logo/fonte falhar, corrigir path/conexao antes de seguir.

## Passo 6: Verificacao Visual (OBRIGATORIO)

**Leia (Read) cada PNG gerado.** Checklist:

- [ ] **Copy fiel:** todo texto/numero confere LITERAL com copy.txt (ex: 8.200, 62%, 9.023, 100% —
      sem digito trocado, sem corte). Esta e a razao de renderizar em HTML; valide de verdade.
- [ ] **Marca:** cores da paleta, fontes certas (display vs body), grafia + artigo da marca corretos.
- [ ] **Contraste:** todo texto legivel; nenhum texto reprovando AA (especial atencao a acentos claros).
- [ ] **Layout:** sem overflow, sem colisao texto×mascote, respiro adequado, decorativos discretos.
- [ ] **Safe zone (so `uso=anuncio`):** abra o `-guia.png` e confirme que logo, texto, numeros e CTA
      estao DENTRO do tracejado verde — nada critico nas faixas vermelhas (reservas de UI). Mascote/
      decorativo pode tocar a faixa, conteudo informativo NAO.

Iterar no CSS/HTML e re-renderizar ate passar. (Corrigir copy introduz risco de IA — reconferir
contagens de em-dash/clichês se editar texto; ver `conhecimento/editorial/regras-anti-ia.md`.)

## Passo 7: Entrega

- Entregue o **caminho absoluto da pasta** no chat (Victor abre no Explorer e sobe onde precisar).
  NAO tentar upload automatizado pro Drive (base64 trunca — ver memoria `feedback-criativos-pasta-local`).
- Liste os PNGs finais por card e formato; em anuncio, mencione os `-guia.png` de QA.
- **Cxpress + prova social:** se a copy cita metrica/numero de cliente, avise que os "Cases de Sucesso
  Verificados" do brandbook estao pendentes — validar com o comercial antes de publicar.
- Sugira proximos passos: outro formato (`/criativo-gerar ... {outro-formato}`), versao anuncio/organico,
  ou copy nova via `/copy-criar {marca} {regiao} estatico {estagio} "{tema}"`.

## Erro recorrente -> melhorar a skill

Se um bug/regra de marca aparecer durante a geracao (contraste, vazamento de IA, path de asset,
safe-zone errada), conserte a skill/base.css/CONTEXT **antes de fechar**, nao so o caso pontual
(memoria `feedback-skill-improvement`). Bumpe `version` e registre no CHANGELOG.
