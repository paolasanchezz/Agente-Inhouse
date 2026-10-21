# Revisao LP — cxpress/elife_cxpress_Buzzsummit26

**Data:** 2026-10-21
**Auditores:** checagens deterministicas do `lp-revisar` (SEO, GTM, em-dash, OG, logo) + passada manual de design e acessibilidade

## Aplicado automaticamente (2 criticos)

- [x] SEO-JSONLD: JSON-LD ausente, adicionado grafo Organization + WebPage (mesmo padrao de `/institucional`)
- [x] A11Y: sem skip-link, adicionado "Ir para o formulario" apontando para `#inscricao`

## Verificado sem achados

- GTM `GTM-T4XDWHL3` (brasil): 1 OK, 0 bloqueios
- Meta description 1, canonical 1, og:* 10, twitter:* 4; OG image 1200x630 com nome canonico
- Em-dash: 0 · SVG do header sem `<text>` vivo · rodape com logo apontando para home.cxpress.io
- Fidelidade de copy: `copy.txt` inexistente (copy autoral desta LP), auditoria pulada
- Hreflang: LP sem irmas, nao se aplica

## Melhorias opcionais

- [ ] Texto do titulo "Termos e Politicas" no rodape tem 12px (abaixo do piso mobile de 14px). Mantido porque o rodape deve ser identico ao de `/institucional`
- [ ] Formulario em Jotform HTML completo carrega CSS/JS de terceiros (peso e dependencia do CDN)

## Nice-to-haves

- [ ] Botao de enviar ~6px deslocado em relacao aos campos (margem interna do tema do Jotform)
