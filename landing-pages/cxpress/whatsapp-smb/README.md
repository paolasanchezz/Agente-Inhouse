# whatsapp-smb

LP do guarda-chuva **content.cxpress.io** (projeto Vercel `cxpress-lp-playbook-whatsapp2026`).

> **Recriação da página `https://agentes.elife.com.br/smb`** (GreatPages), pedida pelo Victor em 2026-08-13.
> Copy, ordem das seções, cores, tipografia e imagens replicam a original. A diferença é a
> construção: a original é GreatPages com posicionamento absoluto e dois layouts fixos
> (desktop + `max-width:800px`); esta é HTML/CSS estático com grid fluido e reflow real
> em qualquer largura.

- [x] Formulário integrado
- **Form provider:** Jotform, form ID `261027639617663` ("LPs - Proposta"), o form unificado das LPs de proposta BR desde o PR #374 (2026-08-26). Antes usava o `262146559200655` (mesmo da `banimento-whatsapp-comercial`); as duas convergiram para o form unico, que ja era o da LP original.
- **lang:** `pt-BR`
- **GTM:** `GTM-T4XDWHL3` (padrão Cxpress BR do repo). A original usa `GTM-KN8BPFG`.

## Assets

LP-local em `assets/smb/` (baixados da própria página original):

| Arquivo | Origem (GreatPages) | Onde aparece |
|---|---|---|
| `hero-plataforma.gif` | `paginas_editor/10252-1d4e15bd….gif` | Hero |
| `star.svg` | `imagens/6.svg` | 5 estrelas da prova social |
| `clientes.svg` | `imagens/8.svg` | Faixa de logos de clientes |
| `whatsapp-celular.jpg` | `imagens/10.jpeg` | Seção WhatsApp CoEx |
| `icone-economia-tempo.svg` | `imagens/14.svg` | Card "Economia de tempo" |
| `icone-respostas-rapidas.svg` | `imagens/12.svg` | Card "Respostas rápidas" |
| `icone-api-oficial.svg` | `imagens/16.svg` | Card "API oficial do WhatsApp" |
| `fundo-gradiente.png` | `imagens/18.png` | Fundo da seção do vídeo |
| `conector-a.svg` / `conector-b.svg` | `imagens/19.svg` / `23.svg` | Tracejados do zigue-zague |
| `badge-chatgpt.webp` | `imagens/21.webp` | Linha "Atendimento automático com IA" |
| `plataforma-tickets.webp` | `imagens/25.webp` | Linha "Centralize os cadastros" |
| `plataforma-triagem.gif` | `paginas_editor/10252-5d854682….gif` | Linha "Organize seu atendimento" |
| `ondas.png` | `imagens/29.png` | Fundo decorativo de "Quem somos" |
| `quem-somos.jpg` | `imagens/31.jpg` | Foto de "Quem somos" |
| `icone-whatsapp.png` / `icone-chatgpt.png` | `imagens/35.png` / `37.png` | Selos de API oficial |
| `logo-elife.png` / `logo-elifegroup.png` | `imagens/33.png` / `39.png` | Selo "Um produto" e rodapé |
| `og-whatsapp-smb.png` | `social_cover/tODMLIBh….png` | OG image (upscale 600×315 → 1200×630) |

Do brand (`brand/cxpress/assets/`), byte-idênticos aos da original:

- `logos/logo-primary.svg` (cabeçalho) e `logos/logo-icon.png` (favicon)
- `plataforma/plataforma-canais.gif` (linha "Otimize a gestão de tickets")
- `plataforma/plataforma-dashboard.gif` (linha "Gerencie com eficiência")

Vídeo: YouTube `36sbDc02_DU` (mesmo embed da original).

## Diferenças conscientes em relação à original

Tudo o que muda em relação a `agentes.elife.com.br/smb`, e por quê:

1. **Responsivo de verdade.** A original tem só dois estados (desktop absoluto e mobile
   `≤800px`). Aqui o layout usa grid e reflui em qualquer largura, com breakpoints em
   1040 / 900 / 600px. No mobile, headline sempre antes do visual (GUIDELINES §3).
2. **Formulário.** Jotform `262146559200655` (o da `banimento-whatsapp-comercial`), como
   pedido, no lugar do `261027639617663` da original.
3. **Bloco de preço não replicado.** A original tem um bloco "Condições especiais /
   MELHOR CUSTO BENEFÍCIO / *Preços para canais WhatsApp + E-mail" marcado com
   `esconder_desktop esconder_mobile`: ele **não renderiza para ninguém** na página no ar.
   Como não é conteúdo visível, ficou de fora. O preço que aparece de fato
   ("Planos a partir de R$ 1.750") está mantido.
4. **Título "Fale com especialista" acima do form.** Na original ele é texto branco sobre
   card branco, ou seja, invisível. Não foi reproduzido; o Jotform já traz o próprio título.
5. **FAQ com cor única.** Na original os 3 primeiros itens usam `#232960` e os 3 últimos
   `#152B65` (resíduo de dois widgets de acordeão empilhados no editor). Aqui os 6 usam
   `#232960`, senão a troca de tom no meio da lista lê como defeito.
6. **Faixa de logos de clientes.** O SVG tem muito respiro embutido; a original resolve com
   uma caixa fixa de 1129×194 e `object-fit: cover`. Reproduzido com `aspect-ratio` +
   `cover` no desktop e SVG inteiro abaixo de 800px (senão os logos ficam ilegíveis).
7. **Rodapé.** A original só mostra logo + copyright no desktop (os links de termos,
   privacidade e as redes sociais aparecem apenas no mobile). Aqui aparecem em todas as
   larguras, porque são links obrigatórios.
8. **Acessibilidade.** Adicionados skip-link, `focus-visible`, `alt`/`aria-hidden`,
   `prefers-reduced-motion`, `<details>` nativo no FAQ e JSON-LD (Organization, WebPage,
   SoftwareApplication, FAQPage).
9. **Números da seção de estatísticas.** Mantido o pareamento do **desktop** da original
   (14% demandas resolvidas · 9% tempo de resolução · 25% desgaste · 45% produtividade).
   O DOM da original lista os textos em outra ordem, o que induz a erro na leitura crua.

## Contraste: 5 falhas herdadas da original (decisão pendente do Victor)

A auditoria de contraste (WCAG AA) passou em 17 de 22 elementos. As 5 falhas usam
**exatamente as cores da página original** e foram mantidas para não descaracterizar
o visual. `landing-pages/GUIDELINES.md` §7 trata contraste como inegociável, então
ficam registradas aqui com a correção pronta:

| Elemento | Cor atual | Contraste | Mínimo | Correção sugerida |
|---|---|---|---|---|
| Overline "WHATSAPP COEX + API OFICIAL" | `#21CC78` sobre branco | 2,11:1 | 4,5:1 | `#0E8B4C` (4,6:1) |
| "organização" no H1 | `#21CC78` sobre branco | 2,11:1 | 3:1 (texto grande) | `#12A75C` (3,2:1) |
| "plataforma oficial do WhatsApp" no hero | `#21CC78` sobre branco | 2,11:1 | 4,5:1 | `#0E8B4C` |
| `comercial@gocxpress.com.br` | `#91999D` sobre branco | 2,90:1 | 4,5:1 | `#6B7275` |
| Selos "Api Oficial do…" | `#767D87` sobre `#F4F4F4` | 3,78:1 | 4,5:1 | `#666D77` |

Para aplicar, basta trocar `--green:#21CC78` por um tom mais escuro **só nos textos**
(o botão verde já passa: 6,91:1, porque o texto dele é escuro sobre o verde).

## Pesos

Os GIFs de plataforma somam ~6 MB (mesmo padrão já usado em `banimento-whatsapp-comercial`,
que serve os mesmos arquivos). Todos abaixo da dobra estão com `loading="lazy"`.
Se o Victor quiser reduzir, o caminho é converter para MP4 com `<video autoplay muted loop>`.

## Atualizacao de preco — 2026-08-28

Novo preco minimo de plano da Cxpress: **R$ 1.750**. A chamada de preco desta LP passou a
`Planos a partir de R$ 1.750`, **sem** mencao a quantidade de acessos — por decisao do usuario,
o detalhamento de acessos fica restrito a LP canonica de precos (`/planos`), que segue intacta
com "A partir de R$ 1.750 por mes, com 5 acessos de operador". Alteracao aplicada em bloco nas
9 LPs BR da Cxpress que citavam preco fora da `/planos`.

As LPs LATAM (`USD 260/mes`) e PT-PT (`295 EUR/mes`) **nao** foram alteradas: os valores oficiais
em USD/EUR ainda nao foram definidos e seguem defasados em relacao ao minimo BR.
