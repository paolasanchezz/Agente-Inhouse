# banimento-whatsapp

LP do guarda-chuva **content.cxpress.io** (projeto Vercel `cxpress-lp-playbook-whatsapp2026`).

> **Fonte recuperada retroativamente em 2026-06-16** a partir do deploy production `dpl_ESQB5LVKyK3EDf3T6tsutiGdv7uF`.
> A LP estava no ar mas nao tinha source no repo (anti-padrao §7.1 — "LP publicada so na sibling").
> Paths de deploy (`/assets/cxpress/...`) revertidos para a convencao do repo
> (brand -> `../../brand/...`, LP-local -> `./assets/...`); reversao verificada
> byte-a-byte contra o HTML do live.

- **lang:** `pt-BR`
- **Formulario:** Jotform `261027639617663` ("LPs - Proposta"), o form unificado das LPs de proposta BR desde o PR #374 (2026-08-26). A pagina de agradecimento pos-submit e configurada no Jotform, nao no embed, entao ela acompanha o form: conferir o destino no proprio `261027639617663` antes de assumir qual e.
- **Assets LP-local recuperados:** plataforma/clientes-cxpress.png, plataforma/mockup-plataforma-laptop.png, plataforma/plataforma-canais.gif, plataforma/plataforma-chatbot-ia.gif, plataforma/plataforma-dashboard.gif, og-banimento-whatsapp.png (OG)

## Atualizacao de preco — 2026-08-28

Novo preco minimo de plano da Cxpress: **R$ 1.750**. A chamada de preco desta LP passou a
`Planos a partir de R$ 1.750`, **sem** mencao a quantidade de acessos — por decisao do usuario,
o detalhamento de acessos fica restrito a LP canonica de precos (`/planos`), que segue intacta
com "A partir de R$ 1.750 por mes, com 5 acessos de operador". Alteracao aplicada em bloco nas
9 LPs BR da Cxpress que citavam preco fora da `/planos`.

As LPs LATAM (`USD 260/mes`) e PT-PT (`295 EUR/mes`) **nao** foram alteradas: os valores oficiais
em USD/EUR ainda nao foram definidos e seguem defasados em relacao ao minimo BR.

## Atualizacao 2026-08-28 — paridade visual com `evite-banimento-whatsapp`

Pedido: aplicar aqui **as mesmas imagens e a correcao de espaco** que ja estavam na LP
`evite-banimento-whatsapp` (variante desta pagina). Nada de copy mudou — so hero visual e ritmo vertical.

| # | O que | De | Para |
|---|---|---|---|
| 1 | Visual do hero | `plataforma-canais.gif` (566x318) + 3 pilulas decorativas (`.hero__pills`) | `./assets/hero-conta-banida-whatsapp.png` (430x901) sobre circulos concentricos (`./assets/hero-circulos-concentricos.svg`) + glow ambar + 2 pilulas (`.hero__decor`) |
| 2 | Espaco morto entre HERO e CLIENTES | `hero__inner` padding 40/88, gap 64; `.clientes` padding-top 104px | aparelho com teto de 272px, `hero__inner` padding 44/56 e gap 56, `.clientes` padding-top 40px |
| 3 | `overflow` do hero | `overflow:hidden` no `.hero` | removido — a sombra do aparelho precisa transbordar; o corte horizontal passou pro `overflow-x:hidden` do `body` |
| 4 | Hero no mobile (<=980px) | `padding:36px 24px 72px`, gap 48; pilula 1 escondida | `padding:32px 24px 48px`, gap 32; aparelho fluido `min(62vw,260px)`, circulos `min(98%,360px)`, pilula 1 escondida; pilula 2 sai em <=520px |
| 5 | Logo Elife em QUEM SOMOS | `<img>` sem width/height (CLS) | `width="250" height="140"` + `loading="lazy"` |

Sobre o **delta 2**: o vazio nao era padding, era a diferenca de altura entre as duas colunas do grid
do hero (`align-items:center` com um visual muito mais alto que o texto cria faixa morta em cima e
embaixo). Medido no render: coluna de texto 516px x visual 570px em 1440px de viewport. O corte de
padding foi complemento.

Sobre o **delta 1**: os circulos sao SVG (~420 bytes), nao PNG — nitidos em qualquer densidade e sem
peso no LCP do hero. No mobile o diametro cai pra `min(98%,360px)` de proposito: acima disso o anel
externo estoura a coluna e o `overflow-x:hidden` do body corta o circulo numa linha reta.

O icone deformado do card `Historico que nao se perde` (corrigido na `evite-` na mesma rodada) **nao**
existe aqui: os cards de BENEFICIOS desta LP usam `.card__pill` decorativa, sem icone SVG.

Medicao: `scrollWidth == clientWidth` em 320 / 390 / 768 / 1440px. Build do guarda-chuva e gate
GTM x regiao rodados localmente antes do PR (54 LPs, 0 bloqueios).

**Assets LP-local novos:** `assets/hero-conta-banida-whatsapp.png` (430x901, 429 KB),
`assets/hero-circulos-concentricos.svg` (~420 B) — copias byte-a-byte das da
`evite-banimento-whatsapp`. As duas LPs mapeiam pro mesmo destino `/assets/cxpress/` no
guarda-chuva, e o build ignora a segunda copia (`if os.path.exists(dest): continue`) — como os
arquivos sao identicos, nao ha divergencia possivel entre as paginas.
