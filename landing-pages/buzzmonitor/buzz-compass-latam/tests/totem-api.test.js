// Testes da API de analise (URL limpa, redirecionamento e debug):  node landing-pages/buzzmonitor/buzz-compass-latam/tests/totem-api.test.js
// A analise e simulada (modulo analise trocado): nada e consultado de verdade.
//
// Regressao importante: em 2026-10-20 uma versao comparava o TEXTO da URL e entrou em laco de redirecionamento em producao
// (a Vercel entrega req.url com %20 no lugar de +). A regra agora so olha valores decodificados, e este teste exercita:
// codificacao diferente, entradas esquisitas e a PROPRIEDADE "seguir o redirecionamento nunca redireciona de novo".
const assert = require('assert');
const path = require('path');

let chamadas = [];
const analisePath = require.resolve(path.join('..', 'api', '_lib', 'analise.js'));
require.cache[analisePath] = { id: analisePath, filename: analisePath, loaded: true, exports: { analisar: async (args) => { chamadas.push(args); return { ok: true, marca: { nome: args.marca } }; } } };
const handler = require('../api/totem.js');

// Monta o pedido como a Vercel: query decodificada em req.query, req.url com a codificacao que ela quiser (aqui %20).
function chamar(url, { host = 'buzzcompass.buzzmonitor.com', method = 'GET', urlDoServidor } = {}) {
  const u = new URL('https://x' + url);
  const query = {};
  for (const [k, v] of u.searchParams) { if (k in query) query[k] = [].concat(query[k], v); else query[k] = v; }
  const reqUrl = urlDoServidor !== undefined ? urlDoServidor : url.replace(/\+/g, '%20');
  return new Promise((resolve) => {
    const res = {
      statusCode: 200, headers: {},
      setHeader(k, v) { this.headers[k] = v; },
      json(obj) { resolve({ status: this.statusCode, headers: this.headers, body: obj }); return this; },
      end() { resolve({ status: this.statusCode, headers: this.headers, body: null }); return this; },
    };
    handler({ method, url: reqUrl, query, headers: { host } }, res);
  });
}

(async () => {
  const limpa = '/api/totem?m=Natura&s=Cosm%C3%A9ticos+e+Beleza&i=naturabrasil&c=Botic%C3%A1rio&c=Eudora';

  // 1) pedido limpo roda a analise e fica no cache da borda, qualquer que seja a codificacao que o servidor mostre em req.url
  for (const urlDoServidor of [undefined, limpa, limpa.replace(/\+/g, '%20'), '/api/totem', '']) {
    chamadas = [];
    const r = await chamar(limpa, { urlDoServidor });
    assert.strictEqual(r.status, 200, 'sem redirecionamento, req.url=' + urlDoServidor);
    assert.strictEqual(chamadas.length, 1);
    assert.deepStrictEqual([chamadas[0].marca, chamadas[0].segmento, chamadas[0].instagram, chamadas[0].informados], ['Natura', 'Cosméticos e Beleza', 'naturabrasil', ['Boticário', 'Eudora']]);
    assert.strictEqual(r.headers['Cache-Control'], 'public, max-age=0, s-maxage=86400');
  }
  // a ordem dos parametros nao muda nada (so existem poucas ordens possiveis; nao e um caminho para furar o cache)
  chamadas = [];
  assert.strictEqual((await chamar('/api/totem?c=Botic%C3%A1rio&c=Eudora&i=naturabrasil&s=Cosm%C3%A9ticos+e+Beleza&m=Natura')).status, 200);

  // 2) variacoes "sujas" viram redirecionamento para a forma limpa, SEM rodar a analise
  chamadas = [];
  const sujas = [
    ['parametro a mais', limpa + '&x=123'],
    ['parametro antes', limpa.replace('?', '?x=1&')],
    ['perfil com @ e maiuscula', limpa.replace('i=naturabrasil', 'i=@NaturaBrasil')],
    ['perfil com muitos @', limpa.replace('i=naturabrasil', 'i=@@@@naturabrasil')],
    ['espaco duplo na marca', limpa.replace('m=Natura', 'm=Natura++')],
    ['concorrente vazio', limpa.replace('&c=Eudora', '&c=&c=Eudora')],
    ['quarto concorrente', limpa + '&c=Avon&c=Rider'],
    ['concorrente repetido', limpa + '&c=Eudora'],
    ['debug em producao', limpa + '&debug=1'],
  ];
  for (const [rotulo, url] of sujas) {
    const r = await chamar(url);
    assert.strictEqual(r.status, 308, 'redireciona: ' + rotulo);
    assert(r.headers.Location.startsWith('/api/totem?m=Natura'), rotulo + ' -> ' + r.headers.Location);
    assert(!/[?&](x|debug)=/.test(r.headers.Location), rotulo + ' perdeu o parametro extra: ' + r.headers.Location);
  }
  assert.strictEqual(chamadas.length, 0, 'redirecionamento nao roda analise');

  // 3) PROPRIEDADE anti-laco: seguir o Location SEMPRE termina em 200 na primeira volta, para qualquer entrada
  const esquisitas = [
    'Natura', '  Natura  ', 'Na  tu   ra', 'O Boticário', "L'Oréal", 'Marca & Cia', 'Ação "Total" 100%', '<script>alert(1)</script>', 'a'.repeat(200), 'ab',
    'x'.repeat(79) + ' y', 'x'.repeat(59) + ' y', '日本語ブランド', 'Café   com   Leite', 'a+b', 'a%b', 'a/b?c=d&e', '\t\ttab\n', '😀 Marca',
  ];
  let testadas = 0;
  for (const m of esquisitas) {
    for (const s of ['', 'Moda e Vestuário', '  Moda   ', 'y'.repeat(80), 'z'.repeat(59) + ' w']) {
      for (const i of ['', '@Natura.Brasil', '@@@x', 'https://www.instagram.com/Natura/?hl=pt', '<b>']) {
        const q = new URLSearchParams();
        q.set('m', m);
        if (s) q.set('s', s);
        if (i) q.set('i', i);
        ['  Eudora ', 'Eudora', 'Avon', 'Rider', 'c'.repeat(70)].forEach((c) => q.append('c', c));
        chamadas = [];
        let r = await chamar('/api/totem?' + q.toString());
        if (r.status === 400) continue; // marca curta demais: nao ha o que redirecionar
        if (r.status === 308) {
          r = await chamar(r.headers.Location);
          assert.strictEqual(r.status, 200, 'LACO: seguir o redirecionamento nao terminou em 200 para m=' + JSON.stringify(m) + ' s=' + JSON.stringify(s) + ' i=' + JSON.stringify(i));
        } else {
          assert.strictEqual(r.status, 200);
        }
        testadas++;
      }
    }
  }
  assert(testadas > 300, 'combinacoes testadas: ' + testadas);

  // 4) debug: so em desenvolvimento local (ou com TOTEM_DEBUG=1)
  chamadas = [];
  let r = await chamar(limpa + '&debug=1', { host: 'localhost:8938' });
  assert.strictEqual(r.status, 200, 'no local o debug vale');
  assert.strictEqual(chamadas[0].debug, true);
  r = await chamar(limpa, { host: 'localhost:8938' });
  assert.strictEqual(chamadas[1].debug, false);
  process.env.TOTEM_DEBUG = '1';
  r = await chamar(limpa + '&debug=1');
  assert.strictEqual(r.status, 200, 'TOTEM_DEBUG=1 libera em producao');
  delete process.env.TOTEM_DEBUG;
  chamadas = [];
  r = await chamar(limpa + '&debug=1');
  assert.strictEqual(r.status, 308);
  assert.strictEqual(chamadas.length, 0);

  // 5) entradas invalidas e metodo
  chamadas = [];
  assert.strictEqual((await chamar('/api/totem')).status, 400, 'sem marca');
  assert.strictEqual((await chamar('/api/totem?m=a')).status, 400, 'marca curta demais');
  assert.strictEqual((await chamar('/api/totem?m=Natura', { method: 'POST' })).status, 405);
  assert.strictEqual((await chamar('/api/totem?m=Natura')).status, 200, 'pedido minimo ja e limpo');
  assert.strictEqual(chamadas.length, 1);

  console.log('totem-api.test.js: ok (' + testadas + ' combinacoes anti-laco)');
})().catch((e) => { console.error(e); process.exit(1); });
