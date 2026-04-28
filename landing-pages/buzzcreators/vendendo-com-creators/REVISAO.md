# Revisão LP — buzzcreators/vendendo-com-creators

**Data:** 2026-04-27
**Auditores:** frontend-design (review mode) + ajustes solicitados pelo usuário em review

---

## Iteração 2 — 2026-04-28 (rodada de melhorias do Victor)

Aplicado direto no source (não passou por `/lp-revisar`). Pendente `/lp-publicar buzzcreators vendendo-com-creators webinar.buzzmonitor.com` para sincronizar com a sibling guarda-chuva e fazer deploy.

### Assets substituídos
- [x] `assets/buzzcreators/logo-full-color.svg` — substituído pela nova versão do brandbook (`logo-colorida.svg` da pasta `Downloads/buzzcreators logo/`, renomeado mantendo o nome original do projeto)
- [x] `assets/buzzcreators/logo-icon.png` — substituído pelo `favicon.png` novo do brandbook
- [x] `assets/buzzcreators/bruno-filho.png` — NOVO (foto do speaker, formato circular renderizado via CSS)

### Mudanças de conteúdo no `index.html`
- [x] **Vagas no hero**: `[X] vagas presenciais` → `Apenas 80 vagas presenciais`
- [x] **Hook ganha dado de mercado**: callout com `53% / 48%` (YOUPIX/Nielsen 2025) reforçando a dor do ROI
- [x] **Benefícios reformatados**: grid 3-col (`.beneficios__grid` com `.benefit-card`) → lista vertical (`.beneficios__list`) espelhando o estilo da `.problema__list`. Adicionado CTA laranja `Quero estar lá dia 20/05` ao final da seção
- [x] **Speaker preenchido**: Bruno Filho — Coordenador de Novos Negócios Buzzcreators, com bio real. Foto agora é circular (CSS: `aspect-ratio:1/1` + `border-radius:50%` + `object-fit:cover`). Removido `<p class="speaker__photo-note">` (placeholder não é mais necessário)
- [x] **Seção PROVA substituída**: removida "Por que confiar no método" (3 stats + nota de microinfluenciadores) → nova seção `.video-buzzcreators` com H2 "Conheça o Buzzcreators", lead institucional e iframe responsive 16:9 do YouTube (`nBK4ehM0YLo`)
- [x] **Headline do CTA final**: `Quatro horas presenciais sobre o que separa influência que viraliza de influência que vende.` → `Dê o próximo passo para obter ROI com creators`
- [x] **Footer**: `© 2026 Buzzcreators · Grupo Elife · comercial@buzzcreators.com.br` → `© 2026 Buzzcreators · Buzzmonitor · eventos@buzzmonitor.com.br`

### CSS novo
- `.hook__stat` + `.hook__stat-source` (callout laranja com border-left)
- `.beneficios__list` + `.beneficios__list .check` + `.beneficios__cta` (lista vertical com checks verdes; CTA centralizado)
- `.video-buzzcreators` + `.video-buzzcreators__lead` + `.video-buzzcreators__embed` (iframe responsive 16:9 com shadow + border-radius)
- `.speaker__photo` reescrito (era placeholder dashed 3:4, virou container circular 240px com `<img>` interno)

### CSS removido (dead code)
- Bloco completo `.prova` / `.prova__inner` / `.prova h2` / `.prova__intro` / `.prova__stats` / `.stat` / `.stat__num` / `.stat__label` / `.prova__note` e media query mobile da seção. A seção foi totalmente substituída pelo vídeo.
- `.beneficios__grid` / `.benefit-card` / `.benefit-card .check` / `.benefit-card p` e media queries de 920px/600px mantidos no CSS por enquanto (podem ser limpos numa próxima iteração se confirmado que não há reuso).

### CSP YouTube
Já permitido no `vercel.json` da sibling (`frame-src ... https://www.youtube.com`). Sem ajuste necessário.

### Próximo passo
- [ ] Rodar `/lp-publicar buzzcreators vendendo-com-creators webinar.buzzmonitor.com` para sincronizar sibling + deploy guarda-chuva preservando as outras 2 LPs Buzzmonitor.

### Iteração 2.1 — ajustes editoriais sobre a Iteração 2

- [x] **Checks da seção benefícios trocados de verde para roxo escuro** — `color: var(--c-success)` + `background: rgba(34,197,94,0.15)` virou `color: var(--c-purple-dark)` + `background: rgba(58,22,82,0.12)`. Motivo: verde sobre fundo `peach` (#fff4ec) não harmonizava com a paleta brand (a marca é roxo + laranja). Roxo escuro mantém alternância de cor entre seções e integra melhor.
- [x] **Reordenação de seções pós-form** — nova ordem: hero → hook → problema → beneficios → speaker → cta-banner → para-quem → **cta-final (form)** → **urgencia** → **video-buzzcreators**. A urgência agora atua como "segunda chance" para quem rolou sem converter, e o vídeo institucional fecha a página como reforço de marca. Antes, urgência vinha pré-form e o vídeo ficava no meio (depois do speaker, no slot da antiga seção `.prova`).

### Iteração 2.4 — remover PROBLEMA + benefícios sobre branco

- [x] **Seção `.problema`** ("Por que a maioria das marcas ainda não vende com creators?") **removida** do HTML e do CSS (dead code purgado: `.problema`, `.problema__inner`, `.problema h2`, `.problema__list`, `.problema__list li/.x-mark`, `.problema__conclusion` — ~50 linhas).
- [x] **`.beneficios`** ganhou cores da seção `.problema`: `background: var(--c-white)` (era `var(--c-peach)`); removidos os 2 radial-gradients do `::before`. Visual mais limpo, sem competir com a seção `.cta-banner` (mesh) que vem depois. Hierarquia agora flui hero → hook (lavender) → benefícios (branco) → speaker (branco) → cta-banner (mesh).
- [x] HTML compacto em 13 linhas; CSS em ~50 linhas.

### Iteração 2.2 — bold dos checks + form como cartão "completo" + endereço

- [x] **Checks da seção benefícios → roxo sólido com check branco** — `background: rgba(58,22,82,0.12)` + `color: var(--c-purple-dark)` (roxo translúcido pareceu cinza no fundo peach) virou `background: var(--c-purple-dark)` + `color: var(--c-white)` + `box-shadow: 0 2px 6px rgba(58,22,82,0.20)`. Visualmente vira "botões redondos roxos com check branco" — mais brand, mais bold, distingue claramente do fundo.
- [x] **H2 do CTA final movido pra DENTRO do card branco do form** — `<h2>` saiu do `.cta-final__inner` direto e passou a ser o primeiro filho de `<div class="form jotform-embed">`. Renomeado para `class="form__title"` (cor roxo escuro, centralizado, font-size `clamp(26px, 3.6vw, 38px)`). O card cresceu de `padding: 16px` para `padding: 56px 48px 36px` (mobile: `36px 22px 24px`). Visual: o card branco agora "engloba" título + form como uma peça única — mais peso visual, mais convidativo.
- [x] **Bloco de endereço + botão Google Maps na seção CTA final** — após o card do form, novo `<div class="cta-final__location">` com label "Onde acontece", endereço completo do Espaço Paulista (Av. Paulista, 807 — 17º Andar) e CTA secundário (`<a class="cta-secondary">`) linkando para o pin no Google Maps (URL CID original do usuário). Botão tem ícone SVG inline de pin geográfico, fundo branco com border roxo escuro 2px, hover invertido (preenche roxo + texto branco). Abre em nova aba (`target="_blank" rel="noopener noreferrer"`).

### Pendência fora do escopo do host (CSS não controlável)

- [ ] **Botão de submit do Jotform em roxo da marca** — o form embed renderiza dentro de um `<iframe>` cross-origin, então o botão CTA do form NÃO pode ser estilizado pelo CSS desta LP. O `<title>` do iframe atualmente é `BR | MKT | LPs - Buzzcreators Evento Presencial [CTA Cinza]` — o sufixo `[CTA Cinza]` indica que provavelmente já existem variantes desse mesmo formulário no Jotform com outras cores de CTA. Caminho:
  1. Verificar no painel Jotform se existe versão com sufixo `[CTA Roxo]` (ou similar) — se sim, basta trocar o ID `260213440661648` na linha do `<script>` do `index.html` para o ID da versão roxa e re-rodar `/lp-publicar`.
  2. Se não existir, duplicar o form atual no Jotform, customizar o botão de submit para `#3a1652` (roxo escuro Buzzcreators) ou `#6a3895` (roxo médio), salvar com novo nome e usar o ID novo aqui.

---

## Aplicado automaticamente (3 críticos)

- [x] **Logo crashada** — path relativo `../../brand/...` resolvia para `/landing-pages/brand/...` (não existia, profundidade real é 3). Corrigido para `../../../brand/...` no `<link rel="icon">` e no `<img src>` do header. Logo agora carrega (300px natural width).
- [x] **Ordem das seções** — `HOOK` veio em primeiro lugar antes do `HERO`, invertendo a hierarquia narrativa. Reordenado: HERO agora é primeira seção, HOOK virou segunda.
- [x] **Excesso de branco / paleta monocromática** — todas as seções não-dark eram brancas ou off-white cinza. Aplicada paleta de fundos brand-aligned em alternância:
  - Hero: branco (clean §3)
  - Hook: lavanda `#f4eefa`
  - Problema: branco
  - Benefícios: pêssego `#fff4ec` + radial sutis
  - Speaker: branco
  - Prova: lavanda `#f4eefa` + radial roxo
  - CTA Intermediário: mesh gradient fluido (ver abaixo)
  - Para Quem: branco
  - Urgência: roxo escuro `#3a1652` (dark, §8)
  - CTA Final: lavanda saturada `#ebddf5` + radial laranja/roxo

- [x] **Gradient CTA Intermediário** — antes era `linear-gradient` rígido. Substituído por **mesh gradient fluido** com 5 radial-gradients sobrepostos (laranja, roxo, laranja escuro, roxo escuro, roxo médio em camadas), sobre base `#2a0e3d`. Adicionada animação `meshFlow` 22s com `prefers-reduced-motion` fallback. Textura de pontos com `mix-blend-mode: overlay` por cima.

## Auditoria GTM

- **Região detectada:** brasil (slug sem sufixo + `<html lang="pt-BR">`)
- **Container esperado por `tracking.json`:** null (Buzzcreators tem `tracking.json` todo null — pendência futura da marca)
- **Container injetado:** `GTM-WFJVK858` (Buzzmonitor Brasil)
- **Severidade:** MELHORIA (estado "Presente, ID qualquer" + "esperado null" pela tabela do skill)
- **Decisão:** **Configuração INTENCIONAL** — pedido explícito do briefing original ("utilize o GTM de Buzzmonitor Brasil nessa página"). Não corrigir. Documentado também no README.md e na página de copy do Notion.

## Melhorias opcionais (5)

Para o Victor decidir. Aplicar via Edit manual ou rodar `/lp-revisar` novamente.

- [ ] **Contraste WCAG AA do CTA principal** — branco `#ffffff` sobre `#ff8119` ≈ 2.3:1. AA Normal exige 4.5:1. Brand-manifest da Buzzcreators **explicitamente endossa** "branco sobre laranja para CTAs" (texto bold large), mesmo aceitando ~3.5:1. Recomendação se quiser passar AA: trocar texto para `var(--c-purple-dark)` (~7:1) — mantém impacto, fica mais legível em monitores não-calibrados. **Decisão atual: manter conforme brand override.**

- [ ] **Repetição "Quero participar" em 4 CTAs** — header, hero, banner intermediário, form button. Bom para conversão; screen readers anunciam 4 vezes idêntico. Sugestão opcional: `aria-label` diferenciado nos secundários (ex: header="Quero participar — pular para inscrição").

- [ ] **`.speaker__name` como `<p>`** — semanticamente poderia ser `<h3>` para entrar no outline da página. Cosmético — visualmente já tem peso de heading.

- [ ] **Pulse animation infinita do dot no overline do hero** — apropriada para evento iminente, mas pode distrair em sessão longa. Opcional: limitar `animation-iteration-count` ou parar após 12s.

- [ ] **Footer minimalista** — uma linha só. Para LP B2B com captura de lead poderia incluir link discreto para política de privacidade (LGPD). Opcional.

## Nice-to-haves (3)

Estilístico. Ignorar é aceitável.

- [ ] Logo no header linka `#topo` (hero) — comportamento intencional ("logo = oferta principal"). Alguns esperam scroll para 0,0.
- [ ] `.urgencia__list li` com `backdrop-filter: blur(4px)` — elegante mas adiciona overhead de paint. Primeiro candidato a remoção se PageSpeed mobile vier abaixo de 90.
- [ ] `alert()` no submit do form mock — só aparece se alguém clicar antes da integração real. Será trocado em `/lp-integrar-form` de qualquer forma.

## Pendências de copy (placeholders)

Todos resolvidos na Iteração 2 (2026-04-28):

- [x] `[X] vagas presenciais` → `Apenas 80 vagas presenciais`
- [x] `[NOME DO MENTOR] — [cargo / posição atual]` → `Bruno Filho — Coordenador de Novos Negócios Buzzcreators`
- [x] `[1-2 frases sobre autoridade...]` → bio real do Bruno Filho
- [x] `[Foto opcional...]` → `bruno-filho.png` (circular, real)

## Próximos passos

- [x] Form Jotform integrado (`260213440661648`)
- [x] Publicada em `https://webinar.buzzmonitor.com/vendendo-com-creators` (sibling guarda-chuva `buzzmonitor-lp-monitoramento-concorrentes`, sem quebrar as 2 LPs Buzzmonitor existentes)
- [ ] Preencher placeholders de copy (`[X] vagas`, `[NOME DO MENTOR]`, etc) e re-rodar publicação
- [ ] PageSpeed manual em https://pagespeed.web.dev/

## Anomalia de processo (2026-04-27)

`/lp-publicar` v1.4.0 ainda assume **1 sibling = 1 projeto = 1 LP**, mas o domínio `webinar.buzzmonitor.com` segue padrão **multi-LP em projeto guarda-chuva** (uma LP por subpasta do mesmo sibling). Esta entrega foi consolidada manualmente nesse padrão:

1. Source ajustado pra usar `./assets/buzzcreators/...` (LP-local com namespace de marca, evitando colisão com `/assets/logos/logo-icon.png` da Buzzmonitor).
2. LP integrada em `buzzmonitor-lp-monitoramento-concorrentes/vendendo-com-creators/`.
3. Re-deploy do projeto guarda-chuva (`prj_bqOBy4RXCnPFu8Fn7csQ6wzyjwb6`).
4. Projeto Vercel novo (`buzzcreators-lp-vendendo-com-creators`) que foi criado no primeiro deploy ficou órfão — remover manualmente via Dashboard.

**Followup recomendado para a skill:** documentar o padrão multi-LP guarda-chuva. O Passo 0 deveria detectar que o domínio passado já está atribuído a outro projeto e propor consolidar lá em vez de criar projeto novo. Ver `lp-publicar/SKILL.md` v1.4.0 Passo 0 e Passo 1.
