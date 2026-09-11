# Revisao LP — buzzmonitor/mcp-claude-latam

**Data:** 2026-09-10
**Auditores:** frontend-design (review mode, contra GUIDELINES §1-§20) + web-design-guidelines (Vercel Labs Web Interface Guidelines)
**Checks deterministicos:** `check_gtm_region.py` (ok · GTM-MKQBX2MG · latam) · `bump_mobile_type.py` (aplicado) · `check_mobile_type.py` (sem overflow real)

## Aplicado automaticamente (9)

Na geracao (lp-gerar Passo 4):

- [x] **A11y / contraste AA** — `.step__n` estava em `rgba(57,1,85,.26)` e `.step__t` em `rgba(26,26,26,.45)` (texto atenuado ate o passo ficar ativo), ambos abaixo de 4.5:1. Numero passou a `var(--ink-2)` e o texto do passo perdeu o dimming. O realce do passo ativo ficou por conta da cor do numero + trilho laranja.
- [x] **HTML invalido** — `<span class="rail">` era filho direto de `<ol>`. Trilho movido para um wrapper `div.steps`, com `<ol class="steps-list">` dentro.
- [x] **Logo ilegivel** — `logo-primary.png`/`logo-reversed.png` sao 250×250 com o wordmark so no miolo (bbox 10..237 × 96..142); com `height:30px` o wordmark saia com ~5px. Criado `.logo-clip` (caixa com `overflow:hidden` + imagem sobredimensionada e deslocada) para o wordmark render a ~26px no header e ~30px no rodape.
- [x] **H1 quebrando em 5 linhas** — `clamp(36px,6.2vw,78px)` estourava a coluna do hero e destruia a mascara de revelacao linha a linha. Reduzido para `clamp(36px,4.9vw,64px)` e coluna do hero para `1.14fr/.86fr`.
- [x] **Pisos tipograficos mobile (GUIDELINES §20)** — `bump_mobile_type.py` aplicado: 14 clamps e 8 regras px subidas (corpo 18px, H2 34px, labels 15-16px no mobile).

Na revisao (lp-revisar Passo 4):

- [x] **`outline:none` sem substituto para teclado** — `.field input:focus` matava o outline tambem no foco por teclado. Agora o outline so some em `:focus:not(:focus-visible)`; teclado mantem o anel.
- [x] **Header sticky cobrindo o alvo das ancoras** — adicionado `section[id]{scroll-margin-top:92px}`. Validado: apos clicar em "Agendar una demo", o topo da secao fica em 92px e a base do header em 70px.
- [x] **Feedback do "Copiar enlace" invisivel para leitor de tela** — o botao so trocava de icone. Adicionado `<span class="sr-only" role="status">` que anuncia "Enlace copiado" e limpa apos 2,2s.
- [x] **Input de email** — adicionados `inputmode="email"` e `spellcheck="false"`; logo do rodape ganhou `loading="lazy" decoding="async"`.

## Verificado e conforme

- **Copy literal (Passo 3.6):** todo texto visivel vem de `copy.txt`. Em-dash: **0** no HTML e 0 no copy.txt. Aspas curvas em "déjame revisar y te confirmo". Frase-ancora do fechamento integra. Fora da copy, so o permitido pela whitelist: skip-link, `aria-label`s, `role="status"`, labels do form e as 4 opcoes do select.
- **Motion com rede (GUIDELINES §4):** testado **sem JavaScript** (tudo visivel, sublinhado laranja desenhado) e com **prefers-reduced-motion: reduce** (0 elementos com opacidade < 0.9). Tres camadas: classe `.js` no `<html>`, `<noscript><style>` e failsafe de 3,5s.
- **Secoes-tipo (§8):** beneficios em grid com marca de check (6 = 6 da copy); urgencia com fundo escuro e tag quente rotacionada, uma unica vez na LP. A copy nao tem bloco de problema nem de prova social, entao a LP nao inventou nenhum (§9).
- **Posicao do form (§10):** MoFu/BoFu, form na 6.ª de 7 secoes, com CTA no hero rolando ate ele.
- **SEO (§15):** 1 description, 1 robots, 10 og, 4 twitter, 1 JSON-LD (parseia, `Organization.url` = `regions.latam.home` do manifest, `sameAs` com LinkedIn + Instagram LATAM), 1 canonical.
- **hreflang (§16):** omitido de proposito. Nao existe LP irma com o mesmo slug-base (`mcp`, `mcp-es`, `mcp-pt` sao outra familia). Se virar familia, o bloco precisa entrar nas 3.
- **Logo regional (§17):** header e footer apontam para `https://getbuzzmonitor.com/es/` com `target="_blank" rel="noopener"` e `aria-label` em espanhol. Nenhum `href="/"`.
- **§19:** LP usa so PNG de logo, nenhum SVG com `<text>` vivo.
- **§14:** `min-height:0` em todo `<img>` dentro de grid; `overflow:hidden` nos containers decorativos.
- **Zero erro de JS** no console; barra de progresso, trilho dos passos, contador do 50% e revelacao palavra a palavra do CTA final funcionando.

## Melhorias opcionais (5)

- [ ] **Sem bloco de prova social** — a copy nao tem. A estrutura minima da §6 pede "prova" e a LP e de intencao comercial. Considerar faixa de logos de clientes ou as metricas que a `mcp-es` usa ("1.000+ clientes en el mundo", "300+ enterprise"). Exige copy aprovada antes.
- [ ] **Secao de pausa (§2)** — a de prompts e a mais aerea, mas nenhuma secao e puramente "respiro". Se a LP parecer densa na leitura final, aumentar o `--pad` em 20%.
- [ ] **Trilho dos passos** — hoje o trilho fica entre o numero e o texto. Alternativa: mover para a esquerda dos numeros, com o numero centrado sobre ele.
- [ ] **`<blockquote>` nos prompts** — sao exemplos de pergunta, nao citacoes. `<ul>/<li>` seria mais preciso semanticamente (impacto baixo, nenhum leitor de tela quebra).
- [ ] **Icone de check dos cards** — `var(--orange-ink)` sobre pessego fica suave; um tom mais escuro daria mais presenca.

## Nice-to-haves (3)

- [ ] Espaco inquebravel em "2 meses", "2 minutos" e "50% OFF" para evitar quebra feia em telas estreitas.
- [ ] `<link rel="preload">` para o CSS do Google Fonts.
- [ ] O anel tracejado laranja do diagrama do hero (`.r2`) quase nao aparece em fundo claro; subir a opacidade se quiser mais presenca.

## Bloqueios antes de publicar

1. **OG image ausente** — gerar `assets/og-mcp-claude-latam.png` (1200×630). Nome unico, nunca `og-image.png` (§18).
2. **URL real de "Probar gratis" / "Crear cuenta gratis"** — hoje apontam para a home ES com UTM. Trocar pela URL de signup/trial se existir.
3. **Dominio** — decidir entre `content.buzzmonitor.com` (conteudo ES-LATAM) e `material.buzzmonitor.com` (onde vivem as outras LPs de MCP).
4. **Formulario real** — hoje mock (§11). Rodar `/lp-integrar-form` so depois do design aprovado.

## Proximos passos

- Design aprovado? -> `/lp-integrar-form buzzmonitor/mcp-claude-latam "{snippet}"`
- Depois: `/lp-publicar buzzmonitor mcp-claude-latam {dominio}`
