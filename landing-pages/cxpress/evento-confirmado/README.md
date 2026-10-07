# LP Cxpress — evento-confirmado

Thanks page **padrão** de confirmação de inscrição em **evento presencial** da Cxpress Brasil.
Aparece logo após a pessoa se inscrever no formulário de qualquer evento presencial (café,
workshop, encontro). Texto fixo e genérico, sem nome nem data do evento: uma URL serve para
todos os eventos, basta apontar o redirect de sucesso do form para ela.

**Gerado em:** 2026-10-06
**Copy-fonte:** `copy.txt` (escrita pelo agente a pedido do usuário, aprovada em 2026-10-06)
**Notion (copy):** https://app.notion.com/p/3f13934026fd8150b6aac6c119b38b15
**Domínio:** `content.cxpress.io` (guarda-chuva migrado pro CI, deploy só via `lp-publicar`)
**URL final:** `https://content.cxpress.io/evento-confirmado`

## Estrutura

- CONFIRMAÇÃO (medalhão do mascote com selo de check + etiqueta "Inscrição confirmada" + H1 "Fique de olho no seu e-mail." + subtítulo)
- QUEM SOMOS (foto + overline + H2 "Prazer, somos a Cxpress" + texto + 3 selos + botão para home.cxpress.io)
- CLIENTES (H2 "Mais de 800 empresas..." + grade de logos `clientes-cxpress.png`)
- FOOTER (padrão do domínio: logo + linha legal + 4 redes, copiado da `obrigado` / `escolha-a-cxpress`)

Base visual: `cadastro-realizado` (medalhão, layout de altura cheia, fundo branco → azul claro,
pílulas decorativas). v2 (2026-10-06, pedido do usuário): saiu o H1 "Sua vaga está garantida." e
a seção "O que fazer agora"; entraram QUEM SOMOS e CLIENTES, com fatos já publicados em outras LPs
Cxpress BR (ver notas em `copy.txt`). O selo Elife é texto: o `elife-logo.png` do brand é cinza claro
sobre fundo opaco e sumia na pílula.

## Exceções deliberadas às GUIDELINES (precedente: cadastro-realizado / conheca-a-cxpress-confirmado)

- **`noindex, follow`**: página pós-ação; o Lighthouse SEO do lp-publicar vai apontar
  "is-crawlable" como falha. Esperado, não "consertar".
- **Sem OG image, sem OG/Twitter/JSON-LD e sem placeholders `{{DOMAIN}}`**: ninguém compartilha
  esta URL.
- **Sem estrutura mínima de LP** (§6) e **sem form**: não há captação, é só confirmação.

## Estado

- [x] HTML gerado
- [x] Revisão (ver `REVISAO.md`)
- [n/a] OG image (thanks page, ver exceções)
- [n/a] Formulário (página pós-form)
- [ ] Publicado — `/lp-publicar cxpress evento-confirmado content.cxpress.io`

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-primary.svg` (header; sem `<text>`, §19 ok)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer; sem `<text>`, §19 ok)
- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `./assets/mascot/samir-joinha-web.png` (cópia da versão otimizada de 76 KB da `cadastro-realizado`)
- `../../brand/cxpress/assets/plataforma/quem-somos-foto.jpg`
- `../../brand/cxpress/assets/plataforma/clientes-cxpress.png`

## Uso

No formulário de inscrição de cada evento presencial Cxpress BR, configurar o redirect de
sucesso para `https://content.cxpress.io/evento-confirmado`. O e-mail de confirmação do evento
precisa trazer data, horário e endereço (a página promete isso).
