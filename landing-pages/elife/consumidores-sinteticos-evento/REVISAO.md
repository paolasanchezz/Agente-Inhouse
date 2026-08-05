# Revisão LP — elife/consumidores-sinteticos-evento

**Data:** 2026-06-04
**Auditores:** lp-revisar manual (SEO, a11y, anti-IA, fidelidade de copy)

---

## Aplicado automaticamente (1 crítico)

- [x] **EM-DASH (9 ocorrências)** — títulos SEO (`og:title`, `twitter:title`, `<title>`, JSON-LD) e comentários HTML/CSS. Substituídos por `|` nos títulos e `;`/`,` nos comentários. Contagem final: 0.

## Resolvido neste PR

- [x] **Logos Elife adicionados** — `brand/elife/assets/logos/` agora tem `logo-primary.svg` (vetor puro, sem `<text>` vivo — passa GUIDELINES §19), `logo-primary.png`, `logo-reversed.png/svg`, `logo-icon.png`, `logo-black.png`, `logo-color.png`, `logo-orange.png`. A LP já referencia `logo-icon.png` (favicon), `logo-reversed.png` (header) e `logo-primary.svg` (JSON-LD).

---

## Resultado da auditoria

| Check | Resultado |
|---|---|
| `meta description` | ✔ 1 |
| `meta robots` | ✔ 1 |
| `og:` count | ✔ 10 (mínimo 8) |
| `twitter:` count | ✔ 4 |
| JSON-LD | ✔ parseia (Organization + WebPage + Event) |
| `canonical` | ✔ 1 |
| Favicon `logo-icon.png` | ✔ referenciado |
| Em-dash no HTML | ✔ 0 |
| Logo href (`/`) | ✔ 0 (aponta para elife.com.br) |
| GTM | ✔ ausente (tracking.json null para Elife) |
| Skip-link | ✔ presente |
| prefers-reduced-motion | ✔ presente |
| min-height: 0 em img grid | ✔ 2 ocorrências |
| H1 literal da copy | ✔ match exato |
| hreflang | ✔ LP única, sem variantes de idioma |

---

## Melhorias opcionais (2)

- [ ] **OG image ausente** — `landing-pages/elife/consumidores-sinteticos-evento/assets/og-consumidores-sinteticos-evento.png` não existe (o `og:image` do HTML ainda aponta pro path legado `/assets/og-image.png` na raiz do domínio — corrigir junto). Gerar template 1200×630 com headline da LP antes de publicar (WhatsApp/LinkedIn ficam sem preview rico). Não é bloqueante para deploy interno.
- [ ] **Placeholders não preenchidos** — `[LOCAL]`, `[DATA]`, `[HORÁRIO]` aparecem em 3 seções (hero ticket, seção evento, CTA final). Preencher em `copy.txt` + rodar `/lp-gerar elife consumidores-sinteticos-evento` antes de publicar para o público.
- [ ] **JSON-LD com domínio errado** — linha 45 do `index.html` declara `Organization.logo: https://content.cxpress.io/...` e `WebPage.@id/url` + `Event.url` apontam para `content.cxpress.io`. Provavelmente copy-paste de uma LP Cxpress. Trocar para o domínio definitivo da Elife (`content.elife.com` reservado por memory `reference_lp_domains.md`) antes de publicar.

---

## Nice-to-haves (2)

- [ ] **Seção de speakers/palestrantes** — a copy não tem essa seção (correto por GUIDELINES §9), mas se o evento tiver nomes confirmados, considerar adicionar para aumentar conversão.
- [ ] **Contador de vagas** — um badge dinâmico ou estático de "X vagas restantes" na seção de inscrição reforçaria a urgência sem alterar a copy existente.

---

## Próximos passos

1. Preencher `[LOCAL]`, `[DATA]`, `[HORÁRIO]` em `copy.txt`
2. Rodar `/lp-gerar elife consumidores-sinteticos-evento` (ou editar direto no HTML)
3. Corrigir domínio do JSON-LD (`cxpress.io` → domínio Elife definitivo)
4. Quando tiver snippet de form: `/lp-integrar-form elife/consumidores-sinteticos-evento "<snippet>"`
5. Publicar: `/lp-publicar elife consumidores-sinteticos-evento [dominio]`
