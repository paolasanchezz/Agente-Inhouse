# atendimento-digital

LP do guarda-chuva **content.cxpress.io** (projeto Vercel `cxpress-lp-playbook-whatsapp2026`).

> **Fonte recuperada retroativamente em 2026-06-16** a partir do deploy production `dpl_ESQB5LVKyK3EDf3T6tsutiGdv7uF`.
> A LP estava no ar mas nao tinha source no repo (anti-padrao §7.1 — "LP publicada so na sibling").
> Paths de deploy (`/assets/cxpress/...`) revertidos para a convencao do repo
> (brand -> `../../brand/...`, LP-local -> `./assets/...`); reversao verificada
> byte-a-byte contra o HTML do live.

- **lang:** `pt-BR`
- **Formulario:** Jotform `261027639617663` ("LPs - Proposta"), o form unificado das LPs de proposta BR desde o PR #374 (2026-08-26). A pagina de agradecimento pos-submit e configurada no Jotform, nao no embed, entao ela acompanha o form: conferir o destino no proprio `261027639617663` antes de assumir qual e.
- **Assets LP-local recuperados:** plataforma/clientes-cxpress.png, plataforma/mockup-plataforma-laptop.png, plataforma/plataforma-canais.gif, plataforma/plataforma-chatbot-ia.gif, plataforma/plataforma-dashboard.gif, og-atendimento-digital.png (OG)

## Atualizacao de preco — 2026-08-28

Novo preco minimo de plano da Cxpress: **R$ 1.750**. A chamada de preco desta LP passou a
`Planos a partir de R$ 1.750`, **sem** mencao a quantidade de acessos — por decisao do usuario,
o detalhamento de acessos fica restrito a LP canonica de precos (`/planos`), que segue intacta
com "A partir de R$ 1.750 por mes, com 5 acessos de operador". Alteracao aplicada em bloco nas
9 LPs BR da Cxpress que citavam preco fora da `/planos`.

As LPs LATAM (`USD 260/mes`) e PT-PT (`295 EUR/mes`) **nao** foram alteradas: os valores oficiais
em USD/EUR ainda nao foram definidos e seguem defasados em relacao ao minimo BR.

## Padronizacao com as LPs irmas — 2026-09-14

Alinhamento com `whatsapp-business`, `chatbot-whatsapp`, `escolha-a-cxpress` e
`banimento-de-whatsapp`. Nenhuma copy foi alterada.

| O que | De | Para |
|---|---|---|
| Menu | `rgba(255,255,255,.94)` + `blur(8px)` | vidro padrao: `.80` + `blur(5px)` + borda `#e2e8f0`, com fallback `@supports` |
| Tela do hero | `mockup-plataforma-laptop.png` (PNG recortado) | `tela-canais.svg` na moldura `.frame`, a mesma tela do bloco "Organize seu atendimento de forma integrada" da `whatsapp-business` |
| Clientes | imagem estatica `clientes-cxpress.png` | esteira `.ticker` com os 14 logos, identica a da `chatbot-whatsapp` |
| Rodape | logo + 2 linhas de texto | rodape padrao: logo, credito e nav de redes sociais (alvo de 44px, anel de 1px) |
| Selo do quem-somos | glifo do WhatsApp consumidor | marca WhatsApp Business (`<symbol id="ico-wab">`) |
| Jotform | `<script src>` inline, parser-blocking | carregamento diferido por `IntersectionObserver` + pre-carga por intencao + rede de seguranca em 3 degraus |

### Contraste

Adotada a escala tonal navy da `whatsapp-business`. O ganho nao e "texto mais
escuro" — e a separacao entre titulo e corpo, que sobe de **1.52:1** para
**1.84:1** sem tocar em nenhuma cor de marca.

- `--neutral-700` `#4a4a4a` -> `#4B5670` (corpo: 7.33:1 no branco, 6.60:1 no tint)
- `--neutral-500` `#606B88` (novo; apoio: 5.31:1 no branco)
- `--neutral-100` `#f5f5f5` -> `#EDF1FA` (fundo das secoes com tinta)
- `--neutral-300` `#d1d1d1` -> `#C6D0E4`, `--rule` `#DCE4F2` (filete de limite de secao)
- `.qs-badge` saiu do cinza fora da paleta `#6b7280` (4.83:1) para `--neutral-500` (6.05:1)

Os usos de `--neutral-100` como **borda** foram remapeados para `--neutral-300`
(cards, FAQ, midia de feature) e `--rule` (limites de secao): o novo valor e um
fundo, e como borda daria 1.05:1.

### Pendencias conhecidas

- `assets/plataforma/` (5,3 MB) nao e referenciado pelo HTML — as imagens vem de
  `../../brand/cxpress/assets/plataforma/`. Ja estava assim antes desta passagem.
- O README acima cita o form `261027639617663`, mas o HTML embeda o
  `261045149477663`. Conferir qual e o correto.

## Hero: conversa simulada no lugar da tela — 2026-09-14 (2a passagem)

A imagem da primeira secao saiu. Onde havia a `tela-canais.svg` na moldura
`.frame`, entra uma **conversa de WhatsApp simulada**.

O bloco `.chat` nao foi inventado aqui: e o mesmo de `atendimento-domingo` e
`black-friday-atendimento`, cujo CSS e byte-a-byte identico entre as duas.
Tres adaptacoes, porque nessas duas o hero e navy e aqui e branco:

| Ajuste | Motivo |
|---|---|
| card ganha `border:1px solid var(--neutral-300)` | branco sobre branco nao tem aresta |
| sombra de `rgba(6,10,38,.45)` para uma equivalente no claro | a original foi calibrada pra fundo escuro; no claro vira mancha |
| ponto de status usa `--wa-ink` `#15884D` em vez de `--green` `#21CC78` | o verde da marca da **2.11:1** no branco e reprova o minimo de 3:1 de elemento grafico (WCAG 1.4.11). `#15884D` da 4.51:1 — mesmo aprendizado ja registrado nas LPs irmas |
| bolha de entrada fixada em `#F2F3F5` | nas LPs de origem ela usa `--neutral-100`, que la vale `#f5f5f5`. Aqui o token foi reaproveitado como fundo de secao (`#EDF1FA`) e puxava a bolha pro azul. O cinza tambem e o que o WhatsApp usa na mensagem recebida |

Tambem: `.chat__head` passou a `align-items:flex-start` com `margin-top:6px` no
ponto. O cabecalho daqui e mais longo que o das LPs de origem e quebra em duas
linhas no mobile — com `center` o ponto boiava entre as linhas. Em uma linha so
o resultado e identico ao de antes.

A conversa carrega os tres beneficios da propria LP: distribuicao automatica
(no divisor), IA no primeiro nivel (no selo) e tempo de resposta medido (no
cabecalho e nos horarios).

### Sairam junto

- CSS `.frame` / `.frame__bar` / `.frame__dot` / `.hero__frame` (ficariam orfaos)
- `assets/telas/tela-canais.svg` (130 KB). O arquivo original segue em
  `whatsapp-business/assets/telas/` — esta LP so tinha uma copia.

### Efeito colateral bom

O elemento de LCP do hero deixa de ser um SVG de 130 KB e passa a ser texto.

### Pilulas decorativas

Foram reposicionadas: estavam calibradas pra moldura larga da tela e, com o card
da conversa (mais estreito e mais alto), a do canto inferior esquerdo ficava ao
**lado** do card em vez de atras e lia como forma solta. Agora o anel laranja e
deitado, como o `f2` do fecho, e abraca o canto.
