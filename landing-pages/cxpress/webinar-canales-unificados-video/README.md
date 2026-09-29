# LP Cxpress — webinar-canales-unificados-video

**Gerado em:** 2026-08-18
**Form provider:** Jotform (2026-09-29) — form ID `252398149653872`, wrapper `.jotform-embed` canonico aplicado.
**Copy-fonte:** `copy.txt` (bloco CTA final fornecido literalmente pelo usuario; demais textos adaptados/reaproveitados, ver notas abaixo)
**Design espelhado:** `landing-pages/cxpress/video-atendimento-obrigado/index.html` (secao de video + tokens) + secao "clientes" de `landing-pages/cxpress/banimento-whatsapp-latam/index.html`, a pedido do usuario ("basicamente como este ejemplo" citando `contenido.getbuzzmonitor.com/webinar-marketing-trends-2026`)
**Regiao:** latam (es-419) · GTM-WRQ47B9R · Pixel LATAM 1484678896147110
**Dominio:** content.cxpress.io (guarda-chuva migrado pro CI)

## O que e esta pagina

Pagina **pos-inscricao** do webinar `webinar-canales-unificados`: o lead que ja se inscreveu chega aqui pra assistir o video e, ao final, agendar uma demo. Sem formulario de captura (o lead ja se inscreveu antes) — `noindex, follow` deliberado, mesmo precedente de `video-atendimento-obrigado` e `conheca-a-cxpress-confirmado`.

## Decisoes tomadas nesta sessao

1. **Video (resolvido 2026-08-19):** publicado inicialmente com placeholder visual (icone de play + "El video estará disponible muy pronto."), pois o usuario ainda estava subindo o video no YouTube. Usuario mandou o link (`https://www.youtube.com/watch?v=i6Af5pEo8aI`) e o placeholder foi trocado pelo `<iframe>` real (`youtube.com/embed/i6Af5pEo8aI?rel=0`), CSS do placeholder removido. Nao foi feito upload/commit de nenhum arquivo de video no repo (git nao e lugar pra hospedar video, e o CSP do guarda-chuva so libera embed do dominio youtube.com).
2. **Secao "Clientes":** heading e asset (`clientes-cxpress.png`) reaproveitados literalmente de `banimento-whatsapp-latam` (mesma marca, mesma secao, ja aprovada e publicada).
3. **CTA final:** texto 100% literal do que o usuario forneceu (H2, BODY, 3 LABELs, CTA). Em 2026-09-29 o botao mock (`href="#"`) foi substituido pelo embed Jotform `252398149653872` (form de demo) dentro da propria secao `#agendar`.
4. **Redes sociais no footer:** usuario pediu icones de redes sociais + link pro site no footer. Primeira tentativa: verificado no footer visivel de `https://cxpress.ai` (via browser), usado o set "cxpress.io". Usuario corrigiu (2026-08-19): as contas certas sao o set "cxpress.es" — Facebook `facebook.com/profile.php?id=61584681389155`, Instagram `instagram.com/cxpress.es`. LinkedIn mantido (`linkedin.com/company/cxpress`, e o mesmo nos dois sets). Adicionado tambem YouTube (`youtube.com/@Cxpress_es`), fornecido pelo usuario (nao estava visivel no footer do site institucional).
5. **Sem secao dedicada de redes sociais no corpo:** decisao alinhada com o usuario — pagina pos-conversao deve manter foco numa unica acao (agendar demo); redes sociais ficam so no footer, nao competem com o CTA principal.

## Estrutura

- Header (logo, sem CTA)
- VIDEO — eyebrow "Video liberado" + H1 + video (placeholder ate ter o link do YouTube)
- CLIENTES — heading + logos (reaproveitado de banimento-whatsapp-latam)
- CTA FINAL — h2 + body + 3 labels + formulario Jotform de demo
- Footer — logo + copyright + link pro site + icones de redes sociais (Facebook, Instagram, LinkedIn)

## Estado

- [x] HTML gerado
- [x] Revisao tecnica (em-dash: 0, ellipsis 0 literal, GTM 2/2, Pixel 1x, `check_gtm_region.py` OK, fidelidade de copy conferida via texto renderizado) — ver `REVISAO.md`
- [x] Video real do YouTube integrado (2026-08-19)
- [x] CTA de agendamento integrado (Jotform `252398149653872`, 2026-09-29)
- [x] Publicacao — via fluxo CI

## Pendencias

1. ~~**CTA de agendamento**~~ — resolvido em 2026-09-29 com o embed Jotform `252398149653872`.
2. **OG image** — nao gerada; pagina e `noindex`, entao baixa prioridade.

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-primary.svg`, `logo-reversed.svg`, `logo-icon.png`
- `../../brand/cxpress/assets/plataforma/clientes-cxpress.png` (asset de marca ja existente, reaproveitado)
