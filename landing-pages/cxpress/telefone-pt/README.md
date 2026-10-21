# Cxpress · LP telefone-pt

Reconstrução da `https://www.cxpress.pt/telefone` (Cxpress.voz, telefone em nuvem com IA) em PT-PT, com a mesma copy da página atual e visual novo.

| | |
|---|---|
| **Marca / região** | Cxpress · Portugal (`pt-PT`) |
| **Leadpages** | org Tami Buzzmonitor, slug `telefone-pt`, pageId `wi0lec3sox66tqhms9t8fp1z`, **rascunho** (noindex) |
| **Nomenclatura** | igual às irmãs PT: slug `<tema>-pt`, título `[PT] ... \| Cxpress` |
| **GTM** | `GTM-NW6V5KBM` (o das LPs PT do repo) |
| **Formulário** | `form-cxpress-pt-v1.js` da biblioteca (Jotform `261904529617867`), o mesmo das LPs PT |
| **Fonte da copy** | https://www.cxpress.pt/telefone (lida por resumo, ver pendências) |

## Estrutura

Hero com palco animado de 15 s → faixa de números → clientes → formulário → vídeo "Telefone em nuvem com IA" (YouTube `7lA4FOTJw7E`) → "Eleve o nível do atendimento com a Cxpress" (5 cartões interativos) → faixa de diagnóstico → Quem somos → FAQ (5).

## Conferência de copy (2026-10-21)

Copy conferida contra o print da página atual enviado pelo Bruno e a FAQ colada por ele, adaptada a PT-PT ("a responder" em vez de gerúndio, "pretender", "assistente", "ligar" em vez de "conectar", "contacto", "à resolução", "na perfeição"). Saíram as secções que eu tinha montado a partir de texto invisível no print: chatbot/WhatsApp, "Condições especiais" e o fecho repetido. Se a página viva as mostra noutra vista, é só reinserir.

## Palco de 15 s (a "motion")

Cena em HTML/CSS/JS dentro da página, em loop de 5 capítulos de 3 s: chamada a entrar, voicebot a atender, encaminhamento para a fila certa, dashboard, um número com todos os canais. Capítulos clicáveis; `prefers-reduced-motion` mostra a cena 3 parada. Os textos e números do palco e dos cartões são ilustrativos e estão rotulados.

## Ficheiros

- `index.html`: fonte local (paths relativos) para testar com o servidor `lp-repo-root`.
- `leadpages/telefone-v1.css` e `telefone-v1.js`: subidos como assets de página.
- `assets/clientes-pt.png` (380x67) e `configuracao-audio.webp`.

## Pendências

- Faixa de logótipos com só 380 px de largura: pedir versão maior.
- Footer: o print mostra logo Elife Group e ícones de redes sociais; ficaram o logo Cxpress e os dois links legais (`cx.elifeportugal.com`). Faltam os URLs das redes.
- Voicebot e distribuição de chamadas vêm da página oficial, mas não constam no BRANDBOOK.
- OG image, publicação e domínio por fazer.
