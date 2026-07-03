---
name: social-pipeline
description: Orquestrador completo de redes sociais da Buzzmonitor — costura analytics + planejamento + copies + designs com pausas pra aprovação. Roda mês a mês pra fechar o ciclo. Aceita só Instagram da Buzzmonitor por enquanto.
argument-hint: "[marca] [mes] — ex: buzzmonitor julho | buzzmonitor 2026-07 (default: buzzmonitor mes-atual)"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill, AskUserQuestion, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-fetch, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-search, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-pages, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-update-page
version: 0.2.0
---

# Skill: Pipeline Social Buzzmonitor

Orquestrador que executa o ciclo mensal completo de redes sociais — do aprendizado do mês passado até os designs prontos no Canva. **Você é o maestro**: chama as skills certas na ordem certa, **pausa nos pontos de decisão**, e mantém contexto entre etapas.

## Princípios

- **Dados sempre manuais** — analytics vem via chat, não puxa API
- **Você é uma maestrina, não a banda** — invoque as skills `/social-analytics`, `/social-plan`, `/social-canva` ao invés de reimplementar a lógica delas
- **Pausas explícitas** — entre cada etapa, pergunte com chips antes de seguir
- **Estado salvo em arquivo** — entre execuções (se a Catharina sair e voltar), você lê o que já foi feito no `social-media/{marca}/{YYYYMM}/` e retoma do ponto certo
- **Idempotente** — rodar de novo no meio do mês não quebra; identifica o que já existe

## Passo 0 — Parsing de argumentos

`$ARGUMENTS` tem 2 partes opcionais:
- `marca` (default: `buzzmonitor`) — **única aceita por enquanto**. Outras marcas → recusar com mensagem clara.
- `mes` (default: mês atual) — aceitar `julho`, `julho 2026`, `2026-07`, `07/2026`. Normalizar pra `YYYY-MM`.

Definir:
- `{MARCA}` (ex: `buzzmonitor`)
- `{YYYYMM_ATUAL}` (ex: `2026-07`)
- `{MES_NOME}` em PT-BR (ex: `Julho`)
- `{YYYYMM_ANTERIOR}` (ex: `2026-06`)
- `{PASTA_ATUAL}` = `social-media/{MARCA}/{YYYYMM_ATUAL}/`
- `{PASTA_ANTERIOR}` = `social-media/{MARCA}/{YYYYMM_ANTERIOR}/`

## Passo 1 — Diagnóstico inicial

Cheque o que **já existe** no estado atual antes de fazer qualquer pergunta:

```
- {PASTA_ANTERIOR}/analytics/relatorio.md existe?
- {PASTA_ATUAL}/planejamento-restante.md OU planejamento.md existe?
- {PASTA_ATUAL}/copies/copies-{mes}.md existe?
- {PASTA_ATUAL}/designs/ tem arquivos?
- brand/buzzmonitor/canva-template-ids.json tem cover/narrativa/cta preenchidos?
```

Apresente um quadro de estado **antes de mais nada**:

```
## Pipeline social · Buzzmonitor · {MES_NOME} {ANO}

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
Pra fechar o aprendizado de {MES_ANTERIOR}, preciso dos exports do Meta Business Suite — manda direto aqui no chat (anexa, cola conteúdo, ou aponta caminho do Downloads). Eu organizo na pasta certa.

Exports esperados:
- Posts do mês: Meta Business Suite → Insights → Conteúdo → Exportar
- Agregados: Meta Business Suite → Insights → Resultados → Exportar (Alcance, Seguidores, Visitas, Cliques no link, Interações, Visualizações, Público)

Se faltar algum, sigo com o que chegar e aviso o que ficou de fora.
```

Quando ela enviar:
- Salva cada CSV em `{PASTA_ANTERIOR}/analytics/raw/` com nome padronizado (regra: dados chegam via chat, a skill organiza na pasta certa)
- Invoca `Skill: social-analytics` com argumento `{YYYYMM_ANTERIOR}`

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
args: {YYYYMM_ATUAL}
```

A `/social-plan` v2.0+ vai automaticamente:
- Ler o relatorio.md de {MES_ANTERIOR} (regra)
- Fazer as 4 perguntas obrigatórias com chips (novidade, case, dashboard, sazonal — regra)
- Gerar calendário só com carrossel/imagem (regra)
- Incluir justificativa por post (regra)
- Incluir seção "Sugestões de vídeos pra produzir" (regra)
- Publicar no Notion

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

Pra cada post do calendário aprovado, gerar 1 copy escolhida com:
- **Caption do feed** (regra: todo post tem legenda + slides)
- **Slides em storytelling contínuo** (regra: cada slide puxa o anterior — narrativa com arco, não "insight 1, insight 2")
- **"Por quê esta abordagem"** explicado em 1-2 linhas (regra: a skill escolhe a melhor variação e justifica, em vez de oferecer opções)
- Posts marcados como "pendente aprovação" no calendário ficam **fora do lote**

**Auto-checagem anti-IA (antes de salvar):** rode contagem de `—` em todas as captions e slides — o resultado deve ser **zero**. Releia procurando antítese-por-negação repetida ("não X, mas Y" no mesmo eixo). Se achar, corrija e **conte de novo** (a correção costuma reintroduzir os tiques — regra de re-checagem pós-correção do `regras-anti-ia.md`).

Salva tudo num artefato único:
- Local: `{PASTA_ATUAL}/copies/copies-{mes}.md`
- Notion: siga o "Padrão de página por mês" em `conhecimento/config/notion-ids.md` — ache (ou crie, se não existir) a página-hub `{MES_NOME} {ANO}` dentro de `redes-sociais`, e crie/atualize o child `Copies` **dentro dela** (nunca solto direto em `redes-sociais`, e nunca uma segunda página `Copies` se já existir uma pro mês)

### C.3 — Pausa pra aprovar

```
{N} copies geradas: <link Notion> · <local>

Cada post tem caption + slides em narrativa contínua.

Aprova pra gerar os designs no Canva?
```

Chips: "Aprovado, gera designs" / "Ajustar antes (qual post?)" / "Parar aqui — vou montar manualmente no Canva"

## Passo 5 — Etapa D: Designs no Canva

### D.1 — Verifica pré-requisitos

Lê `brand/buzzmonitor/canva-template-ids.json`. Se `cover`, `narrativa` ou `cta` estiverem null:

```
⚠️ Brand templates do Canva ainda não foram criados ou os IDs não foram registrados.

Pra a /social-canva rodar, você precisa:
1. Criar os 3 brand templates seguindo [brand/buzzmonitor/canva-brand-templates.md](brand/buzzmonitor/canva-brand-templates.md)
2. Me passar os 3 IDs (formato BTM_xxx)

Enquanto isso não acontece, as copies do {MES} já estão prontas. Você pode:
A) Pausar o pipeline aqui — design fica manual no Canva
B) Criar os templates agora e voltar (eu sigo de onde parei)
C) Pular permanentemente a etapa de design — só copies basta
```

Chips: "Vou criar templates agora" / "Design segue manual neste mês" / "Pular design sempre"

Se ela escolher seguir manual: pipeline termina com sucesso, registra no relatório final.

### D.2 — Roda /social-canva em lote

Se templates prontos:
```
Skill: social-canva
args: {PASTA_ATUAL}/copies/copies-{mes}.md
```

A skill itera por todos os posts, gera designs, devolve URLs.

### D.3 — Apresenta links

Apresenta a lista de designs com URLs do Canva, salva também em `{PASTA_ATUAL}/designs/designs-{YYYY-MM-DD}.md`.

## Passo 6 — Etapa E: Fechamento

Apresenta resumo final:

```
## Pipeline de {MES_NOME} {ANO} — Concluído ✅

Entregas:
- Relatório de {MES_ANTERIOR}: <link>
- Planejamento de {MES_ATUAL}: <link>
- Copies (N posts): <link>
- Designs no Canva: N URLs <link>

Próximos passos pra você:
1. Revisa os designs no Canva
2. Exporta como PNG/JPG
3. Programa no Meta Business Suite (caption tá nas copies, slides tá nos designs)
4. No início de {MES_SEGUINTE}, roda /social-pipeline buzzmonitor {MES_SEGUINTE} pra fechar o próximo ciclo
```

## Casos de erro e exceções

- **Marca diferente de buzzmonitor**: parar com mensagem "v0.1 só cobre Buzzmonitor. Outras marcas em backlog."
- **Mês futuro distante** (>2 meses à frente): perguntar se é planejamento antecipado mesmo.
- **Mês muito antigo** (>3 meses atrás): perguntar pra que — pode ser reanálise histórica, ok seguir.
- **Posts marcados como "Pendente aprovação"** no calendário: ficam fora do lote de copies. Aparecem em seção "Bloqueados" no relatório final.
- **CSV faltando** na Etapa A: continuar com o que tem, alertar no relatório o que ficou de fora.
- **Skill subjacente falha**: NÃO tentar recuperar — propagar o erro pra a Catharina com o que aconteceu e onde parou.

## Notas de design

- **Roda no início do mês** — a cadência ideal é 1ª segunda-feira do mês, depois que o mês anterior já fechou.
- **Não substitui as skills individuais** — `/social-analytics`, `/social-plan`, `/social-canva` podem ser invocadas standalone quando precisar (ex: replanejar mid-month, gerar 1 design avulso).
- **Memória entre execuções** — se a pipeline parar no meio, rodar de novo retoma do diagnóstico (Passo 1). Estado mora nos arquivos do filesystem, não em variáveis.
- **Não publica nada automaticamente** — pipeline gera, você revisa e programa. Zero auto-post.
