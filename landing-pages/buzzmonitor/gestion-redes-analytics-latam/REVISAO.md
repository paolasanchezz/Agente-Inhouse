# Revision LP — buzzmonitor/gestion-redes-analytics-latam

**Data:** 2026-10-25
**Auditores:** design review (GUIDELINES) + web-design-guidelines (a11y/HTML) + checks deterministicos (GTM, SEO, contraste, mobile)

## v2 (2026-10-25): redesign premium a pedido do usuario

Feedback: "mais premium, menos pasteis; amigavel e acessivel, mas profissional; transmitir confianca, fiabilidade e seguranca".

- Paleta reduzida: roxo quase preto (`#1c0629`) nas secoes escuras, branco/off-white quente, laranja so em CTA e acentos pontuais, teal so nos checks. Removidos todos os blobs/cards pasteis.
- Hero: grid de pontos sutil + janela de produto unica (barra lateral escura, calendario, bandeja com resposta IA, grafico) no lugar dos 3 cards flutuantes. Sublinhado laranja em "armar reportes". Selo de escudo na prova social.
- Gestion: cards de vidro escuro com borda fina, icones de linha e lista com checks e divisorias.
- Analytics: cards brancos com borda fina e sombra suave.
- Para quien: grade unica com divisorias e icones em quadrado roxo (antes 4 cards pasteis).
- Testimonios: comilla decorativa laranja (aspas inline removidas para nao duplicar), autor com divisoria.
- CTA final e footer em roxo quase preto com grid de pontos.
- Copy intacta. Contraste re-medido: todos os textos >= 5.2:1. Mobile 375px: 0 overflow, minimo 14px.
- OG image regenerada no novo estilo.

## Aplicado automaticamente na v1 (5 criticos)

- [x] LOGO: header/footer usavam `logo-primary.png`/`logo-reversed.png` (PNG quadrado 250×250, o wordmark renderizava com 30px de largura). Trocado pelos SVG do brand (0 `<text>`, web-safe §19), igual a LP todo-en-uno.
- [x] HERO: overline, H1, sub, CTA e prova social estavam com `.rv` (opacity 0 ate o JS rodar). Removido no hero: o texto acima da dobra aparece sem depender de JS (LCP).
- [x] SKIP-LINK: `left:-9999px` acusava overflow horizontal no `check_mobile_type.py`. Trocado por `top:-80px` / `:focus{top:8px}`.
- [x] MOCKUP: o card de metricas do hero tinha um numero ficticio ("+24%"). Trocado por barra decorativa, sem dados inventados.
- [x] OG IMAGE: gerada `assets/og-gestion-redes-analytics-latam.png` (1200×630, H1 + mockup + logo).

## Checks que passaram

- GTM `GTM-MKQBX2MG` (regiao latam pelo sufixo do slug): `status=ok`, selo gravado com `--write-stamp`.
- Em-dash: 0 no HTML e na copy.
- Fidelidade da copy: todos os textos visiveis literais da `copy.txt`. Fora dela so a whitelist: "Saltar al contenido", aria-labels e o disclaimer do form ("Al enviar aceptas recibir comunicaciones de Buzzmonitor.").
- SEO: description, robots, canonical, 10 `og:`, 4 `twitter:`, JSON-LD valido (Organization + WebPage + SoftwareApplication). Sem LPs irmas, entao sem hreflang.
- Logo header/footer → `https://buzzmonitor.com/es/` com `target="_blank" rel="noopener"`.
- Ancora: nenhum JS grava `#` na URL; CTAs sao `<a href="#inscripcion">`.
- Contraste (AA): botao 6.3:1, overlines 5.2:1, textos sobre roxo 9.6 a 11.6:1, legal 5.8:1. Destaque laranja do H1 3.9:1 (texto grande, passa AA large).
- Mobile 375px: H1 36px, corpo 17px, minimo 14px, 0 overflow.
- `prefers-reduced-motion` desliga reveal e flutuacao; `<noscript>` mostra os `.rv`.

## Melhorias opcionais (4)

- [ ] **Formulario real:** integrar o Jotform LATAM com `/lp-integrar-form`. As LPs irmas usam 241825239057661 (confirmar se e o form certo para esta campanha).
- [ ] **Campo País:** hoje e texto livre. Um `<select>` com os paises LATAM melhora a qualidade do dado (provavelmente resolvido pelo proprio Jotform).
- [ ] **Ancora sem hash:** se a LP for para um dominio fora do CI (`MIGRADOS.json`), colar `ancoras-sem-hash.js` antes do `</body>`. Nos guarda-chuvas migrados (ex.: `content.buzzmonitor.com`) o build injeta.
- [ ] **Nav mobile:** abaixo de 980px so o botao "Agendar demo" fica visivel. Aceitavel numa LP curta; um menu so se o time sentir falta.

## Nice-to-haves (2)

- [ ] Logos de clientes/agencias (McCann, Publicis, Sube) perto dos depoimentos, reaproveitando `todo-en-uno/assets/logos-agencias/`.
- [ ] Capturas reais da interface (calendario, bandeja, Analytics) no lugar dos mockups abstratos, se o time tiver prints aprovados.

## Proximos passos

- Design aprovado? → `/lp-integrar-form buzzmonitor/gestion-redes-analytics-latam "<snippet>"`
- Publicar → `/lp-publicar buzzmonitor gestion-redes-analytics-latam [dominio]`
