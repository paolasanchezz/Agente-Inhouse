# Revisao LP — cxpress/webinar-canales-unificados-video

**Data:** 2026-08-18
**Auditores:** auditoria manual (fidelidade de copy + GTM + Pixel + SEO + GUIDELINES), mesmo checklist aplicado as demais LPs desta serie

## Auditorias que passaram sem achados

- **Fidelidade de copy:** H1, heading da secao Clientes e o bloco CTA final (H2, BODY, 3 labels, CTA) batem literal com `copy.txt`, conferido via `get_page_text` do preview.
- **Anti-IA:** em-dash 0, ellipsis 0 ocorrencias literais.
- **GTM:** `GTM-WRQ47B9R` presente 2/2 (head + noscript) — `check_gtm_region.py` OK.
- **Meta Pixel:** `1484678896147110` presente (script + noscript), mesmo ID das demais LPs desta serie.
- **Robots:** `noindex, follow` deliberado (pagina pos-acao, mesmo precedente de `video-atendimento-obrigado`).
- **Acessibilidade:** skip-link, `:focus-visible`, alt descritivo na imagem de clientes, icone de play do placeholder marcado `aria-hidden`, icones de redes sociais no footer com `aria-label` individual (Facebook/Instagram/LinkedIn), `prefers-reduced-motion` coberto.
- **Assets:** `clientes-cxpress.png` (brand/cxpress) confirmado existente antes de referenciar.

## Decisoes de design registradas (nao sao "criticos", sao escolhas deliberadas)

- **Placeholder de video:** o video ainda nao esta hospedado no YouTube. Em vez de publicar um `<iframe>` quebrado ou bloquear a entrega, foi construido um estado visual "aguardando" (icone de play + texto) que nao passa a impressao de pagina com erro, mais o snippet do embed real ja deixado pronto (comentado) pra troca rapida assim que o link chegar.
- **Redes sociais so no footer, sem secao dedicada:** decisao explicita do usuario, alinhada com boas praticas de paginas pos-conversao (nao competir com o CTA principal de agendar demo).
- **URLs de redes sociais verificadas ao vivo, nao do config:** `brand/cxpress/social-media.json` tem os campos `null`. Em vez de deixar em aberto ou inventar, o footer real de `cxpress.ai` foi inspecionado via browser (JS `getBoundingClientRect`/`offsetParent`) pra confirmar quais links estao de fato visiveis e ativos, descartando um segundo set de links ocultos no DOM (variante "cxpress.es" nao renderizada). Isso evita tanto inventar URLs quanto usar um link que existe no HTML mas nao esta realmente em uso no site.

## Verificacao de assets (preview local)

- Texto renderizado conferido via `get_page_text` — bate com `copy.txt`.
- Imagem de clientes (`clientes-cxpress.png`, asset de marca fora da pasta do projeto) nao carregou no preview `file://` local — mesma limitacao ja documentada nas LPs anteriores desta sessao (a mesma imagem ja esta confirmada funcional em producao via `banimento-whatsapp-latam`). Confirmacao definitiva via HTTP real apos o deploy CI.

## Proximos passos

- Trocar o placeholder de video pelo embed real assim que o usuario mandar o link do YouTube.
- CTA de agendamento ainda e mock (`href="#"`) — quando tiver o link real, rodar `/lp-integrar-form cxpress/webinar-canales-unificados-video "snippet"`.
- Publicar: `content.cxpress.io` esta no fluxo CI — adicionar ao manifest + abrir PR.
