// Buzz Compass: pipeline: form do lead -> Buzzmonitor Trends (guest) -> scores deterministicos -> IA (narrativa) -> JSON.
// Ver landing-pages/buzzmonitor/buzz-radar/README.md e SCORING.md para o racional completo.

const BM_API_BASE = 'https://api.buzzmonitor.com.br';
const BM_INFLUENCERS_BASE = 'https://crawler.influencers.buzzmonitor.com.br';

// Credencial "guest" da propria ferramenta gratuita publica da Buzzmonitor
// (trends.app.buzzmonitor.com.br), capturada via inspecao de rede em 2026-09-02: o mesmo
// acesso anonimo que qualquer visitante daquele site ja tem, sem login. Nao e uma API oficial
// documentada para este uso: antes de escalar trafego pago sobre isto, validar limite de uso
// com engenharia. Nunca expor esta chave em material de pitch/slides.
const BM_GUEST_AUTH = {
  bm_user: 'guest',
  api_key: 'MfcySfJ4jw8Wj3bSlxExD4UEnpDoiAfVDfhjlRdsdafk1g2cDw',
};

const OPENAI_URL = 'https://api.openai.com/v1/chat/completions';
const ANTHROPIC_URL = 'https://api.anthropic.com/v1/messages';
const ANTHROPIC_VERSION = '2023-06-01';

const SEGMENTOS_VALIDOS = new Set([
  'cosmeticos', 'moda', 'ecommerce', 'alimentacao', 'fintech', 'seguros',
  'educacao', 'saude', 'imobiliario', 'turismo', 'automotivo', 'telecom',
  'tecnologia', 'agencias de marketing', 'ongs',
]);

function normalize(value, max) {
  if (typeof value !== 'string') return '';
  return value.trim().slice(0, max);
}

function isValidEmail(value) {
  return typeof value === 'string' && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
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

async function bmVolume(query, grouping, services, since, until) {
  const body = {
    authentication_params: BM_GUEST_AUTH,
    general_params: { since, until, language: [], timezone: '-3.0', service: services, query },
    grouping,
  };
  const r = await fetchWithTimeout(`${BM_API_BASE}/historical_volume.json`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify(body),
  }, 8000);
  if (!r.ok) throw new Error(`bm_volume_${r.status}`);
  return r.json();
}

async function bmPosts(query, services, since, until, size) {
  const body = {
    authentication_params: BM_GUEST_AUTH,
    general_params: { since, until, language: [], timezone: '-3.0', service: services, query },
    sort_by: 'top_posts_field',
    size,
  };
  const r = await fetchWithTimeout(`${BM_API_BASE}/historical_posts.json`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify(body),
  }, 8000);
  if (!r.ok) throw new Error(`bm_posts_${r.status}`);
  return r.json();
}

async function bmInfluencers(query) {
  const qs = new URLSearchParams({
    searchFor: `""${query}""`,
    socialNetworks: '["instagram", "facebook", "youtube"]',
    whereToSearch: '["username", "name", "top_hashtags", "top_terms", "top_entities", "top_mentions", "bio"]',
    min_followers: '1000',
    max_followers: '100000000',
    gender: '["M", "F", "ORG"]',
    'languages[]': '[]',
    age: '[]',
    page: '0',
    countries: '[]',
    interests: '[]',
  });
  const r = await fetchWithTimeout(`${BM_INFLUENCERS_BASE}/influencers/search?${qs.toString()}`, {
    headers: { Accept: 'application/json' },
  }, 8000);
  if (!r.ok) throw new Error(`bm_influencers_${r.status}`);
  return r.json();
}

// --- Scores deterministicos (nunca vem do modelo de IA: ver SCORING.md) ---

function volumeScore(total) {
  const buckets = [[50, 15], [200, 30], [1000, 50], [5000, 70], [20000, 85], [Infinity, 97]];
  for (const [limite, score] of buckets) if (total <= limite) return score;
  return 97;
}

function sentimentoScore(positivos, negativos) {
  if (positivos + negativos === 0) return 50;
  return Math.round((positivos / (positivos + negativos)) * 100);
}

function momentumScore(serieDiaria) {
  if (!Array.isArray(serieDiaria) || serieDiaria.length < 14) return 50;
  const ultimos7 = serieDiaria.slice(-7).reduce((s, d) => s + d.value, 0);
  const anteriores7 = serieDiaria.slice(-14, -7).reduce((s, d) => s + d.value, 0);
  if (anteriores7 === 0) return ultimos7 > 0 ? 75 : 50;
  const crescimentoPct = (ultimos7 - anteriores7) / anteriores7;
  return Math.round(50 + Math.max(-50, Math.min(50, crescimentoPct * 100)));
}

function diversidadeTemasScore(termsData) {
  if (!Array.isArray(termsData) || termsData.length < 3) return 50;
  const total = termsData.reduce((s, t) => s + (t.value || 0), 0) || 1;
  const ordenado = termsData.slice().sort((a, b) => (b.value || 0) - (a.value || 0));
  const top3Share = ordenado.slice(0, 3).reduce((s, t) => s + (t.value || 0), 0) / total;
  // Quanto MENOR a concentracao nos 3 termos principais, mais diversificada e a conversa.
  // Faixa calibrada observando varios segmentos reais: concentracao entre ~25% (bem diverso)
  // e ~45% (bem concentrado, tipicamente quando o proprio termo buscado domina o volume).
  const score = 100 - Math.round(((top3Share - 0.25) / 0.20) * 100);
  return Math.max(0, Math.min(100, score));
}

function radarScoreFinal(scores) {
  return Math.round(
    scores.presenca * 0.25 + scores.sentimento * 0.25 + scores.oportunidades * 0.30 + scores.diversidade_temas * 0.20
  );
}

// --- Narrativa (IA escreve texto em cima dos numeros ja calculados acima; OpenAI ou Anthropic, o que estiver configurado e funcionando) ---

const NARRATIVE_SCHEMA = {
  type: 'object',
  properties: {
    oportunidade: {
      type: 'object',
      properties: { titulo: { type: 'string' }, texto: { type: 'string' } },
      required: ['titulo', 'texto'],
      additionalProperties: false,
    },
    risco: {
      type: 'object',
      properties: { titulo: { type: 'string' }, texto: { type: 'string' } },
      required: ['titulo', 'texto'],
      additionalProperties: false,
    },
    espaco_competitivo: {
      type: 'object',
      properties: { titulo: { type: 'string' }, texto: { type: 'string' } },
      required: ['titulo', 'texto'],
      additionalProperties: false,
    },
    tendencia_emergente: {
      type: 'object',
      properties: { titulo: { type: 'string' }, texto: { type: 'string' } },
      required: ['titulo', 'texto'],
      additionalProperties: false,
    },
    cta_texto: { type: 'string' },
  },
  required: ['oportunidade', 'risco', 'espaco_competitivo', 'tendencia_emergente', 'cta_texto'],
  additionalProperties: false,
};

const SYSTEM_PROMPT = `Voce e a analista de inteligencia de mercado por tras do Buzz Compass, uma ferramenta da Buzzmonitor.
Tom de voz: profissional, acessivel, orientado a dados, com energia e clareza. Nunca use "revolucionario", "disruptivo" ou hype vazio. Nunca sugira que a inteligencia artificial substitui pessoas. A marca e sempre feminina: "a Buzzmonitor" (nunca "o Buzzmonitor").
Personalizacao obrigatoria: em todos os cards, toda vez que for se referir a empresa do lead, use o nome real dela (campo "empresa"), nunca "sua empresa" ou "sua marca" generico.
Regra inegociavel: use apenas os numeros do payload de dados que voce recebe. Nunca invente estatistica, nunca cite numero ou fonte que nao esteja no payload.
Se "empresa_mencoes" for zero ou muito baixo, isso nao e um erro de busca, mas tambem nao e prova de que a marca nao e comentada em lugar nenhum: a busca roda sobre uma base de dados limitada (projetos ja monitorados por clientes da Buzzmonitor), nao a internet inteira em tempo real. Enquadre assim: "a marca ainda nao aparece na nossa base de monitoramento" (nunca como certeza absoluta de ausencia), e trate isso como UM angulo possivel (risco de baixa visibilidade monitorada + espaco em branco pra ocupar) dentro do card de risco, nunca como o unico assunto do card nem da narrativa inteira. O objetivo do Buzz Compass e diagnosticar o MERCADO, nao so a presenca da marca do lead.
O card "risco" precisa trazer riscos REAIS do mercado, nao só a questao de visibilidade da marca. Use "exemplos_conteudo_negativo" (posts reais com sentimento negativo, sem nome de quem postou) pra identificar temas/assuntos concretos gerando sentimento negativo no segmento agora, e traga isso como o risco principal quando houver material suficiente. A questao de visibilidade da marca (paragrafo acima) pode aparecer como um segundo ponto do card, mas nunca sozinha.
O card "oportunidade" espelha a mesma logica do risco, ao contrario: use "exemplos_conteudo_positivo" (posts reais com sentimento positivo, sem nome de quem postou) pra identificar temas/assuntos concretos gerando sentimento positivo agora, em vez de descrever oportunidade so como "o volume esta crescendo".
Use "termos_mais_citados" para ancorar a leitura no que o mercado esta genuinamente discutindo: cite pelo menos 2 ou 3 desses termos, especialmente no card de espaco_competitivo, conectando-os com o volume, o sentimento e os exemplos de posts. Esses termos sao o retrato mais rico do payload: priorize-os sobre repetir o mesmo argumento de "a marca nao aparece" em varios cards.
"termos_emergentes_2a_quinzena" e diferente de "termos_mais_citados": sao termos que cresceram proporcionalmente da primeira pra segunda metade do periodo, ou seja, o que e genuinamente NOVO na conversa (nao so grande o mes inteiro). Use essa lista especificamente no card "tendencia_emergente" (pode vir vazia se nada emergiu de forma clara; nesse caso, use termos_mais_citados como no anterior).
Se "dados_parciais" for true, seja mais cauteloso nas afirmacoes (a leitura desta rodada ficou incompleta).
Nunca use a palavra "momentum" (jargao em ingles, confunde o leitor leigo). Use "ritmo de crescimento" ou "variacao de volume" no lugar, mesmo que o payload traga o campo "ritmo_crescimento_pct".
Use "tendencia_sentimento_pp" para dizer se a conversa esta melhorando ou piorando dentro do proprio periodo (positivo = sentimento subindo, negativo = caindo), como sinal distinto do ritmo de crescimento (que mede volume, nao qualidade da conversa).
"conteudos_que_performaram_bem" traz o tipo (foto, video, etc), engajamento e um resumo curto dos posts com mais alcance do segmento. Use isso pra comentar que FORMATO de conteudo esta funcionando bem (ex.: "posts em video estao performando melhor que foto"). Regra dura: NUNCA cite nome de pessoa, pagina, perfil ou marca que aparece nos dados de posts ou de influenciadores, mesmo que o payload traga esse nome em algum campo. Fale de formato e tema, nunca de quem postou.
Escreva em portugues do Brasil, direto, sem cliches de texto generico, sem em-dash. Cada card tem 2 a 4 frases, cita pelo menos um numero real do payload quando fizer sentido, e fecha com uma implicacao pratica para quem decide marketing.`;

async function gerarNarrativaOpenAI(payload, apiKey) {
  const model = process.env.OPENAI_MODEL || 'gpt-4o-mini';
  const resp = await fetchWithTimeout(OPENAI_URL, {
    method: 'POST',
    headers: { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model,
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: JSON.stringify(payload) },
      ],
      response_format: { type: 'json_schema', json_schema: { name: 'buzz_radar_output', strict: true, schema: NARRATIVE_SCHEMA } },
      temperature: 0.7,
      max_tokens: 900,
    }),
  }, 20000);

  if (!resp.ok) {
    throw new Error(`openai_${resp.status}: ${await resp.text().catch(() => '')}`);
  }
  const data = await resp.json();
  return JSON.parse(data.choices[0].message.content);
}

async function gerarNarrativaAnthropic(payload, apiKey) {
  const model = process.env.ANTHROPIC_MODEL || 'claude-sonnet-5';
  const resp = await fetchWithTimeout(ANTHROPIC_URL, {
    method: 'POST',
    headers: {
      'x-api-key': apiKey,
      'anthropic-version': ANTHROPIC_VERSION,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model,
      max_tokens: 900,
      system: SYSTEM_PROMPT,
      messages: [{ role: 'user', content: JSON.stringify(payload) }],
      tools: [{
        name: 'gerar_radar_narrativa',
        description: 'Gera a narrativa estruturada do Buzz Compass a partir dos dados fornecidos.',
        input_schema: NARRATIVE_SCHEMA,
      }],
      tool_choice: { type: 'tool', name: 'gerar_radar_narrativa' },
    }),
  }, 20000);

  if (!resp.ok) {
    throw new Error(`anthropic_${resp.status}: ${await resp.text().catch(() => '')}`);
  }
  const data = await resp.json();
  const toolUse = (data.content || []).find((block) => block.type === 'tool_use');
  if (!toolUse) throw new Error('anthropic_no_tool_use');
  return toolUse.input;
}

// Tenta os provedores configurados em ordem ate um funcionar. Existe pra nao depender de um
// unico provedor estar com credito/disponivel no momento da demo (ja aconteceu na pratica).
async function gerarNarrativa(payload) {
  const tentativas = [
    process.env.OPENAI_API_KEY && (() => gerarNarrativaOpenAI(payload, process.env.OPENAI_API_KEY)),
    process.env.ANTHROPIC_API_KEY && (() => gerarNarrativaAnthropic(payload, process.env.ANTHROPIC_API_KEY)),
  ].filter(Boolean);

  for (const tentar of tentativas) {
    try {
      return await tentar();
    } catch (err) {
      console.error('[buzz-radar] provedor de IA falhou, tentando proximo (se houver)', err.message || err);
    }
  }
  return null;
}

// --- ActiveCampaign (opcional, desligado por padrao: ver README.md) ---

async function syncActiveCampaign({ email, nome, empresa, cargo, segmento, radarScore }) {
  const base = process.env.ACTIVECAMPAIGN_API_URL;
  const token = process.env.ACTIVECAMPAIGN_API_TOKEN;
  if (!base || !token || !email) return;

  try {
    const syncRes = await fetchWithTimeout(`${base}/api/3/contact/sync`, {
      method: 'POST',
      headers: { 'Api-Token': token, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contact: { email, firstName: nome, orgname: empresa, fieldValues: [] },
      }),
    }, 5000);
    if (!syncRes.ok) throw new Error(`ac_sync_${syncRes.status}`);
    const syncData = await syncRes.json();
    const contactId = syncData && syncData.contact && syncData.contact.id;

    const tagId = process.env.ACTIVECAMPAIGN_TAG_ID;
    if (contactId && tagId) {
      await fetchWithTimeout(`${base}/api/3/contactTags`, {
        method: 'POST',
        headers: { 'Api-Token': token, 'Content-Type': 'application/json' },
        body: JSON.stringify({ contactTag: { contact: contactId, tag: tagId } }),
      }, 5000);
    }
  } catch (err) {
    // Nunca deixa a captura de CRM derrubar a resposta pro lead.
    console.error('[buzz-radar] activecampaign sync falhou (ignorado)', err);
  }
}

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');

  if (req.method !== 'POST') {
    res.statusCode = 405;
    return res.json({ ok: false, error: 'method_not_allowed' });
  }

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch (_) { body = null; }
  }
  if (!body || typeof body !== 'object') {
    res.statusCode = 400;
    return res.json({ ok: false, error: 'invalid_payload' });
  }

  // Honeypot: bot preenche, humano nao ve (campo escondido via CSS no form).
  if (typeof body._hp === 'string' && body._hp.trim().length > 0) {
    res.statusCode = 200;
    return res.json({ ok: true, honeypot: true });
  }
  // Submit em menos de 2s do form renderizado = quase certamente script, nao humano lendo o form.
  const renderedAt = Number(body._ts);
  if (Number.isFinite(renderedAt) && Date.now() - renderedAt < 2000) {
    res.statusCode = 200;
    return res.json({ ok: true, honeypot: true });
  }

  const nome = normalize(body.nome, 100);
  const empresa = normalize(body.empresa, 150);
  const site = normalize(body.site, 200);
  const segmentoRaw = normalize(body.segmento, 100);
  const segmento = SEGMENTOS_VALIDOS.has(segmentoRaw) ? segmentoRaw : normalize(body.segmento_outro, 80);
  const cargo = normalize(body.cargo, 100);
  const email = normalize(body.email, 200).toLowerCase();

  if (!nome || !empresa || !segmento || !cargo || !email) {
    res.statusCode = 400;
    return res.json({ ok: false, error: 'missing_fields', message: 'Preencha nome, empresa, segmento, cargo e e-mail.' });
  }
  if (!isValidEmail(email)) {
    res.statusCode = 400;
    return res.json({ ok: false, error: 'invalid_email', message: 'E-mail invalido.' });
  }

  const until = new Date();
  const since = new Date(until.getTime() - 30 * 24 * 60 * 60 * 1000);
  const meio = new Date(since.getTime() + 15 * 24 * 60 * 60 * 1000);
  const sinceStr = bmDate(since);
  const untilStr = bmDate(until);
  const meioStr = bmDate(meio);
  const services = ['facebook', 'instagram', 'misc'];

  const [
    sentimentRes, serviceRes, dailyRes, termsRes, postsRes, influencersRes, empresaRes,
    sentimentPrimeiraMetadeRes, sentimentSegundaMetadeRes,
    termosPrimeiraMetadeRes, termosSegundaMetadeRes, genderRes,
  ] = await Promise.allSettled([
    bmVolume(segmento, 'sentiment', services, sinceStr, untilStr),
    bmVolume(segmento, 'service', services, sinceStr, untilStr),
    bmVolume(segmento, 'period_daily', services, sinceStr, untilStr),
    bmVolume(segmento, 'term', services, sinceStr, untilStr),
    // size 50 (nao 5): a API nao filtra por sentimento no request (testado, ignorado), entao
    // buscamos um lote maior e filtramos POSITIVE/NEGATIVE no codigo. Na pratica a API limita
    // a resposta a ~30 itens independente do size pedido (testado com 50 em 2 segmentos).
    bmPosts(segmento, services, sinceStr, untilStr, 50),
    bmInfluencers(segmento),
    // Frase exata (aspas): nome de empresa com palavra comum (ex.: "Loja Teste") sem aspas
    // casa qualquer post que cite "loja" OU "teste" separadamente, inflando o volume.
    empresa ? bmVolume(`"${empresa}"`, 'sentiment', services, sinceStr, untilStr) : Promise.resolve(null),
    // Tendencia de sentimento: metade mais antiga vs metade mais recente do periodo de 30 dias.
    // Sinal distinto do "ritmo de crescimento" (que mede volume, nao qualidade da conversa).
    bmVolume(segmento, 'sentiment', services, sinceStr, meioStr),
    bmVolume(segmento, 'sentiment', services, meioStr, untilStr),
    // Termos emergentes: comparar as duas metades pra achar o que e NOVO na conversa, nao so
    // o que e grande no mes inteiro (termos_mais_citados mistura os dois).
    bmVolume(segmento, 'term', services, sinceStr, meioStr),
    bmVolume(segmento, 'term', services, meioStr, untilStr),
    bmVolume(segmento, 'gender', services, sinceStr, untilStr),
  ]);

  const dadosParciais = [sentimentRes, serviceRes, dailyRes, termsRes, postsRes, influencersRes].some((r) => r.status === 'rejected');

  const sentimentData = sentimentRes.status === 'fulfilled' ? sentimentRes.value.data || [] : [];
  const positivos = sentimentData.find((d) => d.label === 'positive')?.value || 0;
  const negativos = sentimentData.find((d) => d.label === 'negative')?.value || 0;
  const neutros = sentimentData.find((d) => d.label === 'neutral')?.value || 0;
  const volumeTotal = positivos + negativos + neutros;

  const pctPositivo = (arr) => {
    const pos = arr.find((d) => d.label === 'positive')?.value || 0;
    const neg = arr.find((d) => d.label === 'negative')?.value || 0;
    return pos + neg === 0 ? null : Math.round((pos / (pos + neg)) * 100);
  };
  const sentimentoPrimeiraMetade = sentimentPrimeiraMetadeRes.status === 'fulfilled' ? pctPositivo(sentimentPrimeiraMetadeRes.value.data || []) : null;
  const sentimentoSegundaMetade = sentimentSegundaMetadeRes.status === 'fulfilled' ? pctPositivo(sentimentSegundaMetadeRes.value.data || []) : null;
  const tendenciaSentimento = (sentimentoPrimeiraMetade !== null && sentimentoSegundaMetade !== null)
    ? sentimentoSegundaMetade - sentimentoPrimeiraMetade
    : null;

  const serviceData = serviceRes.status === 'fulfilled' ? serviceRes.value.data || [] : [];
  const canaisAtivos = serviceData.filter((d) => d.value > 0).length;

  const genderData = genderRes.status === 'fulfilled' ? genderRes.value.data || [] : [];

  const dailyData = dailyRes.status === 'fulfilled' ? (dailyRes.value.data || []).sort((a, b) => a.label.localeCompare(b.label)) : [];

  const termsData = termsRes.status === 'fulfilled'
    ? (termsRes.value.data || []).slice().sort((a, b) => b.value - a.value).slice(0, 20)
    : [];

  // Termos emergentes: o que cresceu proporcionalmente mais da 1a metade pra 2a metade do
  // periodo (termos_mais_citados acima mistura o mes inteiro e esconde o que e recente).
  const termosPrimeiraMetade = termosPrimeiraMetadeRes.status === 'fulfilled' ? (termosPrimeiraMetadeRes.value.data || []) : [];
  const termosSegundaMetade = termosSegundaMetadeRes.status === 'fulfilled' ? (termosSegundaMetadeRes.value.data || []) : [];
  const valorAnteriorPorTermo = new Map(termosPrimeiraMetade.map((t) => [t.label, t.value]));
  const termosEmergentes = termosSegundaMetade
    .filter((t) => t.value >= 15) // ignora termos com volume insignificante (ruido)
    .map((t) => {
      const antes = valorAnteriorPorTermo.get(t.label) || 0;
      const crescimento = antes === 0 ? Infinity : (t.value - antes) / antes;
      return { label: t.label, crescimento };
    })
    .filter((t) => t.crescimento > 0.3 || t.crescimento === Infinity) // so o que de fato cresceu
    .sort((a, b) => b.crescimento - a.crescimento)
    .slice(0, 8)
    .map((t) => t.label);

  const postsAll = postsRes.status === 'fulfilled' ? (postsRes.value.posts || postsRes.value.data || []) : [];
  const postsRaw = postsAll.slice(0, 5);
  // Sem nome de autor/pagina aqui de proposito: isso alimenta a narrativa da IA, que deve falar
  // de TIPO de conteudo que performou bem (formato, engajamento), nunca citar quem postou.
  const conteudosDestaque = postsRaw.map((p) => ({
    tipo: p.content_type || p.type || null,
    curtidas: p.likes || 0,
    compartilhamentos: p.shares || 0,
    resumo: normalize(p.text || p.content || '', 140),
  })).filter((p) => p.resumo);

  // Amostra de posts NEGATIVE/POSITIVE (a API nao filtra por sentimento no request; filtramos
  // aqui em cima de um lote maior) pra dar a IA temas reais de risco e oportunidade, alem da
  // presenca da marca e do volume bruto.
  const filtrarPorSentimento = (alvo) => postsAll
    .filter((p) => String(p.sentiment || '').toUpperCase() === alvo)
    .slice(0, 5)
    .map((p) => ({
      tipo: p.content_type || p.type || null,
      resumo: normalize(p.text || p.content || '', 160),
    }))
    .filter((p) => p.resumo);
  const postsNegativos = filtrarPorSentimento('NEGATIVE');
  const postsPositivos = filtrarPorSentimento('POSITIVE');

  const postsDestaque = postsRaw.slice(0, 3).map((p) => {
    const curtidas = p.likes || 0;
    const compartilhamentos = p.shares || 0;
    const comentarios = p.comments_amounts || 0;
    return {
      texto: normalize(p.text || p.content || '', 260),
      rede: p.service || null,
      autor: normalize(p.author && p.author.name, 80) || null,
      link: p.link || p.url || null,
      data: p.date || null,
      curtidas,
      compartilhamentos,
      comentarios,
      interacoes: curtidas + compartilhamentos + comentarios,
    };
  }).filter((p) => p.texto);

  const influencersRaw = influencersRes.status === 'fulfilled' ? (influencersRes.value.data || []) : [];
  const qtdInfluenciadores = influencersRes.status === 'fulfilled' ? (influencersRes.value.info?.profiles_found || 0) : 0;
  const nomesVistos = new Set();
  const influenciadoresDestaque = influencersRaw.map((inf) => {
    const social = (inf.social || [])[0] || {};
    return {
      nome: normalize(inf.name, 60) || null,
      rede: social.social_network || null,
      seguidores: social.followers || 0,
    };
  }).filter((inf) => {
    // A busca de influenciadores as vezes repete o mesmo perfil no topo do resultado.
    if (!inf.nome || nomesVistos.has(inf.nome)) return false;
    nomesVistos.add(inf.nome);
    return true;
  }).slice(0, 3);

  const empresaVolumeData = empresaRes.status === 'fulfilled' && empresaRes.value ? empresaRes.value.data || [] : [];
  const empresaMencoes = empresaVolumeData.reduce((s, d) => s + (d.value || 0), 0);

  const scores = {
    presenca: volumeScore(volumeTotal),
    sentimento: sentimentoScore(positivos, negativos),
    oportunidades: momentumScore(dailyData),
    diversidade_temas: diversidadeTemasScore(termsData),
  };
  scores.radar_score = radarScoreFinal(scores);

  const narrativaPayload = {
    empresa, cargo, segmento, dados_parciais: dadosParciais,
    volume_total_30d: volumeTotal,
    sentimento: { positivos, neutros, negativos },
    canais_ativos: canaisAtivos,
    ritmo_crescimento_pct: dailyData.length >= 14
      ? Math.round(((dailyData.slice(-7).reduce((s, d) => s + d.value, 0) - dailyData.slice(-14, -7).reduce((s, d) => s + d.value, 0)) / Math.max(1, dailyData.slice(-14, -7).reduce((s, d) => s + d.value, 0))) * 100)
      : null,
    tendencia_sentimento_pp: tendenciaSentimento,
    termos_mais_citados: termsData.slice(0, 12).map((t) => t.label),
    termos_emergentes_2a_quinzena: termosEmergentes,
    conteudos_que_performaram_bem: conteudosDestaque,
    exemplos_conteudo_negativo: postsNegativos,
    exemplos_conteudo_positivo: postsPositivos,
    influenciadores_no_nicho: qtdInfluenciadores,
    empresa_mencoes: empresaMencoes,
    scores,
  };

  const narrativa = await gerarNarrativa(narrativaPayload);

  syncActiveCampaign({ email, nome, empresa, cargo, segmento, radarScore: scores.radar_score }).catch(() => {});

  res.statusCode = 200;
  return res.json({
    ok: true,
    scores,
    narrativa,
    charts: {
      sentimento: { positivos, neutros, negativos },
      canais: serviceData,
      serie_diaria: dailyData,
      termos: termsData,
      genero: genderData,
    },
    prova: {
      posts: postsDestaque,
      influenciadores: influenciadoresDestaque,
    },
    meta: {
      dados_parciais: dadosParciais,
      empresa_mencoes: empresaMencoes,
      volume_total_30d: volumeTotal,
      influenciadores_no_nicho: qtdInfluenciadores,
    },
  });
};
