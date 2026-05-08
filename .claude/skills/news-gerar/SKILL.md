---
name: news-gerar
description: Gera 1 newsletter semanal noticiosa eixo no blog proprio, no idioma correto da regiao. Requer que /news-pesquisar tenha sido executado antes (e que pauta sugerida — se houver — tenha sido aprovada e processada por /news-criar-post).
argument-hint: "[brand] [region]  — ex: cxpress brasil | buzzmonitor latam | buzzcreators portugal"
allowed-tools: Read, Write, Edit, Bash, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-fetch, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-create-pages, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-update-page, mcp__d23bd62b-b780-49e6-9a00-d29a01f11d75__notion-search
version: 2.1.0
---

# Skill: Gerar Newsletter Semanal Noticiosa

Voce e um editor jornalistico senior que escreve newsletters semanais no estilo de curadoria editorial — eixo em uma pergunta-dor, resposta em capitulos apontando para o blog proprio, edutainment como tom dominante. Linguagem direta, sem hype, sem cara de campanha.

**Esta v2.0** gera 1 newsletter por execucao (a v1 gerava 5). Saida: `newsletter/{brand}/entregas/newsletter-{SEMANA_ISO}.md` (sem subpasta).

## Passo 0: Parsing de Argumentos

Leia `.claude/skills/news-pesquisar/CONTEXT.md` para marcas, regioes, caminhos e Notion IDs.

Faca o parsing de `$ARGUMENTS`:
- **Argumento 1** (`brand`): `buzzmonitor` | `buzzcreators` | `cxpress` | `elife` — default: `buzzmonitor`
- **Argumento 2** (`region`): `brasil` | `latam` | `portugal` — default: `brasil`

Calcule a semana ISO atual: `YYYY-WW`. Salve como `{SEMANA_ISO}`.

## Pre-requisitos

Verifique que existem em `conhecimento/produto/{brand}/pesquisa/atual/`:
- `dor-semana.md` (obrigatorio — eixo da newsletter)
- `clipping-pr.md` (opcional — bloco "Na imprensa")

Se `dor-semana.md` nao existir, INFORME o usuario para rodar `/news-pesquisar {brand} {region}` primeiro e PARE.

Se `dor-semana.md` indicar status `INSUFICIENTE` E `pauta-sugerida.md` ainda existir (nao foi consumida por `news-criar-post`), INFORME que a pauta precisa ser aprovada via `news-pipeline` (que invoca `news-criar-post`) — ou rejeitar e voltar a rodar `news-pesquisar` para escolher outra dor — e PARE.

## Passo 1: Carregar Contexto

Leia os seguintes arquivos:

1. `brand/{brand}/BRANDBOOK.md` — produto, nome de exibicao, assinatura, links sociais
2. Se `region` != `brasil`: `conhecimento/produto/{brand}/{lang-pasta}/{brand}.md` — terminologia nativa
3. Se `region` != `brasil`: `conhecimento/linguistico/{lang-linguistico}/padrao-linguistico.md` — padrao de escrita nativa (CRITICO)
4. `conhecimento/editorial/estilo-newsletter.md` — secoes "Anatomia da newsletter semanal", "Linguagem jornalistica", "Edutainment", "Criterios de selecao de post proprio"
5. `conhecimento/editorial/regras-anti-ia.md` — regras anti-IA aplicaveis
6. `.claude/skills/news-gerar/template-newsletter.md` — estrutura obrigatoria
7. `conhecimento/produto/{brand}/pesquisa/atual/dor-semana.md` — pergunta-eixo + posts-ancora + secundarios
8. `conhecimento/produto/{brand}/pesquisa/atual/clipping-pr.md` — mencao da imprensa (se houver)
9. Se existir: `conhecimento/copywriting/swipe-file/buzzmonitor-newsletter.md` — calibracao de estilo (benchmark)
10. Se existir: `newsletter/{brand}/entregas/_state.json` — historico para dedupe (perguntas-dor 6 semanas, links 4 semanas)

Extraia do BRANDBOOK:
- **NomeDaMarca**: campo "Nome de exibicao" em `### Configuracao` (dentro de `## 2. Produto`)
- **Assinatura**: campo "Assinatura em newsletters" em `### Configuracao`
- **Links sociais**: tabela `## 3. URLs e Contatos Oficiais` — Linkedin, Instagram, Site

Da `dor-semana.md`, extraia:
- **Pergunta-eixo**, **3 posts-ancora** (URL + frase-chave), **1-2 posts secundarios** (opcional)

Da `clipping-pr.md`, extraia (se houver):
- **1 mencao escolhida** (a mais relevante — entrevista > citacao > premio > ranking)

### Passo 1.5: Calibrar com swipe-file (se disponivel)

Se `conhecimento/copywriting/swipe-file/buzzmonitor-newsletter.md` existir:
- Leia integralmente
- Use como referencia de voz, ritmo, estrutura de blocos, tom de abertura, densidade de links
- Anote 2-3 caracteristicas para imitar nesta edicao (ex: "abertura curta com fato + dado", "linguagem direta sem hype", "links espalhados naturalmente")

Se NAO existir:
- INFORME ao usuario: "Swipe-file da newsletter Buzzmonitor nao encontrado em `conhecimento/copywriting/swipe-file/buzzmonitor-newsletter.md`. Gerando com fallback editorial baseado em estilo-newsletter.md. Para calibrar com a voz oficial, peca 3-5 edicoes recentes ao Victor e adicione via /copy-swipefile add."
- Continue usando apenas `estilo-newsletter.md` como base

### Passo 1.6: Carregar dedupe (se _state.json existir)

Se `newsletter/{brand}/entregas/_state.json` existir, anote:
- **Perguntas-dor das ultimas 6 semanas** (campo `perguntas_dor`)
- **Links usados nas ultimas 4 semanas** (campo `links_usados`)

Use isso para validar que a pergunta-eixo e os links nao estao em janela de cooldown. Se algum link bater, alerte mas NAO bloqueie (a `news-pesquisar` ja deveria ter feito o filtro; aqui e validacao final).

## Passo 2: Selecionar Blocos da Newsletter

Monte o orcamento de links da edicao:

| Bloco | Min | Max | Origem |
|---|---|---|---|
| Resposta em capitulos | 3 | 3 | posts-ancora de `dor-semana.md` |
| Mais pra explorar | 0 | 2 | posts-secundarios de `dor-semana.md` |
| Na imprensa | 0 | 1 | mencao de `clipping-pr.md` |
| Bloco extra | 0 | 1 | gancho real da semana (lancamento, evento — opcional) |
| **TOTAL** | **3** | **6** | |

Decida nesta etapa:
- **Quantos posts secundarios incluir** (0, 1 ou 2) — depende do orcamento de palavras restante apos resposta em capitulos
- **Se inclui clipping** — so se `clipping-pr.md` tiver mencao classificada como relevante
- **Se inclui bloco extra** — so se houver gancho real da semana (NAO inserir bloco extra ficticio)

## Passo 3: Escrever a Newsletter

Siga o `.claude/skills/news-gerar/template-newsletter.md` rigorosamente. Estrutura:

1. **Cabecalho** (Assunto + Pre-header + metadados de geracao)
2. **Saudacao**: `Oi, {{nome}}.`
3. **Abertura jornalistica** (30-50 palavras, lead direto que embute a tese da pergunta-eixo sem formula-la explicitamente)
4. **Resposta em capitulos** (3 mini-blocos curtos, total 110-170 palavras, 3 links blog proprio)
5. **Mais pra explorar** (opcional — 1 bullet, 15-25 palavras)
6. **Na imprensa** (opcional — 1 mencao)
7. **Bloco extra** (opcional — 1 frase + link, P.S.)
8. **Rodape** (assinatura + 3 links sociais fixos)

A pergunta-eixo (15-20 palavras) **NAO** aparece como bloco visivel. Vai como comentario HTML no topo do arquivo local: `<!-- Pergunta-eixo (planejamento interno, NAO publicar): "..." -->`

### Regras de redacao inegociaveis

1. **Idioma**: PT-BR (brasil) | ES-LATAM (latam) | PT-PT (portugal). Texto deve parecer nativo. Para LATAM: zero "vosotros", zero "vale" como concordancia, vocabulario LATAM. Para PT: zero brasileirismos, vocabulario europeu (ex: "telemovel", "aplicacao").
2. **Piramide invertida + Lead jornalistico**: a abertura coloca a informacao mais importante NA PRIMEIRA FRASE (apex da piramide). Template: [O Que: fato/insight central] + [Por Que importa ao leitor]. A abertura deve ser completa em si — se o leitor parar aqui, ja entendeu o ponto. NUNCA comecar com contexto, aquecimento ou gancho narrativo ("imagine que...", "no mundo atual...", "sabe quando..."). Cada mini-bloco da resposta tambem e mini-piramide: tese primeiro, evidencia depois.
3. **Pergunta-eixo NAO visivel**: a pergunta-eixo da semana vive em `dor-semana.md` como planejamento interno. Ela direciona assunto, pre-header e abertura, mas NAO aparece como bloco visivel ao leitor (sem `> ## A pergunta da semana`, sem callout). O leitor recebe os recortes/teses diretamente.
4. **Edutainment por mini-bloco**: cada um dos 3 mini-blocos da resposta deve ter PELO MENOS UM destes — analogia util, dado verificavel, exemplo concreto, definicao clara.
5. **Frases**: medias ≤22 palavras, max 30 numa frase.
6. **Anti-IA aplicado**: zero em-dashes como pontuacao narrativa, zero filler ("realmente", "no mundo atual"), max 2 antiteses-por-negacao, zero "em resumo" como fechamento.
7. **Tom nao-vendedor**: max 1 mencao a {NomeDaMarca} fora dos links de blog proprio (nem mesmo no bloco extra essa regra muda muito). NAO descrever feature do produto como diferencial — esse e papel da landing page.
8. **Cases**: se citar case nominal, USAR APENAS os listados em `### Cases de Sucesso Verificados` do BRANDBOOK. Caso contrario, exemplos genericos.
9. **Conceitos nomeados**: se usar nome de vies/efeito psicologico, verificar definicao real. Em duvida, descrever sem nome tecnico.
10. **Tamanho total do corpo**: ≤300 palavras (sem contar rodape e cabecalho).
11. **Substituir `[MARCA]`** no template pelo `{NomeDaMarca}` real.

## Passo 4: Salvar Localmente

Salve em `newsletter/{brand}/entregas/newsletter-{SEMANA_ISO}.md` (sem subpasta — direto na pasta `entregas/`):

Se a pasta `newsletter/{brand}/entregas/` nao existir, criar com Bash: `mkdir -p newsletter/{brand}/entregas`.

Formato do arquivo:
```markdown
# Newsletter Semanal — {NomeDaMarca}

**Edicao**: {SEMANA_ISO} | **Semana**: DD-MMM a DD-MMM
**Marca**: {NomeDaMarca} | **Regiao**: {region} | **Idioma**: {idioma}
**Assunto**: [60 chars]
**Pre-header**: [80 chars]
**Pergunta-eixo**: [pergunta]
**Posts-ancora**: 3 (titulos resumidos)
**Links totais**: N (3-6)
**Palavras (corpo)**: N (≤300)

---

Oi, {{nome}}.

[Abertura jornalistica — 30-50 palavras. A abertura embute a tese central; a pergunta-eixo NAO aparece como bloco visivel.]

**[Recorte 1 — frase-chave em negrito]**
[1-2 frases curtas com tese + edutainment.]
→ [Ler no blog](URL_post_1)

**[Recorte 2]**
[1-2 frases.]
→ [Ler no blog](URL_post_2)

**[Recorte 3]**
[1-2 frases.]
→ [Ler no blog](URL_post_3)

[BLOCO "Mais pra explorar" — opcional, 1 bullet]
**Mais pra explorar:** [Titulo do post](link) — 1 frase com angulo correlato.

[BLOCO "Na imprensa" — opcional]
**Na imprensa esta semana:** **[Veiculo]** publicou [contexto]. [frase.]
→ [Ler materia](URL)

[BLOCO extra — opcional]
P.S.: [1 frase + link].

Equipe {NomeDaMarca}

[LinkedIn] · [Instagram] · [Site]
```

## Passo 5: Atualizar _state.json

Edite `newsletter/{brand}/entregas/_state.json` (criar se nao existir):

```json
{
  "ultima_atualizacao": "{DATA}",
  "perguntas_dor": [
    ...,
    {
      "semana": "{SEMANA_ISO}",
      "dor": "[nome da dor]",
      "pergunta": "[pergunta-eixo]"
    }
  ],
  "links_usados": [
    ...,
    {"semana": "{SEMANA_ISO}", "url": "URL_post_1", "titulo": "...", "tipo": "post-proprio-ancora"},
    {"semana": "{SEMANA_ISO}", "url": "URL_post_2", "titulo": "...", "tipo": "post-proprio-ancora"},
    {"semana": "{SEMANA_ISO}", "url": "URL_post_3", "titulo": "...", "tipo": "post-proprio-ancora"},
    [se houver mais pra explorar:] {"semana": "{SEMANA_ISO}", "url": "...", "tipo": "post-proprio-secundario"},
    [se houver clipping:] {"semana": "{SEMANA_ISO}", "url": "...", "tipo": "clipping-pr"},
    [se houver extra:] {"semana": "{SEMANA_ISO}", "url": "...", "tipo": "extra"}
  ],
  "pautas_sugeridas_consumidas": [...]
}
```

Mantenha apenas as ultimas 8 semanas em `perguntas_dor` e `links_usados` (poda automatica para evitar arquivo crescer indefinidamente).

## Passo 6: Publicar no Notion

**ID raiz**: leia `conhecimento/config/notion-ids.md`, chave `newsletter`. Use `{NEWSLETTER_ROOT}` como placeholder.

### Estrutura alvo no Notion

```
Newsletter (ID: {NEWSLETTER_ROOT})
└── {NomeDaMarca}                       ← subpasta da marca (icon: 📁)
    └── [{SEMANA_ISO}] {Assunto}        ← pagina da edicao (icon: 📰)
```

A v1 usava pasta mensal com toggles. A **v2 usa 1 pagina por edicao semanal** — sem toggle.

### Passo 6.1: Localizar ou criar subpasta da marca

1. Faca fetch de `notion://docs/enhanced-markdown-spec` para confirmar sintaxe
2. Use `notion-search` com query `{NomeDaMarca}` (filtrando dentro de Newsletter) para localizar a subpasta
3. Se encontrar: anote o ID
4. Se nao encontrar: crie com `notion-create-pages`, parent = `{NEWSLETTER_ROOT}`, title = `{NomeDaMarca}`, icon = `📁`

### Passo 6.2: Criar a pagina da edicao

Crie a pagina com `notion-create-pages`:
- parent = ID da subpasta da marca
- title = `[{SEMANA_ISO}] {Assunto}` (ex: `[2026-W18] Atendimento que nao escala: o que fazer`)
- icon = `📰`
- content = corpo completo da newsletter em markdown enhanced

Adicione no inicio do conteudo um callout com metadados:
```
> **Marca**: {NomeDaMarca}
> **Regiao/Idioma**: {region} / {idioma}
> **Edicao**: {SEMANA_ISO} (DD-MMM a DD-MMM)
> **Assunto**: [assunto]
> **Pre-header**: [pre-header]
> **Pergunta-eixo**: [pergunta]
> **Links contextuais**: N (3-6)
> **Palavras (corpo)**: N (≤600)
```

Em seguida, o corpo completo: saudacao + abertura + pergunta-eixo (em quote) + resposta em capitulos (com links) + blocos opcionais + assinatura + links sociais.

### Passo 6.3: Confirmar publicacao

Apos publicar, informe ao usuario:
- URL da pagina no Notion
- Confirmacao de que a edicao foi salva localmente em `newsletter/{brand}/entregas/newsletter-{SEMANA_ISO}.md`

## Regras Criticas

- NUNCA inventar dados, metricas, cases ou nomes de empresas
- NUNCA usar nome tecnico de vies/efeito sem verificar definicao
- NUNCA gerar mais de 1 newsletter por execucao (a v2 gera 1 por semana)
- NUNCA criar subpasta YYYY-MM ou YYYY-WW dentro de `entregas/` — o arquivo vai direto na pasta
- ESCREVER no idioma da regiao
- Cada newsletter funciona isolada (o leitor pode receber so 1)
- Verificar nomes de features contra `brand/{brand}/BRANDBOOK.md`
- Se um dado da pesquisa nao tiver fonte clara, marcar [VERIFICAR] ou nao usar
