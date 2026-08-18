# LP Cxpress — webinar-canales-unificados

**Gerado em:** 2026-08-18
**Copy-fonte:** `copy.txt` (usuario reescreveu a partir do rascunho v1 de 2026-08-03, backup em `copy.txt.2026-08-03_bak`)
**Design espelhado:** `landing-pages/cxpress/webinar-bloqueo-whatsapp/index.html` (versao atual, ja com os PRs #249-#259 de polimento visual), a pedido explicito do usuario ("sigue el mismo diseño de la anterior" / "buscamos hacer un diseño similar a este")
**Regiao:** latam (es-419) · GTM-WRQ47B9R · Pixel LATAM 1484678896147110
**Dominio:** content.cxpress.io (guarda-chuva migrado pro CI)

## Decisoes tomadas nesta sessao

1. **Dado "9 canales" sem citacao:** o rascunho v1 citava a fonte ("Salesforce, State of the Connected Customer"), mas a copy final do usuario trouxe o mesmo dado sem a citacao. Mantida a atribuicao a Salesforce (mesma fonte do guiao original), seguindo o mesmo criterio ja aplicado na LP anterior desta serie e a regra do Brandbook Cxpress ("nao afirmar resultados cuantitativos sem case verificado, usar dados de mercado como gancho").
2. **Design espelhado da versao MAIS RECENTE de `webinar-bloqueo-whatsapp`** (nao da versao original que eu tinha gerado) — o usuario apontou a URL ao vivo como referencia. Essa versao evoluiu (fora desta sessao, PRs #249-#259) para ter uma imagem flutuante no hero e um mockup de celular no CTA final (layout 2 colunas), mas com graficos especificos de WhatsApp (`Icone_WhatsApp.svg`, `Celular_WhatsApp.svg`) que nao fazem sentido tematico aqui (esta LP e sobre centralizacao de canais, nao especificamente WhatsApp). Reproduzida a MESMA composicao visual (imagem no hero acima do formulario + mockup no CTA final em grid 2 colunas), trocando os assets por imagens reais e ja existentes da propria plataforma Cxpress:
   - Hero: `brand/cxpress/assets/plataforma/plataforma-canais.gif` (animacao mostrando os canais de atencao integrados no mesmo painel — ja usada em `banimento-whatsapp-latam` e outras LPs Cxpress).
   - CTA final: `brand/cxpress/assets/plataforma/mockup-plataforma-laptop.png` (mockup de laptop com a plataforma).
   - Nenhum asset novo foi criado nem baixado — ambos ja existiam no repo, sem nenhuma questao de marca registrada (sao capturas do proprio produto Cxpress).
3. **Speaker reaproveitada:** Laura Rodriguez, Business Developer · Cxpress — mesma speaker da LP anterior, foto copiada de `webinar-bloqueo-whatsapp/assets/laura-rodriguez.jpg`.
4. **CTA sem exclamacao:** a copy do usuario trouxe "Inscríbete gratis al webinar" (sem "¡...!"), mantido literal nas 3 ocorrencias (header, hero, CTA final) — nenhuma pontuacao adicionada por conta propria.
5. **Troca de imagens (2026-08-18, pos-publicacao):** usuario pediu trocar as duas imagens de lugar: (a) o gif `plataforma-canais.gif` (que estava no hero) foi movido pro CTA final, substituindo `mockup-plataforma-laptop.png`; (b) uma imagem nova enviada pelo usuario (`Webinar canales.png`, fila de icones de telefone/Facebook/WhatsApp/Instagram/correo/Messenger) foi pra o hero, no lugar onde estava o gif. A imagem original (1920x1080, com bastante espaco vazio) foi recortada pro bounding box real do conteudo (1822x272) antes de usar, e o `.hero-media-card` perdeu a moldura de "screenshot" (borda/sombra/overflow) porque agora e uma fila de icones com fundo transparente, nao uma captura de tela. Nenhum texto da copy foi alterado, so as imagens.

## Estrutura

- HERO (kicker + h1 + body + "10 minutos" + imagem da plataforma + formulario mock de inscricao)
- LO QUE VAS A VER — 3 cards numerados (01-03) com callout "Qué vas a ver"
- RESULTADOS — 3 stat cards (numero + label)
- QUIEN PRESENTA — Laura Rodriguez, Business Developer · Cxpress
- PARA QUIÉN ES — grid 2x2 (4 itens)
- CTA FINAL — grid 2 colunas: conteudo (h2 + body + 3 labels + CTA) + mockup do laptop
- Footer

## Estado

- [x] HTML gerado
- [x] Revisao tecnica (em-dash: 0, ellipsis `&hellip;` OK, GTM 2/2, Pixel 1x, `check_gtm_region.py` OK, fidelidade de copy conferida via texto renderizado) — ver `REVISAO.md`
- [ ] CTA integrado com link/embed real de inscricao — rodar `/lp-integrar-form` quando tiver o link
- [ ] Publicacao — pendente PR via fluxo CI (`content.cxpress.io` esta no guarda-chuva migrado)

## Pendencias

1. **Formulario de inscricao** e mock (sem backend real) — mesmo padrao das demais LPs de webinar desta serie.
2. **OG image** — nao gerada, aponta pro logo da marca via `{{BRAND_LOGO_PNG_PATH}}`.
3. `{{DOMAIN}}` e `{{BRAND_LOGO_PNG_PATH}}` sao placeholders resolvidos no fluxo de publicacao (CI).

## Assets referenciados

- `../../brand/cxpress/assets/logos/logo-primary.svg`, `logo-reversed.svg`, `logo-icon.png`
- `../../brand/cxpress/assets/plataforma/plataforma-canais.gif` (asset de marca ja existente, reaproveitado)
- `../../brand/cxpress/assets/plataforma/mockup-plataforma-laptop.png` (asset de marca ja existente, reaproveitado)
- `./assets/laura-rodriguez.jpg` (LP-local, reaproveitado de `webinar-bloqueo-whatsapp/assets/`)
