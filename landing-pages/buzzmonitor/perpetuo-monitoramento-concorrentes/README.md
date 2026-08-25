# LP · perpetuo-monitoramento-concorrentes (par captura + tks)

Par de páginas de **webinar perpétuo**, clonado do par `perpetuo-social-listening` e adaptado pro tema de **monitoramento de concorrente**. A captura leva à thank-you, onde o vídeo do webinar fica embedado.

| Página | Slug | Papel | robots |
|---|---|---|---|
| Captura | `perpetuo-monitoramento-concorrentes` | hero + form "preencha e assista" + "o que você vai aprender" + autoridade | noindex |
| Thank-you | `perpetuo-monitoramento-concorrentes-confirmado` | vídeo embedado + CTA "fale com especialista" | noindex |

**Fluxo:** captura (form mock) → submit redireciona pra `/perpetuo-monitoramento-concorrentes-confirmado` → assiste ao vídeo → CTA final leva pra `content.buzzmonitor.com/monitoramento-com-ia`.

**Vídeo:** `https://www.youtube.com/watch?v=fG4KpFnwbb4` (embed `www.youtube.com/embed/fG4KpFnwbb4`). **Usar youtube.com, NÃO youtube-nocookie** — o CSP do guarda-chuva webinar.buzzmonitor.com só libera `www.youtube.com` no `frame-src` (o nocookie é bloqueado e o vídeo não aparece).

## Fonte da copy (2026-08-12)

Briefing da Catharina: título "como construir um monitoramento de concorrentes", promessa "montar um monitoramento de concorrente que avisa antes do cliente avisar", e o objetivo do webinar (criar tema dedicado ao concorrente com variações de grafia, comparar marca x concorrente num dashboard de benchmarking competitivo, configurar AI Insights + Buzz Pills pra avisar quando o concorrente se mexer). Cards em **nível teaser** (sem catálogo de feature), igual ao par social-listening. Sem stat inventada.

## Pendências antes de finalizar

- **Link do WhatsApp (header):** o CTA do header da tks ("Falar com especialista") ainda está com temp `https://buzzmonitor.com/`. Trocar pelo link real quando a Catharina mandar. O CTA final já foi trocado (2026-08-25) pra `content.buzzmonitor.com/monitoramento-com-ia`.
- **Form real:** a captura ainda é MOCK (redireciona no submit).
- **OG dedicada:** hoje reusa `og-primeiro-listening-5-passos.png` (do par irmão). Trocar por uma de concorrente.
- **Dados de autoridade (Victor):** confirmar números (1.000+/300+/500+/10mil) e uso das marcas.
- **Flip `index`** quando for a versão final (hoje `noindex` de review).

## Construção

Captura **dark premium**; tks **clara** (fundo branco). Anti-IA aplicado (0 em-dash, "a Buzzmonitor" feminino). Publicar via fluxo CI: worktree a partir da main + entrada no manifesto + PR pela web (sem `gh` nesta máquina; o merge-bot auto-mergeia conteúdo).
