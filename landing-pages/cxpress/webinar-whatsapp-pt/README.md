# LP Cxpress — webinar-whatsapp-pt

**Gerado em:** 2026-09-04
**Copy-fonte:** `copy.txt` (output de /lp-preparar, a partir de "Webinar Perpétuo Cxpress.pdf")
**Guarda-chuva:** `content.cxpress.io` (projeto Vercel `cxpress-lp-playbook-whatsapp2026`) — dominio MIGRADO pro CI
**lang:** `pt-PT` · **GTM:** `GTM-NW6V5KBM` (regiao portugal)
**Thanks page irma:** `landing-pages/cxpress/webinar-whatsapp-pt-confirmado`

Webinar perpetuo (automated recurring) transmitido no ClickMeeting. Trafego vem de anuncio
Meta (1 estatico + 1 video) — criativos em `conhecimento/copywriting/criacao/cxpress/2026-09-04/`.

## Estrutura

1. HERO (kicker + H1 com a dor + sub + CTA + cartao factual com Samir)
2. INSCRICAO (form MOCK, 2.a seccao — ToFu por GUIDELINES §10)
3. PROBLEMA (lista vertical, 5 X vermelhos + bloco de fechamento navy)
4. CONSEQUENCIA (3 cards de impacto: cliente / equipa / negocio + frase-ancora)
5. PROGRAMA (3 cards numerados)
6. TRES-FORMAS (comparativo 3 colunas; API Oficial destacada em verde)
7. NUMERO (grid 2x2 de beneficios com check verde + nota de boas praticas)
8. COEX (diferencial: texto + painel de 3 itens)
9. PLATAFORMA (seccao de pausa, GUIDELINES §2 — centrada + pills de canais)
10. PARA QUEM (4 itens + mascote Samir)
11. URGENCIA (fundo navy + tag laranja rotacionada — aparece 1x, GUIDELINES §8)
12. CTA-FINAL (gradiente royal->navy, o unico gradiente da LP)
13. FOOTER

Contagem de blocos bate item a item com `copy.txt` (GUIDELINES §9): 5 dores, 3 cards de
programa, 3 formas, 4 beneficios, 3 itens de COEX, 4 itens de "para quem".

## Estado

- [x] HTML gerado
- [x] OG image 1200×630 → `assets/og-webinar-whatsapp-pt.png` (template em `og-template-webinar-whatsapp-pt.html`)
- [x] Revisao (ver `REVISAO.md`)
- [ ] **Formulario integrado** — publicada SEM form real, a pedido da Marielle. O mock
      (`action="#"`) fica no ar. Integrar depois via `/lp-integrar-form cxpress/webinar-whatsapp-pt "snippet"`
      OU via a API do ClickMeeting (form custom + `api/clickmeeting-register.js`, que ja existe
      no guarda-chuva — brief completo em `landing-pages/cxpress/conheca-a-cxpress/BRIEF-IMPLEMENTACAO.md`).
- [x] Publicado

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
- `../../brand/cxpress/assets/mascot/samir-sticker.png` (cartao do hero)
- `../../brand/cxpress/assets/mascot/samir-laptop.png` (seccao Para quem)
- `./assets/og-webinar-whatsapp-pt.png` (OG, via `{{OG_IMAGE_PATH}}`)

Os 3 SVGs de logo da Cxpress foram validados com `grep -c '<text'` = 0 (GUIDELINES §19).

## Pendencias conhecidas

1. **Form real** (acima) — bloqueia a captacao de lead. Hoje a LP so aquece e o registo
   tem de acontecer noutro lugar.
2. **hreflang cruzado com a versao ES.** Existe a LP irma `webinar-bloqueo-whatsapp`
   (ES-LATAM, mesmo webinar). Nenhuma das duas declara `hreflang` hoje. Cruzar exige editar
   tambem a LP ES (que esta no ar) — fora do escopo deste pedido. Enquanto isso, esta LP
   declara so `canonical` pra si mesma, que e o comportamento correto de LP unica
   (lp-gerar Passo 1, "Se for unica, omitir hreflang").
