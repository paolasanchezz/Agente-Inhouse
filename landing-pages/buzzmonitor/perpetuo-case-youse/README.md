# LP · perpetuo-case-youse (par captura + tks)

Par de páginas de **webinar perpétuo** (case, BOFU), clonado do par `perpetuo-monitoramento-concorrentes` e adaptado pro **case Youse: SLA de 36h para 3h**. A captura leva à thank-you, onde o vídeo fica embedado.

| Página | Slug | Papel | robots |
|---|---|---|---|
| Captura | `perpetuo-case-youse` | hero + form "preencha e assista" + "o que você vai aprender" + autoridade | noindex |
| Thank-you | `perpetuo-case-youse-confirmado` | vídeo embedado + CTA "fale com especialista" | noindex |

**Fluxo (desde 2026-11-05):** captura (Jotform BR compartilhado `261904654263661`, com `data-perpetuo-next="/perpetuo-case-youse-confirmado"`) → o despachante da tks da `perpetuo-social-listening` encaminha pra `/perpetuo-case-youse-confirmado` → assiste ao vídeo → CTA "Agendar demo gratuita" (`content.buzzmonitor.com/monitoramento-com-ia?utm_source=webinar-perp&utm_content=perpetuo-case-youse`). Até essa data o form era mock e não gravava lead.

**Vídeo:** `https://www.youtube.com/watch?v=pv9r6IKA4fg` (embed `www.youtube.com/embed/pv9r6IKA4fg`). **Usar youtube.com, NÃO youtube-nocookie** — o CSP do guarda-chuva só libera `www.youtube.com` no `frame-src`.

## Fonte da copy (2026-08-12)

Briefing da Catharina: tema "Como a Youse cortou o SLA de 36h pra 3h (case)", estágio BOFU, fonte do case = blog Buzzmonitor, promessa "entender o que a Youse mudou no SAC ao trazer o atendimento pra dentro de casa, e o que você replica no seu time".

**Tom de case (regra da Catharina):** aposto do que a empresa faz ("a Youse, seguradora digital"); "antes" factual (SAC fora de casa, SLA 36h), **sem dramatizar**. Fatos usados (grounded nos cases antigos): SLA 36h→3h, equipe 75% menor.

## Pendências antes de finalizar

- **Confirmar dados do case (Victor):** SLA 36h→3h, equipe 75% menor, "seguradora digital" — vêm dos cases antigos; conferir.
- **CTA da tks:** saiu do temp `https://buzzmonitor.com/` pra página de demo com UTM. Se o destino certo for WhatsApp, trocar o link.
- **OG dedicada:** hoje reusa `og-primeiro-listening-5-passos.png`. Trocar por uma do case.
- **Números de autoridade (Victor):** 1.000+/300+/500+/10mil + uso das marcas.
- **Flip `index`** quando for a versão final (hoje `noindex` de review).

## Construção

Visual refeito em 2026-11-05 (referência Jitter: fundo branco, título gigante com personagens, pílulas lilás), igual aos outros 5 pares VSL. Anti-IA (0 em-dash, "a Buzzmonitor" feminino). Publicar via fluxo CI: worktree a partir da main + entrada no manifesto + PR pela web.
