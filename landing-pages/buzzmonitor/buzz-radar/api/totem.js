// Totem Buzz Compass: analise de uma marca contra 3 concorrentes.
// GET /api/totem?m=Marca&s=Segmento&i=perfil_instagram&c=Concorrente1&c=Concorrente2&c=Concorrente3  (s, i e c opcionais, c ate 3)
//
// GET de proposito: a resposta nao tem dado pessoal (o lead vai em /api/totem-lead) e por isso pode ficar no cache da
// borda por 24h. O totem consulta primeiro; quando a pessoa abre o link do QR code ou do e-mail (mesma URL de
// analise), o celular recebe o resultado pronto em vez de refazer 20+ chamadas. Se o cache nao estiver la, a
// analise roda de novo (demora, mas funciona).

const { normalize } = require('./_lib/trends');
const { analisar } = require('./_lib/analise');
const { limparPerfil } = require('./_lib/perfil');

function paraLista(valor) {
  if (Array.isArray(valor)) return valor;
  return typeof valor === 'string' ? [valor] : [];
}

// ?debug=1 devolve o texto que a IA recebeu. So em desenvolvimento local (ou com TOTEM_DEBUG=1 no projeto): em producao ele
// abriria um caminho para furar o cache e gastar IA.
function debugPermitido(req) {
  const host = String((req.headers && (req.headers['x-forwarded-host'] || req.headers.host)) || '');
  return process.env.TOTEM_DEBUG === '1' || /^(localhost|127\.0\.0\.1|\[::1\])(:\d+)?$/.test(host);
}

module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    res.setHeader('Cache-Control', 'no-store');
    res.statusCode = 405;
    return res.json({ ok: false, error: 'method_not_allowed' });
  }

  const marca = normalize(String((req.query && req.query.m) || ''), 80);
  if (marca.length < 2) {
    res.setHeader('Cache-Control', 'no-store');
    res.statusCode = 400;
    return res.json({ ok: false, error: 'missing_brand', message: 'Informe o nome da marca.' });
  }

  // Segmento e opcional na API (links antigos sem ele continuam funcionando); o formulario do totem exige.
  const segmento = normalize(String((req.query && req.query.s) || ''), 60);

  // @ do Instagram da marca (opcional): so o handle limpo vai para a busca.
  const instagram = limparPerfil(req.query && req.query.i);

  const vistos = new Set([marca.toLowerCase()]);
  const informados = [];
  for (const bruto of paraLista(req.query && req.query.c)) {
    const nome = normalize(String(bruto || ''), 60);
    if (nome.length < 2 || vistos.has(nome.toLowerCase())) continue;
    vistos.add(nome.toLowerCase());
    informados.push(nome);
    if (informados.length === 3) break;
  }

  // URL canonica: a borda guarda a resposta por URL, entao parametro a mais (&x=1), c a mais ou valor "sujo" (@Natura, espaco
  // duplo) geraria uma analise nova (IA + Trends) para o mesmo pedido. Esses casos sao redirecionados para a forma limpa, que
  // e a unica que roda a analise e fica no cache.
  // A comparacao e feita pelos VALORES ja decodificados (req.query), nunca pelo texto da URL: a Vercel entrega req.url com
  // outra codificacao (%20 no lugar de +) e uma comparacao de texto nunca bateria, o que causou um laco de redirecionamento
  // em producao (2026-10-20). A forma limpa so tem chaves permitidas e valores ja normalizados, entao nunca redireciona de novo.
  const debug = Boolean(req.query && req.query.debug === '1' && debugPermitido(req));
  const q = req.query || {};
  const permitidas = new Set(['m', 's', 'i', 'c', ...(debug ? ['debug'] : [])]);
  const brutosC = paraLista(q.c);
  const suja = Object.keys(q).some((k) => !permitidas.has(k))
    || q.m !== marca
    || (q.s === undefined ? '' : String(q.s)) !== segmento
    || (q.i === undefined ? '' : String(q.i)) !== instagram
    || brutosC.length !== informados.length
    || brutosC.some((c, k) => c !== informados[k]);
  if (suja) {
    const canonica = new URLSearchParams();
    canonica.set('m', marca);
    if (segmento) canonica.set('s', segmento);
    if (instagram) canonica.set('i', instagram);
    informados.forEach((c) => canonica.append('c', c));
    if (debug) canonica.set('debug', '1');
    res.statusCode = 308;
    res.setHeader('Location', `/api/totem?${canonica.toString()}`);
    res.setHeader('Cache-Control', 'public, max-age=0, s-maxage=86400');
    return res.end();
  }

  try {
    const resultado = await analisar({ marca, segmento, informados, instagram, debug });
    // Cache so na borda (s-maxage): max-age=0 faz o navegador sempre perguntar a borda. Sem isso (ou com
    // stale-while-revalidate) o navegador serve uma copia velha, e o totem mostraria resultado desatualizado.
    res.setHeader('Cache-Control', 'public, max-age=0, s-maxage=86400');
    res.statusCode = 200;
    return res.json(resultado);
  } catch (err) {
    console.error('[buzz-radar-totem] analise falhou', err && err.message ? err.message : err);
    res.setHeader('Cache-Control', 'no-store');
    res.statusCode = 502;
    return res.json({ ok: false, error: 'analysis_failed', message: 'Nao foi possivel consultar a Trends agora.' });
  }
};
