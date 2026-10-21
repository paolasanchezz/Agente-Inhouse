/* render.js — Buzzcreators: monta o HTML do conteudo a partir do objeto `d` do motor.js.
 *
 * Port do dashboard-cxpress-vercel/render.js, adaptado ao funil Buzzcreators:
 *   Lead · Agendamento · Reuniao realizada · Fechamento (+ Perdidos)
 * Sem etapa Proposta (o Pipedrive nao tem data de entrada em Proposta).
 *
 * Idioma PT-BR, moeda BRL. Deal linka pro Pipedrive.
 */
(function (root, factory) {
  if (typeof module !== 'undefined' && module.exports) module.exports = factory();
  else root.RenderBuzzcreators = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // ---------- FORMATTERS ----------
  const MESES = ['Jan', 'Fev', 'Mar', 'Abr', 'Maio', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
  const MESES_CURTOS = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
  const DIAS_ACENTO = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom'];

  function fmtInt(n) {
    if (n === null || n === undefined) return '0';
    return Number(n).toLocaleString('pt-BR').replace(/,/g, '.');
  }
  function fDec(n) { return Number(n).toFixed(1).replace('.', ','); }
  function fmtPctSafe(num, den) { return den ? `${Math.round(100 * num / den)}%` : '—'; }
  function fmtDataBr(s) { // DD/MM
    if (!s) return '—';
    const d = new Date(s + 'T00:00:00');
    if (isNaN(d.getTime())) return s;
    return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}`;
  }
  function fmtDataLonga(s) { // '09 de Maio (sáb)'
    if (!s) return '—';
    const d = new Date(s + 'T00:00:00');
    if (isNaN(d.getTime())) return s;
    return `${String(d.getDate()).padStart(2, '0')} de ${MESES[d.getMonth()]} (${DIAS_ACENTO[(d.getDay() + 6) % 7]})`;
  }
  // Pipedrive guarda o valor do negocio em `value` (numeric) + currency — sem "/mês" como no AC.
  function fmtMoedaBr(v) {
    if (v === null || v === undefined || v === '') return '—';
    const n = Math.round(Number(v));
    if (!isFinite(n) || n === 0) return '—';
    return `R$ ${n.toLocaleString('pt-BR').replace(/,/g, '.')}`;
  }
  function escapeHtml(s) {
    if (s === null || s === undefined) return '';
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function decodeContent(v) { // unquote_plus (+ -> espaco, %XX)
    if (!v) return null;
    try { return decodeURIComponent(String(v).replace(/\+/g, ' ')); }
    catch (e) { return String(v).replace(/\+/g, ' '); }
  }
  // A URL de conversao as vezes vem gigante (query string inteira do anuncio) — encurta pra caber.
  function fmtUrl(v, max) {
    if (!v) return '—';
    let s = String(v).replace(/^https?:\/\//, '');
    try { s = decodeURIComponent(s.replace(/\+/g, ' ')); } catch (e) { /* mantem cru */ }
    const lim = max || 48;
    const curto = s.length > lim ? s.slice(0, lim - 1) + '…' : s;
    return `<span title="${escapeHtml(v)}">${escapeHtml(curto)}</span>`;
  }
  // Rotulo curto de intervalo que NAO mente quando o periodo atravessa mes ou ano.
  // (o template Cxpress/BR assume mes e ano unicos — em YtD isso vira "01–26 Ago 2026",
  //  e o periodo anterior de um YtD, que cai no ano passado, aparecia rotulado com o ano atual.)
  function rangeCurto(ini, fim) {
    const a = new Date(ini + 'T00:00:00'), b = new Date(fim + 'T00:00:00');
    const dd = (d) => String(d.getDate()).padStart(2, '0');
    const anoB = b.getFullYear();
    if (a.getFullYear() !== anoB)
      return `${dd(a)} ${MESES_CURTOS[a.getMonth()]} ${a.getFullYear()}–${dd(b)} ${MESES_CURTOS[b.getMonth()]} ${anoB}`;
    if (a.getMonth() !== b.getMonth())
      return `${dd(a)} ${MESES_CURTOS[a.getMonth()]}–${dd(b)} ${MESES_CURTOS[b.getMonth()]} ${anoB}`;
    return `${dd(a)}–${dd(b)} ${MESES_CURTOS[b.getMonth()]} ${anoB}`;
  }
  // Idem sem o ano, pros rotulos compactos do painel de perdas.
  function rangeCurtoSemAno(ini, fim) {
    const a = new Date(ini + 'T00:00:00'), b = new Date(fim + 'T00:00:00');
    const dd = (d) => String(d.getDate()).padStart(2, '0');
    if (a.getMonth() !== b.getMonth() || a.getFullYear() !== b.getFullYear())
      return `${dd(a)} ${MESES_CURTOS[a.getMonth()]}–${dd(b)} ${MESES_CURTOS[b.getMonth()]}`;
    return `${dd(a)}–${dd(b)} ${MESES_CURTOS[b.getMonth()]}`;
  }
  function rankCell(idx) {
    const cls = idx === 0 ? 'rk-1' : idx === 1 ? 'rk-2' : idx === 2 ? 'rk-3' : 'rk-n';
    return `<span class="rk ${cls}">${idx + 1}</span>`;
  }
  const BADGE_CLASSES = {
    'meta': 'b-meta', 'chatgpt.com': 'b-chatgpt', 'email': 'b-email', 'blog': 'b-blog',
    'lp-agradecimento': 'b-lp', 'linkedin': 'b-linkedin', 'inmail': 'b-linkedin', 'tiktok': 'b-tiktok',
    'webinar': 'b-lp', 'pos-webinar': 'b-lp', 'organic': 'b-blog', 'organic/direct': 'b-blog',
  };
  function badgeSource(name) {
    const raw = name || '';
    const n = raw.trim().toLowerCase();
    if (!n) return '<span class="b">(vazio)</span>';
    if (n === 'ig' || n === 'fb' || n.startsWith('instagram') || n.startsWith('facebook') || n === 'reels' || n === 'feed')
      return `<span class="b b-meta">${escapeHtml(raw)}</span>`;
    const cls = BADGE_CLASSES[n];
    return cls ? `<span class="b ${cls}">${escapeHtml(raw)}</span>` : `<span class="b">${escapeHtml(raw)}</span>`;
  }
  function badgeFunil(f) {
    const v = (f || '').trim();
    if (!v) return '<span class="dim">—</span>';
    const cls = v === 'Outbound' ? 'b-reason-soft' : 'b-status-ok';
    return `<span class="b ${cls}">${escapeHtml(v)}</span>`;
  }
  function formatDelta(atual, anterior, invert) {
    if (anterior === 0 && atual === 0) return { texto: '— igual ant.', classe: 'd-flat' };
    if (anterior === 0 && atual > 0) return { texto: `▲ novo (0 → ${atual})`, classe: 'd-new' };
    if (atual === anterior) return { texto: '— igual ant.', classe: 'd-flat' };
    const delta = atual - anterior;
    const pct = anterior ? Math.round((delta / anterior) * 100) : 0;
    const arrow = delta > 0 ? '▲' : '▼';
    const sign = delta > 0 ? '+' : '−';
    const texto = `${arrow} ${sign}${Math.abs(pct)}% vs ant.`;
    const classe = invert ? (delta < 0 ? 'd-up' : 'd-down') : (delta > 0 ? 'd-up' : 'd-down');
    return { texto, classe };
  }

  // Pipedrive: /deal/{id} resolve pra empresa do usuario logado.
  const PIPEDRIVE_DEAL_BASE = 'https://app.pipedrive.com/deal/';
  function dealCell(d) {
    const name = escapeHtml(d.deal);
    if (!d.id) return `<span class="deal-name">${name}</span>`;
    return `<a class="deal-name" href="${PIPEDRIVE_DEAL_BASE}${d.id}" target="_blank" rel="noopener noreferrer" title="Abrir deal no Pipedrive">${name}</a>`;
  }
  function resp(d) { return escapeHtml(d.responsavel || '—'); }
  function emptyRow(cols) { return `<tr><td colspan="${cols}" class="dim center">(sem dados no período)</td></tr>`; }

  // ---------- ROWS — LISTAS ----------
  function rowLead(d) {
    const ag = d.data_agendamento
      ? `<span class="b b-status-ok">✓ ${fmtDataBr(d.data_agendamento)}</span>`
      : '<span class="b b-status-pending">Pendente</span>';
    return `<tr><td>${dealCell(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(decodeContent(d.utm_content) || '—')}</td>`
      + `<td class="dim">${fmtUrl(d.url_conversao)}</td>`
      + `<td>${badgeFunil(d.funil)}</td>`
      + `<td class="dim" data-sort="${d.data_evento || ''}">${fmtDataBr(d.data_evento)}</td><td>${resp(d)}</td><td>${ag}</td></tr>`;
  }
  function rowAgendamento(d) {
    const rr = d.data_reuniao
      ? `<span class="b b-status-ok">✓ ${fmtDataBr(d.data_reuniao)}</span>`
      : '<span class="b b-status-pending">Pendente</span>';
    return `<tr><td>${dealCell(d)}</td><td>${resp(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(decodeContent(d.utm_content) || '—')}</td>`
      + `<td class="dim" data-sort="${d.data_evento || ''}">${fmtDataBr(d.data_evento)}</td><td>${rr}</td></tr>`;
  }
  function rowReuniao(d) {
    const fech = d.data_fechamento
      ? `<span class="b b-status-ok">✓ ${fmtDataBr(d.data_fechamento)}</span>`
      : `<span class="dim">${escapeHtml(d.etapa_atual || '—')}</span>`;
    return `<tr><td>${dealCell(d)}</td><td>${resp(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(decodeContent(d.utm_content) || '—')}</td>`
      + `<td class="dim" data-sort="${d.data_evento || ''}">${fmtDataBr(d.data_evento)}</td><td>${fech}</td></tr>`;
  }
  function rowFech(d) {
    let valor = fmtMoedaBr(d.valor);
    valor = valor !== '—' ? `<b>${valor}</b>` : '—';
    return `<tr><td>${dealCell(d)}</td><td>${resp(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(decodeContent(d.utm_content) || '—')}</td>`
      + `<td class="dim" data-sort="${d.data_evento || ''}">${fmtDataBr(d.data_evento)}</td><td class="num">${valor}</td></tr>`;
  }
  function rowPerda(d) {
    const motivo = d.motivo || '';
    const strong = ['Sem fit', 'Sem orçamento', 'Sem budget', 'Desqualificado', 'Sem perfil'];
    const cls = strong.includes(motivo) ? 'b-reason' : 'b-reason-soft';
    const motivoHtml = motivo ? `<span class="b ${cls}">${escapeHtml(motivo)}</span>` : '<span class="dim">—</span>';
    return `<tr><td>${dealCell(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(decodeContent(d.utm_content) || '—')}</td>`
      + `<td class="dim">${escapeHtml(d.etapa_atual || '—')}</td>`
      + `<td class="dim" data-sort="${d.data_evento || ''}">${fmtDataBr(d.data_evento)}</td><td>${motivoHtml}</td></tr>`;
  }

  // ---------- RANKINGS ----------
  const _MET = ['leads', 'agendamento', 'reuniao', 'fechamento'];
  function renderRankingSource(rows, topN = 8) {
    if (!rows || !rows.length) return emptyRow(8);
    const top = rows.slice(0, topN), outros = rows.slice(topN);
    const out = top.map((r, i) => rowRkSrc(i, r));
    if (outros.length) {
      const ag = {}; _MET.forEach((k) => ag[k] = outros.reduce((s, r) => s + (r[k] || 0), 0));
      out.push('<tr><td><span class="rk rk-n">—</span></td>'
        + `<td class="dim">outros (${outros.length})</td>`
        + `<td class="num">${fmtInt(ag.leads)}</td>`
        + `<td class="num">${fmtInt(ag.agendamento)}</td><td class="num">—</td>`
        + `<td class="num">${fmtInt(ag.reuniao)}</td><td class="num">—</td>`
        + `<td class="num">${fmtInt(ag.fechamento)}</td></tr>`);
    }
    return out.join('\n              ');
  }
  function rowRkSrc(idx, r) {
    const leads = r.leads || 0;
    const leadsHtml = idx < 3 ? `<b>${fmtInt(leads)}</b>` : fmtInt(leads);
    return `<tr><td>${rankCell(idx)}</td><td>${badgeSource(r.dim)}</td>`
      + `<td class="num">${leadsHtml}</td>`
      + `<td class="num">${fmtInt(r.agendamento || 0)}</td>`
      + `<td class="num">${fmtPctSafe(r.agendamento || 0, leads)}</td>`
      + `<td class="num">${fmtInt(r.reuniao || 0)}</td>`
      + `<td class="num">${fmtPctSafe(r.reuniao || 0, r.agendamento || 0)}</td>`
      + `<td class="num">${fmtInt(r.fechamento || 0)}</td></tr>`;
  }
  function renderRankingContent(rows, srcMap, topN = 12) {
    if (!rows || !rows.length) return emptyRow(7);
    const top = rows.slice(0, topN), outros = rows.slice(topN);
    const out = top.map((r, i) => rowRkCt(i, r, srcMap));
    if (outros.length) {
      const ag = {}; _MET.forEach((k) => ag[k] = outros.reduce((s, r) => s + (r[k] || 0), 0));
      out.push('<tr><td><span class="rk rk-n">—</span></td>'
        + `<td class="dim">outros (${outros.length})</td><td class="dim">—</td>`
        + `<td class="num">${fmtInt(ag.leads)}</td>`
        + `<td class="num">${fmtInt(ag.agendamento)}</td>`
        + `<td class="num">${fmtInt(ag.reuniao)}</td>`
        + `<td class="num">${fmtInt(ag.fechamento)}</td></tr>`);
    }
    return out.join('\n              ');
  }
  function rowRkCt(idx, r, srcMap) {
    const leads = r.leads || 0, fech = r.fechamento || 0;
    const leadsHtml = idx < 3 ? `<b>${fmtInt(leads)}</b>` : fmtInt(leads);
    const fechHtml = fech > 0 ? `<b>${fmtInt(fech)}</b>` : fmtInt(fech);
    const content = decodeContent(r.dim) || '(sem conteúdo)';
    const src = srcMap ? srcMap[r.dim] : null;
    return `<tr><td>${rankCell(idx)}</td><td>${escapeHtml(content)}</td><td>${badgeSource(src)}</td>`
      + `<td class="num">${leadsHtml}</td>`
      + `<td class="num">${fmtInt(r.agendamento || 0)}</td>`
      + `<td class="num">${fmtInt(r.reuniao || 0)}</td>`
      + `<td class="num">${fechHtml}</td></tr>`;
  }

  // ---------- KPIs ----------
  const KPIS = [
    ['leads', null, 'Leads'],
    ['agendamento', 'leads', 'Agendamento'],
    ['reuniao', 'agendamento', 'Reunião realizada'],
    ['fechamento', 'reuniao', 'Fechamento'],
    ['perd', 'leads', 'Perdidos'],
  ];
  const INVERT = new Set(['perd']);
  function kpiItem(label, val, pct, delta, med) {
    const pctH = pct != null ? `<div class="pct">${pct}</div>` : '';
    const deltaH = delta ? `<div class="delta ${delta.classe}">${delta.texto}</div>` : '';
    const medH = med ? `<div class="foot">${med}</div>` : '';
    return `<div class="kpi-item"><div class="label">${label}</div>`
      + `<div class="main"><div class="val">${fmtInt(val)}</div>${pctH}</div>${deltaH}${medH}</div>`;
  }
  function kpiRow(k, comp, ky, semDiv) {
    const items = KPIS.map(([key, denom, label]) => {
      const val = k[key];
      const pct = denom ? fmtPctSafe(val, k[denom]) : null;
      let delta = null, med = null;
      if (comp) delta = formatDelta(val, comp[key], INVERT.has(key));
      if (ky && semDiv) med = `méd. ${fDec(ky[key] / semDiv)}`;
      return kpiItem(label, val, pct, delta, med);
    });
    return `<div class="kpi-row">${items.join('')}</div>`;
  }

  // ---------- TOGGLE / TABLE helpers ----------
  function toggle(titulo, countLabel, thead, rowsHtml) {
    return '<details class="toggle"><summary><span class="toggle-title">'
      + `<span>${titulo}</span><span class="toggle-count">${countLabel}</span>`
      + '</span><span class="caret">▼</span></summary>'
      + `<div class="table-wrap"><table><thead>${thead}</thead><tbody>${rowsHtml}</tbody></table></div></details>`;
  }
  function rkTable(title, period, thead, rowsHtml) {
    return `<div><div class="col-head"><span class="title">${title}</span>`
      + `<span class="period">${period}</span></div>`
      + `<div class="table-wrap"><table><thead>${thead}</thead><tbody>${rowsHtml}</tbody></table></div></div>`;
  }
  const TH_SRC = '<tr><th>#</th><th>Fonte</th><th class="num">Leads</th><th class="num">Agend.</th>'
    + '<th class="num">% Agd</th><th class="num">Reunião</th><th class="num">% Reu</th>'
    + '<th class="num">Fech.</th></tr>';
  const TH_CT = '<tr><th>#</th><th>Conteúdo</th><th>Fonte</th><th class="num">Leads</th>'
    + '<th class="num">Agend.</th><th class="num">Reunião</th><th class="num">Fech.</th></tr>';

  function lst(rows, fn, cols) {
    return (rows && rows.length) ? rows.map(fn).join('') : emptyRow(cols);
  }

  // ---------- RENDER ----------
  function render(d) {
    const p = d.periodos;
    const fa = p.fim_atual, hoje = p.hoje;
    const semDiv = Math.max(1, p.semanas_decorridas_ytd);
    const pn = p.periodo_nome || 'Período';
    const faY = new Date(fa + 'T00:00:00');
    const mtdFimD = new Date(p.mtd_fim + 'T00:00:00');
    const mtdIniD = new Date(p.mtd_ini + 'T00:00:00');

    // ---- header ----
    const cob = d.cobertura;
    // deals_total ausente ou zero daria NaN%/Infinity% no cabecalho — nesse caso omite
    // so a percentagem e mantem as contagens, que continuam a ser verdade.
    const cobPct = (cob && Number(cob.deals_total) > 0)
      ? ` (${Math.round(100 * cob.com_source / cob.deals_total)}%)`
      : '';
    const cobTxt = cob
      ? `Atribuição recuperada por contato: <b>${fmtInt(cob.com_source)}</b> de ${fmtInt(cob.deals_total)} deals `
        + `com UTM${cobPct} · <b>${fmtInt(cob.no_escopo_cm)}</b> no escopo CM.`
      : '';
    const header = '<div class="top"><div class="chip">Content Marketing · Buzzcreators Brasil</div>'
      + '<h1>Resultados — Content Marketing</h1><div class="sub">Dashboard · seletor de período · Buzzcreators Brasil</div>'
      + '<div class="meta">'
      + `<div class="item"><span class="lbl">Período</span><span class="val">${fmtDataLonga(p.ini_atual)} → ${fmtDataLonga(fa)} · ${faY.getFullYear()}</span></div>`
      + `<div class="item"><span class="lbl">vs. período anterior</span><span class="val">${rangeCurto(p.ini_ant, p.fim_ant)}</span></div>`
      + `<div class="item"><span class="lbl"><span class="no-upper">MtD</span> · Mês atual</span><span class="val">${String(mtdIniD.getDate()).padStart(2, '0')} → ${String(mtdFimD.getDate()).padStart(2, '0')} ${MESES_CURTOS[mtdFimD.getMonth()]} ${faY.getFullYear()}</span></div>`
      + `<div class="item"><span class="lbl"><span class="no-upper">YtD</span> · Acumulado do ano</span><span class="val">Jan → ${MESES_CURTOS[faY.getMonth()]} ${faY.getFullYear()} (${semDiv} ${semDiv === 1 ? 'período' : 'períodos'})</span></div>`
      + `<div class="item"><span class="lbl">Gerado em</span><span class="val">${fmtGeradoEm(hoje)}</span></div>`
      + '</div>'
      + '<div class="sources"><b>Fonte:</b> Supabase · Pipedrive (<code>deals_pipedrive_vendas_buzzcreators</code>) '
      + '+ atribuição recuperada do contato (<code>dim_pipedrive_persons</code> → <code>dim_contacts</code>). '
      + `${cobTxt} Moeda: BRL.</div></div>`;

    // ---- bloco 1 ----
    const tagSem = rangeCurto(p.ini_atual, fa);
    const bloco1 = '<section><div class="section-head"><div class="icon">1</div>'
      + `<h2>Content Marketing · Visão Geral · ${pn}</h2>`
      + `<span class="tag">${tagSem}</span></div>`
      + kpiRow(d.semana, d.sem_ant, d.ytd, semDiv)
      + '<div class="sub-head">Acumulado <span class="no-upper">MtD</span></div>'
      + kpiRow(d.mtd)
      + '<div class="sub-head">Acumulado <span class="no-upper">YtD</span></div>'
      + kpiRow(d.ytd)
      + '</section>';

    // ---- bloco 2 (perdas) ----
    function lossItem(lbl, k, periodo) {
      const perd = k.perd, leads = k.leads;
      const pct = leads ? Math.round(100 * perd / leads) : 0;
      return `<div class="loss-item"><div class="label">% Perdidos · ${lbl}</div>`
        + `<div class="pct">${pct}%</div>`
        + `<div class="abs">${perd} perdidos · ${leads} leads · ${periodo}</div>`
        + `<div class="bar"><span style="width:${Math.min(pct, 100)}%"></span></div></div>`;
    }
    const perdRows = (d.perdidos_periodo.length ? d.perdidos_periodo.map(rowPerda).join('') : emptyRow(6));
    const bloco2 = '<section><div class="section-head"><div class="icon">2</div>'
      + '<h2>Perdas · Período / MtD / YtD</h2><span class="tag">coorte · leads criados no período</span></div>'
      + '<div class="loss-panel">'
      + lossItem(pn, d.semana, rangeCurtoSemAno(p.ini_atual, fa))
      + lossItem('<span class="no-upper">MtD</span>', d.mtd, rangeCurtoSemAno(p.mtd_ini, p.mtd_fim))
      + lossItem('<span class="no-upper">YtD</span>', d.ytd, `Jan–${MESES_CURTOS[faY.getMonth()]}`)
      + '</div>'
      + toggle('Leads perdidos no período · detalhe', `${d.perdidos_periodo.length} deals`,
        '<tr><th>Deal</th><th>Fonte</th><th>Conteúdo</th><th>Etapa</th><th>Perdido em</th><th>Motivo</th></tr>', perdRows)
      + '</section>';

    // ---- bloco 3 (listas) ----
    const bloco3 = '<section><div class="section-head"><div class="icon">3</div>'
      + '<h2>Listas de Acesso Rápido · Período</h2><span class="tag">drill-down do funil</span></div>'
      + toggle('3.1 · Leads do período', `${d.leads_semana.length} deals`,
        '<tr><th>Deal</th><th>Fonte</th><th>Conteúdo</th><th>URL de conversão</th><th>Funil</th><th>Data</th><th>Responsável</th><th>Agendou?</th></tr>',
        lst(d.leads_semana, rowLead, 8))
      + toggle('3.2 · Agendamentos do período', `${d.agend_semana.length} deals`,
        '<tr><th>Deal</th><th>Responsável</th><th>Fonte</th><th>Conteúdo</th><th>Data</th><th>Reunião?</th></tr>',
        lst(d.agend_semana, rowAgendamento, 6))
      + toggle('3.3 · Reuniões realizadas no período', `${d.reuniao_semana.length} deals`,
        '<tr><th>Deal</th><th>Responsável</th><th>Fonte</th><th>Conteúdo</th><th>Data</th><th>Fechou?</th></tr>',
        lst(d.reuniao_semana, rowReuniao, 6))
      + toggle('3.4 · Fechamentos do período', `${d.fech_semana.length} deals`,
        '<tr><th>Deal</th><th>Responsável</th><th>Fonte</th><th>Conteúdo</th><th>Data</th><th class="num">Valor</th></tr>',
        lst(d.fech_semana, rowFech, 6))
      + '</section>';

    // ---- bloco 4 (rankings) ----
    const perLbls = {
      semana: rangeCurto(p.ini_atual, fa),
      sem_ant: rangeCurto(p.ini_ant, p.fim_ant),
      mtd: rangeCurto(p.mtd_ini, p.mtd_fim),
      ytd: `Jan–${MESES_CURTOS[faY.getMonth()]} ${faY.getFullYear()}`,
    };
    const titles = { semana: pn, sem_ant: 'Período Anterior', mtd: 'MtD', ytd: 'YtD' };
    const srcTbl = (key) => rkTable(titles[key], perLbls[key], TH_SRC, renderRankingSource(d['rk_src_' + key]));
    const ctTbl = (key) => rkTable(titles[key], perLbls[key], TH_CT, renderRankingContent(d['rk_ct_' + key], d.src_map));
    const bloco4 = '<section><div class="section-head"><div class="icon">4</div>'
      + '<h2>Detalhe · Período / Período Anterior / MtD / YtD</h2>'
      + '<span class="tag">% Agd = Agend./Leads · % Reu = Reunião/Agend.</span></div>'
      + '<div class="sub-head">4.a · Ranking de Fontes</div>'
      + `<div class="two-col">${srcTbl('semana')}${srcTbl('sem_ant')}</div>`
      + `<div class="two-col">${srcTbl('mtd')}${srcTbl('ytd')}</div>`
      + '<div class="sub-head">4.b · Ranking de Conteúdo (UTM Content)</div>'
      + `<div class="two-col">${ctTbl('semana')}${ctTbl('sem_ant')}</div>`
      + `<div class="two-col">${ctTbl('mtd')}${ctTbl('ytd')}</div>`
      + '</section>';

    // ---- bloco 5 (tendencia) ----
    const bloco5 = '<section><div class="section-head"><div class="icon">5</div>'
      + '<h2>Tendências · Últimos 12 meses</h2><span class="tag">52 semanas</span></div>'
      + '<div class="chart-wrap"><div class="chart-head">'
      + '<h3>Agendamentos por semana · Tx de conversão</h3>'
      + '<span class="ctx">Tx = Agendamentos ÷ Deals criados na semana · Média 4 sem. = média móvel das últimas 4 semanas · clique na legenda para ocultar séries</span></div>'
      + '<div class="chart-canvas"><canvas id="chartTimeseries"></canvas></div></div>'
      + '</section>';

    // ---- bloco 6 (motivos de perda) ----
    const j = d.janela_12m;
    const bloco6 = '<section><div class="section-head"><div class="icon">6</div>'
      + '<h2>Motivos de Perda</h2><span class="tag">coorte · leads criados no intervalo</span></div>'
      + '<div class="two-col">'
      + pieWrap('chartMotivosPeriodo', pn === 'Período' ? 'Período selecionado' : `Período selecionado · ${pn}`, `${totalMotivos(d.motivos_periodo)} perdidos · ${rangeCurto(p.ini_atual, fa)}`, d.motivos_periodo)
      + pieWrap('chartMotivos12m', 'Últimos 12 meses', `${totalMotivos(d.motivos_12m)} perdidos · ${rangeCurto(j[0], j[1])} · mesma janela do gráfico de tendência`, d.motivos_12m)
      + '</div></section>';

    const nota = '<div class="sources" style="margin-top:18px"><b>Como ler esta dashboard.</b> '
      + 'O deal do Pipedrive <b>não tem UTM</b> — a atribuição é recuperada do contato '
      + '(<code>dim_pipedrive_persons.custom_fields</code>; só para deals criados antes de mar/2026 há fallback por e-mail em <code>dim_contacts</code>/ActiveCampaign — '
      + 'desde então o Pipedrive é a fonte única e deal sem UTM nem URL lá fica fora). '
      + 'Duas consequências: (1) <b>last touch</b> — os campos [AUTO] do contato são sobrescritos a cada nova conversão, '
      + 'então a fonte mostrada é o último toque conhecido, não necessariamente o que gerou o deal; '
      + '(2) leads sem UTM em nenhuma das duas bases ficam fora da dashboard. '
      + 'Escopo CM = <code>utm_source</code> na whitelist (Meta/IG, LinkedIn/InMail, e-mail, webinars e LPs de conteúdo, '
      + 'eventos, orgânico e GEO) — <b>exclui google/cpc</b> (Search pago) e toques internos (cs, comercial, bds, sdr). '
      + 'A etapa <b>Proposta não existe aqui</b>: o Pipedrive não registra data de entrada em Proposta. '
      + 'Cada etapa é contada pela data do evento; perdidos são coorte por data do lead. '
      + 'Detalhes em <code>dashboard/MAPEAMENTO-CAMPOS-buzzcreators.md</code>.</div>';

    const footer = '<footer><b>Dashboard de Content Marketing · dados reais do Supabase</b><br>'
      + `${pn} ${fmtDataBr(p.ini_atual)}-${fmtDataBr(fa)} ${faY.getFullYear()} · `
      + `MtD ${fmtDataBr(p.mtd_ini)}-${fmtDataBr(p.mtd_fim)} · YtD Jan-${MESES_CURTOS[faY.getMonth()]} ${faY.getFullYear()}<br>`
      + 'Cada etapa contabilizada pela data do evento · Buzzcreators Brasil · uso interno</footer>';

    return header + bloco1 + bloco2 + bloco3 + bloco4 + bloco5 + bloco6 + nota + footer;
  }

  function fmtGeradoEm(s) {
    const d = new Date(s + 'T00:00:00');
    return `${String(d.getDate()).padStart(2, '0')} ${MESES_CURTOS[d.getMonth()]} ${d.getFullYear()}`;
  }

  // ---------- CHARTS ----------
  const PIE_CORES = ['#0B63FF', '#F59E0B', '#16A34A', '#DC2626', '#7C3AED', '#0E9D9B', '#DB2777', '#92400E', '#94A3B8'];
  const FONTE = { family: 'Inter', size: 12 };
  let _charts = { ts: null, pp: null, p12: null };

  function totalMotivos(rows) { return (rows || []).reduce((t, r) => t + r.n, 0); }
  function pieWrap(id, titulo, ctx, rows) {
    const corpo = (rows && rows.length)
      ? `<div class="chart-canvas chart-canvas-pie"><canvas id="${id}"></canvas></div>`
      : '<div class="dim center chart-vazio">(sem perdidos no intervalo)</div>';
    return `<div class="chart-wrap"><div class="chart-head"><h3>${titulo}</h3><span class="ctx">${ctx}</span></div>${corpo}</div>`;
  }

  // Linhas solidas = agendamentos da semana; linha tracejada (eixo %) = agendamentos / deals criados na semana. Sem linha de Propostas: o Pipedrive nao data a entrada nessa etapa.
  function chartTendencia(s) {
    const agend = s.agendamento, leads = s.leads; 
    const tx = leads.map((l, i) => (l ? Math.round((agend[i] / l) * 100) : null));
    const mm4 = agend.map((_, i) => (i < 3 ? null : agend.slice(i - 3, i + 1).reduce((a, b) => a + b, 0) / 4)); // media movel 4 semanas (inclui a semana corrente)
    return new Chart(document.getElementById('chartTimeseries').getContext('2d'), {
      data: {
        labels: s.labels, datasets: [
          { type: 'line', label: 'Tx de conversão (%)', data: tx, borderColor: '#16A34A', backgroundColor: '#16A34A', borderWidth: 2, borderDash: [6, 3], cubicInterpolationMode: 'monotone', pointRadius: 2, pointHoverRadius: 5, spanGaps: true, yAxisID: 'yPct', order: 1 },
          { type: 'line', label: 'Agendamentos', data: agend, borderColor: '#0B63FF', backgroundColor: '#0B63FF', borderWidth: 2.4, cubicInterpolationMode: 'monotone', pointRadius: 2, pointHoverRadius: 5, yAxisID: 'y', order: 2 },
          { type: 'line', label: 'Agendamentos · média 4 sem.', data: mm4, borderColor: '#1E3A8A', backgroundColor: '#1E3A8A', borderWidth: 3, cubicInterpolationMode: 'monotone', pointRadius: 0, pointHoverRadius: 4, yAxisID: 'y', order: 2 },
        ],
      },
      options: {
        responsive: true, maintainAspectRatio: false, interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { position: 'top', align: 'end', labels: { font: { family: 'Inter', size: 13 }, color: '#374151', usePointStyle: true, pointStyle: 'rectRounded', padding: 16 } },
          tooltip: {
            backgroundColor: '#1F2937', padding: 12, cornerRadius: 8,
            callbacks: {
              label: (c) => c.dataset.yAxisID === 'yPct'
                ? `${c.dataset.label}: ${c.parsed.y == null ? '—' : c.parsed.y + '%'} (${agend[c.dataIndex]} de ${leads[c.dataIndex]} deals)`
                : `${c.dataset.label}: ${c.dataset.data === mm4 ? fDec(c.parsed.y) : c.parsed.y}`,
            },
          },
        },
        scales: {
          x: { ticks: { font: { family: 'Inter', size: 11 }, color: '#6B7280', maxRotation: 0, autoSkip: true, maxTicksLimit: 13 }, grid: { display: false } },
          y: { type: 'linear', position: 'left', beginAtZero: true, title: { display: true, text: 'Agendamentos', font: { ...FONTE, weight: '600' }, color: '#4B5563' }, ticks: { font: FONTE, color: '#6B7280', precision: 0 }, grid: { color: '#F1F5F9' } },
          yPct: { type: 'linear', position: 'right', beginAtZero: true, suggestedMax: 100, title: { display: true, text: 'Tx de conversão (%)', font: { ...FONTE, weight: '600' }, color: '#16A34A' }, ticks: { callback: (v) => v + '%', font: FONTE, color: '#16A34A' }, grid: { display: false } },
        },
      },
    });
  }

  function chartMotivos(id, rows) {
    const el = document.getElementById(id);
    if (!el || !rows || !rows.length) return null;
    const total = totalMotivos(rows);
    const pct = (n) => `${Math.round((100 * n) / total)}%`;
    return new Chart(el.getContext('2d'), {
      type: 'doughnut',
      data: { labels: rows.map((r) => r.motivo), datasets: [{ data: rows.map((r) => r.n), backgroundColor: rows.map((_, i) => PIE_CORES[i % PIE_CORES.length]), borderColor: '#fff', borderWidth: 2 }] },
      options: {
        responsive: true, maintainAspectRatio: false, cutout: '52%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              font: FONTE, color: '#374151', usePointStyle: true, pointStyle: 'rectRounded', padding: 10,
              generateLabels: (ch) => Chart.overrides.doughnut.plugins.legend.labels.generateLabels(ch)
                .map((l, i) => Object.assign(l, { text: `${rows[i].motivo} · ${rows[i].n} (${pct(rows[i].n)})` })),
            },
          },
          tooltip: { backgroundColor: '#1F2937', padding: 12, cornerRadius: 8, callbacks: { label: (c) => ` ${c.label}: ${c.parsed} (${pct(c.parsed)})` } },
        },
      },
    });
  }

  function montarCharts(d) {
    if (typeof Chart === 'undefined') return;
    Object.values(_charts).forEach((c) => c && c.destroy());
    _charts = {
      ts: chartTendencia(d.serie),
      pp: chartMotivos('chartMotivosPeriodo', d.motivos_periodo),
      p12: chartMotivos('chartMotivos12m', d.motivos_12m),
    };
  }

  // ---------- SORTABLE ----------
  // Data na celula vem como DD/MM: ordenar pelo texto pegava so o dia ("03/10" virava 3).
  // Celula de data carrega data-sort=ISO; badge com data (✓ 03/10) cai no parse DD/MM.
  function chaveCelula(td) {
    const t = (td?.innerText || '').trim();
    if (td && td.dataset.sort !== undefined) return { data: td.dataset.sort, t };
    const dm = t.match(/^(?:✓\s*)?(\d{1,2})\/(\d{1,2})(?:\/(\d{2,4}))?$/);
    if (dm) return { data: `${dm[3] || '0000'}-${dm[2].padStart(2, '0')}-${dm[1].padStart(2, '0')}`, t };
    return { data: null, t };
  }
  function compararCelulas(tdA, tdB, locale) {
    const a = chaveCelula(tdA), b = chaveCelula(tdB);
    if (a.data !== null && b.data !== null) return a.data < b.data ? -1 : a.data > b.data ? 1 : 0;
    const num = (s) => { const m = (s || '').match(/-?[\d.,]+/); return m ? parseFloat(m[0].replace(/\./g, '').replace(',', '.')) : NaN; };
    const na = num(a.t), nb = num(b.t);
    if (!isNaN(na) && !isNaN(nb)) return na - nb;
    return a.t.localeCompare(b.t, locale, { numeric: true, sensitivity: 'base' });
  }
  function makeSortable(table) {
    if (table.dataset.sortable === '1') return;
    const ths = table.querySelectorAll('thead th');
    ths.forEach((th, idx) => {
      if (th.textContent.trim() === '#') return;
      th.classList.add('sortable');
      if (!th.querySelector('.sort-ind')) {
        const ind = document.createElement('span'); ind.className = 'sort-ind'; ind.textContent = '⇅'; th.appendChild(ind);
      }
      th.addEventListener('click', () => {
        const tbody = table.querySelector('tbody'); if (!tbody) return;
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const dir = th.classList.contains('sort-asc') ? 'desc' : 'asc';
        ths.forEach((t) => { t.classList.remove('sort-asc', 'sort-desc'); const i = t.querySelector('.sort-ind'); if (i) i.textContent = '⇅'; });
        th.classList.add(dir === 'asc' ? 'sort-asc' : 'sort-desc');
        const ind = th.querySelector('.sort-ind'); if (ind) ind.textContent = dir === 'asc' ? '▲' : '▼';
        rows.sort((a, b) => {
          const c = compararCelulas(a.children[idx], b.children[idx], 'pt-BR');
          return dir === 'asc' ? c : -c;
        });
        rows.forEach((r) => tbody.appendChild(r));
      });
    });
    table.dataset.sortable = '1';
  }

  return { render: render, montarCharts: montarCharts, makeSortable: makeSortable };
});
