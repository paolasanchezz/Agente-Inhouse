// Servidor local para testar o Buzz Radar (paginas + funcoes de api/) sem `vercel dev`.
//   node landing-pages/buzzmonitor/buzz-radar/dev-server.js [porta]     (porta padrao 8936)
// Imita o que a Vercel faz no deploy: cleanUrls (/totem -> totem.html), funcoes em /api/<nome> com req.query,
// req.body e res.json, e /brand/* apontando para a pasta brand/ do repo (os HTMLs de source usam ../../brand/...,
// que o passo de deploy reescreve para /assets/logos/...).
// Variaveis de ambiente (OPENAI_API_KEY, RESEND_API_KEY...) vem do processo; sem chave a IA fica desligada e o
// totem usa os fallbacks (busca pelo nome exato, sem concorrente sugerido, sem narrativa).

const http = require('http');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

const RAIZ = __dirname;
const REPO = path.resolve(__dirname, '..', '..', '..');
const PORTA = Number(process.argv[2]) || 8936;
const TIPOS = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.json': 'application/json', '.ico': 'image/x-icon',
};

function arquivoSeguro(base, relativo) {
  const alvo = path.resolve(base, '.' + path.posix.normalize('/' + relativo));
  return alvo.startsWith(base) && fs.existsSync(alvo) && fs.statSync(alvo).isFile() ? alvo : null;
}

function servirArquivo(res, arquivo) {
  res.statusCode = 200;
  res.setHeader('Content-Type', TIPOS[path.extname(arquivo).toLowerCase()] || 'application/octet-stream');
  res.setHeader('Cache-Control', 'no-store');
  fs.createReadStream(arquivo).pipe(res);
}

async function lerCorpo(req) {
  const partes = [];
  for await (const p of req) partes.push(p);
  const texto = Buffer.concat(partes).toString('utf8');
  if (!texto) return undefined;
  try { return JSON.parse(texto); } catch (_) { return texto; }
}

http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORTA}`);
  const rota = decodeURIComponent(url.pathname);

  if (rota.startsWith('/api/')) {
    const nome = rota.slice(5).replace(/[^a-z0-9-]/gi, '');
    const arquivo = path.join(RAIZ, 'api', `${nome}.js`);
    if (!nome || !fs.existsSync(arquivo)) { res.statusCode = 404; return res.end('sem funcao'); }
    req.query = {};
    for (const chave of new Set(url.searchParams.keys())) {
      const todos = url.searchParams.getAll(chave);
      req.query[chave] = todos.length > 1 ? todos : todos[0];
    }
    if (req.method !== 'GET') req.body = await lerCorpo(req);
    res.json = (obj) => { res.setHeader('Content-Type', 'application/json; charset=utf-8'); res.end(JSON.stringify(obj)); };
    // Recarrega a rota e tudo de api/ (inclui _lib): assim editar um helper vale na proxima requisicao.
    Object.keys(require.cache).forEach((k) => { if (k.startsWith(path.join(RAIZ, 'api'))) delete require.cache[k]; });
    try {
      return await require(arquivo)(req, res);
    } catch (err) {
      console.error(err);
      res.statusCode = 500;
      return res.end('erro na funcao');
    }
  }

  const candidatos = [];
  if (rota === '/') candidatos.push([RAIZ, 'index.html']);
  else {
    candidatos.push([RAIZ, rota], [RAIZ, `${rota}.html`]);
    if (rota.startsWith('/brand/')) candidatos.push([REPO, rota]);
    if (rota.startsWith('/assets/logos/')) candidatos.push([path.join(REPO, 'brand', 'buzzmonitor'), rota]);
  }
  for (const [base, rel] of candidatos) {
    const arquivo = arquivoSeguro(base, rel);
    if (arquivo) return servirArquivo(res, arquivo);
  }
  res.statusCode = 404;
  res.end('nao encontrado');
}).listen(PORTA, () => console.log(`Buzz Radar local em http://localhost:${PORTA}`));
