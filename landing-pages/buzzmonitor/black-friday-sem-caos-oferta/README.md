# LP Buzzmonitor — black-friday-sem-caos-oferta

**Gerado em:** 2026-10-16
**Copy-fonte:** `copy.txt`
**Template-fonte:** `reports-monitoramento-ia-agencias-oferta` (mesmo padrão visual das ofertas pós-webinar)
**Domínio-alvo:** webinar.buzzmonitor.com (guarda-chuva migrado pro CI)

## O que é

LP de oferta pós-webinar (não é a LP de inscrição). Destino do link enviado por e-mail/replay para quem participou do webinar `black-friday-sem-caos` (05/nov/2026, 11h).

## Diferença para as ofertas anteriores

O destaque aqui é **50% off nos 2 primeiros meses** (pedido da Catharina). Nas ofertas anteriores o número gigante era "14 dias" e o desconto aparecia vago no bônus ("desconto imperdível").

- Watermark do hero: `50%`
- Número gigante da seção Oferta: `50% off` / "nos 2 primeiros meses de Buzzmonitor"
- Bônus virou a explicação da mecânica: 14 dias grátis → se continuar, metade do valor nos 2 primeiros meses
- Mantido tudo o que as outras ofertas têm: 14 dias grátis, suporte consultivo, configuração (aqui: alertas de possível crise para a Black Friday)

## Padrão reaproveitado

HTML/CSS/JS idênticos ao template. Reaproveitado sem alteração: Módulos, Prova Social, Clientes (mural), Footer, form. Adaptado: Hero, Oferta, Benefícios (temas da LP de inscrição), corpo da Urgência (cita 27/nov), sub do CTA final.

- **Form:** JotForm `253573505200650` (mesmo de todas as LPs de oferta).
- **GTM:** `GTM-WFJVK858`.

## Estado

- [x] HTML gerado
- [ ] OG image 1200×630 → `assets/og-black-friday-sem-caos-oferta.png`
- [ ] Revisão (`/lp-revisar buzzmonitor/black-friday-sem-caos-oferta`)
- [ ] Publicado — rodar `/lp-publicar buzzmonitor black-friday-sem-caos-oferta webinar.buzzmonitor.com`

## Pendências

- Confirmar se o JotForm `253573505200650` precisa de algum campo/etiqueta pra comercial saber que o lead veio com a condição de 50% off (o form é compartilhado com as outras ofertas).
- A LP de inscrição `black-friday-sem-caos` foi revertida da main (commit `efedfc2`); publicar a oferta não depende dela, mas vale alinhar a ordem.

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg`, `logo-reversed.svg`, `logo-icon.png`
- `./assets/logos/mural-1.jpeg`, `./assets/logos/mural-2.jpeg`
