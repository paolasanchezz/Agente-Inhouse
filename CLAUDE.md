# Agente Inhouse — Grupo Elife

Este agente automatiza a criacao de newsletters, traducoes de copy e analise de campanhas Meta Ads para as marcas do Grupo Elife: Buzzmonitor, Buzzcreators, Cxpress e Elife.

---

## Como Usar Este Agente

### Newsletters

Cada comando aceita `[brand]` e `[region]` como argumentos. Default: `buzzmonitor brasil`.

| Comando | O que faz |
|---|---|
| `/news-pipeline [brand] [region]` | Faz tudo: pesquisa, gera 5 newsletters e revisa |
| `/news-pesquisar [brand] [region]` | So a pesquisa (blog da marca, noticias, concorrentes) |
| `/news-gerar [brand] [region]` | So gera os rascunhos (requer pesquisa feita antes) |
| `/news-revisar [brand] [region]` | So revisa os rascunhos gerados |

**Valores validos:**
- `[brand]`: `buzzmonitor` | `buzzcreators` | `cxpress` | `elife`
- `[region]`: `brasil` (PT-BR) | `latam` (ES-LATAM) | `portugal` (PT-PT)

**Exemplos:**
```
/news-pipeline buzzmonitor brasil
/news-pipeline buzzcreators latam
/news-pipeline cxpress portugal
/news-gerar elife brasil
```

### Traducao de Copy

| Comando | O que faz |
|---|---|
| `/trad-pipeline [arquivo] pt-pt` | Traduz e revisa para Portugues Europeu |
| `/trad-pipeline [arquivo] es-latam` | Traduz e revisa para Espanhol Latino-Americano |
| `/trad-traduzir [arquivo] [pt-pt\|es-latam]` | So traduz (sem revisar) |
| `/trad-revisar [arquivo] [pt-pt\|es-latam]` | So revisa uma traducao ja feita |
| `/trad-calibrar pt-pt` | Atualiza o padrao linguistico PT-PT com novos exemplos nativos |
| `/trad-calibrar es-latam` | Atualiza o padrao linguistico ES-LATAM com novos exemplos nativos |

**Exemplo de traducao**: `/trad-pipeline meu-texto.md pt-pt`

---

### Meta Ads (SOMENTE LEITURA)

Requer Python 3.10+ e token Meta Ads configurado no `.env` (veja `meta-ads/.env.example`).

| Comando | O que faz |
|---|---|
| `/meta-ads [conta] [periodo]` | Pipeline completo: coleta estrutura + insights + gera relatorio |
| `/meta-ads-fetch [conta] [periodo]` | So atualiza dados locais (sem gerar relatorio) |
| `/meta-ads-report [conta] [periodo]` | So gera relatorio (dados ja no banco, sem nova coleta) |
| `/meta-ads-trends [conta]` | Foco em tendencias temporais (3d/7d/15d/30d) |

**Contas validas:**
- `buzzmonitor_brl` | `buzzmonitor_usd` | `buzzmonitor_eur`
- `cxpress_brl` | `cxpress_usd` | `cxpress_eur`

**Periodos validos:** `mes_atual` | `mes_anterior` | `ultimos_30`

**Exemplos:**
```
/meta-ads buzzmonitor_brl mes_atual
/meta-ads cxpress_usd ultimos_30
/meta-ads-fetch buzzmonitor_eur mes_anterior
/meta-ads-report cxpress_brl mes_atual
```

**Primeira execucao:** instalar dependencias antes:
```bash
cd meta-ads && pip install -r requirements.txt
```

---

## Onde Encontrar os Resultados

| O que procura | Onde esta |
|---|---|
| Newsletters da Buzzmonitor | `newsletter/buzzmonitor/entregas/YYYY-MM/` |
| Newsletters da Buzzcreators | `newsletter/buzzcreators/entregas/YYYY-MM/` |
| Newsletters da Cxpress | `newsletter/cxpress/entregas/YYYY-MM/` |
| Newsletters da Elife | `newsletter/elife/entregas/YYYY-MM/` |
| Pesquisa que originou as newsletters | `conhecimento/produto/{brand}/pesquisa/` |
| Traducoes do mes atual | `traducao/entregas/YYYY-MM/` |
| Conhecimento de produto por marca | `conhecimento/produto/{brand}/` |
| Guia de estilo de escrita | `conhecimento/editorial/` |
| Padroes linguisticos (PT-PT / ES-LATAM) | `conhecimento/linguistico/` |
| Relatorios Meta Ads gerados | `meta-ads/data/reports/` |
| Benchmarks Meta Ads (editavel) | `meta-ads/data/benchmarks.json` |

---

## Estrutura do Projeto

```
CLAUDE.md                             <- voce esta aqui
conhecimento/
  produto/
    buzzmonitor/                      <- buzzmonitor.md, concorrentes.md, pt-pt/, es/
      pesquisa/                       <- material do ciclo atual (blog, noticias, concorrentes)
      pesquisa/arquivo/YYYY-MM/       <- pesquisas anteriores arquivadas
    buzzcreators/                     <- idem
    cxpress/                          <- idem
    elife/                            <- idem
  editorial/                          <- estilo-newsletter.md
  linguistico/                        <- pt-portugal/, es-latam/
newsletter/
  buzzmonitor/
    entregas/YYYY-MM/                 <- newsletters finais por mes
  buzzcreators/ ...
  cxpress/ ...
  elife/ ...
traducao/
  entregas/YYYY-MM/                   <- traducoes finais por mes
meta-ads/
  scripts/                            <- Python: fetch, analise, relatorio
    cache_manager.py                  <- banco SQLite, ACCOUNTS, inferencia de campanha
    fetch_campaigns.py                <- coleta hierarquica (campanhas->adsets->ads)
    fetch_insights.py                 <- coleta incremental de metricas
    trend_analyzer.py                 <- tendencias por janelas 3/7/15/30 dias
    benchmark_checker.py              <- classificacao vs valores de referencia
    report_generator.py               <- geracao de relatorio Markdown
    full_analysis.py                  <- orquestrador end-to-end
  data/
    benchmarks.json                   <- valores de referencia por moeda/tipo (versionado)
    meta_ads.db                       <- banco SQLite local (gitignored)
    reports/                          <- relatorios gerados (gitignored)
    cache/                            <- jsons brutos da API (gitignored)
  requirements.txt
  .env.example                        <- template de configuracao (nao commitar .env real)
.claude/                              <- configuracao do agente (nao editar)
```

---

## Regras de Qualidade (OBRIGATORIAS)

### Construcoes Proibidas
1. **Nunca** usar "Nao e X, e Y" ou variacoes ("Nao se trata de X, mas sim de Y")
2. **Nunca** usar aberturas genericas de IA: "No cenario atual...", "Em um mundo cada vez mais...", "Nos ultimos anos...", "E inegavel que..."
3. **Nunca** usar filler words: "realmente", "verdadeiramente", "simplesmente", "basicamente", "literalmente", "definitivamente"
4. **Nunca** iniciar mais de 1 paragrafo por newsletter com "Imagine que..."
5. **Nunca** usar listas de exatamente 3 itens como padrao (variar entre 2, 4, 5)
6. **Nunca** usar "Alem disso" como abertura de paragrafo mais de 1 vez por newsletter
7. **Nunca** usar CTAs agressivos ("Nao perca!", "Corra!", "Ultima chance!")

### Obrigacoes
- Cada newsletter deve abrir com gancho baseado em dado real, vies cognitivo ou cenario surpreendente
- A marca deve ser posicionada como facilitadora, nunca como protagonista
- Preferir dados concretos e exemplos reais a afirmacoes genericas
- **Maximo 600 palavras por newsletter**
- Verificar nomes de features contra `conhecimento/produto/{brand}/{brand}.md` antes de publicar
- **Idioma definido pela regiao**: brasil → PT-BR | latam → ES-LATAM | portugal → PT-PT
- **Todo texto deve ter acentuacao e pontuacao corretas no idioma da regiao** (nao omitir acentos)
- **Se usar nome de vies cognitivo ou efeito psicologico, a descricao deve corresponder a definicao real do conceito**

---

## Arquivos de Referencia

### Newsletter
- `conhecimento/produto/{brand}/{brand}.md` — Features, cases, nomes corretos do produto e configuracao (blog URL, assinatura)
- `conhecimento/produto/{brand}/concorrentes.md` — Mapa competitivo com diferenciais por marca
- `conhecimento/produto/{brand}/pesquisa/` — Pesquisa do ciclo atual: blog, noticias de mercado, analise de concorrentes, RESUMO
- `conhecimento/produto/{brand}/pesquisa/arquivo/YYYY-MM/` — Pesquisas de ciclos anteriores
- `conhecimento/produto/{brand}/pt-pt/{brand}.md` — Terminologia PT-PT adaptada para a marca
- `conhecimento/produto/{brand}/es/{brand}.md` — Terminologia ES-LATAM adaptada para a marca
- `conhecimento/editorial/estilo-newsletter.md` — Guia de estilo detalhado e anti-patterns

### Traducao
- `conhecimento/linguistico/pt-portugal/padrao-linguistico.md` — Vocabulario, tom e anti-patterns PT-PT
- `conhecimento/linguistico/es-latam/padrao-linguistico.md` — Vocabulario, tom e anti-patterns ES-LATAM
