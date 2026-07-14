# Revisão LP — cxpress/cafe-bogota-jul26

**Data:** 2026-07-10
**Auditores:** frontend-design (review mode) + web-design-guidelines + checks determinísticos (SEO/anti-IA/GTM/logo/OG).
**Base:** clone do design já auditado de `gestao-canais-ia-2026`. O `<style>` compartilhado é byte-a-byte idêntico — os achados concentram no que é novo aqui (hero curto + seção "Caso en vivo" + cierre).

## Aplicado automaticamente (13)

**Críticos (2) — ambos herdados do design da LP-referência:**
- [x] **Contraste AA — hero eyebrow.** Royal `#4A69BD` sobre lilás `#D7E2FF` ≈ 4.0:1 (reprova p/ 13px bold). → `.hero .eyebrow{color:var(--navy)}` (~10:1).
- [x] **Countdown inundava screen readers.** `aria-live="polite"` num contador de 1s (WCAG 2.2.2). → trocado por `aria-hidden="true"` (a data está no hero e no JSON-LD).

**Design (3) — refinam as seções que EU adicionei, aproximando do design system da referência:**
- [x] **Perguntas deixam de imitar os cards de benefício** (GUIDELINES §8). Antes: cards com badge circular lilás igual aos `.ben-card` adjacentes. Agora: lista numerada (numerais laranja + pergunta em Bitter itálico), com linha-intro literal da copy-fonte. Corrige também alturas desiguais.
- [x] **Narrativa do "Caso en vivo" alinhada à esquerda** (`.case-lead` + `.case-close`) — parágrafos longos centralizados prejudicavam a leitura; agora seguem o padrão de narrativa do `.context`.
- [x] **Cierre deixa de ser o 3º gradiente.** Era o 3º bloco com o mesmo gradiente royal→navy (dilui o "um momento dramático" das GUIDELINES). Agora navy sólido; os 2 gradientes (form + mapa) seguem iguais à referência.

**a11y / SEO / semântica (8):**
- [x] `html{scroll-padding-top:80px}` — âncoras (#inscripcion etc.) não ficam mais sob o header sticky.
- [x] E-mail: `spellcheck="false" autocapitalize="none"`; Telefone: `inputmode="tel"` (paridade com a LP-ref.).
- [x] `aria-label` do form: removido o "(placeholder)" do nome acessível.
- [x] Faixa de clientes: `loading="lazy"` (abaixo da dobra).
- [x] `<iframe>` noscript do GTM: `title` adicionado.
- [x] "Conoce a Liana y a Cora": `<div>` → `<h3>` (entra no outline do documento).
- [x] Meta description encurtada (~205 → ~158 chars, dentro do alvo do Google).
- [x] `color-scheme:light` + `text-wrap:balance` nos títulos (polish; evita viúvas e controles nativos estranhos no modo escuro do SO).

Validação pós-edição: em-dash **0**, GTM `GTM-WRQ47B9R` (head+noscript) correto p/ LATAM, hero eyebrow ~10:1, question list renderiza (4 itens, Bitter itálico), cierre navy sólido — tudo confirmado no preview.

## Melhorias opcionais (não aplicadas)

- [ ] **Contraste de texto branco semitransparente no início (claro) dos gradientes** (`.a2`, `.cb-lab`, `.signup-sub`) ≈ 4.0–4.2:1 — limítrofe p/ texto pequeno. Herdado do design da referência; não mexi p/ preservar fidelidade ao clone. Se quiser AA estrito, escurecer o 1º stop do gradiente (ex: royal → `#3a56a6`).
- [ ] **`<img>` de logo sem `width`/`height`** — a referência omitiu de propósito (tamanho via CSS; forçar ratio arriscaria distorção). Baixo impacto de CLS.
- [ ] **Tags de locale**: `html lang="es-419"` vs `og:locale="es_CO"` vs JSON-LD `inLanguage="es-CO"`. Todos válidos; `es-419` é obrigatório p/ o hreflang/lang LATAM, `es_CO`/`es-CO` são mais específicos p/ Colômbia. Deixei como está.
- [ ] `translate="no"` em nomes de marca, dica "abre nova aba" nos logos, reticências em placeholders — baixo valor.

## Nice-to-haves

- [ ] Hero H1 "Atención digital desorganizada" é curto e o hero fica levemente esparso. **Mantido de propósito** — é o título que o Victor escolheu. `text-wrap:balance` já ajuda o equilíbrio.
- [ ] JSON-LD `Event` sem `endDate` — adicionar quando o horário de término for definido (hoje local/horário ainda placeholder).

## Placeholders resolvidos (2026-07-14)

Os 4 placeholders intencionais foram preenchidos com as informações do Victor:

1. **Formulário real** — ✅ Jotform `261303944881662` (jsform) integrado via `/lp-integrar-form`. Título interno do form: "Webinar - Cxpress LATAM". Wrapper `.jotform-embed` sem herança de `.form`.
2. **Ponentes** — ✅ 1 card: **Laura Rodríguez · Cxpress** (foto `assets/laura-rodriguez.jpg`, sem cargo). 2º card removido.
3. **Local (venue)** — ✅ **Edificio Ecotek**, Cl. 99 #10-57, cerca del Parque de la 93 · Bogotá. Atualizado em `.reach-addr`, iframe do mapa e JSON-LD.
4. **OG image** — ✅ `og-cafe-bogota-jul26.png` (1200×630) gerada com o design system Cxpress.

## Back-port recomendado

Os 2 críticos de a11y (contraste do hero eyebrow + countdown com `aria-live`) existem também na LP-referência `gestao-canais-ia-2026` (mesmo `<style>`). Vale aplicar lá também.

## Próximo passo

Design revisado. Publicação: definir estratégia do form mock + índice (ver decisão pendente), depois `/lp-publicar cxpress cafe-bogota-jul26 content.cxpress.io`.
