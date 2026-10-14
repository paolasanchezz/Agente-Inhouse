# LP · perpetuo-monitoramento-vsl (par captura + tks)

Par de páginas de **webinar perpétuo on-demand (VSL)**: a pessoa preenche e assiste na hora, com o
vídeo gravado na thank-you. Duplicado do par `perpetuo-monitoramento-concorrentes` (que hoje é
**ao vivo**, série ClickMeeting 18043) a partir da versão on-demand dele (commit `294d119`,
anterior a 2026-09-02). A tks segue o molde da `perpetuo-case-youse-confirmado`.

| Página | Slug | Papel | robots |
|---|---|---|---|
| Captura | `perpetuo-monitoramento-vsl` | hero + Jotform "preencha e assista" + "o que você vai aprender" + speaker + autoridade | noindex |
| Thank-you | `perpetuo-monitoramento-vsl-confirmado` | vídeo embedado + CTA "Agendar demo gratuita" | noindex |

**Fluxo:** captura (Jotform compartilhado `261904654263661`, com `data-perpetuo-next="/perpetuo-monitoramento-vsl-confirmado"`)
→ o Jotform aterrissa na tks da `perpetuo-social-listening`, cujo despachante lê o `sessionStorage`
e encaminha pra `/perpetuo-monitoramento-vsl-confirmado`. Nada a configurar no painel do Jotform.
Detalhes em [`GUIA-webinar-perpetuo-destino.md`](../../GUIA-webinar-perpetuo-destino.md).

**Vídeo:** `https://www.youtube.com/watch?v=fG4KpFnwbb4` (embed `www.youtube.com/embed/fG4KpFnwbb4` —
youtube.com, não nocookie: o CSP do guarda-chuva só libera `www.youtube.com`).

**CTA da tks (header + bloco final):** "Agendar demo gratuita" →
`https://content.buzzmonitor.com/monitoramento-com-ia?utm_source=webinar-perp&utm_content=perpetuo-monitoramento-vsl`
(UTMs definidas pela Catharina em 2026-10-14).

**OG:** reusa `og-perpetuo-monitoramento-concorrentes.png` da LP-mãe (mesma headline do tema).
**Speaker:** Victor Gurgel (foto copiada da LP-mãe).

## Pendências

- **Flip `index`** quando for a versão final (hoje `noindex`, igual à LP-mãe).
- **Testar no ar:** preencher o form, confirmar que caiu no vídeo certo e que o lead entrou no Jotform.
