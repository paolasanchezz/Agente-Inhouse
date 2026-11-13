// Reserva de IA (api/_lib/llm.js): node landing-pages/buzzmonitor/buzz-compass-latam/tests/llm-reserva.test.js
// Caso real de 2026-11-13: OpenAI da LATAM sem credito (429 credit_balance_exhausted) e o Claude com so 15s para o diagnostico.
const assert = require('assert');

const chamadas = [];
let roteiro = {};
global.fetch = async (url, opts) => {
  const corpo = JSON.parse(opts.body);
  const provedor = url.includes('openai') ? `openai:${corpo.model}` : 'anthropic';
  chamadas.push({ provedor, timeoutAbortavel: Boolean(opts.signal) });
  const r = roteiro[provedor] || roteiro[url.includes('openai') ? 'openai' : 'anthropic'];
  if (r.atraso) await new Promise((ok) => setTimeout(ok, r.atraso));
  if (r.status !== 200) return { ok: false, status: r.status, text: async () => r.texto || '' };
  return { ok: true, status: 200, json: async () => r.json };
};
const silenciar = () => { const e = console.error; const l = console.log; console.error = () => {}; console.log = () => {}; return () => { console.error = e; console.log = l; }; };

(async () => {
  process.env.OPENAI_API_KEY = 'sk-teste';
  process.env.ANTHROPIC_API_KEY = 'sk-ant-teste';
  delete process.env.OPENAI_MODEL; delete process.env.ANTHROPIC_MODEL;
  const { chamarJSON, ERRO_DE_CONTA_OPENAI } = require('../api/_lib/llm.js');
  const semCredito = '{"error":{"type":"insufficient_quota","code":"credit_balance_exhausted"}}';
  const okClaude = { content: [{ type: 'tool_use', input: { titulo: 'ok' } }] };

  // 1) OpenAI sem credito: pula o segundo modelo OpenAI (mesma chave) e o Claude recebe o prazo cheio (nao 15s)
  roteiro = { openai: { status: 429, texto: semCredito }, anthropic: { status: 200, json: okClaude } };
  chamadas.length = 0;
  let restaura = silenciar();
  let r = await chamarJSON({ system: 's', user: {}, schema: {}, schemaName: 'buzz_compass_totem', timeoutMs: 32000, modeloOpenAI: 'gpt-4o' });
  restaura();
  assert.deepStrictEqual(chamadas.map((c) => c.provedor), ['openai:gpt-4o', 'anthropic'], 'nao tenta o gpt-4o-mini com a mesma chave sem credito');
  assert.strictEqual(r.titulo, 'ok');
  assert.strictEqual(r._modelo, 'anthropic:claude-sonnet-5');

  // 2) prazo do Claude: com falha rapida antes, recebe os 32s inteiros (medido pelo timeout passado ao fetchWithTimeout)
  const trends = require('../api/_lib/trends.js');
  const prazos = [];
  const fwt = trends.fetchWithTimeout;
  trends.fetchWithTimeout = (url, o, ms) => { prazos.push([url.includes('openai') ? 'openai' : 'anthropic', ms]); return fwt(url, o, ms); };
  delete require.cache[require.resolve('../api/_lib/llm.js')];
  const llm2 = require('../api/_lib/llm.js');
  restaura = silenciar();
  await llm2.chamarJSON({ system: 's', user: {}, schema: {}, schemaName: 'buzz_compass_totem', timeoutMs: 32000, modeloOpenAI: 'gpt-4o' });
  restaura();
  assert.deepStrictEqual(prazos, [['openai', 32000], ['anthropic', 32000]], 'reserva com prazo cheio depois de falha rapida');

  // 3) falha lenta antes (timeout de verdade): a reserva continua com no maximo 15s
  prazos.length = 0;
  roteiro = { openai: { status: 500, texto: 'lento', atraso: 5200 }, anthropic: { status: 200, json: okClaude } };
  restaura = silenciar();
  await llm2.chamarJSON({ system: 's', user: {}, schema: {}, schemaName: 'x', timeoutMs: 32000 });
  restaura();
  assert.deepStrictEqual(prazos, [['openai', 32000], ['anthropic', 15000]], 'depois de gastar tempo, reserva com 15s');
  trends.fetchWithTimeout = fwt;

  // 4) erro passageiro do OpenAI (429 de limite por minuto, 500) NAO pula o modelo padrao
  assert(!ERRO_DE_CONTA_OPENAI.test('openai_429: {"error":{"type":"requests","code":"rate_limit_exceeded"}}'));
  assert(!ERRO_DE_CONTA_OPENAI.test('openai_500: erro'));
  assert(ERRO_DE_CONTA_OPENAI.test('openai_401: invalid api key'));
  assert(ERRO_DE_CONTA_OPENAI.test('openai_429: ' + semCredito));

  // 5) tudo funcionando: so o primeiro modelo e chamado
  roteiro = { openai: { status: 200, json: { choices: [{ message: { content: '{"titulo":"gpt"}' } }] } }, anthropic: { status: 200, json: okClaude } };
  chamadas.length = 0;
  r = await llm2.chamarJSON({ system: 's', user: {}, schema: {}, schemaName: 'x', modeloOpenAI: 'gpt-4o' });
  assert.deepStrictEqual(chamadas.map((c) => c.provedor), ['openai:gpt-4o']);
  assert.strictEqual(r._modelo, 'openai:gpt-4o');
  console.log('llm-reserva.test.js: ok');
})().catch((e) => { console.error(e); process.exit(1); });
