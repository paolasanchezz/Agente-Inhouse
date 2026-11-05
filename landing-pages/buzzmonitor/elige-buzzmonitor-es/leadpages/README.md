# elige-buzzmonitor-es (Leadpages, ES-LATAM)

Versão ES-LATAM de `escolha-a-buzzmonitor` (comparador Buzzmonitor vs. outras plataformas).
Rascunho na org Tami Buzzmonitor: slug `elige-buzzmonitor-es`, pageId `rm9y347b5p65uvapeupajbud`. **Não publicado.**

- Fonte BR lida por `get_page` em 2026-11-04: `source-br.html` (sem GTM na fonte).
- `index.html` = HTML enviado ao rascunho (totalLength 39042 conferido). CSS e JS da página viraram assets:
  `styles-es.css` = `/api/pages/elige-buzzmonitor-es/assets/ow4yosszhiqbhj60locdsw94` (o `ro8hkujzr49k1b70335wy3oq` é a v1 sem text-wrap, não usada);
  `page-es.js` = `/api/pages/elige-buzzmonitor-es/assets/i33d3ugvz2jqq67pvr5rh5uu`.
- GTM `GTM-PC4TJ6H` (head + noscript). Form Jotform LATAM `241825239057661` (mesmo embed das LPs LATAM).
- Vídeo: `nBMZZZKrMpI` (versão ES usada nas LPs LATAM) no lugar de `Z1FddOh05O4`.
- Hero: tela ES `/api/pages/buzzmonitor-ia-latam/assets/opedsdj4k8xqy9lo9c72jagy`.
- Depoimentos: as 4 imagens PT viraram cards de texto com as 3 citações ES já usadas nas LPs LATAM (McCann, TotalPass, McDonald's).
- Preço: R$ 1.790,00/mês → USD 390/mes (padrão LATAM).
- Runtime assado removido (`is-in`, `data-done`, estilos inline do JS, `data-persist-nav-*`, matriz pré-renderizada, CSS de breakpoint da Leadpages). Acrescentado `text-wrap: balance/pretty`.
- SEO: indexável (origem é index,follow), favicon `r4blvhgoch5t7sruh3183cjj`, og:image em branco (a da origem é screenshot automático em PT).

Pendências:
- GIF do HUD (`q2adg6gb34o4uk9c7ahd93ng`) tem texto em PT (comentário + "Responder", "Mensagem pública").
- Mural de logos (`fpokt249ckqs18i8vnm2k5bt`) e marquee são clientes brasileiros.
- Claims mantidos como na origem e a confirmar para LATAM: "Reclame Aqui" na lista de canais, "organismos de defensa del consumidor", "Oferta por tiempo limitado", 14 días gratis.
- Tag do GTM-PC4TJ6H (`add_utm_stuff`) dá erro "jQuery is not defined" (a página não tem jQuery).
