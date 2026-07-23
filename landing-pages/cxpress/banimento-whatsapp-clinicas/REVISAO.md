# Revisao LP — cxpress/banimento-whatsapp-clinicas

**Data:** 2026-07-22
**Auditores:** frontend-design (review mode) + web-design-guidelines + checks deterministicos (GTM, SEO, copy fidelity, logo regional, hreflang)

## Contexto da revisão

Esta LP é um clone quase literal de `landing-pages/cxpress/banimento-whatsapp/index.html` (mesmo CSS, mesma copy), já publicado e já revisado anteriormente. O delta desta LP é: (1) metadados de SEO apontando pro novo slug, (2) troca do asset visual do hero (GIF genérico → PNG estático de mockup, tema clínica). A revisão focou nesse delta + nos checks determinísticos completos.

## Aplicado automaticamente (0 críticos)

Nenhum crítico encontrado. Checks determinísticos, todos OK:

- [x] GTM — `GTM-T4XDWHL3` bate com a região (`brasil`), stamp gravado (`stamp_match: true`)
- [x] SEO — 1 description, 1 robots, 10 tags `og:`, 4 `twitter:`, 1 JSON-LD (parseia corretamente), 1 canonical
- [x] Em-dash — 0 ocorrências
- [x] Logo header/footer — `href="https://home.cxpress.io"` (bate com `brand-manifest.json > websites.brasil`), `target="_blank" rel="noopener"`, `aria-label` localizado
- [x] Logo SVG web-safe — Cxpress já documentado como OK (paths/outline, sem `<text>` vivo)
- [x] Fidelidade de copy — H1, frase de fechamento (FECHO) e todos os headings (h1-h3) idênticos byte-a-byte à referência (diff = vazio)
- [x] Hreflang — corretamente omitido. `banimento-whatsapp-clinicas` não é uma variante de idioma (é variante de segmento/público, PT-BR o tempo todo) — não entra na família hreflang de `banimento-whatsapp` / `banimento-whatsapp-pt`

## Melhorias opcionais (1)

- [ ] **`brand/cxpress/brand-manifest.json` está no formato antigo** (`websites`, não `regions`) — JSON-LD `Organization` sai sem `sameAs` (LinkedIn/Instagram regional). Pré-existente (mesmo gap na referência original), não introduzido por esta LP. Migrar o manifest da marca beneficiaria todas as LPs Cxpress, não só esta.

## Nice-to-haves (0)

Nenhum.

## Atualização 2026-07-22 (pós-publicação inicial) — hero substituído

- [x] **Imagem de hero definitiva**: o usuário enviou uma foto própria (via link do Google Drive) de uma médica de jaleco usando o WhatsApp no celular, com elementos ilustrativos de segurança (escudo, cadeado). Baixada, redimensionada pra 1080×810 e recomprimida em JPEG (~80KB, de 1.6MB original). Substitui o `mockup-plataforma-laptop.png` que era placeholder temporário. Arquivo: `assets/hero-clinica.jpg` (LP-local). Isso fecha as duas pendências anteriores (mockup reaproveitado + upscaling de 16%) — não se aplicam mais.
- [x] OG image dedicada — `assets/og-image.png` (1200×630), gerada via Chrome headless + `.claude/skills/lp-gerar/og-template.html`.

## Atualização 2026-07-22 (2ª rodada) — hero trocado de novo + integração com gradiente

- [x] **2ª foto do hero**: usuário enviou uma nova imagem (recepcionista de clínica ao telefone, usando WhatsApp no laptop) substituindo a 1ª foto. Redimensionada pra 1400×788, JPEG ~87KB.
- [x] **Tratamento visual pedido pelo usuário**: "integrar melhor com gradiente" — trocado o tratamento de card retangular + drop-shadow por sangria até a borda direita da viewport (`.hero__mockup{width:calc(100% + 110px)}` dentro de `.hero__visual{overflow:visible}`, clipado por `.hero{overflow:hidden}`) com `mask-image: linear-gradient(...)` esmaecendo a borda esquerda da foto (que já é clara/neutra) até transparente, misturando com o fundo branco da seção. Breakpoint mobile usa fade mais suave (a imagem não sangra, ocupa só a largura da coluna).
- **Verificação**: build local do guarda-chuva rodado (`build_umbrella.py`, 0 avisos novos) e servido via `python -m http.server` local; confirmado via `getComputedStyle` que o `mask-image` aplica corretamente nos dois breakpoints e que não há overflow horizontal (`document.documentElement.scrollWidth == clientWidth`) em desktop (1265px) nem mobile (375px). Não foi possível tirar screenshot nesta sessão (painel do navegador indisponível) — verificação foi via computed styles + dimensões, não visual direta.

## Atualização 2026-07-22 (3ª rodada) — imagem como background da seção + correção de padding

- [x] **Imagem como fundo da seção hero** (pedido do usuário): reestruturado de "imagem em coluna própria com sangria" pra "imagem cobrindo a seção inteira" — `.hero__bg` (`<img>` `position:absolute;inset:0;object-fit:cover;object-position:78% center` desktop / `68% center` mobile) + `.hero__scrim` (`absolute;inset:0`, gradiente branco por cima). Removidos `.hero__visual`, `.hero__pills` (pills decorativas não faziam mais sentido atrás de uma foto cheia) e a antiga `.hero__mockup`. `.hero__inner` virou single-column (`.hero__content{max-width:600px}`), sem grid de 2 colunas.
- [x] **Gradiente desktop**: horizontal, esquerda→direita (`rgba(255,255,255,.97)` → transparente aos 76%), protegendo o texto e deixando a foto nítida à direita. **Gradiente mobile**: vertical (topo→base), porque o texto ocupa a largura toda da tela nesse breakpoint e um fade lateral não sobra espaço pra funcionar.
- [x] **Verificação de contraste (rigorosa, via canvas)**: como não há screenshot disponível nesta sessão, simulei o `object-fit:cover` + gradiente em canvas (drawImage com crop calculado manualmente a partir de `object-position`, depois composição alpha do scrim) e amostrei pixels nos 4 cantos do H1 e do subtítulo. Resultado: contraste texto/fundo entre **12.4:1 e 13.4:1** em desktop e mobile — folga grande sobre o mínimo WCAG AA (4.5:1). Também confirmado: sem overflow horizontal em nenhum dos dois breakpoints.
- [x] **Correção do espaçamento menu→H1** (pedido do usuário: "espaço em branco grande demais"): causa raiz identificada — regra genérica `section{padding:130px 0}` (destinada às demais seções da LP) também batia na `.hero` (é um `<section>`), empilhando com o padding do `.hero__inner`. Fix: `.hero{padding:0}`, deixando só o `.hero__inner` controlar o respiro. Gap menu→H1 medido: **276px → 146px** (desktop), **154px** (mobile). Reduzir só o padding do `.hero__inner` (rodada anterior, 110px→64px) não teria resolvido sozinho — a regra genérica de `section` era a maior fatia do problema.

## Atualização 2026-07-22 (4ª rodada) — copy pro público de clínicas + logo Elife corrigida

- [x] **Copy**: "clientes" → "pacientes" (sub do hero), "cliente" → "paciente" (card "Histórico que não se perde"), "agenda do cliente" → "agenda do paciente" (Fecho). H1 sem ponto final. `copy.txt` atualizado em paralelo (fonte-verdade não pode divergir do HTML).
- [x] **Logo Elife (badge Quem Somos) corrigida**: causa raiz do "mal diagramado" identificada por análise de pixel — `brand/cxpress/assets/plataforma/elife-logo.png` (asset compartilhado, usado por 8 LPs Cxpress) tem alpha=255 uniforme em todo o canvas (250×140), mas o wordmark real só ocupa as linhas 0–77 (55% da altura); o resto é um preenchimento cinza-claro opaco (RGB 244,244,244) que não é transparente. Com `.qs-badge{align-items:center}`, esse "espaço morto" era centralizado junto com a logo, empurrando o wordmark visível pra cima e fazendo-o parecer pequeno/desalinhado em relação ao texto "Um produto" e às duas badges de ícone SVG vizinhas (30×30px). Fix: reconstrução de canal alfa via unmultiply (`alpha = (244 - luminância) / (244 - 100)`, onde 100 é o tom mais escuro do traço) + crop no bbox real (235×81, contra os 250×140 originais) → novo arquivo **LP-local** `assets/elife-logo-badge.png` (não sobrescrevi o asset compartilhado pra não impactar as outras 7 LPs sem revisão — ver pendência abaixo). Badge `.qs-badge img` ajustado de `height:24px` pra `height:28px` pra ocupar visualmente o mesmo peso das duas SVGs.
- **Verificação**: confirmado via canvas (`drawImage` + `getImageData`) que o canto da imagem renderiza `rgba(0,0,0,0)` (transparência real, não só branco) e um ponto do traço renderiza `rgba(100,100,100,220)` (opaco). Badge renderiza a 81×28px preenchendo 100% da altura do badge, `verticalCenterOffset: 0`.
- **Não foi possível inspecionar a referência pedida** (`https://home.cxpress.io/app-whatsapp`, badge "Um produto Elife"): a página não expõe nenhum `<img>` nem `<svg>` no DOM (0 de cada no documento inteiro) — o logo lá provavelmente é renderizado via lazy-load/background-image que não disparou na automação, ou vive num contexto inacessível. Sem screenshot disponível nesta sessão pra inspeção visual direta. O fix aplicado foi baseado em diagnóstico direto do bug (não em replicar o layout da referência).
- **Pendência sinalizada como tarefa separada**: o mesmo bug de transparência no `elife-logo.png` compartilhado provavelmente afeta as outras 7 LPs Cxpress que o referenciam (`atencion-digital-latam`, `atendimento-clinicas`, `atendimento-digital`, `banimento-whatsapp`, `banimento-whatsapp-latam`, `coex-whatsapp`, `coex-whatsapp-latam`). Corrigir o asset compartilhado beneficiaria todas, mas é uma mudança de blast-radius maior que não estava no escopo pedido aqui.

## Próximos passos

- Design aprovado, form Jotform próprio (`261027639617663`), hero (foto como fundo de seção + gradiente + espaçamento corrigido), copy ajustada pro público de clínicas e logo Elife corrigida — tudo integrado.
- Publicar atualização: `/lp-publicar cxpress banimento-whatsapp-clinicas content.cxpress.io`.
