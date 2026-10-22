# LP · perpetuo-monitoramento-vsl-pt (par captura + tks) · PT-PT

Versão PT-PT do par [`perpetuo-monitoramento-vsl`](../perpetuo-monitoramento-vsl/README.md):
**webinar perpétuo on-demand (VSL)**, a pessoa preenche e assiste na hora, com o vídeo gravado na
thank-you. Pedido da Catharina em 2026-10-19.

| Página | Slug | Papel | robots |
|---|---|---|---|
| Captura | `perpetuo-monitoramento-vsl-pt` | hero + Jotform "preencha e assista" + "o que vai aprender" + speaker + autoridade | noindex |
| Thank-you | `perpetuo-monitoramento-vsl-pt-confirmado` | vídeo embedado + CTA "Pedir demonstração gratuita" | noindex |

**Origem:**
- **Captura:** duplicada da `perpetuo-monitoramento-concorrentes-pt` na versão on-demand (commit
  `f59655a`, 2026-08-25, antes de virar webinar ao vivo em 2026-09-04). Copy PT-PT já revista
  naquela versão. O form mock deu lugar ao Jotform compartilhado, igual ao par BR.
- **Thank-you:** molde da `perpetuo-monitoramento-vsl-confirmado` (BR), com a mesma copy traduzida
  para PT-PT via `/traduzir` (`traducao/entregas/2026-10/tks-perpetuo-monitoramento-vsl-pt-pt.md`
  + log de revisão).

**Fluxo:** captura (Jotform `261127236463050` "Webinars Portugal", com `data-perpetuo-next="/perpetuo-monitoramento-vsl-pt-confirmado"`)
→ a LP grava o destino em `sessionStorage` **e** no cookie `bm_next` (`.buzzmonitor.com`, 30 min)
→ o Jotform aterrissa em `content.buzzmonitor.com/obrigado-pt`, que lê o cookie e encaminha para
`/perpetuo-monitoramento-vsl-pt-confirmado`. Pré-requisito: Thank You Page do form apontando para
`https://content.buzzmonitor.com/obrigado-pt` (ver README da `obrigado-pt`).
Detalhes em [`GUIA-webinar-perpetuo-destino.md`](../../GUIA-webinar-perpetuo-destino.md).

**Vídeo:** o mesmo do par BR, `https://www.youtube.com/watch?v=fG4KpFnwbb4` (embed `www.youtube.com/embed/fG4KpFnwbb4`).

**Destinos: nada aponta para buzzmonitor.com** (regra das LPs PT, decisão do Victor 2026-09-04).
CTA do header, CTA final, logos e link "Saber mais" do rodapé, nas duas páginas:

```
https://content.buzzmonitor.com/monitoramento-manual-pt?utm_source=webinar-perp&utm_content=perpetuo-monitoramento-vsl-pt
```

UTMs no mesmo padrão do par BR (`utm_source=webinar-perp` + `utm_content` = slug da LP).

**GTM:** `GTM-NCFT22CW` (contentor PT, igual à LP PT-mãe). **OG:** reusa
`og-perpetuo-monitoramento-concorrentes.png` do par BR. **Speaker:** Victor Gurgel.

## Pendências

- **Jotform PT-PT:** desde 2026-10-22 a captura usa o "Webinars Portugal" (`261127236463050`,
  rótulos PT-PT, ex: "Apelido"), no lugar do compartilhado BR (`261904654263661`).
- **Vídeo:** gravação em PT-BR. Trocar o embed se houver gravação PT-PT.
- **Flip `index`** quando for a versão final (hoje `noindex`).
- **Testar no ar:** preencher o form, confirmar que caiu no vídeo certo e que o lead entrou no Jotform.

**Form provider:** Jotform — troca para `261127236463050` "Webinars Portugal" (2026-10-22)
