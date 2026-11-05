// Teste: contato que ja existe no ActiveCampaign (pelo e-mail) e campos de rastreio (URL Conversao + UTMs):
//   node landing-pages/buzzmonitor/buzz-compass-latam/tests/ac-contato-existente.test.js
// Regras: nunca criar contato novo se o e-mail ja existe; contato existente so recebe a tag e os campos de rastreio, sem tocar
// em nome e empresa que ja estao no AC; contato novo e criado completo. Nos dois casos entram URL Conversao [Auto] e as UTMs.
// A rede e simulada (nada e enviado de verdade).
const assert = require('assert');

let chamadas = [];
let roteador = () => ({ status: 200, json: {} });
global.fetch = async (url, opts) => {
  const o = opts || {};
  chamadas.push({ url: String(url), metodo: o.method || 'GET', corpo: o.body ? JSON.parse(o.body) : null });
  const r = await roteador(String(url), o.method || 'GET');
  return { ok: r.status >= 200 && r.status < 300, status: r.status, json: async () => r.json || {}, text: async () => JSON.stringify(r.json || {}) };
};
const { executarAC, urlDeConversao, valoresDeRastreio, _reiniciarCacheAC } = require('../api/totem-lead.js');

const ENV_UTM = ['TOTEM_UTM_SOURCE_PADRAO', 'TOTEM_UTM_MEDIUM_PADRAO', 'TOTEM_UTM_CAMPAIGN_PADRAO', 'TOTEM_UTM_CONTENT_PADRAO', 'TOTEM_UTM_TERM_PADRAO', 'ACTIVECAMPAIGN_URL_CONVERSAO_FIELD_ID'];
const limparEnv = () => ENV_UTM.forEach((k) => delete process.env[k]);
process.env.ACTIVECAMPAIGN_API_URL = 'https://ac.test';
process.env.ACTIVECAMPAIGN_API_TOKEN = 'tok';
process.env.ACTIVECAMPAIGN_TOTEM_TAG_ID = '9'; // tag nao e o foco deste teste
const URL_CONV = 'https://buzzcompass.buzzmonitor.com/';
const dados = { email: 'ana@empresa.com.br', nome: 'TESTE THAMIRES RIOS', marca: 'Teste Buzzmonitor', urlConversao: URL_CONV };

// campos de contato do AC, copiados da conta real da Buzzmonitor (ids e titulos de verdade, inclusive a grafia "Campaing" do 847),
// com as armadilhas que existem la: campos numerados do historico ("UTM Campaign 1" etc.), "Origem", Gclid, AdName, outros tipos.
// Em 2026-10-23 a campanha foi parar em "UTM Campaign 1" (1016) porque o 847 se chama "Campaing" e a regra antiga nao o reconhecia.
const T = (id, title, type = 'text') => ({ id: String(id), title, type });
const CAMPOS = { fields: [
  T(389, 'UTM Source - Origem [AUTO]'), T(457, 'URL de Origem [AUTO]'), T(573, 'Data última Conversão [AUTO]', 'date'),
  T(845, 'UTM Source [AUTO]'), T(846, 'UTM Medium [AUTO]'), T(847, 'UTM Campaing [AUTO]'), T(848, 'UTM Content [AUTO]'), T(849, 'UTM Term [AUTO]'),
  T(850, 'Gclid [AUTO]'), T(851, 'URL Conversão [AUTO]'), T(881, 'UTM ADNAME [AUTO]'),
  T(1001, 'UTM Source 1 '), T(1006, 'UTM Medium 1'), T(1011, 'UTM Content 1'), T(1016, 'UTM Campaign 1'), T(1017, 'UTM Campaign 2'), T(1021, 'UTM Term 1'),
  T(1026, ' UTM Source 0'), T(1027, 'URL_Conversão 1'), T(1031, 'URL_Conversão 5'), T(1051, 'Interesses demonstrados durante a conversa', 'dropdown'),
], meta: { total: '21' } };
const rota = ({ contatos = [], campos = CAMPOS } = {}) => (url, metodo) => {
  if (url.includes('/contacts?email=')) return { status: 200, json: { contacts: contatos } };
  if (url.includes('/fields?')) return { status: 200, json: campos };
  if (url.endsWith('/contact/sync')) return { status: 200, json: { contact: { id: '700' } } };
  if (/\/contacts\/\d+$/.test(url) && metodo === 'PUT') return { status: 200, json: {} };
  return { status: 201, json: {} };
};
const existente = (extra) => rota({ contatos: [{ id: '55', email: 'ANA@Empresa.com.br' }], ...extra });
const valoresDoPut = () => chamadas.find((c) => c.metodo === 'PUT').corpo.contact.fieldValues;
const comoMapa = (lista) => Object.fromEntries(lista.map((f) => [f.field, f.value]));

(async () => {
  // ---- 1) E-MAIL JA EXISTE, URL sem UTM: nao cria contato; PUT so com campos de rastreio; padroes do Compass nas UTMs ----
  _reiniciarCacheAC(); limparEnv();
  roteador = existente();
  chamadas = [];
  let r = await executarAC(dados);
  assert.deepStrictEqual([r.status, r.contato, r.avisos], ['enviado', 'atualizado', []]);
  assert(!chamadas.some((c) => c.url.endsWith('/contact/sync')), 'NAO usa o sync para contato existente');
  assert(!chamadas.some((c) => c.metodo === 'POST' && /\/contacts$/.test(c.url)), 'NAO cria contato');
  const put = chamadas.find((c) => c.metodo === 'PUT');
  assert.strictEqual(put.url, 'https://ac.test/api/3/contacts/55', 'atualiza o contato que ja existe');
  assert.deepStrictEqual(put.corpo.contact.fieldValues, [
    { field: '851', value: URL_CONV },
    { field: '845', value: 'evento' }, // padrao do Compass (vocabulario fechado da convencao: evento presencial)
    { field: '846', value: '' }, // o que nao veio e limpo, para nao misturar com a atribuicao anterior
    { field: '847', value: '' },
    { field: '848', value: 'captacao-buzz-compass' }, // {tipo-de-pagina}-{conteudo}
    { field: '849', value: '' },
  ]);
  assert(!JSON.stringify(put.corpo).match(/firstName|lastName|orgname|"email"/), 'nome, empresa e e-mail do contato existente NAO sao reescritos');
  assert.deepStrictEqual(chamadas.find((c) => c.url.endsWith('/contactTags')).corpo.contactTag, { contact: '55', tag: '9' });
  const usados = new Set(valoresDoPut().map((f) => f.field));
  ['1016', '1017', '1001', '1006', '1011', '1021', '1026', '1027', '1031', '389', '457', '573', '850', '881', '1051'].forEach((id) => assert(!usados.has(id), 'campo-isca ' + id + ' NUNCA e usado'));
  assert(usados.has('847'), 'a campanha vai para o 847 ("UTM Campaing [AUTO]"), nao para o "UTM Campaign 1"');

  // ---- 2) E-MAIL NOVO: cria completo ja com os campos; so os que tem valor (nada para limpar num contato novo) ----
  _reiniciarCacheAC();
  roteador = rota();
  chamadas = [];
  r = await executarAC(dados);
  assert.deepStrictEqual([r.status, r.contato], ['enviado', 'criado']);
  assert.deepStrictEqual(chamadas.find((c) => c.url.endsWith('/contact/sync')).corpo.contact, {
    email: 'ana@empresa.com.br', firstName: 'TESTE', lastName: 'THAMIRES RIOS', orgname: 'Teste Buzzmonitor',
    fieldValues: [{ field: '851', value: URL_CONV }, { field: '845', value: 'evento' }, { field: '848', value: 'captacao-buzz-compass' }],
  });
  assert.strictEqual(chamadas.find((c) => c.url.endsWith('/contactTags')).corpo.contactTag.contact, '700');
  assert(!chamadas.some((c) => c.metodo === 'PUT'));

  // ---- 3) UTMs na URL da pagina (QR de cartaz do evento): valem as da URL, nos dois casos (criado e atualizado) ----
  const urlCartaz = 'https://buzzcompass.buzzmonitor.com/?utm_source=social&utm_medium=cartaz&utm_campaign=marketing-day&utm_content=captacao-cartaz-a&utm_term=compass';
  _reiniciarCacheAC(); roteador = existente(); chamadas = [];
  await executarAC({ ...dados, urlConversao: urlCartaz });
  assert.deepStrictEqual(comoMapa(valoresDoPut()), { 851: urlCartaz, 845: 'social', 846: 'cartaz', 847: 'marketing-day', 848: 'captacao-cartaz-a', 849: 'compass' }, 'atualizado: URL e as 5 UTMs da pagina');
  _reiniciarCacheAC(); roteador = rota(); chamadas = [];
  await executarAC({ ...dados, urlConversao: urlCartaz });
  assert.deepStrictEqual(comoMapa(chamadas.find((c) => c.url.endsWith('/contact/sync')).corpo.contact.fieldValues), { 851: urlCartaz, 845: 'social', 846: 'cartaz', 847: 'marketing-day', 848: 'captacao-cartaz-a', 849: 'compass' }, 'criado: idem');
  // UTM parcial: source vem da URL, content cai no padrao, o resto vazio
  _reiniciarCacheAC(); roteador = rota(); chamadas = [];
  await executarAC({ ...dados, urlConversao: URL_CONV + '?utm_source=blog' });
  assert.deepStrictEqual(comoMapa(chamadas.find((c) => c.url.endsWith('/contact/sync')).corpo.contact.fieldValues), { 851: URL_CONV + '?utm_source=blog', 845: 'blog', 848: 'captacao-buzz-compass' });

  // ---- 4) padroes configuraveis sem mexer no codigo (ex.: campanha do evento) ----
  limparEnv();
  process.env.TOTEM_UTM_CAMPAIGN_PADRAO = 'marketing-day';
  process.env.TOTEM_UTM_MEDIUM_PADRAO = 'totem';
  process.env.TOTEM_UTM_SOURCE_PADRAO = 'evento';
  _reiniciarCacheAC(); roteador = rota(); chamadas = [];
  await executarAC(dados);
  assert.deepStrictEqual(comoMapa(chamadas.find((c) => c.url.endsWith('/contact/sync')).corpo.contact.fieldValues), { 851: URL_CONV, 845: 'evento', 846: 'totem', 847: 'marketing-day', 848: 'captacao-buzz-compass' });
  // a URL manda mais que o padrao
  _reiniciarCacheAC(); roteador = rota(); chamadas = [];
  await executarAC({ ...dados, urlConversao: URL_CONV + '?utm_campaign=outra' });
  assert.strictEqual(comoMapa(chamadas.find((c) => c.url.endsWith('/contact/sync')).corpo.contact.fieldValues)[847], 'outra');
  limparEnv();

  // ---- 5) busca exata: e-mail parecido nao e o mesmo contato; e-mail com + vai codificado ----
  _reiniciarCacheAC(); roteador = rota({ contatos: [{ id: '56', email: 'ana@empresa.com.br.outro.com' }, { id: '57', email: 'maria.ana@empresa.com.br' }] }); chamadas = [];
  r = await executarAC(dados);
  assert.strictEqual(r.contato, 'criado', 'so igualdade exata de e-mail conta');
  _reiniciarCacheAC(); roteador = rota(); chamadas = [];
  await executarAC({ ...dados, email: 'ana+compass@empresa.com.br' });
  assert(chamadas[0].url.endsWith('/contacts?email=ana%2Bcompass%40empresa.com.br'), chamadas[0].url);

  // ---- 6) campos achados por titulo (sem acento/maiuscula), em varias paginas, com cache de 10 min ----
  _reiniciarCacheAC();
  const pagina1 = { fields: Array.from({ length: 100 }, (_, i) => ({ id: String(1000 + i), title: 'Campo ' + i })), meta: { total: '104' } };
  const pagina2 = { fields: [{ id: '2001', title: 'outro' }, { id: '2002', title: 'URL CONVERSAO [AUTO]' }, { id: '2003', title: 'utm source [auto]' }, { id: '2004', title: 'UTM Content [AUTO]' }], meta: { total: '104' } };
  roteador = (url, metodo) => {
    if (url.includes('/fields?limit=100&offset=0')) return { status: 200, json: pagina1 };
    if (url.includes('/fields?limit=100&offset=100')) return { status: 200, json: pagina2 };
    return existente()(url, metodo);
  };
  chamadas = [];
  await executarAC(dados);
  assert.deepStrictEqual(comoMapa(valoresDoPut()), { 2002: URL_CONV, 2003: 'evento', 2004: 'captacao-buzz-compass' }, 'achou na 2a pagina');
  chamadas = [];
  await executarAC(dados);
  assert(!chamadas.some((c) => c.url.includes('/fields')), 'mapa de campos guardado: o lead seguinte nao procura de novo');

  // ---- 7) falta algum campo no AC (ex.: nao ha UTM Term nem UTM Content): o que existe e preenchido, o resto vira aviso ----
  _reiniciarCacheAC();
  roteador = existente({ campos: { fields: [{ id: '851', title: 'URL Conversão [Auto]' }, { id: '845', title: 'UTM Source [Auto]' }], meta: { total: '2' } } });
  chamadas = [];
  r = await executarAC(dados);
  assert.deepStrictEqual([r.status, r.contato, r.avisos], ['enviado', 'atualizado', ['campo_utm_content_nao_encontrado']], 'so avisa dos campos que tinham valor para gravar');
  assert.deepStrictEqual(comoMapa(valoresDoPut()), { 851: URL_CONV, 845: 'evento' });
  assert(chamadas.some((c) => c.url.endsWith('/contactTags')), 'a tag e aplicada mesmo assim');

  // ---- 8) nenhum campo de rastreio no AC: contato e tag seguem, avisos completos, nada a gravar nos campos ----
  _reiniciarCacheAC();
  roteador = existente({ campos: { fields: [{ id: '1', title: 'Cargo' }], meta: { total: '1' } } });
  chamadas = [];
  r = await executarAC(dados);
  assert.strictEqual(r.status, 'enviado');
  assert.deepStrictEqual(r.avisos, ['campo_url_conversao_nao_encontrado', 'campo_utm_source_nao_encontrado', 'campo_utm_content_nao_encontrado']);
  assert(!chamadas.some((c) => c.metodo === 'PUT'), 'sem campos, nada a atualizar no contato');
  assert(chamadas.some((c) => c.url.endsWith('/contactTags')));
  chamadas = [];
  await executarAC(dados);
  assert(!chamadas.some((c) => c.url.includes('/fields')), 'dentro dos 10 min nao repete a busca, mesmo sem achar');

  // ---- 9) o AC nao lista os campos (erro): contato e tag seguem, aviso claro ----
  _reiniciarCacheAC();
  roteador = (url, metodo) => (url.includes('/fields?') ? { status: 500, json: {} } : existente()(url, metodo));
  chamadas = [];
  r = await executarAC(dados);
  assert.deepStrictEqual([r.status, r.avisos], ['enviado', ['campos_de_rastreio_indisponiveis']]);
  assert(!chamadas.some((c) => c.metodo === 'PUT') && chamadas.some((c) => c.url.endsWith('/contactTags')));

  // ---- 10) ID do campo de URL forcado por variavel ----
  _reiniciarCacheAC(); limparEnv();
  process.env.ACTIVECAMPAIGN_URL_CONVERSAO_FIELD_ID = '4242';
  roteador = existente(); chamadas = [];
  await executarAC(dados);
  assert.strictEqual(comoMapa(valoresDoPut())['4242'], URL_CONV);
  limparEnv();

  // ---- 11) busca do contato falhou: o lead nao se perde; o sync tambem nao duplica por e-mail ----
  _reiniciarCacheAC();
  roteador = (url, metodo) => (url.includes('/contacts?email=') ? { status: 500, json: {} } : rota()(url, metodo));
  chamadas = [];
  r = await executarAC(dados);
  assert.deepStrictEqual([r.status, r.avisos], ['enviado', ['busca_contato_falhou']]);
  assert(chamadas.some((c) => c.url.endsWith('/contact/sync')));

  // ---- 12) falha ao atualizar o existente: reportada como falha ----
  _reiniciarCacheAC();
  roteador = (url, metodo) => (metodo === 'PUT' ? { status: 403, json: {} } : existente()(url, metodo));
  assert.strictEqual((await executarAC(dados)).status, 'falhou');

  // ---- 13) nunca cria negocio ----
  assert(!chamadas.some((c) => /deal/i.test(c.url)));

  // ---- 13b) reconhecimento dos campos: grafias, [AUTO] obrigatorio, so campos de texto ----
  const camposVariados = (lista) => ({ fields: lista, meta: { total: String(lista.length) } });
  const mapaDe = async (lista, extra = {}) => {
    _reiniciarCacheAC();
    roteador = existente({ campos: camposVariados(lista) });
    chamadas = [];
    await executarAC({ ...dados, urlConversao: URL_CONV + '?utm_medium=m&utm_campaign=c&utm_term=t', ...extra });
    return Object.fromEntries(valoresDoPut().map((f) => [f.field, f.value]));
  };
  // "Campaign", "Campaing" (grafia da conta real) e "Campanha" servem; o numerado e o sem [AUTO] nao
  assert.strictEqual((await mapaDe([T(1, 'UTM Campaign [AUTO]'), T(2, 'UTM Campaign 1')]))['1'], 'c');
  assert.strictEqual((await mapaDe([T(1, 'UTM Campaing [AUTO]'), T(2, 'UTM Campaign 1')]))['1'], 'c');
  assert.strictEqual((await mapaDe([T(1, 'UTM Campanha [AUTO]'), T(2, 'UTM Campaign 3')]))['1'], 'c');
  // so existe o campo numerado ou o sem [AUTO]: NAO escreve em nenhum (melhor avisar do que gravar no campo errado)
  chamadas = [];
  _reiniciarCacheAC();
  roteador = existente({ campos: camposVariados([T(1, 'UTM Campaign 1'), T(2, 'UTM Campaign'), T(3, 'UTM Medium [AUTO]')]) });
  r = await executarAC({ ...dados, urlConversao: URL_CONV + '?utm_medium=m&utm_campaign=c' });
  assert(r.avisos.includes('campo_utm_campaign_nao_encontrado'), 'avisa que nao achou o campo de campanha: ' + r.avisos);
  assert.deepStrictEqual(valoresDoPut().map((f) => f.field).filter((id) => id === '1' || id === '2'), [], 'nada escrito nos campos numerado/sem [AUTO]');
  // campo com o titulo certo mas de outro tipo (lista suspensa, data) nunca recebe texto
  assert.deepStrictEqual(Object.keys(await mapaDe([T(1, 'UTM Medium [AUTO]', 'dropdown'), T(2, 'UTM Term [AUTO]', 'date'), T(3, 'UTM Campaing [AUTO]')])).sort(), ['3'], 'so o campo de texto e usado');

  // ---- 14) valoresDeRastreio: limpeza do que vem do navegador ----
  limparEnv();
  const sujo = valoresDeRastreio(URL_CONV + '?utm_source=' + encodeURIComponent('even\u0000to\n') + '&utm_content=' + 'x'.repeat(500));
  assert.strictEqual(sujo.utm_source, 'even to', 'caractere de controle some');
  assert.strictEqual(sujo.utm_content.length, 200, 'corta em 200');
  assert.deepStrictEqual([valoresDeRastreio('').utm_source, valoresDeRastreio('lixo').utm_content, valoresDeRastreio(undefined).url_conversao], ['evento', 'captacao-buzz-compass', ''], 'sem URL valida: so os padroes');

  // ---- 15) URL de conversao enviada pelo navegador: so a pagina do totem do proprio projeto ----
  const req = { headers: { host: 'buzzcompass.buzzmonitor.com' } };
  // o totem fica na raiz do dominio; /totem (endereco antigo, que redireciona) e aceito e vira a raiz
  const padrao = 'https://buzzcompass.buzzmonitor.com/';
  assert.strictEqual(urlDeConversao(req, 'https://buzzcompass.buzzmonitor.com/'), padrao);
  assert.strictEqual(urlDeConversao(req, 'https://buzzcompass.buzzmonitor.com'), padrao);
  assert.strictEqual(urlDeConversao(req, 'https://buzzcompass.buzzmonitor.com/totem'), padrao, '/totem antigo vira a raiz');
  assert.strictEqual(urlDeConversao(req, 'https://buzzcompass.buzzmonitor.com/?utm_source=evento&utm_medium=qr&idle=8000&fbclid=abc#topo'),
    'https://buzzcompass.buzzmonitor.com/?utm_source=evento&utm_medium=qr', 'mantem as UTMs; tira idle, fbclid e #hash');
  assert.strictEqual(urlDeConversao(req, 'https://buzzcompass.buzzmonitor.com/totem?utm_source=evento&utm_medium=qr'),
    'https://buzzcompass.buzzmonitor.com/?utm_source=evento&utm_medium=qr', 'link antigo com /totem e UTMs vira raiz com as UTMs');
  assert.strictEqual(urlDeConversao(req, 'https://buzzmonitor-lp-buzz-compass-latam.vercel.app/'), 'https://buzzmonitor-lp-buzz-compass-latam.vercel.app/');
  for (const ruim of ['https://site-malicioso.com/', 'http://buzzcompass.buzzmonitor.com/', 'javascript:alert(1)', 'nao-e-url', '', undefined, null,
    'https://buzzcompass.buzzmonitor.com/outra-pagina', 'https://buzzcompass.buzzmonitor.com/lp', 'https://buzzcompass.buzzmonitor.com.evil.com/']) {
    assert.strictEqual(urlDeConversao(req, ruim), padrao, 'vira o padrao: ' + ruim);
  }
  assert(urlDeConversao(req, 'https://buzzcompass.buzzmonitor.com/?utm_campaign=' + 'x'.repeat(900)).length <= 500, 'corta em 500');

  console.log('ac-contato-existente.test.js: ok');
})().catch((e) => { console.error(e); process.exit(1); });
