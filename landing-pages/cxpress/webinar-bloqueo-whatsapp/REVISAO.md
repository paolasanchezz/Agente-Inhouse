# Revisao LP — cxpress/webinar-bloqueo-whatsapp

**Data:** 2026-08-10
**Auditores:** auditoria manual (fidelidade de copy + GTM + SEO + GUIDELINES), mesmo checklist aplicado as LPs Buzzmonitor desta sessao

## Auditorias que passaram sem achados

- **Fidelidade de copy:** todo texto visivel (overline, H1, SUB, "10 minutos", CTA x3, 3x H3/BODY/LABEL de "Lo que vas a ver", H2 + 3 stats de Resultados, bio + tags de Laura, 4x LIST ITEM de "Para quien es", H2/BODY/labels do CTA final) bate literal com `copy.txt`, conferido via `get_page_text` do preview. Os 3 stats de Resultados foram divididos visualmente em numero+label sem alterar nenhuma palavra (concatenacao reconstroi a frase original).
- **Anti-IA:** em-dash 0 (1 ocorrencia encontrada num comentario CSS, nao em copy publica, mesmo assim corrigida por padronizacao). Ellipsis: 1 ocorrencia ("si&hellip;"), corretamente `&hellip;`.
- **GTM:** `GTM-WRQ47B9R` presente 2/2 (head + noscript) — validado tambem por `check_gtm_region.py` (1 OK, 0 avisos).
- **SEO:** 1 meta description, 14 tags `og:`/`twitter:`, JSON-LD com 3 nos (Organization + WebPage + SoftwareApplication, mesmo padrao do modelo de referencia `primer-listening-5-pasos`), 1 canonical.
- **Logos:** header/footer usam `brand/cxpress/assets/logos/logo-primary.svg` e `logo-reversed.svg` (confirmados existentes no repo antes de referenciar).
- **GUIDELINES §16 (hreflang):** omitido corretamente, sem LP-irma noutro idioma.
- **GUIDELINES §14 (`min-height:0`):** presente no `<img>` da foto da Laura (herdado do bloco `.speaker-photo-frame img`).
- **Acessibilidade:** skip-link, `:focus-visible`, alt descritivo na foto da Laura, decorativos (`decor-*`, `speaker-photo-decor`, icones de check, elementos internos do mockup) marcados `aria-hidden`, `prefers-reduced-motion` coberto globalmente. O mockup ilustrativo usa `role="img"` + `aria-label` descritivo no container (colapsa a subarvore pra leitores de tela, evitando duplicar o texto "Cuenta suspendida" que ja e visivel/real).
- **Marca cruzada (branding Cxpress aplicado a um layout Buzzmonitor):** cores, fontes e sombras trocadas 1:1 pelos tokens de `brand/cxpress/tokens.json`; nenhum residuo visual de Buzzmonitor (nem cor, nem fonte, nem classe CSS com nome de marca) ficou no HTML final.

## Decisao de design registrada (nao e "critico", e escolha deliberada)

- **CTA longo sem uppercase/nowrap:** o `.btn` e `.header-cta` compartilhados normalmente usam `text-transform: uppercase` + `white-space: nowrap`, adequados a CTAs curtos (2-4 palavras) das outras LPs. Como a copy desta LP trouxe um CTA de frase completa ("¡Inscríbete y aprende cómo evitar que bloqueen tu WhatsApp!"), essas duas regras foram sobrescritas *so nesta pagina* (`text-transform: none`, `white-space: normal`) pra manter o texto literal sem cortar nem forcar leitura em caixa alta. Nao afeta nenhuma outra LP (CSS inline por pagina).
- **Ilustracao "WhatsApp bloqueado" em vez de screenshot real:** ver `README.md` item 4 — decisao de compliance (marca registrada/direitos autorais), nao uma limitacao tecnica.

## Verificacao de assets (preview local)

- `./assets/laura-rodriguez.jpg` presente na pasta, verificado visualmente antes de referenciar no HTML.
- Layout do hero conferido via JS no preview: `.blocked-mockup` (420×202px) empilhado sobre `.hero-form` (420×479px) com 22px de gap, sem sobreposicao.
- Logos `brand/cxpress/assets/logos/*.svg` nao carregaram no preview `file://` local (limitacao conhecida da ferramenta de preview pra arquivos fora de um servidor real — mesma limitacao ja documentada nas LPs anteriores desta sessao). Confirmacao definitiva via HTTP real apos o deploy CI.

## Proximos passos

- CTA ainda e mock (`href="#form"`, formulario local sem backend) — quando tiver o link real de inscricao, rodar `/lp-integrar-form cxpress/webinar-bloqueo-whatsapp "snippet"`.
- Publicar: `content.cxpress.io` esta no fluxo CI — adicionar ao manifest + abrir PR.

## Segunda passada (2026-08-11, pos-publicacao — Meta Pixel)

Usuario perguntou se a LP tinha o Pixel LATAM correto (`1484678896147110`) depois de ja publicada. Confirmado que nao tinha nenhum Pixel (so GTM). Adicionado o snippet oficial (script `fbq('init', ...)` + `fbq('track', 'PageView')` + `<noscript>` de fallback), copiado literal de `atencion-clinicas-latam/index.html` (LP que ja usa esse mesmo ID), posicionado logo apos o bloco GTM no `<head>`.

- Revalidado: em-dash 0, GTM 2/2, pixel `fbq('init'` 1x.
- Nenhuma outra secao do HTML foi tocada.
