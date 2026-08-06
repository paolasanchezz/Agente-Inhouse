# LP Buzzmonitor — caso-smartfit

**Gerado em:** 2026-08-06 (copy atualizado no mesmo dia — v2)
**Copy-fonte:** `copy.txt` (v2 — usuario reescreveu o copy completo em 2026-08-06; backup da v1 em `copy.txt.2026-08-06_v2_bak`)
**Design espelhado:** `landing-pages/buzzmonitor/que-es-mcp/index.html` (paleta, tipografia, cards de programa com callout, secao de speaker) — adaptado pra formato de **caso de cliente** (BoFu, CTA "agenda una conversacion", nao formulario de inscricao)
**Regiao:** latam (es-419) · GTM-MKQBX2MG

## Decisoes tomadas nesta sessao

1. **Bio de Milagro Pantoja** — mantida generica (nao afirma que ela acompanhou diretamente a implementacao de Smart Fit), a pedido do usuario. Item historico [VERIFICAR] do guiao original fica assim resolvido.
2. **Logo do Smart Fit** — usuario confirmou autorizacao de uso e enviou o arquivo (`Smart_Fit_logo.svg.webp`, na verdade um WEBP 1280x468 com transparencia, apesar do nome). Copiado para `assets/smart-fit-logo.webp` e usado no card do hero.
3. **Sem badges "Gratis"/"En vivo"** no hero — formato do caso (gravacao vs sessao ao vivo) ficou ambiguo no guiao original; copy.txt ja resolveu isso omitindo os badges, mantido assim.
4. ~~CTA e BoFu, nao ToFu~~ — **atualizado 2026-08-06:** com o copy v2 (framing "en 10 minutos descubriras...", nao mais "agenda una llamada"), o usuario pediu formulario mock no hero igual as demais LPs. Adicionado (Nombre completo, Correo electrónico, Empresa opcional), mesmo padrao visual/CSS de `primer-listening-5-pasos`. Logo do Smart Fit mantido acima do form. Vitor conecta o backend real depois via `/lp-integrar-form`.
5. **Texto do CTA mudou pra "¡Reserva tu lugar!"** (2 ocorrencias: HERO e CTA FINAL) — a pedido do usuario, pra manter consistencia com `primer-listening-5-pasos`.
6. **Copy v2 (2026-08-06):** usuario reescreveu SUB, H2/H3/BODY/LABEL da secao "Lo que vas a ver", RESULTADOS, bio da Milagro, os 4 itens de "Para quien es" e o H2/BODY/labels do CTA FINAL. Mudanca mais importante: o CTA FINAL deixou de falar em "agenda una llamada de 30 minutos" (BoFu) e passou a falar em "en 10 minutos descubriras..." (labels trocaram de "30 minutos"/"Sin demo enlatada" pra "10 minutos"/"Caso real") — isso resolve a tensao semantica anotada antes: agora "¡Reserva tu lugar!" faz sentido, porque se reserva o acesso a um conteudo de 10 min, nao a uma chamada 1:1.

## Estrutura

- HERO (kicker + h1 + body + "10 minutos" + logo Smart Fit + formulario mock de inscricao)
- LO QUE VAS A VER — 3 cards numerados com callout "Qué vas a ver"
- RESULTADOS (secao nova, sem equivalente no modelo que-es-mcp) — grid 2x2 de stats reais do caso
- QUIEN PRESENTA — Milagro Pantoja (foto reaproveitada de `atencion-al-cliente-es`)
- PARA QUIÉN ES — grid 2x2 (4 itens)
- CTA FINAL — h2 + body + 2 labels + CTA (mock, aguardando link real de agendamento)
- Footer

## Estado

- [x] HTML gerado
- [x] Revisao (frontend-design review + web-design-guidelines) — ver `REVISAO.md` (2 criticos aplicados: hreflang desnecessario removido, lazy-loading corrigido no logo do hero)
- [ ] CTA integrado com link/embed real de agendamento (Calendly, HubSpot Meetings, etc.) — rodar `/lp-integrar-form` quando tiver o link
- [ ] Publicado — `webinar.buzzmonitor.com` esta migrado pro fluxo CI (manifest + PR)

## Pendencias

1. **Formulario de inscricao** e mock (sem backend real, so JS local) — precisa conectar a um provedor real (ClickMeeting, Jotform, HubSpot, etc.) antes de publicar, via `/lp-integrar-form`.
2. **OG image** — nao gerada, `og:image`/`twitter:image` apontam pro logo da marca via `{{BRAND_LOGO_PNG_PATH}}` (mesmo criterio das ultimas LPs).
3. `{{DOMAIN}}` e `{{BRAND_LOGO_PNG_PATH}}` sao placeholders resolvidos no fluxo de publicacao (CI).

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg`, `logo-reversed.svg`, `logo-icon.png`
- `./assets/milagro-pantoja.jpg` (LP-local, reaproveitado de `atencion-al-cliente-es/assets/`)
- `./assets/smart-fit-logo.webp` (LP-local, logo do cliente, autorizado pelo usuario em 2026-08-06)
