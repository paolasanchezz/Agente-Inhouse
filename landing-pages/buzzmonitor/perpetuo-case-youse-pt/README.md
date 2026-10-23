# LP · perpetuo-case-youse-pt (par captura + tks) · PT-PT

Versão PT-PT do par [`perpetuo-case-youse`](../perpetuo-case-youse/README.md): **webinar perpétuo on-demand**, a pessoa preenche e
assiste na hora, com o vídeo gravado na thank-you. Pedido da Catharina em 2026-10-23 (para os anúncios
de Meta Ads em Portugal). Duplicado 1:1 do par BR, só o idioma e as integrações mudam. Molde das
integrações: `perpetuo-monitoramento-vsl-pt`.

| Página | Slug | robots |
|---|---|---|
| Captura | `perpetuo-case-youse-pt` | noindex |
| Thank-you | `perpetuo-case-youse-pt-confirmado` | noindex |

**Título:** Caso Youse: SLA de 36h para 3h. **Speaker:** Nathalia Crivellaro. **Vídeo:** o mesmo do par BR (`youtube.com/embed/pv9r6IKA4fg`), sem legendas PT-PT.

**Fluxo:** captura (Jotform `261127236463050` "Webinars Portugal", com
`data-perpetuo-next="/perpetuo-case-youse-pt-confirmado"`) → a LP grava o destino em `sessionStorage` **e** no cookie
`bm_next` (`.buzzmonitor.com`, 30 min) → o Jotform aterrissa em `content.buzzmonitor.com/obrigado-pt`,
que lê o cookie e encaminha para `/perpetuo-case-youse-pt-confirmado`. A captura BR ainda usa form **mock**; a PT ja nasce com o Jotform real.
Detalhes em [`GUIA-webinar-perpetuo-destino.md`](../../GUIA-webinar-perpetuo-destino.md).

**Destinos: nada aponta para buzzmonitor.com** (regra das LPs PT, Victor 2026-09-04). Logo, CTA e rodapé:
`https://content.buzzmonitor.com/monitoramento-manual-pt?utm_source=webinar-perp&utm_content=perpetuo-case-youse-pt`.

**GTM:** `GTM-NCFT22CW` (contentor PT). **OG:** reusa a imagem do par BR.

**PT-PT:** `conhecimento/linguistico/pt-portugal/padrao-linguistico.md` (equipa, utilizadores, captura de
ecrã, folha de cálculo, "a funcionar", "o seu/a sua", "connosco") + `regras-anti-ia.md` (0 em-dash).

## Pendências

- Mesmas do par BR (números/marcas a confirmar; link de WhatsApp).
- **Testar no ar:** preencher o form, confirmar que caiu no vídeo certo e que o lead entrou no Jotform PT.
