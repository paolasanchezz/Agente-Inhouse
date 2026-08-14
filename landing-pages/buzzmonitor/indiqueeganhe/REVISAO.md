# Revisão LP — buzzmonitor/indiqueeganhe

**Última revisão:** 2026-08-14
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel Labs)

## Revisão 2026-08-14 — design + formulário (revisão da versão no ar em content.buzzmonitor.com)

Auditoria feita sobre a página em produção (`https://content.buzzmonitor.com/indiqueeganhe`), com screenshots em 1440px.

### Corrigido nesta rodada

**Bugs**

- [x] **Stepper marcava o passo errado em laranja.** `.step:nth-child(4) .step__num` contava a `<span class="stepper__line">` como 1º filho, então o destaque caía no **3º passo** ("Reunião acontece") em vez do 4º ("Contrato fechado"). Trocado por `.step:last-child`. Confirmado visualmente antes e depois.
- [x] **Link morto no rodapé.** "Política de privacidade" apontava para `href="#"`. Agora vai para `https://buzzmonitor.com/politica-de-privacidade/` (mesma URL usada nas outras 9 LPs Buzzmonitor), com `target="_blank" rel="noopener"`.
- [x] **Promessa sem link no regulamento.** "Dúvidas? Leia o regulamento completo ou fale com a gente" oferecia um regulamento completo que não existe em lugar nenhum (a própria seção já é o regulamento). Reescrito para "Dúvidas sobre alguma regra? Fale com a gente em…".

**Design**

- [x] **Formulário parecia widget de terceiro colado na página.** O Jotform renderiza um card cinza-frio (`#f0f3f5`, fonte Inter) que ficava boiando direto sobre o gradiente roxo→laranja. O embed passou a viver dentro de um cartão branco da marca (`--radius-lg` + `--shadow-lg`): o cinza vira painel de campos e o bloco lê como card, não como enxerto. Validado injetando o CSS na página em produção antes de aplicar.
- [x] **CTA redundante.** O botão "Indique agora" ficava imediatamente acima de um formulário já visível e apontava para uma âncora ~50px abaixo. Removido; o formulário é a única ação da seção. No lugar entrou uma linha de reforço ("Leva menos de 2 minutos…").
- [x] **Caixinhas de segmento com artefato visual.** O losango laranja no canto superior direito (`::before` rotacionado + `overflow:hidden`) era cortado pela borda e lia como glitch. Removido; as caixinhas agora centralizam o texto e ficam com altura igual.
- [x] **Hero sem rótulo de contexto.** A classe `.hero__eyebrow` existia no CSS mas nunca era usada. Agora carrega o selo "Programa de indicação" (contraste `#390155` sobre `#F2D8FF` ≈ 12:1).

**Melhorias que estavam abertas desde 2026-08-05 (5 das 7 fechadas)**

- [x] Padding mobile agora respeita o piso das GUIDELINES: `@media (max-width:780px)` leva `.section` para 80px e `.hero` para 64/72px.
- [x] `scroll-margin-top:88px` em `section[id]` — âncoras não ficam mais sob o header sticky.
- [x] `R$&nbsp;500` / `R$&nbsp;1.000` em todas as ocorrências do corpo (hero, recompensas, stepper, regulamento).
- [x] `preconnect` para `youtube.com` e `form.jotform.com`.
- [x] `text-wrap:balance` em h1/h2/h3.

**Nice-to-haves fechados**

- [x] `touch-action: manipulation` + `-webkit-tap-highlight-color: transparent` em botões e links.
- [x] `:hover` nos links do rodapé.
- [x] O laranja do stepper agora tem lógica visual clara: é o último passo, o único que fecha o ciclo.

### Aberto — depende de decisão

- [ ] **Formulário (Jotform `242464989976077`) precisa de ajustes que só podem ser feitos dentro do Jotform.** São 188 submissões em produção, então nada foi alterado sem aprovação. Diagnóstico:
  - **Botão de envio verde** (`Enviar indicação`) num fluxo onde todo CTA é laranja `#EB7C2E`. É o único botão da página fora da marca, e é justamente o que converte.
  - **Placeholder no lugar de label** nos 8 campos: os `<label>` contêm literalmente `*`. Leitor de tela anuncia "asterisco"; e como os dois blocos ("Seus dados" e "Dados da pessoa interessada") têm placeholders idênticos, quem começa a digitar perde a referência de qual bloco está preenchendo.
  - **"REQUIRED" em inglês e vermelho** ao lado do checkbox de consentimento, numa página inteiramente em PT-BR.
  - **Fonte Inter e card `#f0f3f5`** contra Lato/League Spartan e branco do resto da página (mitigado pelo cartão branco, mas a fonte segue destoando).
  - **Link "Política de Privacidade"** em azul sublinhado padrão, apontando para `buzzmonitor.com.br/privacidade/?_ga=…` (URL antiga, com parâmetro `_ga` de 2024 colado).
  - **8 campos obrigatórios** para uma indicação. Vale avaliar tornar "Empresa" (do indicador) e "WhatsApp" (do indicado) opcionais.
- [ ] **Deploy solo antigo continua no ar e indexável.** `https://buzzmonitor-lp-indiqueeganhe.vercel.app/indiqueeganhe` responde 200, com `robots: index, follow` e canonical apontando para ele mesmo — conteúdo duplicado competindo com `content.buzzmonitor.com/indiqueeganhe`. Retirar o projeto do ar (ou pôr `noindex` + canonical para o guarda-chuva) é decisão do Victor.

### Segue aberto (não afetado)

- [ ] **Paleta com 4 cores fortes** (roxo + laranja + teal + amarelo) — GUIDELINES §1 recomenda 2-3. Roxo e laranja carregam a LP; teal e amarelo aparecem só como tint de ícone e figura. Mantido por ora.
- [ ] **Nenhuma seção de "pausa"** (GUIDELINES §2). Criar uma seção nova violaria a §9 ("copy dita estrutura"), então o respiro foi tratado só por espaçamento.


## Revisão 2026-08-05 — pós-alterações (título hero, subtítulo, linha do stepper, imagem "quem vale a pena", fonte do H2, cor das caixinhas)

**0 críticos novos.** As alterações desta rodada (remoção de "por isso" no H1, troca da 1ª frase do subtítulo, linha única conectando os 4 passos do stepper, imagem `assets/quem-vale-a-pena.png` no lugar das caixinhas antigas, aumento da fonte do H2 "Quem vale a pena indicar?" e caixinhas de segmento em lilás/roxo) não introduziram nenhuma quebra visível, problema de contraste ou vazamento de copy.

Checagens re-executadas após as mudanças:
- **GTM:** `status: ok`, `stamp_match: true` (fingerprint não mudou — mudança de copy/CSS não afeta região/GTM).
- **Fidelidade de copy:** H1 e subtítulo do hero no HTML batem literal com `copy.txt` atualizado. 0 em-dash.
- **SEO:** description=1, robots=1, og=10, twitter=4, JSON-LD=1 (parseia, tipos `Organization`/`WebPage`/`SoftwareApplication` corretos), canonical=1 — inalterados.
- **Logo regional:** sem regressão, hrefs corretos, sem `<text>` vivo nos SVGs.
- **Imagem nova:** `<img>` com `alt` descritivo, `width`/`height` explícitos (1672×941) e `loading="lazy"` (correto — está abaixo da dobra). `alt` não é literal de `copy.txt` (a copy não tinha texto para essa imagem no momento em que foi escrita) — tratado como descrição de acessibilidade necessária, mesmo critério já aplicado ao `title` do vídeo do hero.
- **Contraste das caixinhas de segmento:** fundo `primary-light` `#F2D8FF` + texto `primary` `#390155` ≈ 12:1 — muito acima do mínimo.

## Aplicado em revisões anteriores (2026-07-02, 2 críticos)

- [x] Contraste de ícone falha WCAG 1.4.11 em 2 dos 4 persona-cards — corrigido unificando o `fill` para `var(--primary)`.
- [x] Vídeo do hero com `loading="lazy"` indevido (acima da dobra) — removido.
- [x] OG image ausente — gerada (`assets/og-image.png`, 1200×630).

## Melhorias opcionais (7 — ainda abertas, nenhuma delas foi afetada pelas mudanças desta rodada)

Para o usuário decidir. Aplicar via Edit manual ou pedir `/lp-revisar` novamente.

- [ ] **Paleta com 4 cores fortes em uso** (roxo + laranja + teal + amarelo) — GUIDELINES §1 recomenda 2-3.
- [ ] **Nenhuma seção de "pausa"** (GUIDELINES §2) — as 7 seções são todas densas (cards, listas, form).
- [ ] **Sem `@media` reduzindo padding no mobile** — `.section{padding:120px 0}` e `.hero{padding:96px 0 100px}` não caem para o piso de 80px em telas pequenas.
- [ ] **`scroll-margin-top` ausente nos ids de âncora** (`#como-funciona`, `#form`, `#quem-pode-indicar`) — funciona hoje por causa do padding generoso, mas é frágil.
- [ ] **"R$ 500" / "R$ 1.000" sem non-breaking space** — pode quebrar linha entre "R$" e o número.
- [ ] **Sem `preconnect` para os embeds** (`youtube.com`, `form.jotform.com`).
- [ ] **`text-wrap: balance` ausente em h1/h2** — headlines longas podem quebrar com palavra órfã.

## Nice-to-haves (4 — ainda abertos)

Estilístico. Ignorar é aceitável.

- [ ] `.step:nth-child(4) .step__num` muda de roxo para laranja sem explicação visual clara.
- [ ] `touch-action: manipulation` e `-webkit-tap-highlight-color` não definidos nos botões/links.
- [ ] `.footer__links a` não tem `:hover` além do sublinhado estático.
- [ ] `.persona-card:hover` anima `box-shadow` junto com `transform` — impacto desprezível.

## Próximos passos

- Design aprovado, vídeo, form e imagem já integrados.
- Rever mais algum crítico? → editar e rodar `/lp-revisar` novamente.
- Publicar → `/lp-publicar buzzmonitor indiqueeganhe [dominio]`
