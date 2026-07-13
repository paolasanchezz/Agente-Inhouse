# LP Buzzmonitor — primeiro-listening-5-passos

**Gerado em:** 2026-07-09
**Copy-fonte:** `copy.txt` (origem: Notion "Copy LP · Buzzmonitor · primeiro-listening-5-passos · 2026-07-07")
**Referência de estilo:** mesmos moldes da `case-youse` (DNA da `mcp-na-pratica-p` + melhorias visuais).
**Região/idioma:** brasil / pt-BR · **GTM:** GTM-WFJVK858 · **Domínio previsto:** webinar.buzzmonitor.com (guarda-chuva)

## Estrutura

- HERO (kicker + H1 com "5 passos" em marker laranja + body + meta) com card de formulário à direita (mock)
- O QUE VOCÊ VAI VER (5 passos em 3 cards + chips teal "Passos 1 e 2 / 3 e 4 / 5" com feature oficial)
- QUEM APRESENTA (Leandra Lira, foto placeholder)
- PARA QUEM (4 checks em grid 2x2)
- CTA FINAL (seção dark roxo, botão laranja, scroll pro form)
- FOOTER

## Estado

- [x] HTML gerado
- [x] Revisao — mesmas validações da case-youse (em-dash 0, SEO completo, JSON-LD ok, GTM ok, fidelidade literal, screenshots desktop) + OG image gerada
- [ ] Formulario integrado — rodar `/lp-integrar-form buzzmonitor/primeiro-listening-5-passos [fluxo ClickMeeting]`
- [ ] Publicado — rodar `/lp-publicar buzzmonitor primeiro-listening-5-passos webinar.buzzmonitor.com`

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)
- `./assets/og-image.png` (OG 1200×630 — no deploy vira `/assets/buzzmonitor/og-primeiro-listening-5-passos.png`)

## Pendências

- **Foto da speaker:** copy trouxe link de edição do Canva (não exportado). Placeholder "Foto em breve"; trocar quando o PNG chegar.
- **Form real (ClickMeeting):** mock (GUIDELINES §11). Integração = criar série recorrente no ClickMeeting + adicionar chave `primeiro-listening-5-passos` (ou curta, ex. `listening-5-passos`) no mapa SERIES de `_clickmeeting-api/next-webinar.js` e `clickmeeting-register.js` + JS da referência; página `-confirmado` se quiser confirmação on-site.
- **Copy (sugestões marcadas em copy.txt):** H1 abre pelo método (MoFu — GUIDELINES §3 sugere dor primeiro; estrutura clonada da referência, decisão do Victor); frase "O nome de quem apresenta aparece aqui..." na bio parece sobra de placeholder.
- Se posicionar como **gravação sob demanda**: trocar badges e verbos do CTA.
