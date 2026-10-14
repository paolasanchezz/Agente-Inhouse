# Revisao LP — cxpress/gestao-canais-ia-2027

**Data:** 2026-10-14
**Auditores:** checagens deterministicas do /lp-revisar (GTM, SEO, OG, logo, em-dash, fidelidade) + auditoria manual de design e acessibilidade + Lighthouse mobile

## Aplicado automaticamente (1 critico)

- [x] COPY-DIVERGENCIA: o texto do Sobre no HTML (enviado e aprovado em 14/10) diferia do copy.txt. Fonte unica realinhada: copy.txt atualizado com o texto aprovado. HTML nao precisou mudar.

## Resultado das checagens

| Checagem | Resultado |
|---|---|
| GTM (regiao brasil) | ok, GTM-T4XDWHL3, selo em dia |
| Pacote SEO (§15) | description 1 · robots 1 · og 10 · twitter 4 · JSON-LD 1 (parseia: Organization, WebPage, Event) · canonical 1 |
| hreflang | LP unica, so x-default: ok |
| Logo (§17/§19) | sem href="/"; logo-primary e logo-reversed sem <text> |
| OG image (§18) | og-gestao-canais-ia-2027.png, 1200x630 |
| Em-dash | 0 |
| Fidelidade da copy | sem texto inventado. Fora da copy.txt so rotulos funcionais (skip-link, eyebrow de secao, countdown, termos e politicas) e a regua decorativa 9h/10h/11h/12h da barra do dia |
| Lighthouse mobile (no ar, com GTM e Pixel) | desempenho 70 (era 46), LCP 3,1 s (era 9,2 s), CLS 0,005, acessibilidade 100, SEO 100, boas praticas 77 |

## Melhorias opcionais (3)

- [ ] **Pixel do Facebook via GTM:** responde por quase todo o TBT (~970 ms) e pelo 77 em boas praticas (cookie de terceiro). Mudar o disparo do Pixel no contêiner GTM-T4XDWHL3 para depois do carregamento. Fora do codigo da LP.
- [ ] **Botao do formulario:** o texto "Cadastrar" vem do Jotform 260995815122663. Trocar por "Quero participar" no builder do Jotform (e na traducao Portugues (Brasil)). A LP ja forca language=pt-BR (bandeira do Brasil).
- [ ] **JSON-LD Organization sem sameAs:** brand/cxpress/brand-manifest.json nao tem bloco regions/socials. Migrar o manifest resolve em todas as LPs Cxpress.

## Nice-to-haves (2)

- [ ] Inscricao no fim da pagina (pedido de 14/10) reduz conversao esperada; se a taxa cair, voltar a 2a posicao (GUIDELINES §10).
- [ ] Endereco sem andar/sala e sem CEP (nao informados).

## Proximos passos

- Form integrado e pagina publicada: https://content.cxpress.io/gestao-canais-ia-2027
