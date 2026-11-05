// Versao LATAM: e-mail do resultado pela automacao do ActiveCampaign (TOTEM_EMAIL_VIA_AC=1).
//   node landing-pages/buzzmonitor/buzz-compass-latam/tests/email-via-ac.test.js
const assert = require('assert');

// ---- Versao LATAM: e-mail pela automacao do ActiveCampaign (TOTEM_EMAIL_VIA_AC=1) ----
(async () => {
  const handler = require('../api/totem-lead.js');
  handler._reiniciarCacheAC();
  const original = global.fetch;
  const vars = ['TOTEM_EMAIL_VIA_AC', 'ACTIVECAMPAIGN_API_URL', 'ACTIVECAMPAIGN_API_TOKEN', 'SENDGRID_API_KEY', 'RESEND_API_KEY', 'TOTEM_LEADS_WEBHOOK_URL', 'TOTEM_BASE_URL', 'ACTIVECAMPAIGN_TOTEM_TAG_ID'];
  const antes = Object.fromEntries(vars.map((v) => [v, process.env[v]]));
  vars.forEach((v) => delete process.env[v]);
  Object.assign(process.env, { TOTEM_EMAIL_VIA_AC: '1', ACTIVECAMPAIGN_API_URL: 'https://x.api-us1.com', ACTIVECAMPAIGN_API_TOKEN: 't', SENDGRID_API_KEY: 'SG.nao-usar' });
  const chamadas = [];
  let jaTemTag = false;
  global.fetch = async (url, o = {}) => {
    chamadas.push({ url, metodo: o.method || 'GET', corpo: o.body ? JSON.parse(o.body) : null });
    const r = (status, json) => ({ ok: status < 300, status, json: async () => json, text: async () => JSON.stringify(json), headers: { get: () => null } });
    if (url.includes('sendgrid')) return r(202, {});
    if (url.includes('/contacts?email')) return r(200, { contacts: [] });
    if (url.includes('/fields')) return r(200, { fields: [{ id: '851', title: 'URL Conversão [AUTO]', type: 'text' }, { id: '901', title: 'Buzz Compass Link [AUTO]', type: 'textarea' }, { id: '902', title: 'Buzz Compass QR [AUTO]', type: 'textarea' }, { id: '903', title: 'Buzz Compass Marca [AUTO]', type: 'text' }], meta: { total: 4 } });
    if (url.endsWith('/contact/sync')) return r(200, { contact: { id: '7' } });
    if (url.includes('/tags?search')) return r(200, { tags: [{ id: '5', tag: 'Buzz Compass LATAM' }] });
    if (url.endsWith('/contactTags') && (o.method || 'GET') === 'POST') { if (jaTemTag) { jaTemTag = false; return r(422, {}); } return r(201, {}); }
    if (url.endsWith('/contacts/7/contactTags')) return r(200, { contactTags: [{ id: '99', tag: '5' }] });
    if (url.endsWith('/contactTags/99')) return r(200, {});
    return r(200, {});
  };
  const chamar = () => new Promise((resolve) => {
    const res = { statusCode: 200, setHeader() {}, json(b) { resolve(b); return this; } };
    handler({ method: 'POST', headers: { host: 'buzzcompass.buzzmonitor.com' }, query: {}, body: { nome: 'Ana López', email: 'ana@empresa.mx', marca: 'OXXO', segmento: 'Tiendas', concorrentes: ['7-Eleven'], _ts: Date.now() - 5000, url_conversao: 'https://buzzcompass.buzzmonitor.com/es' } }, res);
  });
  let b = await chamar();
  assert.strictEqual(b.email, 'via_ac', 'e-mail sai pela automacao do AC');
  assert(!chamadas.some((c) => c.url.includes('sendgrid')), 'nao chama o SendGrid mesmo com a chave');
  const campos = Object.fromEntries(chamadas.find((c) => c.url.endsWith('/contact/sync')).corpo.contact.fieldValues.map((f) => [f.field, f.value]));
  assert.strictEqual(campos['901'], 'https://buzzcompass.buzzmonitor.com/es/totem-resultado?m=OXXO&s=Tiendas&c=7-Eleven');
  assert.strictEqual(campos['903'], 'OXXO', 'marca do Compass em campo proprio');
  assert.strictEqual(campos['902'], 'https://buzzcompass.buzzmonitor.com/es/api/qr?d=' + encodeURIComponent(campos['901']));
  // mesma pessoa de novo: a tag ja existe (422) -> tira e aplica de novo, para a automacao disparar outra vez
  chamadas.length = 0; jaTemTag = true;
  b = await chamar();
  assert.strictEqual(b.email, 'via_ac');
  assert(chamadas.some((c) => c.metodo === 'DELETE' && c.url.endsWith('/contactTags/99')), 'tira a tag repetida');
  assert.strictEqual(chamadas.filter((c) => c.url.endsWith('/contactTags') && c.metodo === 'POST').length, 2, 'aplica a tag de novo');
  // sem os campos Buzz Compass no AC: o e-mail nao sai e a resposta diz isso
  handler._reiniciarCacheAC();
  const semCampos = global.fetch;
  global.fetch = async (url, o) => (url.includes('/fields') ? { ok: true, status: 200, json: async () => ({ fields: [], meta: { total: 0 } }) } : semCampos(url, o));
  b = await chamar();
  assert.strictEqual(b.email, 'falhou', 'sem campos Link/QR o e-mail via AC e marcado como falho');
  global.fetch = original;
  vars.forEach((v) => { if (antes[v] === undefined) delete process.env[v]; else process.env[v] = antes[v]; });
  handler._reiniciarCacheAC();
  console.log('email-via-ac.test.js: ok');
})().catch((e) => { console.error(e); process.exit(1); });
