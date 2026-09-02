const CLICKMEETING_API_BASE = 'https://api.clickmeeting.com/v1';

function formatDatePt(d) {
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: 'long',
    timeZone: 'America/Sao_Paulo',
  }).format(d);
}

function formatTimePt(d) {
  return new Intl.DateTimeFormat('pt-BR', {
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'America/Sao_Paulo',
  }).format(d).replace(':', 'h');
}

function capitalize(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

function formatFullPt(d) {
  const weekday = new Intl.DateTimeFormat('pt-BR', {
    weekday: 'long',
    timeZone: 'America/Sao_Paulo',
  }).format(d);
  return `${capitalize(weekday)}, ${formatDatePt(d)} · ${formatTimePt(d)} (horário de Brasília)`;
}

// Roteamento por LP. ?series=<chave> resolve para um recurring_config_id especifico.
// Sem o parametro -> usa o env padrao (serie placeholder compartilhada do dominio).
// Chave desconhecida -> tambem cai no padrao (fallback seguro, nunca quebra as LPs vizinhas).
const SERIES = {
  atencion: '17701', // Buzzmonitor Atención al Cliente (LP /atencion-al-cliente-es) — série recriada 2026-07-08 (antiga 17544 esgotou as sessões)
  buzzcreators: '18050', // Buzzcreators (LP /conheca-o-buzzcreators) — série recriada 2026-09-02 (antiga 17727 esgotou as sessões), room_pin 983-466-465, PT-BR, tz America/Sao_Paulo, 10:20 BRT
  'mcp-es': '17646', // Buzzmonitor Que es MCP (LP /que-es-mcp + -confirmado), room_pin 224-255-882, ES-LATAM, tz America/Mexico_City
  'listening-es': '17927', // Tu primer listening en 5 pasos (LP /primer-listening-5-pasos + -confirmado), room_pin 568-312-489, ES-LATAM, tz America/Mexico_City
  'smartfit-es': '17928', // Caso Smart Fit Latam (LP /caso-smartfit + -confirmado), room_pin 854-775-474, ES-LATAM, tz America/Mexico_City
  'crisis-es': '17933', // Gestión de Crisis (LP /gestion-crisis + -confirmado), room_pin 361-697-942, ES-LATAM, tz America/Mexico_City
  'concorrentes-br': '18043', // Como construir um monitoramento de concorrentes (LP /perpetuo-monitoramento-concorrentes + -confirmado), room_pin 692-573-549, PT-BR, tz America/Sao_Paulo, 09:00 BRT
};
// Aposentada 2026-08-19: mcp (17601, Buzzmonitor MCP PT-BR). Serie apagada no ClickMeeting
// por limite de disco (zero inscritos em 57 sessoes). A LP /mcp-na-pratica-p seguiu no ar
// com aviso de encerrada e nao chama mais esta function.

module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    res.statusCode = 405;
    return res.json({ ok: false, error: 'method_not_allowed' });
  }

  const apiKey = process.env.CLICKMEETING_API_KEY;
  if (!apiKey) {
    console.error('[next-webinar] CLICKMEETING_API_KEY ausente');
    res.statusCode = 500;
    return res.json({ ok: false, error: 'config_error' });
  }

  const seriesKey = (req.query && typeof req.query.series === 'string') ? req.query.series.trim() : '';
  const recurringConfigId = (seriesKey && SERIES[seriesKey])
    ? SERIES[seriesKey]
    : (process.env.CLICKMEETING_RECURRING_CONFIG_ID || null);
  const bufferMinutes = parseInt(process.env.MIN_BUFFER_MINUTES || '0', 10);

  // Sem serie resolvida (chave desconhecida E env padrao vazio) o filtro por
  // recurring_config_id abaixo seria pulado e a resposta traria a proxima sessao de
  // QUALQUER serie da conta, ou seja, a LP anunciaria o webinar errado. Falhar aqui e
  // preferivel: a LP cai no texto de "proxima sessao em breve".
  if (!recurringConfigId) {
    console.warn('[next-webinar] serie nao resolvida (series=%s)', seriesKey || '(vazio)');
    res.setHeader('Cache-Control', 'public, max-age=60, s-maxage=60, stale-while-revalidate=300');
    res.statusCode = 200;
    return res.json({ ok: false, error: 'no_series', message: 'Proxima sessao sendo agendada.' });
  }

  let apiResponse;
  try {
    apiResponse = await fetch(`${CLICKMEETING_API_BASE}/conferences/active`, {
      headers: { 'X-Api-Key': apiKey, 'Accept': 'application/json' },
    });
  } catch (err) {
    console.error('[next-webinar] network error', err);
    res.statusCode = 502;
    return res.json({ ok: false, error: 'fetch_failed' });
  }

  if (!apiResponse.ok) {
    console.error('[next-webinar] api error status', apiResponse.status);
    res.statusCode = 502;
    return res.json({ ok: false, error: 'fetch_failed' });
  }

  let conferences;
  try {
    conferences = await apiResponse.json();
  } catch (_) {
    res.statusCode = 502;
    return res.json({ ok: false, error: 'parse_failed' });
  }
  if (!Array.isArray(conferences)) conferences = [];

  const now = Date.now();
  const bufferMs = bufferMinutes * 60 * 1000;

  const eligible = conferences
    .filter((c) => {
      if (!c || !c.starts_at) return false;
      const starts = new Date(c.starts_at).getTime();
      if (!Number.isFinite(starts)) return false;
      // Vale ate o FIM da sessao, nao ate o inicio. Numa serie diaria a proxima sessao so
      // e materializada ~10 min depois desta terminar; enquanto a sessao corria, filtrar
      // por starts_at devolvia no_upcoming e derrubava o formulario de todas as LPs por
      // ~30-40 min todo dia (constatado em producao 2026-08-19).
      const ends = new Date(c.ends_at || c.starts_at).getTime();
      const limite = Number.isFinite(ends) ? ends : starts;
      if (limite <= now + bufferMs) return false;
      if (recurringConfigId && String(c.recurring_config_id) !== String(recurringConfigId)) return false;
      if (c.registration_enabled !== 1 && c.registration_enabled !== true) return false;
      return true;
    })
    .sort((a, b) => new Date(a.starts_at).getTime() - new Date(b.starts_at).getTime());

  if (eligible.length === 0) {
    res.setHeader('Cache-Control', 'public, max-age=60, s-maxage=60, stale-while-revalidate=300');
    res.statusCode = 200;
    return res.json({
      ok: false,
      error: 'no_upcoming',
      message: 'Próxima sessão sendo agendada.',
    });
  }

  const next = eligible[0];
  const startsAt = new Date(next.starts_at);

  res.setHeader('Cache-Control', 'public, max-age=300, s-maxage=300, stale-while-revalidate=600');
  res.statusCode = 200;
  return res.json({
    ok: true,
    room_id: next.id,
    room_pin: next.room_pin || null,
    starts_at: next.starts_at,
    in_progress: startsAt.getTime() <= now,
    formatted_date_pt: formatDatePt(startsAt),
    formatted_time_pt: formatTimePt(startsAt),
    formatted_full_pt: formatFullPt(startsAt),
    timezone: next.timezone || 'America/Sao_Paulo',
  });
};
