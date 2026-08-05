# que-es-mcp (buzzmonitor)

LP de **webinar perpetuo** ES-LATAM no guarda-chuva `webinar.buzzmonitor.com` → https://webinar.buzzmonitor.com/que-es-mcp
Página de confirmação: `que-es-mcp-confirmado` → https://webinar.buzzmonitor.com/que-es-mcp-confirmado

## O que é

Versão **ES-LATAM** do webinar perpétuo **Buzzmonitor MCP** (irmã da PT-BR `mcp-na-pratica-p`). Mostra a Buzzmonitor MCP ao vivo: conectar a conta ao Claude e gerar reportes de social listening por prompt (menciones, tendencias, competidores, dashboards).

- **Base:** clonada da LP `mcp-na-pratica-p` (PT-BR). Copy traduzida nativamente para ES-LATAM (não-literal), seguindo `conhecimento/linguistico/es-latam/padrao-linguistico.md` + anti-IA (`conhecimento/editorial/regras-anti-ia.md`, anexo ES-LATAM).
- **JS de data/registro:** padrão da `atencion-al-cliente-es` — o endpoint devolve o ISO em `starts_at` e a data é remontada **client-side** em ES (`formatFullEs`, México DF + linha de horários MX/CO/PE/CL/AR). Não usa `formatted_full_pt`.

## Idioma / região

- `<html lang="es-419">`, GTM **`GTM-MKQBX2MG`** (Buzzmonitor LATAM).
- **Atenção ao slug:** `que-es-mcp` **não** tem sufixo `-es`/`-latam`, então a cascata de detecção de região das skills lp-* (CONTEXT §5.1) **não** resolve LATAM pelo slug — resolve pelo `<html lang="es-419">` (passo 2 da cascata). `lp-revisar`/`lp-publicar` usam a cascata completa e acertam o GTM LATAM. `lp-gerar` (que pula o passo 2) cairia em `brasil` — mas esta LP é feita à mão, não via `lp-gerar`, então não se aplica. Manter o `lang` correto é o que garante o GTM certo.

## ClickMeeting — roteamento

Form nativo → serverless functions do guarda-chuva (`_clickmeeting-api/`):

- **Série (recurring_config_id):** `17646` — "Buzzmonitor Que es MCP", room_pin 224-255-882, `type:2`/`automated_enabled:1`, tz **America/Mexico_City**, registration_enabled.
- **Chave de roteamento:** `?series=mcp-es` (mapa `SERIES` em `next-webinar.js`). O front passa `series: 'mcp-es'` no fetch de `/api/next-webinar` e no body do `/api/clickmeeting-register`.
- **E-mail de confirmação:** idioma `es` (entrada `'mcp-es': 'es'` em `SERIES_LANG` no `clickmeeting-register.js`).
- **sessionStorage key:** `bm_mcp_es_confirmation` (distinta das vizinhas BR/ES/BC no mesmo domínio: `bm_mcp_webinar_confirmation`, `bm_atencion_confirmation`).

### Ordem de deploy INEGOCIÁVEL

1. **Functions primeiro.** A mudança em `_clickmeeting-api/next-webinar.js` (`'mcp-es': '17646'`) e em `clickmeeting-register.js` (`SERIES_LANG['mcp-es']='es'`) tem que estar **no live** antes de publicar a LP. `lp-publicar` NÃO carrega mudança de `api/` (o sync 0.5.d restaura a versão do live), então o deploy da function é manual: `/lp-sync webinar.buzzmonitor.com` → copiar os 2 arquivos pro `api/` da sibling → `vercel deploy --prod --force`. Sem isso, `?series=mcp-es` cai no fallback do env (`17529`, Cxpress) e os leads entram no webinar errado.
2. **Depois a LP** (e a `-confirmado`) via `/lp-publicar buzzmonitor que-es-mcp webinar.buzzmonitor.com` + `/lp-publicar buzzmonitor que-es-mcp-confirmado webinar.buzzmonitor.com`.

## Validação pós-deploy

- `GET /api/next-webinar?series=mcp-es` → `ok:true` com a sala 17646 (sessão futura).
- `GET /api/next-webinar` (sem série) → continua resolvendo o placeholder do domínio (não quebrou vizinhas).
- Registro com honeypot (`_hp` preenchido) → não cria lead.
- Vizinhas (`/mcp-na-pratica-p`, `/atencion-al-cliente-es`, `/conheca-a-buzzmonitor`, `/conheca-o-buzzcreators`, `/mcp-para-social-listening` etc.) intactas (smoke test do `lp-publicar`).

## Assets

- Logos: brand (`logo-primary.svg`, `logo-reversed.svg`, favicon `logo-icon.png`).
- OG: `assets/og-que-es-mcp.png` (versão ES — headline "Crea un reporte de social listening con un solo prompt"). No guarda-chuva resolve em `/assets/buzzmonitor/og-que-es-mcp.png`.
- Speaker: `assets/nadia.jpg` (400×400). Foto da Nadia Lezcano (Business Development, Buzzmonitor), seção "Quién presenta". Referenciada no HTML como `./assets/nadia.jpg`; no guarda-chuva resolve em `/assets/buzzmonitor/nadia.jpg` (mesmo asset compartilhado que a LP `agentes-automatizacion-junio-2026-latam` ja usa para a mesma pessoa; md5 idêntico, sem duplicação). Esta LP passa a ser a fonte-verdade do `nadia.jpg` no repo. Substituiu o placeholder "Presentador por confirmar" em 2026-06-30.

GTM: `GTM-MKQBX2MG` (Buzzmonitor LATAM).
