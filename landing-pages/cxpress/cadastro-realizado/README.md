# LP Cxpress — cadastro-realizado

Thanks page de confirmação de cadastro. Recriação, dentro do nosso pipeline (`content.cxpress.io`),
da página `home.cxpress.io/obrigado` — hoje hospedada no site institucional em GreatPages, fora do
pipeline de LPs e sem acesso de edição direto por aqui.

**Gerado em:** 2026-08-11
**Redesenhado em:** 2026-08-13 (mascote + composição; copy inalterada)
**Copy-fonte:** transcrição literal de `home.cxpress.io/obrigado`, ver `copy.txt`.

## Redesign 2026-08-13

A pedido do usuário, a página ganhou o mascote e o acabamento da referência
(`home.cxpress.io/obrigado`), mantendo o pixel (GTM `GTM-T4XDWHL3`) e **sem** o link de WhatsApp.
Copy 100% preservada, nenhum bloco novo de texto (GUIDELINES §9: copy dita estrutura).

O que mudou:

- **Medalhão do mascote** — Samir joinha dentro de um disco âmbar (`overflow: hidden` + `bottom: -4%`),
  com anel externo e selo de check laranja sobreposto. O disco recorta o corte reto da base da arte;
  sem isso sobra uma linha dura de hoodie sob o mascote.
- **Layout de altura cheia** — `body` flex com `min-height: 100dvh` e seção centralizada verticalmente.
  A página tem 2 linhas de copy; sem isso vira uma faixa curta com o rodapé colado no topo da tela.
- **Fundo** — gradiente branco → azul muito claro (`#E9F1FF`), no lugar do branco chapado, ecoando a
  referência. Pílulas decorativas ficaram mais discretas e encolhem abaixo de 720px.
- **Tipografia** — H1 maior (`clamp(29px, 4vw, 46px)`) com `text-wrap: balance`.
- **Animação** — entrada do medalhão (sobe + assenta) e traço do check via `stroke-dashoffset`.
  Mesmo fallback triplo do reveal já usado nas outras LPs; `prefers-reduced-motion` zera tudo.

### Asset do mascote — cópia otimizada local (deliberado)

`brand/cxpress/assets/mascot/samir-joinha.png` tem **2,5 MB** (1536×1024). Numa página cujo único peso
é essa imagem, isso domina o LCP. A LP referencia `./assets/mascot/samir-joinha-web.png`
(**84 KB**, 760×644): recorte no bounding box do conteúdo (`126,0,1334,1024`), resize LANCZOS e
quantização FASTOCTREE em 200 cores com alpha preservado. Sem perda visual perceptível no tamanho
de exibição (máx. 320px).

Como o `build_umbrella.py` resolve `brand/` primeiro e só depois `{lp}/assets/`, o nome
`samir-joinha-web.png` (que **não** existe no brand) garante que a cópia local é a usada. Validado:
`dist/assets/cxpress/mascot/samir-joinha-web.png` = 84 KB.

Se outra LP Cxpress quiser o mesmo tratamento, promover esse arquivo pro brand é a evolução natural,
mas isso mexeria no asset de 12 LPs que hoje apontam pro PNG pesado, então ficou fora deste escopo.

## Origem e diferença deliberada da fonte

A pedido do usuário, dois elementos da página original foram **removidos**, não apenas adaptados:

1. O botão "Falar no WhatsApp" (link `https://api.whatsapp.com/send?phone=551150395028&...`).
2. O texto de apoio "Caso prefira, clique no botão abaixo do Whatsapp e já seja atendido. (Nossa
   equipe atende de segunda a sexta das 9h às 18h.)" — removido junto com o botão, seguindo o
   precedente de `video-atendimento-obrigado` (2026-08-03): sem o botão, o texto prometia um
   contato sem caminho.

O menu de Soluções e o rodapé extenso (Termos, Documentações, redes sociais) do site institucional
**não foram replicados** — decisão explícita do usuário de seguir o padrão simples já usado nas
thanks pages do nosso pipeline (logo no header + rodapé mínimo), em vez de reproduzir o site
completo.

## Estrutura

- CONFIRMAÇÃO (medalhão do mascote com selo de check + H1 "Cadastro realizado com sucesso." + subtítulo)
- FOOTER (mínimo)

## Estado

- [x] HTML gerado
- [x] Revisão — ver `REVISAO.md` (1 crítico aplicado: logo faltando no footer)
- [x] Redesign com mascote (2026-08-13)
- [x] Publicado — https://content.cxpress.io/cadastro-realizado (redesign no ar em 2026-08-13, PR #283)

## Exceções deliberadas às GUIDELINES (precedente: video-atendimento-obrigado / conheca-a-cxpress-confirmado)

- **`noindex, follow`**: página pós-ação; o Lighthouse SEO do lp-publicar vai apontar "is-crawlable"
  como falha — esperado, não "consertar".
- **Sem OG image, sem OG/Twitter/JSON-LD e sem placeholders `{{DOMAIN}}`**: ninguém compartilha esta
  URL.
- **Sem estrutura mínima de LP** (§6): não há form nem captação aqui, é só confirmação.

## Notas

- GTM injetado: `GTM-T4XDWHL3` (região brasil, mesmo container das demais LPs Cxpress BR).
- Ainda não se sabe qual formulário do site institucional redireciona para esta página — a URL de
  destino real (`content.cxpress.io/cadastro-realizado`) precisa ser configurada onde quer que o
  form aponte hoje para `home.cxpress.io/obrigado`, se a intenção for substituir o destino em produção.

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
- `./assets/mascot/samir-joinha-web.png` (medalhão — cópia otimizada local, ver acima)
