# LP Cxpress — Estudo Primeiro Contato Saúde (página de obrigado)

**Gerado em:** 2026-09-17
**Copy-fonte:** `copy.txt` (output de /lp-preparar)
**Região:** brasil (pt-BR) · **GTM:** GTM-T4XDWHL3
**URL:** `content.cxpress.io/estudo-primeiro-contato-saude-confirmado`
**Página de captura:** `../estudo-primeiro-contato-saude/`

## Estrutura

- Nav com a logo (sem CTA, a pessoa já converteu)
- Hero em 2 colunas: à esquerda H1, subtítulo e botão "Abrir o estudo" apontando para o PDF; à direita a capa do estudo com o selo de check animado. No mobile empilha com a headline primeiro (GUIDELINES §3)
- Limite: seção em gradiente com H2 "O que este estudo não faz", parágrafo e botão "Falar com a nossa equipe"
- Footer navy com as duas linhas da copy

## Decisões registradas

1. **Copy versão 2 (2026-09-17):** a copy do §9 do documento-fonte foi substituída pela "opção C — super sinceridade", escolhida pelo Bruno entre três propostas. O bloco secundário deixou de ser oferta solta ("Quer olhar a sua operação...") e passou a nascer do limite declarado do estudo ("O que este estudo não faz"), no mesmo tom da seção METODOLOGIA da página de captura. Premissa antes de oferta, `fundamentos-copy.md` §4.1.
2. **Selo de check animado sobre a capa:** CSS puro, sem JS. O selo entra com `seloEntra` (escala 0.4 → overshoot ~1.12 → 1, via `cubic-bezier(.34,1.56,.64,1)`, delay 200ms), o traço do check se desenha com `riscoDesenha` (`stroke-dasharray/dashoffset`, delay 600ms) e um anel pulsa uma vez. Em `prefers-reduced-motion: reduce` as três animações são desligadas e o selo já aparece no estado final (GUIDELINES §4). O selo é `aria-hidden` porque a confirmação já está no H1.
3. **O PDF é servido pelo próprio domínio:** `assets/estudo-primeiro-contato-saude.pdf` no source, `/assets/cxpress/estudo-primeiro-contato-saude.pdf` no deploy (3,8 MB, 17 páginas). É o destino do botão "Abrir o estudo", que abre em nova aba.
4. **`noindex, follow`**, como as demais páginas de obrigado da Cxpress (`video-atendimento-obrigado`, `conheca-a-cxpress-confirmado`, `cadastro-realizado`).
5. **Botão secundário no padrão WhatsApp da marca** (`wa.me/551150395028`) com mensagem pré-preenchida citando o estudo. É a convenção usada pelas outras LPs Cxpress para "falar com especialista"; a copy não define destino.
6. **A capa entra com nome próprio: `capa-estudo.webp`.** No guarda-chuva os assets são achatados por marca (`./assets/X` → `/assets/cxpress/X`), então reusar o nome `ebook-estudo-primeiro-contato-saude.webp` faria as duas LPs escreverem no mesmo caminho do dist. Mesmo conteúdo hoje, mas qualquer edição futura numa página mudaria a outra em silêncio. Arquivo próprio custa 97 KB e corta o acoplamento.
7. **Sem a linha "Gratuito · 17 páginas · PDF".** Ela é da copy da página de captura, não desta; não foi transposta para não inventar texto.

## Verificação feita

- em-dash: 0 · `noindex, follow` presente · GTM nos 2 blocos
- Pisos de tipografia mobile (GUIDELINES §20) OK a 375px: H1 34px, H2 28px, subtítulo 18px, corpo 17px, botão 17px, rodapé 15px
- Sem overflow horizontal em 1440 e 375 (o único elemento fora da viewport é o arco decorativo, recortado por `overflow:hidden` do pai)
- Sem erro de console; PDF servido com `Content-Type: application/pdf`
- Animação do selo medida quadro a quadro: opacidade 0 → 1 e escala 0.4 → 1.12 → 1; estado final `stroke-dashoffset: 0`. Com `reduced-motion`, estado final direto, sem transform

## Estado

- [x] HTML gerado e publicado (2026-09-17, via fluxo CI)
- [x] PDF hospedado e linkado
- [ ] Revisão `/lp-revisar cxpress/estudo-primeiro-contato-saude-confirmado`
- [ ] **Conferir o envio por e-mail.** O subtítulo diz "Uma cópia também foi para o seu e-mail". Isso só é verdade se a automação do formulário disparar o PDF. Validar ao trocar o form; se não houver envio, a frase sai.

> **Ninguém chega aqui ainda.** O formulário da página de captura é o Jotform `262104279010647`, que é da LP `video-atendimento` e redireciona para `video-atendimento-obrigado`. Quando o form correto do estudo entrar, ele precisa apontar o "Após o envio" para esta URL.

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
- `./assets/estudo-primeiro-contato-saude.pdf` (o estudo)
- `./assets/capa-estudo.webp` (capa do estudo no hero)
