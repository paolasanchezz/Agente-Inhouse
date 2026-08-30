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
