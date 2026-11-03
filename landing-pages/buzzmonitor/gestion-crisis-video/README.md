# LP Buzzmonitor — gestion-crisis-video

**Gerado em:** 2026-11-03
**Design espelhado:** `landing-pages/buzzmonitor/primer-listening-5-pasos-video/` (mesmo template, so troca copy, video e UTM)
**Regiao:** latam (es-419) · GTM-MKQBX2MG
**Dominio:** webinar.buzzmonitor.com (guarda-chuva migrado pro CI)

## O que e esta pagina

Pagina **pos-inscricao** do perpetuo `gestion-crisis` no modelo "LP Aula": video ja liberado + botao pra LP comercial + redes LATAM no footer. `noindex, follow` (pagina pos-acao). Terceira das 3 paginas de video dos perpetuos LATAM.

## Decisoes

1. **Slug novo (`-video`):** `gestion-crisis-confirmado` segue servindo o fluxo ClickMeeting ate a troca do form.
2. **Video:** YouTube `be5dKHz0z9c` ("Webinar: Cómo evitar descubrir una crisis cuando ya es demasiado tarde"), embed `?rel=0`.
3. **Copy enxuta** (padrao aprovado na `primer-listening-5-pasos-video`): H1 e linha de apoio = H1/SUB da LP de captura.
4. **Botao:** "¡Agenda una demo gratuita!" → `content.buzzmonitor.com/plataforma-integral-social-media?utm_source=perpetuo&utm_content=agradecimento-perpetuo-gestion-crisis`. A `-confirmado` de crise nao tinha botao comercial; usado o mesmo destino dos outros 2 perpetuos LATAM (nao existe LP comercial de crise em ES — `gestao-de-crises` e PT-BR).

## Estado

- [x] HTML gerado e conferido
- [ ] LP de captura `gestion-crisis` trocar o form ClickMeeting pelo Jotform LATAM `261188302248052` + redirect pra esta pagina (ver `landing-pages/GUIA-webinar-perpetuo-destino.md`)
