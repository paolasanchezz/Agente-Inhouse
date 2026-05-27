# Criativos — GUIDELINES universais

> Regras de design para imagens de criativo (estatico/carrossel) de TODAS as marcas do Grupo Elife.
> Co-desenhadas com o Victor em 2026-05-27. Lidas pela skill `/criativo` antes de gerar e de revisar.
> Valores exatos de marca (cor, fonte, radius) vem de `brand/{marca}/tokens.json` +
> `generation-rules.json`. Aqui ficam as regras UNIVERSAIS de formato, composicao e processo.

---

## 1. Formatos & dimensoes

| Formato | px | Plataforma |
|---|---|---|
| `1x1` | 1080×1080 | Quadrado — universal (IG / FB / LinkedIn) |
| `4x5` | 1080×1350 | Vertical — **default do feed** (mais area, melhor presenca) |
| `9x16` | 1080×1920 | Stories / Reels |

- Carrossel: **todos os cards no mesmo formato**.
- Default quando o uso nao especificar: **`4x5`**. Os demais saem sob pedido (aceita CSV).

## 2. Uso & safe-zones

A margem de seguranca muda conforme `uso` × `formato`:

| uso | Feed (1x1, 4x5) | Stories/Reels (9x16) |
|---|---|---|
| `organico` | margem estetica ~7%; mascote pode sangrar a borda | topo ~120px / base ~160px / lados 64px |
| `anuncio` | margem ~10%; conteudo critico (logo/texto/numero/CTA) dentro | **topo 250px / base 340px / lados 64px** (reservas da UI do Stories/Reels) |

- Em `anuncio`, a skill **gera um overlay-guia** (`-guia.png`): faixas vermelhas nas zonas reservadas
  + retangulo verde tracejado da area segura, pra QA visual.
- Em `anuncio`, a skill **avisa se a peca estiver muito textual** (a entrega do Meta penaliza) e
  sugere enxugar.
- A skill **NAO recompoe a peca sozinha** pra caber na safe-zone (nao move mascote/decorativo
  automaticamente). O guia mostra a margem; a revisao sinaliza vazamento; **a recomposicao e
  decisao humana** — preserva a composicao que voce desenhou.

## 3. Escolha da engine

Duas engines independentes — cada uma monta a peca inteira:

- **HTML/CSS + Playwright = padrao.** Texto pixel-perfect. Use em qualquer peca com texto/numero
  critico (a grande maioria). Renderiza via Chromium headless, DPR=1.
- **Bloom (IA) = opt-in.** Peca inteira gerada por IA — so quando o CONCEITO e um key-visual
  generativo (cena, ilustracao). **Risco de tipografia PT-BR** (acentos/c saem tortos) -> revisao
  reforcada no Passo de revisao (regenerar / `bloom_edit_image` se o texto sair corrompido).
- **Bloom e desligavel.** Sem assinatura/MCP do Bloom conectado, a opcao **nao aparece** e tudo
  vai por HTML. A skill detecta e degrada sem erro.

> Regra pratica: na duvida, HTML. Bloom so quando o usuario pede explicitamente um visual de IA.

## 4. Estrutura (a copy dita)

- **A COPY dita a estrutura** — sem template fixo (mesma regra das LPs: GUIDELINES de LP §9).
  Se a copy tem 3 cards, saem 3; se tem 7, saem 7.
- **Arco de referencia** (carrossel, so sugestao): cover → contexto → insight → conector → CTA.
- **Estatico de referencia**: hook (+ sub) + CTA.

## 5. Tipografia & hierarquia

- Titulo na **fonte display** da marca; corpo na **fonte body**. NUNCA display em corpo longo
  (ex: Cxpress = Open Sans no titulo, Source Sans 3 no corpo; Bitter so destaque, nunca corpo).
- **Uma ideia por card.** Hierarquia clara: hook > corpo > stat/CTA.
- Numero/dado com destaque visual (tamanho/peso/chip).

## 6. Cor

- **60/30/10.** So a paleta da marca (`tokens.json`) — sem cor de fora.
- Numero/dado destacado em **acento** (laranja/amarelo) — **NUNCA vermelho**.
- **WCAG AA: a skill auto-corrige a cor de texto pra passar AA** (contraste e regra, nao gosto).
  Cilada classica: texto **branco sobre laranja** claro (Cxpress `#EF863C` / Buzzmonitor) **reprova**
  -> usar texto escuro (navy/primaryDark) sobre o laranja, ou fundo escuro + texto branco.

## 7. Decorativos

- So as **formas canonicas da marca** (pills/arcos na Cxpress), nas cores da paleta.
- Respeitar o **limite do `generation-rules`** (ex: Cxpress max 5 formas). Combinar em grupos.
- Longe do texto e da zona critica; em cantos. Sem formas nao-canonicas (triangulo, estrela).

## 8. Mascote

- So **renders oficiais** de `brand/{marca}/assets/mascot/`. **Nunca redesenhar** nem mudar cor.
- Usar **so quando agrega** calor humano ao conceito — nao como enchimento.
- A **regra de marca** (`generation-rules.adCreative`) pode sobrepor (ex: capa de carrossel Cxpress
  pede "mascote visivel"). Nesse caso, segue a regra da marca.

## 9. Fidelidade & adaptacao da copy

Comportamento **ADAPTATIVO**, conforme a qualidade da copy que chega:

- Copy **ja bem estruturada e que encaixa** no layout → **preferir LITERAL** (so diagramar, sem mexer).
- Copy **crua/desestruturada** → **adaptar estrutura** (quebrar em cards/blocos), **enxugar leve**
  pra caber, e passar **anti-IA** (`conhecimento/editorial/regras-anti-ia.md`).
- **SEMPRE preservar numeros, dados e claims EXATOS.** Nunca inventar frase, hook ou CTA novo.
- Rotulos curtos neutros de organizacao visual (ex: "Antes" / "Depois") sao permitidos.
- Grafia + artigo da marca conforme `nameUsage` do manifest (a Cxpress / a Buzzmonitor / o Buzzcreators;
  ES-LATAM sem artigo).

## 10. Revisao da imagem (automatica, antes de entregar)

A skill **le (Read) cada PNG** e confere:

- [ ] **Copy fiel** — numero/texto literal bate com `copy.txt` (ex: 8.200, 62%, 9.023, 100%).
- [ ] **Marca** — paleta, fontes (display vs body), grafia + artigo.
- [ ] **Contraste** — tudo legivel, AA.
- [ ] **Layout** — sem overflow/colisao, respiro adequado.
- [ ] **Safe-zone** (so `anuncio`) — nada critico nas faixas reservadas (conferir `-guia.png`).
- [ ] **Tipografia** — sem caractere torto/trocado. **Atencao redobrada no Bloom** (acentos/c).

Comportamento: **auto-corrige o corrigivel e re-renderiza ate passar** no checklist (combina com o
auto-corrigir contraste da §6). Peca Bloom com texto corrompido → regenerar ou `bloom_edit_image`.

## 11. Entrega

- Pasta `criativos/{marca}/{regiao}/{slug}/`: `copy.txt` + fontes (HTML/CSS) + PNGs + `-guia.png` (anuncio).
- `criativos/` e **gitignored** (PNGs pesados, sem PII no git; este GUIDELINES e a unica excecao
  versionada). Entregar o **caminho absoluto no chat** pro Victor abrir no Explorer e subir manualmente.
  **Sem upload automatico** (base64 trunca >3KB — ver memoria `feedback-criativos-pasta-local`).
- **Entrega direto apos a auto-revisao** (sem pausa de aprovacao). O usuario pede ajuste depois, se quiser.

---

## Lembretes de marca

- **Cxpress — cases pendentes:** BRANDBOOK marca "Cases de Sucesso Verificados" como vazio. Se a copy
  citar metrica/numero de cliente (BoFu/prova social), avisar que precisa validacao comercial antes de publicar.
- **Branco sobre laranja** (Cxpress/Buzzmonitor) reprova AA → texto escuro (ver §6).
- **Pre-requisito tecnico** (engine HTML): Playwright + Chromium —
  `python -m pip install playwright && python -m playwright install chromium`.
