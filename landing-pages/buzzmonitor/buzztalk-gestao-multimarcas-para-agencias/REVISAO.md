# Revisao LP — buzzmonitor/buzztalk-gestao-multimarcas-para-agencias

**Data:** 2026-08-27
**Auditores:** frontend-design (review mode) + web-design-guidelines (auditoria manual seguindo os checklists das skills, já que ambas rodam como orientação inline, não como agentes externos)

## Aplicado automaticamente (6 críticos)

- [x] **Contraste AA no botão laranja** — `.btn-laranja` tinha texto branco sobre fundo `#EB7C2E` (contraste ~2.8:1, abaixo do mínimo 4.5:1 da GUIDELINES §7). Trocado o texto para roxo escuro `#390155` (~5.7:1) e ajustado o hover para inverter (fundo roxo + texto branco, ~16:1).
- [x] **COPY-VAZAMENTO: "Garanta sua vaga"** — título inventado no card do formulário do hero, não existe em `copy.txt`. Removido; o form fica sem heading, com o contexto já dado pelo H1/body ao lado.
- [x] **COPY-VAZAMENTO: kicker "Como chegar"** — label decorativo acima do H2, não literal da copy. Removido.
- [x] **COPY-VAZAMENTO: kicker "O que você vai aprender"** — idem, duplicava (com texto diferente) a linha "Neste evento, você vai aprender:" que já é literal da copy. Removido.
- [x] **COPY-VAZAMENTO: kicker "Agenda do dia"** — não existe em `copy.txt` (a seção só tem H2 "Cronograma"). Removido.
- [x] **Contador regressivo sem fallback para JS desabilitado** — sem JS, os 4 números ficavam travados em "00" (parece que o evento já começou/passou). Adicionado `<noscript>` que esconde o contador e mostra a data por extenso.

## Aplicado após informação do usuário (não fazia parte da auditoria original)

- [x] Endereço do evento confirmado pelo usuário (Av. Paulista, 807, 17º Andar, Espaço Paulista Promoções Eventos) + embed do Google Maps na seção "Como chegar". `copy.txt`, `index.html` e o JSON-LD (`Event.location`) atualizados.
- [x] `landing-pages/dominios/content-buzzmonitor-com/vercel.json` — adicionado `https://www.google.com` ao `frame-src` do CSP (patch cirúrgico, só essa entrada) para o embed do Maps não ficar bloqueado no live. Como é um arquivo mecânico do guarda-chuva (afeta todas as LPs do domínio), o PR provavelmente cai em `precisa-revisao-victor` em vez de auto-merge (CONTEXT.md §2.6) — atenção ao abrir o PR.
- [x] Mediadora confirmada pelo usuário (Barbara Gomes) — placeholder circular trocado pela foto real (`assets/mediador-barbara-gomes.jpg`, 1037×1600, fornecida em 2026-08-27). `alt` da imagem = "Barbara Gomes". CSS morta do placeholder (`.avatar-placeholder`) removida.

## Melhorias opcionais (2)

- [ ] Grid do contador regressivo fica apertado em telas muito pequenas (<350px) — considerar layout 2×2 nesse breakpoint.
- [ ] Ícones sociais do footer são só texto ("YouTube @...", "Instagram @..."); dá pra trocar por ícones SVG das redes para ficar mais compacto, mas texto é mais acessível e já está ok.

## Nice-to-haves (1)

- [ ] Aspas decorativas do card de citação (`.quote-card::before`) poderiam ganhar leve animação de entrada — puramente estético, ignorar é aceitável.

## Auditorias determinísticas

- **GTM:** `status: ok` — container `GTM-WFJVK858` bate com a região `brasil` (cascata via `<html lang="pt-BR">`). Selo `.tracking.lock` gravado.
- **Em-dash:** 0 ocorrências (checado após cada edição).
- **JSON-LD:** parseia como JSON válido; `Organization.url`/`sameAs` batem com `brand/buzzmonitor/brand-manifest.json`.
- **SEO obrigatório (GUIDELINES §15):** 1 description, 10 tags `og:`, 4 tags `twitter:`, 1 JSON-LD, 1 canonical — todos dentro do esperado.
- **Multi-idioma (§16):** LP única, sem irmãs — hreflang omitido corretamente, só canonical.
- **Logo regional (§17):** header e footer apontam para `https://buzzmonitor.com/` (brand-manifest `regions.brasil.home`), `target="_blank" rel="noopener"`, aria-label localizado.
- **Logo SVG web-safe (§19):** `logo-primary.svg`, `logo-reversed.svg`, `logo-icon.svg` — todos com `grep -c '<text'` = 0 (raster/base64), sem risco de serifar.
- **OG image (§18):** ainda não gerada (pendente — ver README "Estado").

## Ajustes de layout pedidos pelo usuário (2026-08-27, via review do link publicado)

- [x] **Botão laranja com texto branco** — pedido explícito do usuário, revertendo a correção de contraste do item acima. **Atenção:** `#EB7C2E` com texto branco dá ~2.8:1 de contraste, abaixo do mínimo AA de 4.5:1 (GUIDELINES §7). Aplicado mesmo assim por decisão de design do usuário — se isso vier a incomodar em auditoria de acessibilidade, a correção é reverter para texto `var(--roxo)` ou escurecer o laranja especificamente nos botões.
- [x] **Menos pastel, mais contraste** — countdown, hora do cronograma e sublinhado do contato trocados de tons `-light` para cores cheias da marca.
- [x] **Seção "Como chegar" redesenhada** — texto centralizado, endereço com cor mais escura (`var(--texto)` em vez de `--texto-sec`), contador virou um card roxo "flutuante" sobreposto ao topo do mapa, mostrando a data por extenso junto dos números.
- [x] **Seção "Aprendizados"** — bloco de texto introdutório centralizado e alargado (860px), reduzindo o vazio lateral.
- [x] **Seção "Mediador" redesenhada** — layout em duas colunas (foto grande + nome), foto de 140px para 220px com blob decorativo em gradiente atrás.
- [x] **Cronograma reconstruído** — grid de 3 colunas fixas (horário/ponto/descrição) em vez de posicionamento absoluto, corrigindo a colisão visual entre o texto do horário e o pontinho da timeline.
- [x] **Prova social com fundo fotográfico + parallax** — foto de plateia do evento (`assets/evento-plateia-buzzmonitor.jpg`, fornecida pelo usuário) a 14% de opacidade atrás do card de citação, com parallax via scroll (JS, respeita `prefers-reduced-motion`).

## Próximos passos

- Nome/foto do mediador e formulário real (Jotform/RD Station/HubSpot) seguem como bloqueadores antes do publish — ver `README.md`.
- Gerar OG image 1200×630 → `assets/og-buzztalk-gestao-multimarcas-para-agencias.png`.
- Form real → `/lp-integrar-form buzzmonitor/buzztalk-gestao-multimarcas-para-agencias "<snippet>"`.
- Quando aprovado → `/lp-publicar buzzmonitor buzztalk-gestao-multimarcas-para-agencias content.buzzmonitor.com`.
