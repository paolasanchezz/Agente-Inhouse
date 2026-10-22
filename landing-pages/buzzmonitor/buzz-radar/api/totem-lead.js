// Totem Buzz Compass: captura do lead depois que ele pediu a analise.
// POST /api/totem-lead  { nome, email, marca, segmento, instagram, concorrentes[], _hp, _ts }
//
// Faz tres coisas, todas opcionais, independentes entre si e sem derrubar a resposta se alguma falhar:
//   1. e-mail para o lead com o QR code e o link do resultado (Resend; precisa RESEND_API_KEY e remetente verificado)
//   2. webhook de leads (TOTEM_LEADS_WEBHOOK_URL): hoje o Apps Script que grava na planilha do Google Sheets
//      (integracoes/google/buzz-compass-leads.gs), protegido por TOTEM_LEADS_WEBHOOK_TOKEN
//   3. ActiveCampaign: contato + tag "Buzz Compass" (achada ou criada pelo nome), nunca deal; desligado sem credencial
// Sem nenhuma configurada o lead so aparece no log da funcao: ver README.md.

const { normalize, fetchWithTimeout } = require('./_lib/trends');
const { limparPerfil } = require('./_lib/perfil');

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

function baseUrl(req) {
  if (process.env.TOTEM_BASE_URL) return process.env.TOTEM_BASE_URL.replace(/\/$/, '');
  const host = req.headers['x-forwarded-host'] || req.headers.host || 'buzzmonitor-lp-buzz-radar.vercel.app';
  return `https://${host}`;
}

// Mesma URL de analise do totem (m + c), sem dado pessoal na URL (a ordem dos parametros e a do totem: e a chave do cache).
function linkDoResultado(req, { marca, segmento, instagram, concorrentes }) {
  const p = new URLSearchParams();
  p.set('m', marca);
  if (segmento) p.set('s', segmento);
  if (instagram) p.set('i', instagram);
  concorrentes.forEach((c) => p.append('c', c));
  return `${baseUrl(req)}/totem-resultado?${p.toString()}`;
}

// Destino do botao "Agende uma demonstracao gratuita" do e-mail. TOTEM_DEMO_URL troca o endereco sem mexer no codigo.
// Entram as UTMs do Buzz Compass (sem sobrescrever as que o endereco ja tiver): sem utm_source o lead de CM some das dashboards.
function urlDemo() {
  const bruto = process.env.TOTEM_DEMO_URL || 'https://buzzmonitor.com/';
  let u;
  try { u = new URL(bruto); } catch (e) { u = new URL('https://buzzmonitor.com/'); }
  if (!/^https?:$/.test(u.protocol)) u = new URL('https://buzzmonitor.com/');
  const utms = { utm_source: 'buzz-compass', utm_medium: 'email', utm_campaign: 'buzz-compass-resultado' };
  Object.keys(utms).forEach((k) => { if (!u.searchParams.has(k)) u.searchParams.set(k, utms[k]); });
  return u.href;
}

// qrUrl: endereco https do PNG do QR (api/qr.js). Sem ele o e-mail sai so com o botao e o link.
function htmlDoEmail({ nome, marca, link, qrUrl }) {
  const primeiro = esc((nome || '').split(' ')[0] || 'Olá');
  const saudacao = nome ? `Olá, ${primeiro}!` : 'Olá!';
  const bloco = (conteudo, extra = '') => `<tr><td${extra}>${conteudo}</td></tr>`;
  const qr = qrUrl
    ? `<tr><td align="center" style="padding:0 0 10px"><table role="presentation" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:16px"><tr><td style="padding:14px"><img src="${esc(qrUrl)}" width="184" height="184" alt="QR code do Buzz Compass de ${esc(marca)}" style="display:block;width:184px;height:184px;border:0"></td></tr></table></td></tr>
<tr><td align="center" style="font-size:14px;line-height:1.5;color:#bdbdbd;padding:0 0 26px">Aponte a câmera do celular para o QR code e abra o seu Compass.</td></tr>`
    : '';
  return `<!doctype html><html lang="pt-BR"><body style="margin:0;background:#0b0b0c;font-family:Arial,Helvetica,sans-serif;color:#ffffff">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#0b0b0c"><tr><td align="center" style="padding:32px 16px">
<table role="presentation" width="560" cellpadding="0" cellspacing="0" style="max-width:560px;width:100%">
${bloco('BUZZ COMPASS', ' style="padding:0 0 20px;font-size:13px;letter-spacing:.12em;color:#EB7C2E;font-weight:700"')}
${bloco(`${saudacao} O Buzz Compass de ${esc(marca)} está pronto.`, ' style="font-size:26px;line-height:1.25;font-weight:800;padding:0 0 14px"')}
${bloco(`Reunimos conversas reais dos últimos 30 dias sobre a ${esc(marca)} na base de dados do Buzzmonitor Trends, comparamos ${esc(marca)} com os concorrentes e escrevemos o diagnóstico. Abra pelo celular ou pelo computador.`, ' style="font-size:16px;line-height:1.6;color:#d9d9d9;padding:0 0 26px"')}
${qr}
<tr><td align="center" style="padding:0 0 28px"><a href="${esc(link)}" style="display:inline-block;background:#EB7C2E;color:#ffffff;text-decoration:none;font-weight:700;font-size:16px;padding:15px 30px;border-radius:999px">Ver meu Compass</a></td></tr>
${bloco(`<strong style="color:#ffffff">Quer mostrar para o seu time?</strong><br>Encaminhe este e-mail. O botão e o QR code funcionam para qualquer pessoa, a qualquer momento, e o resultado fica disponível para consultar de novo.`, ' style="font-size:15px;line-height:1.6;color:#d9d9d9;background:#151517;border-radius:12px;padding:18px 20px"')}
<tr><td style="height:24px;line-height:24px;font-size:0">&nbsp;</td></tr>
<tr><td style="background:#EB7C2E;background-image:linear-gradient(135deg,#EB7C2E,#DE2451);border-radius:16px;padding:28px 26px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">
<tr><td style="font-size:24px;line-height:1.25;font-weight:800;color:#ffffff;padding:0 0 14px">Isso é só 10% do que a Buzzmonitor pode entregar!</td></tr>
<tr><td style="font-size:16px;line-height:1.6;color:#ffffff;padding:0 0 12px">Com um projeto de monitoramento dedicado à sua marca e com todos os canais sincronizados, a plataforma entrega análises ainda mais completas e estratégicas.</td></tr>
<tr><td style="font-size:16px;line-height:1.6;color:#ffffff;padding:0 0 12px">E em uma só plataforma você centraliza monitoramento, concorrentes, atendimento, analytics, dashboards, relatórios de IA e agendamento.</td></tr>
<tr><td style="font-size:16px;line-height:1.6;color:#ffffff;font-weight:700;padding:0 0 22px">Veja tudo isso na prática em conversa com um de nossos especialistas.</td></tr>
<tr><td><a href="${esc(urlDemo())}" style="display:inline-block;background:#ffffff;color:#1b1b1d;text-decoration:none;font-weight:800;font-size:16px;padding:15px 30px;border-radius:999px">Agende uma demonstração gratuita</a></td></tr>
</table></td></tr>
<tr><td style="height:24px;line-height:24px;font-size:0">&nbsp;</td></tr>
${bloco(`Se o botão não abrir, copie este endereço no navegador:<br><span style="color:#bdbdbd;word-break:break-all">${esc(link)}</span><br><br>Buzzmonitor`, ' style="font-size:13px;line-height:1.6;color:#8a8a8a;border-top:1px solid #26262a;padding:18px 0 0"')}
</table></td></tr></table></body></html>`;
}

// Uma segunda tentativa para oscilacao de rede ou erro 5xx do destino. Erro 4xx (credencial, dado recusado) nao melhora
// repetindo, entao nao repete. Assim um soluco passageiro do ActiveCampaign ou da planilha nao perde o lead.
async function tentarDeNovo(fn) {
  try {
    return await fn();
  } catch (err) {
    if (/_4\d\d\b/.test(String((err && err.message) || ''))) throw err;
    await new Promise((r) => setTimeout(r, 400));
    return fn();
  }
}

async function enviarEmail({ nome, email, marca, link, qrUrl }) {
  const key = process.env.RESEND_API_KEY;
  if (!key) return 'nao_configurado';
  try {
    const r = await fetchWithTimeout('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: process.env.TOTEM_EMAIL_FROM || 'Buzzmonitor <onboarding@resend.dev>',
        to: [email],
        subject: `Seu Buzz Compass de ${marca} está pronto`,
        html: htmlDoEmail({ nome, marca, link, qrUrl }),
        text: `${nome ? `Olá, ${nome.split(' ')[0]}! ` : ''}O Buzz Compass de ${marca} está pronto: ${link}\n\nPara mostrar ao seu time, encaminhe este e-mail: o link funciona para qualquer pessoa, a qualquer momento.\n\nIsso é só 10% do que a Buzzmonitor pode entregar!\nCom um projeto de monitoramento dedicado à sua marca e com todos os canais sincronizados, a plataforma entrega análises ainda mais completas e estratégicas. E em uma só plataforma você centraliza monitoramento, concorrentes, atendimento, analytics, dashboards, relatórios de IA e agendamento.\nVeja tudo isso na prática em conversa com um de nossos especialistas.\nAgende uma demonstração gratuita: ${urlDemo()}\n\nBuzzmonitor`,
      }),
    }, 8000);
    if (!r.ok) throw new Error(`resend_${r.status}: ${await r.text().catch(() => '')}`);
    return 'enviado';
  } catch (err) {
    console.error('[buzz-radar-totem] e-mail falhou', err && err.message ? err.message : err);
    return 'falhou';
  }
}

async function enviarWebhook(lead) {
  const url = process.env.TOTEM_LEADS_WEBHOOK_URL;
  if (!url) return 'nao_configurado';
  try {
    // O token vai no corpo (Apps Script nao le cabecalhos); o script da planilha recusa quem nao o tiver.
    const corpo = JSON.stringify({ ...(process.env.TOTEM_LEADS_WEBHOOK_TOKEN ? { token: process.env.TOTEM_LEADS_WEBHOOK_TOKEN } : {}), ...lead });
    await tentarDeNovo(async () => {
      const r = await fetchWithTimeout(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: corpo, redirect: 'follow' }, 8000);
      if (!r.ok) throw new Error(`webhook_${r.status}`);
      // O Apps Script responde 200 mesmo quando recusa o token: o resultado vem no JSON.
      const txt = await r.text().catch(() => '');
      if (/"ok"\s*:\s*false/.test(txt)) throw new Error(`webhook_recusou_400 ${txt.slice(0, 120)}`);
    });
    return 'enviado';
  } catch (err) {
    console.error('[buzz-radar-totem] webhook falhou', err && err.message ? err.message : err);
    return 'falhou';
  }
}

// --- ActiveCampaign: contato + tag "Buzz Compass" + URL de conversao (nunca deal) ---
const AC_TAG_PADRAO = 'Buzz Compass';
const AC_TEMPO_POR_CHAMADA_MS = 12000; // o AC as vezes demora mais que 5 a 6s; 12s cobre o lento sem segurar o lead
const AC_ORCAMENTO_TOTAL_MS = 50000; // teto de todas as chamadas do AC juntas (a funcao tem 60s)
const idsDeTag = new Map(); // nome da tag -> id (so vale enquanto a funcao esta quente; refaz a busca depois)
let idCampoUrlConversao; // id do campo "URL Conversao" depois de achado (undefined = ainda nao achou)

function acHeaders(token) { return { 'Api-Token': token, 'Content-Type': 'application/json' }; }

// Uma chamada ao AC com nome de etapa: timeout vira "ac_<etapa>_timeout" (e nao o generico "This operation was aborted"),
// e o tempo que cada etapa levou vai para o log, para saber se o AC esta lento ou se o problema e outro.
async function acFetch(passo, url, opcoes, limite) {
  const ms = Math.max(1500, Math.min(AC_TEMPO_POR_CHAMADA_MS, limite - Date.now()));
  const t0 = Date.now();
  try {
    const r = await fetchWithTimeout(url, opcoes, ms);
    console.log(`[buzz-radar-totem] ac ${passo} ${r.status} ${Date.now() - t0}ms`);
    return r;
  } catch (err) {
    const abortou = (err && err.name === 'AbortError') || /aborted/i.test(String((err && err.message) || ''));
    console.error(`[buzz-radar-totem] ac ${passo} ${abortou ? `sem resposta em ${Date.now() - t0}ms` : `erro de rede (${(err && err.message) || err})`}`);
    throw new Error(abortou ? `ac_${passo}_timeout` : `ac_${passo}_rede`);
  }
}

const semAcentoAC = (s) => String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

// Acha a tag pelo nome; se nao existir, cria. Assim ninguem precisa copiar o ID da tag para o painel da Vercel.
async function acIdDaTag(base, token, nome, limite) {
  if (idsDeTag.has(nome)) return idsDeTag.get(nome);
  const busca = await acFetch('tags_busca', `${base}/api/3/tags?search=${encodeURIComponent(nome)}`, { headers: acHeaders(token) }, limite);
  if (!busca.ok) throw new Error(`ac_tags_busca_${busca.status}`);
  const lista = ((await busca.json()).tags) || [];
  const achada = lista.find((t) => String(t.tag || '').trim().toLowerCase() === nome.toLowerCase());
  let id = achada && achada.id;
  if (!id) {
    const cria = await acFetch('tags_cria', `${base}/api/3/tags`, {
      method: 'POST',
      headers: acHeaders(token),
      body: JSON.stringify({ tag: { tag: nome, tagType: 'contact', description: 'Leads do Buzz Compass (totem do evento e LP)' } }),
    }, limite);
    if (!cria.ok) throw new Error(`ac_tags_cria_${cria.status}`);
    id = ((await cria.json()).tag || {}).id;
  }
  if (!id) throw new Error('ac_tag_sem_id');
  idsDeTag.set(nome, id);
  return id;
}

// Campo personalizado de contato "URL Conversão [Auto]": procurado pelo TITULO (o numero do campo muda de conta para conta).
// Entre varios candidatos, o que tem "[auto]" no nome ganha. ACTIVECAMPAIGN_URL_CONVERSAO_FIELD_ID forca o ID.
async function acIdDoCampoUrlConversao(base, token, limite) {
  if (process.env.ACTIVECAMPAIGN_URL_CONVERSAO_FIELD_ID) return String(process.env.ACTIVECAMPAIGN_URL_CONVERSAO_FIELD_ID).trim();
  if (idCampoUrlConversao !== undefined) return idCampoUrlConversao;
  const candidatos = [];
  for (let offset = 0; offset < 1000; offset += 100) {
    const r = await acFetch('campos', `${base}/api/3/fields?limit=100&offset=${offset}`, { headers: acHeaders(token) }, limite);
    if (!r.ok) throw new Error(`ac_campos_${r.status}`);
    const corpo = await r.json();
    const pagina = corpo.fields || [];
    pagina.forEach((f) => {
      const t = semAcentoAC(f.title);
      if (t.includes('url') && t.includes('conversao')) candidatos.push({ id: String(f.id), auto: t.includes('[auto]') || t.includes('(auto)') });
    });
    const total = Number((corpo.meta && corpo.meta.total) || 0);
    if (pagina.length < 100 || offset + 100 >= total) break;
  }
  const escolhido = candidatos.find((c) => c.auto) || candidatos[0] || null;
  // So guarda o que achou: se o campo nao existe ainda, a proxima vez procura de novo (criou o campo, ja vale no lead seguinte)
  if (escolhido) idCampoUrlConversao = escolhido.id;
  return escolhido ? escolhido.id : null;
}

// Contato ja existente pelo e-mail (comparacao exata, sem diferenciar maiusculas). Devolve { id } ou null.
async function acAcharContato(base, token, email, limite) {
  const r = await acFetch('busca_contato', `${base}/api/3/contacts?email=${encodeURIComponent(email)}`, { headers: acHeaders(token) }, limite);
  if (!r.ok) throw new Error(`ac_busca_contato_${r.status}`);
  const achado = (((await r.json()).contacts) || []).find((c) => String(c.email || '').trim().toLowerCase() === email.trim().toLowerCase());
  return achado ? { id: String(achado.id) } : null;
}

// Retorna { status, avisos[], contato: 'criado' | 'atualizado' }. Nunca lanca.
async function executarAC({ email, nome, marca, urlConversao }) {
  const base = (process.env.ACTIVECAMPAIGN_API_URL || '').trim().replace(/\/+$/, '').replace(/\/api\/3$/i, '');
  const token = (process.env.ACTIVECAMPAIGN_API_TOKEN || '').trim();
  if (!base || !token) return { status: 'nao_configurado', avisos: [] };
  const limite = Date.now() + AC_ORCAMENTO_TOTAL_MS;
  const avisos = [];
  try {
    // 1) Esse e-mail ja esta no AC? (busca que falha nao trava o lead: o sync abaixo tambem nao duplica por e-mail)
    let existente = null;
    try { existente = await tentarDeNovo(() => acAcharContato(base, token, email, limite)); } catch (err) {
      avisos.push('busca_contato_falhou');
      console.error('[buzz-radar-totem] activecampaign aviso', err && err.message ? err.message : err);
    }

    // 2) Campo "URL Conversao [Auto]" (melhor esforco: se nao achar, o contato e a tag seguem)
    let campoId = null;
    if (urlConversao) {
      try { campoId = await tentarDeNovo(() => acIdDoCampoUrlConversao(base, token, limite)); } catch (err) {
        avisos.push('campo_url_conversao_indisponivel');
        console.error('[buzz-radar-totem] activecampaign aviso', err && err.message ? err.message : err);
      }
      if (urlConversao && campoId === null && !avisos.includes('campo_url_conversao_indisponivel')) {
        avisos.push('campo_url_conversao_nao_encontrado');
        console.error('[buzz-radar-totem] activecampaign aviso: nao ha campo de contato com "URL Conversao" no nome');
      }
    }
    const fieldValues = campoId ? [{ field: campoId, value: urlConversao }] : [];

    // 3) Contato: existente = so atualiza a URL de conversao (nome e empresa que ja estao no AC ficam como estao);
    //    novo = cria completo (nome separado, marca na empresa) ja com a URL de conversao
    let contactId;
    if (existente) {
      contactId = existente.id;
      if (fieldValues.length) {
        await tentarDeNovo(async () => {
          const r = await acFetch('atualiza_contato', `${base}/api/3/contacts/${contactId}`, {
            method: 'PUT',
            headers: acHeaders(token),
            body: JSON.stringify({ contact: { fieldValues } }),
          }, limite);
          if (!r.ok) throw new Error(`ac_atualiza_contato_${r.status}`);
        });
      }
    } else {
      const partes = String(nome || '').trim().split(/\s+/);
      contactId = await tentarDeNovo(async () => {
        const sync = await acFetch('contato', `${base}/api/3/contact/sync`, {
          method: 'POST',
          headers: acHeaders(token),
          body: JSON.stringify({ contact: { email, firstName: partes[0] || '', lastName: partes.slice(1).join(' '), orgname: marca, fieldValues } }),
        }, limite);
        if (!sync.ok) throw new Error(`ac_contato_${sync.status}`);
        const id = ((await sync.json()).contact || {}).id;
        if (!id) throw new Error('ac_contato_sem_id');
        return String(id);
      });
    }

    // 4) Tag: ID fixo por variavel (se alguem quiser forcar) ou achada/criada pelo nome
    const tagId = process.env.ACTIVECAMPAIGN_TOTEM_TAG_ID || await tentarDeNovo(() => acIdDaTag(base, token, process.env.TOTEM_AC_TAG_NOME || AC_TAG_PADRAO, limite));
    await tentarDeNovo(async () => {
      const r = await acFetch('aplicar_tag', `${base}/api/3/contactTags`, {
        method: 'POST',
        headers: acHeaders(token),
        body: JSON.stringify({ contactTag: { contact: contactId, tag: tagId } }),
      }, limite);
      // 422 = contato ja tinha a tag (mesma pessoa rodando de novo): esta tudo certo
      if (!r.ok && r.status !== 422) throw new Error(`ac_aplicar_tag_${r.status}`);
    });

    // 5) Lista (opcional): so quando ha ID configurado. Inscrever em lista e decisao de marketing/consentimento, por isso desligado por padrao.
    const listaId = process.env.ACTIVECAMPAIGN_TOTEM_LIST_ID;
    if (listaId) {
      await tentarDeNovo(async () => {
        const r = await acFetch('lista', `${base}/api/3/contactLists`, {
          method: 'POST',
          headers: acHeaders(token),
          body: JSON.stringify({ contactList: { list: listaId, contact: contactId, status: 1 } }),
        }, limite);
        if (!r.ok && r.status !== 422) throw new Error(`ac_lista_${r.status}`);
      });
    }
    return { status: 'enviado', avisos, contato: existente ? 'atualizado' : 'criado' };
  } catch (err) {
    console.error('[buzz-radar-totem] activecampaign falhou', err && err.message ? err.message : err);
    return { status: 'falhou', avisos };
  }
}

// Versao simples (so o status), usada nos testes e por quem nao precisa dos detalhes.
async function syncActiveCampaign(dados) { return (await executarAC(dados)).status; }

// URL de conversao que vai para o campo "URL Conversao [Auto]" do AC: a pagina do totem onde o lead foi gerado (a mesma coisa
// que as LPs mandam). O navegador informa; o servidor so aceita https, host do proprio projeto e caminho /totem, tira o ruido
// (idle, fbclid, #hash) e corta em 500 caracteres. Qualquer outra coisa vira o endereco padrao do totem.
function urlDeConversao(req, bruto) {
  const padrao = `${baseUrl(req)}/totem`;
  try {
    const u = new URL(String(bruto || ''));
    const hosts = new Set(['buzzcompass.buzzmonitor.com', 'buzzmonitor-lp-buzz-radar.vercel.app']);
    try { hosts.add(new URL(baseUrl(req)).host.toLowerCase()); } catch (e) { /* ignora */ }
    if (u.protocol !== 'https:' || !hosts.has(u.host.toLowerCase()) || !/^\/totem\/?$/.test(u.pathname)) return padrao;
    ['idle', 'fbclid'].forEach((k) => u.searchParams.delete(k));
    u.hash = '';
    return u.href.slice(0, 500);
  } catch (e) {
    return padrao;
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

  // Honeypot e tempo minimo: mesmo criterio da LP original.
  if (typeof body._hp === 'string' && body._hp.trim()) return res.json({ ok: true, honeypot: true });
  const renderedAt = Number(body._ts);
  if (Number.isFinite(renderedAt) && Date.now() - renderedAt < 1500) return res.json({ ok: true, honeypot: true });

  const nome = normalize(body.nome, 100);
  const email = normalize(body.email, 200).toLowerCase();
  const marca = normalize(body.marca, 80);
  const segmento = normalize(body.segmento, 60);
  const instagram = limparPerfil(body.instagram);
  const concorrentes = (Array.isArray(body.concorrentes) ? body.concorrentes : [])
    .map((c) => normalize(String(c || ''), 60)).filter(Boolean).slice(0, 3);

  if (!nome || !marca || !email) {
    res.statusCode = 400;
    return res.json({ ok: false, error: 'missing_fields', message: 'Preencha nome, e-mail e marca.' });
  }
  if (!EMAIL_RE.test(email)) {
    res.statusCode = 400;
    return res.json({ ok: false, error: 'invalid_email', message: 'E-mail inválido.' });
  }

  const link = linkDoResultado(req, { marca, segmento, instagram, concorrentes });
  const urlConversao = urlDeConversao(req, body.url_conversao);
  const lead = { origem: 'buzz-compass-totem', criado_em: new Date().toISOString(), nome, email, marca, segmento, instagram, concorrentes, link, url_conversao: urlConversao };

  // Registro de seguranca: enquanto nenhuma integracao estiver ligada, este log e o unico lugar onde o lead existe.
  console.log('[totem-lead]', JSON.stringify(lead));

  // QR do e-mail: PNG gerado por /api/qr (so links do proprio resultado)
  const qrUrl = `${baseUrl(req)}/api/qr?d=${encodeURIComponent(link)}`;

  const [emailStatus, webhookStatus, ac] = await Promise.all([
    enviarEmail({ nome, email, marca, link, qrUrl }),
    enviarWebhook(lead),
    executarAC({ email, nome, marca, urlConversao }),
  ]);

  res.statusCode = 200;
  return res.json({ ok: true, email: emailStatus, webhook: webhookStatus, crm: ac.status, ...(ac.contato ? { crm_contato: ac.contato } : {}), ...(ac.avisos && ac.avisos.length ? { crm_avisos: ac.avisos } : {}), link });
};

module.exports.htmlDoEmail = htmlDoEmail;
module.exports.urlDemo = urlDemo;
module.exports.syncActiveCampaign = syncActiveCampaign;
module.exports.executarAC = executarAC;
module.exports.urlDeConversao = urlDeConversao;
module.exports._reiniciarCacheAC = () => { idsDeTag.clear(); idCampoUrlConversao = undefined; };
module.exports.enviarWebhook = enviarWebhook;
