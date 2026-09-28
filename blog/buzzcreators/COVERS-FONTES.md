# Capas do blog — fontes e licença

As capas em `public/assets/covers/*.jpg` são fotografias do **Pexels** ([licença Pexels](https://www.pexels.com/license/): uso comercial livre, sem atribuição obrigatória, modificação permitida). Substituíram as capas HTML→PNG geradas pelo `gen_cover.py` em 2026-07-07, a pedido dos sócios (imagens livres de copyright).

Cada capa foi baixada já recortada em 1200×630 via CDN do Pexels (`?w=1200&h=630&fit=crop`).

| Post (slug) | Foto Pexels |
|---|---|
| agencias-escalar-influencia | https://www.pexels.com/photo/6476257/ |
| briefing-para-influenciadores-modelo | https://www.pexels.com/photo/8547193/ |
| como-encontrar-microinfluenciadores | https://www.pexels.com/photo/6964949/ |
| como-escolher-influenciadores | https://www.pexels.com/photo/12903101/ |
| como-fazer-campanha-influenciadores | https://www.pexels.com/photo/7710074/ |
| como-identificar-influenciadores-falsos | https://www.pexels.com/photo/5240546/ |
| como-medir-roi-marketing-de-influencia | https://www.pexels.com/photo/577210/ |
| creator-economy-no-brasil | https://www.pexels.com/photo/20040022/ |
| employee-advocacy-colaboradores-vozes-marca | https://www.pexels.com/photo/22046230/ |
| gestao-influenciadores-sem-caos | https://www.pexels.com/photo/5990265/ |
| metricas-marketing-de-influencia-vaidade | https://www.pexels.com/photo/9822668/ |
| micro-vs-macro-influenciadores | https://www.pexels.com/photo/3689546/ |
| microinfluenciadores-roi-3x | https://www.pexels.com/photo/36730088/ |
| o-que-e-marketing-de-influencia | https://www.pexels.com/photo/23225012/ |
| o-que-e-ugc-conteudo-gerado-usuario | https://www.pexels.com/photo/5717972/ |
| o-que-sao-nanoinfluenciadores | https://www.pexels.com/photo/9179068/ |
| plataforma-marketing-de-influencia | https://www.pexels.com/photo/139387/ |
| quanto-custa-contratar-influenciador | https://www.pexels.com/photo/5900228/ |
| tendencias-marketing-de-influencia-2026 | https://www.pexels.com/photo/8728288/ |
| tipos-de-influenciadores | https://www.pexels.com/photo/7550544/ |
| formatos-de-campanha-com-creators | https://www.pexels.com/photo/9909081/ |
| o-que-e-seeding-de-influenciadores | https://www.pexels.com/photo/4440774/ |
| gifting-de-influenciadores | https://www.pexels.com/photo/6334621/ |
| embaixadores-de-marca-como-estruturar | https://www.pexels.com/photo/4793177/ |
| marketing-de-afiliados-com-creators | https://www.pexels.com/photo/10223868/ |
| whitelisting-de-influenciadores | https://www.pexels.com/photo/238480/ |
| ugc-pago-creator-ads | https://www.pexels.com/photo/8117901/ |
| campanha-de-review-e-unboxing | https://www.pexels.com/photo/6612545/ |
| sorteio-com-influenciadores | https://www.pexels.com/photo/8459420/ |
| takeover-com-creators | https://www.pexels.com/photo/38062351/ |
| collab-de-produto-com-creators | https://www.pexels.com/photo/9850422/ |
| live-commerce-com-influenciadores | https://www.pexels.com/photo/7242798/ |
| always-on-ou-campanha-pontual | https://www.pexels.com/photo/15635233/ |
| social-listening-para-encontrar-influenciadores | https://www.pexels.com/photo/5965649/ |
| como-pagar-influenciadores | https://www.pexels.com/photo/20051498/ |
| taxa-de-engajamento-como-calcular | https://www.pexels.com/photo/8143737/ |
| cpm-cpe-cpv-marketing-de-influencia | https://www.pexels.com/photo/8636589/ |
| como-avaliar-midia-kit-de-influenciador | https://www.pexels.com/photo/9869392/ |
| marketing-de-influencia-para-restaurantes | https://www.pexels.com/photo/3756456/ |
| quanto-tempo-leva-resultado-influencia | https://www.pexels.com/photo/4397906/ |
| novidades-plataforma-julho-2026 | https://www.pexels.com/photo/10352379/ |
| como-trabalhar-com-micro-e-nano-influenciadores | https://www.pexels.com/photo/8360444/ |
| plataformas-de-influenciadores-como-escolher | https://www.pexels.com/photo/7710142/ |
| geo-com-influenciadores | https://www.pexels.com/photo/7859172/ |
| micro-e-nano-creators-na-busca-por-ia | https://www.pexels.com/photo/12673799/ |
| influenciador-de-autoridade | https://www.pexels.com/photo/6129444/ |
| briefing-de-creators-para-busca-por-ia | https://www.pexels.com/photo/9809834/ |
| onde-publicar-conteudo-de-creator-para-ia | https://www.pexels.com/photo/4144975/ |
| creators-no-linkedin-marketing-b2b | https://www.pexels.com/photo/6893890/ |
| case-eskala-gestao-de-influenciadores | https://www.pexels.com/photo/7679476/ |
| case-apsen-colaboradores-creators | https://www.pexels.com/photo/8370422/ |
| case-buzzmonitor-creators-linkedin-cpl | https://www.pexels.com/photo/36766661/ |

## Posts novos

Post novo sem `cover:` ganha foto Pexels **automaticamente** no Passo 0.6 da skill `blog-publicar`, via `pexels_cover.py` (busca por query em inglês, baixa 1200×630 pelo CDN, preenche `cover`/`coverAlt` e acrescenta a linha desta tabela). O `gen_cover.py` (HTML→PNG, estilo rejeitado pelos sócios) segue **só como fallback** quando a busca falha — capa gerada por ele deve ser trocada por foto depois. Alternativa por IA (Bloom) documentada no PR da troca original (#46); requer créditos no workspace.
