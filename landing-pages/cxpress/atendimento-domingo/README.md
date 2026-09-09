# LP · cxpress / atendimento-domingo

LP de agendamento de demonstração (BoFu). Refação da LP "Domingo às 22h" na identidade visual
da Cxpress, com o Samir e revisão anti-IA da copy. Histórico da refação em `REVISAO.md`.

**URL:** https://content.cxpress.io/atendimento-domingo
**Domínio:** `content.cxpress.io` (guarda-chuva no CI, ver `landing-pages/dominios/MIGRADOS.json`)

## Status

- [x] Copy preparada
- [x] HTML gerado
- [x] Revisado (design + anti-IA)
- [x] Formulário integrado
- [x] Publicado

**Form provider:** Jotform · `261045149477663` (integrado em 2026-09-09)

O embed entra em `.jotform-embed` na seção `#agendar`, sem a classe `.form` do mock: o Jotform
já traz card próprio e herdar `.form` causaria card dentro de card. As regras CSS do mock
(`.form`, `.campo`, `.campo-check`, `.form__nota`) seguem no `<style>` sem uso no markup, de
propósito, para o caso de precisar voltar ao mock.

## Assets próprios

| Arquivo | Uso |
|---|---|
| `assets/og-atendimento-domingo.png` | OG image 1200×630 |
| `assets/logo-cacau-show.png` | Case Cacau Show |
| `assets/clientes/` | 42 logos da esteira de clientes |

Mascote e logos vêm de `brand/cxpress/assets/` por path relativo, resolvido no build.
