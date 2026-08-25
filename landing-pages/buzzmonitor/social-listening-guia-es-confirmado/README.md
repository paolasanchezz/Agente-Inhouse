# LP Buzzmonitor — social-listening-guia-es-confirmado

Thanks page da LP `social-listening-guia-es`: entrega el link de la guía + CTA de conversión comercial.

**Gerado em:** 2026-08-25
**Página mãe:** `landing-pages/buzzmonitor/social-listening-guia-es/` (publicar sempre em batch)

## Estrutura

- HERO (icone check + eyebrow "GUÍA LISTA" + H1 + sub + CTA "Descargar la guía")
- CTA COMERCIAL (fundo gradiente roxo→laranja, H2 + BODY + CTA "Conocer Buzzmonitor" com UTM)
- FOOTER (5 redes sociais + link do site + copyright)

## Links e UTM

- **Descargar la guía** → `https://app.notion.com/p/3c63934026fd81f5b0a4fc0e507ac58a` (playbook público no Notion). **PENDENTE:** a página ainda não foi compartilhada publicamente — alguém do time precisa ativar "compartir en la web" no Notion antes de publicar esta LP.
- **Conocer Buzzmonitor** → `https://content.buzzmonitor.com/ia-para-social-listening-es?utm_source=material&utm_medium=thank_you_page&utm_campaign=social-listening-guia&utm_content=cta-comercial`

## Configuração pendente (fora do repo)

- **Thank You URL do Jotform:** configurar no builder do form (jotform.com, form `262355185955871`) para redirecionar para esta página após o envio: `https://material.buzzmonitor.com/social-listening-guia-es-confirmado`. Isso é feito na plataforma do Jotform, não no código.

## Estado

- [x] HTML gerado
- [ ] Publicado — adicionar ao manifesto `landing-pages/dominios/material-buzzmonitor-com/manifest.json` junto com a LP-mãe
- [ ] Notion do playbook compartilhado publicamente (bloqueador do CTA "Descargar la guía")
- [ ] Thank You URL configurada no Jotform

## Exceções deliberadas às GUIDELINES (precedente: estudo-diversidade-2026-obrigado)

- **`noindex, follow`**: página pós-ação.
- **Sem OG completo, sem JSON-LD**: ninguém compartilha esta URL.
- **Sem estrutura mínima de LP** (§6): não há form/captação aqui, é entrega + CTA.

## Notas

- GTM injetado: `GTM-MKQBX2MG` (região LATAM), mesmo container da LP-mãe.
- Slug termina em `-confirmado`, não em `-es` — a cascata de detecção de região por sufixo do slug cai no fallback `brasil`; por isso o `<html lang>` e o GTM foram fixados manualmente como `es-419` / `GTM-MKQBX2MG` (mesma lógica da LP-mãe).
