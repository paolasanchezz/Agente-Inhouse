// Testes dos insights montados sem IA:  node landing-pages/buzzmonitor/buzz-compass-latam/tests/narrativa.test.js
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
  assert(!/gr[aá]fic|abajo|nube|tabla|\bmira\b/i.test(texto), `${k}: nao pode mandar ver grafico`);
  assert(!/datos insuficientes|sin datos|datos limitados|aparece poco en la base/i.test(texto), `${k}: sem linguagem de "dados insuficientes"`);
  assert(!texto.includes('—'), `${k}: sem em-dash`);
  assert(/\d/.test(texto), `${k}: cita numero real`);
}
const todos = Object.values(n).map((c) => `${c.segmento} ${c.marca}`).join(' ');
assert(n.concorrentes.segmento.includes('Melissa lidera'), 'lider por volume (paragrafo do segmento)');
assert(n.concorrentes.marca.includes('Havaianas tiene el 34%'), 'posicao da marca (paragrafo da marca)');
assert(!/Ipanema, com 99%|Ipanema, com \+900%/.test(todos), 'marca com menos de 50 mencoes nao entra em ranking');
assert(n.concorrentes.segmento.includes('Ipanema tiene poca conversación'), 'explica sem dizer "dados insuficientes"');
assert(n.risco.segmento.includes('bajó 4 puntos'), 'tendencia de sentimento e do segmento');
assert(n.tendencia_emergente.segmento.includes('cupom y liquidação'), 'termos emergentes');
assert(n.tendencia_emergente.segmento.includes('video'), 'formato que performa');
assert(n.oportunidade.segmento.includes('Sandália confortável'), 'exemplo positivo real');
assert(n.oportunidade.marca.includes('78%'), 'a marca tem o proprio percentual positivo no paragrafo dela');
console.log('narrativa.test.js: ok');

// Card da IA vazio ou cortado (Claude no limite de tokens, 2026-11-13): troca so ele pelo card dos dados
const { completarNarrativa } = require('../api/_lib/analise.js');
const daIA = {
  oportunidade: { titulo: 'Antojo de quincena', segmento: 'texto do mercado', marca: 'texto da marca' },
  risco: { titulo: 'Risco', segmento: 'x', marca: 'y' },
  tendencia_emergente: { titulo: 'Tendencia', segmento: 'x', marca: 'y' },
};
Object.defineProperty(daIA, '_modelo', { value: 'anthropic:claude-sonnet-5', enumerable: false });
const erroOriginal = console.error; console.error = () => {};
const completa = completarNarrativa(daIA, () => n);
console.error = erroOriginal;
assert.strictEqual(completa.oportunidade.titulo, 'Antojo de quincena', 'card da IA completo fica');
assert.deepStrictEqual(completa.concorrentes, n.concorrentes, 'card que faltou vem dos dados');
assert.strictEqual(completa._modelo, 'anthropic:claude-sonnet-5', 'mantem o modelo que escreveu');
const vazio = completarNarrativa({ ...daIA, concorrentes: { titulo: 'Competidores', segmento: '', marca: 'algo' } }, () => n);
assert.deepStrictEqual(vazio.concorrentes, n.concorrentes, 'card com campo vazio tambem e trocado');
let chamouReserva = false;
const inteira = { ...daIA, concorrentes: { titulo: 'a', segmento: 'b', marca: 'c' } };
assert.strictEqual(completarNarrativa(inteira, () => { chamouReserva = true; return n; }), inteira, 'narrativa completa passa direto');
assert(!chamouReserva, 'sem card faltando, nem monta a reserva');
console.log('narrativa.test.js (cards completos): ok');
