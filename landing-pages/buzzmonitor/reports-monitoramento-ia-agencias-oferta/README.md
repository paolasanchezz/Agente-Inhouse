# LP Buzzmonitor — reports-monitoramento-ia-agencias-oferta

**Gerado em:** 2026-09-01
**Copy-fonte:** `copy.txt`
**Template-fonte:** `gestao-de-crises-ia-agosto-2026-oferta` (mesma oferta, mesmo padrão visual, adaptado pro webinar "Reports e Monitoramento com IA para Agências")
**Domínio-alvo:** webinar.buzzmonitor.com (guarda-chuva migrado pro CI)

## O que é

LP de oferta pós-webinar (não é a LP de inscrição). Destino do link enviado por e-mail/replay para quem participou do webinar `reports-monitoramento-ia-agencias`, oferecendo 14 dias grátis + desconto de continuidade.

## Padrão reaproveitado

HTML/CSS/JS **idênticos** ao template `gestao-de-crises-ia-agosto-2026-oferta` (Poppins + Lato, ícones Tabler via CDN, fundo roxo→laranja na seção Oferta, count-up animado na Prova Social). Só o conteúdo textual foi adaptado:

- **Reaproveitado sem alteração:** seção Oferta (mecânica 14 dias + desconto), seção Módulos (descrição genérica da plataforma), Prova Social, Urgência (texto já genérico), Clientes (mural), Footer.
- **Adaptado pro tema "reports e agências":** Hero (H1+SUB), corpo da Oferta + 3º item da lista (era "triggers e alertas", virou "relatórios e dashboards"), os 5 itens de Benefícios (antes focados em crise, agora em relatório/IA/SAC/multi-conta), sub do CTA final.
- **Form:** mesmo JotForm reaproveitado em todas as LPs de oferta (ID `253573505200650`), diferente do form de inscrição do webinar (`252154974852667`).

## Estado

- [x] HTML gerado
- [ ] OG image 1200×630 → `assets/og-reports-monitoramento-ia-agencias-oferta.png`
- [ ] Revisão (`/lp-revisar buzzmonitor/reports-monitoramento-ia-agencias-oferta`)
- [ ] Publicado — rodar `/lp-publicar buzzmonitor reports-monitoramento-ia-agencias-oferta webinar.buzzmonitor.com`

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `./assets/logos/mural-1.jpeg` e `./assets/logos/mural-2.jpeg` (mural de clientes, copiados de `gestao-de-crises-ia-agosto-2026-oferta`)

## Notas

- GTM: `GTM-WFJVK858` (região Brasil).
- Ícones Tabler (`@tabler/icons-webfont@3.31.0` via jsDelivr) — validado via CSS computado que todos os ícones usados (`ti-report`, `ti-brain`, `ti-calendar-plus`, `ti-users-group`, `ti-headset`, `ti-rocket`, `ti-gift`, `ti-sparkles`, `ti-arrow-right`) resolvem para glifos reais.
- JSON-LD tipo `Service` (mesma estrutura do template-fonte).
