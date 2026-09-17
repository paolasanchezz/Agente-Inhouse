# LP Cxpress — Estudo Primeiro Contato Saúde

**Gerado em:** 2026-09-17
**Copy-fonte:** `copy.txt` (output de /lp-preparar)
**Região:** brasil (pt-BR) · **GTM:** GTM-T4XDWHL3
**Domínio-alvo:** `content.cxpress.io` (guarda-chuva migrado pro CI)

## Estrutura

- Nav sticky (logo + CTA âncora para o form)
- Hero: overline + H1 + sub + CTA "Baixar o estudo" + nota "Gratuito · 17 páginas · PDF", com o mockup do ebook (tablet) à direita e chip flutuante "1.932 interações"
- Números: 3 cards (92% contra 61% · 16% · 3x), um em gradiente navy→royal e dois em fundo tingido
- Tese: seção escura navy (única do corpo) com H2 + 3 parágrafos e arcos decorativos sangrados
- O que você vai encontrar: grid de 6 cards com check royal (GUIDELINES §8)
- Metodologia: bloco discreto em off-white, 3 fontes com limitação declarada, borda-topo laranja
- Para quem: seção de pausa, arejada, com o mascote Samir
- Form (`#baixar`): seção em gradiente, H2 à esquerda + embed do Jotform num card branco à direita. Linha de privacidade **abaixo do embed** (a copy diz "se você autorizar acima", então ela precisa vir depois do checkbox)
- Footer navy com logo reversed

## Direção de design

Referência pedida pelo usuário: `material.buzzmonitor.com/estudo-diversidade-2026` (source em `../../buzzmonitor/estudo-diversidade-2026/`). Reaproveitada a **linguagem visual e a arquitetura CSS** (nav sticky com blur, hero em 2 colunas com elementos flutuantes, cards de dado com forma geométrica no canto, seção escura de tese, CTA em 2 colunas com o form à direita, reveal por IntersectionObserver com stagger). Trocados paleta, tipografia e conteúdo pelos da Cxpress.

Paleta (GUIDELINES §1): navy `#232960` + royal `#4A69BD` + laranja `#EF863C` como acento de preenchimento. **Um único gradiente** (`135deg, navy → royal`), usado em 2 momentos: o primeiro card de número e a seção do form. Hero em tint chapado `#F7F9FF`.

Tipografia: Open Sans 700/800 (títulos) + Source Sans 3 400/600 (corpo). Sem Bitter.

## Decisões registradas (validar na revisão)

1. **Mockup do ebook (2026-09-17, enviado pelo usuário no chat):** substituiu a capa que eu tinha montado em CSS. Arquivo original tinha ~28% de margem transparente no topo e ~25% embaixo; recortado pelo bbox de conteúdo, redimensionado para 900px de largura e convertido para WebP (733KB → 97KB). Vive em `./assets/ebook-estudo-primeiro-contato-saude.webp`.
2. **Contraste do laranja:** `#EF863C` aparece só como preenchimento (arco decorativo da tese, borda-topo dos cards de metodologia). Nenhum texto laranja, nenhum botão laranja. Regra que já reprovou AA em LP desta marca.
3. **H1 descritivo (herdado da copy):** a `copy.txt` marca como sugestão que o H1 não lidera pela dor (GUIDELINES §5/§3). Não alterado aqui, é decisão de quem aprova a copy.
4. **Form na última seção (herdado da copy):** GUIDELINES §10 daria default de 2ª seção para material rico em tráfego frio. Mantida a ordem da copy (§9), com CTA no hero rolando até o form. Override documentável se o objetivo for volume.
5. **Quebra do H1 medida (GUIDELINES §21):** `max-width:15ch` dá 4 linhas com 18% de desequilíbrio; sem cap dá 3 linhas com 42%. Ficou o 15ch.
6. **Piso de tipografia mobile (§20):** corpo da metodologia e label do opt-in subiram para 17px em ≤640px.
7. **Manifest antigo:** `brand/cxpress/brand-manifest.json` ainda usa o formato `websites`, sem bloco `regions` nem `socials`. Por isso o JSON-LD saiu **sem `sameAs`** (LinkedIn/Instagram) e `home` veio de `websites.brasil`. Migrar o manifest da Cxpress para o formato `regions` resolve.

## Verificação feita

- em-dash: 0 (`—` e `&mdash;`)
- Fidelidade da copy: todo texto visível bate literal com `copy.txt`. Fora dela, apenas whitelist (labels de form, placeholders da copy, skip-link, aria-labels) e o chip "1.932 interações", que são fragmentos literais do SUB do hero
- SEO: canonical + x-default + description + robots + 10 tags `og:` + 4 `twitter:` + JSON-LD válido (Organization, WebPage, Article)
- GTM: 2 blocos, ID correto nos dois
- Sem overflow horizontal em 1440 e em 375; pisos de tipografia mobile OK
- 19 elementos `.reveal` aparecem ao rolar; fallback `<noscript>` presente; hero não depende de animação
- Logos e mascote carregam; logos SVG do brand não têm `<text>` vivo (§19)

## Estado

- [x] HTML gerado
- [x] OG image 1200×630 gerada em 2026-09-17 → `assets/og-estudo-primeiro-contato-saude.png` (47 KB). Feita do `og-template.html` com o overline e o H1 literais da copy
- [ ] Revisão (frontend-design review + web-design-guidelines) — rodar `/lp-revisar cxpress/estudo-primeiro-contato-saude`
- [x] Formulário integrado em 2026-09-17 — **mas com o form ERRADO, e isso está no ar.** Entrou o embed do Jotform `262104279010647`, mas esse form é da LP irmã `../video-atendimento/`: título "ASSISTA AGORA", botão "▶ Assistir agora", 5 campos (Nome, Empresa, E-mail corporativo, Cargo, WhatsApp), checkbox de **opt-out** e, em Configurações > Após o envio, redirect para `https://content.cxpress.io/video-atendimento-obrigado`. Ou seja: quem preencher na LP do estudo cai no vídeo e nunca recebe o PDF. Mudar o texto do botão no builder conserta aqui e **quebra** a `video-atendimento`. O certo é duplicar o form no Jotform (ID novo) com 3 campos, opt-in, botão "Baixar o estudo" e redirect para `content.cxpress.io/estudo-primeiro-contato-saude-confirmado`. Publicado assim por decisão explícita do Bruno em 2026-09-17, que vai mandar o ID novo em seguida; a troca é 1 linha no `<script src>` do embed + novo PR
- [ ] Página de obrigado — copy já preparada em `../estudo-primeiro-contato-saude-confirmado/copy.txt`, falta gerar o HTML
- [x] Publicado em 2026-09-17 via fluxo CI (manifesto de `content.cxpress.io` + PR + `lp-deploy.yml`)

## Pendências herdadas da copy

- Conferir o número de páginas do PDF (17 é estimativa e aparece no hero)
- Links primários dos benchmarks no PDF (a LP promete "com fonte em cada número")
- UTMs do CTA do e-mail apontando para esta URL
- Link direto do PDF no botão "Abrir o estudo" da página de obrigado

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
- `../../brand/cxpress/assets/mascot/samir-laptop.png` (seção "Para quem")
- `./assets/ebook-estudo-primeiro-contato-saude.webp` (mockup do ebook no hero)
- `./assets/og-estudo-primeiro-contato-saude.png` (OG image 1200×630, referenciada por URL absoluta no `<head>`)

> No preview local as logos do brand aparecem quebradas se você servir só a pasta da LP, porque `../../brand/` sobe acima da raiz servida. Sirva a raiz do repo (`py -m http.server` na raiz) ou confie no deploy, onde a `lp-publicar` reescreve os paths.

**Form provider:** Jotform, form `262104279010647` (integrado em 2026-09-17 — ver ressalva no Estado: é o form da `video-atendimento`, a ser trocado)
