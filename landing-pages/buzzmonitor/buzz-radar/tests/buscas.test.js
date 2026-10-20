// Testes do sanitizador de buscas:  node landing-pages/buzzmonitor/buzz-radar/tests/buscas.test.js
const assert = require('assert');
const { sanitizarQuery, queryExata, categoriaPeloSegmento, removerAutoExclusoes, soAncoras, comPerfil } = require('../api/_lib/buscas.js');
const { limparPerfil } = require('../api/_lib/perfil.js');

// @ do Instagram: limpeza do que o visitante digita
assert.strictEqual(limparPerfil('@NaturaBrasil'), 'naturabrasil');
assert.strictEqual(limparPerfil('  natura.brasil  '), 'natura.brasil');
assert.strictEqual(limparPerfil('https://www.instagram.com/oboticario/?hl=pt'), 'oboticario');
assert.strictEqual(limparPerfil('instagram.com/vivo'), 'vivo');
assert.strictEqual(limparPerfil('@@ana_silva'), 'ana_silva');
assert.strictEqual(limparPerfil('@'), '');
assert.strictEqual(limparPerfil('a'), '');
assert.strictEqual(limparPerfil(''), '');
assert.strictEqual(limparPerfil(null), '');
assert.strictEqual(limparPerfil('<script>alert(1)</script>'), 'scriptalert1', 'sem < > ( ); o resto depois da barra e descartado como caminho de URL');
assert.strictEqual(limparPerfil('a'.repeat(50)).length, 30);

// @ entra na busca da marca como alternativa (OR), as exclusoes ficam no fim, e nao duplica
assert.strictEqual(comPerfil('"Natura" OR #natura', 'naturabrasil'), '"Natura" OR #natura OR @naturabrasil');
assert.strictEqual(comPerfil('"vivo fibra" OR #vivo -"vivo bem" -jogo', 'vivo'), '"vivo fibra" OR #vivo OR @vivo -"vivo bem" -jogo');
assert.strictEqual(comPerfil('"Natura" OR @naturabrasil', 'naturabrasil'), '"Natura" OR @naturabrasil', 'ja tem: nao muda');
assert.strictEqual(comPerfil('"Natura" OR @naturabrasil.oficial', 'naturabrasil'), '"Natura" OR @naturabrasil.oficial OR @naturabrasil', 'prefixo de outro @ nao conta como o mesmo');
assert.strictEqual(comPerfil('"Natura"', ''), '"Natura"', 'sem @: busca intacta');
assert.strictEqual(comPerfil('-jogo', 'x1'), '@x1 -jogo', 'so exclusoes: o @ vira o termo positivo');
assert.strictEqual(sanitizarQuery(comPerfil('"Natura" OR #natura', 'naturabrasil')), '"Natura" OR #natura OR @naturabrasil', 'o sanitizador aceita a busca montada');

const casos = [
  ['ipanema AND chinelo', 'ipanema chinelo'],
  ['sprite NOT jogo', 'sprite -jogo'],
  ['sprite NOT (jogo OR espirito)', 'sprite -(jogo OR espirito)'],
  ['sprite NOT "sprite de jogo"', 'sprite -"sprite de jogo"'],
  ['melissa -"melissa and doug"', 'melissa -"melissa and doug"'], // AND dentro de aspas nao pode mudar
  ['"rock and roll" OR #rock', '"rock and roll" OR #rock'],
  ['a & b && c', 'a b c'],
  ['"havaianas OR havaiana', 'havaianas OR havaiana'], // aspa sobrando: remove todas
  ['(a OR b', 'a OR b'], // parentese aberto: remove
  ['"havaianas" OR havaiana OR #havaianas OR @havaianas', '"havaianas" OR havaiana OR #havaianas OR @havaianas'],
  ['  muito   espaco  ', 'muito espaco'],
  // alternativas coladas so por espaco (erro real visto em producao): viram OR
  ['"Havaianas" "Havaiana" "havaianas" "havaiana" #havaianas @havaianas', '"Havaianas" OR "Havaiana" OR "havaianas" OR "havaiana" OR #havaianas OR @havaianas'],
  ['("Ipanema" "ipanema" #ipanema @ipanema)', '("Ipanema" OR "ipanema" OR #ipanema OR @ipanema)'],
  ['"vivo fibra" #vivo -"vivo bem"', '"vivo fibra" OR #vivo -"vivo bem"'],
  ['melissa -"melissa mccarthy" -"melissa doug"', 'melissa -"melissa mccarthy" -"melissa doug"'], // exclusoes nao viram OR
  ['-"jogo" "sprite"', '-"jogo" "sprite"'], // positivo depois de exclusao nao vira OR
  ['vivo operadora', 'vivo operadora'], // palavras soltas seguem sendo E (co-ocorrencia de proposito)
  ['"a" OR "b" "c"', '"a" OR "b" OR "c"'],
];
casos.forEach(([entrada, esperado]) => assert.strictEqual(sanitizarQuery(entrada), esperado, `sanitizar(${entrada})`));
assert.strictEqual(sanitizarQuery('x'.repeat(500)).length, 380);
assert.strictEqual(sanitizarQuery(''), '');
assert.strictEqual(queryExata('Ypê "Casa"'), '"Ypê Casa"');
assert.strictEqual(queryExata('   '), '');
assert.deepStrictEqual(categoriaPeloSegmento('Cosméticos e Beleza'), { nome: 'Cosméticos e Beleza', query: 'Cosméticos OR Beleza' });
assert.strictEqual(categoriaPeloSegmento('Telecom').query, 'Telecom');
assert.strictEqual(categoriaPeloSegmento('ab'), null);
assert.strictEqual(categoriaPeloSegmento(''), null);
// exclusao que contradiz a propria busca e descartada; exclusao legitima fica
assert.strictEqual(removerAutoExclusoes('"Vivo" OR vivo OR #vivo OR @vivobr -"ao vivo" -"vivo" -"está vivo"'), '"Vivo" OR vivo OR #vivo OR @vivobr -"ao vivo" -"está vivo"');
assert.strictEqual(removerAutoExclusoes('"vivo fibra" -vivo'), '"vivo fibra"', 'excluir uma palavra que a propria frase positiva contem anula a busca');
assert.strictEqual(removerAutoExclusoes('"Renner" OR #renner -"Rick & Renner" -rick'), '"Renner" OR #renner -"Rick & Renner" -rick');
assert.strictEqual(removerAutoExclusoes('melissa -"melissa mccarthy"'), 'melissa -"melissa mccarthy"');
assert.strictEqual(removerAutoExclusoes('-"jogo" sprite'), '-"jogo" sprite');
assert.strictEqual(removerAutoExclusoes('"Claro" OR #claro -Claro'), '"Claro" OR #claro');
// modo ancora: descarta o nome solto, fica com @perfil, #hashtag e frases compostas, mantem exclusoes
assert.strictEqual(soAncoras('"Vivo" OR vivo OR #vivo OR @vivobr -"ao vivo"'), '#vivo OR @vivobr -"ao vivo"');
assert.strictEqual(soAncoras('"Renner" OR "lojas Renner" OR @lojasrenner'), '"lojas Renner" OR @lojasrenner');
assert.strictEqual(soAncoras('"Oi" OR oi'), null, 'sem ancora nao ha o que manter');
assert.strictEqual(soAncoras('"vivo fibra" OR "vivo fibra"'), '"vivo fibra"', 'sem repeticao');
console.log(`buscas.test.js: ${casos.length + 18} verificacoes ok`);
