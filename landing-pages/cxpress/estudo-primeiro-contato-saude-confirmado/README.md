# LP Cxpress — Estudo Primeiro Contato Saúde (página de obrigado)

**Gerado em:** 2026-09-17
**Copy-fonte:** `copy.txt` (output de /lp-preparar)
**Região:** brasil (pt-BR) · **GTM:** GTM-T4XDWHL3
**URL:** `content.cxpress.io/estudo-primeiro-contato-saude-confirmado`
**Página de captura:** `../estudo-primeiro-contato-saude/`

## Estrutura

- Nav com a logo (sem CTA, a pessoa já converteu)
- Hero centrado: selo de confirmação, H1, subtítulo e botão "Abrir o estudo" apontando para o PDF
- Diagnóstico: seção em gradiente com H2, parágrafo e botão "Falar com a nossa equipe"
- Footer navy com as duas linhas da copy

## Decisões registradas

1. **O PDF é servido pelo próprio domínio:** `assets/estudo-primeiro-contato-saude.pdf` no source, `/assets/cxpress/estudo-primeiro-contato-saude.pdf` no deploy (3,8 MB, 17 páginas). É o destino do botão "Abrir o estudo", que abre em nova aba.
2. **`noindex, follow`**, como as demais páginas de obrigado da Cxpress (`video-atendimento-obrigado`, `conheca-a-cxpress-confirmado`, `cadastro-realizado`).
3. **Botão secundário no padrão WhatsApp da marca** (`wa.me/551150395028`) com mensagem pré-preenchida citando o estudo. É a convenção usada pelas outras LPs Cxpress para "falar com especialista"; a copy não define destino.
4. **Sem o mockup do tablet.** No guarda-chuva os assets são achatados por marca (`./assets/X` → `/assets/cxpress/X`), então reusar `ebook-estudo-primeiro-contato-saude.webp` aqui colidiria com o arquivo da página de captura no dist. A tks é sobre a ação, não precisa do visual.
5. **Sem a linha "Gratuito · 17 páginas · PDF".** Ela é da copy da página de captura, não desta; não foi transposta para não inventar texto.

## Verificação feita

- em-dash: 0 · `noindex, follow` presente · GTM nos 2 blocos
- Pisos de tipografia mobile (GUIDELINES §20) OK a 375px: H1 34px, H2 28px, subtítulo 18px, corpo 17px, botão 17px, rodapé 15px
- Sem overflow horizontal em 1440 e 375 (o único elemento fora da viewport é o arco decorativo, recortado por `overflow:hidden` do pai)
- Sem erro de console; PDF servido com `Content-Type: application/pdf`

## Estado

- [x] HTML gerado e publicado (2026-09-17, via fluxo CI)
- [x] PDF hospedado e linkado
- [ ] Revisão `/lp-revisar cxpress/estudo-primeiro-contato-saude-confirmado`

> **Ninguém chega aqui ainda.** O formulário da página de captura é o Jotform `262104279010647`, que é da LP `video-atendimento` e redireciona para `video-atendimento-obrigado`. Quando o form correto do estudo entrar, ele precisa apontar o "Após o envio" para esta URL.

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
- `./assets/estudo-primeiro-contato-saude.pdf` (o estudo)
