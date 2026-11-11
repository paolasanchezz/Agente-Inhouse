// Testes do pais (selector "País" do totem):  node landing-pages/buzzmonitor/buzz-compass-latam/tests/pais.test.js
// Nada e consultado de verdade: a analise e o fetch sao simulados.
const assert = require('assert');
const path = require('path');
const { limparPais, dadosDoPais, fusoHoras, PAISES } = require('../api/_lib/paises');
const { comFuso, fusoAtual } = require('../api/_lib/trends');

(async () => {
  // 1) so os 5 paises do totem
  assert.deepStrictEqual(Object.keys(PAISES), ['MX', 'CO', 'CL', 'AR', 'PE']);
  assert.strictEqual(limparPais(' mx '), 'MX');
  assert.strictEqual(limparPais('BR'), '');
  assert.strictEqual(limparPais('Mexico'), '');
  assert.strictEqual(limparPais(undefined), '');
  assert.strictEqual(dadosDoPais('pe').nome, 'Perú');
  assert.strictEqual(dadosDoPais('xx'), null);

  // 2) fuso por pais (Chile muda com o horario de verao)
  assert.strictEqual(fusoHoras('MX'), -6);
  assert.strictEqual(fusoHoras('CO'), -5);
  assert.strictEqual(fusoHoras('PE'), -5);
  assert.strictEqual(fusoHoras('AR'), -3);
  assert.strictEqual(fusoHoras('CL', new Date('2026-01-15T12:00:00Z')), -3);
  assert.strictEqual(fusoHoras('CL', new Date('2026-07-15T12:00:00Z')), -4);
  assert.strictEqual(fusoHoras(''), -6, 'sem pais: Cidade do Mexico, como antes');

  // 3) o fuso fica isolado por analise, mesmo com duas rodando juntas
  assert.strictEqual(fusoAtual(), -6);
  const [a, b] = await Promise.all([
    comFuso(-3, async () => { await new Promise((r) => setTimeout(r, 20)); return fusoAtual(); }),
    comFuso(-5, async () => { await new Promise((r) => setTimeout(r, 5)); return fusoAtual(); }),
  ]);
  assert.deepStrictEqual([a, b], [-3, -5]);

  // 4) a chamada da Trends leva o fuso do pais; a busca de perfis leva o codigo do pais
  const pedidos = [];
  const fetchOriginal = global.fetch;
  global.fetch = async (url, opts) => {
    pedidos.push({ url: String(url), body: opts && opts.body ? JSON.parse(opts.body) : null });
    return { ok: true, status: 200, json: async () => ({ data: [] }) };
  };
  const { bmVolume, bmInfluencers } = require('../api/_lib/trends');
  await comFuso(fusoHoras('CO'), () => bmVolume('"x"', 'sentiment', '20261001000000', '20261031000000'));
  assert.strictEqual(pedidos[0].body.general_params.timezone, '-5.0');
  await bmVolume('"x"', 'sentiment', '20261001000000', '20261031000000');
  assert.strictEqual(pedidos[1].body.general_params.timezone, '-6.0', 'fora de uma analise: -6');
  await bmInfluencers('cerveza', '["es"]', '["AR"]');
  assert.strictEqual(new URL(pedidos[2].url).searchParams.get('countries'), '["AR"]');
  await bmInfluencers('cerveza', '["es"]');
  assert.strictEqual(new URL(pedidos[3].url).searchParams.get('countries'), '[]');
  global.fetch = fetchOriginal;

  // 5) API: p entra na URL limpa (ordem m, s, p, i, c), valor invalido e redirecionado para fora, e chega na analise
  let chamadas = [];
  const analisePath = require.resolve(path.join('..', 'api', '_lib', 'analise.js'));
  require.cache[analisePath] = { id: analisePath, filename: analisePath, loaded: true, exports: { analisar: async (args) => { chamadas.push(args); return { ok: true }; } } };
  const handler = require('../api/totem.js');
  const chamar = (url) => {
    const u = new URL('https://x' + url);
    const query = {};
    for (const [k, v] of u.searchParams) { if (k in query) query[k] = [].concat(query[k], v); else query[k] = v; }
    return new Promise((resolve) => {
      const res = {
        statusCode: 200, headers: {},
        setHeader(k, v) { this.headers[k] = v; },
        json(obj) { resolve({ status: this.statusCode, headers: this.headers, body: obj }); return this; },
        end() { resolve({ status: this.statusCode, headers: this.headers, body: null }); return this; },
      };
      handler({ method: 'GET', url, query, headers: { host: 'buzzcompass.buzzmonitor.com' } }, res);
    });
  };
  let r = await chamar('/api/totem?m=Oxxo&s=Tiendas&p=CO&c=D1');
  assert.strictEqual(r.status, 200);
  assert.strictEqual(chamadas[0].pais, 'CO');
  r = await chamar('/api/totem?m=Oxxo&s=Tiendas&p=co&c=D1');
  assert.strictEqual(r.status, 308);
  assert.strictEqual(r.headers.Location, '/es/api/totem?m=Oxxo&s=Tiendas&p=CO&c=D1');
  r = await chamar('/api/totem?m=Oxxo&s=Tiendas&p=BR');
  assert.strictEqual(r.status, 308);
  assert.strictEqual(r.headers.Location, '/es/api/totem?m=Oxxo&s=Tiendas', 'pais fora da lista sai da URL');
  chamadas = [];
  r = await chamar('/api/totem?m=Oxxo&s=Tiendas');
  assert.strictEqual(r.status, 200, 'link antigo sem pais continua valendo');
  assert.strictEqual(chamadas[0].pais, '');

  // 6) o front monta a mesma URL que o servidor considera limpa
  global.window = {};
  require('../assets/totem-render.js');
  const TR = global.window.TotemRender;
  assert.strictEqual(TR.apiUrl('Oxxo', ['D1'], 'Tiendas', 'oxxo', 'CO'), '/es/api/totem?m=Oxxo&s=Tiendas&p=CO&i=oxxo&c=D1');
  assert.strictEqual(TR.limparPais('ar'), 'AR');
  assert.strictEqual(TR.limparPais('BR'), '');
  chamadas = [];
  r = await chamar(TR.apiUrl('Oxxo', ['D1'], 'Tiendas', 'oxxo', 'CO').replace('/es', ''));
  assert.strictEqual(r.status, 200, 'URL do front nao redireciona');

  console.log('pais.test.js: ok');
})().catch((err) => { console.error(err); process.exit(1); });
