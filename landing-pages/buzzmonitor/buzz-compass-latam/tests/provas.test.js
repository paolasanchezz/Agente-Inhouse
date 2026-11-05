// Testes da escolha dos posts da marca:  node landing-pages/buzzmonitor/buzz-compass-latam/tests/provas.test.js
const assert = require('assert');
const { escolherPostsDaMarca, lerMeta, previaDoSite } = require('../api/_lib/analise.js');

const post = (service, link, autor, texto, likes, extra = {}) => ({ service, link, author: { name: autor }, text: texto, likes, shares: 0, comments_amounts: 0, date: '20261019120000', ...extra });
// X e sites chegam com o endereco no campo "url" (nao em "link")
const postUrl = (service, url, autor, texto, likes, extra = {}) => ({ service, url, link: null, author: { name: autor }, text: texto, likes, date: '20261019120000', ...extra });
const ok = (posts) => ({ ok: true, value: { posts } });

const ig = ok([
  post('instagram', 'https://www.instagram.com/reel/AAA111/', 'Havaianas', 'Nova coleção Havaianas', 9000),
  post('instagram', 'https://www.instagram.com/p/BBB222/', 'Helô Gomes', 'Meu chinelo Havaianas favorito', 3000),
  post('instagram', 'https://www.instagram.com/p/CCC333/', 'Outra Pessoa', 'Viagem incrível, nada sobre a marca', 50000), // nao fala da marca
  post('instagram', 'https://www.instagram.com/havaianas/', 'Havaianas', 'Havaianas', 99999), // perfil, nao e post
]);
const fb = ok([
  post('facebook', 'https://www.facebook.com/123/posts/456', 'Shopping Norte', 'Chegou Havaianas aqui', 20),
  post('facebook', 'https://www.facebook.com/reel/789/', 'Meio e Mensagem', 'Havaianas lança campanha', 40),
]);
const x = ok([
  postUrl('twitter', 'http://twitter.com/ana/statuses/2102857232257802297', 'Ana', 'Fui na loja da havaianas hoje https://t.co/abc123', 44, { picture_full_size: 'https://pbs.twimg.com/media/foto.jpg' }),
  postUrl('twitter', 'http://twitter.com/promo/statuses/2105670737612988678', 'promo out of context', 'HAVAIANAS DUAL por R$ 45 https://t.co/xyz', 1, { picture_full_size: 'https://video.twimg.com/tweet_video/v.mp4' }),
  postUrl('twitter', 'https://x.com/marca', 'Perfil', 'Havaianas', 500), // perfil, nao e post
]);
const sites = ok([
  postUrl('blogs', 'https://www.nit.pt/compras/havaianas-mules', 'NiT', 'A marca brasileira Havaianas lança mules fechadas', 0),
  postUrl('news', 'https://exemplo.com/outra', 'Jornal', 'Notícia sobre outro assunto', 0), // nao fala da marca
  postUrl('blogs', 'ftp://exemplo.com/x', 'Estranho', 'Havaianas', 0), // protocolo invalido
]);

let r = escolherPostsDaMarca([ig, fb, x, sites], 'Havaianas', 'havaianas');
assert(r.length <= 6, 'ate 6 posts');
assert(r.length >= 4, 'pelo menos um de cada rede: ' + r.map((p) => p.rede));
['instagram', 'facebook', 'x', 'site'].forEach((rede) => assert(r.some((p) => p.rede === rede), 'tem ' + rede));
assert(!r.some((p) => p.autor === 'Outra Pessoa' || p.autor === 'Jornal'), 'post que nao fala da marca fica de fora');
assert(!r.some((p) => /instagram\.com\/havaianas\/$|x\.com\/marca$/.test(p.link)), 'perfil nao e post');
assert(!r.some((p) => p.autor === 'Estranho'), 'protocolo invalido fica de fora');
assert(r.every((p) => /^https?:\/\//.test(p.link)));
const tweet = r.find((p) => p.rede === 'x' && p.autor === 'Ana');
assert(tweet && !/t\.co|https?:/.test(tweet.texto), 'URL some do texto de X e sites: ' + (tweet && tweet.texto));
assert.strictEqual(tweet.imagem, 'https://pbs.twimg.com/media/foto.jpg', 'foto do post de X vira imagem do cartao');
const promo = r.find((p) => p.autor === 'promo out of context');
if (promo) assert.strictEqual(promo.imagem, null, 'video nao vira imagem');
assert(r.filter((p) => p.rede === 'instagram' || p.rede === 'facebook').every((p) => p.imagem === null), 'quadro oficial dispensa imagem');
assert.strictEqual(r.filter((p) => p.propria).length, r.filter((p) => p.autor === 'Havaianas').length, 'perfil da propria marca e marcado');
const ordem = r.map((p) => p.interacoes);
assert.deepStrictEqual(ordem, ordem.slice().sort((a, b) => b - a), 'saem do mais para o menos engajado');

// quem fala de fora entra antes do perfil da marca quando a lista aperta
const muitos = ok(['A', 'B', 'C', 'D', 'E', 'F', 'G'].map((n, i) => post('instagram', `https://www.instagram.com/p/ZZ${i}/`, 'Pessoa ' + n, 'Havaianas', 10 + i)));
const proprio = ok([post('instagram', 'https://www.instagram.com/reel/PROP/', 'Havaianas', 'Havaianas', 99999)]);
const so = escolherPostsDaMarca([muitos, proprio], 'Havaianas', 'havaianas');
assert.strictEqual(so.length, 2, 'no maximo 2 posts por rede');
assert(!so.some((p) => p.propria), 'com posts de fora de sobra, o da propria marca nao entra');

// falhas e listas vazias nao quebram
assert.deepStrictEqual(escolherPostsDaMarca([{ ok: false }, null, ok([])], 'X', 'xxxx'), []);
// sem ficha (nome curto demais), nao filtra por texto mas segue exigindo endereco valido
assert(escolherPostsDaMarca([ig], 'Oi', null).every((p) => /instagram\.com\/(p|reel)\//.test(p.link)));

// previa do link: meta tags (og e twitter), entidades decodificadas, aspas simples e duplas
const m = lerMeta(`<head><title>Titulo da aba</title>
  <meta property="og:title" content="Havaianas lan&ccedil;a mules &amp; novidades">
  <meta property='og:description' content='Marca "brasileira" volta ao outono'>
  <meta name="twitter:image" content="/img/capa.jpg"><meta property="og:site_name" content="NiT"></head>`);
assert.strictEqual(m.site, 'NiT');
assert.strictEqual(m.titulo, 'Havaianas lan&ccedil;a mules & novidades', 'decodifica o basico (&amp;); entidade rara fica como esta');
assert.strictEqual(m.descricao, 'Marca "brasileira" volta ao outono');
assert.strictEqual(m.imagem, '/img/capa.jpg');
assert.strictEqual(lerMeta('<head><title>So titulo</title></head>').titulo, 'So titulo');
assert.deepStrictEqual(lerMeta('').titulo, null);

(async () => {
  // nunca busca endereco interno nem protocolo estranho
  global.fetch = async () => { throw new Error('nao deveria buscar'); };
  for (const url of ['http://localhost:3000/x', 'http://127.0.0.1/x', 'http://192.168.0.10/', 'http://[::1]/', 'http://servidor/x', 'ftp://exemplo.com/x', 'file:///etc/passwd', 'texto-solto']) {
    assert.strictEqual(await previaDoSite(url), null, 'nao busca: ' + url);
  }
  // site normal: usa meta, resolve imagem relativa contra a URL final, ignora imagem http
  global.fetch = async () => ({
    ok: true, url: 'https://www.exemplo.com/post/1', headers: { get: () => 'text/html; charset=utf-8' },
    text: async () => '<html><head><meta property="og:title" content="Titulo"><meta property="og:image" content="/capa.jpg"></head><body>corpo</body></html>',
  });
  let pv = await previaDoSite('https://www.exemplo.com/post/1');
  assert.strictEqual(pv.titulo, 'Titulo');
  assert.strictEqual(pv.imagem, 'https://www.exemplo.com/capa.jpg');
  assert.strictEqual(pv.site, 'exemplo.com', 'sem og:site_name usa o dominio');
  global.fetch = async () => ({ ok: true, url: 'https://x.com/a', headers: { get: () => 'text/html' }, text: async () => '<head><meta property="og:title" content="T"><meta property="og:image" content="http://inseguro.com/a.jpg"></head>' });
  assert.strictEqual((await previaDoSite('https://x.com/a')).imagem, null, 'imagem http nao entra');
  // falha, nao-HTML e pagina sem meta: nulo, nunca erro
  global.fetch = async () => ({ ok: false, headers: { get: () => 'text/html' }, text: async () => '' });
  assert.strictEqual(await previaDoSite('https://exemplo.com/'), null);
  global.fetch = async () => ({ ok: true, headers: { get: () => 'application/pdf' }, text: async () => '%PDF' });
  assert.strictEqual(await previaDoSite('https://exemplo.com/a.pdf'), null);
  global.fetch = async () => { throw new Error('rede'); };
  assert.strictEqual(await previaDoSite('https://exemplo.com/'), null);
  console.log('provas.test.js: ok');
})().catch((e) => { console.error(e); process.exit(1); });
