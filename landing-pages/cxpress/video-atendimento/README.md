# LP Cxpress — video-atendimento

Página de captura (video gate): form de 5 campos que libera vídeo exclusivo. Após o envio, o lead vai para a thanks page irmã `video-atendimento-obrigado`, onde o vídeo carrega imediatamente (sem envio por e-mail, sem etapas extras).

**Gerado em:** 2026-07-29
**Copy-fonte:** `copy.txt` (output de /lp-preparar)
**Página irmã:** `landing-pages/cxpress/video-atendimento-obrigado/` (destino do form — publicar sempre em batch)

## Estrutura

- HERO (eyebrow + H1 + frase de apoio) com form card à direita (Nome, Empresa, E-mail corporativo, Cargo, WhatsApp + CTA "Assistir agora")
- FOOTER

LP deliberadamente curta (squeeze page): a copy do briefing tem só hero + form (GUIDELINES §9 — copy dita estrutura).

## Estado

- [x] HTML gerado
- [x] Revisão (frontend-design review + web-design-guidelines) — ver `REVISAO.md`
- [x] OG image (1200×630) — `assets/og-image.png` (template em `assets/og-template.html`)
- [x] **Publicado** em 2026-07-31 via **CI** — https://content.cxpress.io/video-atendimento (guarda-chuva `content.cxpress.io`, listada em `landing-pages/dominios/content-cxpress-io/manifest.json`)
- [x] **Formulário integrado** em 2026-07-29 — Jotform, form `262104279010647` (embed `jsform`, renderiza em iframe de `form.jotform.com`)

**Form provider:** Jotform — form `262104279010647` (integrado em 2026-07-29)

> ⚠️ **O redirect para a thanks page depende de configuração no Jotform.** O embed roda num iframe de outra origem, então o JS da LP não pode interceptar o submit. Em **Configurações do form > Após o envio**, escolher *Redirecionar para link externo* e apontar para `https://content.cxpress.io/video-atendimento-obrigado`. Sem isso, o lead vê a tela de agradecimento padrão do Jotform e nunca chega ao vídeo.

**Nota sobre o embed:** a thanks page usa `www.youtube.com`, que o CSP do guarda-chuva já libera. `youtube-nocookie.com` (mais privado, sem cookie até o play) exigiria mudar `landing-pages/dominios/content-cxpress-io/vercel.json`, que é path protegido e trava o auto-merge. Decisão da Marielle em 2026-08-03: publicar com `youtube.com`. Se o nocookie virar prioridade, é 1 linha no `frame-src` do CSP + 1 no embed, num PR com revisão do Victor.

**Fluxo de atualização (CI, desde 2026-07-15):** editar o source aqui e abrir PR — o merge-bot mergeia diff de conteúdo e o `lp-deploy.yml` publica. Não existe mais sibling nem deploy local para este domínio. Antes de mexer, confirmar que o checkout está na main (`git rev-list --count HEAD..origin/main`) — branch velha carrega skill velha. Ver `landing-pages/CONTEXT.md` §2.6 e §7.2 (2026-07-31).

## Notas

- GTM injetado: `GTM-T4XDWHL3` (região brasil, `brand/cxpress/tracking.json`).
- Mock do form simula o fluxo real: valida os campos e redireciona para `video-atendimento-obrigado` (path relativo, resolve certo no deploy com cleanUrls). O `lp-integrar-form` substitui pelo embed real.
- Títulos alternativos do briefing (não usados) e sugestão de H1-dor: ver `copy.txt` e página da copy no Notion.

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
