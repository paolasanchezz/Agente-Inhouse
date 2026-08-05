# Guidelines — Landing Pages

> Regras gerais para toda LP gerada dentro de `landing-pages/`.
> Complementa `brand/{marca}/generation-rules.json` — quando houver conflito, o brand vence no **que** (cores, fontes), este arquivo vence no **como** (composição, ritmo).

## 1. Paleta — consistência > variedade

**Escolher 2 a 3 cores fortes por LP e manter até o fim.** A marca pode ter 5 cores, mas a LP usa um subset.

- Escolher 1 cor primária (CTA, links, acentos fortes) + 1 ou 2 de apoio.
- Fugir da tentação de "usar todas as cores da paleta porque existem".
- As cores escolhidas aparecem em CTA, headings de destaque, bordas e micro-acentos — não em fundos grandes.
- **Nunca** tingir seções inteiras com variantes claras diferentes (rosa-claro, roxo-claro, teal-claro alternando). Isso vira colcha de retalhos.
- Se precisar variar fundo entre seções, **alternar branco ↔ neutral-100 (off-white)**. Só isso. Uma única seção pode ser escura (dark = cor primária da marca) para criar contraste dramático.
- Gradientes: usar no máximo **um tipo de gradiente por LP** (ex.: rosa → laranja) e aplicar em 1-2 momentos de alto impacto, não em fundo de seção.

**Checklist antes de publicar:**
- [ ] Consigo listar as 2-3 cores da LP em uma frase?
- [ ] Existe apenas 1 gradiente ativo?
- [ ] Nenhuma seção tem fundo de cor-clara que "briga" com outra?

## 2. Ritmo e respiro

- **Espaço em branco é feature, não bug.** Seções devem respirar — `padding` vertical generoso (min `120px` desktop, `80px` mobile; para LPs premium mirar `160px` / `100px`).
- Dar ao menos **1 seção de "pausa"** sem CTA nem card — só um título grande ou uma linha forte — para o olho descansar antes do próximo bloco de densidade.
- Entre o hero e a primeira seção de conteúdo, reservar transição visual (ticker, divisor, ou apenas respiro extra).
- **Não empilhar cards direto em cima de cards.** Sempre intercalar com seções mais aéreas.

**Regra prática:** se rolar a LP inteira e a sensação for "apertada", aumentar todos os `padding` de seção em 20%.

## 3. Hero

- **H1 carrega a dor, não a solução.** A primeira linha do hero nomeia o problema mais latente do público; a promessa e o método vão para o H2 / sub-headline. É a regra que vem antes de todas — ver `conhecimento/copywriting/fundamentos-copy.md` §0. Ex.: H1 "Monitorar as redes sociais virou uma confusão" + H2 "Veja como marcas unificam o social listening em 5 passos" — **não** H1 "Monte o seu monitoramento em 5 passos". Exceção: lead quente/BoFu já consciente da dor pode abrir pelo ganho (calibrar pelo funil).
- Padrão de referência: **fundo branco (ou neutral-100)**, texto à esquerda, elemento visual clean à direita. Gradientes full-bleed coloridos só quando o briefing pedir impacto máximo — senão, preferir limpeza.
- Título principal no peso mais pesado da display font. Subtítulo em peso leve para contraste tipográfico.
- Elemento da direita: **um** elemento forte (card de data, ilustração minimalista, foto com crop editorial). Não encher de formas.
- CTA primário visível sem scroll. CTA secundário (opcional) ghost ao lado.
- Indicador de data/formato no header (ex.: "Webinar gratuito", dot pulsante): texto curto e **sempre em uma única linha** (`white-space: nowrap`). Nunca duplicar info que já aparece em outro lugar do hero — o indicador é um resumo discreto, não um repositório de dados. Se a tela for estreita demais para a linha única, preferir esconder via `@media` a quebrar em duas linhas.
- **Mobile — headline sempre primeiro.** No `@media (max-width: 980px)` o `.hero-content` (overline + H1 + body + CTA) precede o visual (card-ticket / ilustração). Nunca usar `order: -1` no `.hero-visual` para "puxar" o card pra cima — quebra a hierarquia narrativa (usuário precisa entender O QUÊ antes de QUANDO). Se o DOM tiver `.hero-content` antes de `.hero-visual` (padrão do `lp-gerar`), basta NÃO aplicar `order` no mobile e o grid empilha naturalmente na ordem certa. Histórico: 2026-05-15, LP `latam-webinar-atencionalcliente` (Cxpress) reportada pelo Victor com card de data acima da headline no mobile. Mesmo padrão presente em `playbook-whatsapp2026` e `webinar-tecnologia-maio2026` (todas Cxpress).

## 4. Animação

- Motion serve ao conteúdo, não o esconde. Reveals com `opacity: 0 → 1` precisam de fallback caso a animação não dispare (ex.: `@supports` ou prefers-reduced-motion).
- **Nunca** deixar texto essencial invisível esperando animação. Se a animação falhar por qualquer motivo (lentidão, bug, extensão do browser), o texto deve aparecer.
- Usar motion em 2-3 momentos-chave: entrada do hero, scroll-reveal de cards, hover de CTA. Basta.

## 5. Copy

- Respeitar copy do briefing/Notion — ajustes cosméticos ok, mas não reescrever tom.
- **Hero lidera com a dor** (ver §3 e `conhecimento/copywriting/fundamentos-copy.md` §0). Se o H1 do briefing abre pela solução/método/oferta em vez do problema do público, **sinalizar como sugestão** (mesma postura conservadora do anti-IA — não reescrever o tom silenciosamente). O ajuste do H1 é decisão de quem aprova a copy.
- Usar aspas curvas (`&ldquo; &rdquo;`) e ellipsis (`&hellip;`) corretos.
- **Em-dash (`—` / `&mdash;`) PROIBIDO** — tolerância zero, ver `conhecimento/editorial/regras-anti-ia.md`. Substituir por vírgula, ponto ou parênteses conforme a função. Vale para copy bruta, copy estruturada e HTML renderizado. Validação: `grep -c "—" index.html` deve retornar 0; `grep -c "&mdash;" index.html` deve retornar 0.
- Números em algarismos (23 de Abril, não "vinte e três").

## 6. Estrutura mínima

Toda LP tem: **Hero → Problema/contexto → Oferta/Programa → Diferencial → Para quem → Prova (speakers/social proof) → Urgência → CTA final → Footer.** Pode cortar seções, mas não inverter a ordem narrativa. Onde o formulário aparece dentro dessa estrutura é decidido pela §10 (2ª seção para ToFu; 4ª ou última para MoFu/BoFu/Remarketing).

## 7. Acessibilidade (non-negotiable)

Seguir [Vercel Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md) — ver skill `web-design-guidelines`. Em especial: skip-link, focus-visible, labels em todos os inputs, `alt`/`aria-hidden` em imagens, `prefers-reduced-motion`.

Dois pontos que já reprovaram AA em LPs reais — checar sempre:

- **Contraste de texto em fundo tingido: ≥4.5:1.** Texto sobre pílula/badge/tag/chip com cor de fundo (eyebrow, selo) usa a cor **escura** da marca (ex.: navy), nunca o tom médio de destaque (ex.: royal). Royal `#4A69BD` sobre lilás claro `#D7E2FF` dá ≈4.0:1 e **reprova**; navy `#232960` sobre o mesmo lilás dá ≈10:1. Regra: quanto mais claro o tint de fundo, mais escuro o texto. Atenção especial ao eyebrow do hero, que costuma herdar a cor de destaque do `.eyebrow` base e só trocar o fundo.
- **Sem `aria-live` em contador/timer que atualiza sozinho.** Countdown de evento leva `aria-hidden="true"` — a data já vive na copy do hero e no JSON-LD. `aria-live` (mesmo `polite`) num contador que muda a cada segundo inunda leitores de tela (WCAG 2.2.2).

## 8. Seções-tipo com linguagem visual consistente

Cada tipo de seção tem gramática visual fixa. Não misturar.

- **Problema / dor** — lista vertical (não grid), cada item com ícone **X vermelho** (`color: var(--danger)` ou red-600). Texto curto, uma frase por item. O objetivo é parecer "checklist do que está errado hoje". Fundo branco ou neutral-100.
- **Benefícios / o que você vai levar** — grid (2 ou 3 colunas desktop, 1 mobile), cada card com ícone **✓ verde** (`color: var(--success)` ou green-600) ou marcador da cor primária da marca. Contraste deliberado com a seção de problema: grid vs. lista, verde vs. vermelho.
- **Urgência / escassez** — **fundo escuro** (preferir a cor primária da marca em tom dark, não preto puro), com uma **tag ou selo em cor quente rotacionada levemente** (ex.: `transform: rotate(-3deg)`, fundo amarelo/laranja, texto escuro). Regra: aparece **uma vez** na LP. É o único momento de "gritar".
- **Prova / speakers** — cards horizontais com foto circular ou crop editorial à esquerda, nome + cargo à direita. Sem badges exagerados.
- **CTA final** — seção full-width com fundo destaque (gradiente ou cor primária), título grande, form ou botão centralizado. Última coisa antes do footer.

A regra por trás: o olho aprende **um vocabulário por tipo de seção** e reconhece o contexto sem ler. Se problema e benefício usam o mesmo layout, o leitor não distingue.

## 9. Copy dita estrutura

A ordem e a quantidade de blocos da LP seguem a narrativa da copy — não o gosto estético de quem gera.

- Se a copy tem **3 bullets de benefício**, a LP tem grid de 3 (não 4 para "ficar bonito", não 2 para "simplificar").
- Se a copy começa problematizando em 5 dores, a seção de problema tem 5 itens — não resumir para 3 "principais".
- Se a copy não tem seção de diferencial explícita, **não inventar uma**. Vazio é válido.
- Antes de gerar HTML, mapear: quantos blocos de cada tipo a copy pede? Essa contagem é a planta baixa, não sugestão.

Regra prática: se precisou adicionar ou cortar bloco para "a LP ficar equilibrada", pare — o desequilíbrio é da copy, não do HTML. Volte ao autor da copy.

## 10. Posicionamento do formulário por tipo de LP

A posição ideal varia com a temperatura do tráfego. **Default forte** — override permitido quando o briefing pedir explicitamente, quando a marca já for muito conhecida do tráfego (lead quente), ou quando teste A/B local provar o contrário. Justificar no PR / REVISAO.md.

**Contagem de seções:** hero é §1. Cada bloco visual subsequente (problema, benefícios, prova, urgência, CTA final) conta como §2, §3, §4 etc. Footer não conta.

- **ToFu — webinar, material rico, lead frio** → formulário na **2ª seção** (logo após o hero). Lead frio aceita preencher por curiosidade; o objetivo é volume, MQL pipeline filtra depois. Mover o form para o fim aqui desperdiça intenção quente.
- **MoFu / BoFu / Remarketing — material avançado, comparativos, agendar demo, falar com vendas, retargeting** → formulário na **4ª seção ou na última seção** (meio/fim da página, após prova social e diferencial). O scroll funciona como filtro de intenção: quem chega ao form passou pelo argumento e tende a converter como SQL. Form no topo aqui infla CPL com leads que ainda não entenderam a oferta.
- **Em todos os casos**: manter um **CTA visível no hero (§1)** — botão que rola suave até o form. Captura tráfego decidido sem sacrificar quem precisa do contexto.

## 11. Integração tardia de formulário

Formulário real (Jotform, RD Station, HubSpot embed) **só entra depois do design aprovado**. Durante toda a fase de design e revisão, usar mock:

```html
<form class="form" action="#" method="post" onsubmit="event.preventDefault()">
  <!-- inputs mock -->
</form>
```

Razão: embeds externos atrapalham iteração de design (iframe lento, CSS de terceiros, altura dinâmica) e obrigam retrabalho a cada ajuste de layout. Integrar via skill `lp-integrar-form` só quando o layout está travado. Wrapper CSS canônico do embed em `.claude/skills/lp-integrar-form/SKILL.md` Passo 3.

Logo em hero/CTA: **pode ser grande se for transparente** (SVG com fundo transparente). PNG com fundo branco fica pequeno ou vira "adesivo". Regra: logo respira se o formato permite.

## 12. Favicon — PNG do brand, path absoluto

Toda LP **tem que ter** favicon. Padrão único, sem variação:

**No source (repo):**
```html
<link rel="icon" type="image/png" href="../../brand/{marca}/assets/logos/logo-icon.png" />
```

**No sibling/deploy (após `lp-publicar`):**
```html
<link rel="icon" type="image/png" href="/assets/logos/logo-icon.png" />
```

Regras:
- **Um link só.** Não adicionar `apple-touch-icon` duplicado nem `<link rel="icon" type="image/svg+xml">`.
- **Usar `logo-icon.png` do brand** (~13KB). Nunca os SVGs de `brand/{marca}/assets/logos/*.svg` — são auto-traceados, pesam 100KB+ e Edge/Chrome rejeitam em silêncio (aparece globinho genérico).
- **Path absoluto com `/` inicial no deploy.** Relativo (`favicon.png`) **quebra** porque `vercel.json` usa `cleanUrls: true` + `trailingSlash: false` — o browser resolve URL sem barra como se o último segmento fosse arquivo, e busca no root do domínio em vez da subrota.
- Não criar `favicon.png`/`favicon.svg` na pasta da LP. Sempre apontar pro `logo-icon.png` que já existe no brand.

**Validar pós-deploy:**
```bash
curl -I https://{dominio}/assets/logos/logo-icon.png  # deve dar 200
```

Se vier 404, a skill `lp-publicar` não copiou o `logo-icon.png` pro `assets/logos/` da sibling — checar antes de fechar.

## 13. Performance — PageSpeed basta

GTmetrix avaliado e descartado (free tier redireciona pra signup após o 1º teste público; API dá só 5 trial credits totais). Se um dia precisar de segunda ferramenta, usar WebPageTest.org (API grátis, 200/dia).

## 14. `<img>` em grid container — `min-height: 0` obrigatório

Padrão recorrente em LPs (mascote, hero image, ilustração de seção) é colocar `<img>` com dimensões intrínsecas (`width`/`height` HTML) dentro de um container grid com `aspect-ratio` no pai. **Sem `min-height: 0` no `<img>`, Safari iOS quebra**: o default `min-height: auto` de grid items combinado com a altura intrínseca grande da imagem faz Safari ignorar a referência percentual e renderizar a imagem em tamanho gigante. Chrome/Firefox aplicam `max-width: 100%` como cap retroativo; Safari iOS não.

**Regra:**

```css
.container {
  display: grid; place-items: center;
  aspect-ratio: 1/1;     /* ou outro ratio */
  max-width: 380px;
  width: 100%;
}
.container img {
  height: 102%;          /* ou outra % */
  width: auto;
  max-width: 100%;
  min-height: 0;         /* ← INEGOCIÁVEL: sem isso, Safari iOS explode pra altura intrínseca */
}
```

**Defesa em profundidade:** seções que contêm `.for-visual`-like (qualquer container com imagem decorativa que possa vazar) devem ter `overflow: hidden`. Custo zero, blinda contra qualquer outro overflow futuro.

Aplica-se a qualquer `<img>` filho de grid item — não só mascote. Mesma armadilha cabe em `<picture>` (o `<img>` interno é o renderizado, pega o bug).

Histórico: 2026-05-11, LP `analise-preditiva-maio-2026` (Buzzmonitor) reportada pelo Victor com mascote oversized cobrindo a seção `.speakers` no iPhone. Mesmo padrão presente em `monitoramento-concorrentes-maio-2026-pt` e `social-listening-mayo-2026-latam` (todas Buzzmonitor, todas com mascot.png 810×1080). Fix aplicada nas 3 e documentada aqui.

## 15. SEO obrigatório — pacote completo no `<head>`

Toda LP **tem que ter** o pacote SEO completo. Não é opcional. Without `meta description` Google usa o primeiro parágrafo aleatório; sem `og:image` o WhatsApp/LinkedIn renderizam o logo do navbar minúsculo; sem JSON-LD a marca não aparece em rich results.

**Obrigatórios:**

```html
<!-- 1. Descrição (~150-160 chars, copy localizada por idioma) -->
<meta name="description" content="...">
<meta name="robots" content="index, follow">

<!-- 2. Open Graph (mínimo 8 tags) -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="{Marca}">
<meta property="og:locale" content="{pt_BR | es_LA | pt_PT}">
<meta property="og:url" content="https://{dominio}/{slug}">
<meta property="og:title" content="{título da LP — pode ser igual ao <title>}">
<meta property="og:description" content="{descrição curta — 150 chars}">
<meta property="og:image" content="https://{dominio}/assets/{marca}/og-{slug}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{descrição da imagem}">

<!-- 3. Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="...">
<meta name="twitter:description" content="...">
<meta name="twitter:image" content="{mesma URL de og:image}">

<!-- 4. JSON-LD (Organization + WebPage + SoftwareApplication/Article/Event conforme natureza da LP) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", "@id": "{home-da-marca}#organization", "name": "{Marca}", "url": "{home-regional-da-marca}", "logo": "https://{dominio}/assets/{marca}/logos/logo-primary.png", "sameAs": ["{linkedin}", "{instagram-regional}"] },
    { "@type": "WebPage", "@id": "https://{dominio}/{slug}#webpage", "url": "https://{dominio}/{slug}", "name": "{<title>}", "inLanguage": "{pt-BR | es-419 | pt-PT}", "isPartOf": { "@id": "{home-da-marca}#organization" }, "description": "..." },
    { "@type": "{SoftwareApplication | Article | Event ...}", "name": "...", "url": "...", "inLanguage": "...", "publisher": { "@id": "{home-da-marca}#organization" } }
  ]
}
</script>
```

**Regras:**

- `og:image` precisa ser **URL absoluta** (não relativa) — Facebook/LinkedIn não resolvem relativa. Mesma regra para `twitter:image` e logos em JSON-LD.
- `og:image` deve apontar para arquivo `.png` ou `.jpg` que **existe** no domínio (`curl -I` retorna 200). Sem isso o preview some.
- `meta description` tem que ser **única por idioma** — não duplicar a copy do BR no PT/ES. Sintaxe nativa importa.
- JSON-LD: o objeto `Organization` referencia `home-regional-da-marca`, `sameAs` lista LinkedIn global + Instagram da região, `logo` aponta para PNG absoluto. Source de verdade é o `brand/{marca}/brand-manifest.json` (campos `regions.{regiao}.home`, `regions.{regiao}.instagram`, `socials.linkedin`).
- O `<title>` da página NÃO deve ter sufixos de trabalho (`[REVISADO]`, `[TESTE]`, `[DRAFT]`) — `lp-publicar` remove, mas geração já deve sair limpa.
- Encoding: usar UTF-8 literal no `content="..."` (acentos diretos). Entidades HTML (`&aacute;`) também funcionam mas misturam estilo — escolher uma.

**Validação local antes de publicar:**

```bash
# 1. Counts esperados (1 description, ≥8 og, ≥4 twitter, 1 jsonld)
grep -c 'meta name="description"' index.html  # 1
grep -c 'meta property="og:' index.html       # >= 8
grep -c 'meta name="twitter:' index.html      # >= 4
grep -c 'application/ld+json' index.html      # 1

# 2. JSON-LD parseia
python -c "import re,json,sys; m=re.search(r'<script type=\"application/ld\+json\">(.*?)</script>', open('index.html').read(), re.S); json.loads(m.group(1)); print('OK')"
```

## 16. Multi-idioma — `hreflang` + `canonical`

Quando a LP tem variantes em outros idiomas (ex: `mcp`, `mcp-es`, `mcp-pt`), **cada uma** das LPs precisa listar TODAS as variantes (incluindo a si mesma) via `<link rel="alternate" hreflang="...">`, mais um `x-default` apontando para a versão principal.

```html
<link rel="canonical" href="https://{dominio}/{slug-desta-LP}">
<link rel="alternate" hreflang="pt-BR" href="https://{dominio}/{slug-br}">
<link rel="alternate" hreflang="es-419" href="https://{dominio}/{slug-es}">
<link rel="alternate" hreflang="pt-PT" href="https://{dominio}/{slug-pt}">
<link rel="alternate" hreflang="x-default" href="https://{dominio}/{slug-default}">
```

**Regras:**

- `x-default` é a versão **autoritativa** (geralmente a do mercado principal, ex: BR).
- Cada LP tem `canonical` apontando para **si mesma** — não para o default. Sem isso, Google pode tratar todas as variantes como duplicadas e indexar só uma.
- `<html lang>` deve bater com o `hreflang` da própria LP (`pt-BR` em BR, `es-419` em LATAM, `pt-PT` em PT).
- Códigos válidos: `pt-BR`, `pt-PT`, `es-419` (latin america), `es-ES` (espanha). Inventar `es-LA` ou `pt-LATAM` quebra a validação do Google.
- Source de verdade dos códigos: `brand/{marca}/brand-manifest.json#regions.{regiao}.{htmlLang, hreflang, ogLocale}`.

## 17. Header / Footer — logo regional, abrir em nova aba

Logo na navbar e footer **não** linka para `/` (página que pode não existir no guarda-chuva). Linka para a **home oficial da marca naquela região**, abrindo em nova aba para não interromper a LP.

```html
<!-- Header -->
<a href="{home-da-regiao}" class="navbar__logo" target="_blank" rel="noopener" aria-label="{Marca}: página inicial">
  <img src="../../brand/{marca}/assets/logos/logo-primary.svg" alt="" ...>
</a>

<!-- Footer -->
<a href="{home-da-regiao}" class="footer__logo" target="_blank" rel="noopener" aria-label="{Marca}: página inicial">
  <img src="../../brand/{marca}/assets/logos/logo-reversed.svg" alt="" ...>
</a>
```

**Regras:**

- `{home-da-regiao}` vem de `brand/{marca}/brand-manifest.json#regions.{regiao}.home`. Nunca hardcodar URL no HTML.
- `target="_blank" rel="noopener"` sempre (segurança contra `window.opener` + UX: usuário não perde o scroll/form preenchido).
- `aria-label` localizado por idioma (`página inicial` em PT, `página principal` em ES).

**Por que não `href="/"`:** em guarda-chuva (`material.buzzmonitor.com/mcp`), `/` resolve para a raiz do domínio onde **não existe LP**. Logo vira link quebrado. Em solo com domínio próprio (`webinar.buzzmonitor.com`), `/` resolve para a própria LP — auto-link que não acrescenta nada. Em ambos os casos, a home da marca é o destino correto.

## 18. OG image — 1200×630 com namespace por slug em guarda-chuva

Cada LP **tem que ter** uma OG image dedicada (1200×630 px, PNG ou JPG, idealmente < 600 KB). Sem isso, preview no WhatsApp/LinkedIn/X usa fallback inconsistente (primeira imagem encontrada, geralmente o logo do navbar minúsculo).

**Geração:** template HTML 1200×630 com brand tokens + headline localizado, renderizar com Chrome headless:

```bash
chrome --headless=new --disable-gpu --hide-scrollbars \
  --window-size=1200,630 --virtual-time-budget=4000 \
  --screenshot="og-{slug}.png" \
  "file:///path/to/og-template.html?lang={br|es|pt}"
```

**Convenção de path no source (repo) — nome único, sufixo de slug:**

```
landing-pages/{marca}/{slug}/assets/og-{slug}.png
```

⛔ **Nunca gere `og-image.png`.** O nome do arquivo no source é `og-{slug}.png` e mais nada — um arquivo por LP, mesmo nome no source e no deploy, zero rename. Gerar as duas cópias (`og-image.png` + `og-{slug}.png`) é o anti-padrão que encheu o repo de 31 duplicatas byte-a-byte (~4,5 MB), removidas em 2026-08-05: o `build_umbrella.py` só resolve `og-{slug}.png`, então a cópia `og-image.png` nunca chegava ao deploy.

**Convenção de path no deploy:**

| Modo | Source HTML (`og:image content=`) | Path no deploy |
|---|---|---|
| **solo** | `https://{dominio}/assets/og-{slug}.png` | `{sibling}/assets/og-{slug}.png` |
| **guarda-chuva** | `https://{dominio}/assets/{marca}/og-{slug}.png` | `dist/assets/{marca}/og-{slug}.png` (resolvido pelo `build_umbrella.py`) |

Nos dois modos o arquivo mantém o nome do source. No guarda-chuva o `build_umbrella.py` (linha 53) resolve `{{OG_IMAGE_PATH}}` para `assets/{marca}/og-{slug}.png` e copia de `landing-pages/{marca}/{slug}/assets/og-{slug}.png` — se o source tiver outro nome, o build emite `asset referenciado inexistente` e a LP vai pro ar com `og:image` 404.

**Por que sufixo de slug:** sem ele, três LPs irmãs (`mcp`, `mcp-es`, `mcp-pt`) com o mesmo nome de arquivo colidem em `assets/{marca}/og-image.png` — o último deploy sobrescreve os anteriores e todas as 3 LPs ficam com a OG image errada. Histórico: 2026-05-18, sessão MCP material.buzzmonitor.com — convenção estabelecida.

**Exceção legítima — OG compartilhada entre LPs irmãs:** quando variantes de uma mesma LP reusam de propósito a mesma imagem (ex.: `banimento-whatsapp`, `-pt`, `-latam`, `-comercial` apontam todas pra `og-banimento-whatsapp.png`), referencie o arquivo da LP-mãe **por path literal** no `og:image` em vez do placeholder `{{OG_IMAGE_PATH}}`, e mantenha só uma cópia física — na pasta da LP que a referencia.

**Validação:**

```bash
# 1. Existe no source com o nome canônico
test -f "landing-pages/{marca}/{slug}/assets/og-{slug}.png" && echo OK

# 2. Nenhum og-image.png sobrando (tem que sair vazio)
ls landing-pages/{marca}/{slug}/assets/og-image.png 2>/dev/null && echo "ERRO: og-image.png é anti-padrão — renomeie para og-{slug}.png"

# 3. Dimensões corretas (1200×630)
python -c "from PIL import Image; im=Image.open('landing-pages/{marca}/{slug}/assets/og-{slug}.png'); print(im.size)"
# espera (1200, 630)

# 4. Pós-deploy: retorna 200
curl -I https://{dominio}/assets/{marca}/og-{slug}.png  # solo: /assets/og-{slug}.png
```

## 19. Logo do header/footer/OG — SVG com `<text>` vivo é PROIBIDO

Logo de marca em `<img src="...svg">` **tem que** renderizar a tipografia certa em qualquer navegador. SVG que usa `<text>` vivo (a fonte não está embutida) cai no fallback do browser — tipicamente **serifada** — e a logo sai errada (ex.: "BUZZ" sans + "CREATORS" serifada). O usuário percebe na hora.

**Validação obrigatória antes de usar qualquer logo SVG:**

```bash
grep -c '<text' brand/{marca}/assets/logos/{logo}.svg   # TEM que ser 0
```

- `> 0` → o SVG serifa no browser. **Não usar.** Alternativas, em ordem:
  1. **SVG raster** do mesmo logo (`grep -c base64 {logo}.svg` > 0) — fonte achatada na imagem, renderiza sempre certo. Mais pesado (100KB+) mas correto.
  2. **PNG** do logo (ex.: `logo-color.png`) — leve e correto, pode não ter todas as variantes (cor/branco/tagline).
  3. Converter o `<text>` em contornos (outline/paths) e re-exportar.
- `== 0` e sem base64 → vetor com paths (outline). OK usar.

**Estado por marca (2026-05-27):**
- **Buzzcreators:** TODOS os SVGs de wordmark do brand (`logo-color.svg`, `logo-full-color.svg`, `logo-white.svg`, `logo-vertical-*`) têm `<text>` vivo → serifam. Usar `logo-color.png` (354×50, sem tagline, no brand) **ou** o raster `logo-full-color.svg` que está no deploy (`/assets/buzzcreators/logo-full-color.svg`, ~115KB, com tagline). Footer escuro: `filter: brightness(0) invert(1)` no logo colorido.
- **Buzzmonitor:** SVGs de logo já são raster (base64) → OK.
- **Cxpress / Elife:** SVGs com paths (outline) → OK.

Histórico: 2026-05-27, LP `buzzcreators-estado-arte-influencia` publicada 2× com "CREATORS" serifada — a review (e o `lp-gerar`) trocaram o raster correto pelo "vetor limpo" sem checar o `<text>`. Referência viva correta: `evento.buzzmonitor.com/vendendo-com-creators`.

---

Este arquivo é vivo. Adicionar regra aqui sempre que um aprendizado novo vier de uma review.
