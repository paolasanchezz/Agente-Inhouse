// Teste da conferencia de relevancia dos posts da marca:  node landing-pages/buzzmonitor/buzz-radar/tests/relevancia.test.js
// A IA e simulada (modulo llm trocado): nada e enviado de verdade.
const assert = require('assert');
const path = require('path');

let resposta = null;
let ultimoPedido = null;
const llmPath = require.resolve(path.join('..', 'api', '_lib', 'llm.js'));
require.cache[llmPath] = { id: llmPath, filename: llmPath, loaded: true, exports: { chamarJSON: async (args) => { ultimoPedido = args; if (resposta instanceof Error) throw resposta; return resposta; } } };
const { conferirRelevancia } = require('../api/_lib/analise.js');

const post = (rede, autor, texto, propria = false) => ({ rede, autor, texto, propria, link: `https://exemplo.com/${autor}`, interacoes: 1 });
const lista = () => [
  post('site', 'DN', 'A Comissão Europeia mantém processo sobre a rede Natura 2000'),
  post('x', 'anaju', 'meu namorado comprou esse perfume da natura pra mim'),
  post('instagram', 'Natura', 'Nova linha Natura Ekos', true),
  post('facebook', 'Feira', 'Frutas in natura direto do produtor'),
];

(async () => {
  // a IA aponta so o post 1: os outros saem, mas o perfil da propria marca (indice 2) fica mesmo sem ser apontado
  resposta = { relevantes: [1] };
  let r = await conferirRelevancia(lista(), 'Natura', 'Cosméticos e Beleza');
  assert.deepStrictEqual(r.map((p) => p.autor), ['anaju', 'Natura']);
  // a IA recebe marca, segmento e os textos numerados
  assert.strictEqual(ultimoPedido.user.marca, 'Natura');
  assert.strictEqual(ultimoPedido.user.segmento, 'Cosméticos e Beleza');
  assert.deepStrictEqual(ultimoPedido.user.posts.map((p) => p.n), [0, 1, 2, 3]);
  assert(/Natura 2000/.test(ultimoPedido.system) && /in natura/.test(ultimoPedido.system), 'o prompt explica os homonimos');

  // IA indisponivel ou resposta estranha: mantem todos (so vale o filtro de palavra inteira)
  for (const falha of [null, {}, { relevantes: 'x' }, new Error('timeout')]) {
    resposta = falha;
    r = await conferirRelevancia(lista(), 'Natura', 'Cosméticos');
    assert.strictEqual(r.length, 4, 'sem conferencia valida, nao corta nada');
  }
  // indices invalidos sao ignorados; lista vazia nem chama a IA
  resposta = { relevantes: [99, -1, 1.5, 0] };
  r = await conferirRelevancia(lista(), 'Natura', null);
  assert.deepStrictEqual(r.map((p) => p.autor), ['DN', 'Natura']);
  ultimoPedido = null;
  assert.deepStrictEqual(await conferirRelevancia([], 'Natura', null), []);
  assert.strictEqual(ultimoPedido, null);

  console.log('relevancia.test.js: ok');
})().catch((e) => { console.error(e); process.exit(1); });
