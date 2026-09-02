# LP Cxpress — cxpress-na-pratica

**Gerado em:** 2026-09-02
**Copy-fonte:** `copy.txt` (escrita nesta sessão a partir do briefing de Brand Performance, não veio de `/lp-preparar`)
**Região:** brasil (PT-BR) · **GTM:** `GTM-T4XDWHL3` (`brand/cxpress/tracking.json` → `regions.brasil`)
**Domínio sugerido:** `content.cxpress.io` (guarda-chuva migrado pro CI — ver `landing-pages/dominios/MIGRADOS.json`)

## Contexto da campanha

Tráfego de YouTube (Brand Performance), vindo de vídeos longos e educativos sobre CX, retenção e churn.
Lead morno/quente (MoFu-BoFu): já reconhece a dor, precisa de filtro de fit. O formulário é o filtro
(e-mail corporativo + cargo + tamanho da equipe de atendimento), reforçado pela seção "Para quem essa
conversa faz sentido", que declara explicitamente quando ainda não é a hora.

## Estrutura

1. Header (logo + CTA âncora)
2. Hero — overline, H1 (dor), subheadline, **formulário na primeira dobra**
3. Problema — lista vertical, 5 itens, X vermelho (§8)
4. Benefícios — grid de 3 cards, check verde (§8) — tempo, centralização, experiência do cliente
5. Para quem — 2 colunas ("Faz sentido se" 3 itens · "Ainda não é a hora se" 2 itens)
6. CTA final — única seção escura (navy), Samir + H2 + botão que rola até o form
7. Footer

## Decisões que fogem do default (justificar em review)

- **Formulário na 1ª dobra, não na última.** GUIDELINES §10 manda form na 4ª/última seção para
  tráfego MoFu/BoFu. Override **pedido explicitamente pelo Victor** nesta sessão. §10 permite o
  override quando o briefing pede. O CTA final continua existindo e ancora de volta no `#form`.
- **Sem prova social / cases.** O `BRANDBOOK.md` da Cxpress registra "não inventar cases, aguardar
  validação interna". Quando houver case verificado, cabe uma seção entre Benefícios e Para quem.
- **H1 com 37% de desequilíbrio de linha (§21).** É o piso do algoritmo: `text-wrap: balance` converge
  em 3 linhas (475/360/571 px) independente da largura da coluna e do tamanho da fonte, porque
  "história do seu cliente" é a menor linha máxima possível. Não há órfã, as 3 linhas têm 3+ palavras.
  Só muda com mudança de copy do H1.
- **Mascote otimizado como asset local.** `brand/cxpress/assets/mascot/samir-laptop.png` tem 2,1 MB
  (1536×1024). A LP usa uma cópia reduzida e quantizada em `./assets/samir-laptop.png` (880×587, 59 KB).

## Pendência de brand (fora do escopo desta LP)

`brand/cxpress/brand-manifest.json` ainda usa o formato antigo `websites` em vez de `regions`.
Consequência: o JSON-LD saiu com `Organization` **sem `sameAs`** (não há `regions.{regiao}.instagram`
nem `socials.linkedin` no manifest) e a home regional foi lida de `websites.brasil`.
Migrar o manifest para o formato `regions` e rodar `/lp-revisar` para completar o `sameAs`.

## Validação já executada

| Item | Resultado |
|---|---|
| Em-dash / `&mdash;` (§5, anti-IA) | 0 / 0 |
| GTM head + noscript, ID da região | 1 / 1, `GTM-T4XDWHL3` |
| SEO: canonical · description · robots · favicon | 1 · 1 · 1 · 1 |
| Open Graph / Twitter / JSON-LD | 10 / 4 / 1 (JSON-LD parseia, 3 nós) |
| hreflang | ausente por decisão (LP única, sem irmãs) |
| Logo header/footer para home regional (§17) | 2, `target="_blank" rel="noopener"` |
| Logo SVG com `<text>` vivo (§19) | 0 nos 3 SVGs da Cxpress |
| Form em mock (§11) | `action="#" onsubmit="event.preventDefault()"` |
| Contagens da copy (§9) | problema 5 · benefícios 3 · para quem 3+2 · campos 4 |
| Fidelidade da copy | 0 textos inventados, 0 linhas ausentes |
| Pisos tipográficos mobile (§20) | H1 34 · H2 28 · H3 22 · corpo/botão 17 · label 15 · caption 14 |
| Overflow horizontal em 390px | nenhum (`scrollWidth` = `clientWidth` = 390) |
| Desequilíbrio de linha (§21, 1440px) | todos ≤ 24%, exceto H1 (37%, piso do algoritmo) |

## Estado

- [x] HTML gerado
- [ ] OG image 1200×630 → `assets/og-cxpress-na-pratica.png` (arquivo **único** — nunca também `og-image.png`).
      Template em `.claude/skills/lp-gerar/og-template.html` + Chrome headless.
- [ ] Revisão — rodar `/lp-revisar cxpress/cxpress-na-pratica`
- [ ] Formulário integrado — rodar `/lp-integrar-form cxpress/cxpress-na-pratica "snippet"`
- [ ] Publicado — rodar `/lp-publicar cxpress cxpress-na-pratica content.cxpress.io`

## Assets referenciados

| Path no source | Uso |
|---|---|
| `../../brand/cxpress/assets/logos/logo-primary.svg` | logo do header |
| `../../brand/cxpress/assets/logos/logo-reversed.svg` | logo do footer (fundo navy) |
| `../../brand/cxpress/assets/logos/logo-icon.png` | favicon (§12) |
| `./assets/samir-laptop.png` | mascote Samir na seção de CTA final |

## Paleta usada (§1)

`#232960` navy (texto, seção escura) · `#4A69BD` royal (CTA primário, foco de input) ·
`#EF863C` laranja (régua do hero, botão de conversão, outline decorativo).
Apoio: `#D7E2FF` lilás (pílulas e arco), `#FFDCC3` pêssego (pílula), `#f5f5f5` (alternância de fundo).
Semânticos de seção-tipo: `#dc2626` (X do problema), `#16a34a` (check dos benefícios).
Zero gradiente.
