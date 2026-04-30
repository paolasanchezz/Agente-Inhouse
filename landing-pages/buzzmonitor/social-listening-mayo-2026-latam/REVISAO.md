# Revisão LP — buzzmonitor/social-listening-mayo-2026-latam

**Data:** 2026-04-29
**Auditores:** frontend-design (REVIEW ONLY mode) + lp-revisar Passo 3.6 (auditoria de fidelidade da copy)
**Versões das skills:** lp-gerar 1.5.0, lp-revisar 1.4.0 (ambas bumpadas neste round em resposta ao incidente — ver CHANGELOG)

## Aplicado automaticamente (9 críticos/melhorias)

### Críticos — fidelidade da copy (Passo 3.6, novo na lp-revisar 1.4.0)

- [x] **Cierre H2 — frase-âncora truncada.** Linha 1042. HTML dizia `"…sino las que mejor escuchan"`. Restaurado para o literal da `copy.txt`: `"…sino las que mejor entienden lo que se dice de ellas"`. Mantida a tag rotacionada com a palavra `entienden`.
- [x] **Cierre `<p class="question">` inventado.** Linhas 1044-1046 (HTML antigo). Texto `"Sobran datos. Falta lectura. Vamos a leer juntos el 28 de Mayo."` não existia em `copy.txt`. Removido. Substituído por CTA literal `"Quiero inscribirme gratis"` da copy (cierre tem CTA na copy original).
- [x] **Pull-quote inventado em "Para Quien".** Linhas 1026-1032 (HTML antigo). `<aside class="for-quote">` com `"Si tu marca existe en redes sociales, alguien ya está hablando de ella…"` não existia em `copy.txt`. Bloco substituído por composição geométrica decorativa sem texto (`<aside class="for-art">` com círculos concêntricos em gradient da marca).
- [x] **5 em-dashes adicionados ao body (regras-anti-ia.md tolerância zero).** Substituídos:
  - Linha 858 (problema item 2): `"…quejas recurrentes — todo pasa…"` → `"…quejas recurrentes, todo pasa…"`
  - Linha 876 (problema item 4): `"…se mueven primero — tú reaccionas…"` → `"…se mueven primero. Tú reaccionas…"`
  - Linha 902 (diff-art kicker): `"No es solo monitorear redes sociales — es entender…"` → `"No es solo monitorear redes sociales. Es entender…"`
  - Linha 929 (beneficio 1): `"…en conversaciones digitales — más allá del volumen."` → `"…en conversaciones digitales, más allá del volumen."`
  - Linha 1097 (form-success): `"(Demo — formulario real…)"` → `"(Demo: formulario real…)"`
  - Linha 17 (og:title): `"Marcas y Agencias — Webinar Buzzmonitor"` → `"Marcas y Agencias · Webinar Buzzmonitor"`
  - Linha 770 (aria-label header): `"Buzzmonitor — página inicial"` → `"Buzzmonitor · página inicial"`
- [x] **Punchline de marketing inventada.** Linha 1058. `"Sin spam, sin enredos."` removido — não estava em `copy.txt` e não é boilerplate compliance. Mantido apenas o texto factual `"Tu inscripción te garantiza el acceso al evento en vivo."`

### Críticos — sinônimos cosméticos

- [x] **Hero H1 reescrita parcialmente.** Linha 787. `"cómo usar las redes sociales"` → `"cómo utilizar las redes sociales"` (literal de `copy.txt`).
- [x] **Hero SUB com pontuação reestruturada.** Linhas 789-791. `"…sobre las marcas. La mayoría de equipos…"` → `"…sobre las marcas, pero la mayoría de equipos…"` (vírgula + conjunção literal).

### Melhorias — design / a11y aplicadas

- [x] **Beneficios check icon — gradient rosa→laranja → roxo primary.** Linha 494. `.l-item .check { background: var(--grad-hot) }` → `background: var(--c-primary)`. Cria contraste real com o X rosa do problema (vocabulário visual problema↔benefício per GUIDELINES §8). Antes ambos usavam o mesmo gradient e o olho não distinguia.
- [x] **Header indicator reduzido.** Linha 770-771. `"En vivo · 28 May"` → `"En vivo"` (data já aparece 2× na primeira dobra: hero-eyebrow + ticket card; GUIDELINES §3 diz "indicador é resumo discreto, não repositório de dados").
- [x] **Reveal on scroll com fallback robusto.** Adicionado `<noscript><style>.reveal{opacity:1!important;transform:none!important}</style></noscript>` no `<head>` (linha 24). Antes, se JS bloqueasse/falhasse + usuário com `prefers-reduced-motion: no-preference`, conteúdo abaixo da dobra ficava `opacity:0` invisível (GUIDELINES §4 explícito: texto JAMAIS invisível esperando animação).
- [x] **`role="marquee"` deprecated removido do ticker.** Linha 822. Atributo deletado, semantic do `<div>` basta.

## Melhorias opcionais (não aplicadas)

Para o usuário decidir. Aplicar via Edit manual ou pedir `/lp-revisar` novamente.

- [ ] **Hero H1 com 3 spans coloridos+itálicos.** `Social Listening` em gradient + `detectar oportunidades` em itálico rosa + `anticipar crisis` em itálico rosa. H1 tem ~25 palavras com muita marcação — funciona, mas é denso. Sugestão opcional: manter só `<span class="grad">Social Listening</span>` em gradient e remover os dois `<span class="ital">` para limpar — o H1 já tem peso visual suficiente.
- [ ] **Disclaimer compliance do form (linha 1100).** `"Al registrarte aceptas recibir comunicaciones de Buzzmonitor sobre el webinar y materiales relacionados."` é boilerplate aceitável para LP de evento (whitelist Passo 4.2 da lp-gerar), mas não está em `copy.txt`. Validar com o time legal LATAM se o texto exato é compliance OK ou se precisa adaptar.
- [ ] **Email de contato `eventos@buzzmonitor.com` (linha 1120).** Endereço não-validado. Confirmar com a equipe Buzzmonitor LATAM se essa é a caixa correta ou trocar para o email regional oficial.

## Nice-to-haves (opcionais, estilísticos)

Estilístico. Ignorar é aceitável.

- [ ] **Speakers em layout vertical** (foto top + nome + cargo) em vez de horizontal (foto esq + texto dir) — GUIDELINES §8 pede horizontal. Pre-existing pattern da LP de referência (`monitoramento-concorrentes-maio-2026`). Como ainda é placeholder `[Speaker TBD]`, é momento certo para revisitar antes de inserir os speakers reais.
- [ ] **Estrutura — ordem das seções.** Atual: Hero → Ticker → Problema → Diferencial → Programa → Speakers → Para quem → Urgência → Final. GUIDELINES §6: Hero → Problema → Programa → Diferencial → Para quem → Prova → Urgência → Final. Inversões aceitas (a referência também reordena), mas se quiser disciplina total mover Diferencial pra depois do Programa.
- [ ] **CTA final com fundo destaque.** Atual `.final { background: var(--c-n100) }` — GUIDELINES §8 sugere "destaque (gradiente ou cor primária)". Pre-existing pattern. A urgency dark já faz o impacto anterior; se o final também for destaque, fica double-statement.
- [ ] **Padding 128/80 em vez de premium 160/100.** Acima do mínimo (120/80). Pre-existing. Aceitável.
- [ ] **`<meta property="og:image">` ausente.** Sem OG image, preview no LinkedIn/WhatsApp/Slack não tem thumbnail. Sugestão: gerar imagem 1200×630 com lockup do hero e referenciar.
- [ ] **Diff-art `kicker`** ainda repete o conceito da H3+SUB do `diff-copy`. Redundância intencional para reforço editorial. Pode-se trocar o kicker por algo curto/quebrador (ex: métrica concreta) se houver dado disponível, mas como não está em `copy.txt`, deixar como está respeita a regra de fidelidade.

## Auditoria de GTM (Passo 3.5)

- ✓ GTM-MKQBX2MG (LATAM) injetado no `<head>` linha 8-12 (após viewport, antes de title)
- ✓ Noscript imediatamente após `<body>` linha 760-762
- ✓ Cascata de região resolveu corretamente: sufixo `-latam` no slug → `regions.latam` em `brand/buzzmonitor/tracking.json`

## Próximos passos

- ✓ Auditoria de design + a11y aplicada
- ✓ Auditoria de fidelidade da copy aplicada (todos os 5 críticos resolvidos)
- ✓ 4 melhorias aplicadas
- ✓ 3 melhorias opcionais marcadas (não aplicadas — decisão do Victor)
- ✓ 6 nice-to-haves marcadas
- [ ] Substituir `[Speaker TBD]` (2 cards na seção Speakers — comentário `<!-- TODO -->` no HTML linha 977)
- [ ] Quando design aprovado: `/lp-integrar-form buzzmonitor/social-listening-mayo-2026-latam "<snippet>"` para trocar form mock por embed real
- [ ] Quando form integrado e tudo conferido: `/lp-publicar buzzmonitor social-listening-mayo-2026-latam webinar.buzzmonitor.com` (modo guarda-chuva — anexa ao projeto Vercel `buzzmonitor-lp-monitoramento-concorrentes`)

## Aprendizado para skills

O incidente desta LP motivou bumps preventivos em `lp-gerar` (1.4.0 → 1.5.0) e `lp-revisar` (1.3.0 → 1.4.0) — ver entrada do `CHANGELOG.md` para LP family v1.8.0. Em resumo:
- `lp-gerar` Passo 3 ganhou bloco **Regra de Fidelidade da Copy** explicitando que TODO texto visível vem literal de `copy.txt` + whitelist exata + lista de "não inventar".
- `lp-gerar` Passo 4.2 ganhou auditoria de fidelidade (diff textual em 4 buckets, busca dos 4 padrões mais comuns de vazamento, contagem de em-dash).
- `lp-revisar` ganhou Passo 3.6 — segunda camada independente da auditoria de fidelidade, tratada com mesma prioridade do GTM (CRÍTICO, não opcional).

Próximas LPs não devem reproduzir o padrão.
