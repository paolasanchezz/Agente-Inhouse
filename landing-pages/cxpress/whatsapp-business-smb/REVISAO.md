# Revisao LP — cxpress/whatsapp-business-smb

**Data:** 2026-07-24
**Auditores:** checks determinísticos (GTM, SEO, em-dash, assets, overflow responsivo) + verificação manual de fidelidade de copy

## Contexto da revisão

Esta LP é uma reconstrução, no nosso pipeline, do conteúdo integral de `home.cxpress.io/whatsapp-business-smb` (site GreatPages externo), a pedido explícito do usuário: "duplique essa landing mas aprimore o seu design de acordo com o que fizemos para clínicas... mantenha o conteúdo integral e original da LP". Design reaproveita o sistema visual corrigido em `banimento-whatsapp-clinicas` (fix de padding, badge Elife); conteúdo é transcrição literal da fonte (sem `/lp-preparar` via Notion — fonte foi uma página viva, extraída via inspeção de DOM).

## Aplicado automaticamente / verificado (0 críticos)

- [x] **Em-dash** — 0 ocorrências (`copy.txt` e `index.html`)
- [x] **GTM** — `GTM-T4XDWHL3` bate com a região (`brasil`), stamp gravado (`stamp_match: true`)
- [x] **SEO** — 1 description, 10 tags `og:`, 4 `twitter:`, 1 JSON-LD (parseia corretamente), 1 canonical
- [x] **Favicon** — aponta pro `logo-icon.png` do brand (path único, sem duplicação)
- [x] **Logo header/footer** — `href="https://home.cxpress.io"`, `target="_blank" rel="noopener"`, `aria-label` localizado
- [x] **Logo SVG web-safe** — Cxpress já documentado como OK (paths/outline, sem `<text>` vivo)
- [x] **Logo Elife (badge Quem Somos)** — corrigida desde a criação, mesma técnica validada em `banimento-whatsapp-clinicas` (crop + reconstrução de alfa). Badge renderiza 81×28px preenchendo 100% da altura do badge.
- [x] **Assets** — todos os 10 arquivos referenciados (7 brand + 3 LP-local) respondem HTTP 200 no build local do guarda-chuva
- [x] **Espaçamento hero→menu** — `.hero{padding:0}` aplicado desde a primeira versão (não uma correção posterior). Gap medido: 146px desktop.
- [x] **Grids responsivos** — `.destaque__grid` (2 col desktop / 1 col mobile), `.beneficios__grid` (3/1), `.prova__grid` (4/2/1) — todos confirmados via `getComputedStyle` em 1265px, 768px e 375px.
- [x] **Sem overflow horizontal** — confirmado em desktop (1265px) e tablet (768px) desde a primeira versão. **Mobile (375px) teve um bug encontrado e corrigido nesta revisão** — ver abaixo.

## Crítico encontrado e corrigido durante a revisão

- [x] **Overflow horizontal de 3px no mobile (375px)** — causa: removi o padrão de texto curto/longo do CTA do menu (`.navbar__cta-full` / `.navbar__cta-short`) que existia no template original, colocando só "Fale com um especialista" (24 caracteres) sem quebra — largo demais pro botão em telas de 375px, empurrando `scrollWidth` pra 378px. Fix: reintroduzido o padrão curto/longo já estabelecido no template-base, com "Fale conosco" como variante mobile (dentro do whitelist de "nav meta minimal", GUIDELINES lp-gerar — texto curto, não repete a copy literal, função idêntica ao CTA completo). Confirmado pós-fix: `scrollWidth == clientWidth == 375`.

## Fidelidade de copy — achado e corrigido durante a criação

- [x] **Heading inventado na seção PROVA** — ao montar o HTML, adicionei por engano um H2 "Resultados comprovados de atendimento com IA" que não existe na fonte (o `copy.txt` já registrava "sem headline própria na fonte", mas a instrução se perdeu na hora de escrever o HTML). Removido antes mesmo de rodar os testes; seção agora usa `aria-label` (não-visível, funcional) em vez de um H2 visível, preservando a acessibilidade sem inventar copy.

## Melhorias opcionais (0)

Nenhuma identificada — o design reaproveita componentes já validados (cards, grids, FAQ accordion) sem introduzir padrões novos que precisassem de ajuste fino.

## Nice-to-haves (1)

- [ ] A seção "Plataforma" tem 2 cards `feature--textonly` consecutivos (features 3 e 4, "Centralize os cadastros dos clientes..." e "Otimize a gestão de tickets") porque a fonte não tem imagem própria pra nenhuma das duas e a ordem do conteúdo não podia ser alterada (fidelidade). Visualmente aceitável, mas se o time quiser, dá pra gerar/produzir uma imagem nova pra uma delas no futuro pra alternar o ritmo imagem/texto.

## Decisão de design registrada (não é achado, é contexto)

Ao contrário de `banimento-whatsapp-clinicas` (hero como fundo de seção inteira + gradiente, adequado a uma foto rica), esta LP manteve o padrão "texto à esquerda + mockup em card à direita com sombra" (drop-shadow), porque o visual real da fonte é uma animação pequena do dashboard (604×340), não uma foto — um tratamento de fundo-com-gradiente ficaria esticado/pixelizado e não agregaria. Julguei que aplicar o padrão de card (já testado em 8+ LPs Cxpress) era a escolha de design mais criteriosa pra este conteúdo específico, mesmo mantendo a intenção de "design aprimorado" do pedido do usuário (correção de espaçamento, badge Elife corrigida, tipografia consistente).

## Próximos passos

- Publicar: `/lp-publicar cxpress whatsapp-business-smb content.cxpress.io`.
