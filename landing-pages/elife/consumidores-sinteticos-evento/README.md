# consumidores-sinteticos-evento (elife)

LP da marca **Elife** no guarda-chuva `content.cxpress.io` -> https://content.cxpress.io/consumidores-sinteticos-evento

Evento presencial "Consumidores Sintéticos: valide antes de investir". Multi-marca no guarda-chuva Cxpress segue o mesmo precedente da LP Buzzcreators em `evento.buzzmonitor.com`: o source vive na pasta da marca da LP (`landing-pages/elife/`), e o namespace de assets no deploy é o da marca (`/assets/elife/...`).

**Origem:** source reconstruido a partir do deploy READY em producao (pull do conteudo live em 2026-06-09), porque a LP existia no ar sem fonte versionada no repo — anti-padrao "LP publicada só na sibling" (landing-pages/CONTEXT.md §7.1). Round-trip validado: source + rewrite do lp-publicar == HTML servido, byte a byte (normalizado). Por isso nao tem `copy.txt`/`REVISAO.md` como uma LP gerada pelo fluxo normal `lp-preparar -> lp-gerar`.

Os logos Elife referenciados (`logo-icon.png`, `logo-reversed.png` + `logo-primary.png`, `logo-reversed.svg`) só existiam no deploy; nesta recuperacao foram trazidos para `brand/elife/assets/logos/` (casa canonica).

Alteracoes futuras: editar os arquivos aqui e publicar via
`/lp-publicar elife consumidores-sinteticos-evento content.cxpress.io`.

## Pendencias conhecidas (pre-existentes, mantidas na copia fiel)

- **FORM MOCK EM PRODUCAO (urgente).** O formulario de inscricao tem `action="#"` + `onsubmit="event.preventDefault()"` — e o mock do `lp-gerar` que nunca passou pelo `/lp-integrar-form`. O evento e em **03/07/2026** (futuro): quem preenche o form no live hoje e descartado em silencio. Corrigir com `/lp-integrar-form elife/consumidores-sinteticos-evento "<snippet do provedor>"` + republicacao. Achado da review do PR #13.
- **Sem GTM.** A LP nao carrega nenhum container. Se a marca Elife tiver ID em `brand/elife/tracking.json`, rodar `/lp-revisar elife/consumidores-sinteticos-evento` injeta automaticamente.
- **og:image 404.** `<meta property="og:image">` aponta para `https://content.cxpress.io/assets/og-image.png`, que nao existe no deploy (HTTP 404 confirmado em 2026-06-09).
- **JSON-LD com logo de outra marca.** `Organization.logo` aponta para `https://content.cxpress.io/assets/logos/logo-primary.svg`, que e o logo legacy **Cxpress**, nao o da Elife.

As 4 pendencias se corrigem numa futura passada de `/lp-integrar-form` + `/lp-revisar` + republicacao — nao foram alteradas aqui para manter o source identico ao live.
