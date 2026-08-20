const CLICKMEETING_API_BASE = 'https://api.clickmeeting.com/v1';
// Rede de seguranca: so entra em cena quando a API nao devolve a URL da sala, ou quando o
// honeypot dispara. Por serie, cai na propria pagina de confirmacao da LP.
const SERIES_THANK_YOU = {
  'bloqueo-whatsapp': 'https://content.cxpress.io/webinar-bloqueo-whatsapp-confirmado',
};
const FALLBACK_THANK_YOU = 'https://content.cxpress.io/webinar-bloqueo-whatsapp-confirmado';

// Idioma do e-mail de confirmacao do ClickMeeting, por serie. Default 'br' (PT-BR).
// Codigos validos ClickMeeting: pl, en, de, ru, es, fr, it, br.
// ia-voz e PT-BR -> cai no default. Adicionar 'chave':'es' quando houver serie LATAM neste dominio.
const SERIES_LANG = { 'bloqueo-whatsapp': 'es' };

function isValidEmail(value) {
  return typeof value === 'string' && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function normalize(value, max) {
  if (typeof value !== 'string') return '';
  return value.trim().slice(0, max);
}

async function resolveRoomId(req, series) {
  const proto = req.headers['x-forwarded-proto'] || 'https';
  const host = req.headers['x-forwarded-host'] || req.headers.host;
  if (!host) return { ok: false, error: 'no_host' };

  const qs = series ? ('?series=' + encodeURIComponent(series)) : '';
  let nwRes;
  try {
    nwRes = await fetch(`${proto}://${host}/api/next-webinar${qs}`, {
      headers: { 'Accept': 'application/json' },
    });
  } catch (err) {
    console.error('[clickmeeting-register] next-webinar fetch failed', err);
    return { ok: false, error: 'resolve_failed' };
  }

  let nwData = null;
  try { nwData = await nwRes.json(); } catch (_) { nwData = null; }

  if (!nwData || !nwData.ok) {
    return { ok: false, error: nwData && nwData.error ? nwData.error : 'no_webinar' };
  }
  return { ok: true, room_id: nwData.room_id };
}

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');

  if (req.method !== 'POST') {
    res.statusCode = 405;
    return res.json({ ok: false, error: 'method_not_allowed' });
  }

  const apiKey = process.env.CLICKMEETING_API_KEY;
  if (!apiKey) {
    console.error('[clickmeeting-register] CLICKMEETING_API_KEY ausente');
    res.statusCode = 500;
    return res.json({ ok: false, error: 'config_error' });
  }

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch (_) { body = null; }
  }
  if (!body || typeof body !== 'object') {
    res.statusCode = 400;
    return res.json({ ok: false, error: 'invalid_payload', message: 'Payload inválido.' });
  }

  if (typeof body._hp === 'string' && body._hp.trim().length > 0) {
    res.statusCode = 200;
    return res.json({ ok: true, redirect_url: SERIES_THANK_YOU[series] || FALLBACK_THANK_YOU });
  }

  const firstName = normalize(body.first_name, 100);
  const lastName = normalize(body.last_name, 100);
  const email = normalize(body.email, 200).toLowerCase();
  const company = normalize(body.company, 200);
  const series = normalize(body.series, 40);

  if (!firstName || !lastName || !email) {
    res.statusCode = 400;
    return res.json({ ok: false, error: 'missing_fields', message: 'Preencha nome, sobrenome e email.' });
  }
  if (!isValidEmail(email)) {
    res.statusCode = 400;
    return res.json({ ok: false, error: 'invalid_email', message: 'Email inválido.' });
  }

  const room = await resolveRoomId(req, series);
  if (!room.ok) {
    res.statusCode = 503;
    const isNoWebinar = room.error === 'no_upcoming' || room.error === 'no_webinar';
    return res.json({
      ok: false,
      error: isNoWebinar ? 'no_webinar' : 'resolve_failed',
      message: isNoWebinar
        ? 'Nenhum webinar disponível no momento. Tente novamente em alguns minutos.'
        : 'Não foi possível concluir sua inscrição agora. Tente novamente em instantes.',
    });
  }

  const params = new URLSearchParams();
  params.append('registration[1]', firstName);
  params.append('registration[2]', lastName);
  params.append('registration[3]', email);
  if (company) params.append('registration[10]', company);
  params.append('confirmation_email[enabled]', '1');
  params.append('confirmation_email[lang]', SERIES_LANG[series] || 'br');

  let apiResponse;
  try {
    apiResponse = await fetch(`${CLICKMEETING_API_BASE}/conferences/${room.room_id}/registration`, {
      method: 'POST',
      headers: {
        'X-Api-Key': apiKey,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
      },
      body: params.toString(),
    });
  } catch (err) {
    console.error('[clickmeeting-register] api network error', err);
    res.statusCode = 502;
    return res.json({ ok: false, error: 'cm_unreachable', message: 'Não foi possível concluir sua inscrição agora. Tente novamente em instantes.' });
  }

  const rawText = await apiResponse.text();
  let apiBody = null;
  try { apiBody = JSON.parse(rawText); } catch (_) { apiBody = null; }

  const apiBodyStr = JSON.stringify(apiBody || rawText);
  const isAlreadyRegistered = /exist|already|duplicate|registered/i.test(apiBodyStr);

  if (!apiResponse.ok || !apiBody || apiBody.status !== 'OK') {
    console.error('[clickmeeting-register] api error', {
      status: apiResponse.status,
      body: rawText.slice(0, 500),
    });
    if (isAlreadyRegistered || apiResponse.status === 409 || apiResponse.status === 422) {
      res.statusCode = 409;
      return res.json({ ok: false, error: 'already_registered', message: 'Este email já está inscrito neste webinar.' });
    }
    res.statusCode = 502;
    return res.json({ ok: false, error: 'cm_failed', message: 'Não foi possível concluir sua inscrição. Tente novamente.' });
  }

  res.statusCode = 200;
  return res.json({
    ok: true,
    redirect_url: (apiBody && typeof apiBody.url === 'string') ? apiBody.url : (SERIES_THANK_YOU[series] || FALLBACK_THANK_YOU),
  });
};
