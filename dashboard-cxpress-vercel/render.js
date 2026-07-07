/* render.js — Cxpress: monta o HTML do conteudo a partir do objeto `d` do motor.js.
 *
 * Port fiel de dashboard/gerar_relatorio_cxpress.py::render_html + render_helpers_cxpress.py
 * (f-strings viram template literals). Retorna a string HTML do miolo (header + blocos 1-5 +
 * nota + footer) — o index.html injeta em #content, monta os charts e ativa o sortable.
 *
 * Idioma PT-BR, moeda BRL. Funil: Lead · Triagem · Agendamento · Demo · Proposta · Fechamento (+ Perdido).
 */
(function (root, factory) {
  if (typeof module !== 'undefined' && module.exports) module.exports = factory();
  else root.RenderCxpress = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // ---------- FORMATTERS (port de render_helpers / datas.py) ----------
  const MESES = ['Jan', 'Fev', 'Mar', 'Abr', 'Maio', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
  const MESES_CURTOS = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
  const DIAS_ACENTO = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom'];

  function fmtInt(n) {
    if (n === null || n === undefined) return '0';
    return Number(n).toLocaleString('pt-BR').replace(/,/g, '.');
  }
  function fDec(n) { return Number(n).toFixed(1).replace('.', ','); } // f_dec
  function fmtPctSafe(num, den) { return den ? `${Math.round(100 * num / den)}%` : '—'; }
  function fmtDataBr(s) { // fmt_data_curta: DD/MM
    if (!s) return '—';
    const d = new Date(s + 'T00:00:00');
    if (isNaN(d.getTime())) return s;
    return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}`;
  }
  function fmtDataLonga(s) { // fmt_data_longa: '09 de Maio (sáb)'
    if (!s) return '—';
    const d = new Date(s + 'T00:00:00');
    if (isNaN(d.getTime())) return s;
    return `${String(d.getDate()).padStart(2, '0')} de ${MESES[d.getMonth()]} (${DIAS_ACENTO[(d.getDay() + 6) % 7]})`;
  }
  function fmtMoedaBr(v) {
    if (v === null || v === undefined || v === 0) return '—';
    const n = Math.round(Number(v));
    if (!isFinite(n)) return '—';
    return `R$ ${n.toLocaleString('pt-BR').replace(/,/g, '.')}/mês`;
  }
  function parseValorText(v) {
    if (!v) return '—';
    let s = String(v).trim();
    if (!s) return '—';
    s = s.replace(/R\$/gi, '').trim();
    if (s.includes('/')) s = s.split('/')[0].trim();
    if (s.includes(',')) s = s.replace(/\./g, '').replace(',', '.');
    const n = parseFloat(s);
    if (!isFinite(n)) return '—';
    return fmtMoedaBr(n);
  }
  function escapeHtml(s) {
    if (s === null || s === undefined) return '';
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function decodeContent(v) { // _decode_content: unquote_plus (+ -> espaco, %XX)
    if (!v) return null;
    try { return decodeURIComponent(String(v).replace(/\+/g, ' ')); }
    catch (e) { return String(v).replace(/\+/g, ' '); }
  }
  function rankCell(idx) {
    const cls = idx === 0 ? 'rk-1' : idx === 1 ? 'rk-2' : idx === 2 ? 'rk-3' : 'rk-n';
    return `<span class="rk ${cls}">${idx + 1}</span>`;
  }
  const BADGE_CLASSES = {
    'meta': 'b-meta', 'chatgpt.com': 'b-chatgpt', 'email': 'b-email', 'blog': 'b-blog',
    'lp-agradecimento': 'b-lp', 'linkedin': 'b-linkedin', 'tiktok': 'b-tiktok',
  };
  function badgeSource(name) { // badge_source Cxpress: ig/fb/instagram*/facebook* -> b-meta
    const raw = name || '';
    const n = raw.trim().toLowerCase();
    if (!n) return '<span class="b">(vazio)</span>';
    if (n === 'ig' || n === 'fb' || n.startsWith('instagram') || n.startsWith('facebook'))
      return `<span class="b b-meta">${escapeHtml(raw)}</span>`;
    const cls = BADGE_CLASSES[n];
    return cls ? `<span class="b ${cls}">${escapeHtml(raw)}</span>` : `<span class="b">${escapeHtml(raw)}</span>`;
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

  const AC_DEALS_BASE = 'https://elife.activehosted.com/app/deals/';
  function dealCell(d) {
    const name = escapeHtml(d.deal);
    if (!d.id) return `<span class="deal-name">${name}</span>`;
    return `<a class="deal-name" href="${AC_DEALS_BASE}${d.id}" target="_blank" rel="noopener noreferrer" title="Abrir deal no ActiveCampaign">${name}</a>`;
  }
  function resp(d) { return escapeHtml(d.responsavel || '—'); }
  function emptyRow(cols) { return `<tr><td colspan="${cols}" class="dim center">(sem dados no período)</td></tr>`; }

  // ---------- ROWS — LISTAS (port render_helpers_cxpress) ----------
  function rowLead(d) {
    return `<tr><td>${dealCell(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(decodeContent(d.utm_content) || '—')}</td>`
      + `<td class="dim">${fmtDataBr(d.data_evento)}</td><td>${resp(d)}</td></tr>`;
  }
  function rowAgendamento(d) {
    const demo = d.data_demo
      ? `<span class="b b-status-ok">✓ ${fmtDataBr(d.data_demo)}</span>`
      : '<span class="b b-status-pending">Pendente</span>';
    return `<tr><td>${dealCell(d)}</td><td>${resp(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(decodeContent(d.utm_content) || '—')}</td>`
      + `<td class="dim">${fmtDataBr(d.data_evento)}</td><td>${demo}</td></tr>`;
  }
  function rowDemo(d) {
    const prop = d.data_proposta
      ? '<span class="b b-status-ok">✓ Sim</span>'
      : '<span class="b b-status-no">Não</span>';
    return `<tr><td>${dealCell(d)}</td><td>${resp(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(decodeContent(d.utm_content) || '—')}</td>`
      + `<td class="dim">${fmtDataBr(d.data_evento)}</td><td>${prop}</td></tr>`;
  }
  function rowProp(d) {
    return `<tr><td>${dealCell(d)}</td><td>${resp(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(decodeContent(d.utm_content) || '—')}</td>`
      + `<td class="dim">${fmtDataBr(d.data_evento)}</td>`
      + `<td class="num">${parseValorText(d.valor_text)}</td></tr>`;
  }
  function rowFech(d) {
    let valor = parseValorText(d.valor_text);
    valor = valor !== '—' ? `<b>${valor}</b>` : '—';
    return `<tr><td>${dealCell(d)}</td><td>${resp(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(decodeContent(d.utm_content) || '—')}</td>`
      + `<td class="dim">${fmtDataBr(d.data_evento)}</td><td class="num">${valor}</td></tr>`;
  }
  function rowPerda(d) {
    const motivo = d.motivo || '';
    const strong = ['Sem fit', 'Sem orçamento', 'Sem budget', 'Desqualificado'];
    const cls = strong.includes(motivo) ? 'b-reason' : 'b-reason-soft';
    const motivoHtml = motivo ? `<span class="b ${cls}">${escapeHtml(motivo)}</span>` : '<span class="dim">—</span>';
    return `<tr><td>${dealCell(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(decodeContent(d.utm_content) || '—')}</td>`
      + `<td class="dim">${escapeHtml(d.etapa || '—')}</td>`
      + `<td class="dim">${fmtDataBr(d.data_evento)}</td><td>${motivoHtml}</td></tr>`;
  }

  // ---------- RANKINGS (port render_helpers_cxpress) ----------
  const _MET = ['leads', 'triagem', 'agendamento', 'demo', 'proposta', 'fechamento'];
  function renderRankingSource(rows, topN = 8) {
    if (!rows || !rows.length) return emptyRow(10);
    const top = rows.slice(0, topN), outros = rows.slice(topN);
    const out = top.map((r, i) => rowRkSrc(i, r));
    if (outros.length) {
      const ag = {}; _MET.forEach((k) => ag[k] = outros.reduce((s, r) => s + (r[k] || 0), 0));
      out.push('<tr><td><span class="rk rk-n">—</span></td>'
        + `<td class="dim">outros (${outros.length})</td>`
        + `<td class="num">${fmtInt(ag.leads)}</td>`
        + `<td class="num">${fmtInt(ag.triagem)}</td><td class="num">—</td>`
        + `<td class="num">${fmtInt(ag.agendamento)}</td><td class="num">—</td>`
        + `<td class="num">${fmtInt(ag.demo)}</td>`
        + `<td class="num">${fmtInt(ag.proposta)}</td>`
        + `<td class="num">${fmtInt(ag.fechamento)}</td></tr>`);
    }
    return out.join('\n              ');
  }
  function rowRkSrc(idx, r) {
    const leads = r.leads || 0;
    const leadsHtml = idx < 3 ? `<b>${fmtInt(leads)}</b>` : fmtInt(leads);
    return `<tr><td>${rankCell(idx)}</td><td>${badgeSource(r.dim)}</td>`
      + `<td class="num">${leadsHtml}</td>`
      + `<td class="num">${fmtInt(r.triagem || 0)}</td>`
      + `<td class="num">${fmtPctSafe(r.triagem || 0, leads)}</td>`
      + `<td class="num">${fmtInt(r.agendamento || 0)}</td>`
      + `<td class="num">${fmtPctSafe(r.agendamento || 0, r.triagem || 0)}</td>`
      + `<td class="num">${fmtInt(r.demo || 0)}</td>`
      + `<td class="num">${fmtInt(r.proposta || 0)}</td>`
      + `<td class="num">${fmtInt(r.fechamento || 0)}</td></tr>`;
  }
  function renderRankingContent(rows, srcMap, topN = 12) {
    if (!rows || !rows.length) return emptyRow(8);
    const top = rows.slice(0, topN), outros = rows.slice(topN);
    const out = top.map((r, i) => rowRkCt(i, r, srcMap));
    if (outros.length) {
      const keys = ['leads', 'agendamento', 'demo', 'proposta', 'fechamento'];
      const ag = {}; keys.forEach((k) => ag[k] = outros.reduce((s, r) => s + (r[k] || 0), 0));
      out.push('<tr><td><span class="rk rk-n">—</span></td>'
        + `<td class="dim">outros (${outros.length})</td><td class="dim">—</td>`
        + `<td class="num">${fmtInt(ag.leads)}</td>`
        + `<td class="num">${fmtInt(ag.agendamento)}</td>`
        + `<td class="num">${fmtInt(ag.demo)}</td>`
        + `<td class="num">${fmtInt(ag.proposta)}</td>`
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
      + `<td class="num">${fmtInt(r.demo || 0)}</td>`
      + `<td class="num">${fmtInt(r.proposta || 0)}</td>`
      + `<td class="num">${fechHtml}</td></tr>`;
  }

  // ---------- KPIs (port gerar_relatorio_cxpress) ----------
  const KPIS = [
    ['leads', null, 'Leads'], ['triagem', 'leads', 'Triagem'],
    ['agendamento', 'triagem', 'Agendamento'], ['demo', 'agendamento', 'Demo realizada'],
    ['proposta', 'demo', 'Proposta'], ['fechamento', 'proposta', 'Fechamento'],
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
  const TH_SRC = '<tr><th>#</th><th>Fonte</th><th class="num">Leads</th><th class="num">Triagem</th>'
    + '<th class="num">% Tri</th><th class="num">Agend.</th><th class="num">% Agd</th>'
    + '<th class="num">Demo</th><th class="num">Prop.</th><th class="num">Fech.</th></tr>';
  const TH_CT = '<tr><th>#</th><th>Conteúdo</th><th>Fonte</th><th class="num">Leads</th>'
    + '<th class="num">Agend.</th><th class="num">Demo</th><th class="num">Prop.</th>'
    + '<th class="num">Fech.</th></tr>';

  function lst(rows, fn, cols) {
    return (rows && rows.length) ? rows.map(fn).join('') : emptyRow(cols);
  }

  // ---------- RENDER (port render_html) ----------
  function render(d) {
    const p = d.periodos;
    const fa = p.fim_atual, hoje = p.hoje;
    const semDiv = Math.max(1, p.semanas_decorridas_ytd);
    const pn = p.periodo_nome || 'Semana';
    const faY = new Date(fa + 'T00:00:00');
    const mtdFimD = new Date(p.mtd_fim + 'T00:00:00');
    const mtdIniD = new Date(p.mtd_ini + 'T00:00:00');
    const iniAtualD = new Date(p.ini_atual + 'T00:00:00');

    // ---- header ----
    const header = '<div class="top"><div class="chip">Content Marketing · Cxpress Brasil</div>'
      + '<h1>Resultados — Content Marketing</h1><div class="sub">Dashboard · seletor de período · Cxpress Brasil</div>'
      + '<div class="meta">'
      + `<div class="item"><span class="lbl">Período</span><span class="val">${fmtDataLonga(p.ini_atual)} → ${fmtDataLonga(fa)} · ${faY.getFullYear()}</span></div>`
      + `<div class="item"><span class="lbl">vs. período anterior</span><span class="val">${fmtDataBr(p.ini_ant)} → ${fmtDataBr(p.fim_ant)}</span></div>`
      + `<div class="item"><span class="lbl"><span class="no-upper">MtD</span> · Mês atual</span><span class="val">${String(mtdIniD.getDate()).padStart(2, '0')} → ${String(mtdFimD.getDate()).padStart(2, '0')} ${MESES_CURTOS[mtdFimD.getMonth()]} ${faY.getFullYear()}</span></div>`
      + `<div class="item"><span class="lbl"><span class="no-upper">YtD</span> · Acumulado do ano</span><span class="val">Jan → ${MESES_CURTOS[faY.getMonth()]} ${faY.getFullYear()} (${semDiv} semanas)</span></div>`
      + `<div class="item"><span class="lbl">Gerado em</span><span class="val">${fmtGeradoEm(hoje)}</span></div>`
      + '</div>'
      + '<div class="sources"><b>Fonte:</b> Supabase (cxpress_deals_funil_principal_prod) · '
      + 'funil Inbound + filtro Content Marketing calibrado · escopo em MAPEAMENTO-CAMPOS-cxpress.md. Moeda: BRL.</div></div>';

    // ---- bloco 1 ----
    const tagSem = `${String(iniAtualD.getDate()).padStart(2, '0')}–${String(faY.getDate()).padStart(2, '0')} ${MESES_CURTOS[faY.getMonth()]} ${faY.getFullYear()}`;
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
      + lossItem(pn, d.semana, `${String(iniAtualD.getDate()).padStart(2, '0')}–${String(faY.getDate()).padStart(2, '0')} ${MESES_CURTOS[faY.getMonth()]}`)
      + lossItem('<span class="no-upper">MtD</span>', d.mtd, `${String(mtdIniD.getDate()).padStart(2, '0')}–${String(mtdFimD.getDate()).padStart(2, '0')} ${MESES_CURTOS[mtdFimD.getMonth()]}`)
      + lossItem('<span class="no-upper">YtD</span>', d.ytd, `Jan–${MESES_CURTOS[faY.getMonth()]}`)
      + '</div>'
      + toggle('Leads perdidos no período · detalhe', `${d.perdidos_periodo.length} deals`,
        '<tr><th>Deal</th><th>Fonte</th><th>Conteúdo</th><th>Etapa do lost</th><th>Perdido em</th><th>Motivo</th></tr>', perdRows)
      + '</section>';

    // ---- bloco 3 (listas) ----
    const bloco3 = '<section><div class="section-head"><div class="icon">3</div>'
      + '<h2>Listas de Acesso Rápido · Período</h2><span class="tag">drill-down do funil</span></div>'
      + toggle('3.1 · Leads do período', `${d.leads_semana.length} deals`,
        '<tr><th>Deal</th><th>Fonte</th><th>Conteúdo</th><th>Data</th><th>Responsável</th></tr>',
        lst(d.leads_semana, rowLead, 5))
      + toggle('3.2 · Agendamentos do período', `${d.agend_semana.length} deals`,
        '<tr><th>Deal</th><th>Responsável</th><th>Fonte</th><th>Conteúdo</th><th>Data</th><th>Demo?</th></tr>',
        lst(d.agend_semana, rowAgendamento, 6))
      + toggle('3.3 · Demos realizadas no período', `${d.demo_semana.length} deals`,
        '<tr><th>Deal</th><th>Responsável</th><th>Fonte</th><th>Conteúdo</th><th>Data</th><th>Proposta?</th></tr>',
        lst(d.demo_semana, rowDemo, 6))
      + toggle('3.4 · Propostas do período', `${d.prop_semana.length} deals`,
        '<tr><th>Deal</th><th>Responsável</th><th>Fonte</th><th>Conteúdo</th><th>Data</th><th class="num">Valor</th></tr>',
        lst(d.prop_semana, rowProp, 6))
      + toggle('3.5 · Fechamentos do período', `${d.fech_semana.length} deals`,
        '<tr><th>Deal</th><th>Responsável</th><th>Fonte</th><th>Conteúdo</th><th>Data</th><th class="num">Valor</th></tr>',
        lst(d.fech_semana, rowFech, 6))
      + '</section>';

    // ---- bloco 4 (rankings) ----
    const perLbls = {
      semana: `${fmtDataBr(p.ini_atual)}–${fmtDataBr(fa)} ${faY.getFullYear()}`,
      sem_ant: `${fmtDataBr(p.ini_ant)}–${fmtDataBr(p.fim_ant)} ${faY.getFullYear()}`,
      mtd: `${fmtDataBr(p.mtd_ini)}–${fmtDataBr(p.mtd_fim)} ${faY.getFullYear()}`,
      ytd: `Jan–${MESES_CURTOS[faY.getMonth()]} ${faY.getFullYear()}`,
    };
    const titles = { semana: pn, sem_ant: 'Período Anterior', mtd: 'MtD', ytd: 'YtD' };
    const srcTbl = (key) => rkTable(titles[key], perLbls[key], TH_SRC, renderRankingSource(d['rk_src_' + key]));
    const ctTbl = (key) => rkTable(titles[key], perLbls[key], TH_CT, renderRankingContent(d['rk_ct_' + key], d.src_map));
    const bloco4 = '<section><div class="section-head"><div class="icon">4</div>'
      + '<h2>Detalhe · Período / Período Anterior / MtD / YtD</h2>'
      + '<span class="tag">% Tri = Triagem/Leads · % Agd = Agend./Triagem</span></div>'
      + '<div class="sub-head">4.a · Ranking de Fontes</div>'
      + `<div class="two-col">${srcTbl('semana')}${srcTbl('sem_ant')}</div>`
      + `<div class="two-col">${srcTbl('mtd')}${srcTbl('ytd')}</div>`
      + '<div class="sub-head">4.b · Ranking de Conteúdo (UTM Content)</div>'
      + `<div class="two-col">${ctTbl('semana')}${ctTbl('sem_ant')}</div>`
      + `<div class="two-col">${ctTbl('mtd')}${ctTbl('ytd')}</div>`
      + '</section>';

    // ---- bloco 5 (charts) ----
    const bloco5 = '<section><div class="section-head"><div class="icon">5</div>'
      + '<h2>Tendências · Últimos 12 meses</h2><span class="tag">52 semanas</span></div>'
      + '<div class="chart-wrap"><div class="chart-head">'
      + '<h3>Série temporal semanal · Funil + Tx Triagem</h3>'
      + '<span class="ctx">52 semanas · clique na legenda para ocultar séries</span></div>'
      + '<div class="chart-canvas"><canvas id="chartTimeseries"></canvas></div></div>'
      + '<div class="chart-wrap"><div class="chart-head">'
      + '<h3>Agendamentos e Demos por fonte · 12 meses</h3>'
      + '<span class="ctx">Agend. = Agendamentos · Demo = Demos realizadas</span></div>'
      + '<div class="chart-canvas chart-canvas-tall"><canvas id="chartSourceShare"></canvas></div></div>'
      + '</section>';

    const nota = '<div class="sources" style="margin-top:18px"><b>Dashboard de Content Marketing</b> sobre dados reais '
      + 'da tabela <code>cxpress_deals_funil_principal_prod</code>. Escopo: funil Inbound + filtro CM calibrado '
      + '(exclui Google Ads e tráfego whatsapp/youtube; inclui Meta/IG/FB/LinkedIn/Email/Blog/TikTok + LP '
      + '<code>atendimento-para-clinicas</code> + <code>content.cxpress.io</code>) — detalhes em MAPEAMENTO-CAMPOS-cxpress.md §2. '
      + 'As datas de etapa vêm do ActiveCampaign como texto e são lidas como ISO (YYYY-MM-DD). Sem dedup por pessoa (a tabela não tem e-mail).</div>';

    const footer = '<footer><b>Dashboard de Content Marketing · dados reais do Supabase</b><br>'
      + `${pn} ${fmtDataBr(p.ini_atual)}-${fmtDataBr(fa)} ${faY.getFullYear()} · `
      + `MtD ${fmtDataBr(p.mtd_ini)}-${fmtDataBr(p.mtd_fim)} · YtD Jan-${MESES_CURTOS[faY.getMonth()]} ${faY.getFullYear()}<br>`
      + 'Cada etapa contabilizada pela data do evento · Cxpress Brasil · uso interno</footer>';

    return header + bloco1 + bloco2 + bloco3 + bloco4 + bloco5 + nota + footer;
  }

  function fmtGeradoEm(s) {
    const d = new Date(s + 'T00:00:00');
    return `${String(d.getDate()).padStart(2, '0')} ${MESES_CURTOS[d.getMonth()]} ${d.getFullYear()}`;
  }

  // ---------- CHARTS (port do bloco _JS de gerar_relatorio_cxpress) ----------
  let _charts = { ts: null, ss: null };
  function montarCharts(d) {
    if (typeof Chart === 'undefined') return;
    const s = d.serie;
    const leads = s.leads, triagem = s.triagem, agendamento = s.agendamento, proposta = s.proposta, fechamento = s.fechamento;
    const txTriagem = leads.map((l, i) => l ? Math.round((triagem[i] / l) * 100) : 0);

    if (_charts.ts) _charts.ts.destroy();
    _charts.ts = new Chart(document.getElementById('chartTimeseries').getContext('2d'), {
      type: 'line',
      data: {
        labels: s.labels, datasets: [
          { label: 'Leads', data: leads, borderColor: '#1F2937', borderWidth: 2.6, tension: .35, pointRadius: 0, pointHoverRadius: 5, yAxisID: 'y' },
          { label: 'Triagem', data: triagem, borderColor: '#0B63FF', borderWidth: 2.2, tension: .35, pointRadius: 0, pointHoverRadius: 5, yAxisID: 'y' },
          { label: 'Tx Triagem (%)', data: txTriagem, borderColor: '#6EA7FF', borderWidth: 2, borderDash: [6, 3], tension: .35, pointRadius: 0, yAxisID: 'yPct' },
          { label: 'Agendamentos', data: agendamento, borderColor: '#6B7280', borderWidth: 1.8, borderDash: [3, 3], tension: .35, pointRadius: 0, yAxisID: 'y' },
          { label: 'Propostas', data: proposta, borderColor: '#F59E0B', borderWidth: 1.8, tension: .35, pointRadius: 0, yAxisID: 'y' },
          { label: 'Fechamentos', data: fechamento, borderColor: '#16A34A', backgroundColor: 'rgba(22,163,74,0.1)', borderWidth: 2.5, tension: .2, pointRadius: 3, pointHoverRadius: 5, yAxisID: 'y' },
        ],
      },
      options: {
        responsive: true, maintainAspectRatio: false, interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { position: 'top', align: 'end', labels: { font: { family: 'Inter', size: 13 }, color: '#374151', usePointStyle: true, pointStyle: 'rectRounded', padding: 16 } },
          tooltip: {
            backgroundColor: '#1F2937', padding: 12, cornerRadius: 8,
            callbacks: { label: (c) => c.dataset.yAxisID === 'yPct' ? `${c.dataset.label}: ${c.parsed.y}%` : `${c.dataset.label}: ${c.parsed.y}` },
          },
        },
        scales: {
          x: { ticks: { font: { family: 'Inter', size: 11 }, color: '#6B7280', maxRotation: 0, autoSkip: true, maxTicksLimit: 13 }, grid: { display: false } },
          y: { type: 'linear', position: 'left', beginAtZero: true, title: { display: true, text: 'Volumes (Leads · Triagem · Agend. · Prop. · Fech.)', font: { family: 'Inter', size: 12, weight: '600' }, color: '#4B5563' }, ticks: { font: { family: 'Inter', size: 12 }, color: '#6B7280' }, grid: { color: '#F1F5F9' } },
          yPct: { type: 'linear', position: 'right', beginAtZero: true, max: 100, title: { display: true, text: 'Tx Triagem (%)', font: { family: 'Inter', size: 12, weight: '600' }, color: '#0B63FF' }, ticks: { callback: (v) => v + '%', font: { family: 'Inter', size: 12 }, color: '#0B63FF' }, grid: { display: false } },
        },
      },
    });

    if (_charts.ss) _charts.ss.destroy();
    _charts.ss = new Chart(document.getElementById('chartSourceShare').getContext('2d'), {
      type: 'bar',
      data: {
        labels: ['Agendamentos (12m)', 'Demos (12m)'],
        datasets: (d.proporcao || []).map((x) => ({ label: x.label, data: [x.RA, x.RR], backgroundColor: x.color, borderWidth: 0, borderRadius: 4, barPercentage: 0.7, categoryPercentage: 0.7 })),
      },
      options: {
        indexAxis: 'y', responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', align: 'start', labels: { font: { family: 'Inter', size: 12 }, color: '#374151', usePointStyle: true, pointStyle: 'rectRounded', padding: 14, boxWidth: 14 } },
          tooltip: {
            backgroundColor: '#1F2937', padding: 12, cornerRadius: 8,
            callbacks: { label: (c) => { const t = c.chart.data.datasets.reduce((s2, ds) => s2 + ds.data[c.dataIndex], 0); const v = c.parsed.x; return `${c.dataset.label}: ${v} (${t ? ((v / t) * 100).toFixed(1) : 0}%)`; } },
          },
        },
        scales: {
          x: { stacked: true, beginAtZero: true, ticks: { font: { family: 'Inter', size: 12 }, color: '#6B7280' }, grid: { color: '#F1F5F9' } },
          y: { stacked: true, ticks: { font: { family: 'Inter', size: 13, weight: '600' }, color: '#374151' }, grid: { display: false } },
        },
      },
    });
  }

  // ---------- SORTABLE (port do _JS) ----------
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
        const num = (s) => { const m = (s || '').match(/-?[\d.,]+/); return m ? parseFloat(m[0].replace(/\./g, '').replace(',', '.')) : NaN; };
        rows.sort((a, b) => {
          const sa = (a.children[idx]?.innerText || '').trim(), sb = (b.children[idx]?.innerText || '').trim();
          const na = num(sa), nb = num(sb); let c;
          if (!isNaN(na) && !isNaN(nb)) c = na - nb; else c = sa.localeCompare(sb, 'pt-BR', { numeric: true, sensitivity: 'base' });
          return dir === 'asc' ? c : -c;
        });
        rows.forEach((r) => tbody.appendChild(r));
      });
    });
    table.dataset.sortable = '1';
  }

  return { render: render, montarCharts: montarCharts, makeSortable: makeSortable };
});
