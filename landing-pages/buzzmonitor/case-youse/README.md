# LP Buzzmonitor — case-youse

**Gerado em:** 2026-07-09
**Copy-fonte:** `copy.txt` (output de /lp-preparar; origem: Notion "Copy LP · Buzzmonitor · case-youse-sla · 2026-07-07"; slug final `case-youse` definido pelo Victor)
**Referência de estilo:** `landing-pages/buzzmonitor/mcp-na-pratica-p/` (webinar.buzzmonitor.com/mcp-na-pratica-p), com melhorias visuais pedidas pelo Victor.
**Região/idioma:** brasil / pt-BR · **GTM:** GTM-WFJVK858 · **Domínio previsto:** webinar.buzzmonitor.com (guarda-chuva)

## Estrutura

- HERO (kicker + H1 com destaques tipográficos + body + meta) com card de formulário à direita (mock)
- O QUE VOCÊ VAI VER (3 pilares em cards + chips "Na tela" em teal)
- QUEM APRESENTA (Nathalia Crivellaro, foto placeholder)
- PARA QUEM (4 checks em grid 2x2)
- CTA FINAL (seção dark roxo, botão laranja, scroll pro form)
- FOOTER

## Melhorias visuais vs. referência mcp-na-pratica-p

- Hero com wash radial lilás + padrão de pontos; composição geométrica extra (anel teal-light, dot teal)
- Destaque tipográfico no H1: "3 horas" (marker laranja) e "75% menor" (sublinhado teal)
- Linha gradiente (roxo→laranja) no topo do header e do card de form — único tipo de gradiente da LP
- Cards de pilar com numeral gigante outline (ghost) + chips "Na tela" com ícone de monitor (teal)
- Reveals com stagger por card; hovers com barra de acento animada (pilares e para-quem)
- CTA final em seção escura (único momento dark) com glow do gradiente da marca

## Estado

- [x] HTML gerado
- [x] Revisao (frontend-design review + web-design-guidelines) — 1 critico aplicado (OG image), opcionais em `REVISAO.md`
- [ ] Formulario integrado — rodar `/lp-integrar-form buzzmonitor/case-youse [snippet]`
- [ ] Publicado — rodar `/lp-publicar buzzmonitor case-youse webinar.buzzmonitor.com`

## Assets referenciados

- `../../brand/buzzmonitor/assets/logos/logo-primary.svg` (header)
- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (footer)
- `../../brand/buzzmonitor/assets/logos/logo-icon.png` (favicon)

## Pendências

- ~~OG image~~ **feita** — `assets/og-image.png` (1200×630) gerada em 2026-07-09. No deploy vira `/assets/buzzmonitor/og-case-youse.png`.
- **Foto da speaker:** copy trouxe link de edição do Canva (não exportado). Placeholder "Foto em breve" no lugar; trocar quando o PNG chegar.
- **Form real (ClickMeeting):** mock nesta fase (GUIDELINES §11). Integração = (1) criar série recorrente no ClickMeeting pro webinar do case Youse; (2) adicionar a chave `case-youse` no mapa SERIES de `landing-pages/buzzmonitor/_clickmeeting-api/next-webinar.js` e `clickmeeting-register.js`; (3) trocar o mock pelo JS da referência (`mcp-na-pratica-p`) com `SERIES='case-youse'` e, se quiser página de confirmação, criar `case-youse-confirmado`.
- **Copy:** frase "O nome de quem apresenta aparece aqui e no e-mail de inscrição." na bio parece sobra do placeholder da referência (speaker já nomeada) — decisão do Victor.
