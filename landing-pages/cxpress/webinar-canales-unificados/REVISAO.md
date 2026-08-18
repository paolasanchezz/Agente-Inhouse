# Revisao LP — cxpress/webinar-canales-unificados

**Data:** 2026-08-18
**Auditores:** auditoria manual (fidelidade de copy + GTM + Pixel + SEO + GUIDELINES), mesmo checklist aplicado a `webinar-bloqueo-whatsapp`

## Auditorias que passaram sem achados

- **Fidelidade de copy:** todo texto visivel (overline, H1, SUB, "10 minutos", CTA x3, 3x H3/BODY/LABEL de "Lo que vas a ver", H2 + 3 stats de Resultados, bio + tags de Laura, 4x LIST ITEM de "Para quien es", H2/BODY/labels do CTA final) bate literal com `copy.txt`, conferido via `get_page_text` do preview.
- **Anti-IA:** em-dash 0, ellipsis 1 ocorrencia como `&hellip;` ("si&hellip;").
- **GTM:** `GTM-WRQ47B9R` presente 2/2 (head + noscript) — `check_gtm_region.py` OK.
- **Meta Pixel:** `1484678896147110` presente (script + noscript), mesmo ID confirmado pelo usuario nas LPs anteriores desta serie.
- **SEO:** 1 meta description, 14 tags `og:`/`twitter:`, JSON-LD com 3 nos (Organization + WebPage + SoftwareApplication), 1 canonical.
- **Logos:** header/footer usam `brand/cxpress/assets/logos/logo-primary.svg` e `logo-reversed.svg` (ja confirmados existentes).
- **GUIDELINES §16 (hreflang):** omitido corretamente, sem LP-irma noutro idioma.
- **GUIDELINES §14 (`min-height:0`):** presente nos `<img>` de `.hero-media-card`, `.cta-final-media` e na foto da speaker.
- **Acessibilidade:** skip-link, `:focus-visible`, alt descritivo em todas as imagens informativas (gif dos canais, mockup do laptop, foto da Laura), decorativos (`decor-*`, `speaker-photo-decor`, icones de check) marcados `aria-hidden`, `prefers-reduced-motion` coberto globalmente.
- **Uso de assets de marca (plataforma-canais.gif, mockup-plataforma-laptop.png):** sao capturas reais e ja existentes do proprio produto Cxpress (ja usadas em outras LPs como `banimento-whatsapp-latam`) — sem nenhuma questao de marca registrada de terceiros, ao contrario dos graficos de WhatsApp que existem na LP de referencia mas nao se aplicam aqui.

## Decisao de design registrada (nao e "critico", e escolha deliberada)

- **Layout hero + CTA final em 2 colunas com mockup:** o usuario pediu explicitamente pra espelhar a composicao visual da versao mais recente de `webinar-bloqueo-whatsapp` (imagem no hero + mockup no CTA final). Como os graficos daquela LP sao especificos de WhatsApp (nao aplicaveis ao tema de centralizacao de canais), a MESMA composicao foi reconstruida com assets reais e neutros da plataforma Cxpress (`plataforma-canais.gif`, `mockup-plataforma-laptop.png`) — ver `README.md` item 2 para o raciocinio completo.

## Verificacao de assets (preview local)

- Layout do hero e do CTA final conferidos visualmente no preview — grid nao quebra, sem sobreposicao.
- Imagens (`plataforma-canais.gif`, `mockup-plataforma-laptop.png`, `logo-primary.svg`, `logo-reversed.svg`, `laura-rodriguez.jpg`) nao carregaram no preview `file://` local (limitacao conhecida da ferramenta de preview pra arquivos fora de um servidor real — mesma limitacao ja documentada nas LPs anteriores desta sessao). Confirmacao definitiva via HTTP real apos o deploy CI.

## Proximos passos

- CTA ainda e mock (`href="#form"`, formulario local sem backend) — quando tiver o link real de inscricao, rodar `/lp-integrar-form cxpress/webinar-canales-unificados "snippet"`.
- Publicar: `content.cxpress.io` esta no fluxo CI — adicionar ao manifest + abrir PR.

## Segunda passada (2026-08-18, pos-publicacao — troca de imagens)

Usuario pediu trocar as duas imagens: gif dos canais (hero -> CTA final) e nova imagem de icones (CTA final não, foi pro hero). Imagem enviada (`Webinar canales.png`) localizada em Downloads pelo nome exato informado pelo usuario, verificada visualmente (fila de 6 icones: telefone, Facebook, WhatsApp, Instagram, correo, Messenger), recortada de 1920x1080 pro bounding box real (1822x272) antes de usar.

- **Consideracao de marca:** a imagem contem icones oficiais de apps de terceiros (Facebook, WhatsApp, Instagram, Messenger). Diferente do caso anterior (logo do WhatsApp tachado com sinal de proibicao, contexto negativo), aqui o uso e descritivo/nominativo — mostrar quais canais a plataforma integra, sem modificar os icones nem associa-los a conotacao negativa. Pratica comum e amplamente aceita no setor de martech/atencao ao cliente (uso factual "integra com estes canais"). Nao configura o mesmo risco do caso anterior.
- Revalidado: em-dash 0, GTM 2/2, pixel 1x, `check_gtm_region.py` OK. Nenhum texto da copy foi alterado.
- Layout conferido via JS no preview: `.hero-media-card` (340x75px) empilhado sobre `.hero-form`, sem sobreposicao.
