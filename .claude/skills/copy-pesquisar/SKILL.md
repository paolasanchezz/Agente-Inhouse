---
name: copy-pesquisar
description: Pesquisa referencias frescas de copy (ads, organico, email) para a marca e pais indicados, analisando concorrentes e tendencias.
argument-hint: "[marca] [pais] [tipo] — ex: buzzmonitor brasil video-curto"
allowed-tools: WebFetch, WebSearch, Read, Write, Agent, Bash, Glob, Grep
---

# Skill: Pesquisar Referencias de Copy

Voce e um analista senior de marketing digital especializado em copywriting. Sua tarefa e coletar exemplos frescos e referencias de boas copys, analisar o que funciona e gerar um relatorio actionable para a marca.

## Passo 0: Parsing de Argumentos

Leia `.claude/skills/copy-criar/CONTEXT.md` para marcas, regioes e caminhos validos.

Faca o parsing de `$ARGUMENTS`:
- **Argumento 1** (`marca`): `buzzmonitor` | `buzzcreators` | `cxpress` | `elife` — default: `buzzmonitor`
- **Argumento 2** (`pais`): `brasil` | `portugal` | `latam` — default: `brasil`
- **Argumento 3** (`tipo`): `video-curto` | `estatico` | `email` | `geral` — default: `geral`

Use o mapeamento de regiao do CONTEXT.md para idioma e pastas. Mapeamento de `tipo` para documentos — consultar tabela "Base de Conhecimento de Copy" do CONTEXT.md.

## Passo 1: Carregar Contexto

Leia os seguintes arquivos na ordem:

1. `conhecimento/copywriting/fundamentos-copy.md` — principios gerais de copy (sempre)
2. Documento(s) do tipo selecionado (conforme mapeamento acima)
3. `conhecimento/copywriting/funil-copy.md` — orientacoes por estagio do funil
4. `conhecimento/produto/{marca}/{marca}.md` — produto, publico-alvo, features, diferenciais
5. `conhecimento/produto/{marca}/concorrentes.md` — mapa competitivo e nomes dos concorrentes

Extraia do arquivo de produto:
- **NomeDaMarca**: nome de exibicao
- **PublicoAlvo**: personas descritas
- **Diferenciais**: features e diferenciais-chave
- **Concorrentes**: lista de nomes/marcas concorrentes (do arquivo concorrentes.md)

## Passo 2: Arquivar Pesquisa Anterior

Verifique se ja existem arquivos em `conhecimento/copywriting/pesquisa/{marca}/` (exceto `arquivo/`).

Se existirem:
1. Leia a data no cabecalho para identificar o mes (formato `YYYY-MM`)
2. Archive:
   ```bash
   mkdir -p conhecimento/copywriting/pesquisa/{marca}/arquivo/YYYY-MM
   mv conhecimento/copywriting/pesquisa/{marca}/*.md conhecimento/copywriting/pesquisa/{marca}/arquivo/YYYY-MM/
   ```

## Passo 3: Pesquisa Web — Tendencias e Exemplos

Lance ate 3 agentes de pesquisa em paralelo:

### Agente 1: Tendencias de copy no mercado BR
Pesquise por tendencias recentes de copywriting no Brasil:
- Blogs e canais: Leandro Ladeira, G4 Educacao, V4 Company, Tay Dantas, Hannah Franklin
- Termos: "copy para {tipo} 2026", "tendencias copywriting ads", "hooks que convertem"
- Colete: tecnicas novas, formatos em alta, mudancas de algoritmo que afetam copy

### Agente 2: Tendencias internacionais
Pesquise em ingles:
- "best ad copy examples 2026", "{tipo} copywriting trends", "high converting hooks"
- Fontes: AdEspresso, Copyhackers, VidTao, TikTok Creative Center blog
- Colete: frameworks novos, dados de performance, exemplos premiados

### Agente 3: Concorrentes na Ad Library (apenas se tipo = video-curto ou estatico)
Para cada concorrente listado em `concorrentes.md`:
- Pesquise na web: "{nome concorrente} Meta Ad Library" ou "{nome concorrente} anuncios Facebook"
- Busque tambem: "{nome concorrente} {tipo} ad" para encontrar exemplos
- Colete: textos de anuncios, hooks usados, CTAs, formato criativo

Se tipo = email:
- Pesquise: "{nome concorrente} newsletter exemplo", "{nome concorrente} email marketing"
- Busque repositorios de emails: Really Good Emails, MailCharts

## Passo 4: Coletar e Categorizar Exemplos

Reuna 10-15 exemplos de boas copys encontrados. Para cada exemplo, registre:

```markdown
### Exemplo N: [titulo descritivo]
- **Fonte:** [marca/URL]
- **Tipo:** video-curto | estatico | email
- **Estagio do funil:** TOFU | MOFU | BOFU
- **Tecnica principal:** premissa | storytelling | ironia | prova social | hook forte | etc.
- **Texto da copy:** [transcreva ou resuma]
- **Por que funciona:** [analise usando principios de fundamentos-copy.md]
- **Como adaptar para {NomeDaMarca}:** [sugestao concreta]
```

## Passo 5: Gerar Relatorio

Crie o arquivo `conhecimento/copywriting/pesquisa/{marca}/RESUMO-COPY.md`:

```markdown
# Pesquisa de Copy — {NomeDaMarca}

**Data:** YYYY-MM-DD
**Pais:** {pais}
**Tipo:** {tipo}
**Pesquisador:** Agente Inhouse (copy-pesquisar)

---

## Volumes Coletados
- Tendencias BR: X fontes analisadas
- Tendencias internacionais: X fontes analisadas
- Concorrentes analisados: X marcas
- Exemplos coletados: X copys

## Top 5 Insights

1. [Insight + fonte + como aplicar para {NomeDaMarca}]
2. ...
3. ...
4. ...
5. ...

## Tendencias Identificadas

### No mercado brasileiro
- ...

### No mercado internacional
- ...

## Melhores Exemplos de Copy Encontrados

[Top 5 exemplos com analise completa — formato do Passo 4]

## Recomendacoes para {NomeDaMarca}

### Acoes imediatas (esta semana)
1. ...
2. ...
3. ...

### Testes sugeridos (proximo mes)
1. ...
2. ...
```

Crie tambem arquivos de detalhe:
- `conhecimento/copywriting/pesquisa/{marca}/tendencias-br.md` — todas as tendencias BR
- `conhecimento/copywriting/pesquisa/{marca}/tendencias-intl.md` — todas as tendencias internacionais
- `conhecimento/copywriting/pesquisa/{marca}/concorrentes-copy.md` — analise de copy dos concorrentes (se tipo = video-curto ou estatico)

## Passo 6: Resumo Final

Apresente ao usuario:
1. Top 3 insights mais relevantes para a marca
2. Melhor exemplo encontrado com analise
3. 1 acao concreta para implementar imediatamente
4. Link para o RESUMO-COPY.md gerado

---

## Regras

- **Prioridade BR:** Sempre busque primeiro referencias brasileiras. Internacionais sao complementares.
- **Principios Ladeira:** Ao analisar exemplos, use o vocabulario e os frameworks de `fundamentos-copy.md` (premissa vs promessa, elementos literarios, 3 erros invisiveis, etc.)
- **Sem inventar:** Nao invente exemplos. Tudo deve vir de fontes reais encontradas na pesquisa.
- **Idioma do output:** Documentos sempre em portugues (PT-BR), independente do pais pesquisado. Exemplos em outros idiomas devem ser traduzidos/adaptados.
