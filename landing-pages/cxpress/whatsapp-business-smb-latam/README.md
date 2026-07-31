# whatsapp-business-smb-latam

LP do guarda-chuva **content.cxpress.io** (projeto Vercel `cxpress-lp-playbook-whatsapp2026`).

Clone de `whatsapp-business-smb` (PT-BR) criado em 2026-07-30 a pedido explícito do usuário
("traduce esta LP al español neutro para que funcione en todo latam":
https://home.cxpress.io/whatsapp-business-smb): design 100% idêntico ao original, copy adaptada
para ES-LATAM (protocolo linguístico + anti-IA aplicado, mesmo processo já validado em
`whatsapp-business-smb-pt`).

- **lang:** `es-419`
- **GTM:** `GTM-WRQ47B9R` (região latam, `brand/cxpress/tracking.json`)
- **Organization/WebPage (JSON-LD) + hrefs de logo:** apontam para `https://home.cxpress.io`
  (igual ao BR — `brand-manifest.json` não tem home dedicado para latam, diferente de Portugal
  que usa `cxpress.pt`)
- **hreflang:** `es-419` (self) + `pt-BR` (`whatsapp-business-smb`) + `pt-PT`
  (`whatsapp-business-smb-pt`) + `x-default` (BR)

## Seção Clientes (idêntica ao BR, ao contrário do PT-PT)

Diferente de `whatsapp-business-smb-pt` (que trocou os logos por clientes portugueses), aqui o
grid de clientes BR (Koin, Advanta, Mondial, Vivo, Sephora, Smartfit, ThermoFisher, J&T Express,
Eletrobras, Cacau Show) foi **mantido sem troca** — segue o mesmo critério já usado em
`coex-whatsapp-latam` e `banimento-whatsapp-latam` (nenhuma dessas duas LPs LATAM trocou o asset
de clientes; não existe hoje um asset de clientes específico para LATAM).

## Pendências resolvidas (2026-07-30, a pedido do usuário)

1. **Preço:** "Planos a partir de R$ 1.290/mês para até 5 acessos" (BR) → "Planes desde USD
   260/mes" — conversão aproximada, sem mencionar quantidade de acessos, a pedido explícito
   (mesmo critério do clone PT-PT, que converteu para EUR sem mencionar acessos).
2. **E-mail comercial BR:** removido (`comercial@gocxpress.com.br` e o mailto correspondente) —
   mesmo critério do clone PT-PT.
3. **Formulário:** Jotform LATAM já compartilhado `252398149653872` (mesmo ID usado em
   `coex-whatsapp-latam` e `banimento-whatsapp-latam`), substituindo o Jotform BR
   `261027639617663`.

## Assets

Reaproveitados de `whatsapp-business-smb` (imagens/gifs sem texto embutido) — nenhum asset novo
necessário.

## Notion

Não publicado — MCP do Notion não estava conectado nesta sessão. `copy.txt` é a fonte-verdade
local; publicar manualmente quando o MCP estiver disponível, se desejado.

## Hreflang / og:locale:alternate

Como esta é a 3ª variante da família (BR + PT + LATAM), atualizei os dois irmãos
(`whatsapp-business-smb` e `whatsapp-business-smb-pt`) para listar as 3 variantes em
`hreflang` + `og:locale:alternate` (GUIDELINES §16 exige que cada LP da família liste todas).
O BR não tinha nenhum bloco `hreflang` antes desta sessão (lacuna pré-existente, corrigida de
passagem).

## Estado

- [x] Copy traduzida ES-LATAM (`copy.txt`), estrutura idêntica ao BR (10 blocos)
- [x] HTML gerado — mesmo sistema visual/CSS de `whatsapp-business-smb` e `whatsapp-business-smb-pt`,
      conteúdo 1:1 com `copy.txt` (auditoria de fidelidade feita manualmente linha a linha)
- [x] SEO completo (title, description, canonical, hreflang ×4, OG ×12, Twitter ×4, JSON-LD) —
      slug `whatsapp-business-smb-latam`
- [x] GTM — `GTM-WRQ47B9R` (região `latam`), validado via `check_gtm_region.py` (`.tracking.lock` OK)
- [x] OG image dedicada — `assets/og-whatsapp-business-smb-latam.png` (1200×630), gerada via
      Chrome headless + template adaptado de `.claude/skills/lp-gerar/og-template.html`
- [x] Formulário Jotform LATAM (`252398149653872`, já compartilhado por `coex-whatsapp-latam` e
      `banimento-whatsapp-latam`) — integrado direto (não é mock; mesmo critério dos 2 irmãos,
      que também usam o form real desde a criação por serem clones de uma LP já publicada)
- [ ] Revisão de design (`/lp-revisar cxpress/whatsapp-business-smb-latam`)
- [ ] Publicado (`/lp-publicar cxpress whatsapp-business-smb-latam content.cxpress.io`)
