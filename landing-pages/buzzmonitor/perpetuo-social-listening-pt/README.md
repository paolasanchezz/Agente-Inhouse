# LP · perpetuo-social-listening-pt (par captura + tks) · PT-PT

Versão PT-PT do par [`perpetuo-social-listening`](../perpetuo-social-listening/README.md): **webinar perpétuo on-demand**, a pessoa preenche e
assiste na hora, com o vídeo gravado na thank-you. Pedido da Catharina em 2026-10-23 (para os anúncios
de Meta Ads em Portugal). Duplicado 1:1 do par BR, só o idioma e as integrações mudam. Molde das
integrações: `perpetuo-monitoramento-vsl-pt`.

| Página | Slug | robots |
|---|---|---|
| Captura | `perpetuo-social-listening-pt` | noindex |
| Thank-you | `perpetuo-social-listening-pt-confirmado` | noindex |

**Título:** O seu primeiro listening em 5 passos. **Speaker:** Leandra Lira. **Vídeo:** o mesmo do par BR (`youtube.com/embed/fflNMhqjr48`), sem legendas PT-PT.

**Fluxo:** captura (Jotform `261127236463050` "Webinars Portugal", com
`data-perpetuo-next="/perpetuo-social-listening-pt-confirmado"`) → a LP grava o destino em `sessionStorage` **e** no cookie
`bm_next` (`.buzzmonitor.com`, 30 min) → o Jotform aterrissa em `content.buzzmonitor.com/obrigado-pt`,
que lê o cookie e encaminha para `/perpetuo-social-listening-pt-confirmado`. A tks PT nao leva o despachante (§2.2 do guia): o form PT nao aterrissa nela.
Detalhes em [`GUIA-webinar-perpetuo-destino.md`](../../GUIA-webinar-perpetuo-destino.md).

**Destinos: nada aponta para buzzmonitor.com** (regra das LPs PT, Victor 2026-09-04). Logo, CTA e rodapé:
`https://content.buzzmonitor.com/monitoramento-manual-pt?utm_source=webinar-perp&utm_content=perpetuo-social-listening-pt`.

**GTM:** `GTM-NCFT22CW` (contentor PT). **OG:** reusa a imagem do par BR.

**PT-PT:** `conhecimento/linguistico/pt-portugal/padrao-linguistico.md` (equipa, utilizadores, captura de
ecrã, folha de cálculo, "a funcionar", "o seu/a sua", "connosco") + `regras-anti-ia.md` (0 em-dash).

## Pendências

- Mesmas do par BR (números/marcas a confirmar; link de WhatsApp).
- **Testar no ar:** preencher o form, confirmar que caiu no vídeo certo e que o lead entrou no Jotform PT.
