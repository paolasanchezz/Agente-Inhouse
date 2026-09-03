# Revisão — cxpress/banimento-de-whatsapp

**Data:** 2026-08-30
**Escopo:** LP nova. Design + acessibilidade + fidelidade de copy, medidos no navegador (Chromium 148, 1440×900 e 375×812).

---

## Críticos aplicados

| # | Achado | Correção |
|---|---|---|
| 1 | **Texto de item flex quebrando em coluna estreita.** Nos 7 recursos da seção API OFICIAL a frase quebrava palavra a palavra dentro da pílula e vazava do card. Causa: `text-wrap:balance` num item flex sem base de largura encolhe até `min-content`. | `.sinal .t, .recurso .t, .col li .t { flex:1 1 0; min-width:0 }` |
| 2 | **Ícone virando elipse verde atrás do texto.** `.recurso span` pegava também o `<span class="t">` do texto, aplicando `background:var(--wa)` e `border-radius:50%` nele. | Seletor escopado para `.recurso > span:not(.t)` |
| 3 | **`text-wrap` não agia no texto dos itens.** O texto de `.sinal`, `.recurso` e `.col li` era caixa anônima de flex, e `text-wrap` pertence ao bloco que forma as linhas (GUIDELINES §21, ressalva 3). | Texto envolvido em `<span class="t">` e os seletores de `balance` apontados para o span |
| 4 | **Contraste de elemento gráfico abaixo de 3:1.** O ✓ solto (`--wa-dark` #1AAE63) dava 2,89:1 em branco e 2,60:1 sobre o tint, reprovando o mínimo de WCAG 1.4.11. | Token novo `--wa-ink:#15884D` (4,51:1 em branco / 4,06:1 no tint) para os 5 glifos soltos. O `--wa-dark` continua só em fundo de hover |
| 5 | **Texto de apoio no limite do contraste.** `--text-muted` #6a7085 dava 4,43:1 sobre o tint, abaixo dos 4,5:1 de AA. | `--text-muted` → `#5d6275` (6,05:1 branco / 5,45:1 tint) |
| 6 | **Em-dash em comentário do HTML.** Tolerância zero (GUIDELINES §5). | Trocado por parênteses. `grep -c "—"` = 0 |
| 7 | **H1 do hero em 5 linhas com 38% de desequilíbrio.** Em 48px o `balance` do Chrome não fechava. | Teto para 44px + coluna de texto de 1.02fr para 1.12fr. Agora 4 linhas, com a linha mais longa em 570px de 612 disponíveis (o mínimo possível: "atendimento" sozinha já ocupa 285px) |
| 8 | **`.hero__sub` com órfã de 200px na última linha** (61% de desequilíbrio) usando `pretty`. | Movido para `balance` (bloco de 4 linhas, GUIDELINES §21). Caiu para 16% |
| 9 | **H2 da seção IA em 3 linhas crescentes** (41%). | Teto próprio de 36px nessa coluna. Agora 2 linhas com 1% |
| 10 | **✓ centralizado verticalmente em título de 2 linhas** nos passos 01 e 03 da seção COMO EVITAR, flutuando entre as linhas. | `align-items:flex-start` + `margin-top:4px` no SVG |
| 11 | **CTA da navbar em 13px no mobile**, abaixo do piso de 14px (GUIDELINES §20). | 14px. Sem overflow em 375px |

## Fidelidade de copy (auditoria do Passo 4.2 da `lp-gerar`)

Diff entre os textos visíveis do HTML e o `copy.txt`: **100 strings visíveis, 6 fora da copy, todas na whitelist** e nenhuma violação.

| String | Whitelist |
|---|---|
| "Pular para o conteúdo" | skip link (item 5) |
| "Agendar demo" | nav meta minimal, 2 palavras (item 1) |
| "Nome" / "E-mail corporativo" / "Site da empresa" | labels de form (item 3) |
| "Ao enviar, você aceita receber comunicações da Cxpress." | disclaimer de compliance (item 3) |

Dois textos inventados foram apanhados na geração e corrigidos antes do commit:

- As tags do hero traziam "Conta banida" e "Operação na Cxpress", que não existem na copy. Trocadas pelos rótulos literais da seção COMPARATIVO: **"Operação convencional"** e **"Com a Cxpress"** (mapeiam exatamente nos dois lados da composição).
- O nó do diagrama trazia um `<small>` com "Uma única fila". Removido; o nó ficou só com a logo.

Contagens: em-dash 0 · `&mdash;` 0 · antítese-por-negação 0 · exclamações 1 (H1 do hero, veio do doc) · perguntas retóricas 1 por seção.

## Decisões de estrutura

- **Formulário na última seção.** GUIDELINES §10 manda MoFu/BoFu no fim, e o doc pede explicitamente ("jogar o formulário lá pra baixo, e todo botão/cta redirecionar para" ele). Os 5 CTAs da página apontam para `#agendar`.
- **Sem PROVA e sem QUEM SOMOS.** Decisão do Victor (2026-08-30): seguir só o doc. As duas seções existem na LP irmã `/evite-banimento-whatsapp` e ficaram de fora aqui.
- **Uma só seção dark** (FECHO), alternância branco ↔ tint no resto (GUIDELINES §1 e §2).
- **Gramática visual por tipo de seção** (§8): dor em lista vertical com X vermelho, benefício em grid/passos com ✓ verde, comparativo com as duas linguagens lado a lado.

## Opcionais (não aplicados)

| # | Sugestão | Por quê não entrou agora |
|---|---|---|
| 1 | Reincluir no FAQ a pergunta "A Cxpress consegue desbloquear minha conta?" com a resposta "Não" | Não está no doc, e a decisão foi seguir o doc. Mas a campanha compra keywords de quem já foi banido ("whatsapp banido", "mensagem de banimento"), então a ausência deixa margem para o visitante entender que a Cxpress desbloqueia contas. **Victor decidiu manter como o doc entrega** (2026-08-30) |
| 2 | Trocar "Use o WhatsApp **de forma profissional** com a API Oficial" por "como canal profissional" | "de forma X" é filler listado em `regras-anti-ia.md`. O título veio pronto do doc e carrega keyword, então ficou marcado como sugestão em `copy.txt` em vez de reescrito |
| 3 | ~~Confirmar GTM/GA4 e o ID do Jotform~~ | **Resolvido em 2026-08-30:** Victor confirmou o container de Ads (GTM-KN8BPFG + GA4 339689858) e o mesmo Jotform da irmã (`261034073026647`), já integrado |
| 4 | Painel do hero com legibilidade limitada | O `plataforma-canais.gif` roda a ~300px de largura, então a interface lê como "painel organizado", não como tela legível. É o papel dele na composição (o contraste com o celular banido é o argumento), mas se quiser a tela legível, cabe um crop dedicado do painel |

## Como validar

```bash
cd landing-pages && py -m http.server 8137 --bind 127.0.0.1
```

Depois abrir `http://127.0.0.1:8137/cxpress/banimento-de-whatsapp/index.html` (servindo a partir de `landing-pages/`, para o symlink `brand` resolver).

---

# Revisão de 2026-09-03 — as alterações de hoje

**Escopo:** o que mudou hoje (embed do Jotform na seção, listener anti-colisão, pulso do
botão flutuante, troca do ícone do card, `max-width` do H3 e do corpo do form).
**Auditores:** design contra `GUIDELINES.md` §1–21 + `web-design-guidelines` (Vercel Web
Interface Guidelines), com tudo medido no Chromium contra a página em produção (1440 e 390).

## Aplicado automaticamente (1 crítico)

| # | Achado | Correção |
|---|---|---|
| 1 | **8 em-dashes no HTML.** Tolerância zero (GUIDELINES §5 e `regras-anti-ia.md`). Um deles em **copy renderizada** (aviso de envio do pop-up, linha 1590); os outros 7 em comentários de CSS/JS. O item 6 da revisão de 2026-08-30 já tinha zerado esse grep: os 8 voltaram depois, no trabalho do botão flutuante (3) e nas alterações de hoje (4). As LPs irmãs `evite-banimento-whatsapp`, `whatsapp-business` e `planos` estão todas em 0. | Copy: a pausa forte virou ponto ("…numa nova aba. Se ela não abriu, toque aqui."). Comentários: vírgula, ponto e vírgula, dois-pontos ou parênteses conforme a função (tabela de `regras-anti-ia.md`). `grep -c "—"` = 0 |

## Melhorias opcionais (4)

- [ ] **Nome acessível do iframe do Jotform da seção** — o `jsform` cria o iframe com o nome
  interno do formulário como `title` ("CXPRESS BR | MKT | LPs - Proposta (V2)"), que é o que
  o leitor de tela anuncia. O iframe do pop-up tem título próprio em português. Cumpre o
  WCAG 4.1.2 (tem nome), mas o nome é administrativo. Fix: 3 linhas de script setando o
  `title` depois do load.
- [ ] **`.agendar h3` no mobile: 2 linhas com 43% de desequilíbrio** (160px + 280px), acima
  do que a §21 aceita. **Não é regressão de hoje** — medido com `max-width:34ch` (o valor
  anterior) e com `44ch` (o atual): resultado idêntico, porque em 390px quem limita é o card
  (340px), não o `max-width`. O `balance` já faz o melhor split possível; a alavanca da
  ressalva 4 da §21 (baixar o teto de fonte) não fecha em 1 linha nessa largura.
- [ ] **Botão flutuante cobre a borda direita dos campos.** Sendo `fixed`, ele passa por cima
  do formulário conforme a pessoa rola (em 390px ocupa x 322–374 e o form vai até 365) — e
  agora são campos de verdade, não mais o mock. Um `bottom` maior dentro da seção do form, ou
  esconder o FAB quando a seção estiver visível, resolveria.
- [ ] **Sem `<meta name="theme-color">`** (pré-existente).

## Nice-to-haves (1)

- [ ] **Loops decorativos infinitos** (pulso do FAB e o dot do overline do hero) começam
  sozinhos e passam de 5s, o que a WCAG 2.2.2 pede pausar. Os dois param sob
  `prefers-reduced-motion`, que é o remédio que a própria diretriz prevê para loop decorativo.

## Verificado e sem achado

| Item | Resultado |
|---|---|
| GTM (script determinístico) | `status=wrong`, mas `grandfathered=true` e selo batendo. É o container de Google Ads que o Victor escolheu em 2026-08-30. **Não mexer** |
| `hreflang` | Ausente e correto: não há LP irmã com o mesmo slug-base |
| Pacote SEO (§15) | description 1, robots 1, og 10, twitter 4, JSON-LD 1, canonical 1 |
| OG image (§18) | `og-banimento-de-whatsapp.png`, 1200×630, sem `og-image.png` órfão |
| Logo regional (§17) | Nenhum `href="/"` em navbar/footer |
| Âncora `#agendar` × navbar sticky | 0px do H2 coberto (197px no desktop, 145px no mobile, contra 77px de navbar) |
| Overflow horizontal do halo | 0 nas duas larguras |
| Equilíbrio §21 no desktop | `.agendar__body` 6%, `.agendar__req` 9%, card do impacto 1% |
| Motion | Só `transform`/`opacity`; nenhum `transition: all`; tudo dentro de `prefers-reduced-motion` |
| Toque e foco | `touch-action:manipulation` + `-webkit-tap-highlight-color` cobrem o FAB; `:focus-visible` global; FAB 58×58 (52×52 no mobile) |
| Ícone trocado | `aria-hidden="true"` no wrapper; varredura dos 47 SVGs da página não achou outro arco com raio menor que a corda |
