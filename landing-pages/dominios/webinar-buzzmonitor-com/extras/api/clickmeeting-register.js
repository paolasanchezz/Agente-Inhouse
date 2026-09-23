const CLICKMEETING_API_BASE = 'https://api.clickmeeting.com/v1';
// Rede de seguranca: so entra em cena quando a API nao devolve a URL da sala, ou quando o
// honeypot dispara. Por serie, cai na propria pagina de confirmacao da LP.
// Ate 2026-08-19 isto apontava para home.cxpress.io mesmo no dominio da Buzzmonitor.
const SERIES_THANK_YOU = {
  atencion: 'https://webinar.buzzmonitor.com/atencion-al-cliente-es-confirmado',
  buzzcreators: 'https://webinar.buzzmonitor.com/conheca-o-buzzcreators-confirmado',
  'mcp-es': 'https://webinar.buzzmonitor.com/que-es-mcp-confirmado',
  'listening-es': 'https://webinar.buzzmonitor.com/primer-listening-5-pasos-confirmado',
  'smartfit-es': 'https://webinar.buzzmonitor.com/caso-smartfit-confirmado',
  'crisis-es': 'https://webinar.buzzmonitor.com/gestion-crisis-confirmado',
  'concorrentes-br': 'https://webinar.buzzmonitor.com/perpetuo-monitoramento-concorrentes-confirmado',
  'concorrentes-pt': 'https://webinar.buzzmonitor.com/perpetuo-monitoramento-concorrentes-pt-confirmado',
};
const FALLBACK_THANK_YOU = 'https://webinar.buzzmonitor.com/primer-listening-5-pasos-confirmado';

// Idioma da serie: escolhe o pack de mensagens devolvido ao visitante E o e-mail de
// confirmacao do ClickMeeting. Default 'br' (PT-BR).
const SERIES_LANG = { atencion: 'es', 'mcp-es': 'es', 'listening-es': 'es', 'smartfit-es': 'es', 'crisis-es': 'es', 'concorrentes-pt': 'pt' };
// Codigos validos no ClickMeeting: pl, en, de, ru, es, fr, it, br. Nao existe pt-PT, entao a
// serie portuguesa (concorrentes-pt) recebe o e-mail de confirmacao no pack 'br', que e o em
// portugues. Isto vale so pro e-mail: as mensagens da LP saem em PT-PT (MESSAGES.pt).
const CM_EMAIL_LANG = { pt: 'br' };

// Mensagens ao visitante, no idioma da serie. O dominio serve LPs em PT-BR e em ES-LATAM;
// ate 2026-08-25 todas as respostas saiam em PT-BR, inclusive nas LPs espanholas.
const MESSAGES = {
  br: {
    invalid_payload: 'Dados inv\u00e1lidos. Recarregue a p\u00e1gina e tente de novo.',
    missing_fields: 'Preencha nome, sobrenome, e-mail, empresa e telefone.',
    invalid_phone: 'Telefone inv\u00e1lido. Confira o n\u00famero.',
    invalid_email: 'E-mail inv\u00e1lido.',
    no_webinar: 'Nenhum webinar dispon\u00edvel no momento. Tente novamente em alguns minutos.',
    resolve_failed: 'N\u00e3o foi poss\u00edvel concluir sua inscri\u00e7\u00e3o agora. Tente novamente em instantes.',
    cm_unreachable: 'N\u00e3o foi poss\u00edvel concluir sua inscri\u00e7\u00e3o agora. Tente novamente em instantes.',
    validation_error: 'Confira os dados: nome, sobrenome, e-mail, empresa e telefone s\u00e3o obrigat\u00f3rios.',
    already_registered: 'Este e-mail j\u00e1 est\u00e1 inscrito neste webinar.',
    cm_failed: 'N\u00e3o foi poss\u00edvel concluir sua inscri\u00e7\u00e3o. Tente novamente.',
  },
  es: {
    invalid_payload: 'Datos inv\u00e1lidos. Recarga la p\u00e1gina e int\u00e9ntalo de nuevo.',
    missing_fields: 'Completa nombre, apellido, correo, empresa y tel\u00e9fono.',
    invalid_phone: 'Tel\u00e9fono inv\u00e1lido. Revisa el n\u00famero.',
    invalid_email: 'Correo inv\u00e1lido.',
    no_webinar: 'No hay ninguna sesi\u00f3n disponible en este momento. Int\u00e9ntalo de nuevo en unos minutos.',
    resolve_failed: 'No pudimos completar tu registro ahora. Int\u00e9ntalo de nuevo en un momento.',
    cm_unreachable: 'No pudimos completar tu registro ahora. Int\u00e9ntalo de nuevo en un momento.',
    validation_error: 'Revisa los datos: nombre, apellido, correo, empresa y tel\u00e9fono son obligatorios.',
    already_registered: 'Este correo ya est\u00e1 registrado en este webinar.',
    cm_failed: 'No pudimos completar tu registro. Int\u00e9ntalo de nuevo.',
  },
  pt: {
    invalid_payload: 'Dados inv\u00e1lidos. Recarregue a p\u00e1gina e tente novamente.',
    missing_fields: 'Preencha o nome, o apelido, o e-mail, a empresa e o telefone.',
    invalid_phone: 'N\u00famero de telefone inv\u00e1lido. Confirme o n\u00famero.',
    invalid_email: 'E-mail inv\u00e1lido.',
    no_webinar: 'N\u00e3o h\u00e1 nenhuma sess\u00e3o dispon\u00edvel neste momento. Tente novamente dentro de alguns minutos.',
    resolve_failed: 'N\u00e3o foi poss\u00edvel concluir a sua inscri\u00e7\u00e3o agora. Tente novamente dentro de instantes.',
    cm_unreachable: 'N\u00e3o foi poss\u00edvel concluir a sua inscri\u00e7\u00e3o agora. Tente novamente dentro de instantes.',
    validation_error: 'Confirme os dados: nome, apelido, e-mail, empresa e telefone s\u00e3o obrigat\u00f3rios.',
    already_registered: 'Este e-mail j\u00e1 est\u00e1 inscrito neste webinar.',
    cm_failed: 'N\u00e3o foi poss\u00edvel concluir a sua inscri\u00e7\u00e3o. Tente novamente.',
  },
};

function msg(series, key) {
  const pack = MESSAGES[SERIES_LANG[series]] || MESSAGES.br;
  return pack[key];
}

function isValidEmail(value) {
  return typeof value === 'string' && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

// Telefone chega da LP ja no formato do ClickMeeting (DDI + numero, so digitos). O servidor
// refaz a limpeza e confere o tamanho E.164 (8 a 15 digitos) pra nao gravar lixo no campo 11.
function normalizePhone(value) {
  if (typeof value !== 'string') return '';
  return value.replace(/\D/g, '').replace(/^0+/, '').slice(0, 20);
}

function isValidPhone(value) {
  return /^\d{8,15}$/.test(value);
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
    return res.json({ ok: false, error: 'invalid_payload', message: msg('', 'invalid_payload') });
  }

  const firstName = normalize(body.first_name, 100);
  const lastName = normalize(body.last_name, 100);
  const email = normalize(body.email, 200).toLowerCase();
  const company = normalize(body.company, 200);
  const series = normalize(body.series, 40);
  const phone = normalizePhone(body.phone);

  // Honeypot depois das constantes: ate 2026-08-25 este bloco lia `series` antes do
  // `const series`, o que estoura ReferenceError (TDZ) em vez de devolver o 200 falso.
  if (typeof body._hp === 'string' && body._hp.trim().length > 0) {
    res.statusCode = 200;
    return res.json({ ok: true, redirect_url: SERIES_THANK_YOU[series] || FALLBACK_THANK_YOU });
  }

  // Empresa e obrigatoria: o formulario de registro das series exige o campo 10 (Company)
  // no ClickMeeting. Sem ele a API devolve 422 e a inscricao NAO acontece.
  // Telefone (campo 11) e obrigatorio na LP desde 2026-09-23.
  if (!firstName || !lastName || !email || !company || !phone) {
    res.statusCode = 400;
    return res.json({ ok: false, error: 'missing_fields', message: msg(series, 'missing_fields') });
  }
  if (!isValidEmail(email)) {
    res.statusCode = 400;
    return res.json({ ok: false, error: 'invalid_email', message: msg(series, 'invalid_email') });
  }

  if (!isValidPhone(phone)) {
    res.statusCode = 400;
    return res.json({ ok: false, error: 'invalid_phone', message: msg(series, 'invalid_phone') });
  }

  const room = await resolveRoomId(req, series);
  if (!room.ok) {
    res.statusCode = 503;
    const isNoWebinar = room.error === 'no_upcoming' || room.error === 'no_webinar';
    return res.json({
      ok: false,
      error: isNoWebinar ? 'no_webinar' : 'resolve_failed',
      message: msg(series, isNoWebinar ? 'no_webinar' : 'resolve_failed'),
    });
  }

  const params = new URLSearchParams();
  params.append('registration[1]', firstName);
  params.append('registration[2]', lastName);
  params.append('registration[3]', email);
  params.append('registration[10]', company);
  params.append('registration[11]', phone);
  params.append('confirmation_email[enabled]', '1');
  const serieLang = SERIES_LANG[series] || 'br';
  params.append('confirmation_email[lang]', CM_EMAIL_LANG[serieLang] || serieLang);

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
    return res.json({ ok: false, error: 'cm_unreachable', message: msg(series, 'cm_unreachable') });
  }

  const rawText = await apiResponse.text();
  let apiBody = null;
  try { apiBody = JSON.parse(rawText); } catch (_) { apiBody = null; }

  // Inscricao duplicada NAO e erro: o ClickMeeting devolve 200 com status OK, exist:1 e a URL
  // da sala. Ja o 422 (VALIDATION_ERRORS) e campo obrigatorio faltando. Ate 2026-08-25 o 422
  // caia no ramo `already_registered` e o visitante lia "voce ja esta inscrito" depois de uma
  // inscricao que nao aconteceu.
  const isValidationError = apiResponse.status === 422
    || (apiBody && (apiBody.code === 422 || apiBody.name === 'VALIDATION_ERRORS'));

  if (!apiResponse.ok || !apiBody || apiBody.status !== 'OK') {
    console.error('[clickmeeting-register] api error', {
      status: apiResponse.status,
      body: rawText.slice(0, 500),
    });
    if (isValidationError) {
      res.statusCode = 400;
      return res.json({ ok: false, error: 'validation_error', message: msg(series, 'validation_error') });
    }
    if (apiResponse.status === 409) {
      res.statusCode = 409;
      return res.json({ ok: false, error: 'already_registered', message: msg(series, 'already_registered') });
    }
    res.statusCode = 502;
    return res.json({ ok: false, error: 'cm_failed', message: msg(series, 'cm_failed') });
  }

  res.statusCode = 200;
  return res.json({
    ok: true,
    redirect_url: (apiBody && typeof apiBody.url === 'string') ? apiBody.url : (SERIES_THANK_YOU[series] || FALLBACK_THANK_YOU),
  });
};
