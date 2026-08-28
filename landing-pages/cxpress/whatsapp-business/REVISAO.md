# Revisão LP — cxpress/whatsapp-business

**Data:** 2026-08-28
**Atualizado:** 2026-08-28 (2ª rodada, após as decisões das 5 lacunas)
**Auditores:** frontend-design (review mode) + web-design-guidelines (Vercel Web Interface Guidelines) + medição instrumentada (Playwright 390 / 1440px) + `check_mobile_type.py` + `check_gtm_region.py` + cálculo de contraste WCAG + teste funcional do formulário

---

## Aplicado automaticamente (10 críticos)

### Contraste WCAG AA (GUIDELINES §7)

- [x] **`.feat-index` (índices 01–05) reprovava AA** — laranja `#EF863C` sobre `#F7F9FE` = **2.45:1** (mínimo 4.5:1). Criado token `--accent-text:#A85207` (**5.14:1**) só para texto; o `#EF863C` original segue nos elementos decorativos (régua do índice, ponto do `.hero-note`, badge da OG). Aplica a regra do §7: quanto mais claro o fundo, mais escuro o texto.
- [x] **`.hero-note` reprovava AA** — `#6b7280` sobre a faixa inferior do gradiente do hero (`≈#EDF1FF`) = **4.29:1**. Trocado para `--neutral-700` (**7.86:1**).
- [x] **`.btn--wa:hover` reprovava AA** — verde `#1E9E5A` a 16px = **3.45:1** sobre branco. Criado `--success-text:#12703E` (**6.15:1**) para o texto no hover; o verde original fica no ícone e na borda (componente de UI, limiar 3:1).

### Acessibilidade / Web Interface Guidelines

- [x] **Formulário sem identificação de erro (WCAG 3.3.1 AA)** — a validação da etapa 1 só pintava a borda e focava sempre o campo `Nome`. Agora cada campo tem `<p class="field-error">` próprio ligado por `aria-describedby`, recebe `aria-invalid`, e o foco vai para o **primeiro campo inválido**. O e-mail passou a validar formato, não só preenchimento.
- [x] **Troca de etapa não era anunciada** — adicionado `<p id="formLive" aria-live="polite" class="sr-only">` que anuncia "Etapa 1 de 2" / "Etapa 2 de 2". O indicador visual de passos é `aria-hidden` (é redundante para leitor de tela).
- [x] **Âncora `#contato` ficava sob o header sticky** — `scroll-margin-top:84px` em `section`. Sem isso, o CTA do hero rolava até esconder o topo da seção atrás da navbar (WIG: "sticky headers must not cover the focused element").
- [x] **`touch-action: manipulation`** em `a, button, summary, input, select` — remove o atraso de 300ms do double-tap zoom no mobile.
- [x] **`spellcheck="false"`** em e-mail e telefone (WIG: campos de código/e-mail não devem ser corrigidos).

### Performance / SEO

- [x] **Imagem do hero sem prioridade** — `fetchpriority="high"` em `tela-tickets.svg` (é LCP). Todas as demais já estavam com `loading="lazy"`.
- [x] **`<meta name="theme-color" content="#ffffff">`** ausente (WIG) — adicionado.

### Correções aplicadas ainda durante a geração

Registradas aqui por transparência (foram feitas antes deste relatório fechar, na iteração de layout):

- [x] **`.sec-head{max-width:22ch}`** espremia o H2 da plataforma em 8 linhas no desktop — trocado por `max-width:640px` + `17ch` no próprio H2.
- [x] **`.hero h1{max-width:15ch}`** forçava 6 linhas — ampliado para `19ch`.
- [x] **Logos de clientes ilegíveis no mobile** (uma imagem de 7 colunas comprimida em 390px, logos com ~10px de altura) — a faixa virou contêiner com rolagem horizontal (`overflow-x:auto`) e a imagem trava em 660px no `≤640px`. Mesmo padrão que o GUIDELINES §20 já reconhece como aceitável ("marquee de logos é mais largo que a tela por design").
- [x] **`.eyebrow` a 13px** violava o piso de 14px do §20 para label — subido para 14px (com `letter-spacing` reduzido de `.09em` para `.08em` para não crescer a caixa).
- [x] **Eyebrows inventados removidos (fidelidade de copy)** — "A plataforma" e "Quem somos" (este duplicava o H2 logo abaixo) não existiam na copy. Removidos. Ver a auditoria de fidelidade abaixo.
- [x] **Parágrafo de introdução do formulário removido** — "Preencha os dados ao lado e um especialista da Cxpress entra em contato…" era copy inventada (não está em `copy.txt`), e no mobile o texto ficava factualmente errado: o formulário fica **abaixo**, não "ao lado".

---

## Auditorias determinísticas (todas passaram)

| Auditoria | Comando | Resultado |
|---|---|---|
| GTM × região (§5.4 CONTEXT) | `check_gtm_region.py` | `status=ok` · `GTM-T4XDWHL3` (Cxpress brasil) no `<head>` **e** no `<noscript>` · selo `.tracking.lock` gravado |
| Em-dash (anti-IA, tolerância zero) | `grep -c "—\|&mdash;"` | **0** |
| Pacote SEO (§15) | contagem de tags | description=1 · robots=1 · og=10 · twitter=4 · JSON-LD=1 · canonical=1 |
| Antítese-por-negação (anti-IA) | `grep` das 6 roupagens | **1** ocorrência (limite é 2) |
| Contraste das seções novas | cálculo WCAG | métrica 4.93 · rótulo 8.41 · dor 17.4 · ícone X 4.76 · chip 12.8 — todos ≥ 4.5:1 |
| JSON-LD parseia | `json.loads` | OK — `Organization` + `WebPage` + `SoftwareApplication` + `FAQPage` |
| hreflang (§16) | busca de LPs irmãs | LP única (`whatsapp-business` sem `-es`/`-pt`) — hreflang corretamente omitido, canonical presente |
| Logo regional (§17) | `grep href` | navbar e footer apontam `https://home.cxpress.io` com `target="_blank" rel="noopener"` e `aria-label` |
| Logo web-safe (§19) | `grep -c '<text'` | `logo-primary.svg` = 0 · `logo-reversed.svg` = 0 (vetor outline, não serifa) |
| OG image (§18) | Pillow + `ls` | `assets/og-whatsapp-business.png` **(1200, 630)**, 355 KB · nenhum `og-image.png` órfão |
| Tipografia mobile (§20) | `check_mobile_type.py` | H1=31 · corpo=17 · menor fonte=14 — pisos atendidos (H1 com MAX 43 cai na faixa 36-43, piso 28) |
| Overflow horizontal | `scrollWidth` a 390px | **390 = 390** (sem overflow). Os 3 itens que o script lista são conhecidos e intencionais: skip-link fora da tela por design, `.hero__wave` recortada por `overflow:hidden`, faixa de logos dentro de `overflow-x:auto` |
| Formulário (pós-integração) | Playwright | Embed do Jotform carrega · iframe 575×796 no desktop e 346×947 a 390px · `scrollWidth` 390 = 390 (sem overflow) · acordeão do FAQ abre · **0 erros de JS** |

---

## Auditoria de fidelidade da copy (Passo 3.6)

**Vazamentos encontrados e corrigidos: 3.** Nenhum restante.

| Texto | Onde estava | Ação |
|---|---|---|
| "A plataforma" (eyebrow) | acima do H2 da seção de funcionalidades | Removido — label decorativo inventado, não está na copy |
| "Quem somos" (eyebrow) | acima do H2 "Quem somos" | Removido — além de inventado, duplicava o H2 |
| "Preencha os dados ao lado e um especialista da Cxpress entra em contato para entender a sua operação de atendimento." | intro do formulário | Removido — copy de marketing inventada, e a referência espacial quebrava no mobile |

**Textos fora de `copy.txt` que permanecem, todos dentro da whitelist do `lp-gerar` Passo 4.2:**

- Labels e opções dos `<select>` do formulário (whitelist item 3). Os rótulos vêm da etapa 2 do guia (Porte, Canal, Dor, Volume); as opções de cada `select` são valores factuais de qualificação, não copy de marketing.
- Disclaimer de consentimento: "Ao enviar, você concorda em receber comunicações da Cxpress sobre a plataforma de atendimento." (whitelist item 3, boilerplate de compliance).
- Mensagens de erro inline dos 4 campos (funcionais, exigidas pela WCAG 3.3.1).
- Botões de navegação do formulário: "Continuar" e "Voltar" (controles de UI, não copy).
- Confirmação de envio: "Recebemos os seus dados. Um especialista da Cxpress entra em contato." (estado de UI; some quando o Jotform real entrar via `/lp-integrar-form`).
- Rodapé: copyright, links institucionais, `mailto:` (whitelist item 4).
- Skip-link e `aria-label`s (whitelist item 5).
- `<title>`, `meta description`, `og:*` (SEO derivado, não introduz copy nova na página).

**Um item para você decidir (não corrigi por conta própria):**

- ⚠️ **Eyebrow do hero "Plataforma de automação de WhatsApp"** — não é literal da copy, é derivado do H1. Não está na whitelist. Mantive porque a pílula de categoria é o bloco 1 do guia ("Hero: **categoria** + dor + resultado + CTA") e o texto não acrescenta nenhuma informação nova. **Se você preferir rigor total de fidelidade, é só remover a linha `<span class="eyebrow">` do hero** — o layout aguenta sem ela.

---

## Lacunas vs. o guia — status após as decisões de 2026-08-28

Victor decidiu as 5 no dia 28/08. Quatro foram aplicadas; uma foi adiada por decisão dele.

### 1. Bloco "Dores resolvidas" — RESOLVIDO ✅

Saída escolhida: **(b) eu escrevo, você aprova.** Copy produzida nesta sessão sob o protocolo obrigatório (`fundamentos-copy.md` + `regras-anti-ia.md`; PT-BR, sem padrão linguístico estrangeiro a carregar).

Seção nova entre a prova rápida e a plataforma, na ordem que o guia pede (Hero → Prova → Dores → Como funciona). Formato conforme GUIDELINES §8: **lista vertical com X vermelhos**, uma frase por item, nunca grid.

**H2:** "O problema do atendimento não é o volume. É o sistema." — frase sancionada do `brand-manifest.json` (`voice.samplePhrases.do`), não inventada.

**Os 5 itens:**

1. Seu cliente repete a mesma história para três atendentes diferentes.
2. A equipe abre WhatsApp, Instagram, e-mail e telefone em abas separadas.
3. Mensagem que chega às 19h só é lida no dia seguinte.
4. Ninguém sabe dizer quantos atendimentos ficaram sem resposta hoje.
5. Cada pessoa que sai da equipe leva junto o histórico dos clientes que atendia.

**Como foi construída:** cada item nomeia uma **cena da rotina**, não uma feature ausente. É a regra de ouro §0 do `fundamentos-copy.md` (a dor gera identificação; identificação compra o segundo seguinte de atenção). Os três temas que o guia pede estão cobertos: canais soltos (2), fila crescendo (3 e 4), perda de histórico (1 e 5). O item 1 é o exemplo canônico de Cxpress do próprio `fundamentos-copy.md` §0.

**Conformidade anti-IA:** em-dash 0 · antítese-por-negação 1 instância (o H2, limite é 2) · filler words 0 · 5 itens em vez de 3, fugindo do anti-padrão de lista sempre-3 · comprimento de frase variado, sem cantilena.

**Status: APROVADO pelo Victor em 2026-08-28.** Copy fechada, nenhum item pendente neste bloco.

### 2. Headline do hero — RESOLVIDO ✅

Escolhida a **variante B**: "Centralize seus canais de atendimento e automatize o primeiro contato com IA sem perder histórico, SLA ou controle da operação".

Dois ajustes que a troca exigiu:

- **Escala tipográfica.** A B tem 24 palavras contra 11 da anterior. O H1 caiu de `clamp(34px, 4.1vw, 54px)` para `clamp(31px, 3.15vw, 43px)`, a medida de linha subiu para `30ch` e a coluna de texto do hero passou de `1fr` para `1.1fr`. Resultado: 6 linhas equilibradas, sem órfã. Continua dentro do §20 (MAX 43 cai na faixa 36-43, cujo piso móvel é 28; está em 31).
- **Uma linha do briefing saiu do hero.** "Centralize e automatize o seu atendimento, simples e eficaz." ficaria colada logo abaixo de um H1 que já abre com "Centralize seus canais... e automatize" — é o anti-padrão de ritmo sintático repetitivo do `regras-anti-ia.md`. **Não descartei a linha:** ela virou o subtítulo da seção da plataforma e segue na OG image.

O H1 antigo não se perdeu: continua como `<title>`, `og:title` e como a pílula de categoria acima do H1 (que é o elemento "categoria" do bloco 1 do guia).

### 3. Prova rápida com números — RESOLVIDO ✅ (com uma pendência)

Saída escolhida: **(b) métricas próprias da Cxpress**, no lugar dos estudos NBER/McKinsey da LP irmã. Dois cards logo abaixo do título de clientes, acima da grade de logos:

- **85%** de redução de SLA
- **+220%** de interações nas redes sociais

O grid já está pronto para receber os próximos números que você mencionou: é `flex-wrap`, então basta acrescentar cards e eles se reorganizam sozinhos, em qualquer quantidade.

> 📌 **Atribuição dos números: adiada por decisão do Victor (2026-08-28).** Os dois cards vão para o ar sem nota de fonte, para avaliar depois.
>
> Fica o registro do porquê isso foi levantado: são resultados atribuídos à Cxpress, não a um estudo de terceiro com fonte citada. Afirmação de resultado sem lastro costuma voltar do jurídico depois da publicação. **Não é bloqueante e não muda nada no layout** — quando quiser resolver, uma linha de nota abaixo dos cards (`.stat` + um `<p>` na seção) ou o nome do case cobrem, e é edição de 2 minutos.

### 4. Bloco "Casos de uso" — ADIADO por decisão sua ⏸️

Fica para a segunda rodada. Nenhum débito técnico: a seção entra entre a plataforma e as integrações sem mexer no que já existe.

### 5. Bloco "Integrações" — RESOLVIDO ✅

Seção nova entre a plataforma e o "Quem somos", com os 7 sistemas que você passou. Grafia normalizada para a oficial de cada produto (o briefing veio em caixa livre): **HubSpot · Buzzmonitor · RD Station Marketing · Pipedrive · TOTVS · ActiveCampaign · Jira**.

Duas decisões de execução:

- **Chips de texto, não logos.** Só existe o logo do Buzzmonitor dentro do repositório. Um logo real ao lado de 6 nomes em texto fica pior do que 7 chips consistentes. Se você conseguir os 7 logos em SVG ou PNG transparente, eu troco.
- **Mantive a ressalva da análise técnica prévia** ("Integrações passam por uma análise prévia da nossa equipe técnica."). Não é ressalva inventada: é a mesma condição que já está na resposta do FAQ sobre CRM, duas seções abaixo. Sem ela, a seção prometeria integração plug-and-play que a própria FAQ desmente.

---

## Nota sobre "de forma X" (anti-IA)

A varredura de filler words acusa duas ocorrências de `de forma X`, que o `regras-anti-ia.md` manda cortar:

- "Organize seu atendimento **de forma integrada**" (título da funcionalidade 03)
- "Podem ser integrados **de forma nativa** o WhatsApp, e-mail…" (resposta do FAQ)

**Não corrigi as duas.** Ambas vêm literais do briefing e da página viva. A regra de fidelidade de copy vence a limpeza anti-IA quando o texto é do cliente, não meu. Se você quiser reescrever, é decisão sua e eu aplico.

## Melhorias opcionais (5)

- [ ] **CTA secundário do WhatsApp ocupa duas linhas no desktop** — `.btn--wa` no hero. O texto do briefing ("Fale com um de nossos consultores no WhatsApp agora mesmo!") tem 10 palavras, longo demais para um botão em linha única ao lado do CTA primário. Mantive literal (regra de fidelidade). Se você autorizar encurtar para "Falar no WhatsApp", vira botão de uma linha e a dupla rota do guia §4 fica mais limpa. No mobile já mostro só "WhatsApp".
- [ ] **Segundo gradiente na seção escura** — `.about::after` usa um `radial-gradient` de brilho além do `linear-gradient` do hero. O GUIDELINES §1 pede um gradiente por LP. São da mesma família de azul e o efeito é muito sutil, mas é tecnicamente um segundo gradiente. Trocar por uma cor chapada com opacidade resolve.
- [ ] **Telas do produto recortadas na borda direita** — a aba "Facebook" na tela do chatbot e a coluna "Ações" na tela de canais aparecem cortadas. Vem do recorte do artboard nos SVGs de origem (exportados do Figma em 2023), não do CSS. Lê como "o app continua além da moldura", que é convenção comum de product shot, mas dá para pedir um re-export com o artboard completo.
- [ ] **Coluna esquerda de "Quem somos" fica vazia** — só o H2 numa coluna de 0.62fr. É uma composição editorial deliberada, mas se quiser densidade, cabe ali a foto `brand/cxpress/assets/plataforma/quem-somos-foto.jpg` ou o mascote Samir.
- [ ] **Fontes sem `preload`** — a WIG recomenda `<link rel="preload" as="font">` para as fontes críticas. Hoje há `preconnect` para o Google Fonts e `display=swap`, que já evita texto invisível. Ganho pequeno.

## Nice-to-haves (3)

- [ ] `preconnect` para `googletagmanager.com` (o GTM é o primeiro script do `<head>`).
- [ ] O `transition-delay` escalonado dos reveals é aplicado por JS via `style` inline num laço. Funciona, mas daria para resolver em CSS puro com `:nth-child`.
- [ ] `font-variant-numeric: tabular-nums` nos índices 01–05 (alinhamento vertical perfeito dos números entre as features).

---

## Próximos passos

1. ~~Aprovar a copy das 5 dores~~ **feito** (28/08) · ~~definir atribuição dos números~~ **adiado por decisão** (28/08). Nada pendente de conteúdo.
2. ~~Integrar formulário~~ **feito** (28/08) — Jotform `261027639617663`, o compartilhado com a irmã. O mock de 2 etapas saiu, com CSS e JS.

   Correção de uma preocupação que levantei antes de ver o form: eu disse que os 4 campos de qualificação da etapa 2 não teriam onde cair. Só 2 ficaram de fora. O Jotform já pergunta **"O que você gostaria de resolver na sua operação?"** (maior dor) e **"Quantidade de colaboradores"** (porte), além de **"Site da empresa"**, que casa com o pré-requisito declarado na FAQ. Faltam apenas *principal canal* e *volume de atendimentos por mês* — e isso se resolve no Jotform, não na LP.

3. Publicar → `/lp-publicar cxpress whatsapp-business content.cxpress.io`
