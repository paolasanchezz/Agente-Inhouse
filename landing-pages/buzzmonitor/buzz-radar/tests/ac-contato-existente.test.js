// Teste: contato que ja existe no ActiveCampaign (pelo e-mail) e URL de conversao:
//   node landing-pages/buzzmonitor/buzz-radar/tests/ac-contato-existente.test.js
// Regras: nunca criar contato novo se o e-mail ja existe; so atualizar o campo "URL Conversao [Auto]" e aplicar a tag, sem
// tocar em nome e empresa que ja estao no AC. A rede e simulada (nada e enviado de verdade).
const assert = require('assert');

let chamadas = [];
let roteador = () => ({ status: 200, json: {} });
global.fetch = async (url, opts) => {
  const o = opts || {};
  chamadas.push({ url: String(url), metodo: o.method || 'GET', corpo: o.body ? JSON.parse(o.body) : null });
  const r = await roteador(String(url), o.method || 'GET');
  return { ok: r.status >= 200 && r.status < 300, status: r.status, json: async () => r.json || {}, text: async () => JSON.stringify(r.json || {}) };
};
const { executarAC, urlDeConversao, _reiniciarCacheAC } = require('../api/totem-lead.js');

process.env.ACTIVECAMPAIGN_API_URL = 'https://ac.test';
process.env.ACTIVECAMPAIGN_API_TOKEN = 'tok';
process.env.ACTIVECAMPAIGN_TOTEM_TAG_ID = '9'; // tag nao e o foco deste teste
const URL_CONV = 'https://buzzcompass.buzzmonitor.com/totem';
const dados = { email: 'ana@empresa.com.br', nome: 'TESTE THAMIRES RIOS', marca: 'Teste Buzzmonitor', urlConversao: URL_CONV };

const CAMPOS = { fields: [
  { id: '457', title: 'URL de Origem' },
  { id: '850', title: 'Gclid' },
  { id: '852', title: 'URL Conversão' }, // sem [Auto]
  { id: '851', title: 'URL Conversão [Auto]' },
  { id: '845', title: 'UTM Source [Auto]' },
], meta: { total: '5' } };
const rota = ({ contatos = [], campos = CAMPOS } = {}) => (url, metodo) => {
  if (url.includes('/contacts?email=')) return { status: 200, json: { contacts: contatos } };
  if (url.includes('/fields?')) return { status: 200, json: campos };
  if (url.endsWith('/contact/sync')) return { status: 200, json: { contact: { id: '700' } } };
  if (/\/contacts\/\d+$/.test(url) && metodo === 'PUT') return { status: 200, json: {} };
  return { status: 201, json: {} };
};
const mutacoes = () => chamadas.filter((c) => c.metodo !== 'GET');

(async () => {
  // ---- 1) E-MAIL JA EXISTE: nao cria contato; so atualiza o campo e aplica a tag; nome/empresa do AC ficam como estao ----
  _reiniciarCacheAC();
  roteador = rota({ contatos: [{ id: '55', email: 'ANA@Empresa.com.br', firstName: 'Ana', lastName: 'Souza', orgname: 'Natura' }] });
  chamadas = [];
  let r = await executarAC(dados);
  assert.deepStrictEqual([r.status, r.contato], ['enviado', 'atualizado']);
  assert(!chamadas.some((c) => c.url.endsWith('/contact/sync')), 'NAO usa o sync (criar/atualizar tudo) para contato existente');
  assert(!chamadas.some((c) => c.metodo === 'POST' && /\/contacts$/.test(c.url)), 'NAO cria contato');
  const put = chamadas.find((c) => c.metodo === 'PUT');
  assert.strictEqual(put.url, 'https://ac.test/api/3/contacts/55', 'atualiza o contato que ja existe (id 55)');
  assert.deepStrictEqual(put.corpo, { contact: { fieldValues: [{ field: '851', value: URL_CONV }] } }, 'so o campo URL Conversao [Auto] (id 851, o que tem [Auto]) vai no PUT');
  assert(!JSON.stringify(put.corpo).match(/firstName|lastName|orgname|email/), 'nome, empresa e e-mail do contato existente NAO sao reescritos');
  const tag = chamadas.find((c) => c.url.endsWith('/contactTags'));
  assert.deepStrictEqual(tag.corpo.contactTag, { contact: '55', tag: '9' }, 'a tag vai para o contato existente');
  assert.deepStrictEqual(r.avisos, []);

  // ---- 2) E-MAIL NOVO: cria completo (nome separado, empresa) ja com a URL de conversao e a tag ----
  _reiniciarCacheAC();
  roteador = rota({ contatos: [] });
  chamadas = [];
  r = await executarAC(dados);
  assert.deepStrictEqual([r.status, r.contato], ['enviado', 'criado']);
  const sync = chamadas.find((c) => c.url.endsWith('/contact/sync'));
  assert.deepStrictEqual(sync.corpo.contact, { email: 'ana@empresa.com.br', firstName: 'TESTE', lastName: 'THAMIRES RIOS', orgname: 'Teste Buzzmonitor', fieldValues: [{ field: '851', value: URL_CONV }] });
  assert.strictEqual(chamadas.find((c) => c.url.endsWith('/contactTags')).corpo.contactTag.contact, '700');
  assert(!chamadas.some((c) => c.metodo === 'PUT'), 'contato novo nao usa PUT');

  // ---- 3) busca exata: e-mail parecido (nao igual) NAO conta como o mesmo contato ----
  _reiniciarCacheAC();
  roteador = rota({ contatos: [{ id: '56', email: 'ana@empresa.com.br.outro.com' }, { id: '57', email: 'maria.ana@empresa.com.br' }] });
  chamadas = [];
  r = await executarAC(dados);
  assert.strictEqual(r.contato, 'criado', 'so igualdade exata de e-mail conta');
  assert(chamadas.some((c) => c.url.endsWith('/contact/sync')));

  // ---- 4) busca do e-mail com caractere especial vai codificada ----
  _reiniciarCacheAC();
  roteador = rota();
  chamadas = [];
  await executarAC({ ...dados, email: 'ana+compass@empresa.com.br' });
  assert(chamadas[0].url.endsWith('/contacts?email=ana%2Bcompass%40empresa.com.br'), chamadas[0].url);

  // ---- 5) campo URL Conversao: acha por titulo, ignorando acento e maiuscula, e em varias paginas ----
  _reiniciarCacheAC();
  const pagina1 = { fields: Array.from({ length: 100 }, (_, i) => ({ id: String(1000 + i), title: 'Campo ' + i })), meta: { total: '130' } };
  const pagina2 = { fields: [{ id: '2001', title: 'outro' }, { id: '2002', title: 'URL CONVERSAO [AUTO]' }], meta: { total: '130' } };
  roteador = (url, metodo) => {
    if (url.includes('/fields?limit=100&offset=0')) return { status: 200, json: pagina1 };
    if (url.includes('/fields?limit=100&offset=100')) return { status: 200, json: pagina2 };
    return rota({ contatos: [{ id: '55', email: 'ana@empresa.com.br' }] })(url, metodo);
  };
  chamadas = [];
  r = await executarAC(dados);
  assert.strictEqual(chamadas.find((c) => c.metodo === 'PUT').corpo.contact.fieldValues[0].field, '2002', 'achou na 2a pagina, sem diferenciar acento/maiuscula');
  // o id achado fica guardado: o proximo lead nao procura os campos de novo
  chamadas = [];
  await executarAC(dados);
  assert(!chamadas.some((c) => c.url.includes('/fields')), 'id do campo guardado');

  // ---- 6) sem o campo no AC: contato e tag seguem, com aviso claro; e a proxima vez procura de novo ----
  _reiniciarCacheAC();
  roteador = rota({ contatos: [{ id: '55', email: 'ana@empresa.com.br' }], campos: { fields: [{ id: '1', title: 'Cargo' }], meta: { total: '1' } } });
  chamadas = [];
  r = await executarAC(dados);
  assert.deepStrictEqual([r.status, r.contato, r.avisos], ['enviado', 'atualizado', ['campo_url_conversao_nao_encontrado']]);
  assert(!chamadas.some((c) => c.metodo === 'PUT'), 'sem campo, nada a atualizar no contato');
  assert(chamadas.some((c) => c.url.endsWith('/contactTags')), 'a tag e aplicada mesmo assim');
  chamadas = [];
  await executarAC(dados);
  assert(chamadas.some((c) => c.url.includes('/fields')), 'ausencia nao fica guardada: procura de novo no lead seguinte');

  // ---- 7) ID do campo forcado por variavel dispensa a busca ----
  _reiniciarCacheAC();
  process.env.ACTIVECAMPAIGN_URL_CONVERSAO_FIELD_ID = '4242';
  roteador = rota({ contatos: [{ id: '55', email: 'ana@empresa.com.br' }] });
  chamadas = [];
  await executarAC(dados);
  assert.strictEqual(chamadas.find((c) => c.metodo === 'PUT').corpo.contact.fieldValues[0].field, '4242');
  assert(!chamadas.some((c) => c.url.includes('/fields')));
  delete process.env.ACTIVECAMPAIGN_URL_CONVERSAO_FIELD_ID;

  // ---- 8) busca de contato falhou (AC fora do ar): o lead nao se perde; o sync tambem nao duplica por e-mail ----
  _reiniciarCacheAC();
  roteador = (url, metodo) => (url.includes('/contacts?email=') ? { status: 500, json: {} } : rota()(url, metodo));
  chamadas = [];
  r = await executarAC(dados);
  assert.deepStrictEqual([r.status, r.avisos], ['enviado', ['busca_contato_falhou']]);
  assert(chamadas.some((c) => c.url.endsWith('/contact/sync')), 'cai no sync, que faz criar-ou-atualizar pelo e-mail');

  // ---- 9) falha ao atualizar o contato existente: reportada como falha (nao fingir que deu certo) ----
  _reiniciarCacheAC();
  roteador = (url, metodo) => (metodo === 'PUT' ? { status: 403, json: {} } : rota({ contatos: [{ id: '55', email: 'ana@empresa.com.br' }] })(url, metodo));
  r = await executarAC(dados);
  assert.strictEqual(r.status, 'falhou');

  // ---- 10) nunca cria negocio, em nenhum caminho ----
  assert(!chamadas.some((c) => /deal/i.test(c.url)));
  assert(!mutacoes().some((c) => /\/deals?/i.test(c.url)));

  // ---- 11) URL de conversao enviada pelo navegador: so a pagina do totem do proprio projeto ----
  const req = { headers: { host: 'buzzcompass.buzzmonitor.com' } };
  const padrao = 'https://buzzcompass.buzzmonitor.com/totem';
  assert.strictEqual(urlDeConversao(req, 'https://buzzcompass.buzzmonitor.com/totem'), padrao);
  assert.strictEqual(urlDeConversao(req, 'https://buzzcompass.buzzmonitor.com/totem?utm_source=evento&utm_medium=qr&idle=8000&fbclid=abc#topo'),
    'https://buzzcompass.buzzmonitor.com/totem?utm_source=evento&utm_medium=qr', 'mantem as UTMs; tira idle, fbclid e #hash');
  assert.strictEqual(urlDeConversao(req, 'https://buzzmonitor-lp-buzz-radar.vercel.app/totem'), 'https://buzzmonitor-lp-buzz-radar.vercel.app/totem', 'endereco antigo do projeto vale');
  for (const ruim of ['https://site-malicioso.com/totem', 'http://buzzcompass.buzzmonitor.com/totem', 'javascript:alert(1)', 'nao-e-url', '', undefined, null,
    'https://buzzcompass.buzzmonitor.com/outra-pagina', 'https://buzzcompass.buzzmonitor.com.evil.com/totem']) {
    assert.strictEqual(urlDeConversao(req, ruim), padrao, 'vira o padrao: ' + ruim);
  }
  assert(urlDeConversao(req, 'https://buzzcompass.buzzmonitor.com/totem?utm_campaign=' + 'x'.repeat(900)).length <= 500, 'corta em 500');

  console.log('ac-contato-existente.test.js: ok');
})().catch((e) => { console.error(e); process.exit(1); });
