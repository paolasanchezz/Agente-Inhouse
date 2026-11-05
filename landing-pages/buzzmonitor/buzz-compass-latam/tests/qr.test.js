// Testes do gerador de QR (assets/qr.js):  node landing-pages/buzzmonitor/buzz-compass-latam/tests/qr.test.js
// 1) vetores conhecidos da especificacao (correcao de erro, bits de formato e de versao)
// 2) leitura de volta: um decodificador escrito separadamente, so a partir da especificacao, le a matriz gerada
//    (mascara, zigzag, desintercalacao, checagem Reed-Solomon, cabecalho e texto) para varios tamanhos e os dois niveis.
// Nao substitui escanear com um celular real, mas pega erro de posicionamento e de tabela.

const assert = require('assert');
const QR = require('../assets/qr.js');
const { restoRS, divisorRS, bitsFormato, BLOCOS, capacidadeDados } = QR._interno;

// --- 1. Vetores conhecidos ---
// "HELLO WORLD" versao 1-M (exemplo classico da especificacao / tutoriais): dados e correcao.
const dadosHello = [32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17];
assert.deepStrictEqual(restoRS(dadosHello, divisorRS(10)), [196, 35, 39, 119, 235, 215, 231, 226, 93, 23], 'Reed-Solomon 1-M');
assert.strictEqual(bitsFormato('M', 0), 0b101010000010010, 'formato M mascara 0');
assert.strictEqual(bitsFormato('L', 0), 0b111011111000100, 'formato L mascara 0');
assert.strictEqual(bitsFormato('L', 4), 0b110011000101111, 'formato L mascara 4');
assert.strictEqual(bitsFormato('L', 7), 0b110100101110110, 'formato L mascara 7');
assert.strictEqual(bitsFormato('M', 5), 0b100000011001110, 'formato M mascara 5');
// Bits de versao 7: BCH(18,6), gerador 0x1F25 -> 000111110010010100 (0x07C94)
(function () {
  let r = 7;
  for (let i = 0; i < 12; i++) r = (r << 1) ^ ((r >>> 11) * 0x1f25);
  assert.strictEqual((7 << 12) | r, 0x07c94, 'versao 7');
})();
// Consistencia das tabelas: dados + correcao = total de codewords da versao.
const TOTAL = [null, 26, 44, 70, 100, 134, 172, 196, 242, 292, 346];
['L', 'M'].forEach((nivel) => {
  for (let v = 1; v <= 10; v++) {
    const [ec, grupos] = BLOCOS[nivel][v];
    const blocos = grupos.reduce((s, g) => s + g[0], 0);
    assert.strictEqual(capacidadeDados(v, nivel) + ec * blocos, TOTAL[v], `tabela ${nivel}${v}`);
  }
});

// --- 2. Leitor independente ---
const ALINH = [null, [], [6, 18], [6, 22], [6, 26], [6, 30], [6, 34], [6, 22, 38], [6, 24, 42], [6, 26, 46], [6, 28, 50]];

function ehFuncao(tam, versao, x, y) {
  if ((x <= 8 && y <= 8) || (x >= tam - 8 && y <= 8) || (x <= 8 && y >= tam - 8)) return true;
  if (x === 6 || y === 6) return true;
  if (versao >= 7 && ((x >= tam - 11 && y <= 5) || (y >= tam - 11 && x <= 5))) return true;
  const p = ALINH[versao];
  for (let a = 0; a < p.length; a++) {
    for (let b = 0; b < p.length; b++) {
      if ((a === 0 && b === 0) || (a === 0 && b === p.length - 1) || (a === p.length - 1 && b === 0)) continue;
      if (Math.abs(x - p[a]) <= 2 && Math.abs(y - p[b]) <= 2) return true;
    }
  }
  return false;
}

function mascara(n, x, y) {
  return [
    (x + y) % 2 === 0, y % 2 === 0, x % 3 === 0, (x + y) % 3 === 0,
    (Math.floor(x / 3) + Math.floor(y / 2)) % 2 === 0, ((x * y) % 2) + ((x * y) % 3) === 0,
    (((x * y) % 2) + ((x * y) % 3)) % 2 === 0, (((x + y) % 2) + ((x * y) % 3)) % 2 === 0,
  ][n];
}

function ler(qr) {
  const { size: tam, modules: m } = qr;
  const versao = (tam - 17) / 4;
  // formato (primeira copia, na ordem da especificacao)
  let bits = 0;
  const pos = [[8, 0], [8, 1], [8, 2], [8, 3], [8, 4], [8, 5], [8, 7], [8, 8], [7, 8], [5, 8], [4, 8], [3, 8], [2, 8], [1, 8], [0, 8]];
  pos.forEach(([x, y], i) => { if (m[y][x]) bits |= 1 << i; });
  let achado = null;
  for (const nivel of ['L', 'M']) for (let k = 0; k < 8; k++) if (bitsFormato(nivel, k) === bits) achado = { nivel, k };
  assert(achado, 'formato nao reconhecido');
  // segunda copia tem que bater com a primeira
  let bits2 = 0;
  for (let i = 0; i < 8; i++) if (m[8][tam - 1 - i]) bits2 |= 1 << i;
  for (let i = 8; i < 15; i++) if (m[tam - 15 + i][8]) bits2 |= 1 << i;
  assert.strictEqual(bits2, bits, 'copias do formato diferentes');
  assert.strictEqual(achado.nivel, qr.ecc);

  // zigzag
  const lidos = [];
  for (let direita = tam - 1; direita >= 1; direita -= 2) {
    if (direita === 6) direita = 5;
    const sobe = ((direita + 1) & 2) === 0;
    for (let v = 0; v < tam; v++) {
      for (let j = 0; j < 2; j++) {
        const x = direita - j;
        const y = sobe ? tam - 1 - v : v;
        if (ehFuncao(tam, versao, x, y)) continue;
        lidos.push(m[y][x] !== mascara(achado.k, x, y));
      }
    }
  }
  const [ecPorBloco, grupos] = BLOCOS[achado.nivel][versao];
  const nBlocos = grupos.reduce((s, g) => s + g[0], 0);
  const totalDados = capacidadeDados(versao, achado.nivel);
  const total = totalDados + ecPorBloco * nBlocos;
  const palavras = [];
  for (let i = 0; i < total; i++) {
    let v = 0;
    for (let b = 0; b < 8; b++) v = (v << 1) | (lidos[i * 8 + b] ? 1 : 0);
    palavras.push(v);
  }
  // desintercalar
  const tamanhos = [];
  grupos.forEach((g) => { for (let i = 0; i < g[0]; i++) tamanhos.push(g[1]); });
  const blocos = tamanhos.map(() => []);
  let p = 0;
  for (let i = 0; i < Math.max(...tamanhos); i++) tamanhos.forEach((t, b) => { if (i < t) blocos[b].push(palavras[p++]); });
  const ecs = tamanhos.map(() => []);
  for (let i = 0; i < ecPorBloco; i++) tamanhos.forEach((_, b) => ecs[b].push(palavras[p++]));
  // Reed-Solomon: a correcao recalculada tem que ser igual a lida
  blocos.forEach((b, i) => assert.deepStrictEqual(restoRS(b, divisorRS(ecPorBloco)), ecs[i], 'RS do bloco ' + i));
  const dados = [].concat(...blocos);
  // cabecalho e texto
  const bitsDados = dados.map((d) => d.toString(2).padStart(8, '0')).join('');
  assert.strictEqual(bitsDados.slice(0, 4), '0100', 'modo byte');
  const nCount = versao >= 10 ? 16 : 8;
  const len = parseInt(bitsDados.slice(4, 4 + nCount), 2);
  const bytes = [];
  for (let i = 0; i < len; i++) bytes.push(parseInt(bitsDados.slice(4 + nCount + i * 8, 4 + nCount + i * 8 + 8), 2));
  return { texto: Buffer.from(bytes).toString('utf8'), versao, mascara: achado.k };
}

const amostras = [
  'a', 'HELLO WORLD', 'https://buzzmonitor-lp-buzz-radar.vercel.app/totem-resultado?m=Natura',
  'https://buzzmonitor-lp-buzz-radar.vercel.app/totem-resultado?m=Boticário&c=Eudora&c=Avon&c=O+Boticário&n=Thamires',
  'ação, coração, não: ã é ç ü', 'x'.repeat(100), 'y'.repeat(150), 'https://exemplo.com/' + 'z'.repeat(180),
];
for (let n = 1; n <= 200; n += 7) amostras.push('t'.repeat(n));
let casos = 0;
const versoesVistas = new Set();
for (const nivel of ['L', 'M']) {
  for (const t of amostras) {
    const max = capacidadeDados(10, nivel) - 3;
    if (Buffer.byteLength(t) > max) continue;
    const qr = QR.encode(t, { ecc: nivel });
    const lido = ler(qr);
    assert.strictEqual(lido.texto, t, `ida e volta falhou (${nivel}, ${t.length} chars)`);
    versoesVistas.add(`${nivel}${lido.versao}`);
    casos++;
  }
}
assert.throws(() => QR.encode('q'.repeat(300), { ecc: 'M' }), /grande demais/);
assert(QR.toSvg('teste').startsWith('<svg'));

console.log(`qr.test.js: ${casos} casos de ida e volta ok, versoes cobertas: ${[...versoesVistas].sort().join(' ')}`);
