// Gera PNG (tons de cinza, 8 bits) a partir da matriz de um QR code, sem dependencia. Serve para o QR dentro do e-mail:
// Gmail e Outlook nao mostram SVG nem imagem embutida (data:), so imagem por endereco https, em PNG.
const zlib = require('zlib');

const TABELA_CRC = (() => {
  const t = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    t[n] = c >>> 0;
  }
  return t;
})();

function crc32(buf) {
  let c = 0xffffffff;
  for (let i = 0; i < buf.length; i++) c = TABELA_CRC[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

function bloco(tipo, dados) {
  const corpo = Buffer.concat([Buffer.from(tipo, 'ascii'), dados]);
  const tam = Buffer.alloc(4);
  tam.writeUInt32BE(dados.length, 0);
  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32(corpo), 0);
  return Buffer.concat([tam, corpo, crc]);
}

// modules: matriz [linha][coluna] de 0/1 (1 = modulo escuro). escala: pixels por modulo. margem: modulos de borda clara.
function matrizParaPng(modules, { escala = 8, margem = 3 } = {}) {
  const n = modules.length;
  const lado = (n + margem * 2) * escala;
  const linhaBytes = lado + 1; // 1 byte de filtro (0) por linha
  const cru = Buffer.alloc(linhaBytes * lado, 255); // fundo branco
  for (let y = 0; y < lado; y++) cru[y * linhaBytes] = 0;
  for (let my = 0; my < n; my++) {
    for (let mx = 0; mx < n; mx++) {
      if (!modules[my][mx]) continue;
      for (let dy = 0; dy < escala; dy++) {
        const y = (my + margem) * escala + dy;
        const ini = y * linhaBytes + 1 + (mx + margem) * escala;
        cru.fill(0, ini, ini + escala);
      }
    }
  }
  const cabecalho = Buffer.alloc(13);
  cabecalho.writeUInt32BE(lado, 0);
  cabecalho.writeUInt32BE(lado, 4);
  cabecalho[8] = 8; // 8 bits por canal
  cabecalho[9] = 0; // tons de cinza
  return Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    bloco('IHDR', cabecalho),
    bloco('IDAT', zlib.deflateSync(cru, { level: 9 })),
    bloco('IEND', Buffer.alloc(0)),
  ]);
}

module.exports = { matrizParaPng, crc32 };
