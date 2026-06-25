# mcp-na-pratica-p (buzzmonitor)

LP de **webinar perpétuo** no guarda-chuva `webinar.buzzmonitor.com` → https://webinar.buzzmonitor.com/mcp-na-pratica-p
Página de confirmação: `mcp-na-pratica-p-confirmado` → https://webinar.buzzmonitor.com/mcp-na-pratica-p-confirmado

## O que é

Webinar perpétuo **Buzzmonitor MCP** (PT-BR, Brasil). É um recorte do webinar completo de MCP — mostra a Buzzmonitor MCP ao vivo: conectar a conta ao Claude e gerar relatórios de social listening por prompt (menções, tendências, concorrentes, dashboards).

- **Estrutura:** clonada da família de webinar perpétuo `conheca-a-buzzmonitor` (+ `-confirmado`) — form nativo ClickMeeting, não iframe.
- **Copy:** inspirada na LP "Buzzmonitor MCP / MCP na prática" (`landing-pages/buzzmonitor/mcp/`).

## ClickMeeting — roteamento

Form nativo → serverless functions do guarda-chuva (`_clickmeeting-api/`):

- **Série (recurring_config_id):** `17601` — "Buzzmonitor MCP", room_pin 988-444-441, `type:2`/`automated_enabled:1`, tz America/Sao_Paulo, criada 2026-06-23.
- **Chave de roteamento:** `?series=mcp` (mapa `SERIES` em `next-webinar.js`). O front passa `series: 'mcp'` no fetch de `/api/next-webinar` e no body do `/api/clickmeeting-register`.
- **E-mail de confirmação:** idioma default `br` (sem entrada em `SERIES_LANG`, que só desvia ES).
- **sessionStorage key:** `bm_mcp_webinar_confirmation` (distinta das vizinhas BR/ES/BC no mesmo domínio).

### Ordem de deploy INEGOCIÁVEL

1. **Functions primeiro.** A mudança em `_clickmeeting-api/next-webinar.js` (`mcp: '17601'`) tem que estar **no live** antes de publicar a LP. `lp-publicar` NÃO carrega mudança de `api/` (o sync 0.5.d restaura a versão do live), então o deploy da function é manual: `/lp-sync webinar.buzzmonitor.com` → copiar `next-webinar.js` pro `api/` da sibling → `vercel deploy --prod --force`. Sem isso, `?series=mcp` cai no fallback do env (`17529`, Cxpress) e os leads entram no webinar errado.
2. **Depois a LP** (e a `-confirmado`) via `/lp-publicar buzzmonitor mcp-na-pratica-p webinar.buzzmonitor.com`.

## Validação pós-deploy

- `GET /api/next-webinar?series=mcp` → `ok:true` com a sala 17601 (sessão futura).
- `GET /api/next-webinar` (sem série) → continua resolvendo o placeholder do domínio (não quebrou vizinhas).
- Registro com honeypot (`_hp` preenchido) → não cria lead.
- Vizinhas (`/conheca-a-buzzmonitor`, `/atencion-al-cliente-es`, `/conheca-o-buzzcreators`, `/mcp-para-social-listening` etc.) intactas (smoke test do `lp-publicar`).

## Assets

- Logos: brand (`logo-primary.svg`, `logo-reversed.svg`, favicon `logo-icon.png`).
- OG: `assets/og-mcp-na-pratica-p.png` (reaproveitada da LP `mcp/`). No guarda-chuva resolve em `/assets/buzzmonitor/og-mcp-na-pratica-p.png`.

GTM: `GTM-WFJVK858` (Buzzmonitor BR).
