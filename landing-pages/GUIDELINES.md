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

- Padrão de referência: **fundo branco (ou neutral-100)**, texto à esquerda, elemento visual clean à direita. Gradientes full-bleed coloridos só quando o briefing pedir impacto máximo — senão, preferir limpeza.
- Título principal no peso mais pesado da display font. Subtítulo em peso leve para contraste tipográfico.
- Elemento da direita: **um** elemento forte (card de data, ilustração minimalista, foto com crop editorial). Não encher de formas.
- CTA primário visível sem scroll. CTA secundário (opcional) ghost ao lado.
- Indicador de data/formato no header (ex.: "Webinar gratuito", dot pulsante): texto curto e **sempre em uma única linha** (`white-space: nowrap`). Nunca duplicar info que já aparece em outro lugar do hero — o indicador é um resumo discreto, não um repositório de dados. Se a tela for estreita demais para a linha única, preferir esconder via `@media` a quebrar em duas linhas.

## 4. Animação

- Motion serve ao conteúdo, não o esconde. Reveals com `opacity: 0 → 1` precisam de fallback caso a animação não dispare (ex.: `@supports` ou prefers-reduced-motion).
- **Nunca** deixar texto essencial invisível esperando animação. Se a animação falhar por qualquer motivo (lentidão, bug, extensão do browser), o texto deve aparecer.
- Usar motion em 2-3 momentos-chave: entrada do hero, scroll-reveal de cards, hover de CTA. Basta.

## 5. Copy

- Respeitar copy do briefing/Notion — ajustes cosméticos ok, mas não reescrever tom.
- Usar aspas curvas (`&ldquo; &rdquo;`), ellipsis (`&hellip;`) e em-dash (`&mdash;`) corretos.
- Números em algarismos (23 de Abril, não "vinte e três").

## 6. Estrutura mínima

Toda LP tem: **Hero → Problema/contexto → Oferta/Programa → Diferencial → Para quem → Prova (speakers/social proof) → Urgência → CTA final com formulário → Footer.** Pode cortar seções, mas não inverter a ordem narrativa.

## 7. Acessibilidade (non-negotiable)

Seguir [Vercel Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md) — ver skill `web-design-guidelines`. Em especial: skip-link, focus-visible, labels em todos os inputs, `alt`/`aria-hidden` em imagens, `prefers-reduced-motion`.

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

## 10. Integração tardia de formulário

Formulário real (Jotform, RD Station, HubSpot embed) **só entra depois do design aprovado**. Durante toda a fase de design e revisão, usar mock:

```html
<form class="form" action="#" method="post" onsubmit="event.preventDefault()">
  <!-- inputs mock -->
</form>
```

Razão: embeds externos atrapalham iteração de design (iframe lento, CSS de terceiros, altura dinâmica) e obrigam retrabalho a cada ajuste de layout. Integrar via skill `lp-integrar-form` só quando o layout está travado.

Wrapper para embed (quando chegar a hora):

```css
.form.jotform-embed { padding: 16px; overflow: hidden; }
.form.jotform-embed iframe { width: 100% !important; max-width: 100% !important; border: 0; display: block; }
```

Logo em hero/CTA: **pode ser grande se for transparente** (SVG com fundo transparente). PNG com fundo branco fica pequeno ou vira "adesivo". Regra: logo respira se o formato permite.

---

Este arquivo é vivo. Adicionar regra aqui sempre que um aprendizado novo vier de uma review.
