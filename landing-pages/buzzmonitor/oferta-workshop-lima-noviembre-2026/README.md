# LP Buzzmonitor — oferta-workshop-lima-noviembre-2026

Oferta pos-evento do workshop presencial "El valor del tiempo" (Lima, 19/11/2026, Nobility Grand Hotel). LP de inscricao do evento: `buzzmonitor/workshop-lima-noviembre-2026` (evento.buzzmonitor.com).

**Gerado em:** 2026-11-04
**Copy-fonte:** `copy.txt`
**Idioma / regiao:** ES-LATAM (`es-419`) · GTM `GTM-MKQBX2MG`
**Dominio destino:** `content.buzzmonitor.com` (guarda-chuva migrado pro CI, mesmo das ofertas de Bogota e CDMX)

## Origem

- **Oferta e estrutura:** `buzzmonitor/oferta-workshop-reportes-cdmx-octubre-2026` (15 dias gratis + soporte consultivo + primer panel configurado + 50% nas 2 primeiras mensalidades; form Jotform `241825239057661`; hero → oferta → consecuencia → beneficios → modulos → prova social → urgencia → form).
- **Estilo visual:** herdado da LP de inscricao do workshop de Lima (mesmo bloco CSS `.bzlm`): hero roxo profundo com trama de pontos e spotlight, H1 com destaque amarelo/laranja animado, ticket flutuante com relogio (aqui virou o "ticket da oferta": 15 dias gratis), kicker com anel, cards creme com numero em gradiente e barra no topo, secao escura de lista numerada (Skills), cards de icone colorido (modulos), secao de fecho roxa com box de info, form-card com borda laranja, footer `#13001c` com redes.
- **Copy:** o tema da LP do CDMX era crise; aqui foi readaptado ao tema do workshop de Lima (tempo, sinais, decisoes, 6 IAs + 7 Skills). Condicoes da oferta mantidas.

## Decisoes

- Form na **ultima secao** (BoFu/remarketing, GUIDELINES §10), CTA no hero e na barra.
- Botao laranja usa `--orange-dark` (`#CE5F14`) como fundo em vez do `#EB7C2E` da LP de Lima, pra melhorar contraste do texto branco.
- Pisos tipograficos mobile aplicados (`bump_mobile_type.py`). Sem overflow horizontal em 375 e 1440.
- Links de redes no footer seguem o `brand-manifest.json` LATAM (buzzmonitor.es / buzzmonitor_es), nao os antigos da LP de Lima.

## Pendencias

- [ ] **Data limite da oferta: 28 de novembro e um SUPOSTO** (mesmo intervalo de 9 dias usado no CDMX: evento 28/10 → oferta ate 6/11). Confirmar. Aparece na barra, ticket do hero, oferta, urgencia (2x) e OG image.
- [ ] Publicar: PR com source + entrada no `landing-pages/dominios/content-buzzmonitor-com/manifest.json` (o CI deploya).

## Assets

- `../../brand/buzzmonitor/assets/logos/logo-reversed.svg` (barra e footer), `logo-icon.png` (favicon)
- `./assets/logos/mural-{1,2}.jpeg` (mural de clientes, copiados da oferta CDMX)
- `./assets/og-oferta-workshop-lima-noviembre-2026.png` (OG 1200×630, gerada no estilo do hero)
