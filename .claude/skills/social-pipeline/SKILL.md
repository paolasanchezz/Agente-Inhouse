---
name: social-pipeline
description: Orquestrador completo de redes sociais das marcas do Grupo Elife (Buzzmonitor, Cxpress, Buzzcreators, Elife) — costura analytics + planejamento + copies + designs com pausas pra aprovação. Roda mês a mês pra fechar o ciclo. Instagram + LinkedIn.
argument-hint: "[marca] [mes] — ex: buzzmonitor julho | cxpress 2026-07 (default: buzzmonitor mes-atual)"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill, AskUserQuestion, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-fetch, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-search, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-pages, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-update-page
version: 1.0.0
---

# Skill: Pipeline Social — Grupo Elife

Orquestrador que executa o ciclo mensal completo de redes sociais — do aprendizado do mês passado até os designs prontos no Canva. **Você é o maestro**: chama as skills certas na ordem certa, **pausa nos pontos de decisão**, e mantém contexto entre etapas. Funciona pra qualquer marca do grupo; as decisões específicas de cada marca (contas, modelo de rede, pilares, cadência) vivem em `brand/{marca}/social-media.json`.

## Princípios

- **Dados sempre manuais** — analytics vem via chat, não puxa API
- **Você é uma maestrina, não a banda** — invoque as skills `/social-analytics`, `/social-plan`, `/social-canva` ao invés de reimplementar a lógica delas
- **Pausas explícitas** — entre cada etapa, pergunte com chips antes de seguir
- **Estado salvo em arquivo** — entre execuções (se o usuário sair e voltar), você lê o que já foi feito no `social-media/{marca}/{YYYYMM}/` e retoma do ponto certo
- **Idempotente** — rodar de novo no meio do mês não quebra; identifica o que já existe
- **Config de marca é fonte de verdade** — nada de decisão hardcoded por marca dentro da skill; o que for específico da marca mora em `brand/{marca}/social-media.json`

## Passo 0 — Parsing de argumentos

`$ARGUMENTS` tem 2 partes opcionais:
- `marca` (default: `buzzmonitor`) — aceita `buzzmonitor` | `cxpress` | `buzzcreators` | `elife`. Qualquer outro valor → recusar com mensagem clara.
- `mes` (default: mês atual) — aceitar `julho`, `julho 2026`, `2026-07`, `07/2026`. Normalizar pra `YYYY-MM`.

Definir:
- `{MARCA}` (ex: `buzzmonitor`)
- `{NOME_MARCA}` = displayName do `brand/{MARCA}/brand-manifest.json` (ex: `Buzzmonitor`)
- `{YYYYMM_ATUAL}` (ex: `2026-07`)
- `{MES_NOME}` em PT-BR (ex: `Julho`)
- `{YYYYMM_ANTERIOR}` (ex: `2026-06`)
- `{PASTA_ATUAL}` = `social-media/{MARCA}/{YYYYMM_ATUAL}/`
- `{PASTA_ANTERIOR}` = `social-media/{MARCA}/{YYYYMM_ANTERIOR}/`

## Passo 0.5 — Carregar e validar config da marca

Leia `brand/{MARCA}/social-media.json`. Ela alimenta todas as etapas (handles, modelo de rede, pilares, cadência, referências).

1. **Arquivo não existe** → PARE. Oriente a criar copiando o formato de `brand/buzzmonitor/social-media.json` (a config da Buzzmonitor é o modelo de referência).
2. **`contas.instagram.handle` é null** → pergunte ao usuário o @ da conta de Instagram da marca (com chip "Não sei agora"). Se responder, **salve de volta no JSON** (Edit) antes de seguir — a config se completa com o uso. Se não souber, dá pra seguir com as etapas B e C (planejamento e copies), mas a Etapa A (analytics) fica bloqueada — avise.
3. **`status` é `rascunho` ou `esqueleto`** → avise em 1 linha que pilares/referências da marca ainda são rascunho derivado do brand-manifest, e que o planejamento vai usá-los como base editável. Não bloqueia.

## Passo 1 — Diagnóstico inicial

Cheque o que **já existe** no estado atual antes de fazer qualquer pergunta:

```
- {PASTA_ANTERIOR}/analytics/relatorio.md existe?
- {PASTA_ATUAL}/planejamento-restante.md OU planejamento.md existe?
- {PASTA_ATUAL}/copies/copies-{mes}.md existe?
- {PASTA_ATUAL}/designs/ tem arquivos?
- brand/{MARCA}/canva-template-ids.json existe e tem cover/narrativa/cta preenchidos?
```

Apresente um quadro de estado **antes de mais nada**:

```
## Pipeline social · {NOME_MARCA} · {MES_NOME} {ANO}

Status do ciclo:
[✅ ou ⏳ ou ❌] Etapa A — Analytics de {MES_ANTERIOR}: <existe? não? pronto?>
[✅ ou ⏳ ou ❌] Etapa B — Planejamento de {MES_ATUAL}: <existe?>
[✅ ou ⏳ ou ❌] Etapa C — Copies de {MES_ATUAL}: <existe?>
[✅ ou ⏳ ou ❌] Etapa D — Designs no Canva: <existe?>

Pronto pra continuar de onde paramos: <Etapa X>
```

Aí entra na primeira etapa pendente.

## Passo 2 — Etapa A: Analytics do mês anterior

### A.1 — Verifica se já tem relatório

Se `{PASTA_ANTERIOR}/analytics/relatorio.md` já existe:
- Mostra o TL;DR resumido (3-5 bullets)
- Pula pra Etapa B

Se NÃO existe:

### A.2 — Pede os CSVs no chat

```
Pra fechar o aprendizado de {MES_ANTERIOR}, preciso dos exports do Meta Business Suite da conta @{handle da config} — manda direto aqui no chat (anexa, cola conteúdo, ou aponta caminho do Downloads). Eu organizo na pasta certa.

Exports esperados:
- Posts do mês: Meta Business Suite → Insights → Conteúdo → Exportar
- Agregados: Meta Business Suite → Insights → Resultados → Exportar (Alcance, Seguidores, Visitas, Cliques no link, Interações, Visualizações, Público)

Se faltar algum, sigo com o que chegar e aviso o que ficou de fora.
```

Quando o usuário enviar:
- Salva cada CSV em `{PASTA_ANTERIOR}/analytics/raw/` com nome padronizado (regra: dados chegam via chat, a skill organiza na pasta certa)
- Invoca `Skill: social-analytics` com argumentos `{MARCA} {YYYYMM_ANTERIOR}`

### A.3 — Apresenta TL;DR e pausa

Após `/social-analytics` rodar, mostra TL;DR (3-5 bullets) e **pausa**:

```
Relatório de {MES_ANTERIOR} pronto: <link Notion> · <caminho local>

Seguimos pro planejamento de {MES_ATUAL}?
```

Chips: "Sim, seguir" / "Antes quero olhar o relatório" / "Parar aqui"

## Passo 3 — Etapa B: Planejamento do mês

### B.1 — Verifica se já tem planejamento

Se já existe: mostra resumo (número de posts, formato vencedor, justificativas) e pergunta se quer regerar ou seguir pra copies.

Se NÃO existe:

### B.2 — Roda /social-plan

```
Skill: social-plan
args: {MARCA} {YYYYMM_ATUAL}
```

A `/social-plan` v4.0+ vai automaticamente:
- Ler a config da marca (`brand/{MARCA}/social-media.json`) — modelo de rede, pilares, cadência, referências
- Ler o relatorio.md de {MES_ANTERIOR} (regra)
- Fazer as 4 perguntas obrigatórias com chips (novidade, case, dashboard/análise, sazonal — regra)
- Gerar calendário só com formatos estáticos (regra)
- Incluir justificativa por post (regra)
- Incluir seção "Sugestões de vídeos pra produzir" (regra)
- Publicar no Notion (hub do mês da marca)

### B.3 — Pausa pra aprovar

Apresenta resumo do calendário (tabela de N posts × data × tema × formato × justificativa) e pausa:

```
Calendário pronto: <link Notion>

Total: N posts em {MES_NOME}. Formato: 100% carrossel/imagem. {N_VIDEO_SUGGEST} sugestões de vídeo na seção separada.

Aprova pra gerar todas as copies em lote?
```

Chips: "Aprovado, gera copies" / "Ajustar antes (qual post?)" / "Parar aqui"

## Passo 4 — Etapa C: Copies em lote

### C.1 — Verifica se já existe

Se `{PASTA_ATUAL}/copies/copies-{mes}.md` existe: mostra status e oferece regerar/seguir.

Se NÃO existe:

### C.2 — Gera copies em lote

**Antes de escrever qualquer copy, leia (obrigatório):**
1. `conhecimento/editorial/regras-anti-ia.md` — caption e slides são texto publicável; valem TODAS as regras, incluindo tolerância zero a em-dash (`—`) e veto a antítese-por-negação em série
2. `conhecimento/copywriting/fundamentos-copy.md` — hooks, estrutura, CTA
3. `brand/{MARCA}/brand-manifest.json` — tom de voz e artigo gramatical da marca (`nameUsage` — ex: "a Buzzmonitor" mas "o Buzzcreators")
4. `conhecimento/produto/{MARCA}/{MARCA}.md` — produto, features e grafias exatas (não inventar feature)

Pra cada post do calendário aprovado, gerar 1 copy escolhida com:
- **Caption do feed** (regra: todo post tem legenda + slides)
- **Slides em storytelling contínuo** (regra: cada slide puxa o anterior — narrativa com arco, não "insight 1, insight 2")
- **"Por quê esta abordagem"** explicado em 1-2 linhas (regra: a skill escolhe a melhor variação e justifica, em vez de oferecer opções)
- Posts marcados como "pendente aprovação" no calendário ficam **fora do lote**

**Auto-checagem anti-IA (antes de salvar):** rode contagem de `—` em todas as captions e slides — o resultado deve ser **zero**. Releia procurando antítese-por-negação repetida ("não X, mas Y" no mesmo eixo). Se achar, corrija e **conte de novo** (a correção costuma reintroduzir os tiques — regra de re-checagem pós-correção do `regras-anti-ia.md`).

Salva tudo num artefato único:
- Local: `{PASTA_ATUAL}/copies/copies-{mes}.md`
- Notion: siga o "Padrão de página por mês" em `conhecimento/config/notion-ids.md` — ache (ou crie, se não existir) a página-hub do mês **da marca** dentro de `redes-sociais`, e crie/atualize o child `Copies` **dentro dela** (nunca solto direto em `redes-sociais`, e nunca uma segunda página `Copies` se já existir uma pro mês)

### C.3 — Pausa pra aprovar

```
{N} copies geradas: <link Notion> · <local>

Cada post tem caption + slides em narrativa contínua.

Aprova pra gerar os designs no Canva?
```

Chips: "Aprovado, gera designs" / "Ajustar antes (qual post?)" / "Parar aqui — vou montar manualmente no Canva"

## Passo 5 — Etapa D: Designs no Canva

### D.1 — Verifica pré-requisitos

Lê `brand/{MARCA}/canva-template-ids.json`. Se o arquivo **não existe**, ou se `cover`, `narrativa` ou `cta` estiverem null/vazios:

```
⚠️ Brand templates do Canva da {NOME_MARCA} ainda não foram criados ou os IDs não foram registrados.

Pra a /social-canva rodar, você precisa:
1. Criar os templates no Canva seguindo a especificação em [brand/buzzmonitor/canva-brand-templates.md](brand/buzzmonitor/canva-brand-templates.md) (vale como modelo pra qualquer marca — use o brand kit da {NOME_MARCA})
2. Registrar os IDs em brand/{MARCA}/canva-template-ids.json (copie o formato do arquivo da Buzzmonitor)

Enquanto isso não acontece, as copies do {MES} já estão prontas. Você pode:
A) Pausar o pipeline aqui — design fica manual no Canva
B) Criar os templates agora e voltar (eu sigo de onde parei)
C) Pular permanentemente a etapa de design — só copies basta
```

Chips: "Vou criar templates agora" / "Design segue manual neste mês" / "Pular design sempre"

Se o usuário escolher seguir manual: pipeline termina com sucesso, registra no relatório final.

### D.2 — Roda /social-canva em lote

Se templates prontos:
```
Skill: social-canva
args: {PASTA_ATUAL}/copies/copies-{mes}.md
```

A skill deriva a marca do caminho do arquivo, itera por todos os posts, gera designs, devolve URLs.

### D.3 — Apresenta links

Apresenta a lista de designs com URLs do Canva, salva também em `{PASTA_ATUAL}/designs/designs-{YYYY-MM-DD}.md`.

## Passo 6 — Etapa E: Fechamento

Apresenta resumo final:

```
## Pipeline de {MES_NOME} {ANO} · {NOME_MARCA} — Concluído ✅

Entregas:
- Relatório de {MES_ANTERIOR}: <link>
- Planejamento de {MES_ATUAL}: <link>
- Copies (N posts): <link>
- Designs no Canva: N URLs <link>

Próximos passos pra você:
1. Revisa os designs no Canva
2. Exporta como PNG/JPG
3. Programa no Meta Business Suite (caption tá nas copies, slides tá nos designs)
4. No início de {MES_SEGUINTE}, roda /social-pipeline {MARCA} {MES_SEGUINTE} pra fechar o próximo ciclo
```

## Casos de erro e exceções

- **Marca fora da lista** (não é buzzmonitor/cxpress/buzzcreators/elife): parar com mensagem clara listando as 4 aceitas.
- **Config da marca ausente** (`brand/{MARCA}/social-media.json` não existe): parar e orientar a criar a partir do modelo da Buzzmonitor (Passo 0.5).
- **Mês futuro distante** (>2 meses à frente): perguntar se é planejamento antecipado mesmo.
- **Mês muito antigo** (>3 meses atrás): perguntar pra que — pode ser reanálise histórica, ok seguir.
- **Posts marcados como "Pendente aprovação"** no calendário: ficam fora do lote de copies. Aparecem em seção "Bloqueados" no relatório final.
- **CSV faltando** na Etapa A: continuar com o que tem, alertar no relatório o que ficou de fora.
- **Skill subjacente falha**: NÃO tentar recuperar — propagar o erro pro usuário com o que aconteceu e onde parou.

## Notas de design

- **Roda no início do mês** — a cadência ideal é 1ª segunda-feira do mês, depois que o mês anterior já fechou.
- **Não substitui as skills individuais** — `/social-analytics`, `/social-plan`, `/social-canva` podem ser invocadas standalone quando precisar (ex: replanejar mid-month, gerar 1 design avulso).
- **Memória entre execuções** — se a pipeline parar no meio, rodar de novo retoma do diagnóstico (Passo 1). Estado mora nos arquivos do filesystem, não em variáveis.
- **Não publica nada automaticamente** — pipeline gera, você revisa e programa. Zero auto-post.
- **Cada marca tem seu ciclo independente** — rodar Cxpress não toca em nada da Buzzmonitor: pastas (`social-media/{marca}/`), hub do Notion e config são namespaced por marca.
