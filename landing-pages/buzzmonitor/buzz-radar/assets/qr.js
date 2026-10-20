// Gerador de QR code sem dependencia (modo byte, correcao L ou M, versoes 1 a 10, ate 213 bytes em M).
// Escrito dentro do projeto de proposito: a pagina nao carrega nada de CDN e a CSP continua so com 'self'.
// Estrutura baseada na especificacao ISO/IEC 18004; validado com vetores conhecidos e leitura de volta
// (ver tests/qr.test.js). Uso:  QR.toSvg('https://exemplo.com', { ecc: 'M' })  ->  string <svg>

(function (raiz) {
  'use strict';

  // [versao 1..10] -> por nivel: [codewords de correcao por bloco, [[qtd de blocos, codewords de dados por bloco], ...]]
  var BLOCOS = {
    L: [null,
      [7, [[1, 19]]], [10, [[1, 34]]], [15, [[1, 55]]], [20, [[1, 80]]], [26, [[1, 108]]],
      [18, [[2, 68]]], [20, [[2, 78]]], [24, [[2, 97]]], [30, [[2, 116]]], [18, [[2, 68], [2, 69]]]],
    M: [null,
      [10, [[1, 16]]], [16, [[1, 28]]], [26, [[1, 44]]], [18, [[2, 32]]], [24, [[2, 43]]],
      [16, [[4, 27]]], [18, [[4, 31]]], [22, [[2, 38], [2, 39]]], [22, [[3, 36], [2, 37]]], [26, [[4, 43], [1, 44]]]],
  };
  var ALINHAMENTO = [null, [], [6, 18], [6, 22], [6, 26], [6, 30], [6, 34], [6, 22, 38], [6, 24, 42], [6, 26, 46], [6, 28, 50]];
  var BITS_FORMATO_ECC = { L: 1, M: 0 };

  function capacidadeDados(versao, nivel) {
    return BLOCOS[nivel][versao][1].reduce(function (s, g) { return s + g[0] * g[1]; }, 0);
  }

  // --- Corpo de Galois GF(256), polinomio 0x11D ---
  function mulGF(x, y) {
    var z = 0;
    for (var i = 7; i >= 0; i--) {
      z = (z << 1) ^ ((z >>> 7) * 0x11d);
      z ^= ((y >>> i) & 1) * x;
    }
    return z;
  }

  function divisorRS(grau) {
    var r = new Array(grau).fill(0);
    r[grau - 1] = 1;
    var raiz = 1;
    for (var i = 0; i < grau; i++) {
      for (var j = 0; j < grau; j++) {
        r[j] = mulGF(r[j], raiz);
        if (j + 1 < grau) r[j] ^= r[j + 1];
      }
      raiz = mulGF(raiz, 2);
    }
    return r;
  }

  function restoRS(dados, divisor) {
    var r = divisor.map(function () { return 0; });
    dados.forEach(function (b) {
      var fator = b ^ r.shift();
      r.push(0);
      divisor.forEach(function (c, i) { r[i] ^= mulGF(c, fator); });
    });
    return r;
  }

  function utf8(texto) {
    var s = unescape(encodeURIComponent(texto));
    var out = [];
    for (var i = 0; i < s.length; i++) out.push(s.charCodeAt(i));
    return out;
  }

  // --- Dados: cabecalho, bytes, terminador, preenchimento ---
  function montarCodewords(bytes, versao, nivel) {
    var capacidade = capacidadeDados(versao, nivel);
    var bits = [];
    function empurra(valor, qtd) { for (var i = qtd - 1; i >= 0; i--) bits.push((valor >>> i) & 1); }
    empurra(4, 4); // modo byte
    empurra(bytes.length, versao >= 10 ? 16 : 8);
    bytes.forEach(function (b) { empurra(b, 8); });
    empurra(0, Math.min(4, capacidade * 8 - bits.length));
    while (bits.length % 8) bits.push(0);
    var palavras = [];
    for (var i = 0; i < bits.length; i += 8) {
      var v = 0;
      for (var k = 0; k < 8; k++) v = (v << 1) | bits[i + k];
      palavras.push(v);
    }
    for (var pad = 0xec; palavras.length < capacidade; pad ^= 0xec ^ 0x11) palavras.push(pad);
    return palavras;
  }

  // Divide em blocos, calcula a correcao de cada um e intercala (dados primeiro, correcao depois).
  function intercalar(palavras, versao, nivel) {
    var ecPorBloco = BLOCOS[nivel][versao][0];
    var blocos = [];
    var pos = 0;
    BLOCOS[nivel][versao][1].forEach(function (g) {
      for (var n = 0; n < g[0]; n++) {
        blocos.push(palavras.slice(pos, pos + g[1]));
        pos += g[1];
      }
    });
    var divisor = divisorRS(ecPorBloco);
    var ecs = blocos.map(function (b) { return restoRS(b, divisor); });
    var out = [];
    var maxDados = Math.max.apply(null, blocos.map(function (b) { return b.length; }));
    for (var i = 0; i < maxDados; i++) blocos.forEach(function (b) { if (i < b.length) out.push(b[i]); });
    for (var j = 0; j < ecPorBloco; j++) ecs.forEach(function (e) { out.push(e[j]); });
    return out;
  }

  // --- Matriz ---
  function criarMatriz(tam) {
    var m = [];
    var f = [];
    for (var y = 0; y < tam; y++) { m.push(new Array(tam).fill(false)); f.push(new Array(tam).fill(false)); }
    return { m: m, f: f, tam: tam };
  }

  function funcao(mat, x, y, escuro) {
    mat.m[y][x] = escuro;
    mat.f[y][x] = true;
  }

  function bitDe(valor, i) { return ((valor >>> i) & 1) !== 0; }

  function desenharPadroes(mat, versao) {
    var tam = mat.tam;
    var i;
    for (i = 0; i < tam; i++) { funcao(mat, 6, i, i % 2 === 0); funcao(mat, i, 6, i % 2 === 0); }
    function localizador(cx, cy) {
      for (var dy = -4; dy <= 4; dy++) {
        for (var dx = -4; dx <= 4; dx++) {
          var dist = Math.max(Math.abs(dx), Math.abs(dy));
          var x = cx + dx, y = cy + dy;
          if (x >= 0 && x < tam && y >= 0 && y < tam) funcao(mat, x, y, dist !== 2 && dist !== 4);
        }
      }
    }
    localizador(3, 3); localizador(tam - 4, 3); localizador(3, tam - 4);
    var pos = ALINHAMENTO[versao];
    var n = pos.length;
    for (var a = 0; a < n; a++) {
      for (var b = 0; b < n; b++) {
        if ((a === 0 && b === 0) || (a === 0 && b === n - 1) || (a === n - 1 && b === 0)) continue;
        for (var dy = -2; dy <= 2; dy++) {
          for (var dx = -2; dx <= 2; dx++) funcao(mat, pos[a] + dx, pos[b] + dy, Math.max(Math.abs(dx), Math.abs(dy)) !== 1);
        }
      }
    }
    desenharFormato(mat, 'M', 0); // reserva as areas; sera redesenhado com o valor certo
    if (versao >= 7) {
      var resto = versao;
      for (i = 0; i < 12; i++) resto = (resto << 1) ^ ((resto >>> 11) * 0x1f25);
      var bits = (versao << 12) | resto;
      for (i = 0; i < 18; i++) {
        var cor = bitDe(bits, i);
        var p = tam - 11 + (i % 3);
        var q = Math.floor(i / 3);
        funcao(mat, p, q, cor);
        funcao(mat, q, p, cor);
      }
    }
  }

  function bitsFormato(nivel, mascara) {
    var dados = (BITS_FORMATO_ECC[nivel] << 3) | mascara;
    var resto = dados;
    for (var i = 0; i < 10; i++) resto = (resto << 1) ^ ((resto >>> 9) * 0x537);
    return ((dados << 10) | resto) ^ 0x5412;
  }

  function desenharFormato(mat, nivel, mascara) {
    var bits = bitsFormato(nivel, mascara);
    var tam = mat.tam;
    var i;
    for (i = 0; i <= 5; i++) funcao(mat, 8, i, bitDe(bits, i));
    funcao(mat, 8, 7, bitDe(bits, 6));
    funcao(mat, 8, 8, bitDe(bits, 7));
    funcao(mat, 7, 8, bitDe(bits, 8));
    for (i = 9; i < 15; i++) funcao(mat, 14 - i, 8, bitDe(bits, i));
    for (i = 0; i < 8; i++) funcao(mat, tam - 1 - i, 8, bitDe(bits, i));
    for (i = 8; i < 15; i++) funcao(mat, 8, tam - 15 + i, bitDe(bits, i));
    funcao(mat, 8, tam - 8, true); // modulo escuro fixo
  }

  function posicionarDados(mat, palavras) {
    var tam = mat.tam;
    var i = 0;
    for (var direita = tam - 1; direita >= 1; direita -= 2) {
      if (direita === 6) direita = 5;
      for (var vert = 0; vert < tam; vert++) {
        for (var j = 0; j < 2; j++) {
          var x = direita - j;
          var sobe = ((direita + 1) & 2) === 0;
          var y = sobe ? tam - 1 - vert : vert;
          if (!mat.f[y][x] && i < palavras.length * 8) {
            mat.m[y][x] = bitDe(palavras[i >>> 3], 7 - (i & 7));
            i++;
          }
        }
      }
    }
  }

  function mascaraInverte(mascara, x, y) {
    switch (mascara) {
      case 0: return (x + y) % 2 === 0;
      case 1: return y % 2 === 0;
      case 2: return x % 3 === 0;
      case 3: return (x + y) % 3 === 0;
      case 4: return (Math.floor(x / 3) + Math.floor(y / 2)) % 2 === 0;
      case 5: return ((x * y) % 2) + ((x * y) % 3) === 0;
      case 6: return (((x * y) % 2) + ((x * y) % 3)) % 2 === 0;
      default: return (((x + y) % 2) + ((x * y) % 3)) % 2 === 0;
    }
  }

  function aplicarMascara(mat, mascara) {
    for (var y = 0; y < mat.tam; y++) {
      for (var x = 0; x < mat.tam; x++) {
        if (!mat.f[y][x] && mascaraInverte(mascara, x, y)) mat.m[y][x] = !mat.m[y][x];
      }
    }
  }

  // Penalidade das 4 regras da especificacao (so serve para escolher a melhor mascara; qualquer mascara le).
  function penalidade(mat) {
    var tam = mat.tam, m = mat.m, total = 0, x, y, k;
    function linhas(get) {
      for (var a = 0; a < tam; a++) {
        var corrida = 1, str = '';
        for (var b = 0; b < tam; b++) {
          var v = get(a, b);
          str += v ? '1' : '0';
          if (b > 0 && v === get(a, b - 1)) { corrida++; if (corrida === 5) total += 3; else if (corrida > 5) total++; } else corrida = 1;
        }
        var re = /(?=(10111010000|00001011101))/g;
        while (re.exec(str)) { total += 40; re.lastIndex++; }
      }
    }
    linhas(function (a, b) { return m[a][b]; });
    linhas(function (a, b) { return m[b][a]; });
    for (y = 0; y < tam - 1; y++) {
      for (x = 0; x < tam - 1; x++) {
        if (m[y][x] === m[y][x + 1] && m[y][x] === m[y + 1][x] && m[y][x] === m[y + 1][x + 1]) total += 3;
      }
    }
    var escuros = 0;
    for (y = 0; y < tam; y++) for (x = 0; x < tam; x++) if (m[y][x]) escuros++;
    k = Math.ceil(Math.abs(escuros * 20 - tam * tam * 10) / (tam * tam)) - 1;
    return total + Math.max(0, k) * 10;
  }

  function codificar(texto, opcoes) {
    var nivel = (opcoes && opcoes.ecc) === 'L' ? 'L' : 'M';
    var bytes = utf8(String(texto));
    var versao = 0;
    for (var v = 1; v <= 10; v++) {
      var cabecalho = 4 + (v >= 10 ? 16 : 8);
      if (cabecalho + bytes.length * 8 <= capacidadeDados(v, nivel) * 8) { versao = v; break; }
    }
    if (!versao) throw new Error('texto grande demais para o QR code (maximo ' + (capacidadeDados(10, nivel) - 3) + ' bytes)');

    var palavras = intercalar(montarCodewords(bytes, versao, nivel), versao, nivel);
    var base = criarMatriz(17 + versao * 4);
    desenharPadroes(base, versao);
    posicionarDados(base, palavras);

    var melhor = null, melhorPenalidade = Infinity, melhorMascara = 0;
    for (var mascara = 0; mascara < 8; mascara++) {
      var copia = { tam: base.tam, f: base.f, m: base.m.map(function (linha) { return linha.slice(); }) };
      aplicarMascara(copia, mascara);
      desenharFormato(copia, nivel, mascara);
      var p = penalidade(copia);
      if (p < melhorPenalidade) { melhorPenalidade = p; melhor = copia; melhorMascara = mascara; }
    }
    return { size: melhor.tam, modules: melhor.m, version: versao, mask: melhorMascara, ecc: nivel };
  }

  function toSvg(texto, opcoes) {
    var o = opcoes || {};
    var qr = codificar(texto, o);
    var margem = o.margin == null ? 4 : o.margin;
    var dim = qr.size + margem * 2;
    var path = '';
    for (var y = 0; y < qr.size; y++) {
      for (var x = 0; x < qr.size; x++) {
        if (qr.modules[y][x]) path += 'M' + (x + margem) + ',' + (y + margem) + 'h1v1h-1z';
      }
    }
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + dim + ' ' + dim + '" shape-rendering="crispEdges" role="img" aria-label="QR code">' +
      '<rect width="' + dim + '" height="' + dim + '" fill="' + (o.light || '#ffffff') + '"/>' +
      '<path d="' + path + '" fill="' + (o.dark || '#000000') + '"/></svg>';
  }

  var API = { encode: codificar, toSvg: toSvg, _interno: { divisorRS: divisorRS, restoRS: restoRS, bitsFormato: bitsFormato, capacidadeDados: capacidadeDados, BLOCOS: BLOCOS } };
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
  else raiz.QR = API;
})(typeof window !== 'undefined' ? window : this);
