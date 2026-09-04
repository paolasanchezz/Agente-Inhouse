# Revisão — cxpress/webinar-whatsapp-pt (+ -confirmado)

**Data:** 2026-09-04
**Escopo:** as duas LPs (`webinar-whatsapp-pt` e `webinar-whatsapp-pt-confirmado`)
**Método:** checklists da `lp-gerar` (4.1 técnico · 4.1.1 SEO · 4.1.2 header/footer · 4.2 fidelidade
de copy) + auditoria de contraste WCAG calculada sobre os estilos computados no browser +
`bump_mobile_type.py` (GUIDELINES §20) + medição de overflow a 375×812 e 1440×900.

> `check_mobile_type.py` **não** pôde rodar: o Playwright desta máquina está quebrado
> (`ImportError: DLL load failed while importing _greenlet`). A medição de overflow foi feita
> pelo browser embutido, com o mesmo critério (elemento visível cuja borda direita passa da
> largura do viewport). Vale corrigir o Playwright antes do próximo `/lp-revisar`.

---

## CRÍTICOS — aplicados

### 1. Contraste do CTA laranja reprovava AA (2,58:1)
`.btn-accent` usava texto branco sobre `--accent` `#EF863C`. Isso dá **2,58:1**, contra os
4,5:1 exigidos (o botão tem 15px bold, que não conta como "texto grande" pela WCAG: o corte é
18,66px bold). Atingia o CTA principal do formulário ("Quero ver o webinar") e o CTA final.

**Correção:** texto passou a `--primary-dark` (navy) sobre o mesmo laranja → **5,23:1**. O
`:hover` também mudou: `--accent-hover` de `#dd7730` para `#f7a065` (clarear em vez de escurecer),
porque navy sobre `#dd7730` dava 4,34:1 e continuava a reprovar. Navy sobre `#f7a065` dá 6,53:1.

⚠️ **Isto divergiu das LPs irmãs.** `webinar-tecnologia-pt`, `banimento-whatsapp-pt` e as outras
Cxpress no ar usam o mesmo `.btn-accent` com texto branco, ou seja **todas carregam a mesma
falha**. Não reverti aqui (GUIDELINES §7 é non-negotiable e o BRANDBOOK lista "texto branco
sobre fundos de cor primary sem contraste suficiente" como anti-pattern). Fica a decisão da
Marielle: ou aceitamos a diferença visual, ou faço o back-port para as irmãs num PR separado.

### 2. Número do card de programa reprovava (2,58:1)
`.program-number` (`01`/`02`/`03`, 42px 800) em `--accent` sobre branco. Mesmo como texto grande
(mínimo 3,0:1) não passava.
**Correção:** token novo `--accent-dark: #c2650f` → **4,07:1**. Mantém a identidade laranja.

### 3. Texto sobre o gradiente do CTA final reprovava
`.closing-body` (branco a 88%) dava 4,43:1 e `.closing-meta` (branco a 78%) dava 3,85:1 no ponto
mais claro do gradiente (`#4A69BD`). Idem `.platform-body` / `.platform-note` na thanks page.
**Correção:** branco puro nos quatro → **5,19:1**. A hierarquia passa a vir de tamanho e peso.

### 4. Badge de confirmação reprovava na thanks page
`.confirm-badge` em `--success` `#16a34a` sobre `--success-bg` `#dcfce7` dava 3,0:1 num texto de
14px.
**Correção:** token `--success-strong: #15803d` → **4,57:1**.

### 5. Separador órfão no `hero-meta`
O `hero-meta` tinha um só item ("Inscrição gratuita") mas herdou o `.meta-dot` do padrão de dois
itens, e o ponto aparecia solto a abrir a linha, com cara de bullet perdido.
**Correção:** ponto removido do hero. Onde há dois itens (CTA final, thanks page) ele fica.

### 6. Pisos de tipografia mobile (GUIDELINES §20)
`bump_mobile_type.py` subiu 6 clamps na LP principal e 1 na thanks page (mínimos de 28/30px para
34px nos H2 de secção com máximo ≥44px, e 20→22px no fechamento do comparativo). Desktop intacto.

### 7. Em-dash em comentário de HTML
3 ocorrências de `—`, todas dentro de comentários (não visíveis). A validação da GUIDELINES §5 é
`grep -c "—" index.html` = 0, sem exceção para comentário. Trocados por vírgula e dois pontos.
**Contagem final: 0 em ambas as LPs.**

---

## VERIFICADO — sem achados

| Verificação | Resultado |
|---|---|
| Contraste WCAG AA (todos os nós de texto, estilo computado, alfa e gradiente resolvidos) | 0 falhas nas 2 LPs |
| Overflow horizontal a 375×812 | 0 (só o `.skip-link`, off-screen de propósito) |
| Overflow horizontal a 1440×900 | 0 |
| `h1` único · hierarquia de headings | 1 `h1`, 0 saltos de nível |
| Inputs com `label[for]` | 4/4 |
| Links com nome acessível | 100% |
| `target="_blank"` com `rel="noopener"` | 100% |
| Imagens com `alt` ou `aria-hidden` | 7/7 |
| `<html lang>` | `pt-PT` nas duas |
| Form em mock | `action="#"` + `onsubmit="event.preventDefault()"` |
| Fallback do reveal sem JS | `<noscript>` com `.reveal{opacity:1}` presente |
| `prefers-reduced-motion` | bloco presente, desliga reveal e scroll suave |
| SEO §15 | 1 description · 10 og · 4 twitter · 1 JSON-LD (parseia) nas duas |
| Logo header/footer aponta para home regional (§17) | `https://www.cxpress.pt`, 0 `href="/"` |
| SVG de logo sem `<text>` vivo (§19) | os 3 SVGs Cxpress dão `grep -c '<text'` = 0 |
| Favicon (§12) | `logo-icon.png` do brand, 1 único `<link rel="icon">` |
| GTM da região (§5 do CONTEXT) | `GTM-NW6V5KBM` (portugal), no `<head>` e no `noscript` |
| OG image (§18) | `og-webinar-whatsapp-pt.png`, 1200×630, 60 KB, 1 ficheiro só |
| Fidelidade da copy (4.2) | ver abaixo |
| Contagem de blocos = contagem da copy (§9) | 5 dores · 3 programa · 3 formas · 4 benefícios · 3 COEX · 4 para-quem |
| `min-height: 0` em `<img>` dentro de grid (§14) | presente nos 3 mascotes |
| Anti-IA | em-dash 0 · antítese-por-negação 1 (limite 2) · 0 exclamações · 1 pergunta retórica por secção |

### Fidelidade da copy (checklist 4.2)

Todo texto visível vem literal do `copy.txt`. O que está fora dele cai na whitelist da `lp-gerar`:

- **Ticket boilerplate factual** (hero): `Formato / Online`, `Duração / 10 minutos`,
  `Investimento / Gratuito`. Whitelist item 2.
- **Labels de secção** (`O que costuma acontecer`, `O que está em jogo`, `Programa`,
  `Comparativo`, `Migração`, `COEX`, `Para quem`, `Antes de entrar`): eyebrows de navegação,
  ≤4 palavras, sem repetir informação da copy. Whitelist item 1. `COEX` é literal da copy.
- **Numeração** `01/02/03` e `1..4`: ordinais decorativos, `aria-hidden`.
- **Pills de canais** (`WhatsApp`, `Instagram`, `Facebook`, `E-mail`, `Chat`, `Telefonia`):
  repetição literal dos canais que a frase logo acima já lista, em `aria-hidden` para não
  duplicar no leitor de ecrã.
- **Form labels + disclaimer**: literais da copy. Whitelist item 3.
- **Footer + skip link + aria-labels**: whitelist itens 4 e 5.

Zero pull-quote inventado, zero kicker novo, zero disclaimer de marketing fora da copy, zero
frase-âncora truncada, zero sinónimo trocado.

---

## OPCIONAIS — não aplicados

1. **`hreflang` cruzado com a versão ES.** Existe `webinar-bloqueo-whatsapp` (ES-LATAM), que é
   este mesmo webinar. Nenhuma das duas declara `hreflang` hoje. Cruzar exige editar também a LP
   ES, que está no ar, e sai do escopo deste pedido. Esta LP declara só `canonical` para si mesma,
   que é o comportamento correto de LP única. Se quiser, faço as duas pontas num PR à parte.
2. **Back-port do fix de contraste do `.btn-accent`** para as LPs Cxpress já publicadas (ver
   Crítico 1).
3. **Prova social.** A GUIDELINES §6 prevê secção de prova (speakers/cases) e a LP não tem, porque
   a copy não tem, porque o deck não tem, e o BRANDBOOK proíbe inventar case não verificado
   ("Não inventar cases, aguardar validação interna"). Quando houver case PT validado, entra
   entre `PARA QUEM` e `URGENCIA`.
4. **Logo da OG image** está a 58px de altura, discreta. Dá para subir a 72px se quiser mais
   presença de marca no preview do WhatsApp/LinkedIn.
