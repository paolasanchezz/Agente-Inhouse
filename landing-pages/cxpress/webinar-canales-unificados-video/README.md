# LP Cxpress — webinar-canales-unificados-video

**Gerado em:** 2026-08-18
**Copy-fonte:** `copy.txt` (bloco CTA final fornecido literalmente pelo usuario; demais textos adaptados/reaproveitados, ver notas abaixo)
**Design espelhado:** `landing-pages/cxpress/video-atendimento-obrigado/index.html` (secao de video + tokens) + secao "clientes" de `landing-pages/cxpress/banimento-whatsapp-latam/index.html`, a pedido do usuario ("basicamente como este ejemplo" citando `contenido.getbuzzmonitor.com/webinar-marketing-trends-2026`)
**Regiao:** latam (es-419) · GTM-WRQ47B9R · Pixel LATAM 1484678896147110
**Dominio:** content.cxpress.io (guarda-chuva migrado pro CI)

## O que e esta pagina

Pagina **pos-inscricao** do webinar `webinar-canales-unificados`: o lead que ja se inscreveu chega aqui pra assistir o video e, ao final, agendar uma demo. Sem formulario de captura (o lead ja se inscreveu antes) — `noindex, follow` deliberado, mesmo precedente de `video-atendimento-obrigado` e `conheca-a-cxpress-confirmado`.

## Decisoes tomadas nesta sessao

1. **Video ainda nao esta no YouTube:** usuario esta subindo o video. Em vez de bloquear a LP, foi construido um placeholder visual (`.video-frame.is-placeholder`, com icone de play + "El video estará disponible muy pronto.") no exato lugar onde o `<iframe>` do YouTube vai entrar — o HTML ja traz, comentado, o snippet pronto pra colar o embed assim que o usuario mandar o link. Nao foi feito upload/commit de nenhum arquivo de video no repo (git nao e lugar pra hospedar video, e o CSP do guarda-chuva so libera embed do dominio youtube.com).
2. **Secao "Clientes":** heading e asset (`clientes-cxpress.png`) reaproveitados literalmente de `banimento-whatsapp-latam` (mesma marca, mesma secao, ja aprovada e publicada).
3. **CTA final:** texto 100% literal do que o usuario forneceu (H2, BODY, 3 LABELs, CTA). CTA ainda mock (`href="#"`) — aguardando link real de agendamento (Calendly, HubSpot Meetings, etc.), rodar `/lp-integrar-form` quando tiver.
4. **Redes sociais no footer:** usuario pediu icones de redes sociais + link pro site no footer. `brand/cxpress/social-media.json` tem os handles como `null` (nao confirmados) — em vez de inventar ou perguntar de novo, as URLs foram verificadas diretamente no footer real e visivel de `https://cxpress.ai` (via browser): Facebook `facebook.com/cxpress.io`, Instagram `instagram.com/cxpress.io`, LinkedIn `linkedin.com/company/cxpress`. Havia um segundo set de links "cxpress.es" no DOM da mesma pagina, mas oculto (sem `offsetParent`, dimensao zero) — descartado por nao ser o que esta realmente visivel/ativo no site.
5. **Sem secao dedicada de redes sociais no corpo:** decisao alinhada com o usuario — pagina pos-conversao deve manter foco numa unica acao (agendar demo); redes sociais ficam so no footer, nao competem com o CTA principal.

## Estrutura

- Header (logo, sem CTA)
- VIDEO — eyebrow "Video liberado" + H1 + video (placeholder ate ter o link do YouTube)
- CLIENTES — heading + logos (reaproveitado de banimento-whatsapp-latam)
- CTA FINAL — h2 + body + 3 labels + botao (mock, aguardando link real de agendamento)
- Footer — logo + copyright + link pro site + icones de redes sociais (Facebook, Instagram, LinkedIn)

## Estado

- [x] HTML gerado
- [x] Revisao tecnica (em-dash: 0, ellipsis 0 literal, GTM 2/2, Pixel 1x, `check_gtm_region.py` OK, fidelidade de copy conferida via texto renderizado) — ver `REVISAO.md`
- [ ] Video real do YouTube — pendente do usuario subir e mandar o link
- [ ] CTA de agendamento integrado com link real — rodar `/lp-integrar-form` quando tiver
- [ ] Publicacao — pendente PR via fluxo CI

## Pendencias

1. **Embed do video** — trocar o placeholder pelo `<iframe>` do YouTube assim que o usuario mandar o link (snippet ja deixado comentado no HTML, pronto pra colar).
2. **CTA de agendamento** — mock, aguardando link real (Calendly, HubSpot Meetings, etc.).
3. **OG image** — nao gerada; pagina e `noindex`, entao baixa prioridade.

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-primary.svg`, `logo-reversed.svg`, `logo-icon.png`
- `../../brand/cxpress/assets/plataforma/clientes-cxpress.png` (asset de marca ja existente, reaproveitado)
