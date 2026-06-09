# Brief: Form custom ClickMeeting + LP fixa dinâmica — `conheca-a-cxpress`

Prompt self-contained para implementar a integração da LP `conheca-a-cxpress` com a API do ClickMeeting. Decisões arquiteturais já foram tomadas — siga este brief literalmente.

---

## 1. Missão

Substituir o iframe `<script src="https://embed.clickmeeting.com/embed_conference.html?r=18264519010002406...">` da LP `landing-pages/cxpress/conheca-a-cxpress/index.html` por um **form HTML custom** estilizado com os tokens da marca Cxpress, que registra o lead via **API REST do ClickMeeting** (server-side proxy). A LP é **fixa** (uma URL só, sem deploy diário) e resolve o `room_id` + data/hora do próximo webinar em runtime via API.

---

## 2. Premissas validadas (não re-verificar — já foi feito GET na API)

- **Webinar Cxpress (atual)**: `id=10003144`, `room_pin=321743856` (formato amigável `321-743-856`), `starts_at=2026-06-10T11:05:00-03:00`, `recurring_config_id=17497`, `automated_enabled=1`, `type=2`.
- **`registration_enabled: 1`** → aceita registro via API.
- **`thank_you_page_url`**: `https://home.cxpress.io/webinar-inscricao-realizada`.
- **`thank_you_emails_enabled: true`** → ClickMeeting já manda email de confirmação automaticamente.
- O webinar é **automated/recurring** → quando a sessão atual acaba, o ClickMeeting cria automaticamente a próxima. `GET /v1/conferences/active` sempre retorna a próxima sessão ativa. **NÃO faça hardcode** do `room_id`.

---

## 3. Decisões arquiteturais (não questionar — já alinhadas)

| Decisão | Escolha |
|---|---|
| Onde fica a serverless function | Dentro do guarda-chuva `content.cxpress.io` (mesmo projeto Vercel das outras LPs Cxpress) — `api/*.js` na root do sibling |
| Campos do form | Apenas os 4 padrão da API ClickMeeting: nome, sobrenome, email, empresa |
| Como exibir data/hora do webinar | **Client-side fetch** com skeleton (não usar Vercel Cron) |
| Buffer mínimo antes do webinar | **0 minutos** — aceita registro até o `starts_at` do webinar |
| Custom fields | NÃO existem na API — não tentar enviar campos extras |

---

## 4. Endpoints / API ClickMeeting (referência)

Base: `https://api.clickmeeting.com/v1/`

Headers obrigatórios em toda chamada:
```
X-Api-Key: {CLICKMEETING_API_KEY}
```
⚠️ Essa key **JAMAIS** pode ir pro código-fonte, git, console.log, ou ser exposta ao client. Use exclusivamente env var.

### Endpoints usados

**GET `/conferences/active`** — Lista webinars ativos.
- Resposta: array de objetos com `id`, `room_pin`, `name`, `starts_at`, `ends_at`, `timezone`, `recurring_config_id`, etc.

**POST `/conferences/{room_id}/registration`** — Registra participante.
- Header extra: `Content-Type: application/x-www-form-urlencoded`
- Body (urlencoded):
  - `registration[1]` = primeiro nome (obrigatório)
  - `registration[2]` = sobrenome (obrigatório)
  - `registration[3]` = email (obrigatório)
  - `registration[10]` = empresa (opcional)
  - `confirmation_email[enabled]` = `1`
  - `confirmation_email[lang]` = `br`
- Resposta sucesso: `{ "status": "OK", "url": "https://...clickmeeting.com/123/?r=ZGN..." }`
- A `url` retornada é a URL única de acesso do participante — passar pro client como redirect.

---

## 5. Arquitetura

```
content.cxpress.io/  (sibling do projeto Vercel cxpress-lp-playbook-whatsapp2026)
├── conheca-a-cxpress/
│   └── index.html               ← form HTML custom + JS de fetch
├── playbook-whatsapp2026/...    ← vizinhas NÃO mexer
├── webinar-tecnologia-maio2026/...
├── livraria/...
├── latam-webinar-atencionalcliente/...
├── ebook-marketing-conversacion-latam/...
├── webinar-tecnologia-maio2026-oferta/...
└── api/                         ← NOVA pasta na root do projeto Vercel
    ├── next-webinar.js          ← GET — retorna próximo webinar
    └── clickmeeting-register.js ← POST — registra lead
```

Endpoints finais:
- `GET https://content.cxpress.io/api/next-webinar`
- `POST https://content.cxpress.io/api/clickmeeting-register`

---

## 6. Implementação — Function 1: `api/next-webinar.js`

**Objetivo**: retornar dados do próximo webinar ativo (com filtro de buffer).

**Pseudo-spec**:
```js
export default async function handler(req, res) {
  if (req.method !== 'GET') return res.status(405).json({ ok: false, error: 'Method not allowed' });

  const apiKey = process.env.CLICKMEETING_API_KEY;
  const recurringConfigId = process.env.CLICKMEETING_RECURRING_CONFIG_ID; // "17497" (filtro opcional)
  const bufferMinutes = parseInt(process.env.MIN_BUFFER_MINUTES || '0', 10);

  if (!apiKey) return res.status(500).json({ ok: false, error: 'Config error' });

  try {
    const r = await fetch('https://api.clickmeeting.com/v1/conferences/active', {
      headers: { 'X-Api-Key': apiKey }
    });
    if (!r.ok) throw new Error(`API ${r.status}`);
    const conferences = await r.json();

    const now = Date.now();
    const bufferMs = bufferMinutes * 60 * 1000;

    // Filtra: só sessões cujo starts_at > NOW + buffer
    // Filtra opcionalmente por recurring_config_id (se env var setada)
    const eligible = conferences
      .filter(c => {
        const starts = new Date(c.starts_at).getTime();
        if (starts <= now + bufferMs) return false;
        if (recurringConfigId && String(c.recurring_config_id) !== recurringConfigId) return false;
        return true;
      })
      .sort((a, b) => new Date(a.starts_at) - new Date(b.starts_at));

    if (eligible.length === 0) {
      return res.status(200).json({
        ok: false,
        error: 'no_upcoming',
        message: 'Próxima sessão sendo agendada. Entre em contato: contato@cxpress.io'
      });
    }

    const next = eligible[0];
    const startsAt = new Date(next.starts_at);

    // Cache de 5 min (Vercel CDN)
    res.setHeader('Cache-Control', 'public, max-age=300, s-maxage=300, stale-while-revalidate=600');

    return res.status(200).json({
      ok: true,
      room_id: next.id,
      starts_at: next.starts_at,
      formatted_date_pt: formatDatePt(startsAt),  // ex: "10 de junho"
      formatted_time_pt: formatTimePt(startsAt),  // ex: "11h05"
      formatted_full_pt: formatFullPt(startsAt),  // ex: "Quarta, 10 de junho · 11h05 (horário de Brasília)"
      timezone: next.timezone || 'America/Sao_Paulo'
    });
  } catch (err) {
    console.error('next-webinar error:', err);
    return res.status(500).json({ ok: false, error: 'fetch_failed' });
  }
}

function formatDatePt(d) {
  return new Intl.DateTimeFormat('pt-BR', { day: '2-digit', month: 'long', timeZone: 'America/Sao_Paulo' }).format(d);
}
function formatTimePt(d) {
  return new Intl.DateTimeFormat('pt-BR', { hour: '2-digit', minute: '2-digit', timeZone: 'America/Sao_Paulo' }).format(d).replace(':', 'h');
}
function formatFullPt(d) {
  const weekday = new Intl.DateTimeFormat('pt-BR', { weekday: 'long', timeZone: 'America/Sao_Paulo' }).format(d);
  return `${capitalize(weekday)}, ${formatDatePt(d)} · ${formatTimePt(d)} (horário de Brasília)`;
}
function capitalize(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
```

---

## 7. Implementação — Function 2: `api/clickmeeting-register.js`

**Objetivo**: validar payload, resolver `room_id` corrente (chamando `/api/next-webinar` internamente — não confia no client), registrar lead na API ClickMeeting, retornar URL única.

**Pseudo-spec**:
```js
export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'Method not allowed' });

  const apiKey = process.env.CLICKMEETING_API_KEY;
  if (!apiKey) return res.status(500).json({ ok: false, error: 'Config error' });

  const { first_name, last_name, email, company, _hp } = req.body || {};

  // Honeypot: bots geralmente preenchem todos os campos
  if (_hp) return res.status(200).json({ ok: true, redirect_url: 'https://home.cxpress.io/webinar-inscricao-realizada' });

  // Validações
  if (!first_name || !last_name || !email) {
    return res.status(400).json({ ok: false, error: 'missing_fields', message: 'Preencha nome, sobrenome e email.' });
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ ok: false, error: 'invalid_email', message: 'Email inválido.' });
  }
  if (first_name.length > 100 || last_name.length > 100 || email.length > 200 || (company && company.length > 200)) {
    return res.status(400).json({ ok: false, error: 'too_long' });
  }

  // Resolve room_id via next-webinar (mesma function host, fetch interno)
  let roomId;
  try {
    const proto = req.headers['x-forwarded-proto'] || 'https';
    const host = req.headers['x-forwarded-host'] || req.headers.host;
    const nw = await fetch(`${proto}://${host}/api/next-webinar`);
    const nwData = await nw.json();
    if (!nwData.ok) {
      return res.status(503).json({ ok: false, error: 'no_webinar', message: 'Nenhum webinar disponível no momento. Tente novamente em alguns minutos.' });
    }
    roomId = nwData.room_id;
  } catch (err) {
    console.error('resolve room_id failed:', err);
    return res.status(503).json({ ok: false, error: 'resolve_failed' });
  }

  // Registra no ClickMeeting
  try {
    const body = new URLSearchParams({
      'registration[1]': first_name.trim(),
      'registration[2]': last_name.trim(),
      'registration[3]': email.trim().toLowerCase(),
      'confirmation_email[enabled]': '1',
      'confirmation_email[lang]': 'br'
    });
    if (company && company.trim()) body.append('registration[10]', company.trim());

    const r = await fetch(`https://api.clickmeeting.com/v1/conferences/${roomId}/registration`, {
      method: 'POST',
      headers: {
        'X-Api-Key': apiKey,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: body.toString()
    });

    const data = await r.json().catch(() => ({}));

    if (!r.ok || data.status !== 'OK') {
      console.error('ClickMeeting registration failed:', r.status, data);
      // Email já registrado é caso comum — checar mensagem da API e tratar com mensagem amigável
      if (data.message && /exist|already|duplicate/i.test(JSON.stringify(data))) {
        return res.status(409).json({ ok: false, error: 'already_registered', message: 'Este email já está inscrito neste webinar.' });
      }
      return res.status(502).json({ ok: false, error: 'cm_failed', message: 'Não foi possível concluir sua inscrição. Tente novamente.' });
    }

    return res.status(200).json({
      ok: true,
      redirect_url: data.url || 'https://home.cxpress.io/webinar-inscricao-realizada'
    });
  } catch (err) {
    console.error('register error:', err);
    return res.status(500).json({ ok: false, error: 'internal' });
  }
}

// Necessário em algumas versões da Vercel pra parsing automático do body JSON:
// O default já parseia JSON automaticamente; se não estiver, adicionar manualmente.
```

---

## 8. Implementação — Form HTML/CSS/JS na LP

Arquivo: `landing-pages/cxpress/conheca-a-cxpress/index.html`

### 8.1 — Remover (linhas 929-931):
```html
<div class="clickmeeting-embed">
  <script type="text/javascript" src="https://embed.clickmeeting.com/embed_conference.html?r=18264519010002406&w=1024&h=768"></script>
</div>
```

### 8.2 — Remover do CSS (linhas ~400-408 e ~843):
```css
.hero-form .clickmeeting-embed { min-height: 380px; }
.hero-form .clickmeeting-embed iframe { width: 100% !important; min-height: 380px; border: 0; display: block; }
.clickmeeting-embed iframe { width: 100% !important; max-width: 100% !important; border: 0; display: block; }
```

### 8.3 — Inserir no lugar do iframe (dentro de `.hero-form`, após `.hero-form-head` e antes de `.hero-form-note`):

```html
<!-- Webinar info dinâmico (preenchido via /api/next-webinar) -->
<div class="webinar-info" data-state="loading">
  <span class="webinar-info-skeleton" aria-hidden="true"></span>
  <span class="webinar-info-text"></span>
</div>

<form class="cm-form" id="cmForm" novalidate>
  <div class="cm-form-row cm-form-row-2col">
    <label class="cm-field">
      <span class="cm-label">Nome</span>
      <input type="text" name="first_name" required autocomplete="given-name" maxlength="100">
    </label>
    <label class="cm-field">
      <span class="cm-label">Sobrenome</span>
      <input type="text" name="last_name" required autocomplete="family-name" maxlength="100">
    </label>
  </div>
  <label class="cm-field">
    <span class="cm-label">Email corporativo</span>
    <input type="email" name="email" required autocomplete="email" maxlength="200">
  </label>
  <label class="cm-field">
    <span class="cm-label">Empresa <span class="cm-optional">(opcional)</span></span>
    <input type="text" name="company" autocomplete="organization" maxlength="200">
  </label>
  <!-- Honeypot anti-spam -->
  <input type="text" name="_hp" tabindex="-1" autocomplete="off" aria-hidden="true" class="cm-honeypot">
  <button type="submit" class="cm-submit">Garantir minha vaga</button>
  <p class="cm-feedback" role="status" aria-live="polite"></p>
</form>
```

### 8.4 — CSS a adicionar (mantendo tokens existentes da LP `--primary`, `--accent`, etc):

```css
/* Webinar info dinâmico */
.webinar-info {
  display: flex; align-items: center; gap: 8px;
  font-size: 14px; font-weight: 600;
  color: var(--primary, #4A69BD);
  background: rgba(74, 105, 189, 0.08);
  padding: 10px 14px; border-radius: 8px;
  margin-bottom: 16px;
  min-height: 42px;
}
.webinar-info[data-state="loading"] .webinar-info-skeleton {
  display: inline-block;
  width: 180px; height: 16px;
  background: linear-gradient(90deg, rgba(74,105,189,0.1) 0%, rgba(74,105,189,0.2) 50%, rgba(74,105,189,0.1) 100%);
  background-size: 200% 100%;
  animation: cm-skeleton 1.4s infinite;
  border-radius: 4px;
}
.webinar-info[data-state="ready"] .webinar-info-skeleton { display: none; }
.webinar-info[data-state="ready"] .webinar-info-text { opacity: 0; animation: cm-fadein 0.4s ease forwards; }
@keyframes cm-skeleton {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
@keyframes cm-fadein { to { opacity: 1; } }

/* Form */
.cm-form { display: flex; flex-direction: column; gap: 14px; }
.cm-form-row-2col { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
@media (max-width: 480px) { .cm-form-row-2col { grid-template-columns: 1fr; } }
.cm-field { display: flex; flex-direction: column; gap: 6px; }
.cm-label {
  font-size: 13px; font-weight: 600;
  color: #333; letter-spacing: 0.01em;
}
.cm-optional { color: #888; font-weight: 400; }
.cm-field input {
  padding: 12px 14px; border: 1.5px solid #d8dce5; border-radius: 8px;
  font-size: 15px; font-family: inherit; color: #1a1a1a;
  background: #fff; transition: border-color 0.15s, box-shadow 0.15s;
}
.cm-field input:focus {
  outline: none; border-color: var(--primary, #4A69BD);
  box-shadow: 0 0 0 3px rgba(74,105,189,0.15);
}
.cm-field input:invalid:not(:placeholder-shown) { border-color: #d9534f; }
.cm-honeypot { position: absolute !important; left: -9999px !important; opacity: 0; pointer-events: none; }
.cm-submit {
  margin-top: 4px;
  padding: 14px 20px; border: 0; border-radius: 8px;
  background: var(--accent, #EF863C); color: #fff;
  font-size: 16px; font-weight: 700; letter-spacing: 0.01em;
  cursor: pointer; transition: background 0.15s, transform 0.05s;
}
.cm-submit:hover:not(:disabled) { background: #e07028; }
.cm-submit:active:not(:disabled) { transform: translateY(1px); }
.cm-submit:disabled { background: #b8b8b8; cursor: not-allowed; }
.cm-feedback {
  margin: 4px 0 0; font-size: 13px; min-height: 18px;
  color: #d9534f;
}
.cm-feedback[data-state="success"] { color: #2e7d4f; }
```

### 8.5 — JS a adicionar (antes do `</body>`):

```html
<script>
(function() {
  // 1. Preenche webinar info no carregamento
  const info = document.querySelector('.webinar-info');
  const infoText = info?.querySelector('.webinar-info-text');

  fetch('/api/next-webinar')
    .then(r => r.json())
    .then(data => {
      if (!data.ok) {
        info.dataset.state = 'ready';
        infoText.textContent = data.message || 'Próxima sessão em breve';
        return;
      }
      infoText.textContent = data.formatted_full_pt;
      info.dataset.state = 'ready';
    })
    .catch(() => {
      info.dataset.state = 'ready';
      infoText.textContent = 'Próxima sessão · Online · Vagas limitadas';
    });

  // 2. Submit handler
  const form = document.getElementById('cmForm');
  const submitBtn = form.querySelector('.cm-submit');
  const feedback = form.querySelector('.cm-feedback');
  const submitDefaultText = submitBtn.textContent;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    feedback.textContent = '';
    feedback.dataset.state = '';

    const fd = new FormData(form);
    const payload = {
      first_name: fd.get('first_name'),
      last_name: fd.get('last_name'),
      email: fd.get('email'),
      company: fd.get('company') || '',
      _hp: fd.get('_hp') || ''
    };

    // Validação client-side rápida
    if (!payload.first_name || !payload.last_name || !payload.email) {
      feedback.textContent = 'Preencha nome, sobrenome e email.';
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Enviando...';

    try {
      const r = await fetch('/api/clickmeeting-register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await r.json();

      if (data.ok && data.redirect_url) {
        // dataLayer pra GTM
        if (window.dataLayer) {
          window.dataLayer.push({ event: 'webinar_lead_submitted', form_id: 'cmForm' });
        }
        feedback.dataset.state = 'success';
        feedback.textContent = 'Inscrição confirmada! Redirecionando...';
        setTimeout(() => { window.location.href = data.redirect_url; }, 600);
      } else {
        feedback.textContent = data.message || 'Não foi possível concluir sua inscrição. Tente novamente.';
        submitBtn.disabled = false;
        submitBtn.textContent = submitDefaultText;
      }
    } catch (err) {
      feedback.textContent = 'Erro de conexão. Verifique sua internet e tente novamente.';
      submitBtn.disabled = false;
      submitBtn.textContent = submitDefaultText;
    }
  });
})();
</script>
```

---

## 9. Env vars no painel Vercel

Projeto: `cxpress-lp-playbook-whatsapp2026` (o projeto que serve o guarda-chuva `content.cxpress.io`).

Configurar em **Production + Preview + Development**:

| Variável | Valor |
|---|---|
| `CLICKMEETING_API_KEY` | `{CLICKMEETING_API_KEY}` |
| `CLICKMEETING_RECURRING_CONFIG_ID` | `17497` |
| `MIN_BUFFER_MINUTES` | `0` |

⚠️ **NUNCA** commitar essa key. Nunca colocar em `.env` versionado. Nunca em log de console no client.

---

## 10. CSP — não precisa mexer

O `vercel.template.json` do `lp-publicar` já tem `connect-src 'self'`, que cobre o fetch da LP pras functions na mesma origem. Como o `<script>` do `embed.clickmeeting.com` será removido, **não há nova regra de CSP a adicionar**.

Antes do deploy, **verificar** se o `vercel.json` em produção do sibling tem alguma referência a `*.clickmeeting.com` (resquício de outra LP) — se tiver, pode deixar (não atrapalha) ou limpar.

---

## 11. Plano de testes (executar em ordem)

### Fase A — Local
1. `cd` pra sibling local do projeto guarda-chuva (consultar `landing-pages/CONTEXT.md` §4 pro caminho exato — provavelmente `$env:DASHBOARD_SIBLING_BASE\..\cxpress-lp-playbook-whatsapp2026\` ou similar)
2. `vercel env pull .env.local`
3. `vercel dev` na porta 3000
4. Abrir `http://localhost:3000/conheca-a-cxpress/`
5. Verificar:
   - Form custom renderiza (sem iframe)
   - Skeleton aparece e depois exibe data/hora do webinar (`"Quarta, 10 de junho · 11h05"`)
6. Preencher com dados de teste (`teste-claude+webinar1@cxpress.io`)
7. Submeter → confirmar:
   - Network: POST `/api/clickmeeting-register` → 200 com `{ok: true, redirect_url}`
   - Browser redireciona pro `redirect_url` retornado
8. Validar registro via API:
   ```
   curl -H "X-Api-Key: {CLICKMEETING_API_KEY}" https://api.clickmeeting.com/v1/conferences/10003144/registrations
   ```
   → deve ver o lead recém-criado
9. Verificar email de confirmação no inbox de teste

### Fase B — Preview deploy
10. `vercel` (sem `--prod`) na sibling → cria preview URL
11. Repetir passos 5-9 na preview URL
12. Testar erro proposital (email inválido, campos vazios) — mensagens inline devem aparecer

### Fase C — Não-regressão
13. Antes do production, rodar smoke test MD5 das LPs vizinhas (`/lp-publicar` faz isso automático). Vizinhas no guarda-chuva:
    - `playbook-whatsapp2026`
    - `webinar-tecnologia-maio2026`
    - `webinar-tecnologia-maio2026-oferta`
    - `livraria`
    - `latam-webinar-atencionalcliente`
    - `ebook-marketing-conversacion-latam`

### Fase D — Production
14. Deploy via `/lp-publicar cxpress conheca-a-cxpress content.cxpress.io` (nunca `vercel deploy` direto)
15. Testar em `https://content.cxpress.io/conheca-a-cxpress`
16. Avisar o Victor pra limpar os 2-3 registros de teste do painel ClickMeeting

---

## 12. Critérios de aceite

- [ ] Form renderiza nativo Cxpress (zero iframe ClickMeeting)
- [ ] Data/hora do próximo webinar aparece na LP via fetch
- [ ] Quando o webinar atual passar, a LP automaticamente reflete o próximo (sem redeploy)
- [ ] Submit cria registro real no ClickMeeting (verificado via `GET /registrations`)
- [ ] Email de confirmação chega ao inbox de teste
- [ ] Link único de acesso ao webinar funciona
- [ ] API key NUNCA aparece no client (auditar via DevTools)
- [ ] Honeypot bloqueia bots (testar enviando POST com `_hp` preenchido — deve retornar sucesso falso)
- [ ] Nenhuma LP vizinha do guarda-chuva regrediu (MD5 igual pré/pós-deploy)
- [ ] CSP não regrediu
- [ ] dataLayer registra `webinar_lead_submitted` no GTM (LP tem `GTM-T4XDWHL3`)

---

## 13. Cuidados / não fazer

- ❌ Não hardcodar `room_id 10003144` — resolver sempre via `/api/next-webinar`
- ❌ Não expor a API key no client, no HTML, no JS, em log do browser
- ❌ Não commitar `.env.local` ou qualquer arquivo com a key
- ❌ Não usar `vercel deploy --prod` direto — sempre via `/lp-publicar`
- ❌ Não sobrescrever `vercel.json` inteiro do sibling — patches cirúrgicos se necessário
- ❌ Não mexer nas pastas vizinhas (`playbook-whatsapp2026/`, etc) no sibling
- ❌ Não criar `package.json` na sibling se ainda não houver — Vercel auto-detecta `api/*.js` sem isso
- ❌ Não usar dependências npm (`got`, `axios`, `node-fetch`) — usar `globalThis.fetch` nativo (Node 18+ na Vercel)

---

## 14. Estrutura final esperada

**No repo (vai pro git via `/commit`):**
- `landing-pages/cxpress/conheca-a-cxpress/index.html` — modificado (form + JS)

**Na sibling fora do repo (não vai pro git):**
- `content.cxpress.io/api/next-webinar.js` — novo
- `content.cxpress.io/api/clickmeeting-register.js` — novo
- `content.cxpress.io/conheca-a-cxpress/index.html` — sync do repo via `lp-publicar`

**No painel Vercel:**
- 3 env vars configuradas

---

## 15. Próximas iterações (fora deste escopo)

- Rate limit por IP no `/api/clickmeeting-register` (Vercel KV ou similar)
- Telemetria (logs estruturados de sucesso/falha)
- Fallback se ClickMeeting estiver fora do ar (capturar lead no Supabase e re-tentar depois)
- Suporte a múltiplas séries (filtrar `recurring_config_id` por marca/idioma)
