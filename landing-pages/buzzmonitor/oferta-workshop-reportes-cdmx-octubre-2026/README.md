# LP Buzzmonitor — oferta-workshop-reportes-cdmx-octubre-2026

> **Copia creada em 2026-10-21** a partir de `buzzmonitor/oferta-workshop-reportes-ia-bogota`, para o workshop de reportes com IA em Cidade do Mexico (28/10). Mudou so o slug e a data limite da oferta (6 de novembro); copy, form (Jotform 241825239057661), hero e OG sao os da LP de Bogota.

> **Copia creada em 2026-09-28** a partir de `buzzmonitor/oferta-webinar-gestion-crisis-ia-septiembre-26`, para o workshop de reportes com IA em Bogota. Copy, form, hero e dominio ainda sao os da LP original — pendentes de adaptacao. `REVISAO.md` e o historico da LP original.

**Gerado em:** 2026-09-21 · **Restyle sobre o criativo do webinar:** 2026-09-21
**Copy-fonte:** `copy.txt` (output de /lp-preparar)
**Idioma / regiao:** ES-LATAM (`es-419`) · GTM `GTM-MKQBX2MG`
**Dominio destino:** `webinar.buzzmonitor.com` (guarda-chuva, migrado pro CI)
**Contexto:** redesenho completo da LP legada `contenido.getbuzzmonitor.com/oferta-webinar-monitoreo-competidores-con-ia` (GreatPages), com a oferta readaptada para a edicao de setembro/2026 do webinar "Gestión de Crisis con IA". LP irma de captacao: `buzzmonitor/gestion-crisis` (mesma familia tipografica). Equivalente PT-BR: `buzzmonitor/gestao-de-crises-ia-agosto-2026-oferta`.

## Estrutura

- HERO (badge + H1 + lead + CTA; a direita, imagem do painel de atividade da concorrencia com lupa, fornecida pelo usuario)
- OFERTA (fundo roxo solido, "15 días gratis de Buzzmonitor" em display, 3 cards com stagger, bonus do desconto, pilula de validade, CTA)
- CONSECUENCIA (lista vertical com X vermelho, 3 itens, frase-ancora grande, CTA ghost)
- BENEFICIOS (grid de 5 cards com borda-topo e check)
- MODULOS (4 blocos flat em 2x2, Social Listening primeiro)
- PRUEBA SOCIAL (fundo roxo, 4 metricas com count-up)
- CLIENTES (mural de logos em slideshow crossfade 16s)
- URGENCIA (fundo roxo escuro, selo amarelo rotacionado -3deg, CTA)
- CTA FINAL / form mock (`id="form-section"`, gradiente com scrim, 2 colunas, 7 campos)
- FOOTER

## Design

**Direcao visual: derivada do criativo do webinar "Gestión de Crisis con IA" (24/set)**, enviado pelo Victor em 2026-09-21. Elementos traduzidos do criativo pra LP:

- **Fundo creme** (`#FBF6F1`, alternando com branco e `#F4ECE4`) no lugar do cinza off-white. E o fundo do criativo.
- **Trama de pontos (halftone)** em coral, como textura decorativa nos cantos de hero, oferta, beneficios, prova social e urgencia. Puro CSS (`radial-gradient` + `mask`), sem imagem. Escondida no mobile.
- **Tipografia display preta** (`#131313`) com a frase-chave em coral, exatamente como "Crisis" aparece no criativo.
- **Pills roxas** com sombra solida deslocada em coral (`box-shadow: 6px 6px 0`) no badge do hero e no selo de urgencia. E o tratamento de "WEBINAR GRATUITO" e "SPEAKERS" do criativo.
- **Eyebrows como pilula coral** com texto branco, no lugar do texto colorido solto (padrao "SPEAKER" do criativo).
- **Icones de linha dentro de circulo** (stroke fino, `currentColor`) no lugar dos icones chapados, como os icones de radar/escudo/balao do criativo.
- **Aneis concentricos tipo radar** no painel do hero, com blip coral. Motivo do radar do criativo, e tematicamente exato pra deteccao de crise.
- **Cantos mais arredondados** (20px em cards, 28px em paineis).

- Fontes: League Spartan (headings) + Lato (corpo), via Google Fonts. Mesma dupla da LP irma `gestion-crisis`.
- Paleta: roxo `#390155` + coral `#DE2451` + laranja `#EB7C2E`, sobre creme e branco. Um unico gradiente, o **gradiente 3 do brand** (`tokens.json`: coral -> laranja), usado em 3 pontos: texto display da oferta, regua do painel do hero e fundo do CTA final (este com scrim escuro pra garantir AA).
- CTA primario em **roxo com texto branco** (16:1), hover coral. Decisao tomada por acessibilidade e por fidelidade ao criativo, que usa pills roxas. Ver `REVISAO.md`.
- Animacao: IntersectionObserver com stagger via `data-delay`, count-up nas metricas (com restauracao forcada do valor literal em 2.2s), crossfade no mural. Fallback `<noscript>`, safety-net de 3s e `prefers-reduced-motion` respeitado.
- Icones desenhados em SVG inline (sem CDN de icones).

## Estado

- [x] Copy preparada (`/lp-preparar`) — ES-LATAM, revisao anti-IA sem achados
- [x] HTML gerado (`/lp-gerar` + `frontend-design`)
- [x] Pisos tipograficos mobile aplicados (`bump_mobile_type.py`, GUIDELINES §20)
- [x] Revisao (`/lp-revisar`) — 8 criticos aplicados, ver `REVISAO.md`
- [x] Restyle sobre o criativo do webinar (2026-09-21) + revalidacao completa de AA, overflow e fidelidade de copy
- [x] Data limite da oferta definida (30 de setembro) (2026-09-21)
- [x] Visual do hero: imagem fornecida pelo usuario no lugar do grafico SVG (2026-09-21)
- [x] OG image 1200×630 → `assets/og-oferta-workshop-reportes-cdmx-octubre-2026.png`
- [x] Formulario integrado — Jotform `241825239057661` (2026-09-21, embed `jsform`)
- [ ] Publicado — via fluxo CI (manifesto `landing-pages/dominios/webinar-buzzmonitor-com/manifest.json` + PR)

**Form provider:** Jotform (2026-09-21) — form `241825239057661`, embed `jsform`.

## Pendencias de conteudo

- **Os campos do form real nao batem com os LABELs do `copy.txt`.** O `copy.txt` lista os 7 campos que estavam no mock (Nombre completo / Correo electrónico profesional / Teléfono / Empresa / País / cargo / área). O Jotform `241825239057661` pede outro conjunto: Nombre completo, E-mail Comercial, País, Empresa, "¿Usas alguna herramienta actualmente?", "Perfil de la Empresa", "Área en la que trabajas", mais um checkbox de opt-out de newsletter. Quem manda e o formulario (foi o escolhido pelo usuario); os LABELs do `copy.txt` ficaram obsoletos e estao mantidos so como registro do mock.
- **O botao do Jotform e laranja `#FF6100`, fora da paleta da LP.** Isso e tema do proprio formulario e so muda dentro do Jotform, nao pelo CSS da LP (iframe cross-origin).
- **A imagem do hero fala de concorrencia, a LP fala de crise.** O mockup na tela do notebook traz "Actividad de la competencia", "Menciones por periodo" e "Competencia A/B/C"; o arquivo de origem e de uma campanha de *monitoreo de competidores*. A LP vende *gestion de crisis*. A escolha foi do usuario e foi mantida, mas se aparecer uma peca equivalente com painel de sentimento ou de alertas, o encaixe com a copy fica mais direto.

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `./assets/hero-actividad-competencia.{webp,png}` (visual do hero; WebP 117 KB servido por `<picture>`, PNG 157 KB de fallback. Origem: `Webinar LATAM ADS  Monitoreo de competidores.png`, 1080x1080, enviado pelo usuario em 2026-09-21. Recortado no bounding box, redimensionado pra 1000 px de largura e quantizado pra 256 cores)
- `./assets/logos/mural-1.jpeg`, `./assets/logos/mural-2.jpeg` (mural de clientes, copiados de `gestao-de-crises-ia-agosto-2026-oferta` para manter a LP self-contained)
- `./assets/og-oferta-workshop-reportes-cdmx-octubre-2026.png` (OG)
