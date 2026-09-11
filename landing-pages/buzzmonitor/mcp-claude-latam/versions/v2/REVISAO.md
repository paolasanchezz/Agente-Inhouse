# Revisao LP · buzzmonitor/mcp-claude-latam (v2)

**Data:** 2026-09-10
**Auditores:** frontend-design (review mode, contra GUIDELINES §1 a §20) + web-design-guidelines (Vercel Labs Web Interface Guidelines)
**Checks deterministicos:** `check_gtm_region.py` (ok, GTM-MKQBX2MG, latam) · `bump_mobile_type.py` (aplicado) · `check_mobile_type.py` (sem overflow real)
**Revisao da v1:** `versions/v1/REVISAO.md`

## Desvios deliberados das GUIDELINES (aprovados por Ulises no briefing da v2)

- **§1 e §3 pedem fundo claro** (branco alternando com neutral-100, hero branco). A v2 e escura ponta a ponta por pedido
  explicito ("utiliza un fondo oscuro con degradados de naranja a rojo"). O espirito da §1 fica preservado: 3 cores fortes
  (ambar, laranja, vermelho) sobre preto quente, alternancia unica de fundo (`--void` com `--void-2`) e **uma so** familia de
  degradado em toda a pagina. A v1 clara continua disponivel em `versions/v1/` para comparar.
- **§5 e fundamentos-copy §0: o H1 abre pela solucao,** nao pela dor. Foi sinalizado na v1 e Ulises optou pelo copy do brief.
  A versao que abria pela dor esta em `versions/v1/copy.txt` e serve como braco B de um teste.

## Aplicado automaticamente (8)

- [x] **Titulares display espremidos** em VALOR e CONVERSACION. As regras `.valor__head{max-width:22ch}` e
      `.conver__head{max-width:26ch}` usavam `ch` num container com fonte de corpo (Lato 18px), o que resolvia para
      ~200px e quebrava o H2 em 5 linhas de duas palavras. O `max-width` em `ch` passou para os proprios headings,
      onde resolve na fonte display.
- [x] **Borda dura no feixe do spotlight.** O `clip-path` era aplicado depois do `filter: blur()`, o que recriava uma
      diagonal nitida na direita do hero. Trocado por `conic-gradient` + `mask`, que degrada sozinho.
- [x] **URL do MCP quebrando no meio da palavra** (`https://mcp.buzzmonitor.c / om.br/sse`) por `word-break:break-all`
      numa coluna estreita. A caixa passou a empilhar (URL numa linha, botao embaixo) com `overflow-wrap:anywhere`.
- [x] **Atributo `style` duplicado** na linha de CTAs do hero (HTML invalido). Fundido, e a centralizacao virou classe.
- [x] **Ancora inexistente** no CTA "Conectar ahora" (`#conexion-ancla` nao existia). Criada na caixa da URL, com
      scroll suave, destaque temporario e foco no botao de copiar.
- [x] **Reveal do MacBook so disparava pelo failsafe de 3,5 s** em viewports altas: o `threshold:.1` combinado com
      `rootMargin:-10%` deixava o elemento logo abaixo do gatilho. Ajustado para `threshold:0` / `-6%`.
- [x] **Pisos tipograficos mobile (§20)** via `bump_mobile_type.py`: 13 clamps e 9 regras px subidas.
- [x] **CTA da nav estourando no mobile.** Em 390px, "AGENDAR UNA REUNIÓN" a 15px em caixa alta nao cabia ao lado do
      logo. Reduzidos padding e letter-spacing e escondida a seta decorativa abaixo de 640px. Medido: botao 151..369,
      logo termina em 135, sem scroll horizontal.

## Privacidade: o video do hero

A gravacao original expunha dados pessoais numa pagina que vai a publico: a barra lateral do Claude com titulos de
conversas do Ulises e o rodape "Ulises · Free", mais a saudacao "Buenas tardes, Ulises" nos primeiros segundos.
O video publicado foi **recortado para o painel de conteudo** e **cortado nos primeiros 2,8 s**. Nada disso aparece.
Se a gravacao for refeita, repetir o recorte (ver README).

## Verificado e conforme

- **Copy literal (Passo 3.6):** todo texto visivel vem do `copy.txt` do brief. Em-dash: **0** no HTML e 0 no copy.
  Aspas curvas nos prompts e no par "déjame revisar" / "aquí está el insight". Fora da copy, so o whitelist:
  skip-link, `aria-label`s, `role="status"`, labels do form e as 4 opcoes do select. Os numeros 01 a 06 das filas sao
  `counter()` de um `<ol>` (marcador de lista, nao texto inventado) e estao `aria-hidden`.
- **Motion com rede (§4):** testado **sem JavaScript** (tudo visivel, o video ate toca) e com **prefers-reduced-motion**
  (0 elementos com opacidade < 0.9, `mac` sem transform, **video pausado**). Tres camadas: `.js` no `<html>`,
  `<noscript><style>` e failsafe de 3,5 s.
- **Contraste AA no escuro:** branco 19:1; secundario `rgba(255,255,255,.64)` cerca de 11:1; laranja `#EB7C2E` sobre
  `#0A0507` 6,9:1. O vermelho `#DE2451` fica em 4,19:1, abaixo de 4.5 para texto pequeno, entao aparece **so** em
  degradado de texto display (acima de 24px em negrito, onde o limite e 3:1) e em brilhos. Botao com degradado
  ambar/laranja e texto quase preto (6,9:1 no ponto mais escuro), porque branco sobre laranja da 2,8:1 e reprova.
- **Video acessivel:** `aria-label` descrevendo o fluxo, botao de pausa com `aria-label` dinamico, sem audio (nao
  precisa de legenda) e os 3 passos em texto ao lado servem de alternativa.
- **§9 copy dita estrutura:** 3 passos, 6 filas, 4 prompts, 4 checks, exatamente o que o copy pede. Sem bloco de
  problema nem de prova social, porque o copy nao tem.
- **§10 posicao do form:** MoFu/BoFu, na 6.ª de 7 secoes, com CTA no hero e na nav levando ate ela.
- **§14:** `min-height:0` em todo `<img>`/`<video>` dentro de grid; `overflow:hidden` nos containers decorativos.
- **§15 SEO:** 1 description, 1 robots, 10 og, 4 twitter, 1 JSON-LD (parseia, `Organization.url` igual a
  `regions.latam.home` do manifest, `sameAs` com LinkedIn e Instagram LATAM), 1 canonical.
- **§16 hreflang:** omitido de proposito, nao ha LP irma com o mesmo slug-base.
- **§17 logo regional:** header e footer para `https://getbuzzmonitor.com/es/` com `target="_blank" rel="noopener"` e
  `aria-label` em espanhol. Nenhum `href="/"`.
- **§19:** so PNG de logo, nenhum SVG com `<text>` vivo.
- **Zero erro de JS.** Barra de progresso a 100%, contador chegando a 50, copiar com anuncio em `role="status"`,
  toggle do video alternando estado e label, sem scroll horizontal em 1440px nem em 390px.

## Melhorias opcionais (4)

- [ ] **Sem bloco de prova social.** O copy nao tem. A §6 pede "prova" e a LP e de intencao comercial. Uma faixa de
      logos de clientes ou as metricas que a `mcp-es` usa ("1.000+ clientes en el mundo", "300+ enterprise") fechariam
      a estrutura. Exige copy aprovada.
- [ ] **Legibilidade do MacBook no mobile.** A UI do Claude a 1024px reduzida para ~350px fica ilegivel. Ja ha um zoom
      de 1,22 abaixo de 640px; um recorte dedicado (so o modal) renderizaria melhor.
- [ ] **"performance"** no bloco VALOR e anglicismo; o padrao ES-LATAM prefere "desempeño". Mantido literal por pedido.
- [ ] **Peso do hero.** Video de 217 KB carrega com `preload="metadata"` e autoplay. Se o LCP incomodar, trocar por
      `preload="none"` com play no primeiro scroll.

## Nice-to-haves (3)

- [ ] Espaco inquebravel em "2 meses" e "50% OFF".
- [ ] `<link rel="preload">` para o CSS do Google Fonts.
- [ ] Uma versao WebM do video (VP9) ao lado do MP4 economizaria mais alguns KB.

## Bloqueios antes de publicar

1. **OG image ausente:** gerar `assets/og-mcp-claude-latam.png` (1200x630).
2. **URL real de "Probar gratis" e "Crear cuenta gratis".**
3. **Destino definitivo do CTA "Conectar ahora".**
4. **Dominio:** `content.buzzmonitor.com` ou `material.buzzmonitor.com`.
5. **Formulario real** (hoje mock, §11).

## Proximos passos

- Design aprovado? `/lp-integrar-form buzzmonitor/mcp-claude-latam "{snippet}"`
- Depois: `/lp-publicar buzzmonitor mcp-claude-latam {dominio}`
