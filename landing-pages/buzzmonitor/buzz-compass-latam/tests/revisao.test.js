// Testes da checagem de homonimo (revisarBusca):  node landing-pages/buzzmonitor/buzz-compass-latam/tests/revisao.test.js
// A IA e simulada (llm.js trocado): o que se testa e a regra que decide quando corrigir.
const assert = require('assert');
const path = require('path');

let resposta = null; let chamadas = 0;
const llmPath = require.resolve(path.join(__dirname, '../api/_lib/llm.js'));
require.cache[llmPath] = { id: llmPath, filename: llmPath, loaded: true, exports: { chamarJSON: async () => { chamadas++; return resposta; } } };
const { revisarBusca } = require('../api/_lib/buscas.js');

const posts = (n) => Array.from({ length: n }, (_, i) => ({ texto: `post ${i}`, autor: 'perfil' }));
const base = { nome: 'Renner', segmento: 'Moda', query: '"Renner" OR #renner' };

(async () => {
  // amostra pequena demais: nem chama a IA
  assert.strictEqual(await revisarBusca({ ...base, posts: posts(5) }), null);
  assert.strictEqual(chamadas, 0, 'amostra pequena nao gasta chamada de IA');

  // sem IA disponivel (chamarJSON devolve null): segue sem correcao
  resposta = null;
  assert.strictEqual(await revisarBusca({ ...base, posts: posts(20) }), null);

  // busca boa (poucos posts fora do assunto): nao corrige, mesmo que a IA mande uma query
  resposta = { posts_fora_do_assunto: 3, assunto_errado: '', query_corrigida: '"Renner" -rick' };
  let r = await revisarBusca({ ...base, posts: posts(20) });
  assert.strictEqual(r.corrigida, null, 'menos de 30% fora: nao mexe na busca');
  assert.strictEqual(r.fora, 3);

  // homonimo (14 de 20 fora): corrige e passa pelo sanitizador (AND vira espaco, NOT vira hifen)
  resposta = { posts_fora_do_assunto: 14, assunto_errado: 'dupla sertaneja', query_corrigida: '"Renner" OR #renner NOT rick AND loja' };
  r = await revisarBusca({ ...base, posts: posts(20) });
  assert.strictEqual(r.fora, 14);
  assert.strictEqual(r.assunto, 'dupla sertaneja');
  assert.strictEqual(r.corrigida, '"Renner" OR #renner -rick loja', 'query corrigida sanitizada');

  // IA diz que tem problema mas devolve a mesma busca ou vazio: nada a aplicar
  resposta = { posts_fora_do_assunto: 15, assunto_errado: 'x', query_corrigida: '' };
  assert.strictEqual((await revisarBusca({ ...base, posts: posts(20) })).corrigida, null);
  resposta = { posts_fora_do_assunto: 15, assunto_errado: 'x', query_corrigida: '"Renner" OR #renner' };
  assert.strictEqual((await revisarBusca({ ...base, posts: posts(20) })).corrigida, null, 'mesma busca nao e correcao');

  // a IA se contradiz (exclui o proprio nome): a exclusao e removida e o resto da correcao vale
  resposta = { posts_fora_do_assunto: 17, assunto_errado: 'eventos', query_corrigida: '"Vivo" OR vivo OR #vivo -"ao vivo" -vivo' };
  r = await revisarBusca({ ...base, nome: 'Vivo', query: '"Vivo" OR vivo OR #vivo', posts: posts(20) });
  assert.strictEqual(r.corrigida, '"Vivo" OR vivo OR #vivo -"ao vivo"', 'auto-exclusao descartada');
  assert.strictEqual(r.problema, true);

  // contagem absurda da IA e limitada ao tamanho da amostra
  resposta = { posts_fora_do_assunto: 999, assunto_errado: '', query_corrigida: '"Renner" -rick' };
  r = await revisarBusca({ ...base, posts: posts(20) });
  assert.strictEqual(r.fora, 20);

  console.log('revisao.test.js: ok');
})().catch((e) => { console.error(e); process.exit(1); });
