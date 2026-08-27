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
- **§11 formulário:** era mock nesta passada; o embed real (Jotform `261034073026647`) entrou depois, via `/lp-integrar-form`.
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

---

# Revisão 2 — alterações de copy pedidas pelo Victor (2026-08-27)

**Escopo:** 4 alterações de copy solicitadas no chat, aplicadas em `copy.txt` (fonte-verdade) e no `index.html`, seguidas das auditorias determinísticas.

## Aplicado

| # | Pedido | O que mudou |
|---|---|---|
| 1 | "basic embaixo pode colocar valor de licença adicional R$ 120,00" | nova linha ao pé do card Basic, em pílula lilás: "Acesso adicional de operador humano: R$ 120,00 por mês." (`.pk-addon`, 17px, navy sobre `#D7E2FF` ≈10:1) |
| 2 | tirar "em pacotes de até 5 mil ligações mensais" do Voice Agent | removido nos 2 lugares: card Enterprise ("Voice Agent: a IA de telefonia") e linha da tabela comparativa ("Voice Agent, IA de telefonia"). Zero ocorrências de "5 mil" restantes |
| 3 | nova frase principal do hero | subtítulo do hero trocado por "Centralize seus canais, organize toda a operação e potencialize o atendimento com inteligência artificial. Escolha o modelo mais adequado ao momento e aos objetivos da sua empresa." |
| 4 | título e texto da segunda seção | H2 virou "Duas formas de contratar. / Uma plataforma completa." (quebra entre as duas frases, a segunda em navy bold como destaque) e o subtítulo virou "Comece com o Basic, utilizando toda a tecnologia da Cxpress com sua própria equipe, ou escolha o Enterprise para uma solução personalizada, combinando canais, agentes de IA e especialistas dedicados à sua operação." |

**Leitura registrada:** "frase principal" foi aplicada como o **subtítulo** do hero, não como o H1. O texto tem duas frases descritivas e não caberia num H1 de 64px; o H1 segue "O plano certo para o seu atendimento". Trocar é uma linha, se a intenção era o H1.

**Nota de escopo:** o item 1 reverte, por decisão explícita do Victor, a escolha anterior de manter os preços unitários dos incrementos fora da página. Só o acesso de operador (R$ 120,00) entrou; os demais incrementos seguem sem preço, porque o Enterprise é sob demanda.

## Auditorias após a alteração (todas passaram, 0 críticos)

| Gate | Resultado |
|---|---|
| `check_gtm_region.py` | `status: ok`, `GTM-T4XDWHL3`, região brasil, `stamp_match: true` |
| em-dash (§5 / anti-IA) | 0 no HTML, 0 no `copy.txt` |
| SEO (§15) | description 1, robots 1, og 10, twitter 4, JSON-LD 1, canonical 1 |
| JSON-LD | parseia; `Organization` + `WebPage` + `SoftwareApplication`; `Organization.url` = `https://home.cxpress.io` (bate com o brand-manifest) |
| Logo regional (§17) | 0 ocorrências de `href="/"` |
| OG image (§18) | `og-planos.png` 1200×630, sem `og-image.png` duplicado |
| Tipografia mobile (§20) | `bump_mobile_type.py` dry-run limpo (0 regras a subir) |
| Overflow a 375px | só o `.skip-link` em `left:-9999px` (fora de tela por construção) |
| Fidelidade de copy | os 4 textos novos aparecem literais, 1× cada. Nenhum texto inventado |

## Melhorias opcionais desta passada

Todas do mesmo tema: agora que o preço do acesso adicional é público, há 3 lugares que falam de acesso extra sem citá-lo. Nenhuma é erro, só coerência.

- [ ] **Nota ao pé da seção de planos** diz "Acessos, canais, agentes de IA e serviços adicionais são cotados junto com o time comercial". Não contradiz (R$ 120 é preço de tabela), mas se quiser blindar, basta tirar "Acessos," dessa lista.
- [ ] **FAQ "O que conta como acesso de operador?"** diz que acessos adicionais "entram como incremento", sem o valor. Poderia citar os R$ 120,00.
- [ ] **Linha da tabela "Acessos de operador humano"** mostra "5 incluídos" no Basic. Poderia mostrar "5 incluídos (+R$ 120/acesso)".
