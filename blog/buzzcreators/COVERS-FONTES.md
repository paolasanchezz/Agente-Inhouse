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

## Posts novos

O `gen_cover.py` (skill `blog-publicar`, Passo 0.6) continua existindo e gera capa HTML→PNG **apenas para post sem `cover:`**. Para manter o padrão fotográfico, ao criar post novo escolher uma foto no Pexels, salvar como `public/assets/covers/{slug}.jpg` (1200×630) e preencher `cover`/`coverAlt` à mão — e registrar a fonte nesta tabela. Alternativa por IA (Bloom) documentada no PR desta troca; requer créditos no workspace.
