# LP Cxpress — custo-atendimento-manual

**Gerado em:** 2026-09-10
**Copy-fonte:** `copy.txt` (output de /lp-preparar)
**Destino:** `content.cxpress.io/custo-atendimento-manual` (guarda-chuva, dominio migrado pro CI)
**Anuncio de origem:** `[Ad07]` da campanha `[meta][fundo][conversao][smb][gatilhos]`
**Regiao:** brasil · `<html lang="pt-BR">` · GTM `GTM-T4XDWHL3`

## Estrutura

1. Hero (banda azul-marinho) — overline, H1 com a dor, sub, CTA + nota, linha de prova. Visual: mostrador de turno (donut com ~52% em amarelo) + Samir flutuando
2. Esteira de clientes (42 logos, marquee)
3. A conta — H2, intro, 6 tarefas em lista vertical com X vermelho, faixa de total em navy, fecho
4. O que a IA assume — H2, intro, grid de 6 cards com check verde
5. Case Cacau Show — logo, H2, 2 paragrafos, 3 numeros, pull-quote (literal da copy)
6. O que sobra pro time — secao de pausa (so H2 grande + 1 paragrafo, sem card e sem CTA)
7. Agendar — H2, kicker, explicacao, pilula de preco, requisito de site, formulario mock
8. Fecho (banda azul-marinho) — frase-ancora + CTA + Samir
9. Footer

Contagem de blocos bate 1:1 com a copy (GUIDELINES §9): 6 tarefas, 6 cards, 3 numeros de case, 6 campos de formulario.

## Estado

- [x] HTML gerado
- [ ] OG image 1200×630 → `assets/og-custo-atendimento-manual.png` (arquivo **unico** — nunca tambem `og-image.png`).
      Gerar com o template `.claude/skills/lp-gerar/og-template.html` + Chrome headless antes de publicar.
- [ ] Revisao (frontend-design review + web-design-guidelines) — rodar `/lp-revisar cxpress/custo-atendimento-manual`
- [ ] Formulario integrado — rodar `/lp-integrar-form cxpress/custo-atendimento-manual "<script type=\"text/javascript\" src=\"https://form.jotform.com/jsform/261045149477663\"></script>"`
      (Jotform obrigatorio das LPs de midia paga da Cxpress BR: "CXPRESS BR | MKT | LPs - Proposta | META ADS")
- [ ] Publicado — rodar `/lp-publicar cxpress custo-atendimento-manual content.cxpress.io`

⚠️ **A publicacao precisa de worktree a partir de `origin/main`.** O manifest do
`content.cxpress.io` tem 69 LPs na main e 66 nesta base local — editar o manifest aqui
apagaria 3 LPs que estao no ar.

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (header e footer; `<text>` vivo = 0, web-safe por §19)
- `../../brand/cxpress/assets/mascot/samir-laptop.png` (hero)
- `../../brand/cxpress/assets/mascot/samir-joinha.png` (fecho)
- `./assets/logo-cacau-show.png`
- `./assets/clientes/cliente-01.png` … `cliente-42.png`

## Validacoes rodadas

| Checagem | Resultado |
|---|---|
| em-dash / `&mdash;` | 0 / 0 |
| `meta name="description"` | 1 |
| `meta property="og:` | 10 |
| `meta name="twitter:` | 4 |
| JSON-LD | 1 bloco, parseia como JSON valido |
| GTM `GTM-T4XDWHL3` | script no `<head>` + noscript apos `<body>` |
| Formulario | mock (`action="#"`), conforme §11 |
| `href="/"` em logo | 0 (aponta pra `https://home.cxpress.io`, target `_blank`) |
| `<img>` sem `alt` | 0 |
| Paths de asset quebrados | 0 |
| `bump_mobile_type.py --dry-run` | 0 clamps a corrigir |
| Overflow horizontal a 375px | nenhum (`scrollWidth == clientWidth`); a esteira de logos e mais larga por design, dentro de `overflow:hidden` |
| Overflow horizontal a 1265px | nenhum |
| Pisos de tipo mobile (§20) | H1 34 · lead 18 · H2 28 · card H3 22 · corpo 17 · label 14 |

`check_mobile_type.py` **nao rodou**: o Playwright desta maquina esta quebrado
(`ImportError: DLL load failed while importing _greenlet`). A medicao acima foi feita
com JS no painel do navegador, no mesmo viewport de 375×812.

## Auditoria de fidelidade da copy

Diff programatico entre os textos visiveis do HTML e o `copy.txt`. Tudo que ficou fora da
copy e whitelist declarada da `lp-gerar` (Passo 3), com uma excecao anotada:

| Texto fora do copy.txt | Classificacao |
|---|---|
| "Pular para o conteudo" | skip-link (a11y, whitelist 5) |
| Nav: "A conta", "O que a IA assume", "Case" | nav meta minimal — os tres vem dos proprios rotulos de secao do `copy.txt` |
| "Marcas que atendem com a Cxpress" | **excecao anotada** — ver abaixo |
| "Selecione", faixas de investimento, faixas de time | labels e opcoes de formulario (whitelist 3) |
| "Nao desejo receber a newsletter e as novidades da Cxpress" | opt-out de compliance (whitelist 3), igual ao campo do Jotform |

Zero pull-quote inventado, zero kicker novo, zero tag rotacionada com texto proprio, zero
punchline de marketing ("sem spam", "vagas limitadas" e afins). A frase-ancora do fecho
("As quatro horas de amanha ja estao na fila de hoje.") esta integral, sem encurtamento.

**Excecao: esteira de clientes.** O `copy.txt` nao pede a secao. Ela entrou porque e
componente padronizado das LPs Cxpress (commit `f7472e5`, "Padronizar a esteira de
clientes das 5 LPs pelo modelo da chatbot-whatsapp") e esta LP e destino de midia paga
como as outras. O rotulo e o mesmo da `atendimento-domingo`. Se a revisao preferir
fidelidade estrita ao §9, e uma remocao de um bloco.

**Normalizacao cosmetica aplicada:** os itens que a copy escreve com separador `·`
("Triagem manual · cerca de 45 minutos", "8h para 26 min · SLA de primeira resposta",
"R$ 1.750 · planos a partir de / mes") foram divididos em dois elementos visuais, e o `·`
saiu como glifo. Os dois lados ficaram literais. Mesmo padrao do bloco `.nums` da
`atendimento-domingo`.

## Decisoes de layout que valem revisar

1. **CTA do header escondido abaixo de 760px.** "Agendar demonstracao gratuita" nao cabe
   ao lado da logo em tela estreita, e encurtar o texto violaria a fidelidade da copy. O
   hero, o fecho e o formulario mantem o mesmo CTA, e o §3 (CTA visivel sem scroll) segue
   atendido pelo hero. Se o time quiser CTA fixo tambem no mobile, o caminho e aprovar um
   rotulo curto na copy, nao truncar aqui.
2. **Visual do hero = mostrador de turno.** Donut com 52% preenchido (4h10 de um turno de
   8h) e, embaixo, o LABEL literal da secao "A conta". Foi a forma de ter um elemento
   visual forte (§3) sem inventar texto: a unica frase do painel ja existe na copy. O
   `aria-label` do SVG descreve a proporcao; o significado numerico fica no texto.
3. **Case sem os subtitulos "Contexto" e "Solucao".** A `atendimento-domingo` tem esses
   dois H3, mas eles nao estao neste `copy.txt` — entao os dois paragrafos ficaram em duas
   colunas sem cabecalho.
4. **`brand-manifest.json` da Cxpress ainda esta no formato antigo** (`websites`, sem o
   bloco `regions` nem `socials`). O JSON-LD reusa `https://home.cxpress.io` mais o
   LinkedIn e o Instagram que a `atendimento-domingo` ja publicou. O manifest da marca
   precisa migrar pro formato `regions` pra `lp-gerar` parar de degradar aqui.

## Pendencias herdadas do copy.txt

Continuam valendo (estao no rodape do `copy.txt`):

1. Os tempos das seis tarefas vem da arte do `[Ad07]`, com "~" de aproximado, e estao
   rotulados como **estimativa** de proposito — nao ha case verificado que os meca
   (`conhecimento/produto/cxpress/cases.md`). Se o time de produto tiver a fonte, trocar o
   rotulo e citar.
2. Case Cacau Show e os numeros "8h para 26 min" e "34%": autorizados nominalmente pela
   Marielle a partir do PDF "Case Cacau Show & Elife".
3. Preco R$ 1.750 confirmado pela Marielle em 10/09/2026.
