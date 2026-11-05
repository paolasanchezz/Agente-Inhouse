// QR code em PNG, para a imagem dentro do e-mail do lead.
// GET /api/qr?d=<link do resultado codificado>   (so aceita links /totem-resultado deste projeto)
//
// Por que existe: o e-mail precisa do QR como imagem por endereco https (Gmail e Outlook bloqueiam SVG e imagem embutida).
// O mesmo gerador de QR do totem (assets/qr.js) roda aqui. O PNG e deterministico para o mesmo link, entao fica no cache da
// borda por 1 ano.

const QR = require('../assets/qr.js');
const { matrizParaPng } = require('./_lib/png');

const HOSTS_EXTRA = ['buzzcompass.buzzmonitor.com', 'buzzmonitor-lp-buzz-compass-latam.vercel.app']; // versao LATAM: + host da requisicao e de TOTEM_BASE_URL

// So links do proprio resultado: sem isso o endpoint viraria gerador de QR para qualquer endereco (phishing com a nossa marca).
function linkPermitido(valor, hostDaRequisicao) {
  let u;
  try { u = new URL(String(valor || '')); } catch (e) { return null; }
  // versao LATAM: o resultado vive em /es/totem-resultado (o /totem-resultado sem prefixo tambem vale, no endereco direto do projeto)
  if (u.protocol !== 'https:' || !/^(\/es)?\/totem-resultado$/.test(u.pathname)) return null;
  const hosts = new Set([...HOSTS_EXTRA, String(hostDaRequisicao || '').toLowerCase()]);
  if (process.env.TOTEM_BASE_URL) { try { hosts.add(new URL(process.env.TOTEM_BASE_URL).host.toLowerCase()); } catch (e) { /* ignora */ } }
  return hosts.has(u.host.toLowerCase()) ? u.href : null;
}

function gerar(texto) {
  // M corrige mais erro; se o link for longo demais para M, cai para L (cabe mais texto)
  for (const ecc of ['M', 'L']) {
    try { return matrizParaPng(QR.encode(texto, { ecc }).modules, { escala: 8, margem: 3 }); } catch (e) { /* tenta o proximo */ }
  }
  return null;
}

module.exports = (req, res) => {
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    res.setHeader('Cache-Control', 'no-store');
    res.statusCode = 405;
    return res.end();
  }
  const host = (req.headers && (req.headers['x-forwarded-host'] || req.headers.host)) || '';
  const link = linkPermitido(req.query && req.query.d, host);
  const png = link ? gerar(link) : null;
  if (!png) {
    res.setHeader('Cache-Control', 'no-store');
    res.statusCode = 400;
    return res.end();
  }
  res.setHeader('Content-Type', 'image/png');
  res.setHeader('Content-Length', String(png.length));
  res.setHeader('Cache-Control', 'public, max-age=31536000, s-maxage=31536000, immutable');
  res.statusCode = 200;
  return req.method === 'HEAD' ? res.end() : res.end(png);
};

module.exports.linkPermitido = linkPermitido;
