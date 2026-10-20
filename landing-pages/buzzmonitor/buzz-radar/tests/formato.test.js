// Testes do formato brasileiro de numeros no texto da IA:  node landing-pages/buzzmonitor/buzz-radar/tests/formato.test.js
const assert = require('assert');
const { formatarNumerosPtBr: f, formatarTextosPtBr } = require('../api/_lib/analise.js');

const casos = [
  // milhar sem separador ganha ponto
  ['com 40459 menções positivas no segmento', 'com 40.459 menções positivas no segmento'],
  ['são 2391 menções', 'são 2.391 menções'],
  ['1234567 posts', '1.234.567 posts'],
  ['5083 curtidas e 12000 seguidores', '5.083 curtidas e 12.000 seguidores'],
  // milhar que ja esta certo nao muda
  ['11.179 menções e 30.249 posts', '11.179 menções e 30.249 posts'],
  ['1.234.567 perfis', '1.234.567 perfis'],
  // decimal com ponto vira virgula
  ['2.4% das menções', '2,4% das menções'],
  ['0.7% usando linguagem de reclamação', '0,7% usando linguagem de reclamação'],
  ['14.35% de queixas', '14,35% de queixas'],
  ['crescimento de 1.5 mil', 'crescimento de 1,5 mil'],
  // decimal e milhar juntos
  ['11.179 menções (2.4%)', '11.179 menções (2,4%)'],
  // ja no formato brasileiro, nao muda
  ['2,4% e 0,7%', '2,4% e 0,7%'],
  ['97% positivas', '97% positivas'],
  ['crescimento de 12% na última semana', 'crescimento de 12% na última semana'],
  // anos e nomes com numero nao mudam
  ['em 2026 a marca cresceu', 'em 2026 a marca cresceu'],
  ['a rede Natura 2000 da União Europeia', 'a rede Natura 2000 da União Europeia'],
  ['coleção 2025 e 1999', 'coleção 2025 e 1999'],
  // ano so e ano quando nao vem contagem logo depois
  ['2024 menções no período', '2.024 menções no período'],
  // numeros pequenos e vazios
  ['top 3 temas, 20 perfis, 999 posts', 'top 3 temas, 20 perfis, 999 posts'],
  ['sem numero nenhum', 'sem numero nenhum'],
  ['', ''],
];
casos.forEach(([entrada, esperado]) => assert.strictEqual(f(entrada), esperado, `"${entrada}" -> "${f(entrada)}"`));

// idempotente: passar duas vezes nao estraga
casos.forEach(([, esperado]) => assert.strictEqual(f(f(esperado)), esperado, 'idempotente: ' + esperado));

// nao-texto passa direto
assert.strictEqual(f(null), null);
assert.strictEqual(f(12345), 12345);

// o objeto inteiro da narrativa (cards com titulo, segmento e marca)
const narrativa = formatarTextosPtBr({
  oportunidade: { titulo: 'Conforto em alta', segmento: 'Com 40459 menções positivas', marca: 'A marca tem 2391 menções (2.4% de queixa)' },
  lista: ['5083 curtidas', { x: '0.7%' }],
  numero: 7,
});
assert.strictEqual(narrativa.oportunidade.segmento, 'Com 40.459 menções positivas');
assert.strictEqual(narrativa.oportunidade.marca, 'A marca tem 2.391 menções (2,4% de queixa)');
assert.strictEqual(narrativa.oportunidade.titulo, 'Conforto em alta');
assert.strictEqual(narrativa.lista[0], '5.083 curtidas');
assert.strictEqual(narrativa.lista[1].x, '0,7%');
assert.strictEqual(narrativa.numero, 7);

console.log('formato.test.js: ok');
