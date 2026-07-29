# whatsapp-business-smb-pt

LP do guarda-chuva **content.cxpress.io** (projeto Vercel `cxpress-lp-playbook-whatsapp2026`).

Clone de `whatsapp-business-smb` (PT-BR) criado em 2026-07-28 a pedido explícito ("replique a página
para uma versão em pt-pt": https://home.cxpress.io/whatsapp-business-smb): design 100% idêntico ao
original, copy adaptada para PT-PT (protocolo linguístico + anti-IA aplicado, mesmas regras já
validadas em `banimento-whatsapp-pt`).

- **lang:** `pt-PT`
- **GTM:** `GTM-NW6V5KBM` (região Portugal, `brand/cxpress/tracking.json`)
- **Organization/WebPage (JSON-LD) + hrefs de logo:** apontam para `https://www.cxpress.pt` (não `home.cxpress.io`, que é o domínio institucional BR)
- **hreflang:** `pt-PT` (self) + `pt-BR` (`whatsapp-business-smb`) + `x-default` (BR)

## Secao Clientes (divergente do original BR)

Mesma correção já aplicada em `banimento-whatsapp-pt`: os clientes do grid BR (Koin, Advanta, Mondial,
Vivo, Sephora, smartfit, ThermoFisher, J&T Express, Eletrobras, Cacau Show) nao fazem sentido para
Portugal. Substituido pelo asset `clientes-cxpress-pt.png` (Continente, Delta Q, Hertz, CAOA, Saude
Prime — extraido de https://www.cxpress.pt/ em 2026-07-10), agora promovido para
`brand/cxpress/assets/plataforma/` (nivel de marca, reutilizavel por qualquer LP PT-PT futura).

## Pendencias resolvidas (2026-07-28, a pedido do usuario)

1. **Preco:** "Planos a partir de R$ 1.290/mes para ate 5 acessos" (BR) -> "Planos a partir de 295
   €/mes" — sem mencionar quantidade de acessos, a pedido explicito.
2. **E-mail comercial BR:** removido (`comercial@gocxpress.com.br` e o mailto correspondente).
3. **Formulario:** Jotform PT dedicado `261904529617867` (mesmo form ja usado em
   `banimento-whatsapp-pt`), substituindo o Jotform BR compartilhado `261027639617663`.

## Assets

Reaproveitados de `whatsapp-business-smb` (imagens/gifs sem texto embutido), exceto a secao Clientes
(ver acima).
