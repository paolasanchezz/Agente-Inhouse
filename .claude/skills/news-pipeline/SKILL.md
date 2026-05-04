---
name: news-pipeline
description: Executa o pipeline completo de newsletter semanal — pesquisa + (pausa para aprovar pauta sugerida, se houver lacuna) + criacao de post + geracao + revisao. 1 newsletter por execucao.
argument-hint: "[brand] [region]  — ex: cxpress brasil | buzzmonitor latam | buzzcreators portugal"
allowed-tools: WebFetch, WebSearch, Read, Write, Edit, Agent, Bash, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-fetch, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-pages, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-update-page, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-search
version: 2.0.0
---

# Skill: Pipeline Completo de Newsletter Semanal

Voce e o orquestrador do processo de criacao da newsletter semanal. Execute as etapas abaixo em sequencia, com **pausa explicita** para aprovacao de pauta sugerida quando houver lacuna no blog.

**Esta v2.0** gera 1 newsletter por execucao (em vez de 5). O argumento `foco` foi removido (a v2 escolhe a dor da semana automaticamente a partir do mapeamento de dores + cobertura no blog).

## Passo 0: Parsing de Argumentos

Faca o parsing de `$ARGUMENTS`:
- **Argumento 1** (`brand`): `buzzmonitor` | `buzzcreators` | `cxpress` | `elife` — default: `buzzmonitor`
- **Argumento 2** (`region`): `brasil` | `latam` | `portugal` — default: `brasil`

Mapeamento de `region`:
- `brasil` → idioma: PT-BR | nome idioma: "Portugues Brasileiro" | pasta linguistico: nenhuma | pasta produto lang: nenhuma
- `latam` → idioma: ES-LATAM | nome idioma: "Espanol Latinoamericano" | pasta linguistico: `es-latam` | pasta produto lang: `es`
- `portugal` → idioma: PT-PT | nome idioma: "Portugues Europeu" | pasta linguistico: `pt-portugal` | pasta produto lang: `pt-pt`

Calcule a semana ISO atual: `YYYY-WW`. Salve como `{SEMANA_ISO}`.

---

## Etapa 1: Pesquisa

Execute o fluxo completo da skill `/news-pesquisar` com argumentos `{brand} {region}`.

Consulte `.claude/skills/news-pesquisar/SKILL.md` e execute todos os passos na integra.

**Checkpoint**: verificar que existem em `conhecimento/produto/{brand}/pesquisa/atual/`:
- `dores-candidatas.md`
- `indice-blog.md`
- `dor-semana.md`
- `clipping-pr.md`
- `RESUMO.md`

E que `conhecimento/produto/{brand}/blog-cache.md` foi atualizado.

---

## Etapa 2: Pausa de Aprovacao de Pauta (CONDICIONAL)

Verifique se existe `conhecimento/produto/{brand}/pesquisa/atual/pauta-sugerida.md`.

### Se NAO existir
A dor da semana ja tem cobertura suficiente (≥3 posts) no blog. Pule para Etapa 4 (Geracao).

### Se existir
A pesquisa detectou lacuna — apresente ao usuario e pergunte se aprova a criacao do post novo.

#### Apresentacao ao usuario

Mostre um resumo limpo:
```
A dor da semana e "[Nome da dor]" mas o blog tem cobertura insuficiente
(N posts cobrem parcialmente — ideal seria ≥3).

Pauta sugerida para post novo:

H1: [titulo]
Pergunta-eixo: [pergunta]
Outline: [H2s da pauta]
Tamanho alvo: 1500-2500 palavras

Aprovar criacao deste post de blog?
- SIM → news-criar-post escreve o post, publica draft no Notion, e a news segue.
- NAO → o pipeline pula esta dor e usa a proxima dor candidata com cobertura ≥3.
```

#### Esperar resposta do usuario

**NAO PROSSEGUIR** sem confirmacao explicita.

#### Se aprovado: Etapa 3 (criar post)
#### Se rejeitado:
1. Delete `pauta-sugerida.md` da pasta `atual/` (ou move para `arquivo/{SEMANA_ISO}/rejeitada-pauta-sugerida.md`)
2. Re-executar `news-pesquisar` (Etapa 1) com instrucao adicional ao agente: "ignore a dor X e escolha a proxima dor candidata com cobertura ≥3"
3. Voltar para Etapa 2 com a nova `dor-semana.md` (e nova decisao sobre lacuna)

---

## Etapa 3: Criacao de Post de Blog (CONDICIONAL — somente se pauta foi aprovada)

Execute o fluxo completo da skill `/news-criar-post` com argumentos `{brand} {region}`.

Consulte `.claude/skills/news-criar-post/SKILL.md` e execute todos os passos na integra.

**Checkpoint**: verificar que:
- `newsletter/{brand}/posts-sugeridos/post-{SLUG}-{SEMANA_ISO}.md` existe
- Pagina no Notion sob `Entregas > Drafts de Blog > {NomeDaMarca}` foi criada
- `dor-semana.md` foi atualizado para incluir o novo post como ancora 1
- `_state.json` registrou a pauta consumida

**Aviso ao usuario**:
> O post foi criado como DRAFT no Notion. Antes da news ir ao ar, o time editorial precisa:
> 1. Revisar o draft no Notion
> 2. Publicar no blog real
> 3. Substituir a URL Notion pela URL final do blog em `dor-semana.md` (post-ancora 1)
>
> A news que vou gerar agora cita a URL Notion como temporaria — o time edita antes do disparo.

---

## Etapa 4: Geracao da Newsletter

Execute o fluxo completo da skill `/news-gerar` com argumentos `{brand} {region}`.

Consulte `.claude/skills/news-gerar/SKILL.md` e execute todos os passos na integra.

**Checkpoint**: verificar que:
- `newsletter/{brand}/entregas/newsletter-{SEMANA_ISO}.md` existe (sem subpasta)
- Pagina no Notion sob `Newsletter > {NomeDaMarca}` foi criada
- `_state.json` foi atualizado com pergunta-dor e links da edicao

---

## Etapa 5: Revisao da Newsletter

Execute o fluxo completo da skill `/news-revisar` com argumentos `{brand} {region}`.

Consulte `.claude/skills/news-revisar/SKILL.md` e execute todos os passos na integra.

**Checkpoint**: verificar que:
- `newsletter/{brand}/entregas/newsletter-{SEMANA_ISO}.md` foi sobrescrita com versao revisada
- `newsletter/{brand}/entregas/REVISAO-LOG-{SEMANA_ISO}.md` existe

---

## Etapa 6: Relatorio Final

Crie `newsletter/{brand}/entregas/RELATORIO-{SEMANA_ISO}.md`:

```markdown
# Relatorio — Pipeline Newsletter Semanal {SEMANA_ISO}
**Data**: {DATA}
**Marca**: {NomeDaMarca}
**Regiao**: {region} | **Idioma**: {idioma}

## Pipeline executado

- [x] Etapa 1: Pesquisa (dores, blog, clipping)
- [x] Etapa 2: [Pauta aprovada | Pauta rejeitada e dor trocada | Sem pauta — cobertura suficiente]
- [x] Etapa 3 (se aplicavel): Post de blog criado em draft no Notion
- [x] Etapa 4: Newsletter gerada
- [x] Etapa 5: Newsletter revisada

## Newsletter

- **Edicao**: {SEMANA_ISO}
- **Assunto**: ...
- **Pergunta-eixo**: ...
- **Posts-ancora** (3): listar titulos + URLs
- **Posts secundarios**: N
- **Clipping PR**: N (Veiculo)
- **Bloco extra**: SIM/NAO
- **Total de links contextuais**: N (3-6)
- **Palavras (corpo)**: N (≤600)
- **Status**: APROVADA | REQUER ATENCAO
- **URL Notion**: ...

## Post de blog (se Etapa 3 executada)
- **H1**: ...
- **URL Notion (draft)**: ...
- **Caminho local**: ...
- **Acao requerida do time editorial**: revisar, publicar no blog real, atualizar dor-semana.md com URL final, depois confirmar para disparo da news

## Pendencias
[Itens REQUER ATENCAO da revisao + acoes do time editorial]

## Cadencia automatica (opcional)

Para automatizar a execucao semanal desta marca, use:
- `/loop 7d /news-pipeline {brand} {region}` (modo recorrente in-session)
- ou `/schedule` para criar routine cron remota

Decisao por marca/regiao do usuario — nao auto-agendar.
```

---

## Notas Importantes

- Se qualquer etapa falhar, PARE e informe o usuario com detalhes do erro
- Nao pule a pausa da Etapa 2 — ela e o ponto de aprovacao manual da pauta sugerida
- A criacao de post (Etapa 3) so ocorre apos aprovacao explicita
- A v2.0 gera 1 NL por execucao, no padrao semanal — para multi-marcas em paralelo, rode o pipeline separado por marca/regiao
- O processo completo pode levar alguns minutos devido as buscas web e ao tamanho do post de blog (quando aplicavel)
- Se o contexto ficar muito grande, descarregue arquivos de pesquisa apos cada etapa
