# LP Cxpress — obrigado

Thanks page. Recriação, dentro do nosso pipeline (`content.cxpress.io/obrigado`), da página
`home.cxpress.io/obrigado` — hoje no site institucional em GreatPages, fora do pipeline de LPs.

**Gerada em:** 2026-09-09
**Copy-fonte:** transcrição literal de `home.cxpress.io/obrigado` (hero) + rodapé de
`content.cxpress.io/institucional`. Ver `copy.txt`.
**Domínio:** `content.cxpress.io` (guarda-chuva migrado pro CI — deploy só via `lp-publicar`)

## O que foi pedido

1. Conteúdo **igual** ao de `home.cxpress.io/obrigado` (hero completo, incluindo o botão de WhatsApp).
2. Rodapé da LP `institucional`, com duas mudanças: **tirar o bloco de CTA** e **jogar o contato pra lá**.
3. Usar os assets enviados (mascote, pattern de fundo, ícone de ligação).

## Estrutura

- HERO (logo + H1 + CTA WhatsApp + lead + nota de horário + card "Escolheu receber uma ligação?" + mascote)
- FOOTER (importado da `institucional`, sem o CTA, com Contatos no topo)

Nenhum bloco de texto novo: a página-fonte tem 1 seção, a LP tem 1 seção (GUIDELINES §9).

## Rodapé — o que mudou em relação ao da `institucional`

| Item | `institucional` | aqui |
|---|---|---|
| `.k2x-top` | logo + botão "Falar com um especialista" (âncora `#proposta`) | logo + bloco **Contatos** |
| `.k2x-grid` | 2 colunas (texto + Contatos) | 1 coluna (texto + "Canais integrados") |
| `.k2x-btn` | gradiente royal, shimmer no hover | **removido** (CSS inclusive) |
| `.k2x-logo` | `<img>` solto | envolvido em link pra home da marca, nova aba (GUIDELINES §17) |
| `.k2x-contato-tel` | sem CSS (telefone e ícone caíam como inline) | `flex` com `gap`, ícone alinhado ao número |
| `.k2x-title` ("Contatos") | `#8a8a8a` (≈4,0:1 no fundo escuro, reprova AA) | `#B9BDCC` (6,9:1) |
| `.k2x-social`, `.k2x-row`, `.k2x-wibix` | declarados | removidos (CSS morto — não existem neste rodapé) |
| `.fade-in` | reveal próprio da `institucional` | rodapé sem animação; o reveal é só do hero |

A remoção do CTA não é cosmética: a âncora `#proposta` aponta pro formulário da `institucional`,
que não existe aqui. Mantê-lo seria link quebrado no rodapé.

## Decisões de design

- **Verde do CTA `#0E7C40`, não o `#22c55e` da página-fonte.** Branco sobre `#22c55e` dá 2,2:1 e
  reprova AA (GUIDELINES §7, contraste é non-negotiable). Em `#0E7C40` dá **5,28:1** e o botão
  continua lendo como WhatsApp. Hover `#0A6633` (7,09:1).
- **Botão sem ícone.** A primeira versão tinha um glifo do WhatsApp no CTA; saiu no ajuste de
  2026-09-09 (a página-fonte não tem, o mock do Bruno não tem, e sem ele o label cabe numa linha
  no celular).
- **Card branco no bloco da ligação** em vez de texto solto sobre o pattern: separa o "plano B"
  (ligação) do caminho principal (WhatsApp) sem inventar seção nova.
- **Tipografia Open Sans + Inter**, o mesmo par que a `institucional` carrega — o rodapé importado
  depende de Inter (`.k2x-title`, `.k2x-copy`, o `+` dos divisores) e Open Sans no corpo. Evita
  carregar uma terceira família só pro hero.
- **Nota de horário em 15px** (a fonte usa 9px, ilegível no celular; piso de label da §20 é 14px).
- Mascote e pattern entram como `<picture>` / `image-set()` **WebP com fallback PNG**: os assets
  enviados são WebP (é o formato que a página-fonte serve, mesmo com extensão `.png`), e a §3.6 pede
  PNG pra mascote. Os PNGs foram gerados a partir dos WebP (Pillow), então há as duas versões.

## Ajuste de mobile — 2026-09-09

Pedido do Bruno ("corrigir mobile, imagem do mascote em primeiro e menor e corrigir CTA"), com mock
de referência. O empilhado deixou de ser uma versão estreita do desktop e virou layout próprio:

- **Ordem: logo → mascote → headline → CTA → lead → nota → ligação.** O mascote era o último
  elemento da página (só aparecia depois de todo o texto); agora vem logo abaixo da logo.
  Feito por `grid-template-areas` (`"logo" "visual" "content"`), **não** por `order`. Pra isso a
  `.hero__logo` saiu de dentro da `.hero__content` e virou irmã dela no grid.
- **Mascote menor:** 210px até 980px, 190px até 600px (era 340/260).
- **Tudo centralizado** abaixo de 980px, como no mock (era alinhado à esquerda).
- **Bloco da ligação sem a caixa branca** no empilhado: coluna centralizada com o ícone acima do
  título. No desktop o card branco continua.
- **CTA numa linha só:** com o ícone fora e `padding` lateral de 20px (mais respiro do container em
  20px), "Continue a conversa pelo WhatsApp" cabe numa linha a partir de ~390px de largura, que
  cobre praticamente todos os celulares. Abaixo disso o label quebra em **2 linhas parelhas**
  (`text-wrap: balance` num `<span>` em `display:block`, GUIDELINES §21 ressalva 3) em vez de soltar
  "WhatsApp" sozinho. A fonte fica nos 17px do piso da §20; nada de reduzir texto pra caber.
- **Pattern de fundo abrandado no empilhado.** Com `cover` numa tela estreita, o pattern aparece
  inteiro na vertical e as diagonais da base dele caíam exatamente sobre o texto da ligação. Um véu
  da própria cor de fundo (66%) por cima mantém a textura e devolve o contraste do texto.

Medições depois do ajuste (desequilíbrio de linha, §21): CTA 0% (1440 e 390), H1 6% no desktop,
parágrafo do rodapé caiu de 62% para 21% em 390. Zero overflow horizontal em 1440/1200/980/820/600/375.

## Estado

- [x] HTML gerado
- [x] Ajuste de mobile (mascote em primeiro e menor, CTA em 1 linha) — 2026-09-09
- [x] QA local (1440 / 1200 / 980 / 820 / 600 / 390 / 375): zero overflow horizontal, todos os assets 200
- [x] `check_gtm_region.py`: 1 OK, 0 bloqueio
- [x] `bump_mobile_type.py --dry-run`: 0 clamps a ajustar (H1 34px, corpo 17px, mínimo 15px no mobile)
- [x] `build_umbrella.py` com manifesto de teste: 0 aviso, 0 path relativo sobrando, 10 assets copiados
- [ ] Revisão (`lp-revisar`)
- [ ] Publicada — falta entrar em `landing-pages/dominios/content-cxpress-io/manifest.json` via `lp-publicar`

## Exceções deliberadas às GUIDELINES (precedente: cadastro-realizado / video-atendimento-obrigado)

- **`noindex, follow`**: página pós-ação. O Lighthouse SEO do `lp-publicar` vai apontar
  "is-crawlable" como falha — esperado, não "consertar".
- **Sem OG image, sem JSON-LD e sem `canonical`/`{{DOMAIN}}`**: ninguém compartilha esta URL.
  Ficaram só `og:title`/`og:description`/`og:type`/`og:site_name`/`og:locale`, para o caso de alguém
  colar o link num chat.
- **Sem estrutura mínima de LP (§6)**: não há captação aqui, é confirmação.
- **§3 "headline sempre antes do visual no mobile" invertida** (2026-09-09, a pedido): a regra existe
  para LP de captação não esconder a proposta atrás de um card de data. Aqui é thanks page, não há
  decisão a tomar, e o mascote é justamente o "deu certo". Registrado no CSS junto da media query
  para ninguém "consertar" numa revisão futura.

## Atenção — sobreposição com `cadastro-realizado`

`landing-pages/cxpress/cadastro-realizado` já é uma recriação desta **mesma** página-fonte
(`home.cxpress.io/obrigado`), publicada em `content.cxpress.io/cadastro-realizado` desde 2026-08-13,
com duas diferenças pedidas na época: **sem** o bloco de WhatsApp e com rodapé mínimo.

Ou seja: depois de publicar, o pipeline terá duas thanks pages para a mesma origem. Vale decidir qual
é a canônica e para onde os formulários do site institucional passam a apontar. Não mexi na
`cadastro-realizado`.

## Notas

- GTM: `GTM-T4XDWHL3` (região brasil, mesmo container das demais LPs Cxpress BR).
- O formulário que hoje redireciona para `home.cxpress.io/obrigado` precisa ser reapontado para
  `content.cxpress.io/obrigado` — a troca é fora do repo, no site institucional.

## Assets referenciados

| Path | Origem |
|---|---|
| `../../brand/cxpress/assets/logos/logo-icon.png` | brand (favicon) |
| `../../brand/cxpress/assets/logos/logo-primary.svg` | brand (logo do hero) |
| `./assets/hero-pattern.webp` + `.png` | pattern de fundo enviado pelo usuário (1440×900) |
| `./assets/mascot/samir-apontando.webp` + `.png` | mascote enviado pelo usuário (470×439) |
| `./assets/icon-ligacao.svg` | ícone de ligação enviado pelo usuário |
| `./assets/imgi_1_3433378_1_176476463169302bd7a5301467666886-1.png` | logo do rodapé, copiado da `institucional` |
| `./assets/Cxpress_icons_social-scaled.png` | "Canais integrados", copiado da `institucional` |
| `./assets/whatsapp-icon.png` | ícone do rodapé, copiado da `institucional` |

Os três últimos são byte-a-byte iguais aos da `institucional`, então convivem no mesmo
`/assets/cxpress/` do guarda-chuva sem colisão de conteúdo.
