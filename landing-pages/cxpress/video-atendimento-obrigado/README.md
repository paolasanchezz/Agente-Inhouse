# LP Cxpress — video-atendimento-obrigado

Thanks page da LP `video-atendimento`: entrega o vídeo embedado imediatamente após o envio do form (sem e-mail, sem etapas extras) + CTA de conversa com especialista via WhatsApp.

**Gerado em:** 2026-07-29
**Copy-fonte:** `copy.txt` (output de /lp-preparar)
**Página mãe:** `landing-pages/cxpress/video-atendimento/` (publicar sempre em batch)

## Estrutura

- VIDEO (eyebrow "Vídeo liberado" + H1 + embed YouTube 16:9)
- DÚVIDAS (H2 + body + CTA "Conversar pelo WhatsApp")
- FOOTER

## Vídeo

- YouTube `dfxipCR2vTo` via `https://www.youtube.com/embed/dfxipCR2vTo?rel=0` (carrega no load, sem gate adicional).

## Estado

- [x] HTML gerado
- [x] Revisão — ver `REVISAO.md`
- [x] **Publicado** em 2026-07-31 via **CI** — https://content.cxpress.io/video-atendimento-obrigado (listada em `landing-pages/dominios/content-cxpress-io/manifest.json`)
- [ ] **PENDÊNCIA ABERTA:** trocar o `href="#"` do botão "Conversar pelo WhatsApp" pelo link `wa.me` do especialista (número não existe no repo — pedir à Marielle). Está no ar com placeholder por decisão dela; sem o form integrado, ninguém chega aqui pelo fluxo real. Trocar junto com a integração do form.

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
