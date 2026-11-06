# Form Cxpress BR v9-limpo-enviar (Leadpages)

**Publicado em 2026-11-06 (Bruno)** nas 7 LPs Cxpress BR da Leadpages: chatbot-de-atendimento, chatbot-whatsapp, escolha-a-cxpress, help-desk, sistema-de-atendimento, sistema-de-chamados, whatsapp-business.

- Arquivo: `form-cxpress-v9-limpo-enviar.js` = form v9 de produção (Jotform 261034073026647, revisão 748505cdcb1) + bloco `<style id="cx-form-limpo">` dentro do iframe, o mesmo layout da LP app-whatsapp. Fora desse bloco o conteúdo é idêntico ao v9 (comparado por código): mesmo envio (`submit.jotform.com/submit/261034073026647`), mesmos campos, mesmos campos ocultos de UTM/gclid/fbclid, mesmo carregador.
- Texto do botão mantido em **"Enviar"** (para não mexer na conversão). Botão passa a ser navy `#232960` nas 6 páginas que tinham verde-azulado.
- Biblioteca: `/api/library/oulth0sddlh71in65bvnlk6p` (cópia conferida byte a byte com este arquivo).
- `teste.html`: página mínima para testar localmente (`python -m http.server` nesta pasta, abrir com `?utm_source=...`).

## Conferido no ar (promo.cxpress.io, 1440 e 390 px)

Nas 7: form novo carregado, botão "Enviar", envio para o Jotform 261034073026647, UTMs e gclid da URL nos campos ocultos, GA4 + Google Ads + LinkedIn + Meta disparando, sem rolagem horizontal. O erro de console `fbq is not defined` em chatbot-de-atendimento, chatbot-whatsapp, escolha-a-cxpress e whatsapp-business é anterior (tags gravadas no HTML dessas 4, a "fase A" ainda pendente nelas) e não tem relação com o form.

## Como reverter (só o visual volta)

Em cada página, `edit_page_draft` trocando o `src` do script e `publish_page_draft`:
- chatbot-whatsapp, escolha-a-cxpress, help-desk, sistema-de-atendimento, sistema-de-chamados, whatsapp-business: `/api/library/oulth0sddlh71in65bvnlk6p` → `/api/library/jd1vu4lpa8aq84zhyzd81ee1` (v9)
- chatbot-de-atendimento: `/api/library/oulth0sddlh71in65bvnlk6p` → `/api/pages/chatbot-de-atendimento/assets/ah5xeevaxyyn3eauhe9xhjjw` (v9 variante botão navy)
