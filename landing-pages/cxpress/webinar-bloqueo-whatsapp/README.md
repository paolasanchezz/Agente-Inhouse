# LP Cxpress — webinar-bloqueo-whatsapp

**Gerado em:** 2026-08-10
**Copy-fonte:** `copy.txt` (usuario reescreveu o copy completo; havia um rascunho v1 de 2026-08-03 com o mesmo topico, que ficou sem uso — o v1 tinha CTA BoFu "Agenda tu demo gratuita", o final e ToFu "Inscribete al webinar")
**Design espelhado:** `landing-pages/buzzmonitor/primer-listening-5-pasos/index.html` (a pedido explicito do usuario), com branding **Cxpress LATAM** (`brand/cxpress/tokens.json`) no lugar de Buzzmonitor
**Regiao:** latam (es-419) · GTM-WRQ47B9R (mesmo GTM usado nas demais LPs `*-latam` do Cxpress)
**Dominio:** content.cxpress.io (guarda-chuva migrado pro CI)

## Decisoes tomadas nesta sessao

1. **Marca cruzada (Buzzmonitor -> Cxpress):** usuario pediu explicitamente pra copiar a estrutura/design de uma LP Buzzmonitor mas aplicar o branding Cxpress. Tokens trocados 1:1: cores (`--primary:#4A69BD`, `--primary-dark:#232960`, `--accent:#EF863C`), fontes (Open Sans / Source Sans 3, no lugar de League Spartan / Lato / Manrope), sombras retintadas com o RGB do primary-dark do Cxpress (35,41,96), seguindo a mesma convencao ja usada em `banimento-whatsapp-latam` (LP Cxpress existente).
2. **Dado "200 milhoes de empresas" vs "175 milhoes de pessoas/dia":** o rascunho v1 tinha uma duvida nao resolvida sobre isso (fontes distintas: Meta 2020 "175M pessoas escrevem/dia" vs. o bloco final "200M empresas usam o app"). Perguntado ao usuario via AskUserQuestion; confirmado explicitamente manter "200 millones de empresas" como veio na copy final.
3. **Secao RESULTADOS com stat cards (numero grande + label):** o modelo de referencia (`primer-listening-5-pasos`) NAO tem secao de resultados, mas a copy do usuario trouxe uma (3 stats). Adicionada seguindo a logica "copy dita estrutura" (mesma usada em `gestion-crisis`). Pra dar destaque aos numeros, cada LABEL foi dividido visualmente em numero grande + texto (ex: "200 millones" + "de empresas ya usan WhatsApp Business") sem alterar nenhuma palavra — a concatenacao reconstrói a frase original literal.
4. **Imagem ilustrativa de "WhatsApp bloqueado":** usuario pediu pra adicionar imagens referentes ao WhatsApp bloqueado. Em vez de usar uma captura real da interface do WhatsApp (risco de marca registrada/direitos autorais da Meta, e nao ha como baixar de fonte confiavel dentro das regras da sessao), foi construida uma ilustracao propria em HTML/CSS/SVG, posicionada no hero, acima do formulario de inscricao (`.blocked-icon`, `role="img"` com `aria-label` descritivo).
   - **Iteracao 1:** um "mockup" de chat generico em caixa escura (avatar, linhas, bolhas de mensagem) com overlay de texto.
   - **Iteracao 2 (final):** usuario enviou uma imagem de referencia contendo o logo oficial do WhatsApp com um circulo de proibicao, pedindo pra aumentar o elemento e tirar o fundo/caixa. Foi explicado ao usuario que o logo oficial do WhatsApp (marca registrada da Meta, imagem de origem nao confirmada) nao pode ser reproduzido numa peca comercial da Cxpress. Reconstruido como um icone grande (200x200px) **sem caixa/fundo**: circulo vermelho de proibicao sobre um icone generico de balao de chat (SVG proprio, nao o logo do WhatsApp), mantendo o mesmo texto de apoio "Cuenta suspendida / Por uso no autorizado de la aplicación" abaixo.
5. **Foto de Laura Rodriguez:** enviada pelo usuario no chat, localizada em Downloads por timestamp recente (`1624464380385 (1) (1).jpg`, JPEG 400x400), confirmada visualmente antes de copiar pra `assets/laura-rodriguez.jpg`.
6. **CTA longo ("¡Inscríbete y aprende cómo evitar que bloqueen tu WhatsApp!"):** mantido literal nas 3 ocorrencias (header, hero, CTA final), sem parafrasear pra encurtar. Ajustes de CSS feitos so nesta pagina pra acomodar o texto longo: `.btn` e `.header-cta` com `white-space: normal` (permite quebra de linha) e sem `text-transform: uppercase` (que deixaria uma frase inteira em caixa alta, ilegivel).
7. **Sem hreflang:** nao ha LP-irma em outro idioma pra este slug — omitido, so `canonical` presente (GUIDELINES §16).
8. **Meta Pixel (2026-08-11, pos-publicacao):** usuario pediu confirmacao/adicao do Meta Pixel LATAM (`1484678896147110`). O HTML gerado nao trazia Pixel (so GTM), pois o modelo de referencia `primer-listening-5-pasos` (Buzzmonitor) tambem so usa GTM. Verificado que o Pixel nao e um padrao universal nas LPs `*-latam` do Cxpress (so `atencion-clinicas-latam` e `whatsapp-business-smb-latam` tinham antes desta LP) — mesmo assim, adicionado o snippet identico (script + noscript) logo apos o bloco GTM, com o ID confirmado pelo usuario.

## Estrutura

- HERO (kicker + h1 + body + "10 minutos" + ilustracao "WhatsApp bloqueado" + formulario mock de inscricao)
- LO QUE VAS A VER — 3 cards numerados (01-03) com callout "Qué vas a ver"
- RESULTADOS — 3 stat cards (numero + label)
- QUIEN PRESENTA — Laura Rodriguez, Business Developer · Cxpress
- PARA QUIÉN ES — grid 2x2 (4 itens)
- CTA FINAL — h2 + body + 2 labels + CTA (mock, aguardando link real de inscricao)
- Footer

## Estado

- [x] HTML gerado
- [x] Revisao tecnica (em-dash: 0, ellipsis: 1 ocorrencia como `&hellip;`, GTM 2/2, `check_gtm_region.py` OK, fidelidade de copy conferida via texto renderizado) — ver `REVISAO.md`
- [ ] CTA integrado com link/embed real de inscricao — rodar `/lp-integrar-form` quando tiver o link
- [ ] Publicacao — pendente PR via fluxo CI (`content.cxpress.io` esta no guarda-chuva migrado)

## Pendencias

1. **Formulario de inscricao** e mock (sem backend real) — mesmo padrao das demais LPs de webinar desta serie.
2. **OG image** — nao gerada, aponta pro logo da marca via `{{BRAND_LOGO_PNG_PATH}}`.
3. `{{DOMAIN}}` e `{{BRAND_LOGO_PNG_PATH}}` sao placeholders resolvidos no fluxo de publicacao (CI).

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-primary.svg`, `logo-reversed.svg`, `logo-icon.png`
- `./assets/laura-rodriguez.jpg` (LP-local, enviada pelo usuario em 2026-08-10)
