# LP Cxpress — webinar-whatsapp-pt-confirmado

**Gerado em:** 2026-09-04
**Copy-fonte:** `copy.txt`
**Guarda-chuva:** `content.cxpress.io` — dominio MIGRADO pro CI
**lang:** `pt-PT` · **GTM:** `GTM-NW6V5KBM` · **robots:** `noindex, follow`
**LP-mae:** `landing-pages/cxpress/webinar-whatsapp-pt`

Thanks page do webinar perpetuo PT-PT. Mesmo padrao das irmas ja no ar
(`conheca-a-cxpress-confirmado` BR, `webinar-bloqueo-whatsapp-confirmado` ES).

## Estrutura

1. HERO (badge verde de confirmacao + H1 + sub + CTA "Abrir o webinar" + meta)
2. PREPARACAO (4 passos numerados + mascote Samir joinha)
3. PLATAFORMA / CTA (gradiente royal->navy + CTA de demonstracao com UTM)
4. FOOTER

## Estado

- [x] HTML gerado
- [x] OG image — **reusa** a da LP-mae (`assets/cxpress/og-webinar-whatsapp-pt.png`), por path
      literal. Excecao legitima da GUIDELINES §18 ("OG compartilhada entre LPs irmas"):
      um unico ficheiro fisico, guardado na pasta da LP-mae.
- [x] Revisao (ver `../webinar-whatsapp-pt/REVISAO.md`)
- [ ] **CTA "Abrir o webinar" e MOCK** (`href="#"`, marcado com `data-cm-join`). O destino
      definitivo e a `join_url` que a API do ClickMeeting devolve no registo — so existe
      depois da integracao do formulario. Enquanto o form nao entrar, o utilizador chega
      aqui pelo e-mail de confirmacao do ClickMeeting, que a copy do hero ja explica.
- [x] Publicado

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
- `../../brand/cxpress/assets/mascot/samir-joinha.png` (seccao Preparacao)
- `assets/cxpress/og-webinar-whatsapp-pt.png` (OG da LP-mae, path literal)
