# LP Buzzmonitor — agencias-es (ex-plataforma-integral-agencias, renomeada 2026-08-12 a pedido do Victor)

**Gerado em:** 2026-08-12
**Copy-fonte:** `copy.txt` (réplica literal de https://contenido.getbuzzmonitor.com/agencias, estruturada via /lp-preparar)
**Design base:** `landing-pages/buzzmonitor/plataforma-integral-social-media` (mesmo design system: paleta orange/pink/ink, Inter, gradient-text, reveal, quote-cards, logo marquee)
**Região/idioma:** LATAM · es-419 (slug com sufixo `-es` resolve latam na cascata; confirmado pelo gate de CI)
**GTM:** GTM-MKQBX2MG (latam, tracking.json) + Meta Pixel 935436740448328 (mesmo par da LP design base, mesmo domínio)

## Estrutura (v3, 2026-08-31)

Racional dos cortes em `REVISAO.md` e no cabecalho do `copy.txt`.

1. HERO (H1 "Tus clientes no cancelan por precio." + H2 + H3 + CTA + **video** `social-listening-es.mp4`)
2. Prova social imediata: "Empresas que ya confian en Buzzmonitor" (numeros + parede de logos de clientes)
3. Soluciones (3 splits com print: Monitoreo · Atencion Centralizada · Dashboards, 4 bullets cada)
   + **caixa "Redes y canales integrados"** (15 canais, 5 visiveis + "Ver mas") + CTA
4. Modulos restantes (grade de 3: Metricas · Programacion · Gestion de Crisis)
5. IA (print ai-insights + 6 cards com nomes oficiais)
6. Depoimentos (6 agencias)
7. CTA final: oferta de 14 dias + **form nativo** (replica do GreatPages)
8. Fechamento: faixa de logos de agencias ("Agencias que ya confian en Buzzmonitor")
9. Footer

### v3 — o que mudou (2026-08-31, pedido do Victor)

- **Hero**: a frase de dor deixou de ser eyebrow e virou o H1; o antigo H1 desceu pra H2 (`.hero-sub`)
  e o paragrafo virou H3 (`.hero-lead`). Sem eyebrow.
- **"Empresas que ya confian"** subiu de 7ª pra 2ª secao; a faixa de logos de agencias, que era a 2ª,
  desceu pro fim da pagina.
- **Secao "Lo que las mejores agencias hacen diferente" removida** — o argumento vive agora no hero.
- **Mobile — legibilidade do hero**: a textura de bolinhas (`.hero:before`) pintava POR CIMA da
  headline, porque pseudo-elemento posicionado pinta acima de conteudo nao posicionado. Corrigido
  com `position:relative; z-index:1` no `.hero-grid` (vale em qualquer largura) + textura menor e
  mais clara em `<=980px` (380px, opacity .6) e `<=640px` (240px, opacity .45).
- **Tipografia mobile subida pros pisos da GUIDELINES §20** (o bloco que existia na LP era de um
  sweep anterior, com valores mais baixos): corpo/lista/CTA 15-16px → **17px**, lead do hero 17 →
  **18px**, H2 do hero `clamp(23px, 2.4vw, 32px)` → `clamp(26px, 2.4vw, 32px)`, titulo de card
  18.7 → **20px**, label/caption 13 → **14px**. Desktop intacto (só o MIN dos clamps e os
  overrides de ≤640px sobem).
  Excecao tratada a parte: o CTA da navbar (`.nav .btn-primary`) — a linha do header nao tem folga
  (79 + 183 + 37 + 2×24 = 347px, exatamente a largura util), entao foi de 13 → **14px** com o
  padding caindo de 18 → 15px pra largura do botao nao crescer. Medido em 375×812:
  `scrollWidth` = `clientWidth` = 375, sem overflow novo alem do marquee (clipado por design) e
  do skip-link. QA: `check_mobile_type.py` reporta h1=38 h2=26 p=17 li=17 btn=14, menor fonte 14.
- **Caixa "Redes y canales integrados"** logo abaixo do split de Monitoreo (`.nets`): grade de
  chips com os **15 canais** que a plataforma monitora. **5 visiveis** antes do clique (WhatsApp,
  Instagram, Facebook, TikTok, YouTube) e **10 atras do botao "Ver mas"** (LinkedIn, Threads,
  Pinterest, Reddit, Bluesky, Google My Business, Google Play Store, WordPress, E-mail,
  Reclame Aqui). Racional das 5 visiveis: top de penetracao de redes na LATAM (ver `copy.txt`
  com as fontes). Os 5 tambem fecham exatamente uma linha da grade no desktop (5x3 quando aberta).
  - Icones: `./assets/plataformas/*.webp` (68x68, ~33 KB os 15 juntos), copiados da LP
    `monitoramento-com-ia`. **Subpasta de proposito:** no guarda-chuva todo asset de LP
    buzzmonitor cai em `/assets/buzzmonitor/`, e os nomes flat da LP de origem colidiriam com
    os dela. `plataformas/` isola.
  - **Progressive enhancement:** o HTML entrega os 15 canais abertos e o JS colapsa no load. Sem
    JS nada fica inacessivel. Botao com `aria-expanded` + `aria-controls`; os icones tem `alt=""`
    (decorativos) porque o nome do canal ja esta em texto ao lado.
- Paddings reajustados por causa da troca de vizinhanca: `.clients-proof` voltou a ter padding-top
  (76px, antes 0 porque colava no bloco de depoimentos), `#soluciones` perdeu o `padding-top:0`
  inline e `.logos` passou a `76px 0 86px` (antes 10px no topo, porque colava no hero).

## Estado

- [x] HTML gerado
- [x] OG image 1200×630 → `assets/og-agencias-es.png`
- [x] Validações: em-dash 0 · SEO completo (1 desc, 10 og, 4 twitter, JSON-LD parseia) · GTM gate OK (latam/MKQBX2MG)
- [x] Revisão (frontend-design review + web-design-guidelines) — 8 críticos aplicados, ver `REVISAO.md`
- [x] Formulário integrado — réplica do form GreatPages de `contenido.getbuzzmonitor.com/agencias` (2026-08-14; substituiu o Jotform `241825239057661`)

## Formulário (2026-08-14)

Jotform saiu; entrou uma réplica nativa do form GreatPages da LP original, mesmo padrão da
`la-mejor-plataforma-social-listening-es`. Contrato conferido campo a campo contra o XHR real da página:

- Endpoint: `POST https://contenido.getbuzzmonitor.com/conversion` (JSON, `keepalive`)
- `elemento`: `e_293578_1_178010771767293654` (page id **293578**)
- Obrigado: `https://contenido.getbuzzmonitor.com/muchas-gracias`
- Campos (mesmos ids e mesmos `titulo`): Nombre · E-mail Profesional · Teléfono · País · Empresa ·
  ¿Cuál es tu cargo? · ¿Qué funcionalidad te interesa más? + UTMs/GCLID/adset + Referral source /
  Dispositivo / URL. `eclid` recebe o `fbclid` da query.
- A resposta do `/conversion` é cross-origin e não expõe CORS: o lead é criado, mas o browser não lê a
  resposta. Por isso o redirect roda no `.then` **e** no `.catch` (+ timeout de 6s como rede).
- GTM: push `generate_lead` com `form_id: demo-agencias-es` antes do redirect.

## Correções visuais (2026-08-14)

- `ai-insights.png` estava esticado: os atributos `width/height` diziam 1200×750, mas o arquivo tem
  430×284. Corrigido para o tamanho real + `height:auto`/`aspect-ratio` no CSS, e `.ia-print` caiu de
  860px para 620px de largura máxima (acima disso o print embaça).
- Degradê do CTA final trocado de laranja→vermelho (`#c04a00 → #c2103c`) para uma varredura contínua
  roxo→magenta→framboesa (`#2A0140 → #4A0B54 → #7E1152 → #B81E4A`, 135°) com um brilho radial suave.
  Contraste com texto branco em todas as paradas: 17.9 / 12.6 / 10.0 / 6.3:1 (AA folgado).
- [x] Publicado em https://content.buzzmonitor.com/agencias-es (guarda-chuva CI)

## Assets referenciados

- `./assets/plataformas/*.webp` (15 icones de canais: whatsapp, instagram, facebook, tiktok,
  youtube, linkedin, threads, pinterest, reddit, bluesky, googlemybusiness, playstore,
  wordpress, email, reclameaqui) — origem: `landing-pages/buzzmonitor/monitoramento-com-ia/assets/`

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header/footer; raster base64, web-safe §19)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `./assets/social-listening-es.mp4` + `social-listening-es-poster.jpg` (hero — origem: ia-para-social-listening-es)
- `./assets/ai-insights.png`, `crises-1.png`, `crises-2.jpg`, `img-relatorios-dashboard.png` (prints — origem: ia-para-social-listening-es)
- `./assets/logos-agencias/*` e `./assets/logos-clientes/*` (origem: plataforma-integral-social-media)
- `./assets/og-agencias-es.png`

## Notas

- Sugestões de idioma/anti-IA pendentes de decisão do Victor no fim do `copy.txt` (destaque: "Monitorización" é grafia de Espanha; LATAM seria "Monitoreo" — mantido literal da LP original).
- hreflang: LP única (sem irmãs BR/PT no repo) — só canonical + x-default.
