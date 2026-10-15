# Contexto Compartilhado — blog-criar-artigo-intl

> Skill standalone (nao faz parte da familia `news-*`). Buzzmonitor Portugal (PT-PT) e Buzzmonitor LATAM (ES-LATAM). Irma de `blog-criar-artigo` (Buzzmonitor Brasil) — mesmo craft de metadados/GEO/anti-IA, mas editorialmente invertida em varios pontos porque o publico e o objetivo de funil sao outros.

---

## Origem e escopo

Nasceu de uma analise de publico feita pela usuaria fora deste repo (2026-07-22): o publico de PT e LATAM ainda esta em desenvolvimento no tema, com CTR organico muito baixo (PT ~0,8%, LATAM ~0,4%), busca majoritariamente informacional/basica ("o que e", "como") e vocabulario desalinhado com o produto. So 2,2% das keywords do `/es/` tem intencao comercial. A estrategia aqui e **educar e gerar awareness**, nunca converter — o oposto do racional de `blog-criar-artigo` (BR).

**Mudanca de modelo (2026-07-24, decisao da Barbara, mesma data e mesma logica aplicada em `blog-criar-artigo`):** ate a v1.2.3 a skill consumia uma fila fixa de 20 pautas compartilhadas entre PT e LATAM (`conteudo-blog/buzzmonitor/briefings-intl/2026-07-topo-funil-pt-latam.md`). As duas filas foram encerradas (20/20 em cada regiao) e nao serao mais usadas. A partir de agora a skill gera artigos **sob demanda**, escolhendo tema entre os clusters de `conhecimento/produto/buzzmonitor/seo/clusters-{portugal|latam}.md` (arquivos novos, trazidos pela Barbara nesta mesma data) ou recebendo o tema direto dela.

## Em que isso difere de `blog-criar-artigo` (Buzzmonitor Brasil)

| Aspecto | `blog-criar-artigo` (BR) | `blog-criar-artigo-intl` (PT/LATAM) |
|---|---|---|
| Maturidade de publico | Alta — busca com intencao comercial | Baixa — busca informacional basica ("o que e X") |
| Pilar linguistico | Nao precisa (PT-BR e a base) | **Obrigatorio** — carregar `conhecimento/linguistico/{pt-portugal\|es-latam}/padrao-linguistico.md` antes de escrever qualquer palavra |
| Onde o produto aparece | Cedo, comparativo direto ok | Tarde e leve — 1 mencao breve perto do fim |
| CTA | Comercial forte: "teste gratis" / "fale com consultor" | **Proibido** CTA de trial/consultor — sempre "leia mais", ebook ou webinar/estudo |
| Tamanho alvo | 1200-2000 palavras | 900-1500 palavras |
| Origem do tema | Tema trazido ou escolhido entre clusters de `clusters-brasil.md` | Tema trazido ou escolhido entre clusters de `clusters-{portugal\|latam}.md` (por regiao) |
| Banco de dados Semrush | `br` | `pt` (Portugal) ou `mx` (LATAM — Mexico como mercado de referencia) |
| Dedupe contra o blog real | Sim — `blog-cache.md` + crawl ao vivo do sitemap (so URLs BR, sem `/blog/es/` e `/blog/pt-pt/`) | Sim, desde a migracao de set/2026 — crawl ao vivo do mesmo sitemap, filtrado pelo prefixo da regiao (`/blog/pt-pt/` ou `/blog/es/`) + historico da propria skill (`_state-{regiao}.json`). Sem `blog-cache` local |
| Regiao | So brasil, hardcoded | Argumento `[regiao]` = `pt` ou `latam` — obrigatorio |
| Log de artigos | `_state.json` unico | `_state-pt.json` e `_state-latam.json` separados, cada um com seu proprio contador sequencial |

**Nao misturar as duas.** Se o pedido for de artigo comercial de meio/fundo de funil pra Buzzmonitor Brasil, isso e `blog-criar-artigo`, nao esta skill.

## Clusters de conteudo

Fonte: `conhecimento/produto/buzzmonitor/seo/clusters-portugal.md` (regiao `pt`) e `conhecimento/produto/buzzmonitor/seo/clusters-latam.md` (regiao `latam`) — arquivos trazidos pela Barbara em 2026-07-24.

- **PT** (5 clusters, todos em rotacao): O Que É Social Listening · Inteligência Artificial · Relacionamento com o Cliente · Métricas & Desenvolvimento · Estratégia de Social Media.
- **LATAM** (5 clusters, todos em rotacao): Qué Es Social Listening · Inteligencia Artificial · Atención al Cliente · Métricas y Performance · Estrategia en Social Media.
- Diferente do mapa BR (`clusters-brasil.md`), **nenhum cluster de PT/LATAM esta marcado como "fora de rotacao" ainda** — todos sao topo de funil e fazem parte da escolha automatica normal. Se surgir um cluster de case nominal ou tutorial de plataforma pra essas regioes no futuro, aplicar a mesma logica do BR (fora de rotacao, so como peca avulsa trazida pela Barbara).
- Ao escolher sozinha, a skill cruza: cluster nao repetido em relacao ao ultimo artigo gerado NESSA regiao (`_state-{regiao}.json`).

## Caminhos

- **Artigos gerados (local)**: `conteudo-blog/buzzmonitor/artigos-pt/{NUMERO}-{SLUG}.md` (PT-PT) e `conteudo-blog/buzzmonitor/artigos-latam/{NUMERO}-{SLUG}.md` (ES-LATAM).
- **Log de artigos**: `conteudo-blog/buzzmonitor/_state-pt.json` e `conteudo-blog/buzzmonitor/_state-latam.json` — independentes, cada regiao com seu proprio contador sequencial.
- **Clusters por regiao**: `conhecimento/produto/buzzmonitor/seo/clusters-portugal.md` e `conhecimento/produto/buzzmonitor/seo/clusters-latam.md`.
- **Fila antiga (historico, nao usada mais)**: `conteudo-blog/buzzmonitor/briefings-intl/2026-07-topo-funil-pt-latam.md` — mantida so como referencia de como os 40 primeiros artigos (20 PT + 20 LATAM) foram decididos.

## Notion

| Regiao | Chave em `conhecimento/config/notion-ids.md` | ID |
|---|---|---|
| PT | `artigos-blog-pt-buzzmonitor` | `3a53934026fd80b3a6b0c917e3fb2db8` |
| LATAM | `artigos-blog-latam-buzzmonitor` | `3a53934026fd805a8810cca32f521275` |

Cada artigo = 1 pagina filha direta da pasta da regiao correspondente. Title = H1 do artigo (no idioma nativo), icon `📝`.

## Idioma e pilar linguistico (obrigatorio, sem excecao)

Antes de escrever qualquer linha — inclusive os metadados (Title SEO, Meta descricao) — carregar:
- **PT**: `conhecimento/linguistico/pt-portugal/padrao-linguistico.md`
- **LATAM**: `conhecimento/linguistico/es-latam/padrao-linguistico.md`

Nunca escrever PT-PT ou ES "de cabeca". Ver tambem `conhecimento/editorial/regras-anti-ia.md` **+ o anexo do idioma correspondente**.

## Pesquisa de palavra-chave (Semrush Keyword Magic Tool) — Passo 3

Adicionado em 2026-07-24, mesma logica de `blog-criar-artigo` (BR), com uma diferenca importante: **o banco de dados regional e fixo por regiao**, decisao da Barbara:

| Regiao | Banco de dados Semrush | Motivo |
|---|---|---|
| PT | `pt` | Banco de dados de Portugal, sem ambiguidade |
| LATAM | `mx` | Semrush nao tem banco unico "LATAM" (e por pais) — Mexico escolhido como mercado de referencia (maior mercado de espanhol da regiao, dado mais robusto). Decisao explicita da Barbara em 2026-07-24: **so Mexico**, sem combinar com outros paises nem variar por tema |

Fluxo: `keyword_research` → `get_report_schema` → `execute_report`, comparando 2-4 candidatas **no idioma nativo da regiao** (nunca traduzir do briefing em portugues do Brasil) antes de fechar a keyword principal. Criterio de escolha: volume real + intencao **informacional** (nao comercial — diferente do BR) + ausencia de sobreposicao (Passo 2.5). Documentar as candidatas comparadas no relatorio final.

## Links internos e externos por regiao

> **Migracao de dominio (concluida por volta de 2026-09-20):** `getbuzzmonitor.com` deixou de existir como site. Tudo de LATAM e PT foi pra `buzzmonitor.com`, mesmo dominio do BR:
>
> | Regiao | Site | Blog (posts e cases) |
> |---|---|---|
> | LATAM | `https://buzzmonitor.com/es/` | `https://buzzmonitor.com/blog/es/{slug}/` |
> | PT | `https://buzzmonitor.com/pt-pt/` | `https://buzzmonitor.com/blog/pt-pt/{slug}/` |
>
> O prefixo do blog e `/blog/{idioma}/`, nunca `/{idioma}/blog/`. O de Portugal e `pt-pt`, nunca `pt`. URLs antigas de LATAM (`getbuzzmonitor.com/es/...`) redirecionam pro blog novo, mas as de PT (`getbuzzmonitor.com/pt-pt/...`) caem na home do BR, entao **nunca** escreva URL com `getbuzzmonitor.com` no artigo. Unica excecao: as LPs comerciais abaixo, que ainda vivem nos subdominios `contenido.`/`conteudo.getbuzzmonitor.com`. Todas as URLs desta secao foram revalidadas (HTTP 200, sem redirect) em 2026-10-15.

### Home

| Regiao | URL |
|---|---|
| PT | `https://buzzmonitor.com/pt-pt/` |
| LATAM | `https://buzzmonitor.com/es/` |

### CTA de conteudo (ebook / estudos / webinars) — usar quando o tema pedir "download de ebook" ou nao houver angulo de "leia mais" disponivel

| Regiao | Ebooks | Estudos/cases | Webinars |
|---|---|---|---|
| PT | `https://buzzmonitor.com/pt-pt/ebooks/` | `https://buzzmonitor.com/pt-pt/estudos/` | `https://buzzmonitor.com/pt-pt/webinars/` |
| LATAM | `https://buzzmonitor.com/es/ebooks/` | `https://buzzmonitor.com/es/estudios/` | `https://buzzmonitor.com/es/webinars/` |

**Nota:** nao existe ainda uma URL dedicada de inscricao em newsletter pra PT/LATAM. Usar a pagina de ebooks como destino e sinalizar a pendencia no rodape do artigo.

### LPs comerciais (mencao leve, NUNCA como CTA de fechamento)

| Regiao | LPs |
|---|---|
| LATAM | `https://contenido.getbuzzmonitor.com/plataforma-completa-monitorizacion-redes-sociales`, `https://contenido.getbuzzmonitor.com/la-mejor-plataforma`, `https://contenido.getbuzzmonitor.com/gestion-social-media`, `https://contenido.getbuzzmonitor.com/plataforma-completa-social-listening` |
| PT | `https://conteudo.getbuzzmonitor.com/atendimento-multicanal`, `https://conteudo.getbuzzmonitor.com/institucional` |

Escolher a LP pelo tema do artigo — nao usar por padrao fixo, e nao forcar se nao encaixar naturalmente.

**Por que estas LPs ainda estao em `getbuzzmonitor.com`:** a migracao levou o site e o blog, mas estas LPs continuam publicadas nos subdominios antigos (200 em 2026-10-15). Quando ganharem versao em `buzzmonitor.com`, trocar aqui. Se alguma passar a redirecionar ou der erro, nao use e avise no relatorio.

### Cases publicados (usar so quando o tema pedir naturalmente, nunca forcar)

**Regra de verificacao de numero:** Youse (SLA 36h→3h, -75% headcount) e Hering (NPS +11 pontos em 12 meses) ja estao verificados no `BRANDBOOK.md` — pode citar o numero exato. Qualquer outro case desta lista **nao tem numero verificado neste repo** — so mencionar de forma descritiva, sem inventar metrica.

**Dominio dos cases (atualizado em 2026-10-15, pos-migracao):** os cases agora sao posts do blog regional, em `buzzmonitor.com/blog/{pt-pt|es}/{slug}/`, com o mesmo slug que tinham em `getbuzzmonitor.com`. Uma excecao: a versao ES do case Sube ganhou o sufixo `-2` (`sube-agencia-experiencia-buzzmonitor-2`); o slug sem sufixo redireciona pra versao PT-PT. Cada URL abaixo foi validada por HTTP 200 sem redirect.

**PT-PT:**
- `https://buzzmonitor.com/blog/pt-pt/como-o-grupo-casas-bahia-gere-1-200-filiais-no-google-meu-negocio-com-relatorios-diarios-de-ia/`
- `https://buzzmonitor.com/blog/pt-pt/sube-agencia-experiencia-buzzmonitor/`
- `https://buzzmonitor.com/blog/pt-pt/como-eureka-centralizou-a-sua-gestao-digital-e-optimizou-a-sua-escuta-social-com-buzzmonitor/`
- `https://buzzmonitor.com/blog/pt-pt/caso-de-sucesso-como-a-caffeine-army-transformou-a-sua-estrategia-de-social-listening/`
- `https://buzzmonitor.com/blog/pt-pt/caso-de-sucesso-a-arauco-impulsiona-uma-estrategia-de-escuta-ativa-e-analise-de-dados/`
- `https://buzzmonitor.com/blog/pt-pt/caso-de-sucesso-a-smart-fit-otimiza-o-seu-atendimento-ao-cliente-integrando-a-buzzmonitor/`
- `https://buzzmonitor.com/blog/pt-pt/como-a-youse-reduziu-seu-sla-de-36-para-3-horas-com-inteligencia-artificial/` (verificado — BRANDBOOK)
- `https://buzzmonitor.com/blog/pt-pt/caso-imed-group-monitorizacao-eficaz-das-redes-sociais-e-identificacao-de-tendencias/`
- `https://buzzmonitor.com/blog/pt-pt/caso-turismo-porto-e-norte-como-a-inteligencia-artificial-ajuda-na-analise-do-buzz-gerado-nas-redes-sociais/`
- `https://buzzmonitor.com/blog/pt-pt/caso-buzzmonitor-e-grupo-trigo-gestao-de-crises-e-monitorizacao-eficiente-nas-redes-sociais/`
- `https://buzzmonitor.com/blog/pt-pt/caso-oi-otimizacao-de-resultados-operacionais-com-o-ai-insights/`
- `https://buzzmonitor.com/blog/pt-pt/como-fidelizar-clientes-atraves-das-redes-sociais-caso-de-sucesso-da-pague-menos-e-extrafarma/`
- `https://buzzmonitor.com/blog/pt-pt/caso-panvel/`
- `https://buzzmonitor.com/blog/pt-pt/caso-camil-alimentos/`
- `https://buzzmonitor.com/blog/pt-pt/caso-grupo-rai-monitorizacao-redes-social-ia/`
- `https://buzzmonitor.com/blog/pt-pt/caso-bizum-como-utilizar-o-social-listening-para-impulsionar-campanhas-criativas/`
- `https://buzzmonitor.com/blog/pt-pt/social-media-na-pratica-star-wars-o-despertar-de-um-caso-de-estudo/`

**ES-LATAM:**
- `https://buzzmonitor.com/blog/es/como-bionatural-transformo-una-campana-en-inteligencia-de-marca-con-monitoreo-en-tiempo-real/`
- `https://buzzmonitor.com/blog/es/caso-exito-youse-buzzmonitor-sla-ia/` (verificado — BRANDBOOK)
- `https://buzzmonitor.com/blog/es/hering-mejoro-su-nps-con-social-istening/` (verificado — BRANDBOOK; slug real do site, nao e typo)
- `https://buzzmonitor.com/blog/es/como-reducir-sla-en-agencia-caso-koko-buzzmonitor/`
- `https://buzzmonitor.com/blog/es/caso-exito-caffeine-army-estrategia-de-social-listening/`
- `https://buzzmonitor.com/blog/es/casas-bahia-gestion-google-my-business-ia/`
- `https://buzzmonitor.com/blog/es/sube-agencia-experiencia-buzzmonitor-2/`
- `https://buzzmonitor.com/blog/es/como-eureka-centralizo-su-gestion-digital-y-optimizo-su-escucha-social-con-buzzmonitor/`
- `https://buzzmonitor.com/blog/es/como-unidas-redujo-el-sla-de-atencion-al-cliente-en-un-93-con-la-ia-de-buzzmonitor/`
- `https://buzzmonitor.com/blog/es/agencia-aumento-productividad-marketing/`
- `https://buzzmonitor.com/blog/es/grupo-casas-bahia-optimiza-las-interacciones-en-redes-sociales-con-chatgpt-integrado-con-buzzmonitor/`
- `https://buzzmonitor.com/blog/es/caso-buzzmonitor-y-stone-co-gestion-centralizada-de-redes-sociales/`
- `https://buzzmonitor.com/blog/es/caso-de-exito-viacao-ideal-como-optimizar-la-atencion-al-cliente-en-redes-sociales/`
- `https://buzzmonitor.com/blog/es/caso-buzzmonitor-y-camil-alimentos/`
- `https://buzzmonitor.com/blog/es/como-fidelizar-clientes-a-traves-de-las-redes-sociales-caso-de-exito-de-pague-menos-y-extrafarma/`
- `https://buzzmonitor.com/blog/es/caso-de-exito-smart-fit-optimiza-su-atencion-al-cliente-integrando-buzzmonitor/`
- `https://buzzmonitor.com/blog/es/caso-de-exito-arauco-impulsa-una-estrategia-de-escucha-activa-y-analisis-de-datos/`
- `https://buzzmonitor.com/blog/es/caso-sest-senat-y-buzzmonitor-centralizacion-de-servicios-para-161-unidades-operativas/`
- `https://buzzmonitor.com/blog/es/caso-via-varejo-ia-en-la-optimizacion-del-servicio-al-cliente/`
- `https://buzzmonitor.com/blog/es/caso-gil-do-vigor-seguimiento-con-buzzmonitor/`
- `https://buzzmonitor.com/blog/es/caso-teleperformance-record-atencion-al-cliente-con-buzzmonitor/`
- `https://buzzmonitor.com/blog/es/social-media-en-la-practica-aprende-con-el-caso-mcdonalds/`
- `https://buzzmonitor.com/blog/es/caso-de-exito-houz-comunicacao-social-listening-y-programacion-de-contenido-en-redes-sociales/`
- `https://buzzmonitor.com/blog/es/caso-bizum-como-usar-el-social-listening-para-impulsar-campanas-creativas/`
- `https://buzzmonitor.com/blog/es/caso-trento-oportunidades-de-mercado-con-monitorizacion-de-redes-sociales/`
- `https://buzzmonitor.com/blog/es/caso-sonae-sierra-atencion-centralizada-y-bots-de-voz/`
- `https://buzzmonitor.com/blog/es/caso-mc-donalds/`
- `https://buzzmonitor.com/blog/es/caso-yammi-como-mantener-buenas-relaciones-en-grupos-de-fans-de-facebook/`
- `https://buzzmonitor.com/blog/es/caso-de-exito-imed-group-monitoreo-eficaz-e-identificacion-de-tendencias/`
- `https://buzzmonitor.com/blog/es/caso-de-exito-oi-optimizacion-de-resultados-operacionales-con-ai-insights/`
- `https://buzzmonitor.com/blog/es/caso-de-exito-cesgranrio-monitoreo-estrategico-de-la-marca-y-percepcion-en-concursos-publicos/`
- `https://buzzmonitor.com/blog/es/el-caso-del-bot-de-enotel-un-chatbot-que-se-activa-a-partir-de-comentarios/`
- `https://buzzmonitor.com/blog/es/caso-o-boticario-para-acabar-con-los-efectos-del-estres-en-la-piel-de-los-tuiteros/`
- `https://buzzmonitor.com/blog/es/caso-turismo-de-oporto-y-norte-de-portugal-como-la-inteligencia-artificial-ayuda-en-el-analisis-del-buzz-generado-en-las-redes-sociales/`
- `https://buzzmonitor.com/blog/es/caso-vigor-monitorizacion-con-buzzmonitor/`
- `https://buzzmonitor.com/blog/es/social-media-en-la-practica-el-caso-ultragaz-como-administrar-el-contenido-de-mas-de-700-distribuidores-en-facebook/`

### Links internos (artigos ja gerados por esta skill) — URL real de producao, nunca placeholder

Linka so artigos **ja gerados** por esta skill, na mesma regiao (ver `_state-{regiao}.json`), usando a URL real de producao:

```
PT:    https://buzzmonitor.com/blog/pt-pt/{slug}/
LATAM: https://buzzmonitor.com/blog/es/{slug}/
```

`{slug}` = exatamente o slug gravado no `_state-{regiao}.json` do artigo linkado. **Sem UTM** nestes links (internos, mesmo dominio).

**Nota historica — mecanica de reserva de slug (desativada em 2026-07-24):** ate a v1.2.3, quando um artigo linkava outro item da MESMA fila fixa que ainda nao tinha sido gerado, a skill reservava o slug com antecedencia (`status: "reservado"` em `_state-{regiao}.json`) pra manter o link valido quando o item fosse escrito depois. Essa mecanica dependia de uma fila fixa e conhecida de antemao — sem ela, nao ha como saber o slug de um tema que ainda nao foi decidido. Os itens antigos com `reservado`/`reservado_por` ja resolvidos (todos os 40 artigos do lote de julho ja estao `publicado`) ficam no arquivo como historico; a mecanica em si nao se aplica mais a artigos novos. Se for preciso linkar um tema futuro ainda nao gerado, usar texto placeholder `[LINK: tema X — a gerar]` e avisar no relatorio.

### Formula de UTM (mesma convencao do resto da base, aplicar em toda URL externa)

```
?utm_source=blog-buzzmonitor&utm_medium=organic&utm_campaign={slug-do-artigo-atual}&utm_content={destino}
```

`{slug-do-artigo-atual}` = o `{SLUG}` do artigo sendo escrito. `{utm_content}` = um identificador curto do destino.

## Sobreposicao com conteudo ja publicado (Passo 2.5)

O Passo 2.5 cruza o tema/angulo escolhido contra duas fontes:

1. **Historico da propria skill** (`_state-{regiao}.json`, desde 2026-07-24) — evita que esta skill repita a mesma pergunta central em dois artigos da mesma regiao.
2. **Blog de producao real, via sitemap ao vivo** (desde 2026-10-15). Em julho a Barbara deixou essa camada de fora porque o sitemap internacional ainda nao existia, e ficou combinado ligar quando ele estivesse pronto. Com a migracao de set/2026 ficou: os posts de LATAM e PT entraram no mesmo sitemap do blog BR.

**Como fazer o crawl:**

- Sitemap-index: `https://buzzmonitor.com/blog/sitemap.xml` (redireciona pra `sitemap_index.xml`). Siga os filhos `post-sitemap*.xml` (hoje sao 3) e agregue.
- **Filtre pelo prefixo da regiao:** `pt` → so URLs com `/blog/pt-pt/`; `latam` → so URLs com `/blog/es/`. O resto (BR, `/blog/en/`) nao conta. Nao existe sitemap separado por idioma (`/blog/es/sitemap.xml` e `/blog/pt-pt/sitemap.xml` dao 404).
- Volume em 2026-10-15: ~860 posts ES e ~870 PT-PT. Como o `WebFetch` resume paginas grandes e pode cortar a lista, prefira `curl` via Bash e compare pelo slug:
  ```bash
  for sm in $(curl -sL https://buzzmonitor.com/blog/sitemap_index.xml | grep -oE 'https://[^<]+post-sitemap[0-9]*\.xml'); do
    curl -sL "$sm" | grep -oE '<loc>[^<]+</loc>' | sed -E 's#</?loc>##g'
  done | grep '/blog/pt-pt/'   # ou '/blog/es/' pra LATAM
  ```
- Muitos desses posts sao herdados do antigo `getbuzzmonitor.com` (inclusive os cases). Cruze slug e tema: o mesmo "o que e X" ja publicado anos atras conta como JA_COBERTO ou PARCIAL, dependendo do angulo.
- Se o sitemap falhar (timeout, 5xx), siga so com o `_state-{regiao}.json` e registre a falha em "Pendencias". Nao trave a execucao por isso.

Diferente do BR, nao ha `blog-cache` local pra PT/LATAM: o crawl ao vivo e a unica fonte do blog real.

## Schema de `_state-{regiao}.json` (log corrido, desde 2026-07-24)

```json
{
  "ultima_atualizacao": "YYYY-MM-DD",
  "regiao": "pt",
  "idioma": "pt-pt",
  "total_artigos": 21,
  "itens": [
    {
      "numero": "21",
      "titulo": "...",
      "cluster": "Métricas & Desenvolvimento",
      "slug": "...",
      "title_seo": "...",
      "meta_descricao": "...",
      "palavra_chave": "...",
      "keyword_candidatas": [{"termo": "...", "volume": 0, "database": "pt"}],
      "url_notion": "https://...",
      "caminho_local": "conteudo-blog/buzzmonitor/artigos-pt/21-{slug}.md",
      "pendencias": "",
      "data": "YYYY-MM-DD"
    }
  ]
}
```

**Compatibilidade com o schema antigo:** os 20 itens do lote de julho/2026 (numeros 01-20) continuam no arquivo com o schema antigo (`status: "publicado"`, sem `cluster`/`keyword_candidatas` — alguns tiveram `status: "reservado"` transitorio, ja todos resolvidos) — nao reescrever essas entradas, so adicionar as novas a partir do numero 21. `regiao`/`idioma` sao fixos por arquivo.

## Quando NAO usar esta skill

- Artigo comercial de meio/fundo de funil pra Buzzmonitor Brasil → `blog-criar-artigo`
- Artigo editorial ancorado em noticia recente → `pauta-quente` ou `news-criar-post`
- Newsletter semanal → familia `news-*`
- Conteudo para redes sociais → familia `social-*`
