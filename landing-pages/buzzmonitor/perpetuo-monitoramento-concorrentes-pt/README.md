# LP · perpetuo-monitoramento-concorrentes-pt (par captura + tks) · PT-PT

Duplicação **1:1** do par PT-BR [`perpetuo-monitoramento-concorrentes`](../perpetuo-monitoramento-concorrentes/README.md) — mesmo design, mesmo vídeo, mesma copy — traduzida para Português Europeu (PT-PT).

| Página | Slug | Papel | robots |
|---|---|---|---|
| Captura | `perpetuo-monitoramento-concorrentes-pt` | hero + form "preencha e assista" + "o que vai aprender" + autoridade | noindex |
| Thank-you | `perpetuo-monitoramento-concorrentes-pt-confirmado` | vídeo embedado + CTA "fale com especialista" | noindex |

**Fluxo:** captura (form mock) → submit redireciona para `/perpetuo-monitoramento-concorrentes-pt-confirmado` → assiste ao vídeo → CTA de WhatsApp.

**Vídeo:** o mesmo do par PT-BR — `https://www.youtube.com/watch?v=fG4KpFnwbb4` (embed `www.youtube.com/embed/fG4KpFnwbb4`), sem legendas/dobragem PT-PT. **Usar youtube.com, NÃO youtube-nocookie** — o CSP do guarda-chuva webinar.buzzmonitor.com só liberta `www.youtube.com` no `frame-src`.

## Origem da copy (2026-08-25)

Duplicação pedida pela Catharina do par PT-BR `perpetuo-monitoramento-concorrentes` (fonte original: briefing de 2026-08-12). Mesma estrutura, mesmo vídeo, mesma copy — apenas traduzida para PT-PT seguindo `conhecimento/linguistico/pt-portugal/padrao-linguistico.md` (Regras de Ouro: "está a funcionar", "utilizador(es)", possessivo com artigo, "folha de cálculo", "captura de ecrã", "monitorização"/"monitorizar") e `conhecimento/editorial/regras-anti-ia.md`.

## Pendências antes de finalizar (mesmas do par PT-BR)

- **Link do WhatsApp:** os CTAs da tks estão com temp `https://buzzmonitor.com/` (header + cta-final). Trocar pelo link real quando a Catharina mandar.
- **Form real:** a captura ainda é MOCK (redireciona no submit).
- **OG dedicada:** hoje reusa `og-primeiro-listening-5-passos.png` (do par PT-BR/irmão). Trocar por uma de concorrente.
- **Dados de autoridade (Victor):** confirmar números (1.000+/300+/500+/10mil) e uso das marcas — os mesmos números e marcas do par PT-BR foram mantidos por pedido explícito de duplicação 1:1.
- **Flip `index`** quando for a versão final (hoje `noindex` de review).

## Construção

Captura **dark premium**; tks **clara** (fundo branco). Anti-IA aplicado (0 em-dash, "a Buzzmonitor" feminino). Publicar via fluxo CI: worktree a partir da main + entrada no manifesto + PR pela web (sem `gh` nesta máquina; o merge-bot auto-mergeia conteúdo).
