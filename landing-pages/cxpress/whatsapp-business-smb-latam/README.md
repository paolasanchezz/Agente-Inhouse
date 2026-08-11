# whatsapp-business-smb-latam

LP do guarda-chuva **content.cxpress.io** (projeto Vercel `cxpress-lp-playbook-whatsapp2026`).

Clone de `whatsapp-business-smb` (PT-BR) criado em 2026-07-30 a pedido explícito do usuário
("traduce esta LP al español neutro para que funcione en todo latam":
https://home.cxpress.io/whatsapp-business-smb): design 100% idêntico ao original, copy adaptada
para ES-LATAM (protocolo linguístico + anti-IA aplicado, mesmo processo já validado em
`whatsapp-business-smb-pt`).

- **lang:** `es-419`
- **GTM:** `GTM-WRQ47B9R` (região latam, `brand/cxpress/tracking.json`)
- **Organization/WebPage (JSON-LD) + hrefs de logo:** apontam para `https://home.cxpress.io`
  (igual ao BR — `brand-manifest.json` não tem home dedicado para latam, diferente de Portugal
  que usa `cxpress.pt`)
- **hreflang:** `es-419` (self) + `pt-BR` (`whatsapp-business-smb`) + `pt-PT`
  (`whatsapp-business-smb-pt`) + `x-default` (BR)

## Seção Clientes (idêntica ao BR, ao contrário do PT-PT)

Diferente de `whatsapp-business-smb-pt` (que trocou os logos por clientes portugueses), aqui o
grid de clientes BR (Koin, Advanta, Mondial, Vivo, Sephora, Smartfit, ThermoFisher, J&T Express,
Eletrobras, Cacau Show) foi **mantido sem troca** — segue o mesmo critério já usado em
`coex-whatsapp-latam` e `banimento-whatsapp-latam` (nenhuma dessas duas LPs LATAM trocou o asset
de clientes; não existe hoje um asset de clientes específico para LATAM).

## Pendências resolvidas (2026-07-30, a pedido do usuário)

1. **Preço:** "Planos a partir de R$ 1.290/mês para até 5 acessos" (BR) → "Planes desde USD
   260/mes" — conversão aproximada, sem mencionar quantidade de acessos, a pedido explícito
   (mesmo critério do clone PT-PT, que converteu para EUR sem mencionar acessos).
2. **E-mail comercial BR:** removido (`comercial@gocxpress.com.br` e o mailto correspondente) —
   mesmo critério do clone PT-PT.
3. **Formulário:** Jotform LATAM já compartilhado `252398149653872` (mesmo ID usado em
   `coex-whatsapp-latam` e `banimento-whatsapp-latam`), substituindo o Jotform BR
   `261027639617663`.

## Assets

Reaproveitados de `whatsapp-business-smb` (imagens/gifs sem texto embutido) — nenhum asset novo
necessário.

## Notion

Não publicado — MCP do Notion não estava conectado nesta sessão. `copy.txt` é a fonte-verdade
local; publicar manualmente quando o MCP estiver disponível, se desejado.

## Hreflang / og:locale:alternate

Como esta é a 3ª variante da família (BR + PT + LATAM), atualizei os dois irmãos
(`whatsapp-business-smb` e `whatsapp-business-smb-pt`) para listar as 3 variantes em
`hreflang` + `og:locale:alternate` (GUIDELINES §16 exige que cada LP da família liste todas).
O BR não tinha nenhum bloco `hreflang` antes desta sessão (lacuna pré-existente, corrigida de
passagem).

## Estado

- [x] Copy traduzida ES-LATAM (`copy.txt`), estrutura idêntica ao BR (10 blocos)
- [x] HTML gerado — mesmo sistema visual/CSS de `whatsapp-business-smb` e `whatsapp-business-smb-pt`,
      conteúdo 1:1 com `copy.txt` (auditoria de fidelidade feita manualmente linha a linha)
- [x] SEO completo (title, description, canonical, hreflang ×4, OG ×12, Twitter ×4, JSON-LD) —
      slug `whatsapp-business-smb-latam`
- [x] GTM — `GTM-WRQ47B9R` (região `latam`), validado via `check_gtm_region.py` (`.tracking.lock` OK)
- [x] OG image dedicada — `assets/og-whatsapp-business-smb-latam.png` (1200×630), gerada via
      Chrome headless + template adaptado de `.claude/skills/lp-gerar/og-template.html`
- [x] Formulário Jotform LATAM (`252398149653872`, já compartilhado por `coex-whatsapp-latam` e
      `banimento-whatsapp-latam`) — integrado direto (não é mock; mesmo critério dos 2 irmãos,
      que também usam o form real desde a criação por serem clones de uma LP já publicada)
- [ ] Revisão de design (`/lp-revisar cxpress/whatsapp-business-smb-latam`)
- [ ] Publicado (`/lp-publicar cxpress whatsapp-business-smb-latam content.cxpress.io`)

---

## 2026-08-10 — Restyle: alinhamento visual com os criativos da campanha BOFU

A campanha de Meta Ads (9 estáticos ES-LATAM, WhatsApp SMB) usa um sistema visual proprio:
navy profundo com trama de losangos, arcos empilhados no canto superior direito
(laranja + amarelo + royal), palavra-chave em laranja no titulo e CTA laranja em caixa alta.
A LP estava no sistema antigo (fundo branco, CTA navy) e o lead nao reconhecia a ligacao
anuncio -> pagina. Alinhado:

- **Hero**: navy com gradiente radial + trama de losangos + arcos no canto. H1 branco com
  destaque laranja. Sub em `--on-dark`. Mockup com sombra pra fundo escuro.
- **Navbar**: navy translucido, logo reversed, CTA laranja em caixa alta.
- **CTA (`.btn`)**: laranja com texto navy, caixa alta, tracking largo. **Texto navy e nao branco**:
  branco sobre `#EF863C` da 2.5:1 e reprova AA (os criativos usam branco, a LP nao pode).
- **Cards**: tile de icone arredondado (SVG inline: WhatsApp, relogio, agentes, historico,
  raio, escudo) no lugar da pilula abstrata, como nos cards brancos dos anuncios.
- **Prova (stats)**: faixa escura com numeros em laranja (5.2:1 sobre navy) e cards translucidos.
- **CTA final (`.agendar`)**: faixa escura com arcos; o card branco do formulario ganha contraste.
- **Secoes claras** (`destaque`, `faq`): mesma trama de losangos em navy 5.5% de opacidade.
- **Destaque de palavra**: `.hl` (laranja) so em fundo escuro; `.hl-b` (royal, 5.0:1) em fundo claro.
- Limpeza: `.hero__pills` e `.card__pill` removidos (os arcos e os tiles assumiram o papel).

**Desvio consciente de GUIDELINES §1** ("uma unica secao pode ser escura"): a LP passa a ter
3 faixas escuras (hero, prova, CTA final) + footer. Justificativa: o pedido e casar a identidade
com os anuncios, que sao majoritariamente navy. A regra de nao alternar tints claros diferentes
segue respeitada (so branco <-> neutral-100 nas secoes claras).

Validado: build do guarda-chuva OK, `grep "—"` = 0, contraste AA em todos os pares novos,
render desktop 1440 e mobile 390.

- [ ] Publicado com o restyle (`/lp-publicar cxpress whatsapp-business-smb-latam content.cxpress.io`)

### 2026-08-10 (2) — Camada de movimento e interacao

Enriquecimento de motion sobre o restyle, dentro de GUIDELINES §4 (motion serve ao conteudo,
nenhum texto essencial depende de animacao):

- **Barra de progresso de leitura** (3px, laranja -> amarelo) fixa no topo, `aria-hidden`.
- **Navbar reativa**: compacta e ganha sombra depois de 40px de scroll.
- **Arcos** entram de cima escalonados (.10s / .20s / .30s) no load.
- **Mockup do hero** flutua em loop lento (7s).
- **CTAs**: seta que desliza no hover + brilho diagonal atravessando o botao.
- **Cards**: tile do icone sobe, escala e gira levemente no hover; borda muda de cor.
- **Reveal escalonado** por posicao dentro dos grids (90ms entre irmaos).
- **Contadores** nos indicadores (14/9/25/45), animados na entrada em viewport, easing cubic-out.
  O valor final ja esta no HTML: sem JS ou com reduced-motion, aparece o numero certo.
- **Imagens da plataforma** com zoom sutil no hover do bloco.
- **FAQ virou acordeao animado** (altura), um item aberto por vez. Marcacao ganhou
  `div.faq__body` por item pra permitir a transicao. Sem JS, os `<details>` seguem nativos.
- **CTA fixo no mobile** (<=720px): aparece depois do hero, some quando o formulario entra em
  tela. `aria-hidden` + `tabindex` sincronizados pra nao duplicar foco (o mesmo CTA ja existe
  na navbar).

Todo o JS checa `prefers-reduced-motion` e o CSS ja tinha o bloco global de reducao.
Testado: sem erro de console, contadores corretos com reduced-motion, acordeao com 1 aberto,
CTA mobile ligando e desligando nos limites certos, build do guarda-chuva OK.

### 2026-08-10 (3) — Hero: GIF PT-BR substituido por mockup animado em espanhol

O `assets/hero-dashboard.gif` (604×340, 177 frames, 1,2 MB) tem o texto **queimado nos frames**
e esta em portugues: menu do painel (Dashboard, Histórico, Consumidores, Disparo Ativo, Sair da
Cxpress), chips de canais (Telefone) e um chat "Olá! Boa tarde. / Olá, Miguel. Obrigado...".
Havia ate um seletor "BR | PT" no rodape do menu. Nao existe arquivo fonte (AE/Figma) no repo,
entao nao da pra traduzir o GIF: foi **reconstruido em HTML/CSS**, nativo e em espanhol.

Mesmas 3 batidas do original, em loop de 16,5s com cross-fade:
1. **Menu do painel** — Panel, Tickets, Historial, Consumidores, Agentes, Envío activo, Configuraciones
2. **Canales** — Correo, WhatsApp, Facebook, Instagram, Webchat, Teléfono
3. **Conversa no WhatsApp** — "¡Hola! Buenas tardes." respondido pela IA ("Hola, Miguel. Gracias
   por escribirnos, ¿en qué podemos ayudarte hoy?") com selo IA e indicador de digitacao

Ganhos: texto em espanhol de verdade, nitido em qualquer densidade de tela, **1,2 MB a menos**
no carregamento do hero (o GIF era `loading="eager"`), e adere a `prefers-reduced-motion`
(sem loop, mostra so a cena da conversa). Acessibilidade: bloco com `role="img"` +
`aria-label` equivalente ao alt anterior; conteudo interno `aria-hidden`.

O arquivo `assets/hero-dashboard.gif` ficou **sem referencia** (o build so copia asset citado no
HTML, entao ele nao vai pro dist). Mantido no repo por ora; pode ser removido numa limpeza, ou
voltar a ser usado se o time entregar a versao ES do motion original.

Ajuste de passagem: a seta do CTA (`.btn__arrow`) some abaixo de 560px, senao quebrava sozinha
numa segunda linha no mobile.
