// Teste do script da planilha (integracoes/google/buzz-compass-leads.gs) com os servicos do Google simulados:
//   node landing-pages/buzzmonitor/buzz-radar/tests/apps-script.test.js
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const codigo = fs.readFileSync(path.join(__dirname, '..', '..', '..', '..', 'integracoes', 'google', 'buzz-compass-leads.gs'), 'utf8');

function criarAmbiente({ token = 'segredo', trava = true } = {}) {
  const linhas = [];
  const propriedades = token === null ? {} : { TOKEN: token };
  const formatos = [];
  const aba = {
    getLastRow: () => linhas.length + 1, // linha 1 e o cabecalho
    getRange: (linha) => ({
      setNumberFormat: (f) => { formatos[linha] = f; },
      setValues: (v) => { linhas[linha - 2] = v[0]; return { setFontWeight() {} }; },
      setFontWeight() {},
    }),
    setFrozenRows() {}, setColumnWidth() {},
  };
  const contexto = {
    console,
    SpreadsheetApp: { openById: () => ({ getSheetByName: () => aba, insertSheet: () => aba }) },
    PropertiesService: { getScriptProperties: () => ({ getProperty: (k) => propriedades[k] || null }) },
    LockService: { getScriptLock: () => ({ waitLock() { if (!trava) throw new Error('timeout'); }, releaseLock() {} }) },
    ContentService: { MimeType: { JSON: 'json' }, createTextOutput: (t) => ({ texto: t, setMimeType() { return this; } }) },
    Utilities: { formatDate: (d, tz, fmt) => `${tz}|${fmt}|${d.toISOString()}` },
  };
  vm.createContext(contexto);
  vm.runInContext(codigo + '\nID_PLANILHA = "planilha-teste";', contexto);
  const post = (obj) => JSON.parse(vm.runInContext('doPost', contexto)({ postData: { contents: typeof obj === 'string' ? obj : JSON.stringify(obj) } }).texto);
  return { linhas, formatos, post, doGet: () => JSON.parse(vm.runInContext('doGet', contexto)().texto) };
}

const lead = { token: 'segredo', origem: 'buzz-compass-totem', criado_em: '2026-10-21T15:30:00.000Z', nome: 'Ana Souza', email: 'ana@empresa.com.br', marca: 'Natura', segmento: 'Cosméticos e Beleza', instagram: 'naturabrasil', concorrentes: ['Boticário', 'Eudora'], link: 'https://buzzcompass.buzzmonitor.com/totem-resultado?m=Natura',
  url_conversao: 'https://buzzcompass.buzzmonitor.com/totem?utm_source=evento&utm_campaign=marketing-day', utm_source: 'evento', utm_medium: '', utm_campaign: 'marketing-day', utm_content: 'captacao-buzz-compass', utm_term: '' };

// grava uma linha com os campos certos, na ordem das colunas
let amb = criarAmbiente();
assert.deepStrictEqual(amb.post(lead), { ok: true });
assert.strictEqual(amb.linhas.length, 1);
const [dataHora, nome, email, marca, segmento, insta, concorrentes, link, origem] = amb.linhas[0];
assert(dataHora.startsWith('America/Sao_Paulo|dd/MM/yyyy HH:mm:ss|2026-10-21T15:30'), 'data em horario de Brasilia: ' + dataHora);
assert.deepStrictEqual([nome, email, marca, segmento, insta, concorrentes, origem], ['Ana Souza', 'ana@empresa.com.br', 'Natura', 'Cosméticos e Beleza', '@naturabrasil', 'Boticário, Eudora', 'buzz-compass-totem']);
assert.strictEqual(link, lead.link);
// colunas de rastreio (URL de conversao + 5 UTMs) logo depois da Origem; as vazias ficam vazias
assert.deepStrictEqual(Array.from(amb.linhas[0]).slice(9), ['https://buzzcompass.buzzmonitor.com/totem?utm_source=evento&utm_campaign=marketing-day', 'evento', '', 'marketing-day', 'captacao-buzz-compass', '']);
assert.strictEqual(amb.linhas[0].length, 15, '9 colunas antigas + 6 de rastreio');

// token errado, ausente ou script sem TOKEN configurado: nao grava nada
amb = criarAmbiente();
assert.deepStrictEqual(amb.post({ ...lead, token: 'errado' }), { ok: false, erro: 'token' });
assert.deepStrictEqual(amb.post({ ...lead, token: undefined }), { ok: false, erro: 'token' });
assert.strictEqual(amb.linhas.length, 0, 'sem token valido nada e gravado');
amb = criarAmbiente({ token: null });
assert.strictEqual(amb.post(lead).ok, false, 'sem TOKEN nas propriedades recusa tudo (nunca fica aberto)');
assert.strictEqual(amb.linhas.length, 0);

// corpo invalido e e-mail ausente nao quebram nem gravam
amb = criarAmbiente();
assert.strictEqual(amb.post('isto nao e json').ok, false);
assert.deepStrictEqual(amb.post({ token: 'segredo', nome: 'x' }), { ok: false, erro: 'sem e-mail' });
assert.strictEqual(amb.linhas.length, 0);

// injecao de formula: a linha e formatada como TEXTO PURO ("@") antes de receber os valores, e os valores ficam exatos
// (sem apostrofo na frente). O @ do Instagram continua aparecendo como @marca.
amb = criarAmbiente();
amb.post({ ...lead, nome: '=IMPORTXML("http://x")', marca: '+55 11 99999', segmento: '-cmd', concorrentes: ['@SUM(A1)'] });
const l = amb.linhas[0];
assert.strictEqual(amb.formatos[2], '@', 'formato texto puro aplicado na linha antes de gravar');
assert.deepStrictEqual([l[1], l[3], l[4], l[6]], ['=IMPORTXML("http://x")', '+55 11 99999', '-cmd', '@SUM(A1)'], 'valores exatos, sem apostrofo');
assert.strictEqual(l[5], '@naturabrasil');
// quebras de linha somem e texto enorme e cortado
amb.post({ ...lead, nome: 'Ana\nSouza\t' + 'x'.repeat(900) });
assert(!/[\r\n\t]/.test(amb.linhas[1][1]) && amb.linhas[1][1].length <= 500);

// sem criado_em ou com data invalida usa agora; sem instagram fica vazio; origem padrao
amb.post({ ...lead, criado_em: 'lixo', instagram: '', origem: undefined });
assert(/^America\/Sao_Paulo\|/.test(amb.linhas[2][0]));
assert.strictEqual(amb.linhas[2][5], '');
assert.strictEqual(amb.linhas[2][8], 'buzz-compass-totem');

// evento cheio: se nao conseguir a trava, avisa em vez de perder em silencio (o backend tenta de novo)
amb = criarAmbiente({ trava: false });
assert.deepStrictEqual(amb.post(lead), { ok: false, erro: 'ocupado' });

// o GET devolve so que esta no ar, nunca a planilha
amb = criarAmbiente();
amb.post(lead);
assert.deepStrictEqual(amb.doGet(), { ok: true, servico: 'buzz-compass-leads' });

console.log('apps-script.test.js: ok');
