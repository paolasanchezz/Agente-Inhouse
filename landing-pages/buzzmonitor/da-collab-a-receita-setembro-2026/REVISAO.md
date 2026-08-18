# Revisão — LP "Da Collab à Receita" (Buzzmonitor + Buzzcreators)

**Data:** 18/08/2026 (v3: ajustes de design por seção) · **Status:** gerada local, aguardando aprovação (não publicada)

## v3 — Ajustes de design pedidos seção a seção
- **Hero:** H1 agora cabe em 1 linha ("Da collab à receita.", `white-space:nowrap` acima de 560px), "collab" com c minúsculo, texto do corpo resumido (2 frases → 1), toda menção a Bruno Filho removida do hero (fica só na seção "Quem apresenta", com foto real).
- **Seção Problema:** trocou o H2-frase + 4 cards com caixa por um **stat-callout centralizado** (número "35,6%" gigante em gradiente + legenda) seguido de uma **lista corrida sem caixinhas** (divisores, sem card/sombra/borda).
- **Seção "frase de impacto" (punchline):** removida por completo, junto com o CSS não usado.
- **Seção Conceito:** saiu o box de cor sólida (rosa/gradiente); entrou um **mockup de player de vídeo** (moldura escura + botão de play + barra de progresso + controles + card de título "Da collab à receita" / canal "Buzzmonitor + Buzzcreators" abaixo, como uma tela de vídeo). Ícones desenhados em SVG inline (não é a marca real do YouTube, é um motivo genérico de player, para não usar a marca de terceiros).
- **Seção Programa:** título "O que você vai levar deste webinar" agora cabe em 1 linha (fonte padronizada + `max-width` do cabeçalho ampliado).
- **Quem apresenta:** troquei o avatar de iniciais "BF" pela **foto real do Bruno Filho** (copiada de `landing-pages/buzzcreators/vendendo-com-creators/assets/bruno-filho.png`, já usada em outras LPs) e adicionei o **logo da Buzzcreators** (`brand/buzzcreators/assets/logos/logo-color.png`, a versão raster recomendada pela GUIDELINES §19) abaixo do cargo.
- **Global:** tamanho de fonte dos títulos de seção padronizado num único `clamp()` (era 3 escalas diferentes: sec-head/urgency/final/diff); `max-width` dos cabeçalhos ampliado pra evitar quebra de linha prematura com espaço disponível; removidos os eyebrows "O problema", "O conceito", "O programa", "Quem conduz", "Para quem é", "Para fechar", "Vaga gratuita" (mantive só o badge do hero "Webinar gratuito · Buzzmonitor + Buzzcreators", que é status/formato, não rótulo de categoria).
- Revalidado: 0 em-dash, SEO/JSON-LD intactos.

**Nota sobre o preview:** no preview local cru (`file://` ou `python -m http.server`), imagens locais (foto do Bruno, logo da Buzzcreators, logos da Buzzmonitor) podem não renderizar dependendo do navegador/sandbox — os caminhos resolvem certo após `/lp-publicar`. Confirmei que o arquivo da foto existe e está correto (665×665px) e que o servidor local devolve 200 pra ele.

## v2 — Reescrita de copy (pedido: menos figuras de linguagem, tom didático, título do webinar em destaque)
- **H1 trocado.** Saiu "Você paga o creator e recebe um *print* de volta" (dor em metáfora). Entrou **"Da Collab à Receita."** — o próprio título do webinar, em destaque, com "Collab" no gradiente (consistente com a OG image). Isso é uma **exceção deliberada** à regra padrão da GUIDELINES §3 (H1 = dor, não solução/título) — decisão sua, registrada aqui em vez de reescrita silenciosa.
- **Metáforas cortadas em cascata** por linguagem factual/didática: "explodiu"/"parado no tempo" → dado real (35,6% YoY, YOUPIX/Nielsen); "decide no escuro" → "53% das marcas não medem"; "recomeça do zero" → "começa do zero" (mais literal); "todo creator recebe igual" → "pagamento não reflete a performance"; punchline "campanha solta não vira receita" → "faltam dados dos dois lados da campanha" (conclusão causal, não frase de efeito); card do conceito "do dado à operação" → "de 2 para 4 colaboradores por post" (dado real, técnica "mostrar > falar"); H3 "onde termina o dado, começa a operação" → "o Buzzmonitor coleta o dado, o Buzzcreators faz a operação" (frase funcional); urgência "saírem na frente" → ancorada na data real da API (jun/2026).
- Revalidado: 0 em-dash, 1 negação simples (dentro do limite de 2 da família antítese-por-negação), SEO/JSON-LD intactos.

## Validações automáticas (todas OK)
- Em-dash (`—`): 0 · `&mdash;`: 0
- `meta description`: 1 · `og:*`: 10 · `twitter:*`: 4 · `application/ld+json`: 1 (parseia)
- Antítese-por-negação "X, não Y": 1 instância (limite: 2) — checado após a reescrita
- OG image: `assets/og-da-collab-a-receita-setembro-2026.png` — 1200×630, 338 KB
- Favicon: `../../brand/buzzmonitor/assets/logos/logo-icon.png` (padrão GUIDELINES §12)
- JSON-LD: Organization + WebPage + Event (startDate 2026-09-15T15:00-03:00, performer Bruno Filho)

## Aderência às GUIDELINES
- **§3 Hero:** H1 agora é o título do webinar ("Da Collab à Receita"), não a dor — exceção deliberada pedida por você (ver nota v2 acima). A dor entra explícita na seção Problema, com dado real (35,6% YoY).
- **§6 Estrutura:** Hero → Problema (4) → Conceito/diferencial → Programa (6) → Speaker → Para quem (5) → Urgência → CTA+form → Footer. ✔
- **§8 Gramática visual:** problema = lista vertical com X vermelho; programa = grid com ✓; urgência = fundo roxo + tag rotacionada (1x). ✔
- **§9 Copy dita estrutura:** 4 dores, 6 itens de programa, 5 perfis, 1 palestrante — contagem = a copy. ✔
- **§10 Form:** ToFu/MoFu — CTA no hero + form ao final (§inscricao). Jotform real já integrado (252154974852667). ✔
- **§7 A11y:** skip-link, focus-visible, countdown `aria-hidden`, SVGs decorativos `aria-hidden`, prefers-reduced-motion. ✔

## Decisões e pontos de atenção (para a Catharina revisar)
1. **Horário 15h — a confirmar.** A data (15/set, terça) veio de você; o horário não foi informado. Usei **15h (Brasília)** no hero, ticket, box de contagem, JSON-LD, CTA final e OG. Se for outro, é 1 troca em 6 pontos (me avisa).
2. **Marca:** hospedada em `webinar.buzzmonitor.com`, logo Buzzmonitor no nav/footer; co-branding "Buzzmonitor + Buzzcreators" no badge do hero. Speaker único: Bruno Filho, com foto real e logo da Buzzcreators (ver v3 acima).
3. **Sem demo ao vivo:** o roteiro diz explicitamente que não há demo prática. Por isso o item destacado do programa é o **case real** (marca D2C: 53→120+ creators), não uma demonstração de plataforma.
4. **Concorrentes:** Sephora/Glossier/Shopee (citados no roteiro como referência de mercado) foram **omitidos** da copy pública por precaução.
5. **Countdown:** mantido dentro do box da data (dias/horas/min/seg), padrão da LP-irmã de gestão de crises (mesma branch). Sem ticker/marquee.

## Pendências antes de publicar
- [ ] Confirmar horário (15h?).
- [ ] (Opcional) foto do Bruno Filho.
- [ ] Publicar via `/lp-publicar buzzmonitor da-collab-a-receita-setembro-2026 webinar.buzzmonitor.com` (fluxo CI).
