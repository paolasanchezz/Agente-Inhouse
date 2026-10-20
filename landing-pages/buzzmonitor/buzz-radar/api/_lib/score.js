// Compass Score da MARCA (0 a 100): 4 sub-scores calculados em codigo, sem IA. Formulas em SCORING.md.
//
//   Presenca             quanto a marca aparece na conversa, frente aos concorrentes comparados e em volume absoluto
//   Reputacao            posts positivos entre os que tem polaridade, mais o peso das queixas
//   Ritmo de crescimento ultima semana contra a anterior
//   Vantagem competitiva reputacao e ritmo da marca contra a media dos concorrentes
//
// Marca com pouca conversa NUNCA vira "sem dados": a Trends so devolve 30 dias (testado: 60, 90 e 180 dias voltam o mesmo
// total), entao nao da para ampliar o periodo. Em vez disso, reputacao e ritmo sao completados pelo segmento na proporcao
// da falta de dados (ponderacao por confianca): com muita conversa o numero e so da marca; com pouca, vai puxando para o do
// segmento, e o sub-score recebe o rotulo "estimado". Presenca nao entra nessa regra: ser pouco falada e, ela mesma, o
// resultado.

const PESOS = { presenca: 0.25, reputacao: 0.30, ritmo: 0.20, vantagem: 0.25 };
const K_REPUTACAO = 40; // posts com polaridade que dao ao segmento o mesmo peso da marca
const K_RITMO = 30; // mencoes nas duas ultimas semanas que dao ao segmento o mesmo peso da marca
const CONFIANCA_MINIMA = 0.6; // abaixo disso o sub-score e marcado como estimado
const VOLUME_PARA_QUEIXA = 200; // abaixo disso o percentual de queixa e ruido e nao pesa

const clamp = (x, min = 0, max = 100) => Math.max(min, Math.min(max, x));

function volumeScore(total) {
  const buckets = [[50, 15], [200, 30], [1000, 50], [5000, 70], [20000, 85], [Infinity, 97]];
  for (const [limite, score] of buckets) if (total <= limite) return score;
  return 97;
}

// Variacao da ultima semana contra a anterior, em %. null sem serie suficiente.
function crescimentoPct(serie) {
  if (!Array.isArray(serie) || serie.length < 14) return null;
  const ultimos7 = serie.slice(-7).reduce((s, v) => s + v, 0);
  const anteriores7 = serie.slice(-14, -7).reduce((s, v) => s + v, 0);
  if (anteriores7 === 0) return ultimos7 > 0 ? 100 : 0;
  return Math.round(((ultimos7 - anteriores7) / anteriores7) * 100);
}

// 50 = estavel; teto e piso de +-50 pontos (um pico de 1 dia nao estoura a escala).
function ritmoScore(serie) {
  if (!Array.isArray(serie) || serie.length < 14) return 50;
  const ultimos7 = serie.slice(-7).reduce((s, v) => s + v, 0);
  const anteriores7 = serie.slice(-14, -7).reduce((s, v) => s + v, 0);
  if (anteriores7 === 0) return ultimos7 > 0 ? 75 : 50;
  const pct = (ultimos7 - anteriores7) / anteriores7;
  return Math.round(50 + clamp(pct * 100, -50, 50));
}

// peso do grupo = n / (n + K). Devolve o valor misturado e se a confianca ficou baixa.
function misturar(valorGrupo, n, valorBase, K) {
  const w = n / (n + K);
  return { valor: w * valorGrupo + (1 - w) * valorBase, estimado: w < CONFIANCA_MINIMA };
}

// g: { positivos, negativos, total, reclamacao_pct }   base: { pctPositivo, ritmo }
function reputacaoDe(g, base) {
  const n = g.positivos + g.negativos;
  const pctGrupo = n ? (g.positivos / n) * 100 : base.pctPositivo;
  const m = misturar(pctGrupo, n, base.pctPositivo, K_REPUTACAO);
  let valor = m.valor;
  if (g.reclamacao_pct != null && g.total >= VOLUME_PARA_QUEIXA) {
    const semQueixa = 100 - clamp(g.reclamacao_pct * 10); // 10% das mencoes com linguagem de queixa zera
    valor = 0.7 * valor + 0.3 * semQueixa;
  }
  return { valor: Math.round(valor), estimado: m.estimado };
}

// g: { serie }
function ritmoDe(g, base) {
  const serie = g.serie || [];
  const n14 = serie.slice(-14).reduce((s, v) => s + v, 0);
  const m = misturar(ritmoScore(serie), n14, base.ritmo, K_RITMO);
  return { valor: Math.round(m.valor), estimado: m.estimado };
}

// Participacao frente a uma divisao igual entre as marcas comparadas (2x a fatia justa = 100) + escala de volume.
function presencaDe(g, todos) {
  const vol = volumeScore(g.total);
  if (todos.length < 2) return vol;
  const soma = todos.reduce((s, x) => s + x.total, 0);
  const fatia = soma ? g.total / soma : 0;
  const naFatiaJusta = clamp(50 * (fatia / (1 / todos.length)));
  return Math.round(0.5 * naFatiaJusta + 0.5 * vol);
}

const media = (lista) => (lista.length ? lista.reduce((s, x) => s + x, 0) / lista.length : null);

// marca e concorrentes: { positivos, negativos, total, reclamacao_pct, serie }. mercado: { positivos, negativos, serie }.
function scoreDaMarca({ marca, concorrentes, mercado }) {
  const polaridade = mercado.positivos + mercado.negativos;
  const base = {
    pctPositivo: polaridade ? (mercado.positivos / polaridade) * 100 : 50,
    ritmo: ritmoScore(mercado.serie),
  };
  const todos = [marca, ...concorrentes];

  const rep = reputacaoDe(marca, base);
  const rit = ritmoDe(marca, base);
  const presenca = presencaDe(marca, todos);

  // Vantagem: reputacao e ritmo da marca menos a media dos concorrentes (cada um com a mesma regra de confianca).
  const repConc = media(concorrentes.map((c) => reputacaoDe(c, base).valor));
  const ritConc = media(concorrentes.map((c) => ritmoDe(c, base).valor));
  const vantagem = repConc === null
    ? 50
    : Math.round(clamp(50 + 0.6 * (rep.valor - repConc) + 0.4 * (rit.valor - ritConc)));

  const compass = Math.round(PESOS.presenca * presenca + PESOS.reputacao * rep.valor + PESOS.ritmo * rit.valor + PESOS.vantagem * vantagem);
  return {
    presenca,
    reputacao: rep.valor,
    ritmo: rit.valor,
    vantagem,
    compass_score: compass,
    estimado: { reputacao: rep.estimado, ritmo: rit.estimado, vantagem: rep.estimado || rit.estimado },
  };
}

module.exports = { scoreDaMarca, volumeScore, ritmoScore, crescimentoPct, PESOS, K_REPUTACAO, K_RITMO };
