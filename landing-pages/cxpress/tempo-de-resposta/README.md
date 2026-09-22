# LP Cxpress — tempo-de-resposta

**Gerado em:** 2026-09-18
**Copy-fonte:** `copy.txt` (output de /lp-preparar) · [Notion](https://app.notion.com/p/3df3934026fd81188ea3f823b73d7c4c)
**Destino:** `content.cxpress.io/tempo-de-resposta` (guarda-chuva, dominio migrado pro CI)
**Regiao:** brasil · `<html lang="pt-BR">` · GTM `GTM-T4XDWHL3`

## Criativos que apontam pra ca

| Criativo | Angulo |
|---|---|
| `INST 01 - Gerente SLA` | gerente de atendimento, reducao de SLA com agente de IA |
| `INST 02 - Mesma equipe` | mesma equipe atendendo mais |
| `SMB 08 - Tempo de resposta` | 1h45 de espera, "e assim que voce perde clientes" |

Os outros dois do lote ja tinham destino: `SMB 09 - Planilha` vai pra `atendimento-digital`
e `FRIO 01 - WhatsApp banido` vai pra `banimento-whatsapp`.

## Estrutura

1. Hero (banda navy) — overline, H1 com o 1h45 em destaque, sub, CTA 1, nota e linha de prova. Visual: cartao da espera (balões sem texto + contador 1h45) mais Samir flutuando
2. Esteira de clientes (42 logos)
3. A conta da espera — H2, intro, 5 etapas em lista vertical com X vermelho, faixa de fecho em navy, CTA 2
4. O que a IA assume — H2, intro, grid 2x2 de 4 cards com check verde
5. Case Cacau Show — logo, H2, 2 paragrafos, 3 numeros, CTA 3
6. O que sobra pro time — secao de pausa (so H2 grande + 1 paragrafo)
7. Agendar — H2, kicker, explicacao, pilula de preco, requisito de site, formulario mock
8. Fecho (banda navy) — frase-ancora + CTA 4 + Samir
9. Footer

Contagem bate 1:1 com a copy (GUIDELINES §9): 5 etapas, 4 cards, 3 numeros de case, 6 campos de formulario.

## Os 4 CTAs de rolagem

| Secao | Texto | Destino |
|---|---|---|
| Hero | Encurtar o tempo de resposta | `#agendar` |
| A conta da espera | Ver isso na sua operacao | `#agendar` |
| Case | Quero esse tempo de resposta | `#agendar` |
| Fecho | Agendar demonstracao gratuita | `#agendar` |

Mais o CTA do header (`Agendar demonstracao gratuita`, escondido abaixo de 760px) e o botao
`Enviar` do formulario. Os tres primeiros usam verbo sobre a dor do leitor; so o ultimo fala
em agendar. Padrao de copy fechado com a Marielle em 18/09 a partir do benchmark de ASAAS,
RD Station, G4, Digisac e Salvy.

## Estado

- [x] HTML gerado
- [x] OG image 1200×630 → `assets/og-tempo-de-resposta.png` (192 KB)
- [ ] Revisao — rodar `/lp-revisar cxpress/tempo-de-resposta`
- [ ] Formulario integrado — `/lp-integrar-form cxpress/tempo-de-resposta "<script type=\"text/javascript\" src=\"https://form.jotform.com/jsform/261045149477663\"></script>"`
- [ ] Publicado — `/lp-publicar cxpress tempo-de-resposta content.cxpress.io`

⚠️ **A publicacao precisa de worktree a partir de `origin/main`.** O manifest do
`content.cxpress.io` tem mais LPs na main do que nesta base local, entao editar o manifest
daqui apagaria LPs que estao no ar.

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (header e footer; `<text>` = 0, web-safe por §19)
- `../../brand/cxpress/assets/mascot/samir-laptop.png` (hero)
- `../../brand/cxpress/assets/mascot/samir-joinha.png` (fecho)
- `./assets/logo-cacau-show.png`
- `./assets/clientes/cliente-01.png` … `cliente-42.png`
- `./assets/og-tempo-de-resposta.png`

## Validacoes rodadas

| Checagem | Resultado |
|---|---|
| em-dash / `&mdash;` | 0 / 0 |
| `meta name="description"` · robots · canonical | 1 · 1 · 1 |
| `meta property="og:` · `meta name="twitter:` | 10 · 4 |
| JSON-LD | 1 bloco, parseia como JSON valido |
| GTM | `check_gtm_region.py` → `status: ok`, selo `.tracking.lock` gravado |
| Formulario | mock (`action="#"`), conforme §11 |
| `href="/"` em logo | 0 (aponta pra `https://home.cxpress.io`, target `_blank`) |
| `<img>` sem `alt` | 0 |
| Paths de asset quebrados | 0 |
| `bump_mobile_type.py --dry-run` | 0 clamps a corrigir |
| Overflow horizontal a 375px | nenhum (`scrollWidth == clientWidth == 375`) |
| Overflow horizontal a 1265px | nenhum |
| Pisos de tipo mobile §20 | H1 34 · lead 18 · H2 28 · card H3 22 · corpo 17 |
| Anel de foco | navy no claro (10,4:1), amarelo nas bandas escuras (6,7:1) |
| OG image §18 | 1200×630, nome canonico, nenhum `og-image.png` orfao |

`check_mobile_type.py` **nao rodou**: o Playwright desta maquina segue quebrado
(`ImportError: DLL load failed while importing _greenlet`). A medicao foi feita por JS no
painel do navegador, no mesmo viewport de 375×812.

## Fidelidade da copy

Todo texto visivel vem literal do `copy.txt`, com duas excecoes declaradas, ambas as mesmas
da `custo-atendimento-manual`:

- **Esteira de clientes** ("Marcas que atendem com a Cxpress"): componente padronizado das LPs
  Cxpress (commit `f7472e5`), nao esta no `copy.txt`.
- **Nav, skip-link, placeholders e opcoes de formulario, opt-out de compliance**: whitelist
  declarada da `lp-gerar` (Passo 3). Os rotulos da nav vem dos proprios nomes de secao do `copy.txt`.

O cartao da espera no hero **nao tem texto inventado**: os balões sao formas decorativas
(`aria-hidden`) e o unico texto e o `1h45`, literal do H1. O `aria-label` do cartao descreve
a cena sem afirmar nada que nao esteja na copy.

## Pendencias herdadas do copy.txt

1. O **1h45** do H1 vem da cena do criativo `SMB 08` (print de WhatsApp, 19h04 as 20h49).
   E cena ilustrativa, nao metrica de mercado. Nao transformar em dado numa revisao futura.
2. Case Cacau Show (8h para 26 min, 34%, zero contratacoes): autorizados nominalmente pela
   Marielle a partir do PDF "Case Cacau Show & Elife". **Nao misturar** com os numeros do
   relatorio Sentinela em `conhecimento/produto/cxpress/cases.md`.
3. O **94%** do criativo `INST 01` nao entrou na LP. E derivado do 8h para 26 min e so se
   sustenta atribuido a Cacau Show. A LP usa o par 8h/26min com o dono do resultado ao lado.
4. Preco R$ 1.750 confirmado pela Marielle em 10/09/2026.
