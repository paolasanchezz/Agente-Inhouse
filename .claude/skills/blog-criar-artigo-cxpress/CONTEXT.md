# Contexto Compartilhado — blog-criar-artigo-cxpress

> Skill standalone. Cxpress (BR + PT-PT + ES-LATAM). Nao faz parte da familia `news-*` nem das skills de blog da Buzzmonitor.

---

## Origem e escopo

Criada em 2026-08-20 pela Barbara a partir de pesquisa propria sobre o publico da Cxpress: as 3 regioes (Brasil, Portugal, LATAM) tem maturidade de audiencia equivalente — todas buscam solucao para atendimento fragmentado, com intencao comercial/de avaliacao de ferramenta. Por isso o conteudo e **sempre MoFu/BoFu nas 3 regioes** — comparativos, guias de implementacao, casos de uso — diferente da `blog-criar-artigo-intl` (Buzzmonitor PT/LATAM), que era topo de funil por maturidade de publico inferior.

O run gera **3 versoes simultaneas por execucao**: o artigo base e escrito em PT-BR e depois traduzido/adaptado para PT-PT e ES-LATAM no mesmo run, mantendo a estrutura intacta e aplicando o pilar linguistico de cada regiao.

Lote inicial: 20+ artigos pre-existentes por regiao (listados nos blog-caches abaixo) — esses artigos sao o inventario de partida para dedupe e linkagem interna.

## Em que isso difere das skills irmas

| Aspecto | `blog-criar-artigo` (Buzz BR) | `blog-criar-artigo-intl` (Buzz PT/LATAM) | `blog-criar-artigo-cxpress` |
|---|---|---|---|
| Marca | Buzzmonitor | Buzzmonitor | **Cxpress** |
| Produto | Social listening | Social listening | **Atendimento via WhatsApp/omnichannel** |
| Regioes | So BR | PT ou LATAM (1 por run) | **BR + PT + LATAM (3 por run)** |
| Funil | MoFu/BoFu | Topo (puro) | **MoFu/BoFu para todas as regioes** |
| CTA | Trial / consultor | Leia mais / ebook | **Demo / fale com especialista (todas as regioes)** |
| Pilar linguistico | Nao precisa | Obrigatorio (1 regiao) | **Obrigatorio para PT-PT e ES-LATAM** |
| Clusters | 5 (Buzz) | 5 por regiao (Buzz) | **4 (WhatsApp, Atendimento, IA/Chatbot, CRM)** |
| Cases verificados | Sim (Youse, Hering) | Sim (Youse, Hering) | **Nenhum ainda — nao inventar** |
| Sitemap ao vivo | 1 (buzzmonitor.com/blog, so URLs BR) | 1 (mesmo sitemap, filtrado por `/blog/pt-pt/` ou `/blog/es/`) | **3 sitemaps (io / pt / ai)** |

## Clusters de conteudo

Fonte: `conhecimento/produto/cxpress/seo/clusters-cxpress.md` — os 4 clusters sao os mesmos para BR, PT e LATAM.

**Todos em rotacao** (nenhum restrito):
1. WhatsApp para Empresas
2. Atendimento via WhatsApp
3. Automacao e IA
4. CRM e Gestao da Experiencia do Cliente

Ao escolher sozinha, a skill cruza: cluster nao repetido em relacao ao ultimo run (`_state-{regiao}.json`) + lacuna real (blog-caches + sitemaps ao vivo, Passo 2.5).

## Caminhos

| O que | Caminho |
|---|---|
| Artigos BR (local) | `conteudo-blog/cxpress/artigos-br/{NUMERO}-{SLUG-BR}.md` |
| Artigos PT (local) | `conteudo-blog/cxpress/artigos-pt/{NUMERO}-{SLUG-PT}.md` |
| Artigos LATAM (local) | `conteudo-blog/cxpress/artigos-latam/{NUMERO}-{SLUG-LATAM}.md` |
| Log BR | `conteudo-blog/cxpress/_state-br.json` |
| Log PT | `conteudo-blog/cxpress/_state-pt.json` |
| Log LATAM | `conteudo-blog/cxpress/_state-latam.json` |
| Clusters | `conhecimento/produto/cxpress/seo/clusters-cxpress.md` |
| Blog-cache BR | `conhecimento/produto/cxpress/blog-cache-br.md` |
| Blog-cache PT | `conhecimento/produto/cxpress/blog-cache-pt.md` |
| Blog-cache LATAM | `conhecimento/produto/cxpress/blog-cache-latam.md` |

## Notion — IDs das subpastas por cluster e regiao

Cada artigo vai para a subpasta do cluster correto. Use o ID correspondente ao cluster identificado no Passo 2.

| Cluster | ID subpasta BR | ID subpasta PT | ID subpasta LATAM |
|---|---|---|---|
| 1 — WhatsApp para Empresas | `3893934026fd8091af79c4efe3a292a5` | `39e3934026fd805c98afe191b048db54` | `39e3934026fd80e08ea8ff340e1e473e` |
| 2 — Atendimento via WhatsApp | `3893934026fd806c836ed3feccd130ff` | `39e3934026fd801ab57cd08624df34d5` | `39e3934026fd8063a101f3e8596cc194` |
| 3 — Automacao e IA | `3893934026fd80139293d842dfbc7295` | `39e3934026fd80a5ab2aca2a05ba2578` | `39e3934026fd80759954fa019a205cc8` |
| 4 — CRM e Gestao | `3893934026fd80cb9c17f63b4f1df2d4` | `39e3934026fd80c8831ee9473983a132` | `39e3934026fd800f8618f98e2a59f75f` |

Pastas pai (para referencia):
- BR: `3893934026fd80e68fa0e780bb11a36d` (📚 Subtopicos artigos)
- PT: `39e3934026fd809da4b1f5ead2264e61` (📁 Cxpress PT-PT)
- LATAM: `39e3934026fd808aad7bd299ef576b64` (📁 Cxpress Latam)

## Sitemaps ao vivo (Passo 2.5)

| Regiao | URL do sitemap-index |
|---|---|
| BR | `https://blog.cxpress.io/sitemap_index.xml` |
| PT | `https://blog.cxpress.pt/sitemap_index.xml` |
| LATAM | `https://blog.cxpress.ai/sitemap_index.xml` |

Se o sitemap-index retornar sitemaps filhos, siga cada um e agregue todas as URLs encontradas.

## Pesquisa de palavra-chave (Semrush) — bancos por regiao

| Regiao | Banco Semrush | Observacao |
|---|---|---|
| BR | `br` | Banco Brasil |
| PT | `pt` | Banco Portugal |
| LATAM | `mx` | Mexico como mercado de referencia (sem banco unico LATAM no Semrush) |

## Links externos por regiao

### CTAs de LP (obrigatorio em todo artigo, 1 por versao)

| Regiao | URL da LP | utm_content |
|---|---|---|
| BR | `https://home.cxpress.io/atendimento-omnicanal-whatsapp` | `lp-atendimento-omnicanal-whatsapp` |
| PT | `https://www.cxpress.pt/whatsapp` | `lp-whatsapp-pt` |
| LATAM | `https://www.cxpress.ai/chatbot-para-whatsapp` | `lp-chatbot-whatsapp-latam` |

### Homes (usar 1 vez por artigo, para mencao geral da marca)

| Regiao | URL | utm_content |
|---|---|---|
| BR | `https://home.cxpress.io/` | `home-br` |
| PT | `https://www.cxpress.pt/` | `home-pt` |
| LATAM | `https://www.cxpress.ai/` | `home-latam` |

### Formula de UTM (aplicar em toda URL externa, sem excecao)

```
?utm_source=blog-cxpress&utm_medium=organic&utm_campaign={slug-do-artigo-atual}&utm_content={utm_content-da-tabela}
```

`{slug-do-artigo-atual}` = o `{SLUG}` gerado no Passo 3.5 pro artigo **da regiao correspondente** (slug BR vai em artigo BR, slug PT vai em artigo PT). `{utm_content}` vem das tabelas acima.

**Links internos (mesmo blog da regiao) NUNCA levam UTM.**

## Links internos — URLs de producao por regiao

```
BR:    https://blog.cxpress.io/{slug}/
PT:    https://blog.cxpress.pt/blog/{slug}/
LATAM: https://blog.cxpress.ai/blog/{slug}/
```

`{slug}` = o slug exato do artigo existente, conforme registrado nos blog-caches ou nos `_state-{regiao}.json`.

Nunca misturar regioes nos links internos: artigo PT-PT so linka artigos do blog.cxpress.pt; artigo ES-LATAM so linka blog.cxpress.ai.

## Idioma e pilar linguistico

| Versao | Banco Semrush | Pilar linguistico |
|---|---|---|
| PT-BR | `br` | Nao precisa (e a base) |
| PT-PT | `pt` | `conhecimento/linguistico/pt-portugal/padrao-linguistico.md` — **obrigatorio** |
| ES-LATAM | `mx` | `conhecimento/linguistico/es-latam/padrao-linguistico.md` — **obrigatorio** |

Nunca escrever PT-PT ou ES de cabeca. Carregar o arquivo antes de adaptar.

## Anti-IA por regiao

- PT-BR: `conhecimento/editorial/regras-anti-ia.md`
- PT-PT: `conhecimento/editorial/regras-anti-ia.md` + anexo PT-PT (se existir)
- ES-LATAM: `conhecimento/editorial/regras-anti-ia.md` + anexo ES-LATAM (se existir)

## Regras de produto e cases

- **Produto pode aparecer cedo** (MoFu/BoFu em todas as regioes). Nao ha restricao de "so na antepenultima H2".
- **Cases verificados**: BRANDBOOK seccao "Cases de Sucesso Verificados" diz "A preencher pelo time com casos reais e metricas verificadas." — nao citar case com numero especifico. Usar dados de mercado (Zendesk CX Trends 2026, fontes abertas) como suporte quantitativo.
- **Concorrentes**: tom factual e tecnico. Nao citar por nome de forma depreciativa. Diferenciais da Cxpress devem vir do BRANDBOOK.
- **Grafia "Cxpress"**: ver tabela de grafias incorretas no BRANDBOOK. Sempre feminino em PT ("a Cxpress"); sem artigo em ES ("Cxpress unifica...").

## Em que isso difere de `blog-copy.md`

Algumas regras do `blog-copy.md` sao invertidas de proposito nesta skill (como em `blog-criar-artigo`):

| Regra de blog-copy.md | Como se aplica aqui |
|---|---|
| Produto so na antepenultima H2 | **Nao se aplica** — produto pode aparecer mais cedo se o argumento pedir |
| Tom editorial neutro, sem tom de vendas | **Nao se aplica** — tom comercial e esperado; CTA de demo/especialista e o padrao |
| Nao comparar com concorrentes por nome | Mantido — comparacoes factuais ok, mas nunca depreciativo |

## Schema de `_state-{regiao}.json`

```json
{
  "ultima_atualizacao": "YYYY-MM-DD",
  "regiao": "br",
  "total_artigos": 1,
  "itens": [
    {
      "numero": "01",
      "titulo": "...",
      "cluster": "WhatsApp para Empresas",
      "slug": "...",
      "title_seo": "...",
      "meta_descricao": "...",
      "palavra_chave": "...",
      "keyword_candidatas": [
        {"termo": "...", "volume": 0, "dificuldade": 0, "database": "br"}
      ],
      "url_notion": "https://...",
      "caminho_local": "conteudo-blog/cxpress/artigos-br/01-{slug}.md",
      "pendencias": "",
      "data": "YYYY-MM-DD"
    }
  ]
}
```

O mesmo numero sequencial e usado nas 3 regioes dentro do mesmo run. `numero` nunca e reaproveitado mesmo que um run anterior tenha sido abortado no meio.

## Quando NAO usar esta skill

- Artigo para Buzzmonitor → `blog-criar-artigo` (BR) ou `blog-criar-artigo-intl` (PT/LATAM)
- Newsletter semanal Cxpress → familia `news-*`
- Artigo editorial ancorado em noticia recente → `pauta-quente`
- Criativo ou social media → familias proprias
