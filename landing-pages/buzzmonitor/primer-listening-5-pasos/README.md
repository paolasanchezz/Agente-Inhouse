# LP Buzzmonitor — primer-listening-5-pasos

**Gerado em:** 2026-08-06
**Copy-fonte:** `copy.txt` (ja preparado em sessao anterior — 2026-07-15/08-03, sem alteracoes)
**Design espelhado:** `landing-pages/buzzmonitor/que-es-mcp/index.html` (paleta, tipografia League Spartan/Lato/Manrope, cards de programa com callout, secao de speaker, grid "para quien")
**Regiao:** latam (es-419) · GTM-MKQBX2MG
**Tipo:** webinar bajo demanda / perpetuo (sem tarjeta de fecha nem badge "En vivo", ao contrario do modelo que-es-mcp que e ao vivo com fecha fixa) — objetivo ToFu (inscripcion), nao BoFu

**Ajuste 2026-08-06 (a pedido do usuario):** CTA mudou de "Agenda una demo de 30 minutos..." pra "Reserva tu lugar gratis" (2 ocorrencias em copy.txt: HERO e CTA FINAL) + adicionado formulario mock de inscricao no hero (Nombre/Correo/Empresa), mesmo padrao visual do que-es-mcp.

## Estrutura

- HERO (kicker + h1 + body + meta de 3 itens + formulario mock de inscricao no hero-visual)
- LO QUE VAS A VER — 3 cards numerados com callout "Qué vas a ver"
- QUIEN PRESENTA — Juan Diego Forero (foto reaproveitada de `monitoreo-competidores-ia-latam`)
- PARA QUIÉN ES — grid 2x2 (4 itens)
- CTA FINAL — h2 + body + CTA "Reserva tu lugar gratis" (ancora pro form do hero)
- Footer

## Hreflang / multi-idioma

Esta LP tem uma irma em PT-BR ja publicada: `primeiro-listening-5-passos`. O HTML desta LP referencia as 2 variantes (`es-419` + `pt-BR`) + `x-default` apontando pra BR (mercado principal). **A LP PT-BR publicada NAO foi alterada** (decisao do usuario) — so tem hreflang auto-referente por enquanto. Idealmente ela ganha o link de volta pra esta versao ES numa proxima atualizacao dela.

## Estado

- [x] HTML gerado
- [x] Revisao (frontend-design review + web-design-guidelines) — ver `REVISAO.md` (2 criticos aplicados, 2 melhorias + 1 nice-to-have documentados)
- [ ] CTA final integrado com link/embed real de inscricao (ClickMeeting, Jotform, HubSpot, etc.) — rodar `/lp-integrar-form` quando tiver o provedor
- [ ] Publicado — `webinar.buzzmonitor.com` esta migrado pro fluxo CI (manifest + PR), ver `.claude/skills/lp-publicar/SKILL.md` Passo 0.0

## Pendencias

1. **Formulario de inscricao** e mock (`action` inline via JS, sem backend) — precisa conectar a um provedor real (ClickMeeting, Jotform, HubSpot, etc.) antes de publicar, via `/lp-integrar-form`.
2. **OG image** — nao gerada (decisao do usuario, igual `webinar-atencion-multicanal-latam`). `og:image`/`twitter:image` apontam pro logo da marca via `{{BRAND_LOGO_PNG_PATH}}`.
3. `{{DOMAIN}}` e `{{BRAND_LOGO_PNG_PATH}}` sao placeholders resolvidos no fluxo de publicacao (CI, ver manifest.json do dominio).

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg`, `logo-reversed.svg`, `logo-icon.png`
- `./assets/juan-diego-forero.jpg` (LP-local, reaproveitado de `monitoreo-competidores-ia-latam/assets/`)
