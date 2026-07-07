/* render.js — LATAM: monta o HTML do conteudo a partir do objeto `d` do motor.js.
 *
 * Port fiel de dashboard/gerar_relatorio_latam.py::render_html + render_helpers_latam.py.
 * Idioma espanhol, moeda USD. Funil: Leads · Primer contacto · Reunión · Cierre (+ Perdido).
 * Retorna a string HTML do miolo (header + blocos 1-5 + nota + footer).
 */
(function (root, factory) {
  if (typeof module !== 'undefined' && module.exports) module.exports = factory();
  else root.RenderLatam = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const MESES_F = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
  const MESES_C = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
  const DIA = ['lun', 'mar', 'mié', 'jue', 'vie', 'sáb', 'dom'];

  function fmtInt(n) {
    if (n === null || n === undefined) return '0';
    return Number(n).toLocaleString('es', { useGrouping: true }).replace(/,/g, '.').replace(/ /g, '.');
  }
  function fDec(n) { return Number(n).toFixed(1).replace('.', ','); }
  function fmtPct(num, den) { return den ? `${Math.round(100 * (num || 0) / den)}%` : '—'; }
  function fmtFecha(s) {
    if (!s) return '—';
    const d = new Date(s + 'T00:00:00');
    if (isNaN(d.getTime())) return s;
    return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}`;
  }
  function fLarga(s) {
    if (!s) return '—';
    const d = new Date(s + 'T00:00:00');
    if (isNaN(d.getTime())) return s;
    return `${String(d.getDate()).padStart(2, '0')} de ${MESES_F[d.getMonth()]} (${DIA[(d.getDay() + 6) % 7]})`;
  }
  function fmtUsd(v) {
    if (v === null || v === undefined || Number(v) === 0) return '—';
    const n = Math.round(Number(v));
    if (!isFinite(n)) return '—';
    return `US$ ${n.toLocaleString('en-US').replace(/,/g, '.')}/mes`;
  }
  function escapeHtml(s) {
    if (s === null || s === undefined) return '';
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function rankCell(idx) {
    const cls = idx === 0 ? 'rk-1' : idx === 1 ? 'rk-2' : idx === 2 ? 'rk-3' : 'rk-n';
    return `<span class="rk ${cls}">${idx + 1}</span>`;
  }
  const BADGE_CLASSES = {
    'meta': 'b-meta', 'chatgpt.com': 'b-chatgpt', 'email': 'b-email', 'blog': 'b-blog',
    'linkedin': 'b-linkedin', 'tiktok': 'b-tiktok',
  };
  function badgeSource(name) {
    const raw = (name == null) ? '' : String(name).trim();
    if (!raw || raw === '(vacío)') return '<span class="b">(vacío)</span>';
    const cls = BADGE_CLASSES[raw.toLowerCase()];
    return cls ? `<span class="b ${cls}">${escapeHtml(raw)}</span>` : `<span class="b">${escapeHtml(raw)}</span>`;
  }
  function formatDelta(atual, anterior, invert) {
    if (anterior === 0 && atual === 0) return { texto: '— igual', classe: 'd-flat' };
    if (anterior === 0 && atual > 0) return { texto: `▲ nuevo (0 → ${atual})`, classe: 'd-new' };
    if (atual === anterior) return { texto: '— igual', classe: 'd-flat' };
    const delta = atual - anterior;
    const pct = anterior ? Math.round((delta / anterior) * 100) : 0;
    const arrow = delta > 0 ? '▲' : '▼';
    const sign = delta > 0 ? '+' : '−';
    const texto = `${arrow} ${sign}${Math.abs(pct)}% vs sem. ant.`;
    const classe = invert ? (delta < 0 ? 'd-up' : 'd-down') : (delta > 0 ? 'd-up' : 'd-down');
    return { texto, classe };
  }

  const AC_DEALS_BASE = 'https://elifeeurope.activehosted.com/app/deals/';
  function dealCell(d) {
    const name = escapeHtml(d.deal);
    if (!d.id) return `<span class="deal-name">${name}</span>`;
    return `<a class="deal-name" href="${AC_DEALS_BASE}${d.id}" target="_blank" rel="noopener noreferrer" title="Abrir deal no ActiveCampaign">${name}</a>`;
  }
  function resp(d) { return escapeHtml(d.responsable || '—'); }
  function emptyRow(cols) { return `<tr><td colspan="${cols}" class="dim center">(sin datos en el período)</td></tr>`; }

  // ---------- ROWS ----------
  function rowLead(d) {
    return `<tr><td>${dealCell(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(d.utm_content || '—')}</td>`
      + `<td class="dim">${escapeHtml(d.pais || '—')}</td>`
      + `<td class="dim">${fmtFecha(d.data_conversao)}</td><td>${resp(d)}</td></tr>`;
  }
  function rowReunion(d) {
    return `<tr><td>${dealCell(d)}</td><td>${resp(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(d.utm_content || '—')}</td>`
      + `<td class="dim">${escapeHtml(d.pais || '—')}</td>`
      + `<td class="dim">${fmtFecha(d.data_evento)}</td></tr>`;
  }
  function rowCierre(d) {
    const v = d.valor;
    const valorHtml = (v && Number(v) > 0) ? `<b>${fmtUsd(v)}</b>` : '—';
    return `<tr><td>${dealCell(d)}</td><td>${resp(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(d.pais || '—')}</td>`
      + `<td class="dim">${fmtFecha(d.data_fech)}</td><td class="num">${valorHtml}</td></tr>`;
  }
  function rowPerda(d) {
    return `<tr><td>${dealCell(d)}</td><td>${badgeSource(d.utm_source)}</td>`
      + `<td class="dim">${escapeHtml(d.utm_content || '—')}</td>`
      + `<td class="dim">${escapeHtml(d.pais || '—')}</td>`
      + `<td class="dim">${fmtFecha(d.data_evento)}</td></tr>`;
  }

  // ---------- RANKINGS ----------
  const _MET = ['leads', 'pc', 'reunion', 'cierre'];
  function renderRankingSource(rows, topN = 8) {
    if (!rows || !rows.length) return emptyRow(8);
    const top = rows.slice(0, topN), outros = rows.slice(topN);
    const out = top.map((r, i) => rowRkSrc(i, r));
    if (outros.length) {
      const ag = {}; _MET.forEach((k) => ag[k] = outros.reduce((s, r) => s + (r[k] || 0), 0));
      out.push('<tr><td><span class="rk rk-n">—</span></td>'
        + `<td class="dim">otros (${outros.length})</td>`
        + `<td class="num">${fmtInt(ag.leads)}</td>`
        + `<td class="num">${fmtInt(ag.pc)}</td><td class="num">—</td>`
        + `<td class="num">${fmtInt(ag.reunion)}</td><td class="num">—</td>`
        + `<td class="num">${fmtInt(ag.cierre)}</td></tr>`);
    }
    return out.join('\n              ');
  }
  function rowRkSrc(idx, r) {
    const leads = r.leads || 0;
    const leadsHtml = idx < 3 ? `<b>${fmtInt(leads)}</b>` : fmtInt(leads);
    return `<tr><td>${rankCell(idx)}</td><td>${badgeSource(r.dim)}</td>`
      + `<td class="num">${leadsHtml}</td>`
      + `<td class="num">${fmtInt(r.pc || 0)}</td>`
      + `<td class="num">${fmtPct(r.pc || 0, leads)}</td>`
      + `<td class="num">${fmtInt(r.reunion || 0)}</td>`
      + `<td class="num">${fmtPct(r.reunion || 0, r.pc || 0)}</td>`
      + `<td class="num">${fmtInt(r.cierre || 0)}</td></tr>`;
  }
  function renderRankingContent(rows, srcMap, topN = 12) {
    if (!rows || !rows.length) return emptyRow(7);
    const top = rows.slice(0, topN), outros = rows.slice(topN);
    const out = top.map((r, i) => rowRkCt(i, r, srcMap));
    if (outros.length) {
      const ag = {}; _MET.forEach((k) => ag[k] = outros.reduce((s, r) => s + (r[k] || 0), 0));
      out.push('<tr><td><span class="rk rk-n">—</span></td>'
        + `<td class="dim">otros (${outros.length})</td><td class="dim">—</td>`
        + `<td class="num">${fmtInt(ag.leads)}</td>`
        + `<td class="num">${fmtInt(ag.pc)}</td>`
        + `<td class="num">${fmtInt(ag.reunion)}</td>`
        + `<td class="num">${fmtInt(ag.cierre)}</td></tr>`);
    }
    return out.join('\n              ');
  }
  function rowRkCt(idx, r, srcMap) {
    const leads = r.leads || 0, cierre = r.cierre || 0;
    const leadsHtml = idx < 3 ? `<b>${fmtInt(leads)}</b>` : fmtInt(leads);
    const cierreHtml = cierre > 0 ? `<b>${fmtInt(cierre)}</b>` : fmtInt(cierre);
    const content = r.dim || '(vacío)';
    const src = srcMap ? srcMap[r.dim] : null;
    return `<tr><td>${rankCell(idx)}</td><td>${escapeHtml(content)}</td><td>${badgeSource(src)}</td>`
      + `<td class="num">${leadsHtml}</td>`
      + `<td class="num">${fmtInt(r.pc || 0)}</td>`
      + `<td class="num">${fmtInt(r.reunion || 0)}</td>`
      + `<td class="num">${cierreHtml}</td></tr>`;
  }

  // ---------- KPIs (5) ----------
  const KPIS = [
    ['leads', null, 'Leads'], ['pc', 'leads', 'Primer contacto'],
    ['reunion', 'pc', 'Reunión'], ['cierre', 'reunion', 'Cierres'],
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
      const pct = denom ? fmtPct(val, k[denom]) : null;
      let delta = null, med = null;
      if (comp) delta = formatDelta(val, comp[key], INVERT.has(key));
      if (ky && semDiv) med = `prom. ${fDec(ky[key] / semDiv)}`;
      return kpiItem(label, val, pct, delta, med);
    });
    return `<div class="kpi-row">${items.join('')}</div>`;
  }

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
  const TH_SRC = '<tr><th>#</th><th>Fuente</th><th class="num">Leads</th><th class="num">PC</th>'
    + '<th class="num">% PC</th><th class="num">Reun.</th><th class="num">% Reu</th><th class="num">Cierre</th></tr>';
  const TH_CT = '<tr><th>#</th><th>Contenido</th><th>Fuente</th><th class="num">Leads</th>'
    + '<th class="num">PC</th><th class="num">Reun.</th><th class="num">Cierre</th></tr>';

  function lst(rows, fn, cols) { return (rows && rows.length) ? rows.map(fn).join('') : emptyRow(cols); }

  // ---------- RENDER ----------
  function render(d) {
    const p = d.periodos;
    const fa = p.fim_atual, hoje = p.hoje;
    const semDiv = Math.max(1, p.semanas_decorridas_ytd);
    const pn = p.periodo_nome || 'Semana';
    const faY = new Date(fa + 'T00:00:00');
    const mtdFimD = new Date(p.mtd_fim + 'T00:00:00');
    const mtdIniD = new Date(p.mtd_ini + 'T00:00:00');
    const iniAtualD = new Date(p.ini_atual + 'T00:00:00');

    const header = '<div class="top"><div class="chip">Content Marketing · Buzzmonitor LATAM</div>'
      + '<h1>Resultados Content Marketing</h1><div class="sub">Dashboard · selector de período · LATAM</div>'
      + '<div class="meta">'
      + `<div class="item"><span class="lbl">Período</span><span class="val">${fLarga(p.ini_atual)} → ${fLarga(fa)} · ${faY.getFullYear()}</span></div>`
      + `<div class="item"><span class="lbl">vs. período anterior</span><span class="val">${fmtFecha(p.ini_ant)} → ${fmtFecha(p.fim_ant)}</span></div>`
      + `<div class="item"><span class="lbl"><span class="no-upper">MtD</span> · Mes actual</span><span class="val">${String(mtdIniD.getDate()).padStart(2, '0')} → ${String(mtdFimD.getDate()).padStart(2, '0')} ${MESES_C[mtdFimD.getMonth()]} ${faY.getFullYear()}</span></div>`
      + `<div class="item"><span class="lbl"><span class="no-upper">YtD</span> · Acumulado del año</span><span class="val">Ene → ${MESES_C[faY.getMonth()]} ${faY.getFullYear()} (${semDiv} semanas)</span></div>`
      + `<div class="item"><span class="lbl">Generado el</span><span class="val">${String(new Date(hoje + 'T00:00:00').getDate()).padStart(2, '0')} ${MESES_C[new Date(hoje + 'T00:00:00').getMonth()]} ${new Date(hoje + 'T00:00:00').getFullYear()}</span></div>`
      + '</div>'
      + '<div class="sources"><b>Fuentes:</b> Supabase (deals_latam_*_staging) · UTM tracking + dominio de contenido getbuzzmonitor.com · '
      + 'filtro Content Marketing (ver MAPEAMENTO-CAMPOS-latam.md). Moneda: USD.</div></div>';

    const tagSem = `${String(iniAtualD.getDate()).padStart(2, '0')}–${String(faY.getDate()).padStart(2, '0')} ${MESES_C[faY.getMonth()]} ${faY.getFullYear()}`;
    const bloco1 = '<section><div class="section-head"><div class="icon">1</div>'
      + `<h2>Visión General · ${pn}</h2><span class="tag">${tagSem}</span></div>`
      + kpiRow(d.semana, d.sem_ant, d.ytd, semDiv)
      + '<div class="sub-head">Acumulado <span class="no-upper">MtD</span></div>'
      + kpiRow(d.mtd)
      + '<div class="sub-head">Acumulado <span class="no-upper">YtD</span></div>'
      + kpiRow(d.ytd)
      + '</section>';

    function lossItem(lbl, k, periodo) {
      const perd = k.perd, leads = k.leads;
      const pct = leads ? Math.round(100 * perd / leads) : 0;
      return `<div class="loss-item"><div class="label">% Perdidos · ${lbl}</div>`
        + `<div class="pct">${pct}%</div>`
        + `<div class="abs">${perd} perdidos · ${leads} leads · ${periodo}</div>`
        + `<div class="bar"><span style="width:${Math.min(pct, 100)}%"></span></div></div>`;
    }
    const perdRows = (d.perdidos_mtd.length ? d.perdidos_mtd.map(rowPerda).join('') : emptyRow(5));
    const bloco2 = '<section><div class="section-head"><div class="icon">2</div>'
      + '<h2>Pérdidas · Período / MtD / YtD</h2><span class="tag">status = Perdido</span></div>'
      + '<div class="loss-panel">'
      + lossItem(pn, d.semana, `${String(iniAtualD.getDate()).padStart(2, '0')}–${String(faY.getDate()).padStart(2, '0')} ${MESES_C[faY.getMonth()]}`)
      + lossItem('<span class="no-upper">MtD</span>', d.mtd, `${String(mtdIniD.getDate()).padStart(2, '0')}–${String(mtdFimD.getDate()).padStart(2, '0')} ${MESES_C[mtdFimD.getMonth()]}`)
      + lossItem('<span class="no-upper">YtD</span>', d.ytd, `Ene–${MESES_C[faY.getMonth()]}`)
      + '</div>'
      + toggle('Leads perdidos en el MtD · detalle', `${d.perdidos_mtd.length} deals`,
        '<tr><th>Deal</th><th>Fuente</th><th>Contenido</th><th>País</th><th>Fecha</th></tr>', perdRows)
      + '</section>';

    const bloco3 = '<section><div class="section-head"><div class="icon">3</div>'
      + '<h2>Listas de Acceso Rápido · Período</h2><span class="tag">drill-down del embudo</span></div>'
      + toggle('3.1 · Leads del período', `${d.leads_semana.length} deals`,
        '<tr><th>Deal</th><th>Fuente</th><th>Contenido</th><th>País</th><th>Fecha</th><th>Responsable</th></tr>',
        lst(d.leads_semana, rowLead, 6))
      + toggle('3.2 · Reuniones del período', `${d.reuniones_semana.length} deals`,
        '<tr><th>Deal</th><th>Responsable</th><th>Fuente</th><th>Contenido</th><th>País</th><th>Fecha</th></tr>',
        lst(d.reuniones_semana, rowReunion, 6))
      + toggle('3.3 · Cierres del período', `${d.cierres_semana.length} deals`,
        '<tr><th>Deal</th><th>Responsable</th><th>Fuente</th><th>País</th><th>Fecha</th><th class="num">Valor</th></tr>',
        lst(d.cierres_semana, rowCierre, 6))
      + '</section>';

    const perLbls = {
      semana: `${fmtFecha(p.ini_atual)}–${fmtFecha(fa)} ${faY.getFullYear()}`,
      sem_ant: `${fmtFecha(p.ini_ant)}–${fmtFecha(p.fim_ant)} ${faY.getFullYear()}`,
      mtd: `${fmtFecha(p.mtd_ini)}–${fmtFecha(p.mtd_fim)} ${faY.getFullYear()}`,
      ytd: `Ene–${MESES_C[faY.getMonth()]} ${faY.getFullYear()}`,
    };
    const titles = { semana: pn, sem_ant: 'Período Anterior', mtd: 'MtD', ytd: 'YtD' };
    const srcTbl = (key) => rkTable(titles[key], perLbls[key], TH_SRC, renderRankingSource(d['rk_src_' + key]));
    const ctTbl = (key) => rkTable(titles[key], perLbls[key], TH_CT, renderRankingContent(d['rk_ct_' + key], d.src_map));
    const bloco4 = '<section><div class="section-head"><div class="icon">4</div>'
      + '<h2>Detalle · Período / Período Anterior / MtD / YtD</h2>'
      + '<span class="tag">% PC = PC/Leads · % Reu = Reu/PC</span></div>'
      + '<div class="sub-head">4.a · Ranking de Fuentes</div>'
      + `<div class="two-col">${srcTbl('semana')}${srcTbl('sem_ant')}</div>`
      + `<div class="two-col">${srcTbl('mtd')}${srcTbl('ytd')}</div>`
      + '<div class="sub-head">4.b · Ranking de Contenido (UTM Content)</div>'
      + `<div class="two-col">${ctTbl('semana')}${ctTbl('sem_ant')}</div>`
      + `<div class="two-col">${ctTbl('mtd')}${ctTbl('ytd')}</div>`
      + '</section>';

    const bloco5 = '<section><div class="section-head"><div class="icon">5</div>'
      + '<h2>Tendencias · Últimos 12 meses</h2><span class="tag">52 semanas</span></div>'
      + '<div class="chart-wrap"><div class="chart-head">'
      + '<h3>Serie temporal semanal · Embudo + Tx Primer contacto</h3>'
      + '<span class="ctx">52 semanas · clic en la leyenda para ocultar series</span></div>'
      + '<div class="chart-canvas"><canvas id="chartTimeseries"></canvas></div></div>'
      + '<div class="chart-wrap"><div class="chart-head">'
      + '<h3>Primer contacto y Reuniones por fuente · 12 meses</h3>'
      + '<span class="ctx">PC = Primer contacto · Reu = Reuniones</span></div>'
      + '<div class="chart-canvas chart-canvas-tall"><canvas id="chartSourceShare"></canvas></div></div>'
      + '</section>';

    const nota = '<div class="sources" style="margin-top:18px">⚠️ <b>Datos sobre tablas staging.</b> '
      + 'Solo se sincronizan los pipelines <b>Inbound</b> y <b>Outbound</b> Latam: los leads marcados como Perdidos '
      + 'y movidos al pipeline <b>Nutrición</b> salen del conjunto → <b>Leads y Perdidos quedan subestimados</b>. '
      + 'La atribución de canal tampoco cubre todos los leads (UTM vacío en inbound). Los cierres incluyen negocios '
      + 'con pago, contrato o fecha de cierre reales; el valor usa el campo <b>value</b> (USD). Valores y fechas de '
      + 'cierre son aproximados, pendientes de validación con el equipo LATAM.</div>';

    const footer = '<footer><b>Dashboard de Content Marketing · datos reales de Supabase (filtro CM)</b><br>'
      + `${pn} ${fmtFecha(p.ini_atual)}-${fmtFecha(fa)} ${faY.getFullYear()} · `
      + `MtD ${fmtFecha(p.mtd_ini)}-${fmtFecha(p.mtd_fim)} · YtD Ene-${MESES_C[faY.getMonth()]} ${faY.getFullYear()}<br>`
      + 'Reuniones y Cierres contabilizados por fecha del evento · Buzzmonitor LATAM · uso interno</footer>';

    return header + bloco1 + bloco2 + bloco3 + bloco4 + bloco5 + nota + footer;
  }

  // ---------- CHARTS ----------
  let _charts = { ts: null, ss: null };
  function montarCharts(d) {
    if (typeof Chart === 'undefined') return;
    const s = d.serie;
    const leads = s.leads, pc = s.pc, reunion = s.reunion, cierres = s.cierres;
    const txPC = leads.map((l, i) => l ? Math.round((pc[i] / l) * 100) : 0);

    if (_charts.ts) _charts.ts.destroy();
    _charts.ts = new Chart(document.getElementById('chartTimeseries').getContext('2d'), {
      type: 'line',
      data: {
        labels: s.labels, datasets: [
          { label: 'Leads', data: leads, borderColor: '#1F2937', borderWidth: 2.6, tension: .35, pointRadius: 0, pointHoverRadius: 5, yAxisID: 'y' },
          { label: 'Primer contacto', data: pc, borderColor: '#0B63FF', borderWidth: 2.2, tension: .35, pointRadius: 0, pointHoverRadius: 5, yAxisID: 'y' },
          { label: 'Tx Primer contacto (%)', data: txPC, borderColor: '#6EA7FF', borderWidth: 2, borderDash: [6, 3], tension: .35, pointRadius: 0, yAxisID: 'yPct' },
          { label: 'Reuniones', data: reunion, borderColor: '#6B7280', borderWidth: 1.8, borderDash: [3, 3], tension: .35, pointRadius: 0, yAxisID: 'y' },
          { label: 'Cierres', data: cierres, borderColor: '#16A34A', backgroundColor: 'rgba(22,163,74,0.1)', borderWidth: 2.5, tension: .2, pointRadius: 3, pointHoverRadius: 5, yAxisID: 'y' },
        ],
      },
      options: {
        responsive: true, maintainAspectRatio: false, interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { position: 'top', align: 'end', labels: { font: { family: 'Inter', size: 13 }, color: '#374151', usePointStyle: true, pointStyle: 'rectRounded', padding: 16 } },
          tooltip: { backgroundColor: '#1F2937', padding: 12, cornerRadius: 8, callbacks: { label: (c) => c.dataset.yAxisID === 'yPct' ? `${c.dataset.label}: ${c.parsed.y}%` : `${c.dataset.label}: ${c.parsed.y}` } },
        },
        scales: {
          x: { ticks: { font: { family: 'Inter', size: 11 }, color: '#6B7280', maxRotation: 0, autoSkip: true, maxTicksLimit: 13 }, grid: { display: false } },
          y: { type: 'linear', position: 'left', beginAtZero: true, title: { display: true, text: 'Volúmenes (Leads · PC · Reu · Cierres)', font: { family: 'Inter', size: 12, weight: '600' }, color: '#4B5563' }, ticks: { font: { family: 'Inter', size: 12 }, color: '#6B7280' }, grid: { color: '#F1F5F9' } },
          yPct: { type: 'linear', position: 'right', beginAtZero: true, max: 100, title: { display: true, text: 'Tx Primer contacto (%)', font: { family: 'Inter', size: 12, weight: '600' }, color: '#0B63FF' }, ticks: { callback: (v) => v + '%', font: { family: 'Inter', size: 12 }, color: '#0B63FF' }, grid: { display: false } },
        },
      },
    });

    if (_charts.ss) _charts.ss.destroy();
    _charts.ss = new Chart(document.getElementById('chartSourceShare').getContext('2d'), {
      type: 'bar',
      data: {
        labels: ['Primer contacto (12m)', 'Reuniones (12m)'],
        datasets: (d.proporcao || []).map((x) => ({ label: x.label, data: [x.PC, x.RE], backgroundColor: x.color, borderWidth: 0, borderRadius: 4, barPercentage: 0.7, categoryPercentage: 0.7 })),
      },
      options: {
        indexAxis: 'y', responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', align: 'start', labels: { font: { family: 'Inter', size: 12 }, color: '#374151', usePointStyle: true, pointStyle: 'rectRounded', padding: 14, boxWidth: 14 } },
          tooltip: { backgroundColor: '#1F2937', padding: 12, cornerRadius: 8, callbacks: { label: (c) => { const t = c.chart.data.datasets.reduce((s2, ds) => s2 + ds.data[c.dataIndex], 0); const v = c.parsed.x; return `${c.dataset.label}: ${v} (${t ? ((v / t) * 100).toFixed(1) : 0}%)`; } } },
        },
        scales: {
          x: { stacked: true, beginAtZero: true, ticks: { font: { family: 'Inter', size: 12 }, color: '#6B7280' }, grid: { color: '#F1F5F9' } },
          y: { stacked: true, ticks: { font: { family: 'Inter', size: 13, weight: '600' }, color: '#374151' }, grid: { display: false } },
        },
      },
    });
  }

  // ---------- SORTABLE ----------
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
        const num = (str) => { const m = (str || '').match(/-?[\d.,]+/); return m ? parseFloat(m[0].replace(/\./g, '').replace(',', '.')) : NaN; };
        rows.sort((a, b) => {
          const sa = (a.children[idx]?.innerText || '').trim(), sb = (b.children[idx]?.innerText || '').trim();
          const na = num(sa), nb = num(sb); let c;
          if (!isNaN(na) && !isNaN(nb)) c = na - nb; else c = sa.localeCompare(sb, 'es', { numeric: true, sensitivity: 'base' });
          return dir === 'asc' ? c : -c;
        });
        rows.forEach((r) => tbody.appendChild(r));
      });
    });
    table.dataset.sortable = '1';
  }

  return { render: render, montarCharts: montarCharts, makeSortable: makeSortable };
});
