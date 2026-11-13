# LP Buzzcreators — buzzcreators-early-access

**Gerado em:** 2026-11-13
**Copy-fonte:** `copy.txt` (ES-LATAM, escrita no chat com os 3 pilares carregados; Notion indisponivel na sessao)
**Tipo:** teaser ToFu de pre-lancamento LATAM (lista de espera / acesso antecipado)

## Estrutura

Versao v3 (atual):

1. Hero: H1 de dor + sub + CTA, celular animado "do caos ao orden" (+ fitas cruzadas decorativas)
2. Como funciona: 4 passos em carrossel deslizavel (mobile) / grid 2×2 (desktop), cada um com mini-interface animada
3. Para quem: tabs Agencia / Marca / Creador
4. Registro: embed Jotform 241825239057661 (`#inscripcion`)
5. Fecho: H2 + CTA
6. Footer

**Desvio de GUIDELINES §10:** o form saiu da 2a secao (ToFu) e foi pra 4a. A ordem conta a historia antes de pedir os dados; pra nao perder quem ja esta decidido, ha CTA no header, no hero e um CTA fixo no rodape do celular. Validar com o Victor (ou testar A/B contra form na 2a secao).

## Decisoes de design

> **2026-11-13 (v3): redesign "experiencia" mobile-first + copy nova** (ver `REVISAO.md`). Antes disso houve a versao clara e a "dark premium".
>
> **2026-11-13: redesign "dark premium"** a pedido do Ulises: degradê preto -> roxo como identidade da pagina, laranja so como acento. Desvia de GUIDELINES §1/§3 e do BRANDBOOK §7 (base clara) por decisao do usuario. Detalhes e contraste em `REVISAO.md`. Os itens abaixo descrevem a versao clara original e valem so no que nao conflita.

- **Paleta segue o Style Guide PDF do Ulises** ("BuzzCreators Style Guide.pdf", 3 p.): Rich Purple `#3a1652`, Violet `#6a3895`, Sundown `#ec7c29`, Border `#e2e8f0`, Background `#f8fafc`. Divergencia com `brand/buzzcreators/tokens.json` (laranja `#ff8119`) registrada pra decisao do Victor.
- **CTA laranja com texto Rich Purple** (contraste ~5:1). Branco sobre Sundown da ~2.9:1 e reprova AA.
- **Gradiente unico** (roxo -> laranja) so na borda do simbolo do hero, no traco da pausa e na faixa do CTA final.
- Overline em DM Sans Light (HK Grotesk nao esta no Google Fonts).
- Logos web-safe (§19): `logo-color.png` no header, `logo-branca-2.svg` (paths, sem `<text>`) no footer, `logo-icon-color.svg`/`logo-icon-white.svg` (paths) como simbolo.
- Sem GTM: `brand/buzzcreators/tracking.json` esta todo `null`.
- `brand-manifest.json` da marca ainda no formato antigo (`websites`, sem `regions`): home LATAM = `https://buzzcreators.com`, JSON-LD sem `sameAs`. Manifest precisa ser migrado.

## Estado

- [x] HTML gerado
- [x] Checagem manual: em-dash 0, JSON-LD valido, 10 og + 4 twitter, sem JS que grava `#`, pisos mobile ok (H1 34px, H2 28px, corpo 17-18px), sem overflow horizontal em 375px
- [x] OG image 1200×630 → `assets/og-buzzcreators-early-access.png`
- [x] Revisao formal (`/lp-revisar`, 2026-11-13) — 4 criticos aplicados, opcionais em `REVISAO.md`
- [x] Formulario integrado

**Form provider:** Jotform, form `241825239057661` via embed `jsform` (2026-11-13, a pedido do Ulises pra nao esperar o backend custom). Os campos e o texto do form vem do Jotform, nao do `copy.txt` (labels Nome/Correio/Pais/Perfil e a nota "Solo te escribiremos..." do mock sairam). Pendente no Jotform: Nome e E-mail estao como campo oculto e "Tu WhatsApp" aparece 2x. Ajustar no Jotform nao precisa de redeploy. Backend custom (form proprio -> funcao serverless -> API Jotform) segue como evolucao futura com revisao do Victor.
- [ ] Publicado — rodar `/lp-publicar buzzcreators buzzcreators-early-access [dominio]` (sugestao: `content.buzzmonitor.com`)

## Assets referenciados

- `../../brand/buzzcreators/assets/logos/logo-color.png`
- `../../brand/buzzcreators/assets/logos/logo-icon-color.svg`
- `../../brand/buzzcreators/assets/logos/logo-icon-white.svg`
- `../../brand/buzzcreators/assets/logos/logo-branca-2.svg`
- `../../brand/buzzcreators/assets/logos/logo-icon.png` (favicon)
