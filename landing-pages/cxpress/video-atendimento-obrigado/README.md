# LP Cxpress — video-atendimento-obrigado

Thanks page da LP `video-atendimento`: entrega o vídeo embedado imediatamente após o envio do form (sem e-mail, sem etapas extras) + CTA de conversa com a Cxpress no WhatsApp.

**Gerado em:** 2026-07-29
**Copy-fonte:** `copy.txt` (output de /lp-preparar)
**Página mãe:** `landing-pages/cxpress/video-atendimento/` (publicar sempre em batch)

## Estrutura

- VIDEO (eyebrow "Vídeo liberado" + H1 + embed YouTube 16:9)
- CTA FINAL (linha de apoio + CTA "Agende uma demonstração gratuita" → WhatsApp). Sem H2, por decisão da Marielle
- FOOTER

## Vídeo

- YouTube `dfxipCR2vTo` via `https://www.youtube.com/embed/dfxipCR2vTo?rel=0` (carrega no load, sem gate adicional).

## Estado

- [x] HTML gerado
- [x] Revisão — ver `REVISAO.md`
- [x] **Publicado** em 2026-07-31 via **CI** — https://content.cxpress.io/video-atendimento-obrigado (listada em `landing-pages/dominios/content-cxpress-io/manifest.json`)
- [x] **CTA de WhatsApp ativo** desde 2026-08-03: `https://wa.me/551150395028` com mensagem pré-preenchida, CTA "Agende uma demonstração gratuita", abrindo em nova aba. Número e texto informados pela Marielle. A seção chegou a ser removida no mesmo dia (o botão estava com `href="#"` por falta do número) e foi reposta com o link real.

## Exceções deliberadas às GUIDELINES (precedente: conheca-a-cxpress-confirmado)

- **`noindex, follow`** (exceção ao §15): página pós-ação; o Lighthouse SEO do lp-publicar vai apontar "is-crawlable" como falha — esperado, não "consertar".
- **Sem OG image, sem og/twitter/JSON-LD e sem placeholders `{{DOMAIN}}`**: ninguém compartilha esta URL; validação do lp-publicar é condicional.
- **Sem estrutura mínima de LP** (§6): não há form nem captação aqui.

## Atenção no deploy (CSP)

O embed usa `https://www.youtube.com`, já coberto pelo `frame-src` do CSP em `landing-pages/dominios/content-cxpress-io/vercel.json` (o CSP do guarda-chuva vive no repo desde a migração pro CI). Se o iframe aparecer vazio no live, é a primeira coisa a conferir. **Não troque para `youtube-nocookie.com` sem adicionar o domínio ao `frame-src` no mesmo PR** — o iframe fica em branco e o path do CSP é protegido (exige revisão do Victor).

## Notas

- GTM injetado: `GTM-T4XDWHL3` (região brasil).

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
