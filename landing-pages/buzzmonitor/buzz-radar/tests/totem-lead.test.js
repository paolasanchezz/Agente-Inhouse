// Testes da captura de lead do totem:  node landing-pages/buzzmonitor/buzz-radar/tests/totem-lead.test.js
// A rede e simulada (fetch trocado): nada e enviado de verdade.
const assert = require('assert');

const chamadas = [];
global.fetch = async (url, opts) => {
  chamadas.push({ url: String(url), opts });
  if (String(url).includes('resend.com')) return { ok: true, status: 200, json: async () => ({ id: 'x' }), text: async () => '' };
  if (String(url).includes('webhook.test')) return { ok: true, status: 200, json: async () => ({}), text: async () => '' };
  if (String(url).includes('ac.test/api/3/contact/sync')) return { ok: true, status: 200, json: async () => ({ contact: { id: '77' } }), text: async () => '' };
  return { ok: true, status: 200, json: async () => ({}), text: async () => '' };
};

function chamar(handler, { method = 'POST', body, headers = { host: 'radar.exemplo.com' } } = {}) {
  return new Promise((resolve) => {
    const res = {
      statusCode: 200, headers: {},
      setHeader(k, v) { this.headers[k] = v; },
      json(obj) { resolve({ status: this.statusCode, body: obj }); return this; },
    };
    handler({ method, body, headers, query: {} }, res);
  });
}

(async () => {
  const handler = require('../api/totem-lead.js');
  const valido = { nome: '<b>Ana</b> Souza', email: 'ANA@Empresa.com.br', marca: 'Natura & Cia', segmento: 'Cosméticos e Beleza', concorrentes: ['Boticário', 'Avon', '', 'Eudora', 'Quarto'], _ts: Date.now() - 5000 };

  // 1) sem nenhuma integracao configurada: responde ok e nao chama ninguem
  for (const k of ['RESEND_API_KEY', 'TOTEM_LEADS_WEBHOOK_URL', 'ACTIVECAMPAIGN_API_URL', 'ACTIVECAMPAIGN_API_TOKEN']) delete process.env[k];
  let r = await chamar(handler, { body: valido });
  assert.strictEqual(r.status, 200);
  assert.deepStrictEqual([r.body.email, r.body.webhook, r.body.crm], ['nao_configurado', 'nao_configurado', 'nao_configurado']);
  assert.strictEqual(chamadas.length, 0);
  assert(r.body.link.startsWith('https://radar.exemplo.com/totem-resultado?m=Natura+%26+Cia&s=Cosm%C3%A9ticos+e+Beleza&c=Botic%C3%A1rio&c=Avon&c=Eudora'), r.body.link); // m, s, c nessa ordem (chave do cache); ate 3 concorrentes, vazio descartado
  assert(!r.body.link.includes('Ana') && !r.body.link.includes('Empresa'), 'sem dado pessoal na URL');

  // 1b) @ do Instagram: entra no link entre s e c (ordem da chave de cache), limpo; lixo vira vazio e some do link
  r = await chamar(handler, { body: { ...valido, instagram: 'https://www.instagram.com/NaturaBrasil/?hl=pt', concorrentes: ['Avon'] } });
  assert(r.body.link.includes('&s=Cosm%C3%A9ticos+e+Beleza&i=naturabrasil&c=Avon'), r.body.link);
  r = await chamar(handler, { body: { ...valido, instagram: '@<script>' } });
  assert(!r.body.link.includes('i=') || r.body.link.includes('i=script'), 'handle so com caracteres validos: ' + r.body.link);
  assert(!/[<>]/.test(r.body.link), 'sem caractere perigoso no link');
  r = await chamar(handler, { body: { ...valido, instagram: '@' } });
  assert(!r.body.link.includes('i='), 'handle vazio nao entra no link');

  // 2) tudo configurado
  process.env.RESEND_API_KEY = 're_teste';
  process.env.TOTEM_EMAIL_FROM = 'Buzzmonitor <radar@exemplo.com>';
  process.env.TOTEM_LEADS_WEBHOOK_URL = 'https://webhook.test/lead';
  process.env.ACTIVECAMPAIGN_API_URL = 'https://ac.test';
  process.env.ACTIVECAMPAIGN_API_TOKEN = 'tok';
  process.env.ACTIVECAMPAIGN_TOTEM_TAG_ID = '99';
  chamadas.length = 0;
  r = await chamar(handler, { body: valido });
  assert.deepStrictEqual([r.body.email, r.body.webhook, r.body.crm], ['enviado', 'enviado', 'enviado']);

  const resend = chamadas.find((c) => c.url.includes('resend.com'));
  const corpo = JSON.parse(resend.opts.body);
  assert.deepStrictEqual(corpo.to, ['ana@empresa.com.br'], 'e-mail em minusculo');
  assert.strictEqual(corpo.from, 'Buzzmonitor <radar@exemplo.com>');
  assert(!corpo.html.includes('<b>Ana'), 'HTML do nome precisa ser escapado');
  assert(corpo.html.includes('&lt;b&gt;Ana&lt;/b&gt;'), 'nome escapado aparece como texto (so o primeiro nome entra no e-mail)');
  assert(!corpo.html.includes('Souza'), 'sobrenome nao vai no e-mail');
  assert(corpo.html.includes('Natura &amp; Cia'), 'marca escapada');
  assert(corpo.html.includes(r.body.link.replace(/&/g, '&amp;')), 'o botao leva ao link do resultado');
  assert.strictEqual(resend.opts.headers.Authorization, 'Bearer re_teste');

  const hook = JSON.parse(chamadas.find((c) => c.url.includes('webhook.test')).opts.body);
  assert.strictEqual(hook.origem, 'buzz-compass-totem');
  assert.strictEqual(hook.segmento, 'Cosméticos e Beleza');
  assert.strictEqual(hook.email, 'ana@empresa.com.br');

  // CRM: so contato + tag, nunca negocio
  const urlsAC = chamadas.filter((c) => c.url.includes('ac.test')).map((c) => c.url);
  // busca o contato pelo e-mail, procura o campo "URL Conversao", cria o contato (nao existia) e aplica a tag
  assert.deepStrictEqual(urlsAC, ['https://ac.test/api/3/contacts?email=ana%40empresa.com.br', 'https://ac.test/api/3/fields?limit=100&offset=0', 'https://ac.test/api/3/contact/sync', 'https://ac.test/api/3/contactTags']);
  assert(!urlsAC.some((u) => /deal/i.test(u)), 'nunca cria deal');
  assert.strictEqual(JSON.parse(chamadas.find((c) => c.url.endsWith('contactTags')).opts.body).contactTag.tag, '99');

  // 3) falha de um destino nao derruba a resposta
  global.fetch = async (url) => { if (String(url).includes('resend.com')) throw new Error('rede'); return { ok: true, status: 200, json: async () => ({ contact: { id: '1' } }), text: async () => '' }; };
  r = await chamar(handler, { body: valido });
  assert.strictEqual(r.status, 200);
  assert.strictEqual(r.body.email, 'falhou');

  // 4) validacoes
  for (const k of ['RESEND_API_KEY', 'TOTEM_LEADS_WEBHOOK_URL', 'ACTIVECAMPAIGN_API_URL']) delete process.env[k];
  assert.strictEqual((await chamar(handler, { body: { ...valido, email: 'sem-arroba' } })).status, 400);
  assert.strictEqual((await chamar(handler, { body: { ...valido, nome: '' } })).status, 400);
  assert.strictEqual((await chamar(handler, { body: { ...valido, marca: '' } })).status, 400);
  assert.strictEqual((await chamar(handler, { method: 'GET' })).status, 405);
  assert.strictEqual((await chamar(handler, { body: 'nao-json' })).status, 400);
  r = await chamar(handler, { body: { ...valido, _hp: 'robo' } });
  assert.strictEqual(r.body.honeypot, true);
  r = await chamar(handler, { body: { ...valido, _ts: Date.now() - 200 } });
  assert.strictEqual(r.body.honeypot, true, 'envio rapido demais e tratado como robo');

  console.log('totem-lead.test.js: ok');
})().catch((e) => { console.error(e); process.exit(1); });
