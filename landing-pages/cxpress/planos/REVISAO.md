# Revisão — cxpress/planos

**Data:** 2026-08-27
**Escopo:** auditoria de design, acessibilidade e fidelidade de copy sobre o HTML gerado.

## Críticos aplicados

| # | Achado | Correção |
|---|---|---|
| 1 | Em-dash em comentário do JS (`grep -c "—"` retornava 1). Tolerância zero, `regras-anti-ia.md` | trocado por dois-pontos. Contagem final: 0 |
| 2 | `.pk-tag` (pílula "Mais contratado" / "Sob demanda") a 13px, abaixo do piso de 14px para label (GUIDELINES §20) | subido para 14px. `check_mobile_type` agora reporta `min=14` |
| 3 | Pisos de tipografia mobile abaixo do especificado em 11 regras (`.cxp-submit` 16px, `.k2x-block a` 16px, `.k2x-sub` 16px, `.skip-link` 16px, labels 14px etc.) | `bump_mobile_type.py` aplicado (só mobile; desktop intacto) |
| 4 | Preço do Enterprise quebrava em duas linhas com pesos diferentes ("Precificação" grande + "sob demanda" pequeno), invertendo a ênfase da frase | frase única em 28px, literal da copy: "Precificação sob demanda" |
| 5 | `:focus-visible` com outline navy `#232960` ficava quase invisível sobre o card Enterprise, a seção do formulário e o footer (todos escuros) | outline branco nesses três contextos |
| 6 | Faixa de canais do hero usava `role="list"` num `<div>` e `role="listitem"` em `<img>`, o que sobrescreve a semântica de imagem | trocado por `<ul>`/`<li>` real |
| 7 | Perguntas do FAQ estavam em `<span>`, mas a copy as rotula como `H3` (perdia navegação por headings em leitor de tela) | `<summary><h3>…</h3></summary>`, com `font:inherit` para não mudar o visual |
| 8 | Tabela comparativa sem `<caption>` | `<caption class="sr-only">` descrevendo o comparativo |
| 9 | **Logo e pílula "Planos Cxpress" desalinhados no hero** (reportado pelo Victor, 2026-08-27). `.pk-hero-logo` era `inline-block` e `.pk-overline` também, então os dois caíam na mesma linha do fluxo inline e o *par* é que ficava centralizado: logo à esquerda do eixo, pílula à direita | `.pk-hero-logo` virou `display:block` com `width` igual à da imagem e `margin:0 auto`, para ocupar a própria linha. A largura do bloco também foi acertada no `@media (max-width:600px)` (170px), senão o logo menor ficaria encostado à esquerda de uma caixa de 200px |

## Verificado e conforme

- **Fidelidade de copy (§9 e regra de fidelidade do `lp-gerar`):** todo texto visível vem literal
  de `copy.txt`. Fora dela, só o que a whitelist permite: labels do form (`Nome`, `E-mail
  corporativo`, `Telefone`, `Empresa`, `Pessoas no atendimento`, opções de faixa), o disclaimer
  de compliance, os cabeçalhos funcionais da tabela (`Recurso`, `Basic`, `Enterprise`), o
  skip-link, o `caption` e os `aria-label`. Nenhum pull-quote, kicker, tag rotacionada ou
  punchline inventada.
- **Contagem de blocos = contagem da copy:** 2 planos, 7 grupos na tabela, 6 perguntas no FAQ,
  3 bullets na seção do form. Nada arredondado para "ficar bonito".
- **§8 seções-tipo:** itens inclusos usam o check verde do brand; "não incluído" usa traço
  neutro em CSS (não o em-dash de texto) com `sr-only` "Não incluído".
- **§7 contraste:** texto sobre o lilás `#D7E2FF` usa navy `#232960` (≈10:1), nunca o royal.
  Branco sobre royal `#4A69BD` dá ≈5,2:1.
- **§11 formulário:** mock (`action="#"` + `onsubmit="event.preventDefault()"`), sem embed.
- **§10 posicionamento do form:** página BoFu, form na última seção, com CTA no hero rolando
  até lá.
- **§12 favicon:** um único link, PNG do brand.
- **§15 SEO:** description única, 10 `og:`, 4 `twitter:`, JSON-LD (Organization + WebPage +
  SoftwareApplication com AggregateOffer `lowPrice: 1290 BRL`) parseando.
- **§18 OG image:** `assets/og-planos.png`, 1200×630, 353 KB, sem `og-image.png` duplicado.
- **§4 animação:** reveal com dois caminhos idempotentes (IntersectionObserver + checador de
  scroll), `<noscript>` forçando `opacity:1` e bloco `prefers-reduced-motion`.
- **§16 hreflang:** não se aplica, LP única (sem irmã `-pt`/`-es`).
- **GTM:** `GTM-T4XDWHL3` (brasil) nos dois blocos; `check_gtm_region.py` = 1 OK, 0 bloqueios.

## Opcionais (não aplicados)

1. **Alturas dos dois cards de plano não se igualam** no desktop, porque o Basic lista mais
   itens. Igualar exigiria `align-items: stretch` com scroll interno ou cortar itens, e cortar
   item de plano é pior que a assimetria. Fica como está.
2. **Faixa de canais do hero sem rótulo.** Um texto tipo "canais no mesmo painel" ajudaria a
   leitura, mas não existe na copy e a whitelist não cobre. Se quiserem, é uma linha nova em
   `copy.txt` e um `/lp-gerar`.
3. **Mascote Samir** não entrou (a `institucional` também não usa). Cabe bem ao lado do bloco
   do formulário, se quiserem calor visual na última dobra.
4. **Sem seção de urgência** (§8). Deliberado: página de pricing perene não tem escassez real.
