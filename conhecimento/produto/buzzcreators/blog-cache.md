# Blog cache — Buzzcreators

> Índice cumulativo de posts do blog Buzzcreators, usado para **dedupe** pelas skills `/blog-diario` e `news-*`.
> Disciplina **append-only**: nunca deletar entrada; só acrescentar e atualizar "Última verificação".
> A skill `/blog-diario` adiciona aqui os posts que cria, marcados `status: draft-notion` (troca para `publicado` + URL viva quando o time sobe no CMS).

**Blog:** https://blog.buzzcreators.com.br · **Última verificação:** 2026-09-25

---

## Estado do inventário (2026-07-21)

**O blog está PUBLICADO em `https://blog.buzzcreators.com.br` — não é mais greenfield.**

- Blog Astro estático (fonte: `blog/buzzcreators/src/content/blog/*.md` neste repo), publicado via `/blog-publicar`. Posts servem em `/blog/{slug}`.
- **1ª leva (jun-jul/2026):** os 20 posts do plano editorial (`seo/plano-editorial-20-artigos.md`) — publicados.
- **Changelog:** série "Novidades" (não-SEO, para clientes) — 1 post publicado.
- **2ª leva (2026-07-21):** 20 posts novos criados no repo — série **"Formatos de Campanha"** (12 posts: hub + um por tipo de campanha com creators) + **lacunas GEO** (8 posts: social listening, pagamento lado-marca, always-on, taxa de engajamento, mídia kit, CPM/CPE/CPV, vertical restaurantes, tempo de resultado). Status `repo` até o próximo deploy.
- Nota histórica: até 2026-07-02 o domínio institucional (`buzzcreators.com.br/blog/`) retornava 404 e este cache marcava "greenfield". O blog nasceu no subdomínio próprio.

**Implicação para dedupe:** os 6 clusters originais (C1–C6) estão majoritariamente cobertos e a série Formatos de Campanha ocupa o espaço de "tipos de campanha". Antes de produzir tema novo, conferir a tabela abaixo — a maioria dos "subtópicos a criar" do `clusters-brasil.md` original JÁ EXISTE.

---

## Posts indexados

| Data | Título (H1) | Slug | Cluster | Funil | Keyword principal | Status | URL |
|---|---|---|---|---|---|---|---|
| 2026-06-10 | Gestão de influenciadores sem caos: como sair da planilha | gestao-influenciadores-sem-caos | C3 Gestão | MoFu→BoFu | gestão de influenciadores | publicado | https://blog.buzzcreators.com.br/blog/gestao-influenciadores-sem-caos |
| 2026-06-12 | Por que microinfluenciadores entregam ROI maior que os macros | microinfluenciadores-roi-3x | C2 Micro & Nano | MoFu | microinfluenciadores ROI | publicado | https://blog.buzzcreators.com.br/blog/microinfluenciadores-roi-3x |
| 2026-06-15 | Como agências escalam campanhas de influência sem inchar a equipe | agencias-escalar-influencia | C3 Gestão | MoFu | agência de influenciadores | publicado | https://blog.buzzcreators.com.br/blog/agencias-escalar-influencia |
| 2026-06-16 | O que é marketing de influência: o guia para marcas em 2026 | o-que-e-marketing-de-influencia | C1 Fundamentos | ToFu | marketing de influência | publicado | https://blog.buzzcreators.com.br/blog/o-que-e-marketing-de-influencia |
| 2026-06-17 | Quanto custa contratar um influenciador no Brasil em 2026 | quanto-custa-contratar-influenciador | C5 ROI & Preço | MoFu→BoFu | quanto custa contratar influenciador | publicado | https://blog.buzzcreators.com.br/blog/quanto-custa-contratar-influenciador |
| 2026-06-18 | Como escolher os influenciadores certos para a sua campanha | como-escolher-influenciadores | C4 Descoberta | MoFu | como escolher influenciadores | publicado | https://blog.buzzcreators.com.br/blog/como-escolher-influenciadores |
| 2026-06-19 | Como medir o ROI do marketing de influência: as métricas certas | como-medir-roi-marketing-de-influencia | C5 ROI & Preço | BoFu | roi marketing de influência | publicado | https://blog.buzzcreators.com.br/blog/como-medir-roi-marketing-de-influencia |
| 2026-06-20 | O que é UGC (conteúdo gerado pelo usuário) e como as marcas usam | o-que-e-ugc-conteudo-gerado-usuario | C6 Creator Economy | ToFu | o que é ugc | publicado | https://blog.buzzcreators.com.br/blog/o-que-e-ugc-conteudo-gerado-usuario |
| 2026-06-21 | Como fazer uma campanha de influência: do briefing ao relatório | como-fazer-campanha-influenciadores | C3 Gestão | MoFu | como fazer campanha com influenciadores | publicado | https://blog.buzzcreators.com.br/blog/como-fazer-campanha-influenciadores |
| 2026-06-22 | Tipos de influenciadores: mega, macro, micro e nano | tipos-de-influenciadores | C1 Fundamentos | ToFu→MoFu | tipos de influenciadores | publicado | https://blog.buzzcreators.com.br/blog/tipos-de-influenciadores |
| 2026-06-23 | Como encontrar microinfluenciadores para a sua marca | como-encontrar-microinfluenciadores | C4 Descoberta | MoFu | como encontrar microinfluencers | publicado | https://blog.buzzcreators.com.br/blog/como-encontrar-microinfluenciadores |
| 2026-06-24 | Plataforma de marketing de influência: o que é e como escolher | plataforma-marketing-de-influencia | C3 Gestão | MoFu→BoFu | plataforma de influenciadores | publicado | https://blog.buzzcreators.com.br/blog/plataforma-marketing-de-influencia |
| 2026-06-25 | Tendências de marketing de influência para 2026 | tendencias-marketing-de-influencia-2026 | C1 Fundamentos | ToFu | tendências marketing de influência 2026 | publicado | https://blog.buzzcreators.com.br/blog/tendencias-marketing-de-influencia-2026 |
| 2026-06-26 | O que são nanoinfluenciadores e como usá-los na estratégia | o-que-sao-nanoinfluenciadores | C2 Micro & Nano | MoFu | nano influenciadores | publicado | https://blog.buzzcreators.com.br/blog/o-que-sao-nanoinfluenciadores |
| 2026-06-27 | Micro vs. macro influenciadores: qual escolher por objetivo | micro-vs-macro-influenciadores | C2 Micro & Nano | MoFu | micro influenciadores | publicado | https://blog.buzzcreators.com.br/blog/micro-vs-macro-influenciadores |
| 2026-06-28 | Como escrever um briefing para influenciadores (com modelo) | briefing-para-influenciadores-modelo | C3 Gestão | MoFu | briefing para influenciadores | publicado | https://blog.buzzcreators.com.br/blog/briefing-para-influenciadores-modelo |
| 2026-06-29 | Creator economy no Brasil: o que é e por que importa | creator-economy-no-brasil | C6 Creator Economy | ToFu | creator economy | publicado | https://blog.buzzcreators.com.br/blog/creator-economy-no-brasil |
| 2026-06-30 | Métricas de influência que importam (e as de vaidade a evitar) | metricas-marketing-de-influencia-vaidade | C5 ROI & Preço | MoFu | métricas de influenciadores | publicado | https://blog.buzzcreators.com.br/blog/metricas-marketing-de-influencia-vaidade |
| 2026-07-01 | Employee advocacy: como transformar colaboradores em vozes da marca | employee-advocacy-colaboradores-vozes-marca | C6 Creator Economy | MoFu | employee advocacy | publicado | https://blog.buzzcreators.com.br/blog/employee-advocacy-colaboradores-vozes-marca |
| 2026-07-02 | Como identificar influenciadores falsos e engajamento inflado | como-identificar-influenciadores-falsos | C4 Descoberta | MoFu | influenciadores falsos | publicado | https://blog.buzzcreators.com.br/blog/como-identificar-influenciadores-falsos |
| 2026-07-09 | Tipos de campanha com creators: os 11 formatos que as marcas usam | formatos-de-campanha-com-creators | C7 Formatos (hub) | ToFu→MoFu | tipos de campanha com influenciadores | publicado | https://blog.buzzcreators.com.br/blog/formatos-de-campanha-com-creators |
| 2026-07-09 | O que é seeding de influenciadores e como fazer bem | o-que-e-seeding-de-influenciadores | C7 Formatos | MoFu | seeding de influenciadores | publicado | https://blog.buzzcreators.com.br/blog/o-que-e-seeding-de-influenciadores |
| 2026-07-09 | Social listening para encontrar influenciadores que já amam sua marca | social-listening-para-encontrar-influenciadores | C4 Descoberta | MoFu | social listening influenciadores | publicado | https://blog.buzzcreators.com.br/blog/social-listening-para-encontrar-influenciadores |
| 2026-07-10 | Gifting de influenciadores: o que é e quando faz sentido | gifting-de-influenciadores | C7 Formatos | MoFu | gifting | publicado | https://blog.buzzcreators.com.br/blog/gifting-de-influenciadores |
| 2026-07-10 | Taxa de engajamento: como calcular e o que é um bom número | taxa-de-engajamento-como-calcular | C5 ROI & Preço | MoFu | taxa de engajamento | publicado | https://blog.buzzcreators.com.br/blog/taxa-de-engajamento-como-calcular |
| 2026-07-13 | Embaixadores de marca: como estruturar um programa com creators | embaixadores-de-marca-como-estruturar | C7 Formatos | MoFu | embaixador de marca | publicado | https://blog.buzzcreators.com.br/blog/embaixadores-de-marca-como-estruturar |
| 2026-07-13 | Como pagar influenciadores: o guia da marca, do PIX à escala | como-pagar-influenciadores | C3 Gestão | MoFu→BoFu | como pagar influenciadores | publicado | https://blog.buzzcreators.com.br/blog/como-pagar-influenciadores |
| 2026-07-13 | UGC pago: contratar creators para produzir anúncios da marca | ugc-pago-creator-ads | C7 Formatos | MoFu | ugc ads / creator ads | publicado | https://blog.buzzcreators.com.br/blog/ugc-pago-creator-ads |
| 2026-07-14 | Marketing de afiliados com creators: comissão por venda na influência | marketing-de-afiliados-com-creators | C7 Formatos | MoFu | marketing de afiliados influenciadores | publicado | https://blog.buzzcreators.com.br/blog/marketing-de-afiliados-com-creators |
| 2026-07-14 | CPM, CPE e CPV no marketing de influência: o que cada um mede | cpm-cpe-cpv-marketing-de-influencia | C5 ROI & Preço | MoFu | cpm cpe cpv influência | publicado | https://blog.buzzcreators.com.br/blog/cpm-cpe-cpv-marketing-de-influencia |
| 2026-07-15 | Whitelisting de influenciadores: anúncios com a cara do creator | whitelisting-de-influenciadores | C7 Formatos | MoFu | whitelisting | publicado | https://blog.buzzcreators.com.br/blog/whitelisting-de-influenciadores |
| 2026-07-15 | Review e unboxing com creators: prova social que vende | campanha-de-review-e-unboxing | C7 Formatos | MoFu | review unboxing influenciadores | publicado | https://blog.buzzcreators.com.br/blog/campanha-de-review-e-unboxing |
| 2026-07-16 | Sorteio com influenciadores: quando o giveaway vale a pena | sorteio-com-influenciadores | C7 Formatos | MoFu | sorteio com influenciadores / giveaway | publicado | https://blog.buzzcreators.com.br/blog/sorteio-com-influenciadores |
| 2026-07-16 | Influência always-on ou campanha pontual: qual estratégia usar | always-on-ou-campanha-pontual | C3 Gestão | MoFu | always-on marketing de influência | publicado | https://blog.buzzcreators.com.br/blog/always-on-ou-campanha-pontual |
| 2026-07-17 | Takeover: quando o creator assume o perfil da marca | takeover-com-creators | C7 Formatos | MoFu | takeover redes sociais | publicado | https://blog.buzzcreators.com.br/blog/takeover-com-creators |
| 2026-07-17 | Como avaliar o mídia kit de um influenciador antes de fechar | como-avaliar-midia-kit-de-influenciador | C4 Descoberta | MoFu | mídia kit influenciador | publicado | https://blog.buzzcreators.com.br/blog/como-avaliar-midia-kit-de-influenciador |
| 2026-07-17 | Marketing de influência para restaurantes e delivery: o guia local | marketing-de-influencia-para-restaurantes | Setores | MoFu | marketing de influência restaurantes | publicado | https://blog.buzzcreators.com.br/blog/marketing-de-influencia-para-restaurantes |
| 2026-07-20 | Collab de produto com creators: co-criação que vira lançamento | collab-de-produto-com-creators | C7 Formatos | MoFu | collab com influenciador | publicado | https://blog.buzzcreators.com.br/blog/collab-de-produto-com-creators |
| 2026-07-20 | Live commerce com influenciadores: vender ao vivo com creators | live-commerce-com-influenciadores | C7 Formatos | MoFu | live commerce | publicado | https://blog.buzzcreators.com.br/blog/live-commerce-com-influenciadores |
| 2026-07-20 | Quanto tempo leva para o marketing de influência dar resultado | quanto-tempo-leva-resultado-influencia | C5 ROI & Preço | MoFu | quanto tempo marketing de influência resultado | publicado | https://blog.buzzcreators.com.br/blog/quanto-tempo-leva-resultado-influencia |
| 2026-07-21 | Novidades da plataforma Buzzcreators em julho de 2026 | novidades-plataforma-julho-2026 | Novidades (changelog) | — | — (não-SEO) | publicado | https://blog.buzzcreators.com.br/blog/novidades-plataforma-julho-2026 |
| 2026-07-28 | Como trabalhar com micro e nano influenciadores em escala | como-trabalhar-com-micro-e-nano-influenciadores | C2 Micro & Nano (ponte C3) | MoFu→BoFu | como trabalhar com micro e nano influenciadores | publicado | https://blog.buzzcreators.com.br/blog/como-trabalhar-com-micro-e-nano-influenciadores |
| 2026-08-26 | Plataformas de influenciadores: quais existem e como escolher | plataformas-de-influenciadores-como-escolher | C3 Gestão (ponte C4) | MoFu→BoFu | plataformas de influenciadores | publicado | https://blog.buzzcreators.com.br/blog/plataformas-de-influenciadores-como-escolher |
| 2026-09-25 | GEO com influenciadores: por que sua marca some das respostas da IA | geo-com-influenciadores | C9 Busca por IA (pillar) | ToFu→MoFu | o que é geo / geo com influenciadores | publicado | https://blog.buzzcreators.com.br/blog/geo-com-influenciadores |
| 2026-09-25 | Seguidores não garantem citação: micro e nano creators na busca por IA | micro-e-nano-creators-na-busca-por-ia | C9 Busca por IA (ponte C2) | MoFu | micro influenciadores + busca por IA | publicado | https://blog.buzzcreators.com.br/blog/micro-e-nano-creators-na-busca-por-ia |
| 2026-09-25 | Influenciador de autoridade: o que é e por que a IA prefere especialistas | influenciador-de-autoridade | C9 Busca por IA (ponte C1/C4) | MoFu | influenciador de autoridade | publicado | https://blog.buzzcreators.com.br/blog/influenciador-de-autoridade |
| 2026-09-25 | Briefing de influenciadores para a busca por IA: o que incluir | briefing-de-creators-para-busca-por-ia | C9 Busca por IA (ponte C3) | MoFu | briefing para influenciadores + IA | publicado | https://blog.buzzcreators.com.br/blog/briefing-de-creators-para-busca-por-ia |
| 2026-09-25 | Onde o conteúdo de creator precisa estar para a IA conseguir ler | onde-publicar-conteudo-de-creator-para-ia | C9 Busca por IA | MoFu | youtube seo / conteúdo de creator para IA | publicado | https://blog.buzzcreators.com.br/blog/onde-publicar-conteudo-de-creator-para-ia |
| 2026-09-25 | Creators no LinkedIn: marketing de influência B2B que a IA também lê | creators-no-linkedin-marketing-b2b | C9 Busca por IA (ponte C6) | MoFu | marketing de influência B2B / thought leadership | publicado | https://blog.buzzcreators.com.br/blog/creators-no-linkedin-marketing-b2b |

> Plano da 1ª leva (histórico): `conhecimento/produto/buzzcreators/seo/plano-editorial-20-artigos.md`
> Arquitetura de clusters (fonte de temas): `conhecimento/produto/buzzcreators/seo/clusters-brasil.md`
> **C9 Busca por IA** = cluster "Creators e busca por IA (GEO/AEO)", aberto em 2026-09-25 a partir do guia da Later + classificação YOUPIX. `tipos-de-influenciadores` ganhou seção YOUPIX (updatedDate 2026-09-25).
> **C7 Formatos** = série "Formatos de Campanha" (2ª leva, 2026-07-21): hub + 1 post por tipo de campanha com creators. **Setores** = verticais por indústria (expansível: turismo, beleza…).
> Status `repo` = arquivo pronto em `blog/buzzcreators/src/content/blog/`, entra no ar no próximo `/blog-publicar` (trocar para `publicado` ao confirmar no sitemap). **Reconciliação 2026-07-28:** a 2ª leva (20 posts que estavam `repo`) foi confirmada viva no `sitemap-0.xml` e marcada `publicado`. Novos rascunhos gerados pelo `/blog-diario` entram como `draft-notion` (URL = Notion) até subirem no CMS.
