# LP Buzzmonitor — primer-listening-5-pasos-video

**Gerado em:** 2026-11-03
**Design espelhado:** `landing-pages/cxpress/webinar-canales-unificados-video/index.html` (estrutura video-hero + CTA final + footer com redes), com tokens/tipografia da `primer-listening-5-pasos` (Buzzmonitor: #390155 / League Spartan + Lato + Manrope)
**Regiao:** latam (es-419) · GTM-MKQBX2MG
**Dominio:** webinar.buzzmonitor.com (guarda-chuva migrado pro CI)

## O que e esta pagina

Pagina **pos-inscricao** do perpetuo `primer-listening-5-pasos` no modelo "LP Aula": o lead preenche o Jotform na LP de captura e cai aqui com o video ja liberado + botao pra LP comercial. Sem ClickMeeting, sem sala, sem data. `noindex, follow` deliberado (pagina pos-acao).

Parte da migracao dos 3 perpetuos LATAM (`caso-smartfit`, `gestion-crisis`, `primer-listening-5-pasos`) de ClickMeeting pra Jotform + video on-demand. Esta e a primeira.

## Decisoes tomadas nesta sessao

1. **Slug novo (`-video`), nao reaproveitar `-confirmado`:** a usuaria pediu manter tudo do ClickMeeting no ar ate a troca do form. `primer-listening-5-pasos-confirmado` segue servindo o fluxo atual (sala ClickMeeting); quando a LP de captura migrar pro Jotform, o destino passa a ser esta pagina.
2. **Video:** YouTube `_En4vJnCsLc` ("Webinar: Tu primer listening en 5 pasos", canal Buzzmonitor en Español), embed `youtube.com/embed/_En4vJnCsLc?rel=0`, carrega no load.
3. **Botao comercial:** mesmo destino e UTMs da `-confirmado` atual (`content.buzzmonitor.com/plataforma-integral-social-media?utm_source=perpetuo&utm_content=agradecimento-perpetuo-primer-listening`) e texto trocado pra "¡Agenda una demo gratuita!" a pedido da usuaria (2026-11-03).
4. **Redes sociais LATAM no footer:** Instagram `buzzmonitor.es`, X `Buzzmonitor_ES`, Facebook `Buzzmonitorespanol`, LinkedIn `buzzmonitor`, YouTube `@buzzmonitor_es` (mesmo set atual de `agencias-es` e demais LPs LATAM, pos-PR 861); site `buzzmonitor.com/es/`.
5. **Sem secao de clientes** (a referencia Cxpress tem): escopo pedido foi video + botao + redes.

## Estrutura

- Header (logo, sem CTA)
- VIDEO — eyebrow "Webinar online" + H1 + sub + embed 16:9
- CTA FINAL — H2 + body + botao pra LP comercial
- Footer — logo + copyright + getbuzzmonitor.com + 5 redes LATAM

## Estado

- [x] HTML gerado e conferido em desktop e mobile (servidor local; video toca)
- [ ] LP de captura `primer-listening-5-pasos` trocar o form ClickMeeting pelo Jotform LATAM `261188302248052` (integracao com a usuaria)
- [ ] Redirect pos-envio: o form `261188302248052` e compartilhado com os webinars ao vivo LATAM e tem uma unica Thank You Page. Aplicar o despachante de `landing-pages/GUIA-webinar-perpetuo-destino.md` (§2) na pagina onde ele aterrissa hoje + limpar a chave `bmPerpetuoNext` nas LPs ao vivo que usam o mesmo form
- [ ] Adicionar o slug ao `manifest.json` do dominio e publicar via `/lp-publicar` (PR, CI)
