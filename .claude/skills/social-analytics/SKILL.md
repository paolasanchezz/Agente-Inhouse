---
name: social-analytics
description: Gera relatório mensal de performance orgânica do Instagram da Buzzmonitor a partir dos CSVs exportados do Meta Business Suite. Identifica top/bottom posts, padrões por formato e tema, cadência, perfil de audiência e recomendações para o próximo mês. Pensado pra alimentar a /social-plan.
argument-hint: "[YYYY-MM] — ex: 2026-05 (default: mês passado)"
allowed-tools: Read, Write, Edit, Bash, Glob, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-pages, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-fetch
version: 0.1.1
---

# Skill: Análise de Performance Orgânica — Instagram Buzzmonitor

Você é analista sênior de social media B2B. Sua missão é transformar CSVs crus do Meta Business Suite em um relatório de performance que vira input direto pro planejamento do mês seguinte.

## Passo 0 — Parsing de argumentos

Faça parsing de `$ARGUMENTS`:
- **Argumento 1** (`mes_ref`): `YYYY-MM`. Default: mês passado completo (calcule a partir da data atual).
- Defina `{PASTA}` = `social-media/buzzmonitor/{mes_ref}/analytics`

Se o usuário passar formato livre ("maio 2026", "maio", "junho"), normalize pra `YYYY-MM`.

## Passo 1 — Verificar inputs

1. Confira que `{PASTA}/raw/` existe e tem pelo menos um CSV.
2. Liste os arquivos com `Glob` em `{PASTA}/raw/*.csv`.
3. Se a pasta estiver vazia, **pare e oriente o usuário** a enviar os dados **direto no chat** (não pedir pra ela salvar em pasta — você organiza). Mensagem padrão:

   > "Pra rodar a análise de {mes_ref}, preciso dos exports do Meta Business Suite. Manda direto aqui no chat (anexa os arquivos, cola conteúdo, ou aponta o caminho do Downloads) — eu organizo na pasta certa. Os arquivos esperados são:
   > - **Posts do mês**: Meta Business Suite → Insights → Conteúdo → Exportar (filtro Instagram, período do mês)
   > - **Agregados**: Meta Business Suite → Insights → Resultados → Exportar (cada métrica: Alcance, Seguidores, Visitas, Cliques no link, Interações, Visualizações, Público)
   > Se faltar algum, eu sigo com o que chegar e aviso o que ficou de fora."

4. Quando ela enviar (em mensagem subsequente), **eu (skill) salvo cada CSV em `{PASTA}/raw/`** com os nomes padronizados:
   - `posts.csv` (lista de posts individuais)
   - `alcance.csv` · `seguidores.csv` · `visitas.csv` · `cliques.csv` · `interacoes.csv` · `visualizacoes.csv` · `publico.csv` (agregados)

   Identifico qual é qual pelo nome original OU pelo conteúdo (header da primeira linha não-vazia). Se o nome dela não bater, renomeio na hora de copiar. **Não pergunto qual é qual** — descubro.

## Passo 2 — Normalizar CSVs

Rode o helper Python:

```bash
# Python resiliente ao shim da Store no Windows (testa execucao; macOS/Linux -> python3). Single-token.
PYBIN=""; for _c in py python3 python; do command -v "$_c" >/dev/null 2>&1 && "$_c" -c '' >/dev/null 2>&1 && { PYBIN="$_c"; break; }; done; PYBIN="${PYBIN:-python}"
"$PYBIN" .claude/skills/social-analytics/parse_csvs.py {PASTA}/raw
```

Isso gera `{PASTA}/parsed.json` com:
- `posts[]` — lista de posts com type, views, reach, likes, shares, comments, saves, engagement, description, published_at
- `aggregates{}` — séries diárias (alcance, seguidores_novos, visitas_perfil, cliques_link, interacoes, visualizacoes)
- `audience{}` — Principais cidades, Principais países, Faixa etária e gênero

Confira o output do print do helper. Se faltar agregado importante ou public, avise no relatório.

## Passo 3 — Ler dados parseados

`Read` em `{PASTA}/parsed.json`. Pra arquivos grandes, leia em chunks ou foque em campos chave.

## Passo 4 — Análise

### 4.1 Separar contas

Posts vêm de várias contas (a Meta exporta @buzzmonitorbr, @buzzcreatorsbr, e UGC marcando essas contas). Separe:
- **Próprios**: `username == "buzzmonitorbr"` — foco principal do relatório
- **Buzzcreators**: `username == "buzzcreatorsbr"` — análise secundária (linha separada no relatório)
- **UGC**: outras contas marcando as duas — citar como sinal, sem incluir nas médias

### 4.2 Cadência

- Total de posts no mês (próprios)
- Posts/semana (média)
- Comparar com **mínimo recomendado: 3 posts/semana**. Se abaixo, sinalizar como **risco crítico** — orgânico precisa de cadência.

### 4.3 Performance por post (próprios)

Pra cada post, calcule:
- `view_rate` = views / reach (qualidade da impressão)
- `engagement_rate` = engagement / reach × 100 (qualidade do engajamento)
- `save_rate` = saves / reach × 1000 (sinal de valor educativo)

Ordene por views e por engagement. Identifique:
- **Top 3 por views** (alcance) — o que viralizou
- **Top 3 por engagement_rate** (qualidade) — o que conectou
- **Top 3 por saves** — o que vira referência
- **Bottom 3 por views** — o que não funcionou

### 4.4 Médias por formato

Agrupe próprios por `type`:
- "Carrossel do Instagram"
- "Reel do Instagram"
- "Imagem do Instagram"

Pra cada formato: média de views, reach, engagement, n posts. Identifique vencedor e perdedor.

### 4.5 Padrões temáticos (qualitativo)

Leia as descriptions dos top 3 e bottom 3. Identifique:
- **Temas que funcionaram**: cultural / trend-jacking / pergunta aberta / educativo / produto
- **Temas que não funcionaram**
- **Hipóteses** de por quê (cuidado: amostra pequena, marque como hipótese)

### 4.6 Tendências dos agregados

Se `aggregates` estiver populado:
- Seguidores: total ganho no período, média/dia, tendência (subindo/estável/caindo nos últimos 7d vs 7d anteriores)
- Alcance: maior dia, menor dia, pico vs média
- Cliques no link: tendência (relevante pra conversão)
- Interações: dia de pico — cruzar com posts publicados naquele dia

### 4.7 Audiência

Da seção `audience`:
- Top 5 cidades
- Top 3 países (e %BR — sinaliza se internacional cresceu)
- Faixa etária dominante + balanço gênero

### 4.8 Cross-check com Buzzcreators (se houver posts)

Resumo de 3-4 linhas — não é o foco, mas vale registrar performance comparada.

## Passo 5 — Escrever relatório

**Atalho opcional**: rode `_gen_report.py {PASTA}` com o interpretador resolvido (`$PYBIN`, como no Passo 2 — no Windows o `python` do PATH pode ser o shim da Store) — gera um esqueleto mecânico do relatório (rankings, tabelas e agregados prontos). Se usar, **enriqueça o resultado** com o que o script não faz — padrões temáticos (4.5), recomendações pro próximo mês e ajustes de TL;DR — e garanta que o arquivo final siga a estrutura abaixo, que é a fonte de verdade. Se o script e esta estrutura divergirem, vale a estrutura do SKILL.md.

Salve em `{PASTA}/relatorio.md` com esta estrutura:

```markdown
# Relatório de Performance — Instagram Buzzmonitor — {MES_NOME} {ANO}

> Gerado em {DATA_HOJE} a partir de `{PASTA}/raw/` ({N} arquivos)
> Período coberto: {primeira_data} a {última_data}

## TL;DR

3-5 bullets com os achados que mais importam pra o próximo planejamento.

## Cadência

- **{N} posts** publicados no mês
- **Média: {X} posts/semana** ({status: saudável >=3 / abaixo do mínimo <3})
- [se abaixo: ⚠️ recomendação de aumentar cadência]

## Top performers

### Por views (alcance)
Tabela: rank | data | tipo | resumo do tema | views | reach | engagement

### Por engagement rate (qualidade)
Mesma tabela com engagement_rate em %.

### Por saves (referência futura)
Mesma tabela com saves.

## Bottom performers

Tabela bottom 3 + 1 linha explicando padrão observado.

## Performance por formato

Tabela: formato | n posts | avg views | avg reach | avg engagement | veredito (✅/⚠️/❌)

Texto curto: qual formato vencer, qual subutilizar.

## Padrões temáticos

3-5 bullets com hipóteses. Marcar claramente como hipótese se amostra pequena (n<15).

## Audiência

- Top 5 cidades
- Top 3 países
- Faixa etária dominante + gênero

## Tendências agregadas

(se houver agregados — senão, omitir seção)
- Seguidores no período
- Alcance pico vs média
- Cliques no link: tendência

## Recomendações pro próximo mês

5-7 bullets acionáveis. Cada bullet com "por quê" baseado nos dados.

Estes vão alimentar a `/social-plan` quando ela rodar pro próximo mês.

## Buzzcreators (cross-check)

(se houver posts — senão omitir)

## Limitações desta análise

- Amostra de {N} posts
- Período: ...
- Faltam dados de: ... (se algum agregado/secao faltou)
```

## Passo 6 — Publicar no Notion

1. Leia `conhecimento/config/notion-ids.md` e pegue o ID da chave `redes-sociais-relatorios`.
2. Crie uma página filha sob esse parent (`type: page_id`) com:
   - **Title**: `Relatório Performance · Buzzmonitor · {MES_NOME} {ANO}` (ex: "Relatório Performance · Buzzmonitor · Maio 2026")
   - **Icon**: `📊`
   - **Content**: o conteúdo integral do `relatorio.md` em Markdown
3. Anote o URL retornado.
4. Adicione o URL no topo do `relatorio.md` local como linha extra:
   `> **Notion**: <url-da-pagina>`

## Passo 7 — Output ao usuário

Imprima na conversa:
1. Confirmação dos dois destinos: `{PASTA}/relatorio.md` local + URL Notion
2. TL;DR resumida (3-5 bullets)
3. Top 1 post + bottom 1 post
4. Avisar próximo passo: "Pra o planejamento de {próximo mês}, rode `/social-plan {próximo mês}` — ela vai consumir este relatório."

## Notas de design

- **Não consumir dados de outras contas** — esta v0.1 cobre só Buzzmonitor Brasil. Buzzcreators é cross-check, não foco.
- **Hipóteses ≠ conclusões** — amostras menores que 15 posts → sempre marcar achados como hipótese.
- **Cuidado com vieses de poucos dias**: se o mês está incompleto (ex: rodando dia 15), avisar isso no TL;DR.
