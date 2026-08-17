# Revisão LP — buzzmonitor/buzzsummit-2026-indique-e-ganhe

**Data:** 2026-08-17
**Auditores:** revisão de design (convenção frontend-design review-only) + web-design-guidelines (fetch das guidelines externas falhou com 503; auditoria feita com base em WCAG 2.1 AA + conhecimento das Web Interface Guidelines) + verificações determinísticas (GTM, copy fidelity, SEO)

## Aplicado automaticamente (8 críticos)

- [x] **Contraste AA — `.evento-theme h3`**: cor `var(--accent)` (#FF7300) sobre card branco dava ~2,73:1 (texto grande precisa de 3:1). Trocado para `var(--primary-dark)` (#C7621E, ~4,05:1) e removido do gradiente de texto (o degradê tem uma ponta clara #FFB000 que reprova ainda mais, ~1,8:1).
- [x] **Contraste AA — `.funciona-card__num`**: mesmo problema (`--accent` sobre card claro `--light`). Mesma correção (`--primary-dark`, sem gradiente).
- [x] **Contraste AA — `.form-consent a`** (link "Política de privacidade" no form): `--accent` sobre card branco em texto pequeno (13,5px) precisa de 4,5:1, dava 2,73:1. Trocado para `var(--text)` (quase-preto, ~15:1).
- [x] **Contraste AA — `.form-row input/textarea:focus` (borda de foco)**: `--accent` contra fundo branco do input dava 2,73:1 (não-texto precisa de 3:1). Trocado para `var(--primary-dark)` (4,05:1).
- [x] **Contraste AA — `:focus-visible` (outline global)**: mesmo problema, `--accent` falha em fundos claros. Trocado para `var(--primary-dark)`, que passa 3:1 tanto em fundo claro (4,05:1) quanto escuro (4,26:1) — funciona nos dois contextos que a LP usa.
- [x] **Contraste AA — `.evento-chip:hover` (borda)**: `var(--primary)` (#EB7C2E) contra chip branco dava ~2,90:1, abaixo de 3:1. Trocado para `var(--primary-dark)`.
- [x] **OG image ausente (GUIDELINES §18)**: `og:image` apontava para `{{OG_IMAGE_PATH}}` sem arquivo correspondente. Gerada `assets/og-buzzsummit-2026-indique-e-ganhe.png` (1200×630, 80 KB) via Chrome headless a partir de um template com a identidade da LP (fundo escuro, degradê âmbar, logo). Fonte Bebas Neue não carregou no render headless (sem acesso a Google Fonts offline) — caiu no fallback sans-serif bold do sistema. Visualmente correto e on-brand, mas pode ser refeito com a fonte embutida se quiser pixel-perfect.
- [x] **`copy.txt` desatualizado vs. HTML**: as fusões de parágrafo e re-quebras de label feitas nas rodadas anteriores (pedido do usuário) nunca foram refletidas na copy-fonte. Sincronizado com notas `[REFLOW v2]` explicando cada mudança. Conferido palavra por palavra: nenhum texto foi cortado, reescrito ou adicionado além do já documentado (disclaimer de formulário e copyright, ambos já marcados como `[ADICIONADO]` desde a criação).

## Verificações que passaram sem achados

- **GTM**: container `GTM-WFJVK858` bate com a região Brasil (`<html lang="pt-BR">`). Selo `.tracking.lock` gravado.
- **Copy fidelity**: nenhum vazamento encontrado (sem pull-quote inventado, sem frase-âncora truncada, sem sinônimo cosmético, 0 em-dash no HTML renderizado).
- **SEO**: 1 description, 1 robots, 10 og:, 4 twitter:, 1 JSON-LD (parseia OK), 1 canonical. Todos dentro do mínimo exigido pelo GUIDELINES §15.
- **Multi-idioma**: LP única (sem irmãs `-es`/`-pt`), hreflang `x-default` presente e correto — nada a adicionar.

## Melhorias opcionais (2)

- [ ] **Logo do header/footer não linca para a home da marca (GUIDELINES §17)**: linca para `https://www.buzzsummit.com.br/` em vez de `https://buzzmonitor.com/`. Isso é **desvio intencional**, pedido explicitamente pelo usuário duas vezes nesta sessão — registrando aqui só para constar como exceção documentada à regra padrão, não como pendência a corrigir.
- [ ] **Nav some inteiro abaixo de 860px sem alternativa (menu hamburguer)**: em mobile/tablet estreito os links "Por que indicar / Quem indicar / O evento / Dúvidas" ficam inacessíveis via navegação (`display:none`), só dá pra chegar neles rolando a página. Não é falha de acessibilidade (nada fica invisível pra leitor de tela, o conteúdo continua no fluxo normal), mas é uma limitação de UX. Se quiser, dá pra adicionar um menu hamburguer depois.

## Nice-to-haves (1)

- [ ] OG image gerada com fonte fallback (não é Bebas Neue de verdade, ver nota acima). Refazer com a fonte embutida via `@font-face` + base64 se quiser fidelidade tipográfica total no preview de compartilhamento.

## Pendências já conhecidas (fora do escopo desta revisão, seguem no README.md)

- Arquivos de imagem originais muito pesados ainda na pasta `assets/` (`Buzzsummit_2025-4527.jpg` 21,5 MB, `Buzzsummit_2025-5454.jpg` 18,7 MB) — recomendado remover antes de commitar.
- Domínio de publicação ainda não decidido.

## Próximos passos

- Design aprovado? → `/lp-integrar-form buzzmonitor/buzzsummit-2026-indique-e-ganhe "{snippet}"`
- Rever mais algum ponto? → editar e rodar `/lp-revisar` novamente
