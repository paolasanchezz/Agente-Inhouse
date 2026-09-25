# LP Cxpress — gestao-canais-ia-2027

**Gerado em:** 2026-09-25
**Copy-fonte:** `copy.txt` (output de /lp-preparar) · Notion: https://app.notion.com/p/3e63934026fd81bbb84ef2690773d410
**Evento:** presencial · 12/11/2026 · 9h às 12h · Espaço Eureka, Av. Paulista, 688, São Paulo/SP
**Guarda-chuva:** `content.cxpress.io` (migrado pro CI — publicar via `/lp-publicar`)

## Origem do layout

HTML derivado da LP `gestao-canais-ia-2026` (mesma marca, mesmo tema, design ja auditado e no ar),
a pedido explicito da solicitante ("usar como referencia a LP de gestao de canais").
Em vez de regerar via `frontend-design`, o HTML de referencia foi adaptado a nova `copy.txt`:

- Estado "Vagas esgotadas" trocado por form mock aberto (GUIDELINES §11) como 2a secao (§10, evento ToFu).
- Secao nova **NOVIDADES** (card lilas) entre POR-QUE-IR e COMO CHEGAR.
- Palestrantes: so Enrico Chiari (card unico centralizado).
- Programacao sem cases de cliente; destaque visual (bolinha laranja cheia) em 11h20 "Novidades da plataforma Cxpress".
- Endereco, mapa, countdown (2026-11-12 09:00 -03:00) e JSON-LD `Event` atualizados.
- Bloco `text-wrap` (GUIDELINES §21) adicionado.

## Estrutura

1. HERO (eyebrow + h1 + sub + pilula data/hora/local + CTA → #inscricao)
2. INSCRICAO (form mock: nome, e-mail corporativo, empresa, cargo, WhatsApp)
3. POR QUE IR
4. NOVIDADES DA PLATAFORMA
5. COMO CHEGAR (mapa + endereco + data + countdown)
6. APRENDIZADOS (6 cards)
7. PROGRAMACAO (8 itens)
8. PALESTRANTES (Enrico Chiari)
9. SOBRE A CXPRESS (+ faixa de clientes)
10. FOOTER

## Estado

- [x] HTML gerado
- [x] OG image 1200×630 → `assets/og-gestao-canais-ia-2027.png`
- [x] Revisao — ver `REVISAO.md`
- [ ] Formulario integrado — rodar `/lp-integrar-form cxpress/gestao-canais-ia-2027 "snippet"`
- [ ] Publicado — rodar `/lp-publicar cxpress gestao-canais-ia-2027 content.cxpress.io`

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-primary.svg` (header + card do palestrante)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `./assets/enrico-chiari.jpg` (copiado da LP 2026)
- `./assets/clientes-cxpress.png` (copiado da LP 2026)
- `./assets/og-gestao-canais-ia-2027.png` (og:image)

## Observacoes

- GTM `GTM-T4XDWHL3` (regiao brasil) — ok, selo gravado em `.tracking.lock`.
- `brand/cxpress/brand-manifest.json` nao tem bloco `regions`/`socials`: JSON-LD `Organization` sem `sameAs` (mesma situacao da LP 2026). Migrar o manifest resolve em todas as LPs Cxpress.
- Endereco sem andar/sala e sem CEP (nao informados). Se houver, incluir em `.a2` e no JSON-LD.
