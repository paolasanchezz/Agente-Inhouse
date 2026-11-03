# LP Buzzmonitor — gestion-crisis

**Gerado em:** 2026-08-07
**Copy-fonte:** `copy.txt` (usuario reescreveu o copy completo em 2026-08-07; backup do copy anterior em `copy.txt.2026-08-07_bak`)
**Design espelhado:** `landing-pages/buzzmonitor/caso-smartfit/index.html` (paleta, tipografia, hero com formulario mock, cards de programa numerados com callout "Qué vas a ver", secao de resultados com logos, speaker) — a pedido explicito do usuario ("LP de referencia https://webinar.buzzmonitor.com/caso-smartfit")
**Regiao:** latam (es-419) · GTM-MKQBX2MG

## Decisoes tomadas nesta sessao

1. **Caso E-CLIK confirmado** — o `copy.txt` original trazia um item `[VERIFICAR]` sobre referenciar um caso brasileiro (E-CLIK) em conteudo LATAM. Perguntado ao usuario via AskUserQuestion; confirmado explicitamente que pode ser usado.
2. **Logo CRM Bonus (nao "E-CLIK")** — o usuario enviou um logo com o texto "CRM Bonus", nao "E-CLIK". Foi sinalizada a discrepancia diretamente ao usuario antes de prosseguir; o usuario esclareceu que E-CLIK e a empresa de tecnologia (retail/fidelizacao) e CRM Bonus e a marca comercial da sua plataforma, confirmando o uso do logo de CRM Bonus na secao de Resultados. Arquivo salvo em `assets/crm-bonus-logo.jpg` (447x447, JPEG).
3. **Foto de Lorena Rodriguez reaproveitada** — mesma foto ja usada em `social-listening-mayo-2026-latam/assets/lorena-rodriguez.jpg`, copiada para `assets/lorena-rodriguez.jpg` desta LP.
4. **5 cards de programa (nao 3)** — a copy trouxe 5 componentes do sistema (numerados 01-05 nos H3), entao o grid "Lo que vas a ver" tem 5 `program-card` em vez dos 3 do template de referencia. CSS do grid (`repeat(3, 1fr)`) se ajusta automaticamente com wrap em telas menores; mobile ja empilha em 1 coluna.
5. **2 cards de resultado (nao 4)** — a copy trouxe apenas 2 LABELs em RESULTADOS (crise contida em <1h, 28 melhorias de produto). Grid `results-grid` (`repeat(2, 1fr)`) fica naturalmente preenchido, sem espaco vazio.
6. **Sem logo de cliente no hero** — ao contrario de `caso-smartfit` (caso de cliente com logo no card do form), esta LP e um webinar (nao um caso isolado), entao o `hero-form` segue o padrao de `primer-listening-5-pasos`/`webinar-atencion-multicanal-latam`: sem `hero-card-logo`, so o formulario mock de inscricao.
7. **CTA "¡Reserva tu lugar!"** em todas as 3 ocorrencias (header, hero, CTA final) — ja veio assim na copy fornecida pelo usuario, sem pivotagem necessaria nesta sessao.
8. **Ajuste pos-publicacao (2026-08-07):** usuario pediu (a) trocar overline/H2 de "Lo que vas a ver" -> "Lo que aprenderás" / "Cinco pasos para detectar y gestionar una crisis, con el caso real de E-CLIK." e (b) aumentar o tamanho dos logos Buzzmonitor × CRM Bonus na secao Resultados, que estavam ilegiveis. `.results-logos img` foi de `height: 26px` para `height: 44px` (gap de 18px para 24px, separador "×" de 14px para 18px).

## Estrutura

- HERO (kicker + h1 + body + "10 minutos" + formulario mock de inscricao)
- LO QUE VAS A VER — 5 cards numerados (01-05) com callout "Qué vas a ver"
- RESULTADOS — logos Buzzmonitor × CRM Bonus + 2 cards de stats do caso E-CLIK
- QUIEN PRESENTA — Lorena Rodriguez, Business Developer · Buzzmonitor (foto reaproveitada)
- PARA QUIÉN ES — grid 2x2 (4 itens)
- CTA FINAL — h2 + body + label + CTA (mock, aguardando link real de inscricao)
- Footer

## Estado

- [x] HTML gerado
- [x] Revisao tecnica (em-dash: 0, ellipsis: 1 ocorrencia como `&hellip;`, GTM 2/2, SEO meta completo, `check_gtm_region.py` e `build_umbrella.py` OK) — ver `REVISAO.md`
- [ ] CTA integrado com link/embed real de inscricao (ClickMeeting, HubSpot Meetings, etc.) — rodar `/lp-integrar-form` quando tiver o link
- [ ] Publicacao — pendente PR via fluxo CI (`webinar.buzzmonitor.com` esta no guarda-chuva migrado)

## Pendencias

1. **Formulario de inscricao** e mock (sem backend real, so JS local) — precisa conectar a um provedor real antes de considerar a LP "completa" (nao bloqueia publicacao, mesmo padrao das demais LPs desta leva).
2. **OG image** — nao gerada, `og:image`/`twitter:image` apontam pro logo da marca via `{{BRAND_LOGO_PNG_PATH}}` (mesmo criterio das ultimas LPs).
3. `{{DOMAIN}}` e `{{BRAND_LOGO_PNG_PATH}}` sao placeholders resolvidos no fluxo de publicacao (CI).

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg`, `logo-reversed.svg`, `logo-icon.png`
- `./assets/lorena-rodriguez.jpg` (LP-local, reaproveitado de `social-listening-mayo-2026-latam/assets/`)
- `./assets/crm-bonus-logo.jpg` (LP-local, logo do cliente, autorizado pelo usuario em 2026-08-07 — ver nota no `copy.txt`)

**Form provider:** Jotform 261188302248052 (2026-11-03) — substituiu o form proprio do ClickMeeting (`/api/clickmeeting-register`). A inscricao na sala e a pagina de agradecimento passam a ser do Jotform; o bloco de data da proxima sessao (`/api/next-webinar`) continua.
