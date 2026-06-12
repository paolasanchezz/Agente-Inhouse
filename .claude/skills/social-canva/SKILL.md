---
name: social-canva
description: Gera designs no Canva pra cada slide de um carrossel da Buzzmonitor, usando brand templates fixos da marca. Recebe a copy aprovada da /copies, escolhe o template certo por slide (cover, narrativa, CTA), preenche os campos e devolve os links dos designs prontos pra revisar e exportar.
argument-hint: "[copies-file-path] [post-number] — ex: social-media/buzzmonitor/2026-06/copies/copies-junho.md 1 (sem post-number, gera todos)"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, mcp__c185b134-dca1-4634-9a93-8261ae280a3c__create-design-from-brand-template, mcp__c185b134-dca1-4634-9a93-8261ae280a3c__start-editing-transaction, mcp__c185b134-dca1-4634-9a93-8261ae280a3c__perform-editing-operations, mcp__c185b134-dca1-4634-9a93-8261ae280a3c__commit-editing-transaction, mcp__c185b134-dca1-4634-9a93-8261ae280a3c__cancel-editing-transaction, mcp__c185b134-dca1-4634-9a93-8261ae280a3c__get-brand-template-dataset, mcp__c185b134-dca1-4634-9a93-8261ae280a3c__get-design
version: 0.1.0
---

# Skill: Geração de designs no Canva — Buzzmonitor

Sua missão é transformar a copy aprovada (output do fluxo de copies em lote) em designs no Canva, slide por slide, usando os brand templates fixos da Buzzmonitor.

## Pré-requisitos (checar antes de rodar)

1. **MCP do Canva conectado** — a conta Canva da Buzzmonitor precisa estar conectada ao agente.
2. **Templates configurados** seguindo a especificação em [brand/buzzmonitor/canva-brand-templates.md](../../../brand/buzzmonitor/canva-brand-templates.md):
   - **Template "Carrosséis"** com páginas variantes pra cada papel (Capa, Narrativa, CTA) — cada página com seus dataset fields
   - **Template "Estáticos"** com páginas variantes (1 página = 1 layout completo)
3. **Config preenchida** em `brand/buzzmonitor/canva-template-ids.json`:
   ```json
   {
     "carrossel_template": {
       "id": "EAHMXaCZdd4",
       "pages": { "cover": [1, 4], "narrativa": [2, 5, 6], "cta": [3] }
     },
     "estaticos_template": { "id": "...", "pages": { "default": [1, 2, 3] } }
   }
   ```

Note os **arrays** em `pages` — cada papel suporta múltiplas variantes (regra: os 2 templates funcionam como repositórios permanentes de layouts; variantes evitam slides visualmente idênticos em sequência).

Se algum pré-requisito falhar, **pare e oriente o usuário** a completar — não tente improvisar.

## Passo 0 — Parsing de argumentos

`$ARGUMENTS` tem 1 ou 2 partes:
- `copies-file-path` (obrigatório): caminho do arquivo de copies (ex: `social-media/buzzmonitor/2026-06/copies/copies-junho.md`)
- `post-number` (opcional): número do post a gerar. Se omitido, gera **todos os posts** do arquivo em lote.

Default: se nada for passado, mostra erro pedindo o caminho do arquivo.

## Passo 1 — Carregar config do template

```
Read brand/buzzmonitor/canva-template-ids.json
```

Extrair:
- `template_id` = `carrossel_template.id`
- `pages.cover` = número da página da capa
- `pages.narrativa` = número da página de narrativa
- `pages.cta` = número da página de CTA

Se algum estiver null ou ausente → parar, orientar a Catharina a configurar conforme `canva-brand-templates.md`.

**Validação**: rodar `get-brand-template-dataset` no template ID. Confirma que tem os campos esperados (`SELO`, `TITULO`, `PARAGRAFO`, etc.). Se vazio, parar — significa que os dataset fields ainda não foram configurados.

## Passo 2 — Carregar copies

Ler o arquivo de copies passado em `$ARGUMENTS`. Parse esperado:

```markdown
## Post N · DD/MM · Tema
**Caption do feed**:
...

**Slides do carrossel**:
**Slide 1 (cover)**: <texto>
**Slide 2**: <texto>
...
**Slide N (CTA)**: <texto>
```

Pra cada post identificado, extrair:
- `post_number` (N)
- `data` (DD/MM)
- `tema` (do header)
- `caption` (texto do feed — guarda mas não vai pro design, só pro relatório final)
- `slides[]` — lista com `{numero, papel: "cover" | "narrativa" | "cta", texto}`

**Detecção de papel** do slide:
- Slide 1 = cover (papel = "cover")
- Último slide = CTA (papel = "cta")
- Slides do meio = narrativa (papel = "narrativa")

## Passo 3 — Decidir escopo

- Se `post-number` foi passado: filtra só esse post.
- Se não: itera por todos os posts.

Antes de criar designs, mostra ao usuário o resumo do que vai fazer e pede confirmação:

```
Vou gerar designs no Canva pros seguintes posts:
- Post 1 (12/06) — Dia dos Namorados — 7 slides
- Post 2 (15/06) — Reforço webinar — 7 slides
- ...
Total: N designs (N posts × média 7 slides).
Isso vai criar ~N designs novos no seu Canva. Confirma?
```

## Passo 4 — Gerar designs (para cada post)

Pra cada post selecionado, pra cada slide:

### 4.1 Escolher página variante (regra: alternar pra evitar repetição)

`pages.{papel}` é um **array** de números de página variantes. Regra de seleção:

- **Cover** (slide 1): se array tem 1 elemento, usa ele; se múltiplos, escolhe 1 (rotação simples ou aleatório, sem repetir o usado no carrossel anterior).
- **Narrativa** (slides do meio): **itera ciclicamente** pelo array — slide 2 = variante[0], slide 3 = variante[1], slide 4 = variante[2 mod N], etc. Se array tem 1 só, todos os slides do meio usam ela (sem variação possível).
- **CTA** (último slide): se array tem 1, usa; se múltiplos, alterna entre carrosséis.

### 4.2 Criar design a partir da página escolhida

```
create-design-from-brand-template:
  brand_template_id: <template_id>
  page_numbers: [<numero_da_pagina_escolhida>]
  user_intent: "Criar design para slide {N} do post {M} da Buzzmonitor — papel: {papel} · variante: página {X}"
```

Retorna `design_id` e `url`.

### 4.3 Abrir transação de edição

```
start-editing-transaction:
  design_id: <design_id retornado>
  user_intent: "Preencher campos do template com a copy do slide"
```

Retorna `transaction_id`.

### 4.3.5 Validar tamanho de texto (REGRA INEGOCIÁVEL)

**Antes** de aplicar `set_text`, comparar `len(novo_texto)` com `len(texto_original)` (extraído de `containerElement.regions[].text` na resposta de `start-editing-transaction`).

- Se diferença ≤ **±20%** → prosseguir com set_text normal
- Se diferença > 20% → **adaptar o texto da copy** pra caber. Ex: encurtar overline de "Buzz Pills · Dia dos Namorados 2026" (35 chars) pra "BUZZ PILLS" (10 chars) quando o original era "Um lembrete:" (12 chars).
- Se a copy NÃO PODE ser encurtada sem perder mensagem essencial → pular esse elemento, manter placeholder, e **alertar no relatório final** que esse slide precisa de variante de layout com mais espaço.

Layout bagunçado é entrega inaceitável — o texto novo respeita o espaço do layout original; quem se adapta é a copy, não o design.

### 4.4 Mapear copy → campos do template

**Pra Cover (slide 1)**:
- `SELO` ← primeira palavra-chave temática do post (Buzz Pills / Pergunta da semana / Recap / Case / etc — derivar do tema)
- `TITULO` ← texto do Slide 1 da copy
- `SUBTITULO` ← se a copy tiver um "subtítulo" claro, usar; senão deixar vazio

**Pra Narrativa (slides do meio)**:
- `NUMERO_SLIDE` ← `"{N} / {total_slides}"`
- `PARAGRAFO` ← texto do slide
- `DESTAQUE_OPCIONAL` ← extrair primeira métrica/dado em destaque do parágrafo (ex: "3.118 conversas") — opcional

**Pra CTA (último slide)**:
- `HEADLINE_CTA` ← primeira frase do slide (até primeira pontuação forte)
- `CONVITE` ← segunda parte do slide (corpo do convite)
- `DESTINO` ← extrair "link na bio" / "comenta" / "DM" — parte final do slide

### 4.5 Aplicar edições

```
perform-editing-operations:
  transaction_id: <transaction_id>
  operations: [
    { type: "set_text", element_dataset_label: "TITULO", value: "..." },
    { type: "set_text", element_dataset_label: "SELO", value: "..." },
    ...
  ]
```

(A skill descobre os labels reais via `get-brand-template-dataset` em runtime.)

### 4.6 Commitar transação

```
commit-editing-transaction:
  transaction_id: <transaction_id>
  user_intent: "Salvar slide preenchido"
```

Se falhar em qualquer etapa entre 4.3 e 4.6, **chamar `cancel-editing-transaction`** pra não deixar lixo.

### 4.7 Coletar URL

Guardar o `url` do design criado em uma lista `designs_gerados[]`.

## Passo 5 — Output ao usuário

Após processar todos os slides de todos os posts selecionados, entregar:

```markdown
## Designs gerados no Canva

### Post 1 (12/06) — Dia dos Namorados — 7 slides
- Slide 1 (Cover): <url>
- Slide 2 (Narrativa): <url>
- Slide 3 (Narrativa): <url>
- ...
- Slide 7 (CTA): <url>

### Post 2 (15/06) — Reforço webinar — 7 slides
...

Total: N designs criados. Próximos passos:
1. Abra os links acima pra revisar visualmente
2. Ajuste o que precisar diretamente no Canva
3. Exporte cada slide como PNG/JPG na ordem
4. Monte o carrossel no Meta Business Suite na hora de publicar
5. Caption do feed: copia do arquivo de copies (`{path}`) — não tá no design
```

Salvar também esse output em `social-media/buzzmonitor/{YYYYMM}/designs/designs-{YYYY-MM-DD}.md` pra ter rastreio.

## Passo 6 — Publicar resumo no Notion

(Opcional, v0.2). Por enquanto entrega só local + mostra na conversa.

## Notas de design

- **Não rodar sem confirmação** — gerar 50+ designs no Canva é ação com volume; sempre confirmar com chip antes (Passo 3).
- **Caption fica fora do design** — design é só arte. A caption do feed copia-cola na hora de publicar no IG.
- **Erros graciosos** — se 1 slide falhar, segue os outros, e relata no fim quais falharam (com motivo).
- **Não inventar texto** — se um campo do template não tem correspondente claro na copy, deixar vazio. Não preencher com placeholder genérico.
- **Templates evoluem** — quando a Catharina criar novos templates (slide com dado, slide com print, etc.), atualizar `canva-template-ids.json` e estender o mapeamento do Passo 4.3.

## Limitação conhecida

O MCP do Canva atual não expõe `autofill-design` diretamente — usamos o caminho **create + edit transaction**, que é mais verboso mas funciona. Se Canva liberar autofill-design no MCP, simplificar Passo 4 (1 chamada em vez de 4).
