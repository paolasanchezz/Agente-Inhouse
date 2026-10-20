// Totem Buzz Compass: captura do lead depois que ele pediu a analise.
// POST /api/totem-lead  { nome, email, marca, segmento, instagram, concorrentes[], _hp, _ts }
//
// Faz tres coisas, todas opcionais e sem derrubar a resposta se falharem:
//   1. e-mail com o link do resultado (Resend, mesmo caminho das rotinas do repo; precisa RESEND_API_KEY)
//   2. webhook de leads (TOTEM_LEADS_WEBHOOK_URL: n8n, Apps Script, o que a equipe preferir)
//   3. ActiveCampaign: so contato + tag, nunca deal (igual a api/radar.js; desligado sem credencial)
// Sem nenhuma das tres configuradas o lead so aparece no log da funcao: ver README.md.

const { normalize, fetchWithTimeout } = require('./_lib/trends');
const { limparPerfil } = require('./_lib/perfil');

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

function baseUrl(req) {
  if (process.env.TOTEM_BASE_URL) return process.env.TOTEM_BASE_URL.replace(/\/$/, '');
  const host = req.headers['x-forwarded-host'] || req.headers.host || 'buzzmonitor-lp-buzz-radar.vercel.app';
  return `https://${host}`;
}

// Mesma URL de analise do totem (m + c), sem dado pessoal na URL (a ordem dos parametros e a do totem: e a chave do cache).
function linkDoResultado(req, { marca, segmento, instagram, concorrentes }) {
  const p = new URLSearchParams();
  p.set('m', marca);
  if (segmento) p.set('s', segmento);
  if (instagram) p.set('i', instagram);
  concorrentes.forEach((c) => p.append('c', c));
  return `${baseUrl(req)}/totem-resultado?${p.toString()}`;
}

function htmlDoEmail({ nome, marca, link }) {
  const primeiro = esc((nome || '').split(' ')[0] || 'Olá');
  const saudacao = nome ? `Olá, ${primeiro}!` : 'Olá!';
  return `<!doctype html><html lang="pt-BR"><body style="margin:0;background:#0b0b0c;font-family:Arial,Helvetica,sans-serif;color:#ffffff">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#0b0b0c"><tr><td align="center" style="padding:32px 16px">
<table role="presentation" width="560" cellpadding="0" cellspacing="0" style="max-width:560px;width:100%">
<tr><td style="padding:0 0 20px;font-size:13px;letter-spacing:.12em;color:#EB7C2E;font-weight:700">BUZZ COMPASS</td></tr>
<tr><td style="font-size:26px;line-height:1.25;font-weight:800;padding:0 0 14px">${saudacao} O Buzz Compass de ${esc(marca)} está pronto.</td></tr>
<tr><td style="font-size:16px;line-height:1.6;color:#d9d9d9;padding:0 0 26px">Reunimos conversas reais dos últimos 30 dias, comparamos ${esc(marca)} com concorrentes e escrevemos o diagnóstico. Abra pelo celular ou pelo computador.</td></tr>
<tr><td style="padding:0 0 28px"><a href="${esc(link)}" style="display:inline-block;background:#EB7C2E;color:#ffffff;text-decoration:none;font-weight:700;font-size:16px;padding:15px 30px;border-radius:999px">Ver meu Compass</a></td></tr>
<tr><td style="font-size:13px;line-height:1.6;color:#8a8a8a;border-top:1px solid #26262a;padding:18px 0 0">Se o botão não abrir, copie este endereço no navegador:<br><span style="color:#bdbdbd;word-break:break-all">${esc(link)}</span><br><br>Buzzmonitor</td></tr>
</table></td></tr></table></body></html>`;
}

async function enviarEmail({ nome, email, marca, link }) {
  const key = process.env.RESEND_API_KEY;
  if (!key) return 'nao_configurado';
  try {
    const r = await fetchWithTimeout('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: process.env.TOTEM_EMAIL_FROM || 'Buzzmonitor <onboarding@resend.dev>',
        to: [email],
        subject: `Seu Buzz Compass de ${marca} está pronto`,
        html: htmlDoEmail({ nome, marca, link }),
        text: `${nome ? `Olá, ${nome.split(' ')[0]}! ` : ''}O Buzz Compass de ${marca} está pronto: ${link}`,
      }),
    }, 8000);
    if (!r.ok) throw new Error(`resend_${r.status}: ${await r.text().catch(() => '')}`);
    return 'enviado';
  } catch (err) {
    console.error('[buzz-radar-totem] e-mail falhou', err && err.message ? err.message : err);
    return 'falhou';
  }
}

async function enviarWebhook(lead) {
  const url = process.env.TOTEM_LEADS_WEBHOOK_URL;
  if (!url) return 'nao_configurado';
  try {
    const r = await fetchWithTimeout(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(lead) }, 6000);
    if (!r.ok) throw new Error(`webhook_${r.status}`);
    return 'enviado';
  } catch (err) {
    console.error('[buzz-radar-totem] webhook falhou', err && err.message ? err.message : err);
    return 'falhou';
  }
}

async function syncActiveCampaign({ email, nome, marca }) {
  const base = process.env.ACTIVECAMPAIGN_API_URL;
  const token = process.env.ACTIVECAMPAIGN_API_TOKEN;
  if (!base || !token) return 'nao_configurado';
  try {
    const sync = await fetchWithTimeout(`${base}/api/3/contact/sync`, {
      method: 'POST',
      headers: { 'Api-Token': token, 'Content-Type': 'application/json' },
      body: JSON.stringify({ contact: { email, firstName: nome, orgname: marca, fieldValues: [] } }),
    }, 5000);
    if (!sync.ok) throw new Error(`ac_sync_${sync.status}`);
    const dados = await sync.json();
    const contactId = dados && dados.contact && dados.contact.id;
    const tagId = process.env.ACTIVECAMPAIGN_TOTEM_TAG_ID || process.env.ACTIVECAMPAIGN_TAG_ID;
    if (contactId && tagId) {
      await fetchWithTimeout(`${base}/api/3/contactTags`, {
        method: 'POST',
        headers: { 'Api-Token': token, 'Content-Type': 'application/json' },
        body: JSON.stringify({ contactTag: { contact: contactId, tag: tagId } }),
      }, 5000);
    }
    return 'enviado';
  } catch (err) {
    console.error('[buzz-radar-totem] activecampaign falhou', err && err.message ? err.message : err);
    return 'falhou';
  }
}

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') {
    res.statusCode = 405;
    return res.json({ ok: false, error: 'method_not_allowed' });
  }

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch (_) { body = null; }
  }
  if (!body || typeof body !== 'object') {
    res.statusCode = 400;
    return res.json({ ok: false, error: 'invalid_payload' });
  }

  // Honeypot e tempo minimo: mesmo criterio da LP original.
  if (typeof body._hp === 'string' && body._hp.trim()) return res.json({ ok: true, honeypot: true });
  const renderedAt = Number(body._ts);
  if (Number.isFinite(renderedAt) && Date.now() - renderedAt < 1500) return res.json({ ok: true, honeypot: true });

  const nome = normalize(body.nome, 100);
  const email = normalize(body.email, 200).toLowerCase();
  const marca = normalize(body.marca, 80);
  const segmento = normalize(body.segmento, 60);
  const instagram = limparPerfil(body.instagram);
  const concorrentes = (Array.isArray(body.concorrentes) ? body.concorrentes : [])
    .map((c) => normalize(String(c || ''), 60)).filter(Boolean).slice(0, 3);

  if (!nome || !marca || !email) {
    res.statusCode = 400;
    return res.json({ ok: false, error: 'missing_fields', message: 'Preencha nome, e-mail e marca.' });
  }
  if (!EMAIL_RE.test(email)) {
    res.statusCode = 400;
    return res.json({ ok: false, error: 'invalid_email', message: 'E-mail inválido.' });
  }

  const link = linkDoResultado(req, { marca, segmento, instagram, concorrentes });
  const lead = { origem: 'buzz-compass-totem', criado_em: new Date().toISOString(), nome, email, marca, segmento, instagram, concorrentes, link };

  // Registro de seguranca: enquanto nenhuma integracao estiver ligada, este log e o unico lugar onde o lead existe.
  console.log('[totem-lead]', JSON.stringify(lead));

  const [emailStatus, webhookStatus, acStatus] = await Promise.all([
    enviarEmail({ nome, email, marca, link }),
    enviarWebhook(lead),
    syncActiveCampaign({ email, nome, marca }),
  ]);

  res.statusCode = 200;
  return res.json({ ok: true, email: emailStatus, webhook: webhookStatus, crm: acStatus, link });
};
