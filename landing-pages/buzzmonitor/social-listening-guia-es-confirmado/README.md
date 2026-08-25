# LP Buzzmonitor — social-listening-guia-es-confirmado

Thanks page da LP `social-listening-guia-es`: entrega el link de la guía + CTA de conversión comercial.

**Gerado em:** 2026-08-25
**Página mãe:** `landing-pages/buzzmonitor/social-listening-guia-es/` (publicar sempre em batch)

## Estrutura

- HERO (icone check + eyebrow "GUÍA LISTA" + H1 + sub + CTA "Descargar la guía")
- CTA COMERCIAL (fundo gradiente roxo→laranja, H2 + BODY + CTA "Conocer Buzzmonitor" com UTM)
- FOOTER (5 redes sociais + link do site + copyright)

## Links e UTM

- **Descargar la guía** → `https://gamy-meerkat-e13.notion.site/Una-gu-a-para-transformar-conversaciones-en-decisiones-3c73934026fd80aaa792dc6615b41502` (página pública final do playbook, compartilhada pela Paola em 2026-08-25 — versão com imagens reais e vídeo do webinar embedado, mantida em outra área do workspace Notion: `Buzzmonitor 🇲🇽 > Campaña | Material rico Social Listening > PLAYBOOK`). Substitui a página interna de rascunho (`3c639340-26fd-81f5-b0a4-fc0e507ac58a`, em Entregas) que era usada como placeholder antes de existir a versão pública.
- **Conocer Buzzmonitor** → `https://content.buzzmonitor.com/ia-para-social-listening-es?utm_source=material&utm_medium=thank_you_page&utm_campaign=social-listening-guia&utm_content=cta-comercial`

## Configuração pendente (fora do repo)

- **Thank You URL do Jotform:** configurar no builder do form (jotform.com, form `262355185955871`) para redirecionar para esta página após o envio: `https://material.buzzmonitor.com/social-listening-guia-es-confirmado`. Isso é feito na plataforma do Jotform, não no código.

## Estado

- [x] HTML gerado
- [x] Publicado — live em `material.buzzmonitor.com/social-listening-guia-es-confirmado` (PR #360)
- [x] Notion do playbook compartilhado publicamente (link atualizado em 2026-08-25)
- [ ] Thank You URL configurada no Jotform

## Exceções deliberadas às GUIDELINES (precedente: estudo-diversidade-2026-obrigado)

- **`noindex, follow`**: página pós-ação.
- **Sem OG completo, sem JSON-LD**: ninguém compartilha esta URL.
- **Sem estrutura mínima de LP** (§6): não há form/captação aqui, é entrega + CTA.

## Notas

- GTM injetado: `GTM-MKQBX2MG` (região LATAM), mesmo container da LP-mãe.
- Slug termina em `-confirmado`, não em `-es` — a cascata de detecção de região por sufixo do slug cai no fallback `brasil`; por isso o `<html lang>` e o GTM foram fixados manualmente como `es-419` / `GTM-MKQBX2MG` (mesma lógica da LP-mãe).
