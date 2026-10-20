// Testes do Compass Score da marca:  node landing-pages/buzzmonitor/buzz-radar/tests/score.test.js
const assert = require('assert');
const { scoreDaMarca, ritmoScore, crescimentoPct, volumeScore } = require('../api/_lib/score.js');

const plano = (v) => Array(30).fill(v);
const serie = (antes, depois) => [...Array(16).fill(antes), ...Array(7).fill(antes), ...Array(7).fill(depois)].slice(-30);
const mercado = { positivos: 8000, negativos: 2000, serie: plano(100) }; // 80% positivo, ritmo estavel
const grupo = (volume, pctPos, serieGrupo, queixa = 1) => {
  const pol = Math.round(volume * 0.9);
  return { positivos: Math.round(pol * pctPos), negativos: pol - Math.round(pol * pctPos), total: volume, reclamacao_pct: queixa, serie: serieGrupo };
};

// ---- formulas basicas (as mesmas da LP original) ----
assert.strictEqual(volumeScore(0), 15);
assert.strictEqual(volumeScore(30000), 97);
assert.strictEqual(ritmoScore(plano(10)), 50, 'estavel = 50');
assert.strictEqual(ritmoScore(serie(10, 20)), 100, 'dobrou = teto');
assert.strictEqual(ritmoScore(serie(10, 0)), 0, 'zerou = piso');
assert.strictEqual(crescimentoPct(serie(10, 15)), 50);

// ---- marca forte e bem avaliada, na frente dos concorrentes ----
let r = scoreDaMarca({
  marca: grupo(30000, 0.97, serie(100, 130), 1),
  concorrentes: [grupo(15000, 0.9, serie(100, 100), 2), grupo(5000, 0.88, serie(100, 90), 3)],
  mercado,
});
['presenca', 'reputacao', 'ritmo', 'vantagem', 'compass_score'].forEach((k) => assert(r[k] >= 0 && r[k] <= 100, `${k} dentro de 0 a 100`));
assert(r.presenca > 70, 'lidera a conversa: presenca alta');
assert(r.vantagem > 55, 'melhor que a media dos concorrentes: vantagem acima de 50');
assert.deepStrictEqual([r.estimado.reputacao, r.estimado.ritmo], [false, false], 'muita conversa: nada estimado');

// ---- marca pequena: o score SEMPRE existe, e reputacao e ritmo viram estimativa puxada para o segmento ----
r = scoreDaMarca({
  marca: grupo(30, 1, serie(1, 3), 0), // 27 posts com polaridade, 100% positivos, mas 30 mencoes
  concorrentes: [grupo(15000, 0.9, serie(100, 100), 2)],
  mercado,
});
assert(Number.isFinite(r.compass_score), 'score numerico, nunca "sem dados"');
assert(r.reputacao < 100 && r.reputacao > 80, 'reputacao puxada para os 80% do segmento, nao fica nos 100% de 27 posts: ' + r.reputacao);
assert.strictEqual(r.estimado.reputacao, true);
assert.strictEqual(r.estimado.ritmo, true);
assert(r.presenca < 30, 'presenca baixa de verdade: ser pouco falada e o resultado');

// ---- marca sem nenhuma mencao: ainda assim 4 numeros ----
r = scoreDaMarca({
  marca: { positivos: 0, negativos: 0, total: 0, reclamacao_pct: null, serie: plano(0) },
  concorrentes: [grupo(15000, 0.9, serie(100, 100), 2)],
  mercado,
});
['presenca', 'reputacao', 'ritmo', 'vantagem', 'compass_score'].forEach((k) => assert(Number.isFinite(r[k]), `${k} existe com zero mencoes`));
assert.strictEqual(r.reputacao, 80, 'sem posts: reputacao e a do segmento');
assert.strictEqual(r.ritmo, 50, 'sem posts: ritmo estavel do segmento');
assert(r.presenca <= 10, 'zero mencoes: presenca no piso');
assert.strictEqual(r.estimado.reputacao, true);

// ---- sem concorrentes: vantagem neutra e presenca so pelo volume ----
r = scoreDaMarca({ marca: grupo(5000, 0.9, plano(100)), concorrentes: [], mercado });
assert.strictEqual(r.vantagem, 50);
assert.strictEqual(r.presenca, volumeScore(5000));

// ---- queixa pesa so com volume que a sustente ----
const semQueixa = scoreDaMarca({ marca: grupo(5000, 0.9, plano(100), 0.5), concorrentes: [], mercado });
const comQueixa = scoreDaMarca({ marca: grupo(5000, 0.9, plano(100), 8), concorrentes: [], mercado });
assert(comQueixa.reputacao < semQueixa.reputacao, 'mais queixa, menos reputacao');
const pouco1 = scoreDaMarca({ marca: grupo(100, 0.9, plano(3), 0.5), concorrentes: [], mercado });
const pouco2 = scoreDaMarca({ marca: grupo(100, 0.9, plano(3), 9), concorrentes: [], mercado });
assert.strictEqual(pouco1.reputacao, pouco2.reputacao, 'com menos de 200 mencoes o percentual de queixa e ruido e nao entra');

// ---- sem teto: marca pequena ou sem mencoes recebe o score calculado, sem corte ----
const zero = scoreDaMarca({ marca: grupo(0, 1, plano(0), 0), concorrentes: [], mercado });
assert.strictEqual(zero.compass_score, 50, 'zero mencoes: reputacao e ritmo do segmento, vantagem neutra, presenca no piso');
assert.strictEqual(zero.limitado, undefined, 'nao existe mais o campo limitado');
assert.strictEqual(zero.score_sem_teto, undefined);

console.log('score.test.js: ok');
