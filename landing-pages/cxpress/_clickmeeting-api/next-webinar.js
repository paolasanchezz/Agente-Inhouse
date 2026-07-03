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
// Sem o parametro -> usa o env padrao (serie placeholder do dominio: hoje 17529 = conheca-a-cxpress).
// Chave desconhecida -> tambem cai no padrao (fallback seguro, nunca quebra as LPs vizinhas).
const SERIES = {
  'ia-voz': '17671', // Cxpress Vozxpress — estudo de caso IA de Voz (LP /case-ia-de-voz). Conf id 10070428, room_pin 754-174-641, PT-BR, tz America/Sao_Paulo, automated type 2
};

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
      if (!Number.isFinite(starts) || starts <= now + bufferMs) return false;
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
      message: 'Próxima sessão sendo agendada. Entre em contato: contato@cxpress.io',
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
    formatted_date_pt: formatDatePt(startsAt),
    formatted_time_pt: formatTimePt(startsAt),
    formatted_full_pt: formatFullPt(startsAt),
    timezone: next.timezone || 'America/Sao_Paulo',
  });
};
