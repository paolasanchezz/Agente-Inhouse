// Testes dos insights montados sem IA:  node landing-pages/buzzmonitor/buzz-radar/tests/narrativa.test.js
// Garantias: 4 cards com texto pronto, numeros reais, nada de "veja o grafico", e marca pequena demais nao entra em ranking.
const assert = require('assert');
const { narrativaPorDados } = require('../api/_lib/analise.js');

const mercado = {
  sent: { positivos: 14462, neutros: 4000, negativos: 4076, total: 22538 },
  serie: [...Array(23).fill(100), ...Array(7).fill(120)],
  termos: [{ label: 'conforto', value: 9 }, { label: 'estilo', value: 8 }, { label: 'verão', value: 7 }],
  emergentes: ['cupom', 'liquidação'],
  tendenciaSentimento: -4,
  positivos: [{ tipo: 'foto', resumo: 'Sandália confortável para o dia a dia' }],
  negativos: [{ tipo: 'foto', resumo: 'Chinelo que estragou na primeira semana' }],
  destaques: [{ tipo: 'VIDEO', curtidas: 10, compartilhamentos: 2, resumo: 'x' }],
};
const comparacao = [
  { rotulo: 'Havaianas', tipo: 'marca', origem: 'informado', volume: 2829, share_pct: 34, pct_positivo: 78, crescimento_pct: 28 },
  { rotulo: 'Melissa', tipo: 'concorrente', origem: 'sugerido', volume: 4726, share_pct: 56, pct_positivo: 74, crescimento_pct: -11 },
  { rotulo: 'Ipanema', tipo: 'concorrente', origem: 'informado', volume: 16, share_pct: 0, pct_positivo: 99, crescimento_pct: 900 },
];

const n = narrativaPorDados({ marca: 'Havaianas', segmento: 'Calçados e Chinelos', mercado, comparacao, sugeridos: true });

assert.deepStrictEqual(Object.keys(n).sort(), ['concorrentes', 'oportunidade', 'risco', 'tendencia_emergente']);
for (const [k, c] of Object.entries(n)) {
  assert(c.titulo, `${k}: titulo`);
  assert(c.segmento.length > 40, `${k}: paragrafo do segmento com texto de verdade`);
  assert(c.marca.length > 40, `${k}: paragrafo da marca com texto de verdade`);
  const texto = `${c.segmento} ${c.marca}`;
  assert(!/gr[aá]fico|abaixo|nuvem|tabela|veja/i.test(texto), `${k}: nao pode mandar ver grafico`);
  assert(!/dados insuficientes|sem dados|dados limitados|aparece pouco na (nossa )?base/i.test(texto), `${k}: sem linguagem de "dados insuficientes"`);
  assert(!texto.includes('—'), `${k}: sem em-dash`);
  assert(/\d/.test(texto), `${k}: cita numero real`);
}
const todos = Object.values(n).map((c) => `${c.segmento} ${c.marca}`).join(' ');
assert(n.concorrentes.segmento.includes('Melissa lidera'), 'lider por volume (paragrafo do segmento)');
assert(n.concorrentes.marca.includes('Havaianas tem 34%'), 'posicao da marca (paragrafo da marca)');
assert(!/Ipanema, com 99%|Ipanema, com \+900%/.test(todos), 'marca com menos de 50 mencoes nao entra em ranking');
assert(n.concorrentes.segmento.includes('Ipanema tem pouca conversa'), 'explica sem dizer "dados insuficientes"');
assert(n.risco.segmento.includes('caiu 4 pontos'), 'tendencia de sentimento e do segmento');
assert(n.tendencia_emergente.segmento.includes('cupom e liquidação'), 'termos emergentes');
assert(n.tendencia_emergente.segmento.includes('video'), 'formato que performa');
assert(n.oportunidade.segmento.includes('Sandália confortável'), 'exemplo positivo real');
assert(n.oportunidade.marca.includes('78%'), 'a marca tem o proprio percentual positivo no paragrafo dela');
console.log('narrativa.test.js: ok');
