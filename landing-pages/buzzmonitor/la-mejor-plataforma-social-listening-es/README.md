# LP Buzzmonitor — la-mejor-plataforma-social-listening-es

**Gerado em:** 2026-07-17
**Copy-fonte:** `copy.txt` (estruturada a partir da LP publicada em contenido.getbuzzmonitor.com/la-mejor-plataforma-social-listening-marketing + referência de design escolha-a-buzzmonitor.webflow.io)
**Região/idioma:** LATAM · ES-419 · destino `content.buzzmonitor.com/la-mejor-plataforma-social-listening-es` (migrada de `material.buzzmonitor.com` em 2026-07-21; path antigo faz 301)

## Estrutura

- HERO (overline + H1 + sub + 2 CTAs + 3 stats + tela da plataforma)
- LOGOS — logo wall de 10 marcas extraídas 1:1 da LP publicada (Samsung, Sony, IKEA, Sephora, Santander, Havas, TBWA, McCann, Fundación Real Madrid, Bizum). Assets em `assets/clientes/`.
- COMPARATIVO na **segunda dobra** (tabela 15 features × Buzzmonitor + 10 concorrentes; dados em `comparativo.json`, transcritos 1:1 da LP publicada) — movido pra cá a pedido do Victor, 2026-07-20
- CTA-FINAL + FORM na **terceira dobra** (embed Jotform; cabeçalho mostra preço "Planes desde 390 USD/mes")
- POR-QUE-ELEGIR (texto + checklist de 6)
- SOLO-BUZZMONITOR (lista de 6 + grid de 12 ícones de canais)
- VISION-INTEGRAL (4 cards)
- OFERTA (dark, tag rotacionada "14 días gratis"; SEM preço na versão LATAM)
- TESTIMONIOS (6 citas literais de clientes) + FOOTER

## Form (embed Jotform)

**Form provider:** Jotform (integrado em 2026-08-24) — form **241825239057661**
("Buzzmonitor LATAM_Form Proposta_v3 Conversão Remarketing"), embed `jsform`
dentro do wrapper canônico `.jotform-embed`. Mesmo form já usado na LP irmã
`plataforma-integral-social-media`.

Substituiu a réplica do form GreatPages (page id **2705735**, POST em
`https://contenido.getbuzzmonitor.com/conversion` + redirect pro `/muchas-gracias`),
que era a decisão original desta LP. O que mudou com a troca:

- **Destino do lead:** agora é o Jotform, não mais o endpoint `/conversion`.
- **Campos:** Nombre completo · E-mail Comercial · Empresa · País · Utiliza actualmente ·
  Perfil de · Área en (antes eram 5: Nombre, E-mail, Teléfono, País, Empresa).
- **UTMs:** o Jotform tem campos ocultos próprios (`utm_source`, `utm_medium`, `utm_campaign`,
  `utm_content`, `utm_term`, `url`, `gclid`, `adset`) e recebe a querystring da LP via
  `parentURL` do embed. O JS que montava os campos ocultos à mão foi removido — não recriar
  shim (ver nota da skill `lp-integrar-form`).
- **Redirect:** o pós-envio passa a ser o do próprio Jotform, não mais `/muchas-gracias`.
  Isso derruba o racional que escolheu o `GTM-PC4TJ6H` (ver Tracking abaixo).
- **dataLayer:** o push manual de `generate_lead` saiu junto com o form antigo.

O título "Agenda una demo", o subtítulo e o preço "Planes desde 390 USD/mes" foram preservados
como cabeçalho (`.form-panel`) acima do embed — sobre o gradiente, sem card branco, pra não
criar card-dentro-de-card com o card do próprio Jotform.

### Moldura branca no embed (2026-08-24)

Este Jotform vem com **fundo transparente** (`body { background-color: transparent }`), e a
seção `.final` é um gradiente escuro — sem moldura, os labels e inputs do form caem direto
sobre o roxo e ficam ilegíveis. Por isso o `.jotform-embed` aqui **é uma exceção** ao wrapper
canônico "sem card" da `lp-integrar-form`: leva `background:#fff`, `border-radius:18px`,
`padding:20px 18px` (16px/14px abaixo de 980px) e sombra suave. Enxuto de propósito — o
próprio form já tem respiro interno.

### Termly — classificação do embed (2026-08-24)

O `GTM-PC4TJ6H` carrega o resource-blocker do **Termly** com `autoBlock=on`. Ele classifica
`form.jotform.com` como `unclassified` e, quando o scan dele encontra o iframe já no DOM,
troca o `src` por `data-src` + `display:none` — o form vira o placeholder *"Enable this content?"*
até o visitante aceitar cookies. Reproduzido em 2026-08-24 (o form nativo anterior era imune,
por ser HTML próprio).

**Não é determinístico:** o Termly escaneia o DOM uma vez; bloqueia o que já existe quando roda.
Como ele entra via GTM (async) e o `jsform` cria o iframe via `document.write` durante o parse,
o resultado depende de quem chega primeiro. Em recarregamentos locais deu bloqueado uma vez e
livre nas demais.

**O que foi feito no código:** o embed é declarado como conteúdo **essencial**
(`data-categories="essential"` no `<script>` do jsform + carimbado no iframe que ele gera, via
`MutationObserver`). É o mecanismo documentado do Termly pra classificação manual, e a leitura
se sustenta: é o formulário de demo da página, não um tracker. O código **não** desbloqueia
nada que o Termly já tenha bloqueado — isso seria passar por cima do consentimento.

**Correção durável (pendente, fora do código):** classificar `form.jotform.com` no painel do
Termly. Vale pro domínio inteiro, não depende de ordem de carregamento e não precisa de deploy.
A alternativa seria migrar pro `GTM-MKQBX2MG` (container canônico de LATAM, sem Termly), mas o
Victor pediu pra manter o `PC4TJ6H`.

**Verificar no live pós-deploy:** abrir a LP numa aba anônima, sem consentimento prévio, e
confirmar que o form aparece. Se aparecer o placeholder, a saída é o painel do Termly.

## Tracking

- **GTM `GTM-PC4TJ6H`** (pedido do Victor, 2026-08-06). Substitui o `GTM-5PNK2VZ` usado de
  2026-07-17 até aqui. O racional do `5PNK2VZ` era "o mesmo container das páginas LATAM
  atuais", mas a verificação em 2026-08-06 mostrou que isso não se sustentava: `5PNK2VZ`
  estava só nas **duas** páginas GreatPages de onde estas LPs foram clonadas
  (`/ia-para-social-listening` e `/la-mejor-plataforma-social-listening-marketing`).
  O resto do parque LATAM — `getbuzzmonitor.com/es/`, as outras LPs em
  `contenido.getbuzzmonitor.com` e a página de obrigado `/muchas-gracias` — usa `PC4TJ6H`.
- O `/muchas-gracias` é o ponto crítico: é pra lá que o form redireciona. Com `5PNK2VZ` a
  jornada quebrava no meio (pageview num container, conversão em outro).
- Diverge do `tracking.json` latam (`GTM-MKQBX2MG`) → selo `.tracking.lock` com
  `grandfathered: true`, fingerprint reemitido em 2026-08-06. Decidir depois se o
  `tracking.json` muda ou se as LPs migram pro container canônico.
- CSP não precisou mudar: `PC4TJ6H` carrega do mesmo `googletagmanager.com`. Quais tags
  ele dispara (Termly, Meta Pixel, LinkedIn, GA4, Google Ads) não foi reauditado — conferir
  o console após o deploy.

- **Revisar (2026-08-24):** o argumento que sustentava o `PC4TJ6H` era o redirect pro
  `/muchas-gracias`. Com o embed Jotform esse redirect deixou de existir, e o container
  canônico da região (`GTM-MKQBX2MG`, `tracking.json`) volta a ser o candidato natural —
  com o bônus de não carregar o Termly. Decisão do Victor.

## Estado

- [x] HTML gerado
- [x] Revisao (responsivo 390/768/1440 sem overflow; SEO completo; JSON-LD parseia; imgs com alt; em-dash 0)
- [x] Formulario integrado (embed Jotform 241825239057661, ver acima)
- [ ] Publicado — manifesto + merge na main (deploy via CI `lp-deploy.yml`)

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/{logo-icon.png, logo-primary.svg, logo-reversed.svg}`
- `./assets/img-plataforma-hero.avif` + `./assets/tela-computador-bm2.png` (hero/oferta)
- `./assets/icon-*.webp` (12 canais) · `./assets/og-la-mejor-plataforma-social-listening-es.png` (1200×630)

## Pendências conhecidas

- Telas da plataforma estão com UI em PT-BR (assets enviados pelo Bruno no Drive). Trocar quando houver capturas ES.
- Teste real de submit do form pendente (gera lead de verdade — fazer 1 envio de teste pós-deploy e apagar o lead no Jotform).
- Confirmar no live, em aba anônima, se o Termly ainda bloqueia o iframe do Jotform — ver secao Termly.
- Classificar `form.jotform.com` no painel do Termly (Victor) — correção durável.
