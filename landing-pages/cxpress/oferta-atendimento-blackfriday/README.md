# LP Cxpress — oferta-atendimento-blackfriday

**Gerado em:** 2026-09-09
**Copy-fonte:** `copy.txt` (output de `/lp-preparar`)
**Clone estrutural de:** `landing-pages/cxpress/oferta-atendimento-metrica` (mesma família de "oferta pós-webinar" em `content.cxpress.io`), a pedido explícito do usuário.

## Estrutura

- Header (logo)
- Hero + formulário (kicker, H1, 2 parágrafos de recap/transição, oferta em 3 bullets, form mock, disclaimer)
- Impacto (H2 + 2 parágrafos)
- Card destacado (case Cacau Show — H2, H3, 2 parágrafos)
- Depois da virada (H2 + grid de 4 benefícios + fechamento + CTA)
- Footer

## Decisões tomadas (documentar para quem revisar)

- **Seção "Clientes" (prova social) não portada.** A LP de referência tem uma banda de logos de clientes que não está registrada no `copy.txt` dela nem foi pedida no `copy.txt` desta LP — e não existe asset de logos para a campanha Black Friday. Se quiser essa seção aqui, preciso do asset de imagem (banda de logos) e do texto do rótulo antes de adicionar.
- **Só 3 bullets na oferta do hero (não 4).** A LP de referência mistura um 4º bullet ("avaliação gratuita...") que na prática é uma paráfrase do parágrafo de abertura dela, fora do que o `copy.txt` dela mesma lista. Aqui segui os 3 `LIST ITEM` literais do `copy.txt` desta LP, sem adicionar um 4º item derivado.
- **Sem contador de validade ("condição válida por N dias").** A referência tem essa linha, mas o `copy.txt` desta LP não define um prazo real — não inventei um número. Se houver uma data/prazo real da oferta, me avise que eu adiciono.
- **Botão do form do hero usa o texto "Garantir oferta"**, reaproveitando literalmente o CTA que já existe no `copy.txt` (seção Depois da Virada), em vez de inventar um rótulo novo — mesmo texto nos dois pontos de conversão da página.
- **Campos do formulário mock:** Nome, E-mail de trabalho, Telefone, Nome da empresa (subconjunto do padrão de formulário da Cxpress documentado no BRANDBOOK). Trocar pelo embed real via `/lp-integrar-form`.
- **Manifest da marca sem bloco `regions`:** `brand/cxpress/brand-manifest.json` só tem `websites` (formato antigo). Usei `websites.brasil` para a home no header/footer/JSON-LD e omiti `sameAs` (LinkedIn/Instagram) no JSON-LD — mesma degradação que a LP de referência já tem. Migrar o manifest pro formato `regions` resolveria isso pra todas as LPs Cxpress de uma vez.

## Estado

- [x] HTML gerado
- [x] OG image 1200×630 → `assets/og-oferta-atendimento-blackfriday.png`
- [x] Revisão (`frontend-design` review + `web-design-guidelines`) — ver `REVISAO.md` (3 críticos aplicados: foco de teclado, piso tipográfico, OG image)
- [x] Formulário integrado — mesmo Jotform da LP de referência (`oferta-atendimento-metrica`)
- [ ] Publicado — rodar `/lp-publicar cxpress oferta-atendimento-blackfriday content.cxpress.io`

**Form provider:** Jotform (`261045149477663`), integrado em 2026-09-09 — mesmo formulário compartilhado usado em `oferta-atendimento-metrica`, a pedido do usuário. (Nota: o `README.md` da LP de referência cita um ID diferente, `261027639617663`, mas o `index.html` dela embeda `261045149477663` — segui o que está de fato embedado e ao vivo.)

## Validações já feitas

- em-dash / `&mdash;`: 0 ocorrências
- Tags Open Graph: 10 (mínimo 8) · Twitter: 4 (mínimo 4) · JSON-LD: 1 bloco, parseia válido
- GTM `GTM-T4XDWHL3` (região brasil) injetado no `<head>` e como `<noscript>` após `<body>`
- Logos usados (`logo-primary.svg`, `logo-reversed.svg`) validados sem `<text>` vivo (não serifa)
- Fidelidade de copy: texto visível extraído do HTML confere 1:1 com `copy.txt` (única adição fora da copy: labels de formulário e skip-link, ambos whitelist)

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)

## Como atualizar

```
/lp-publicar cxpress oferta-atendimento-blackfriday content.cxpress.io
```
