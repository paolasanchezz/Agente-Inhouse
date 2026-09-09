# LP Cxpress — obrigado

Thanks page. Recriação, dentro do nosso pipeline (`content.cxpress.io/obrigado`), da página
`home.cxpress.io/obrigado` — hoje no site institucional em GreatPages, fora do pipeline de LPs.

**Gerada em:** 2026-09-09
**Copy-fonte:** transcrição literal de `home.cxpress.io/obrigado` (hero). Rodapé: o padrão do
domínio, copiado da `escolha-a-cxpress` (trocado em 2026-09-09; antes vinha da `institucional`).
Ver `copy.txt`.
**Domínio:** `content.cxpress.io` (guarda-chuva migrado pro CI — deploy só via `lp-publicar`)

## O que foi pedido

1. Conteúdo **igual** ao de `home.cxpress.io/obrigado` (hero completo, incluindo o botão de WhatsApp).
2. Rodapé da LP `institucional`, com duas mudanças: **tirar o bloco de CTA** e **jogar o contato pra lá**.
3. Usar os assets enviados (mascote, pattern de fundo, ícone de ligação).
4. Depois da publicação: **rodapé igual ao de `content.cxpress.io/escolha-a-cxpress`** (substitui o
   item 2 — ver seção abaixo).

## Estrutura

- HERO (logo + H1 + CTA WhatsApp + lead + nota de horário + card "Escolheu receber uma ligação?" + mascote)
- FOOTER (padrão do domínio: logo + linha legal + 4 redes)

Nenhum bloco de texto novo: a página-fonte tem 1 seção, a LP tem 1 seção (GUIDELINES §9).

## Rodapé — trocado em 2026-09-09 (pós-publicação)

A primeira versão importava o rodapé pesado da LP `institucional` (gradiente radial escuro, bloco de
Contatos, "Canais integrados", texto legal com CNPJ e endereço), com o CTA removido e o contato
movido pro topo. A pedido do Bruno, passou a usar o **rodapé padrão das LPs Cxpress do domínio**,
tomando `escolha-a-cxpress` como referência: faixa navy, logo à esquerda, linha legal ao centro,
4 ícones de rede à direita; empilhado e centrado abaixo de 720px.

Copiado 1:1 de `landing-pages/cxpress/escolha-a-cxpress` (versão da `origin/main`, que é a que está
no ar — conferida contra o live). Só os nomes de variável mudaram, para os tokens que esta LP já
declara: `var(--navy)` → `var(--primary-dark)` (mesmo `#232960`), `var(--lilac)` →
`var(--primary-lighter)` (mesmo `#D7E2FF`), `var(--wrap)` → `1180px` literal.

Conferência de paridade contra o live da `escolha-a-cxpress` (Playwright, 1440): background,
`padding`, `border-top`, altura (137px), largura e padding do `.footer__inner`, colunas do grid
(425,25 / 217,5 / 425,25), `gap`, cor/tamanho/`line-height`/`text-wrap` do parágrafo, logo 150×34 e
os 4 botões de 44×44 com a mesma cor, borda e raio — **todos idênticos**.

O que saiu junto:

- **3 assets órfãos apagados** (só serviam ao rodapé antigo): o logo PNG do institucional, o
  `Cxpress_icons_social-scaled.png` e o `whatsapp-icon.png`. 141 KB a menos no repo.
- **Inter saiu do carregamento de fontes.** Era usada só pelo rodapé antigo (`.k2x-title`,
  `.k2x-copy`, o `+` dos divisores). Uma família a menos na request.

## Decisões de design

- **Verde do CTA `#0E7C40`, não o `#22c55e` da página-fonte.** Branco sobre `#22c55e` dá 2,2:1 e
  reprova AA (GUIDELINES §7, contraste é non-negotiable). Em `#0E7C40` dá **5,28:1** e o botão
  continua lendo como WhatsApp. Hover `#0A6633` (7,09:1).
- **Botão sem ícone.** A primeira versão tinha um glifo do WhatsApp no CTA; saiu no ajuste de
  2026-09-09 (a página-fonte não tem, o mock do Bruno não tem, e sem ele o label cabe numa linha
  no celular).
- **Card branco no bloco da ligação** em vez de texto solto sobre o pattern: separa o "plano B"
  (ligação) do caminho principal (WhatsApp) sem inventar seção nova.
- **Tipografia: par do brand — Open Sans nos títulos, Source Sans 3 no corpo.** A primeira versão
  usava Open Sans no corpo + Inter, porque era disso que o rodapé importado da `institucional`
  dependia. Com a troca do rodapé (2026-09-09) os dois motivos caíram, e o texto do rodapé da
  `escolha-a-cxpress` é Source Sans 3 — era a única diferença de medida que sobrava na paridade
  (Source Sans 3 é mais estreita que Open Sans, então a coluna do meio do grid dava 217,5px lá e
  247,4px aqui). Adotar o par do brand fechou a paridade e alinhou a LP com `brand/cxpress/tokens.json`
  e com as LPs irmãs do domínio.
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

Medições depois do ajuste (desequilíbrio de linha, §21): CTA 0% (1440 e 390), H1 6% no desktop.
Zero overflow horizontal em 1440/1200/980/820/600/390/375.

## Estado

- [x] HTML gerado
- [x] Ajuste de mobile (mascote em primeiro e menor, CTA em 1 linha) — 2026-09-09
- [x] QA local (1440 / 1200 / 980 / 820 / 600 / 390 / 375): zero overflow horizontal, todos os assets 200
- [x] `check_gtm_region.py`: 1 OK, 0 bloqueio
- [x] `bump_mobile_type.py --dry-run`: 0 clamps a ajustar (H1 34px, corpo 17px, mínimo 15px no mobile)
- [x] `build_umbrella.py` com manifesto de teste: 0 aviso, 0 path relativo sobrando, 10 assets copiados
- [x] Publicada — https://content.cxpress.io/obrigado (2026-09-09, PR #566, deploy CI run 34394978336)
- [x] Rodapé trocado pelo padrão do domínio (referência `escolha-a-cxpress`) + par tipográfico do brand — 2026-09-09
- [ ] Revisão (`lp-revisar`) — opcional, a LP não passou por auditoria de design/a11y automatizada

Validações do live em cada entrega: hash do servido idêntico ao do dist, todos os assets 200,
7/7 headers de segurança, GTM 3/3 tokens, vizinhas intactas (smoke do CI nas URLs do manifesto).
PageSpeed não rodou (API devolveu 429, quota do dia) — pendente.
Relatório: Notion, `Entregas > Entrega LP · Cxpress · obrigado · 2026-09-09`.

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
| `../../brand/cxpress/assets/logos/logo-reversed.svg` | brand (logo do rodapé) |

Os ícones de rede do rodapé são SVG inline, não arquivo (igual à `escolha-a-cxpress`). Os 3 assets
do rodapé antigo (logo PNG do institucional, `Cxpress_icons_social-scaled.png`, `whatsapp-icon.png`)
foram apagados na troca de 2026-09-09.
