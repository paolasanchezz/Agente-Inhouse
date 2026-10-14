# LP Cxpress — evento-confirmado-pt

Thanks page **padrão** de inscrição em **eventos da Cxpress Portugal** (PT-PT). Texto fixo e
genérico, sem nome nem data do evento: uma URL serve para todos os eventos, basta apontar o
redirect de sucesso do form para ela.

**Gerado em:** 2026-10-14
**Copy-fonte:** `copy.txt`
**Base visual:** `evento-confirmado` (BR), mesma estrutura e CSS; textos reescritos em PT-PT.
**Domínio:** `content.cxpress.io` (guarda-chuva migrado pro CI, deploy só via `lp-publicar`)
**URL final:** `https://content.cxpress.io/evento-confirmado-pt`

## Diferenças vs. evento-confirmado (BR)

- `lang="pt-PT"`, copy PT-PT, links de logo/CTA para `https://www.cxpress.pt` (padrão das LPs PT).
- Mensagem: não fala em confirmação manual de vaga; só promete mais informações por e-mail.
- Logos de clientes: faixa `clientes-cxpress-pt.png` (clientes de Portugal, copiada de `whatsapp-agencias-pt`).

## Exceções deliberadas às GUIDELINES (mesmas da evento-confirmado)

- `noindex, follow` (página pós-ação); sem OG/Twitter/JSON-LD; sem form.

## Estado

- [x] HTML gerado
- [ ] Publicado — `/lp-publicar cxpress evento-confirmado-pt content.cxpress.io`
