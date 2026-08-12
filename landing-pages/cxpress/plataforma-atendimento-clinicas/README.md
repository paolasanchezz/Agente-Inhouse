# LP Cxpress — plataforma-atendimento-clinicas

**Gerado em:** 2026-08-12
**Copy-fonte:** `copy.txt` — réplica de `landing-pages/cxpress/banimento-whatsapp-clinicas/` com edições pontuais pedidas pelo usuário.

## Origem

Duplicada de [`content.cxpress.io/banimento-whatsapp-clinicas`](https://content.cxpress.io/banimento-whatsapp-clinicas) (source local em `landing-pages/cxpress/banimento-whatsapp-clinicas/`). Segmento-alvo mantido: **clínicas e serviços de saúde** (já listado em `brand/cxpress/brand-manifest.json > audience.segments`).

**Nota de slug:** o pedido original era publicar em `atendimento-clinicas`, mas esse slug já pertence a outra LP ao vivo (MoFu clínicas, alvo de campanhas de remarketing confirmado pelo Victor em 2026-06-30 — ver `landing-pages/catalogo/lps-cxpress.md`). Slug ajustado para `plataforma-atendimento-clinicas` com aprovação do usuário para não sobrescrever a LP existente.

## Diferenças vs. a referência (banimento-whatsapp-clinicas)

1. **HERO**: H1 e SUB reescritos — muda o eixo de "evitar banimento do WhatsApp" para "plataforma unificada de atendimento". H1: "Uma plataforma para organizar todo o seu atendimento". SUB: "Centralize WhatsApp, redes sociais, telefonia, webchat e e-mail em um único sistema e tenha controle total do atendimento da sua clínica."
2. **PLATAFORMA**: H2 trocado de "A estrutura que o seu número ganha na plataforma" para "Descubra tudo o que é possível fazer com a plataforma Cxpress!".
3. **FECHO removida**: a seção inteira ("Seu número levou anos para entrar na agenda do paciente. Não deixe um improviso tirar ele de lá." + CTA) foi excluída do HTML e do `copy.txt`.
4. **Metadados** (title, canonical, description, OG, Twitter Card, JSON-LD) atualizados pro novo slug e pro novo eixo de mensagem (plataforma unificada, não mais banimento). OG image renomeada para `assets/og-plataforma-atendimento-clinicas.png`.
5. Demais seções (CLIENTES, FORM, BENEFICIOS, PROVA, FAQ, QUEM SOMOS, FOOTER), CSS, assets e formulário (Jotform `261027639617663`) idênticos à referência — não foram pedidos pelo usuário.

## Estrutura

- HERO (com CTA)
- CLIENTES (prova social)
- FORM / agendar (Jotform `261027639617663`)
- BENEFICIOS
- PROVA (stats)
- PLATAFORMA (features)
- FAQ
- QUEM SOMOS
- FOOTER

## Estado

- [x] HTML duplicado + edições de copy aplicadas
- [ ] Revisão (`/lp-revisar cxpress/plataforma-atendimento-clinicas`)
- [ ] Formulário — herdado da referência (Jotform `261027639617663`); confirmar com o usuário se é o form correto pra esta LP ou se precisa trocar
- [ ] OG image — herdada da referência (mesma foto/hero), só renomeada. Se quiser OG dedicada ao novo H1, regenerar.
- [ ] Publicado — rodar `/lp-publicar cxpress plataforma-atendimento-clinicas [dominio]`

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-primary.svg` (header)
- `../../brand/cxpress/assets/logos/logo-reversed.svg` (footer)
- `../../brand/cxpress/assets/logos/logo-icon.png` (favicon)
- `./assets/hero-clinica.jpg` (hero, LP-local, herdado da referência)
- `./assets/elife-logo-badge.png` (badge Quem Somos, LP-local, herdado da referência)
- `./assets/og-plataforma-atendimento-clinicas.png` (OG image, renomeada da referência)
- `../../brand/cxpress/assets/plataforma/clientes-cxpress.png` (prova social)
- `../../brand/cxpress/assets/plataforma/plataforma-canais.gif`, `plataforma-chatbot-ia.gif`, `plataforma-dashboard.gif` (seção Plataforma)
- `../../brand/cxpress/assets/plataforma/quem-somos-foto.jpg`
