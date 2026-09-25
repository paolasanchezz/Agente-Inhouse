# Revisao LP — cxpress/gestao-canais-ia-2027

**Data:** 2026-09-25
**Escopo:** LP derivada da `gestao-canais-ia-2026` (design e acessibilidade ja auditados la, incl. fix AA de contraste/countdown no commit 61d88f3). Revisao focada no que mudou + checagens deterministicas completas.

## Checagens deterministicas

- [x] GTM (`check_gtm_region.py`): `ok` — GTM-T4XDWHL3, regiao brasil. Selo gravado.
- [x] SEO §15: description 1 · robots 1 · og: 10 · twitter: 4 · JSON-LD 1 (parseia: Organization, WebPage, Event) · canonical 1
- [x] §16 hreflang: LP unica (sem irmas -es/-pt) → so canonical + x-default
- [x] §17 logo header/footer → `https://home.cxpress.io`, `target=_blank rel=noopener`, aria-label PT-BR
- [x] §19 logos SVG sem `<text>` (logo-primary 0, logo-reversed 0)
- [x] §18 OG image `assets/og-gestao-canais-ia-2027.png` 1200×630, sem `og-image.png` orfao
- [x] Em-dash no HTML: 0 (1 ocorrencia em comentario HTML removida)
- [x] Fidelidade da copy: textos visiveis batem literal com `copy.txt`. Fora da copy, so whitelist/heranca da LP 2026: nav meta "Evento presencial", eyebrows de secao ("O encontro", "Programação", "No palco", "Sobre"), labels do countdown, skip-link.
- [x] Mobile 375px: sem overflow horizontal (scrollWidth = 375)

## Aplicado automaticamente (1 critico)

- [x] Em-dash em comentario HTML da secao de inscricao — trocado por dois-pontos.

## Ajustes feitos durante a revisao visual

- [x] Eyebrow "Novidades da plataforma" nao cabe em 1 linha a 375px no piso de 14px (§20) — em ≤420px vira bloco de cantos 14px (em vez de pilula) pra acomodar as 2 linhas sem deformar.

## Melhorias opcionais (3)

- [ ] Endereco sem andar/sala e CEP — completar `.a2` e `PostalAddress` quando o Espaco Eureka confirmar.
- [ ] `brand-manifest.json` da Cxpress sem `regions`/`socials` — JSON-LD sem `sameAs` (afeta todas as LPs Cxpress, nao so esta).
- [ ] Regra CSS `.news-body .btn` sem uso (sobra de layout) — pode ser removida.

## Nice-to-haves (1)

- [ ] Programacao: considerar badge "Novidade" no item 11h20 alem da bolinha laranja (hoje so peso de fonte + marcador cheio).

## Proximos passos

- Design aprovado? -> /lp-integrar-form cxpress/gestao-canais-ia-2027 "{snippet}"
- Ou publicar com form mock: /lp-publicar cxpress gestao-canais-ia-2027 content.cxpress.io
