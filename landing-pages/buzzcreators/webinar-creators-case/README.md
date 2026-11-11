# LP Buzzcreators — webinar-creators-case

**Gerado em:** 2026-11-11
**Copy-fonte:** `copy.txt` (montada a partir do briefing da conversa; sem passar pelo /lp-preparar nem pelo Notion)
**Tipo:** LP Aula / webinar perpetuo (captura). Par: [`../webinar-creators-case-confirmado/`](../webinar-creators-case-confirmado/) com o video.
**Dominio previsto:** `webinar.buzzmonitor.com` (guarda-chuva migrado pro CI, como a `conheca-o-buzzcreators`).

## Estrutura

**v2 (2026-11-11):** a v1 foi reprovada por ser "muito extensa e muito branca". Referencia visual: `buzzcreators.com.br/gestao-de-influenciadores` (faixas roxas, cards brancos e detalhes em laranja). Passou de 9 para 4 secoes de conteudo, com cerca de 19% menos altura no celular (7.982px → 6.477px a 375px). Boa parte do que sobrou e o proprio form.

1. **Hero roxo:** overline, H1 com destaque em laranja, sub, 4 itens e o form branco ao lado (no mobile, logo abaixo). Os numeros (3x · 12x · 4,5x · 3.719) ficam na base da mesma faixa.
2. **A estrategia** (fundo `#f7f9fb`, v6): card roxo centralizado com "Essa marca olhou para dentro". Os 3 caminhos caros (influenciador famoso, e-commerce, midia paga) sairam a pedido do time: essas estrategias nao estao erradas, a LP so destaca a diferente.
3. **O que voce vai aprender** (branco): faixa roxa da governanca + grid de 4 pilares com borda laranja.
4. **Clientes** (fundo `#f7f9fb`, v3): 1.000+ clientes · 500+ agencias · 300+ enterprise · 10k usuarios, com a grade de logos no meio. No celular os numeros vem em 2x2 e os logos em 2 blocos empilhados, para nao ficarem minusculos.
5. **Fechamento escuro:** speaker em card translucido, tag "E no final", teaser do erro e 2 CTAs, o laranja (rola ate o form) e o contorno "Conhecer o Buzzcreators" (pagina comercial com UTM, nova aba).
6. Footer roxo com redes sociais e politica de privacidade.

Cortado na v2: o fluxo do cupom (o Pilar 3 ja cobre) e o H2/body do CTA final antigo. Detalhes no `copy.txt`.

Paleta (v3): roxo escuro `#3a1652`/`#2c1040` (faixas), roxo medio `#6a3895` (CTA, cards e destaques) e branco. O laranja `#ff8119` ficou no hero (destaque do H1, ponto do selo, checks da lista e circulo tracejado, que voltaram a pedido do time) e em micro-detalhe no resto (linha do eyebrow, setas dos botoes e marcador dos pilares). O time pediu na v3 para tirar o "amarelo": sairam o destaque laranja do H1, o botao laranja do fechamento, a tag laranja, as bordas laranja dos pilares e os circulos tracejados laranja.

**Logos de clientes:** `assets/clientes-a.png` (colunas 1-5) e `assets/clientes-b.png` (colunas 6-9), recortados da imagem que o time enviou. Sao os mesmos clientes da secao "1.000+" da LP gestao-de-influenciadores. Os numeros ficaram em roxo, nao em laranja como na imagem original, porque laranja sobre branco nao passa no contraste e o time pediu menos laranja.

## Decisoes que fogem do padrao (justificar no PR)

- **Form no hero, nao na 2a secao (GUIDELINES §10).** Webinar ToFu pede form na 2a secao, mas o briefing pediu o form ao lado do hero. No mobile ele aparece logo depois do subtitulo.
- **H1 abre pelo ganho, nao pela dor (GUIDELINES §3).** Mantido porque e o gancho do video e veio do briefing. Alternativa pela dor anotada no `copy.txt`. Decisao de quem aprova a copy.
- **JSON-LD `Event` sem `startDate`.** Webinar gravado nao tem data; o Google pode avisar no Rich Results Test.
- **Mais de uma faixa escura (§1/§8 pedem uma so).** O hero e o fechamento sao roxos por pedido explicito (LP "muito branca") e para seguir a referencia da Buzzcreators. A tag rotacionada de urgencia aparece uma vez so.
- **Redes do rodape:** o Buzzcreators so tem Instagram proprio (`@buzzcreatorsbr`, em `brand/buzzcreators/social-media.json`). LinkedIn, YouTube e Facebook sao os da Buzzmonitor, como na LP de referencia.
- **CTA comercial abre em nova aba,** para nao tirar o visitante da LP antes de se inscrever. UTM: `utm_source=webinar&utm_content=captacao-perpetuo-creators-case`.
- **Manifest sem bloco `regions`.** `brand/buzzcreators/brand-manifest.json` ainda esta no formato `websites`: home = `https://buzzcreators.com.br` e o JSON-LD saiu sem `sameAs`. Migrar o manifest resolve.

## Estado

- [x] HTML gerado (testado em 375px: H1 34px, H2 28px, corpo 17px, sem scroll lateral)
- [x] Foto do speaker copiada de `../conheca-o-buzzcreators/assets/bruno-filho.png` para `./assets/bruno-filho.png`
- [x] OG image 1200×630 em `assets/og-webinar-creators-case.png` (arquivo unico, gerado pelo `og-template.html`)
- [ ] GTM: `brand/buzzcreators/tracking.json` esta com container `null`, entao nao foi injetado
- [x] Link da politica de privacidade: `https://buzzmonitor.com.br/privacidade` (o mesmo da LP de referencia)
- [x] v2 com mais cor e mais curta, redes no rodape e CTA comercial com UTM
- [x] v3: laranja reduzido a micro-detalhe e secao de clientes (1.000+ / logos) adicionada
- [ ] Aprovar o design da v2 (inclui a decisao do H1 pelo ganho e o form no hero)
- [x] Revisao (2026-11-11): 6 criticos aplicados. Melhorias e nice-to-haves em [`REVISAO.md`](REVISAO.md)
- [x] Formulario integrado: Jotform exclusivo `263146158898674` (2026-11-11). **Conferir no Jotform** que a Thank You Page redireciona para `https://webinar.buzzmonitor.com/webinar-creators-case-confirmado`.
- [ ] Publicado — `/lp-publicar buzzcreators webinar-creators-case webinar.buzzmonitor.com` (os 2 slugs no manifesto)

## Formulario

**Form provider:** Jotform exclusivo deste webinar, `263146158898674` (integrado em 2026-11-11 via `/lp-integrar-form`).

Campos (definidos no proprio Jotform pelo time): Nome, E-mail corporativo, Empresa, Telefone, Cargo, Nº de colaboradores e a caixa "Não desejo receber newsletter e novidades da Buzzmonitor". Botao "Quero assistir agora". Abaixo do embed fica so o microcopy "Acesso imediato · 12 minutos"; a linha legal do mock saiu porque o form ja traz o opt-out.

Redirect pos-envio: Thank You Page do proprio Jotform, apontando direto para `/webinar-creators-case-confirmado` (sem `data-perpetuo-next`, sem despachante). O JS do mock (validacao + `sessionStorage` com o primeiro nome) saiu junto; a tks agora mostra o titulo generico "Pronto! Seu acesso foi liberado". Nunca submeter o form a partir do preview local: grava lead real.

Historico: em 2026-11-11 o form compartilhado `261904654263661` chegou a ser integrado e foi revertido no mesmo dia. Ele mandava o lead para a tks de social listening e misturava webinars, e o time vetou formulario compartilhado.

## Assets referenciados

- `../../brand/buzzcreators/assets/logos/logo-color.png` (header e footer; PNG por causa do §19)
- `../../brand/buzzcreators/assets/logos/logo-icon.png` (favicon)
- `./assets/bruno-filho.png`
- `./assets/og-webinar-creators-case.png` (OG, resolvida pelo build via `{{OG_IMAGE_PATH}}`)
