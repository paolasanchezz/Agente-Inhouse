// Testes do formato mexicano de numeros no texto da IA:  node landing-pages/buzzmonitor/buzz-compass-latam/tests/formato.test.js
// Mexico: virgula separa milhar (40,459), ponto separa decimal (2.4%).
const assert = require('assert');
const { formatarNumerosEsMx: f, formatarTextosEsMx } = require('../api/_lib/analise.js');

const casos = [
  // milhar sem separador ganha virgula
  ['con 40459 menciones positivas en el sector', 'con 40,459 menciones positivas en el sector'],
  ['son 2391 menciones', 'son 2,391 menciones'],
  ['1234567 posts', '1,234,567 posts'],
  ['5083 me gusta y 12000 seguidores', '5,083 me gusta y 12,000 seguidores'],
  // milhar no estilo europeu (ponto) vira virgula
  ['11.179 menciones y 30.249 posts', '11,179 menciones y 30,249 posts'],
  ['1.234.567 perfiles', '1,234,567 perfiles'],
  // decimal com virgula antes de % vira ponto
  ['2,4% de las menciones', '2.4% de las menciones'],
  ['0,7% con lenguaje de queja', '0.7% con lenguaje de queja'],
  // ja no formato mexicano, nao muda
  ['11,179 menciones (2.4%)', '11,179 menciones (2.4%)'],
  ['14.35% de quejas', '14.35% de quejas'],
  ['97% positivas', '97% positivas'],
  ['crecimiento de 12% en la última semana', 'crecimiento de 12% en la última semana'],
  // anos nao mudam
  ['en 2026 la marca creció', 'en 2026 la marca creció'],
  ['colección 2025 y 1999', 'colección 2025 y 1999'],
  // ano so e ano quando nao vem contagem logo depois
  ['2024 menciones en el periodo', '2,024 menciones en el periodo'],
  // numeros pequenos e vazios
  ['top 3 temas, 20 perfiles, 999 posts', 'top 3 temas, 20 perfiles, 999 posts'],
  ['sin ningún número', 'sin ningún número'],
  ['', ''],
];
casos.forEach(([entrada, esperado]) => assert.strictEqual(f(entrada), esperado, `"${entrada}" -> "${f(entrada)}"`));

// idempotente: passar duas vezes nao estraga
casos.forEach(([, esperado]) => assert.strictEqual(f(f(esperado)), esperado, 'idempotente: ' + esperado));

// nao-texto passa direto
assert.strictEqual(f(null), null);
assert.strictEqual(f(12345), 12345);

const narrativa = formatarTextosEsMx({
  oportunidade: { titulo: 'Comodidad en alza', segmento: 'Con 40459 menciones positivas', marca: 'La marca tiene 2391 menciones (2,4% de queja)' },
  lista: ['5083 me gusta', { x: '0,7%' }],
  numero: 7,
});
assert.strictEqual(narrativa.oportunidade.segmento, 'Con 40,459 menciones positivas');
assert.strictEqual(narrativa.oportunidade.marca, 'La marca tiene 2,391 menciones (2.4% de queja)');
assert.strictEqual(narrativa.lista[0], '5,083 me gusta');
assert.strictEqual(narrativa.lista[1].x, '0.7%');
assert.strictEqual(narrativa.numero, 7);

console.log('formato.test.js: ok');
