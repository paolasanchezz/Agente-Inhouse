# Revisão LP — cxpress/atencion-clinicas-latam

**Data:** 2026-07-28
**Auditores:** frontend-design (review mode) + web-design-guidelines

## Aplicado automaticamente (4 críticos)

- [x] **GTM com ID errado** — `GTM-T4XDWHL3` (Brasil/default) estava aplicado numa LP `-latam`; `brand/cxpress/tracking.json` define `GTM-WRQ47B9R` para `regions.latam`. Substituído nos 2 blocos (`<head>` script + `<body>` noscript).
- [x] **Contraste insuficiente no ícone "+" do FAQ** — `.faq summary::after` usava `var(--accent)` (#EF863C) sobre branco = 2,59:1 (abaixo até do mínimo 3:1 para componente de UI). Trocado para `var(--primary-dark)`.
- [x] **Contraste insuficiente nos labels em negrito dos cards de Beneficios** — `.bcard__sub strong` usava `var(--accent)` = 2,59:1, texto real (não decorativo). Trocado para `var(--primary-dark)`.
- [x] **Overline do hero quebrava em 2 linhas no mobile estreito** — `@media (max-width:520px){.hero__overline{white-space:normal}}` permitia quebra dentro da pill arredondada (GUIDELINES §3 pede esconder, não quebrar). Trocado para `display:none`.

## Melhorias opcionais (8)

Para o usuário decidir. Aplicar via Edit manual ou pedir `/lp-revisar` novamente.

- [ ] **Ordem narrativa e posição do formulário (Formulário/FAQ antes de Dolor/Solución; página termina em "Quiénes somos" sem CTA final full-width)** — diverge da estrutura mínima padrão (GUIDELINES §6/§9/§10). **Não é erro de geração**: é a ordem exata que o usuário ditou explicitamente ao colar a copy final, seguida à risca por pedido dele. Documentado aqui para transparência, não reaberto como pergunta.
- [ ] **Paleta com cor extra sem significado semântico** — `.rcard__pill` cicla por primary/accent/warning/success nos 5 cards de "resuelve", introduzindo `--warning` só por variedade (GUIDELINES §1 pede 2-3 cores). Sugestão: usar só 2 cores alternadas.
- [ ] **Grid de 5 cards em 3 colunas** (`.resuelve__grid`) deixa a última linha com 2 de 3 colunas ocupadas — buraco visual à direita no desktop. Sugestão: grid 2 colunas (2-2-1) ou reagrupar.
- [ ] **Asteriscos (`*`) nos 4 stats de "Resultados" sem nota de rodapé** — usuário não informou a fonte; não inventei citação. Confirmar fonte para adicionar nota, ou remover os asteriscos.
- [ ] **Logo do header/footer aponta para `https://cxpress.ai/`**, enquanto `brand/cxpress/brand-manifest.json#websites.latam` lista `https://home.cxpress.io`. Mantido igual à LP irmã já publicada `atencion-digital-latam` (mesmo padrão, consistência entre LPs ES-LATAM de Cxpress no guarda-chuva) — não alterado sem confirmar qual é a URL correta atual da marca.
- [ ] **Sem `hreflang`** cruzando com `atendimento-clinicas` (PT-BR, mesmo tema, mas slug-base diferente — não é detectado pela convenção mecânica de sufixo `-es`/`-pt`). Avaliar se vale linkar as duas como variantes de idioma.
- [ ] **Fonte `Bitter` (`--font-accent`) importada e declarada mas nunca usada** no CSS — peso de rede sem benefício. Remover da URL do Google Fonts se confirmado que não vai ser usada.
- [ ] **`.btn--light` declarado mas não usado no HTML** — código morto, ou aproveitar como CTA secundário ghost no hero (GUIDELINES §3 sugere).

## Nice-to-haves (7)

Estilístico. Ignorar é aceitável.

- [ ] `style="list-style:none"` inline no `<ul class="stats__grid">` — mover para classe CSS.
- [ ] Cor do ícone SVG em `.qs-badge` hardcoded (`fill="#6b7280"`) em vez de `var(--neutral-700)`.
- [ ] Seção "Clientes" usa logo wall; considerar 1-2 depoimentos com foto se quiser reforçar autoridade além de reconhecimento de marca.
- [ ] Sem indicador visual de campo obrigatório no formulário (todos são `required`, mas sem asterisco/nota antes do envio).
- [ ] `hero__bg-photo` (imagem crítica above-the-fold) sem `fetchpriority="high"`; `hero__canales` (ícones, também above-the-fold) tem `loading="lazy"` que atrasa render de conteúdo visível.
- [ ] Alguns `alt` muito longos/enumerativos (lista de clientes, lista de canais) — considerar mais concisos.
- [ ] `:focus` em vez de `:focus-visible` no CSS do `.form input:focus` (tem fallback visual, então não bloqueia, mas diverge do padrão `:focus-visible` já usado no resto do arquivo).

## Pendências fora do escopo desta revisão (já sinalizadas ao usuário)

- **Imagem OG** (`assets/og-atencion-clinicas-latam.png`, 1200×630) — ainda não gerada. `og:image` no `<head>` referencia um arquivo que não existe no source.
- **Formulário mock** — troca pelo embed real via `/lp-integrar-form` fica para depois da aprovação final do design.

## Auditoria de fidelidade de copy

Copy não passou por geração automática (`frontend-design`/`lp-gerar`) — foi escrita diretamente a partir do texto final que o usuário colou no chat, seguindo a estrutura literal dele. Em-dash: 0 ocorrências. Nenhum pull-quote, kicker ou punchline inventado identificado.

## Próximos passos

- Resolver as 3 pendências (imagem OG, fonte dos asteriscos, formulário real) quando possível.
- Design aprovado? → `/lp-integrar-form cxpress/atencion-clinicas-latam "{snippet}"` quando tiver o snippet do provedor.
- Rever mais algum ponto da lista de melhorias? → editar e rodar `/lp-revisar` novamente.
