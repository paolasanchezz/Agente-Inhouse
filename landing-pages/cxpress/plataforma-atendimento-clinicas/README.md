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
5. Demais seções (CLIENTES, FORM, PROVA, QUEM SOMOS, FOOTER), CSS, assets e formulário (Jotform `261027639617663`) idênticos à referência — não foram pedidos pelo usuário.
6. **FAQ trocada (pós-publicação, 2026-08-12)**: as 5 perguntas herdadas de `banimento-whatsapp-clinicas` (tema banimento/API oficial) foram substituídas pelas 6 perguntas literais da LP [`whatsapp-business-smb`](https://content.cxpress.io/whatsapp-business-smb) (pré-requisitos, WhatsApp CoEx, IA no N1, múltiplos números, canais integráveis, integração de CRM) — pedido explícito do usuário, copiado verbatim do source dessa LP.
7. **BENEFICIOS trocada (pós-publicação, 2026-08-12)**: H2 alterado de "O que muda na sua operação com a integração oficial" para "Centralize e automatize o seu atendimento" (texto dado literalmente pelo usuário). Os 3 cards (Integração oficial da Meta / Vários atendentes, um número / Histórico que não se perde) foram substituídos pelos 3 cards literais da seção "Centralize e automatize o seu atendimento, simples e eficaz" de `whatsapp-business-smb` (Economia de tempo / Respostas rápidas / API oficial do WhatsApp).
8. **FORM enxugada (pós-publicação, 2026-08-12)**: removidas as linhas "Planos a partir de R$ 1.290" e "Ter um site ativo é um dos requisitos para se tornar cliente da Cxpress." (pedido explícito do usuário).

## Estrutura

- HERO (com CTA)
- CLIENTES (prova social)
- FORM / agendar (Jotform `261027639617663`)
- BENEFICIOS (herdada de `whatsapp-business-smb` — ver item 7 acima)
- PROVA (stats)
- PLATAFORMA (features)
- FAQ (herdada de `whatsapp-business-smb` — ver item 6 acima)
- QUEM SOMOS
- FOOTER

## Estado

- [x] HTML duplicado + edições de copy aplicadas
- [x] Revisão (`/lp-revisar` — 0 críticos aplicáveis; ver `REVISAO.md`)
- [x] Publicado — `https://content.cxpress.io/plataforma-atendimento-clinicas` (PR #256, merge automático + deploy CI)
- [x] FAQ trocada pela de `whatsapp-business-smb` (pós-publicação, 2026-08-12)
- [x] BENEFICIOS trocada pela de `whatsapp-business-smb` (pós-publicação, 2026-08-12)
- [x] FORM enxugada — removidas as linhas de preço/requisito (pós-publicação, 2026-08-12)
- [ ] Formulário — herdado da referência (Jotform `261027639617663`); confirmar com o usuário se é o form correto pra esta LP ou se precisa trocar
- [ ] OG image — herdada da referência (mesma foto/hero), só renomeada. Se quiser OG dedicada ao novo H1, regenerar.

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
