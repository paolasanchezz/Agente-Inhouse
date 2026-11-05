// Testes dos destinos do lead (ActiveCampaign, planilha, e-mail com QR) e do PNG do QR:
//   node landing-pages/buzzmonitor/buzz-compass-latam/tests/leads-destinos.test.js
// A rede e simulada (fetch trocado): nada e enviado de verdade.
const assert = require('assert');
const zlib = require('zlib');

let chamadas = [];
let roteador = () => ({ status: 200, json: {} });
global.fetch = async (url, opts) => {
  chamadas.push({ url: String(url), opts: opts || {}, corpo: opts && opts.body ? JSON.parse(opts.body) : null });
  const r = await roteador(String(url), opts || {}, chamadas.length);
  return { ok: r.status >= 200 && r.status < 300, status: r.status, json: async () => r.json || {}, text: async () => (r.text !== undefined ? r.text : JSON.stringify(r.json || {})) };
};
const limparEnv = () => ['SENDGRID_API_KEY', 'TOTEM_EMAIL_FROM', 'RESEND_API_KEY', 'TOTEM_LEADS_WEBHOOK_URL', 'TOTEM_LEADS_WEBHOOK_TOKEN', 'ACTIVECAMPAIGN_API_URL', 'ACTIVECAMPAIGN_API_TOKEN', 'ACTIVECAMPAIGN_TOTEM_TAG_ID', 'ACTIVECAMPAIGN_TAG_ID', 'ACTIVECAMPAIGN_TOTEM_LIST_ID', 'TOTEM_AC_TAG_NOME', 'TOTEM_BASE_URL'].forEach((k) => delete process.env[k]);

const handlerLead = require('../api/totem-lead.js');
const { syncActiveCampaign, enviarWebhook, htmlDoEmail } = handlerLead;
const handlerQr = require('../api/qr.js');
const { matrizParaPng, crc32 } = require('../api/_lib/png.js');
const QR = require('../assets/qr.js');

function resHttp() {
  return { statusCode: 200, headers: {}, corpo: null, setHeader(k, v) { this.headers[k] = v; }, json(o) { this.corpo = o; return this; }, end(b) { this.corpo = b || null; return this; } };
}

(async () => {
  // ---------- ActiveCampaign ----------
  limparEnv();
  process.env.ACTIVECAMPAIGN_API_URL = 'https://ac.test/';
  process.env.ACTIVECAMPAIGN_API_TOKEN = 'tok';

  // 1) tag ja existe: acha pelo NOME (so a igualdade exata conta, "Buzz Compass 2024" nao serve), nao cria outra
  process.env.TOTEM_AC_TAG_NOME = 'Tag Existente';
  roteador = (url) => {
    if (url.includes('/tags?search=')) return { status: 200, json: { tags: [{ id: '5', tag: 'Tag Existente 2024' }, { id: '7', tag: 'tag existente' }] } };
    if (url.endsWith('/contact/sync')) return { status: 200, json: { contact: { id: '321' } } };
    return { status: 201, json: {} };
  };
  chamadas = [];
  assert.strictEqual(await syncActiveCampaign({ email: 'a@b.com', nome: 'Ana Maria da Silva', marca: 'Natura' }), 'enviado');
  const sync = chamadas.find((c) => c.url.endsWith('/contact/sync'));
  assert.strictEqual(sync.url, 'https://ac.test/api/3/contact/sync', 'barra final da URL base nao duplica');
  assert.deepStrictEqual([sync.corpo.contact.firstName, sync.corpo.contact.lastName, sync.corpo.contact.orgname], ['Ana', 'Maria da Silva', 'Natura'], 'nome separado em primeiro e sobrenome');
  assert.strictEqual(sync.opts.headers['Api-Token'], 'tok');
  const tag = chamadas.find((c) => c.url.endsWith('/contactTags'));
  assert.deepStrictEqual(tag.corpo.contactTag, { contact: '321', tag: '7' }, 'usa o ID da tag de nome igual');
  assert(!chamadas.some((c) => c.url.endsWith('/api/3/tags')), 'nao cria tag que ja existe');
  assert(!chamadas.some((c) => /deal/i.test(c.url)), 'nunca cria deal');
  assert(!chamadas.some((c) => /contactLists/.test(c.url)), 'sem lista configurada, nao inscreve em lista');

  // 2) tag nao existe: cria (tipo contato) e usa o ID novo; a segunda pessoa reaproveita o ID (nao busca de novo)
  process.env.TOTEM_AC_TAG_NOME = 'Tag Nova';
  roteador = (url) => {
    if (url.includes('/tags?search=')) return { status: 200, json: { tags: [] } };
    if (url.endsWith('/api/3/tags')) return { status: 201, json: { tag: { id: '88', tag: 'Tag Nova' } } };
    if (url.endsWith('/contact/sync')) return { status: 200, json: { contact: { id: '1' } } };
    return { status: 201, json: {} };
  };
  chamadas = [];
  assert.strictEqual(await syncActiveCampaign({ email: 'a@b.com', nome: 'Ana', marca: 'X' }), 'enviado');
  const cria = chamadas.find((c) => c.url.endsWith('/api/3/tags'));
  assert.strictEqual(cria.corpo.tag.tag, 'Tag Nova');
  assert.strictEqual(cria.corpo.tag.tagType, 'contact');
  assert.strictEqual(chamadas.find((c) => c.url.endsWith('/contactTags')).corpo.contactTag.tag, '88');
  chamadas = [];
  await syncActiveCampaign({ email: 'c@d.com', nome: 'Beto', marca: 'Y' });
  assert(!chamadas.some((c) => c.url.includes('/tags')), 'ID da tag fica guardado: sem nova busca nem criacao');
  assert.strictEqual(chamadas.find((c) => c.url.endsWith('/contact/sync')).corpo.contact.lastName, '', 'sem sobrenome');

  // 3) tag padrao se nada for configurado = "Buzz Compass LATAM"
  delete process.env.TOTEM_AC_TAG_NOME;
  roteador = (url) => {
    if (url.includes('/tags?search=')) return { status: 200, json: { tags: [{ id: '42', tag: 'Buzz Compass LATAM' }] } };
    if (url.endsWith('/contact/sync')) return { status: 200, json: { contact: { id: '9' } } };
    return { status: 201, json: {} };
  };
  chamadas = [];
  await syncActiveCampaign({ email: 'a@b.com', nome: 'Ana', marca: 'X' });
  assert(decodeURIComponent(chamadas.find((c) => c.url.includes('/tags?search=')).url).endsWith('search=Buzz Compass LATAM'), 'procura "Buzz Compass LATAM"');
  assert.strictEqual(chamadas.find((c) => c.url.endsWith('/contactTags')).corpo.contactTag.tag, '42');

  // 4) ID fixo por variavel dispensa a busca; 422 (contato ja tem a tag) conta como sucesso; lista so se configurada
  process.env.ACTIVECAMPAIGN_TOTEM_TAG_ID = '99';
  process.env.ACTIVECAMPAIGN_TOTEM_LIST_ID = '3';
  roteador = (url) => {
    if (url.endsWith('/contact/sync')) return { status: 200, json: { contact: { id: '9' } } };
    return { status: 422, json: {} };
  };
  chamadas = [];
  assert.strictEqual(await syncActiveCampaign({ email: 'a@b.com', nome: 'Ana', marca: 'X' }), 'enviado', '422 de duplicado e sucesso');
  assert(!chamadas.some((c) => c.url.includes('/tags')), 'com ID fixo nao busca tag');
  assert.deepStrictEqual(chamadas.find((c) => c.url.endsWith('/contactLists')).corpo.contactList, { list: '3', contact: '9', status: 1 });
  delete process.env.ACTIVECAMPAIGN_TOTEM_TAG_ID;
  delete process.env.ACTIVECAMPAIGN_TOTEM_LIST_ID;

  // 5) falha passageira (5xx) tenta de novo e o lead nao se perde; erro 4xx (token ruim) nao repete e e relatado
  process.env.TOTEM_AC_TAG_NOME = 'Tag Retry';
  let tentativasSync = 0;
  roteador = (url) => {
    if (url.endsWith('/contact/sync')) { tentativasSync++; return tentativasSync === 1 ? { status: 503, json: {} } : { status: 200, json: { contact: { id: '4' } } }; }
    if (url.includes('/tags?search=')) return { status: 200, json: { tags: [{ id: '6', tag: 'Tag Retry' }] } };
    return { status: 201, json: {} };
  };
  assert.strictEqual(await syncActiveCampaign({ email: 'a@b.com', nome: 'Ana', marca: 'X' }), 'enviado');
  assert.strictEqual(tentativasSync, 2, '5xx: segunda tentativa');
  let t401 = 0;
  roteador = (url) => { if (url.endsWith('/contact/sync')) { t401++; return { status: 401, json: {} }; } return { status: 200, json: {} }; };
  assert.strictEqual(await syncActiveCampaign401(), 'falhou');
  async function syncActiveCampaign401() { return syncActiveCampaign({ email: 'a@b.com', nome: 'Ana', marca: 'X' }); }
  assert.strictEqual(t401, 1, '4xx nao repete');
  // sem credencial: desligado
  delete process.env.ACTIVECAMPAIGN_API_TOKEN;
  assert.strictEqual(await syncActiveCampaign({ email: 'a@b.com', nome: 'Ana', marca: 'X' }), 'nao_configurado');

  // 6) URL do AC colada com /api/3 ou barras no fim, ou com espaco: o sistema limpa em vez de montar /api/3/api/3/...
  process.env.ACTIVECAMPAIGN_API_TOKEN = '  tok  ';
  process.env.ACTIVECAMPAIGN_TOTEM_TAG_ID = '7';
  for (const colada of ['https://ac.test/api/3', 'https://ac.test/api/3/', 'https://ac.test///', ' https://ac.test ']) {
    process.env.ACTIVECAMPAIGN_API_URL = colada;
    roteador = (url) => (url.endsWith('/contact/sync') ? { status: 200, json: { contact: { id: '1' } } } : { status: 201, json: {} });
    chamadas = [];
    assert.strictEqual(await syncActiveCampaign({ email: 'a@b.com', nome: 'Ana', marca: 'X' }), 'enviado', 'URL colada: ' + colada);
    assert(chamadas.length >= 2 && chamadas.every((c) => c.url.startsWith('https://ac.test/api/3/') && !c.url.includes('/api/3/api/3')), 'URLs limpas: ' + chamadas.map((c) => c.url).join(' | '));
    assert.strictEqual(chamadas.find((c) => c.url.endsWith('/contact/sync')).url, 'https://ac.test/api/3/contact/sync');
    assert(chamadas.every((c) => c.opts.headers['Api-Token'] === 'tok'), 'chave sem espacos em todas as chamadas');
  }
  delete process.env.ACTIVECAMPAIGN_TOTEM_TAG_ID;

  // 7) AC sem responder (timeout): o log diz QUAL etapa e quanto esperou, nao so "operation was aborted"; o lead nao quebra
  process.env.ACTIVECAMPAIGN_API_URL = 'https://ac.test';
  process.env.ACTIVECAMPAIGN_API_TOKEN = 'tok';
  const fetchOriginal = global.fetch;
  const errosLogados = [];
  const consoleErrorOriginal = console.error;
  console.error = (...a) => errosLogados.push(a.join(' '));
  global.fetch = async () => { const e = new Error('This operation was aborted'); e.name = 'AbortError'; throw e; };
  const resultadoTimeout = await syncActiveCampaign({ email: 'a@b.com', nome: 'Ana', marca: 'X' });
  global.fetch = fetchOriginal;
  console.error = consoleErrorOriginal;
  assert.strictEqual(resultadoTimeout, 'falhou');
  assert(errosLogados.some((l) => /ac contato sem resposta em \d+ms/.test(l)), 'log da etapa: ' + errosLogados.join(' | '));
  assert(errosLogados.some((l) => /activecampaign falhou ac_contato_timeout/.test(l)), 'motivo especifico no log: ' + errosLogados.join(' | '));
  assert(!errosLogados.some((l) => /This operation was aborted/.test(l.replace(/activecampaign falhou ac_contato_timeout/, ''))), 'sem a mensagem generica');

  // ---------- Planilha (webhook do Apps Script) ----------
  limparEnv();
  process.env.TOTEM_LEADS_WEBHOOK_URL = 'https://script.google.test/macros/s/abc/exec';
  process.env.TOTEM_LEADS_WEBHOOK_TOKEN = 'segredo-123';
  const lead = { origem: 'buzz-compass-totem', criado_em: '2026-10-21T12:00:00.000Z', nome: 'Ana', email: 'a@b.com', marca: 'Natura', segmento: 'Cosméticos', instagram: '', concorrentes: ['Avon'], link: 'https://x/totem-resultado?m=Natura' };
  roteador = () => ({ status: 200, text: '{"ok":true}' });
  chamadas = [];
  assert.strictEqual(await enviarWebhook(lead), 'enviado');
  assert.deepStrictEqual([chamadas[0].corpo.token, chamadas[0].corpo.email, chamadas[0].corpo.marca, chamadas[0].corpo.concorrentes], ['segredo-123', 'a@b.com', 'Natura', ['Avon']], 'token e campos do lead no corpo');
  // o Apps Script responde 200 mesmo recusando: {"ok":false} tem que contar como falha (e nao repete: e erro de dado)
  roteador = () => ({ status: 200, text: '{"ok":false,"erro":"token"}' });
  chamadas = [];
  assert.strictEqual(await enviarWebhook(lead), 'falhou', 'recusa do script e falha');
  assert.strictEqual(chamadas.length, 1, 'recusa nao repete');
  // oscilacao 500: repete uma vez e passa
  let n500 = 0;
  roteador = () => (++n500 === 1 ? { status: 500, text: 'erro' } : { status: 200, text: '{"ok":true}' });
  assert.strictEqual(await enviarWebhook(lead), 'enviado');
  assert.strictEqual(n500, 2);
  // sem token configurado, nao manda campo token
  delete process.env.TOTEM_LEADS_WEBHOOK_TOKEN;
  roteador = () => ({ status: 200, text: '{"ok":true}' });
  chamadas = [];
  await enviarWebhook(lead);
  assert(!('token' in chamadas[0].corpo));

  // ---------- Handler completo: os 3 destinos independentes + QR no e-mail ----------
  limparEnv();
  process.env.RESEND_API_KEY = 're_teste';
  process.env.TOTEM_EMAIL_FROM = 'Buzzmonitor <compass@exemplo.com>';
  process.env.TOTEM_LEADS_WEBHOOK_URL = 'https://script.google.test/exec';
  process.env.ACTIVECAMPAIGN_API_URL = 'https://ac.test';
  process.env.ACTIVECAMPAIGN_API_TOKEN = 'tok';
  process.env.TOTEM_AC_TAG_NOME = 'Tag Handler';
  roteador = (url) => {
    if (url.includes('resend.com')) return { status: 200, json: { id: 'x' } };
    if (url.includes('script.google')) return { status: 200, text: '{"ok":true}' };
    if (url.includes('/tags?search=')) return { status: 200, json: { tags: [{ id: '2', tag: 'Tag Handler' }] } };
    if (url.endsWith('/contact/sync')) return { status: 200, json: { contact: { id: '5' } } };
    return { status: 201, json: {} };
  };
  const chamarLead = (body) => new Promise((resolve) => {
    const res = { statusCode: 200, headers: {}, setHeader() {}, json(o) { resolve({ status: this.statusCode, body: o }); return this; } };
    handlerLead({ method: 'POST', body, headers: { host: 'buzzcompass.buzzmonitor.com' }, query: {} }, res);
  });
  const valido = { nome: 'Ana Souza', email: 'ana@empresa.com.br', marca: 'Natura', segmento: 'Cosméticos e Beleza', concorrentes: ['Boticário'], _ts: Date.now() - 5000 };
  chamadas = [];
  let r = await chamarLead(valido);
  assert.deepStrictEqual([r.body.email, r.body.webhook, r.body.crm], ['enviado', 'enviado', 'enviado']);
  const email = chamadas.find((c) => c.url.includes('resend.com')).corpo;
  const qrEsperado = 'https://buzzcompass.buzzmonitor.com/es/api/qr?d=' + encodeURIComponent(r.body.link);
  assert(email.html.includes(qrEsperado.replace(/&/g, '&amp;')), 'o e-mail tem a imagem do QR apontando para o resultado');
  assert(email.html.includes('¿Quieres mostrárselo a tu equipo?') && email.html.includes('Reenvía este correo'), 'texto de compartilhamento');
  assert(email.text.includes(r.body.link) && /reenvía/i.test(email.text), 'versao em texto tambem leva o link e o convite a encaminhar');
  assert(!/—/.test(email.html + email.text), 'sem travessao no texto publico');
  assert.strictEqual(email.subject, 'Tu Buzz Compass de Natura ya está listo');

  // 3 destinos independentes: se o e-mail falhar (remetente nao verificado), AC e planilha seguem; e vice-versa
  roteador = (url) => {
    if (url.includes('resend.com')) return { status: 403, text: '{"message":"domain not verified"}' };
    if (url.includes('script.google')) return { status: 200, text: '{"ok":true}' };
    if (url.includes('/tags?search=')) return { status: 200, json: { tags: [{ id: '2', tag: 'Tag Handler' }] } };
    if (url.endsWith('/contact/sync')) return { status: 200, json: { contact: { id: '5' } } };
    return { status: 201, json: {} };
  };
  r = await chamarLead(valido);
  assert.deepStrictEqual([r.status, r.body.ok, r.body.email, r.body.webhook, r.body.crm], [200, true, 'falhou', 'enviado', 'enviado'], 'e-mail fora do ar nao derruba AC nem planilha');
  roteador = (url) => (url.includes('resend.com') ? { status: 200, json: {} } : url.includes('script.google') ? { status: 500, text: 'x' } : { status: 401, json: {} });
  r = await chamarLead(valido);
  assert.deepStrictEqual([r.body.email, r.body.webhook, r.body.crm], ['enviado', 'falhou', 'falhou'], 'e-mail sai mesmo com planilha e AC fora');

  // e-mail sem QR (link longo demais ou sem qrUrl) continua valido, com botao e link
  const htmlSemQr = htmlDoEmail({ nome: 'Ana', marca: 'X', link: 'https://x/totem-resultado?m=X' });
  assert(!/<img /.test(htmlSemQr) && /Ver mi Compass/.test(htmlSemQr));
  // marca e nome com HTML: escapados
  const htmlHostil = htmlDoEmail({ nome: '<img src=x onerror=1>', marca: '"><script>alert(1)</script>', link: 'https://x/?a=1&b="2"', qrUrl: 'https://x/api/qr?d=a&b="c"' });
  assert(!/<script>/.test(htmlHostil) && !/<img src=x/.test(htmlHostil), 'html escapado');

  // ---------- Copy do e-mail: paragrafo com a marca e caixa final com o convite para a demonstracao ----------
  const { urlDemo } = handlerLead;
  const html = htmlDoEmail({ nome: 'Ana Souza', marca: 'Natura', link: 'https://x/totem-resultado?m=Natura', qrUrl: 'https://x/api/qr?d=a' });
  assert(html.includes('Reunimos conversaciones reales de los últimos 30 días sobre Natura en la base de datos de Buzzmonitor Trends, comparamos a Natura con sus competidores y escribimos el diagnóstico. Ábrelo desde tu celular o tu computadora.'), 'paragrafo com a marca nos dois lugares');
  for (const frase of [
    'Esto es solo el 10% de lo que Buzzmonitor puede hacer por tu marca',
    'Con un proyecto de monitoreo dedicado a tu marca y todos tus canales conectados, la plataforma te entrega análisis más completos y estratégicos.',
    'Y en una sola plataforma centralizas monitoreo, competidores, atención al cliente, analytics, dashboards, reportes con IA y programación de publicaciones.',
    'Míralo funcionando en una llamada con uno de nuestros especialistas.',
    'Quiero agendar mi demo gratis',
  ]) assert(html.includes(frase), 'caixa final traz: ' + frase);
  // ordem: a caixa em destaque vem depois do bloco de compartilhar e antes do rodape com o endereco de reserva
  const posCompartilhar = html.indexOf('¿Quieres mostrárselo a tu equipo?');
  const posCaixa = html.indexOf('Esto es solo el 10%');
  const posRodape = html.indexOf('Si el botón no abre');
  assert(posCompartilhar > 0 && posCompartilhar < posCaixa && posCaixa < posRodape, 'ordem dos blocos do e-mail');
  assert(/linear-gradient\(135deg,#EB7C2E,#DE2451\)/.test(html) && /background:#EB7C2E;/.test(html), 'caixa laranja/rosa, com cor solida de reserva para clientes sem gradiente');
  // o botao leva a pagina de demonstracao, com as UTMs do Compass
  const botao = html.match(/<a href="([^"]+)"[^>]*>Quiero agendar mi demo gratis<\/a>/);
  assert(botao, 'botao de demonstracao existe');
  const u = new URL(botao[1].replace(/&amp;/g, '&'));
  // UTMs no padrao de conhecimento/config/convencao-utm.md: utm_source = canal (vocabulario fechado: email), utm_content = {tipo-de-pagina}-{conteudo}
  assert.deepStrictEqual([u.origin, u.searchParams.get('utm_source'), u.searchParams.get('utm_medium'), u.searchParams.get('utm_content'), u.searchParams.has('utm_campaign')], ['https://content.buzzmonitor.com', 'buzz-compass', 'e-mail-resultado', 'resultado-buzz-compass', false]);
  // marca com HTML nao quebra a copy nova
  assert(!/<script>/.test(htmlDoEmail({ nome: 'A', marca: '<script>x</script>', link: 'https://x/' })), 'marca escapada tambem no paragrafo novo');

  // urlDemo: variavel de ambiente troca o destino; UTMs que o endereco ja tem sao respeitadas; valor invalido nao quebra o e-mail
  process.env.TOTEM_DEMO_URL = 'https://buzzmonitor.com.br/agende-uma-demonstracao';
  assert.strictEqual(urlDemo(), 'https://buzzmonitor.com.br/agende-uma-demonstracao?utm_source=buzz-compass&utm_medium=e-mail-resultado&utm_content=resultado-buzz-compass');
  process.env.TOTEM_DEMO_URL = 'https://buzzmonitor.com.br/demo?ref=abc&utm_source=outra';
  const comUtm = new URL(urlDemo());
  assert.deepStrictEqual([comUtm.searchParams.get('ref'), comUtm.searchParams.get('utm_source'), comUtm.searchParams.get('utm_medium')], ['abc', 'outra', 'e-mail-resultado'], 'nao sobrescreve utm existente; o que falta entra');
  for (const ruim of ['javascript:alert(1)', 'nao-e-url', '', 'ftp://x.com/a']) {
    process.env.TOTEM_DEMO_URL = ruim;
    assert(urlDemo().startsWith('https://content.buzzmonitor.com/plataforma-completa-social-media-latam?'), 'valor invalido cai no padrao: ' + ruim);
  }
  delete process.env.TOTEM_DEMO_URL;

  // a versao em texto do e-mail leva a mesma mensagem e o link da demonstracao
  process.env.RESEND_API_KEY = 're_teste';
  roteador = (url) => (url.includes('resend.com') ? { status: 200, json: {} } : { status: 200, text: '{"ok":true}', json: { contact: { id: '1' }, tags: [{ id: '1', tag: 'Tag Handler' }] } });
  chamadas = [];
  await chamarLead(valido);
  const texto2 = chamadas.find((c) => c.url.includes('resend.com')).corpo.text;
  assert(texto2.includes('Esto es solo el 10% de lo que Buzzmonitor puede hacer por tu marca') && texto2.includes('dedicado a tu marca') && /Quiero agendar mi demo gratis: https:\/\/content\.buzzmonitor\.com\/plataforma-completa-social-media-latam\?utm_source=buzz-compass&utm_medium=e-mail-resultado&utm_content=resultado-buzz-compass/.test(texto2), 'texto simples: ' + texto2.slice(-420));
  assert(!/—/.test(chamadas.find((c) => c.url.includes('resend.com')).corpo.html + texto2), 'sem travessao');

  // ---------- SendGrid: provedor preferencial quando ha SENDGRID_API_KEY ----------
  limparEnv();
  process.env.SENDGRID_API_KEY = 'SG.teste';
  process.env.RESEND_API_KEY = 're_teste';
  process.env.TOTEM_EMAIL_FROM = 'Buzzmonitor Compass <compass@exemplo.com>';
  roteador = (url) => (url.includes('sendgrid.com') ? { status: 202, text: '' } : { status: 200, json: { id: 'x' } });
  chamadas = [];
  r = await chamarLead(valido);
  assert.strictEqual(r.body.email, 'enviado', 'SendGrid responde 202 sem corpo: conta como enviado');
  assert(!chamadas.some((c) => c.url.includes('resend.com')), 'com as duas chaves, so o SendGrid envia');
  const sgChamada = chamadas.find((c) => c.url.includes('api.sendgrid.com/v3/mail/send'));
  assert(sgChamada, 'chamou a API de envio do SendGrid');
  assert.strictEqual(sgChamada.opts.headers.Authorization, 'Bearer SG.teste');
  const sg = sgChamada.corpo;
  assert.deepStrictEqual(sg.personalizations, [{ to: [{ email: 'ana@empresa.com.br' }] }]);
  assert.deepStrictEqual(sg.from, { email: 'compass@exemplo.com', name: 'Buzzmonitor Compass' }, 'remetente separado em nome e e-mail');
  assert.strictEqual(sg.subject, 'Tu Buzz Compass de Natura ya está listo');
  assert.deepStrictEqual(sg.content.map((c) => c.type), ['text/plain', 'text/html'], 'text/plain vem antes do html');
  assert(sg.content[1].value.includes('¿Quieres mostrárselo a tu equipo?') && sg.content[0].value.includes(r.body.link), 'mesmo conteudo do e-mail de sempre');
  assert(!/—/.test(sg.content[0].value + sg.content[1].value), 'sem travessao');
  assert.deepStrictEqual(sg.tracking_settings, { click_tracking: { enable: false, enable_text: false } }, 'links nao sao reescritos pelo SendGrid');
  // remetente sem nome
  process.env.TOTEM_EMAIL_FROM = 'compass@exemplo.com';
  chamadas = [];
  await chamarLead(valido);
  assert.deepStrictEqual(chamadas.find((c) => c.url.includes('sendgrid.com')).corpo.from, { email: 'compass@exemplo.com' });
  // sem remetente verificado nao ha padrao seguro: nao chama a API e os outros destinos seguem
  delete process.env.TOTEM_EMAIL_FROM;
  chamadas = [];
  r = await chamarLead(valido);
  assert.strictEqual(r.body.email, 'falhou');
  assert(!chamadas.some((c) => c.url.includes('sendgrid.com')), 'sem remetente nao chama o SendGrid');
  // API recusa (remetente nao verificado / chave invalida): falha so do e-mail
  process.env.TOTEM_EMAIL_FROM = 'Buzzmonitor <compass@exemplo.com>';
  roteador = (url) => (url.includes('sendgrid.com') ? { status: 403, text: '{"errors":[{"message":"The from address does not match a verified Sender Identity."}]}' } : { status: 200, json: {} });
  r = await chamarLead(valido);
  assert.strictEqual(r.body.email, 'falhou');
  // so SendGrid configurado (sem Resend) tambem funciona; so Resend continua funcionando como antes
  delete process.env.RESEND_API_KEY;
  roteador = (url) => (url.includes('sendgrid.com') ? { status: 202, text: '' } : { status: 200, json: {} });
  assert.strictEqual((await chamarLead(valido)).body.email, 'enviado');
  limparEnv();
  assert.strictEqual((await chamarLead(valido)).body.email, 'nao_configurado', 'sem nenhum provedor o e-mail fica desligado');

  // ---------- PNG do QR ----------
  assert.strictEqual(crc32(Buffer.from('123456789')), 0xcbf43926, 'CRC-32 com o vetor padrao');
  const texto = 'https://buzzcompass.buzzmonitor.com/totem-resultado?m=Natura&s=Cosm%C3%A9ticos+e+Beleza&c=Botic%C3%A1rio';
  const { modules, size } = QR.encode(texto, { ecc: 'M' });
  const png = matrizParaPng(modules, { escala: 8, margem: 3 });
  assert.deepStrictEqual([...png.subarray(0, 8)], [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a], 'assinatura PNG');
  // decodificacao independente: le IHDR e IDAT e confere modulo por modulo (centro de cada quadrado)
  let pos = 8; const blocos = {};
  while (pos < png.length) {
    const tam = png.readUInt32BE(pos); const tipo = png.toString('ascii', pos + 4, pos + 8);
    const dados = png.subarray(pos + 8, pos + 8 + tam);
    assert.strictEqual(png.readUInt32BE(pos + 8 + tam), crc32(png.subarray(pos + 4, pos + 8 + tam)), 'CRC do bloco ' + tipo);
    (blocos[tipo] = blocos[tipo] || []).push(dados); pos += 12 + tam;
  }
  const lado = blocos.IHDR[0].readUInt32BE(0);
  assert.strictEqual(lado, (size + 6) * 8);
  assert.deepStrictEqual([blocos.IHDR[0][8], blocos.IHDR[0][9]], [8, 0], '8 bits, tons de cinza');
  const cru = zlib.inflateSync(Buffer.concat(blocos.IDAT));
  assert.strictEqual(cru.length, (lado + 1) * lado);
  let divergentes = 0;
  for (let my = 0; my < size; my++) for (let mx = 0; mx < size; mx++) {
    const y = (my + 3) * 8 + 4, x = (mx + 3) * 8 + 4;
    const escuro = cru[y * (lado + 1) + 1 + x] === 0;
    if (escuro !== Boolean(modules[my][mx])) divergentes++;
  }
  assert.strictEqual(divergentes, 0, 'o PNG reproduz o QR modulo por modulo');
  assert.strictEqual(cru[1], 255, 'margem branca');

  // ---------- endpoint /api/qr ----------
  const linkBom = 'https://buzzcompass.buzzmonitor.com/totem-resultado?m=Natura&s=Moda';
  let rq = resHttp(); handlerQr({ method: 'GET', query: { d: linkBom }, headers: { host: 'buzzcompass.buzzmonitor.com' } }, rq);
  assert.strictEqual(rq.statusCode, 200);
  assert.strictEqual(rq.headers['Content-Type'], 'image/png');
  assert(/immutable/.test(rq.headers['Cache-Control']));
  assert(Buffer.isBuffer(rq.corpo) && rq.corpo.length > 500);
  // o mesmo link gera exatamente o mesmo PNG (deterministico: por isso pode ficar 1 ano no cache)
  let rq2 = resHttp(); handlerQr({ method: 'GET', query: { d: linkBom }, headers: { host: 'buzzcompass.buzzmonitor.com' } }, rq2);
  assert(rq.corpo.equals(rq2.corpo));
  // so links do proprio resultado: nada de QR para site de terceiros, outro caminho, http ou lixo
  const recusados = ['https://site-malicioso.com/totem-resultado?m=x', 'https://buzzcompass.buzzmonitor.com/login', 'http://buzzcompass.buzzmonitor.com/totem-resultado?m=x',
    'javascript:alert(1)', 'nao-e-url', '', undefined, 'https://buzzcompass.buzzmonitor.com.evil.com/totem-resultado?m=x'];
  for (const d of recusados) {
    rq = resHttp(); handlerQr({ method: 'GET', query: { d }, headers: { host: 'buzzcompass.buzzmonitor.com' } }, rq);
    assert.strictEqual(rq.statusCode, 400, 'recusa: ' + d);
    assert.strictEqual(rq.headers['Cache-Control'], 'no-store');
  }
  // host do projeto na Vercel e o da propria requisicao tambem valem (prévias e o endereco antigo)
  for (const [d, host] of [['https://buzzmonitor-lp-buzz-compass-latam.vercel.app/totem-resultado?m=x', 'qualquer'], ['https://preview-abc.vercel.app/totem-resultado?m=x', 'preview-abc.vercel.app']]) {
    rq = resHttp(); handlerQr({ method: 'GET', query: { d }, headers: { host } }, rq);
    assert.strictEqual(rq.statusCode, 200, 'aceita: ' + d);
  }
  rq = resHttp(); handlerQr({ method: 'POST', query: { d: linkBom }, headers: { host: 'buzzcompass.buzzmonitor.com' } }, rq);
  assert.strictEqual(rq.statusCode, 405);
  // link grande: cai de M para L e ainda gera; grande demais de verdade: 400 (o e-mail sai sem QR, so com o botao)
  const longo = 'https://buzzcompass.buzzmonitor.com/totem-resultado?m=' + 'a'.repeat(200); // 254 bytes: passa do limite do nivel M (213) e cabe no L (268)
  rq = resHttp(); handlerQr({ method: 'GET', query: { d: longo }, headers: { host: 'buzzcompass.buzzmonitor.com' } }, rq);
  assert.strictEqual(rq.statusCode, 200, 'link de 254 bytes cabe no nivel L');
  const enorme = 'https://buzzcompass.buzzmonitor.com/totem-resultado?m=' + 'a'.repeat(400);
  rq = resHttp(); handlerQr({ method: 'GET', query: { d: enorme }, headers: { host: 'buzzcompass.buzzmonitor.com' } }, rq);
  assert.strictEqual(rq.statusCode, 400);

  limparEnv();
  console.log('leads-destinos.test.js: ok');
})().catch((e) => { console.error(e); process.exit(1); });

