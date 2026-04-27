# Revisão LP — buzzcreators/vendendo-com-creators

**Data:** 2026-04-27
**Auditores:** frontend-design (review mode) + ajustes solicitados pelo usuário em review

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

Renderizados literalmente no HTML conforme briefing. Substituir antes do deploy:

- `[X] vagas presenciais` (HERO label)
- `[NOME DO MENTOR] — [cargo / posição atual]` (SPEAKER name)
- `[1-2 frases sobre autoridade...]` (SPEAKER bio)
- `[Foto opcional...]` (SPEAKER photo note)

## Próximos passos

- Design aprovado pelo Victor → `/lp-integrar-form buzzcreators/vendendo-com-creators "<jotform-snippet>"` (snippet já fornecido: `https://form.jotform.com/jsform/260213440661648`)
- Após integração → `/lp-publicar buzzcreators vendendo-com-creators`
