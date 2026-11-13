// Versao LATAM: e-mail do resultado pela automacao do ActiveCampaign (TOTEM_EMAIL_VIA_AC=1).
//   node landing-pages/buzzmonitor/buzz-compass-latam/tests/email-via-ac.test.js
// O gatilho da automacao e o campo "Buzz Compass Envio [AUTO]" (data e hora do envio, muda a cada lead). A tag so segmenta.
// O AC real responde 200 (nao 422) quando a tag ja esta no contato: visto em producao em 2026-11-13.
const assert = require('assert');

(async () => {
  const handler = require('../api/totem-lead.js');
  handler._reiniciarCacheAC();
  const original = global.fetch;
  const vars = ['TOTEM_EMAIL_VIA_AC', 'ACTIVECAMPAIGN_API_URL', 'ACTIVECAMPAIGN_API_TOKEN', 'SENDGRID_API_KEY', 'RESEND_API_KEY', 'TOTEM_LEADS_WEBHOOK_URL', 'TOTEM_BASE_URL', 'ACTIVECAMPAIGN_TOTEM_TAG_ID'];
  const antes = Object.fromEntries(vars.map((v) => [v, process.env[v]]));
  vars.forEach((v) => delete process.env[v]);
  Object.assign(process.env, { TOTEM_EMAIL_VIA_AC: '1', ACTIVECAMPAIGN_API_URL: 'https://x.api-us1.com', ACTIVECAMPAIGN_API_TOKEN: 't', SENDGRID_API_KEY: 'SG.nao-usar' });
  const silencio = { log: console.log, error: console.error };
  console.log = () => {}; console.error = () => {};

  const camposAC = [
    { id: '851', title: 'URL Conversão [AUTO]', type: 'text' },
    { id: '901', title: 'Buzz Compass Link [AUTO]', type: 'textarea' },
    { id: '902', title: 'Buzz Compass QR [AUTO]', type: 'textarea' },
    { id: '903', title: 'Buzz Compass Marca [AUTO]', type: 'text' },
    { id: '904', title: 'Buzz Compass Envío [AUTO]', type: 'text' },
  ];
  let campos = camposAC;
  let contatoExiste = false;
  const chamadas = [];
  global.fetch = async (url, o = {}) => {
    chamadas.push({ url, metodo: o.method || 'GET', corpo: o.body ? JSON.parse(o.body) : null });
    const r = (status, json) => ({ ok: status < 300, status, json: async () => json, text: async () => JSON.stringify(json), headers: { get: () => null } });
    if (url.includes('sendgrid')) return r(202, {});
    if (url.includes('/contacts?email')) return r(200, { contacts: contatoExiste ? [{ id: '7', email: 'ana@empresa.mx' }] : [] });
    if (url.includes('/fields')) return r(200, { fields: campos, meta: { total: campos.length } });
    if (url.endsWith('/contact/sync')) return r(200, { contact: { id: '7' } });
    if (url.endsWith('/contacts/7') && o.method === 'PUT') return r(200, { contact: { id: '7' } });
    if (url.includes('/tags?search')) return r(200, { tags: [{ id: '5', tag: 'Buzz Compass LATAM' }] });
    // como o AC real: tag repetida responde 200 com a associacao que ja existia
    if (url.endsWith('/contactTags') && o.method === 'POST') return r(contatoExiste ? 200 : 201, { contactTag: { id: '99', tag: '5', contact: '7' } });
    return r(200, {});
  };
  const chamar = () => new Promise((resolve) => {
    const res = { statusCode: 200, setHeader() {}, json(b) { resolve(b); return this; } };
    handler({ method: 'POST', headers: { host: 'buzzcompass.buzzmonitor.com' }, query: {}, body: { nome: 'Ana López', email: 'ana@empresa.mx', marca: 'OXXO', segmento: 'Tiendas', concorrentes: ['7-Eleven'], _ts: Date.now() - 5000, url_conversao: 'https://buzzcompass.buzzmonitor.com/es' } }, res);
  });
  const camposGravados = () => {
    const c = chamadas.find((x) => x.url.endsWith('/contact/sync') || (x.url.endsWith('/contacts/7') && x.metodo === 'PUT'));
    return Object.fromEntries(c.corpo.contact.fieldValues.map((f) => [f.field, f.value]));
  };

  try {
    // 1) contato novo: link, QR, marca e o carimbo de envio no mesmo sync; SendGrid nao e chamado
    let b = await chamar();
    assert.strictEqual(b.email, 'via_ac', 'e-mail sai pela automacao do AC');
    assert(!chamadas.some((c) => c.url.includes('sendgrid')), 'nao chama o SendGrid mesmo com a chave');
    let v = camposGravados();
    assert.strictEqual(v['901'], 'https://buzzcompass.buzzmonitor.com/es/totem-resultado?m=OXXO&s=Tiendas&c=7-Eleven');
    assert.strictEqual(v['902'], 'https://buzzcompass.buzzmonitor.com/es/api/qr?d=' + encodeURIComponent(v['901']));
    assert.strictEqual(v['903'], 'OXXO', 'marca do Compass em campo proprio');
    assert(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/.test(v['904']), 'envio em data e hora UTC sem milissegundo: ' + v['904']);
    const primeiroEnvio = v['904'];

    // 2) mesma pessoa, mesma marca, de novo: o link nao muda, mas o envio muda (dispara a automacao); a tag nao e mexida
    await new Promise((ok) => setTimeout(ok, 1100));
    chamadas.length = 0; contatoExiste = true;
    b = await chamar();
    assert.strictEqual(b.email, 'via_ac');
    v = camposGravados();
    assert.notStrictEqual(v['904'], primeiroEnvio, 'o carimbo de envio muda a cada lead');
    assert.strictEqual(v['901'], 'https://buzzcompass.buzzmonitor.com/es/totem-resultado?m=OXXO&s=Tiendas&c=7-Eleven', 'link igual ao anterior');
    assert(!chamadas.some((c) => c.metodo === 'DELETE'), 'nao tira tag');
    assert.strictEqual(chamadas.filter((c) => c.url.endsWith('/contactTags') && c.metodo === 'POST').length, 1, 'tag aplicada uma vez so (200 do AC e sucesso)');

    // 3) campo Envio de data/hora tambem serve
    handler._reiniciarCacheAC();
    campos = camposAC.map((f) => (f.id === '904' ? { ...f, type: 'datetime' } : f));
    chamadas.length = 0;
    b = await chamar();
    assert.strictEqual(b.email, 'via_ac', 'campo de data/hora aceito');
    assert(camposGravados()['904'], 'carimbo gravado no campo de data/hora');

    // 4) sem o campo Envio no AC: a automacao nao teria gatilho, entao o e-mail e marcado como falho e o aviso diz qual campo
    handler._reiniciarCacheAC();
    campos = camposAC.filter((f) => f.id !== '904');
    b = await chamar();
    assert.strictEqual(b.email, 'falhou', 'sem o campo Envio o e-mail via AC nao e prometido');
    assert((b.crm_avisos || []).includes('campo_compass_envio_nao_encontrado'), 'aviso nomeia o campo: ' + JSON.stringify(b.crm_avisos));

    // 5) sem nenhum campo Buzz Compass: tambem falho
    handler._reiniciarCacheAC();
    campos = [];
    b = await chamar();
    assert.strictEqual(b.email, 'falhou');
  } finally {
    console.log = silencio.log; console.error = silencio.error;
    global.fetch = original;
    vars.forEach((k) => { if (antes[k] === undefined) delete process.env[k]; else process.env[k] = antes[k]; });
    handler._reiniciarCacheAC();
  }
  console.log('email-via-ac.test.js: ok');
})().catch((e) => { console.error(e); process.exit(1); });
