# LP Buzzmonitor — caso-smartfit-video

**Gerado em:** 2026-11-03
**Design espelhado:** `landing-pages/buzzmonitor/primer-listening-5-pasos-video/` (mesmo template, so troca copy, video e UTM)
**Regiao:** latam (es-419) · GTM-MKQBX2MG
**Dominio:** webinar.buzzmonitor.com (guarda-chuva migrado pro CI)

## O que e esta pagina

Pagina **pos-inscricao** do perpetuo `caso-smartfit` no modelo "LP Aula": video ja liberado + botao pra LP comercial + redes LATAM no footer. `noindex, follow` (pagina pos-acao). Segunda das 3 paginas de video dos perpetuos LATAM (depois de `primer-listening-5-pasos-video`).

## Decisoes

1. **Slug novo (`-video`):** `caso-smartfit-confirmado` segue servindo o fluxo ClickMeeting ate a troca do form.
2. **Video:** YouTube `LM6sBxbL_MA` ("Webinar: Cómo Smart Fit centralizó la atención de 40 franquicias en una sola plataforma"), embed `?rel=0`.
3. **Copy enxuta** (padrao aprovado na `primer-listening-5-pasos-video`): H1 = titulo do caso, 1 linha de apoio, CTA final curto.
4. **Botao:** "¡Agenda una demo gratuita!" → `content.buzzmonitor.com/plataforma-integral-social-media?utm_source=perpetuo&utm_content=agradecimento-perpetuo-caso-smartfit` (mesmo destino/UTM da `-confirmado`).

## Estado

- [x] HTML gerado e conferido em desktop e mobile
- [ ] LP de captura `caso-smartfit` trocar o form ClickMeeting pelo Jotform LATAM `261188302248052` + redirect pra esta pagina (ver `landing-pages/GUIA-webinar-perpetuo-destino.md`)
