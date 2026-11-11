// Helpers compartilhados do totem (api/totem.js e api/totem-lead.js) para falar com a Buzzmonitor Trends (guest).
// A pasta _lib nao vira rota da Vercel (prefixo "_"). A api/radar.js (LP original) continua autocontida de proposito.
//
// Sintaxe da busca (testada na API guest em 2026-10-16, ver SCORING.md):
//   - OR entre termos, aspas para frase exata, parenteses so para agrupar termos ligados por OR
//   - "-termo" exclui, "#hashtag" e "@perfil" funcionam como termos comuns
//   - palavras separadas por espaco, sem aspas, exigem que TODAS aparecam no post (E implicito)
//   - AND, NOT, && e & NAO sao operadores: viram palavra literal e zeram o resultado

const { AsyncLocalStorage } = require('node:async_hooks');

const BM_API_BASE = 'https://api.buzzmonitor.com.br';

// Fuso da analise em curso (horas em relacao a UTC). Cada analise roda dentro de comFuso(), entao duas analises
// simultaneas na mesma instancia (paises diferentes) nao se misturam. Fora de comFuso() vale -6 (Cidade do Mexico).
const contexto = new AsyncLocalStorage();
function fusoAtual() {
  const store = contexto.getStore();
  return store && Number.isFinite(store.fuso) ? store.fuso : -6;
}
function comFuso(fuso, fn) {
  return contexto.run({ fuso }, fn);
}

// Credencial "guest" da ferramenta gratuita publica (trends.app.buzzmonitor.com.br). Mesma da api/radar.js.
// Nao e API oficial documentada para este uso: validar limite com engenharia antes de escalar trafego.
const BM_GUEST_AUTH = {
  bm_user: 'guest',
  api_key: process.env.BM_GUEST_API_KEY || 'MfcySfJ4jw8Wj3bSlxExD4UEnpDoiAfVDfhjlRdsdafk1g2cDw',
};

function normalize(value, max) {
  if (typeof value !== 'string') return '';
  return value.replace(/\s+/g, ' ').trim().slice(0, max).trim(); // aparar de novo: o corte pode deixar espaco no fim
}

function bmDate(d) {
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getUTCFullYear()}${p(d.getUTCMonth() + 1)}${p(d.getUTCDate())}${p(d.getUTCHours())}${p(d.getUTCMinutes())}${p(d.getUTCSeconds())}`;
}

async function fetchWithTimeout(url, opts, ms) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ms);
  try {
    return await fetch(url, { ...opts, signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

// Versao LATAM: idioma es (a Trends nao filtra por pais, entao entra Mexico, resto da America Latina e Espanha) e fuso do pais escolhido (padrao -6, Cidade do Mexico). Barra falso positivo em ingles e portugues. Para volume, service vazio = todas as redes.
// O endpoint de posts responde 500 com service vazio (testado em 2026-10-16): precisa da lista explicita.
const SERVICES_POSTS = ['facebook', 'instagram', 'misc', 'twitter'];

function generalParams(query, since, until, service = []) {
  return { since, until, language: ['es'], timezone: fusoAtual().toFixed(1), service, query };
}

// Erro passageiro (rede, timeout, 5xx) merece uma segunda tentativa; 4xx (query invalida) nao: repetir nao muda nada.
const erroDefinitivo = (err) => /_4\d\d$/.test(String((err && err.message) || ''));
async function comRetry(fn) {
  try {
    return await fn();
  } catch (err) {
    if (erroDefinitivo(err)) throw err;
    await new Promise((r) => setTimeout(r, 350));
    return fn();
  }
}

function bmVolume(query, grouping, since, until) {
  return comRetry(async () => {
    const r = await fetchWithTimeout(`${BM_API_BASE}/historical_volume.json`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ authentication_params: BM_GUEST_AUTH, general_params: generalParams(query, since, until), grouping }),
    }, 12000);
    if (!r.ok) throw new Error(`bm_volume_${r.status}`);
    return r.json();
  });
}

// sort: 'top_posts_field' (mais engajados, para exibir) ou 'random' (amostra representativa do periodo, o certo para
// achar temas: a skill de buscas usa random para montar base).
function bmPosts(query, since, until, size, sort = 'top_posts_field', servicos = SERVICES_POSTS) {
  return comRetry(async () => {
    const r = await fetchWithTimeout(`${BM_API_BASE}/historical_posts.json`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ authentication_params: BM_GUEST_AUTH, general_params: generalParams(query, since, until, servicos), sort_by: sort, size }),
    }, 12000);
    if (!r.ok) throw new Error(`bm_posts_${r.status}`);
    return r.json();
  });
}

// Perfis influentes ligados a uma palavra. A busca so responde a UMA palavra (frase composta e OR devolvem 0).
// paises: lista JSON de codigos ISO (ex.: '["CO"]'). Diferente dos posts, aqui o filtro por pais funciona (testado em 2026-11-10).
async function bmInfluencers(palavra, idiomas = '[]', paises = '[]') {
  const qs = new URLSearchParams({
    searchFor: `""${palavra}""`,
    socialNetworks: '["instagram", "facebook", "youtube"]',
    whereToSearch: '["username", "name", "top_hashtags", "top_terms", "top_entities", "top_mentions", "bio"]',
    min_followers: '1000',
    max_followers: '100000000',
    gender: '["M", "F", "ORG"]',
    'languages[]': idiomas,
    age: '[]',
    page: '0',
    countries: paises,
    interests: '[]',
  });
  const r = await fetchWithTimeout(`https://crawler.influencers.buzzmonitor.com.br/influencers/search?${qs.toString()}`, {
    headers: { Accept: 'application/json' },
  }, 12000);
  if (!r.ok) throw new Error(`bm_influencers_${r.status}`);
  return r.json();
}

// Procura o perfil do Instagram pelo @ (username). A resposta traz nome, seguidores e tipo (ORG = empresa), mas nao o
// username: a busca e aproximada (avonbrasil trouxe tambem uma pessoa), entao quem chama confere o nome. Perfil fora da
// base devolve lista vazia: isso nao prova que o @ esta errado.
async function bmPerfilInstagram(handle) {
  const qs = new URLSearchParams({
    searchFor: `""${handle}""`,
    socialNetworks: '["instagram"]',
    whereToSearch: '["username"]',
    min_followers: '1000',
    max_followers: '100000000',
    gender: '["M", "F", "ORG"]',
    'languages[]': '[]',
    age: '[]',
    page: '0',
    countries: '[]',
    interests: '[]',
  });
  const r = await fetchWithTimeout(`https://crawler.influencers.buzzmonitor.com.br/influencers/search?${qs.toString()}`, {
    headers: { Accept: 'application/json' },
  }, 8000);
  if (!r.ok) throw new Error(`bm_perfil_${r.status}`);
  return r.json();
}

// Executa tarefas (funcoes que devolvem promise) com no maximo `limite` em voo, sem nunca rejeitar:
// cada posicao devolve { ok, value } ou { ok:false, error }. Mantem a ordem das tarefas.
async function emLote(tarefas, limite) {
  const resultados = new Array(tarefas.length);
  let proximo = 0;
  async function worker() {
    while (proximo < tarefas.length) {
      const i = proximo++;
      try {
        resultados[i] = { ok: true, value: await tarefas[i]() };
      } catch (error) {
        resultados[i] = { ok: false, error };
      }
    }
  }
  await Promise.all(Array.from({ length: Math.min(limite, tarefas.length) }, worker));
  return resultados;
}

module.exports = { fusoAtual, comFuso, BM_GUEST_AUTH, normalize, bmDate, fetchWithTimeout, bmVolume, bmPosts, bmInfluencers, bmPerfilInstagram, emLote };
